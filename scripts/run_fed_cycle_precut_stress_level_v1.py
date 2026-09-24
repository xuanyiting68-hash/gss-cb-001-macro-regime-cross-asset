#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P019 = ROOT / "results" / "fed_cycle_precut_state_v1" / "PRECUT_STATE_CYCLE_PANEL.csv"
Q019 = ROOT / "results" / "fed_cycle_precut_state_v1" / "QC.json"
M005 = ROOT / "results" / "fed_cycle_stress_layer_v1" / "STRESS_CYCLE_PHASE_METRICS.csv"
Q005 = ROOT / "results" / "fed_cycle_stress_layer_v1" / "QC.json"
OUT = ROOT / "results" / "fed_cycle_precut_stress_level_v1"
OUT.mkdir(parents=True, exist_ok=True)

PREDICTORS = ["BAA_SPREAD_LEVEL", "VIX_LEVEL", "CURVE_STRESS_BP", "GROWTH_STRESS"]
OUTCOMES = ["RISK3_MEDIAN_TROUGH_MONTH", "RISK3_LATE_TROUGH_SHARE"]

def rank_corr(x, y):
    x = pd.Series(x, dtype=float)
    y = pd.Series(y, dtype=float)
    if len(x) < 3 or x.nunique() < 2 or y.nunique() < 2:
        return np.nan
    return float(np.corrcoef(x.rank(method="average"), y.rank(method="average"))[0, 1])

def support_label(n):
    if n >= 6:
        return "SUPPORTED_EXPLORATORY"
    if n == 5:
        return "LIMITED_EXPLORATORY"
    return "INSUFFICIENT_SUPPORT"

def diagnostic(df, predictor, outcome, sample):
    z = df[[predictor, outcome, "broad_episode_id"]].dropna().copy()
    full = rank_corr(z[predictor], z[outcome])
    loo = []
    for bid in z["broad_episode_id"]:
        q = z[z["broad_episode_id"] != bid]
        loo.append(rank_corr(q[predictor], q[outcome]))
    finite = [v for v in loo if np.isfinite(v)]
    sign_ok = bool(
        np.isfinite(full)
        and finite
        and all((full == 0 and v == 0) or full * v > 0 for v in finite)
    )
    return {
        "sample": sample,
        "predictor": predictor,
        "outcome": outcome,
        "n_broad_episodes": len(z),
        "support_status": support_label(len(z)),
        "spearman_rho": full,
        "loo_defined_count": len(finite),
        "loo_total_count": len(loo),
        "loo_all_defined": len(finite) == len(loo),
        "loo_finite_sign_consistent": sign_ok,
        "loo_min_rho": min(finite) if finite else np.nan,
        "loo_max_rho": max(finite) if finite else np.nan,
        "max_abs_loo_change": max(abs(v - full) for v in finite)
        if finite and np.isfinite(full) else np.nan,
        "pvalue_generated": False,
    }

