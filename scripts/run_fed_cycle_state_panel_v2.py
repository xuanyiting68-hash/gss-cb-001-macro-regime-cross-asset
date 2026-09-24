#!/usr/bin/env python3
"""
FED-CYCLE-STATE-PANEL-002
Within-cycle monthly continuous-state panel with dependence-aware sign-flip
inference and BY-FDR for the frozen primary family.

Reference:
research/FED_CYCLE_STATE_PANEL_002_LOCK.md
"""
from __future__ import annotations

import hashlib
import io
import itertools
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_state_panel_v2"
OUT.mkdir(parents=True, exist_ok=True)

CYCLES_FILE = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_TIGHTENING_CYCLES.csv"

GOLD_SOURCE_COMMIT = "95bfea9197222dcda13d8c4d9928fb631fe745aa"
GOLD_URL = f"https://raw.githubusercontent.com/datasets/gold-prices/{GOLD_SOURCE_COMMIT}/data/monthly.csv"
GOLD_PACKAGE_URL = f"https://raw.githubusercontent.com/datasets/gold-prices/{GOLD_SOURCE_COMMIT}/datapackage.json"

FRED_SERIES = {
    "CPIAUCNS": ("U.S. BLS via FRED", "macro_current_vintage"),
    "INDPRO": ("Board of Governors via FRED", "macro_current_vintage"),
    "DGS10": ("Board of Governors via FRED", "market_history"),
    "DGS2": ("Board of Governors via FRED", "market_history"),
    "DCOILWTICO": ("U.S. EIA via FRED", "market_history"),
    "NFCI": ("Federal Reserve Bank of Chicago via FRED", "macro_current_vintage"),
    "DFII10": ("Board of Governors via FRED", "market_history_limited"),
    "TWEXM": ("Board of Governors via FRED", "usd_legacy"),
    "DTWEXAFEGS": ("Board of Governors via FRED", "usd_modern"),
}

PRIMARY_PREDICTORS = ["CPI_YOY", "CPI_MOMENTUM", "INDPRO_YOY", "WTI_6M_RET"]
PRIMARY_OUTCOMES = ["GOLD_FWD_6M_RET", "GOLD_FWD_6M_MDD"]

SECONDARY_PREDICTORS = [
    "CURVE_BP", "DGS10_LEVEL", "REAL_RATE_PROXY_PP",
    "NFCI", "USD_6M_RET", "DFII10",
]


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
    direct = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    errors = []
    for _ in range(2):
        try:
            raw = fetch_bytes(direct, timeout=30)
            df = pd.read_csv(io.BytesIO(raw))
            date_col = df.columns[0]
            value_col = series_id if series_id in df.columns else df.columns[1]
            df = df.rename(columns={date_col: "date", value_col: "value"})
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
            return df, {
                "url": direct,
                "acquisition_method": "FRED_DIRECT_CSV",
                "sha256": hashlib.sha256(raw).hexdigest(),
                "raw_bytes": len(raw),
            }
        except Exception as exc:
            errors.append(repr(exc))

    mirror = f"https://api.db.nomics.world/v22/series/FRED/{series_id}?observations=1"
    raw = fetch_bytes(mirror, timeout=60)
    obj = json.loads(raw.decode("utf-8"))
    docs = obj["series"]["docs"]
    if not docs:
        raise RuntimeError(f"No FRED data for {series_id}; direct errors={errors}")
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
        "url": mirror,
        "acquisition_method": "DBNOMICS_FRED_MIRROR",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "raw_bytes": len(raw),
    }


