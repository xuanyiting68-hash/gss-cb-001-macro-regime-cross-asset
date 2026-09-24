#!/usr/bin/env python3
"""
FED-CYCLE-PROSPECTIVE-GCF-012
Freeze a separately versioned prospective model using historical World Bank
Gold training features and a GC=F live feature measurement contract.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_prospective_gcf_v1"
OUT.mkdir(parents=True, exist_ok=True)

TRAIN_FILE = ROOT / "results" / "fed_cycle_gold_oos_v1" / "OOS_FEATURE_PANEL.csv"
BRIDGE_QC_FILE = ROOT / "results" / "fed_cycle_gold_live_bridge_v1" / "QC.json"
POLICY_FILE = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_POLICY_CHANGE_REGISTRY.csv"
REGISTRY_FILE = OUT / "PREDICTION_REGISTRY.csv"

TARGET = "GOLD_FWD_6M_RET"
CANDIDATE_FIRST_HIKE_MONTH = pd.Period("2026-09", freq="M")

MODEL_FEATURES = {
    "B1_GOLD_HISTORY": [
        "GOLD_RET_3M_LAGGED",
        "GOLD_RET_6M_LAGGED",
        "GOLD_VOL_6M_LAGGED",
    ],
    "B2_GOLD_PLUS_CYCLE_AGE": [
        "GOLD_RET_3M_LAGGED",
        "GOLD_RET_6M_LAGGED",
        "GOLD_VOL_6M_LAGGED",
        "CYCLE_AGE_MONTHS",
    ],
    "M3_PLUS_REALTIME_IPT": [
        "GOLD_RET_3M_LAGGED",
        "GOLD_RET_6M_LAGGED",
        "GOLD_VOL_6M_LAGGED",
        "CYCLE_AGE_MONTHS",
        "RT_IPT_YOY",
    ],
}

SPEC = {
    "module": "FED-CYCLE-PROSPECTIVE-GCF-012",
    "version": "v1",
    "frozen_date": "2026-09-24",
    "historical_training_source": "OOS008_WORLD_BANK_GOLD_FEATURE_PANEL",
    "live_gold_measurement": "GC=F_DAILY_CLOSE_CALENDAR_MONTH_MEAN",
    "bridge_dependency": "FED-CYCLE-GOLD-LIVE-BRIDGE-011",
    "bridge_required_status": "PROXY_FEATURE_BRIDGE_CANDIDATE",
    "live_gold_min_daily_obs_per_month": 10,
    "target": TARGET,
    "models": MODEL_FEATURES,
    "baseline": "B0_HISTORICAL_WEIGHTED_MEAN",
    "training_broad_episodes": ["B01","B02","B03","B04","B05","B06","B07"],
    "training_weight_rule": "BROAD_EPISODE_TOTAL_1_THEN_EQUAL_CYCLE_TOTAL_THEN_EQUAL_ROWS",
    "standardization": "TRAINING_ONLY_WEIGHTED_MEAN_SD",
    "prospective_cycle_rule": {"min_hikes": 2, "min_cumulative_hike_bp": 50.0},
    "retroactive_predictions": False,
    "within_episode_refit": False,
    "active_episode_outcomes_in_training": False,
    "oos008_performance_inherited": False,
    "deployment_status": "NOT_DEPLOYABLE",
}

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

def canonical_hash(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

SPEC_HASH = canonical_hash(SPEC)

def hierarchical_weights(df):
    w = pd.Series(index=df.index, dtype=float)
    for bid, gb in df.groupby("broad_episode_id"):
        cycles = sorted(gb["cycle_id"].unique())
        for cid in cycles:
            idx = gb.index[gb["cycle_id"] == cid]
            w.loc[idx] = 1.0 / len(cycles) / len(idx)
    return w.astype(float)

def wmean(x, w):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    return float(np.sum(w * x) / np.sum(w))

def wstd(x, w):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    mu = wmean(x, w)
    return float(math.sqrt(max(0.0, np.sum(w * (x - mu) ** 2) / np.sum(w))))

def fit_wls(train, features, target, weights):
    X = train[features].to_numpy(float)
    y = train[target].to_numpy(float)
    w = weights.loc[train.index].to_numpy(float)

    mus = np.array([wmean(X[:, j], w) for j in range(X.shape[1])], dtype=float)
    sds = np.array([wstd(X[:, j], w) for j in range(X.shape[1])], dtype=float)
    active = sds > 1e-12

    Xz = np.zeros_like(X, dtype=float)
    if active.any():
        Xz[:, active] = (X[:, active] - mus[active]) / sds[active]

    Z = np.column_stack([np.ones(len(Xz)), Xz])
    sw = np.sqrt(w)
    coef, *_ = np.linalg.lstsq(Z * sw[:, None], y * sw, rcond=None)

    return {
        "features": list(features),
        "weighted_means": mus.tolist(),
        "weighted_sds": sds.tolist(),
        "active": active.astype(bool).tolist(),
        "coefficients_intercept_then_standardized_features": coef.tolist(),
    }

def read_policy():
    with POLICY_FILE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def cycle_gate(policy):
    trailing = []
    for r in reversed(policy):
        if r["direction"].strip().upper() == "HIKE":
            trailing.append(r)
        else:
            break
    trailing = list(reversed(trailing))
    n = len(trailing)
    cum = float(sum(float(r["change_bp"]) for r in trailing))
    qualifies = n >= 2 and cum >= 50.0
    return {
        "candidate_first_hike": trailing[0]["event_date"] if trailing else "",
        "candidate_last_hike": trailing[-1]["event_date"] if trailing else "",
        "n_hikes": n,
        "cumulative_hike_bp": cum,
        "qualifies": qualifies,
    }

def ensure_registry():
    if REGISTRY_FILE.exists():
        with REGISTRY_FILE.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        if not rows or rows[0] != PREDICTION_COLUMNS:
            raise RuntimeError("Prospective GCF registry schema mismatch")
        return len(rows) - 1
    with REGISTRY_FILE.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow(PREDICTION_COLUMNS)
    return 0

def main():
    bridge = json.loads(BRIDGE_QC_FILE.read_text(encoding="utf-8"))
    bridge_ok = bridge.get("bridge_status") == "PROXY_FEATURE_BRIDGE_CANDIDATE"

    train = pd.read_csv(TRAIN_FILE)
    if len(train) != 165:
        raise RuntimeError(f"Expected 165 historical training rows, got {len(train)}")

    needed = sorted(set([TARGET] + sum(MODEL_FEATURES.values(), [])))
    if train[needed].isna().any().any():
        raise RuntimeError("Historical training panel has missing frozen model fields")

    broad = sorted(train["broad_episode_id"].unique().tolist())
    weights = hierarchical_weights(train)

    weight_errors = []
    for bid, g in train.groupby("broad_episode_id"):
        weight_errors.append(abs(float(weights.loc[g.index].sum()) - 1.0))
    max_broad_weight_error = float(max(weight_errors)) if weight_errors else np.nan

    target_end = pd.PeriodIndex(train["TARGET_END_PERIOD"].astype(str), freq="M")
    latest_target_end = target_end.max()
    target_leak_rows = int((target_end >= CANDIDATE_FIRST_HIKE_MONTH).sum())

    model = {
        "spec_sha256": SPEC_HASH,
        "module": SPEC["module"],
        "training_rows": int(len(train)),
        "training_broad_episodes": broad,
        "latest_training_target_end_period": str(latest_target_end),
        "B0_HIST_MEAN": {
            "prediction": wmean(train[TARGET].to_numpy(float), weights.to_numpy(float))
        },
    }
    for name, feats in MODEL_FEATURES.items():
        model[name] = fit_wls(train, feats, TARGET, weights)

    MODEL_FOR_HASH = dict(model)
    TRAINING_MODEL_HASH = canonical_hash(MODEL_FOR_HASH)
    model["training_model_sha256"] = TRAINING_MODEL_HASH
    (OUT / "FROZEN_TRAINING_MODEL.json").write_text(
        json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    spec_out = dict(SPEC)
    spec_out["spec_sha256"] = SPEC_HASH
    spec_out["training_model_sha256"] = TRAINING_MODEL_HASH
    (OUT / "MODEL_SPEC.json").write_text(
        json.dumps(spec_out, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    gate = cycle_gate(read_policy())
    pd.DataFrame([gate]).to_csv(OUT / "CURRENT_CYCLE_GATE.csv", index=False)

    registry_rows = ensure_registry()
    predictions_created = 0

    qc = {
        "qc_gate": "PASS",
        "module": "FED-CYCLE-PROSPECTIVE-GCF-012",
        "spec_sha256": SPEC_HASH,
        "training_model_sha256": TRAINING_MODEL_HASH,
        "bridge_status": bridge.get("bridge_status"),
        "bridge_required_status_pass": bridge_ok,
        "training_rows": int(len(train)),
        "training_broad_episodes": broad,
        "training_broad_episode_count": int(len(broad)),
        "latest_training_target_end_period": str(latest_target_end),
        "training_target_overlap_current_candidate_rows": target_leak_rows,
        "max_broad_episode_weight_error": max_broad_weight_error,
        "current_candidate_first_hike": gate["candidate_first_hike"],
        "current_candidate_hikes": gate["n_hikes"],
        "current_candidate_cumulative_hike_bp": gate["cumulative_hike_bp"],
        "current_candidate_qualifies": gate["qualifies"],
        "prediction_registry_rows": registry_rows,
        "predictions_created": predictions_created,
        "oos008_performance_inherited": False,
        "within_episode_refit_allowed": False,
        "retroactive_prediction_allowed": False,
        "deployment_status": "NOT_DEPLOYABLE",
        "evidence_status": "PROXY_MEASUREMENT_SHADOW_READY_NO_PROSPECTIVE_EVIDENCE",
    }

    hard_fail = (
        not bridge_ok
        or len(train) != 165
        or len(broad) != 7
        or broad != ["B01","B02","B03","B04","B05","B06","B07"]
        or target_leak_rows != 0
        or max_broad_weight_error > 1e-10
        or (not gate["qualifies"] and predictions_created != 0)
        or registry_rows != 0
    )
    qc["qc_gate"] = "FAIL" if hard_fail else "PASS"
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# FED-CYCLE-PROSPECTIVE-GCF-012 — Frozen Proxy-Measurement Shadow Model",
        "",
        "**PROXY-MEASUREMENT MODEL FREEZE / NO PROSPECTIVE PREDICTIONS YET / NOT DEPLOYABLE**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- spec SHA256: `{SPEC_HASH}`",
        f"- frozen training-model SHA256: `{TRAINING_MODEL_HASH}`",
        f"- historical training rows: {len(train)}",
        f"- historical broad episodes: {', '.join(broad)}",
        f"- latest realized training target end: {latest_target_end}",
        f"- current 2026 edge run: {gate['n_hikes']} hike(s), {gate['cumulative_hike_bp']:.0f} bp",
        f"- current cycle qualifies: **{gate['qualifies']}**",
        f"- prediction registry rows: {registry_rows}",
        "",
        "Historical model fitting uses only the frozen OOS-008 World Bank feature panel. Future live Gold measurement is separately defined as the BRIDGE-011 GC=F monthly-mean proxy.",
        "",
        "No OOS-008 forecast-performance label is inherited by this measurement-amended specification.",
    ]
    (OUT / "STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-PROSPECTIVE-GCF-012 QC failed")

    print(json.dumps(qc, indent=2))

if __name__ == "__main__":
    main()
