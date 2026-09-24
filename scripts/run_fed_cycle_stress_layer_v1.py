#!/usr/bin/env python3
"""
FED-CYCLE-STRESS-LAYER-005
VIX x Baa-10Y credit spread x Copper phase diagnostics.

Reference:
research/FED_CYCLE_STRESS_LAYER_005_LOCK.md
"""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_stress_layer_v1"
OUT.mkdir(parents=True, exist_ok=True)

ANCHORS = {
    "FIRST_HIKE": "first_hike",
    "LAST_HIKE": "last_hike",
    "PAUSE_START": "pause_start",
    "FIRST_CUT": "first_cut",
}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


STATE_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py", "state_panel_v2_stress")


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


def source_row(series_id, label, df, acq):
    return {
        "series_id": series_id,
        "label": label,
        "url": acq["url"],
        "acquisition_method": acq["acquisition_method"],
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": acq["sha256"],
        "raw_bytes": acq["raw_bytes"],
        "rows_total": int(len(df)),
        "rows_nonmissing": int(df["value"].notna().sum()),
        "first_date": str(df["date"].min().date()) if len(df) else "",
        "last_date": str(df["date"].max().date()) if len(df) else "",
        "raw_committed": False,
    }


def load_sources():
    prov = []

    vix, a = STATE_MOD.fetch_fred("VIXCLS")
    prov.append(source_row("VIXCLS", "CBOE VIX via FRED", vix, a))
    v = vix.dropna(subset=["value"]).copy()
    v["period"] = v["date"].dt.to_period("M")
    vix_monthly = v.groupby("period").agg(
        vix_avg=("value", "mean"),
        vix_max=("value", "max"),
        n_daily=("value", "size"),
    ).reset_index()

    baa, a = STATE_MOD.fetch_fred("BAA10YM")
    prov.append(source_row("BAA10YM", "Moody's Baa minus 10Y Treasury via FRED", baa, a))
    b = baa.dropna(subset=["value"]).copy()
    b["period"] = b["date"].dt.to_period("M")
    baa_monthly = b.groupby("period", as_index=False)["value"].last().rename(columns={"value": "spread_pp"})

    copper, a = STATE_MOD.fetch_fred("PCOPPUSDM")
    prov.append(source_row("PCOPPUSDM", "Global price of Copper via FRED", copper, a))
    cp = copper.dropna(subset=["value"]).copy()
    cp["period"] = cp["date"].dt.to_period("M")
    copper_monthly = cp.groupby("period", as_index=False)["value"].last().rename(columns={"value": "copper_price"})

    return vix_monthly, baa_monthly, copper_monthly, pd.DataFrame(prov)


