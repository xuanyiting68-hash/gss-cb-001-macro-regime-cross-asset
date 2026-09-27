#!/usr/bin/env python3
"""Frozen 041 discrete-horizon descriptive cash-hurdle map; no network access."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/fed_cycle_cash_hurdle_horizon_crossing_041_v1"
PHASES = ["FIRST_HIKE", "LAST_HIKE", "PAUSE_START", "FIRST_CUT"]
ASSETS = ["GOLD", "SP500", "NASDAQ", "WTI", "DXY", "VUSTX_LONG_TREASURY_PROXY", "VGSIX_REIT_PROXY", "BTC_USD"]
TIERS = dict(zip(ASSETS, ["CORE_SUPPORTED"] * 5 + ["SUPPORTED_PROXY_DESCRIPTIVE", "LIMITED_PROXY_DESCRIPTIVE", "LIMITED_DESCRIPTIVE"]))
HORIZONS = (3, 6, 12)
PATTERNS = [f"{i:03b}" for i in range(8)]
SOURCES = {
    "004": "results/fed_cycle_phase_clock_v1/PHASE_CYCLE_ASSET_METRICS.csv",
    "014_MARKET": "results/fed_cycle_cross_asset_expansion_v1/MARKET_PHASE_METRICS.csv",
    "035": "results/fed_cycle_long_treasury_proxy_bridge_035_v1/VUSTX_EXTENDED_PHASE_METRICS.csv",
    "036": "results/fed_cycle_listed_reit_proxy_bridge_036_v1/VGSIX_EXTENDED_PHASE_METRICS.csv",
    "014_CASH": "results/fed_cycle_cross_asset_expansion_v1/CASH_PHASE_METRICS.csv",
    "040_FROZEN_INPUT": "data/public/CASH_HURDLE_REAL_RETURN_EVENT_INPUTS_20260927.csv",
    "040_PANEL": "results/fed_cycle_cash_hurdle_real_return_map_040_v1/EVENT_HURDLE_REAL_RETURN_PANEL.csv",
}
KEY = ["asset", "anchor", "cycle_id"]
EVENT_KEY = ["anchor", "cycle_id"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def weighted_median(values, weights):
    v, w = np.asarray(values, float), np.asarray(weights, float)
    order = np.argsort(v, kind="stable")
    return float(v[order][np.searchsorted(np.cumsum(w[order]), w.sum() * .5, side="left")])


def weighted_share(flags, weights):
    return float(np.average(np.asarray(flags, float), weights=np.asarray(weights, float)))


def fail_if(condition, message):
    if condition:
        raise ValueError(message)


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    qc_paths = {
        "004": "results/fed_cycle_phase_clock_v1/QC.json",
        "014": "results/fed_cycle_cross_asset_expansion_v1/QC.json",
        "035": "results/fed_cycle_long_treasury_proxy_bridge_035_v1/QC.json",
        "036": "results/fed_cycle_listed_reit_proxy_bridge_036_v1/QC.json",
        "040": "results/fed_cycle_cash_hurdle_real_return_map_040_v1/QC.json",
    }
    upstream = {k: json.loads((ROOT / p).read_text())["qc_gate"] for k, p in qc_paths.items()}
    fail_if(any(s != "PASS" for s in upstream.values()), f"upstream QC failed: {upstream}")
    source = pd.DataFrame([{"source_id": k, "path": p, "sha256": sha256(ROOT / p), "bytes": (ROOT / p).stat().st_size} for k, p in SOURCES.items()])
    cols = ["asset", "asset_label", "anchor", "cycle_id", "broad_episode_id", "anchor_date", "episode_weight"] + [f"ret_{h}m" for h in HORIZONS]
    parts = []
    for k, allowed in [("004", ASSETS[:4]), ("014_MARKET", ["DXY", "BTC_USD"]), ("035", [ASSETS[5]]), ("036", [ASSETS[6]])]:
        df = pd.read_csv(ROOT / SOURCES[k]); fail_if(any(c not in df for c in cols), f"{k} missing columns")
        parts.append(df.loc[df.asset.isin(allowed) & df.anchor.isin(PHASES), cols])
    ev = pd.concat(parts, ignore_index=True)
    cash = pd.read_csv(ROOT / SOURCES["014_CASH"])
    inp = pd.read_csv(ROOT / SOURCES["040_FROZEN_INPUT"])
    prior = pd.read_csv(ROOT / SOURCES["040_PANEL"])
    fail_if(len(ev) != 232 or len(prior) != 232 or len(cash) != 37 or len(inp) != 37, "frozen row count mismatch")
    for name, df, keys in [("asset events", ev, KEY), ("040", prior, KEY), ("cash", cash, EVENT_KEY), ("input", inp, EVENT_KEY)]:
        fail_if(df.duplicated(keys).any(), f"duplicate {name} keys")
    ev = ev.merge(cash[EVENT_KEY + ["broad_episode_id", "anchor_date", "episode_weight"] + [f"cash_carry_{h}m" for h in HORIZONS]], on=EVENT_KEY, suffixes=("", "_cash"), validate="many_to_one")
    ev = ev.merge(inp[EVENT_KEY + ["broad_episode_id", "anchor_month", "fedfunds_monthly_pct"]], on=EVENT_KEY, suffixes=("", "_input"), validate="many_to_one")
    ev = ev.merge(prior[KEY + ["evidence_tier", "broad_episode_id", "anchor_date", "episode_weight", "ret_12m", "matched_cash_carry", "asset_vs_cash", "beats_cash", "positive_nominal_but_not_cash"]], on=KEY, suffixes=("", "_040"), validate="one_to_one")
    fail_if(len(ev) != 232 or set(map(tuple, ev[KEY].to_numpy())) != set(map(tuple, prior[KEY].to_numpy())), "event keys differ from 040")
    for c in ["broad_episode_id", "broad_episode_id_cash", "broad_episode_id_input", "broad_episode_id_040"]:
        fail_if(ev[c].isna().any() or (ev[c].astype(str) != ev.broad_episode_id.astype(str)).any(), f"episode mismatch: {c}")
    fail_if((pd.to_datetime(ev.anchor_date) != pd.to_datetime(ev.anchor_date_cash)).any() or (pd.to_datetime(ev.anchor_date) != pd.to_datetime(ev.anchor_date_040)).any(), "anchor dates differ")
    fail_if((pd.to_datetime(ev.anchor_date).dt.to_period("M").astype(str) != ev.anchor_month.astype(str)).any(), "frozen rate month mismatch")
    for c in ["episode_weight", "ret_12m"]:
        fail_if(not np.allclose(ev[c], ev[c + "_040"], rtol=0, atol=1e-12), f"040 {c} mismatch")
    fail_if(not np.allclose(ev.episode_weight, ev.episode_weight_cash, rtol=0, atol=1e-12), "cash weight mismatch")
    fail_if((ev.episode_weight <= 0).any() or ev.episode_weight.isna().any(), "invalid weights")
    for _, g in ev.groupby(["asset", "anchor", "broad_episode_id"]):
        fail_if(abs(g.episode_weight.sum() - 1) > 1e-10, "episode weight does not sum to 1")
    fail_if(not ev.asset.isin(ASSETS).all() or not ev.anchor.isin(PHASES).all(), "asset/phase leakage")
    fail_if(any(set(ev.loc[ev.asset == a, "evidence_tier"]) != {tier} for a, tier in TIERS.items()), "evidence tier mismatch")
    required = [f"ret_{h}m" for h in HORIZONS] + [f"cash_carry_{h}m" for h in HORIZONS] + ["fedfunds_monthly_pct"]
    fail_if(ev[required].isna().any().any(), "missing horizon return, cash, or anchor rate")
    for c in required:
        ev[c] = pd.to_numeric(ev[c], errors="raise")
    fail_if((ev[[f"ret_{h}m" for h in HORIZONS]] <= -1).any().any(), "invalid asset gross return")

    ev["asset_order"] = ev.asset.map({a: i for i, a in enumerate(ASSETS)})
    ev["phase_order"] = ev.anchor.map({a: i for i, a in enumerate(PHASES)})
    ev = ev.sort_values(["asset_order", "phase_order", "anchor_date", "cycle_id"]).reset_index(drop=True)
    long = []
    for h in HORIZONS:
        post = ev[f"cash_carry_{h}m"]
        matched = (1 + post) * (1 + ev.fedfunds_monthly_pct / 1200) - 1
        excess = (1 + ev[f"ret_{h}m"]) / (1 + matched) - 1
        ev[f"matched_cash_{h}m"] = matched
        ev[f"asset_vs_cash_{h}m"] = excess
        ev[f"beats_cash_{h}m"] = excess > 0
        ev[f"positive_nominal_but_not_cash_{h}m"] = (ev[f"ret_{h}m"] > 0) & ~(excess > 0)
        for r in ev.itertuples(index=False):
            long.append({"asset": r.asset, "anchor": r.anchor, "cycle_id": r.cycle_id, "broad_episode_id": r.broad_episode_id,
                         "episode_weight": r.episode_weight, "evidence_tier": r.evidence_tier, "horizon_months": h,
                         "nominal_ret": getattr(r, f"ret_{h}m"), "canonical_cash_014_post": getattr(r, f"cash_carry_{h}m"),
                         "matched_cash": getattr(r, f"matched_cash_{h}m"), "asset_vs_cash": getattr(r, f"asset_vs_cash_{h}m"),
                         "nominal_positive": getattr(r, f"ret_{h}m") > 0, "beats_cash": getattr(r, f"beats_cash_{h}m"),
                         "positive_nominal_but_not_cash": getattr(r, f"positive_nominal_but_not_cash_{h}m")})
    delta_cash = np.abs(ev.matched_cash_12m - ev.matched_cash_carry).max()
    delta_excess = np.abs(ev.asset_vs_cash_12m - ev.asset_vs_cash).max()
    fail_if(delta_cash > 1e-12 or delta_excess > 1e-12, "12M reproduction of 040 failed")
    for col in ["beats_cash", "positive_nominal_but_not_cash"]:
        fail_if((ev[f"{col}_12m"] != ev[col]).any(), f"040 {col} flag mismatch")
    ev["pattern_3_6_12"] = ev.apply(lambda r: "".join(str(int(r[f"beats_cash_{h}m"])) for h in HORIZONS), axis=1)
    fail_if(not ev.pattern_3_6_12.isin(PATTERNS).all(), "invalid bit pattern")
    ev["first_observed_beating_horizon"] = ev.apply(lambda r: next((f"{h}M" for h in HORIZONS if r[f"beats_cash_{h}m"]), "NONE"), axis=1)
    ev["last_observed_below_cash_horizon"] = ev.apply(lambda r: next((f"{h}M" for h in reversed(HORIZONS) if not r[f"beats_cash_{h}m"]), "NONE"), axis=1)
    ev["late_improvement_by_12m"] = ev.pattern_3_6_12.isin(["001", "011"])
    ev["early_advantage_lost_by_12m"] = ev.pattern_3_6_12.isin(["010", "100", "110"])
    ev["mixed_nonmonotonic"] = ev.pattern_3_6_12.isin(["010", "101", "110"])
    summary, patterns = [], []
    for asset in ASSETS:
        for phase in PHASES:
            g = ev[(ev.asset == asset) & (ev.anchor == phase)]
            fail_if(g.empty, f"missing {asset}/{phase}")
            w = g.episode_weight
            row = {"asset": asset, "anchor": phase, "evidence_tier": TIERS[asset], "n_legs": g.cycle_id.nunique(), "n_broad_episodes": g.broad_episode_id.nunique()}
            for h in HORIZONS:
                row.update({f"weighted_median_nominal_ret_{h}m": weighted_median(g[f"ret_{h}m"], w),
                            f"weighted_median_matched_cash_{h}m": weighted_median(g[f"matched_cash_{h}m"], w),
                            f"weighted_median_asset_vs_cash_{h}m": weighted_median(g[f"asset_vs_cash_{h}m"], w),
                            f"weighted_share_beats_cash_{h}m": weighted_share(g[f"beats_cash_{h}m"], w),
                            f"weighted_share_positive_nominal_but_not_cash_{h}m": weighted_share(g[f"positive_nominal_but_not_cash_{h}m"], w)})
            for pat in PATTERNS:
                patterns.append({"asset": asset, "anchor": phase, "evidence_tier": TIERS[asset], "pattern_3_6_12": pat,
                                 "n_legs": int((g.pattern_3_6_12 == pat).sum()),
                                 "weighted_share": weighted_share(g.pattern_3_6_12 == pat, w)})
            for name, flag in [("000", g.pattern_3_6_12 == "000"), ("111", g.pattern_3_6_12 == "111"),
                               ("late_improvement_by_12m", g.late_improvement_by_12m),
                               ("early_advantage_lost_by_12m", g.early_advantage_lost_by_12m)]:
                row[f"weighted_share_{name}"] = weighted_share(flag, w)
            summary.append(row)
    summary = pd.DataFrame(summary)
    pattern_df = pd.DataFrame(patterns)
    long = pd.DataFrame(long)
    fail_if(len(summary) != 32 or len(pattern_df) != 256 or len(long) != 696, "output row count mismatch")
    fail_if(not np.allclose(pattern_df.groupby(["asset", "anchor"]).weighted_share.sum(), 1, atol=1e-12), "pattern shares do not sum to one")
    fail_if(not np.isfinite(long[["nominal_ret", "matched_cash", "asset_vs_cash"]]).all().all(), "non-finite horizon value")
    ev.drop(columns=["broad_episode_id_cash", "broad_episode_id_input", "broad_episode_id_040", "anchor_date_cash", "anchor_date_040", "episode_weight_cash", "episode_weight_040", "ret_12m_040"]).to_csv(OUT / "EVENT_HORIZON_PATTERN_PANEL.csv", index=False)
    long.to_csv(OUT / "HORIZON_LONG_PANEL.csv", index=False)
    summary.to_csv(OUT / "ASSET_PHASE_HORIZON_SUMMARY.csv", index=False)
    pattern_df.to_csv(OUT / "EIGHT_PATTERN_DISTRIBUTION.csv", index=False)
    source.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    qc = {"module": "FED-CYCLE-CASH-HURDLE-HORIZON-CROSSING-041", "qc_gate": "PASS", "upstream_qc": upstream,
          "event_rows": len(ev), "horizon_rows": len(long), "summary_rows": len(summary), "pattern_rows": len(pattern_df),
          "unique_macro_event_keys": len(inp), "max_abs_040_cash_delta": float(delta_cash), "max_abs_040_asset_vs_cash_delta": float(delta_excess),
          "source_hashes": dict(zip(source.source_id, source.sha256)), "horizons_months": list(HORIZONS),
          "monthly_crossover_estimated": False, "new_p_values": False, "optimized_horizon": False,
          "causal_claim": False, "forecast": False, "deployable": False, "private_paper_inputs": False}
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n")
    lines = ["# 041 Cash-hurdle horizon crossing — report", "", "**QC PASS / DISCRETE 3M–6M–12M DESCRIPTIVE / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**", "",
             "The observed three endpoints do not identify the month of an intervening cash-hurdle crossover. Asset and phase rows remain in frozen order; limited sample tiers are unchanged.", "",
             "## Whole-panel diagnostics", ""]
    for h in HORIZONS:
        g = long[long.horizon_months == h]
        lines.append(f"- {h}M: {int(g.nominal_positive.sum())} positive nominal event rows; {int(g.positive_nominal_but_not_cash.sum())} positive nominal rows still below matched cash (out of {len(g)} asset-event rows; overlapping rows are not independent observations).")
    lines += ["", "## Fixed-order asset × phase examples", ""]
    for row in summary.itertuples():
        lines.append(f"- {row.asset} / {row.anchor} [{row.evidence_tier}; {row.n_legs} legs, {row.n_broad_episodes} broad episodes]: cash-relative weighted medians 3M {row.weighted_median_asset_vs_cash_3m:+.1%}, 6M {row.weighted_median_asset_vs_cash_6m:+.1%}, 12M {row.weighted_median_asset_vs_cash_12m:+.1%}; 000 share {row.weighted_share_000:.0%}, 111 share {row.weighted_share_111:.0%}, late improvement {row.weighted_share_late_improvement_by_12m:.0%}, early advantage lost {row.weighted_share_early_advantage_lost_by_12m:.0%}.")
    lines += ["", "## Interpretation", "", "Each 3M/6M/12M return includes the anchor month t from baseline t-1; mechanical cash adds that month's official FEDFUNDS rate to canonical 014 post-anchor cash. 12M values reproduce 040 to tolerance 1e-12. The pattern describes three discrete observations, not within-month or intervening-month crossing, investable cash rates, expected returns, causal Fed effects or a current allocation rule."]
    (OUT / "FED_CYCLE_CASH_HURDLE_HORIZON_CROSSING_041_REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: qc[k] for k in ("qc_gate", "event_rows", "horizon_rows", "summary_rows", "pattern_rows", "max_abs_040_cash_delta", "max_abs_040_asset_vs_cash_delta")}, indent=2))


if __name__ == "__main__":
    run()
