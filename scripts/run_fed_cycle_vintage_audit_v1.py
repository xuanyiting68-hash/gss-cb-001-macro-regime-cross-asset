#!/usr/bin/env python3
"""
FED-CYCLE-VINTAGE-AUDIT-007
Real-time Philadelphia Fed RTDSM industrial-production revision audit.

Reference:
research/FED_CYCLE_VINTAGE_AUDIT_007_LOCK.md
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_vintage_audit_v1"
OUT.mkdir(parents=True, exist_ok=True)

IPT_PAGE = "https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/ipt"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


STATE_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py", "state_panel_v2_vintage")

EVENT_FILE = ROOT / "results" / "fed_cycle_state_v1" / "STATE_EVENT_PANEL.csv"
PANEL_FILE = ROOT / "results" / "fed_cycle_state_panel_v2" / "MONTHLY_STATE_PANEL.csv"


def discover_official_xlsx(page_url: str, filename_fragment: str):
    raw = STATE_MOD.fetch_bytes(page_url, timeout=60)
    soup = BeautifulSoup(raw, "html.parser")
    urls = []
    for a in soup.find_all("a", href=True):
        href = str(a["href"])
        if filename_fragment.lower() in href.lower():
            urls.append(urljoin(page_url, href))
    if not urls:
        raise RuntimeError(f"Could not discover {filename_fragment} on official page")
    url = urls[0]
    if "philadelphiafed.org" not in url.lower():
        raise RuntimeError(f"Non-official RTDSM URL: {url}")
    return url, hashlib.sha256(raw).hexdigest()


def parse_vintage_name(value):
    s = str(value).strip().upper().replace(" ", "")
    m = re.fullmatch(r"IPT(\d{2})M(\d{1,2})", s)
    if not m:
        return None
    yy, mm = int(m.group(1)), int(m.group(2))
    year = 1900 + yy if yy >= 60 else 2000 + yy
    if not 1 <= mm <= 12:
        return None
    return pd.Period(f"{year:04d}-{mm:02d}", freq="M")


def parse_obs_period(value):
    if isinstance(value, (pd.Timestamp, datetime)):
        return pd.Timestamp(value).to_period("M")
    s = str(value).strip().upper().replace(" ", "")
    for pat in [
        r"^(\d{4})[:/-](\d{1,2})$",
        r"^(\d{4})M(\d{1,2})$",
        r"^(\d{4}):M(\d{1,2})$",
    ]:
        m = re.fullmatch(pat, s)
        if m:
            y, mm = int(m.group(1)), int(m.group(2))
            if 1 <= mm <= 12:
                return pd.Period(f"{y:04d}-{mm:02d}", freq="M")
    return None


def parse_rtdsm_workbook(raw: bytes):
    xls = pd.ExcelFile(io.BytesIO(raw), engine="openpyxl")
    records = []
    schema = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None, dtype=object)
        header_row = None
        vint_cols = []

        for r in range(min(40, len(df))):
            hits = []
            for c in range(df.shape[1]):
                vp = parse_vintage_name(df.iat[r, c])
                if vp is not None:
                    hits.append((c, vp))
            if hits:
                header_row = r
                vint_cols = hits
                break

        if header_row is None:
            schema.append({
                "sheet": sheet,
                "header_row": np.nan,
                "vintage_columns": 0,
                "parsed_rows": 0,
                "status": "NO_VINTAGE_HEADER",
            })
            continue

        first_vcol = min(c for c, _ in vint_cols)
        sheet_rows = 0

        for r in range(header_row + 1, len(df)):
            obs = None
            # Search cells left of the first vintage column for observation label.
            for c in range(max(1, first_vcol + 1)):
                obs = parse_obs_period(df.iat[r, c])
                if obs is not None:
                    break
            if obs is None:
                continue

            for c, vp in vint_cols:
                val = pd.to_numeric(pd.Series([df.iat[r, c]]), errors="coerce").iloc[0]
                if pd.isna(val):
                    continue
                records.append({
                    "observation_period": obs,
                    "vintage_period": vp,
                    "value": float(val),
                    "sheet": sheet,
                })
                sheet_rows += 1

        schema.append({
            "sheet": sheet,
            "header_row": int(header_row),
            "vintage_columns": int(len(vint_cols)),
            "parsed_rows": int(sheet_rows),
            "status": "PARSED",
        })

    out = pd.DataFrame(records)
    if out.empty:
        raise RuntimeError(f"RTDSM workbook parsed zero observations; schema={schema}")

    # Duplicate same observation/vintage pairs should agree. Keep last after checking.
    dup = (
        out.groupby(["observation_period", "vintage_period"])["value"]
        .agg(["count", "min", "max"])
        .reset_index()
    )
    conflict = dup[(dup["count"] > 1) & ((dup["max"] - dup["min"]).abs() > 1e-10)]
    if len(conflict):
        raise RuntimeError(f"Conflicting duplicate RTDSM cells: {len(conflict)}")

    out = (
        out.sort_values(["observation_period", "vintage_period", "sheet"])
        .drop_duplicates(["observation_period", "vintage_period"], keep="last")
        .reset_index(drop=True)
    )
    return out, pd.DataFrame(schema), xls.sheet_names


def select_vintage(long_df, info_month: pd.Period):
    max_vintage = info_month - 1
    eligible = long_df.loc[long_df["vintage_period"] <= max_vintage, "vintage_period"]
    if eligible.empty:
        return None
    return eligible.max()


def vintage_value(long_df, vintage, obs):
    x = long_df[
        (long_df["vintage_period"] == vintage)
        & (long_df["observation_period"] == obs)
    ]
    if x.empty:
        return np.nan
    return float(x.iloc[-1]["value"])


def realtime_yoy(long_df, info_month, target_obs):
    vintage = select_vintage(long_df, info_month)
    if vintage is None:
        return {
            "vintage_period": None,
            "target_period": target_obs,
            "base_period": target_obs - 12,
            "target_value": np.nan,
            "base_value": np.nan,
            "yoy": np.nan,
        }
    cur = vintage_value(long_df, vintage, target_obs)
    base = vintage_value(long_df, vintage, target_obs - 12)
    yoy = cur / base - 1.0 if np.isfinite(cur) and np.isfinite(base) and base != 0 else np.nan
    return {
        "vintage_period": vintage,
        "target_period": target_obs,
        "base_period": target_obs - 12,
        "target_value": cur,
        "base_value": base,
        "yoy": yoy,
    }


def growth_state(yoy):
    if not np.isfinite(yoy):
        return "UNAVAILABLE"
    return "STRONG" if yoy >= 0.02 else "WEAK"


def event_audit(long_df):
    ev = pd.read_csv(EVENT_FILE, parse_dates=["event_date"])
    if ev["cycle_id"].duplicated().any():
        raise RuntimeError("Duplicate event cycle_id in STATE_EVENT_PANEL")

    rows = []
    for _, r in ev.iterrows():
        info_month = pd.Timestamp(r["event_date"]).to_period("M")
        target = pd.Period(str(r["state_macro_period"]), freq="M")
        rt = realtime_yoy(long_df, info_month, target)

        current = float(r["INDPRO_YOY_LAG2"])
        rt_yoy = rt["yoy"]
        cur_state = str(r["GROWTH_STATE"])
        rt_state = growth_state(rt_yoy)

        rows.append({
            "cycle_id": r["cycle_id"],
            "event_date": r["event_date"],
            "event_month": str(info_month),
            "target_period": str(target),
            "selected_vintage_period": str(rt["vintage_period"]) if rt["vintage_period"] is not None else "",
            "current_vintage_indpro_yoy": current,
            "realtime_ipt_yoy": rt_yoy,
            "revision_gap_pp": 100.0 * (current - rt_yoy) if np.isfinite(rt_yoy) else np.nan,
            "current_growth_state": cur_state,
            "realtime_growth_state": rt_state,
            "state_flip": bool(rt_state != "UNAVAILABLE" and rt_state != cur_state),
        })
    return pd.DataFrame(rows)


def panel_with_realtime(long_df):
    panel = pd.read_csv(
        PANEL_FILE,
        parse_dates=["panel_month_start", "first_hike", "first_cut"],
    )
    rt_vals = []
    rt_vintages = []

    for _, r in panel.iterrows():
        info_month = pd.Period(str(r["panel_month"]), freq="M")
        target = pd.Period(str(r["macro_state_period"]), freq="M")
        rt = realtime_yoy(long_df, info_month, target)
        rt_vals.append(rt["yoy"])
        rt_vintages.append(str(rt["vintage_period"]) if rt["vintage_period"] is not None else "")

    panel["RT_IPT_YOY"] = rt_vals
    panel["RT_IPT_VINTAGE_PERIOD"] = rt_vintages
    return panel


def exact_test_from_sample(sample, predictor, outcome):
    core = STATE_MOD.regression_core(sample, predictor, outcome)
    if core is None:
        return None
    supported = core["n_cycles"] >= 5 and core["n_broad_clusters"] >= 4
    p_broad = STATE_MOD.exact_signflip_p(core["broad_scores"].to_numpy()) if supported else np.nan
    p_mech = STATE_MOD.exact_signflip_p(core["mech_scores"].to_numpy()) if supported else np.nan

    full_sign = int(np.sign(core["beta"]))
    loo_signs = []
    if supported and full_sign != 0:
        for bid in sorted(core["data"]["broad_episode_id"].unique()):
            sub = core["data"][core["data"]["broad_episode_id"] != bid].copy()
            rc = STATE_MOD.regression_core(sub, predictor, outcome)
            if rc is not None and rc["n_cycles"] >= 4 and rc["n_broad_clusters"] >= 3:
                loo_signs.append(int(np.sign(rc["beta"])))
    stable = bool(loo_signs) and all(s == full_sign for s in loo_signs)

    return {
        "beta": float(core["beta"]),
        "p_broad": p_broad,
        "p_mechanical": p_mech,
        "n_rows": int(core["n_rows"]),
        "n_cycles": int(core["n_cycles"]),
        "n_broad": int(core["n_broad_clusters"]),
        "loo_sign_stable": stable,
        "max_cycle_weight_error": float(np.max(np.abs(core["cycle_weight_sum"].to_numpy() - 1.0))),
        "supported": supported,
    }


def panel_audit(panel):
    rows = []
    for outcome in ["GOLD_FWD_6M_RET", "GOLD_FWD_6M_MDD"]:
        same = panel.dropna(subset=["RT_IPT_YOY", "INDPRO_YOY", outcome]).copy()
        rt = exact_test_from_sample(same, "RT_IPT_YOY", outcome)
        cur = exact_test_from_sample(same, "INDPRO_YOY", outcome)
        if rt is None or cur is None:
            rows.append({
                "outcome": outcome,
                "status": "INSUFFICIENT_SUPPORT",
            })
            continue
        rows.append({
            "outcome": outcome,
            "same_sample_rows": int(len(same)),
            "n_cycles": rt["n_cycles"],
            "n_broad_episodes": rt["n_broad"],
            "realtime_beta_per_1sd": rt["beta"],
            "realtime_p_broad_exact": rt["p_broad"],
            "realtime_p_mechanical_exact": rt["p_mechanical"],
            "realtime_loo_sign_stable": rt["loo_sign_stable"],
            "current_same_sample_beta_per_1sd": cur["beta"],
            "current_same_sample_p_broad_exact": cur["p_broad"],
            "current_same_sample_p_mechanical_exact": cur["p_mechanical"],
            "current_same_sample_loo_sign_stable": cur["loo_sign_stable"],
            "beta_sign_agreement": bool(np.sign(rt["beta"]) == np.sign(cur["beta"])),
            "beta_difference_realtime_minus_current": float(rt["beta"] - cur["beta"]),
            "status": "SUPPORTED_REVISION_AUDIT" if rt["supported"] else "INSUFFICIENT_SUPPORT",
            "max_cycle_weight_error": max(rt["max_cycle_weight_error"], cur["max_cycle_weight_error"]),
        })
    return pd.DataFrame(rows)


def main():
    xlsx_url, landing_hash = discover_official_xlsx(IPT_PAGE, "iptMvMd.xlsx")
    raw = STATE_MOD.fetch_bytes(xlsx_url, timeout=120)
    long_df, schema, sheet_names = parse_rtdsm_workbook(raw)

    ev = event_audit(long_df)
    panel = panel_with_realtime(long_df)
    pa = panel_audit(panel)

    event_available = ev["realtime_ipt_yoy"].notna()
    flips = int(ev.loc[event_available, "state_flip"].sum())
    n_avail = int(event_available.sum())
    abs_gap = ev.loc[event_available, "revision_gap_pp"].abs()

    summary = {
        "event_rows": int(len(ev)),
        "event_realtime_available": n_avail,
        "event_state_flips": flips,
        "event_state_flip_share": float(flips / n_avail) if n_avail else np.nan,
        "event_median_abs_revision_gap_pp": float(abs_gap.median()) if n_avail else np.nan,
        "event_max_abs_revision_gap_pp": float(abs_gap.max()) if n_avail else np.nan,
        "panel_rows": int(len(panel)),
        "panel_realtime_available": int(panel["RT_IPT_YOY"].notna().sum()),
    }

    # QC timing.
    vintage_timing_bad = 0
    target_bad = 0
    for _, r in ev.iterrows():
        if r["selected_vintage_period"]:
            vp = pd.Period(r["selected_vintage_period"], freq="M")
            em = pd.Period(r["event_month"], freq="M")
            if vp >= em:
                vintage_timing_bad += 1
        expected = pd.Period(r["event_month"], freq="M") - 2
        if pd.Period(r["target_period"], freq="M") != expected:
            target_bad += 1

    panel_vintage_bad = 0
    panel_target_bad = 0
    for _, r in panel.iterrows():
        pm = pd.Period(str(r["panel_month"]), freq="M")
        if r["RT_IPT_VINTAGE_PERIOD"]:
            vp = pd.Period(r["RT_IPT_VINTAGE_PERIOD"], freq="M")
            if vp >= pm:
                panel_vintage_bad += 1
        target = pd.Period(str(r["macro_state_period"]), freq="M")
        if target != pm - 2:
            panel_target_bad += 1

    supported_tests = int((pa["status"] == "SUPPORTED_REVISION_AUDIT").sum())
    weight_bad = int(
        (
            (pa["status"] == "SUPPORTED_REVISION_AUDIT")
            & (pd.to_numeric(pa["max_cycle_weight_error"], errors="coerce") > 1e-10)
        ).sum()
    )

    hard_fail = (
        len(ev) != 10
        or vintage_timing_bad != 0
        or target_bad != 0
        or panel_vintage_bad != 0
        or panel_target_bad != 0
        or weight_bad != 0
        or len(long_df) < 10000
        or long_df["vintage_period"].nunique() < 100
        or supported_tests != 2
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-VINTAGE-AUDIT-007",
        "source_host": "www.philadelphiafed.org",
        "workbook_url": xlsx_url,
        "workbook_sha256": hashlib.sha256(raw).hexdigest(),
        "workbook_bytes": len(raw),
        "landing_page_sha256": landing_hash,
        "sheet_count": int(len(sheet_names)),
        "parsed_cells": int(len(long_df)),
        "vintage_count": int(long_df["vintage_period"].nunique()),
        "first_vintage": str(long_df["vintage_period"].min()),
        "last_vintage": str(long_df["vintage_period"].max()),
        **summary,
        "event_vintage_timing_violations": vintage_timing_bad,
        "event_target_period_violations": target_bad,
        "panel_vintage_timing_violations": panel_vintage_bad,
        "panel_target_period_violations": panel_target_bad,
        "supported_panel_revision_tests": supported_tests,
        "cycle_weight_violations": weight_bad,
        "raw_workbook_committed": False,
        "cpi_status": "NOT_SUBSTITUTED_PCPI_IS_DIFFERENT_SERIES",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    pd.DataFrame([{
        "source": "Federal Reserve Bank of Philadelphia RTDSM",
        "variable": "IPT",
        "landing_page": IPT_PAGE,
        "workbook_url": xlsx_url,
        "workbook_sha256": hashlib.sha256(raw).hexdigest(),
        "workbook_bytes": len(raw),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "parsed_cells": len(long_df),
        "vintage_count": long_df["vintage_period"].nunique(),
        "first_vintage": str(long_df["vintage_period"].min()),
        "last_vintage": str(long_df["vintage_period"].max()),
        "raw_committed": False,
    }]).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    schema.to_csv(OUT / "WORKBOOK_SCHEMA_AUDIT.csv", index=False)
    ev.to_csv(OUT / "EVENT_REVISION_AUDIT.csv", index=False)
    panel[[
        "cycle_id","broad_episode_id","panel_month","macro_state_period",
        "INDPRO_YOY","RT_IPT_YOY","RT_IPT_VINTAGE_PERIOD",
        "GOLD_FWD_6M_RET","GOLD_FWD_6M_MDD"
    ]].to_csv(OUT / "PANEL_REALTIME_IPT.csv", index=False)
    pa.to_csv(OUT / "PANEL_REVISION_TESTS.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    report = [
        "# FED-CYCLE-VINTAGE-AUDIT-007 — Report",
        "",
        "**REAL-TIME REVISION AUDIT / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "## Event-level revision summary",
        "",
        f"- events: {summary['event_rows']}",
        f"- real-time IPT available: {summary['event_realtime_available']}",
        f"- growth-state flips: {summary['event_state_flips']}",
        f"- flip share: {summary['event_state_flip_share']:.3f}",
        f"- median absolute YoY revision gap: {summary['event_median_abs_revision_gap_pp']:.3f} pp",
        f"- max absolute YoY revision gap: {summary['event_max_abs_revision_gap_pp']:.3f} pp",
        "",
        ev.to_markdown(index=False),
        "",
        "## Same-sample within-cycle revision tests",
        "",
        pa.to_markdown(index=False),
        "",
        "## CPI boundary",
        "",
        "- Original inflation state uses CPIAUCNS (not seasonally adjusted).",
        "- Philadelphia Fed PCPI is seasonally adjusted and is not substituted.",
        "- This module upgrades only industrial production to an exact RTDSM real-time vintage audit.",
    ]
    (OUT / "FED_CYCLE_VINTAGE_AUDIT_007_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-VINTAGE-AUDIT-007 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
