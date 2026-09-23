#!/usr/bin/env python3
"""
Post-run confounding diagnostic for FED-CYCLE-STATE-001.

Adds the USD contrast already permitted by the frozen lock after the source-
bridge/support gate passed, and audits chronological separation of state groups.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_state_v1"
PANEL = OUT / "STATE_EVENT_PANEL.csv"
CONTRASTS = OUT / "STATE_CONTRASTS.csv"
QC = OUT / "QC.json"

PRIMARY_STATE_ORIENTATION = {
    "INFLATION_LEVEL": ("HIGH", "LOW_OR_MODERATE"),
    "INFLATION_DIRECTION": ("RISING", "FALLING_OR_FLAT"),
    "GROWTH_STATE": ("STRONG", "WEAK"),
    "YIELD_CURVE_STATE": ("INVERTED", "POSITIVE"),
    "REAL_RATE_PROXY_STATE": ("POSITIVE", "NONPOSITIVE"),
    "ENERGY_DIRECTION_STATE": ("RISING", "FALLING_OR_FLAT"),
    "NFCI_STATE": ("TIGHT", "LOOSE_OR_AVERAGE"),
}
USD_STATE = ("USD_DIRECTION_DIAGNOSTIC", "RISING", "FALLING_OR_FLAT")
OUTCOMES = ["gold_ret_12m", "gold_mdd_24m"]


def median(x):
    x = pd.to_numeric(x, errors="coerce").dropna()
    return float(x.median()) if len(x) else np.nan


def contrast(panel, state_var, a, b, outcome):
    ga = panel[panel[state_var] == a]
    gb = panel[panel[state_var] == b]
    na, nb = len(ga), len(gb)
    ma, mb = median(ga[outcome]), median(gb[outcome])
    supported = na >= 3 and nb >= 3
    return {
        "state_var": state_var,
        "state_a": a,
        "state_b": b,
        "outcome": outcome,
        "n_a": na,
        "n_b": nb,
        "median_a": ma,
        "median_b": mb,
        "oriented_median_diff_a_minus_b": ma - mb if supported else np.nan,
        "status": "SUPPORTED_DESCRIPTIVE" if supported else "INSUFFICIENT_SUPPORT",
    }


def loo(panel, state_var, a, b, outcome, full_diff):
    full_sign = int(np.sign(full_diff)) if np.isfinite(full_diff) else 0
    rows = []
    for cycle in panel["cycle_id"].unique():
        sub = panel[panel["cycle_id"] != cycle]
        r = contrast(sub, state_var, a, b, outcome)
        if r["status"] != "SUPPORTED_DESCRIPTIVE":
            continue
        diff = float(r["oriented_median_diff_a_minus_b"])
        rows.append({
            "dropped_cycle_id": cycle,
            "loo_diff": diff,
            "loo_sign": int(np.sign(diff)),
            "same_sign": bool(full_sign != 0 and np.sign(diff) == full_sign),
        })
    stable = bool(rows) and full_sign != 0 and all(r["same_sign"] for r in rows)
    return rows, stable


def temporal_audit(panel, state_var, a, b):
    ga = panel[panel[state_var] == a].copy()
    gb = panel[panel[state_var] == b].copy()
    years_a = sorted(ga["cycle_start_year"].astype(int).tolist())
    years_b = sorted(gb["cycle_start_year"].astype(int).tolist())
    if not years_a or not years_b:
        perfect = False
        direction = ""
    else:
        a_before_b = max(years_a) < min(years_b)
        b_before_a = max(years_b) < min(years_a)
        perfect = bool(a_before_b or b_before_a)
        direction = (
            "A_ALL_BEFORE_B" if a_before_b
            else "B_ALL_BEFORE_A" if b_before_a
            else "OVERLAPPING_ERAS"
        )
    return {
        "state_var": state_var,
        "state_a": a,
        "state_b": b,
        "n_a": len(ga),
        "n_b": len(gb),
        "years_a": ";".join(map(str, years_a)),
        "years_b": ";".join(map(str, years_b)),
        "min_year_a": min(years_a) if years_a else np.nan,
        "max_year_a": max(years_a) if years_a else np.nan,
        "min_year_b": min(years_b) if years_b else np.nan,
        "max_year_b": max(years_b) if years_b else np.nan,
        "perfect_time_separation": perfect,
        "time_separation_direction": direction,
    }


def main():
    panel = pd.read_csv(PANEL, parse_dates=["event_date"])
    frozen = pd.read_csv(CONTRASTS)
    qc = json.loads(QC.read_text(encoding="utf-8"))

    if qc.get("qc_gate") != "PASS":
        raise RuntimeError("STATE-001 base QC is not PASS")
    if float(qc.get("usd_bridge_sign_agreement", 0)) < 0.90:
        raise RuntimeError("Frozen USD bridge gate did not pass")
    if not bool(qc.get("usd_primary_promotable")):
        raise RuntimeError("Frozen USD support gate did not pass")

    # USD contrasts permitted by the frozen source/support rule.
    usd_rows = []
    usd_loo_rows = []
    for outcome in OUTCOMES:
        r = contrast(panel, *USD_STATE, outcome)
        usd_rows.append(r)
        if r["status"] == "SUPPORTED_DESCRIPTIVE":
            detail, stable = loo(
                panel, USD_STATE[0], USD_STATE[1], USD_STATE[2],
                outcome, r["oriented_median_diff_a_minus_b"]
            )
            for d in detail:
                d.update({"state_var": USD_STATE[0], "outcome": outcome})
            usd_loo_rows.extend(detail)
            r["loo_sign_stable"] = stable
        else:
            r["loo_sign_stable"] = False

    usd_df = pd.DataFrame(usd_rows)
    usd_loo = pd.DataFrame(usd_loo_rows)

    # Chronological separation audit for all frozen primary states and USD.
    temporal_rows = []
    for state_var, (a, b) in PRIMARY_STATE_ORIENTATION.items():
        temporal_rows.append(temporal_audit(panel, state_var, a, b))
    temporal_rows.append(temporal_audit(panel, *USD_STATE))
    temporal = pd.DataFrame(temporal_rows)

    # Exact support map.
    support_rows = []
    for state_var, (a, b) in PRIMARY_STATE_ORIENTATION.items():
        for label in (a, b):
            g = panel[panel[state_var] == label]
            support_rows.append({
                "state_var": state_var,
                "state": label,
                "n": int(len(g)),
                "cycle_years": ";".join(map(str, sorted(g["cycle_start_year"].astype(int).tolist()))),
            })
    for label in USD_STATE[1:]:
        g = panel[panel[USD_STATE[0]] == label]
        support_rows.append({
            "state_var": USD_STATE[0],
            "state": label,
            "n": int(len(g)),
            "cycle_years": ";".join(map(str, sorted(g["cycle_start_year"].astype(int).tolist()))),
        })
    support = pd.DataFrame(support_rows)

    usd_time = temporal[temporal["state_var"] == USD_STATE[0]].iloc[0]
    hard_fail = (
        (usd_df["status"] != "SUPPORTED_DESCRIPTIVE").any()
        or int(usd_df.iloc[0]["n_a"]) < 3
        or int(usd_df.iloc[0]["n_b"]) < 3
        or not bool(usd_time["perfect_time_separation"])
    )

    diag_qc = {
        "qc_gate": "PASS" if not hard_fail else "FAIL",
        "module": "FED-CYCLE-STATE-001-CONFOUNDING-DIAGNOSTIC",
        "usd_bridge_sign_agreement": float(qc["usd_bridge_sign_agreement"]),
        "usd_n_rising": int((panel[USD_STATE[0]] == "RISING").sum()),
        "usd_n_falling_or_flat": int((panel[USD_STATE[0]] == "FALLING_OR_FLAT").sum()),
        "usd_perfect_time_separation": bool(usd_time["perfect_time_separation"]),
        "usd_time_separation_direction": usd_time["time_separation_direction"],
        "usd_interpretation": "ERA_CONFOUNDED_DESCRIPTIVE_DIAGNOSTIC",
        "causal_status": "NONE",
        "fdr_status": "NOT_RUN",
    }

    usd_df.to_csv(OUT / "USD_STATE_CONTRASTS.csv", index=False)
    usd_loo.to_csv(OUT / "USD_STATE_LOO_DETAIL.csv", index=False)
    temporal.to_csv(OUT / "STATE_TEMPORAL_CONFOUNDING_AUDIT.csv", index=False)
    support.to_csv(OUT / "STATE_SUPPORT_MAP.csv", index=False)
    (OUT / "CONFOUNDING_QC.json").write_text(json.dumps(diag_qc, indent=2), encoding="utf-8")

    report = [
        "# FED-CYCLE-STATE-001 — Confounding diagnostic",
        "",
        "**DESCRIPTIVE / ASSOCIATIONAL DIAGNOSTIC / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        "## USD frozen-gate result",
        "",
        usd_df.to_markdown(index=False),
        "",
        "## Chronological-separation audit",
        "",
        temporal.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        f"- USD bridge sign agreement: {qc['usd_bridge_sign_agreement']:.2%}.",
        f"- USD FIRST_HIKE support: {diag_qc['usd_n_rising']} rising vs {diag_qc['usd_n_falling_or_flat']} falling/flat.",
        f"- Perfect chronological separation: {diag_qc['usd_perfect_time_separation']} ({diag_qc['usd_time_separation_direction']}).",
        "- Therefore the USD contrast is severely era-confounded in this event sample and cannot establish USD as a Gold driver.",
        "- No state is ranked as dominant.",
        "- No p-values/FDR are run; leave-one-leg-out sign stability remains a fragility diagnostic only.",
    ]
    (OUT / "STATE_CONFOUNDING_DIAGNOSTIC.md").write_text("\n".join(report), encoding="utf-8")

    if hard_fail:
        raise SystemExit("STATE confounding diagnostic hard gate failed")

    print(json.dumps(diag_qc, indent=2))


if __name__ == "__main__":
    main()
