#!/usr/bin/env python3
"""
ENERGY-WEEKLY-PIT-003
Build and audit the full EIA WPSR week_end -> release_date clock.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"energy_weekly_pit_v1"
OUT.mkdir(parents=True,exist_ok=True)

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

PHYS=load_module(
    ROOT/"scripts"/"run_energy_physical_walkforward_v1_1.py",
    "physical_for_full_release_clock",
)

SCHEDULE_URL="https://www.eia.gov/petroleum/supply/weekly/schedule.php"
SERIES=["WCESTUS1","WGTSTUS1","WDISTUS1","WPULEUS3"]

MONTHS={
    "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
    "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
}

def build_full_twip_registry():
    raw=fetch_bytes(PHYS.TWIP_URL,timeout=90)
    soup=BeautifulSoup(raw,"html.parser")
    sections={}
    # The archive has top navigation year labels plus later year-section labels.
    # Take the LAST exact year node in document order, which avoids the nav copy.
    year_nodes={y:[] for y in range(2002,2026)}
    for tag in soup.find_all(True):
        txt=tag.get_text(" ",strip=True)
        if re.fullmatch(r"20\\d{2}",txt):
            year=int(txt)
            if 2002<=year<=2025:
                year_nodes[year].append(tag)
        tid=str(tag.get("id","")).strip()
        if re.fullmatch(r"20\\d{2}",tid):
            year=int(tid)
            if 2002<=year<=2025:
                year_nodes[year].append(tag)
    for year,nodes in year_nodes.items():
        if not nodes:
            continue
        tag=nodes[-1]
        table=tag.find_next("table")
        if table is not None:
            sections[year]=table

    rows=[]
    for year,table in sorted(sections.items()):
        current_month=None
        for tr in table.find_all("tr"):
            cells=[c.get_text(" ",strip=True) for c in tr.find_all(["th","td"])]
            if len(cells)<2:
                continue
            if any("Release date" in c for c in cells):
                continue

            if cells[0] in MONTHS and len(cells)>=3:
                current_month=MONTHS[cells[0]]
                rel_month=current_month
                rel_day=cells[1]
                week_txt=cells[2]
            elif current_month is not None and len(cells)>=2:
                rel_month=current_month
                rel_day=cells[0]
                week_txt=cells[1]
            else:
                continue

            m=re.search(r"\\d+",str(rel_day))
            if not m:
                continue
            try:
                release=pd.Timestamp(year,rel_month,int(m.group(0)))
            except Exception:
                continue

            parts=[int(x) for x in re.findall(r"\\d+",str(week_txt))]
            if not parts:
                continue

            week_end=None
            if "/" in str(week_txt) and len(parts)>=2:
                wm,wd=parts[0],parts[1]
                wy=year-1 if (rel_month==1 and wm==12) else year
                try:
                    week_end=pd.Timestamp(wy,wm,wd)
                except Exception:
                    week_end=None
            else:
                wd=parts[0]
                # Search release month and prior month; accept only plausible WPSR lag.
                candidates=[]
                for delta in [0,-1]:
                    cm=release+pd.DateOffset(months=delta)
                    try:
                        cand=pd.Timestamp(cm.year,cm.month,wd)
                        lag=(release-cand).days
                        if 3<=lag<=12:
                            candidates.append((abs(lag-5),cand))
                    except Exception:
                        pass
                if candidates:
                    week_end=sorted(candidates,key=lambda x:x[0])[0][1]

            if week_end is None:
                continue
            lag=(release-week_end).days
            if not (3<=lag<=12):
                continue

            rows.append({
                "week_end":week_end.normalize(),
                "release_date":release.normalize(),
                "release_method":"EIA_TWIP_ARCHIVE_EXPLICIT",
                "source_url":PHYS.TWIP_URL,
                "section_year":year,
            })

    out=pd.DataFrame(rows)
    if len(out):
        out=out.sort_values(["week_end","release_date"]).drop_duplicates("week_end",keep="last").reset_index(drop=True)
    meta={
        "source_url":PHYS.TWIP_URL,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "rows":int(len(out)),
        "years_found":sorted(sections.keys()),
        "year_count":len(sections),
    }
    return out,meta


def fetch_bytes(url,timeout=90):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 gss-cb-001-public-research/1.0"})
    with urlopen(req,timeout=timeout) as r:
        return r.read()

def parse_2026_exceptions():
    raw=fetch_bytes(SCHEDULE_URL)
    soup=BeautifulSoup(raw,"html.parser")
    rows=[]
    for tr in soup.find_all("tr"):
        cells=[c.get_text(" ",strip=True) for c in tr.find_all(["th","td"])]
        if len(cells)<2:
            continue
        joined=" ".join(cells)
        if "2026" not in joined:
            continue
        # First two date-like cells are week ending and alternate release.
        dates=[]
        for c in cells:
            try:
                d=pd.to_datetime(c,errors="raise")
                if d.year==2026:
                    dates.append(pd.Timestamp(d).normalize())
            except Exception:
                pass
        if len(dates)>=2:
            rows.append({
                "week_end":dates[0],
                "release_date":dates[1],
                "release_method":"EIA_2026_HOLIDAY_EXCEPTION",
                "source_url":SCHEDULE_URL,
            })
    out=pd.DataFrame(rows)
    if len(out):
        out=out.drop_duplicates("week_end").sort_values("week_end").reset_index(drop=True)
    return out, hashlib.sha256(raw).hexdigest()

def build_2026(common_week_ends):
    exc,schedule_sha=parse_2026_exceptions()
    exc_map={} if exc.empty else dict(zip(exc.week_end,exc.release_date))
    rows=[]
    for we in sorted(pd.to_datetime(common_week_ends)):
        if we.year!=2026:
            continue
        standard=we+pd.Timedelta(days=(2-we.weekday())%7 or 7)
        rd=exc_map.get(pd.Timestamp(we).normalize(),standard)
        method="EIA_2026_HOLIDAY_EXCEPTION" if pd.Timestamp(we).normalize() in exc_map else "EIA_2026_STANDARD_SCHEDULE"
        rows.append({
            "week_end":pd.Timestamp(we).normalize(),
            "release_date":pd.Timestamp(rd).normalize(),
            "release_method":method,
            "source_url":SCHEDULE_URL,
        })
    return pd.DataFrame(rows), schedule_sha, exc

def main():
    hist,hist_meta=build_full_twip_registry()
    if hist.empty or "week_end" not in hist.columns:\n        raise RuntimeError(f"TWIP year-section discovery returned no rows; meta={hist_meta}")\n    hist=hist[(hist.week_end.dt.year>=2002)&(hist.week_end.dt.year<=2025)].copy()

    pdata={}
    pmeta=[]
    for sid in SERIES:
        z,m=PHYS.parse_eia_xls(sid)
        pdata[sid]=z
        pmeta.append(m)

    common=set(pdata[SERIES[0]].week_end)
    for sid in SERIES[1:]:
        common &= set(pdata[sid].week_end)
    common=sorted(pd.to_datetime(list(common)))

    exceptions,schedule_sha=parse_2026_exceptions()
    # Rebuild 2026 only on exact common physical grid.
    r2026_rows=[]
    exc_map={} if exceptions.empty else dict(zip(exceptions.week_end,exceptions.release_date))
    for we in common:
        if we.year!=2026:
            continue
        days=(2-we.weekday())%7
        if days==0:
            days=7
        standard=we+pd.Timedelta(days=days)
        rd=exc_map.get(pd.Timestamp(we).normalize(),standard)
        r2026_rows.append({
            "week_end":pd.Timestamp(we).normalize(),
            "release_date":pd.Timestamp(rd).normalize(),
            "release_method":"EIA_2026_HOLIDAY_EXCEPTION" if pd.Timestamp(we).normalize() in exc_map else "EIA_2026_STANDARD_SCHEDULE",
            "source_url":SCHEDULE_URL,
        })
    r2026=pd.DataFrame(r2026_rows)

    registry=pd.concat([hist,r2026],ignore_index=True)
    registry=registry.drop_duplicates("week_end",keep="last").sort_values("week_end").reset_index(drop=True)
    registry["release_lag_days"]=(registry.release_date-registry.week_end).dt.days
    registry["week_end_gap_days"]=registry.week_end.diff().dt.days
    registry["holiday_shift_gt5d"]=registry.release_lag_days>5

    common_hist=pd.DatetimeIndex([x for x in common if 2002<=x.year<=2025])
    reg_hist=set(registry.loc[(registry.week_end.dt.year>=2002)&(registry.week_end.dt.year<=2025),"week_end"])
    mapped=sum(pd.Timestamp(x) in reg_hist for x in common_hist)
    coverage=float(mapped/len(common_hist)) if len(common_hist) else np.nan

    missing_common=pd.DataFrame({"week_end":[x for x in common_hist if pd.Timestamp(x) not in reg_hist]})
    reg_only=pd.DataFrame({"week_end":[x for x in sorted(reg_hist) if pd.Timestamp(x) not in set(common_hist)]})

    hist_rows=int(((registry.week_end.dt.year>=2002)&(registry.week_end.dt.year<=2025)).sum())
    duplicate_we=int(registry.week_end.duplicated().sum())
    duplicate_pair=int(registry[["week_end","release_date"]].duplicated().sum())
    lag_bad=int(((registry.release_lag_days<=0)|(registry.release_lag_days<3)|(registry.release_lag_days>12)).sum())
    med_lag=float(registry.loc[registry.week_end.dt.year<=2025,"release_lag_days"].median())

    # date-grid agreement across physical series on common set is tautologically common;
    # audit each series has unique dates before forming the intersection.
    grid_dup={sid:int(pdata[sid].week_end.duplicated().sum()) for sid in SERIES}

    hard_fail=(
        hist_rows<1200
        or registry.loc[registry.week_end.dt.year<=2025,"week_end"].min().year!=2002
        or registry.loc[registry.week_end.dt.year<=2025,"week_end"].max().year!=2025
        or registry.loc[registry.week_end.dt.year<=2025,"week_end"].max().month!=12
        or duplicate_we!=0
        or duplicate_pair!=0
        or lag_bad!=0
        or not (5.0<=med_lag<=6.0)
        or coverage<0.95
        or any(v!=0 for v in grid_dup.values())
    )

    qc={
        "qc_gate":"FAIL" if hard_fail else "PASS",
        "module":"ENERGY-WEEKLY-PIT-003",
        "historical_registry_rows_2002_2025":hist_rows,
        "registry_rows_total":int(len(registry)),
        "first_week_end":str(registry.week_end.min().date()),
        "last_week_end":str(registry.week_end.max().date()),
        "duplicate_week_ends":duplicate_we,
        "duplicate_week_end_release_pairs":duplicate_pair,
        "release_lag_bad_rows":lag_bad,
        "release_lag_min_days":int(registry.release_lag_days.min()),
        "release_lag_median_days_2002_2025":med_lag,
        "release_lag_max_days":int(registry.release_lag_days.max()),
        "common_physical_week_ends_2002_2025":int(len(common_hist)),
        "common_physical_release_mapping_coverage":coverage,
        "missing_common_physical_week_ends":int(len(missing_common)),
        "registry_only_historical_week_ends":int(len(reg_only)),
        "physical_series_duplicate_dates":grid_dup,
        "historical_archive_sha256":hist_meta["sha256"],
        "historical_year_sections_found":hist_meta.get("years_found",[]),
        "historical_year_section_count":hist_meta.get("year_count",0),
        "schedule_2026_sha256":schedule_sha,
        "holiday_exception_rows_2026":int(len(exceptions)),
        "outcomes_loaded":False,
        "deployment_status":"NOT_DEPLOYABLE",
    }

    registry.to_csv(OUT/"WPSR_RELEASE_REGISTRY.csv",index=False)
    missing_common.to_csv(OUT/"MISSING_COMMON_PHYSICAL_WEEK_ENDS.csv",index=False)
    reg_only.to_csv(OUT/"REGISTRY_ONLY_WEEK_ENDS.csv",index=False)
    pd.DataFrame(pmeta).to_csv(OUT/"PHYSICAL_SOURCE_REGISTRY.csv",index=False)
    exceptions.to_csv(OUT/"WPSR_2026_HOLIDAY_EXCEPTIONS.csv",index=False)
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,default=str)+"\n",encoding="utf-8")

    lagdesc=registry.release_lag_days.value_counts().sort_index().rename_axis("release_lag_days").reset_index(name="n")
    lagdesc.to_csv(OUT/"RELEASE_LAG_DISTRIBUTION.csv",index=False)

    lines=[
        "# ENERGY-WEEKLY-PIT-003 — Full WPSR Release-Clock Audit",
        "",
        "**DATA TIMING / RELEASE-CLOCK INFRASTRUCTURE ONLY**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- historical rows 2002-2025: {hist_rows}",
        f"- full registry rows: {len(registry)}",
        f"- release-lag median 2002-2025: {med_lag:.1f} days",
        f"- common physical-grid coverage: {coverage:.2%}",
        f"- missing common physical week ends: {len(missing_common)}",
        "",
        "## Release-lag distribution",
        "",
        lagdesc.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "A QC pass means the new weekly/daily energy engine may use this registry as its public-information clock.",
        "This module contains no event outcome or forecasting evidence.",
    ]
    (OUT/"ENERGY_WEEKLY_PIT_003_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    print(json.dumps(qc,indent=2,default=str))
    if hard_fail:
        raise SystemExit("ENERGY-WEEKLY-PIT-003 QC failed")

if __name__=="__main__":
    main()
