#!/usr/bin/env python3
"""
Post-run secondary-family multiplicity and USD robustness audit for
FED-CYCLE-STATE-PANEL-002.

Reference:
research/FED_CYCLE_STATE_PANEL_002_USD_DIAGNOSTIC.md
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_state_panel_v2"
PANEL_FILE = OUT / "MONTHLY_STATE_PANEL.csv"
SECONDARY_FILE = OUT / "SECONDARY_DIAGNOSTICS.csv"
RUNNER = ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("fed_cycle_state_panel_v2", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def fdr_adjust_with_total_m(pvals, total_m, by=False):
    idx = [i for i, p in enumerate(pvals) if np.isfinite(p)]
    out = [np.nan] * len(pvals)
    if not idx:
        return out

    ordered = sorted(idx, key=lambda i: pvals[i])
    c_m = sum(1.0 / k for k in range(1, total_m + 1)) if by else 1.0
    raw = []
    for rank, i in enumerate(ordered, start=1):
        raw.append(min(1.0, float(pvals[i]) * total_m * c_m / rank))
    adj = raw[:]
    for j in range(len(adj) - 2, -1, -1):
        adj[j] = min(adj[j], adj[j + 1])
    for i, q in zip(ordered, adj):
        out[i] = q
    return out


def estimate_subset(mod, panel, label):
    core = mod.regression_core(panel, "USD_6M_RET", "GOLD_FWD_6M_RET")
    if core is None:
        return {
            "restriction": label, "n_rows": 0, "n_cycles": 0,
            "n_broad_clusters": 0, "beta_per_1sd_within": np.nan,
            "p_broad_exact": np.nan, "p_mechanical_exact": np.nan,
            "status": "INSUFFICIENT_SUPPORT",
        }

    supported = core["n_cycles"] >= 5 and core["n_broad_clusters"] >= 4
    return {
        "restriction": label,
        "n_rows": core["n_rows"],
        "n_cycles": core["n_cycles"],
        "n_broad_clusters": core["n_broad_clusters"],
        "beta_per_1sd_within": core["beta"],
        "p_broad_exact": mod.exact_signflip_p(core["broad_scores"].to_numpy()) if supported else np.nan,
        "p_mechanical_exact": mod.exact_signflip_p(core["mech_scores"].to_numpy()) if supported else np.nan,
        "status": "SUPPORTED_DIAGNOSTIC" if supported else "INSUFFICIENT_SUPPORT",
    }


def main():
    mod = load_runner()
    panel = pd.read_csv(
        PANEL_FILE,
        parse_dates=["panel_month_start", "first_hike", "first_cut"],
    )
    secondary = pd.read_csv(SECONDARY_FILE)

    if len(secondary) != 12:
        raise RuntimeError(f"Expected 12 predeclared secondary tests, got {len(secondary)}")

    pvals = pd.to_numeric(secondary["p_broad_exact"], errors="coerce").tolist()
    secondary["bh_q_secondary_audit"] = fdr_adjust_with_total_m(pvals, total_m=12, by=False)
    secondary["by_q_secondary_audit"] = fdr_adjust_with_total_m(pvals, total_m=12, by=True)
    secondary["secondary_bh_fdr10_status"] = np.where(
        secondary["bh_q_secondary_audit"].notna()
        & (secondary["bh_q_secondary_audit"] <= 0.10),
        "BH_FDR10_SURVIVOR_DIAGNOSTIC",
        np.where(secondary["p_broad_exact"].notna(), "NO_BH_FDR10", "INSUFFICIENT_SUPPORT"),
    )
    secondary["secondary_by_fdr10_status"] = np.where(
        secondary["by_q_secondary_audit"].notna()
        & (secondary["by_q_secondary_audit"] <= 0.10),
        "BY_FDR10_SURVIVOR_DIAGNOSTIC",
        np.where(secondary["p_broad_exact"].notna(), "NO_BY_FDR10", "INSUFFICIENT_SUPPORT"),
    )

    restrictions = [
        ("FULL_SAMPLE", panel),
        ("EXCLUDE_2022_MODERN_USD_SOURCE", panel[panel["cycle_start_year"] < 2022].copy()),
        ("POST_1994_CYCLES_ONLY", panel[panel["cycle_start_year"] >= 1994].copy()),
        ("EXCLUDE_EARLY_B01_B02", panel[~panel["broad_episode_id"].isin(["B01", "B02"])].copy()),
    ]
    robust = pd.DataFrame(
        [estimate_subset(mod, sub, label) for label, sub in restrictions]
    )

    full_secondary = secondary[
        (secondary["predictor"] == "USD_6M_RET")
        & (secondary["outcome"] == "GOLD_FWD_6M_RET")
    ]
    if len(full_secondary) != 1:
        raise RuntimeError("USD full-sample secondary row missing or duplicated")

    expected_beta = float(full_secondary.iloc[0]["beta_per_1sd_within"])
    expected_p = float(full_secondary.iloc[0]["p_broad_exact"])
    full_row = robust[robust["restriction"] == "FULL_SAMPLE"].iloc[0]
    beta_match = bool(abs(float(full_row["beta_per_1sd_within"]) - expected_beta) < 1e-12)
    p_match = bool(abs(float(full_row["p_broad_exact"]) - expected_p) < 1e-12)

    supported = robust[robust["status"] == "SUPPORTED_DIAGNOSTIC"].copy()
    signs = np.sign(pd.to_numeric(supported["beta_per_1sd_within"], errors="coerce"))
    restriction_sign_stable = bool(len(signs) and (signs == signs.iloc[0]).all() and signs.iloc[0] != 0)

    qc = {
        "qc_gate": "PASS" if beta_match and p_match and len(secondary) == 12 else "FAIL",
        "module": "FED-CYCLE-STATE-PANEL-002-USD-DIAGNOSTIC",
        "secondary_family_size": int(len(secondary)),
        "secondary_bh_fdr10_survivors": int(
            (secondary["secondary_bh_fdr10_status"] == "BH_FDR10_SURVIVOR_DIAGNOSTIC").sum()
        ),
        "secondary_by_fdr10_survivors": int(
            (secondary["secondary_by_fdr10_status"] == "BY_FDR10_SURVIVOR_DIAGNOSTIC").sum()
        ),
        "usd_full_beta_matches_original": beta_match,
        "usd_full_p_matches_original": p_match,
        "usd_restriction_sign_stable": restriction_sign_stable,
        "interpretation": "POST_RUN_HYPOTHESIS_GENERATING_DIAGNOSTIC_ONLY",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    secondary.to_csv(OUT / "SECONDARY_MULTIPLICITY_AUDIT.csv", index=False)
    robust.to_csv(OUT / "USD_ROBUSTNESS_AUDIT.csv", index=False)
    (OUT / "USD_DIAGNOSTIC_QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    usd_mult = secondary[
        (secondary["predictor"] == "USD_6M_RET")
        & (secondary["outcome"] == "GOLD_FWD_6M_RET")
    ]

    report = [
        "# FED-CYCLE-STATE-PANEL-002 — USD secondary diagnostic",
        "",
        "**POST-RUN / HYPOTHESIS-GENERATING / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        "## Secondary-family multiplicity",
        "",
        f"- Predeclared secondary tests: {len(secondary)}",
        f"- BH-FDR 10% diagnostic survivors: {qc['secondary_bh_fdr10_survivors']}",
        f"- BY-FDR 10% diagnostic survivors: {qc['secondary_by_fdr10_survivors']}",
        "",
        "USD full-sample row with secondary-family adjustments:",
        "",
        usd_mult.to_markdown(index=False),
        "",
        "## USD source/era restrictions",
        "",
        robust.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- The unadjusted USD exact p-value is a secondary diagnostic and does not survive family-level multiplicity control if the audit reports zero survivors.",
        "- Sign stability across restrictions may retain USD as a mechanism candidate, but cannot establish a driver ranking.",
        "- Within-cycle fixed effects reduce the perfect event-level era separation seen in STATE-001, but they do not create causal identification.",
        "- No forecasting/OOS or deployment claim is made.",
    ]
    (OUT / "USD_SECONDARY_DIAGNOSTIC.md").write_text("\n".join(report), encoding="utf-8")

    if qc["qc_gate"] != "PASS":
        raise SystemExit("USD diagnostic QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
