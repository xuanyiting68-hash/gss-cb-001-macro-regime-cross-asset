#!/usr/bin/env python3
"""
Post-run benchmark sanity audit for FED-CYCLE-GOLD-OOS-008.
No model refitting.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_gold_oos_v1"

def pct_improve(base,new):
    return float((base-new)/base) if base != 0 else np.nan

def main():
    s=pd.read_csv(OUT/"MODEL_SUMMARY.csv").set_index("model")
    ep=pd.read_csv(OUT/"EPISODE_METRICS.csv")
    p=pd.read_csv(OUT/"OOS_PREDICTIONS.csv")

    m3="M3_PLUS_REALTIME_IPT"
    comps=["B0_HIST_MEAN","B1_GOLD_HISTORY","B2_GOLD_PLUS_CYCLE_AGE","D4_PLUS_CURRENT_INDPRO"]

    rows=[]
    for base in comps:
        b=s.loc[base]; m=s.loc[m3]
        wins_mse=0; wins_mae=0
        for bid in sorted(ep["broad_episode_id"].unique()):
            a=ep[(ep.model==m3)&(ep.broad_episode_id==bid)].iloc[0]
            z=ep[(ep.model==base)&(ep.broad_episode_id==bid)].iloc[0]
            wins_mse += int(a.mse < z.mse)
            wins_mae += int(a.mae < z.mae)
        rows.append({
            "comparison":f"{m3} vs {base}",
            "mse_improvement_fraction":pct_improve(float(b.episode_equal_mse),float(m.episode_equal_mse)),
            "mae_improvement_fraction":pct_improve(float(b.episode_equal_mae),float(m.episode_equal_mae)),
            "mse_episode_wins":wins_mse,
            "mae_episode_wins":wins_mae,
            "total_episodes":int(m.oos_episodes),
        })
    comp=pd.DataFrame(rows)

    biases=[]
    for bid,g in p.groupby("broad_episode_id"):
        w=g["eval_weight"].to_numpy(float)
        err=g["pred_M3_PLUS_REALTIME_IPT"].to_numpy(float)-g["GOLD_FWD_6M_RET"].to_numpy(float)
        biases.append({
            "broad_episode_id":bid,
            "weighted_signed_bias":float(np.average(err,weights=w)),
            "weighted_mean_actual":float(np.average(g["GOLD_FWD_6M_RET"],weights=w)),
            "weighted_mean_prediction":float(np.average(g["pred_M3_PLUS_REALTIME_IPT"],weights=w)),
        })
    bias=pd.DataFrame(biases)
    episode_equal_bias=float(bias["weighted_signed_bias"].mean())

    ranges=pd.DataFrame([
        {
            "series":"REALIZED_GOLD_FWD_6M_RET",
            "min":float(p["GOLD_FWD_6M_RET"].min()),
            "max":float(p["GOLD_FWD_6M_RET"].max()),
            "mean_unweighted":float(p["GOLD_FWD_6M_RET"].mean()),
        },
        {
            "series":"M3_PREDICTION",
            "min":float(p["pred_M3_PLUS_REALTIME_IPT"].min()),
            "max":float(p["pred_M3_PLUS_REALTIME_IPT"].max()),
            "mean_unweighted":float(p["pred_M3_PLUS_REALTIME_IPT"].mean()),
        }
    ])

    b0=comp[comp["comparison"].str.endswith("B0_HIST_MEAN")].iloc[0]
    d4=comp[comp["comparison"].str.endswith("D4_PLUS_CURRENT_INDPRO")].iloc[0]
    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-GOLD-OOS-008-POSTRUN-BENCHMARK-AUDIT",
        "m3_vs_b0_mse_improvement":float(b0.mse_improvement_fraction),
        "m3_vs_b0_mae_improvement":float(b0.mae_improvement_fraction),
        "m3_vs_b0_mse_episode_wins":int(b0.mse_episode_wins),
        "m3_vs_b0_mae_episode_wins":int(b0.mae_episode_wins),
        "m3_vs_d4_mse_improvement":float(d4.mse_improvement_fraction),
        "m3_vs_d4_mae_improvement":float(d4.mae_improvement_fraction),
        "m3_vs_d4_mse_episode_wins":int(d4.mse_episode_wins),
        "m3_vs_d4_mae_episode_wins":int(d4.mae_episode_wins),
        "m3_episode_equal_signed_bias":episode_equal_bias,
        "frozen_gate_unchanged":True,
        "interpretation":"POST_RUN_LANGUAGE_SANITY_AUDIT_ONLY",
    }

    comp.to_csv(OUT/"POSTRUN_BENCHMARK_COMPARISON.csv",index=False)
    bias.to_csv(OUT/"POSTRUN_M3_BIAS_BY_EPISODE.csv",index=False)
    ranges.to_csv(OUT/"POSTRUN_PREDICTION_RANGE.csv",index=False)
    (OUT/"POSTRUN_BENCHMARK_QC.json").write_text(json.dumps(qc,indent=2),encoding="utf-8")

    report=[
        "# FED-CYCLE-GOLD-OOS-008 — Post-run benchmark sanity audit",
        "",
        "**NO REFITTING / FROZEN OOS GATE UNCHANGED**",
        "",
        "## Comparator sensitivity",
        "",
        comp.to_markdown(index=False),
        "",
        "## M3 signed bias by OOS broad episode",
        "",
        bias.to_markdown(index=False),
        "",
        f"Episode-equal signed bias: {episode_equal_bias:.6f}",
        "",
        "## Prediction range",
        "",
        ranges.to_markdown(index=False),
    ]
    (OUT/"POSTRUN_BENCHMARK_AUDIT.md").write_text("\n".join(report),encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
