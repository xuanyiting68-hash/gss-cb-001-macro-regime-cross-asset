#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_figure_registry_024_v1"
OUT.mkdir(parents=True, exist_ok=True)

CLAIMS = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "CLAIM_REGISTRY.csv"
Q022B = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "QC.json"
Q023 = ROOT / "results" / "fed_cycle_realtime_regime_dashboard_v1" / "QC.json"

P0_KEYS = {
    "FIG-PHASE-DXY-FIRST_CUT",
    "FIG-PHASE-GOLD-FIRST_CUT",
    "FIG-PHASE-NASDAQ-FIRST_CUT",
    "FIG-PHASE-SP500-FIRST_CUT",
    "FIG-PHASE-WTI-FIRST_CUT",
    "FIG-RECOVERY-FIRSTCUT-VS-PAUSE",
    "FIG-GUARD-019",
    "FIG-GUARD-020",
    "FIG-CASE-B04",
    "FIG-CASE-B05",
    "FIG-CASE-B06",
    "FIG-CASE-B07",
    "FIG-CURRENT-023-REGIME-SNAPSHOT",
}

P1_CONTEXT = {
    "FIG-CTX-B04_CTX_02",
    "FIG-CTX-B04_CTX_03",
    "FIG-CTX-B05_CTX_03",
    "FIG-CTX-B06_CTX_02",
    "FIG-CTX-B06_CTX_03",
}

REQUIRED = [
    "figure_key","figure_family","linked_claim_ids","source_modules","source_files",
    "data_scope","visual_grammar","primary_encodings","required_annotations",
    "required_disclaimer","prohibited_visual_implications","freshness_rule",
    "output_formats","priority","build_status","public_safe",
    "causal_status","deployment_status",
]


def read_pass(path: Path):
    q = json.loads(path.read_text())
    if q.get("qc_gate") != "PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q


