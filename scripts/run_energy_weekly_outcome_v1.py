#!/usr/bin/env python3
"""
ENERGY-WEEKLY-OUTCOME-008
Strict prospective maturation of 005 events under the 004 WTI outcome convention.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
P5=ROOT/"results"/"energy_weekly_prospective_v1"
REG=P5/"PROSPECTIVE_EVENT_REGISTRY.csv"
CHAIN=P5/"EVENT_CHAIN.csv"
INTEGRITY=P5/"REGISTRY_INTEGRITY.json"
OUT=ROOT/"results"/"energy_weekly_outcome_v1"
OUT.mkdir(parents=True,exist_ok=True)

AUDIT=OUT/"OUTCOME_AUDIT.csv"
AUDIT_INTEGRITY=OUT/"OUTCOME_AUDIT_INTEGRITY.json"

REG_COLS=[
    "event_id","week_end","release_date","price_asof_date",
    "registered_utc","upstream_selected_sha256",
    "pressure_score","pressure_q90_prior",
    "WTI_r5","GAS_r5","HEAT_r5","JET_r5",
    "inventory_improving_count","demand_weak_count","throughput_weak",
    "upstream_supply_up_count","mechanism_class","interpretation_state",
    "historical_same_class_completed_n",
    "historical_same_class_median_wti_8w",
    "historical_same_class_median_wti_13w",
    "historical_same_class_median_short_mae_8w",
    "historical_same_class_median_short_mae_13w",
    "realized_wti_4w","realized_short_mae_4w","realized_short_mfe_4w",
    "realized_wti_8w","realized_short_mae_8w","realized_short_mfe_8w",
    "realized_wti_13w","realized_short_mae_13w","realized_short_mfe_13w",
    "realization_status"
]
IMMUTABLE_COLS=REG_COLS[:23]
CHAIN_COLS=["sequence","event_id","previous_hash","row_hash"]
EVENT_GENESIS=hashlib.sha256(b"ENERGY_WEEKLY_PROSPECTIVE_005_GENESIS_V1").hexdigest()

AUDIT_COLS=[
    "sequence","event_id","horizon","realized_utc",
    "execution_date","execution_wti","endpoint_date","endpoint_wti",
    "wti_source_sha256","endpoint_return","short_mae","short_mfe",
    "previous_hash","row_hash"
]
AUDIT_GENESIS=hashlib.sha256(b"ENERGY_WEEKLY_OUTCOME_008_GENESIS_V1").hexdigest()
HORIZONS={"4W":20,"8W":40,"13W":65}

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

STATE004=load_module(ROOT/"scripts"/"run_energy_weekly_state_v1.py","energy_state004_for_outcome008")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_registry():
    with REG.open("r",encoding="utf-8",newline="") as f:
        r=csv.DictReader(f)
        if r.fieldnames!=REG_COLS:
            raise RuntimeError("prospective registry schema mismatch")
        return list(r)

def read_chain():
    with CHAIN.open("r",encoding="utf-8",newline="") as f:
        r=csv.DictReader(f)
        if r.fieldnames!=CHAIN_COLS:
            raise RuntimeError("prospective event chain schema mismatch")
        return list(r)

def immutable_payload(row):
    return json.dumps([row.get(c,"") for c in IMMUTABLE_COLS],separators=(",",":"),ensure_ascii=False)

def event_row_hash(prev,row):
    return hashlib.sha256((prev+"|"+immutable_payload(row)).encode("utf-8")).hexdigest()

def verify_event_chain(reg,chain):
    if len(reg)!=len(chain):
        raise RuntimeError("prospective registry/chain length mismatch")
    prev=EVENT_GENESIS
    for i,(row,link) in enumerate(zip(reg,chain),start=1):
        if int(link["sequence"])!=i or link["event_id"]!=row["event_id"]:
            raise RuntimeError("prospective event chain identity mismatch")
        if link["previous_hash"]!=prev:
            raise RuntimeError("prospective event chain previous hash mismatch")
        h=event_row_hash(prev,row)
        if link["row_hash"]!=h:
            raise RuntimeError("prospective event immutable hash mismatch")
        prev=h
    return prev

def ensure_audit():
    if not AUDIT.exists():
        with AUDIT.open("w",encoding="utf-8",newline="") as f:
            csv.writer(f).writerow(AUDIT_COLS)

def read_audit():
    ensure_audit()
    with AUDIT.open("r",encoding="utf-8",newline="") as f:
        r=csv.DictReader(f)
        if r.fieldnames!=AUDIT_COLS:
            raise RuntimeError("outcome audit schema mismatch")
        return list(r)

def audit_payload(row):
    core=[
        row["sequence"],row["event_id"],row["horizon"],row["realized_utc"],
        row["execution_date"],row["execution_wti"],row["endpoint_date"],row["endpoint_wti"],
        row["wti_source_sha256"],row["endpoint_return"],row["short_mae"],row["short_mfe"],
    ]
    return json.dumps(core,separators=(",",":"),ensure_ascii=False)

def audit_hash(prev,row):
    return hashlib.sha256((prev+"|"+audit_payload(row)).encode("utf-8")).hexdigest()

def verify_audit(rows):
    prev=AUDIT_GENESIS
    keys=set()
    for i,row in enumerate(rows,start=1):
        if int(row["sequence"])!=i:
            raise RuntimeError("outcome audit sequence mismatch")
        key=(row["event_id"],row["horizon"])
        if key in keys:
            raise RuntimeError("duplicate event-horizon in outcome audit")
        keys.add(key)
        if row["previous_hash"]!=prev:
            raise RuntimeError("outcome audit previous hash mismatch")
        if row["row_hash"]!=audit_hash(prev,row):
            raise RuntimeError("outcome audit row hash mismatch")
        prev=row["row_hash"]; keys.add(key)
    return prev,keys

def write_registry(rows):
    tmp=REG.with_suffix(".tmp")
    with tmp.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=REG_COLS)
        w.writeheader(); w.writerows(rows)
    tmp.replace(REG)

def status_from_row(row):
    if str(row["realized_wti_13w"]).strip()!="":
        return "REALIZED_13W_COMPLETE"
    if str(row["realized_wti_8w"]).strip()!="":
        return "REALIZED_8W"
    if str(row["realized_wti_4w"]).strip()!="":
        return "REALIZED_4W"
    return "UNREALIZED"

def main():
    reg=read_registry()
    chain=read_chain()
    chain_tail=verify_event_chain(reg,chain)
    immutable_before=[immutable_payload(x) for x in reg]

    audit_before=read_audit()
    audit_tail,existing_keys=verify_audit(audit_before)

    # Same official WTI acquisition path as 004.
    daily,prov=STATE004.build_daily_panel()
    wti_source_row=prov.loc[prov["name"]=="WTI"].iloc[0]
    wti_sha=str(wti_source_row["sha256"])

    newly=[]
    now=datetime.now(timezone.utc).isoformat()
    audit_rows=list(audit_before)

    for row in reg:
        release=pd.Timestamp(row["release_date"]).normalize()
        x=daily[daily.date>release][["date","WTI"]].dropna().reset_index(drop=True)
        if x.empty:
            continue
        execution_date=pd.Timestamp(x.iloc[0].date).normalize()
        if execution_date<=release:
            raise RuntimeError("execution timing violation")
        p0=float(x.iloc[0].WTI)

        for horizon,nobs in HORIZONS.items():
            key=(row["event_id"],horizon)
            registry_field=f"realized_wti_{horizon.lower()}"
            mae_field=f"realized_short_mae_{horizon.lower()}"
            mfe_field=f"realized_short_mfe_{horizon.lower()}"

            already=str(row[registry_field]).strip()!=""
            if key in existing_keys:
                if not already:
                    raise RuntimeError("audit says realized but registry field is blank")
                continue
            if already:
                raise RuntimeError("registry has realized horizon missing from audit")

            if len(x)<=nobs:
                continue

            path=x.iloc[:nobs+1].copy()
            rel=path.WTI.astype(float)/p0-1.0
            endpoint_date=pd.Timestamp(path.iloc[-1].date).normalize()
            endpoint_wti=float(path.iloc[-1].WTI)
            if endpoint_date<=execution_date:
                raise RuntimeError("endpoint timing violation")

            endpoint=float(rel.iloc[-1])
            mae=float(rel.max())
            mfe=float(-rel.min())

            new={
                "sequence":str(len(audit_rows)+1),
                "event_id":row["event_id"],
                "horizon":horizon,
                "realized_utc":now,
                "execution_date":execution_date.date().isoformat(),
                "execution_wti":repr(p0),
                "endpoint_date":endpoint_date.date().isoformat(),
                "endpoint_wti":repr(endpoint_wti),
                "wti_source_sha256":wti_sha,
                "endpoint_return":repr(endpoint),
                "short_mae":repr(mae),
                "short_mfe":repr(mfe),
                "previous_hash":audit_tail,
                "row_hash":"",
            }
            new["row_hash"]=audit_hash(audit_tail,new)
            audit_tail=new["row_hash"]
            audit_rows.append(new)
            existing_keys.add(key)

            row[registry_field]=repr(endpoint)
            row[mae_field]=repr(mae)
            row[mfe_field]=repr(mfe)
            newly.append(f"{row['event_id']}:{horizon}")

        row["realization_status"]=status_from_row(row)

    if [immutable_payload(x) for x in reg]!=immutable_before:
        raise RuntimeError("immutable prospective event snapshot changed")

    # Enforce no early settlement for first live event.
    first=next((r for r in reg if r["event_id"]=="ENERGY005_2026-09-23"),None)
    if first is None:
        raise RuntimeError("first live event missing")

    write_registry(reg)

    with AUDIT.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=AUDIT_COLS)
        w.writeheader(); w.writerows(audit_rows)

    # Reverify persisted representations.
    reg2=read_registry()
    if [immutable_payload(x) for x in reg2]!=immutable_before:
        raise RuntimeError("persisted immutable snapshot changed")
    audit2=read_audit()
    persisted_audit_tail,_=verify_audit(audit2)

    integrity=json.loads(INTEGRITY.read_text(encoding="utf-8"))
    if integrity.get("tail_hash")!=chain_tail:
        raise RuntimeError("stored prospective immutable tail hash mismatch")
    integrity.update({
        "registry_sha256":sha(REG),
        "registry_rows":len(reg2),
        "chain_rows":len(chain),
        "tail_hash":chain_tail,
        "realized_horizon_count":len(audit2),
        "last_outcome_maturation_utc":now,
    })
    INTEGRITY.write_text(json.dumps(integrity,indent=2)+"\n",encoding="utf-8")

    ai={
        "schema_version":"ENERGY_WEEKLY_OUTCOME_008_V1",
        "audit_sha256":sha(AUDIT),
        "audit_rows":len(audit2),
        "genesis_hash":AUDIT_GENESIS,
        "tail_hash":persisted_audit_tail,
    }
    AUDIT_INTEGRITY.write_text(json.dumps(ai,indent=2)+"\n",encoding="utf-8")

    # Current 2026-09-24 expected no-early-settlement check is generalized:
    # if fewer than 21 WTI observations exist, 4W must remain blank.
    release=pd.Timestamp(first["release_date"]).normalize()
    xfirst=daily[daily.date>release][["date","WTI"]].dropna().reset_index(drop=True)
    early_violation=bool(len(xfirst)<=20 and str(first["realized_wti_4w"]).strip()!="")

    q={
        "qc_gate":"FAIL" if early_violation else "PASS",
        "module":"ENERGY-WEEKLY-OUTCOME-008",
        "prospective_registry_rows":len(reg2),
        "immutable_event_chain_verified":True,
        "immutable_event_chain_tail":chain_tail,
        "wti_source_sha256":wti_sha,
        "first_event_post_release_wti_observations":int(len(xfirst)),
        "newly_realized_horizons":newly,
        "newly_realized_horizon_count":len(newly),
        "outcome_audit_rows":len(audit2),
        "first_event_status":first["realization_status"],
        "early_settlement_violation":early_violation,
        "model_fitted":False,
        "thresholds_retuned":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(q,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-WEEKLY-OUTCOME-008 — Prospective Outcome Maturation",
        "",
        "**STRICT OBSERVATION-COUNT MATURATION / IMMUTABLE EVENT STATE**",
        "",
        f"- QC: **{q['qc_gate']}**",
        f"- first event post-release WTI observations: {len(xfirst)}",
        f"- newly realized horizons: {', '.join(newly) if newly else 'none'}",
        f"- outcome audit rows: {len(audit2)}",
        f"- first event status: **{first['realization_status']}**",
        "",
        "No horizon is populated until its exact frozen WTI observation count is available.",
        "Registration-state fields remain protected by the original 005 immutable hash chain.",
    ]
    (OUT/"ENERGY_WEEKLY_OUTCOME_008_STATUS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if q["qc_gate"]!="PASS":
        raise SystemExit("ENERGY-WEEKLY-OUTCOME-008 QC failed")
    print(json.dumps(q,indent=2))

if __name__=="__main__":
    main()