def load_gold():
    raw = fetch_bytes(GOLD_URL)
    pkg_raw = fetch_bytes(GOLD_PACKAGE_URL)
    pkg = json.loads(pkg_raw.decode("utf-8"))
    licenses = [x.get("name", "") for x in pkg.get("licenses", [])]
    if "ODC-PDDL-1.0" not in licenses:
        raise RuntimeError(f"Expected Gold source license missing: {licenses}")

    df = pd.read_csv(io.BytesIO(raw))
    df["period"] = pd.PeriodIndex(df["Date"].astype(str), freq="M")
    df["price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["period", "price"]).sort_values("period").drop_duplicates("period")
    df = df[df["period"] >= pd.Period("1960-01", freq="M")].reset_index(drop=True)

    expected = pd.period_range(df["period"].min(), df["period"].max(), freq="M")
    missing = expected.difference(pd.PeriodIndex(df["period"]))
    if len(missing):
        raise RuntimeError(f"Gold monthly source has gaps: {list(missing[:12])}")

    prov = {
        "series_id": "GOLD_MONTHLY",
        "source": "datasets/gold-prices / World Bank Commodity Markets",
        "information_source_class": "OUTCOME_SOURCE",
        "url": GOLD_URL,
        "acquisition_method": "PINNED_GITHUB_RAW",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "raw_bytes": len(raw),
        "first_date": str(df["period"].min()),
        "last_date": str(df["period"].max()),
        "raw_committed": False,
        "source_commit": GOLD_SOURCE_COMMIT,
    }
    return df[["period", "price"]], prov


def source_row(series_id, df, meta):
    source, info_class = FRED_SERIES[series_id]
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
        "source_commit": "",
    }


def load_cycles():
    c = pd.read_csv(
        CYCLES_FILE,
        parse_dates=["first_hike", "last_hike", "pause_start", "first_cut"],
    ).sort_values("first_hike").reset_index(drop=True)
    if len(c) != 10:
        raise RuntimeError(f"Expected 10 frozen mechanical cycles, got {len(c)}")
    return c


def months_between(a: pd.Timestamp, b: pd.Timestamp) -> int:
    pa = a.to_period("M")
    pb = b.to_period("M")
    return (pb.year - pa.year) * 12 + (pb.month - pa.month)


def assign_broad_clusters(cycles):
    out = cycles.copy()
    ids = []
    cluster = 0
    prev = None
    for _, r in out.iterrows():
        dt = pd.Timestamp(r["first_hike"])
        if prev is None or months_between(prev, dt) > 18:
            cluster += 1
        ids.append(f"B{cluster:02d}")
        prev = dt
    out["broad_episode_id"] = ids
    return out


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
    return float(now / prev - 1.0)


def last_before(df: pd.DataFrame, cutoff: pd.Timestamp):
    x = df[(df["date"] < cutoff) & df["value"].notna()]
    return None if x.empty else x.iloc[-1]


def common_yield_before(dgs10, dgs2, cutoff):
    a = dgs10[["date", "value"]].rename(columns={"value": "dgs10"})
    b = dgs2[["date", "value"]].rename(columns={"value": "dgs2"})
    m = a.merge(b, on="date", how="inner").dropna()
    m = m[m["date"] < cutoff]
    return None if m.empty else m.iloc[-1]


def trailing_return_by_obs(df, cutoff, lag_obs):
    x = df[(df["date"] < cutoff) & df["value"].notna()].reset_index(drop=True)
    if len(x) <= lag_obs:
        return None
    last = x.iloc[-1]
    prev = x.iloc[-1 - lag_obs]
    if float(prev["value"]) == 0:
        return None
    return {
        "obs_date": pd.Timestamp(last["date"]),
        "lag_date": pd.Timestamp(prev["date"]),
        "return": float(last["value"] / prev["value"] - 1.0),
    }


def mdd(vals):
    vals = np.asarray(vals, dtype=float)
    peaks = np.maximum.accumulate(vals)
    return float(np.max(1.0 - vals / peaks))


def path_metrics(price_map, month):
    baseline_p = month - 1
    needed = [baseline_p] + [month + k for k in range(6)]
    if any(p not in price_map for p in needed):
        return None
    vals = np.array([float(price_map[p]) for p in needed], dtype=float)
    baseline = vals[0]
    rel = vals / baseline - 1.0
    logret = np.diff(np.log(vals))
    vals3 = vals[:4]

    return {
        "GOLD_BASELINE_PRICE": baseline,
        "GOLD_FWD_3M_RET": float(vals[3] / baseline - 1.0),
        "GOLD_FWD_6M_RET": float(vals[6] / baseline - 1.0),
        "GOLD_FWD_3M_MDD": mdd(vals3),
        "GOLD_FWD_6M_MDD": mdd(vals),
        "GOLD_FWD_6M_MAE": float(np.min(rel)),
        "GOLD_FWD_6M_MFE": float(np.max(rel)),
        "GOLD_FWD_6M_DOWN_SEMIVOL": float(
            math.sqrt(12.0 * np.mean(np.minimum(logret, 0.0) ** 2))
        ),
    }


