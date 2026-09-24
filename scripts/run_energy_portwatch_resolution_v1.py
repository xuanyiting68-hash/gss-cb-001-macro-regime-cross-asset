#!/usr/bin/env python3
"""
ENERGY-PORTWATCH-RESOLUTION-010
Append-only external maritime shock-resolution state machine.
"""
from __future__ import annotations

import csv, hashlib, importlib.util, json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"energy_portwatch_resolution_v1"
OUT.mkdir(parents=True,exist_ok=True)

REG=OUT/"PORTWATCH_STATE_REGISTRY.csv"
INTEGRITY=OUT/"REGISTRY_INTEGRITY.json"

COLS=[
    "sequence","snapshot_utc","latest_settled_date",
    "active_relevant_red_disruptions","petroleum_traffic_stress",
    "hormuz_ratio7_prior90_total","hormuz_ratio7_prior90_tanker",
    "hormuz_ratio30_prioryear_total","hormuz_ratio30_prioryear_tanker",
    "state","clean_snapshot_streak","external_supply_shock_context_active",
    "traffic_source_hash_bundle","disruption_source_sha256",
    "disruption_state_hash","previous_hash","row_hash"
]
GENESIS=hashlib.sha256(b"ENERGY_PORTWATCH_RESOLUTION_010_GENESIS_V1").hexdigest()

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

PW=load_module(ROOT/"scripts"/"run_energy_portwatch_v1.py","portwatch006_for_resolution010")

def payload(row):
    return json.dumps([row.get(c,"") for c in COLS[:-2]],separators=(",",":"),ensure_ascii=False)

def rh(prev,row):
    return hashlib.sha256((prev+"|"+payload(row)).encode("utf-8")).hexdigest()

def ensure_reg():
    if not REG.exists():
        with REG.open("w",encoding="utf-8",newline="") as f:
            csv.writer(f).writerow(COLS)

def read_reg():
    ensure_reg()
    with REG.open("r",encoding="utf-8",newline="") as f:
        r=csv.DictReader(f)
        if r.fieldnames!=COLS: raise RuntimeError("010 registry schema mismatch")
        return list(r)

def verify(rows):
    prev=GENESIS
    for i,row in enumerate(rows,start=1):
        if int(row["sequence"])!=i: raise RuntimeError("010 sequence mismatch")
        if row["previous_hash"]!=prev: raise RuntimeError("010 previous hash mismatch")
        if row["row_hash"]!=rh(prev,row): raise RuntimeError("010 row hash mismatch")
        prev=row["row_hash"]
    return prev

