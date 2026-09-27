#!/usr/bin/env python3
"""
FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040

Preregistered descriptive module.
Compares canonical asset phase endpoints with:
1) a same-month-grid mechanical DFF cash hurdle;
2) matched ex-post CPI purchasing-power inflation;
3) canonical 12M path MDD.

No ranking, no forecast, no causal claim, no trading instruction.
"""

from __future__ import annotations

import hashlib
import io
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_cash_hurdle_real_return_map_040_v1"
OUT.mkdir(parents=True, exist_ok=True)

PHASES = ["FIRST_HIKE", "LAST_HIKE", "PAUSE_START", "FIRST_CUT"]
ASSET_ORDER = [
    "GOLD",
    "SP500",
    "NASDAQ",
    "WTI",
    "DXY",
    "VUSTX_LONG_TREASURY_PROXY",
    "VGSIX_REIT_PROXY",
    "BTC_USD",
]
EVIDENCE_TIER = {
    "GOLD": "CORE_SUPPORTED",
    "SP500": "CORE_SUPPORTED",
    "NASDAQ": "CORE_SUPPORTED",
    "WTI": "CORE_SUPPORTED",
    "DXY": "CORE_SUPPORTED",
    "VUSTX_LONG_TREASURY_PROXY": "SUPPORTED_PROXY_DESCRIPTIVE",
    "VGSIX_REIT_PROXY": "LIMITED_PROXY_DESCRIPTIVE",
    "BTC_USD": "LIMITED_DESCRIPTIVE",
}
SOURCE_MODULE = {
    "GOLD": "004_PHASE_CLOCK",
    "SP500": "004_PHASE_CLOCK",
    "NASDAQ": "004_PHASE_CLOCK",
    "WTI": "004_PHASE_CLOCK",
    "DXY": "014_CROSS_ASSET_EXPANSION",
    "BTC_USD": "014_CROSS_ASSET_EXPANSION",
    "VUSTX_LONG_TREASURY_PROXY": "035_LONG_TREASURY_PROXY",
    "VGSIX_REIT_PROXY": "036_LISTED_REIT_PROXY",
}
FRED = {
    "DFF": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF&cosd=1983-01-01",
    "CPIAUCSL": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL&cosd=1983-01-01",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def assert_upstream_qc():
    deps = {
        "004": ROOT / "results/fed_cycle_phase_clock_v1/QC.json",
        "014": ROOT / "results/fed_cycle_cross_asset_expansion_v1/QC.json",
        "035": ROOT / "results/fed_cycle_long_treasury_proxy_bridge_035_v1/QC.json",
        "036": ROOT / "results/fed_cycle_listed_reit_proxy_bridge_036_v1/QC.json",
    }
    out = {}
    for key, path in deps.items():
        obj = read_json(path)
        gate = obj.get("qc_gate")
        if gate != "PASS":
            raise RuntimeError(f"upstream {key} QC is not PASS: {gate}")
        out[key] = gate
    return out


def fetch_bytes(url: str, attempts: int = 4, timeout: int = 90) -> bytes:
    last = None
    headers = {"User-Agent": "Mozilla/5.0 research-reproducibility/1.0"}
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last = exc
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"fetch failed: {url}: {last!r}")


def fetch_fred(series: str):
    url = FRED[series]
    raw = fetch_bytes(url)
    df = pd.read_csv(io.BytesIO(raw))
    if df.shape[1] < 2:
        raise RuntimeError(f"{series} malformed FRED CSV")
    date_col = df.columns[0]
    value_col = series if series in df.columns else df.columns[1]
    x = pd.DataFrame({
        "date": pd.to_datetime(df[date_col], errors="coerce"),
        "value": pd.to_numeric(df[value_col].replace(".", np.nan), errors="coerce"),
    }).dropna()
    x = x.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)
    if len(x) < 100:
        raise RuntimeError(f"{series} history too short: {len(x)}")
    meta = {
        "series": series,
        "url": url,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "raw_bytes": len(raw),
        "rows_nonmissing": int(len(x)),
        "first_date": str(x["date"].min().date()),
        "last_date": str(x["date"].max().date()),
        "raw_committed": False,
    }
    return x, meta


def monthly_average(df: pd.DataFrame):
    x = df.copy()
    x["period"] = x["date"].dt.to_period("M")
    return x.groupby("period", as_index=False)["value"].mean().sort_values("period")


