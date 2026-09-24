#!/usr/bin/env python3
"""
FED-CYCLE-PROSPECTIVE-ISSUANCE-013
Fail-closed append-only issuance gate for the frozen GCF-012 model.
"""
from __future__ import annotations

import calendar
import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_prospective_gcf_v1"

SPEC_FILE = OUT / "MODEL_SPEC.json"
MODEL_FILE = OUT / "FROZEN_TRAINING_MODEL.json"
REGISTRY_FILE = OUT / "PREDICTION_REGISTRY.csv"
POLICY_FILE = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_POLICY_CHANGE_REGISTRY.csv"
BRIDGE_QC_FILE = ROOT / "results" / "fed_cycle_gold_live_bridge_v1" / "QC.json"

EXPECTED_SPEC_SHA = "f3d3eff3020af41665da93151962d0a488b14f642bf3e7e68dcf16cb156787b4"
EXPECTED_MODEL_SHA = "96520e9316a0cbcc18085f0dfa2d7432fab9892d715e7893fcf5ad2b172ba50d"
BRIDGE_ID = "FED-CYCLE-GOLD-LIVE-BRIDGE-011"

PREDICTION_COLUMNS = [
    "prediction_id","episode_id","forecast_month","issue_timestamp_utc",
    "spec_sha256","training_model_sha256","bridge_id",
    "gold_proxy_source_sha256","rt_ipt_source_sha256","rt_ipt_vintage_period",
    "gold_ret_3m_lagged","gold_ret_6m_lagged","gold_vol_6m_lagged",
    "cycle_age_months","rt_ipt_yoy",
    "pred_b0","pred_b1","pred_b2","pred_m3",
    "target_end_month","realized_target","realized_available_date",
    "error_b0","error_b1","error_b2","error_m3","status"
]

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