def vix_metrics(vmap, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    baseline_p = ep - 1
    posts = [ep + k for k in range(1, 13)]
    if baseline_p not in vmap or any(p not in vmap for p in posts):
        return None, None

    base_avg, _ = vmap[baseline_p]
    avgs = np.array([vmap[p][0] for p in posts], dtype=float)
    maxs = np.array([vmap[p][1] for p in posts], dtype=float)
    changes = avgs - base_avg
    peak_idx = int(np.argmax(changes))

    paths = [{
        "event_month": k + 1,
        "value": float(avgs[k]),
        "secondary_value": float(maxs[k]),
        "change_from_baseline": float(changes[k]),
        "running_stress_extreme": float(np.max(changes[:k + 1])),
    } for k in range(12)]

    metrics = {
        "baseline_value": float(base_avg),
        "change_3m": float(changes[2]),
        "change_6m": float(changes[5]),
        "change_12m": float(changes[11]),
        "max_stress_move": float(np.max(changes)),
        "min_stress_move": float(np.min(changes)),
        "stress_peak_month": peak_idx + 1,
        "max_absolute_level": float(np.max(maxs)),
        "risk_metric": float(np.max(changes)),
    }
    return paths, metrics


def spread_metrics(smap, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    baseline_p = ep - 1
    posts = [ep + k for k in range(1, 13)]
    if baseline_p not in smap or any(p not in smap for p in posts):
        return None, None

    baseline = float(smap[baseline_p])
    vals = np.array([float(smap[p]) for p in posts])
    changes_bp = (vals - baseline) * 100.0
    peak_idx = int(np.argmax(changes_bp))

    paths = [{
        "event_month": k + 1,
        "value": float(vals[k]),
        "secondary_value": np.nan,
        "change_from_baseline": float(changes_bp[k]),
        "running_stress_extreme": float(np.max(changes_bp[:k + 1])),
    } for k in range(12)]

    metrics = {
        "baseline_value": baseline,
        "change_3m": float(changes_bp[2]),
        "change_6m": float(changes_bp[5]),
        "change_12m": float(changes_bp[11]),
        "max_stress_move": float(np.max(changes_bp)),
        "min_stress_move": float(np.min(changes_bp)),
        "stress_peak_month": peak_idx + 1,
        "max_absolute_level": float(np.max(vals)),
        "risk_metric": float(np.max(changes_bp)),
    }
    return paths, metrics


def copper_metrics(cmap, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    baseline_p = ep - 1
    posts = [ep + k for k in range(1, 13)]
    if baseline_p not in cmap or any(p not in cmap for p in posts):
        return None, None

    baseline = float(cmap[baseline_p])
    vals = np.array([float(cmap[p]) for p in posts])
    full = np.concatenate([[baseline], vals])
    ret = vals / baseline - 1.0
    peaks = np.maximum.accumulate(full)
    dd = 1.0 - full / peaks
    mdd = float(dd.max())
    trough_idx = int(np.argmax(dd))
    trough_month = trough_idx if trough_idx > 0 else np.nan

    paths = [{
        "event_month": k + 1,
        "value": float(vals[k]),
        "secondary_value": np.nan,
        "change_from_baseline": float(ret[k]),
        "running_stress_extreme": float(np.max(1.0 - full[:k + 2] / np.maximum.accumulate(full[:k + 2]))),
    } for k in range(12)]

    metrics = {
        "baseline_value": baseline,
        "change_3m": float(ret[2]),
        "change_6m": float(ret[5]),
        "change_12m": float(ret[11]),
        "max_stress_move": mdd,
        "min_stress_move": float(np.min(full / baseline - 1.0)),
        "stress_peak_month": trough_month,
        "max_absolute_level": float(np.max(vals)),
        "risk_metric": mdd,
        "copper_mfe_12m": float(np.max(full / baseline - 1.0)),
    }
    return paths, metrics


def build(cycles, vix, baa, copper):
    vmap = dict(zip(vix["period"], zip(vix["vix_avg"].astype(float), vix["vix_max"].astype(float))))
    smap = dict(zip(baa["period"], baa["spread_pp"].astype(float)))
    cmap = dict(zip(copper["period"], copper["copper_price"].astype(float)))

    observables = {
        "VIX": ("volatility_level", vmap, vix_metrics),
        "BAA10Y_SPREAD": ("credit_spread", smap, spread_metrics),
        "COPPER": ("price_asset", cmap, copper_metrics),
    }

    paths, metrics = [], []

    for obs, (kind, data_map, fn) in observables.items():
        for anchor, col in ANCHORS.items():
            available = []
            for _, cyc in cycles.iterrows():
                dt = cyc[col]
                if pd.isna(dt):
                    continue
                p, m = fn(data_map, dt)
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
                    "observable": obs,
                    "observable_kind": kind,
                    "anchor": anchor,
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


def summarize(metrics):
    rows = []
    for (obs, anchor), g in metrics.groupby(["observable", "anchor"]):
        nlegs = int(g["cycle_id"].nunique())
        nbroad = int(g["broad_episode_id"].nunique())
        supported = nlegs >= 5 and nbroad >= 4
        w = g["episode_weight"].to_numpy(float)

        row = {
            "observable": obs,
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "weighted_median_change_3m": weighted_quantile(g["change_3m"], w, .5),
            "weighted_median_change_6m": weighted_quantile(g["change_6m"], w, .5),
            "weighted_median_change_12m": weighted_quantile(g["change_12m"], w, .5),
            "weighted_median_max_stress_move": weighted_quantile(g["max_stress_move"], w, .5),
            "weighted_median_stress_peak_month": weighted_quantile(g["stress_peak_month"], w, .5),
            "weighted_q75_max_stress_move": weighted_quantile(g["max_stress_move"], w, .75),
            "support_status": "PRIMARY_SUPPORTED" if supported else "DIAGNOSTIC_LIMITED_SUPPORT",
        }
        if obs == "VIX":
            row["unit_note"] = "VIX points; max stress = max increase in monthly-average VIX"
        elif obs == "BAA10Y_SPREAD":
            row["unit_note"] = "basis points; max stress = max credit-spread widening"
        else:
            row["unit_note"] = "decimal return/MDD; max stress = 12M copper MDD"
        rows.append(row)
    return pd.DataFrame(rows)


def path_summary(paths):
    rows = []
    for (obs, anchor, month), g in paths.groupby(["observable", "anchor", "event_month"]):
        w = g["episode_weight"].to_numpy(float)
        rows.append({
            "observable": obs,
            "anchor": anchor,
            "event_month": int(month),
            "n_legs": int(g["cycle_id"].nunique()),
            "n_broad_episodes": int(g["broad_episode_id"].nunique()),
            "weighted_median_change_from_baseline": weighted_quantile(g["change_from_baseline"], w, .5),
            "weighted_median_running_stress_extreme": weighted_quantile(g["running_stress_extreme"], w, .5),
            "weighted_q75_running_stress_extreme": weighted_quantile(g["running_stress_extreme"], w, .75),
        })
    return pd.DataFrame(rows)


def make_figures(pathsum, summary):
    for obs, ylabel in [
        ("VIX", "VIX points"),
        ("BAA10Y_SPREAD", "basis points"),
        ("COPPER", "drawdown / return units"),
    ]:
        g = pathsum[pathsum["observable"] == obs]
        fig, ax = plt.subplots(figsize=(9.7, 5.4))
        for anchor in ANCHORS:
            q = g[g["anchor"] == anchor]
            if len(q):
                y = q["weighted_median_running_stress_extreme"]
                if obs == "COPPER":
                    y = y * 100.0
                ax.plot(q["event_month"], y, label=anchor)
        ax.set_title(f"{obs}: 12M stress accumulation by policy-cycle anchor")
        ax.set_xlabel("Complete months after anchor month")
        ax.set_ylabel(ylabel if obs != "COPPER" else "Running MDD (%)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT / f"01_{obs.lower()}_phase_stress.png", dpi=170, bbox_inches="tight")
        plt.close(fig)

    for obs in ["VIX", "BAA10Y_SPREAD", "COPPER"]:
        g = summary[(summary["observable"] == obs) & (summary["support_status"] == "PRIMARY_SUPPORTED")].copy()
        if g.empty:
            continue
        vals = g["weighted_median_max_stress_move"].copy()
        if obs == "COPPER":
            vals = vals * 100.0
        fig, ax = plt.subplots(figsize=(8.8, 5.0))
        ax.bar(g["anchor"], vals)
        ax.set_title(f"{obs}: median maximum 12M stress by anchor")
        ax.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        fig.savefig(OUT / f"02_{obs.lower()}_max_stress_comparison.png", dpi=170, bbox_inches="tight")
        plt.close(fig)


def write_report(summary, qc):
    primary = summary[summary["support_status"] == "PRIMARY_SUPPORTED"].copy()
    lines = [
        "# FED-CYCLE-STRESS-LAYER-005 — Report",
        "",
        "**DESCRIPTIVE STRESS-STATE LAYER / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "## QC",
        "",
        f"- QC gate: {qc['qc_gate']}",
        f"- primary supported cells: {qc['primary_supported_cells']}",
        "- common 12-complete-month phase window;",
        "- event month omitted;",
        "- broad-episode weighting applied separately inside each observable × phase cell.",
        "",
        "## Primary stress summaries",
        "",
        primary.to_markdown(index=False),
        "",
        "## Evidence boundary",
        "",
        "- VIX, Baa-10Y spread and copper are observed stress/mechanism variables.",
        "- This module does not test optimized thresholds or forecasting rules.",
        "- Visual alignment with asset drawdowns is not causal identification.",
        "- No p-value/FDR family is run.",
        "- OOS: not applicable.",
        "- Deployment: none.",
    ]
    (OUT / "FED_CYCLE_STRESS_LAYER_005_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    cycles = STATE_MOD.assign_broad_clusters(STATE_MOD.load_cycles())
    vix, baa, copper, prov = load_sources()
    paths, metrics = build(cycles, vix, baa, copper)
    summary = summarize(metrics)
    pathsum = path_summary(paths)

    # QC
    event_month_bad = int(((paths["event_month"] < 1) | (paths["event_month"] > 12)).sum())
    copper_bad = int(
        (
            (metrics["observable"] == "COPPER")
            & (pd.to_numeric(metrics["max_stress_move"], errors="coerce") < -1e-12)
        ).sum()
    )

    v = vix.copy()
    vix_max_bad = int((v["vix_max"] + 1e-12 < v["vix_avg"]).sum())

    weight_bad = 0
    for (obs, anchor, bid), g in metrics.groupby(["observable","anchor","broad_episode_id"]):
        if abs(float(g["episode_weight"].sum()) - 1.0) > 1e-10:
            weight_bad += 1

    unsupported_as_primary = int(
        (
            (summary["support_status"] == "PRIMARY_SUPPORTED")
            & ((summary["n_legs"] < 5) | (summary["n_broad_episodes"] < 4))
        ).sum()
    )

    canonical = cycles.set_index("cycle_id")
    anchor_bad = 0
    for _, r in metrics.iterrows():
        expected = canonical.loc[r["cycle_id"], ANCHORS[r["anchor"]]]
        if pd.isna(expected) or pd.Timestamp(r["anchor_date"]) != pd.Timestamp(expected):
            anchor_bad += 1

    expected_cells = 12
    primary_cells = summary[summary["support_status"] == "PRIMARY_SUPPORTED"]

    hard_fail = (
        event_month_bad != 0
        or copper_bad != 0
        or vix_max_bad != 0
        or weight_bad != 0
        or unsupported_as_primary != 0
        or anchor_bad != 0
        or len(primary_cells) != expected_cells
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-STRESS-LAYER-005",
        "path_rows": int(len(paths)),
        "stress_cycle_phase_rows": int(len(metrics)),
        "primary_supported_cells": int(len(primary_cells)),
        "expected_primary_supported_cells": expected_cells,
        "event_month_violations": event_month_bad,
        "vix_max_below_average_violations": vix_max_bad,
        "negative_copper_mdd_violations": copper_bad,
        "broad_episode_weight_violations": weight_bad,
        "unsupported_as_primary": unsupported_as_primary,
        "canonical_anchor_date_violations": anchor_bad,
        "raw_source_histories_committed": False,
        "fdr_status": "NOT_APPLICABLE_DESCRIPTIVE_STRESS_MODULE",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    prov.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    paths.to_csv(OUT / "STRESS_PATHS.csv", index=False)
    metrics.to_csv(OUT / "STRESS_CYCLE_PHASE_METRICS.csv", index=False)
    pathsum.to_csv(OUT / "STRESS_PATH_SUMMARY.csv", index=False)
    summary.to_csv(OUT / "STRESS_PHASE_SUMMARY.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")
    make_figures(pathsum, summary)
    write_report(summary, qc)

    if hard_fail:
        raise SystemExit("FED-CYCLE-STRESS-LAYER-005 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
