#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_realtime_regime_dashboard_v1"
OUT.mkdir(parents=True, exist_ok=True)

SNAPSHOT = ROOT / "data" / "public" / "FED_REALTIME_REGIME_SNAPSHOT_20260925.csv"
GATE = ROOT / "results" / "fed_cycle_prospective_gcf_v1" / "CURRENT_CYCLE_GATE.csv"
GATE_QC = ROOT / "results" / "fed_cycle_prospective_gcf_v1" / "QC.json"
CLAIMS = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "CLAIM_REGISTRY.csv"
CLAIMS_QC = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "QC.json"

SNAPSHOT_TS = pd.Timestamp("2026-09-25T06:08:00Z")
CURRENT_LABEL = "EDGE_TIGHTENING_CANDIDATE__NOT_YET_QUALIFIED"

REQUIRED_SERIES = [
    "FED_TARGET_LOWER","FED_TARGET_UPPER","EFFR",
    "DGS2","DGS10","T5YIE","T10YIE",
    "VIX","BAA10Y","NFCI",
    "UNRATE","INDPRO_YOY","PCEPI_YOY","CORE_PCE_YOY",
]

REFERENCE_CLAIMS = [
    "CLM-PHASE-DXY-FIRST_HIKE",
    "CLM-PHASE-GOLD-FIRST_HIKE",
    "CLM-PHASE-NASDAQ-FIRST_HIKE",
    "CLM-PHASE-SP500-FIRST_HIKE",
    "CLM-PHASE-WTI-FIRST_HIKE",
    "CLM-GUARD-019",
    "CLM-GUARD-020",
]


def read_qc(path: Path):
    q = json.loads(path.read_text())
    if q.get("qc_gate") != "PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q


def one(snapshot: pd.DataFrame, sid: str):
    z = snapshot[snapshot["series_id"] == sid]
    if len(z) != 1:
        raise RuntimeError(f"expected exactly one row for {sid}, got {len(z)}")
    return z.iloc[0]


def val(snapshot: pd.DataFrame, sid: str) -> float:
    return float(one(snapshot, sid)["value"])


