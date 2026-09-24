#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_cross_asset_master_synthesis_v1"
OUT.mkdir(parents=True, exist_ok=True)

PHASES = ["FIRST_HIKE", "LAST_HIKE", "PAUSE_START", "FIRST_CUT"]
CORE_SUPPORTED = {"DXY", "GOLD", "NASDAQ", "SP500", "WTI"}

P004 = ROOT / "results" / "fed_cycle_phase_clock_v1" / "PHASE_COMPARISON.csv"
Q004 = ROOT / "results" / "fed_cycle_phase_clock_v1" / "QC.json"
P005 = ROOT / "results" / "fed_cycle_stress_layer_v1" / "STRESS_PHASE_SUMMARY.csv"
Q005 = ROOT / "results" / "fed_cycle_stress_layer_v1" / "QC.json"
P006 = ROOT / "results" / "fed_cycle_asia_credit_diag_v1" / "ASIA_PHASE_SUMMARY.csv"
Q006 = ROOT / "results" / "fed_cycle_asia_credit_diag_v1" / "QC.json"
PM014 = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "MARKET_PHASE_SUMMARY.csv"
PH014 = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "HOUSING_PHASE_SUMMARY.csv"
PC014 = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "CASH_PHASE_SUMMARY.csv"
PR014 = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "RATE_PHASE_SUMMARY.csv"
Q014 = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "QC.json"
P016 = ROOT / "results" / "fed_cycle_supported_recovery_map_v1" / "SUPPORTED_RECOVERY_CELLS.csv"
Q016 = ROOT / "results" / "fed_cycle_supported_recovery_map_v1" / "QC.json"
P017 = ROOT / "results" / "fed_cycle_total_risk_clock_v1" / "SUPPORTED_TOTAL_CLOCK_SUMMARY.csv"
Q017 = ROOT / "results" / "fed_cycle_total_risk_clock_v1" / "QC.json"

UPSTREAM_QC = [Q004, Q005, Q006, Q014, Q016, Q017]


def require_pass():
    modules = []
    for p in UPSTREAM_QC:
        q = json.loads(p.read_text())
        if q.get("qc_gate") != "PASS":
            raise RuntimeError(f"upstream QC not PASS: {p}")
        modules.append(q.get("module", p.parent.name))
    return modules


def base_meta(df, source_module, evidence_scope, evidence_class="DESCRIPTIVE"):
    out = df.copy()
    out["source_module"] = source_module
    out["evidence_scope"] = evidence_scope
    out["evidence_class"] = evidence_class
    out["causal_status"] = "NONE"
    out["oos_status"] = "NOT_A_FORECASTING_MODEL"
    out["deployment_status"] = "NOT_DEPLOYABLE"
    out["allowed_use"] = "historical descriptive risk-distribution / educational context"
    out["forbidden_claim"] = "no causal Fed claim; no deterministic bottom timing; no trading signal"
    return out


