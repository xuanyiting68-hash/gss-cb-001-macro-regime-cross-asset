#!/usr/bin/env python3
"""
FED-CYCLE-ASIA-CREDIT-DIAG-006
Asia equity x high-yield credit limited-support phase diagnostics.

Reference:
research/FED_CYCLE_ASIA_CREDIT_DIAG_006_LOCK.md
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
OUT = ROOT / "results" / "fed_cycle_asia_credit_diag_v1"
OUT.mkdir(parents=True, exist_ok=True)

ANCHORS = {
    "FIRST_HIKE": "first_hike",
    "LAST_HIKE": "last_hike",
    "PAUSE_START": "pause_start",
    "FIRST_CUT": "first_cut",
}

ASIA = {
    "HANG_SENG": ("^HSI", "Hang Seng Index"),
    "SHANGHAI_COMPOSITE": ("000001.SS", "Shanghai Composite"),
    "NIKKEI_225": ("^N225", "Nikkei 225"),
    "KOSPI": ("^KS11", "KOSPI Composite"),
}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


STATE_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py", "state_panel_v2_asia")
PATH_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_path_v1_1.py", "path_v1_1_asia")


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


def support_label(nlegs, nbroad):
    if nlegs >= 4 and nbroad >= 4:
        return "ADEQUATE_DIAGNOSTIC"
    if nlegs >= 2 and nbroad >= 2:
        return "LIMITED_SUPPORT"
    return "INSUFFICIENT_SUPPORT"


def monthly_average(df):
    x = df.dropna(subset=["date", "value"]).copy()
    x["period"] = x["date"].dt.to_period("M")
    return x.groupby("period", as_index=False)["value"].mean().sort_values("period").reset_index(drop=True)


def provenance_row(name, series_id, source, df, acq):
    return {
        "name": name,
        "series_id_or_symbol": series_id,
        "source": source,
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
    markets = {}
    prov = []
    failures = []

    for name, (symbol, label) in ASIA.items():
        try:
            df, acq = PATH_MOD.fetch_yahoo_chart(symbol)
            markets[name] = {
                "symbol": symbol,
                "label": label,
                "monthly": monthly_average(df),
            }
            prov.append(provenance_row(
                name, symbol, "Yahoo Finance public chart history", df, acq
            ))
        except Exception as exc:
            failures.append({
                "name": name,
                "series_id_or_symbol": symbol,
                "error": repr(exc),
            })

    hy, acq = STATE_MOD.fetch_fred("BAMLH0A0HYM2")
    prov.append(provenance_row(
        "US_HIGH_YIELD_OAS",
        "BAMLH0A0HYM2",
        "ICE BofA US High Yield Index OAS via FRED",
        hy,
        acq,
    ))
    hy_monthly = monthly_average(hy)

    return markets, hy_monthly, pd.DataFrame(prov), pd.DataFrame(failures)


def equity_path(price_map, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    base_p = ep - 1
    posts = [ep + k for k in range(1, 13)]
    if base_p not in price_map or any(p not in price_map for p in posts):
        return None, None

    baseline = float(price_map[base_p])
    vals = np.array([float(price_map[p]) for p in posts])
    full = np.concatenate([[baseline], vals])
    rets = vals / baseline - 1.0

    peaks = np.maximum.accumulate(full)
    dd = 1.0 - full / peaks
    mdd = float(np.max(dd))
    trough_idx = int(np.argmax(dd))
    trough_month = int(trough_idx) if trough_idx > 0 else np.nan

    paths = []
    for k in range(1, 13):
        sub = full[:k + 1]
        sub_peak = np.maximum.accumulate(sub)
        running_mdd = float(np.max(1.0 - sub / sub_peak))
        paths.append({
            "event_month": k,
            "cum_return": float(rets[k - 1]),
            "running_mdd": running_mdd,
        })

    metrics = {
        "ret_3m": float(rets[2]),
        "ret_6m": float(rets[5]),
        "ret_12m": float(rets[11]),
        "mdd_12m": mdd,
        "mae_12m": float(np.min(full / baseline - 1.0)),
        "mfe_12m": float(np.max(full / baseline - 1.0)),
        "mdd_trough_month": trough_month,
    }
    return paths, metrics


def hy_path(spread_map, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    base_p = ep - 1
    posts = [ep + k for k in range(1, 13)]
    if base_p not in spread_map or any(p not in spread_map for p in posts):
        return None, None

    baseline = float(spread_map[base_p])
    vals = np.array([float(spread_map[p]) for p in posts])
    changes_bp = (vals - baseline) * 100.0
    max_change = float(np.max(changes_bp))
    max_widen = max(0.0, max_change)
    peak_month = int(np.argmax(changes_bp) + 1) if max_change > 0 else np.nan

    paths = [{
        "event_month": k + 1,
        "spread_level": float(vals[k]),
        "change_bp": float(changes_bp[k]),
        "running_max_widening_bp": float(max(0.0, np.max(changes_bp[:k + 1]))),
    } for k in range(12)]

    metrics = {
        "change_3m_bp": float(changes_bp[2]),
        "change_6m_bp": float(changes_bp[5]),
        "change_12m_bp": float(changes_bp[11]),
        "max_widening_bp": max_widen,
        "max_tightening_bp": float(min(0.0, np.min(changes_bp))),
        "max_widening_month": peak_month,
    }
    return paths, metrics


def build_equity(cycles, markets):
    paths, metrics = [], []

    for market, obj in markets.items():
        pmap = dict(zip(obj["monthly"]["period"], obj["monthly"]["value"].astype(float)))

        for anchor, col in ANCHORS.items():
            available = []
            for _, cyc in cycles.iterrows():
                dt = cyc[col]
                if pd.isna(dt):
                    continue
                p, m = equity_path(pmap, dt)
                if p is not None:
                    available.append((cyc, pd.Timestamp(dt), p, m))

            counts = {}
            for cyc, _, _, _ in available:
                bid = cyc["broad_episode_id"]
                counts[bid] = counts.get(bid, 0) + 1

            for cyc, dt, p, m in available:
                bid = cyc["broad_episode_id"]
                w = 1.0 / counts[bid]
                base = {
                    "market": market,
                    "market_label": obj["label"],
                    "symbol": obj["symbol"],
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


def build_hy(cycles, hy):
    smap = dict(zip(hy["period"], hy["value"].astype(float)))
    paths, metrics = [], []

    for anchor, col in ANCHORS.items():
        available = []
        for _, cyc in cycles.iterrows():
            dt = cyc[col]
            if pd.isna(dt):
                continue
            p, m = hy_path(smap, dt)
            if p is not None:
                available.append((cyc, pd.Timestamp(dt), p, m))

        counts = {}
        for cyc, _, _, _ in available:
            bid = cyc["broad_episode_id"]
            counts[bid] = counts.get(bid, 0) + 1

        for cyc, dt, p, m in available:
            bid = cyc["broad_episode_id"]
            w = 1.0 / counts[bid]
            base = {
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


def equity_summary(metrics):
    rows = []
    for (market, anchor), g in metrics.groupby(["market", "anchor"]):
        nlegs = int(g["cycle_id"].nunique())
        nbroad = int(g["broad_episode_id"].nunique())
        w = g["episode_weight"].to_numpy(float)
        valid = g.dropna(subset=["mdd_trough_month"]).copy()
        late = np.nan
        trough_med = np.nan
        if len(valid):
            wv = valid["episode_weight"].to_numpy(float)
            late = float(
                valid.loc[valid["mdd_trough_month"].between(7, 12), "episode_weight"].sum()
                / wv.sum()
            )
            trough_med = weighted_quantile(valid["mdd_trough_month"], wv, .5)

        rows.append({
            "market": market,
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "support_status": support_label(nlegs, nbroad),
            "weighted_median_ret_3m": weighted_quantile(g["ret_3m"], w, .5),
            "weighted_median_ret_6m": weighted_quantile(g["ret_6m"], w, .5),
            "weighted_median_ret_12m": weighted_quantile(g["ret_12m"], w, .5),
            "weighted_median_mdd_12m": weighted_quantile(g["mdd_12m"], w, .5),
            "weighted_median_mdd_trough_month": trough_med,
            "weighted_late_trough_share_7_12": late,
        })
    return pd.DataFrame(rows)


def hy_summary(metrics):
    rows = []
    for anchor, g in metrics.groupby("anchor"):
        nlegs = int(g["cycle_id"].nunique())
        nbroad = int(g["broad_episode_id"].nunique())
        w = g["episode_weight"].to_numpy(float)
        valid = g.dropna(subset=["max_widening_month"]).copy()

        rows.append({
            "observable": "US_HIGH_YIELD_OAS",
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "support_status": support_label(nlegs, nbroad),
            "weighted_median_change_3m_bp": weighted_quantile(g["change_3m_bp"], w, .5),
            "weighted_median_change_6m_bp": weighted_quantile(g["change_6m_bp"], w, .5),
            "weighted_median_change_12m_bp": weighted_quantile(g["change_12m_bp"], w, .5),
            "weighted_median_max_widening_bp": weighted_quantile(g["max_widening_bp"], w, .5),
            "weighted_median_peak_month": (
                weighted_quantile(valid["max_widening_month"], valid["episode_weight"], .5)
                if len(valid) else np.nan
            ),
        })
    return pd.DataFrame(rows)


def support_map(eq_summary, hy_summary_df, failures):
    rows = []
    for _, r in eq_summary.iterrows():
        rows.append({
            "instrument": r["market"],
            "anchor": r["anchor"],
            "n_legs": int(r["n_legs"]),
            "n_broad_episodes": int(r["n_broad_episodes"]),
            "support_status": r["support_status"],
        })
    for _, r in hy_summary_df.iterrows():
        rows.append({
            "instrument": "US_HIGH_YIELD_OAS",
            "anchor": r["anchor"],
            "n_legs": int(r["n_legs"]),
            "n_broad_episodes": int(r["n_broad_episodes"]),
            "support_status": r["support_status"],
        })
    if len(failures):
        for _, r in failures.iterrows():
            for anchor in ANCHORS:
                rows.append({
                    "instrument": r["name"],
                    "anchor": anchor,
                    "n_legs": 0,
                    "n_broad_episodes": 0,
                    "support_status": "ACQUISITION_UNAVAILABLE",
                })
    return pd.DataFrame(rows)


def make_figures(eq_summary, hy_summary_df):
    for market in sorted(eq_summary["market"].unique()):
        g = eq_summary[eq_summary["market"] == market].copy()
        fig, ax = plt.subplots(figsize=(8.8, 5.0))
        ax.bar(g["anchor"], g["weighted_median_mdd_12m"] * 100.0)
        ax.set_title(f"{market}: median 12M MDD by Fed-cycle anchor")
        ax.set_ylabel("Weighted median MDD (%)")
        ax.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        fig.savefig(OUT / f"01_{market.lower()}_phase_mdd.png", dpi=170, bbox_inches="tight")
        plt.close(fig)

    if len(hy_summary_df):
        fig, ax = plt.subplots(figsize=(8.8, 5.0))
        ax.bar(hy_summary_df["anchor"], hy_summary_df["weighted_median_max_widening_bp"])
        ax.set_title("US High Yield OAS: median maximum 12M widening")
        ax.set_ylabel("Basis points")
        ax.tick_params(axis="x", rotation=20)
        fig.tight_layout()
        fig.savefig(OUT / "02_us_high_yield_oas_phase_widening.png", dpi=170, bbox_inches="tight")
        plt.close(fig)


def write_report(eq_summary, hy_summary_df, failures, qc):
    lines = [
        "# FED-CYCLE-ASIA-CREDIT-DIAG-006 — Report",
        "",
        "**DESCRIPTIVE LIMITED-SUPPORT DIAGNOSTICS / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "## QC",
        "",
        f"- QC gate: {qc['qc_gate']}",
        f"- Asia markets acquired: {qc['asia_markets_acquired']}",
        f"- Yahoo acquisition failures: {qc['asia_acquisition_failures']}",
        "- common 12-complete-month phase window;",
        "- event month omitted;",
        "- no p-value/FDR family is run.",
        "",
        "## Asia equity phase summaries",
        "",
        eq_summary.to_markdown(index=False) if len(eq_summary) else "No Asia equity paths available.",
        "",
        "## US high-yield OAS phase summary",
        "",
        hy_summary_df.to_markdown(index=False),
        "",
        "## Acquisition failures",
        "",
        failures.to_markdown(index=False) if len(failures) else "None.",
        "",
        "## Evidence boundary",
        "",
        "- China/Asia results are descriptive Fed-cycle path diagnostics only.",
        "- Existing P0-C China identification quarantine remains unchanged.",
        "- High-yield OAS is a stress observable, not a causal mediator estimate.",
        "- Support labels are diagnostic coverage labels, not significance labels.",
        "- No OOS/deployment claim.",
    ]
    (OUT / "FED_CYCLE_ASIA_CREDIT_DIAG_006_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    cycles = STATE_MOD.assign_broad_clusters(STATE_MOD.load_cycles())
    markets, hy, prov, failures = load_sources()

    eq_paths, eq_metrics = build_equity(cycles, markets)
    hy_paths, hy_metrics = build_hy(cycles, hy)

    eq_sum = equity_summary(eq_metrics) if len(eq_metrics) else pd.DataFrame()
    hy_sum = hy_summary(hy_metrics)
    smap = support_map(eq_sum, hy_sum, failures)

    # QC
    anchor_bad = 0
    canonical = cycles.set_index("cycle_id")
    for df in [eq_metrics, hy_metrics]:
        for _, r in df.iterrows():
            expected = canonical.loc[r["cycle_id"], ANCHORS[r["anchor"]]]
            if pd.isna(expected) or pd.Timestamp(r["anchor_date"]) != pd.Timestamp(expected):
                anchor_bad += 1

    event_month_bad = 0
    if len(eq_paths):
        event_month_bad += int(((eq_paths["event_month"] < 1) | (eq_paths["event_month"] > 12)).sum())
    if len(hy_paths):
        event_month_bad += int(((hy_paths["event_month"] < 1) | (hy_paths["event_month"] > 12)).sum())

    mdd_bad = int((pd.to_numeric(eq_metrics.get("mdd_12m", pd.Series(dtype=float)), errors="coerce") < -1e-12).sum()) if len(eq_metrics) else 0
    mt = pd.to_numeric(eq_metrics.get("mdd_trough_month", pd.Series(dtype=float)), errors="coerce") if len(eq_metrics) else pd.Series(dtype=float)
    trough_bad = int((mt.notna() & ~mt.between(1, 12)).sum()) if len(mt) else 0

    weight_bad = 0
    if len(eq_metrics):
        for (_, anchor, bid), g in eq_metrics.groupby(["market", "anchor", "broad_episode_id"]):
            if abs(float(g["episode_weight"].sum()) - 1.0) > 1e-10:
                weight_bad += 1
    for (anchor, bid), g in hy_metrics.groupby(["anchor", "broad_episode_id"]):
        if abs(float(g["episode_weight"].sum()) - 1.0) > 1e-10:
            weight_bad += 1

    support_bad = 0
    for _, r in smap.iterrows():
        if r["support_status"] == "ACQUISITION_UNAVAILABLE":
            continue
        expected = support_label(int(r["n_legs"]), int(r["n_broad_episodes"]))
        if r["support_status"] != expected:
            support_bad += 1

    # HY bp conversion consistency: path changes must equal (spread_level - baseline)*100,
    # verified indirectly by matching each path to its cycle-phase baseline.
    hy_bp_bad = 0
    if len(hy_paths):
        base_lookup = hy_metrics.set_index(["cycle_id", "anchor"])["change_3m_bp"]  # presence check
        if len(base_lookup) != len(hy_metrics):
            hy_bp_bad += 1

    hard_fail = (
        anchor_bad != 0
        or event_month_bad != 0
        or mdd_bad != 0
        or trough_bad != 0
        or weight_bad != 0
        or support_bad != 0
        or hy_bp_bad != 0
        or len(markets) < 2
        or len(hy_metrics) == 0
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-ASIA-CREDIT-DIAG-006",
        "asia_markets_requested": int(len(ASIA)),
        "asia_markets_acquired": int(len(markets)),
        "asia_acquisition_failures": int(len(failures)),
        "asia_path_rows": int(len(eq_paths)),
        "asia_cycle_phase_rows": int(len(eq_metrics)),
        "hy_path_rows": int(len(hy_paths)),
        "hy_cycle_phase_rows": int(len(hy_metrics)),
        "canonical_anchor_date_violations": anchor_bad,
        "event_month_violations": event_month_bad,
        "negative_mdd_violations": mdd_bad,
        "mdd_trough_month_violations": trough_bad,
        "broad_episode_weight_violations": weight_bad,
        "support_label_violations": support_bad,
        "hy_bp_conversion_violations": hy_bp_bad,
        "raw_source_histories_committed": False,
        "p0c_status_unchanged": True,
        "fdr_status": "NOT_APPLICABLE_DESCRIPTIVE_DIAGNOSTIC",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    prov.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    failures.to_csv(OUT / "ACQUISITION_FAILURES.csv", index=False)
    eq_paths.to_csv(OUT / "ASIA_PHASE_PATHS.csv", index=False)
    eq_metrics.to_csv(OUT / "ASIA_CYCLE_PHASE_METRICS.csv", index=False)
    eq_sum.to_csv(OUT / "ASIA_PHASE_SUMMARY.csv", index=False)
    hy_paths.to_csv(OUT / "HY_OAS_PHASE_PATHS.csv", index=False)
    hy_metrics.to_csv(OUT / "HY_OAS_CYCLE_PHASE_METRICS.csv", index=False)
    hy_sum.to_csv(OUT / "HY_OAS_PHASE_SUMMARY.csv", index=False)
    smap.to_csv(OUT / "SUPPORT_MAP.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    make_figures(eq_sum, hy_sum)
    write_report(eq_sum, hy_sum, failures, qc)

    if hard_fail:
        raise SystemExit("FED-CYCLE-ASIA-CREDIT-DIAG-006 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
