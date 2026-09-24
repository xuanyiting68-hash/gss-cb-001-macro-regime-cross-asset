#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1"
OUT.mkdir(parents=True, exist_ok=True)

MASTER = ROOT / "results" / "fed_cycle_cross_asset_master_synthesis_v1" / "MASTER_ASSET_PHASE_MAP.csv"
Q021 = ROOT / "results" / "fed_cycle_cross_asset_master_synthesis_v1" / "QC.json"
CASE_ASSETS = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "CASEBOOK_ASSET_PHASE_METRICS.csv"
EPISODES = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "CASEBOOK_EPISODES.csv"
Q022 = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "QC.json"
CONTEXT = ROOT / "results" / "fed_cycle_historical_context_022a_v1" / "CONTEXT_CLAIMS.csv"
Q022A = ROOT / "results" / "fed_cycle_historical_context_022a_v1" / "QC.json"
Q019 = ROOT / "results" / "fed_cycle_precut_state_v1" / "QC.json"
Q020 = ROOT / "results" / "fed_cycle_precut_stress_level_v1" / "QC.json"
Q017 = ROOT / "results" / "fed_cycle_total_risk_clock_v1" / "QC.json"

CORE = ["DXY", "GOLD", "NASDAQ", "SP500", "WTI"]
PHASES = ["FIRST_HIKE", "LAST_HIKE", "PAUSE_START", "FIRST_CUT"]
EP_IDS = ["B02", "B03", "B04", "B05", "B06", "B07"]

REQUIRED = [
    "claim_id","claim_family","claim_status","title_short","canonical_wording",
    "asset","phase","broad_episode_id","metric_payload","sample_descriptor",
    "support_status","evidence_class","evidence_time","source_modules","source_files",
    "official_source_urls","allowed_wording","prohibited_wording","freshness_rule",
    "figure_key","content_tags","causal_status","oos_status","deployment_status",
]

def read_pass(path: Path):
    q = json.loads(path.read_text())
    if q.get("qc_gate") != "PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def pct(x):
    return f"{float(x)*100:+.2f}%"

def magpct(x):
    return f"{float(x)*100:.2f}%"

def month(x):
    return "NA" if pd.isna(x) else str(int(round(float(x))))

def clean(v):
    return "" if pd.isna(v) else str(v)

def base_row(**kwargs):
    row = {c: "" for c in REQUIRED}
    row.update({
        "claim_status": "CANONICAL_PUBLIC_SAFE",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    })
    row.update(kwargs)
    return row