def build_master_asset_map():
    rows = []

    # Core phase-clock assets.
    p = pd.read_csv(P004)
    p = p[p["asset"].isin(["GOLD", "SP500", "NASDAQ", "WTI"])].copy()
    for _, r in p.iterrows():
        rows.append({
            "asset": r["asset"],
            "asset_class": "PRECIOUS_METAL" if r["asset"] == "GOLD" else ("ENERGY" if r["asset"] == "WTI" else "US_EQUITY"),
            "phase": r["anchor"],
            "n_legs": r["n_legs"],
            "n_broad_episodes": r["n_broad_episodes"],
            "support_status": r["support_status"],
            "scope_tier": "CORE_SUPPORTED",
            "ret_3m": r["weighted_median_ret_3m"],
            "ret_6m": r["weighted_median_ret_6m"],
            "ret_12m": r["weighted_median_ret_12m"],
            "ret_24m": pd.NA,
            "path_risk_metric": "MDD_12M",
            "path_risk_value": r["weighted_median_mdd_12m"],
            "trough_month": r["weighted_median_mdd_trough_month"],
            "late_trough_share": r["mdd_trough_share_late_7_12"],
            "path_horizon_months": 12,
            "source_module": "PHASE-CLOCK-004",
            "evidence_scope": "PRIMARY_CORE",
            "evidence_class": "DESCRIPTIVE",
        })

    # DXY + limited market extensions.
    m = pd.read_csv(PM014)
    for _, r in m.iterrows():
        asset = r["asset"]
        rows.append({
            "asset": asset,
            "asset_class": {"DXY":"USD_INDEX","TLT":"LONG_TREASURY_ETF","VNQ":"REIT_ETF","BTC_USD":"CRYPTO"}[asset],
            "phase": r["anchor"],
            "n_legs": r["n_legs"],
            "n_broad_episodes": r["n_broad_episodes"],
            "support_status": r["support_status"],
            "scope_tier": "CORE_SUPPORTED" if asset == "DXY" else "LIMITED_EXTENSION",
            "ret_3m": r["weighted_median_ret_3m"],
            "ret_6m": r["weighted_median_ret_6m"],
            "ret_12m": r["weighted_median_ret_12m"],
            "ret_24m": pd.NA,
            "path_risk_metric": "MDD_12M",
            "path_risk_value": r["weighted_median_mdd_12m"],
            "trough_month": r["weighted_median_mdd_trough_month"],
            "late_trough_share": r["weighted_late_trough_share_7_12"],
            "path_horizon_months": 12,
            "source_module": "CROSS-ASSET-EXPANSION-014",
            "evidence_scope": "PRIMARY_EXTENSION",
            "evidence_class": "DESCRIPTIVE",
        })

    # Housing is slow-moving and retains its 24M metric ontology.
    h = pd.read_csv(PH014)
    for _, r in h.iterrows():
        rows.append({
            "asset": r["asset"],
            "asset_class": "US_HOUSING",
            "phase": r["anchor"],
            "n_legs": r["n_legs"],
            "n_broad_episodes": r["n_broad_episodes"],
            "support_status": r["support_status"],
            "scope_tier": "SUPPORTED_SLOW_MOVING",
            "ret_3m": pd.NA,
            "ret_6m": r["weighted_median_ret_6m"],
            "ret_12m": r["weighted_median_ret_12m"],
            "ret_24m": r["weighted_median_ret_24m"],
            "path_risk_metric": "DECLINE_24M",
            "path_risk_value": r["weighted_median_decline_24m"],
            "trough_month": r["weighted_median_trough_month_24m"],
            "late_trough_share": pd.NA,
            "path_horizon_months": 24,
            "source_module": "CROSS-ASSET-EXPANSION-014",
            "evidence_scope": "SLOW_MOVING_EXTENSION",
            "evidence_class": "DESCRIPTIVE",
        })

    # Asia remains diagnostic, never promoted to core causal evidence.
    a = pd.read_csv(P006)
    for _, r in a.iterrows():
        rows.append({
            "asset": r["market"],
            "asset_class": "ASIA_EQUITY",
            "phase": r["anchor"],
            "n_legs": r["n_legs"],
            "n_broad_episodes": r["n_broad_episodes"],
            "support_status": r["support_status"],
            "scope_tier": "DIAGNOSTIC_ASIA",
            "ret_3m": r["weighted_median_ret_3m"],
            "ret_6m": r["weighted_median_ret_6m"],
            "ret_12m": r["weighted_median_ret_12m"],
            "ret_24m": pd.NA,
            "path_risk_metric": "MDD_12M",
            "path_risk_value": r["weighted_median_mdd_12m"],
            "trough_month": r["weighted_median_mdd_trough_month"],
            "late_trough_share": r["weighted_late_trough_share_7_12"],
            "path_horizon_months": 12,
            "source_module": "ASIA-CREDIT-DIAG-006",
            "evidence_scope": "DIAGNOSTIC_EXTENSION",
            "evidence_class": "DESCRIPTIVE_DIAGNOSTIC",
        })

    out = pd.DataFrame(rows)
    out["causal_status"] = "NONE"
    out["oos_status"] = "NOT_A_FORECASTING_MODEL"
    out["deployment_status"] = "NOT_DEPLOYABLE"
    out["allowed_use"] = "historical descriptive risk-distribution / educational context"
    out["forbidden_claim"] = "no causal Fed claim; no deterministic bottom timing; no trading signal"

    # Attach supported post-trough recovery only by exact asset x phase.
    rec = pd.read_csv(P016)
    rec = rec[rec["recovery_level"].isin(["50%", "100%"])].copy()
    rp = rec.pivot_table(
        index=["asset", "anchor"],
        columns="recovery_level",
        values=["weighted_km_median_months", "recovery_support_status", "source_module"],
        aggfunc="first",
    )
    rp.columns = [
        f"{a}_{'50' if b == '50%' else '100'}" for a, b in rp.columns
    ]
    rp = rp.reset_index().rename(columns={"anchor":"phase"})
    out = out.merge(rp, on=["asset","phase"], how="left", validate="one_to_one")

    # Attach supported anchor-to-recovery total clock.
    tot = pd.read_csv(P017).rename(columns={"anchor":"phase"})
    keep = [
        "asset","phase","weighted_km_median_anchor_to_50_months",
        "weighted_km_median_anchor_to_100_months",
        "observed_50_recoveries","censored_50_recoveries",
        "observed_100_recoveries","censored_100_recoveries",
    ]
    out = out.merge(tot[keep], on=["asset","phase"], how="left", validate="one_to_one")

    return out.sort_values(["scope_tier","asset","phase"]).reset_index(drop=True)