PATHMOD = load_module(
    ROOT / "scripts" / "run_fed_cycle_path_v1.py",
    "path_for_prospective_issuance",
)
VINTAGE = load_module(
    ROOT / "scripts" / "run_fed_cycle_vintage_audit_v1.py",
    "vintage_for_prospective_issuance",
)

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def read_policy():
    with POLICY_FILE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def registry_rows():
    if not REGISTRY_FILE.exists():
        raise RuntimeError("012 prediction registry missing")
    with REGISTRY_FILE.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    with REGISTRY_FILE.open("r", encoding="utf-8", newline="") as f:
        header = next(csv.reader(f))
    if header != PREDICTION_COLUMNS:
        raise RuntimeError("Prediction registry schema mismatch")
    ids = [r["prediction_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate prediction IDs already exist")
    return rows

def qualification_state(policy):
    trailing = []
    for r in reversed(policy):
        if r["direction"].strip().upper() == "HIKE":
            trailing.append(r)
        else:
            break
    trailing = list(reversed(trailing))
    cumulative = 0.0
    qualification_date = None
    for i, r in enumerate(trailing, start=1):
        cumulative += float(r["change_bp"])
        if qualification_date is None and i >= 2 and cumulative >= 50.0:
            qualification_date = pd.Timestamp(r["event_date"])
    return {
        "rows": trailing,
        "n_hikes": len(trailing),
        "cumulative_hike_bp": float(sum(float(r["change_bp"]) for r in trailing)),
        "first_hike": pd.Timestamp(trailing[0]["event_date"]) if trailing else None,
        "qualification_date": qualification_date,
        "qualifies": qualification_date is not None,
    }

def last_weekday_date(period: pd.Period):
    last_day = calendar.monthrange(period.year, period.month)[1]
    d = pd.Timestamp(year=period.year, month=period.month, day=last_day)
    while d.weekday() >= 5:
        d -= pd.Timedelta(days=1)
    return d.normalize()

def gold_features(forecast_month: pd.Period, now_utc: pd.Timestamp):
    required = forecast_month - 1
    # Conservative no-partial-month operational rule.
    last_calendar_day = calendar.monthrange(required.year, required.month)[1]
    required_last_date = pd.Timestamp(
        year=required.year, month=required.month, day=last_calendar_day, tz="UTC"
    )
    if now_utc.date() != required_last_date.date():
        return None, {
            "ready": False,
            "reason": "REQUIRED_GOLD_MONTH_NOT_AT_FINAL_CALENDAR_DAY",
            "required_period": str(required),
        }

    daily, meta = PATHMOD.fetch_yahoo_chart("GC=F")
    daily["period"] = daily["date"].dt.to_period("M")
    monthly = (
        daily.groupby("period")
        .agg(price=("value","mean"), n=("value","count"), last_date=("date","max"))
        .reset_index()
    )
    monthly = monthly[monthly["n"] >= 10].copy()
    pmap = dict(zip(monthly["period"], monthly["price"].astype(float)))
    nmap = dict(zip(monthly["period"], monthly["n"].astype(int)))
    dmap = dict(zip(monthly["period"], pd.to_datetime(monthly["last_date"])))

    need = [required-k for k in range(0,7)]
    if any(p not in pmap for p in need):
        return None, {"ready": False, "reason": "MISSING_GOLD_PROXY_MONTH", "required_period": str(required)}

    conservative_floor = last_weekday_date(required) - pd.Timedelta(days=3)
    if pd.Timestamp(dmap[required]).normalize() < conservative_floor:
        return None, {"ready": False, "reason": "GOLD_PROXY_MONTH_COMPLETION_UNCERTAIN", "required_period": str(required)}

    prices = np.array([pmap[required-k] for k in range(6,-1,-1)], float)
    log_changes = np.diff(np.log(prices))
    feat = {
        "GOLD_RET_3M_LAGGED": float(pmap[required] / pmap[required-3] - 1.0),
        "GOLD_RET_6M_LAGGED": float(pmap[required] / pmap[required-6] - 1.0),
        "GOLD_VOL_6M_LAGGED": float(np.std(log_changes, ddof=1)),
    }
    return feat, {
        "ready": True,
        "reason": "READY",
        "required_period": str(required),
        "source_sha256": meta["sha256"],
        "required_month_daily_obs": nmap[required],
        "required_month_last_daily_date": str(pd.Timestamp(dmap[required]).date()),
    }

def rt_ipt_feature(forecast_month: pd.Period):
    xlsx_url, landing_hash = VINTAGE.discover_official_xlsx(VINTAGE.IPT_PAGE, "iptMvMd.xlsx")
    raw = VINTAGE.STATE_MOD.fetch_bytes(xlsx_url, timeout=120)
    long_df, schema, sheet_names = VINTAGE.parse_rtdsm_workbook(raw)
    target_obs = forecast_month - 2
    rt = VINTAGE.realtime_yoy(long_df, forecast_month, target_obs)
    yoy = rt["yoy"]
    if yoy is None or not np.isfinite(float(yoy)):
        return None, {
            "ready": False,
            "reason": "RT_IPT_YOY_UNAVAILABLE",
            "target_observation": str(target_obs),
            "last_vintage": str(long_df["vintage_period"].max()),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
        }
    return float(yoy), {
        "ready": True,
        "reason": "READY",
        "target_observation": str(target_obs),
        "selected_vintage": str(rt["vintage_period"]),
        "last_vintage": str(long_df["vintage_period"].max()),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
    }

def predict(model, model_name, feature_values):
    if model_name == "B0_HIST_MEAN":
        return float(model[model_name]["prediction"])
    m = model[model_name]
    coef = np.asarray(m["coefficients_intercept_then_standardized_features"], float)
    means = np.asarray(m["weighted_means"], float)
    sds = np.asarray(m["weighted_sds"], float)
    active = np.asarray(m["active"], bool)
    x = np.asarray([feature_values[f] for f in m["features"]], float)
    z = np.zeros_like(x)
    z[active] = (x[active] - means[active]) / sds[active]
    return float(coef[0] + np.dot(coef[1:], z))

def append_row(row):
    # Re-read immediately before append to make duplicate check fail closed.
    rows = registry_rows()
    if any(r["prediction_id"] == row["prediction_id"] for r in rows):
        raise RuntimeError("Duplicate prediction ID; refusing overwrite")
    with REGISTRY_FILE.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PREDICTION_COLUMNS)
        w.writerow(row)

