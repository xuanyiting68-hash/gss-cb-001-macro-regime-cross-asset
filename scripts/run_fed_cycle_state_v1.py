#!/usr/bin/env python3
"""
FED-CYCLE-STATE-001
Predetermined-state descriptive/associational map for Gold FIRST_HIKE paths.

Reference:
research/FED_CYCLE_STATE_001_LOCK.md
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
OUT = ROOT / "results" / "fed_cycle_state_v1"
OUT.mkdir(parents=True, exist_ok=True)

OUTCOMES_FILE = ROOT / "results" / "gold_long_history_monthly_v1" / "GOLD_MONTHLY_EVENT_METRICS.csv"
CYCLES_FILE = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_TIGHTENING_CYCLES.csv"

SERIES = {
    "DGS10": ("Board of Governors via FRED", "yield"),
    "DGS2": ("Board of Governors via FRED", "yield"),
    "DCOILWTICO": ("U.S. EIA via FRED", "market"),
    "CPIAUCNS": ("U.S. BLS via FRED", "macro_current_vintage"),
    "INDPRO": ("Board of Governors via FRED", "macro_current_vintage"),
    "NFCI": ("Federal Reserve Bank of Chicago via FRED", "macro_current_vintage"),
    "DFII10": ("Board of Governors via FRED", "yield"),
    "TWEXM": ("Board of Governors via FRED", "usd_legacy"),
    "DTWEXAFEGS": ("Board of Governors via FRED", "usd_modern"),
}

PRIMARY_STATES = {
    "INFLATION_LEVEL": ("HIGH", "LOW_OR_MODERATE"),
    "INFLATION_DIRECTION": ("RISING", "FALLING_OR_FLAT"),
    "GROWTH_STATE": ("STRONG", "WEAK"),
    "YIELD_CURVE_STATE": ("INVERTED", "POSITIVE"),
    "REAL_RATE_PROXY_STATE": ("POSITIVE", "NONPOSITIVE"),
    "ENERGY_DIRECTION_STATE": ("RISING", "FALLING_OR_FLAT"),
    "NFCI_STATE": ("TIGHT", "LOOSE_OR_AVERAGE"),
}

OUTCOME_FIELDS = {
    "ret_12m": "PRIMARY",
    "mdd_24m": "PRIMARY",
    "ret_6m": "SECONDARY",
    "ret_24m": "SECONDARY",
    "mae": "SECONDARY",
    "mfe": "SECONDARY",
}


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


def fetch_fred(series_id: str):
    fred_url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    errors = []
    for _ in range(2):
        try:
            raw = fetch_bytes(fred_url, timeout=30)
            df = pd.read_csv(io.BytesIO(raw))
            date_col = df.columns[0]
            value_col = series_id if series_id in df.columns else df.columns[1]
            df = df.rename(columns={date_col: "date", value_col: "value"})
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
            return df, {
                "url": fred_url,
                "acquisition_method": "FRED_DIRECT_CSV",
                "sha256": hashlib.sha256(raw).hexdigest(),
                "raw_bytes": len(raw),
            }
        except Exception as exc:
            errors.append(repr(exc))

    mirror_url = f"https://api.db.nomics.world/v22/series/FRED/{series_id}?observations=1"
    raw = fetch_bytes(mirror_url, timeout=60)
    obj = json.loads(raw.decode("utf-8"))
    docs = obj["series"]["docs"]
    if not docs:
        raise RuntimeError(f"No DBnomics/FRED data for {series_id}; errors={errors}")
    doc = docs[0]
    periods = doc.get("period") or doc.get("period_start_day")
    values = doc.get("value")
    if periods is None or values is None or len(periods) != len(values):
        raise RuntimeError(f"Unexpected DBnomics payload for {series_id}")
    df = pd.DataFrame({"date": periods, "value": values})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return df, {
        "url": mirror_url,
        "acquisition_method": "DBNOMICS_FRED_MIRROR",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "raw_bytes": len(raw),
    }


def source_row(series_id, df, meta):
    source, info_class = SERIES[series_id]
    return {
        "series_id": series_id,
        "source": source,
        "information_source_class": info_class,
        "url": meta["url"],
        "acquisition_method": meta["acquisition_method"],
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": meta["sha256"],
        "raw_bytes": meta["raw_bytes"],
        "rows_total": int(len(df)),
        "rows_nonmissing": int(df["value"].notna().sum()),
        "first_date": str(df["date"].min().date()) if len(df) else "",
        "last_date": str(df["date"].max().date()) if len(df) else "",
        "raw_committed": False,
    }


def last_strictly_before(df: pd.DataFrame, event_date: pd.Timestamp):
    x = df[(df["date"] < event_date) & df["value"].notna()]
    if x.empty:
        return None
    return x.iloc[-1]


def exact_month_value(df: pd.DataFrame, period: pd.Period):
    x = df.copy()
    x["period"] = x["date"].dt.to_period("M")
    y = x[(x["period"] == period) & x["value"].notna()]
    if y.empty:
        return np.nan
    return float(y.iloc[-1]["value"])


def yoy_at(df: pd.DataFrame, period: pd.Period):
    now = exact_month_value(df, period)
    prev = exact_month_value(df, period - 12)
    if not (np.isfinite(now) and np.isfinite(prev) and prev != 0):
        return np.nan
    return now / prev - 1.0


def common_yield_point(dgs10, dgs2, event_date):
    a = dgs10[["date","value"]].rename(columns={"value":"dgs10"})
    b = dgs2[["date","value"]].rename(columns={"value":"dgs2"})
    m = a.merge(b, on="date", how="inner").dropna()
    m = m[m["date"] < event_date]
    if m.empty:
        return None
    return m.iloc[-1]


def trailing_return_by_obs(df: pd.DataFrame, event_date, lag_obs: int):
    x = df[(df["date"] < event_date) & df["value"].notna()].copy().reset_index(drop=True)
    if len(x) <= lag_obs:
        return None
    last = x.iloc[-1]
    prev = x.iloc[-1 - lag_obs]
    if prev["value"] == 0:
        return None
    return {
        "date": pd.Timestamp(last["date"]),
        "value": float(last["value"]),
        "lag_date": pd.Timestamp(prev["date"]),
        "lag_value": float(prev["value"]),
        "return": float(last["value"] / prev["value"] - 1.0),
    }


def usd_bridge_audit(twexm, dtwex):
    legacy = twexm[twexm["value"].notna() & (twexm["date"] >= pd.Timestamp("2006-01-01"))].copy()
    modern = dtwex[dtwex["value"].notna()].copy().reset_index(drop=True)

    rows = []
    for i in range(26, len(legacy)):
        r = legacy.iloc[i]
        dt = pd.Timestamp(r["date"])
        if dt > pd.Timestamp("2019-12-31"):
            break
        legacy_ret = float(r["value"] / legacy.iloc[i-26]["value"] - 1.0)
        mod = modern[modern["date"] <= dt].reset_index(drop=True)
        if len(mod) <= 126:
            continue
        modern_ret = float(mod.iloc[-1]["value"] / mod.iloc[-127]["value"] - 1.0)
        rows.append({
            "date": dt,
            "legacy_26w_return": legacy_ret,
            "modern_126obs_return": modern_ret,
            "legacy_sign": int(np.sign(legacy_ret)),
            "modern_sign": int(np.sign(modern_ret)),
            "sign_agrees": bool(np.sign(legacy_ret) == np.sign(modern_ret)),
        })
    audit = pd.DataFrame(rows)
    agreement = float(audit["sign_agrees"].mean()) if len(audit) else np.nan
    return audit, agreement


def build_state_panel(first_hike, series):
    rows = []
    for _, ev in first_hike.iterrows():
        event_date = pd.Timestamp(ev["event_date"])
        event_period = event_date.to_period("M")
        state_period = event_period - 2

        # Yield curve on a common strictly pre-event date.
        yp = common_yield_point(series["DGS10"], series["DGS2"], event_date)
        if yp is None:
            curve_date = pd.NaT
            dgs10 = dgs2 = curve_bp = np.nan
            curve_state = ""
        else:
            curve_date = pd.Timestamp(yp["date"])
            dgs10 = float(yp["dgs10"])
            dgs2 = float(yp["dgs2"])
            curve_bp = 100.0 * (dgs10 - dgs2)
            curve_state = "INVERTED" if curve_bp <= 0 else "POSITIVE"

        # Energy direction / shock state.
        wti = trailing_return_by_obs(series["DCOILWTICO"], event_date, 126)
        if wti is None:
            wti_date = pd.NaT
            wti_ret = np.nan
            energy_direction = ""
            energy_shock = ""
        else:
            wti_date = wti["date"]
            wti_ret = wti["return"]
            energy_direction = "RISING" if wti_ret > 0 else "FALLING_OR_FLAT"
            energy_shock = (
                "SHOCK_UP" if wti_ret >= 0.20
                else "SHOCK_DOWN" if wti_ret <= -0.20
                else "NEUTRAL"
            )

        # Conservative release-lag-aware monthly current-vintage states.
        cpi_yoy = yoy_at(series["CPIAUCNS"], state_period)
        cpi_yoy_prev3 = yoy_at(series["CPIAUCNS"], state_period - 3)
        inflation_level = (
            "HIGH" if np.isfinite(cpi_yoy) and cpi_yoy > 0.03
            else "LOW_OR_MODERATE" if np.isfinite(cpi_yoy)
            else ""
        )
        inflation_direction = (
            "RISING" if np.isfinite(cpi_yoy) and np.isfinite(cpi_yoy_prev3) and cpi_yoy > cpi_yoy_prev3
            else "FALLING_OR_FLAT" if np.isfinite(cpi_yoy) and np.isfinite(cpi_yoy_prev3)
            else ""
        )

        ip_yoy = yoy_at(series["INDPRO"], state_period)
        growth_state = (
            "STRONG" if np.isfinite(ip_yoy) and ip_yoy >= 0.02
            else "WEAK" if np.isfinite(ip_yoy)
            else ""
        )

        real_proxy = dgs10 - 100.0 * cpi_yoy if np.isfinite(dgs10) and np.isfinite(cpi_yoy) else np.nan
        real_proxy_state = (
            "POSITIVE" if np.isfinite(real_proxy) and real_proxy > 0
            else "NONPOSITIVE" if np.isfinite(real_proxy)
            else ""
        )

        nfci = last_strictly_before(series["NFCI"], event_date)
        if nfci is None:
            nfci_date = pd.NaT
            nfci_val = np.nan
            nfci_state = ""
        else:
            nfci_date = pd.Timestamp(nfci["date"])
            nfci_val = float(nfci["value"])
            nfci_state = "TIGHT" if nfci_val > 0 else "LOOSE_OR_AVERAGE"

        tips = last_strictly_before(series["DFII10"], event_date)
        if tips is None:
            tips_date = pd.NaT
            tips_val = np.nan
            tips_state = ""
        else:
            tips_date = pd.Timestamp(tips["date"])
            tips_val = float(tips["value"])
            tips_state = "POSITIVE" if tips_val > 0 else "NONPOSITIVE"

        # USD own-series direction; never level-spliced.
        if event_date < pd.Timestamp("2020-01-02"):
            usd = trailing_return_by_obs(series["TWEXM"], event_date, 26)
            usd_source = "TWEXM"
        else:
            usd = trailing_return_by_obs(series["DTWEXAFEGS"], event_date, 126)
            usd_source = "DTWEXAFEGS"
        if usd is None:
            usd_date = pd.NaT
            usd_ret = np.nan
            usd_state = ""
        else:
            usd_date = usd["date"]
            usd_ret = usd["return"]
            usd_state = "RISING" if usd_ret > 0 else "FALLING_OR_FLAT"

        rows.append({
            "cycle_id": ev["cycle_id"],
            "cycle_start_year": int(ev["cycle_start_year"]),
            "event_date": event_date,
            "gold_ret_6m": ev["ret_6m"],
            "gold_ret_12m": ev["ret_12m"],
            "gold_ret_24m": ev["ret_24m"],
            "gold_mdd_24m": ev["mdd_24m"],
            "gold_mae": ev["mae"],
            "gold_mfe": ev["mfe"],

            "state_macro_period": str(state_period),
            "CPI_YOY_LAG2": cpi_yoy,
            "INFLATION_LEVEL": inflation_level,
            "CPI_YOY_CHANGE_3M": cpi_yoy - cpi_yoy_prev3 if np.isfinite(cpi_yoy) and np.isfinite(cpi_yoy_prev3) else np.nan,
            "INFLATION_DIRECTION": inflation_direction,
            "INDPRO_YOY_LAG2": ip_yoy,
            "GROWTH_STATE": growth_state,

            "yield_curve_obs_date": curve_date,
            "DGS10": dgs10,
            "DGS2": dgs2,
            "curve_bp": curve_bp,
            "YIELD_CURVE_STATE": curve_state,

            "REAL_RATE_PROXY_PP": real_proxy,
            "REAL_RATE_PROXY_STATE": real_proxy_state,

            "wti_obs_date": wti_date,
            "WTI_126D_RETURN": wti_ret,
            "ENERGY_DIRECTION_STATE": energy_direction,
            "ENERGY_SHOCK_STATE": energy_shock,

            "nfci_obs_date": nfci_date,
            "NFCI": nfci_val,
            "NFCI_STATE": nfci_state,

            "dfii10_obs_date": tips_date,
            "DFII10": tips_val,
            "DFII10_STATE": tips_state,

            "usd_obs_date": usd_date,
            "USD_SOURCE_REGIME": usd_source,
            "USD_6M_RETURN": usd_ret,
            "USD_DIRECTION_DIAGNOSTIC": usd_state,

            "market_state_info_class": "PREDETERMINED_MARKET_HISTORY",
            "macro_state_info_class": "RELEASE_LAG_AWARE_CURRENT_VINTAGE_NOT_STRICT_ALFRED_PIT",
        })
    return pd.DataFrame(rows)


def median_stats(x):
    x = pd.to_numeric(x, errors="coerce").dropna()
    if not len(x):
        return np.nan, np.nan, np.nan
    return float(x.median()), float(x.quantile(.25)), float(x.quantile(.75))


def contrast_for(panel, state_var, state_a, state_b, outcome):
    g = panel[[state_var, outcome, "cycle_id"]].dropna(subset=[outcome]).copy()
    ga = g[g[state_var] == state_a]
    gb = g[g[state_var] == state_b]
    n_a, n_b = len(ga), len(gb)
    ma, q1a, q3a = median_stats(ga[outcome])
    mb, q1b, q3b = median_stats(gb[outcome])
    supported = n_a >= 3 and n_b >= 3
    diff = ma - mb if supported and np.isfinite(ma) and np.isfinite(mb) else np.nan
    return {
        "state_var": state_var,
        "state_a": state_a,
        "state_b": state_b,
        "outcome": outcome,
        "outcome_class": OUTCOME_FIELDS[outcome],
        "n_a": int(n_a),
        "n_b": int(n_b),
        "median_a": ma,
        "q25_a": q1a,
        "q75_a": q3a,
        "median_b": mb,
        "q25_b": q1b,
        "q75_b": q3b,
        "oriented_median_diff_a_minus_b": diff,
        "status": "SUPPORTED_DESCRIPTIVE" if supported else "INSUFFICIENT_SUPPORT",
    }


def loo_stability(panel, row):
    if row["status"] != "SUPPORTED_DESCRIPTIVE":
        return {
            "state_var": row["state_var"],
            "outcome": row["outcome"],
            "full_diff": np.nan,
            "full_sign": 0,
            "computable_loo": 0,
            "same_sign_loo": 0,
            "loo_sign_stable": False,
        }, []

    state_var = row["state_var"]
    state_a = row["state_a"]
    state_b = row["state_b"]
    outcome = row["outcome"]
    full_diff = float(row["oriented_median_diff_a_minus_b"])
    full_sign = int(np.sign(full_diff))

    detail = []
    signs = []
    for cycle_id in panel["cycle_id"].unique():
        sub = panel[panel["cycle_id"] != cycle_id]
        rr = contrast_for(sub, state_var, state_a, state_b, outcome)
        if rr["status"] != "SUPPORTED_DESCRIPTIVE":
            continue
        d = float(rr["oriented_median_diff_a_minus_b"])
        s = int(np.sign(d))
        signs.append(s)
        detail.append({
            "state_var": state_var,
            "outcome": outcome,
            "dropped_cycle_id": cycle_id,
            "loo_diff": d,
            "loo_sign": s,
            "full_sign": full_sign,
            "same_sign_as_full": bool(s == full_sign and full_sign != 0),
        })

    stable = bool(signs) and full_sign != 0 and all(s == full_sign for s in signs)
    return {
        "state_var": state_var,
        "outcome": outcome,
        "full_diff": full_diff,
        "full_sign": full_sign,
        "computable_loo": int(len(signs)),
        "same_sign_loo": int(sum(s == full_sign for s in signs)),
        "loo_sign_stable": stable,
    }, detail


def make_figures(panel, contrasts):
    primary = contrasts[
        (contrasts["outcome"] == "gold_ret_12m")
        & (contrasts["status"] == "SUPPORTED_DESCRIPTIVE")
    ].copy()
    if len(primary):
        fig, ax = plt.subplots(figsize=(10.5, 5.8))
        ax.bar(
            primary["state_var"],
            primary["oriented_median_diff_a_minus_b"] * 100.0,
        )
        ax.axhline(0, linewidth=0.8)
        ax.set_title("Gold +12M oriented median differences by predeclared state")
        ax.set_ylabel("Median difference A - B (percentage points)")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        fig.savefig(OUT / "01_gold_12m_state_contrasts.png", dpi=170, bbox_inches="tight")
        plt.close(fig)

    # Episode map: inflation / curve / energy states versus outcomes.
    cols = [
        "cycle_start_year","INFLATION_LEVEL","INFLATION_DIRECTION","GROWTH_STATE",
        "YIELD_CURVE_STATE","REAL_RATE_PROXY_STATE","ENERGY_DIRECTION_STATE",
        "NFCI_STATE","gold_ret_12m","gold_mdd_24m",
    ]
    table = panel[[c for c in cols if c in panel.columns]].copy()
    table.to_csv(OUT / "STATE_EPISODE_MAP.csv", index=False)


def write_report(panel, contrasts, stability, usd_agreement, qc):
    supported = contrasts[contrasts["status"] == "SUPPORTED_DESCRIPTIVE"].copy()
    primary = supported[supported["outcome_class"] == "PRIMARY"].copy()

    lines = [
        "# FED-CYCLE-STATE-001 — Predetermined-State Gold Heterogeneity Map",
        "",
        "**DESCRIPTIVE / ASSOCIATIONAL MECHANISM MAP / NOT CAUSAL / NOT A FORECASTING MODEL / NOT DEPLOYABLE**",
        "",
        "## Information timing",
        "",
        "- Yield curve and WTI states use observations strictly dated before FIRST_HIKE.",
        "- CPI and industrial-production states use M-2 to reduce release-timing ambiguity but are current-vintage historical values, not ALFRED vintages.",
        "- NFCI uses the last weekly observation strictly before the event but remains a current-vintage factor estimate.",
        "- No current-vintage macro variable is labeled strict PIT.",
        "",
        "## FIRST_HIKE state panel",
        "",
        panel.to_markdown(index=False),
        "",
        "## Supported primary state contrasts",
        "",
        primary.to_markdown(index=False) if len(primary) else "No primary contrast has n>=3 in both groups.",
        "",
        "## Leave-one-leg-out sign stability",
        "",
        stability[stability["outcome"].isin(["gold_ret_12m","gold_mdd_24m"])].to_markdown(index=False)
        if len(stability) else "No supported contrasts.",
        "",
        "## USD bridge diagnostic",
        "",
        f"- Legacy-vs-modern six-month return sign agreement in overlap: {usd_agreement:.4f}"
        if np.isfinite(usd_agreement) else "- USD bridge unavailable.",
        "- USD is not promoted to the primary state family unless bridge sign agreement >=90% and both outcome groups have n>=3.",
        "",
        "## Statistical status",
        "",
        "- No raw p-values are computed.",
        "- BH-FDR: not run / not applicable to this descriptive state map.",
        "- Leave-one-leg-out sign stability is a fragility diagnostic, not statistical significance.",
        "- The 10 mechanical tightening legs are not treated as 10 independent causal experiments.",
        "",
        "## Evidence boundary",
        "",
        "- DATA FACT: state timestamps and group support are auditable.",
        "- DESCRIPTIVE RESULT: supported group medians describe historical heterogeneity.",
        "- ASSOCIATIONAL EVIDENCE: only with explicit current-vintage and small-n limitations.",
        "- CAUSAL EVIDENCE: none.",
        "- OOS: not applicable; this is not a forecasting model.",
        "- DEPLOYMENT: none.",
    ]
    (OUT / "FED_CYCLE_STATE_001_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    if not OUTCOMES_FILE.exists() or not CYCLES_FILE.exists():
        raise RuntimeError("Required prior QC-passed Fed-cycle/Gold outputs are missing")

    outcomes = pd.read_csv(OUTCOMES_FILE, parse_dates=["event_date"])
    first = outcomes[outcomes["event_type"] == "FIRST_HIKE"].copy()
    if len(first) != 10:
        raise RuntimeError(f"Expected 10 FIRST_HIKE Gold outcomes, got {len(first)}")

    # Hash the committed outcome source for auditability.
    outcome_hash = hashlib.sha256(OUTCOMES_FILE.read_bytes()).hexdigest()

    series = {}
    prov = []
    for sid in SERIES:
        df, meta = fetch_fred(sid)
        series[sid] = df
        prov.append(source_row(sid, df, meta))

    usd_audit, usd_agreement = usd_bridge_audit(series["TWEXM"], series["DTWEXAFEGS"])
    panel = build_state_panel(first, series)

    contrast_rows = []
    stability_rows = []
    loo_detail = []
    for state_var, (state_a, state_b) in PRIMARY_STATES.items():
        for outcome in OUTCOME_FIELDS:
            r = contrast_for(panel, state_var, state_a, state_b, f"gold_{outcome}" if not outcome.startswith("gold_") else outcome)
            # OUTCOME_FIELDS keys are raw metric names; panel uses gold_ prefix.
            # Fix metadata lookup while preserving frozen outcome class.
            raw_outcome = outcome
            panel_outcome = f"gold_{raw_outcome}"
            r = contrast_for(panel, state_var, state_a, state_b, panel_outcome)
            r["outcome_class"] = OUTCOME_FIELDS[raw_outcome]
            contrast_rows.append(r)
            stab, detail = loo_stability(panel, r)
            stability_rows.append(stab)
            loo_detail.extend(detail)

    contrasts = pd.DataFrame(contrast_rows)
    stability = pd.DataFrame(stability_rows)
    loo_detail_df = pd.DataFrame(loo_detail)

    # USD diagnostic only if frozen bridge/support criteria pass.
    usd_promotable = bool(np.isfinite(usd_agreement) and usd_agreement >= 0.90)
    usd_group_counts = panel["USD_DIRECTION_DIAGNOSTIC"].value_counts(dropna=False).to_dict()
    if min(
        int(usd_group_counts.get("RISING", 0)),
        int(usd_group_counts.get("FALLING_OR_FLAT", 0)),
    ) < 3:
        usd_promotable = False

    # Timing QC.
    market_date_cols = ["yield_curve_obs_date","wti_obs_date","nfci_obs_date","dfii10_obs_date","usd_obs_date"]
    market_timing_violations = 0
    for col in market_date_cols:
        d = pd.to_datetime(panel[col], errors="coerce")
        market_timing_violations += int((d.notna() & (d >= panel["event_date"])).sum())

    macro_period_violations = 0
    for _, r in panel.iterrows():
        expected = pd.Timestamp(r["event_date"]).to_period("M") - 2
        actual = pd.Period(r["state_macro_period"], freq="M")
        if actual > expected:
            macro_period_violations += 1

    # Threshold/support QC.
    unsupported_presented = int(
        (
            (contrasts["status"] == "SUPPORTED_DESCRIPTIVE")
            & ((contrasts["n_a"] < 3) | (contrasts["n_b"] < 3))
        ).sum()
    )
    dfii_support = int(panel["DFII10"].notna().sum())

    hard_fail = (
        len(panel) != 10
        or market_timing_violations != 0
        or macro_period_violations != 0
        or unsupported_presented != 0
        or dfii_support > 3
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-STATE-001",
        "first_hike_rows": int(len(panel)),
        "gold_outcome_source_sha256": outcome_hash,
        "market_timing_violations": market_timing_violations,
        "macro_period_violations": macro_period_violations,
        "unsupported_presented_as_supported": unsupported_presented,
        "dfii10_first_hike_support": dfii_support,
        "usd_bridge_sign_agreement": usd_agreement,
        "usd_primary_promotable": usd_promotable,
        "primary_state_variables": list(PRIMARY_STATES.keys()),
        "supported_primary_outcome_contrasts": int(
            (
                (contrasts["status"] == "SUPPORTED_DESCRIPTIVE")
                & (contrasts["outcome_class"] == "PRIMARY")
            ).sum()
        ),
        "fdr_status": "NOT_RUN_DESCRIPTIVE_STATE_MAP",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "causal_status": "NONE",
        "raw_source_histories_committed": False,
    }

    pd.DataFrame(prov).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    panel.to_csv(OUT / "STATE_EVENT_PANEL.csv", index=False)
    contrasts.to_csv(OUT / "STATE_CONTRASTS.csv", index=False)
    stability.to_csv(OUT / "STATE_LOO_STABILITY.csv", index=False)
    loo_detail_df.to_csv(OUT / "STATE_LOO_DETAIL.csv", index=False)
    usd_audit.to_csv(OUT / "USD_BRIDGE_AUDIT.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    make_figures(panel, contrasts)
    write_report(panel, contrasts, stability, usd_agreement, qc)

    if hard_fail:
        raise SystemExit("FED-CYCLE-STATE-001 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