def build_policy_rate_cash_context():
    rows = []
    c = pd.read_csv(PC014)
    for _, r in c.iterrows():
        rows.append({
            "series": r["asset"], "context_type": "CASH_CARRY", "phase": r["anchor"],
            "n_legs": r["n_legs"], "n_broad_episodes": r["n_broad_episodes"],
            "support_status": r["support_status"],
            "metric_3m": r["weighted_median_cash_carry_3m"],
            "metric_6m": r["weighted_median_cash_carry_6m"],
            "metric_12m": r["weighted_median_cash_carry_12m"],
            "metric_12m_unit": "DECIMAL_CARRY",
            "secondary_metric": r["weighted_median_avg_dff_12m"],
            "secondary_metric_name": "AVG_DFF_12M_PERCENT",
        })
    y = pd.read_csv(PR014)
    for _, r in y.iterrows():
        rows.append({
            "series": r["series"], "context_type": "TREASURY_YIELD_CHANGE", "phase": r["anchor"],
            "n_legs": r["n_legs"], "n_broad_episodes": r["n_broad_episodes"],
            "support_status": r["support_status"],
            "metric_3m": r["weighted_median_chg_3m_bp"],
            "metric_6m": r["weighted_median_chg_6m_bp"],
            "metric_12m": r["weighted_median_chg_12m_bp"],
            "metric_12m_unit": "BASIS_POINTS",
            "secondary_metric": r["weighted_median_max_decrease_12m_bp"],
            "secondary_metric_name": "MAX_DECREASE_12M_BP",
        })
    out = pd.DataFrame(rows)
    out["source_module"] = "CROSS-ASSET-EXPANSION-014"
    out["evidence_class"] = "DESCRIPTIVE"
    out["causal_status"] = "NONE"
    out["oos_status"] = "NOT_A_FORECASTING_MODEL"
    out["deployment_status"] = "NOT_DEPLOYABLE"
    out["forbidden_claim"] = "cash carry and yield changes are not directly rank-comparable with asset price returns"
    return out.sort_values(["context_type","series","phase"]).reset_index(drop=True)


def build_stress_context():
    s = pd.read_csv(P005).rename(columns={"anchor":"phase"})
    s["source_module"] = "STRESS-LAYER-005"
    s["evidence_class"] = "MECHANISM_CONTEXT"
    s["causal_status"] = "NONE"
    s["oos_status"] = "NOT_A_FORECASTING_MODEL"
    s["deployment_status"] = "NOT_DEPLOYABLE"
    s["allowed_use"] = "historical stress context around realized Fed-cycle phases"
    s["forbidden_claim"] = "not a live bottoming signal; stress peaks are ex-post window statistics"
    return s.sort_values(["observable","phase"]).reset_index(drop=True)