def main():
    now = pd.Timestamp(datetime.now(timezone.utc))
    current_month = now.to_period("M")
    candidate_forecast_month = current_month + 1
    forecast_start = candidate_forecast_month.start_time.tz_localize("UTC")

    spec = read_json(SPEC_FILE)
    model = read_json(MODEL_FILE)
    bridge = read_json(BRIDGE_QC_FILE)
    reg_before = registry_rows()

    hashes_ok = (
        spec.get("spec_sha256") == EXPECTED_SPEC_SHA
        and model.get("training_model_sha256") == EXPECTED_MODEL_SHA
    )
    bridge_ok = bridge.get("bridge_status") == "PROXY_FEATURE_BRIDGE_CANDIDATE"

    cycle = qualification_state(read_policy())
    earliest = (
        cycle["qualification_date"].to_period("M") + 1
        if cycle["qualification_date"] is not None else None
    )

    reasons = []
    if not hashes_ok:
        reasons.append("UPSTREAM_HASH_MISMATCH")
    if not bridge_ok:
        reasons.append("BRIDGE_STATUS_NOT_APPROVED")
    if not cycle["qualifies"]:
        reasons.append("WAITING_CYCLE_QUALIFICATION")
    if earliest is not None and candidate_forecast_month < earliest:
        reasons.append("FORECAST_MONTH_PRECEDES_ELIGIBILITY")
    if now >= forecast_start:
        reasons.append("ISSUE_TIME_NOT_BEFORE_FORECAST_MONTH")

    episode_id = "B08" if cycle["qualifies"] else ""
    prediction_id = (
        f"GCF012_{episode_id}_{candidate_forecast_month}"
        if episode_id else ""
    )
    if prediction_id and any(r["prediction_id"] == prediction_id for r in reg_before):
        reasons.append("DUPLICATE_PREDICTION_ID")

    gold_feat = None
    gold_meta = {"ready": False, "reason": "NOT_CHECKED_BECAUSE_PRECONDITION_FAILED"}
    rt_value = None
    rt_meta = {"ready": False, "reason": "NOT_CHECKED_BECAUSE_PRECONDITION_FAILED"}

    # Only acquire live inputs after structural eligibility passes.
    structural_ok = not reasons
    if structural_ok:
        gold_feat, gold_meta = gold_features(candidate_forecast_month, now)
        if not gold_meta["ready"]:
            reasons.append(gold_meta["reason"])
        rt_value, rt_meta = rt_ipt_feature(candidate_forecast_month)
        if not rt_meta["ready"]:
            reasons.append(rt_meta["reason"])

    issued = 0
    if not reasons:
        cycle_age = int(candidate_forecast_month.ordinal - cycle["first_hike"].to_period("M").ordinal)
        feat = {
            **gold_feat,
            "CYCLE_AGE_MONTHS": cycle_age,
            "RT_IPT_YOY": float(rt_value),
        }
        preds = {
            "pred_b0": predict(model, "B0_HIST_MEAN", feat),
            "pred_b1": predict(model, "B1_GOLD_HISTORY", feat),
            "pred_b2": predict(model, "B2_GOLD_PLUS_CYCLE_AGE", feat),
            "pred_m3": predict(model, "M3_PLUS_REALTIME_IPT", feat),
        }
        row = {k: "" for k in PREDICTION_COLUMNS}
        row.update({
            "prediction_id": prediction_id,
            "episode_id": episode_id,
            "forecast_month": str(candidate_forecast_month),
            "issue_timestamp_utc": now.isoformat(),
            "spec_sha256": EXPECTED_SPEC_SHA,
            "training_model_sha256": EXPECTED_MODEL_SHA,
            "bridge_id": BRIDGE_ID,
            "gold_proxy_source_sha256": gold_meta["source_sha256"],
            "rt_ipt_source_sha256": rt_meta["source_sha256"],
            "rt_ipt_vintage_period": rt_meta["selected_vintage"],
            "gold_ret_3m_lagged": feat["GOLD_RET_3M_LAGGED"],
            "gold_ret_6m_lagged": feat["GOLD_RET_6M_LAGGED"],
            "gold_vol_6m_lagged": feat["GOLD_VOL_6M_LAGGED"],
            "cycle_age_months": feat["CYCLE_AGE_MONTHS"],
            "rt_ipt_yoy": feat["RT_IPT_YOY"],
            **preds,
            "target_end_month": str(candidate_forecast_month + 5),
            "status": "ISSUED_UNREALIZED",
        })
        append_row(row)
        issued = 1

    reg_after = registry_rows()
    expected_growth = len(reg_before) + issued
    append_only_ok = len(reg_after) == expected_growth

    readiness = {
        "run_timestamp_utc": now.isoformat(),
        "candidate_forecast_month": str(candidate_forecast_month),
        "forecast_month_start_utc": forecast_start.isoformat(),
        "spec_hash_ok": hashes_ok,
        "bridge_status_ok": bridge_ok,
        "cycle_first_hike": str(cycle["first_hike"].date()) if cycle["first_hike"] is not None else "",
        "cycle_hikes": cycle["n_hikes"],
        "cycle_cumulative_hike_bp": cycle["cumulative_hike_bp"],
        "cycle_qualifies": cycle["qualifies"],
        "qualification_date": str(cycle["qualification_date"].date()) if cycle["qualification_date"] is not None else "",
        "earliest_eligible_forecast_month": str(earliest) if earliest is not None else "",
        "gold_input_ready": gold_meta.get("ready", False),
        "gold_input_status": gold_meta.get("reason", ""),
        "rt_ipt_ready": rt_meta.get("ready", False),
        "rt_ipt_status": rt_meta.get("reason", ""),
        "registry_rows_before": len(reg_before),
        "predictions_issued_this_run": issued,
        "registry_rows_after": len(reg_after),
        "refusal_reasons": ";".join(reasons),
        "status": "ISSUED" if issued else (
            "WAITING_CYCLE_QUALIFICATION"
            if "WAITING_CYCLE_QUALIFICATION" in reasons
            else "REFUSED"
        ),
    }
    pd.DataFrame([readiness]).to_csv(OUT / "ISSUANCE_READINESS.csv", index=False)

    hard_fail = (
        not hashes_ok
        or not bridge_ok
        or not append_only_ok
        or (not cycle["qualifies"] and issued != 0)
        or (issued and now >= forecast_start)
    )
    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-PROSPECTIVE-ISSUANCE-013",
        **readiness,
        "append_only_registry_growth_ok": append_only_ok,
        "model_fitting_performed": False,
        "retroactive_month_search_performed": False,
        "raw_source_files_committed": False,
        "forecast_performance_evaluated": False,
        "deployment_status": "NOT_DEPLOYABLE",
    }
    (OUT / "ISSUANCE_QC.json").write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# FED-CYCLE-PROSPECTIVE-ISSUANCE-013 — Current Issuance Gate",
        "",
        "**APPEND-ONLY PROSPECTIVE ISSUANCE / NO PERFORMANCE EVIDENCE YET**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- status: **{readiness['status']}**",
        f"- candidate forecast month: {candidate_forecast_month}",
        f"- current cycle: {cycle['n_hikes']} hike(s), {cycle['cumulative_hike_bp']:.0f} bp",
        f"- cycle qualifies: **{cycle['qualifies']}**",
        f"- predictions issued this run: {issued}",
        f"- registry rows after run: {len(reg_after)}",
        f"- refusal reasons: {readiness['refusal_reasons'] or 'none'}",
        "",
        "The issuer cannot fit or change the model. It either appends one immutable row after every frozen gate passes or refuses issuance.",
    ]
    (OUT / "ISSUANCE_STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-PROSPECTIVE-ISSUANCE-013 QC failed")

    print(json.dumps(qc, indent=2))

if __name__ == "__main__":
    main()
