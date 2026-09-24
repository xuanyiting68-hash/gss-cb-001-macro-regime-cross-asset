#!/usr/bin/env python3
"""
HYG price-proxy audit for FED-CYCLE-ASIA-CREDIT-DIAG-006.

Reference:
research/FED_CYCLE_ASIA_CREDIT_DIAG_006_HY_PROXY_AMENDMENT.md
"""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_asia_credit_diag_v1"
OUT.mkdir(parents=True,exist_ok=True)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

BASE=load(ROOT/"scripts"/"run_fed_cycle_asia_credit_diag_v1.py","asia_credit_v1_hyg")

def main():
    cycles=BASE.STATE_MOD.assign_broad_clusters(BASE.STATE_MOD.load_cycles())
    raw,acq=BASE.PATH_MOD.fetch_yahoo_chart("HYG")
    monthly=BASE.monthly_average(raw)
    pmap=dict(zip(monthly["period"],monthly["value"].astype(float)))

    rows=[]
    for anchor,col in BASE.ANCHORS.items():
        available=[]
        for _,cyc in cycles.iterrows():
            dt=cyc[col]
            if pd.isna(dt): continue
            p,m=BASE.equity_path(pmap,dt)
            if p is not None:
                available.append((cyc,pd.Timestamp(dt),m))
        counts={}
        for cyc,_,_ in available:
            bid=cyc["broad_episode_id"]
            counts[bid]=counts.get(bid,0)+1
        for cyc,dt,m in available:
            bid=cyc["broad_episode_id"]
            rows.append({
                "anchor":anchor,
                "cycle_id":cyc["cycle_id"],
                "broad_episode_id":bid,
                "cycle_start_year":int(pd.Timestamp(cyc["first_hike"]).year),
                "anchor_date":dt,
                "episode_weight":1.0/counts[bid],
                **m
            })
    met=pd.DataFrame(rows)

    sums=[]
    for anchor,g in met.groupby("anchor"):
        w=g["episode_weight"].to_numpy(float)
        valid=g.dropna(subset=["mdd_trough_month"])
        nlegs=int(g["cycle_id"].nunique()); nbroad=int(g["broad_episode_id"].nunique())
        sums.append({
            "observable":"HYG_PRICE_PROXY",
            "anchor":anchor,
            "n_legs":nlegs,
            "n_broad_episodes":nbroad,
            "support_status":BASE.support_label(nlegs,nbroad),
            "weighted_median_ret_3m":BASE.weighted_quantile(g["ret_3m"],w,.5),
            "weighted_median_ret_6m":BASE.weighted_quantile(g["ret_6m"],w,.5),
            "weighted_median_ret_12m":BASE.weighted_quantile(g["ret_12m"],w,.5),
            "weighted_median_mdd_12m":BASE.weighted_quantile(g["mdd_12m"],w,.5),
            "weighted_median_mdd_trough_month":BASE.weighted_quantile(valid["mdd_trough_month"],valid["episode_weight"],.5) if len(valid) else np.nan,
            "weighted_late_trough_share_7_12":float(valid.loc[valid["mdd_trough_month"].between(7,12),"episode_weight"].sum()/valid["episode_weight"].sum()) if len(valid) else np.nan,
        })
    summary=pd.DataFrame(sums)

    weight_bad=0
    for (anchor,bid),g in met.groupby(["anchor","broad_episode_id"]):
        if abs(float(g["episode_weight"].sum())-1)>1e-10: weight_bad+=1
    canonical=cycles.set_index("cycle_id")
    anchor_bad=0
    for _,r in met.iterrows():
        if pd.Timestamp(r["anchor_date"])!=pd.Timestamp(canonical.loc[r["cycle_id"],BASE.ANCHORS[r["anchor"]]]):
            anchor_bad+=1
    mdd_bad=int((met["mdd_12m"]< -1e-12).sum())
    support_bad=0
    for _,r in summary.iterrows():
        if r["support_status"]!=BASE.support_label(int(r["n_legs"]),int(r["n_broad_episodes"])):
            support_bad+=1

    qc={
        "qc_gate":"PASS" if weight_bad==0 and anchor_bad==0 and mdd_bad==0 and support_bad==0 else "FAIL",
        "module":"FED-CYCLE-ASIA-CREDIT-DIAG-006-HYG-PROXY",
        "symbol":"HYG",
        "source_first_date":str(raw["date"].min().date()),
        "source_last_date":str(raw["date"].max().date()),
        "cycle_phase_rows":int(len(met)),
        "weight_violations":weight_bad,
        "anchor_violations":anchor_bad,
        "negative_mdd_violations":mdd_bad,
        "support_label_violations":support_bad,
        "raw_source_history_committed":False,
        "interpretation":"LIMITED_SUPPORT_HIGH_YIELD_PRICE_PROXY_NOT_OAS",
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }

    met.to_csv(OUT/"HYG_PROXY_CYCLE_PHASE_METRICS.csv",index=False)
    summary.to_csv(OUT/"HYG_PROXY_PHASE_SUMMARY.csv",index=False)
    pd.DataFrame([BASE.provenance_row("HYG_PRICE_PROXY","HYG","Yahoo Finance public chart history",raw,acq)]).to_csv(OUT/"HYG_PROXY_SOURCE.csv",index=False)
    (OUT/"HYG_PROXY_QC.json").write_text(json.dumps(qc,indent=2),encoding="utf-8")

    fig,ax=plt.subplots(figsize=(8.8,5.0))
    ax.bar(summary["anchor"],summary["weighted_median_mdd_12m"]*100)
    ax.set_title("HYG price proxy: median 12M MDD by Fed-cycle anchor")
    ax.set_ylabel("Weighted median MDD (%)")
    ax.tick_params(axis="x",rotation=20)
    fig.tight_layout()
    fig.savefig(OUT/"03_hyg_price_proxy_phase_mdd.png",dpi=170,bbox_inches="tight")
    plt.close(fig)

    report=[
      "# HYG price-proxy audit",
      "",
      "**LIMITED-SUPPORT PRICE-MARKET CONTEXT / NOT OAS / NOT CAUSAL / NOT DEPLOYABLE**",
      "",
      summary.to_markdown(index=False),
      "",
      "The FRED ICE BofA OAS history is currently truncated to the most recent three years; HYG is retained separately as a price proxy and is not pooled with OAS.",
    ]
    (OUT/"HYG_PROXY_AUDIT.md").write_text("\n".join(report),encoding="utf-8")
    if qc["qc_gate"]!="PASS": raise SystemExit("HYG proxy QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