def weighted_median(values, weights):
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    ok = np.isfinite(v) & np.isfinite(w) & (w > 0)
    v, w = v[ok], w[ok]
    if len(v) == 0:
        return np.nan
    order = np.argsort(v)
    v, w = v[order], w[order]
    c = np.cumsum(w) / np.sum(w)
    return float(v[np.searchsorted(c, 0.5, side="left")])


def weighted_share(flag, weights):
    f = np.asarray(flag, dtype=float)
    w = np.asarray(weights, dtype=float)
    ok = np.isfinite(f) & np.isfinite(w) & (w > 0)
    if not ok.any():
        return np.nan
    return float(np.sum(f[ok] * w[ok]) / np.sum(w[ok]))


def load_asset_events():
    core = pd.read_csv(ROOT / "results/fed_cycle_phase_clock_v1/PHASE_CYCLE_ASSET_METRICS.csv")
    core = core[core["asset"].isin(["GOLD", "SP500", "NASDAQ", "WTI"])].copy()

    market = pd.read_csv(ROOT / "results/fed_cycle_cross_asset_expansion_v1/MARKET_PHASE_METRICS.csv")
    market = market[market["asset"].isin(["DXY", "BTC_USD"])].copy()

    vus = pd.read_csv(ROOT / "results/fed_cycle_long_treasury_proxy_bridge_035_v1/VUSTX_EXTENDED_PHASE_METRICS.csv")
    vgs = pd.read_csv(ROOT / "results/fed_cycle_listed_reit_proxy_bridge_036_v1/VGSIX_EXTENDED_PHASE_METRICS.csv")

    cols = [
        "asset", "asset_label", "anchor", "cycle_id", "broad_episode_id",
        "anchor_date", "episode_weight", "ret_12m", "mdd_12m",
    ]
    for name, df in [("core", core), ("market", market), ("vus", vus), ("vgs", vgs)]:
        missing = [c for c in cols if c not in df.columns]
        if missing:
            raise RuntimeError(f"{name} missing columns: {missing}")

    ev = pd.concat(
        [core[cols], market[cols], vus[cols], vgs[cols]],
        ignore_index=True,
    )
    ev = ev[ev["asset"].isin(ASSET_ORDER) & ev["anchor"].isin(PHASES)].copy()
    ev["anchor_date"] = pd.to_datetime(ev["anchor_date"])
    ev["evidence_tier"] = ev["asset"].map(EVIDENCE_TIER)
    ev["source_module"] = ev["asset"].map(SOURCE_MODULE)
    ev["asset_order"] = ev["asset"].map({a: i for i, a in enumerate(ASSET_ORDER)})
    ev["phase_order"] = ev["anchor"].map({a: i for i, a in enumerate(PHASES)})
    ev = ev.sort_values(["asset_order", "phase_order", "anchor_date", "cycle_id"]).reset_index(drop=True)

    if ev["evidence_tier"].isna().any():
        raise RuntimeError("asset evidence tier missing")
    if ev.duplicated(["asset", "anchor", "cycle_id"]).any():
        raise RuntimeError("duplicate asset-anchor-cycle rows")
    if ev["asset"].str.contains("FRESX", case=False, na=False).any():
        raise RuntimeError("rejected FRESX history entered 040")
    if ev["asset"].isin(["TLT", "VNQ"]).any():
        raise RuntimeError("duplicate target ETF rows entered 040")
    return ev


