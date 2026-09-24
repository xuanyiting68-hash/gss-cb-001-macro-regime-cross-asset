#!/usr/bin/env python3
from __future__ import annotations
import hashlib, io, json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
PROS=ROOT/"results"/"energy_weekly_prospective_v1"/"PROSPECTIVE_EVENT_REGISTRY.csv"
OUT=ROOT/"results"/"energy_portwatch_v1"
OUT.mkdir(parents=True,exist_ok=True)

DAILY_BASE="https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query"
DISR_BASE="https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/portwatch_disruptions_database/FeatureServer/0/query"

CHOKEPOINTS={
 "chokepoint1":"Suez Canal",
 "chokepoint4":"Bab el-Mandeb Strait",
 "chokepoint6":"Strait of Hormuz",
 "chokepoint7":"Cape of Good Hope",
}
RELEVANT_RE=re.compile(r"hormuz|red sea|suez|bab\s+el[- ]?mandeb|mandeb",re.I)

def fetch_json(url,params):
    full=url+"?"+urlencode(params)
    req=Request(full,headers={"User-Agent":"Mozilla/5.0 gss-cb-001-public-research/1.0"})
    with urlopen(req,timeout=90) as r:
        raw=r.read()
    obj=json.loads(raw.decode("utf-8"))
    if "error" in obj:
        raise RuntimeError(obj["error"])
    return obj,raw,full

def features_to_df(obj):
    rows=[x.get("attributes",{}) for x in obj.get("features",[])]
    return pd.DataFrame(rows)

def fetch_chokepoint(pid):
    parts=[]; hashes=[]; urls=[]; offset=0
    while True:
        obj,raw,url=fetch_json(DAILY_BASE,{
            "where":f"portid='{pid}'",
            "outFields":"date,portid,portname,n_total,n_tanker,capacity_tanker,capacity",
            "orderByFields":"date ASC",
            "resultOffset":offset,
            "resultRecordCount":1000,
            "returnGeometry":"false",
            "f":"json",
        })
        z=features_to_df(obj)
        if z.empty: break
        parts.append(z); hashes.append(hashlib.sha256(raw).hexdigest()); urls.append(url)
        if len(z)<1000: break
        offset+=len(z)
    if not parts: raise RuntimeError(f"no PortWatch rows for {pid}")
    df=pd.concat(parts,ignore_index=True)
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    for c in ["n_total","n_tanker","capacity_tanker","capacity"]:
        df[c]=pd.to_numeric(df[c],errors="coerce")
    df=df.dropna(subset=["date"]).sort_values("date").drop_duplicates(["portid","date"],keep="last")
    return df,hashes,urls

def fetch_disruptions():
    obj,raw,url=fetch_json(DISR_BASE,{
        "where":"1=1",
        "outFields":"eventid,eventtype,eventname,htmlname,htmldescription,alertlevel,fromdate,todate,severitytext,pageid",
        "resultOffset":0,
        "resultRecordCount":2000,
        "returnGeometry":"false",
        "f":"json",
    })
    df=features_to_df(obj)
    for c in ["fromdate","todate"]:
        if c in df:
            # ArcGIS date may be epoch ms.
            vals=pd.to_numeric(df[c],errors="coerce")
            df[c]=pd.to_datetime(vals,unit="ms",utc=True,errors="coerce").dt.tz_convert(None)
    return df,hashlib.sha256(raw).hexdigest(),url

