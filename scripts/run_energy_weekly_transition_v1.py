#!/usr/bin/env python3
"""
ENERGY-WEEKLY-TRANSITION-011
Historical post-event mechanism transitions for completed TIGHT_OR_MIXED events.
"""
from __future__ import annotations

import importlib.util, json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
SEL=ROOT/"results"/"energy_weekly_state_v1"/"SELECTED_EVENT_PANEL.csv"
PIT_REG=ROOT/"results"/"energy_weekly_pit_v1"/"WPSR_RELEASE_REGISTRY.csv"
OUT=ROOT/"results"/"energy_weekly_transition_v1"
OUT.mkdir(parents=True,exist_ok=True)

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

STATE=load_module(ROOT/"scripts"/"run_energy_weekly_state_v1.py","state004_for_transition011")
FLOW=load_module(ROOT/"scripts"/"run_energy_flow_decomposition_v2.py","flow002_for_transition011")

def transition_label(classes):
    first_clean=None
    first_confirm=None
    first_confirm_class=None

    for i,c in enumerate(classes, start=1):
        if first_clean is None and c in {"DEMAND_DESTRUCTION","SUPPLY_NORMALIZATION"}:
            first_clean=i

    for i in range(1,len(classes)):
        if classes[i]==classes[i-1] and classes[i] in {"DEMAND_DESTRUCTION","SUPPLY_NORMALIZATION"}:
            first_confirm=i+1
            first_confirm_class=classes[i]
            break

    if first_confirm_class=="DEMAND_DESTRUCTION":
        label="DD_CONFIRMED_WITHIN_4"
    elif first_confirm_class=="SUPPLY_NORMALIZATION":
        label="SN_CONFIRMED_WITHIN_4"
    elif first_clean is not None:
        label="CLEAN_CANDIDATE_ONLY"
    else:
        label="REMAINS_MIXED_OR_INCOMPLETE"
    return label,first_clean,first_confirm,first_confirm_class

def summary(g,label):
    rec={"transition_group":label,"n":len(g)}
    for h in ["4w","8w","13w"]:
        x=g[f"wti_fwd_{h}"].dropna().astype(float)
        rec[f"median_wti_{h}"]=float(x.median()) if len(x) else np.nan
        rec[f"negative_share_{h}"]=float((x<0).mean()) if len(x) else np.nan
    for h in ["8w","13w"]:
        x=g[f"short_mae_{h}"].dropna().astype(float)
        rec[f"median_short_mae_{h}"]=float(x.median()) if len(x) else np.nan
    return rec