def main():
    upstream_modules = require_pass()
    master = build_master_asset_map()
    context = build_policy_rate_cash_context()
    stress = build_stress_context()

    if set(master["phase"].dropna()) - set(PHASES):
        raise RuntimeError("non-canonical phase in master map")
    if set(context["phase"].dropna()) - set(PHASES):
        raise RuntimeError("non-canonical phase in context")
    if set(stress["phase"].dropna()) - set(PHASES):
        raise RuntimeError("non-canonical phase in stress")
    dupes = int(master.duplicated(["asset","phase"]).sum())
    if dupes:
        raise RuntimeError("duplicate asset x phase rows")
    if not (master["causal_status"] == "NONE").all():
        raise RuntimeError("causal-status violation")
    if not (master["deployment_status"] == "NOT_DEPLOYABLE").all():
        raise RuntimeError("deployment-status violation")

    master.to_csv(OUT / "MASTER_ASSET_PHASE_MAP.csv", index=False)
    context.to_csv(OUT / "POLICY_RATE_CASH_CONTEXT.csv", index=False)
    stress.to_csv(OUT / "PHASE_STRESS_CONTEXT.csv", index=False)

    recovery_cols = [
        "asset","phase","scope_tier","support_status",
        "weighted_km_median_months_50","weighted_km_median_months_100",
        "recovery_support_status_50","recovery_support_status_100",
        "weighted_km_median_anchor_to_50_months",
        "weighted_km_median_anchor_to_100_months",
        "observed_50_recoveries","censored_50_recoveries",
        "observed_100_recoveries","censored_100_recoveries",
        "causal_status","oos_status","deployment_status"
    ]
    recmap = master[recovery_cols].copy()
    recmap.to_csv(OUT / "RECOVERY_RISK_CLOCK_MAP.csv", index=False)

    records = master.where(pd.notna(master), None).to_dict(orient="records")
    ref = {
        "module": "FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021",
        "as_of": "2026-09-25",
        "purpose": "evidence-linked historical risk-distribution reference",
        "canonical_phases": PHASES,
        "core_supported_assets": sorted(CORE_SUPPORTED),
        "deterministic_first_cut_timing_guardrail": (
            "019 and 020 do not support a simple predetermined FIRST_CUT bottom-timing rule. "
            "Do not convert 021 medians into a deterministic timing signal."
        ),
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
        "records": records,
    }
    (OUT / "PANDAAI_RISK_DISTRIBUTION_REFERENCE.json").write_text(
        json.dumps(ref, indent=2, ensure_ascii=False, allow_nan=False)
    )

    core = master[master["asset"].isin(CORE_SUPPORTED)]
    first_cut = core[core["phase"] == "FIRST_CUT"].copy()
    report = [
        "# FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED SYNTHESIS / DESCRIPTIVE EVIDENCE MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "021 performs no new price estimation and no new significance search. It harmonizes already-QC-passed public outputs while preserving support labels and metric ontologies.",
        "",
        "## Canonical coverage",
        "",
        f"- price-asset phase rows: {len(master)}",
        f"- unique price assets: {master['asset'].nunique()}",
        f"- core fully supported four-phase assets: {', '.join(sorted(CORE_SUPPORTED))}",
        f"- policy/rate/cash context rows: {len(context)}",
        f"- phase-stress context rows: {len(stress)}",
        "",
        "## FIRST_CUT core risk-distribution snapshot",
        "",
    ]
    for _, r in first_cut.sort_values("asset").iterrows():
        risk = float(r["path_risk_value"]) * 100
        ret = float(r["ret_12m"]) * 100
        total100 = r["weighted_km_median_anchor_to_100_months"]
        report.append(
            f"- {r['asset']}: median +12M endpoint {ret:+.2f}%; "
            f"{r['path_risk_metric']} median {risk:.2f}%; "
            f"trough month {float(r['trough_month']):.0f}; "
            f"anchor-to-full-recovery KM median {total100 if pd.notna(total100) else 'NA'} months."
        )
    report += [
        "",
        "These are historical descriptive distributions. Positive endpoints can coexist with deep interim drawdowns.",
        "",
        "## Interpretation guardrails",
        "",
        "- Realized Fed phases are cycle markers, not identified monetary-policy shocks.",
        "- 019 and 020 failed to support a simple predetermined FIRST_CUT bottom-timing rule.",
        "- VIX/BAA/copper stress peaks are ex-post window statistics and are not live timing signals.",
        "- TLT/VNQ/BTC remain limited extensions; Asia remains diagnostic; housing uses a distinct 24M slow-moving metric ontology.",
        "- Cash carry and Treasury-yield changes are retained in a separate context table and are not ranked against price returns.",
        "",
        "## Product use",
        "",
        "PandaAI may use 021 to present: policy phase + historical asset-specific path-risk distribution + recovery clock + support strength + evidence class + uncertainty. It must not output a deterministic bottom date or convert these tables into a trading recommendation.",
    ]
    (OUT / "FED_CYCLE_CROSS_ASSET_MASTER_SYNTHESIS_021_REPORT.md").write_text("\n".join(report) + "\n")

    qc = {
        "qc_gate": "PASS",
        "module": "FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021",
        "upstream_qc_modules": upstream_modules,
        "new_price_estimation": False,
        "new_inference": False,
        "pvalues_generated": False,
        "master_asset_phase_rows": int(len(master)),
        "unique_assets": int(master["asset"].nunique()),
        "core_supported_assets": sorted(CORE_SUPPORTED),
        "core_supported_asset_phase_rows": int(len(core)),
        "policy_rate_cash_context_rows": int(len(context)),
        "stress_context_rows": int(len(stress)),
        "duplicate_asset_phase_rows": dupes,
        "noncanonical_phase_violations": 0,
        "causal_status_violations": int((master["causal_status"] != "NONE").sum()),
        "deployment_status_violations": int((master["deployment_status"] != "NOT_DEPLOYABLE").sum()),
        "deterministic_first_cut_timing_guardrail": True,
        "private_paper_inputs_used": False,
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n")


if __name__ == "__main__":
    main()