def attach_hurdles(ev: pd.DataFrame, dff_m: pd.DataFrame, cpi_m: pd.DataFrame):
    dff = dict(zip(dff_m["period"], dff_m["value"].astype(float)))
    cpi = dict(zip(cpi_m["period"], cpi_m["value"].astype(float)))

    canon = pd.read_csv(ROOT / "results/fed_cycle_cross_asset_expansion_v1/CASH_PHASE_METRICS.csv")
    canon = canon[["anchor", "cycle_id", "cash_carry_12m"]].rename(
        columns={"cash_carry_12m": "canonical_cash_014_post12"}
    )
    canon_key = canon.set_index(["anchor", "cycle_id"])["canonical_cash_014_post12"].to_dict()

    rows = []
    for _, r in ev.iterrows():
        ep = pd.Timestamp(r["anchor_date"]).to_period("M")
        baseline = ep - 1
        endpoint = ep + 12
        cash_months = [ep + k for k in range(0, 13)]

        missing_dff = [p for p in cash_months if p not in dff or not np.isfinite(dff[p])]
        if missing_dff:
            raise RuntimeError(f"missing DFF for {r['asset']} {r['anchor']} {r['cycle_id']}: {missing_dff}")

        if baseline not in cpi or endpoint not in cpi:
            raise RuntimeError(
                f"missing CPI for {r['asset']} {r['anchor']} {r['cycle_id']} "
                f"baseline={baseline} endpoint={endpoint}"
            )

        rates = np.array([dff[p] for p in cash_months], dtype=float)
        matched_cash = float(np.prod(1.0 + rates / 100.0 / 12.0) - 1.0)
        inflation = float(cpi[endpoint] / cpi[baseline] - 1.0)
        nominal = float(r["ret_12m"])
        key = (r["anchor"], r["cycle_id"])
        if key not in canon_key:
            raise RuntimeError(f"missing canonical cash cross-check row: {key}")
        canonical_cash = float(canon_key[key])

        asset_vs_cash = float((1.0 + nominal) / (1.0 + matched_cash) - 1.0)
        real_asset = float((1.0 + nominal) / (1.0 + inflation) - 1.0)
        real_cash = float((1.0 + matched_cash) / (1.0 + inflation) - 1.0)

        out = r.to_dict()
        out.update({
            "baseline_period": str(baseline),
            "endpoint_period": str(endpoint),
            "matched_cash_months": 13,
            "matched_cash_carry": matched_cash,
            "canonical_cash_014_post12": canonical_cash,
            "cash_timing_gap": matched_cash - canonical_cash,
            "matched_inflation": inflation,
            "asset_vs_cash": asset_vs_cash,
            "real_asset_return": real_asset,
            "real_cash_return": real_cash,
            "nominal_positive": nominal > 0.0,
            "beats_cash": asset_vs_cash > 0.0,
            "beats_inflation": real_asset > 0.0,
            "beats_both": (asset_vs_cash > 0.0) and (real_asset > 0.0),
            "positive_nominal_but_not_cash": (nominal > 0.0) and not (asset_vs_cash > 0.0),
            "positive_nominal_but_not_inflation": (nominal > 0.0) and not (real_asset > 0.0),
        })
        rows.append(out)

    panel = pd.DataFrame(rows)
    return panel


def summarize(panel: pd.DataFrame):
    rows = []
    for asset in ASSET_ORDER:
        for phase in PHASES:
            g = panel[(panel["asset"] == asset) & (panel["anchor"] == phase)].copy()
            if g.empty:
                continue
            w = g["episode_weight"].to_numpy(float)
            rows.append({
                "asset": asset,
                "asset_label": g["asset_label"].iloc[0],
                "anchor": phase,
                "evidence_tier": EVIDENCE_TIER[asset],
                "source_module": SOURCE_MODULE[asset],
                "n_legs": int(g["cycle_id"].nunique()),
                "n_broad_episodes": int(g["broad_episode_id"].nunique()),
                "weighted_median_nominal_ret_12m": weighted_median(g["ret_12m"], w),
                "weighted_median_matched_cash_carry": weighted_median(g["matched_cash_carry"], w),
                "weighted_median_matched_inflation": weighted_median(g["matched_inflation"], w),
                "weighted_median_asset_vs_cash": weighted_median(g["asset_vs_cash"], w),
                "weighted_median_real_asset_return": weighted_median(g["real_asset_return"], w),
                "weighted_median_real_cash_return": weighted_median(g["real_cash_return"], w),
                "weighted_median_mdd_12m": weighted_median(g["mdd_12m"], w),
                "weighted_share_nominal_positive": weighted_share(g["nominal_positive"], w),
                "weighted_share_beats_cash": weighted_share(g["beats_cash"], w),
                "weighted_share_beats_inflation": weighted_share(g["beats_inflation"], w),
                "weighted_share_beats_both": weighted_share(g["beats_both"], w),
                "weighted_share_positive_nominal_but_not_cash": weighted_share(
                    g["positive_nominal_but_not_cash"], w
                ),
                "weighted_share_positive_nominal_but_not_inflation": weighted_share(
                    g["positive_nominal_but_not_inflation"], w
                ),
            })
    out = pd.DataFrame(rows)
    out["asset_order"] = out["asset"].map({a: i for i, a in enumerate(ASSET_ORDER)})
    out["phase_order"] = out["anchor"].map({a: i for i, a in enumerate(PHASES)})
    return out.sort_values(["asset_order", "phase_order"]).drop(columns=["asset_order", "phase_order"])