def build_panel(cycles, gold, s):
    price_map = dict(zip(gold["period"], gold["price"].astype(float)))
    rows = []

    for _, cyc in cycles.iterrows():
        first_hike = pd.Timestamp(cyc["first_hike"])
        first_cut = pd.Timestamp(cyc["first_cut"])
        start = first_hike.to_period("M") + 1
        natural_end = first_cut.to_period("M") - 1
        cap_end = first_hike.to_period("M") + 36
        end = min(natural_end, cap_end)

        for month in pd.period_range(start, end, freq="M"):
            month_start = month.start_time
            macro_period = month - 2

            g = path_metrics(price_map, month)
            if g is None:
                continue

            cpi_yoy = yoy_at(s["CPIAUCNS"], macro_period)
            cpi_prev = yoy_at(s["CPIAUCNS"], macro_period - 3)
            cpi_mom = cpi_yoy - cpi_prev if np.isfinite(cpi_yoy) and np.isfinite(cpi_prev) else np.nan
            indpro_yoy = yoy_at(s["INDPRO"], macro_period)

            yp = common_yield_before(s["DGS10"], s["DGS2"], month_start)
            if yp is None:
                yield_date = pd.NaT
                dgs10 = dgs2 = curve_bp = np.nan
            else:
                yield_date = pd.Timestamp(yp["date"])
                dgs10 = float(yp["dgs10"])
                dgs2 = float(yp["dgs2"])
                curve_bp = 100.0 * (dgs10 - dgs2)

            real_proxy = (
                dgs10 - 100.0 * cpi_yoy
                if np.isfinite(dgs10) and np.isfinite(cpi_yoy)
                else np.nan
            )

            wti = trailing_return_by_obs(s["DCOILWTICO"], month_start, 126)
            if wti is None:
                wti_date = pd.NaT
                wti_ret = np.nan
            else:
                wti_date = wti["obs_date"]
                wti_ret = wti["return"]

            nfci = last_before(s["NFCI"], month_start)
            if nfci is None:
                nfci_date = pd.NaT
                nfci_val = np.nan
            else:
                nfci_date = pd.Timestamp(nfci["date"])
                nfci_val = float(nfci["value"])

            tips = last_before(s["DFII10"], month_start)
            if tips is None:
                tips_date = pd.NaT
                tips_val = np.nan
            else:
                tips_date = pd.Timestamp(tips["date"])
                tips_val = float(tips["value"])

            if month_start < pd.Timestamp("2020-01-02"):
                usd = trailing_return_by_obs(s["TWEXM"], month_start, 26)
                usd_source = "TWEXM"
            else:
                usd = trailing_return_by_obs(s["DTWEXAFEGS"], month_start, 126)
                usd_source = "DTWEXAFEGS"
            if usd is None:
                usd_date = pd.NaT
                usd_ret = np.nan
            else:
                usd_date = usd["obs_date"]
                usd_ret = usd["return"]

            rows.append({
                "cycle_id": cyc["cycle_id"],
                "broad_episode_id": cyc["broad_episode_id"],
                "cycle_start_year": int(first_hike.year),
                "first_hike": first_hike,
                "first_cut": first_cut,
                "panel_month": str(month),
                "panel_month_start": month_start,
                "macro_state_period": str(macro_period),

                "CPI_YOY": cpi_yoy,
                "CPI_MOMENTUM": cpi_mom,
                "INDPRO_YOY": indpro_yoy,

                "yield_obs_date": yield_date,
                "DGS10_LEVEL": dgs10,
                "DGS2_LEVEL": dgs2,
                "CURVE_BP": curve_bp,
                "REAL_RATE_PROXY_PP": real_proxy,

                "wti_obs_date": wti_date,
                "WTI_6M_RET": wti_ret,

                "nfci_obs_date": nfci_date,
                "NFCI": nfci_val,

                "dfii10_obs_date": tips_date,
                "DFII10": tips_val,

                "usd_obs_date": usd_date,
                "USD_SOURCE_REGIME": usd_source,
                "USD_6M_RET": usd_ret,

                **g,
            })

    return pd.DataFrame(rows)


