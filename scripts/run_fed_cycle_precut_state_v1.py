#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/"results"/"fed_cycle_state_panel_v2"/"MONTHLY_STATE_PANEL.csv"
RT=ROOT/"results"/"fed_cycle_vintage_audit_v1"/"PANEL_REALTIME_IPT.csv"
CLOCK=ROOT/"results"/"fed_cycle_total_risk_clock_v1"/"SUPPORTED_EVENT_TOTAL_CLOCK.csv"
OUT=ROOT/"results"/"fed_cycle_precut_state_v1"
OUT.mkdir(parents=True,exist_ok=True)

RISK_ASSETS=["SP500","NASDAQ","WTI"]

def wmedian(v,w):
    v=np.asarray(v,float); w=np.asarray(w,float)
    m=np.isfinite(v)&np.isfinite(w)&(w>0)
    v,w=v[m],w[m]
    if not len(v): return np.nan
    o=np.argsort(v);v,w=v[o],w[o]
    c=np.cumsum(w)/w.sum()
    return float(v[np.searchsorted(c,0.5,side="left")])

def rank_corr(x,y):
    x=pd.Series(x,dtype=float)
    y=pd.Series(y,dtype=float)
    if len(x)<3 or x.nunique()<2 or y.nunique()<2:
        return np.nan
    rx=x.rank(method="average").to_numpy(float)
    ry=y.rank(method="average").to_numpy(float)
    return float(np.corrcoef(rx,ry)[0,1])

