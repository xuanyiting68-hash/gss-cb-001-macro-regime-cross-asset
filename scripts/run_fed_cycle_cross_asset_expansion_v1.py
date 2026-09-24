#!/usr/bin/env python3
"""
FED-CYCLE-CROSS-ASSET-EXPANSION-014
Frozen descriptive extension into duration, listed REITs, Bitcoin, DXY,
direct housing, Treasury yields and a mechanical cash-carry benchmark.

Reference:
research/FED_CYCLE_CROSS_ASSET_EXPANSION_014_LOCK.md
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1"
OUT.mkdir(parents=True, exist_ok=True)

ANCHORS = {
    "FIRST_HIKE": "first_hike",
    "LAST_HIKE": "last_hike",
    "PAUSE_START": "pause_start",
    "FIRST_CUT": "first_cut",
}

MARKET_ASSETS = {
    "TLT": {"symbol": "TLT", "adjusted": True, "required": True,
            "label": "iShares 20+ Year Treasury Bond ETF adjusted-close proxy"},
    "VNQ": {"symbol": "VNQ", "adjusted": True, "required": True,
            "label": "Vanguard Real Estate ETF adjusted-close proxy"},
    "BTC_USD": {"symbol": "BTC-USD", "adjusted": False, "required": True,
                "label": "Bitcoin USD"},
    "DXY": {"symbol": "DX-Y.NYB", "adjusted": False, "required": False,
            "label": "U.S. Dollar Index market proxy"},
}

FRED_REQUIRED = {
    "CSUSHPINSA": "S&P Cotality Case-Shiller U.S. National Home Price Index",
    "DGS2": "2-Year Treasury yield",
    "DGS10": "10-Year Treasury yield",
    "DFF": "Effective Federal Funds Rate",
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


STATE = load_module(ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py", "state_v2_exp014")


def fetch_bytes(url: str, timeout: int = 60) -> bytes:
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 gss-cb-001-public-research/1.0",
            "Accept": "*/*",
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_yahoo(symbol: str, adjusted: bool):
    enc = quote(symbol, safe="")
    urls = [
        f"https://query1.finance.yahoo.com/v8/finance/chart/{enc}?period1=0&period2=1893456000&interval=1d&events=history&includeAdjustedClose=true",
        f"https://query2.finance.yahoo.com/v8/finance/chart/{enc}?period1=0&period2=1893456000&interval=1d&events=history&includeAdjustedClose=true",
    ]
    errs = []
    for url in urls:
        try:
            raw = fetch_bytes(url, timeout=60)
            obj = json.loads(raw.decode("utf-8"))
            result = obj.get("chart", {}).get("result")
            if not result:
                raise RuntimeError(str(obj.get("chart", {}).get("error")))
            block = result[0]
            ts = block.get("timestamp") or []
            quote_block = (block.get("indicators", {}).get("quote") or [{}])[0]
            close = quote_block.get("close") or []
            if len(ts) != len(close) or not ts:
                raise RuntimeError("timestamp/close length mismatch")
            if adjusted:
                adj_block = (block.get("indicators", {}).get("adjclose") or [{}])[0]
                vals = adj_block.get("adjclose") or []
                if len(vals) != len(ts):
                    raise RuntimeError("adjusted close required but unavailable")
                field = "adjusted_close"
            else:
                vals = close
                field = "close"
            df = pd.DataFrame({
                "date": pd.to_datetime(ts, unit="s", utc=True).tz_convert(None).normalize(),
                "value": pd.to_numeric(vals, errors="coerce"),
            })
            df = df.dropna(subset=["date", "value"]).sort_values("date")
            df = df.drop_duplicates("date", keep="last").reset_index(drop=True)
            if len(df) < 100:
                raise RuntimeError(f"history too short: {len(df)}")
            return df, {
                "url": url,
                "method": "YAHOO_FINANCE_CHART_JSON",
                "sha256": hashlib.sha256(raw).hexdigest(),
                "raw_bytes": len(raw),
                "price_field": field,
            }
        except Exception as exc:
            errs.append(f"{url}: {exc!r}")
    raise RuntimeError(" | ".join(errs))


def monthly_average(df: pd.DataFrame) -> pd.DataFrame:
    x = df.dropna(subset=["date", "value"]).copy()
    x["period"] = x["date"].dt.to_period("M")
    return x.groupby("period", as_index=False)["value"].mean().sort_values("period")


def weighted_quantile(values, weights, q=0.5):
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


def support_label(nlegs: int, nbroad: int) -> str:
    if nlegs >= 5 and nbroad >= 4:
        return "SUPPORTED_DESCRIPTIVE"
    if nbroad >= 2:
        return "LIMITED_DESCRIPTIVE"
    return "INSUFFICIENT_SUPPORT"


def load_cycles():
    c = STATE.assign_broad_clusters(STATE.load_cycles())
    if len(c) != 10 or c["broad_episode_id"].nunique() != 7:
        raise RuntimeError("Frozen cycle registry shape changed")
    return c


def make_prov(name, source, meta, df, note=""):
    return {
        "series": name,
        "source": source,
        "url": meta.get("url", ""),
        "acquisition_method": meta.get("method", meta.get("acquisition_method", "")),
        "price_field": meta.get("price_field", ""),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": meta.get("sha256", ""),
        "raw_bytes": meta.get("raw_bytes", ""),
        "rows_total": int(len(df)),
        "rows_nonmissing": int(df["value"].notna().sum()),
        "first_date": str(df["date"].min().date()) if len(df) else "",
        "last_date": str(df["date"].max().date()) if len(df) else "",
        "raw_committed": False,
        "note": note,
    }


def liquid_metrics(price_map, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    basep = ep - 1
    postp = [ep + k for k in range(1, 13)]
    if basep not in price_map or any(p not in price_map for p in postp):
        return None
    base = float(price_map[basep])
    post = np.array([float(price_map[p]) for p in postp])
    vals = np.concatenate([[base], post])
    peaks = np.maximum.accumulate(vals)
    dd = 1.0 - vals / peaks
    return {
        "ret_3m": float(post[2] / base - 1.0),
        "ret_6m": float(post[5] / base - 1.0),
        "ret_12m": float(post[11] / base - 1.0),
        "mdd_12m": float(dd.max()),
        "mdd_trough_month": int(np.argmax(dd)) if float(dd.max()) > 1e-15 else np.nan,
    }


def build_market(cycles, monthly_assets):
    rows = []
    for asset, obj in monthly_assets.items():
        pmap = dict(zip(obj["df"]["period"], obj["df"]["value"].astype(float)))
        for anchor, col in ANCHORS.items():
            tmp = []
            for _, cyc in cycles.iterrows():
                dt = cyc[col]
                if pd.isna(dt):
                    continue
                m = liquid_metrics(pmap, dt)
                if m is not None:
                    tmp.append((cyc, pd.Timestamp(dt), m))
            counts = {}
            for cyc, _, _ in tmp:
                bid = cyc["broad_episode_id"]
                counts[bid] = counts.get(bid, 0) + 1
            for cyc, dt, m in tmp:
                bid = cyc["broad_episode_id"]
                rows.append({
                    "asset": asset,
                    "asset_label": obj["label"],
                    "anchor": anchor,
                    "cycle_id": cyc["cycle_id"],
                    "broad_episode_id": bid,
                    "anchor_date": dt,
                    "episode_weight": 1.0 / counts[bid],
                    **m,
                })
    metrics = pd.DataFrame(rows)
    sums = []
    for (asset, anchor), g in metrics.groupby(["asset", "anchor"]):
        w = g["episode_weight"].to_numpy(float)
        nlegs = int(g["cycle_id"].nunique())
        nbroad = int(g["broad_episode_id"].nunique())
        valid = g.dropna(subset=["mdd_trough_month"])
        if len(valid):
            late = float(
                valid.loc[valid["mdd_trough_month"].between(7, 12), "episode_weight"].sum()
                / valid["episode_weight"].sum()
            )
            trough = weighted_quantile(valid["mdd_trough_month"], valid["episode_weight"], 0.5)
        else:
            late, trough = np.nan, np.nan
        sums.append({
            "asset": asset,
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "support_status": support_label(nlegs, nbroad),
            "weighted_median_ret_3m": weighted_quantile(g["ret_3m"], w),
            "weighted_median_ret_6m": weighted_quantile(g["ret_6m"], w),
            "weighted_median_ret_12m": weighted_quantile(g["ret_12m"], w),
            "weighted_median_mdd_12m": weighted_quantile(g["mdd_12m"], w),
            "weighted_median_mdd_trough_month": trough,
            "weighted_late_trough_share_7_12": late,
        })
    return metrics, pd.DataFrame(sums)


def housing_metrics(price_map, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    basep = ep - 1
    postp = [ep + k for k in range(1, 25)]
    if basep not in price_map or any(p not in price_map for p in postp):
        return None
    base = float(price_map[basep])
    post = np.array([float(price_map[p]) for p in postp])
    vals = np.concatenate([[base], post])
    peaks = np.maximum.accumulate(vals)
    dd = 1.0 - vals / peaks
    return {
        "ret_6m": float(post[5] / base - 1.0),
        "ret_12m": float(post[11] / base - 1.0),
        "ret_24m": float(post[23] / base - 1.0),
        "decline_24m": float(dd.max()),
        "trough_month_24m": int(np.argmax(dd)) if float(dd.max()) > 1e-15 else np.nan,
    }


def build_housing(cycles, housing_monthly):
    pmap = dict(zip(housing_monthly["period"], housing_monthly["value"].astype(float)))
    rows = []
    for anchor, col in ANCHORS.items():
        tmp = []
        for _, cyc in cycles.iterrows():
            dt = cyc[col]
            if pd.isna(dt):
                continue
            m = housing_metrics(pmap, dt)
            if m is not None:
                tmp.append((cyc, pd.Timestamp(dt), m))
        counts = {}
        for cyc, _, _ in tmp:
            bid = cyc["broad_episode_id"]
            counts[bid] = counts.get(bid, 0) + 1
        for cyc, dt, m in tmp:
            bid = cyc["broad_episode_id"]
            rows.append({
                "anchor": anchor,
                "cycle_id": cyc["cycle_id"],
                "broad_episode_id": bid,
                "anchor_date": dt,
                "episode_weight": 1.0 / counts[bid],
                **m,
            })
    metrics = pd.DataFrame(rows)
    sums = []
    for anchor, g in metrics.groupby("anchor"):
        w = g["episode_weight"].to_numpy(float)
        nlegs, nbroad = int(g["cycle_id"].nunique()), int(g["broad_episode_id"].nunique())
        valid = g.dropna(subset=["trough_month_24m"])
        sums.append({
            "asset": "US_HOUSE_PRICE",
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "support_status": support_label(nlegs, nbroad),
            "weighted_median_ret_6m": weighted_quantile(g["ret_6m"], w),
            "weighted_median_ret_12m": weighted_quantile(g["ret_12m"], w),
            "weighted_median_ret_24m": weighted_quantile(g["ret_24m"], w),
            "weighted_median_decline_24m": weighted_quantile(g["decline_24m"], w),
            "weighted_median_trough_month_24m": (
                weighted_quantile(valid["trough_month_24m"], valid["episode_weight"]) if len(valid) else np.nan
            ),
        })
    return metrics, pd.DataFrame(sums)


def rate_metrics(rate_map, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    basep = ep - 1
    postp = [ep + k for k in range(1, 13)]
    if basep not in rate_map or any(p not in rate_map for p in postp):
        return None
    base = float(rate_map[basep])
    post = np.array([float(rate_map[p]) for p in postp])
    diffs = (post - base) * 100.0
    return {
        "chg_3m_bp": float(diffs[2]),
        "chg_6m_bp": float(diffs[5]),
        "chg_12m_bp": float(diffs[11]),
        "max_increase_12m_bp": float(diffs.max()),
        "max_decrease_12m_bp": float(diffs.min()),
    }


def build_rates(cycles, rate_monthlies):
    rows = []
    for series, df in rate_monthlies.items():
        rmap = dict(zip(df["period"], df["value"].astype(float)))
        for anchor, col in ANCHORS.items():
            tmp = []
            for _, cyc in cycles.iterrows():
                dt = cyc[col]
                if pd.isna(dt):
                    continue
                m = rate_metrics(rmap, dt)
                if m is not None:
                    tmp.append((cyc, pd.Timestamp(dt), m))
            counts = {}
            for cyc, _, _ in tmp:
                bid = cyc["broad_episode_id"]
                counts[bid] = counts.get(bid, 0) + 1
            for cyc, dt, m in tmp:
                bid = cyc["broad_episode_id"]
                rows.append({
                    "series": series,
                    "anchor": anchor,
                    "cycle_id": cyc["cycle_id"],
                    "broad_episode_id": bid,
                    "anchor_date": dt,
                    "episode_weight": 1.0 / counts[bid],
                    **m,
                })
    metrics = pd.DataFrame(rows)
    sums = []
    for (series, anchor), g in metrics.groupby(["series", "anchor"]):
        w = g["episode_weight"].to_numpy(float)
        nlegs, nbroad = int(g["cycle_id"].nunique()), int(g["broad_episode_id"].nunique())
        sums.append({
            "series": series,
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "support_status": support_label(nlegs, nbroad),
            "weighted_median_chg_3m_bp": weighted_quantile(g["chg_3m_bp"], w),
            "weighted_median_chg_6m_bp": weighted_quantile(g["chg_6m_bp"], w),
            "weighted_median_chg_12m_bp": weighted_quantile(g["chg_12m_bp"], w),
            "weighted_median_max_increase_12m_bp": weighted_quantile(g["max_increase_12m_bp"], w),
            "weighted_median_max_decrease_12m_bp": weighted_quantile(g["max_decrease_12m_bp"], w),
        })
    return metrics, pd.DataFrame(sums)


def cash_metrics(dff_map, anchor_date):
    ep = pd.Timestamp(anchor_date).to_period("M")
    postp = [ep + k for k in range(1, 13)]
    if any(p not in dff_map for p in postp):
        return None
    rates = np.array([float(dff_map[p]) for p in postp])
    monthly = rates / 100.0 / 12.0
    wealth = np.cumprod(1.0 + monthly) - 1.0
    return {
        "cash_carry_3m": float(wealth[2]),
        "cash_carry_6m": float(wealth[5]),
        "cash_carry_12m": float(wealth[11]),
        "avg_dff_12m": float(rates.mean()),
    }


def build_cash(cycles, dff_monthly):
    dmap = dict(zip(dff_monthly["period"], dff_monthly["value"].astype(float)))
    rows = []
    for anchor, col in ANCHORS.items():
        tmp = []
        for _, cyc in cycles.iterrows():
            dt = cyc[col]
            if pd.isna(dt):
                continue
            m = cash_metrics(dmap, dt)
            if m is not None:
                tmp.append((cyc, pd.Timestamp(dt), m))
        counts = {}
        for cyc, _, _ in tmp:
            bid = cyc["broad_episode_id"]
            counts[bid] = counts.get(bid, 0) + 1
        for cyc, dt, m in tmp:
            bid = cyc["broad_episode_id"]
            rows.append({
                "anchor": anchor,
                "cycle_id": cyc["cycle_id"],
                "broad_episode_id": bid,
                "anchor_date": dt,
                "episode_weight": 1.0 / counts[bid],
                **m,
            })
    metrics = pd.DataFrame(rows)
    sums = []
    for anchor, g in metrics.groupby("anchor"):
        w = g["episode_weight"].to_numpy(float)
        nlegs, nbroad = int(g["cycle_id"].nunique()), int(g["broad_episode_id"].nunique())
        sums.append({
            "asset": "MECHANICAL_CASH_DFF",
            "anchor": anchor,
            "n_legs": nlegs,
            "n_broad_episodes": nbroad,
            "support_status": support_label(nlegs, nbroad),
            "weighted_median_cash_carry_3m": weighted_quantile(g["cash_carry_3m"], w),
            "weighted_median_cash_carry_6m": weighted_quantile(g["cash_carry_6m"], w),
            "weighted_median_cash_carry_12m": weighted_quantile(g["cash_carry_12m"], w),
            "weighted_median_avg_dff_12m": weighted_quantile(g["avg_dff_12m"], w),
        })
    return metrics, pd.DataFrame(sums)


def weight_errors(df, keys):
    bad = 0
    for _, g in df.groupby(keys):
        if abs(float(g["episode_weight"].sum()) - 1.0) > 1e-10:
            bad += 1
    return bad


def write_report(market_sum, housing_sum, rate_sum, cash_sum, qc):
    def md(df):
        return df.to_markdown(index=False) if len(df) else "_No rows_"
    lines = [
        "# FED-CYCLE-CROSS-ASSET-EXPANSION-014 — Report",
        "",
        "**DESCRIPTIVE / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "## QC",
        "",
        f"- QC gate: **{qc['qc_gate']}**",
        f"- Frozen historical cycles: {qc['mechanical_cycles']} mechanical / {qc['broad_episodes']} broad episodes",
        f"- Market acquisition failures: {qc['market_acquisition_failures']}",
        "- Current live 2026 cycle is excluded from historical outcome summaries.",
        "- Raw Yahoo / Case-Shiller source histories are not committed.",
        "",
        "## Liquid market phase summary",
        "",
        md(market_sum),
        "",
        "## Direct housing phase summary",
        "",
        md(housing_sum),
        "",
        "## Treasury-yield phase summary",
        "",
        md(rate_sum),
        "",
        "## Mechanical cash-carry benchmark",
        "",
        md(cash_sum),
        "",
        "## Evidence boundary",
        "",
        "- TLT/VNQ/BTC/DXY have shorter histories than the long-history Gold/equity/WTI layer; support labels must remain visible.",
        "- TLT/VNQ adjusted-close histories are ETF proxies and do not replace security-level bond/real-estate decomposition.",
        "- Case-Shiller is a slow national house-price index, not an investable total-return series.",
        "- DGS2/DGS10 changes are yield changes, not bond returns.",
        "- DFF cash carry is a mechanical benchmark that ignores fees, tax and intra-month compounding.",
        "- No p-value/FDR family is run; no causal or trading claim is authorized.",
    ]
    (OUT / "FED_CYCLE_CROSS_ASSET_EXPANSION_014_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main():
    cycles = load_cycles()
    prov = []
    failures = []

    monthly_assets = {}
    for name, cfg in MARKET_ASSETS.items():
        try:
            df, meta = fetch_yahoo(cfg["symbol"], cfg["adjusted"])
            monthly_assets[name] = {"df": monthly_average(df), "label": cfg["label"]}
            prov.append(make_prov(
                name, "Yahoo Finance public chart history", meta, df,
                "Adjusted close requested" if cfg["adjusted"] else "Close"
            ))
        except Exception as exc:
            failures.append({"asset": name, "required": cfg["required"], "error": repr(exc)})
            prov.append({
                "series": name, "source": "Yahoo Finance public chart history",
                "url": "", "acquisition_method": "FAILED", "price_field": "",
                "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                "sha256": "", "raw_bytes": "", "rows_total": 0, "rows_nonmissing": 0,
                "first_date": "", "last_date": "", "raw_committed": False,
                "note": repr(exc),
            })

    fred = {}
    for sid, label in FRED_REQUIRED.items():
        df, meta = STATE.fetch_fred(sid)
        fred[sid] = monthly_average(df)
        prov.append(make_prov(
            sid, f"{label} via FRED distribution", meta, df,
            "Copyrighted raw source history not committed" if sid == "CSUSHPINSA" else ""
        ))

    market_metrics, market_sum = build_market(cycles, monthly_assets)
    housing_metrics_df, housing_sum = build_housing(cycles, fred["CSUSHPINSA"])
    rate_metrics_df, rate_sum = build_rates(cycles, {"DGS2": fred["DGS2"], "DGS10": fred["DGS10"]})
    cash_metrics_df, cash_sum = build_cash(cycles, fred["DFF"])

    required_failures = [x for x in failures if x["required"]]
    market_negative_mdd = int((pd.to_numeric(market_metrics["mdd_12m"], errors="coerce") < -1e-12).sum())
    housing_negative_decline = int((pd.to_numeric(housing_metrics_df["decline_24m"], errors="coerce") < -1e-12).sum())
    current_cycle_leak = int((pd.to_datetime(cycles["first_hike"]).dt.year >= 2026).sum())

    bad_weights = (
        weight_errors(market_metrics, ["asset", "anchor", "broad_episode_id"])
        + weight_errors(housing_metrics_df, ["anchor", "broad_episode_id"])
        + weight_errors(rate_metrics_df, ["series", "anchor", "broad_episode_id"])
        + weight_errors(cash_metrics_df, ["anchor", "broad_episode_id"])
    )

    # Support-label consistency audit.
    support_bad = 0
    for df, key in [
        (market_sum, None), (housing_sum, None), (rate_sum, None), (cash_sum, None)
    ]:
        for _, r in df.iterrows():
            if r["support_status"] != support_label(int(r["n_legs"]), int(r["n_broad_episodes"])):
                support_bad += 1

    hard_fail = (
        len(required_failures) > 0
        or len(market_metrics) == 0
        or len(housing_metrics_df) == 0
        or len(rate_metrics_df) == 0
        or len(cash_metrics_df) == 0
        or market_negative_mdd != 0
        or housing_negative_decline != 0
        or current_cycle_leak != 0
        or bad_weights != 0
        or support_bad != 0
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-CROSS-ASSET-EXPANSION-014",
        "mechanical_cycles": int(cycles["cycle_id"].nunique()),
        "broad_episodes": int(cycles["broad_episode_id"].nunique()),
        "latest_historical_first_hike_year": int(pd.to_datetime(cycles["first_hike"]).dt.year.max()),
        "market_assets_loaded": sorted(monthly_assets.keys()),
        "market_acquisition_failures": failures,
        "required_market_acquisition_failures": required_failures,
        "market_metric_rows": int(len(market_metrics)),
        "housing_metric_rows": int(len(housing_metrics_df)),
        "rate_metric_rows": int(len(rate_metrics_df)),
        "cash_metric_rows": int(len(cash_metrics_df)),
        "negative_market_mdd_violations": market_negative_mdd,
        "negative_housing_decline_violations": housing_negative_decline,
        "current_2026_cycle_leak_violations": current_cycle_leak,
        "broad_episode_weight_violations": bad_weights,
        "support_label_violations": support_bad,
        "raw_source_histories_committed": False,
        "evidence_class": "DESCRIPTIVE",
        "causal_status": "NONE",
        "fdr_status": "NOT_APPLICABLE_NO_PVALUE_FAMILY",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    pd.DataFrame(prov).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    pd.DataFrame(failures).to_csv(OUT / "ACQUISITION_FAILURES.csv", index=False)
    market_metrics.to_csv(OUT / "MARKET_PHASE_METRICS.csv", index=False)
    market_sum.to_csv(OUT / "MARKET_PHASE_SUMMARY.csv", index=False)
    housing_metrics_df.to_csv(OUT / "HOUSING_PHASE_METRICS.csv", index=False)
    housing_sum.to_csv(OUT / "HOUSING_PHASE_SUMMARY.csv", index=False)
    rate_metrics_df.to_csv(OUT / "RATE_PHASE_METRICS.csv", index=False)
    rate_sum.to_csv(OUT / "RATE_PHASE_SUMMARY.csv", index=False)
    cash_metrics_df.to_csv(OUT / "CASH_PHASE_METRICS.csv", index=False)
    cash_sum.to_csv(OUT / "CASH_PHASE_SUMMARY.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")
    write_report(market_sum, housing_sum, rate_sum, cash_sum, qc)

    if hard_fail:
        raise SystemExit("FED-CYCLE-CROSS-ASSET-EXPANSION-014 QC failed")
    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
