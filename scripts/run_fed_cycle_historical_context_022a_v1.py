#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "research" / "FED_CYCLE_HISTORICAL_CONTEXT_022A_CLAIMS.csv"
EPISODES = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "CASEBOOK_EPISODES.csv"
Q022 = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "QC.json"
OUT = ROOT / "results" / "fed_cycle_historical_context_022a_v1"
OUT.mkdir(parents=True, exist_ok=True)

EXPECTED_EPISODES = ["B02","B03","B04","B05","B06","B07"]
VALID_CLASSES = {
    "CONTEMPORANEOUS_POLICY_CONTEXT",
    "RETROSPECTIVE_DATING",
    "POST_ANCHOR_SHOCK",
    "RETROSPECTIVE_EVENT_CONTEXT",
}


def boolify(v):
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() == "true"


def main():
    q022 = json.loads(Q022.read_text())
    if q022.get("qc_gate") != "PASS":
        raise RuntimeError("022 upstream QC must PASS")

    claims = pd.read_csv(CLAIMS, dtype=str, keep_default_na=False)
    episodes = pd.read_csv(EPISODES, dtype=str, keep_default_na=False)

    required = [
        "claim_id","broad_episode_id","event_date_or_period","relationship_to_first_cut",
        "claim_time_class","claim_text","source_institution","source_title","source_url",
        "source_publication_or_announcement_date","contemporaneous_known","hindsight_warning",
        "allowed_content_use","forbidden_inference",
    ]
    missing = [c for c in required if c not in claims.columns]
    if missing:
        raise RuntimeError(f"missing columns: {missing}")

    if claims["claim_id"].duplicated().any():
        raise RuntimeError("duplicate claim_id")
    if sorted(claims["broad_episode_id"].unique()) != sorted(EXPECTED_EPISODES):
        raise RuntimeError("episode coverage changed")
    if set(claims["claim_time_class"]) - VALID_CLASSES:
        raise RuntimeError("invalid claim_time_class")
    if claims[required].apply(lambda s: s.str.strip().eq("")).any().any():
        raise RuntimeError("blank required claim field")

    counts = claims.groupby("broad_episode_id").size().to_dict()
    if any(counts.get(e) != 3 for e in EXPECTED_EPISODES):
        raise RuntimeError(f"expected 3 context claims per episode, got {counts}")

    claims["contemporaneous_known"] = claims["contemporaneous_known"].map(boolify)
    hindsight_classes = {"RETROSPECTIVE_DATING","POST_ANCHOR_SHOCK"}
    h = claims[claims["claim_time_class"].isin(hindsight_classes)]
    if h["hindsight_warning"].str.strip().eq("").any():
        raise RuntimeError("hindsight-sensitive row missing warning")

    # Frozen anti-hindsight assertions.
    b04shock = claims[
        (claims["broad_episode_id"]=="B04")
        & (claims["claim_time_class"]=="POST_ANCHOR_SHOCK")
        & claims["claim_text"].str.contains("September 11", case=False, regex=False)
    ]
    if len(b04shock) != 1:
        raise RuntimeError("B04 September 11 post-anchor shock guardrail missing")

    b06shock = claims[
        (claims["broad_episode_id"]=="B06")
        & (claims["claim_time_class"]=="POST_ANCHOR_SHOCK")
        & claims["claim_text"].str.contains("coronavirus", case=False, regex=False)
    ]
    if len(b06shock) != 1:
        raise RuntimeError("B06 COVID post-anchor shock guardrail missing")

    for bid in ["B04","B05"]:
        z = claims[(claims["broad_episode_id"]==bid) & (claims["claim_time_class"]=="RETROSPECTIVE_DATING")]
        if len(z) != 1 or z["contemporaneous_known"].any():
            raise RuntimeError(f"{bid} recession dating must be retrospective")

    b07 = claims[(claims["broad_episode_id"]=="B07") & claims["claim_text"].str.contains("most recent recognized", case=False, regex=False)]
    if len(b07) != 1:
        raise RuntimeError("B07 current NBER chronology audit missing")

    claims["evidence_class"] = "HISTORICAL_CONTEXT"
    claims["causal_status"] = "NONE"
    claims["oos_status"] = "NOT_A_FORECASTING_MODEL"
    claims["deployment_status"] = "NOT_DEPLOYABLE"
    claims["source_audit_date"] = "2026-09-25"

    claims.to_csv(OUT / "CONTEXT_CLAIMS.csv", index=False)

    # Expand multi-URL cells into a normalized source registry.
    src_rows = []
    for r in claims.itertuples(index=False):
        urls = [u.strip() for u in str(r.source_url).split(" | ")]
        for i, url in enumerate(urls, start=1):
            if not url.startswith("https://"):
                raise RuntimeError(f"non-https source URL: {url}")
            src_rows.append({
                "claim_id": r.claim_id,
                "broad_episode_id": r.broad_episode_id,
                "source_index": i,
                "source_institution": r.source_institution,
                "source_title": r.source_title,
                "source_url": url,
                "source_publication_or_announcement_date": r.source_publication_or_announcement_date,
                "source_audit_date": "2026-09-25",
            })
    sources = pd.DataFrame(src_rows)
    sources.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)

    # Episode-level content summary with explicit timing tags.
    lines = [
        "# FED-CYCLE-HISTORICAL-CONTEXT-022A — CASE CONTEXT SUMMARY",
        "",
        "This file enriches 022 with independently sourced public context. "
        "It does not alter the audited policy chronology or market-path metrics.",
        "",
        "Timing tags are mandatory: contemporaneous policy context is distinct from retrospective dating and later shocks.",
        "",
    ]
    ep_label = episodes.set_index("broad_episode_id")["content_label"].to_dict()
    for bid in EXPECTED_EPISODES:
        lines += [f"## {bid} — {ep_label[bid]}", ""]
        for r in claims[claims["broad_episode_id"]==bid].itertuples(index=False):
            known = "known/observable at the time" if r.contemporaneous_known else "not contemporaneously available as this later classification/context"
            lines.append(
                f"- **{r.claim_time_class}** ({r.event_date_or_period}; {r.relationship_to_first_cut}): "
                f"{r.claim_text} [{known}]"
            )
            lines.append(f"  - Use: {r.allowed_content_use}")
            lines.append(f"  - Guardrail: {r.hindsight_warning} {r.forbidden_inference}")
        lines.append("")
    (OUT / "CASE_CONTEXT_SUMMARY.md").write_text("\n".join(lines) + "\n")

    ref = {
        "module": "FED-CYCLE-HISTORICAL-CONTEXT-022A",
        "as_of": "2026-09-25",
        "upstream": "FED-CYCLE-HISTORICAL-CASEBOOK-022",
        "claim_time_taxonomy": sorted(VALID_CLASSES),
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
        "episodes": {},
    }
    for bid in EXPECTED_EPISODES:
        ref["episodes"][bid] = json.loads(
            claims[claims["broad_episode_id"]==bid].to_json(orient="records")
        )
    (OUT / "HISTORICAL_CONTEXT_REFERENCE.json").write_text(
        json.dumps(ref, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    )

    report = [
        "# FED-CYCLE-HISTORICAL-CONTEXT-022A — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED SOURCED CONTEXT REGISTRY / ANTI-HINDSIGHT LAYER / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- context claims: {len(claims)}",
        f"- broad episodes: {claims['broad_episode_id'].nunique()}",
        f"- normalized source links: {len(sources)}",
        "",
        "## Claim-time mix",
        "",
    ]
    for k,v in claims["claim_time_class"].value_counts().sort_index().items():
        report.append(f"- {k}: {int(v)}")
    report += [
        "",
        "## Binding interpretation rules",
        "",
        "- 2001 and 2007 recession dates are later NBER determinations, not facts known at the respective first-cut dates.",
        "- September 11, 2001 is a post-January-2001 shock inside the later market path.",
        "- COVID-19 is a post-July-2019 shock and is not part of the 2019 first-cut rationale.",
        "- B07's current NBER chronology status is reported only as-of the 2026-09-25 source audit; it is not a recession forecast.",
        "- Official statements provide stated policy context, not a structural causal decomposition of asset outcomes.",
        "",
        "022 remains canonical for cycle dates and asset metrics. 022A only adds sourced historical context.",
    ]
    (OUT / "FED_CYCLE_HISTORICAL_CONTEXT_022A_REPORT.md").write_text("\n".join(report) + "\n")

    qc = {
        "qc_gate": "PASS",
        "module": "FED-CYCLE-HISTORICAL-CONTEXT-022A",
        "upstream_022_qc": "PASS",
        "context_claim_rows": int(len(claims)),
        "broad_episodes": int(claims["broad_episode_id"].nunique()),
        "claims_per_episode": counts,
        "normalized_source_links": int(len(sources)),
        "claim_time_classes": sorted(claims["claim_time_class"].unique()),
        "blank_required_fields": 0,
        "duplicate_claim_ids": 0,
        "b04_september11_post_anchor_guardrail": True,
        "b06_covid_post_anchor_guardrail": True,
        "b04_b05_recession_dating_retrospective": True,
        "b07_current_nber_chronology_audit": True,
        "private_paper_inputs_used": False,
        "new_price_estimation": False,
        "new_inference": False,
        "pvalues_generated": False,
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n")


if __name__ == "__main__":
    main()
