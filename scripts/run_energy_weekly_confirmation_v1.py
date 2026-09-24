#!/usr/bin/env python3
"""
ENERGY-WEEKLY-CONFIRMATION-009
Post-event EIA physical confirmation path without WTI outcome use.
"""
from __future__ import annotations

import csv, hashlib, importlib.util, json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
PIT_REG=ROOT/"results"/"energy_weekly_pit_v1"/"WPSR_RELEASE_REGISTRY.csv"
PROS=ROOT/"results"/"energy_weekly_prospective_v1"/"PROSPECTIVE_EVENT_REGISTRY.csv"
OUT=ROOT/"results"/"energy_weekly_confirmation_v1"
OUT.mkdir(parents=True,exist_ok=True)

REG=OUT/"POST_EVENT_CONFIRMATION_REGISTRY.csv"
INTEGRITY=OUT/"REGISTRY_INTEGRITY.json"

COLS=[
 "sequence","event_id","week_end","release_date","appended_utc",
 "mechanism_class","inventory_improving_count","demand_weak_count",
 "throughput_weak","upstream_supply_up_count","mechanism_complete",
 "confirmation_state_after_release","source_hash_bundle",
 "previous_hash","row_hash"
]
GENESIS=hashlib.sha256(b"ENERGY_WEEKLY_CONFIRMATION_009_GENESIS_V1").hexdigest()

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

STATE=load_module(ROOT/"scripts"/"run_energy_weekly_state_v1.py","state004_for_confirmation009")
PIT=load_module(ROOT/"scripts"/"run_energy_weekly_pit_v1.py","pit003_for_confirmation009")
FLOW=load_module(ROOT/"scripts"/"run_energy_flow_decomposition_v2.py","flow002_for_confirmation009")

def payload(row):
    core=[row.get(c,"") for c in COLS[:-2]]
    return json.dumps(core,separators=(",",":"),ensure_ascii=False)

def h(prev,row):
    return hashlib.sha256((prev+"|"+payload(row)).encode("utf-8")).hexdigest()

def ensure_reg():
    if not REG.exists():
        with REG.open("w",encoding="utf-8",newline="") as f:
            csv.writer(f).writerow(COLS)

def read_reg():
    ensure_reg()
    with REG.open("r",encoding="utf-8",newline="") as f:
        r=csv.DictReader(f)
        if r.fieldnames!=COLS: raise RuntimeError("009 schema mismatch")
        return list(r)

def verify(rows):
    prev=GENESIS
    keys=set()
    for i,row in enumerate(rows,start=1):
        if int(row["sequence"])!=i: raise RuntimeError("009 sequence mismatch")
        key=(row["week_end"],row["release_date"])
        if key in keys: raise RuntimeError("009 duplicate release row")
        keys.add(key)
        if row["previous_hash"]!=prev: raise RuntimeError("009 previous hash mismatch")
        if row["row_hash"]!=h(prev,row): raise RuntimeError("009 row hash mismatch")
        prev=row["row_hash"]
    return prev,keys

def state_from_classes(classes):
    if len(classes)==0: return "WAITING_NEXT_WPSR_RELEASE"
    last=classes[-1]
    if len(classes)>=2 and classes[-1]==classes[-2]=="DEMAND_DESTRUCTION":
        return "DEMAND_DESTRUCTION_CONFIRMED"
    if len(classes)>=2 and classes[-1]==classes[-2]=="SUPPLY_NORMALIZATION":
        return "SUPPLY_NORMALIZATION_CONFIRMED"
    if last=="DEMAND_DESTRUCTION":
        return "DEMAND_DESTRUCTION_CANDIDATE"
    if last=="SUPPLY_NORMALIZATION":
        return "SUPPLY_NORMALIZATION_CANDIDATE"
    return "NO_CLEAN_CONFIRMATION"

