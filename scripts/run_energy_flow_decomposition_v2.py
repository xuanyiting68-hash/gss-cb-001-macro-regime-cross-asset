#!/usr/bin/env python3
"""
ENERGY-FLOW-002
Post-falsification stock-flow mechanism decomposition.

Descriptive / hypothesis-generating only.
No new confirmatory p-value family is created.
"""
from __future__ import annotations

import hashlib
import io
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
PHYS=ROOT/"results"/"energy_physical_wf_v1_1"/"PHYSICAL_EVENT_PANEL.csv"
OUT=ROOT/"results"/"energy_flow_v2"
OUT.mkdir(parents=True,exist_ok=True)

SERIES={
    "GAS_DEMAND":{"id":"WGFUPUS2","title":"Weekly U.S. Product Supplied of Finished Motor Gasoline","unit":"Thousand Barrels per Day"},
    "DIST_DEMAND":{"id":"WDIUPUS2","title":"Weekly U.S. Product Supplied of Distillate Fuel Oil","unit":"Thousand Barrels per Day"},
    "JET_DEMAND":{"id":"WKJUPUS2","title":"Weekly U.S. Product Supplied of Kerosene-Type Jet Fuel","unit":"Thousand Barrels per Day"},
    "REFINERY_INPUT":{"id":"WCRRIUS2","title":"Weekly U.S. Refiner Net Input of Crude Oil","unit":"Thousand Barrels per Day"},
    "FIELD_PROD":{"id":"WCRFPUS2","title":"Weekly U.S. Field Production of Crude Oil","unit":"Thousand Barrels per Day"},
    "CRUDE_IMPORTS":{"id":"WCRIMUS2","title":"Weekly U.S. Imports of Crude Oil","unit":"Thousand Barrels per Day"},
}