def build_phase_claims(master: pd.DataFrame):
    rows=[]
    z=master[(master["asset"].isin(CORE)) & (master["phase"].isin(PHASES))].copy()
    if len(z) != 20:
        raise RuntimeError(f"expected 20 core phase rows, got {len(z)}")
    for asset in CORE:
        for phase in PHASES:
            g=z[(z["asset"]==asset)&(z["phase"]==phase)]
            if len(g)!=1:
                raise RuntimeError(f"missing/duplicate core phase row {asset} {phase}")
            r=g.iloc[0]
            full = r["weighted_km_median_anchor_to_100_months"]
            wording=(
                f"Across the supported historical broad-episode sample, {asset} around {phase} had "
                f"a broad-episode-weighted median +12M endpoint of {pct(r['ret_12m'])}, "
                f"a 12M maximum-drawdown magnitude of {magpct(r['path_risk_value'])}, "
                f"a median drawdown trough in month {month(r['trough_month'])}"
            )
            if pd.notna(full):
                wording += f", and an anchor-to-full-recovery Kaplan-Meier median of {month(full)} months."
            else:
                wording += "."
            payload={
                "ret_12m": None if pd.isna(r["ret_12m"]) else float(r["ret_12m"]),
                "path_risk_metric": r["path_risk_metric"],
                "path_risk_value": None if pd.isna(r["path_risk_value"]) else float(r["path_risk_value"]),
                "trough_month": None if pd.isna(r["trough_month"]) else float(r["trough_month"]),
                "anchor_to_full_recovery_months": None if pd.isna(full) else float(full),
                "n_legs": int(r["n_legs"]),
                "n_broad_episodes": int(r["n_broad_episodes"]),
            }
            tags=["LONG_VIDEO","DEEP_ARTICLE","IMAGE_CARD","PANDAAI"]
            if phase=="FIRST_CUT":
                tags += ["VIDEO_HOOK","SHORT_VIDEO","MYTH_VS_EVIDENCE"]
            rows.append(base_row(
                claim_id=f"CLM-PHASE-{asset}-{phase}",
                claim_family="CORE_PHASE_DISTRIBUTION",
                title_short=f"{asset} × {phase} historical path",
                canonical_wording=wording,
                asset=asset,
                phase=phase,
                metric_payload=json.dumps(payload, separators=(",",":"), ensure_ascii=False),
                sample_descriptor=f"{int(r['n_legs'])} mechanical legs / {int(r['n_broad_episodes'])} broad episodes",
                support_status=clean(r["support_status"]),
                evidence_class="DESCRIPTIVE",
                evidence_time="DESCRIPTIVE_PATH",
                source_modules=f"FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021|{r['source_module']}|FED-CYCLE-TOTAL-RISK-CLOCK-017",
                source_files="results/fed_cycle_cross_asset_master_synthesis_v1/MASTER_ASSET_PHASE_MAP.csv",
                official_source_urls="N/A_REPO_DERIVED",
                allowed_wording="Use as a historical descriptive distribution with sample/support stated or available; endpoint and path risk must remain distinct.",
                prohibited_wording="Do not say the Fed phase caused the return; do not call the trough month a forecast; do not convert the median into a trading/allocation instruction.",
                freshness_rule="STATIC_UNLESS_UPSTREAM_REBUILT",
                figure_key=f"FIG-PHASE-{asset}-{phase}",
                content_tags="|".join(tags),
            ))
    return rows

def build_case_claims(case_assets: pd.DataFrame, episodes: pd.DataFrame):
    rows=[]
    ep=episodes.set_index("broad_episode_id")
    # B02 is structure-only by design.
    b02=ep.loc["B02"]
    rows.append(base_row(
        claim_id="CLM-CASE-B02",
        claim_family="HISTORICAL_CASE",
        title_short="1987-89 is a multi-leg episode",
        canonical_wording=(
            "The 1987-1989 broad episode B02 contains three separate mechanical tightening/easing sub-cycles "
            "(T03_1987, T04_1987 and T05_1988); the canonical casebook preserves them separately rather than "
            "constructing one synthetic FIRST_HIKE-to-FIRST_CUT policy path."
        ),
        broad_episode_id="B02",
        metric_payload=json.dumps({"n_mechanical_cycles":3,"cycle_ids":["T03_1987","T04_1987","T05_1988"]}, separators=(",",":")),
        sample_descriptor="B02 / 3 mechanical sub-cycles",
        support_status="CANONICAL_STRUCTURE",
        evidence_class="DESCRIPTIVE",
        evidence_time="RETROSPECTIVE_CHRONOLOGY",
        source_modules="FED-CYCLE-HISTORICAL-CASEBOOK-022",
        source_files="results/fed_cycle_historical_casebook_v1/CASEBOOK_EPISODES.csv",
        official_source_urls="N/A_REPO_DERIVED",
        allowed_wording="Use to explain that 1987-89 is structurally more complex than a single standard tightening cycle.",
        prohibited_wording="Do not aggregate B02 into one fictitious policy path or treat its three sub-cycles as three independent broad episodes.",
        freshness_rule="STATIC_UNLESS_UPSTREAM_REBUILT",
        figure_key="FIG-CASE-B02",
        content_tags="LONG_VIDEO|DEEP_ARTICLE|CASE_STUDY|IMAGE_CARD|PANDAAI",
    ))

    for bid in ["B03","B04","B05","B06","B07"]:
        g=case_assets[
            (case_assets["broad_episode_id"]==bid)
            & (case_assets["anchor"]=="FIRST_CUT")
            & (case_assets["asset"].isin(["GOLD","NASDAQ","SP500","WTI"]))
        ].copy()
        if len(g)!=4 or g["cycle_id"].nunique()!=1:
            raise RuntimeError(f"{bid} FIRST_CUT case support changed")
        cycle=g["cycle_id"].iloc[0]
        parts=[]
        payload={}
        for asset in ["GOLD","NASDAQ","SP500","WTI"]:
            r=g[g["asset"]==asset].iloc[0]
            parts.append(
                f"{asset} +12M {pct(r['ret_12m'])}, 12M MDD {magpct(r['mdd_12m'])}, trough month {month(r['mdd_trough_month'])}"
            )
            payload[asset]={
                "ret_12m":float(r["ret_12m"]),
                "mdd_12m":float(r["mdd_12m"]),
                "trough_month":int(r["mdd_trough_month"]),
            }
        label=ep.loc[bid,"content_label"]
        wording=f"In the {label} ({cycle}) FIRST_CUT case, " + "; ".join(parts) + "."
        rows.append(base_row(
            claim_id=f"CLM-CASE-{bid}",
            claim_family="HISTORICAL_CASE",
            title_short=f"{bid} FIRST_CUT four-asset path",
            canonical_wording=wording,
            phase="FIRST_CUT",
            broad_episode_id=bid,
            metric_payload=json.dumps(payload, separators=(",",":"), ensure_ascii=False),
            sample_descriptor=f"{bid} / one mechanical cycle / four core assets",
            support_status="CASE_DESCRIPTIVE",
            evidence_class="DESCRIPTIVE",
            evidence_time="DESCRIPTIVE_PATH",
            source_modules="FED-CYCLE-HISTORICAL-CASEBOOK-022|FED-CYCLE-PHASE-CLOCK-004",
            source_files="results/fed_cycle_historical_casebook_v1/CASEBOOK_ASSET_PHASE_METRICS.csv",
            official_source_urls="N/A_REPO_DERIVED",
            allowed_wording="Use as a dated historical case path; pair with 022A context when explaining why the episode differed from another episode.",
            prohibited_wording="Do not call this the correct current analog; do not attribute the asset path causally to the first cut; do not omit later-shock caveats where 022A identifies them.",
            freshness_rule="STATIC_UNLESS_UPSTREAM_REBUILT",
            figure_key=f"FIG-CASE-{bid}",
            content_tags="VIDEO_HOOK|SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|CASE_STUDY|IMAGE_CARD|PANDAAI",
        ))
    return rows