def main():
    pros=pd.read_csv(PROS)
    e=pros.loc[pros.event_id=="ENERGY005_2026-09-23"]
    if len(e)!=1 or e.iloc[0].mechanism_class!="TIGHT_OR_MIXED":
        raise RuntimeError("frozen ENERGY005 event missing/mismatched")
    event_release=pd.Timestamp(e.iloc[0].release_date).normalize()

    existing=read_reg()
    tail,keys=verify(existing)

    # Fetch fresh weekly series. Four core grids determine release availability.
    weekly={}; metas={}
    for name,sid in STATE.WEEKLY.items():
        z,m=FLOW.parse_eia_xls(sid)
        weekly[name]=z
        metas[name]=m

    core=["CRUDE_STOCK","GAS_STOCK","DIST_STOCK","REFINERY_UTIL"]
    common=set(weekly[core[0]].week_end)
    for name in core[1:]:
        common &= set(weekly[name].week_end)
    common=sorted(pd.to_datetime(list(common)))

    base=pd.read_csv(PIT_REG,parse_dates=["week_end","release_date"]).sort_values("week_end")
    max_base=pd.Timestamp(base.week_end.max()).normalize()

    exc,schedule_sha=PIT.parse_schedule_exceptions((2026,))
    exc_map={} if exc.empty else dict(zip(exc.week_end,exc.release_date))

    fresh=[]
    for we in common:
        we=pd.Timestamp(we).normalize()
        if we<=max_base or we.year!=2026: continue
        rd=exc_map.get(we,PIT.standard_wpsr_release(we))
        fresh.append({"week_end":we,"release_date":pd.Timestamp(rd).normalize()})

    full=pd.concat([base[["week_end","release_date"]],pd.DataFrame(fresh)],ignore_index=True)
    full=full.drop_duplicates("week_end",keep="last").sort_values("week_end").reset_index(drop=True)

    now=pd.Timestamp(datetime.now(timezone.utc)).tz_convert(None).normalize()
    observed=full[(full.release_date>event_release)&(full.release_date<=now)].copy()

    classes=[r["mechanism_class"] for r in existing]
    appended=[]
    source_hash_bundle=json.dumps({
        name:metas[name].get("sha256","") for name in sorted(metas)
    },sort_keys=True,separators=(",",":"))

    for _,rr in observed.iterrows():
        key=(rr.week_end.date().isoformat(),rr.release_date.date().isoformat())
        if key in keys: continue
        event=pd.Series({"week_end":rr.week_end,"release_date":rr.release_date})
        mech=STATE.mechanism_for_event(event,full,weekly)
        classes.append(mech["mechanism_class"])
        cstate=state_from_classes(classes)

        row={
            "sequence":str(len(existing)+len(appended)+1),
            "event_id":"ENERGY005_2026-09-23",
            "week_end":rr.week_end.date().isoformat(),
            "release_date":rr.release_date.date().isoformat(),
            "appended_utc":datetime.now(timezone.utc).isoformat(),
            "mechanism_class":mech["mechanism_class"],
            "inventory_improving_count":str(mech.get("inventory_improving_count","")),
            "demand_weak_count":str(mech.get("demand_weak_count","")),
            "throughput_weak":str(mech.get("throughput_weak","")),
            "upstream_supply_up_count":str(mech.get("upstream_supply_up_count","")),
            "mechanism_complete":str(mech.get("mechanism_complete",False)),
            "confirmation_state_after_release":cstate,
            "source_hash_bundle":source_hash_bundle,
            "previous_hash":tail,
            "row_hash":"",
        }
        row["row_hash"]=h(tail,row)
        tail=row["row_hash"]
        appended.append(row)
        keys.add(key)

    if appended:
        with REG.open("a",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=COLS)
            w.writerows(appended)

    final=read_reg()
    tail,_=verify(final)
    final_classes=[r["mechanism_class"] for r in final]
    current=state_from_classes(final_classes)

    integrity={
        "schema_version":"ENERGY_WEEKLY_CONFIRMATION_009_V1",
        "registry_sha256":hashlib.sha256(REG.read_bytes()).hexdigest(),
        "registry_rows":len(final),
        "genesis_hash":GENESIS,
        "tail_hash":tail,
        "current_confirmation_state":current,
    }
    INTEGRITY.write_text(json.dumps(integrity,indent=2)+"\n",encoding="utf-8")

    qc={
        "qc_gate":"PASS",
        "module":"ENERGY-WEEKLY-CONFIRMATION-009",
        "event_id":"ENERGY005_2026-09-23",
        "event_original_class":"TIGHT_OR_MIXED",
        "fresh_common_week_ends_after_pit_base":len(fresh),
        "observed_post_event_releases":int(len(observed)),
        "new_rows_appended":len(appended),
        "registry_rows":len(final),
        "current_confirmation_state":current,
        "two_release_confirmation_rule":True,
        "prospective_wti_outcomes_used":False,
        "thresholds_changed":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-WEEKLY-CONFIRMATION-009 — Post-Event Physical Confirmation",
        "",
        "**NO PRICE-OUTCOME USE / TWO-RELEASE HYSTERESIS**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- observed post-event WPSR releases: {len(observed)}",
        f"- confirmation registry rows: {len(final)}",
        f"- current state: **{current}**",
        "",
        "A single clean weekly class is only a candidate. Confirmation requires two consecutive observed WPSR releases with the same clean class.",
        "The original ENERGY005 event label remains TIGHT_OR_MIXED and is never rewritten.",
    ]
    (OUT/"ENERGY_WEEKLY_CONFIRMATION_009_STATUS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
