#!/usr/bin/env python3
"""
FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010
Strict live-input timing audit for prospective transport of OOS-008.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_prospective_input_timing_v1"
OUT.mkdir(parents=True, exist_ok=True)

GOLD_REPO = "datasets/gold-prices"
GOLD_COMMITS_API = (
    "https://api.github.com/repos/datasets/gold-prices/commits"
    "?path=data/monthly.csv&per_page=20"
)
GOLD_RAW_TMPL = (
    "https://raw.githubusercontent.com/datasets/gold-prices/{sha}/data/monthly.csv"
)
GOLD_SOURCE_PAGE = "https://www.worldbank.org/en/research/commodity-markets"

def fetch_bytes(url: str, timeout: int = 120) -> bytes:
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 gss-cb-001-public-research/1.0",
            "Accept": "*/*",
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()

def fetch_json(url: str):
    return json.loads(fetch_bytes(url).decode("utf-8"))

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

VINTAGE = load_module(
    ROOT / "scripts" / "run_fed_cycle_vintage_audit_v1.py",
    "vintage_audit_for_input_timing",
)

def max_gold_period(raw: bytes) -> pd.Period:
    df = pd.read_csv(io.BytesIO(raw))
    periods = pd.PeriodIndex(df["Date"].astype(str), freq="M")
    if len(periods) == 0:
        raise RuntimeError("Gold monthly file is empty")
    return periods.max()

def audit_gold_release_timing():
    commits = fetch_json(GOLD_COMMITS_API)
    if len(commits) < 6:
        raise RuntimeError(f"Too few Gold file commits: {len(commits)}")

    snapshots = []
    for c in commits:
        sha = c["sha"]
        ts = pd.Timestamp(c["commit"]["author"]["date"])
        raw = fetch_bytes(GOLD_RAW_TMPL.format(sha=sha), timeout=60)
        snapshots.append({
            "sha": sha,
            "commit_timestamp_utc": ts,
            "file_sha256": hashlib.sha256(raw).hexdigest(),
            "latest_observation_period": max_gold_period(raw),
        })

    hist = pd.DataFrame(snapshots).sort_values("commit_timestamp_utc").reset_index(drop=True)

    introductions = []
    running_max = None
    for _, r in hist.iterrows():
        p = r["latest_observation_period"]
        if running_max is None:
            running_max = p
            continue  # left-censored by the API window
        if p > running_max:
            first_seen = pd.Timestamp(r["commit_timestamp_utc"])
            next_start = (p + 1).start_time.tz_localize("UTC")
            lag_hours = (first_seen - next_start).total_seconds() / 3600.0
            introductions.append({
                "observation_period": str(p),
                "first_seen_commit_timestamp_utc": first_seen.isoformat(),
                "first_seen_commit_sha": r["sha"],
                "file_sha256": r["file_sha256"],
                "next_month_start_utc": next_start.isoformat(),
                "release_lag_hours_after_next_month_start": lag_hours,
                "strict_pre_target_available": bool(lag_hours <= 0.0),
            })
            running_max = p
        elif p < running_max:
            # Preserve source reversions as an audit event but do not reset the
            # running maximum / first-seen history.
            continue

    intro = pd.DataFrame(introductions)
    if len(intro) < 4:
        raise RuntimeError(f"Need >=4 uncensored Gold introductions, got {len(intro)}")

    # Use the most recent up to six introductions for the live transport audit.
    intro = intro.tail(6).reset_index(drop=True)
    exact_ready = bool(intro["strict_pre_target_available"].all())
    return intro, hist.sort_values("commit_timestamp_utc", ascending=False), exact_ready

def audit_rtdsm(now_utc: pd.Timestamp):
    xlsx_url, landing_hash = VINTAGE.discover_official_xlsx(
        VINTAGE.IPT_PAGE, "iptMvMd.xlsx"
    )
    raw = VINTAGE.STATE_MOD.fetch_bytes(xlsx_url, timeout=120)
    long_df, schema, sheet_names = VINTAGE.parse_rtdsm_workbook(raw)

    current_month = now_utc.to_period("M")
    next_forecast_month = current_month + 1
    target_obs = next_forecast_month - 2
    rt = VINTAGE.realtime_yoy(long_df, next_forecast_month, target_obs)

    row = {
        "run_timestamp_utc": now_utc.isoformat(),
        "next_forecast_month_probe": str(next_forecast_month),
        "required_ipt_observation_period": str(target_obs),
        "selected_vintage_period": (
            str(rt["vintage_period"]) if rt["vintage_period"] is not None else ""
        ),
        "rt_ipt_yoy_available": bool(pd.notna(rt["yoy"])),
        "last_workbook_vintage": str(long_df["vintage_period"].max()),
        "workbook_sha256": hashlib.sha256(raw).hexdigest(),
        "landing_page_sha256": landing_hash,
        "workbook_url": xlsx_url,
        "parsed_cells": int(len(long_df)),
        "vintage_count": int(long_df["vintage_period"].nunique()),
        "sheet_count": int(len(sheet_names)),
    }
    return pd.DataFrame([row]), row

def main():
    now_utc = pd.Timestamp(datetime.now(timezone.utc))

    gold_intro, gold_hist, gold_exact_ready = audit_gold_release_timing()
    rt_df, rt = audit_rtdsm(now_utc)

    latest_snapshot = gold_hist.iloc[0]
    current_month = now_utc.to_period("M")
    next_forecast_month = current_month + 1
    required_gold_period = next_forecast_month - 1
    latest_gold_period = latest_snapshot["latest_observation_period"]

    gold_next_probe_ready = bool(latest_gold_period >= required_gold_period)
    rt_next_probe_ready = bool(rt["rt_ipt_yoy_available"])

    transport_status = (
        "EXACT_LIVE_TRANSPORT_READY"
        if gold_exact_ready
        else "SOURCE_TIMING_REPAIR_REQUIRED"
    )
    current_probe_status = (
        "CURRENT_NEXT_MONTH_INPUTS_READY"
        if gold_next_probe_ready and rt_next_probe_ready
        else "CURRENT_SOURCE_REFRESH_PENDING"
    )

    positive_lags = int(
        (gold_intro["release_lag_hours_after_next_month_start"] > 0).sum()
    )
    max_lag = float(gold_intro["release_lag_hours_after_next_month_start"].max())
    min_lag = float(gold_intro["release_lag_hours_after_next_month_start"].min())

    hard_fail = (
        len(gold_intro) < 4
        or rt["parsed_cells"] < 10000
        or rt["vintage_count"] < 100
        or positive_lags < 0
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010",
        "run_timestamp_utc": now_utc.isoformat(),
        "gold_recent_introductions_audited": int(len(gold_intro)),
        "gold_positive_release_lag_cases": positive_lags,
        "gold_all_strict_pre_target_ready": gold_exact_ready,
        "gold_min_release_lag_hours": min_lag,
        "gold_max_release_lag_hours": max_lag,
        "gold_latest_observation_period": str(latest_gold_period),
        "gold_required_period_for_next_month_probe": str(required_gold_period),
        "gold_next_month_probe_ready_now": gold_next_probe_ready,
        "rtdsm_last_vintage": rt["last_workbook_vintage"],
        "rtdsm_required_observation_for_next_month_probe": rt["required_ipt_observation_period"],
        "rtdsm_next_month_probe_yoy_available": rt_next_probe_ready,
        "transport_status": transport_status,
        "current_probe_status": current_probe_status,
        "prospective_predictions_created": 0,
        "forecast_performance_evaluated": False,
        "oos008_spec_changed": False,
        "deployment_status": "NOT_DEPLOYABLE",
    }

    gold_intro.to_csv(OUT / "GOLD_SOURCE_RELEASE_AUDIT.csv", index=False)
    gold_hist[[
        "sha","commit_timestamp_utc","file_sha256","latest_observation_period"
    ]].to_csv(OUT / "GOLD_SOURCE_COMMIT_SNAPSHOTS.csv", index=False)
    rt_df.to_csv(OUT / "RTDSM_READINESS.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")

    source_rows = [
        {
            "source_object": "Gold monthly source and commit history",
            "source": "datasets/gold-prices / World Bank Commodity Markets",
            "url": "https://github.com/datasets/gold-prices",
            "source_detail_url": GOLD_SOURCE_PAGE,
            "raw_committed": False,
        },
        {
            "source_object": "Real-time industrial production vintages",
            "source": "Federal Reserve Bank of Philadelphia RTDSM IPT",
            "url": VINTAGE.IPT_PAGE,
            "source_detail_url": rt["workbook_url"],
            "raw_committed": False,
        },
    ]
    pd.DataFrame(source_rows).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)

    lines = [
        "# FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010 — Report",
        "",
        "**TIMING / DATA-PROVENANCE AUDIT ONLY / NO NEW FORECAST PERFORMANCE EVIDENCE**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- exact OOS-008 live transport status: **{transport_status}**",
        f"- current next-month source probe: **{current_probe_status}**",
        "",
        "## Gold release timing",
        "",
        f"- recent uncensored monthly introductions audited: {len(gold_intro)}",
        f"- introductions arriving after the following month had already begun: {positive_lags}/{len(gold_intro)}",
        f"- release-lag range relative to next-month start: {min_lag:.1f} to {max_lag:.1f} hours",
        f"- latest source month at run time: {latest_gold_period}",
        f"- month required for the current next-month probe ({next_forecast_month}): {required_gold_period}",
        "",
        gold_intro.to_markdown(index=False),
        "",
        "The historical Gold source contract fails strict pre-target transport if its required M-1 monthly value is first published after month M has begun.",
        "",
        "## RTDSM current readiness",
        "",
        rt_df.to_markdown(index=False),
        "",
        "A current RTDSM gap is treated as a refresh dependency, not automatically as a permanent structural failure.",
        "",
        "## Research decision",
        "",
        "- No prediction is issued.",
        "- OOS-008 and PROSPECTIVE-SHADOW-009 remain unchanged.",
        "- If exact Gold source timing fails, a source bridge or target-timing amendment must be separately frozen before testing.",
        "- Any replacement specification starts with no inherited prospective validation evidence.",
    ]
    (OUT / "FED_CYCLE_PROSPECTIVE_INPUT_TIMING_010_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    if hard_fail:
        raise SystemExit("FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010 audit QC failed")

    print(json.dumps(qc, indent=2))

if __name__ == "__main__":
    main()
