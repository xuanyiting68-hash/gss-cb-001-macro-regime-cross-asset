#!/usr/bin/env python3
"""
FED-CYCLE-PHASE-CLOCK-004
Multi-anchor 12-month cross-asset phase clock.

Reference:
research/FED_CYCLE_PHASE_CLOCK_004_LOCK.md
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_phase_clock_v1"
OUT.mkdir(parents=True, exist_ok=True)

ANCHORS = {
    "FIRST_HIKE": "first_hike",
    "LAST_HIKE": "last_hike",
    "PAUSE_START": "pause_start",
    "FIRST_CUT": "first_cut",
}
PRIMARY_ASSETS = {"GOLD", "SP500", "NASDAQ", "WTI"}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


STATE_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py", "state_panel_v2_phase")
RISK_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_cross_asset_risk_clock_v1.py", "risk_clock_v1_phase")


def weighted_quantile(values, weights, q):
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    ok = np.isfinite(v) & np.isfinite(w) & (w > 0)
    v, w = v[ok], w[ok]
    if len(v) == 0:
        return np.nan
    order = np.argsort(v)
    v, w = v[order], w[order]
    c = np.cumsum(w) / np.sum(w)
    return float(v[np.searchsorted(c, q, side="left")])


def path_and_recovery(price_map, anchor_date):
    event_period = pd.Timestamp(anchor_date).to_period("M")
    baseline_period = event_period - 1
    post_periods = [event_period + k for k in range(1, 13)]
    needed = [baseline_period] + post_periods
    if any(p not in price_map for p in needed):
        return None, None

    baseline = float(price_map[baseline_period])
    post = np.array([float(price_map[p]) for p in post_periods], dtype=float)
    vals = np.concatenate([[baseline], post])
    cumret = post / baseline - 1.0

    running_mdd = []
    running_min = []
    new_low = []
    new_mdd = []
    prior_mdd = -1.0
    for k in range(1, 13):
        sub = vals[:k + 1]
        peaks = np.maximum.accumulate(sub)
        dd = 1.0 - sub / peaks
        rmdd = float(dd.max())
        running_mdd.append(rmdd)
        running_min.append(float(np.min(sub / baseline - 1.0)))
        new_low.append(bool(vals[k] < np.min(vals[:k]) - 1e-15))
        new_mdd.append(bool(rmdd > prior_mdd + 1e-15))
        prior_mdd = rmdd

    full_peaks = np.maximum.accumulate(vals)
    full_dd = 1.0 - vals / full_peaks
    mdd = float(full_dd.max())
    event_trough_month = int(np.argmin(post) + 1)

    recovery = {
        "recovery50_months": np.nan,
        "recovery100_months": np.nan,
        "recovery50_observed": False,
        "recovery100_observed": False,
        "recovery_censor_months": np.nan,
    }

    if mdd > 1e-15:
        trough_idx = int(np.argmax(full_dd))
        peak_idx = int(np.argmax(vals[:trough_idx + 1]))
        mdd_trough_month = int(trough_idx)
        peak_price = float(vals[peak_idx])
        trough_price = float(vals[trough_idx])
        threshold50 = trough_price + 0.5 * (peak_price - trough_price)
        threshold100 = peak_price

        trough_period = baseline_period if trough_idx == 0 else event_period + trough_idx
        rec = []
        for j in range(0, 61):
            p = trough_period + j
            if p in price_map:
                rec.append((j, float(price_map[p])))
        if rec:
            hit50 = [j for j, v in rec if v >= threshold50]
            hit100 = [j for j, v in rec if v >= threshold100]
            recovery = {
                "recovery50_months": int(hit50[0]) if hit50 else np.nan,
                "recovery100_months": int(hit100[0]) if hit100 else np.nan,
                "recovery50_observed": bool(hit50),
                "recovery100_observed": bool(hit100),
                "recovery_censor_months": int(rec[-1][0]),
            }
    else:
        mdd_trough_month = np.nan

    paths = []
    for k in range(1, 13):
        paths.append({
            "event_month": k,
            "cum_return": float(cumret[k - 1]),
            "running_mdd": float(running_mdd[k - 1]),
            "running_min_return": float(running_min[k - 1]),
            "new_event_low": bool(new_low[k - 1]),
            "new_running_mdd": bool(new_mdd[k - 1]),
        })

    metrics = {
        "baseline_period": str(baseline_period),
        "ret_3m": float(post[2] / baseline - 1.0),
        "ret_6m": float(post[5] / baseline - 1.0),
        "ret_12m": float(post[11] / baseline - 1.0),
        "mdd_12m": mdd,
        "mae_12m": float(np.min(vals / baseline - 1.0)),
        "mfe_12m": float(np.max(vals / baseline - 1.0)),
        "event_trough_month": event_trough_month,
        "mdd_trough_month": mdd_trough_month,
        **recovery,
    }
    return paths, metrics


def build_phase_paths(cycles, assets):
    paths = []
    metrics = []

    for anchor_name, col in ANCHORS.items():
        for asset, obj in assets.items():
            price_map = dict(zip(obj["df"]["period"], obj["df"]["value"].astype(float)))
            available = []

            for _, cyc in cycles.iterrows():
                dt = cyc[col]
                if pd.isna(dt):
                    continue
                p, m = path_and_recovery(price_map, dt)
                if p is None:
                    continue
                available.append((cyc, pd.Timestamp(dt), p, m))

            counts = {}
            for cyc, _, _, _ in available:
                bid = cyc["broad_episode_id"]
                counts[bid] = counts.get(bid, 0) + 1

            for cyc, dt, p, m in available:
                bid = cyc["broad_episode_id"]
                w = 1.0 / counts[bid]
                base = {
                    "asset": asset,
                    "asset_label": obj["label"],
                    "primary_asset": bool(obj["primary"]),
                    "anchor": anchor_name,
                    "cycle_id": cyc["cycle_id"],
                    "broad_episode_id": bid,
                    "cycle_start_year": int(pd.Timestamp(cyc["first_hike"]).year),
                    "anchor_date": dt,
                    "episode_weight": w,
                }
                for row in p:
                    paths.append({**base, **row})
                metrics.append({**base, **m})

    return pd.DataFrame(paths), pd.DataFrame(metrics)


def phase_summary(metrics):
    rows = []
    for (asset, anchor), g in metrics.groupby(["asset", "anchor"]):
        nlegs = int(g["cycle_id"].nunique())
        nbroad = int(g["broad_episode_id"].nunique())
        status = (
            "PRIMARY_SUPPORTED"
            if asset in PRIMARY_ASSETS and nlegs >= 5 and nbroad >= 4
            else "DIAGNOSTIC_LIMITED_SUPPORT"
        )

        valid = g.dropna(subset=["mdd_trough_month"]).copy()
        if len(valid):
            wv = valid["episode_weight"].to_numpy(float)
            early = float(valid.loc[valid["mdd_trough_month"].between(1, 3), "episode_weight"].sum() / wv.sum())
            mid = float(valid.loc[valid["mdd_trough_month"].between(4, 6), "episode_weight"].sum() / wv.sum())
            late = float(valid.loc[valid["mdd_trough_month"].between(7, 12), "episode_weight"].sum() / wv.sum())
            trough_med = weighted_quantile(valid["mdd_trough_month"], wv, 0.5)
        else:
            early = mid = late = trough_med = np.nan

        w = g["episode_weight"].to_numpy(float)
        rows.append({
            "asset": asset,
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "weighted_median_ret_3m": weighted_quantile(g["ret_3m"], w, 0.5),
            "weighted_median_ret_6m": weighted_quantile(g["ret_6m"], w, 0.5),
            "weighted_median_ret_12m": weighted_quantile(g["ret_12m"], w, 0.5),
            "weighted_median_mdd_12m": weighted_quantile(g["mdd_12m"], w, 0.5),
            "weighted_median_mae_12m": weighted_quantile(g["mae_12m"], w, 0.5),
            "weighted_median_mfe_12m": weighted_quantile(g["mfe_12m"], w, 0.5),
            "weighted_median_mdd_trough_month": trough_med,
            "mdd_trough_share_early_1_3": early,
            "mdd_trough_share_mid_4_6": mid,
            "mdd_trough_share_late_7_12": late,
            "support_status": status,
        })
    return pd.DataFrame(rows)


def path_summary(paths):
    rows = []
    for (asset, anchor, month), g in paths.groupby(["asset", "anchor", "event_month"]):
        w = g["episode_weight"].to_numpy(float)
        rows.append({
            "asset": asset,
            "anchor": anchor,
            "event_month": int(month),
            "n_legs": int(g["cycle_id"].nunique()),
            "n_broad_episodes": int(g["broad_episode_id"].nunique()),
            "weighted_median_cum_return": weighted_quantile(g["cum_return"], w, 0.5),
            "weighted_median_running_mdd": weighted_quantile(g["running_mdd"], w, 0.5),
            "weighted_q75_running_mdd": weighted_quantile(g["running_mdd"], w, 0.75),
            "weighted_new_event_low_share": float(np.average(g["new_event_low"].astype(float), weights=w)),
            "weighted_new_running_mdd_share": float(np.average(g["new_running_mdd"].astype(float), weights=w)),
        })
    return pd.DataFrame(rows)


def weighted_km(g, level):
    observed_col = f"recovery{level}_observed"
    duration_col = f"recovery{level}_months"
    d = g[g["mdd_12m"] > 1e-15].copy()
    if d.empty:
        return pd.DataFrame()

    d["duration"] = np.where(
        d[observed_col].astype(bool),
        pd.to_numeric(d[duration_col], errors="coerce"),
        pd.to_numeric(d["recovery_censor_months"], errors="coerce"),
    )
    d = d.dropna(subset=["duration"]).copy()
    d["duration"] = d["duration"].astype(int)

    surv = 1.0
    rows = [{
        "time_months": 0,
        "at_risk_weight": float(d["episode_weight"].sum()),
        "event_weight": 0.0,
        "censor_weight": 0.0,
        "survival_not_recovered": 1.0,
    }]
    for t in sorted(d["duration"].unique()):
        risk = float(d.loc[d["duration"] >= t, "episode_weight"].sum())
        ev = float(d.loc[(d["duration"] == t) & d[observed_col].astype(bool), "episode_weight"].sum())
        cens = float(d.loc[(d["duration"] == t) & (~d[observed_col].astype(bool)), "episode_weight"].sum())
        if risk > 0 and ev > 0:
            surv *= 1.0 - ev / risk
        rows.append({
            "time_months": int(t),
            "at_risk_weight": risk,
            "event_weight": ev,
            "censor_weight": cens,
            "survival_not_recovered": float(surv),
        })
    return pd.DataFrame(rows)


def recovery_outputs(metrics):
    curves = []
    summary = []
    for (asset, anchor), g in metrics.groupby(["asset", "anchor"]):
        for level in (50, 100):
            km = weighted_km(g, level)
            if km.empty:
                continue
            km["asset"] = asset
            km["anchor"] = anchor
            km["recovery_level"] = f"{level}%"
            curves.append(km)
            hit = km[km["survival_not_recovered"] <= 0.5 + 1e-12]
            median = int(hit.iloc[0]["time_months"]) if len(hit) else np.nan
            summary.append({
                "asset": asset,
                "anchor": anchor,
                "recovery_level": f"{level}%",
                "n_legs": int(g["cycle_id"].nunique()),
                "n_broad_episodes": int(g["broad_episode_id"].nunique()),
                "observed_recoveries": int(g[f"recovery{level}_observed"].astype(bool).sum()),
                "right_censored": int((~g[f"recovery{level}_observed"].astype(bool) & (g["mdd_12m"] > 1e-15)).sum()),
                "weighted_km_median_months": median,
            })
    curves_df = pd.concat(curves, ignore_index=True) if curves else pd.DataFrame()
    return curves_df, pd.DataFrame(summary)


def comparison_table(summary, recovery_summary):
    out = summary.copy()
    for level in ("50%", "100%"):
        z = recovery_summary[recovery_summary["recovery_level"] == level][
            ["asset", "anchor", "weighted_km_median_months"]
        ].rename(columns={"weighted_km_median_months": f"km_median_recovery_{level}"})
        out = out.merge(z, on=["asset", "anchor"], how="left")
    order = pd.CategoricalDtype(list(ANCHORS.keys()), ordered=True)
    out["anchor"] = out["anchor"].astype(order)
    return out.sort_values(["asset", "anchor"]).reset_index(drop=True)


def make_figures(pathsum, comparison):
    for asset in ["GOLD", "SP500", "NASDAQ", "WTI"]:
        g = pathsum[pathsum["asset"] == asset]
        if g.empty:
            continue
        fig, ax = plt.subplots(figsize=(9.8, 5.5))
        for anchor in ANCHORS:
            q = g[g["anchor"] == anchor]
            if len(q):
                ax.plot(q["event_month"], q["weighted_median_running_mdd"] * 100, label=anchor)
        ax.set_title(f"{asset}: 12M running-MDD phase clock")
        ax.set_xlabel("Complete months after anchor month")
        ax.set_ylabel("Weighted median running MDD (%)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT / f"01_{asset.lower()}_phase_running_mdd.png", dpi=170, bbox_inches="tight")
        plt.close(fig)

    supported = comparison[
        (comparison["support_status"] == "PRIMARY_SUPPORTED")
        & comparison["asset"].isin(["GOLD","SP500","NASDAQ","WTI"])
    ].copy()
    if len(supported):
        for asset in ["GOLD", "SP500", "NASDAQ", "WTI"]:
            g = supported[supported["asset"] == asset]
            if g.empty:
                continue
            fig, ax = plt.subplots(figsize=(8.8, 5.0))
            ax.bar(g["anchor"].astype(str), g["weighted_median_mdd_12m"] * 100)
            ax.set_title(f"{asset}: median 12M MDD by policy-cycle anchor")
            ax.set_ylabel("Weighted median MDD (%)")
            ax.tick_params(axis="x", rotation=20)
            fig.tight_layout()
            fig.savefig(OUT / f"02_{asset.lower()}_phase_mdd_comparison.png", dpi=170, bbox_inches="tight")
            plt.close(fig)


def write_report(comparison, qc):
    primary = comparison[comparison["support_status"] == "PRIMARY_SUPPORTED"].copy()
    lines = [
        "# FED-CYCLE-PHASE-CLOCK-004 — Report",
        "",
        "**DESCRIPTIVE PHASE TIMING / NOT CAUSAL / NOT A FORECASTING MODEL / NOT DEPLOYABLE**",
        "",
        "## QC",
        "",
        f"- QC gate: {qc['qc_gate']}",
        f"- primary supported cells: {qc['primary_supported_cells']}",
        "- common window: 12 complete months after each anchor month;",
        "- broad-episode weighting is recalculated within each asset × anchor cell;",
        "- no independent-sample cross-phase significance test is used.",
        "",
        "## Primary phase comparison",
        "",
        primary.to_markdown(index=False),
        "",
        "## Evidence boundary",
        "",
        "- Realized policy anchors are descriptive cycle markers.",
        "- The same cycle can contribute to multiple anchors and windows can overlap.",
        "- No p-value/FDR family is run.",
        "- OOS: not applicable.",
        "- Causality: none.",
        "- Deployment: none.",
    ]
    (OUT / "FED_CYCLE_PHASE_CLOCK_004_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    cycles = STATE_MOD.assign_broad_clusters(STATE_MOD.load_cycles())
    assets, prov = RISK_MOD.load_assets()

    paths, metrics = build_phase_paths(cycles, assets)
    summary = phase_summary(metrics)
    pathsum = path_summary(paths)
    km, recsum = recovery_outputs(metrics)
    comparison = comparison_table(summary, recsum)

    # QC.
    event_month_bad = int(((paths["event_month"] < 1) | (paths["event_month"] > 12)).sum())
    mdd_bad = int((pd.to_numeric(metrics["mdd_12m"], errors="coerce") < -1e-12).sum())
    mt = pd.to_numeric(metrics["mdd_trough_month"], errors="coerce")
    mdd_trough_bad = int((mt.notna() & ~mt.between(1, 12)).sum())

    both = metrics.dropna(subset=["recovery50_months", "recovery100_months"])
    recovery_bad = int((both["recovery100_months"] < both["recovery50_months"]).sum())

    weight_bad = 0
    for (asset, anchor, bid), g in metrics.groupby(["asset", "anchor", "broad_episode_id"]):
        if abs(float(g["episode_weight"].sum()) - 1.0) > 1e-10:
            weight_bad += 1

    unsupported_as_primary = int(
        (
            (summary["support_status"] == "PRIMARY_SUPPORTED")
            & ((summary["n_legs"] < 5) | (summary["n_broad_episodes"] < 4))
        ).sum()
    )

    # Canonical anchor dates are copied from the canonical cycle registry; assert no
    # unexpected anchor labels and that every metric anchor date matches the cycle row.
    canonical = cycles.set_index("cycle_id")
    anchor_date_bad = 0
    for _, r in metrics.iterrows():
        col = ANCHORS[r["anchor"]]
        expected = canonical.loc[r["cycle_id"], col]
        if pd.isna(expected) or pd.Timestamp(r["anchor_date"]) != pd.Timestamp(expected):
            anchor_date_bad += 1

    required_cells = 4 * 4
    primary_cells = summary[
        summary["asset"].isin(PRIMARY_ASSETS)
        & (summary["support_status"] == "PRIMARY_SUPPORTED")
    ]

    hard_fail = (
        event_month_bad != 0
        or mdd_bad != 0
        or mdd_trough_bad != 0
        or recovery_bad != 0
        or weight_bad != 0
        or unsupported_as_primary != 0
        or anchor_date_bad != 0
        or len(primary_cells) != required_cells
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-PHASE-CLOCK-004",
        "path_rows": int(len(paths)),
        "phase_asset_cycle_rows": int(len(metrics)),
        "primary_supported_cells": int(len(primary_cells)),
        "expected_primary_supported_cells": required_cells,
        "event_month_violations": event_month_bad,
        "negative_mdd_violations": mdd_bad,
        "mdd_trough_month_violations": mdd_trough_bad,
        "recovery_order_violations": recovery_bad,
        "broad_episode_weight_violations": weight_bad,
        "unsupported_as_primary": unsupported_as_primary,
        "canonical_anchor_date_violations": anchor_date_bad,
        "raw_source_histories_committed": False,
        "fdr_status": "NOT_APPLICABLE_DESCRIPTIVE_PHASE_MODULE",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    prov.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    paths.to_csv(OUT / "PHASE_PATHS.csv", index=False)
    metrics.to_csv(OUT / "PHASE_CYCLE_ASSET_METRICS.csv", index=False)
    pathsum.to_csv(OUT / "PHASE_PATH_SUMMARY.csv", index=False)
    summary.to_csv(OUT / "PHASE_TIMING_SUMMARY.csv", index=False)
    km.to_csv(OUT / "PHASE_RECOVERY_KM.csv", index=False)
    recsum.to_csv(OUT / "PHASE_RECOVERY_SUMMARY.csv", index=False)
    comparison.to_csv(OUT / "PHASE_COMPARISON.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    make_figures(pathsum, comparison)
    write_report(comparison, qc)

    if hard_fail:
        raise SystemExit("FED-CYCLE-PHASE-CLOCK-004 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