def exact_signflip_p(scores):
    scores = np.asarray(scores, dtype=float)
    g = len(scores)
    if g == 0:
        return np.nan
    observed = abs(scores.sum())
    exceed = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=g):
        val = abs(np.dot(np.asarray(signs), scores))
        if val >= observed - 1e-15:
            exceed += 1
        total += 1
    return float(exceed / total)


def regression_core(sample, predictor, outcome):
    x = pd.to_numeric(sample[predictor], errors="coerce")
    y = pd.to_numeric(sample[outcome], errors="coerce")
    d = sample.assign(_x=x, _y=y).dropna(subset=["_x", "_y"]).copy()

    if d.empty:
        return None

    d["_x_dm"] = d["_x"] - d.groupby("cycle_id")["_x"].transform("mean")
    d["_y_dm"] = d["_y"] - d.groupby("cycle_id")["_y"].transform("mean")

    cycle_var = d.groupby("cycle_id")["_x_dm"].apply(lambda z: float(np.sum(z.to_numpy() ** 2)))
    active_cycles = cycle_var[cycle_var > 1e-14].index.tolist()
    d = d[d["cycle_id"].isin(active_cycles)].copy()
    if d.empty:
        return None

    counts = d.groupby("cycle_id").size()
    d["_w"] = d["cycle_id"].map(lambda c: 1.0 / float(counts.loc[c]))

    total_w = float(d["_w"].sum())
    xrms = math.sqrt(float(np.sum(d["_w"] * d["_x_dm"] ** 2) / total_w))
    if not np.isfinite(xrms) or xrms <= 1e-14:
        return None

    d["_x_std"] = d["_x_dm"] / xrms
    denom = float(np.sum(d["_w"] * d["_x_std"] ** 2))
    numer = float(np.sum(d["_w"] * d["_x_std"] * d["_y_dm"]))
    beta = numer / denom

    broad_scores = (
        d.assign(_score=d["_w"] * d["_x_std"] * d["_y_dm"])
        .groupby("broad_episode_id")["_score"].sum()
    )
    mech_scores = (
        d.assign(_score=d["_w"] * d["_x_std"] * d["_y_dm"])
        .groupby("cycle_id")["_score"].sum()
    )

    cycle_weight_sum = d.groupby("cycle_id")["_w"].sum()

    return {
        "data": d,
        "beta": beta,
        "xrms": xrms,
        "n_rows": int(len(d)),
        "n_cycles": int(d["cycle_id"].nunique()),
        "n_broad_clusters": int(d["broad_episode_id"].nunique()),
        "broad_scores": broad_scores,
        "mech_scores": mech_scores,
        "cycle_weight_sum": cycle_weight_sum,
    }