def build_context_claims(context: pd.DataFrame):
    rows=[]
    if len(context)!=18 or context["claim_id"].nunique()!=18:
        raise RuntimeError("022A context universe changed")
    for r in context.itertuples(index=False):
        freshness="REVERIFY_BEFORE_CURRENT_USE" if r.claim_id=="B07_CTX_02" else "STATIC_SOURCE_AUDIT"
        tags=["LONG_VIDEO","DEEP_ARTICLE","CASE_STUDY","PANDAAI"]
        if r.claim_time_class in {"RETROSPECTIVE_DATING","POST_ANCHOR_SHOCK"}:
            tags.append("MYTH_VS_EVIDENCE")
        payload={
            "event_date_or_period":r.event_date_or_period,
            "relationship_to_first_cut":r.relationship_to_first_cut,
            "contemporaneous_known":bool(r.contemporaneous_known),
            "source_publication_or_announcement_date":r.source_publication_or_announcement_date,
        }
        rows.append(base_row(
            claim_id=f"CLM-CTX-{r.claim_id}",
            claim_family="HISTORICAL_CONTEXT",
            title_short=f"{r.broad_episode_id} context: {r.claim_time_class}",
            canonical_wording=r.claim_text,
            broad_episode_id=r.broad_episode_id,
            metric_payload=json.dumps(payload, separators=(",",":"), ensure_ascii=False),
            sample_descriptor=f"Official-source context claim / {r.broad_episode_id}",
            support_status="OFFICIAL_SOURCE_CONTEXT",
            evidence_class=r.evidence_class,
            evidence_time=r.claim_time_class,
            source_modules="FED-CYCLE-HISTORICAL-CONTEXT-022A",
            source_files="results/fed_cycle_historical_context_022a_v1/CONTEXT_CLAIMS.csv",
            official_source_urls=r.source_url,
            allowed_wording=f"{r.allowed_content_use} Hindsight warning: {r.hindsight_warning}",
            prohibited_wording=r.forbidden_inference,
            freshness_rule=freshness,
            figure_key=f"FIG-CTX-{r.claim_id}",
            content_tags="|".join(tags),
        ))
    return rows