def get_bytes(url,timeout=60,attempts=3):
    last=None
    for i in range(attempts):
        try:
            req=Request(url,headers={"User-Agent":"Mozilla/5.0 gss-cb-001-public-research/1.0"})
            with urlopen(req,timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last=exc
            time.sleep(2*(i+1))
    raise RuntimeError(f"fetch failed {url}: {last!r}")

def parse_eia_xls(series_id):
    url=f"https://www.eia.gov/dnav/pet/hist_xls/{series_id}w.xls"
    raw=get_bytes(url)
    book=pd.ExcelFile(io.BytesIO(raw),engine="xlrd")
    parsed=None
    for sheet in book.sheet_names:
        x=pd.read_excel(io.BytesIO(raw),sheet_name=sheet,header=None,engine="xlrd")
        for ridx in range(min(20,len(x))):
            vals=[str(v).strip() if pd.notna(v) else "" for v in x.iloc[ridx].tolist()]
            if "Date" not in vals:
                continue
            dcol=vals.index("Date")
            vcol=None
            for j in range(dcol+1,len(vals)):
                if vals[j] not in ("","nan","NaN"):
                    vcol=j;break
            if vcol is None:
                vcol=dcol+1
            z=x.iloc[ridx+1:,[dcol,vcol]].copy()
            z.columns=["week_end","value"]
            z["week_end"]=pd.to_datetime(z["week_end"],errors="coerce")
            z["value"]=pd.to_numeric(z["value"],errors="coerce")
            z=z.dropna(subset=["week_end","value"]).sort_values("week_end")
            if len(z)>100:
                parsed=z.reset_index(drop=True);break
        if parsed is not None:
            break
    if parsed is None:
        raise RuntimeError(f"could not parse {series_id}")
    meta={
        "series_id":series_id,
        "download_url":url,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "rows":int(len(parsed)),
        "first_date":str(parsed.week_end.min().date()),
        "last_date":str(parsed.week_end.max().date()),
        "retrieved_utc":datetime.now(timezone.utc).isoformat(),
        "acquisition_method":"EIA_HIST_XLS",
    }
    return parsed,meta

def prior_seasonal_values(df,asof_date):
    d=pd.Timestamp(asof_date)
    target=int(d.isocalendar().week)
    vals=[]
    for y in range(d.year-5,d.year):
        z=df[df.week_end.dt.year==y].copy()
        if z.empty: continue
        z["iso_week"]=z.week_end.dt.isocalendar().week.astype(int)
        dist=(z.iso_week-target).abs()
        dist=np.minimum(dist,53-dist)
        zz=z.loc[dist<=1,"value"].dropna()
        if len(zz): vals.append(float(zz.mean()))
    return vals

def seasonal_gap(df,week_end):
    row=df.loc[df.week_end==pd.Timestamp(week_end),"value"]
    if row.empty:
        return np.nan,np.nan,0
    v=float(row.iloc[-1])
    vals=prior_seasonal_values(df,week_end)
    if len(vals)<3:
        return v,np.nan,len(vals)
    ref=float(np.mean(vals))
    return v,(v-ref)/ref,len(vals)

def main():
    if not PHYS.exists():
        raise SystemExit("physical event panel missing")
    ev=pd.read_csv(PHYS,parse_dates=[
        "s3_date","price_anchor_month","baseline_week_end","decision_week_end",
        "baseline_release_date","decision_date","exec_date"
    ])

    data={}
    meta=[]
    for name,s in SERIES.items():
        z,m=parse_eia_xls(s["id"])
        data[name]=z
        meta.append({"name":name,"title":s["title"],"unit":s["unit"],**m})

    rows=[]
    for _,r in ev.iterrows():
        row={
            "s3_date":r.s3_date,
            "price_anchor_month":r.price_anchor_month,
            "price_layer_classification":r.price_layer_classification,
            "strict_pit":r.strict_pit,
            "baseline_release_date":r.baseline_release_date,
            "decision_date":r.decision_date,
            "baseline_week_end":r.baseline_week_end,
            "decision_week_end":r.decision_week_end,
            "inventory_improving_count":r.get("inventory_improving_count",np.nan),
            "wti_fwd_3m":r.get("wti_fwd_3m",np.nan),
            "wti_fwd_6m":r.get("wti_fwd_6m",np.nan),
            "short_mae_3m":r.get("short_mae_3m",np.nan),
            "short_mae_6m":r.get("short_mae_6m",np.nan),
        }
        if r.strict_pit!="AVAILABLE":
            row["flow_data_complete"]=False
            row["flow_classification"]="STRICT_PIT_UNAVAILABLE"
            rows.append(row)
            continue

        complete=True
        delta={}
        for name,z in data.items():
            bv,bg,bn=seasonal_gap(z,r.baseline_week_end)
            dv,dg,dn=seasonal_gap(z,r.decision_week_end)
            if not (np.isfinite(bg) and np.isfinite(dg)):
                complete=False
            delta[name]=dg-bg if np.isfinite(bg) and np.isfinite(dg) else np.nan
            row.update({
                f"{name.lower()}_baseline":bv,
                f"{name.lower()}_decision":dv,
                f"{name.lower()}_gap_baseline":bg,
                f"{name.lower()}_gap_decision":dg,
                f"{name.lower()}_delta_gap":delta[name],
                f"{name.lower()}_prior_years_baseline":bn,
                f"{name.lower()}_prior_years_decision":dn,
            })

        demand_weak_count=sum(
            bool(np.isfinite(delta[k]) and delta[k]<0)
            for k in ["GAS_DEMAND","DIST_DEMAND","JET_DEMAND"]
        )
        throughput_weak=bool(np.isfinite(delta["REFINERY_INPUT"]) and delta["REFINERY_INPUT"]<0)
        upstream_supply_up_count=sum(
            bool(np.isfinite(delta[k]) and delta[k]>0)
            for k in ["FIELD_PROD","CRUDE_IMPORTS"]
        )

        row["flow_data_complete"]=complete
        row["demand_weak_count"]=demand_weak_count
        row["throughput_weak"]=throughput_weak
        row["upstream_supply_up_count"]=upstream_supply_up_count

        if r.price_layer_classification!="PRICE_PRODUCT_CONFIRMED":
            row["flow_classification"]="PRICE_FALSE_RELIEF_CONTEXT"
        elif not complete:
            row["flow_classification"]="FLOW_DATA_INCOMPLETE"
        else:
            dd=(demand_weak_count>=2 and throughput_weak)
            sn=(
                r.inventory_improving_count>=2
                and upstream_supply_up_count>=1
                and not throughput_weak
                and demand_weak_count<=1
            )
            if dd:
                row["flow_classification"]="FLOW_DD"
            elif sn:
                row["flow_classification"]="FLOW_SN"
            else:
                row["flow_classification"]="FLOW_MIXED"
        rows.append(row)

    out=pd.DataFrame(rows)
    source=pd.DataFrame(meta)

    pc=out[
        (out.strict_pit=="AVAILABLE")
        & (out.price_layer_classification=="PRICE_PRODUCT_CONFIRMED")
        & (out.flow_data_complete==True)
    ].copy()

    desc=[]
    for grp,g in pc.groupby("flow_classification"):
        for m in ["wti_fwd_3m","wti_fwd_6m","short_mae_3m","short_mae_6m"]:
            z=g[m].dropna()
            desc.append({
                "flow_classification":grp,
                "metric":m,
                "n":len(z),
                "mean":z.mean(),
                "median":z.median(),
                "negative_share":(z<0).mean() if m.startswith("wti_fwd") and len(z) else np.nan,
            })
    desc=pd.DataFrame(desc)

    qc={
        "events_total":int(len(out)),
        "strict_pit_available":int((out.strict_pit=="AVAILABLE").sum()),
        "price_confirmed_strict_pit_complete":int(len(pc)),
        "flow_dd":int((pc.flow_classification=="FLOW_DD").sum()) if len(pc) else 0,
        "flow_sn":int((pc.flow_classification=="FLOW_SN").sum()) if len(pc) else 0,
        "flow_mixed":int((pc.flow_classification=="FLOW_MIXED").sum()) if len(pc) else 0,
        "all_flow_series_loaded":bool(len(source)==len(SERIES)),
        "duplicate_s3_dates":int(out.s3_date.duplicated().sum()),
        "statistical_status":"DESCRIPTIVE_POST_LOCK_NO_NEW_PVALUE_FAMILY",
    }
    qc["qc_gate"]="PASS" if qc["all_flow_series_loaded"] and qc["duplicate_s3_dates"]==0 else "FAIL"

    source.to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)
    out.to_csv(OUT/"FLOW_EVENT_PANEL.csv",index=False)
    desc.to_csv(OUT/"FLOW_GROUP_DESCRIPTIVES.csv",index=False)
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2),encoding="utf-8")

    cols=[
        "s3_date","decision_date","price_layer_classification","flow_classification",
        "inventory_improving_count","demand_weak_count","throughput_weak",
        "upstream_supply_up_count","wti_fwd_3m","wti_fwd_6m",
        "short_mae_3m","short_mae_6m"
    ]
    lines=[
        "# ENERGY-FLOW-002 — First Stock–Flow Mechanism Map",
        "Date: 2026-09-24",
        "",
        "## Status",
        "",
        "**POST-v1.1 / DESCRIPTIVE / HYPOTHESIS-GENERATING / NOT DEPLOYABLE**",
        "",
        "No new confirmatory p-value family is created on the same six price-confirmed episodes.",
        "",
        "## QC and support",
        "",
        f"- Strict-PIT events: {qc['strict_pit_available']}",
        f"- Strict-PIT complete price-confirmed events: {qc['price_confirmed_strict_pit_complete']}",
        f"- FLOW_DD: {qc['flow_dd']}",
        f"- FLOW_SN: {qc['flow_sn']}",
        f"- FLOW_MIXED: {qc['flow_mixed']}",
        f"- QC gate: {qc['qc_gate']}",
        "",
        "## Price-confirmed mechanism map",
        "",
        pc[cols].sort_values("decision_date").to_markdown(index=False),
        "",
        "## Group descriptives",
        "",
        desc.to_markdown(index=False) if len(desc) else "No complete groups.",
        "",
        "## Interpretation boundary",
        "",
        "This module is a mechanism map, not a validated forecast.",
        "It was designed after observing the v1.1 stock-only falsification, so its first run cannot be treated as an independent confirmatory test.",
        "",
        "The purpose is to distinguish stock accumulation caused by different flow states before deciding whether an independently testable follow-up is warranted.",
    ]
    (OUT/"ENERGY_FLOW_002_REPORT.md").write_text("\n".join(lines),encoding="utf-8")

    if qc["qc_gate"]!="PASS":
        raise SystemExit("QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