def estimate_test(panel, predictor, outcome):
    core = regression_core(panel, predictor, outcome)
    if core is None:
        return {
            "predictor": predictor,
            "outcome": outcome,
            "n_rows": 0,
            "n_cycles": 0,
            "n_broad_clusters": 0,
            "beta_per_1sd_within": np.nan,
            "p_broad_exact": np.nan,
            "p_mechanical_exact": np.nan,
            "loo_broad_sign_stable": False,
            "loo_broad_computable": 0,
            "status": "INSUFFICIENT_SUPPORT",
            "max_cycle_weight_error": np.nan,
        }

    supported = (
        core["n_cycles"] >= 5
        and core["n_broad_clusters"] >= 4
    )

    p_broad = (
        exact_signflip_p(core["broad_scores"].to_numpy())
        if supported else np.nan
    )
    p_mech = (
        exact_signflip_p(core["mech_scores"].to_numpy())
        if supported else np.nan
    )

    full_sign = int(np.sign(core["beta"]))
    loo_signs = []
    if supported and full_sign != 0:
        for bid in sorted(core["data"]["broad_episode_id"].unique()):
            sub = core["data"][core["data"]["broad_episode_id"] != bid].copy()
            rc = regression_core(sub, predictor, outcome)
            if rc is None or rc["n_cycles"] < 4 or rc["n_broad_clusters"] < 3:
                continue
            loo_signs.append(int(np.sign(rc["beta"])))
    stable = bool(loo_signs) and full_sign != 0 and all(s == full_sign for s in loo_signs)

    max_werr = float(np.max(np.abs(core["cycle_weight_sum"].to_numpy() - 1.0)))

    return {
        "predictor": predictor,
        "outcome": outcome,
        "n_rows": core["n_rows"],
        "n_cycles": core["n_cycles"],
        "n_broad_clusters": core["n_broad_clusters"],
        "beta_per_1sd_within": core["beta"],
        "within_predictor_rms_native_units": core["xrms"],
        "p_broad_exact": p_broad,
        "p_mechanical_exact": p_mech,
        "loo_broad_sign_stable": stable,
        "loo_broad_computable": int(len(loo_signs)),
        "status": "SUPPORTED_TEST" if supported else "INSUFFICIENT_SUPPORT",
        "max_cycle_weight_error": max_werr,
    }


def fdr_adjust_with_total_m(pvals, total_m, by=False):
    idx = [i for i, p in enumerate(pvals) if np.isfinite(p)]
    out = [np.nan] * len(pvals)
    if not idx:
        return out

    ordered = sorted(idx, key=lambda i: pvals[i])
    c_m = sum(1.0 / k for k in range(1, total_m + 1)) if by else 1.0

    raw = []
    for rank, i in enumerate(ordered, start=1):
        raw.append(min(1.0, float(pvals[i]) * total_m * c_m / rank))

    adj = raw[:]
    for j in range(len(adj) - 2, -1, -1):
        adj[j] = min(adj[j], adj[j + 1])

    for i, q in zip(ordered, adj):
        out[i] = q
    return out


def build_broad_registry(cycles):
    rows = []
    for bid, g in cycles.groupby("broad_episode_id", sort=False):
        rows.append({
            "broad_episode_id": bid,
            "n_mechanical_legs": int(len(g)),
            "mechanical_cycle_ids": ";".join(g["cycle_id"].astype(str)),
            "first_hike_min": g["first_hike"].min(),
            "first_hike_max": g["first_hike"].max(),
            "cycle_start_years": ";".join(map(str, g["first_hike"].dt.year.astype(int).tolist())),
        })
    return pd.DataFrame(rows)


def make_figures(primary):
    labels = {
        "CPI_YOY": "CPI YoY",
        "CPI_MOMENTUM": "CPI momentum",
        "INDPRO_YOY": "INDPRO YoY",
        "WTI_6M_RET": "WTI 6M return",
    }
    for outcome, fname, title, ylabel in [
        ("GOLD_FWD_6M_RET", "01_primary_gold_fwd6m_return.png",
         "Within-cycle states vs next 6 complete months Gold return",
         "Coefficient per 1 within-cycle state SD (return units)"),
        ("GOLD_FWD_6M_MDD", "02_primary_gold_fwd6m_mdd.png",
         "Within-cycle states vs next 6 complete months Gold MDD",
         "Coefficient per 1 within-cycle state SD (drawdown units)"),
    ]:
        g = primary[primary["outcome"] == outcome].copy()
        if g.empty:
            continue
        fig, ax = plt.subplots(figsize=(9.5, 5.4))
        ax.bar([labels.get(x, x) for x in g["predictor"]], g["beta_per_1sd_within"] * 100.0)
        ax.axhline(0, linewidth=0.8)
        ax.set_title(title)
        ax.set_ylabel(ylabel.replace("(return units)", "(percentage points)").replace("(drawdown units)", "(percentage points)"))
        ax.tick_params(axis="x", rotation=25)
        fig.tight_layout()
        fig.savefig(OUT / fname, dpi=170, bbox_inches="tight")
        plt.close(fig)


