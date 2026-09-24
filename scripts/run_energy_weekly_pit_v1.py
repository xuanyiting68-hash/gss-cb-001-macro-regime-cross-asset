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

def build_full_twip_registry(common_week_ends):
    """
    Reconstruct actual historical release dates from official TWIP archive hrefs.

    The archive URL encodes release date as:
      /petroleum/weekly/archive/YYYY/YYMMDD/...

    We then map each official release date to the latest common EIA physical
    week-ending observation 3-12 calendar days earlier. This does not assume
    Wednesday and preserves holiday shifts encoded by the archive URL itself.
    """
    raw=fetch_bytes(PHYS.TWIP_URL,timeout=90)
    soup=BeautifulSoup(raw,"html.parser")
    releases={}
    pat=re.compile(r"/petroleum/weekly/archive/(?:(20\d{2})/)?(\d{6})(?:/|$)",re.I)

    for a in soup.find_all("a",href=True):
        href=str(a.get("href",""))
        m=pat.search(href)
        if not m:
            continue
        year_dir=int(m.group(1)) if m.group(1) else None
        code=m.group(2)
        try:
            yy=int(code[:2]); mm=int(code[2:4]); dd=int(code[4:6])
            year=2000+yy
            release=pd.Timestamp(year,mm,dd).normalize()
        except Exception:
            continue
        if not (2002<=year<=2025):
            continue
        if year_dir is not None and year_dir!=year:
            continue
        releases[release]=href

    common=pd.DatetimeIndex(sorted(pd.to_datetime(common_week_ends))).normalize()
    rows=[]
    ambiguous=0
    unmapped=0
    for release,href in sorted(releases.items()):
        candidates=common[(common<release) & ((release-common).days>=3) & ((release-common).days<=12)]
        if len(candidates)==0:
            unmapped+=1
            continue
        # The publication refers to the most recent available weekly grid row.
        week_end=candidates.max()
        same_latest=candidates[candidates==week_end]
        if len(same_latest)!=1:
            ambiguous+=1
            continue
        rows.append({
            "week_end":pd.Timestamp(week_end).normalize(),
            "release_date":pd.Timestamp(release).normalize(),
            "release_method":"EIA_TWIP_ARCHIVE_URL_DATE",
            "source_url":PHYS.TWIP_URL,
            "archive_href":href,
        })

    archive_hrefs=sorted({
        str(a.get("href","")) for a in soup.find_all("a",href=True)
        if "archive" in str(a.get("href","")).lower()
    })
    if not releases:
        print(json.dumps({
            "twip_archive_href_count":len(archive_hrefs),
            "twip_archive_href_sample":archive_hrefs[:80],
            "html_bytes":len(raw),
            "html_sha256":hashlib.sha256(raw).hexdigest(),
        },indent=2))

    out=pd.DataFrame(rows)
    if len(out):
        out=(
            out.sort_values(["week_end","release_date"])
            .drop_duplicates("week_end",keep="last")
            .reset_index(drop=True)
        )
    meta={
        "source_url":PHYS.TWIP_URL,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "archive_release_links":int(len(releases)),
        "rows":int(len(out)),
        "ambiguous_mappings":int(ambiguous),
        "unmapped_release_links":int(unmapped),
        "first_release_date":str(min(releases).date()) if releases else None,
        "last_release_date":str(max(releases).date()) if releases else None,
    }
    return out,meta


def fetch_bytes(url,timeout=90):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 gss-cb-001-public-research/1.0"})
    with urlopen(req,timeout=timeout) as r:
        return r.read()

def parse_schedule_exceptions(years=(2025,2026)):
    raw=fetch_bytes(SCHEDULE_URL)
    soup=BeautifulSoup(raw,"html.parser")
    rows=[]
    years=set(int(y) for y in years)
    for tr in soup.find_all("tr"):
        cells=[cell.get_text(" ",strip=True) for cell in tr.find_all(["th","td"])]
        if len(cells)<2:
            continue
        parsed=[]
        for cell in cells:
            d=pd.to_datetime(cell,errors="coerce")
            if pd.notna(d):
                ts=pd.Timestamp(d).normalize()
                if ts.year in years or (ts.year==2024 and 2025 in years):
                    parsed.append(ts)
        if len(parsed)>=2:
            week_end,release=parsed[0],parsed[1]
            if release>week_end and (week_end.year in years or release.year in years):
                rows.append({
                    "week_end":week_end,
                    "release_date":release,
                    "release_method":"EIA_WPSR_HOLIDAY_EXCEPTION",
                    "source_url":SCHEDULE_URL,
                })
    out=pd.DataFrame(rows)
    if len(out):
        out=out.drop_duplicates("week_end").sort_values("week_end").reset_index(drop=True)
    return out, hashlib.sha256(raw).hexdigest()


def standard_wpsr_release(week_end):
    we=pd.Timestamp(week_end).normalize()
    days=(2-we.weekday())%7
    if days==0:
        days=7
    return we+pd.Timedelta(days=days)