def main():
    if json.loads(Q019.read_text())["qc_gate"] != "PASS":
        raise RuntimeError("019 upstream QC not PASS")
    if json.loads(Q005.read_text())["qc_gate"] != "PASS":
        raise RuntimeError("005 upstream QC not PASS")

    d = pd.read_csv(P019)
    x = d[
        [
            "cycle_id", "broad_episode_id", "first_cut", "episode_weight",
            "RISK3_MEDIAN_TROUGH_MONTH", "RISK3_LATE_TROUGH_SHARE",
            "CURVE_BP", "RT_IPT_YOY",
        ]
    ].copy()
    x["CURVE_STRESS_BP"] = -pd.to_numeric(x.pop("CURVE_BP"), errors="coerce")
    x["GROWTH_STRESS"] = -pd.to_numeric(x.pop("RT_IPT_YOY"), errors="coerce")

    m = pd.read_csv(M005)
    m = m[
        (m["anchor"] == "FIRST_CUT")
        & m["observable"].isin(["BAA10Y_SPREAD", "VIX"])
    ].copy()

    levels = m.pivot(index="cycle_id", columns="observable", values="baseline_value").rename(
        columns={"BAA10Y_SPREAD": "BAA_SPREAD_LEVEL", "VIX": "VIX_LEVEL"}
    )
    dates = m.pivot(index="cycle_id", columns="observable", values="anchor_date").rename(
        columns={"BAA10Y_SPREAD": "BAA_ANCHOR_DATE", "VIX": "VIX_ANCHOR_DATE"}
    )
    x = x.merge(levels, left_on="cycle_id", right_index=True, how="left", validate="one_to_one")
    x = x.merge(dates, left_on="cycle_id", right_index=True, how="left", validate="one_to_one")

    if len(x) != 8 or x["broad_episode_id"].nunique() != 6:
        raise RuntimeError("020 support frame changed")
    if (x["first_cut"].astype(str).str[:4].astype(int) >= 2026).any():
        raise RuntimeError("2026 live-cycle leakage")
    if (x["BAA_ANCHOR_DATE"].astype(str) != x["first_cut"].astype(str)).any():
        raise RuntimeError("BAA anchor mismatch")
    if (
        x["VIX_ANCHOR_DATE"].notna()
        & (x["VIX_ANCHOR_DATE"].astype(str) != x["first_cut"].astype(str))
    ).any():
        raise RuntimeError("VIX anchor mismatch")

    x.to_csv(OUT / "PRECUT_STRESS_LEVEL_CYCLE_PANEL.csv", index=False)

    rows = []
    for bid, g in x.groupby("broad_episode_id"):
        w = pd.to_numeric(g["episode_weight"], errors="coerce")
        row = {
            "broad_episode_id": bid,
            "n_mechanical_cycles": len(g),
            "RISK3_MEDIAN_TROUGH_MONTH": float(
                np.average(g["RISK3_MEDIAN_TROUGH_MONTH"], weights=w)
            ),
            "RISK3_LATE_TROUGH_SHARE": float(
                np.average(g["RISK3_LATE_TROUGH_SHARE"], weights=w)
            ),
        }
        for p in PREDICTORS:
            ok = g[p].notna()
            row[p] = float(np.average(g.loc[ok, p], weights=w[ok])) if ok.any() else np.nan
        rows.append(row)

    broad = pd.DataFrame(rows).sort_values("broad_episode_id")
    broad.to_csv(OUT / "PRECUT_STRESS_LEVEL_BROAD_PANEL.csv", index=False)

    full = pd.DataFrame(
        [
            diagnostic(broad, p, o, "FULL_AVAILABLE")
            for p in PREDICTORS
            for o in OUTCOMES
        ]
    )
    full.to_csv(OUT / "CONTINUOUS_RANK_DIAGNOSTICS.csv", index=False)

    common = broad[broad["VIX_LEVEL"].notna()].copy()
    common_diag = pd.DataFrame(
        [
            diagnostic(common, p, o, "VIX_COMMON_SAMPLE")
            for p in ["BAA_SPREAD_LEVEL", "CURVE_STRESS_BP", "GROWTH_STRESS"]
            for o in OUTCOMES
        ]
    )
    common_diag.to_csv(OUT / "VIX_COMMON_SAMPLE_AUDIT.csv", index=False)

    qc = {
        "qc_gate": "PASS",
        "module": "FED-CYCLE-PRECUT-STRESS-LEVEL-020",
        "mechanical_cycles": int(len(x)),
        "broad_episodes": int(broad["broad_episode_id"].nunique()),
        "vix_broad_episodes": int(common["broad_episode_id"].nunique()),
        "predictor_set": PREDICTORS,
        "outcome_set": OUTCOMES,
        "current_2026_cycle_leak_violations": 0,
        "baa_anchor_mismatch_violations": 0,
        "vix_anchor_mismatch_violations": 0,
        "late_share_unique_values_full_sample": int(
            broad["RISK3_LATE_TROUGH_SHARE"].nunique()
        ),
        "late_share_unique_values_vix_common_sample": int(
            common["RISK3_LATE_TROUGH_SHARE"].nunique()
        ),
        "pvalues_generated": False,
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
        "branch_decision": "STOP_SMALL_SAMPLE_TIMING_RULE_BRANCH",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# FED-CYCLE-PRECUT-STRESS-LEVEL-020",
        "",
        "**EXPLORATORY CONTINUOUS PRE-CUT LEVEL DIAGNOSTIC / SIMPLE CONTINUOUS RULE NOT SUPPORTED**",
        "",
        "## Full available-sample diagnostics",
        "",
        full.to_markdown(index=False),
        "",
        "## VIX common-sample audit",
        "",
        common_diag.to_markdown(index=False),
        "",
        "Late-trough share has only two unique full-sample values and is constant in the VIX-supported sample.",
        "No p-values, optimized thresholds, new predictors, composites or fitted multivariate models are generated.",
        "",
        "**Boundary: exploratory mechanism-hypothesis only; not causal, not OOS and not deployable.**",
    ]
    (OUT / "FED_CYCLE_PRECUT_STRESS_LEVEL_020_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

if __name__ == "__main__":
    main()