def metric_row(pid,name,df,now):
    latest=df.date.max()
    d=df[df.date<=latest].copy()
    last7=d.tail(7)
    prev90=d.iloc[max(0,len(d)-97):max(0,len(d)-7)]
    last30=d.tail(30)
    prevyr=d[d.date.dt.year==latest.year-1]

    def mean(x,c): return float(x[c].mean()) if len(x) and x[c].notna().any() else np.nan
    m={
        "portid":pid,"portname":name,
        "latest_settled_date":latest.date().isoformat(),
        "data_lag_days":int((now.normalize()-latest.normalize()).days),
        "rows":int(len(d)),
        "mean7_total":mean(last7,"n_total"),
        "mean7_tanker":mean(last7,"n_tanker"),
        "prior90_total":mean(prev90,"n_total"),
        "prior90_tanker":mean(prev90,"n_tanker"),
        "mean30_total":mean(last30,"n_total"),
        "mean30_tanker":mean(last30,"n_tanker"),
        "prior_year_total":mean(prevyr,"n_total"),
        "prior_year_tanker":mean(prevyr,"n_tanker"),
    }
    def ratio(a,b):
        return float(a/b) if np.isfinite(a) and np.isfinite(b) and b!=0 else np.nan
    m["ratio7_prior90_total"]=ratio(m["mean7_total"],m["prior90_total"])
    m["ratio7_prior90_tanker"]=ratio(m["mean7_tanker"],m["prior90_tanker"])
    m["ratio30_prioryear_total"]=ratio(m["mean30_total"],m["prior_year_total"])
    m["ratio30_prioryear_tanker"]=ratio(m["mean30_tanker"],m["prior_year_tanker"])
    m["acute_transit_stress"]=bool(
        (np.isfinite(m["ratio7_prior90_total"]) and m["ratio7_prior90_total"]<=0.50)
        or (np.isfinite(m["ratio7_prior90_tanker"]) and m["ratio7_prior90_tanker"]<=0.50)
    )
    m["structural_transit_stress"]=bool(
        (np.isfinite(m["ratio30_prioryear_total"]) and m["ratio30_prioryear_total"]<=0.60)
        or (np.isfinite(m["ratio30_prioryear_tanker"]) and m["ratio30_prioryear_tanker"]<=0.60)
    )
    m["rerouting_elevated"]=bool(
        pid=="chokepoint7" and np.isfinite(m["ratio7_prior90_total"]) and m["ratio7_prior90_total"]>=1.25
    )
    return m