def build_guardrails(q019, q020, q017):
    rows=[]
    rows.append(base_row(
        claim_id="CLM-GUARD-019",
        claim_family="METHOD_GUARDRAIL",
        title_short="Binary pre-cut timing rule not supported",
        canonical_wording=(
            "In the predetermined pre-FIRST_CUT state diagnostic, 8 mechanical cycles collapsed to 6 broad episodes. "
            "Real-time growth contraction had no positive broad episodes, NFCI-tight conditions had only one, and the balanced "
            "curve-inversion split had the same median risk-asset trough month (8) on both sides; the simple binary state rule was not supported."
        ),
        phase="FIRST_CUT",
        metric_payload=json.dumps({
            "mechanical_cycles":8,"broad_episodes":6,
            "curve_inverted_true":3,"curve_inverted_false":3,
            "median_risk3_trough_month_curve_true":8,
            "median_risk3_trough_month_curve_false":8
        }, separators=(",",":")),
        sample_descriptor="8 mechanical cycles / 6 broad episodes",
        support_status="SIMPLE_STATE_RULE_NOT_SUPPORTED",
        evidence_class="DESCRIPTIVE_NEGATIVE_RESULT",
        evidence_time="RESEARCH_CONCLUSION",
        source_modules="FED-CYCLE-PRECUT-STATE-019",
        source_files="results/fed_cycle_precut_state_v1/FED_CYCLE_PRECUT_STATE_019_REPORT.md",
        official_source_urls="N/A_REPO_DERIVED",
        allowed_wording="Use as a negative guardrail: simple predetermined binary state variables did not validate a bottom-timing rule in this sample.",
        prohibited_wording="Do not present the composite count, curve state, NFCI or real-time growth flag as a validated timing score.",
        freshness_rule="STATIC_UNLESS_NEW_PREREGISTERED_EVIDENCE",
        figure_key="FIG-GUARD-019",
        content_tags="MYTH_VS_EVIDENCE|METHODS|DEEP_ARTICLE|PANDAAI|CURRENT_CONTEXT_GUARDRAIL",
    ))
    rows.append(base_row(
        claim_id="CLM-GUARD-020",
        claim_family="METHOD_GUARDRAIL",
        title_short="Continuous pre-cut levels did not rescue timing",
        canonical_wording=(
            "The continuous pre-FIRST_CUT stress-level extension also failed to produce a composition-robust timing relation: "
            "full-sample trough-month Spearman rho was about +0.075 for Baa spread, -0.211 for VIX (5 episodes), +0.029 for curve stress "
            "and -0.177 for real-time growth stress, with leave-one-out sign instability; the small-sample timing-rule branch was stopped."
        ),
        phase="FIRST_CUT",
        metric_payload=json.dumps({
            "broad_episodes":6,"vix_broad_episodes":5,
            "rho_baa":0.0746352,"rho_vix":-0.210819,"rho_curve":0.0294245,"rho_growth":-0.176547,
            "branch_decision":"STOP_SMALL_SAMPLE_TIMING_RULE_BRANCH"
        }, separators=(",",":")),
        sample_descriptor="6 broad episodes; VIX available in 5",
        support_status="CONTINUOUS_LEVEL_RULE_NOT_SUPPORTED",
        evidence_class="MECHANISM_CANDIDATE_NEGATIVE_RESULT",
        evidence_time="RESEARCH_CONCLUSION",
        source_modules="FED-CYCLE-PRECUT-STRESS-LEVEL-020",
        source_files="results/fed_cycle_precut_stress_level_v1/FED_CYCLE_PRECUT_STRESS_LEVEL_020_REPORT.md",
        official_source_urls="N/A_REPO_DERIVED",
        allowed_wording="Use as a methodological guardrail showing that continuous predetermined levels did not rescue the small-sample timing hypothesis.",
        prohibited_wording="Do not cherry-pick the five-episode curve relation, add thresholds/interactions, or build a multivariate timing score from this branch.",
        freshness_rule="STATIC_UNLESS_NEW_PREREGISTERED_EVIDENCE",
        figure_key="FIG-GUARD-020",
        content_tags="MYTH_VS_EVIDENCE|METHODS|DEEP_ARTICLE|PANDAAI|CURRENT_CONTEXT_GUARDRAIL",
    ))
    rows.append(base_row(
        claim_id="CLM-SYNTH-017-FIRSTCUT-RECOVERY",
        claim_family="SYNTHESIS",
        title_short="First cut did not shorten full recovery versus pause",
        canonical_wording=(
            "Across the five fully supported four-phase assets (DXY, Gold, Nasdaq, S&P 500 and WTI), the historical anchor-to-full-recovery "
            "clock after FIRST_CUT was slower than after PAUSE_START in 3 of 5 assets, equal in 2 of 5, and faster in 0 of 5."
        ),
        phase="FIRST_CUT",
        metric_payload=json.dumps({"assets":5,"slower":3,"equal":2,"faster":0}, separators=(",",":")),
        sample_descriptor="5 fully supported four-phase assets",
        support_status="SUPPORTED_DESCRIPTIVE_SYNTHESIS",
        evidence_class="DESCRIPTIVE",
        evidence_time="RESEARCH_CONCLUSION",
        source_modules="FED-CYCLE-TOTAL-RISK-CLOCK-017|FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021",
        source_files="results/fed_cycle_total_risk_clock_v1/SUPPORTED_TOTAL_CLOCK_SUMMARY.csv",
        official_source_urls="N/A_REPO_DERIVED",
        allowed_wording="Use to challenge the simplistic idea that the first cut automatically starts a faster full-recovery clock.",
        prohibited_wording="Do not infer causality from the phase label; do not generalize beyond the supported five-asset historical sample.",
        freshness_rule="STATIC_UNLESS_UPSTREAM_REBUILT",
        figure_key="FIG-RECOVERY-FIRSTCUT-VS-PAUSE",
        content_tags="VIDEO_HOOK|SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|IMAGE_CARD|MYTH_VS_EVIDENCE|PANDAAI",
    ))
    return rows

