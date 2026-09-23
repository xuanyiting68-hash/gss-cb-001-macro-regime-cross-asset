#!/usr/bin/env python3
"""
ENERGY-PRICE-WF-001
Long-history monthly WTI/refined-product walk-forward screen.

Public-source data:
- MCOILWTICO
- MGASUSGULF
- MHOILNYH
- MJFUELUSGULF

The script follows the frozen ENERGY_PRICE_WALKFORWARD_V1_LOCK specification.\nGitHub Actions is the reference execution environment for the public run.
Raw downloaded bytes are used locally for computation and are not written
into the repository output directory.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "energy_price_wf_v1"
OUT.mkdir(parents=True, exist_ok=True)

SERIES = {
    "WTI": {
        "id": "MCOILWTICO",
        "title": "Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma",
        "unit": "USD/barrel",
        "source": "U.S. Energy Information Administration via FRED",
    },
    "GAS": {
        "id": "MGASUSGULF",
        "title": "Conventional Gasoline Prices: U.S. Gulf Coast, Regular",
        "unit": "USD/gallon",
        "source": "U.S. Energy Information Administration via FRED",
    },
    "HEAT": {
        "id": "MHOILNYH",
        "title": "No. 2 Heating Oil Prices: New York Harbor",
        "unit": "USD/gallon",
        "source": "U.S. Energy Information Administration via FRED",
    },
    "JET": {
        "id": "MJFUELUSGULF",
        "title": "Kerosene-Type Jet Fuel Prices: U.S. Gulf Coast",
        "unit": "USD/gallon",
        "source": "U.S. Energy Information Administration via FRED",
    },
}

def fetch_series(series_id: str):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    req = Request(url, headers={"User-Agent": "gss-cb-001-public-research/1.0"})
    with urlopen(req, timeout=60) as resp:
        raw = resp.read()
    sha = hashlib.sha256(raw).hexdigest()
    df = pd.read_csv(io.BytesIO(raw))
    date_col = df.columns[0]
    value_col = series_id if series_id in df.columns else df.columns[1]
    df = df.rename(columns={date_col: "date", value_col: "value"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")
    return df, sha, url

def bh_adjust(pvals):
    p = np.asarray(pvals, dtype=float)
    out = np.full_like(p, np.nan)
    valid = np.isfinite(p)
    pv = p[valid]
    if len(pv) == 0:
        return out
    order = np.argsort(pv)
    ranked = pv[order]
    m = len(ranked)
    q = ranked * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.minimum(q, 1.0)
    tmp = np.empty_like(q)
    tmp[order] = q
    out[valid] = tmp
    return out

def safe_mwu(a, b):
    a = pd.Series(a).dropna().astype(float)
    b = pd.Series(b).dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    return float(mannwhitneyu(a, b, alternative="two-sided").pvalue)

def expanding_z_prior(s: pd.Series, min_periods=60):
    prior = s.shift(1)
    mu = prior.expanding(min_periods=min_periods).mean()
    sd = prior.expanding(min_periods=min_periods).std(ddof=1)
    return (s - mu) / sd

def build_panel():
    provenance = []
    frames = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    for name, meta in SERIES.items():
        df, sha, url = fetch_series(meta["id"])
        provenance.append({
            "name": name,
            "series_id": meta["id"],
            "title": meta["title"],
            "source": meta["source"],
            "unit": meta["unit"],
            "url": url,
            "retrieved_utc": fetched_at,
            "sha256": sha,
            "rows_total": int(len(df)),
            "rows_nonmissing": int(df["value"].notna().sum()),
            "missing_values": int(df["value"].isna().sum()),
            "first_date": str(df["date"].min().date()),
            "last_date": str(df["date"].max().date()),
        })
        frames.append(df[["date", "value"]].rename(columns={"value": name}))

    panel = frames[0]
    for f in frames[1:]:
        panel = panel.merge(f, on="date", how="outer")
    panel = panel.sort_values("date").reset_index(drop=True)

    panel = panel[panel["date"] >= pd.Timestamp("1990-04-01")].copy()
    common_last = min(panel.loc[panel[c].notna(), "date"].max() for c in SERIES)
    panel = panel[panel["date"] <= common_last].copy()
    panel = panel.dropna(subset=list(SERIES)).reset_index(drop=True)

    expected = pd.period_range(panel["date"].min(), panel["date"].max(), freq="M")
    actual = pd.PeriodIndex(panel["date"], freq="M")
    missing_periods = expected.difference(actual)

    for c in SERIES:
        panel[f"{c}_r1"] = np.log(panel[c] / panel[c].shift(1)) * 100
        panel[f"{c}_r3"] = np.log(panel[c] / panel[c].shift(3)) * 100
        panel[f"{c}_z3"] = expanding_z_prior(panel[f"{c}_r3"], min_periods=60)

    zcols = [f"{c}_z3" for c in SERIES]
    panel["pressure_score"] = panel[zcols].mean(axis=1, skipna=False)
    panel["pressure_q90_prior"] = (
        panel["pressure_score"].shift(1).expanding(min_periods=24).quantile(0.90)
    )
    panel["S2_PRICE_EXTREME"] = panel["pressure_score"] > panel["pressure_q90_prior"]

    prod_r1 = ["GAS_r1", "HEAT_r1", "JET_r1"]
    panel["products_down_count"] = (panel[prod_r1] < 0).sum(axis=1)

    recent_extreme = (
        panel["S2_PRICE_EXTREME"].astype(int)
        .rolling(3, min_periods=1)
        .max()
        .astype(bool)
    )
    panel["S3_candidate_raw"] = (
        recent_extreme
        & (panel["WTI_r1"] < 0)
        & (panel["products_down_count"] >= 2)
    )

    selected = np.zeros(len(panel), dtype=bool)
    last_selected = -10000
    for i, flag in enumerate(panel["S3_candidate_raw"].fillna(False).to_numpy()):
        if flag and i - last_selected > 6:
            selected[i] = True
            last_selected = i
    panel["S3_SELECTED"] = selected

    qc = {
        "common_sample_first": str(panel["date"].min().date()),
        "common_sample_last": str(panel["date"].max().date()),
        "common_rows": int(len(panel)),
        "common_missing_months": [str(x) for x in missing_periods],
        "duplicate_dates": int(panel["date"].duplicated().sum()),
        "nonpositive_price_cells": int((panel[list(SERIES)] <= 0).sum().sum()),
        "s2_extreme_months": int(panel["S2_PRICE_EXTREME"].sum()),
        "s3_raw_months": int(panel["S3_candidate_raw"].sum()),
        "s3_selected_events": int(panel["S3_SELECTED"].sum()),
    }
    return panel, pd.DataFrame(provenance), qc

def classify_events(panel):
    events = []
    for i in panel.index[panel["S3_SELECTED"]]:
        if i + 1 >= len(panel):
            continue
        t = panel.loc[i]
        c = panel.loc[i + 1]
        confirmed = (c["WTI_r1"] <= 0) and (c["products_down_count"] >= 2)
        label = "PRICE_PRODUCT_CONFIRMED" if confirmed else "FALSE_RELIEF_VETO"
        row = {
            "s3_date": t["date"],
            "anchor_date": c["date"],
            "classification": label,
            "pressure_score_s3": t["pressure_score"],
            "prior_q90_s3": t["pressure_q90_prior"],
            "wti_r1_s3_pct": t["WTI_r1"],
            "products_down_s3": int(t["products_down_count"]),
            "wti_r1_anchor_pct": c["WTI_r1"],
            "products_down_anchor": int(c["products_down_count"]),
            "WTI_anchor": c["WTI"],
        }
        anchor_i = i + 1
        for h in [1, 3, 6, 12]:
            if anchor_i + h < len(panel):
                p0 = panel.loc[anchor_i, "WTI"]
                p1 = panel.loc[anchor_i + h, "WTI"]
                row[f"wti_fwd_{h}m"] = p1 / p0 - 1
            else:
                row[f"wti_fwd_{h}m"] = np.nan

        for h in [3, 6]:
            p0 = panel.loc[anchor_i, "WTI"]
            end_i = min(anchor_i + h, len(panel) - 1)
            path = panel.loc[anchor_i:end_i, "WTI"] / p0 - 1
            row[f"short_mae_{h}m"] = float(path.max()) if len(path) >= 2 else np.nan
            row[f"short_mfe_{h}m"] = float(-path.min()) if len(path) >= 2 else np.nan
        events.append(row)
    return pd.DataFrame(events)

def summarize(events):
    rows = []
    for label, g in events.groupby("classification"):
        for h in [1, 3, 6, 12]:
            x = g[f"wti_fwd_{h}m"].dropna()
            rows.append({
                "classification": label,
                "metric": f"WTI_fwd_{h}m",
                "n": len(x),
                "mean": x.mean(),
                "median": x.median(),
                "negative_share": (x < 0).mean() if len(x) else np.nan,
            })
        for h in [3, 6]:
            x = g[f"short_mae_{h}m"].dropna()
            rows.append({
                "classification": label,
                "metric": f"short_mae_{h}m",
                "n": len(x),
                "mean": x.mean(),
                "median": x.median(),
                "negative_share": np.nan,
            })
    return pd.DataFrame(rows)

def infer(events):
    specs = [
        ("WTI_fwd_3m", "wti_fwd_3m"),
        ("WTI_fwd_6m", "wti_fwd_6m"),
        ("short_MAE_3m", "short_mae_3m"),
        ("short_MAE_6m", "short_mae_6m"),
    ]
    a = events[events["classification"] == "PRICE_PRODUCT_CONFIRMED"]
    b = events[events["classification"] == "FALSE_RELIEF_VETO"]
    rows = []
    for label, col in specs:
        xa = a[col].dropna()
        xb = b[col].dropna()
        rows.append({
            "test": label,
            "n_confirmed": len(xa),
            "n_veto": len(xb),
            "confirmed_mean": xa.mean(),
            "veto_mean": xb.mean(),
            "confirmed_median": xa.median(),
            "veto_median": xb.median(),
            "difference_median_confirmed_minus_veto": xa.median() - xb.median() if len(xa) and len(xb) else np.nan,
            "mann_whitney_p": safe_mwu(xa, xb),
        })
    out = pd.DataFrame(rows)
    out["bh_q_4test_family"] = bh_adjust(out["mann_whitney_p"])
    return out

def simple_rollover_benchmark(panel):
    raw = (panel["WTI_r1"] < 0) & (panel["WTI_r3"].shift(1) > 0)
    idxs = []
    last = -10000
    for i, flag in enumerate(raw.fillna(False).to_numpy()):
        if flag and i - last > 6:
            idxs.append(i)
            last = i
    rows = []
    for i in idxs:
        row = {"date": panel.loc[i, "date"]}
        for h in [3, 6]:
            if i + h < len(panel):
                row[f"wti_fwd_{h}m"] = panel.loc[i + h, "WTI"] / panel.loc[i, "WTI"] - 1
            else:
                row[f"wti_fwd_{h}m"] = np.nan
        rows.append(row)
    return pd.DataFrame(rows)

def write_report(prov, qc, events, summary, tests, bench):
    confirmed = events[events["classification"] == "PRICE_PRODUCT_CONFIRMED"]
    veto = events[events["classification"] == "FALSE_RELIEF_VETO"]
    lines = [
        "# ENERGY-PRICE-WF-001 — First Exhaustive Public-Source Walk-Forward",
        "Date: 2026-09-24",
        "",
        "## Evidence status",
        "",
        "**EXPLORATORY WALK-FORWARD / PRICE-PRODUCT LAYER ONLY / NOT DEPLOYABLE**",
        "",
        "This run follows the frozen ENERGY_PRICE_WALKFORWARD_V1_LOCK protocol.",
        "It does not use inventory/refinery data and therefore does not identify physical supply normalization.",
        "",
        "## Data QC",
        "",
        f"- Common sample: {qc['common_sample_first']} to {qc['common_sample_last']}",
        f"- Complete common months: {qc['common_rows']}",
        f"- Missing common months: {len(qc['common_missing_months'])}",
        f"- Duplicate dates: {qc['duplicate_dates']}",
        f"- Non-positive price cells: {qc['nonpositive_price_cells']}",
        f"- S2 extreme months: {qc['s2_extreme_months']}",
        f"- Raw S3 rollover months: {qc['s3_raw_months']}",
        f"- De-clustered S3 events: {qc['s3_selected_events']}",
        "",
        "## Event counts",
        "",
        f"- PRICE_PRODUCT_CONFIRMED: {len(confirmed)}",
        f"- FALSE_RELIEF_VETO: {len(veto)}",
        "",
        "## Primary four-test family",
        "",
        tests.to_markdown(index=False),
        "",
        "## Group descriptives",
        "",
        summary.to_markdown(index=False),
        "",
        "## Simple WTI rollover benchmark",
        "",
    ]
    if len(bench):
        lines.append(f"- De-clustered simple-rollover events: {len(bench)}")
        for h in [3, 6]:
            x = bench[f"wti_fwd_{h}m"].dropna()
            lines.append(
                f"- {h}M mean: {100*x.mean():+.2f}%; median: {100*x.median():+.2f}%; negative share: {100*(x<0).mean():.1f}%"
            )
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Even a supportive result is public price-product timing evidence only. It is not proof of physical supply normalization and it is not a deployable short strategy.",
        "",
        "The next gate is a release-aware EIA inventory/refinery extension.",
        "",
        "## Source registry",
        "",
        prov[["series_id","title","source","unit","first_date","last_date","sha256"]].to_markdown(index=False),
    ])
    (OUT / "ENERGY_PRICE_WF_001_REPORT.md").write_text("\\n".join(lines), encoding="utf-8")

def make_figures(events):
    if events.empty:
        return
    order = events.sort_values("anchor_date")
    fig, ax = plt.subplots(figsize=(11, 5.5))
    x = np.arange(len(order))
    ax.bar(x, order["wti_fwd_3m"] * 100)
    ax.axhline(0, linewidth=0.8)
    ax.set_xticks(x, pd.to_datetime(order["anchor_date"]).dt.strftime("%Y-%m"), rotation=45, ha="right")
    ax.set_ylabel("WTI 3M forward return (%)")
    ax.set_title("ENERGY-PRICE-WF-001: WTI 3M outcome by de-clustered event")
    fig.tight_layout()
    fig.savefig(OUT / "01_event_wti_3m_returns.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    groups = ["PRICE_PRODUCT_CONFIRMED", "FALSE_RELIEF_VETO"]
    med3, med6 = [], []
    for g in groups:
        z = events[events["classification"] == g]
        med3.append(z["wti_fwd_3m"].median() * 100)
        med6.append(z["wti_fwd_6m"].median() * 100)
    x = np.arange(2)
    w = 0.36
    ax.bar(x-w/2, med3, w, label="3M median")
    ax.bar(x+w/2, med6, w, label="6M median")
    ax.axhline(0, linewidth=0.8)
    ax.set_xticks(x, ["Confirmed", "Veto"])
    ax.set_ylabel("Median WTI forward return (%)")
    ax.set_title("Persistent product-price weakness vs false relief")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "02_confirmed_vs_veto_medians.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

def main():
    panel, prov, qc = build_panel()
    events = classify_events(panel)
    summary = summarize(events)
    tests = infer(events)
    bench = simple_rollover_benchmark(panel)

    hard_fail = (
        qc["duplicate_dates"] != 0
        or qc["nonpositive_price_cells"] != 0
        or len(qc["common_missing_months"]) != 0
        or len(events) == 0
    )
    qc["qc_gate"] = "FAIL" if hard_fail else "PASS"

    prov.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    panel.to_csv(OUT / "DERIVED_MONTHLY_PANEL.csv", index=False)
    events.to_csv(OUT / "EVENTS.csv", index=False)
    summary.to_csv(OUT / "GROUP_DESCRIPTIVES.csv", index=False)
    tests.to_csv(OUT / "PRIMARY_TESTS.csv", index=False)
    bench.to_csv(OUT / "SIMPLE_WTI_ROLLOVER_BENCHMARK.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")
    write_report(prov, qc, events, summary, tests, bench)
    make_figures(events)

    if hard_fail:
        raise SystemExit("QC gate failed")

    print(json.dumps({
        "qc_gate": qc["qc_gate"],
        "events": int(len(events)),
        "confirmed": int((events["classification"] == "PRICE_PRODUCT_CONFIRMED").sum()),
        "veto": int((events["classification"] == "FALSE_RELIEF_VETO").sum()),
        "last_common_date": qc["common_sample_last"],
    }, indent=2))

if __name__ == "__main__":
    main()
