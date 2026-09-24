#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/"results"/"fed_cycle_phase_clock_v1"/"PHASE_CYCLE_ASSET_METRICS.csv"
STRESS=ROOT/"results"/"fed_cycle_stress_layer_v1"/"STRESS_CYCLE_PHASE_METRICS.csv"
OUT=ROOT/"results"/"fed_cycle_stress_trough_alignment_v1"
OUT.mkdir(parents=True,exist_ok=True)

ASSETS=["GOLD","SP500","NASDAQ","WTI"]
OBS=["BAA10Y_SPREAD","VIX","COPPER"]

def wq(v,w,q=0.5):
    v=np.asarray(v,float); w=np.asarray(w,float)
    m=np.isfinite(v)&np.isfinite(w)&(w>0)
    v,w=v[m],w[m]
    if not len(v): return np.nan
    o=np.argsort(v);v,w=v[o],w[o]
    c=np.cumsum(w)/w.sum()
    return float(v[np.searchsorted(c,q,side="left")])

def support(nlegs,nbroad):
    if nlegs>=5 and nbroad>=4:
        return "SUPPORTED_TIMING_DESCRIPTIVE"
    if nbroad>=2:
        return "LIMITED_TIMING_DESCRIPTIVE"
    return "INSUFFICIENT_SUPPORT"

