#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_release_preflight_030_v1"
OUT.mkdir(parents=True, exist_ok=True)

RC = ROOT / "results" / "fed_cycle_editorial_release_candidate_029_v1" / "RELEASE_CANDIDATES.csv"
CAL = ROOT / "results" / "fed_cycle_editorial_release_candidate_029_v1" / "RELEASE_CALENDAR.csv"
Q029 = ROOT / "results" / "fed_cycle_editorial_release_candidate_029_v1" / "QC.json"
CLAIMS = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "CLAIM_REGISTRY.csv"
Q022B = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "QC.json"
FIGREG = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "FIGURE_REGISTRY.csv"
Q024 = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "QC.json"
R025 = ROOT / "results" / "fed_cycle_p0_visual_evidence_pack_v1" / "RENDER_MANIFEST.csv"
R027 = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1" / "P1_RENDER_MANIFEST.csv"
SHOTS = ROOT / "results" / "fed_cycle_platform_native_production_pack_028_v1" / "DOUYIN_TIKTOK_SHOTLISTS_ZH.csv"
XHS = ROOT / "results" / "fed_cycle_platform_native_production_pack_028_v1" / "XIAOHONGSHU_CAROUSELS_ZH.csv"
Q028 = ROOT / "results" / "fed_cycle_platform_native_production_pack_028_v1" / "QC.json"

ASSESSMENT_DATE = pd.Timestamp("2026-09-25")
CNT02 = "CNT-02-SAME-LABEL-DIFFERENT-PATHS"
CNT04 = "CNT-04-HINDSIGHT-TRAPS"

