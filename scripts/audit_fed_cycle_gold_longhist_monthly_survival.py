#!/usr/bin/env python3
"""
Survival audit for FED-CYCLE-GOLD-LONGHIST-MONTHLY-001.

Reads the frozen monthly Gold event metrics and applies Kaplan-Meier
right-censoring treatment to the already-defined 50%/100% recovery durations.

Reference:
research/FED_CYCLE_GOLD_LONGHIST_MONTHLY_001_RECOVERY_AMENDMENT.md
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gold_long_history_monthly_v1"
INPUT = OUT / "GOLD_MONTHLY_EVENT_METRICS.csv"


def km_curve(durations: pd.Series, observed: pd.Series) -> pd.DataFrame:
    d = pd.DataFrame({
        "duration": pd.to_numeric(durations, errors="coerce"),
        "observed": observed.astype(bool),
    }).dropna(subset=["duration"]).copy()

    if d.empty:
        return pd.DataFrame(
            columns=["time_months","at_risk","events","censored","survival_not_recovered"]
        )

    d["duration"] = d["duration"].astype(int)
    if (d["duration"] < 0).any():
        raise RuntimeError("Negative recovery duration")

    survival = 1.0
    rows = [{
        "time_months": 0,
        "at_risk": int(len(d)),
        "events": 0,
        "censored": 0,
        "survival_not_recovered": 1.0,
    }]

    for t in sorted(d["duration"].unique()):
        at_risk = int((d["duration"] >= t).sum())
        n_events = int(((d["duration"] == t) & d["observed"]).sum())
        n_censored = int(((d["duration"] == t) & (~d["observed"])).sum())
        if at_risk <= 0:
            raise RuntimeError("Invalid KM risk set")
        if n_events:
            survival *= 1.0 - n_events / at_risk
        rows.append({
            "time_months": int(t),
            "at_risk": at_risk,
            "events": n_events,
            "censored": n_censored,
            "survival_not_recovered": float(survival),
        })

    out = pd.DataFrame(rows)
    if (out["survival_not_recovered"].diff().dropna() > 1e-12).any():
        raise RuntimeError("KM survival is not monotone non-increasing")
    return out


def survival_at(curve: pd.DataFrame, landmark: int):
    eligible = curve[curve["time_months"] <= landmark]
    if eligible.empty:
        return np.nan
    return float(eligible.iloc[-1]["survival_not_recovered"])


def km_median(curve: pd.DataFrame):
    hit = curve[curve["survival_not_recovered"] <= 0.5 + 1e-12]
    if hit.empty:
        return np.nan
    return int(hit.iloc[0]["time_months"])


def main():
    if not INPUT.exists():
        raise RuntimeError(f"Missing input: {INPUT}")

    df = pd.read_csv(INPUT)
    required = {
        "event_type","mdd_24m","recovery_censor_months",
        "recovery50_months_from_trough","recovery50_observed",
        "recovery100_months_from_trough","recovery100_observed",
    }
    missing = required.difference(df.columns)
    if missing:
        raise RuntimeError(f"Missing required columns: {sorted(missing)}")

    # Identity check retained from the frozen recovery definition.
    both = df.dropna(
        subset=["recovery50_months_from_trough","recovery100_months_from_trough"]
    )
    recovery_order_bad = int(
        (
            pd.to_numeric(both["recovery100_months_from_trough"], errors="coerce")
            <
            pd.to_numeric(both["recovery50_months_from_trough"], errors="coerce")
        ).sum()
    )

    curve_rows = []
    summary_rows = []

    for event_type, g0 in df.groupby("event_type"):
        # A recovery risk set exists only where there is a positive MDD and
        # censoring support is available.
        g = g0[
            (pd.to_numeric(g0["mdd_24m"], errors="coerce") > 1e-12)
            & pd.to_numeric(g0["recovery_censor_months"], errors="coerce").notna()
        ].copy()

        for level in (50, 100):
            observed_col = f"recovery{level}_observed"
            recovery_col = f"recovery{level}_months_from_trough"

            observed = g[observed_col].astype(str).str.lower().map(
                {"true": True, "false": False}
            )
            if observed.isna().any():
                # pandas can read bools as bool dtype; support both.
                observed = g[observed_col].astype(bool)

            recovery_time = pd.to_numeric(g[recovery_col], errors="coerce")
            censor_time = pd.to_numeric(g["recovery_censor_months"], errors="coerce")
            duration = recovery_time.where(observed, censor_time)

            if observed.any() and recovery_time[observed].isna().any():
                raise RuntimeError(f"Observed recovery missing duration: {event_type} {level}%")
            if (~observed).any() and censor_time[~observed].isna().any():
                raise RuntimeError(f"Censored row missing censor time: {event_type} {level}%")

            curve = km_curve(duration, observed)
            curve["event_type"] = event_type
            curve["recovery_level"] = f"{level}%"
            curve_rows.append(curve)

            summary_rows.append({
                "event_type": event_type,
                "recovery_level": f"{level}%",
                "n_at_risk": int(len(g)),
                "observed_recoveries": int(observed.sum()),
                "right_censored": int((~observed).sum()),
                "km_median_months": km_median(curve),
                "survival_not_recovered_6m": survival_at(curve, 6),
                "survival_not_recovered_12m": survival_at(curve, 12),
                "survival_not_recovered_24m": survival_at(curve, 24),
                "survival_not_recovered_60m": survival_at(curve, 60),
                "max_followup_months": int(pd.to_numeric(duration, errors="coerce").max())
                if len(g) else np.nan,
            })

    curves = pd.concat(curve_rows, ignore_index=True) if curve_rows else pd.DataFrame()
    summary = pd.DataFrame(summary_rows)

    first50 = summary[
        (summary["event_type"] == "FIRST_HIKE")
        & (summary["recovery_level"] == "50%")
    ]
    first100 = summary[
        (summary["event_type"] == "FIRST_HIKE")
        & (summary["recovery_level"] == "100%")
    ]

    hard_fail = (
        recovery_order_bad != 0
        or len(first50) != 1
        or len(first100) != 1
        or int(first50.iloc[0]["n_at_risk"]) != 10
        or int(first50.iloc[0]["observed_recoveries"]) != 8
        or int(first50.iloc[0]["right_censored"]) != 2
        or int(first100.iloc[0]["n_at_risk"]) != 10
        or int(first100.iloc[0]["observed_recoveries"]) != 6
        or int(first100.iloc[0]["right_censored"]) != 4
        or int(first50.iloc[0]["km_median_months"]) != 8
        or int(first100.iloc[0]["km_median_months"]) != 19
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-GOLD-LONGHIST-MONTHLY-001-RECOVERY-SURVIVAL",
        "recovery_order_violations": recovery_order_bad,
        "first_hike_50_n": int(first50.iloc[0]["n_at_risk"]) if len(first50) else None,
        "first_hike_50_observed": int(first50.iloc[0]["observed_recoveries"]) if len(first50) else None,
        "first_hike_50_censored": int(first50.iloc[0]["right_censored"]) if len(first50) else None,
        "first_hike_50_km_median_months": int(first50.iloc[0]["km_median_months"]) if len(first50) else None,
        "first_hike_100_n": int(first100.iloc[0]["n_at_risk"]) if len(first100) else None,
        "first_hike_100_observed": int(first100.iloc[0]["observed_recoveries"]) if len(first100) else None,
        "first_hike_100_censored": int(first100.iloc[0]["right_censored"]) if len(first100) else None,
        "first_hike_100_km_median_months": int(first100.iloc[0]["km_median_months"]) if len(first100) else None,
        "evidence_status": "DESCRIPTIVE_RIGHT_CENSORING_AWARE_NOT_CAUSAL_NOT_DEPLOYABLE",
    }

    curves.to_csv(OUT / "RECOVERY_SURVIVAL_KM.csv", index=False)
    summary.to_csv(OUT / "RECOVERY_SURVIVAL_SUMMARY.csv", index=False)
    (OUT / "SURVIVAL_QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    # FIRST_HIKE 50% and 100% curves.
    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    for level in ("50%", "100%"):
        g = curves[
            (curves["event_type"] == "FIRST_HIKE")
            & (curves["recovery_level"] == level)
        ]
        ax.step(
            g["time_months"],
            g["survival_not_recovered"],
            where="post",
            label=level,
        )
    ax.set_ylim(0, 1.02)
    ax.set_xlim(0, 60)
    ax.set_title("Gold monthly recovery after FIRST_HIKE MDD trough")
    ax.set_xlabel("Months after MDD trough")
    ax.set_ylabel("Kaplan–Meier share not yet recovered")
    ax.legend(title="Recovery threshold")
    fig.tight_layout()
    fig.savefig(OUT / "03_gold_first_hike_recovery_survival.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    report = [
        "# Gold monthly recovery survival audit",
        "",
        "**DESCRIPTIVE / RIGHT-CENSORING AWARE / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        "Observed-only recovery medians are not used as the overall recovery-time summary.",
        "Kaplan–Meier estimates use the already-frozen recovery thresholds and 60-month search horizon.",
        "",
        "## FIRST_HIKE",
        "",
        summary[summary["event_type"] == "FIRST_HIKE"].to_markdown(index=False),
        "",
        "Interpretation:",
        "",
        "- 50% recovery: 8/10 observed and 2/10 right-censored; KM median = 8 months.",
        "- 100% recovery: 6/10 observed and 4/10 right-censored; KM median = 19 months.",
        "- These are historical descriptive recovery distributions, not forecasts.",
        "- No p-value/FDR family is executed; OOS is not applicable.",
    ]
    (OUT / "RECOVERY_SURVIVAL_AUDIT.md").write_text("\n".join(report), encoding="utf-8")

    if hard_fail:
        raise SystemExit("Recovery survival audit QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