def main():
    ev=pd.read_csv(SEL,parse_dates=["week_end","release_date"])
    hist=ev[
        (ev.mechanism_class=="TIGHT_OR_MIXED")
        & ev.wti_fwd_8w.notna()
    ].copy()

    if len(hist)!=10:
        raise RuntimeError(f"expected 10 completed historical mixed events, got {len(hist)}")
    if (hist.release_date==pd.Timestamp("2026-09-23")).any():
        raise RuntimeError("prospective event leaked into historical transition diagnostic")

    reg=pd.read_csv(PIT_REG,parse_dates=["week_end","release_date"]).sort_values("release_date").reset_index(drop=True)

    weekly={}
    for name,sid in STATE.WEEKLY.items():
        z,m=FLOW.parse_eia_xls(sid)
        weekly[name]=z

    rows=[]
    timing_bad=0
    duplicate_bad=0

    for _,e in hist.iterrows():
        idx=reg.index[reg.week_end==e.week_end]
        if len(idx)!=1:
            raise RuntimeError(f"event week_end missing/duplicate in PIT registry: {e.week_end}")
        i=int(idx[0])
        future=reg.iloc[i+1:i+5].copy()
        if len(future)!=4:
            raise RuntimeError(f"insufficient four-release path for {e.release_date.date()}")
        if future.release_date.duplicated().any():
            duplicate_bad+=1
        if not (future.release_date>e.release_date).all():
            timing_bad+=1

        classes=[]
        details=[]
        for k,(_,rr) in enumerate(future.iterrows(),start=1):
            pseudo=pd.Series({"week_end":rr.week_end,"release_date":rr.release_date})
            m=STATE.mechanism_for_event(pseudo,reg,weekly)
            classes.append(m["mechanism_class"])
            details.append(m)

        label,first_clean,first_confirm,confirm_class=transition_label(classes)

        row={
            "event_release_date":e.release_date.date().isoformat(),
            "event_week_end":e.week_end.date().isoformat(),
            "event_original_class":e.mechanism_class,
            "t1_release_date":future.iloc[0].release_date.date().isoformat(),
            "t1_class":classes[0],
            "t2_release_date":future.iloc[1].release_date.date().isoformat(),
            "t2_class":classes[1],
            "t3_release_date":future.iloc[2].release_date.date().isoformat(),
            "t3_class":classes[2],
            "t4_release_date":future.iloc[3].release_date.date().isoformat(),
            "t4_class":classes[3],
            "transition_group":label,
            "first_clean_release_number":first_clean,
            "first_confirm_release_number":first_confirm,
            "first_confirm_class":confirm_class,
            "wti_fwd_4w":e.wti_fwd_4w,
            "wti_fwd_8w":e.wti_fwd_8w,
            "wti_fwd_13w":e.wti_fwd_13w,
            "short_mae_8w":e.short_mae_8w,
            "short_mae_13w":e.short_mae_13w,
        }
        rows.append(row)

    panel=pd.DataFrame(rows)
    panel.to_csv(OUT/"TRANSITION_PANEL.csv",index=False)

    groups=[]
    order=[
        "DD_CONFIRMED_WITHIN_4",
        "SN_CONFIRMED_WITHIN_4",
        "CLEAN_CANDIDATE_ONLY",
        "REMAINS_MIXED_OR_INCOMPLETE",
    ]
    for label in order:
        groups.append(summary(panel[panel.transition_group==label],label))
    summary_df=pd.DataFrame(groups)
    summary_df.to_csv(OUT/"TRANSITION_SUMMARY.csv",index=False)

    confirmed=panel.first_confirm_release_number.dropna().astype(int)
    timing=pd.DataFrame([{
        "historical_mixed_events":len(panel),
        "ever_clean_within_4":int(panel.first_clean_release_number.notna().sum()),
        "ever_two_release_confirmed_within_4":int(panel.first_confirm_release_number.notna().sum()),
        "confirmed_by_t2":int((confirmed<=2).sum()),
        "confirmed_by_t3":int((confirmed<=3).sum()),
        "confirmed_by_t4":int((confirmed<=4).sum()),
        "dd_confirmed_within_4":int((panel.transition_group=="DD_CONFIRMED_WITHIN_4").sum()),
        "sn_confirmed_within_4":int((panel.transition_group=="SN_CONFIRMED_WITHIN_4").sum()),
        "candidate_only":int((panel.transition_group=="CLEAN_CANDIDATE_ONLY").sum()),
        "remains_mixed_or_incomplete":int((panel.transition_group=="REMAINS_MIXED_OR_INCOMPLETE").sum()),
    }])
    timing.to_csv(OUT/"TIMING_SUMMARY.csv",index=False)

    qc={
        "qc_gate":"FAIL" if timing_bad or duplicate_bad or len(panel)!=10 else "PASS",
        "module":"ENERGY-WEEKLY-TRANSITION-011",
        "post_run_diagnostic":True,
        "historical_completed_mixed_events":len(panel),
        "prospective_event_included":False,
        "post_event_timing_violations":timing_bad,
        "duplicate_post_event_release_violations":duplicate_bad,
        "pvalues_generated":False,
        "thresholds_changed":False,
        **timing.iloc[0].to_dict(),
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,default=str)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-WEEKLY-TRANSITION-011 — Historical Mixed-State Transition Diagnostic",
        "",
        "**POST-RUN DESCRIPTIVE / EXACT 004 MECHANISM RULE / NO P-VALUES**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- completed historical TIGHT_OR_MIXED events: {len(panel)}",
        f"- ever clean within 4 releases: {int(timing.iloc[0].ever_clean_within_4)}",
        f"- two-release confirmed within 4: {int(timing.iloc[0].ever_two_release_confirmed_within_4)}",
        f"- DD confirmed within 4: {int(timing.iloc[0].dd_confirmed_within_4)}",
        f"- SN confirmed within 4: {int(timing.iloc[0].sn_confirmed_within_4)}",
        "",
        "## Timing",
        "",
        timing.to_markdown(index=False),
        "",
        "## Outcome descriptives by transition group",
        "",
        summary_df.to_markdown(index=False),
        "",
        "## Event paths",
        "",
        panel.to_markdown(index=False),
        "",
        "This diagnostic is hypothesis-generating only. It does not alter the current live event, 009 confirmation rule, or 008 outcome accounting.",
    ]
    (OUT/"ENERGY_WEEKLY_TRANSITION_011_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if qc["qc_gate"]!="PASS":
        raise SystemExit("ENERGY-WEEKLY-TRANSITION-011 QC failed")
    print(json.dumps(qc,indent=2,default=str))

if __name__=="__main__":
    main()