def read_pass(path):
    q=json.loads(Path(path).read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def split_pipe(x):
    if pd.isna(x) or not str(x).strip():
        return []
    return [v for v in str(x).split("|") if v]

def recompute_hash(payload_json):
    obj=json.loads(payload_json)
    raw=json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(",",":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def main():
    q029=read_pass(Q029); q022b=read_pass(Q022B); q024=read_pass(Q024); q028=read_pass(Q028)
    rc=pd.read_csv(RC)
    cal=pd.read_csv(CAL)
    claims=pd.read_csv(CLAIMS)
    figs=pd.read_csv(FIGREG)
    render=pd.concat([pd.read_csv(R025),pd.read_csv(R027)],ignore_index=True)
    shots=pd.read_csv(SHOTS)
    xhs=pd.read_csv(XHS)

    if len(rc)!=6 or rc["content_id"].nunique()!=6:
        raise RuntimeError("029 RC universe changed")

    claim_set=set(claims["claim_id"])
    fig_set=set(figs["figure_key"])
    rendered_set=set(render["figure_key"])

    primary=cal[cal["slot_type"]=="PRIMARY"].copy()
    if len(primary)!=6 or primary["content_id"].nunique()!=6:
        raise RuntimeError("primary release calendar changed")

    status_rows=[]
    internal_audit={}
    for _,r in rc.iterrows():
        cid=r["content_id"]
        rcid=r["release_candidate_id"]
        checks={}

        checks["rc_unique"]=int((rc["release_candidate_id"]==rcid).sum())==1
        recomputed=recompute_hash(r["immutable_evidence_payload_json"])
        checks["immutable_hash_match"]=recomputed==r["immutable_evidence_sha256"]

        claim_ids=split_pipe(r["claim_ids"])
        fig_keys=split_pipe(r["figure_keys"])
        checks["claims_exist"]=all(x in claim_set for x in claim_ids)
        checks["figures_registered"]=all(x in fig_set for x in fig_keys)
        checks["figures_rendered"]=all(x in rendered_set for x in fig_keys)

        p=primary[primary["content_id"]==cid]
        checks["primary_slot_unique"]=len(p)==1
        if len(p)!=1:
            raise RuntimeError(f"primary slot missing/duplicate: {cid}")
        primary_date=pd.Timestamp(p.iloc[0]["date"])

        sg=shots[shots["content_id"]==cid].sort_values("shot_no")
        checks["seven_shots"]=len(sg)==7
        checks["final_boundary_shot"]=len(sg)>0 and sg.iloc[-1]["role"]=="BOUNDARY"
        checks["no_final_mp4_claim"]=not bool(sg["final_mp4_rendered"].any())

        xg=xhs[xhs["content_id"]==cid].sort_values("card_no")
        checks["xiaohongshu_source_boundary"]=len(xg)>0 and xg.iloc[-1]["role"]=="SOURCE_BOUNDARY"

        checks["mandatory_caveat_present"]=isinstance(r["mandatory_caveat"],str) and bool(r["mandatory_caveat"].strip())
        checks["evidence_payload_unchanged"]=not bool(r["evidence_payload_changed"])
        checks["causal_none"]=r["causal_status"]=="NONE"
        checks["deployment_not_deployable"]=r["deployment_status"]=="NOT_DEPLOYABLE"

        internal_pass=all(checks.values())
        days_to_primary=(primary_date-ASSESSMENT_DATE).days

        if not internal_pass:
            status="HOLD_INTERNAL_QC"
            reason="one or more internal preflight checks failed"
        elif r["freshness_rule"]=="REVERIFY_BEFORE_CURRENT_USE":
            status="HOLD_REVERIFY"
            reason="official current-source re-verification required before scheduled release"
        elif cid==CNT02:
            status="GO_RC1"
            reason="internal QC passes; static historical evidence; first scheduled primary release"
        else:
            status="READY_NOT_DUE"
            reason="internal QC passes; primary release occurs later in the frozen calendar"

        status_rows.append({
            "assessment_date":"2026-09-25",
            "release_candidate_id":rcid,
            "content_id":cid,
            "primary_release_date":str(primary_date.date()),
            "days_to_primary":int(days_to_primary),
            "freshness_rule":r["freshness_rule"],
            "preflight_status":status,
            "reason":reason,
            "internal_checks_pass":internal_pass,
            "immutable_hash_match":checks["immutable_hash_match"],
            "claims_exist":checks["claims_exist"],
            "figures_registered":checks["figures_registered"],
            "figures_rendered":checks["figures_rendered"],
            "seven_shots":checks["seven_shots"],
            "final_boundary_shot":checks["final_boundary_shot"],
            "xiaohongshu_source_boundary":checks["xiaohongshu_source_boundary"],
            "final_mp4_rendered":False,
            "publication_status":"NOT_PUBLISHED",
            "external_reverify_completed":False,
            "evidence_payload_changed":False,
        })
        internal_audit[cid]=checks

    status=pd.DataFrame(status_rows)
    if len(status)!=6:
        raise RuntimeError("expected six preflight rows")
    if status.loc[status["content_id"]==CNT02,"preflight_status"].iloc[0]!="GO_RC1":
        raise RuntimeError("CNT02 should be GO_RC1")
    if status.loc[status["content_id"]==CNT04,"preflight_status"].iloc[0]!="HOLD_REVERIFY":
        raise RuntimeError("CNT04 must remain HOLD_REVERIFY")
    later=status[~status["content_id"].isin([CNT02,CNT04])]
    if not (later["preflight_status"]=="READY_NOT_DUE").all():
        raise RuntimeError("later static packages should be READY_NOT_DUE")
    if not status["internal_checks_pass"].all():
        raise RuntimeError("internal preflight failure")

    status.to_csv(OUT/"RELEASE_PREFLIGHT_STATUS.csv",index=False)

    # Deterministic CNT02 release bundle with preferred 16:9 evidence inserts.
    r2=rc[rc["content_id"]==CNT02].iloc[0]
    s2=shots[shots["content_id"]==CNT02].sort_values("shot_no")
    bundle=[]
    for fk in split_pipe(r2["figure_keys"]):
        z=render[(render["figure_key"]==fk)&(render["variant"]=="PNG_16_9")]
        if len(z)!=1:
            raise RuntimeError(f"missing unique 16:9 render for {fk}")
        rr=z.iloc[0]
        bundle.append({
            "release_candidate_id":r2["release_candidate_id"],
            "content_id":CNT02,
            "primary_release_date":"2026-09-28",
            "primary_title_zh":r2["primary_title_zh"],
            "selected_hook_rc1":r2["selected_hook_rc1"],
            "figure_key":fk,
            "preferred_16x9_path":rr["relative_path"],
            "render_sha256":rr["sha256"],
            "immutable_evidence_sha256":r2["immutable_evidence_sha256"],
            "mandatory_caveat":r2["mandatory_caveat"],
            "shotlist_source":"results/fed_cycle_platform_native_production_pack_028_v1/DOUYIN_TIKTOK_SHOTLISTS_ZH.csv",
            "xiaohongshu_source":"results/fed_cycle_platform_native_production_pack_028_v1/XIAOHONGSHU_CAROUSELS_ZH.csv",
            "wechat_source":"results/fed_cycle_platform_native_production_pack_028_v1/WECHAT_DEEP_ARTICLES_ZH.md",
            "publication_status":"NOT_PUBLISHED",
        })
    bdf=pd.DataFrame(bundle)
    if len(bdf)!=5:
        raise RuntimeError(f"CNT02 expected five case figures, got {len(bdf)}")
    bdf.to_csv(OUT/"RC_CNT02_RELEASE_BUNDLE.csv",index=False)

    lines=[
        "# RC-CNT-02 首发包 — 2026-09-28",
        "",
        f"状态：**GO_RC1 / NOT_PUBLISHED**",
        "",
        f"标题：{r2['primary_title_zh']}",
        "",
        f"RC1 Hook：{r2['selected_hook_rc1']}",
        "",
        "## 7 段短视频分镜",
        "",
    ]
    for x in s2.itertuples(index=False):
        fig=f" | 图：{x.figure_key}" if isinstance(x.figure_key,str) and x.figure_key else ""
        lines.append(f"- {int(x.start_sec):02d}-{int(x.end_sec):02d}s [{x.role}] {x.voiceover_zh}{fig}")
    lines += [
        "",
        "## 推荐证据插图",
        "",
    ]
    for x in bdf.itertuples(index=False):
        lines.append(f"- {x.figure_key}: {x.preferred_16x9_path}")
    lines += [
        "",
        "## 发布边界",
        "",
        r2["mandatory_caveat"],
        "",
        f"Immutable evidence SHA256: {r2['immutable_evidence_sha256']}",
        "",
        "发布前仍需执行人工/平台层最终检查；030只表示证据控制层GO，并不表示已经发布。",
    ]
    (OUT/"RC_CNT02_RELEASE_README_ZH.md").write_text("\n".join(lines)+"\n")

    r4=rc[rc["content_id"]==CNT04].iloc[0]
    hold=f"""# RC-CNT-04 发布 HOLD 说明

Assessment date: 2026-09-25

Status: **HOLD_REVERIFY**

内部证据/QC：PASS。

计划主发布：2026-10-01。

HOLD 原因：该包包含 CLM-CTX-B07_CTX_02，其 freshness rule 为 REVERIFY_BEFORE_CURRENT_USE。该 claim 描述的是 NBER 页面截至审计日的最新官方 business-cycle chronology，因此不能把 2026-09-25 的审计状态永久当作 2026-10-01 的当前状态。

发布前动作：
1. 重新核验 NBER Business Cycle Dating 官方页面；
2. 确认该 current-chronology claim 的表述仍准确；
3. 如状态未变，记录新的 reverify timestamp 后解除 HOLD；
4. 如官方 chronology 已变化，必须更新上游 claim/context 版本，不能只在文案层偷偷修改。

不需要重验/改写的历史事实：
- 2001 NBER recession dating 是 retrospective；
- 9/11 是 post-anchor shock；
- 2007 recession dating 是 retrospective；
- 2020 recession dating 是 retrospective；
- COVID 是 post-anchor shock。

本文件不声称 external reverify 已完成，也不授权提前发布。
"""
    (OUT/"RC_CNT04_HOLD_NOTE.md").write_text(hold)

    audit={
        "module":"FED-CYCLE-RELEASE-PREFLIGHT-030",
        "assessment_date":"2026-09-25",
        "statuses":status.to_dict(orient="records"),
        "internal_checks":internal_audit,
        "cnt02_release_bundle_rows":int(len(bdf)),
        "cnt04_external_reverify_completed":False,
        "current_snapshot_treated_as_live":False,
        "publication_actions_taken":0,
    }
    (OUT/"PREFLIGHT_AUDIT.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# FED-CYCLE-RELEASE-PREFLIGHT-030 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED RELEASE PREFLIGHT / CNT-02 GO_RC1 / CNT-04 HOLD_REVERIFY / NOTHING PUBLISHED**",
        "",
        "- six RCs internally audited: PASS",
        "- CNT-02 (2026-09-28): GO_RC1",
        "- CNT-04 (2026-10-01): HOLD_REVERIFY",
        "- later four RCs: READY_NOT_DUE",
        "- CNT-02 release bundle: five canonical 16:9 case figures + seven-shot plan reference",
        "- CNT-04 external NBER reverify: NOT COMPLETED",
        "- publication actions taken: 0",
        "",
        "GO_RC1 is an editorial evidence-control status only. It is not a market forecast and does not mean the content has been published.",
    ]
    (OUT/"FED_CYCLE_RELEASE_PREFLIGHT_030_REPORT.md").write_text("\n".join(report)+"\n")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-RELEASE-PREFLIGHT-030",
        "upstream_qc":{"029":q029["qc_gate"],"028":q028["qc_gate"],"024":q024["qc_gate"],"022B":q022b["qc_gate"]},
        "assessment_date":"2026-09-25",
        "rc_status_rows":int(len(status)),
        "all_internal_checks_pass":bool(status["internal_checks_pass"].all()),
        "cnt02_status":status.loc[status["content_id"]==CNT02,"preflight_status"].iloc[0],
        "cnt04_status":status.loc[status["content_id"]==CNT04,"preflight_status"].iloc[0],
        "later_ready_not_due_count":int((later["preflight_status"]=="READY_NOT_DUE").sum()),
        "cnt02_immutable_hash_match":bool(status.loc[status["content_id"]==CNT02,"immutable_hash_match"].iloc[0]),
        "cnt02_shot_rows":int(len(s2)),
        "cnt02_final_boundary_shot":bool(s2.iloc[-1]["role"]=="BOUNDARY"),
        "cnt02_bundle_figure_rows":int(len(bdf)),
        "cnt02_publication_status":"NOT_PUBLISHED",
        "cnt04_external_reverify_completed":False,
        "current_snapshot_treated_as_live":False,
        "evidence_payload_changes":0,
        "publication_actions_taken":0,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