def make_question_registry(summary: pd.DataFrame, panel: pd.DataFrame, cash_audit: dict):
    def fmt_pct(x):
        return "NA" if pd.isna(x) else f"{100*x:+.1f}%"

    core_supported = summary[summary["evidence_tier"].isin(["CORE_SUPPORTED", "SUPPORTED_PROXY_DESCRIPTIVE"])]
    pos_fail_cash = panel[(panel["nominal_positive"]) & (~panel["beats_cash"])]
    pos_fail_infl = panel[(panel["nominal_positive"]) & (~panel["beats_inflation"])]

    rows = [
        {
            "question_id": "040-Q01",
            "question": "Can a positive nominal endpoint still fail the cash hurdle?",
            "answer": f"Yes. Event-level positive-nominal-but-not-cash rows: {len(pos_fail_cash)}. The module preserves these cases rather than equating positive nominal return with opportunity outperformance.",
            "boundary": "DESCRIPTIVE_NOT_FORECAST",
        },
        {
            "question_id": "040-Q02",
            "question": "Can a positive nominal endpoint still lose purchasing power?",
            "answer": f"Yes. Event-level positive-nominal-but-not-inflation rows: {len(pos_fail_infl)} using matched current-vintage CPI.",
            "boundary": "EXPOST_REAL_RETURN",
        },
        {
            "question_id": "040-Q03",
            "question": "Does the cash hurdle use the same convention as 014?",
            "answer": f"No. 040 uses a same-month-grid 13-month mechanical hurdle; 014 is retained as a post-anchor 12-month cross-check. Median absolute timing gap: {cash_audit['median_abs_gap']*100:.2f}pp; max: {cash_audit['max_abs_gap']*100:.2f}pp.",
            "boundary": "MEASUREMENT_CONVENTION",
        },
        {
            "question_id": "040-Q04",
            "question": "Are limited-history BTC and REIT rows allowed to upgrade themselves in this module?",
            "answer": "No. BTC remains LIMITED_DESCRIPTIVE and VGSIX remains LIMITED_PROXY_DESCRIPTIVE regardless of attractive or unattractive hurdle-adjusted values.",
            "boundary": "EVIDENCE_TIER_LOCK",
        },
        {
            "question_id": "040-Q05",
            "question": "Does a positive real return mean low path risk?",
            "answer": "No. 040 reports real endpoint outcomes and 12M MDD side by side; it does not collapse them into a single risk-adjusted score.",
            "boundary": "ENDPOINT_NOT_PATH",
        },
        {
            "question_id": "040-Q06",
            "question": "Can PandaAI call one phase or asset best?",
            "answer": "No. Fixed display order is used and no performance ranking, optimizer, expected return, allocation weight or trade instruction is generated.",
            "boundary": "NO_RANKING",
        },
    ]

    # Add a compact factual supported-universe readout without selecting a winner.
    for phase in PHASES:
        g = core_supported[core_supported["anchor"] == phase]
        rows.append({
            "question_id": f"040-{phase}-SUPPORTED",
            "question": f"What should be shown for supported evidence in {phase}?",
            "answer": " | ".join(
                f"{r.asset}: nominal {fmt_pct(r.weighted_median_nominal_ret_12m)}, "
                f"vs cash {fmt_pct(r.weighted_median_asset_vs_cash)}, "
                f"real {fmt_pct(r.weighted_median_real_asset_return)}, "
                f"MDD {fmt_pct(r.weighted_median_mdd_12m)}"
                for r in g.itertuples()
            ),
            "boundary": "SUPPORTED_DESCRIPTIVE_FIXED_ORDER",
        })
    return pd.DataFrame(rows)