def main():
    previous=read_reg()
    tail=verify(previous)
    now=pd.Timestamp(datetime.now(timezone.utc)).tz_convert(None)

    metrics=[]; traffic_hashes={}
    for pid,name in PW.CHOKEPOINTS.items():
        df,hashes,urls=PW.fetch_chokepoint(pid)
        actual=set(df.portname.dropna().astype(str))
        if actual!={name}: raise RuntimeError(f"{pid} name mismatch {actual}")
        metrics.append(PW.metric_row(pid,name,df,now))
        traffic_hashes[pid]=hashes
    metrics=pd.DataFrame(metrics)

    dis,dh,du=PW.fetch_disruptions()
    textcols=[c for c in ["eventname","htmlname","htmldescription","severitytext"] if c in dis.columns]
    blob=dis[textcols].fillna("").astype(str).agg(" ".join,axis=1)
    active=(dis["fromdate"].isna() | (dis["fromdate"]<=now)) & (dis["todate"].isna() | (dis["todate"]>=now))
    relevant=dis[active & blob.str.contains(PW.RELEVANT_RE,na=False)].copy()
    red=relevant[relevant["alertlevel"].fillna("").astype(str).str.upper()=="RED"].copy()

    petroleum=metrics[metrics.portid.isin({"chokepoint1","chokepoint4","chokepoint6"})]
    stress=bool((petroleum.acute_transit_stress | petroleum.structural_transit_stress).any())
    latest=pd.to_datetime(metrics.latest_settled_date).min().date().isoformat()
    hormuz=metrics.loc[metrics.portid=="chokepoint6"].iloc[0]

    disruption_state_payload=[]
    for _,r in red.sort_values(["eventid"]).iterrows():
        disruption_state_payload.append([
            str(r.get("eventid","")),str(r.get("eventname","")),str(r.get("alertlevel","")),
            str(r.get("fromdate","")),str(r.get("todate",""))
        ])
    disruption_state_hash=hashlib.sha256(
        json.dumps(disruption_state_payload,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    # Do not append an unchanged snapshot.
    if previous:
        last=previous[-1]
        unchanged=(
            last["latest_settled_date"]==latest
            and last["disruption_state_hash"]==disruption_state_hash
        )
        if unchanged:
            state=last["state"]
            q={
                "qc_gate":"PASS",
                "module":"ENERGY-PORTWATCH-RESOLUTION-010",
                "new_snapshot_appended":False,
                "registry_rows":len(previous),
                "current_state":state,
                "external_supply_shock_context_active":last["external_supply_shock_context_active"]=="True",
                "wti_outcomes_loaded":False,
                "deployment_status":"NOT_DEPLOYABLE",
            }
            (OUT/"QC.json").write_text(json.dumps(q,indent=2)+"\n",encoding="utf-8")
            (OUT/"ENERGY_PORTWATCH_RESOLUTION_010_STATUS.md").write_text(
                "# ENERGY-PORTWATCH-RESOLUTION-010\n\n"
                f"- QC: **PASS**\n- current state: **{state}**\n"
                "- new materially distinct snapshot: False\n",encoding="utf-8"
            )
            print(json.dumps(q,indent=2)); return

    clean=not stress and len(red)==0
    clean_streak=0

    if stress:
        state="CRITICAL_TRAFFIC_STRESS"
        clean_streak=0
    elif len(red)>0:
        state="TRAFFIC_RECOVERED_ALERT_ACTIVE"
        clean_streak=0
    else:
        # Clean snapshot. Resolution requires a prior clean snapshot at least 7d earlier.
        if previous:
            last=previous[-1]
            last_clean=last["state"] in {"RESOLUTION_CANDIDATE","RESOLVED"}
            gap=(pd.Timestamp(latest)-pd.Timestamp(last["latest_settled_date"])).days
            if last["state"]=="RESOLVED":
                state="RESOLVED"
                clean_streak=int(last["clean_snapshot_streak"])+1
            elif last_clean and gap>=7:
                state="RESOLVED"
                clean_streak=int(last["clean_snapshot_streak"])+1
            else:
                state="RESOLUTION_CANDIDATE"
                clean_streak=1
        else:
            state="RESOLUTION_CANDIDATE"
            clean_streak=1

    external=state!="RESOLVED"

    traffic_bundle=json.dumps(traffic_hashes,sort_keys=True,separators=(",",":"))
    row={
        "sequence":str(len(previous)+1),
        "snapshot_utc":datetime.now(timezone.utc).isoformat(),
        "latest_settled_date":latest,
        "active_relevant_red_disruptions":str(len(red)),
        "petroleum_traffic_stress":str(stress),
        "hormuz_ratio7_prior90_total":repr(float(hormuz.ratio7_prior90_total)),
        "hormuz_ratio7_prior90_tanker":repr(float(hormuz.ratio7_prior90_tanker)),
        "hormuz_ratio30_prioryear_total":repr(float(hormuz.ratio30_prioryear_total)),
        "hormuz_ratio30_prioryear_tanker":repr(float(hormuz.ratio30_prioryear_tanker)),
        "state":state,
        "clean_snapshot_streak":str(clean_streak),
        "external_supply_shock_context_active":str(external),
        "traffic_source_hash_bundle":traffic_bundle,
        "disruption_source_sha256":dh,
        "disruption_state_hash":disruption_state_hash,
        "previous_hash":tail,
        "row_hash":"",
    }
    row["row_hash"]=rh(tail,row)
    with REG.open("a",encoding="utf-8",newline="") as f:
        csv.DictWriter(f,fieldnames=COLS).writerow(row)

    final=read_reg()
    tail=verify(final)
    integrity={
        "schema_version":"ENERGY_PORTWATCH_RESOLUTION_010_V1",
        "registry_sha256":hashlib.sha256(REG.read_bytes()).hexdigest(),
        "registry_rows":len(final),
        "genesis_hash":GENESIS,
        "tail_hash":tail,
        "current_state":state,
        "external_supply_shock_context_active":external,
    }
    INTEGRITY.write_text(json.dumps(integrity,indent=2)+"\n",encoding="utf-8")

    expected_first_ok=True
    if len(final)==1:
        expected_first_ok=(
            state=="CRITICAL_TRAFFIC_STRESS"
            and external
            and stress
            and len(red)>=1
        )

    qc={
        "qc_gate":"PASS" if expected_first_ok else "FAIL",
        "module":"ENERGY-PORTWATCH-RESOLUTION-010",
        "new_snapshot_appended":True,
        "registry_rows":len(final),
        "latest_settled_date":latest,
        "active_relevant_red_disruptions":len(red),
        "petroleum_traffic_stress":stress,
        "current_state":state,
        "clean_snapshot_streak":clean_streak,
        "external_supply_shock_context_active":external,
        "first_snapshot_expected_state_pass":expected_first_ok,
        "wti_outcomes_loaded":False,
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-PORTWATCH-RESOLUTION-010 — External Shock State",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- latest settled date: {latest}",
        f"- active relevant RED disruptions: {len(red)}",
        f"- petroleum traffic stress: {stress}",
        f"- current state: **{state}**",
        f"- clean snapshot streak: {clean_streak}",
        f"- external supply-shock context active: **{external}**",
        "",
        "Resolution requires two clean snapshots at least seven days apart; one clean snapshot is only a candidate.",
    ]
    (OUT/"ENERGY_PORTWATCH_RESOLUTION_010_STATUS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if qc["qc_gate"]!="PASS": raise SystemExit("ENERGY-PORTWATCH-RESOLUTION-010 QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
