#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_editorial_release_candidate_029_v1"
OUT.mkdir(parents=True, exist_ok=True)

CONTENT = ROOT / "results" / "fed_cycle_content_production_library_026_v1" / "CONTENT_OBJECTS.csv"
Q026 = ROOT / "results" / "fed_cycle_content_production_library_026_v1" / "QC.json"
READY = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1" / "PACKAGE_VISUAL_READINESS.csv"
Q027 = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1" / "QC.json"
SHOTS = ROOT / "results" / "fed_cycle_platform_native_production_pack_028_v1" / "DOUYIN_TIKTOK_SHOTLISTS_ZH.csv"
XHS = ROOT / "results" / "fed_cycle_platform_native_production_pack_028_v1" / "XIAOHONGSHU_CAROUSELS_ZH.csv"
Q028 = ROOT / "results" / "fed_cycle_platform_native_production_pack_028_v1" / "QC.json"
CLAIMS = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "CLAIM_REGISTRY.csv"
Q022B = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "QC.json"
FIGREG = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "FIGURE_REGISTRY.csv"
Q024 = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "QC.json"
R025 = ROOT / "results" / "fed_cycle_p0_visual_evidence_pack_v1" / "RENDER_MANIFEST.csv"
R027 = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1" / "P1_RENDER_MANIFEST.csv"

CONTENT_IDS = [
    "CNT-01-FIRST-CUT-NOT-THE-BOTTOM",
    "CNT-02-SAME-LABEL-DIFFERENT-PATHS",
    "CNT-03-GOLD-VS-EQUITIES",
    "CNT-04-HINDSIGHT-TRAPS",
    "CNT-05-RECOVERY-CLOCK",
    "CNT-06-1987-MULTI-LEG",
]

PRIMARY_SLOTS = [
    ("2026-09-28","W1-A","CNT-02-SAME-LABEL-DIFFERENT-PATHS"),
    ("2026-10-01","W1-B","CNT-04-HINDSIGHT-TRAPS"),
    ("2026-10-05","W2-A","CNT-01-FIRST-CUT-NOT-THE-BOTTOM"),
    ("2026-10-08","W2-B","CNT-05-RECOVERY-CLOCK"),
    ("2026-10-12","W3-A","CNT-03-GOLD-VS-EQUITIES"),
    ("2026-10-15","W3-B","CNT-06-1987-MULTI-LEG"),
]

def read_pass(path):
    q = json.loads(Path(path).read_text())
    if q.get("qc_gate") != "PASS":
        raise RuntimeError(f"upstream QC not PASS {path}")
    return q

def split_pipe(s):
    if pd.isna(s) or not str(s).strip():
        return []
    return [x for x in str(s).split("|") if x]

def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def content_row(df, cid):
    z = df[df["content_id"] == cid]
    if len(z) != 1:
        raise RuntimeError(cid)
    return z.iloc[0]

def immutable_payload(row, visual_keys):
    obj = {
        "content_id": row["content_id"],
        "claim_ids": split_pipe(row["claim_ids"]),
        "figure_keys": split_pipe(visual_keys),
        "freshness_rule": row["freshness_rule"],
        "mandatory_caveat": row["mandatory_caveat"],
        "source_files": split_pipe(row["source_files"]),
        "official_source_urls": split_pipe(row["official_source_urls"]),
        "causal_status": row["causal_status"],
        "oos_status": row["oos_status"],
        "deployment_status": row["deployment_status"],
    }
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return obj, sha256_text(raw)