def write_report(summary: pd.DataFrame, panel: pd.DataFrame, qc: dict):
    def pct(x):
        return f"{100*x:+.1f}%"

    lines = [
        "# FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040 — REPORT",
        "",
        "## Status",
        "",
        "**QC PASS / EVENT-MATCHED CASH-HURDLE + EX-POST REAL-RETURN MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**"
        if qc["qc_gate"] == "PASS"
        else "**QC FAIL**",
        "",
        "## Method boundary",
        "",
        "- Asset nominal endpoints and MDD are inherited from canonical public modules.",
        "- Primary cash hurdle is a same-month-grid mechanical DFF benchmark over anchor month through +12.",
        "- CPI purchasing-power adjustment uses current-vintage CPIAUCSL from baseline month t-1 to endpoint t+12.",
        "- Existing 014 post-anchor 12M cash carry is retained only as a timing-convention cross-check.",
        "- No p-values, ranking, optimizer, expected-return forecast or trade instruction are generated.",
        "",
        "## Fixed-order phase map",
        "",
    ]

    for phase in PHASES:
        lines += [f"### {phase}", ""]
        g = summary[summary["anchor"] == phase]
        for r in g.itertuples():
            lines.append(
                f"- {r.asset} [{r.evidence_tier}] — nominal {pct(r.weighted_median_nominal_ret_12m)}, "
                f"vs matched cash {pct(r.weighted_median_asset_vs_cash)}, "
                f"real {pct(r.weighted_median_real_asset_return)}, "
                f"MDD {pct(r.weighted_median_mdd_12m)}, "
                f"beats-cash share {100*r.weighted_share_beats_cash:.0f}%, "
                f"beats-inflation share {100*r.weighted_share_beats_inflation:.0f}%."
            )
        lines.append("")

    n_pos = int(panel["nominal_positive"].sum())
    n_pos_fail_cash = int(panel["positive_nominal_but_not_cash"].sum())
    n_pos_fail_infl = int(panel["positive_nominal_but_not_inflation"].sum())
    lines += [
        "## Cross-cutting diagnostic",
        "",
        f"- event rows with positive nominal endpoint: {n_pos}",
        f"- positive nominal but failed matched cash hurdle: {n_pos_fail_cash}",
        f"- positive nominal but failed matched inflation hurdle: {n_pos_fail_infl}",
        "",
        "These are row counts, not independent statistical observations; broad-episode weighting remains the summary convention.",
        "",
        "## Boundary",
        "",
        "A positive nominal endpoint is not automatically an opportunity-cost win, a purchasing-power win, or a low-risk path.",
        "Historical medians are not expected returns and are not allocation instructions.",
    ]
    (OUT / "FED_CYCLE_CASH_HURDLE_REAL_RETURN_MAP_040_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main():
    upstream = assert_upstream_qc()
    events = load_asset_events()

    dff_raw, dff_meta = fetch_fred("DFF")
    cpi_raw, cpi_meta = fetch_fred("CPIAUCSL")
    dff_m = monthly_average(dff_raw)
    cpi_m = monthly_average(cpi_raw)

    source_registry = pd.DataFrame([dff_meta, cpi_meta])
    source_registry.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)

    panel = attach_hurdles(events, dff_m, cpi_m)
    panel.to_csv(OUT / "EVENT_HURDLE_REAL_RETURN_PANEL.csv", index=False)

    summary = summarize(panel)
    summary.to_csv(OUT / "ASSET_PHASE_HURDLE_REAL_RETURN_SUMMARY.csv", index=False)

    misleading = panel[
        panel["positive_nominal_but_not_cash"] | panel["positive_nominal_but_not_inflation"]
    ].copy()
    misleading.to_csv(OUT / "POSITIVE_NOMINAL_COUNTEREXAMPLES.csv", index=False)

    # QC: preserve upstream broad-episode weights exactly.
    weight_violations = 0
    for (asset, anchor, bid), g in panel.groupby(["asset", "anchor", "broad_episode_id"]):
        if abs(float(g["episode_weight"].sum()) - 1.0) > 1e-10:
            weight_violations += 1

    identity_violations = int((~panel["asset"].isin(ASSET_ORDER)).sum())
    missing_metric_rows = int(
        panel[
            [
                "ret_12m", "mdd_12m", "matched_cash_carry", "matched_inflation",
                "asset_vs_cash", "real_asset_return", "real_cash_return",
            ]
        ].isna().any(axis=1).sum()
    )
    rejected_proxy_rows = int(panel["asset"].str.contains("FRESX", case=False, na=False).sum())
    target_etf_dup_rows = int(panel["asset"].isin(["TLT", "VNQ"]).sum())
    housing_rows = int(panel["asset"].str.contains("HOUS", case=False, na=False).sum())

    # Tier locks.
    tier_bad = 0
    for asset, expected in EVIDENCE_TIER.items():
        vals = set(panel.loc[panel["asset"] == asset, "evidence_tier"])
        if vals != {expected}:
            tier_bad += 1

    # Supported core/proxy minimum-support audit. This is a consistency check, not promotion logic.
    support_count_bad = 0
    for r in summary.itertuples():
        if r.evidence_tier in ["CORE_SUPPORTED", "SUPPORTED_PROXY_DESCRIPTIVE"]:
            if r.n_legs < 5 or r.n_broad_episodes < 4:
                support_count_bad += 1

    # Cash timing audit uses unique event keys so repeated asset rows do not multiply the diagnostic.
    c = panel[
        ["anchor", "cycle_id", "matched_cash_carry", "canonical_cash_014_post12", "cash_timing_gap"]
    ].drop_duplicates(["anchor", "cycle_id"])
    cash_audit = {
        "unique_event_keys": int(len(c)),
        "median_abs_gap": float(c["cash_timing_gap"].abs().median()),
        "max_abs_gap": float(c["cash_timing_gap"].abs().max()),
        "mean_abs_gap": float(c["cash_timing_gap"].abs().mean()),
    }
    pd.DataFrame([cash_audit]).to_csv(OUT / "CASH_TIMING_CONVENTION_AUDIT.csv", index=False)

    hard_fail = any([
        weight_violations != 0,
        identity_violations != 0,
        missing_metric_rows != 0,
        rejected_proxy_rows != 0,
        target_etf_dup_rows != 0,
        housing_rows != 0,
        tier_bad != 0,
        support_count_bad != 0,
        len(summary) != len(ASSET_ORDER) * len(PHASES),
        len(source_registry) != 2,
        source_registry["sha256"].str.len().ne(64).any(),
    ])

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040",
        "upstream_qc": upstream,
        "event_rows": int(len(panel)),
        "summary_rows": int(len(summary)),
        "expected_summary_rows": len(ASSET_ORDER) * len(PHASES),
        "assets": ASSET_ORDER,
        "phases": PHASES,
        "source_hashes_complete": bool(source_registry["sha256"].str.len().eq(64).all()),
        "dff_first_date": dff_meta["first_date"],
        "dff_last_date": dff_meta["last_date"],
        "cpi_first_date": cpi_meta["first_date"],
        "cpi_last_date": cpi_meta["last_date"],
        "current_vintage_cpi_not_pit": True,
        "matched_cash_months": 13,
        "canonical_cash_014_is_crosscheck_only": True,
        "cash_timing_unique_events": cash_audit["unique_event_keys"],
        "cash_timing_median_abs_gap": cash_audit["median_abs_gap"],
        "cash_timing_max_abs_gap": cash_audit["max_abs_gap"],
        "broad_episode_weight_violations": weight_violations,
        "asset_identity_violations": identity_violations,
        "missing_metric_rows": missing_metric_rows,
        "rejected_fresx_rows": rejected_proxy_rows,
        "duplicate_target_etf_rows": target_etf_dup_rows,
        "housing_rows_in_12m_panel": housing_rows,
        "evidence_tier_lock_violations": tier_bad,
        "supported_minimum_count_violations": support_count_bad,
        "positive_nominal_event_rows": int(panel["nominal_positive"].sum()),
        "positive_nominal_but_not_cash_rows": int(panel["positive_nominal_but_not_cash"].sum()),
        "positive_nominal_but_not_inflation_rows": int(panel["positive_nominal_but_not_inflation"].sum()),
        "new_pvalues_generated": False,
        "optimized_thresholds_or_horizons": False,
        "asset_rankings_generated": False,
        "best_phase_outputs": 0,
        "expected_return_forecasts": 0,
        "trade_recommendations": 0,
        "private_paper_inputs_used": False,
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    questions = make_question_registry(summary, panel, cash_audit)
    questions.to_csv(OUT / "INVESTOR_QUESTION_REGISTRY.csv", index=False)

    schema = {
        "module": "FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040",
        "fixed_asset_order": ASSET_ORDER,
        "fixed_phase_order": PHASES,
        "allowed_outputs": [
            "nominal_return_distribution",
            "matched_cash_hurdle",
            "matched_expost_inflation",
            "real_return_distribution",
            "mdd_path_risk",
            "support_tier",
            "counterexample_cases",
            "measurement_convention_audit",
        ],
        "prohibited_outputs": [
            "best_asset",
            "best_phase",
            "asset_rank",
            "allocation_weight",
            "expected_return",
            "current_analog",
            "buy_sell_instruction",
            "causal_fed_claim",
        ],
        "cpi_status": "CURRENT_VINTAGE_EXPOST_NOT_PIT",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }
    (OUT / "PANDAAI_CASH_HURDLE_REAL_RETURN_SCHEMA.json").write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    write_report(summary, panel, qc)

    if hard_fail:
        raise SystemExit("040 QC failed")

    print(json.dumps(qc, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