def main():
    gate_qc = read_qc(GATE_QC)
    claims_qc = read_qc(CLAIMS_QC)

    snapshot = pd.read_csv(SNAPSHOT, dtype={"observation_period": str})
    gate = pd.read_csv(GATE)
    claims = pd.read_csv(CLAIMS)

    # Frozen snapshot assertions.
    if snapshot["series_id"].duplicated().any():
        raise RuntimeError("duplicate current-observable series")
    if set(snapshot["series_id"]) != set(REQUIRED_SERIES):
        missing = sorted(set(REQUIRED_SERIES)-set(snapshot["series_id"]))
        extra = sorted(set(snapshot["series_id"])-set(REQUIRED_SERIES))
        raise RuntimeError(f"current observable universe changed; missing={missing}; extra={extra}")
    if snapshot["snapshot_timestamp_utc"].nunique() != 1:
        raise RuntimeError("snapshot timestamp not unique")
    if pd.Timestamp(snapshot["snapshot_timestamp_utc"].iloc[0]) != SNAPSHOT_TS:
        raise RuntimeError("snapshot timestamp changed")
    if (snapshot["freshness_class"] == "STALE_FAIL").any():
        raise RuntimeError("required current input is stale")

    # Source update dates must not post-date the snapshot date.
    snap_date = SNAPSHOT_TS.date()
    src_dates = pd.to_datetime(snapshot["source_update_date"]).dt.date
    if any(d > snap_date for d in src_dates):
        raise RuntimeError("source update date post-dates snapshot")

    # Observation periods must not post-date snapshot.
    obs_dates = []
    for x in snapshot["observation_period"]:
        obs_dates.append(pd.Period(x[:7], freq="M").start_time.date() if len(x) == 7 else pd.Timestamp(x).date())
    if any(d > snap_date for d in obs_dates):
        raise RuntimeError("observation period post-dates snapshot")

    # Frozen prospective gate must fail closed unless authoritative upstream changed.
    if len(gate) != 1:
        raise RuntimeError("current cycle gate must have exactly one row")
    g = gate.iloc[0]
    if str(g["candidate_first_hike"]) != "2026-09-16":
        raise RuntimeError("current candidate first hike changed; 023 snapshot requires explicit re-lock")
    if int(g["n_hikes"]) != 1 or abs(float(g["cumulative_hike_bp"]) - 25.0) > 1e-9 or bool(g["qualifies"]) is not False:
        raise RuntimeError("prospective gate changed; 023 snapshot requires explicit re-lock")

    # Official target-range consistency.
    lower = val(snapshot, "FED_TARGET_LOWER")
    upper = val(snapshot, "FED_TARGET_UPPER")
    if abs(lower - 3.75) > 1e-9 or abs(upper - 4.00) > 1e-9:
        raise RuntimeError("official target range mismatch")

    midpoint = (lower + upper) / 2.0
    dgs2 = val(snapshot, "DGS2")
    dgs10 = val(snapshot, "DGS10")
    curve_bp = (dgs10 - dgs2) * 100.0
    if abs(curve_bp - 26.0) > 1e-8:
        raise RuntimeError(f"unexpected curve arithmetic: {curve_bp}")

    nfci = val(snapshot, "NFCI")
    pce = val(snapshot, "PCEPI_YOY")
    core_pce = val(snapshot, "CORE_PCE_YOY")
    indpro = val(snapshot, "INDPRO_YOY")

    curve_state = "INVERTED" if curve_bp < 0 else "NON_INVERTED"
    nfci_state = "TIGHTER_THAN_AVERAGE" if nfci > 0 else ("LOOSER_THAN_AVERAGE" if nfci < 0 else "AVERAGE")
    indpro_sign = "POSITIVE" if indpro > 0 else ("NEGATIVE" if indpro < 0 else "ZERO")

    derived = pd.DataFrame([
        {"field":"CURRENT_POLICY_LABEL","value_text":CURRENT_LABEL,"value_numeric":pd.NA,"unit":"","derivation":"frozen 013 gate + 023 ontology"},
        {"field":"TARGET_MIDPOINT","value_text":"","value_numeric":midpoint,"unit":"percent","derivation":"(FED_TARGET_LOWER + FED_TARGET_UPPER)/2"},
        {"field":"CURVE_10Y2Y_BP","value_text":"","value_numeric":curve_bp,"unit":"bp","derivation":"(DGS10 - DGS2)*100"},
        {"field":"CURVE_STATE","value_text":curve_state,"value_numeric":pd.NA,"unit":"","derivation":"INVERTED if CURVE_10Y2Y_BP<0 else NON_INVERTED"},
        {"field":"NFCI_STATE","value_text":nfci_state,"value_numeric":pd.NA,"unit":"","derivation":"official NFCI sign interpretation"},
        {"field":"PCE_ABOVE_2_FLAG","value_text":str(pce > 2.0).upper(),"value_numeric":pd.NA,"unit":"","derivation":"PCEPI_YOY > 2"},
        {"field":"CORE_PCE_ABOVE_2_FLAG","value_text":str(core_pce > 2.0).upper(),"value_numeric":pd.NA,"unit":"","derivation":"CORE_PCE_YOY > 2"},
        {"field":"INDPRO_YOY_SIGN","value_text":indpro_sign,"value_numeric":pd.NA,"unit":"","derivation":"sign(INDPRO_YOY)"},
    ])

    # Reference claim linkage: no analog score, no ranking.
    ref = claims[claims["claim_id"].isin(REFERENCE_CLAIMS)].copy()
    if len(ref) != len(REFERENCE_CLAIMS) or set(ref["claim_id"]) != set(REFERENCE_CLAIMS):
        raise RuntimeError("historical reference claim set changed")
    order = {cid:i for i,cid in enumerate(REFERENCE_CLAIMS)}
    ref["_order"] = ref["claim_id"].map(order)
    ref = ref.sort_values("_order").drop(columns="_order").reset_index(drop=True)

    # Hard fail if prohibited current-analog/ranking fields appear.
    prohibited_tokens = ("analog_score","similarity","nearest_analog","best_asset","rank_score","forecast_return")
    bad_cols = [c for c in list(snapshot.columns)+list(derived.columns)+list(ref.columns) if any(t in c.lower() for t in prohibited_tokens)]
    if bad_cols:
        raise RuntimeError(f"prohibited dashboard fields present: {bad_cols}")

    policy_gate = gate.copy()
    policy_gate["current_policy_label"] = CURRENT_LABEL
    policy_gate["target_lower"] = lower
    policy_gate["target_upper"] = upper
    policy_gate["target_midpoint"] = midpoint
    policy_gate["qualification_caveat"] = (
        "Current 2026 run has only one 25bp hike and does not yet qualify under the frozen >=2 hikes and >=50bp rule."
    )
    policy_gate["forecast_issued"] = False
    policy_gate["prediction_registry_rows_expected"] = 0

    snapshot.to_csv(OUT / "CURRENT_OBSERVABLES.csv", index=False)
    policy_gate.to_csv(OUT / "CURRENT_POLICY_GATE.csv", index=False)
    derived.to_csv(OUT / "CURRENT_STATE_DERIVED.csv", index=False)
    ref.to_csv(OUT / "HISTORICAL_REFERENCE_CLAIMS.csv", index=False)

    current = {r.series_id: {
        "value": float(r.value),
        "unit": r.unit,
        "observation_period": r.observation_period,
        "source_update_date": r.source_update_date,
        "freshness_class": r.freshness_class,
        "source_url": r.source_url,
    } for r in snapshot.itertuples(index=False)}

    state = {
        "module":"FED-CYCLE-REALTIME-REGIME-DASHBOARD-023",
        "snapshot_timestamp_utc":"2026-09-25T06:08:00Z",
        "current_policy_label":CURRENT_LABEL,
        "prospective_cycle_gate":{
            "candidate_first_hike":str(g["candidate_first_hike"]),
            "n_hikes":int(g["n_hikes"]),
            "cumulative_hike_bp":float(g["cumulative_hike_bp"]),
            "qualifies":False,
            "prospective_episode_if_later_qualified":"B08",
            "forecast_issued":False,
        },
        "derived_state":{
            "target_midpoint_percent":midpoint,
            "curve_10y2y_bp":curve_bp,
            "curve_state":curve_state,
            "nfci_state":nfci_state,
            "pce_above_2":bool(pce > 2.0),
            "core_pce_above_2":bool(core_pce > 2.0),
            "indpro_yoy_sign":indpro_sign,
        },
        "current_observables":current,
        "historical_reference_claim_ids":REFERENCE_CLAIMS,
        "interpretation_boundary":{
            "analog_selection":False,
            "similarity_score":False,
            "asset_ranking":False,
            "return_forecast":False,
            "trading_recommendation":False,
        },
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT / "DASHBOARD_STATE.json").write_text(
        json.dumps(state, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    )

    report = [
        "# FED-CYCLE-REALTIME-REGIME-DASHBOARD-023 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED RELEASE-AWARE CURRENT SNAPSHOT / HISTORICAL-CONTEXT LINKAGE / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "Snapshot clock: **2026-09-25 16:08 Australia/Sydney (06:08 UTC)**.",
        "",
        "## Current policy gate",
        "",
        "- 2026 edge candidate FIRST_HIKE: 2026-09-16.",
        "- Current observed tightening: 1 hike / 25 bp.",
        "- Target range: 3.75%-4.00%; midpoint 3.875%.",
        "- Frozen prospective qualification rule: >=2 hikes AND >=50 bp.",
        "- Current qualification: **FALSE**.",
        "- Prospective prediction issued: **NO**.",
        "",
        "The current label is therefore **EDGE_TIGHTENING_CANDIDATE__NOT_YET_QUALIFIED**, not a fully qualified B08 tightening episode.",
        "",
        "## Current observable state",
        "",
        f"- EFFR: {val(snapshot,'EFFR'):.2f}% ({one(snapshot,'EFFR')['observation_period']}).",
        f"- 2Y / 10Y Treasury: {dgs2:.2f}% / {dgs10:.2f}%; 10Y-2Y curve = {curve_bp:.0f} bp ({curve_state}).",
        f"- 5Y / 10Y breakeven inflation: {val(snapshot,'T5YIE'):.2f}% / {val(snapshot,'T10YIE'):.2f}%.",
        f"- VIX: {val(snapshot,'VIX'):.2f} ({one(snapshot,'VIX')['observation_period']}).",
        f"- Baa-10Y spread: {val(snapshot,'BAA10Y'):.2f}%.",
        f"- NFCI: {nfci:.3f} ({nfci_state}).",
        f"- Unemployment rate: {val(snapshot,'UNRATE'):.1f}%.",
        f"- Industrial production YoY: {indpro:.1f}% ({indpro_sign}).",
        f"- Headline / core PCE YoY: {pce:.1f}% / {core_pce:.1f}% (latest available July release; both above 2%).",
        "",
        "## Interpretation",
        "",
        "The snapshot supports a narrow descriptive reading: policy has restarted tightening, while the 10Y-2Y curve is currently non-inverted and the NFCI remains below zero (looser than its long-run average definition). Inflation remains above 2% in the latest PCE release. These dimensions are shown separately; 023 does not combine them into a score.",
        "",
        "## Historical evidence links",
        "",
        "The dashboard exposes the five 022B FIRST_HIKE core-asset historical distribution claims plus the 019/020 negative timing-rule guardrails.",
        "",
        "Historical FIRST_HIKE distributions are **reference distributions only** because the 2026 run has not yet met the frozen broad-cycle qualification gate.",
        "",
        "## Freshness",
        "",
        "High-frequency public series are not synchronized. Each row retains its own observation period, source update date and release cadence. The dashboard does not force all series onto a common date.",
        "",
        "## Prohibited interpretation",
        "",
        "- no closest historical analog;",
        "- no similarity score;",
        "- no asset ranking;",
        "- no prospective return forecast;",
        "- no bottom date;",
        "- no trading recommendation.",
    ]
    (OUT / "FED_CYCLE_REALTIME_REGIME_DASHBOARD_023_REPORT.md").write_text("\n".join(report) + "\n")

    qc = {
        "qc_gate":"PASS",
        "module":"FED-CYCLE-REALTIME-REGIME-DASHBOARD-023",
        "snapshot_timestamp_utc":"2026-09-25T06:08:00Z",
        "required_observable_rows":len(REQUIRED_SERIES),
        "required_observable_rows_present":int(len(snapshot)),
        "stale_fail_rows":int((snapshot["freshness_class"]=="STALE_FAIL").sum()),
        "source_update_post_snapshot_violations":0,
        "observation_post_snapshot_violations":0,
        "prospective_gate_candidate_first_hike":"2026-09-16",
        "prospective_gate_hikes":1,
        "prospective_gate_cumulative_hike_bp":25.0,
        "prospective_gate_qualifies":False,
        "current_policy_label":CURRENT_LABEL,
        "target_range_lower":lower,
        "target_range_upper":upper,
        "target_midpoint":midpoint,
        "curve_10y2y_bp":curve_bp,
        "curve_state":curve_state,
        "nfci_state":nfci_state,
        "historical_reference_claim_count":int(len(ref)),
        "analog_selection_fields":0,
        "similarity_score_fields":0,
        "asset_ranking_fields":0,
        "forecast_outputs":0,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n")


if __name__ == "__main__":
    main()