def main():
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

    hist,hist_meta=build_full_twip_registry(common)
    if hist.empty or "week_end" not in hist.columns:
        raise RuntimeError(f"TWIP archive-link discovery returned no rows; meta={hist_meta}")
    hist=hist[(hist.week_end.dt.year>=2002)&(hist.week_end.dt.year<=2025)].copy()

    exceptions,schedule_sha=parse_schedule_exceptions((2025,2026))
    exc_map={} if exceptions.empty else dict(zip(exceptions.week_end,exceptions.release_date))

    final_twip_we=pd.Timestamp(hist.week_end.max()).normalize()
    post_rows=[]
    for we in common:
        we=pd.Timestamp(we).normalize()
        if we<=final_twip_we:
            continue
        if we.year not in (2025,2026):
            continue
        standard=standard_wpsr_release(we)
        rd=exc_map.get(we,standard)
        post_rows.append({
            "week_end":we,
            "release_date":pd.Timestamp(rd).normalize(),
            "release_method":"EIA_WPSR_HOLIDAY_EXCEPTION" if we in exc_map else "EIA_WPSR_STANDARD_SCHEDULE",
            "source_url":SCHEDULE_URL,
        })
    post=pd.DataFrame(post_rows)

    registry=pd.concat([hist,post],ignore_index=True)
    registry=registry.drop_duplicates("week_end",keep="last").sort_values("week_end").reset_index(drop=True)
    registry["release_lag_days"]=(registry.release_date-registry.week_end).dt.days
    registry["week_end_gap_days"]=registry.week_end.diff().dt.days
    registry["holiday_shift_gt5d"]=registry.release_lag_days>5

    # Independent exact cross-check against the previously curated official
    # event-scoped release registry used by PHYSICAL-WF-001 v1.1.
    curated_path=ROOT/"data"/"public"/"ENERGY_PHYSICAL_EVENT_RELEASE_REGISTRY_V1.csv"
    curated=pd.read_csv(curated_path,parse_dates=["week_end","release_date"])
    curated=curated[(curated.week_end.dt.year>=2002)&(curated.week_end.dt.year<=2025)].copy()
    hmap=dict(zip(hist.week_end,hist.release_date))
    curated_matches=0
    curated_checked=0
    curated_mismatch_rows=[]
    for _,r in curated.iterrows():
        we=pd.Timestamp(r.week_end).normalize()
        rd=pd.Timestamp(r.release_date).normalize()
        if we in hmap:
            curated_checked+=1
            if pd.Timestamp(hmap[we]).normalize()==rd:
                curated_matches+=1
            else:
                curated_mismatch_rows.append({
                    "week_end":we,
                    "curated_release_date":rd,
                    "full_registry_release_date":pd.Timestamp(hmap[we]).normalize(),
                })
    curated_match_share=(curated_matches/curated_checked) if curated_checked else np.nan
    pd.DataFrame(curated_mismatch_rows).to_csv(OUT/"CURATED_RELEASE_CROSSCHECK_MISMATCHES.csv",index=False)

    post_2025=post[post.week_end.dt.year==2025].copy() if len(post) else pd.DataFrame()
    expected_post_2025=[pd.Timestamp(x).normalize() for x in common if pd.Timestamp(x).year==2025 and pd.Timestamp(x).normalize()>final_twip_we]
    post_2025_coverage=(
        float(sum(x in set(post_2025.week_end) for x in expected_post_2025)/len(expected_post_2025))
        if expected_post_2025 else 1.0
    )

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

    regmap=dict(zip(registry.week_end,registry.release_date))
    schedule_anchor_expected={
        pd.Timestamp("2025-11-07"):pd.Timestamp("2025-11-13"),
        pd.Timestamp("2025-12-19"):pd.Timestamp("2025-12-29"),
        pd.Timestamp("2026-09-04"):pd.Timestamp("2026-09-10"),
    }
    schedule_anchor_matches={
        str(k.date()): bool(k in regmap and pd.Timestamp(regmap[k]).normalize()==v)
        for k,v in schedule_anchor_expected.items()
    }
    schedule_anchor_all_pass=all(schedule_anchor_matches.values())

    hard_fail=(
        hist_rows<1200
        or registry.loc[registry.week_end.dt.year<=2025,"week_end"].min().year!=2002
        or registry.loc[registry.week_end.dt.year<=2025,"week_end"].max().year!=2025
        or registry.loc[registry.week_end.dt.year<=2025,"week_end"].max().month!=12
        or post_2025_coverage<1.0
        or len(exceptions)<10
        or not schedule_anchor_all_pass
        or duplicate_we!=0
        or duplicate_pair!=0
        or lag_bad!=0
        or not (5.0<=med_lag<=6.0)
        or coverage<0.95
        or curated_checked<20
        or curated_match_share<1.0
        or hist_meta.get("ambiguous_mappings",0)!=0
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
        "curated_release_rows_checked":int(curated_checked),
        "curated_release_exact_matches":int(curated_matches),
        "curated_release_exact_match_share":float(curated_match_share) if np.isfinite(curated_match_share) else None,
        "missing_common_physical_week_ends":int(len(missing_common)),
        "registry_only_historical_week_ends":int(len(reg_only)),
        "physical_series_duplicate_dates":grid_dup,
        "historical_archive_sha256":hist_meta["sha256"],
        "historical_archive_release_links":hist_meta.get("archive_release_links",0),
        "historical_archive_ambiguous_mappings":hist_meta.get("ambiguous_mappings",0),
        "historical_archive_unmapped_release_links":hist_meta.get("unmapped_release_links",0),
        "schedule_2026_sha256":schedule_sha,
        "schedule_exception_rows_2025_2026":int(len(exceptions)),
        "schedule_anchor_matches":schedule_anchor_matches,
        "schedule_anchor_all_pass":schedule_anchor_all_pass,
        "final_twip_week_end":str(final_twip_we.date()),
        "post_twip_2025_common_week_ends":int(len(expected_post_2025)),
        "post_twip_2025_coverage":post_2025_coverage,
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