def content_pack_index(df: pd.DataFrame):
    ids=set(df["claim_id"])
    packs=[
        ("PACK-01-FIRST-CUT-NOT-THE-BOTTOM",
         "First cut does not mean path risk is finished",
         [f"CLM-PHASE-{a}-FIRST_CUT" for a in CORE]
         + ["CLM-SYNTH-017-FIRSTCUT-RECOVERY","CLM-GUARD-019","CLM-GUARD-020"]
         + ["CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07"]),
        ("PACK-02-SAME-LABEL-DIFFERENT-PATHS",
         "Same FIRST_CUT label, very different historical paths",
         ["CLM-CASE-B03","CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07"]),
        ("PACK-03-GOLD-VS-EQUITIES",
         "Gold versus U.S. equities across cycle phases and cases",
         [f"CLM-PHASE-GOLD-{p}" for p in PHASES]
         + [f"CLM-PHASE-SP500-{p}" for p in PHASES]
         + [f"CLM-PHASE-NASDAQ-{p}" for p in PHASES]
         + ["CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07"]),
        ("PACK-04-HINDSIGHT-TRAPS",
         "What was known then versus what was only known later",
         [f"CLM-CTX-{x}" for x in [
             "B04_CTX_02","B04_CTX_03","B05_CTX_03","B06_CTX_02","B06_CTX_03","B07_CTX_02"
         ]]),
        ("PACK-05-RECOVERY-CLOCK",
         "Why endpoint returns and full recovery clocks are different",
         [f"CLM-PHASE-{a}-{p}" for a in CORE for p in PHASES]
         + ["CLM-SYNTH-017-FIRSTCUT-RECOVERY"]),
        ("PACK-06-1987-MULTI-LEG",
         "Why 1987-89 should not be forced into one standard cycle",
         ["CLM-CASE-B02","CLM-CTX-B02_CTX_01","CLM-CTX-B02_CTX_02","CLM-CTX-B02_CTX_03"]),
    ]
    for _,_,refs in packs:
        missing=[r for r in refs if r not in ids]
        if missing: raise RuntimeError(f"content pack missing claims: {missing}")
    lines=[
        "# FED Cycle Content Pack Index — 022B",
        "",
        "These are routing bundles, not finished scripts. Every factual statement should still resolve to a canonical CLAIM_ID.",
        "",
    ]
    for pid,title,refs in packs:
        lines += [f"## {pid} — {title}", "", "Claims:", ""]
        for cid in refs:
            row=df[df["claim_id"]==cid].iloc[0]
            lines.append(f"- `{cid}` — {row['title_short']}")
        lines += [
            "",
            "Boundary: preserve each claim's evidence-time, support, freshness and prohibited-wording fields.",
            "",
        ]
    return "\n".join(lines)+"\n", len(packs)