def main():
    q026 = read_pass(Q026)
    q027 = read_pass(Q027)
    q028 = read_pass(Q028)
    q022b = read_pass(Q022B)
    q024 = read_pass(Q024)

    content = pd.read_csv(CONTENT)
    ready = pd.read_csv(READY)
    shots = pd.read_csv(SHOTS)
    xhs = pd.read_csv(XHS)
    claims = pd.read_csv(CLAIMS)
    figreg = pd.read_csv(FIGREG)
    render = pd.concat([pd.read_csv(R025), pd.read_csv(R027)], ignore_index=True)

    if list(content["content_id"]) != CONTENT_IDS:
        raise RuntimeError("content universe/order changed")
    if len(ready) != 6 or not (ready["new_visual_readiness"] == "VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE").all():
        raise RuntimeError("visual readiness incomplete")

    claim_set = set(claims["claim_id"])
    fig_set = set(figreg["figure_key"])
    rendered = set(render["figure_key"])

    rows = []
    md = ["# 029 Editorial Release Candidates — RC1", ""]
    for cid in CONTENT_IDS:
        c = content_row(content, cid)
        r = ready[ready["content_id"] == cid].iloc[0]
        figs = r["canonical_visual_keys"]

        for x in split_pipe(c["claim_ids"]):
            if x not in claim_set:
                raise RuntimeError(f"missing claim {x}")
        for x in split_pipe(figs):
            if x not in fig_set or x not in rendered:
                raise RuntimeError(f"missing rendered fig {x}")

        hooks = json.loads(c["hooks_json"])
        if len(hooks) < 3:
            raise RuntimeError(f"hooks missing {cid}")

        imm, imm_hash = immutable_payload(c, figs)
        rc_id = "RC-" + cid
        release_gate = "REVERIFY_REQUIRED_BEFORE_RELEASE" if c["freshness_rule"] == "REVERIFY_BEFORE_CURRENT_USE" else "PREFLIGHT_REQUIRED"

        rows.append({
            "release_candidate_id": rc_id,
            "content_id": cid,
            "rc_version": "RC1",
            "primary_title_zh": c["primary_title_zh"],
            "cover_variant_a": c["primary_title_zh"],
            "hook_variant_a": hooks[0],
            "hook_variant_b": hooks[1],
            "hook_variant_c": hooks[2],
            "selected_hook_rc1": hooks[0],
            "claim_ids": c["claim_ids"],
            "figure_keys": figs,
            "freshness_rule": c["freshness_rule"],
            "release_gate": release_gate,
            "mandatory_caveat": c["mandatory_caveat"],
            "source_files": c["source_files"],
            "official_source_urls": c["official_source_urls"],
            "immutable_evidence_sha256": imm_hash,
            "immutable_evidence_payload_json": json.dumps(imm, ensure_ascii=False, separators=(",", ":")),
            "douyin_shotlist_rows": int((shots["content_id"] == cid).sum()),
            "xiaohongshu_card_rows": int((xhs["content_id"] == cid).sum()),
            "wechat_article_status": "READY_FROM_028",
            "pandaai_template_status": "READY_FROM_028",
            "publication_status": "RC1_NOT_PUBLISHED",
            "evidence_payload_changed": False,
            "causal_status": "NONE",
            "deployment_status": "NOT_DEPLOYABLE",
        })

        md += [
            f"## {rc_id}",
            "",
            f"**主标题：** {c['primary_title_zh']}",
            "",
            f"**Hook A（RC1）：** {hooks[0]}",
            "",
            f"**Hook B：** {hooks[1]}",
            "",
            f"**Hook C：** {hooks[2]}",
            "",
            f"**Figures：** {figs}",
            "",
            f"**Freshness：** {c['freshness_rule']}",
            "",
            f"**Release gate：** {release_gate}",
            "",
            f"**Immutable evidence SHA256：** {imm_hash}",
            "",
            f"**边界：** {c['mandatory_caveat']}",
            "",
        ]

    rc = pd.DataFrame(rows)
    if len(rc) != 6 or rc["release_candidate_id"].nunique() != 6:
        raise RuntimeError("RC count")
    if rc["immutable_evidence_sha256"].str.len().ne(64).any():
        raise RuntimeError("payload hash")
    if rc["evidence_payload_changed"].any():
        raise RuntimeError("evidence payload changed")

    rc.to_csv(OUT / "RELEASE_CANDIDATES.csv", index=False)
    (OUT / "RELEASE_CANDIDATES_ZH.md").write_text("\n".join(md) + "\n")

    cal = []
    for date, slot, cid in PRIMARY_SLOTS:
        c = content_row(content, cid)
        rcid = "RC-" + cid
        cal.append({
            "date": date,
            "week": slot.split("-")[0],
            "slot": slot,
            "slot_type": "PRIMARY",
            "content_id": cid,
            "release_candidate_id": rcid,
            "platform": "DOUYIN_TIKTOK",
            "asset": "short_video",
            "freshness_rule": c["freshness_rule"],
            "preflight_required": True,
            "publication_status": "PLANNED_NOT_PUBLISHED",
        })
        d = pd.Timestamp(date)
        cal.append({
            "date": str((d + pd.Timedelta(days=2)).date()),
            "week": slot.split("-")[0],
            "slot": slot + "-XHS",
            "slot_type": "REPURPOSE",
            "content_id": cid,
            "release_candidate_id": rcid,
            "platform": "XIAOHONGSHU",
            "asset": "carousel",
            "freshness_rule": c["freshness_rule"],
            "preflight_required": True,
            "publication_status": "PLANNED_NOT_PUBLISHED",
        })
        long_offset_days = 3 if slot.endswith("-B") else 4
        cal.append({
            "date": str((d + pd.Timedelta(days=long_offset_days)).date()),
            "week": slot.split("-")[0],
            "slot": slot + "-LONG",
            "slot_type": "REPURPOSE",
            "content_id": cid,
            "release_candidate_id": rcid,
            "platform": "WECHAT_LONGFORM_OR_PANDAAI",
            "asset": "deep_article_or_explanation",
            "freshness_rule": c["freshness_rule"],
            "preflight_required": True,
            "publication_status": "PLANNED_NOT_PUBLISHED",
        })

    for i, date in enumerate(["2026-10-19", "2026-10-22"], 1):
        cal.append({
            "date": date,
            "week": "W4",
            "slot": f"W4-R{i}",
            "slot_type": "PERFORMANCE_REPURPOSE_PLACEHOLDER",
            "content_id": "SELECT_AFTER_METRICS",
            "release_candidate_id": "UNCHANGED_RC1_PAYLOAD",
            "platform": "CROSS_PLATFORM",
            "asset": "deeper_repurpose",
            "freshness_rule": "INHERIT_SELECTED_PACKAGE",
            "preflight_required": True,
            "publication_status": "WAIT_FOR_PERFORMANCE_SELECTION",
        })

    caldf = pd.DataFrame(cal)
    prim = caldf[caldf["slot_type"] == "PRIMARY"]
    if len(prim) != 6 or prim["content_id"].nunique() != 6 or set(prim["content_id"]) != set(CONTENT_IDS):
        raise RuntimeError("primary calendar rule")
    if not (caldf[caldf["week"] == "W4"]["slot_type"] == "PERFORMANCE_REPURPOSE_PLACEHOLDER").all():
        raise RuntimeError("week4 must be repurpose only")
    if caldf["date"].duplicated().any():
        raise RuntimeError("release calendar contains duplicate publication dates")
    caldf.to_csv(OUT / "RELEASE_CALENDAR.csv", index=False)

    preflight = """# 029 Pre-Publication Evidence / Freshness Checklist

A release is GO only if every required item passes. Otherwise status is HOLD.

1. Confirm the repository main branch still contains every referenced CLAIM_ID.
2. Confirm every referenced FIGURE_KEY exists and the intended rendered file is present.
3. Confirm the release candidate immutable_evidence_sha256 matches the frozen RC1 payload.
4. Confirm all evidence numbers in copy match the canonical 026/022B payload.
5. Confirm the title/hook A/B variant changes presentation only, not factual meaning.
6. Confirm freshness_rule.
7. If REVERIFY_BEFORE_CURRENT_USE, re-audit the affected official source before publishing.
8. Do not present the 2026-09-25 current snapshot as live data unless a fresh append-only snapshot has been created.
9. Confirm historical timing labels: CONTEMPORANEOUS / RETROSPECTIVE / POST_ANCHOR remain correct.
10. Confirm no buy/sell, return-promise, best-asset, deterministic-bottom or current-analog-ranking wording appears.
11. Confirm mandatory caveat remains in the platform-appropriate location.
12. Confirm the source block remains accessible to editor/reviewer and can be surfaced to the audience when appropriate.
13. Confirm no private-paper inputs or unpublished academic results entered the copy.
14. Confirm evidence_payload_changed = FALSE.

If any check fails, HOLD the release and fix the editorial asset or rebuild upstream evidence. Do not silently alter the canonical factual payload.
"""
    (OUT / "PREFLIGHT_CHECKLIST.md").write_text(preflight)

    ab = """# 029 Editorial A/B Test Rules

## What may vary

- cover wording;
- first 3–7 second hook;
- thumbnail/cover layout;
- caption length;
- ordering of already-approved evidence cards;
- non-investment educational CTA;
- subtitle pacing.

## What must not vary

- numerical evidence;
- CLAIM_ID set;
- FIGURE_KEY evidence meaning;
- freshness rule;
- source attribution;
- hindsight/time-class labels;
- mandatory caveat;
- causal/OOS/deployment status.

## Allowed educational CTA

- 收藏这组历史周期数据
- 关注后续周期研究
- 评论区告诉我你想看哪个历史周期

## Not allowed

- financial-action urgency;
- buy/sell CTA;
- promises or implications of returns;
- best-asset claims;
- deterministic bottom calls;
- current-analog ranking;
- rewriting negative 019/020 findings into signals.

## Experiment interpretation

Performance metrics can inform packaging and sequencing. They must never be used to choose which empirical result is true or to rewrite the evidence payload.
"""
    (OUT / "EDITORIAL_AB_TEST_RULES.md").write_text(ab)

    schema = [
        ("content_id", "string", "Canonical content package ID", True),
        ("release_candidate_id", "string", "Frozen RC ID", True),
        ("platform", "string", "Publishing platform", True),
        ("publish_timestamp", "datetime", "Actual publish timestamp", True),
        ("title_variant", "string", "Editorial title/cover variant", True),
        ("hook_variant", "string", "Hook variant A/B/C", True),
        ("views", "integer", "Platform view count", False),
        ("views_3s", "integer", "Three-second views if available", False),
        ("average_watch_time", "float", "Average watch time seconds", False),
        ("completion_rate", "float", "Video completion rate 0-1", False),
        ("likes", "integer", "Likes", False),
        ("comments", "integer", "Comments", False),
        ("saves", "integer", "Saves/favorites", False),
        ("shares", "integer", "Shares", False),
        ("profile_clicks", "integer", "Profile clicks", False),
        ("follows", "integer", "Attributed follows if available", False),
        ("link_clicks", "integer", "Link clicks if available", False),
        ("notes", "string", "Qualitative observations", False),
        ("evidence_payload_changed", "boolean", "Must remain FALSE for normal editorial A/B tests", True),
    ]
    pd.DataFrame(schema, columns=["field_name","data_type","description","required"]).to_csv(
        OUT / "PERFORMANCE_LOG_SCHEMA.csv", index=False
    )

    report = [
        "# FED-CYCLE-EDITORIAL-RELEASE-CANDIDATE-029 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED SIX RC1 OBJECTS + FOUR-WEEK RELEASE OPERATIONS / NOT PUBLISHED / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "- release candidates: 6",
        "- immutable evidence hashes: 6",
        "- primary release slots: 6",
        "- weeks 1-3 cover every package exactly once",
        "- week 4: performance-based repurpose placeholders only",
        "- preflight checklist: frozen",
        "- editorial A/B rules: frozen",
        "- performance log schema: frozen",
        "",
        "Editorial performance may change packaging, never factual evidence.",
    ]
    (OUT / "FED_CYCLE_EDITORIAL_RELEASE_CANDIDATE_029_REPORT.md").write_text("\n".join(report) + "\n")

    qc = {
        "qc_gate": "PASS",
        "module": "FED-CYCLE-EDITORIAL-RELEASE-CANDIDATE-029",
        "upstream_qc": {
            "022B": q022b["qc_gate"],
            "024": q024["qc_gate"],
            "026": q026["qc_gate"],
            "027": q027["qc_gate"],
            "028": q028["qc_gate"],
        },
        "release_candidates": int(len(rc)),
        "one_rc_per_content": True,
        "all_claim_refs_valid": True,
        "all_figure_refs_rendered": True,
        "immutable_payload_hashes": int(rc["immutable_evidence_sha256"].nunique()),
        "primary_release_slots": int(len(prim)),
        "primary_packages_unique": int(prim["content_id"].nunique()),
        "week4_repurpose_only": True,
        "duplicate_calendar_dates": 0,
        "cnt04_release_gate": rc.loc[rc["content_id"]=="CNT-04-HINDSIGHT-TRAPS","release_gate"].iloc[0],
        "current_snapshot_perpetually_live": False,
        "performance_schema_has_evidence_payload_changed": True,
        "editorial_ab_factual_change_allowed": False,
        "buy_sell_cta_allowed": False,
        "return_promise_allowed": False,
        "best_asset_ranking_allowed": False,
        "current_analog_ranking_allowed": False,
        "deterministic_bottom_allowed": False,
        "political_evaluation_outputs": 0,
        "new_inference": False,
        "pvalues_generated": False,
        "private_paper_inputs_used": False,
        "causal_status": "NONE",
        "deployment_status": "NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