def claim_spec(r):
    key = r.figure_key
    fam = r.claim_family

    if fam == "CORE_PHASE_DISTRIBUTION":
        figure_family = "CORE_PHASE_EVIDENCE_CARD"
        visual = "four-metric evidence card with separated return/path-risk/time encodings"
        enc = (
            "+12M endpoint as signed return bar; 12M MDD magnitude as separate path-risk bar; "
            "trough month as month marker; anchor-to-full-recovery as separate duration marker"
        )
        annotations = (
            f"asset={r.asset}; phase={r.phase}; sample={r.sample_descriptor}; support={r.support_status}; "
            "label MDD as magnitude and all timing values as historical medians"
        )
        disclaimer = (
            "Historical descriptive distribution; realized Fed phase is not an identified policy shock; "
            "trough/recovery months are not forecasts or trading signals."
        )
        prohibited = (
            "no shared unlabeled axis for endpoint and drawdown; no best/worst badge; no arrow implying Fed causality; "
            "no future-date projection from trough/recovery medians"
        )
        data_scope = f"{r.asset} x {r.phase}"
    elif fam == "HISTORICAL_CASE":
        figure_family = "HISTORICAL_CASE_TIMELINE"
        visual = "dated policy timeline plus case-path evidence panel"
        enc = (
            "policy anchors on chronological axis; FIRST_CUT marker; asset endpoint/MDD/trough evidence in aligned callouts"
        )
        if r.broad_episode_id == "B02":
            annotations = (
                "show T03_1987, T04_1987 and T05_1988 as three separate mechanical sub-cycles; "
                "do not synthesize one policy path"
            )
            prohibited = "no flattened B02 cycle; no current-analog label; no causal policy-to-asset arrows"
        else:
            annotations = (
                f"broad episode={r.broad_episode_id}; FIRST_CUT case metrics; preserve dated historical-case status; "
                "022A context may be layered only with its claim-time class"
            )
            prohibited = "no closest-current-analog label; no causal policy-to-asset arrows; no omitted later-shock caveat"
        disclaimer = (
            "Historical case chronology and path description only; not evidence that the policy action caused the asset path "
            "or that this case predicts the current cycle."
        )
        data_scope = r.broad_episode_id
    elif fam == "HISTORICAL_CONTEXT":
        figure_family = "HISTORICAL_CONTEXT_CARD"
        visual = "official-source context card with mandatory time-class badge"
        enc = "event date/period header; claim-time class badge; concise paraphrase; source institution/footer"
        annotations = (
            f"time_class={r.evidence_time}; source={r.official_source_urls}; "
            "show hindsight warning/allowed-use boundary from claim registry"
        )
        disclaimer = (
            "Context timing must be preserved: retrospective dating and post-anchor shocks were not necessarily known at the earlier policy anchor."
        )
        prohibited = (
            "no backward causal arrow from later event to earlier policy decision; no removal of hindsight label; "
            "no treatment of retrospective dating as a real-time indicator"
        )
        data_scope = r.broad_episode_id
    elif fam == "METHOD_GUARDRAIL":
        figure_family = "METHOD_GUARDRAIL"
        if r.claim_id == "CLM-GUARD-019":
            visual = "binary-state support/contrast diagnostic"
            enc = "state support counts and median trough-month contrast; emphasize equal curve-inversion median trough month"
            annotations = "show 8 mechanical / 6 broad episodes and unsupported/insufficient state variation labels"
            prohibited = "no signal colors; no composite-score promotion; no curve/NFCI/growth buy-sell labels"
        else:
            visual = "full-sample rho plus leave-one-out stability diagnostic"
            enc = "one row per frozen predictor with full-sample rho and LOO range/sign-stability flag"
            annotations = "full sample must be visually primary; five-episode VIX-common curve diagnostic may only appear as sensitivity"
            prohibited = "no cherry-picked five-episode curve headline; no signal colors; no fitted-score visual"
        disclaimer = "Negative small-sample research result; not a timing model, OOS forecast or deployment rule."
        data_scope = "FIRST_CUT predetermined timing-rule branch"
    elif fam == "SYNTHESIS":
        figure_family = "RECOVERY_SYNTHESIS"
        visual = "paired PAUSE_START versus FIRST_CUT anchor-to-full-recovery duration comparison"
        enc = "one paired duration segment per supported asset; months on common duration axis"
        annotations = "five fully supported assets only; slower=3, equal=2, faster=0 must be shown as descriptive sample count"
        disclaimer = "Historical supported-sample comparison; no causal interpretation and no asset winner."
        prohibited = "no best/worst ranking; no causal label; no extrapolation to current cycle"
        data_scope = "DXY|GOLD|NASDAQ|SP500|WTI; PAUSE_START vs FIRST_CUT"
    else:
        raise RuntimeError(f"unknown claim family: {fam}")

    if key in P0_KEYS:
        priority = "P0"
    elif fam == "CORE_PHASE_DISTRIBUTION":
        priority = "P1"
    elif key in {"FIG-CASE-B02","FIG-CASE-B03"} or key in P1_CONTEXT:
        priority = "P1"
    else:
        priority = "P2"

    return {
        "figure_key": key,
        "figure_family": figure_family,
        "linked_claim_ids": r.claim_id,
        "source_modules": r.source_modules,
        "source_files": r.source_files,
        "data_scope": data_scope,
        "visual_grammar": visual,
        "primary_encodings": enc,
        "required_annotations": annotations,
        "required_disclaimer": disclaimer,
        "prohibited_visual_implications": prohibited,
        "freshness_rule": r.freshness_rule,
        "output_formats": "PNG_16_9|PNG_1_1|SVG_RESEARCH|JSON_SPEC",
        "priority": priority,
        "build_status": "SPEC_READY_NOT_RENDERED",
        "public_safe": True,
        "causal_status": "NONE",
        "deployment_status": "NOT_DEPLOYABLE",
    }