def main():
    state=pd.read_csv(
        STATE,
        parse_dates=["first_cut","panel_month_start","yield_obs_date","nfci_obs_date"],
    )
    rt=pd.read_csv(RT)

    # The last panel month is the frozen information month immediately preceding FIRST_CUT.
    last=(
        state.sort_values(["cycle_id","panel_month_start"])
        .groupby("cycle_id",as_index=False)
        .tail(1)
        .copy()
    )
    last=last.merge(
        rt[["cycle_id","panel_month","RT_IPT_YOY","RT_IPT_VINTAGE_PERIOD"]],
        on=["cycle_id","panel_month"],
        how="left",
        validate="one_to_one",
    )

    # Outcome: supported FIRST_CUT trough months for SP500/NASDAQ/WTI.
    clk=pd.read_csv(CLOCK,parse_dates=["anchor_date"])
    clk=clk[(clk.anchor=="FIRST_CUT") & clk.asset.isin(RISK_ASSETS)].copy()
    p=clk.pivot_table(
        index=["cycle_id","broad_episode_id","anchor_date"],
        columns="asset",
        values="trough_month",
        aggfunc="first",
    ).reset_index()
    p=p.dropna(subset=RISK_ASSETS).copy()
    p["RISK3_MEDIAN_TROUGH_MONTH"]=p[RISK_ASSETS].median(axis=1)
    p["RISK3_LATE_TROUGH_SHARE"]=(p[RISK_ASSETS]>=7).mean(axis=1)

    cols=[
        "cycle_id","broad_episode_id","first_cut","panel_month","panel_month_start",
        "yield_obs_date","nfci_obs_date","CURVE_BP","NFCI",
        "RT_IPT_YOY","RT_IPT_VINTAGE_PERIOD",
    ]
    d=p.merge(last[cols],on=["cycle_id","broad_episode_id"],how="inner",validate="one_to_one")

    if len(d)<6 or d.broad_episode_id.nunique()<5:
        raise RuntimeError("019 minimum support not met")
    if d[["CURVE_BP","NFCI","RT_IPT_YOY"]].isna().any().any():
        raise RuntimeError("missing pre-cut state variable")

    d["RT_IPT_VINTAGE_PERIOD_P"]=pd.PeriodIndex(d.RT_IPT_VINTAGE_PERIOD.astype(str),freq="M")
    d["PANEL_MONTH_P"]=pd.PeriodIndex(d.panel_month.astype(str),freq="M")

    timing_bad=int((
        (d.panel_month_start>=d.first_cut)
        | (d.yield_obs_date>=d.first_cut)
        | (d.nfci_obs_date>=d.first_cut)
        | (d.RT_IPT_VINTAGE_PERIOD_P>=d.PANEL_MONTH_P)
    ).sum())
    current_bad=int((pd.to_datetime(d.first_cut).dt.year>=2026).sum())

    d["REALTIME_GROWTH_CONTRACTION"]=d.RT_IPT_YOY<0
    d["CURVE_INVERTED"]=d.CURVE_BP<0
    d["FINANCIAL_CONDITIONS_TIGHT"]=d.NFCI>0
    states=["REALTIME_GROWTH_CONTRACTION","CURVE_INVERTED","FINANCIAL_CONDITIONS_TIGHT"]
    d["PRE_CUT_STRESS_COUNT"]=d[states].astype(int).sum(axis=1)

    counts=d.groupby("broad_episode_id").cycle_id.transform("count")
    d["episode_weight"]=1.0/counts
    d.drop(columns=["RT_IPT_VINTAGE_PERIOD_P","PANEL_MONTH_P"]).to_csv(
        OUT/"PRECUT_STATE_CYCLE_PANEL.csv",index=False
    )

    # Broad-episode aggregation avoids overweighting nearby mechanical legs.
    broad=[]
    for bid,g in d.groupby("broad_episode_id"):
        w=g.episode_weight.astype(float)
        broad.append({
            "broad_episode_id":bid,
            "n_mechanical_cycles":len(g),
            "RT_IPT_YOY":float(np.average(g.RT_IPT_YOY,weights=w)),
            "CURVE_BP":float(np.average(g.CURVE_BP,weights=w)),
            "NFCI":float(np.average(g.NFCI,weights=w)),
            "GROWTH_CONTRACTION_SHARE":float(np.average(g.REALTIME_GROWTH_CONTRACTION.astype(float),weights=w)),
            "CURVE_INVERTED_SHARE":float(np.average(g.CURVE_INVERTED.astype(float),weights=w)),
            "NFCI_TIGHT_SHARE":float(np.average(g.FINANCIAL_CONDITIONS_TIGHT.astype(float),weights=w)),
            "PRE_CUT_STRESS_COUNT":float(np.average(g.PRE_CUT_STRESS_COUNT,weights=w)),
            "RISK3_MEDIAN_TROUGH_MONTH":float(np.average(g.RISK3_MEDIAN_TROUGH_MONTH,weights=w)),
            "RISK3_LATE_TROUGH_SHARE":float(np.average(g.RISK3_LATE_TROUGH_SHARE,weights=w)),
        })
    broad=pd.DataFrame(broad)
    broad.to_csv(OUT/"PRECUT_STATE_BROAD_PANEL.csv",index=False)

    share_map={
        "REALTIME_GROWTH_CONTRACTION":"GROWTH_CONTRACTION_SHARE",
        "CURVE_INVERTED":"CURVE_INVERTED_SHARE",
        "FINANCIAL_CONDITIONS_TIGHT":"NFCI_TIGHT_SHARE",
    }
    broad_contrasts=[]
    support_rows=[]
    for state_name,share_col in share_map.items():
        broad["STATE_VALUE"]=broad[share_col]>=0.5
        ntrue=int(broad.STATE_VALUE.sum())
        nfalse=int((~broad.STATE_VALUE).sum())
        if min(ntrue,nfalse)>=3:
            status="SUPPORTED_BALANCED_DESCRIPTIVE"
        elif min(ntrue,nfalse)>=2:
            status="LIMITED_BINARY_DESCRIPTIVE"
        else:
            status="INSUFFICIENT_STATE_VARIATION"
        support_rows.append({
            "state":state_name,
            "true_broad_episodes":ntrue,
            "false_broad_episodes":nfalse,
            "support_status":status,
        })
        for val in (False,True):
            g=broad[broad.STATE_VALUE==val]
            if len(g)==0: continue
            broad_contrasts.append({
                "state":state_name,
                "state_value":bool(val),
                "n_broad_episodes":int(len(g)),
                "support_status":status,
                "median_risk3_trough_month":float(g.RISK3_MEDIAN_TROUGH_MONTH.median()),
                "median_late_trough_share":float(g.RISK3_LATE_TROUGH_SHARE.median()),
                "mean_late_trough_share":float(g.RISK3_LATE_TROUGH_SHARE.mean()),
            })
    pd.DataFrame(support_rows).to_csv(OUT/"BINARY_STATE_SUPPORT.csv",index=False)
    contrasts=pd.DataFrame(broad_contrasts)
    contrasts.to_csv(OUT/"BINARY_STATE_CONTRASTS.csv",index=False)

    corr_rows=[]
    for outcome in ["RISK3_MEDIAN_TROUGH_MONTH","RISK3_LATE_TROUGH_SHARE"]:
        rho=rank_corr(broad.PRE_CUT_STRESS_COUNT,broad[outcome])
        loo=[]
        for bid in broad.broad_episode_id:
            z=broad[broad.broad_episode_id!=bid]
            loo.append(rank_corr(z.PRE_CUT_STRESS_COUNT,z[outcome]))
        finite=[x for x in loo if np.isfinite(x)]
        finite_consistent=bool(
            np.isfinite(rho)
            and len(finite)>0
            and all((x==0 and rho==0) or (x*rho>0) for x in finite)
        )
        corr_rows.append({
            "predictor":"PRE_CUT_STRESS_COUNT",
            "outcome":outcome,
            "n_broad_episodes":len(broad),
            "spearman_rho":rho,
            "loo_min_rho":min(finite) if finite else np.nan,
            "loo_max_rho":max(finite) if finite else np.nan,
            "loo_defined_count":len(finite),
            "loo_total_count":len(loo),
            "loo_all_defined":len(finite)==len(loo),
            "loo_finite_sign_consistent":finite_consistent,
            "pvalue_generated":False,
        })
    corr=pd.DataFrame(corr_rows)
    corr.to_csv(OUT/"BROAD_RANK_DIAGNOSTICS.csv",index=False)

    predictors={
        "FULL_COUNT":broad.GROWTH_CONTRACTION_SHARE+broad.CURVE_INVERTED_SHARE+broad.NFCI_TIGHT_SHARE,
        "DROP_GROWTH":broad.CURVE_INVERTED_SHARE+broad.NFCI_TIGHT_SHARE,
        "DROP_CURVE":broad.GROWTH_CONTRACTION_SHARE+broad.NFCI_TIGHT_SHARE,
        "DROP_NFCI":broad.GROWTH_CONTRACTION_SHARE+broad.CURVE_INVERTED_SHARE,
        "CURVE_ONLY":broad.CURVE_INVERTED_SHARE,
        "NFCI_ONLY":broad.NFCI_TIGHT_SHARE,
    }
    sens=[]
    for name,x in predictors.items():
        for outcome in ["RISK3_MEDIAN_TROUGH_MONTH","RISK3_LATE_TROUGH_SHARE"]:
            sens.append({
                "specification":name,
                "outcome":outcome,
                "spearman_rho":rank_corr(x,broad[outcome]),
                "post_run_diagnostic":True,
            })
    sensitivity_df=pd.DataFrame(sens)
    sensitivity_df.to_csv(OUT/"COMPONENT_SENSITIVITY.csv",index=False)

    hard_fail=timing_bad or current_bad
    qc={
        "qc_gate":"FAIL" if hard_fail else "PASS",
        "module":"FED-CYCLE-PRECUT-STATE-019",
        "mechanical_cycles":int(len(d)),
        "broad_episodes":int(d.broad_episode_id.nunique()),
        "risk_assets":RISK_ASSETS,
        "state_timing_violations":timing_bad,
        "current_2026_cycle_leak_violations":current_bad,
        "realtime_growth_rows":int(d.RT_IPT_YOY.notna().sum()),
        "pvalues_generated":False,
        "outcome_threshold_month":7,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# FED-CYCLE-PRECUT-STATE-019",
        "",
        "**PREDETERMINED PRE-CUT STATE DIAGNOSTIC / NO P-VALUES**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- mechanical cycles: {len(d)}",
        f"- broad episodes: {d.broad_episode_id.nunique()}",
        "",
        "## Independent broad-episode binary state support",
        "",
        pd.DataFrame(support_rows).to_markdown(index=False),
        "",
        "## Binary pre-cut state contrasts",
        "",
        contrasts.to_markdown(index=False),
        "",
        "## Broad-episode rank diagnostics",
        "",
        corr.to_markdown(index=False),
        "",
        "## Component sensitivity",
        "",
        sensitivity_df.to_markdown(index=False),
        "",
        "RT_IPT is real-time vintage. Curve/NFCI observations are strictly dated before FIRST_CUT.",
        "Binary evidence support is judged at the independent broad-episode level.",
        "This is a small-sample descriptive state diagnostic, not an OOS timing model.",
    ]
    (OUT/"FED_CYCLE_PRECUT_STATE_019_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-PRECUT-STATE-019 QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
