#!/usr/bin/env python3
"""
ENERGY-WEEKLY-PROSPECTIVE-005
Append-only prospective registry for still-unrealized ENERGY-WEEKLY-STATE-004 events.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/"results"/"energy_weekly_state_v1"
OUT=ROOT/"results"/"energy_weekly_prospective_v1"
OUT.mkdir(parents=True,exist_ok=True)

SELECTED=UP/"SELECTED_EVENT_PANEL.csv"
UP_QC=UP/"QC.json"

REG=OUT/"PROSPECTIVE_EVENT_REGISTRY.csv"
CHAIN=OUT/"EVENT_CHAIN.csv"
INTEGRITY=OUT/"REGISTRY_INTEGRITY.json"

OUTCOME_FIELDS=[
    "wti_fwd_4w","short_mae_4w","short_mfe_4w",
    "wti_fwd_8w","short_mae_8w","short_mfe_8w",
    "wti_fwd_13w","short_mae_13w","short_mfe_13w",
]

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
CHAIN_COLS=["sequence","event_id","previous_hash","row_hash"]
GENESIS=hashlib.sha256(b"ENERGY_WEEKLY_PROSPECTIVE_005_GENESIS_V1").hexdigest()

INTERPRETATION={
    "TIGHT_OR_MIXED":"ROLLOVER_WITHOUT_CLEAN_PHYSICAL_CONFIRMATION",
    "DEMAND_DESTRUCTION":"DEMAND_DESTRUCTION_CANDIDATE",
    "SUPPLY_NORMALIZATION":"SUPPLY_NORMALIZATION_CANDIDATE",
    "DATA_INCOMPLETE":"MECHANISM_DATA_INCOMPLETE",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ensure_files():
    if not REG.exists():
        with REG.open("w",encoding="utf-8",newline="") as f:
            csv.writer(f).writerow(REG_COLS)
    if not CHAIN.exists():
        with CHAIN.open("w",encoding="utf-8",newline="") as f:
            csv.writer(f).writerow(CHAIN_COLS)

def read_reg():
    with REG.open("r",encoding="utf-8",newline="") as f:
        r=csv.DictReader(f)
        if r.fieldnames!=REG_COLS:
            raise RuntimeError("prospective registry schema mismatch")
        return list(r)

def read_chain():
    with CHAIN.open("r",encoding="utf-8",newline="") as f:
        r=csv.DictReader(f)
        if r.fieldnames!=CHAIN_COLS:
            raise RuntimeError("event chain schema mismatch")
        return list(r)

def payload(row):
    immutable_cols=REG_COLS[:23]
    return json.dumps([row.get(c,"") for c in immutable_cols],separators=(",",":"),ensure_ascii=False)

def row_hash(prev,row):
    return hashlib.sha256((prev+"|"+payload(row)).encode("utf-8")).hexdigest()

def verify(reg,chain):
    if len(reg)!=len(chain):
        raise RuntimeError("registry/chain row mismatch")
    prev=GENESIS
    for i,(row,link) in enumerate(zip(reg,chain),start=1):
        if int(link["sequence"])!=i:
            raise RuntimeError("chain sequence mismatch")
        if link["event_id"]!=row["event_id"]:
            raise RuntimeError("chain event ID mismatch")
        if link["previous_hash"]!=prev:
            raise RuntimeError("chain previous hash mismatch")
        h=row_hash(prev,row)
        if link["row_hash"]!=h:
            raise RuntimeError("chain row hash mismatch")
        prev=h
    return prev

def blank(v):
    return pd.isna(v) or str(v).strip()==""

def hist_reference(df,clazz,release_date):
    g=df[
        (df["mechanism_class"]==clazz)
        & (pd.to_datetime(df["release_date"])<pd.Timestamp(release_date))
        & df["wti_fwd_8w"].notna()
        & df["wti_fwd_13w"].notna()
        & df["short_mae_8w"].notna()
        & df["short_mae_13w"].notna()
    ].copy()
    return {
        "n":int(len(g)),
        "w8":float(g["wti_fwd_8w"].median()) if len(g) else np.nan,
        "w13":float(g["wti_fwd_13w"].median()) if len(g) else np.nan,
        "mae8":float(g["short_mae_8w"].median()) if len(g) else np.nan,
        "mae13":float(g["short_mae_13w"].median()) if len(g) else np.nan,
    }

def main():
    upqc=json.loads(UP_QC.read_text(encoding="utf-8"))
    if upqc.get("qc_gate")!="PASS":
        raise RuntimeError("ENERGY-WEEKLY-STATE-004 QC is not PASS")

    ensure_files()
    reg_before=read_reg()
    chain_before=read_chain()
    tail=verify(reg_before,chain_before)
    existing={r["event_id"] for r in reg_before}

    df=pd.read_csv(SELECTED)
    df["release_date"]=pd.to_datetime(df["release_date"])
    selected_sha=sha(SELECTED)

    candidates=[]
    for _,r in df.iterrows():
        if str(r.get("SELECTED","")).lower() not in {"true","1"}:
            continue
        if any(not blank(r.get(f)) for f in OUTCOME_FIELDS):
            continue
        event_id=f"ENERGY005_{r['release_date'].date().isoformat()}"
        if event_id in existing:
            continue
        candidates.append(r)

    appended=[]
    now=datetime.now(timezone.utc).isoformat()
    for r in candidates:
        event_id=f"ENERGY005_{r['release_date'].date().isoformat()}"
        clazz=str(r["mechanism_class"])
        ref=hist_reference(df,clazz,r["release_date"])
        row={c:"" for c in REG_COLS}
        row.update({
            "event_id":event_id,
            "week_end":str(r["week_end"]),
            "release_date":r["release_date"].date().isoformat(),
            "price_asof_date":str(r["price_asof_date"]),
            "registered_utc":now,
            "upstream_selected_sha256":selected_sha,
            "pressure_score":r["pressure_score"],
            "pressure_q90_prior":r["pressure_q90_prior"],
            "WTI_r5":r["WTI_r5"],
            "GAS_r5":r["GAS_r5"],
            "HEAT_r5":r["HEAT_r5"],
            "JET_r5":r["JET_r5"],
            "inventory_improving_count":int(r["inventory_improving_count"]) if pd.notna(r["inventory_improving_count"]) else "",
            "demand_weak_count":int(r["demand_weak_count"]) if pd.notna(r["demand_weak_count"]) else "",
            "throughput_weak":str(bool(r["throughput_weak"])),
            "upstream_supply_up_count":int(r["upstream_supply_up_count"]) if pd.notna(r["upstream_supply_up_count"]) else "",
            "mechanism_class":clazz,
            "interpretation_state":INTERPRETATION.get(clazz,"UNMAPPED"),
            "historical_same_class_completed_n":ref["n"],
            "historical_same_class_median_wti_8w":ref["w8"],
            "historical_same_class_median_wti_13w":ref["w13"],
            "historical_same_class_median_short_mae_8w":ref["mae8"],
            "historical_same_class_median_short_mae_13w":ref["mae13"],
            "realization_status":"UNREALIZED",
        })
        with REG.open("a",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=REG_COLS); w.writerow(row)

        # Hash the canonical row exactly as it is serialized and read back
        # from the CSV. This avoids Python scalar/string formatting
        # differences between the in-memory row and the persisted registry.
        persisted_rows=read_reg()
        persisted_row=persisted_rows[-1]
        if persisted_row["event_id"]!=event_id:
            raise RuntimeError("persisted event ID mismatch after append")
        h=row_hash(tail,persisted_row)
        with CHAIN.open("a",encoding="utf-8",newline="") as f:
            csv.writer(f).writerow([len(persisted_rows),event_id,tail,h])
        tail=h
        existing.add(event_id)
        appended.append(event_id)

    reg=read_reg()
    chain=read_chain()
    tail=verify(reg,chain)

    first_ok=True
    if reg:
        first=reg[0]
        first_ok=(
            first["event_id"]=="ENERGY005_2026-09-23"
            and first["mechanism_class"]=="TIGHT_OR_MIXED"
            and first["realization_status"]=="UNREALIZED"
        )

    integrity={
        "schema_version":"ENERGY_WEEKLY_PROSPECTIVE_005_V1",
        "registry_sha256":sha(REG),
        "registry_rows":len(reg),
        "chain_rows":len(chain),
        "genesis_hash":GENESIS,
        "tail_hash":tail,
    }
    INTEGRITY.write_text(json.dumps(integrity,indent=2)+"\n",encoding="utf-8")

    qc={
        "qc_gate":"PASS" if first_ok else "FAIL",
        "module":"ENERGY-WEEKLY-PROSPECTIVE-005",
        "upstream_qc":"PASS",
        "upstream_selected_sha256":selected_sha,
        "new_events_appended":appended,
        "registry_rows":len(reg),
        "chain_rows":len(chain),
        "first_event_frozen_correctly":first_ok,
        "first_event_id":reg[0]["event_id"] if reg else None,
        "first_event_class":reg[0]["mechanism_class"] if reg else None,
        "first_event_realization_status":reg[0]["realization_status"] if reg else None,
        "historical_reference_n":int(reg[0]["historical_same_class_completed_n"]) if reg else 0,
        "historical_reference_median_wti_8w":float(reg[0]["historical_same_class_median_wti_8w"]) if reg else None,
        "historical_reference_median_wti_13w":float(reg[0]["historical_same_class_median_wti_13w"]) if reg else None,
        "historical_reference_median_short_mae_8w":float(reg[0]["historical_same_class_median_short_mae_8w"]) if reg else None,
        "historical_reference_median_short_mae_13w":float(reg[0]["historical_same_class_median_short_mae_13w"]) if reg else None,
        "prospective_outcomes_observed":0,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-WEEKLY-PROSPECTIVE-005 — Live Event Registry",
        "",
        "**GENUINELY PROSPECTIVE / APPEND-ONLY / NO LIVE OUTCOME EVIDENCE YET**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- registry rows: {len(reg)}",
        f"- newly appended: {', '.join(appended) if appended else 'none'}",
        "",
    ]
    if reg:
        x=reg[0]
        lines += [
            "## First frozen event",
            "",
            f"- event: {x['event_id']}",
            f"- release date: {x['release_date']}",
            f"- mechanism: **{x['mechanism_class']}**",
            f"- interpretation: **{x['interpretation_state']}**",
            f"- inventories improving: {x['inventory_improving_count']}/3",
            f"- demand weak: {x['demand_weak_count']}/3",
            f"- throughput weak: {x['throughput_weak']}",
            f"- upstream supply blocks improving: {x['upstream_supply_up_count']}/2",
            "",
            "Historical same-class reference frozen at registration:",
            f"- completed n: {x['historical_same_class_completed_n']}",
            f"- median WTI 8W: {float(x['historical_same_class_median_wti_8w']):.2%}",
            f"- median WTI 13W: {float(x['historical_same_class_median_wti_13w']):.2%}",
            f"- median short MAE 8W: {float(x['historical_same_class_median_short_mae_8w']):.2%}",
            f"- median short MAE 13W: {float(x['historical_same_class_median_short_mae_13w']):.2%}",
            "",
            "No realized 4W/8W/13W outcome is present at registration.",
        ]
    (OUT/"ENERGY_WEEKLY_PROSPECTIVE_005_STATUS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if qc["qc_gate"]!="PASS":
        raise SystemExit("ENERGY-WEEKLY-PROSPECTIVE-005 QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
