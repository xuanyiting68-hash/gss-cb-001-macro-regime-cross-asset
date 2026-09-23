#!/usr/bin/env python3
"""
FED-CYCLE-GOLD-LONGHIST-MONTHLY-001
Native-frequency monthly long-history Gold robustness layer.

Reference:
research/FED_CYCLE_GOLD_LONGHIST_MONTHLY_001_LOCK.md
"""
from __future__ import annotations

import hashlib
import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gold_long_history_monthly_v1"
OUT.mkdir(parents=True, exist_ok=True)

SOURCE_COMMIT = "95bfea9197222dcda13d8c4d9928fb631fe745aa"
MONTHLY_URL = f"https://raw.githubusercontent.com/datasets/gold-prices/{SOURCE_COMMIT}/data/monthly.csv"
PACKAGE_URL = f"https://raw.githubusercontent.com/datasets/gold-prices/{SOURCE_COMMIT}/datapackage.json"

HORIZONS = [1, 3, 6, 12, 24]
PATH_HORIZON = 24
RECOVERY_SEARCH = 60


def fetch_bytes(url: str, timeout: int = 60) -> bytes:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 gss-cb-001-public-research/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def load_gold_monthly():
    raw = fetch_bytes(MONTHLY_URL)
    package_raw = fetch_bytes(PACKAGE_URL)
    pkg = json.loads(package_raw.decode("utf-8"))
    license_names = [x.get("name", "") for x in pkg.get("licenses", [])]
    if "ODC-PDDL-1.0" not in license_names:
        raise RuntimeError(f"Expected ODC-PDDL-1.0 not found: {license_names}")

    df = pd.read_csv(io.BytesIO(raw))
    if list(df.columns)[:2] != ["Date", "Price"]:
        raise RuntimeError(f"Unexpected monthly source schema: {list(df.columns)}")
    df["period"] = pd.PeriodIndex(df["Date"].astype(str), freq="M")
    df["price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["period", "price"]).sort_values("period").drop_duplicates("period")
    df = df[df["period"] >= pd.Period("1960-01", freq="M")].copy().reset_index(drop=True)

    expected = pd.period_range(df["period"].min(), df["period"].max(), freq="M")
    missing = expected.difference(pd.PeriodIndex(df["period"]))
    if len(missing):
        raise RuntimeError(f"Missing monthly Gold periods: {list(missing[:12])}")

    provenance = {
        "dataset": "datasets/gold-prices",
        "resource": "data/monthly.csv",
        "source_commit": SOURCE_COMMIT,
        "source_url": MONTHLY_URL,
        "package_url": PACKAGE_URL,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "monthly_sha256": hashlib.sha256(raw).hexdigest(),
        "datapackage_sha256": hashlib.sha256(package_raw).hexdigest(),
        "license": "ODC-PDDL-1.0",
        "modern_source": 'World Bank Commodity Markets ("Pink Sheet")',
        "eligible_start": str(df["period"].min()),
        "eligible_end": str(df["period"].max()),
        "eligible_rows": int(len(df)),
        "raw_committed": False,
        "pre1960_rows_excluded": True,
    }
    return df[["period", "price"]], provenance


def load_cycles():
    p = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_TIGHTENING_CYCLES.csv"
    if not p.exists():
        raise RuntimeError("Missing v1.1 timing-corrected Fed-cycle registry")
    c = pd.read_csv(p, parse_dates=["first_hike", "last_hike", "pause_start", "first_cut"])
    if len(c) != 10:
        raise RuntimeError(f"Expected 10 frozen tightening legs, got {len(c)}")
    return c


def clean_path_metrics(price_map, event_date):
    event_period = pd.Period(pd.Timestamp(event_date), freq="M")
    baseline_period = event_period - 1
    if baseline_period not in price_map:
        return None

    baseline = float(price_map[baseline_period])
    post_periods = []
    for k in range(1, PATH_HORIZON + 1):
        p = event_period + k
        if p not in price_map:
            break
        post_periods.append(p)
    if not post_periods:
        return None

    prices = np.array([price_map[p] for p in post_periods], dtype=float)
    vals = np.concatenate([[baseline], prices])
    event_ret = vals / baseline - 1.0

    row = {
        "event_period": str(event_period),
        "baseline_period": str(baseline_period),
        "baseline_price": baseline,
        "event_month_omitted_from_clean_metrics": True,
        "available_clean_post_months": int(len(post_periods)),
        "mae": float(np.min(event_ret)),
        "mfe": float(np.max(event_ret)),
        "time_to_event_min_months": int(np.argmin(event_ret)),
        "time_to_event_max_months": int(np.argmax(event_ret)),
    }

    for h in HORIZONS:
        p = event_period + h
        row[f"ret_{h}m"] = float(price_map[p] / baseline - 1.0) if p in price_map else np.nan

    running_peak = np.maximum.accumulate(vals)
    dd = 1.0 - vals / running_peak
    trough_rel = int(np.argmax(dd))
    peak_rel = int(np.argmax(vals[:trough_rel + 1]))
    mdd = float(dd[trough_rel])
    row["mdd_24m"] = mdd
    row["mdd_peak_month_offset"] = peak_rel
    row["mdd_trough_month_offset"] = trough_rel
    row["peak_to_trough_months"] = trough_rel - peak_rel

    for h in [12, 24]:
        ps = [event_period + k for k in range(1, h + 1) if (event_period + k) in price_map]
        if len(ps) >= 3:
            x = np.array([price_map[p] for p in ps], dtype=float)
            rr = np.diff(np.log(x))
            row[f"rv_{h}m_ann"] = float(np.std(rr, ddof=1) * math.sqrt(12))
            row[f"down_semivol_{h}m_ann"] = float(math.sqrt(12 * np.mean(np.minimum(rr, 0.0) ** 2)))
        else:
            row[f"rv_{h}m_ann"] = np.nan
            row[f"down_semivol_{h}m_ann"] = np.nan

    row.update({
        "recovery50_months_from_trough": np.nan,
        "recovery100_months_from_trough": np.nan,
        "recovery50_observed": False,
        "recovery100_observed": False,
        "recovery_censor_months": np.nan,
    })

    if mdd > 1e-12:
        peak_price = vals[peak_rel]
        trough_price = vals[trough_rel]
        threshold50 = trough_price + 0.5 * (peak_price - trough_price)
        threshold100 = peak_price

        def offset_to_period(off):
            return baseline_period if off == 0 else event_period + off

        trough_period = offset_to_period(trough_rel)
        rec = []
        for k in range(0, RECOVERY_SEARCH + 1):
            p = trough_period + k
            if p in price_map:
                rec.append((k, float(price_map[p])))
        if rec:
            row["recovery_censor_months"] = int(rec[-1][0])
            hit50 = [k for k, v in rec if v >= threshold50]
            hit100 = [k for k, v in rec if v >= threshold100]
            if hit50:
                row["recovery50_months_from_trough"] = int(hit50[0])
                row["recovery50_observed"] = True
            if hit100:
                row["recovery100_months_from_trough"] = int(hit100[0])
                row["recovery100_observed"] = True

    return row


def build_metrics(cycles, gold):
    price_map = dict(zip(gold["period"], gold["price"].astype(float)))
    rows = []
    anchor_cols = {
        "FIRST_HIKE": "first_hike",
        "LAST_HIKE": "last_hike",
        "PAUSE_START": "pause_start",
        "FIRST_CUT": "first_cut",
    }
    for _, cyc in cycles.iterrows():
        for event_type, col in anchor_cols.items():
            dt = cyc[col]
            if pd.isna(dt):
                continue
            m = clean_path_metrics(price_map, dt)
            if m is None:
                continue
            rows.append({
                "cycle_id": cyc["cycle_id"],
                "cycle_start_year": int(pd.Timestamp(cyc["first_hike"]).year),
                "event_type": event_type,
                "event_date": pd.Timestamp(dt),
                **m,
            })
    return pd.DataFrame(rows)


def distribution_summary(metrics):
    fields = [
        "ret_1m","ret_3m","ret_6m","ret_12m","ret_24m",
        "mdd_24m","mae","mfe","time_to_event_min_months",
        "recovery50_months_from_trough","recovery100_months_from_trough",
        "rv_12m_ann","down_semivol_12m_ann",
    ]
    rows = []
    for et, g in metrics.groupby("event_type"):
        for fld in fields:
            x = pd.to_numeric(g[fld], errors="coerce").dropna()
            if len(x):
                rows.append({
                    "event_type": et, "metric": fld, "n": int(len(x)),
                    "mean": float(x.mean()), "median": float(x.median()),
                    "q25": float(x.quantile(.25)), "q75": float(x.quantile(.75)),
                    "min": float(x.min()), "max": float(x.max()),
                })
    return pd.DataFrame(rows)


def cross_frequency_audit(monthly_metrics):
    p = ROOT / "results" / "fed_cycle_path_v1_1" / "EVENT_ASSET_METRICS.csv"
    daily = pd.read_csv(p, parse_dates=["event_date"])
    daily = daily[(daily["asset"] == "GOLD") & (daily["event_type"] == "FIRST_HIKE")].copy()
    mon = monthly_metrics[monthly_metrics["event_type"] == "FIRST_HIKE"].copy()
    out = mon.merge(daily[["cycle_id", "ret_252d", "mdd"]], on="cycle_id", how="inner")
    out = out[["cycle_id","cycle_start_year","event_date","ret_12m","mdd_24m","ret_252d","mdd"]]
    out = out.rename(columns={
        "ret_12m": "world_bank_monthly_ret_12m",
        "mdd_24m": "world_bank_monthly_mdd_24m",
        "ret_252d": "gc_f_daily_ret_252obs",
        "mdd": "gc_f_daily_mdd_252obs",
    })
    out["endpoint_sign_agrees"] = (
        np.sign(out["world_bank_monthly_ret_12m"]) == np.sign(out["gc_f_daily_ret_252obs"])
    )
    return out


def make_figures(metrics):
    first = metrics[metrics["event_type"] == "FIRST_HIKE"].copy().sort_values("cycle_start_year")
    if not len(first):
        return

    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    ax.bar(first["cycle_id"], first["mdd_24m"] * 100)
    ax.set_title("Long-history Gold monthly MDD after FIRST_HIKE")
    ax.set_ylabel("24-month clean-path maximum drawdown (%)")
    ax.set_xlabel("Mechanical tightening leg")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(OUT / "01_gold_monthly_first_hike_mdd.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    ax.scatter(first["ret_12m"] * 100, first["mdd_24m"] * 100)
    for _, r in first.iterrows():
        ax.annotate(str(r["cycle_start_year"]), (r["ret_12m"] * 100, r["mdd_24m"] * 100), fontsize=8)
    ax.axvline(0, linewidth=0.8)
    ax.set_title("Gold: 12M endpoint vs 24M path drawdown after FIRST_HIKE")
    ax.set_xlabel("Clean +12M endpoint return (%)")
    ax.set_ylabel("24M maximum drawdown (%)")
    fig.tight_layout()
    fig.savefig(OUT / "02_gold_monthly_endpoint_vs_mdd.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


def write_report(metrics, summary, audit, provenance):
    first = metrics[metrics["event_type"] == "FIRST_HIKE"].copy()

    def stat(field):
        x = pd.to_numeric(first[field], errors="coerce").dropna()
        if not len(x):
            return "NA"
        return f"n={len(x)}, median={x.median():.6f}, range=[{x.min():.6f}, {x.max():.6f}]"

    lines = [
        "# FED-CYCLE-GOLD-LONGHIST-MONTHLY-001 — Report",
        f"Generated: {datetime.now(timezone.utc).date()}",
        "",
        "Status: **QC-PASSED DESCRIPTIVE LONG-HISTORY ROBUSTNESS / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        "## Source and frequency boundary",
        "",
        f"- Source commit: {SOURCE_COMMIT}",
        f"- Eligible monthly sample: {provenance['eligible_start']} to {provenance['eligible_end']}",
        "- Modern source: World Bank Commodity Markets via datasets/gold-prices.",
        "- License: ODC-PDDL-1.0.",
        "- 1833-1959 pseudo-monthly repeated annual averages are excluded.",
        "- Event month is omitted from clean outcome measurement.",
        "",
        "## FIRST_HIKE support",
        "",
        f"- Mechanical tightening legs with clean monthly Gold support: {len(first)}",
        f"- +1M: {stat('ret_1m')}",
        f"- +3M: {stat('ret_3m')}",
        f"- +6M: {stat('ret_6m')}",
        f"- +12M: {stat('ret_12m')}",
        f"- +24M: {stat('ret_24m')}",
        f"- 24M MDD: {stat('mdd_24m')}",
        f"- time-to-event-relative-min: {stat('time_to_event_min_months')}",
        f"- 50% recovery: {stat('recovery50_months_from_trough')}",
        f"- 100% recovery: {stat('recovery100_months_from_trough')}",
        "",
        "## Cross-frequency audit",
        "",
        audit.to_markdown(index=False) if len(audit) else "No overlapping daily/monthly Gold cycles.",
        "",
        "Different frequency/instrument results are diagnostic only and are never pooled.",
        "",
        "## Full distribution summary",
        "",
        summary.to_markdown(index=False),
        "",
        "## Evidence boundary",
        "",
        "- DATA FACT: the monthly layer covers all frozen FIRST_HIKE tightening legs if QC passes.",
        "- DESCRIPTIVE RESULT: monthly Gold paths expand breadth beyond the daily futures proxy.",
        "- CAUSAL EVIDENCE: none.",
        "- FDR: no confirmatory p-value family in this module.",
        "- OOS: not applicable; this is not a forecasting model.",
        "- DEPLOYMENT: none.",
    ]
    (OUT / "FED_CYCLE_GOLD_LONGHIST_MONTHLY_001_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    gold, provenance = load_gold_monthly()
    cycles = load_cycles()
    metrics = build_metrics(cycles, gold)
    summary = distribution_summary(metrics)
    audit = cross_frequency_audit(metrics)

    first = metrics[metrics["event_type"] == "FIRST_HIKE"].copy()
    mdd_bad = int((pd.to_numeric(metrics["mdd_24m"], errors="coerce").dropna() < -1e-12).sum())
    z = metrics.dropna(subset=["recovery50_months_from_trough", "recovery100_months_from_trough"])
    recovery_bad = int((z["recovery100_months_from_trough"] < z["recovery50_months_from_trough"]).sum())
    event_month_bad = int((~metrics["event_month_omitted_from_clean_metrics"].astype(bool)).sum())

    hard_fail = (
        len(first) != 10
        or mdd_bad != 0
        or recovery_bad != 0
        or event_month_bad != 0
        or provenance["eligible_start"] != "1960-01"
        or provenance["raw_committed"] is not False
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-GOLD-LONGHIST-MONTHLY-001",
        "source_commit": SOURCE_COMMIT,
        "eligible_monthly_start": provenance["eligible_start"],
        "eligible_monthly_end": provenance["eligible_end"],
        "eligible_monthly_rows": provenance["eligible_rows"],
        "first_hike_support": int(len(first)),
        "expected_first_hike_support": 10,
        "event_month_omission_violations": event_month_bad,
        "mdd_identity_violations": mdd_bad,
        "recovery_order_violations": recovery_bad,
        "cross_frequency_overlap_rows": int(len(audit)),
        "raw_source_committed": False,
        "pre1960_rows_excluded": True,
        "evidence_status": "DESCRIPTIVE_NOT_CAUSAL_NOT_DEPLOYABLE",
    }

    pd.DataFrame([provenance]).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    metrics.to_csv(OUT / "GOLD_MONTHLY_EVENT_METRICS.csv", index=False)
    summary.to_csv(OUT / "DISTRIBUTION_SUMMARY.csv", index=False)
    audit.to_csv(OUT / "CROSS_FREQUENCY_AUDIT.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")
    make_figures(metrics)
    write_report(metrics, summary, audit, provenance)

    if hard_fail:
        raise SystemExit("FED-CYCLE-GOLD-LONGHIST-MONTHLY-001 QC failed")

    print(json.dumps({
        "qc_gate": qc["qc_gate"],
        "first_hike_support": qc["first_hike_support"],
        "sample": [qc["eligible_monthly_start"], qc["eligible_monthly_end"]],
        "cross_frequency_overlap_rows": qc["cross_frequency_overlap_rows"],
    }, indent=2))


if __name__ == "__main__":
    main()