def main():
    a=pd.read_csv(ASSET)
    a=a[(a.anchor=="FIRST_CUT") & a.asset.isin(ASSETS)].copy()
    a=a.dropna(subset=["mdd_trough_month"])

    s=pd.read_csv(STRESS)
    s=s[(s.anchor=="FIRST_CUT") & s.observable.isin(OBS)].copy()
    s=s.dropna(subset=["stress_peak_month"])

    if (pd.to_datetime(a.anchor_date).dt.year>=2026).any() or (pd.to_datetime(s.anchor_date).dt.year>=2026).any():
        raise RuntimeError("current 2026 cycle leak")

    rows=[]
    duplicate_bad=0
    id_bad=0

    for asset in ASSETS:
        ga=a[a.asset==asset].copy()
        for obs in OBS:
            gs=s[s.observable==obs].copy()
            if ga.cycle_id.duplicated().any() or gs.cycle_id.duplicated().any():
                duplicate_bad+=1
            m=ga.merge(
                gs[["cycle_id","broad_episode_id","cycle_start_year","anchor_date","episode_weight","stress_peak_month","max_stress_move"]],
                on="cycle_id",how="inner",suffixes=("_asset","_stress"),validate="one_to_one"
            )
            if len(m)==0: continue
            id_bad+=int((m.broad_episode_id_asset!=m.broad_episode_id_stress).sum())
            id_bad+=int((pd.to_datetime(m.anchor_date_asset)!=pd.to_datetime(m.anchor_date_stress)).sum())

            # Use asset-side broad-episode weights. For these paired subsets each broad episode
            # may contain multiple mechanical cycles; renormalize each broad episode total to 1.
            counts=m.groupby("broad_episode_id_asset").cycle_id.transform("count")
            m["paired_episode_weight"]=1.0/counts
            m["lead_months"]=pd.to_numeric(m.mdd_trough_month)-pd.to_numeric(m.stress_peak_month)
            m["abs_gap_months"]=m.lead_months.abs()
            m["stress_before"]=m.lead_months>0
            m["same_month"]=m.lead_months==0
            m["before_or_same"]=m.lead_months>=0
            m["near_2m"]=m.abs_gap_months<=2
            m["both_late_7plus"]=(pd.to_numeric(m.mdd_trough_month)>=7)&(pd.to_numeric(m.stress_peak_month)>=7)
            m["asset_name"]=asset
            m["stress_observable"]=obs

            for _,r in m.iterrows():
                rows.append({
                    "asset":asset,
                    "stress_observable":obs,
                    "cycle_id":r.cycle_id,
                    "broad_episode_id":r.broad_episode_id_asset,
                    "cycle_start_year":r.cycle_start_year_asset,
                    "anchor_date":r.anchor_date_asset,
                    "paired_episode_weight":r.paired_episode_weight,
                    "asset_trough_month":r.mdd_trough_month,
                    "stress_peak_month":r.stress_peak_month,
                    "lead_months":r.lead_months,
                    "abs_gap_months":r.abs_gap_months,
                    "stress_before":r.stress_before,
                    "same_month":r.same_month,
                    "before_or_same":r.before_or_same,
                    "near_2m":r.near_2m,
                    "both_late_7plus":r.both_late_7plus,
                    "max_stress_move":r.max_stress_move,
                })

    panel=pd.DataFrame(rows)
    panel.to_csv(OUT/"PAIR_TIMING_PANEL.csv",index=False)

    timing_bad=int((
        ~pd.to_numeric(panel.asset_trough_month).between(1,12)
        | ~pd.to_numeric(panel.stress_peak_month).between(1,12)
    ).sum())

    sums=[]
    for (asset,obs),g in panel.groupby(["asset","stress_observable"]):
        w=g.paired_episode_weight.astype(float)
        sums.append({
            "asset":asset,
            "stress_observable":obs,
            "n_legs":int(g.cycle_id.nunique()),
            "n_broad_episodes":int(g.broad_episode_id.nunique()),
            "support_status":support(int(g.cycle_id.nunique()),int(g.broad_episode_id.nunique())),
            "weighted_median_asset_trough_month":wq(g.asset_trough_month,w),
            "weighted_median_stress_peak_month":wq(g.stress_peak_month,w),
            "weighted_median_lead_months":wq(g.lead_months,w),
            "weighted_median_abs_gap_months":wq(g.abs_gap_months,w),
            "weighted_stress_before_share":float(np.average(g.stress_before.astype(float),weights=w)),
            "weighted_same_month_share":float(np.average(g.same_month.astype(float),weights=w)),
            "weighted_before_or_same_share":float(np.average(g.before_or_same.astype(float),weights=w)),
            "weighted_near_2m_share":float(np.average(g.near_2m.astype(float),weights=w)),
            "weighted_both_late_7plus_share":float(np.average(g.both_late_7plus.astype(float),weights=w)),
        })
    summary=pd.DataFrame(sums)
    summary.to_csv(OUT/"PAIR_TIMING_SUMMARY.csv",index=False)

    supported=summary[summary.support_status=="SUPPORTED_TIMING_DESCRIPTIVE"].copy()
    supported.to_csv(OUT/"SUPPORTED_TIMING_PAIRS.csv",index=False)

    # Broad synthesis by stress observable across supported asset pairs.
    synth=[]
    for obs,g in supported.groupby("stress_observable"):
        synth.append({
            "stress_observable":obs,
            "supported_asset_pairs":int(len(g)),
            "median_of_pair_median_leads":float(g.weighted_median_lead_months.median()),
            "median_near_2m_share":float(g.weighted_near_2m_share.median()),
            "median_before_or_same_share":float(g.weighted_before_or_same_share.median()),
            "median_both_late_share":float(g.weighted_both_late_7plus_share.median()),
        })
    synthesis=pd.DataFrame(synth)
    synthesis.to_csv(OUT/"STRESS_SYNTHESIS.csv",index=False)

    hard_fail=duplicate_bad or id_bad or timing_bad
    qc={
        "qc_gate":"FAIL" if hard_fail else "PASS",
        "module":"FED-CYCLE-STRESS-TROUGH-ALIGNMENT-018",
        "pair_rows":int(len(panel)),
        "pair_cells":int(len(summary)),
        "supported_pair_cells":int(len(supported)),
        "duplicate_cycle_violations":duplicate_bad,
        "identifier_mismatch_violations":id_bad,
        "timing_range_violations":timing_bad,
        "pvalues_generated":False,
        "real_time_signal_status":"NOT_A_REAL_TIME_SIGNAL",
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# FED-CYCLE-STRESS-TROUGH-ALIGNMENT-018",
        "",
        "**POST-ANCHOR MECHANISM TIMING / NOT A REAL-TIME SIGNAL**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        "",
        "## Supported asset × stress timing pairs",
        "",
        supported.to_markdown(index=False),
        "",
        "## Stress-observable synthesis",
        "",
        synthesis.to_markdown(index=False),
        "",
        "Positive lead means the stress maximum occurs before the asset MDD trough.",
        "Near-coincidence means the two occur within two months.",
        "Because both stress peak and trough are future-window statistics, this module is explanatory timing evidence only.",
    ]
    (OUT/"FED_CYCLE_STRESS_TROUGH_ALIGNMENT_018_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-STRESS-TROUGH-ALIGNMENT-018 QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