def main():
    q021=read_pass(Q021); q022=read_pass(Q022); q022a=read_pass(Q022A)
    q019=read_pass(Q019); q020=read_pass(Q020); q017=read_pass(Q017)

    master=pd.read_csv(MASTER)
    case_assets=pd.read_csv(CASE_ASSETS)
    episodes=pd.read_csv(EPISODES)
    context=pd.read_csv(CONTEXT)

    rows=[]
    rows += build_phase_claims(master)
    rows += build_case_claims(case_assets, episodes)
    rows += build_context_claims(context)
    rows += build_guardrails(q019,q020,q017)
    df=pd.DataFrame(rows)[REQUIRED]

    # Core QC.
    if len(df)!=47 or df["claim_id"].nunique()!=47:
        raise RuntimeError(f"expected 47 unique claims, got {len(df)} / {df['claim_id'].nunique()}")
    fam=df["claim_family"].value_counts().to_dict()
    if fam.get("CORE_PHASE_DISTRIBUTION")!=20: raise RuntimeError(fam)
    if fam.get("HISTORICAL_CASE")!=6: raise RuntimeError(fam)
    if fam.get("HISTORICAL_CONTEXT")!=18: raise RuntimeError(fam)
    if fam.get("METHOD_GUARDRAIL",0)+fam.get("SYNTHESIS",0)!=3: raise RuntimeError(fam)
    phase=df[df["claim_family"]=="CORE_PHASE_DISTRIBUTION"]
    for asset in CORE:
        g=phase[phase["asset"]==asset]
        if len(g)!=4 or set(g["phase"])!=set(PHASES):
            raise RuntimeError(f"phase claim coverage failed {asset}")
    ctx=df[df["claim_family"]=="HISTORICAL_CONTEXT"]
    expected={f"CLM-CTX-{x}" for x in context["claim_id"]}
    if set(ctx["claim_id"])!=expected:
        raise RuntimeError("022A context mapping is not 1:1")
    if "three separate mechanical" not in df.loc[df["claim_id"]=="CLM-CASE-B02","canonical_wording"].iloc[0]:
        raise RuntimeError("B02 multi-leg guardrail lost")
    b04=df[df["claim_id"]=="CLM-CTX-B04_CTX_03"].iloc[0]
    if b04["evidence_time"]!="POST_ANCHOR_SHOCK":
        raise RuntimeError("B04 September 11 timing class lost")
    b06=df[df["claim_id"]=="CLM-CTX-B06_CTX_03"].iloc[0]
    if b06["evidence_time"]!="POST_ANCHOR_SHOCK":
        raise RuntimeError("B06 COVID timing class lost")
    b07=df[df["claim_id"]=="CLM-CTX-B07_CTX_02"].iloc[0]
    if b07["freshness_rule"]!="REVERIFY_BEFORE_CURRENT_USE":
        raise RuntimeError("B07 current NBER freshness rule lost")
    boundary_cols=["canonical_wording","sample_descriptor","support_status","evidence_class","evidence_time",
                   "source_modules","source_files","official_source_urls","allowed_wording","prohibited_wording",
                   "freshness_rule","figure_key","content_tags"]
    if df[boundary_cols].apply(lambda x:x.astype(str).str.strip().eq("")).any().any():
        raise RuntimeError("blank boundary/source field")
    if not (df["causal_status"]=="NONE").all(): raise RuntimeError("causal promotion")
    if not (df["oos_status"]=="NOT_A_FORECASTING_MODEL").all(): raise RuntimeError("OOS promotion")
    if not (df["deployment_status"]=="NOT_DEPLOYABLE").all(): raise RuntimeError("deployment promotion")

    df.to_csv(OUT/"CLAIM_REGISTRY.csv",index=False)
    (OUT/"CLAIM_REGISTRY.json").write_text(
        json.dumps({
            "module":"FED-CYCLE-CONTENT-CLAIM-REGISTRY-022B",
            "as_of":"2026-09-25",
            "claim_count":47,
            "claims":json.loads(df.to_json(orient="records")),
        },indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    )
    pack_text,pack_count=content_pack_index(df)
    (OUT/"CONTENT_PACK_INDEX.md").write_text(pack_text)

    report=[
        "# FED-CYCLE-CONTENT-CLAIM-REGISTRY-022B — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED CANONICAL CONTENT CLAIM REGISTRY / PUBLIC-SAFE / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- canonical claims: {len(df)}",
        f"- content routing packs: {pack_count}",
        f"- core asset x phase claims: {fam.get('CORE_PHASE_DISTRIBUTION',0)}",
        f"- historical case claims: {fam.get('HISTORICAL_CASE',0)}",
        f"- official-source historical context claims: {fam.get('HISTORICAL_CONTEXT',0)}",
        f"- guardrail/synthesis claims: {fam.get('METHOD_GUARDRAIL',0)+fam.get('SYNTHESIS',0)}",
        "",
        "## Publishing architecture",
        "",
        "A content title or hook may vary by platform, but factual payloads should resolve to a stable CLAIM_ID. "
        "The registry stores canonical wording, support/sample, evidence-time, sources, allowed wording, prohibited wording, freshness and future figure dependency.",
        "",
        "## High-value content bundles",
        "",
        "- FIRST_CUT_NOT_THE_BOTTOM: combines first-cut path distributions, historical cases, recovery-clock evidence and the negative 019/020 timing-rule guardrails.",
        "- SAME_LABEL_DIFFERENT_PATHS: compares B03-B07 without selecting a current analog.",
        "- GOLD_VS_EQUITIES: compares Gold, S&P 500 and Nasdaq evidence across phases/cases without ranking an asset as best.",
        "- HINDSIGHT_TRAPS: separates later NBER dating and later shocks from contemporaneous policy context.",
        "- RECOVERY_CLOCK: keeps endpoint return, interim MDD and full-recovery clock separate.",
        "- 1987_MULTI_LEG: prevents the 1987-89 sequence from being flattened into one standard cycle.",
        "",
        "## Boundary",
        "",
        "022B is a publishing/retrieval control layer. It creates no new empirical evidence, no asset ranking, no current analog selection and no trading recommendation.",
    ]
    (OUT/"FED_CYCLE_CONTENT_CLAIM_REGISTRY_022B_REPORT.md").write_text("\n".join(report)+"\n")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-CONTENT-CLAIM-REGISTRY-022B",
        "upstream_qc":{"021":q021["qc_gate"],"022":q022["qc_gate"],"022A":q022a["qc_gate"],"019":q019["qc_gate"],"020":q020["qc_gate"],"017":q017["qc_gate"]},
        "claim_rows":int(len(df)),
        "unique_claim_ids":int(df["claim_id"].nunique()),
        "claim_family_counts":fam,
        "core_assets":CORE,
        "core_phase_claims_per_asset":{a:int((phase["asset"]==a).sum()) for a in CORE},
        "context_1to1_mapping":True,
        "b02_multi_leg_guardrail":True,
        "b04_september11_post_anchor_guardrail":True,
        "b06_covid_post_anchor_guardrail":True,
        "b07_current_nber_reverify_rule":True,
        "blank_boundary_source_fields":0,
        "content_pack_count":pack_count,
        "new_price_estimation":False,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n")

if __name__=="__main__":
    main()
