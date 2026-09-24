#!/usr/bin/env python3
"""
FED-CYCLE-PROSPECTIVE-SHADOW-009
Append-only prospective shadow architecture gate.

This runner deliberately does not issue a prediction until a genuinely new
tightening leg satisfies the frozen FED-CYCLE-PATH-001 eligibility rule.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_prospective_shadow_v1"
OUT.mkdir(parents=True, exist_ok=True)

POLICY_FILE = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_POLICY_CHANGE_REGISTRY.csv"
BROAD_FILE = ROOT / "results" / "fed_cycle_state_panel_v2" / "BROAD_EPISODE_REGISTRY.csv"
REGISTRY_FILE = OUT / "PREDICTION_REGISTRY.csv"

MIN_HIKES = 2
MIN_CUM_HIKE_BP = 50.0

PREDICTION_COLUMNS = [
    "prediction_id","episode_id","cycle_id","forecast_month","issue_timestamp_utc",
    "target_end_month","model_spec_sha256","code_commit_sha","training_cutoff_month",
    "training_episode_ids","training_rows","gold_source_commit","gold_source_sha256",
    "rt_ipt_source_sha256","rt_ipt_vintage_period","gold_ret_3m_lagged",
    "gold_ret_6m_lagged","gold_vol_6m_lagged","cycle_age_months","rt_ipt_yoy",
    "pred_b0","pred_b1","pred_b2","pred_m3","realized_target",
    "realized_available_date","realized_source_sha256","error_b0","error_b1",
    "error_b2","error_m3","status"
]

SPEC = {
    "module": "FED-CYCLE-PROSPECTIVE-SHADOW-009",
    "version": "v1",
    "frozen_date": "2026-09-24",
    "upstream_module": "FED-CYCLE-GOLD-OOS-008",
    "upstream_consumed_oos": ["B04","B05","B06","B07"],
    "target": "GOLD_FWD_6M_RET",
    "models": {
        "B0_HIST_MEAN": [],
        "B1_GOLD_HISTORY": [
            "GOLD_RET_3M_LAGGED","GOLD_RET_6M_LAGGED","GOLD_VOL_6M_LAGGED"
        ],
        "B2_GOLD_PLUS_CYCLE_AGE": [
            "GOLD_RET_3M_LAGGED","GOLD_RET_6M_LAGGED","GOLD_VOL_6M_LAGGED",
            "CYCLE_AGE_MONTHS"
        ],
        "M3_PLUS_REALTIME_IPT": [
            "GOLD_RET_3M_LAGGED","GOLD_RET_6M_LAGGED","GOLD_VOL_6M_LAGGED",
            "CYCLE_AGE_MONTHS","RT_IPT_YOY"
        ]
    },
    "cycle_eligibility": {
        "min_positive_changes": MIN_HIKES,
        "min_cumulative_hike_bp": MIN_CUM_HIKE_BP,
        "same_as": "FED-CYCLE-PATH-001"
    },
    "refit_policy": "FIT_ONCE_AT_NEW_ELIGIBLE_BROAD_EPISODE_USING_PRIOR_EPISODES_ONLY",
    "active_episode_outcomes_in_training": False,
    "within_episode_refit": False,
    "retroactive_predictions": False,
    "training_weights": "EACH_BROAD_EPISODE_TOTAL_1_THEN_EQUAL_CYCLE_TOTAL_THEN_EQUAL_ROWS",
    "standardization": "TRAINING_ONLY",
    "live_models": ["B0_HIST_MEAN","B1_GOLD_HISTORY","B2_GOLD_PLUS_CYCLE_AGE","M3_PLUS_REALTIME_IPT"],
    "d4_live": False,
    "deployment_status": "NOT_DEPLOYABLE"
}

def canonical_hash(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

SPEC_HASH = canonical_hash(SPEC)

def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def parse_iso(s):
    return date.fromisoformat(str(s)[:10])

def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)

def next_month_ym(d):
    y, m = d.year, d.month
    if m == 12:
        return f"{y+1:04d}-01"
    return f"{y:04d}-{m+1:02d}"

def ensure_prediction_registry():
    if REGISTRY_FILE.exists():
        with REGISTRY_FILE.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
        if not rows:
            raise RuntimeError("Existing prediction registry is empty without header")
        if rows[0] != PREDICTION_COLUMNS:
            raise RuntimeError("Prediction registry schema mismatch")
        return max(0, len(rows) - 1)

    with REGISTRY_FILE.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow(PREDICTION_COLUMNS)
    return 0

def main():
    policy = read_csv(POLICY_FILE)
    broad = read_csv(BROAD_FILE)
    if not policy:
        raise RuntimeError("Policy registry is empty")
    if not broad:
        raise RuntimeError("Broad episode registry is empty")

    dates = [parse_iso(r["event_date"]) for r in policy]
    duplicate_dates = len(dates) - len(set(dates))
    unsorted = int(dates != sorted(dates))

    sign_label_violations = 0
    for r in policy:
        bp = float(r["change_bp"])
        direction = r["direction"].strip().upper()
        if bp > 0 and direction != "HIKE":
            sign_label_violations += 1
        if bp < 0 and direction != "CUT":
            sign_label_violations += 1

    trailing = []
    for r in reversed(policy):
        if r["direction"].strip().upper() == "HIKE":
            trailing.append(r)
        else:
            break
    trailing = list(reversed(trailing))

    n_hikes = len(trailing)
    cumulative = sum(float(r["change_bp"]) for r in trailing)
    qualifies = n_hikes >= MIN_HIKES and cumulative >= MIN_CUM_HIKE_BP

    max_bid = max(int(r["broad_episode_id"][1:]) for r in broad)
    last_broad_first = max(parse_iso(r["first_hike_max"]) for r in broad)

    if trailing:
        candidate_first = parse_iso(trailing[0]["event_date"])
        candidate_last = parse_iso(trailing[-1]["event_date"])
        gap_months = months_between(last_broad_first, candidate_first)
        if gap_months > 18:
            would_be_bid = f"B{max_bid+1:02d}"
        else:
            would_be_bid = f"B{max_bid:02d}"
        earliest_month = next_month_ym(candidate_last) if qualifies else ""
        target_before = trailing[0]["target_before"]
        target_after = trailing[-1]["target"]
    else:
        candidate_first = candidate_last = None
        gap_months = None
        would_be_bid = ""
        earliest_month = ""
        target_before = target_after = ""

    registry_rows = ensure_prediction_registry()

    # This v1 runner is a gate/architecture runner only. It must never create
    # a prospective prediction automatically.
    automatic_prediction_rows_created = 0

    current_status = (
        "ELIGIBLE_FOR_SEPARATE_PROSPECTIVE_ISSUANCE_STEP"
        if qualifies else
        "ARMED_WAITING_FROZEN_CYCLE_QUALIFICATION"
    )

    gate_row = {
        "candidate_first_hike": candidate_first.isoformat() if candidate_first else "",
        "candidate_last_observed_hike": candidate_last.isoformat() if candidate_last else "",
        "n_hikes": n_hikes,
        "cumulative_hike_bp": f"{cumulative:.6f}",
        "target_before_first_hike": target_before,
        "target_after_last_observed_hike": target_after,
        "qualifies_frozen_cycle_rule": str(bool(qualifies)),
        "months_from_last_broad_first_hike": "" if gap_months is None else gap_months,
        "prospective_broad_episode_if_qualified": would_be_bid,
        "earliest_forecast_month_if_qualified_now": earliest_month,
        "status": current_status
    }

    with (OUT / "PROSPECTIVE_CYCLE_GATE.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(gate_row.keys()))
        w.writeheader()
        w.writerow(gate_row)

    model_spec = dict(SPEC)
    model_spec["model_spec_sha256"] = SPEC_HASH
    (OUT / "MODEL_SPEC.json").write_text(
        json.dumps(model_spec, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    expected_current_candidate = (
        candidate_first is not None
        and candidate_first.isoformat() == "2026-09-16"
        and n_hikes == 1
        and abs(cumulative - 25.0) < 1e-9
        and not qualifies
    )

    hard_fail = (
        duplicate_dates != 0
        or unsorted != 0
        or sign_label_violations != 0
        or automatic_prediction_rows_created != 0
        or (candidate_first is not None and candidate_first.year == 2026 and not expected_current_candidate)
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-PROSPECTIVE-SHADOW-009",
        "model_spec_sha256": SPEC_HASH,
        "policy_rows": len(policy),
        "duplicate_policy_event_dates": duplicate_dates,
        "unsorted_policy_registry": unsorted,
        "direction_sign_violations": sign_label_violations,
        "current_candidate_first_hike": candidate_first.isoformat() if candidate_first else None,
        "current_candidate_hikes": n_hikes,
        "current_candidate_cumulative_hike_bp": cumulative,
        "current_candidate_qualifies": qualifies,
        "prospective_broad_episode_if_qualified": would_be_bid or None,
        "prediction_registry_rows": registry_rows,
        "automatic_prediction_rows_created": automatic_prediction_rows_created,
        "retroactive_prediction_allowed": False,
        "within_episode_refit_allowed": False,
        "historical_oos_consumed": ["B04","B05","B06","B07"],
        "historical_oos_spec_tuning_allowed": False,
        "evidence_status": "PROSPECTIVE_ARCHITECTURE_FROZEN_ARMED_NO_NEW_FORECAST_EVIDENCE",
        "deployment_status": "NOT_DEPLOYABLE"
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# FED-CYCLE-PROSPECTIVE-SHADOW-009 — Current Gate",
        "",
        "**PROSPECTIVE ARCHITECTURE FROZEN / ARMED / NO NEW FORECAST EVIDENCE YET / NOT DEPLOYABLE**",
        "",
        f"- model spec SHA256: `{SPEC_HASH}`",
        f"- current edge candidate FIRST_HIKE: {gate_row['candidate_first_hike'] or 'none'}",
        f"- observed hikes in current edge run: {n_hikes}",
        f"- cumulative tightening in current edge run: {cumulative:.0f} bp",
        f"- frozen qualification rule: >= {MIN_HIKES} hikes and >= {MIN_CUM_HIKE_BP:.0f} bp",
        f"- qualifies now: **{qualifies}**",
        f"- prospective broad episode if it later qualifies: {would_be_bid or 'n/a'}",
        f"- prospective prediction rows currently registered: {registry_rows}",
        "",
        "No prediction is issued by this gate runner. A separate prospective issuance step is allowed only after the frozen cycle rule is satisfied and no retroactive month may be backfilled.",
        "",
        "B04-B07 remain consumed OOS evidence for OOS-008 and are not available for specification tuning."
    ]
    (OUT / "STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-PROSPECTIVE-SHADOW-009 QC failed")

    print(json.dumps(qc, indent=2))

if __name__ == "__main__":
    main()