def main():
    now=pd.Timestamp(datetime.now(timezone.utc)).tz_convert(None)
    reg=pd.read_csv(PROS)
    if len(reg)<1: raise RuntimeError("prospective energy registry empty")
    event=reg.loc[reg.event_id=="ENERGY005_2026-09-23"]
    if len(event)!=1: raise RuntimeError("required ENERGY005 event missing")
    ev=event.iloc[0]
    if ev["mechanism_class"]!="TIGHT_OR_MIXED" or ev["realization_status"]!="UNREALIZED":
        raise RuntimeError("prospective event state not eligible for PortWatch snapshot")

    rows=[]; source=[]
    for pid,name in CHOKEPOINTS.items():
        df,hashes,urls=fetch_chokepoint(pid)
        actual=set(df.portname.dropna().astype(str))
        if actual!={name}:
            raise RuntimeError(f"{pid} name mismatch: {actual} vs {name}")
        rows.append(metric_row(pid,name,df,now))
        source.append({
            "source_object":f"PortWatch daily {pid}",
            "url":DAILY_BASE,
            "raw_sha256_chain":";".join(hashes),
            "batches":len(hashes),
            "rows":len(df),
            "raw_committed":False,
        })

    metrics=pd.DataFrame(rows)

    dis,dh,du=fetch_disruptions()
    textcols=[c for c in ["eventname","htmlname","htmldescription","severitytext"] if c in dis.columns]
    blob=dis[textcols].fillna("").astype(str).agg(" ".join,axis=1)
    active=(dis["fromdate"].isna() | (dis["fromdate"]<=now)) & (dis["todate"].isna() | (dis["todate"]>=now))
    relevant=dis[active & blob.str.contains(RELEVANT_RE,na=False)].copy()

    source.append({
        "source_object":"PortWatch disruptions database",
        "url":DISR_BASE,
        "raw_sha256_chain":dh,
        "batches":1,
        "rows":len(dis),
        "raw_committed":False,
    })

    petroleum_ids={"chokepoint1","chokepoint4","chokepoint6"}
    stress=metrics[metrics.portid.isin(petroleum_ids)]
    traffic_context=bool((stress.acute_transit_stress | stress.structural_transit_stress).any())
    official_context=bool(len(relevant)>0)
    overall=bool(traffic_context or official_context)

    external=pd.DataFrame([{
        "event_id":ev["event_id"],
        "event_release_date":ev["release_date"],
        "snapshot_utc":datetime.now(timezone.utc).isoformat(),
        "mechanism_class":ev["mechanism_class"],
        "prospective_realization_status":ev["realization_status"],
        "official_active_relevant_disruptions":int(len(relevant)),
        "petroleum_chokepoint_traffic_stress":traffic_context,
        "cape_rerouting_elevated":bool(metrics.loc[metrics.portid=="chokepoint7","rerouting_elevated"].iloc[0]),
        "external_supply_shock_context_present":overall,
        "timing_status":"POST_EVENT_PRE_OUTCOME_RETRIEVAL_SNAPSHOT",
    }])

    maxlag=int(metrics.data_lag_days.max())
    minrows=int(metrics.rows.min())
    dup=0
    hard_fail=(
        len(dis)<100
        or minrows<2500
        or maxlag>14
        or len(metrics)!=4
        or ev["realization_status"]!="UNREALIZED"
    )

    qc={
        "qc_gate":"FAIL" if hard_fail else "PASS",
        "module":"ENERGY-PORTWATCH-006",
        "prospective_event_id":ev["event_id"],
        "prospective_event_realization_status":ev["realization_status"],
        "chokepoints_verified":int(len(metrics)),
        "minimum_daily_rows_per_chokepoint":minrows,
        "maximum_data_lag_days":maxlag,
        "disruption_database_rows":int(len(dis)),
        "active_relevant_disruptions":int(len(relevant)),
        "petroleum_chokepoint_traffic_stress":traffic_context,
        "external_supply_shock_context_present":overall,
        "historical_004_reclassified":False,
        "wti_outcomes_used_for_thresholds":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }

    metrics.to_csv(OUT/"CURRENT_CHOKEPOINT_SNAPSHOT.csv",index=False)
    cols=[c for c in ["eventid","eventtype","eventname","htmlname","alertlevel","fromdate","todate","severitytext","pageid"] if c in relevant.columns]
    relevant[cols].to_csv(OUT/"ACTIVE_RELEVANT_DISRUPTIONS.csv",index=False)
    external.to_csv(OUT/"EXTERNAL_CONTEXT_SNAPSHOT.csv",index=False)
    pd.DataFrame(source).to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,default=str)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-PORTWATCH-006 — Prospective External Maritime Context",
        "",
        "**PROSPECTIVE EXTERNAL CONTEXT / NO DIRECTIONAL OUTCOME CLAIM**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- event: {ev['event_id']}",
        f"- external supply-shock context present: **{overall}**",
        f"- active relevant PortWatch disruptions: {len(relevant)}",
        f"- petroleum chokepoint traffic-stress flag: {traffic_context}",
        f"- maximum PortWatch data lag: {maxlag} days",
        "",
        "## Chokepoint snapshot",
        "",
        metrics.to_markdown(index=False),
        "",
        "## Active relevant official disruptions",
        "",
        relevant[cols].to_markdown(index=False) if len(relevant) else "None matched.",
        "",
        "This snapshot is recorded after the event release but before any frozen 4W/8W/13W prospective outcome is observed.",
        "It is not used to retroactively relabel the historical 004 event panel.",
    ]
    (OUT/"ENERGY_PORTWATCH_006_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if hard_fail: raise SystemExit("ENERGY-PORTWATCH-006 QC failed")
    print(json.dumps(qc,indent=2,default=str))

if __name__=="__main__":
    main()
