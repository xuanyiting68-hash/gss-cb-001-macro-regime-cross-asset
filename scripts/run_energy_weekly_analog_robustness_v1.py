#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
SEL=ROOT/"results"/"energy_weekly_state_v1"/"SELECTED_EVENT_PANEL.csv"
PROS=ROOT/"results"/"energy_weekly_prospective_v1"/"PROSPECTIVE_EVENT_REGISTRY.csv"
A12=ROOT/"results"/"energy_weekly_analog_v1"
OUT=ROOT/"results"/"energy_weekly_analog_robustness_v1"
OUT.mkdir(parents=True,exist_ok=True)

FEATURES=[
    "WTI_r5","WTI_r63","GAS_r5","GAS_r63","HEAT_r5","HEAT_r63",
    "JET_r5","JET_r63","pressure_score",
    "inventory_improving_count","demand_weak_count",
    "throughput_weak","upstream_supply_up_count",
]

def boolnum(x):
    return 1.0 if str(x).lower()=="true" else 0.0

def main():
    pros=pd.read_csv(PROS)
    curp=pros.loc[pros.event_id=="ENERGY005_2026-09-23"]
    if len(curp)!=1: raise RuntimeError("current event missing")
    curp=curp.iloc[0]
    if any(pd.notna(curp.get(c)) and str(curp.get(c)).strip()!="" for c in ["realized_wti_4w","realized_wti_8w","realized_wti_13w"]):
        raise RuntimeError("current outcome already realized")

    ev=pd.read_csv(SEL)
    hist=ev[(ev.mechanism_class=="TIGHT_OR_MIXED") & ev.wti_fwd_8w.notna() & ev.wti_fwd_13w.notna() & (ev.release_date!="2026-09-23")].copy()
    if len(hist)!=10: raise RuntimeError("historical pool mismatch")
    cur=ev.loc[ev.release_date=="2026-09-23"]
    if len(cur)!=1: raise RuntimeError("current 004 row missing")
    cur=cur.iloc[0]

    scaling=pd.read_csv(A12/"SCALING.csv").set_index("feature")
    original=pd.read_csv(A12/"TOP3_ANALOGS.csv")
    orig_top=[str(x) for x in original.release_date.tolist()]
    orig_top1=orig_top[0]

    H={}
    C={}
    for f in FEATURES:
        center=float(scaling.loc[f,"center"])
        scale=float(scaling.loc[f,"scale"])
        hv=(hist[f].map(boolnum) if f=="throughput_weak" else pd.to_numeric(hist[f])) 
        cv=boolnum(cur[f]) if f=="throughput_weak" else float(cur[f])
        H[f]=(hv-center)/scale
        C[f]=(cv-center)/scale

    rows=[]
    appearances={x:0 for x in orig_top}
    overlaps=[]
    top1_same=0
    changed=[]

    for drop in FEATURES:
        keep=[f for f in FEATURES if f!=drop]
        dists=[]
        for idx,r in hist.iterrows():
            diffs=np.array([float(H[f].loc[idx])-float(C[f]) for f in keep],float)
            d=float(np.sqrt(np.mean(diffs**2)))
            dists.append((str(r.release_date),d))
        dists.sort(key=lambda x:(x[1],x[0]))
        top=[x[0] for x in dists[:3]]
        overlap=len(set(top)&set(orig_top))
        overlaps.append(overlap)
        if top[0]==orig_top1: top1_same+=1
        else: changed.append(drop)
        for x in orig_top:
            if x in top: appearances[x]+=1
        rows.append({
            "dropped_feature":drop,
            "top1":top[0],"top1_distance":dists[0][1],
            "top2":top[1],"top2_distance":dists[1][1],
            "top3":top[2],"top3_distance":dists[2][1],
            "original_top3_overlap":overlap,
            "original_top1_preserved":top[0]==orig_top1,
        })

    detail=pd.DataFrame(rows)
    detail.to_csv(OUT/"LEAVE_ONE_FEATURE_OUT.csv",index=False)

    app=pd.DataFrame([
        {"original_analog":k,"top3_appearance_count":v,"appearance_share":v/len(FEATURES)}
        for k,v in appearances.items()
    ])
    app.to_csv(OUT/"ORIGINAL_TOP3_APPEARANCE.csv",index=False)

    summary={
        "original_top1":orig_top1,
        "original_top3":orig_top,
        "n_feature_perturbations":len(FEATURES),
        "top1_preserved_count":top1_same,
        "top1_preserved_share":top1_same/len(FEATURES),
        "features_changing_top1":changed,
        "minimum_top3_overlap":int(min(overlaps)),
        "mean_top3_overlap":float(np.mean(overlaps)),
        "original_top3_appearance_counts":appearances,
    }
    (OUT/"ROBUSTNESS_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")

    qc={
        "qc_gate":"PASS",
        "module":"ENERGY-WEEKLY-ANALOG-012A",
        "current_event_outcome_unrealized":True,
        "one_feature_removed_per_run":True,
        "n_feature_perturbations":len(FEATURES),
        "top1_preserved_share":summary["top1_preserved_share"],
        "minimum_top3_overlap":summary["minimum_top3_overlap"],
        "mean_top3_overlap":summary["mean_top3_overlap"],
        "frozen_012_overwritten":False,
        "outcome_fields_in_distance":False,
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-WEEKLY-ANALOG-012A — Leave-One-Feature-Out Robustness",
        "",
        "**CURRENT OUTCOME UNREALIZED / FROZEN 012 BENCHMARK UNCHANGED**",
        "",
        f"- original top-1: {orig_top1}",
        f"- top-1 preserved: {top1_same}/{len(FEATURES)} ({summary['top1_preserved_share']:.1%})",
        f"- minimum original-top3 overlap: {summary['minimum_top3_overlap']}/3",
        f"- mean original-top3 overlap: {summary['mean_top3_overlap']:.2f}/3",
        f"- features changing top-1: {', '.join(changed) if changed else 'none'}",
        "",
        "## Original top-3 appearance stability",
        "",
        app.to_markdown(index=False),
        "",
        "## Perturbations",
        "",
        detail.to_markdown(index=False),
        "",
        "No perturbed run replaces the frozen 012 top-three benchmark.",
    ]
    (OUT/"ENERGY_WEEKLY_ANALOG_012A_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
