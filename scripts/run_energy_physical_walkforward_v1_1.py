#!/usr/bin/env python3
"""
ENERGY-PHYSICAL-WF-001 v1.1
Release-aware physical confirmation extension.

Follows:
- research/ENERGY_PHYSICAL_WALKFORWARD_V1_LOCK.md
- research/ENERGY_PHYSICAL_WF_001_V1_1_TIMING_AMENDMENT.md

This script does not alter the frozen price-event set.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import time
from datetime import datetime, timezone, date, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from scipy.stats import mannwhitneyu

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "energy_physical_wf_v1_1"
OUT.mkdir(parents=True, exist_ok=True)

PRICE_EVENTS = ROOT / "results" / "energy_price_wf_v1" / "EVENTS.csv"

EIA_SERIES = {
    "CRUDE": {
        "id": "WCESTUS1",
        "title": "Weekly U.S. Ending Stocks excluding SPR of Crude Oil",
        "unit": "Thousand Barrels",
    },
    "GASOLINE": {
        "id": "WGTSTUS1",
        "title": "Weekly U.S. Ending Stocks of Total Motor Gasoline",
        "unit": "Thousand Barrels",
    },
    "DISTILLATE": {
        "id": "WDISTUS1",
        "title": "Weekly U.S. Ending Stocks of Distillate Fuel Oil",
        "unit": "Thousand Barrels",
    },
    "REFINERY_UTIL": {
        "id": "WPULEUS3",
        "title": "Weekly U.S. Percent Utilization of Refinery Operable Capacity",
        "unit": "Percent",
    },
}

TWIP_URL = "https://www.eia.gov/petroleum/weekly/"
WPSR_SCHEDULE_URL = "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
WTI_DAILY_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILWTICO"

MONTHS = {
    "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
    "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
}

def get_bytes(url, timeout=45, attempts=3):
    last = None
    for i in range(attempts):
        try:
            req = Request(url, headers={
                "User-Agent":"Mozilla/5.0 gss-cb-001-public-research/1.0",
                "Accept":"*/*",
            })
            with urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last = exc
            time.sleep(2*(i+1))
    raise RuntimeError(f"failed to fetch {url}: {last!r}")

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def parse_eia_xls(series_id):
    url = f"https://www.eia.gov/dnav/pet/hist_xls/{series_id}w.xls"
    raw = get_bytes(url, timeout=60)
    book = pd.ExcelFile(io.BytesIO(raw), engine="xlrd")
    parsed = None

    for sheet in book.sheet_names:
        x = pd.read_excel(io.BytesIO(raw), sheet_name=sheet, header=None, engine="xlrd")
        for ridx in range(min(20, len(x))):
            vals = [str(v).strip() if pd.notna(v) else "" for v in x.iloc[ridx].tolist()]
            if "Date" in vals:
                dcol = vals.index("Date")
                # Pick first non-empty column to the right of Date.
                vcol = None
                for j in range(dcol+1, len(vals)):
                    if vals[j] not in ("", "nan", "NaN"):
                        vcol = j
                        break
                if vcol is None:
                    vcol = dcol+1
                z = x.iloc[ridx+1:, [dcol, vcol]].copy()
                z.columns = ["week_end", "value"]
                z["week_end"] = pd.to_datetime(z["week_end"], errors="coerce")
                z["value"] = pd.to_numeric(z["value"], errors="coerce")
                z = z.dropna(subset=["week_end","value"]).sort_values("week_end")
                if len(z) > 100:
                    parsed = z.reset_index(drop=True)
                    break
        if parsed is not None:
            break

    if parsed is None:
        raise RuntimeError(f"could not parse EIA xls for {series_id}")

    meta = {
        "series_id":series_id,
        "download_url":url,
        "sha256":sha256(raw),
        "rows":int(len(parsed)),
        "first_date":str(parsed.week_end.min().date()),
        "last_date":str(parsed.week_end.max().date()),
        "retrieved_utc":datetime.now(timezone.utc).isoformat(),
        "acquisition_method":"EIA_HIST_XLS",
    }
    return parsed, meta

def parse_md(mmdd, year):
    s = str(mmdd).strip()
    if not s or s.upper() in {"NA","N/A","--"}:
        return None
    if "/" in s:
        m,d = [int(v) for v in s.split("/")[:2]]
        y = year
        # A January release can point to a December week-end.
        if m == 12:
            y = year-1
        return pd.Timestamp(y,m,d)
    return None

def build_twip_release_registry():
    raw = get_bytes(TWIP_URL, timeout=60)
    soup = BeautifulSoup(raw, "html.parser")
    rows = []

    for head in soup.find_all(["h1","h2","h3","h4"]):
        txt = head.get_text(" ", strip=True)
        if not re.fullmatch(r"20\d{2}", txt):
            continue
        year = int(txt)
        if not (2002 <= year <= 2025):
            continue
        table = head.find_next("table")
        if table is None:
            continue
        current_month = None
        for tr in table.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th","td"])]
            if len(cells) < 2:
                continue
            # Header.
            if any("Release date" in c for c in cells):
                continue

            rel_month = None
            rel_day = None
            week_end_text = None

            if cells[0] in MONTHS and len(cells) >= 3:
                current_month = MONTHS[cells[0]]
                rel_month = current_month
                rel_day = cells[1]
                week_end_text = cells[2]
            elif current_month is not None and len(cells) >= 2:
                rel_month = current_month
                rel_day = cells[0]
                week_end_text = cells[1]
            else:
                continue

            try:
                rel_day_i = int(re.findall(r"\d+", str(rel_day))[0])
            except Exception:
                continue

            try:
                release_date = pd.Timestamp(year, rel_month, rel_day_i)
            except Exception:
                continue

            wtxt = str(week_end_text).strip()
            if not wtxt or wtxt.upper() in {"NA","N/A","--"}:
                continue
            if "/" in wtxt:
                parts = re.findall(r"\d+", wtxt)
                if len(parts) < 2:
                    continue
                wm, wd = int(parts[0]), int(parts[1])
                wy = year - 1 if (rel_month == 1 and wm == 12) else year
            else:
                parts = re.findall(r"\d+", wtxt)
                if not parts:
                    continue
                wd = int(parts[0])
                wm = rel_month
                wy = year
                # Most WPSR week ending dates are preceding Friday; if release month
                # rolled from prior month, infer from calendar.
                candidate = release_date - pd.Timedelta(days=(release_date.weekday()-4) % 7 + 5)
                # Fallback to previous Friday based on day token.
                for delta_m in [0,-1]:
                    try:
                        cm = release_date + pd.DateOffset(months=delta_m)
                        cand = pd.Timestamp(cm.year, cm.month, wd)
                        if 3 <= (release_date-cand).days <= 10:
                            wm, wy = cand.month, cand.year
                            break
                    except Exception:
                        pass
            try:
                week_end = pd.Timestamp(wy, wm, wd)
            except Exception:
                continue

            rows.append({
                "week_end":week_end,
                "release_date":release_date,
                "release_method":"EIA_TWIP_ARCHIVE_EXPLICIT",
                "source_url":TWIP_URL,
            })

    out = pd.DataFrame(rows).drop_duplicates(["week_end"], keep="last")
    out = out.sort_values("week_end").reset_index(drop=True)
    return out, {
        "source_url":TWIP_URL,
        "sha256":sha256(raw),
        "rows":int(len(out)),
        "first_week_end":str(out.week_end.min().date()) if len(out) else None,
        "last_week_end":str(out.week_end.max().date()) if len(out) else None,
        "retrieved_utc":datetime.now(timezone.utc).isoformat(),
    }

def build_2026_release_registry(weekly_dates):
    """
    For 2026, use the official current EIA rule:
    standard Wednesday release, with published holiday exceptions.
    Only dates required by the frozen 2026 event window are admitted here.
    There are no listed June/July/August exceptions affecting the needed
    June-19 through July-31 week-end observations.
    """
    rows = []
    needed_start = pd.Timestamp("2026-06-01")
    needed_end = pd.Timestamp("2026-08-31")
    for we in pd.Series(weekly_dates):
        we = pd.Timestamp(we)
        if not (needed_start <= we <= needed_end):
            continue
        # Standard: following Wednesday = +5 days from Friday.
        # If dates are not Friday, move to next Wednesday.
        days = (2 - we.weekday()) % 7
        if days == 0:
            days = 7
        rd = we + pd.Timedelta(days=days)
        rows.append({
            "week_end":we,
            "release_date":rd,
            "release_method":"EIA_2026_STANDARD_SCHEDULE_NO_RELEVANT_EXCEPTION",
            "source_url":WPSR_SCHEDULE_URL,
        })
    return pd.DataFrame(rows)

def seasonal_contrib(df, asof_date, value_col="value"):
    d = pd.Timestamp(asof_date)
    target_week = int(d.isocalendar().week)
    vals=[]
    for y in range(d.year-5, d.year):
        z=df[df.week_end.dt.year==y].copy()
        if z.empty:
            continue
        z["iso_week"] = z.week_end.dt.isocalendar().week.astype(int)
        z["wdist"] = (z.iso_week-target_week).abs()
        z["wdist"] = np.minimum(z["wdist"], 53-z["wdist"])
        zz=z[z.wdist<=1][value_col].dropna()
        if len(zz):
            vals.append(float(zz.mean()))
    return vals

def seasonal_gap(df, week_end):
    row=df.loc[df.week_end==pd.Timestamp(week_end),"value"]
    if row.empty:
        return np.nan, np.nan, 0
    vals=seasonal_contrib(df, week_end)
    if len(vals)<3:
        return float(row.iloc[-1]), np.nan, len(vals)
    ref=float(np.mean(vals))
    v=float(row.iloc[-1])
    return v, (v-ref)/ref, len(vals)

def refinery_state(df, week_end):
    row=df.loc[df.week_end==pd.Timestamp(week_end),"value"]
    if row.empty:
        return np.nan,np.nan,np.nan,0
    vals=seasonal_contrib(df, week_end)
    v=float(row.iloc[-1])
    if len(vals)<3:
        return v,np.nan,np.nan,len(vals)
    q90=float(np.quantile(vals,0.90))
    return v,q90,float(v>q90),len(vals)

def fetch_wti_daily():
    raw=get_bytes(WTI_DAILY_URL,timeout=45)
    x=pd.read_csv(io.BytesIO(raw))
    x.columns=["date","wti"]
    x["date"]=pd.to_datetime(x["date"],errors="coerce")
    x["wti"]=pd.to_numeric(x["wti"],errors="coerce")
    x=x.dropna().sort_values("date").reset_index(drop=True)
    meta={
        "series_id":"DCOILWTICO",
        "download_url":WTI_DAILY_URL,
        "sha256":sha256(raw),
        "rows":int(len(x)),
        "first_date":str(x.date.min().date()),
        "last_date":str(x.date.max().date()),
        "retrieved_utc":datetime.now(timezone.utc).isoformat(),
        "acquisition_method":"FRED_DIRECT_CSV",
    }
    return x,meta

def first_obs_on_or_after(df,target):
    z=df[df.date>=pd.Timestamp(target)]
    if z.empty:
        return None
    return z.iloc[0]

def daily_outcomes(wti, decision_date):
    a=first_obs_on_or_after(wti, decision_date)
    if a is None:
        return {}
    out={"exec_date":a.date,"exec_wti":a.wti}
    for months in [3,6]:
        target=pd.Timestamp(decision_date)+pd.DateOffset(months=months)
        e=first_obs_on_or_after(wti,target)
        if e is None:
            out[f"wti_fwd_{months}m"]=np.nan
            out[f"short_mae_{months}m"]=np.nan
            out[f"endpoint_date_{months}m"]=pd.NaT
            continue
        out[f"endpoint_date_{months}m"]=e.date
        out[f"wti_fwd_{months}m"]=float(e.wti/a.wti-1)
        path=wti[(wti.date>=a.date)&(wti.date<=e.date)].copy()
        out[f"short_mae_{months}m"]=float((path.wti/a.wti-1).max())
    return out

def mwu(a,b):
    a=pd.Series(a).dropna().astype(float)
    b=pd.Series(b).dropna().astype(float)
    if len(a)<2 or len(b)<2:
        return np.nan
    return float(mannwhitneyu(a,b,alternative="two-sided").pvalue)

def bh(pvals):
    p=np.asarray(pvals,dtype=float)
    out=np.full_like(p,np.nan)
    ok=np.isfinite(p)
    pv=p[ok]
    if not len(pv):
        return out
    order=np.argsort(pv); ranked=pv[order]; m=len(ranked)
    q=ranked*m/np.arange(1,m+1)
    q=np.minimum.accumulate(q[::-1])[::-1]
    q=np.minimum(q,1.0)
    tmp=np.empty_like(q); tmp[order]=q; out[ok]=tmp
    return out

def main():
    if not PRICE_EVENTS.exists():
        raise SystemExit("Frozen price EVENTS.csv missing")

    events=pd.read_csv(PRICE_EVENTS,parse_dates=["s3_date","anchor_date"])

    physical={}
    source_rows=[]
    for name,meta in EIA_SERIES.items():
        z,m=parse_eia_xls(meta["id"])
        physical[name]=z
        source_rows.append({**meta,**m})

    twip,twip_meta=build_twip_release_registry()

    # Use crude week-end calendar for 2026 schedule construction.
    r2026=build_2026_release_registry(physical["CRUDE"].week_end)
    release=pd.concat([twip,r2026],ignore_index=True)
    release=release.drop_duplicates(["week_end"],keep="last").sort_values("week_end").reset_index(drop=True)

    # Restrict release rows to week-ends present in all physical series.
    common_we=set(physical["CRUDE"].week_end)
    for k in ["GASOLINE","DISTILLATE","REFINERY_UTIL"]:
        common_we &= set(physical[k].week_end)
    release=release[release.week_end.isin(common_we)].copy()

    wti,wti_meta=fetch_wti_daily()
    source_rows.append({
        "id":"DCOILWTICO","title":"WTI Spot Price daily",
        "unit":"USD/barrel",**wti_meta
    })

    rows=[]
    for _,ev in events.iterrows():
        s3_end=ev.s3_date+pd.offsets.MonthEnd(0)
        conf_end=ev.anchor_date+pd.offsets.MonthEnd(0)

        prior=release[release.release_date<=s3_end]
        after=release[release.release_date>conf_end]

        row={
            "s3_date":ev.s3_date,
            "price_anchor_month":ev.anchor_date,
            "price_layer_classification":ev.classification,
            "s3_month_end":s3_end,
            "confirmation_month_end":conf_end,
        }

        # Strict PIT unavailable for pre-2002 event under current official archive.
        if ev.s3_date.year < 2002 or prior.empty or after.empty:
            row.update({
                "strict_pit":"UNAVAILABLE",
                "physical_classification":"STRICT_PIT_UNAVAILABLE",
            })
            rows.append(row)
            continue

        base=prior.iloc[-1]
        dec=after.iloc[0]
        row.update({
            "strict_pit":"AVAILABLE",
            "baseline_release_date":base.release_date,
            "baseline_week_end":base.week_end,
            "baseline_release_method":base.release_method,
            "decision_date":dec.release_date,
            "decision_week_end":dec.week_end,
            "decision_release_method":dec.release_method,
        })

        improve_count=0
        complete=True
        for name in ["CRUDE","GASOLINE","DISTILLATE"]:
            bv,bgap,bn=seasonal_gap(physical[name],base.week_end)
            dv,dgap,dn=seasonal_gap(physical[name],dec.week_end)
            improving=bool(np.isfinite(bgap) and np.isfinite(dgap) and dgap>bgap)
            if improving:
                improve_count+=1
            if not (np.isfinite(bgap) and np.isfinite(dgap)):
                complete=False
            row.update({
                f"{name.lower()}_baseline":bv,
                f"{name.lower()}_decision":dv,
                f"{name.lower()}_seasonal_gap_baseline":bgap,
                f"{name.lower()}_seasonal_gap_decision":dgap,
                f"{name.lower()}_improving":improving,
                f"{name.lower()}_prior_years_baseline":bn,
                f"{name.lower()}_prior_years_decision":dn,
            })

        bu,bq,bhigh,bn=refinery_state(physical["REFINERY_UTIL"],base.week_end)
        du,dq,dhigh,dn=refinery_state(physical["REFINERY_UTIL"],dec.week_end)
        refinery_high=bool(dhigh==1.0) if np.isfinite(dhigh) else False
        refinery_worsening=bool(refinery_high and du>bu) if np.isfinite(bu) and np.isfinite(du) else False
        refinery_drop=bool((du-bu)<=-5.0) if np.isfinite(bu) and np.isfinite(du) else False
        if not (np.isfinite(bq) and np.isfinite(dq)):
            complete=False

        row.update({
            "inventory_improving_count":improve_count,
            "refinery_util_baseline":bu,
            "refinery_util_decision":du,
            "refinery_q90_baseline":bq,
            "refinery_q90_decision":dq,
            "refinery_high_decision":refinery_high,
            "refinery_worsening":refinery_worsening,
            "refinery_drop_5pp":refinery_drop,
            "physical_data_complete":complete,
        })

        p4a=(
            complete
            and ev.classification=="PRICE_PRODUCT_CONFIRMED"
            and improve_count>=2
            and not refinery_worsening
        )
        p4b=(
            complete
            and ev.classification=="PRICE_PRODUCT_CONFIRMED"
            and refinery_drop
        )
        row["p4a_data_only"]=bool(p4a)
        row["p4b_refinery_drop_candidate"]=bool(p4b)
        row["physical_classification"]="P4A_DATA_ONLY" if p4a else "PHYSICAL_VETO_DATA_ONLY"

        row.update(daily_outcomes(wti,dec.release_date))
        rows.append(row)

    out=pd.DataFrame(rows)

    testspec=[
        ("WTI_fwd_3m","wti_fwd_3m"),
        ("WTI_fwd_6m","wti_fwd_6m"),
        ("short_MAE_3m","short_mae_3m"),
        ("short_MAE_6m","short_mae_6m"),
    ]
    a=out[out.physical_classification=="P4A_DATA_ONLY"]
    b=out[out.physical_classification=="PHYSICAL_VETO_DATA_ONLY"]
    tests=[]
    for label,col in testspec:
        xa=a[col].dropna() if col in a else pd.Series(dtype=float)
        xb=b[col].dropna() if col in b else pd.Series(dtype=float)
        tests.append({
            "test":label,
            "n_p4a":len(xa),
            "n_veto":len(xb),
            "p4a_mean":xa.mean(),
            "veto_mean":xb.mean(),
            "p4a_median":xa.median(),
            "veto_median":xb.median(),
            "difference_median_p4a_minus_veto":xa.median()-xb.median() if len(xa) and len(xb) else np.nan,
            "mann_whitney_p":mwu(xa,xb),
        })
    tests=pd.DataFrame(tests)
    tests["bh_q_4test_family"]=bh(tests.mann_whitney_p)

    counts={
        "events_total":int(len(out)),
        "strict_pit_available":int((out.strict_pit=="AVAILABLE").sum()),
        "strict_pit_unavailable":int((out.strict_pit!="AVAILABLE").sum()),
        "p4a_data_only":int((out.physical_classification=="P4A_DATA_ONLY").sum()),
        "physical_veto_data_only":int((out.physical_classification=="PHYSICAL_VETO_DATA_ONLY").sum()),
        "p4b_refinery_drop_candidate":int(out.get("p4b_refinery_drop_candidate",pd.Series(dtype=bool)).fillna(False).sum()),
        "release_registry_rows":int(len(release)),
    }

    qc={
        **counts,
        "price_event_set_preserved":bool(len(out)==len(events)),
        "duplicate_event_s3_dates":int(out.s3_date.duplicated().sum()),
        "release_registry_duplicate_week_end":int(release.week_end.duplicated().sum()),
        "twip_registry":twip_meta,
        "geopolitical_shock_veto":"NOT_YET_FROZEN",
        "primary_evidence_status":"EXPLORATORY_DATA_ONLY",
    }
    qc["qc_gate"]="PASS" if (
        qc["price_event_set_preserved"]
        and qc["duplicate_event_s3_dates"]==0
        and qc["release_registry_duplicate_week_end"]==0
    ) else "FAIL"

    source=pd.DataFrame(source_rows)
    source.to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)
    release.to_csv(OUT/"RELEASE_DATE_REGISTRY.csv",index=False)
    out.to_csv(OUT/"PHYSICAL_EVENT_PANEL.csv",index=False)
    tests.to_csv(OUT/"PRIMARY_DATA_ONLY_TESTS.csv",index=False)
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,default=str),encoding="utf-8")

    lines=[
        "# ENERGY-PHYSICAL-WF-001 v1.1 — First Release-Aware Data-Only Run",
        "Date: 2026-09-24",
        "",
        "## Status",
        "",
        "**EXPLORATORY / STRICT-PIT DATA-ONLY PHYSICAL LAYER / NOT DEPLOYABLE**",
        "",
        "A complete geopolitical/shipping shock veto has not yet been frozen, so even a small p/q-value cannot be upgraded to full P4A confirmation.",
        "",
        "## QC",
        "",
        f"- Frozen price events preserved: {qc['price_event_set_preserved']}",
        f"- Strict PIT available: {counts['strict_pit_available']} / {counts['events_total']}",
        f"- P4A_DATA_ONLY: {counts['p4a_data_only']}",
        f"- PHYSICAL_VETO_DATA_ONLY: {counts['physical_veto_data_only']}",
        f"- P4B refinery-drop candidates: {counts['p4b_refinery_drop_candidate']}",
        f"- QC gate: {qc['qc_gate']}",
        "",
        "## Primary four-test data-only family",
        "",
        tests.to_markdown(index=False),
        "",
        "## Event panel",
        "",
        out[[
            "s3_date","price_anchor_month","price_layer_classification","strict_pit",
            "baseline_release_date","decision_date","inventory_improving_count",
            "refinery_util_baseline","refinery_util_decision","refinery_worsening",
            "refinery_drop_5pp","physical_classification",
            "wti_fwd_3m","wti_fwd_6m","short_mae_3m","short_mae_6m"
        ]].to_markdown(index=False),
        "",
        "## Interpretation boundary",
        "",
        "This run asks whether release-aware U.S. inventory/refinery information adds discrimination beyond the frozen price layer.",
        "",
        "It does not identify causality, it does not yet apply an independently frozen geopolitical/shipping veto, and it is not a trading system.",
    ]
    (OUT/"ENERGY_PHYSICAL_WF_001_V1_1_REPORT.md").write_text("\n".join(lines),encoding="utf-8")

    if qc["qc_gate"]!="PASS":
        raise SystemExit("QC failed")

    print(json.dumps({**counts,"qc_gate":qc["qc_gate"]},indent=2))

if __name__=="__main__":
    main()