def write_report(panel, primary, secondary, broad, qc):
    survivors = primary[primary["by_q_10pct"].notna() & (primary["by_q_10pct"] <= 0.10)]

    lines = [
        "# FED-CYCLE-STATE-PANEL-002 — Within-Cycle Continuous-State Report",
        "",
        "**ASSOCIATIONAL / DEPENDENCE-AWARE / NOT CAUSAL / NOT A FORECASTING MODEL / NOT DEPLOYABLE**",
        "",
        "## Panel",
        "",
        f"- Monthly panel rows: {len(panel)}",
        f"- Mechanical cycles: {panel['cycle_id'].nunique()}",
        f"- Broad episode clusters: {panel['broad_episode_id'].nunique()}",
        "- Active window: first full month after FIRST_HIKE through month before FIRST_CUT, capped at 36 months.",
        "- Cycle fixed effects: yes.",
        "- Equal mechanical-cycle total regression weight: yes.",
        "- Primary inference: exact broad-episode cluster sign-flip.",
        "",
        "## Broad episode registry",
        "",
        broad.to_markdown(index=False),
        "",
        "## Frozen primary family",
        "",
        primary.to_markdown(index=False),
        "",
        "## BY-FDR 10% survivors",
        "",
        survivors.to_markdown(index=False) if len(survivors) else "No primary test survives BY-FDR 10%.",
        "",
        "## Secondary continuous diagnostics",
        "",
        secondary.to_markdown(index=False),
        "",
        "## Interpretation boundary",
        "",
        "- Current-vintage CPI/INDPRO/NFCI histories are not strict ALFRED PIT vintages.",
        "- Exact sign-flip inference preserves whole broad episode blocks; rows are not treated as IID.",
        "- BY-FDR is the public primary multiplicity rule; BH is shown only as a diagnostic.",
        "- A surviving association would still not identify a causal Gold driver.",
        "- OOS: not applicable; this is not a forecasting model.",
        "- Deployment: none.",
    ]
    (OUT / "FED_CYCLE_STATE_PANEL_002_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    cycles = assign_broad_clusters(load_cycles())
    broad = build_broad_registry(cycles)
    gold, gold_prov = load_gold()

    series = {}
    prov = [gold_prov]
    for sid in FRED_SERIES:
        df, meta = fetch_fred(sid)
        series[sid] = df
        prov.append(source_row(sid, df, meta))

    panel = build_panel(cycles, gold, series)

    # Primary family: exactly 4 x 2 = 8.
    primary_rows = []
    for predictor in PRIMARY_PREDICTORS:
        for outcome in PRIMARY_OUTCOMES:
            primary_rows.append(estimate_test(panel, predictor, outcome))
    primary = pd.DataFrame(primary_rows)

    pvals = primary["p_broad_exact"].tolist()
    primary["bh_q_10pct_diagnostic"] = fdr_adjust_with_total_m(pvals, total_m=8, by=False)
    primary["by_q_10pct"] = fdr_adjust_with_total_m(pvals, total_m=8, by=True)
    primary["by_fdr10_status"] = np.where(
        primary["by_q_10pct"].notna() & (primary["by_q_10pct"] <= 0.10),
        "BY_FDR10_SURVIVOR",
        np.where(primary["status"] == "SUPPORTED_TEST", "NO_BY_FDR10", "INSUFFICIENT_SUPPORT"),
    )

    secondary_rows = []
    for predictor in SECONDARY_PREDICTORS:
        for outcome in PRIMARY_OUTCOMES:
            secondary_rows.append(estimate_test(panel, predictor, outcome))
    secondary = pd.DataFrame(secondary_rows)
    secondary["multiplicity_status"] = "SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM"

    # QC.
    panel["panel_period"] = pd.PeriodIndex(panel["panel_month"], freq="M")
    first_cut_period = panel["first_cut"].dt.to_period("M")
    first_hike_period = panel["first_hike"].dt.to_period("M")

    first_cut_month_violations = int((panel["panel_period"] >= first_cut_period).sum())
    pre_start_violations = int((panel["panel_period"] <= first_hike_period).sum())
    cap_violations = int(
        (
            panel["panel_period"].map(lambda p: p.ordinal).to_numpy()
            >
            (first_hike_period + 36).map(lambda p: p.ordinal).to_numpy()
        ).sum()
    )

    market_date_cols = ["yield_obs_date", "wti_obs_date", "nfci_obs_date", "dfii10_obs_date", "usd_obs_date"]
    market_timing_violations = 0
    for col in market_date_cols:
        d = pd.to_datetime(panel[col], errors="coerce")
        market_timing_violations += int(
            (d.notna() & (d >= panel["panel_month_start"])).sum()
        )

    macro_period_violations = 0
    for _, r in panel.iterrows():
        expected = pd.Period(r["panel_month"], freq="M") - 2
        actual = pd.Period(r["macro_state_period"], freq="M")
        if actual > expected:
            macro_period_violations += 1

    family_size_bad = int(len(primary) != 8)
    supported_weight_bad = int(
        (
            (primary["status"] == "SUPPORTED_TEST")
            & (primary["max_cycle_weight_error"] > 1e-10)
        ).sum()
    )
    unsupported_has_p = int(
        (
            (primary["status"] != "SUPPORTED_TEST")
            & primary["p_broad_exact"].notna()
        ).sum()
    )

    hard_fail = (
        len(panel) < 100
        or cycles["broad_episode_id"].nunique() != 7
        or first_cut_month_violations != 0
        or pre_start_violations != 0
        or cap_violations != 0
        or market_timing_violations != 0
        or macro_period_violations != 0
        or family_size_bad != 0
        or supported_weight_bad != 0
        or unsupported_has_p != 0
        or gold_prov["source_commit"] != GOLD_SOURCE_COMMIT
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-STATE-PANEL-002",
        "panel_rows": int(len(panel)),
        "mechanical_cycles": int(panel["cycle_id"].nunique()),
        "broad_episode_clusters": int(panel["broad_episode_id"].nunique()),
        "first_cut_month_violations": first_cut_month_violations,
        "pre_first_hike_complete_month_violations": pre_start_violations,
        "36m_cap_violations": cap_violations,
        "market_timing_violations": market_timing_violations,
        "macro_period_violations": macro_period_violations,
        "primary_family_size": int(len(primary)),
        "supported_primary_tests": int((primary["status"] == "SUPPORTED_TEST").sum()),
        "supported_weight_violations": supported_weight_bad,
        "unsupported_tests_with_pvalues": unsupported_has_p,
        "by_fdr10_survivors": int((primary["by_fdr10_status"] == "BY_FDR10_SURVIVOR").sum()),
        "bh_fdr10_diagnostic_survivors": int(
            (primary["bh_q_10pct_diagnostic"].notna() & (primary["bh_q_10pct_diagnostic"] <= 0.10)).sum()
        ),
        "gold_source_commit": GOLD_SOURCE_COMMIT,
        "primary_inference": "EXACT_BROAD_EPISODE_CLUSTER_SIGN_FLIP",
        "multiplicity_primary": "BENJAMINI_YEKUTIELI_FDR_10_PERCENT",
        "iid_row_se_used": False,
        "raw_source_histories_committed": False,
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    # Remove helper Period column before public output.
    panel = panel.drop(columns=["panel_period"])

    pd.DataFrame(prov).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    cycles.to_csv(OUT / "CYCLE_REGISTRY_WITH_BROAD_EPISODES.csv", index=False)
    broad.to_csv(OUT / "BROAD_EPISODE_REGISTRY.csv", index=False)
    panel.to_csv(OUT / "MONTHLY_STATE_PANEL.csv", index=False)
    primary.to_csv(OUT / "PRIMARY_TESTS.csv", index=False)
    secondary.to_csv(OUT / "SECONDARY_DIAGNOSTICS.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    make_figures(primary)
    write_report(panel, primary, secondary, broad, qc)

    if hard_fail:
        raise SystemExit("FED-CYCLE-STATE-PANEL-002 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
