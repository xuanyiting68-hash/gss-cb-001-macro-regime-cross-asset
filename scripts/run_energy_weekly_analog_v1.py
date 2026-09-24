#!/usr/bin/env python3
"""
ENERGY-WEEKLY-ANALOG-012
Prospective nearest historical analog benchmark for ENERGY005_2026-09-23.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
SEL=ROOT/"results"/"energy_weekly_state_v1"/"SELECTED_EVENT_PANEL.csv"
PROS=ROOT/"results"/"energy_weekly_prospective_v1"/"PROSPECTIVE_EVENT_REGISTRY.csv"
OUT=ROOT/"results"/"energy_weekly_analog_v1"
OUT.mkdir(parents=True,exist_ok=True)

FEATURES=[
    "WTI_r5","WTI_r63","GAS_r5","GAS_r63","HEAT_r5","HEAT_r63",
    "JET_r5","JET_r63","pressure_score",
    "inventory_improving_count","demand_weak_count",
    "throughput_weak","upstream_supply_up_count",
]
K=3

def as_num_bool(s):
    if s.dtype==bool:
        return s.astype(float)
    return s.map(lambda x: 1.0 if str(x).lower()=="true" else (0.0 if str(x).lower()=="false" else float(x)))

def robust_center_scale(x):
    a=np.asarray(x,float)
    med=float(np.median(a))
    mad=float(np.median(np.abs(a-med)))
    scale=1.4826*mad
    method="MAD"
    if not np.isfinite(scale) or scale<=1e-12:
        scale=float(np.std(a,ddof=1))
        method="SD_FALLBACK"
    active=bool(np.isfinite(scale) and scale>1e-12)
    return med,scale if active else np.nan,method,active

def main():
    ev=pd.read_csv(SEL)
    pros=pd.read_csv(PROS)

    cur=pros.loc[pros.event_id=="ENERGY005_2026-09-23"]
    if len(cur)!=1:
        raise RuntimeError("current prospective event missing")
    cur=cur.iloc[0]

    realized_cols=[
        "realized_wti_4w","realized_wti_8w","realized_wti_13w",
        "realized_short_mae_8w","realized_short_mae_13w"
    ]
    if any(pd.notna(cur.get(c)) and str(cur.get(c)).strip()!="" for c in realized_cols):
        raise RuntimeError("current event outcome already realized; analog freeze too late")

    hist=ev[
        (ev.mechanism_class=="TIGHT_OR_MIXED")
        & ev.wti_fwd_8w.notna()
        & ev.wti_fwd_13w.notna()
        & (ev.release_date!="2026-09-23")
    ].copy()
    if len(hist)!=10:
        raise RuntimeError(f"expected historical analog pool n=10, got {len(hist)}")

    # Current feature vector comes from original 004 selected-event panel to ensure exact frozen values.
    cur004=ev.loc[ev.release_date=="2026-09-23"]
    if len(cur004)!=1:
        raise RuntimeError("current event missing from 004 panel")
    cur004=cur004.iloc[0]

    H=pd.DataFrame(index=hist.index)
    c={}
    scaling=[]
    active_features=[]

    for f in FEATURES:
        if f=="throughput_weak":
            hv=as_num_bool(hist[f])
            cv=1.0 if str(cur004[f]).lower()=="true" else 0.0
        else:
            hv=pd.to_numeric(hist[f],errors="coerce")
            cv=float(cur004[f])
        if hv.isna().any() or not np.isfinite(cv):
            raise RuntimeError(f"missing analog feature {f}")
        center,scale,method,active=robust_center_scale(hv.values)
        scaling.append({
            "feature":f,"center":center,"scale":scale,
            "scale_method":method,"active":active,
        })
        if active:
            H[f]=(hv-center)/scale
            c[f]=(cv-center)/scale
            active_features.append(f)

    if not active_features:
        raise RuntimeError("no active analog features")

    dist=[]
    contrib_rows=[]
    for idx,row in hist.iterrows():
        diffs=np.array([float(H.loc[idx,f])-float(c[f]) for f in active_features],float)
        d=float(np.sqrt(np.mean(diffs**2)))
        dist.append((idx,d))
        for f,diff in zip(active_features,diffs):
            contrib_rows.append({
                "event_release_date":row.release_date,
                "feature":f,
                "squared_z_difference":float(diff**2),
            })

    dist=sorted(dist,key=lambda x:(x[1],str(hist.loc[x[0],"release_date"])))
    top=dist[:K]

    rows=[]
    for rank,(idx,d) in enumerate(top,start=1):
        r=hist.loc[idx]
        rows.append({
            "rank":rank,
            "release_date":r.release_date,
            "distance":d,
            "WTI_r5":r.WTI_r5,
            "WTI_r63":r.WTI_r63,
            "pressure_score":r.pressure_score,
            "inventory_improving_count":r.inventory_improving_count,
            "demand_weak_count":r.demand_weak_count,
            "throughput_weak":r.throughput_weak,
            "upstream_supply_up_count":r.upstream_supply_up_count,
            "wti_fwd_4w":r.wti_fwd_4w,
            "wti_fwd_8w":r.wti_fwd_8w,
            "wti_fwd_13w":r.wti_fwd_13w,
            "short_mae_8w":r.short_mae_8w,
            "short_mae_13w":r.short_mae_13w,
        })
    topdf=pd.DataFrame(rows)
    topdf.to_csv(OUT/"TOP3_ANALOGS.csv",index=False)

    allrows=[]
    for idx,d in dist:
        r=hist.loc[idx]
        allrows.append({
            "release_date":r.release_date,
            "distance":d,
            "wti_fwd_8w":r.wti_fwd_8w,
            "wti_fwd_13w":r.wti_fwd_13w,
            "short_mae_8w":r.short_mae_8w,
            "short_mae_13w":r.short_mae_13w,
        })
    pd.DataFrame(allrows).to_csv(OUT/"ALL_ANALOG_DISTANCES.csv",index=False)
    pd.DataFrame(scaling).to_csv(OUT/"SCALING.csv",index=False)

    contrib=pd.DataFrame(contrib_rows)
    topdates=set(topdf.release_date.astype(str))
    topcontrib=contrib[contrib.event_release_date.astype(str).isin(topdates)].copy()
    topcontrib=topcontrib.sort_values(["event_release_date","squared_z_difference"],ascending=[True,False])
    topcontrib.to_csv(OUT/"TOP3_DISTANCE_CONTRIBUTIONS.csv",index=False)

    ref={
        "top_k":K,
        "historical_pool_n":len(hist),
        "active_feature_n":len(active_features),
        "active_features":active_features,
        "top3_median_wti_4w":float(topdf.wti_fwd_4w.median()),
        "top3_median_wti_8w":float(topdf.wti_fwd_8w.median()),
        "top3_median_wti_13w":float(topdf.wti_fwd_13w.median()),
        "top3_median_short_mae_8w":float(topdf.short_mae_8w.median()),
        "top3_median_short_mae_13w":float(topdf.short_mae_13w.median()),
        "top3_min_wti_8w":float(topdf.wti_fwd_8w.min()),
        "top3_max_wti_8w":float(topdf.wti_fwd_8w.max()),
        "top3_min_wti_13w":float(topdf.wti_fwd_13w.min()),
        "top3_max_wti_13w":float(topdf.wti_fwd_13w.max()),
    }
    (OUT/"ANALOG_REFERENCE.json").write_text(json.dumps(ref,indent=2)+"\n",encoding="utf-8")

    qc={
        "qc_gate":"PASS",
        "module":"ENERGY-WEEKLY-ANALOG-012",
        "current_event_id":"ENERGY005_2026-09-23",
        "current_event_outcome_unrealized":True,
        "historical_pool_n":len(hist),
        "top_k":K,
        "active_feature_n":len(active_features),
        "outcome_fields_in_distance":False,
        "current_event_in_scaling":False,
        "model_fit_to_outcome":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
        **{k:v for k,v in ref.items() if k.startswith("top3_")},
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    current_row=pd.DataFrame([{
        "event_id":"ENERGY005_2026-09-23",
        **{f:(1.0 if f=="throughput_weak" and str(cur004[f]).lower()=="true" else (0.0 if f=="throughput_weak" else float(cur004[f]))) for f in FEATURES}
    }])
    current_row.to_csv(OUT/"CURRENT_EVENT_FEATURES.csv",index=False)

    lines=[
        "# ENERGY-WEEKLY-ANALOG-012 — Prospective Historical Analog Benchmark",
        "",
        "**FROZEN BEFORE CURRENT OUTCOME / NO OUTCOME-FITTED MODEL**",
        "",
        f"- historical same-class pool: {len(hist)}",
        f"- active frozen features: {len(active_features)}",
        f"- top K: {K}",
        "",
        "## Top 3 historical analogs",
        "",
        topdf.to_markdown(index=False),
        "",
        "## Frozen top-3 reference",
        "",
        f"- median WTI 4W: {ref['top3_median_wti_4w']:.2%}",
        f"- median WTI 8W: {ref['top3_median_wti_8w']:.2%}",
        f"- median WTI 13W: {ref['top3_median_wti_13w']:.2%}",
        f"- WTI 8W range: {ref['top3_min_wti_8w']:.2%} to {ref['top3_max_wti_8w']:.2%}",
        f"- WTI 13W range: {ref['top3_min_wti_13w']:.2%} to {ref['top3_max_wti_13w']:.2%}",
        f"- median short MAE 8W: {ref['top3_median_short_mae_8w']:.2%}",
        f"- median short MAE 13W: {ref['top3_median_short_mae_13w']:.2%}",
        "",
        "This is a prospective historical reference set, not a validated forecast.",
    ]
    (OUT/"ENERGY_WEEKLY_ANALOG_012_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
