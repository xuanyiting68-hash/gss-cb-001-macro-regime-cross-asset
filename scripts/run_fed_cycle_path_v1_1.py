#!/usr/bin/env python3
"""
FED-CYCLE-PATH-001
Long-history Fed cycle x cross-asset path-risk foundation.

Reference specification:
research/FED_CYCLE_PATH_001_LOCK.md

Raw downloaded market/source bytes are never written into the repository.
Only provenance hashes, normalized paths, derived metrics, reports and figures
are written to results/fed_cycle_path_v1.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_path_v1_1"
OUT.mkdir(parents=True, exist_ok=True)

MAX_PATH = 252
RECOVERY_HORIZON = 756
ENDPOINTS = [1, 5, 20, 60, 120, 252]
VOL_ENDPOINTS = [20, 60, 120, 252]

FRED_ASSETS = {
    "NASDAQ": {
        "id": "NASDAQCOM",
        "kind": "price",
        "label": "Nasdaq Composite",
        "source": "Nasdaq, Inc. via FRED",
    },
    "WTI": {
        "id": "DCOILWTICO",
        "kind": "price",
        "label": "WTI spot",
        "source": "U.S. Energy Information Administration via FRED",
    },
    "USD_BROAD": {
        "id": "DTWEXBGS",
        "kind": "price",
        "label": "Nominal Broad U.S. Dollar Index",
        "source": "Board of Governors of the Federal Reserve System via FRED",
    },
    "DGS2": {
        "id": "DGS2",
        "kind": "rate",
        "label": "2Y Treasury yield",
        "source": "Board of Governors of the Federal Reserve System via FRED",
    },
    "DGS10": {
        "id": "DGS10",
        "kind": "rate",
        "label": "10Y Treasury yield",
        "source": "Board of Governors of the Federal Reserve System via FRED",
    },
    "DFII10": {
        "id": "DFII10",
        "kind": "rate",
        "label": "10Y real yield",
        "source": "Board of Governors of the Federal Reserve System via FRED",
    },
    "T5YIE": {
        "id": "T5YIE",
        "kind": "rate",
        "label": "5Y breakeven inflation",
        "source": "Federal Reserve Bank of St. Louis via FRED",
    },
}

YAHOO_ASSETS = {
    "GOLD": {
        "symbol": "GC=F",
        "kind": "price",
        "label": "COMEX Gold continuous futures proxy",
        "source": "Yahoo Finance public chart history",
    },
    "SP500": {
        "symbol": "^GSPC",
        "kind": "price",
        "label": "S&P 500 cash index",
        "source": "Yahoo Finance public chart history",
    },
}

POLICY_SERIES = {
    "DFEDTAR": "Federal Funds Target Rate",
    "DFEDTARL": "Federal Funds Target Range - Lower Limit",
    "DFEDTARU": "Federal Funds Target Range - Upper Limit",
}

RECENT_SCHEDULED_DECISIONS = [
    # Explicit Federal Reserve regular-meeting decision dates. These supplement
    # historical pages and close the modern calendar gap identified in v1.
    "2021-01-27","2021-03-17","2021-04-28","2021-06-16",
    "2021-07-28","2021-09-22","2021-11-03","2021-12-15",
    "2022-01-26","2022-03-16","2022-05-04","2022-06-15",
    "2022-07-27","2022-09-21","2022-11-02","2022-12-14",
    "2023-02-01","2023-03-22","2023-05-03","2023-06-14",
    "2023-07-26","2023-09-20","2023-11-01","2023-12-13",
    "2024-01-31","2024-03-20","2024-05-01","2024-06-12",
    "2024-07-31","2024-09-18","2024-11-07","2024-12-18",
    "2025-01-29","2025-03-19","2025-05-07","2025-06-18",
    "2025-07-30","2025-09-17","2025-10-29","2025-12-10",
    "2026-01-28","2026-03-18","2026-04-29","2026-06-17",
    "2026-07-29","2026-09-16","2026-10-28","2026-12-09",
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
    """Direct FRED CSV with DBnomics/FRED mirror fallback."""
    fred_url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    errors = []
    for attempt in range(2):
        try:
            raw = fetch_bytes(fred_url, timeout=25)
            df = pd.read_csv(io.BytesIO(raw))
            date_col = df.columns[0]
            value_col = series_id if series_id in df.columns else df.columns[1]
            df = df.rename(columns={date_col: "date", value_col: "value"})
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna(subset=["date"]).sort_values("date")
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
    df = df.dropna(subset=["date"]).sort_values("date")
    return df, {
        "url": mirror_url,
        "acquisition_method": "DBNOMICS_FRED_MIRROR",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "raw_bytes": len(raw),
    }


def fetch_yahoo_chart(symbol: str):
    """Yahoo Finance chart-history endpoint; raw JSON bytes are not committed."""
    enc = quote(symbol, safe="")
    urls = [
        f"https://query1.finance.yahoo.com/v8/finance/chart/{enc}?period1=0&period2=1893456000&interval=1d&events=history&includeAdjustedClose=true",
        f"https://query2.finance.yahoo.com/v8/finance/chart/{enc}?period1=0&period2=1893456000&interval=1d&events=history&includeAdjustedClose=true",
    ]
    errors = []
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
                raise RuntimeError("Yahoo timestamp/close length mismatch")
            out = pd.DataFrame({
                "date": pd.to_datetime(ts, unit="s", utc=True).tz_convert(None).normalize(),
                "value": pd.to_numeric(close, errors="coerce"),
            })
            out = out.dropna(subset=["date", "value"]).sort_values("date")
            out = out.drop_duplicates("date", keep="last").reset_index(drop=True)
            if len(out) < 100:
                raise RuntimeError(f"Yahoo history too short for {symbol}: {len(out)}")
            return out, {
                "url": url,
                "acquisition_method": "YAHOO_FINANCE_CHART_JSON",
                "sha256": hashlib.sha256(raw).hexdigest(),
                "raw_bytes": len(raw),
            }
        except Exception as exc:
            errors.append(f"{url}: {repr(exc)}")
    raise RuntimeError(f"Yahoo chart history failed for {symbol}: {errors}")


def provenance_row(name, meta, df, acquired, series_id=""):
    return {
        "name": name,
        "series_id_or_symbol": series_id,
        "label": meta.get("label", ""),
        "source": meta.get("source", ""),
        "url": acquired["url"],
        "acquisition_method": acquired["acquisition_method"],
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": acquired["sha256"],
        "raw_bytes": acquired["raw_bytes"],
        "rows_total": int(len(df)),
        "rows_nonmissing": int(df["value"].notna().sum()),
        "first_date": str(df["date"].min().date()) if len(df) else "",
        "last_date": str(df["date"].max().date()) if len(df) else "",
        "raw_committed": False,
    }


def build_policy_registry(prov_rows):
    frames = {}
    for sid, label in POLICY_SERIES.items():
        df, acq = fetch_fred(sid)
        frames[sid] = df.dropna(subset=["value"]).copy()
        prov_rows.append(provenance_row(
            sid,
            {"label": label, "source": "Board of Governors of the Federal Reserve System via FRED"},
            frames[sid],
            acq,
            sid,
        ))

    pre = frames["DFEDTAR"].rename(columns={"value": "target"})
    low = frames["DFEDTARL"].rename(columns={"value": "lower"})
    up = frames["DFEDTARU"].rename(columns={"value": "upper"})
    rg = low.merge(up, on="date", how="inner")
    if ((rg["lower"] > rg["upper"]) & rg[["lower","upper"]].notna().all(axis=1)).any():
        raise RuntimeError("Target range lower bound exceeds upper bound")
    rg["target"] = (rg["lower"] + rg["upper"]) / 2.0

    cutoff = rg["date"].min()
    pre = pre[pre["date"] < cutoff][["date","target"]]
    post = rg[["date","target"]]
    pol = pd.concat([pre, post], ignore_index=True).dropna().sort_values("date")
    pol = pol.drop_duplicates("date", keep="last").reset_index(drop=True)

    # Keep actual source observations. Detect changes between successive observations.
    pol["target_before"] = pol["target"].shift(1)
    pol["change_bp"] = (pol["target"] - pol["target_before"]) * 100.0
    pol["change_bp"] = pol["change_bp"].where(pol["change_bp"].abs() >= 0.5, 0.0)
    changes = pol[pol["change_bp"] != 0].copy().reset_index(drop=True)
    changes["direction"] = np.where(changes["change_bp"] > 0, "HIKE", "CUT")
    return pol, changes


def parse_decision_date(text: str, year: int):
    # Examples: "January 30-31 Meeting - 1984", "Jul/Aug 31-1 Meeting - 2018"
    prefix = text.split(" Meeting", 1)[0].strip()
    m = re.match(r"([A-Za-z]+)(?:/([A-Za-z]+))?\s+(\d{1,2})(?:-(\d{1,2}))?$", prefix)
    if not m:
        return None
    mon1, mon2, d1, d2 = m.groups()
    month_text = mon2 or mon1
    day = int(d2 or d1)
    try:
        return pd.Timestamp(f"{month_text} {day}, {year}").normalize()
    except Exception:
        return None


def fetch_scheduled_meetings(prov_rows):
    dates = []
    audit = []
    for year in range(1982, 2021):
        url = f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm"
        try:
            raw = fetch_bytes(url, timeout=35)
            soup = BeautifulSoup(raw, "html.parser")
            found = []
            for tag in soup.find_all(["h3","h4","h5","h6"]):
                txt = " ".join(tag.stripped_strings)
                if f"Meeting - {year}" not in txt or "Conference Call" in txt:
                    continue
                dt = parse_decision_date(txt, year)
                if dt is not None:
                    found.append(dt)
            found = sorted(set(found))
            dates.extend(found)
            audit.append({
                "year": year, "url": url, "status": "OK" if found else "NO_MATCH",
                "scheduled_meetings": len(found),
                "sha256": hashlib.sha256(raw).hexdigest(),
            })
        except Exception as exc:
            audit.append({
                "year": year, "url": url, "status": f"ERROR:{type(exc).__name__}",
                "scheduled_meetings": 0, "sha256": "",
            })

    dates.extend(pd.to_datetime(RECENT_SCHEDULED_DECISIONS))
    dates = sorted(set(pd.Timestamp(x).normalize() for x in dates))
    audit.append({
        "year": "2021-2026",
        "url": "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
        "status": "EXPLICIT_RECENT_SUPPLEMENT",
        "scheduled_meetings": len(RECENT_SCHEDULED_DECISIONS),
        "sha256": "",
    })
    pd.DataFrame(audit).to_csv(OUT / "FOMC_MEETING_SOURCE_AUDIT.csv", index=False)
    return pd.DatetimeIndex(dates)


def nearest_scheduled_date(dt: pd.Timestamp, scheduled: pd.DatetimeIndex, tol_days=1):
    """Return nearest scheduled decision date within tolerance, else NaT."""
    if len(scheduled) == 0 or pd.isna(dt):
        return pd.NaT
    dt = pd.Timestamp(dt).normalize()
    diffs = np.abs((scheduled - dt).days)
    idx = int(np.argmin(diffs))
    return scheduled[idx] if int(diffs[idx]) <= tol_days else pd.NaT


def nearest_scheduled_flag(dt: pd.Timestamp, scheduled: pd.DatetimeIndex, tol_days=1):
    return not pd.isna(nearest_scheduled_date(dt, scheduled, tol_days))


def build_cycles(changes: pd.DataFrame, scheduled: pd.DatetimeIndex):
    changes = changes.copy().reset_index(drop=True)
    changes["source_effective_date"] = pd.to_datetime(changes["date"]).dt.normalize()

    mapped_dates = []
    bases = []
    scheduled_matches = []
    for dt in changes["source_effective_date"]:
        if dt >= pd.Timestamp("1994-02-04"):
            mapped = nearest_scheduled_date(dt, scheduled, tol_days=1)
            if not pd.isna(mapped):
                mapped_dates.append(mapped)
                bases.append("FOMC_SCHEDULED_DECISION_DATE")
                scheduled_matches.append(True)
            else:
                mapped_dates.append(dt)
                bases.append("TARGET_EFFECTIVE_DATE_UNSCHEDULED_CANDIDATE")
                scheduled_matches.append(False)
        else:
            mapped_dates.append(dt)
            bases.append("HISTORICAL_TARGET_RECONSTRUCTION")
            scheduled_matches.append(nearest_scheduled_flag(dt, scheduled))

    changes["event_date"] = pd.to_datetime(mapped_dates)
    changes["event_date_basis"] = bases
    changes["scheduled_decision_match"] = scheduled_matches
    changes["sign"] = np.sign(changes["change_bp"]).astype(int)
    changes["run_id"] = (changes["sign"] != changes["sign"].shift()).cumsum()

    cycle_rows = []
    event_rows = []
    cycle_no = 0

    positive_runs = []
    for run_id, g in changes.groupby("run_id"):
        if int(g["sign"].iloc[0]) != 1:
            continue
        cum_bp = float(g["change_bp"].sum())
        if len(g) < 2 or cum_bp < 50.0:
            continue
        positive_runs.append((run_id, g.copy(), cum_bp))

    for run_id, g, cum_bp in positive_runs:
        cycle_no += 1
        cycle_id = f"T{cycle_no:02d}_{g['source_effective_date'].iloc[0].year}"
        first = g.iloc[0]
        last = g.iloc[-1]
        later = changes[changes["source_effective_date"] > last["source_effective_date"]]
        next_cuts = later[later["change_bp"] < 0]
        first_cut = next_cuts.iloc[0] if len(next_cuts) else None

        last_event_date = pd.Timestamp(last["event_date"])
        first_cut_event_date = pd.Timestamp(first_cut["event_date"]) if first_cut is not None else pd.NaT
        pause_start = pd.NaT
        if first_cut is not None:
            candidates = scheduled[(scheduled > last_event_date) & (scheduled < first_cut_event_date)]
            if len(candidates):
                pause_start = candidates[0]

        cycle_rows.append({
            "cycle_id": cycle_id,
            "first_hike": first["event_date"],
            "last_hike": last["event_date"],
            "pause_start": pause_start,
            "first_cut": first_cut["event_date"] if first_cut is not None else pd.NaT,
            "first_hike_source_effective_date": first["source_effective_date"],
            "last_hike_source_effective_date": last["source_effective_date"],
            "first_cut_source_effective_date": first_cut["source_effective_date"] if first_cut is not None else pd.NaT,
            "n_hikes": int(len(g)),
            "cumulative_hike_bp": cum_bp,
            "target_before_first_hike": first["target_before"],
            "target_after_last_hike": last["target"],
            "complete_through_first_cut": bool(first_cut is not None),
        })

        def add_event(event_type, row=None, date=None, change_bp=np.nan):
            if row is not None:
                dt = pd.Timestamp(row["event_date"])
                src = pd.Timestamp(row["source_effective_date"])
                cbp = row["change_bp"]
                before = row["target_before"]
                after = row["target"]
                basis = row["event_date_basis"]
                sched_match = bool(row["scheduled_decision_match"])
            else:
                dt = pd.Timestamp(date) if not pd.isna(date) else pd.NaT
                src = pd.NaT
                cbp = change_bp
                before = np.nan
                after = np.nan
                basis = "FOMC_SCHEDULED_DECISION_DATE"
                sched_match = True
            if pd.isna(dt):
                return
            event_rows.append({
                "event_id": f"{cycle_id}_{event_type}",
                "cycle_id": cycle_id,
                "event_type": event_type,
                "event_date": dt,
                "source_effective_date": src,
                "event_date_basis": basis,
                "outcome_eligible": True,
                "target_before": before,
                "target_after": after,
                "change_bp": cbp,
                "scheduled_decision_match": sched_match,
                "cycle_start_year": int(first["source_effective_date"].year),
            })

        add_event("FIRST_HIKE", row=first)
        add_event("TIGHTENING_CYCLE_START", row=first)
        add_event("LAST_HIKE", row=last)
        add_event("TIGHTENING_CYCLE_END", row=last)
        if not pd.isna(pause_start):
            add_event("PAUSE_START", date=pause_start, change_bp=0.0)
        if first_cut is not None:
            add_event("FIRST_CUT", row=first_cut)

    # Easing legs are registry-only context unless they coincide with a primary FIRST_CUT.
    easing_no = 0
    for run_id, g in changes.groupby("run_id"):
        if int(g["sign"].iloc[0]) != -1:
            continue
        easing_no += 1
        e_id = f"E{easing_no:02d}_{g['source_effective_date'].iloc[0].year}"
        for etype, row in [("EASING_CYCLE_START", g.iloc[0]), ("EASING_CYCLE_END", g.iloc[-1])]:
            event_rows.append({
                "event_id": f"{e_id}_{etype}",
                "cycle_id": e_id,
                "event_type": etype,
                "event_date": row["event_date"],
                "source_effective_date": row["source_effective_date"],
                "event_date_basis": row["event_date_basis"],
                "outcome_eligible": False,
                "target_before": row["target_before"],
                "target_after": row["target"],
                "change_bp": row["change_bp"],
                "scheduled_decision_match": bool(row["scheduled_decision_match"]),
                "cycle_start_year": int(g["source_effective_date"].iloc[0].year),
            })

    # Modern unscheduled >=25bp cuts remain timing-unresolved candidates only.
    modern_cuts = changes[
        (changes["source_effective_date"] >= pd.Timestamp("1994-02-04"))
        & (changes["change_bp"] <= -25.0)
        & (~changes["scheduled_decision_match"])
    ]
    for _, row in modern_cuts.iterrows():
        event_rows.append({
            "event_id": f"EMERGENCY_CANDIDATE_{row['source_effective_date'].date()}",
            "cycle_id": "",
            "event_type": "EMERGENCY_CUT_CANDIDATE",
            "event_date": row["source_effective_date"],
            "source_effective_date": row["source_effective_date"],
            "event_date_basis": "UNSCHEDULED_EFFECTIVE_DATE_TIMING_UNRESOLVED",
            "outcome_eligible": False,
            "target_before": row["target_before"],
            "target_after": row["target"],
            "change_bp": row["change_bp"],
            "scheduled_decision_match": False,
            "cycle_start_year": int(row["source_effective_date"].year),
        })

    cycles = pd.DataFrame(cycle_rows).sort_values("first_hike").reset_index(drop=True)
    events = pd.DataFrame(event_rows).sort_values(["event_date","event_type"]).reset_index(drop=True)
    return cycles, events, changes


def load_assets(prov_rows):
    assets = {}

    for name, meta in YAHOO_ASSETS.items():
        df, acq = fetch_yahoo_chart(meta["symbol"])
        df = df[(df["value"] > 0) & df["date"].notna()].copy()
        assets[name] = {"df": df.reset_index(drop=True), **meta}
        prov_rows.append(provenance_row(name, meta, df, acq, meta["symbol"]))

    for name, meta in FRED_ASSETS.items():
        df, acq = fetch_fred(meta["id"])
        df = df.dropna(subset=["value"]).copy()
        if meta["kind"] == "price":
            df = df[df["value"] > 0]
        assets[name] = {"df": df.reset_index(drop=True), **meta}
        prov_rows.append(provenance_row(name, meta, df, acq, meta["id"]))

    return assets


def price_metrics(df, event_date):
    df = df.dropna(subset=["date","value"]).sort_values("date").reset_index(drop=True)
    dates = df["date"].to_numpy(dtype="datetime64[ns]")
    e = np.datetime64(pd.Timestamp(event_date))
    first_post = int(np.searchsorted(dates, e, side="left"))
    b = first_post - 1
    if b < 1 or first_post >= len(df):
        return None

    baseline = float(df.loc[b, "value"])
    post = df.iloc[first_post:min(first_post + MAX_PATH, len(df))].copy()
    if len(post) == 0:
        return None

    row = {
        "baseline_date": df.loc[b, "date"],
        "baseline_value": baseline,
        "first_post_date": post["date"].iloc[0],
        "usable_post_obs_252": int(len(post)),
    }

    for h in ENDPOINTS:
        row[f"ret_{h}d"] = (
            float(post["value"].iloc[h-1] / baseline - 1.0)
            if len(post) >= h else np.nan
        )

    vals = np.concatenate([[baseline], post["value"].to_numpy(float)])
    event_ret = vals / baseline - 1.0
    row["mae"] = float(np.min(event_ret))
    row["mfe"] = float(np.max(event_ret))
    row["time_to_event_min_obs"] = int(np.argmin(event_ret))
    row["time_to_event_max_obs"] = int(np.argmax(event_ret))

    running_peak = np.maximum.accumulate(vals)
    dd = 1.0 - vals / running_peak
    trough_rel = int(np.argmax(dd))
    mdd = float(dd[trough_rel])
    peak_rel = int(np.argmax(vals[:trough_rel+1]))
    row["mdd"] = mdd
    row["mdd_peak_obs"] = peak_rel
    row["mdd_trough_obs"] = trough_rel
    row["time_peak_to_trough_obs"] = trough_rel - peak_rel

    # Recovery from MDD trough using up to 756 valid observations after trough.
    row["recovery50_obs_from_trough"] = np.nan
    row["recovery100_obs_from_trough"] = np.nan
    row["recovery50_obs_from_event"] = np.nan
    row["recovery100_obs_from_event"] = np.nan
    row["recovery50_observed"] = False
    row["recovery100_observed"] = False
    row["recovery_censor_obs"] = np.nan

    if mdd > 1e-12:
        peak_price = vals[peak_rel]
        trough_price = vals[trough_rel]
        threshold50 = trough_price + 0.5 * (peak_price - trough_price)
        threshold100 = peak_price
        trough_global = b + trough_rel
        search_end = min(trough_global + RECOVERY_HORIZON, len(df)-1)
        rec = df.iloc[trough_global:search_end+1]["value"].to_numpy(float)
        row["recovery_censor_obs"] = int(len(rec)-1)

        hit50 = np.where(rec >= threshold50)[0]
        hit100 = np.where(rec >= threshold100)[0]
        if len(hit50):
            row["recovery50_obs_from_trough"] = int(hit50[0])
            row["recovery50_obs_from_event"] = int(trough_rel + hit50[0])
            row["recovery50_observed"] = True
        if len(hit100):
            row["recovery100_obs_from_trough"] = int(hit100[0])
            row["recovery100_obs_from_event"] = int(trough_rel + hit100[0])
            row["recovery100_observed"] = True

    # Volatility and downside semivolatility.
    returns = np.diff(np.log(vals))
    pre_start = max(0, b - 252)
    pre_vals = df.iloc[pre_start:b+1]["value"].to_numpy(float)
    pre_rets = np.diff(np.log(pre_vals))
    tail_cut = np.quantile(pre_rets, 0.05) if len(pre_rets) >= 126 else np.nan

    for h in VOL_ENDPOINTS:
        if len(returns) >= h:
            rr = returns[:h]
            row[f"rv_{h}d_ann"] = float(np.std(rr, ddof=1) * math.sqrt(252))
            row[f"down_semivol_{h}d_ann"] = float(
                math.sqrt(252 * np.mean(np.minimum(rr, 0.0) ** 2))
            )
            row[f"tail_loss_freq_{h}d"] = (
                float(np.mean(rr < tail_cut)) if np.isfinite(tail_cut) else np.nan
            )
        else:
            row[f"rv_{h}d_ann"] = np.nan
            row[f"down_semivol_{h}d_ann"] = np.nan
            row[f"tail_loss_freq_{h}d"] = np.nan

    return row


def rate_metrics(df, event_date):
    df = df.dropna(subset=["date","value"]).sort_values("date").reset_index(drop=True)
    dates = df["date"].to_numpy(dtype="datetime64[ns]")
    e = np.datetime64(pd.Timestamp(event_date))
    first_post = int(np.searchsorted(dates, e, side="left"))
    b = first_post - 1
    if b < 1 or first_post >= len(df):
        return None

    baseline = float(df.loc[b, "value"])
    post = df.iloc[first_post:min(first_post + MAX_PATH, len(df))].copy()
    if len(post) == 0:
        return None
    changes_bp = (post["value"].to_numpy(float) - baseline) * 100.0

    row = {
        "baseline_date": df.loc[b, "date"],
        "baseline_value": baseline,
        "first_post_date": post["date"].iloc[0],
        "usable_post_obs_252": int(len(post)),
        "min_bp_excursion": float(np.min(changes_bp)),
        "max_bp_excursion": float(np.max(changes_bp)),
        "time_to_min_obs": int(np.argmin(changes_bp) + 1),
        "time_to_max_obs": int(np.argmax(changes_bp) + 1),
    }
    for h in ENDPOINTS:
        row[f"chg_{h}d_bp"] = float(changes_bp[h-1]) if len(changes_bp) >= h else np.nan

    vals = np.concatenate([[baseline], post["value"].to_numpy(float)])
    daily_bp = np.diff(vals) * 100.0
    for h in VOL_ENDPOINTS:
        row[f"bp_vol_{h}d_ann"] = (
            float(np.std(daily_bp[:h], ddof=1) * math.sqrt(252))
            if len(daily_bp) >= h else np.nan
        )
    return row


def build_event_metrics(events, assets):
    rows = []
    for _, ev in events.iterrows():
        for asset, obj in assets.items():
            if obj["kind"] == "price":
                m = price_metrics(obj["df"], ev["event_date"])
            else:
                m = rate_metrics(obj["df"], ev["event_date"])
            if m is None:
                continue
            rows.append({
                "event_id": ev["event_id"],
                "cycle_id": ev["cycle_id"],
                "cycle_start_year": ev["cycle_start_year"],
                "event_type": ev["event_type"],
                "event_date": ev["event_date"],
                "asset": asset,
                "asset_kind": obj["kind"],
                **m,
            })
    return pd.DataFrame(rows)


def build_gold_paths(events, gold_df):
    rows = []
    g = gold_df.sort_values("date").reset_index(drop=True)
    dates = g["date"].to_numpy(dtype="datetime64[ns]")
    for _, ev in events.iterrows():
        e = np.datetime64(pd.Timestamp(ev["event_date"]))
        first_post = int(np.searchsorted(dates, e, side="left"))
        b = first_post - 1
        if b < 60 or first_post >= len(g):
            continue
        baseline = float(g.loc[b, "value"])
        start = max(0, b - 60)
        end = min(len(g)-1, b + MAX_PATH)
        s = g.iloc[start:end+1]
        for idx, r in s.iterrows():
            event_time = int(idx - b)
            rows.append({
                "event_id": ev["event_id"],
                "cycle_id": ev["cycle_id"],
                "cycle_start_year": ev["cycle_start_year"],
                "event_type": ev["event_type"],
                "event_date": ev["event_date"],
                "event_time_obs": event_time,
                "date": r["date"],
                "normalized_price": float(r["value"] / baseline),
                "cum_return": float(r["value"] / baseline - 1.0),
            })
    return pd.DataFrame(rows)


def distribution_summary(metrics):
    rows = []
    price = metrics[metrics["asset_kind"] == "price"].copy()
    fields = ["ret_20d","ret_60d","ret_120d","ret_252d","mdd","mae","mfe",
              "time_to_event_min_obs","recovery50_obs_from_trough","recovery100_obs_from_trough",
              "rv_60d_ann","down_semivol_60d_ann"]
    for (asset, etype), g in price.groupby(["asset","event_type"]):
        for f in fields:
            if f not in g:
                continue
            x = pd.to_numeric(g[f], errors="coerce").dropna()
            if len(x) == 0:
                continue
            rows.append({
                "asset": asset,
                "event_type": etype,
                "metric": f,
                "n": int(len(x)),
                "mean": float(x.mean()),
                "median": float(x.median()),
                "q25": float(x.quantile(0.25)),
                "q75": float(x.quantile(0.75)),
                "min": float(x.min()),
                "max": float(x.max()),
            })
    return pd.DataFrame(rows)


def km_curve(durations, observed):
    d = pd.DataFrame({"t": durations, "obs": observed}).dropna()
    if len(d) == 0:
        return pd.DataFrame(columns=["time_obs","at_risk","events","censored","survival"])
    d["t"] = d["t"].astype(int)
    d["obs"] = d["obs"].astype(bool)
    surv = 1.0
    rows = [{"time_obs": 0, "at_risk": int(len(d)), "events": 0, "censored": 0, "survival": 1.0}]
    for t in sorted(d["t"].unique()):
        at_risk = int((d["t"] >= t).sum())
        n_event = int(((d["t"] == t) & d["obs"]).sum())
        n_cens = int(((d["t"] == t) & ~d["obs"]).sum())
        if at_risk > 0 and n_event > 0:
            surv *= (1.0 - n_event / at_risk)
        rows.append({
            "time_obs": int(t),
            "at_risk": at_risk,
            "events": n_event,
            "censored": n_cens,
            "survival": float(surv),
        })
    return pd.DataFrame(rows)


def build_gold_km(metrics):
    gm = metrics[(metrics["asset"] == "GOLD") & (metrics["asset_kind"] == "price")].copy()
    outs = []
    for etype in ["FIRST_HIKE","LAST_HIKE","FIRST_CUT"]:
        g = gm[gm["event_type"] == etype].copy()
        if len(g) == 0:
            continue
        # For no MDD/recovery N/A rows, omit from recovery-risk set.
        g = g[g["mdd"].fillna(0) > 0].copy()
        if len(g) == 0:
            continue
        duration = np.where(
            g["recovery100_observed"].astype(bool),
            g["recovery100_obs_from_trough"],
            g["recovery_censor_obs"],
        )
        km = km_curve(duration, g["recovery100_observed"])
        km["asset"] = "GOLD"
        km["event_type"] = etype
        km["recovery_level"] = "100%"
        outs.append(km)
    return pd.concat(outs, ignore_index=True) if outs else pd.DataFrame()


def make_figures(metrics, gold_paths, km):
    # Gold FIRST_HIKE full paths.
    p = gold_paths[gold_paths["event_type"] == "FIRST_HIKE"].copy()
    if len(p):
        fig, ax = plt.subplots(figsize=(11, 6))
        for (cy, yr), g in p.groupby(["cycle_id","cycle_start_year"]):
            g = g[(g["event_time_obs"] >= -60) & (g["event_time_obs"] <= 252)]
            ax.plot(g["event_time_obs"], g["cum_return"] * 100, alpha=0.55, linewidth=1.1, label=str(yr))
        ax.axvline(0, linewidth=0.8)
        ax.axhline(0, linewidth=0.8)
        ax.set_title("Gold path around FIRST_HIKE across qualifying tightening cycles")
        ax.set_xlabel("Valid Gold observations relative to pre-event baseline")
        ax.set_ylabel("Cumulative return from pre-event baseline (%)")
        if p["cycle_start_year"].nunique() <= 12:
            ax.legend(ncol=2, fontsize=8)
        fig.tight_layout()
        fig.savefig(OUT / "01_gold_first_hike_paths.png", dpi=170, bbox_inches="tight")
        plt.close(fig)

    # 2015 vs 2022, exactly same frozen window.
    q = p[p["cycle_start_year"].isin([2015, 2022])].copy()
    if len(q):
        fig, ax = plt.subplots(figsize=(10.5, 5.8))
        for yr, g in q.groupby("cycle_start_year"):
            g = g[(g["event_time_obs"] >= -60) & (g["event_time_obs"] <= 252)]
            ax.plot(g["event_time_obs"], g["cum_return"] * 100, linewidth=2.0, label=str(yr))
        ax.axvline(0, linewidth=0.8)
        ax.axhline(0, linewidth=0.8)
        ax.set_title("Gold: 2015 vs 2022 FIRST_HIKE under one frozen window")
        ax.set_xlabel("Valid Gold observations relative to pre-event baseline")
        ax.set_ylabel("Cumulative return (%)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT / "02_gold_2015_2022_first_hike.png", dpi=170, bbox_inches="tight")
        plt.close(fig)

    gm = metrics[(metrics["asset"] == "GOLD") & (metrics["event_type"] == "FIRST_HIKE")].copy()
    if len(gm):
        gm = gm.sort_values("cycle_start_year")
        fig, ax = plt.subplots(figsize=(10.5, 5.5))
        ax.bar(gm["cycle_start_year"].astype(str), gm["mdd"] * 100)
        ax.set_title("Gold maximum drawdown in first 252 observations after FIRST_HIKE")
        ax.set_xlabel("Tightening-cycle start year")
        ax.set_ylabel("Maximum drawdown (%)")
        fig.tight_layout()
        fig.savefig(OUT / "03_gold_first_hike_mdd_by_cycle.png", dpi=170, bbox_inches="tight")
        plt.close(fig)

    kk = km[(km["asset"] == "GOLD") & (km["event_type"] == "FIRST_HIKE")].copy() if len(km) else pd.DataFrame()
    if len(kk):
        fig, ax = plt.subplots(figsize=(8.8, 5.2))
        ax.step(kk["time_obs"], kk["survival"], where="post")
        ax.set_ylim(0, 1.02)
        ax.set_title("Gold 100% recovery survival after FIRST_HIKE MDD trough")
        ax.set_xlabel("Valid Gold observations after MDD trough")
        ax.set_ylabel("Share not yet fully recovered")
        fig.tight_layout()
        fig.savefig(OUT / "04_gold_first_hike_recovery_km.png", dpi=170, bbox_inches="tight")
        plt.close(fig)


def build_gold_key_table(metrics):
    cols = [
        "cycle_id","cycle_start_year","event_type","event_date",
        "ret_20d","ret_60d","ret_120d","ret_252d","mdd","mae","mfe",
        "time_to_event_min_obs","time_to_event_max_obs",
        "recovery50_obs_from_trough","recovery50_observed",
        "recovery100_obs_from_trough","recovery100_observed",
        "rv_60d_ann","down_semivol_60d_ann",
    ]
    g = metrics[(metrics["asset"] == "GOLD") &
                (metrics["cycle_start_year"].isin([2015, 2022])) &
                (metrics["event_type"].isin(["FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"]))].copy()
    return g[[c for c in cols if c in g.columns]].sort_values(["cycle_start_year","event_date","event_type"])


def write_report(cycles, events, metrics, summary, key_gold, qc, coverage):
    gm = metrics[(metrics["asset"] == "GOLD") & (metrics["event_type"] == "FIRST_HIKE")].copy()
    lines = [
        "# FED-CYCLE-PATH-001 v1.1 — Timing-Corrected Long-History Descriptive Foundation",
        f"Generated: {datetime.now(timezone.utc).date()}",
        "",
        "## Evidence status",
        "",
        "**DESCRIPTIVE RESULT / REALIZED POLICY ACTION IS NOT AN IDENTIFIED MONETARY-POLICY SHOCK / NOT A FORECASTING MODEL / NOT DEPLOYABLE**",
        "",
        "This run follows research/FED_CYCLE_PATH_001_LOCK.md plus research/FED_CYCLE_PATH_001_V1_1_TIMING_LOCK.md. v1 is quarantined; v1.1 corrects timing ontology without changing horizons or path-risk definitions.",
        "",
        "## Policy-cycle QC",
        "",
        f"- Qualifying tightening cycles: {len(cycles)}",
        f"- Cycle start years: {', '.join(str(x) for x in cycles['first_hike'].dt.year.tolist())}",
        f"- Total event-registry rows: {len(events)}",
        f"- Timing-unresolved emergency-cut candidates (registry only): {int((events['event_type'] == 'EMERGENCY_CUT_CANDIDATE').sum())}",
        f"- QC gate: {qc['qc_gate']}",
        "",
        "## Asset coverage",
        "",
        coverage.to_markdown(index=False),
        "",
        "## Gold — FIRST_HIKE distribution",
        "",
    ]
    if len(gm):
        for field, label, pct in [
            ("ret_20d","20D endpoint return", True),
            ("ret_60d","60D endpoint return", True),
            ("ret_120d","120D endpoint return", True),
            ("ret_252d","252D endpoint return", True),
            ("mdd","252-observation maximum drawdown", True),
            ("time_to_event_min_obs","time to event-relative trough (obs)", False),
            ("recovery50_obs_from_trough","50% recovery from MDD trough (obs)", False),
            ("recovery100_obs_from_trough","100% recovery from MDD trough (obs)", False),
        ]:
            x = pd.to_numeric(gm[field], errors="coerce").dropna()
            if len(x):
                mult = 100 if pct else 1
                unit = "%" if pct else ""
                lines.append(
                    f"- {label}: n={len(x)}, median={x.median()*mult:.2f}{unit}, "
                    f"IQR=[{x.quantile(.25)*mult:.2f}, {x.quantile(.75)*mult:.2f}]{unit}"
                )
        cens = int((~gm["recovery100_observed"].fillna(False).astype(bool) & (gm["mdd"].fillna(0) > 0)).sum())
        lines.append(f"- Full-recovery right-censored observations: {cens}")
    else:
        lines.append("- No usable Gold FIRST_HIKE observations.")

    lines.extend([
        "",
        "## Gold — 2015 and 2022 inside the same frozen framework",
        "",
        key_gold.to_markdown(index=False) if len(key_gold) else "No key-cycle rows available.",
        "",
        "These two episodes are highlighted for interpretation only; they were not given different windows or thresholds.",
        "",
        "## Distribution table",
        "",
        summary[summary["asset"].isin(["GOLD","SP500","NASDAQ"])].head(120).to_markdown(index=False)
        if len(summary) else "No distribution summary available.",
        "",
        "## Interpretation boundary",
        "",
        "- DATA FACT: the cycle registry is mechanically derived from target-rate changes plus scheduled-meeting dates.",
        "- DESCRIPTIVE RESULT: asset paths, drawdowns, volatility and recovery are historical distributions around those markers.",
        "- NOT CAUSAL: this module does not identify target/path/information monetary shocks.",
        "- FDR: no confirmatory p-value family is executed in this foundation run; future confirmatory families are predeclared in the lock.",
        "- OOS: not applicable to this descriptive foundation; no forecasting claim is made.",
        "- Investment implication: use the output as a risk-distribution and timing map, not as a deterministic trade rule.",
    ])
    (OUT / "FED_CYCLE_PATH_001_V1_1_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    prov_rows = []

    policy, changes = build_policy_registry(prov_rows)
    scheduled = fetch_scheduled_meetings(prov_rows)
    cycles, events, mapped_changes = build_cycles(changes, scheduled)

    # v1.1 outcome-eligible set deliberately excludes timing-unresolved emergencies.
    primary_types = {
        "FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT",
        "TIGHTENING_CYCLE_START","TIGHTENING_CYCLE_END",
    }
    outcome_events = events[
        events["event_type"].isin(primary_types) & events["outcome_eligible"].astype(bool)
    ].copy()

    assets = load_assets(prov_rows)
    metrics = build_event_metrics(outcome_events, assets)
    gold_paths = build_gold_paths(outcome_events, assets["GOLD"]["df"])
    summary = distribution_summary(metrics)
    km = build_gold_km(metrics)
    key_gold = build_gold_key_table(metrics)

    coverage_rows = []
    for name, obj in assets.items():
        df = obj["df"]
        coverage_rows.append({
            "asset": name,
            "kind": obj["kind"],
            "first_date": str(df["date"].min().date()),
            "last_date": str(df["date"].max().date()),
            "rows": int(len(df)),
            "usable_event_rows": int((metrics["asset"] == name).sum()) if len(metrics) else 0,
            "source": obj["source"],
        })
    coverage = pd.DataFrame(coverage_rows)

    # Computational QC.
    duplicate_policy = int(policy["date"].duplicated().sum())
    mdd_bad = int(((metrics.get("mdd", pd.Series(dtype=float)).dropna() < -1e-12)).sum()) if len(metrics) else 0
    recovery_order_bad = 0
    if len(metrics) and "recovery50_obs_from_trough" in metrics:
        z = metrics.dropna(subset=["recovery50_obs_from_trough","recovery100_obs_from_trough"])
        recovery_order_bad = int((z["recovery100_obs_from_trough"] < z["recovery50_obs_from_trough"]).sum())

    gold_first = metrics[(metrics["asset"] == "GOLD") & (metrics["event_type"] == "FIRST_HIKE")] if len(metrics) else pd.DataFrame()
    sp_first = metrics[(metrics["asset"] == "SP500") & (metrics["event_type"] == "FIRST_HIKE")] if len(metrics) else pd.DataFrame()

    # Timing-ontology QC.
    cyc22 = cycles[cycles["first_hike"].dt.year == 2022]
    modern_anchor_ok = False
    if len(cyc22) == 1:
        rr = cyc22.iloc[0]
        modern_anchor_ok = (
            pd.Timestamp(rr["first_hike"]) == pd.Timestamp("2022-03-16")
            and pd.Timestamp(rr["last_hike"]) == pd.Timestamp("2023-07-26")
            and pd.Timestamp(rr["first_cut"]) == pd.Timestamp("2024-09-18")
        )

    pre1994_emergency_labels = int(
        ((events["event_date"] < pd.Timestamp("1994-01-01"))
         & events["event_type"].isin(["EMERGENCY_CUT","EMERGENCY_CUT_CANDIDATE"])).sum()
    )
    emergency_2025_candidates = int(
        ((events["event_date"].dt.year == 2025)
         & (events["event_type"] == "EMERGENCY_CUT_CANDIDATE")).sum()
    )
    emergency_metrics = int(metrics["event_type"].astype(str).str.contains("EMERGENCY", na=False).sum()) if len(metrics) else 0
    schedule_2025_required = {
        pd.Timestamp("2025-09-17"),
        pd.Timestamp("2025-10-29"),
        pd.Timestamp("2025-12-10"),
    }
    schedule_2025_ok = schedule_2025_required.issubset(set(pd.Timestamp(x) for x in scheduled))

    hard_fail = (
        duplicate_policy != 0
        or len(cycles) < 4
        or len(gold_first) < 3
        or len(sp_first) < 4
        or mdd_bad != 0
        or recovery_order_bad != 0
        or not modern_anchor_ok
        or pre1994_emergency_labels != 0
        or emergency_2025_candidates != 0
        or emergency_metrics != 0
        or not schedule_2025_ok
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "version": "FED-CYCLE-PATH-001-v1.1",
        "v1_status": "QUARANTINED_TIMING_ONTOLOGY_BUG",
        "policy_rows": int(len(policy)),
        "policy_change_rows": int(len(changes)),
        "duplicate_policy_dates": duplicate_policy,
        "scheduled_meeting_dates": int(len(scheduled)),
        "qualifying_tightening_legs": int(len(cycles)),
        "cycle_start_years": [int(x) for x in cycles["first_hike"].dt.year.tolist()],
        "outcome_event_rows": int(len(outcome_events)),
        "asset_metric_rows": int(len(metrics)),
        "gold_first_hike_rows": int(len(gold_first)),
        "gold_daily_proxy": "GC=F_COMEX_CONTINUOUS_FUTURES_NOT_SPOT",
        "sp500_first_hike_rows": int(len(sp_first)),
        "mdd_identity_violations": mdd_bad,
        "recovery_order_violations": recovery_order_bad,
        "modern_anchor_assertions_pass": bool(modern_anchor_ok),
        "pre1994_emergency_labels": pre1994_emergency_labels,
        "emergency_2025_candidates": emergency_2025_candidates,
        "emergency_rows_in_asset_metrics": emergency_metrics,
        "schedule_2025_required_dates_present": bool(schedule_2025_ok),
        "timing_unresolved_emergency_candidates_registry_only": int((events["event_type"] == "EMERGENCY_CUT_CANDIDATE").sum()),
        "raw_redistribution_uncertain_market_files_committed": False,
        "soft_warning": "Pre-1994 anchors are historical target reconstructions; Gold daily layer is GC=F futures proxy with only three FIRST_HIKE tightening legs.",
    }

    # Public-safe outputs.
    pd.DataFrame(prov_rows).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    mapped_changes[[
        "source_effective_date","event_date","event_date_basis",
        "target_before","target","change_bp","direction","scheduled_decision_match"
    ]].to_csv(OUT / "FED_POLICY_CHANGE_REGISTRY.csv", index=False)
    cycles.to_csv(OUT / "FED_TIGHTENING_CYCLES.csv", index=False)
    events.to_csv(OUT / "FED_CYCLE_EVENTS.csv", index=False)
    coverage.to_csv(OUT / "ASSET_COVERAGE.csv", index=False)
    metrics.to_csv(OUT / "EVENT_ASSET_METRICS.csv", index=False)
    summary.to_csv(OUT / "DISTRIBUTION_SUMMARY.csv", index=False)
    gold_paths.to_csv(OUT / "GOLD_EVENT_PATHS.csv", index=False)
    km.to_csv(OUT / "GOLD_RECOVERY_KM.csv", index=False)
    key_gold.to_csv(OUT / "GOLD_2015_2022_METRICS.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    make_figures(metrics, gold_paths, km)
    write_report(cycles, events, metrics, summary, key_gold, qc, coverage)

    if hard_fail:
        raise SystemExit("FED-CYCLE-PATH-001 v1.1 QC gate failed")

    print(json.dumps({
        "qc_gate": qc["qc_gate"],
        "qualifying_tightening_legs": qc["qualifying_tightening_legs"],
        "cycle_start_years": qc["cycle_start_years"],
        "gold_first_hike_rows": qc["gold_first_hike_rows"],
        "sp500_first_hike_rows": qc["sp500_first_hike_rows"],
        "modern_anchor_assertions_pass": qc["modern_anchor_assertions_pass"],
        "timing_unresolved_emergency_candidates_registry_only": qc["timing_unresolved_emergency_candidates_registry_only"],
    }, indent=2))


if __name__ == "__main__":
    main()