def current_023_spec():
    return {
        "figure_key":"FIG-CURRENT-023-REGIME-SNAPSHOT",
        "figure_family":"CURRENT_REGIME_SNAPSHOT",
        "linked_claim_ids":"CLM-PHASE-DXY-FIRST_HIKE|CLM-PHASE-GOLD-FIRST_HIKE|CLM-PHASE-NASDAQ-FIRST_HIKE|CLM-PHASE-SP500-FIRST_HIKE|CLM-PHASE-WTI-FIRST_HIKE|CLM-GUARD-019|CLM-GUARD-020",
        "source_modules":"FED-CYCLE-REALTIME-REGIME-DASHBOARD-023|FED-CYCLE-CONTENT-CLAIM-REGISTRY-022B",
        "source_files":"results/fed_cycle_realtime_regime_dashboard_v1/CURRENT_OBSERVABLES.csv|results/fed_cycle_realtime_regime_dashboard_v1/CURRENT_POLICY_GATE.csv|results/fed_cycle_realtime_regime_dashboard_v1/CURRENT_STATE_DERIVED.csv",
        "data_scope":"2026-09-25 release-aware current snapshot",
        "visual_grammar":"five-block current-state dashboard card",
        "primary_encodings":"policy gate; rates/curve; breakevens; stress/credit; real economy/inflation; per-row freshness labels",
        "required_annotations":"show 1 hike/25bp/qualification FALSE; show snapshot clock; show observation dates; label FIRST_HIKE historical claims as reference distributions only",
        "required_disclaimer":"Current-state description only; not a qualified B08 episode, analog selection, return forecast, bottom date or investment recommendation.",
        "prohibited_visual_implications":"no similarity meter; no closest analog; no asset rank; no probability forecast; no green/red trade signal palette",
        "freshness_rule":"REBUILD_AS_NEW_APPEND_ONLY_SNAPSHOT",
        "output_formats":"PNG_16_9|PNG_1_1|SVG_RESEARCH|JSON_SPEC",
        "priority":"P0",
        "build_status":"SPEC_READY_NOT_RENDERED",
        "public_safe":True,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }


def main():
    q022b = read_pass(Q022B)
    q023 = read_pass(Q023)
    claims = pd.read_csv(CLAIMS)

    if len(claims) != 47 or claims["claim_id"].nunique() != 47:
        raise RuntimeError("022B claim universe changed")
    if claims["figure_key"].isna().any() or claims["figure_key"].duplicated().any():
        raise RuntimeError("022B figure keys missing or not unique")

    specs = [claim_spec(r) for r in claims.itertuples(index=False)]
    specs.append(current_023_spec())
    reg = pd.DataFrame(specs)[REQUIRED]

    if len(reg) != 48 or reg["figure_key"].nunique() != 48:
        raise RuntimeError("expected 48 unique figure specs")
    claim_keys = set(claims["figure_key"])
    mapped = set(reg[reg["figure_key"] != "FIG-CURRENT-023-REGIME-SNAPSHOT"]["figure_key"])
    if mapped != claim_keys:
        raise RuntimeError("022B figure-key mapping is not 1:1")

    # Timing class preservation for all context figures.
    ctx = claims[claims["claim_family"] == "HISTORICAL_CONTEXT"][["claim_id","figure_key","evidence_time","freshness_rule"]]
    ctx_map = reg[reg["figure_family"] == "HISTORICAL_CONTEXT_CARD"].merge(
        ctx, on="figure_key", how="left", validate="one_to_one"
    )
    if len(ctx_map) != 18 or ctx_map["evidence_time"].isna().any():
        raise RuntimeError("context timing classes not preserved")

    # Frozen anti-hindsight / B02 assertions.
    b02 = reg[reg["figure_key"] == "FIG-CASE-B02"].iloc[0]
    if "three separate mechanical sub-cycles" not in b02["required_annotations"]:
        raise RuntimeError("B02 visual guardrail lost")
    for key in ["FIG-CTX-B04_CTX_03","FIG-CTX-B06_CTX_03"]:
        ev = ctx_map.loc[ctx_map["figure_key"] == key, "evidence_time"].iloc[0]
        if ev != "POST_ANCHOR_SHOCK":
            raise RuntimeError(f"later-shock timing class lost for {key}")
    b07fresh = ctx_map.loc[ctx_map["figure_key"] == "FIG-CTX-B07_CTX_02", "freshness_rule_y"].iloc[0]
    if b07fresh != "REVERIFY_BEFORE_CURRENT_USE":
        raise RuntimeError("B07 NBER context freshness lost")

    p0 = reg[reg["priority"] == "P0"]
    if len(p0) != 13 or set(p0["figure_key"]) != P0_KEYS:
        raise RuntimeError(f"P0 universe changed: {len(p0)}")

    boundary_cols = [
        "source_modules","source_files","data_scope","visual_grammar","primary_encodings",
        "required_annotations","required_disclaimer","prohibited_visual_implications",
        "freshness_rule","output_formats"
    ]
    if reg[boundary_cols].apply(lambda s: s.astype(str).str.strip().eq("")).any().any():
        raise RuntimeError("blank visual source/boundary field")
    if not reg["public_safe"].all():
        raise RuntimeError("non-public-safe row in 024")
    if not (reg["causal_status"] == "NONE").all():
        raise RuntimeError("causal promotion")
    if not (reg["deployment_status"] == "NOT_DEPLOYABLE").all():
        raise RuntimeError("deployment promotion")

    prohibited_cols = [
        c for c in reg.columns
        if any(t in c.lower() for t in ["analog_score","similarity_score","asset_rank","forecast_return"])
    ]
    if prohibited_cols:
        raise RuntimeError(f"prohibited visual fields present: {prohibited_cols}")

    reg.to_csv(OUT / "FIGURE_REGISTRY.csv", index=False)
    p0.to_csv(OUT / "P0_BUILD_QUEUE.csv", index=False)

    spec_json = {
        "module":"FED-CYCLE-FIGURE-REGISTRY-024",
        "as_of":"2026-09-25",
        "figure_spec_count":48,
        "claim_linked_specs":47,
        "supplemental_current_specs":1,
        "p0_count":13,
        "figures":json.loads(reg.to_json(orient="records")),
    }
    (OUT / "FIGURE_REGISTRY.json").write_text(
        json.dumps(spec_json, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    )

    # Build-plan markdown.
    lines = [
        "# FED-CYCLE-FIGURE-REGISTRY-024 — P0 Build Plan",
        "",
        "P0 is a production order, not an evidence ranking.",
        "",
    ]
    for r in p0.itertuples(index=False):
        lines += [
            f"## {r.figure_key}",
            "",
            f"- Family: {r.figure_family}",
            f"- Claims: {r.linked_claim_ids}",
            f"- Grammar: {r.visual_grammar}",
            f"- Encodings: {r.primary_encodings}",
            f"- Required annotation: {r.required_annotations}",
            f"- Disclaimer: {r.required_disclaimer}",
            f"- Never imply: {r.prohibited_visual_implications}",
            "",
        ]
    (OUT / "P0_BUILD_PLAN.md").write_text("\n".join(lines) + "\n")

    report = [
        "# FED-CYCLE-FIGURE-REGISTRY-024 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED VISUAL EVIDENCE SPEC REGISTRY / 48 FIGURE SPECS / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        "- claim-linked figure specs: 47",
        "- supplemental 023 current-regime figure specs: 1",
        "- total specs: 48",
        "- P0 build queue: 13",
        "- P1: " + str(int((reg["priority"] == "P1").sum())),
        "- P2: " + str(int((reg["priority"] == "P2").sum())),
        "",
        "## Visual families",
        "",
    ]
    for k,v in reg["figure_family"].value_counts().sort_index().items():
        report.append(f"- {k}: {int(v)}")
    report += [
        "",
        "## Key design controls",
        "",
        "- endpoint return, drawdown magnitude and recovery duration use explicitly separated encodings;",
        "- B02 remains a three-sub-cycle timeline;",
        "- retrospective dating and post-anchor shocks retain mandatory hindsight labels;",
        "- 019/020 are rendered as negative method guardrails, not signals;",
        "- current 023 snapshot must display cycle qualification FALSE and freshness dates;",
        "- no visual spec contains an analog score, asset ranking or return forecast.",
        "",
        "024 is a specification layer. No rendered chart is treated as new empirical evidence.",
    ]
    (OUT / "FED_CYCLE_FIGURE_REGISTRY_024_REPORT.md").write_text("\n".join(report) + "\n")

    qc = {
        "qc_gate":"PASS",
        "module":"FED-CYCLE-FIGURE-REGISTRY-024",
        "upstream_qc":{"022B":q022b["qc_gate"],"023":q023["qc_gate"]},
        "figure_specs":int(len(reg)),
        "claim_linked_figure_specs":47,
        "supplemental_current_figure_specs":1,
        "unique_figure_keys":int(reg["figure_key"].nunique()),
        "context_figure_specs":int((reg["figure_family"]=="HISTORICAL_CONTEXT_CARD").sum()),
        "context_timing_preserved":True,
        "b02_three_subcycle_visual_guardrail":True,
        "b04_b06_post_anchor_shock_visual_guardrail":True,
        "b07_reverify_freshness_preserved":True,
        "p0_count":int(len(p0)),
        "p1_count":int((reg["priority"]=="P1").sum()),
        "p2_count":int((reg["priority"]=="P2").sum()),
        "blank_visual_boundary_fields":0,
        "analog_score_fields":0,
        "asset_ranking_fields":0,
        "forecast_return_fields":0,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n")


if __name__ == "__main__":
    main()
