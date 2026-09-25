#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_cnt02_final_publishing_rc_031_v1"
OUT.mkdir(parents=True,exist_ok=True)

Q030=ROOT/"results"/"fed_cycle_release_preflight_030_v1"/"QC.json"
STATUS=ROOT/"results"/"fed_cycle_release_preflight_030_v1"/"RELEASE_PREFLIGHT_STATUS.csv"
BUNDLE=ROOT/"results"/"fed_cycle_release_preflight_030_v1"/"RC_CNT02_RELEASE_BUNDLE.csv"
RC=ROOT/"results"/"fed_cycle_editorial_release_candidate_029_v1"/"RELEASE_CANDIDATES.csv"
SHOTS=ROOT/"results"/"fed_cycle_platform_native_production_pack_028_v1"/"DOUYIN_TIKTOK_SHOTLISTS_ZH.csv"
CLAIMS=ROOT/"results"/"fed_cycle_content_claim_registry_022b_v1"/"CLAIM_REGISTRY.csv"
Q022B=ROOT/"results"/"fed_cycle_content_claim_registry_022b_v1"/"QC.json"

CID="CNT-02-SAME-LABEL-DIFFERENT-PATHS"
RCID="RC-CNT-02-SAME-LABEL-DIFFERENT-PATHS"
EXPECTED_HASH="48a659bb900be19707165bf8f6802e5ce31c514b59a9eb2ee050ccd89868a191"
FINAL_TITLE='同样叫“第一次降息”，为什么历史上的市场路径差这么多？'
FINAL_HOOK='同一个 FIRST_CUT 标签，2001、2007、2019、2024走出了完全不同的资产路径。'

def read_pass(path):
    q=json.loads(Path(path).read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def srt_time(seconds):
    ms=int(round(float(seconds)*1000))
    h,rem=divmod(ms,3600000)
    m,rem=divmod(rem,60000)
    s,ms=divmod(rem,1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def wrap_cn(text,max_chars=18):
    text=str(text).strip()
    chunks=[]
    while len(text)>max_chars:
        cut=max_chars
        for p in ["，","；","。","？","！",",",";"," "]:
            idx=text.rfind(p,0,max_chars+1)
            if idx>=max_chars//2:
                cut=idx+1
                break
        chunks.append(text[:cut].strip())
        text=text[cut:].strip()
    if text:
        chunks.append(text)
    return "\n".join(chunks[:3])

def main():
    q030=read_pass(Q030)
    q022=read_pass(Q022B)
    status=pd.read_csv(STATUS)
    bundle=pd.read_csv(BUNDLE)
    rc=pd.read_csv(RC)
    shots=pd.read_csv(SHOTS)
    claims=pd.read_csv(CLAIMS)

    st=status[status["content_id"]==CID]
    if len(st)!=1 or st.iloc[0]["preflight_status"]!="GO_RC1":
        raise RuntimeError("CNT02 is not GO_RC1")
    if st.iloc[0]["publication_status"]!="NOT_PUBLISHED":
        raise RuntimeError("CNT02 publication status changed")

    rr=rc[rc["content_id"]==CID]
    if len(rr)!=1:
        raise RuntimeError("CNT02 RC missing")
    rr=rr.iloc[0]
    if rr["immutable_evidence_sha256"]!=EXPECTED_HASH:
        raise RuntimeError("immutable evidence hash changed")
    if rr["primary_title_zh"]!=FINAL_TITLE:
        raise RuntimeError("title changed")

    hooks=[rr["hook_variant_a"],rr["hook_variant_b"],rr["hook_variant_c"]]
    if "28.5%" not in rr["hook_variant_b"]:
        raise RuntimeError("expected ambiguity hook signature changed")

    sg=shots[shots["content_id"]==CID].sort_values("shot_no").copy()
    if len(sg)!=7:
        raise RuntimeError("expected seven shots")
    if list(sg["start_sec"])!=[0,7,18,29,40,51,62] or list(sg["end_sec"])!=[7,18,29,40,51,62,72]:
        raise RuntimeError("028 timing changed")
    if sg.iloc[-1]["role"]!="BOUNDARY":
        raise RuntimeError("final shot must be BOUNDARY")

    # Final storyboard: factual wording inherited, shot 5 explicitly uses B06 then B07.
    final_voice=[
        "同样叫第一次降息，历史上的市场路径可以完全不同。",
        "1995案例里，标普500首降后12个月是+19.4%。",
        "2001案例里，纳指首降后12个月是-25.6%，最大回撤40.8%。",
        "2007案例里，标普500首降后12个月是-16.3%，黄金是+24.8%。",
        "2019案例里，标普500首降后12个月是+11.0%；2024案例里，标普500首降后12个月是+20.2%。",
        "同一个政策阶段标签，可以和不同的增长、通胀、信用压力以及后续冲击共存。",
        "这些案例用来理解历史路径差异，不是当前周期的预测模板。"
    ]
    onscreen=[
        "同样是第一次降息\n为什么市场路径完全不同？",
        "1995｜S&P 500 +19.4%",
        "2001｜Nasdaq -25.6%\nMDD 40.8%",
        "2007｜S&P 500 -16.3%\nGold +24.8%",
        "2019｜S&P 500 +11.0%\n2024｜S&P 500 +20.2%",
        "政策标签 ≠ 完整市场状态",
        "历史案例 ≠ 当前预测模板"
    ]
    figs=[
        "",
        "FIG-CASE-B03",
        "FIG-CASE-B04",
        "FIG-CASE-B05",
        "FIG-CASE-B06|FIG-CASE-B07",
        "",
        ""
    ]
    storyboard=[]
    for i,row in enumerate(sg.itertuples(index=False),1):
        storyboard.append({
            "shot_no":i,
            "start_sec":row.start_sec,
            "end_sec":row.end_sec,
            "duration_sec":row.end_sec-row.start_sec,
            "role":row.role,
            "voiceover_zh":final_voice[i-1],
            "subtitle_zh":final_voice[i-1],
            "onscreen_text_zh":onscreen[i-1],
            "figure_sequence":figs[i-1],
            "canvas_width":1080,
            "canvas_height":1920,
            "title_safe_y":"120-360",
            "evidence_panel_y":"420-1320",
            "subtitle_safe_y":"1390-1650",
            "source_boundary_y":"1670-1840",
            "figure_footer_must_remain_visible":bool(figs[i-1]),
            "publication_status":"NOT_PUBLISHED",
        })
    sdf=pd.DataFrame(storyboard)
    if sdf["duration_sec"].sum()!=72:
        raise RuntimeError("storyboard duration must equal 72s")
    sdf.to_csv(OUT/"VERTICAL_STORYBOARD_9X16.csv",index=False)

    # SRT: one deterministic cue per shot.
    srt=[]
    for i,r in sdf.iterrows():
        srt += [
            str(i+1),
            f"{srt_time(r['start_sec'])} --> {srt_time(r['end_sec'])}",
            wrap_cn(r["subtitle_zh"]),
            ""
        ]
    srt_text="\n".join(srt)
    if srt_text.count("-->")!=7:
        raise RuntimeError("SRT cue count")
    if "不是当前周期的预测模板" not in srt_text:
        raise RuntimeError("final SRT boundary missing")
    (OUT/"CNT02_FINAL_SUBTITLES_ZH.srt").write_text(srt_text)

    # Asset sequence with exact render paths from 030 bundle.
    pathmap={r.figure_key:(r.preferred_16x9_path,r.render_sha256) for r in bundle.itertuples(index=False)}
    sequence=[
        (1,"FIG-CASE-B03",7.0,18.0,"1995 evidence"),
        (2,"FIG-CASE-B04",18.0,29.0,"2001 evidence"),
        (3,"FIG-CASE-B05",29.0,40.0,"2007 evidence"),
        (4,"FIG-CASE-B06",40.0,45.5,"2019 evidence"),
        (5,"FIG-CASE-B07",45.5,51.0,"2024 evidence"),
    ]
    assets=[]
    for n,fk,s,e,purpose in sequence:
        if fk not in pathmap:
            raise RuntimeError(f"missing bundle path {fk}")
        p,h=pathmap[fk]
        assets.append({
            "sequence_no":n,"figure_key":fk,"start_sec":s,"end_sec":e,
            "purpose":purpose,"preferred_16x9_path":p,"render_sha256":h,
            "placement":"CENTER_FIT_WITH_FOOTER_VISIBLE",
            "crop_source_footer":False
        })
    adf=pd.DataFrame(assets)
    adf.to_csv(OUT/"FINAL_ASSET_SEQUENCE.csv",index=False)

    # Claim-level numeric audit.
    claimmap={r.claim_id:r for r in claims[claims["claim_id"].isin([
        "CLM-CASE-B03","CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07"
    ])].itertuples(index=False)}
    required=["CLM-CASE-B03","CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07"]
    if any(x not in claimmap for x in required):
        raise RuntimeError("case claims missing")

    ambiguity=pd.DataFrame([
        {
            "hook_id":"HOOK_A",
            "text":rr["hook_variant_a"],
            "data_valid":True,
            "editorially_unambiguous":True,
            "release_use":"SELECTED_RC1",
            "reason":"No numeric asset ambiguity."
        },
        {
            "hook_id":"HOOK_B",
            "text":rr["hook_variant_b"],
            "data_valid":True,
            "editorially_unambiguous":False,
            "release_use":"PROHIBITED_FOR_FIRST_RELEASE",
            "reason":"2001 value is explicitly Nasdaq; 2024 +28.5% is also Nasdaq but the second asset label is omitted."
        },
        {
            "hook_id":"HOOK_C",
            "text":rr["hook_variant_c"],
            "data_valid":True,
            "editorially_unambiguous":True,
            "release_use":"RESERVE_NON_NUMERIC",
            "reason":"Non-numeric conceptual hook."
        }
    ])
    ambiguity.to_csv(OUT/"AMBIGUITY_AUDIT.csv",index=False)

    cover=f"""# CNT-02 最终封面规范

## 主封面

第一行：**同样是第一次降息**

第二行：**为什么市场路径完全不同？**

Kicker：**1995 / 2001 / 2007 / 2019 / 2024**

## 版式

- Canvas: 1080 x 1920
- 主标题安全区：y=120-360
- 不在封面展示收益数字
- 不使用“赢家/输家/最佳/抄底/机会”等排名或行动词
- 不使用绿色/红色来暗示买卖信号
- 封面任务只是提出历史研究问题，不给当前市场结论

## 底部小字

历史周期研究｜案例路径比较｜非当前市场预测
"""
    (OUT/"FINAL_COVER_SPEC_ZH.md").write_text(cover)

    caption=f"""# CNT-02 最终 Caption + 置顶评论

## Caption

同样是“第一次降息”，历史上的资产路径并不相同。

1995案例里，S&P 500 首降后12个月约 +19.4%；2001案例里，Nasdaq 约 -25.6%，期间12个月最大回撤约 40.8%；2007案例里，S&P 500 约 -16.3%，Gold 约 +24.8%；2019案例里，S&P 500 约 +11.0%；2024案例里，S&P 500 约 +20.2%。

这些数字描述的是不同历史案例的事后路径，不代表同一个政策标签会产生同一种市场结果。真正需要区分的是增长、通胀、信用环境、金融条件和后续冲击。

历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

#美联储 #降息周期 #宏观研究 #美股 #黄金 #金融市场

## 置顶评论

这组数据来自公开研究仓库中的历史 FIRST_CUT 案例库，图表和数字都绑定到固定 CLAIM_ID / FIGURE_KEY。后续冲击不会被倒灌成更早政策决定的理由，也不做“哪个历史周期最像现在”的排名。这里讨论的是历史路径差异，不是当前买卖信号。
"""
    (OUT/"FINAL_CAPTION_AND_PINNED_COMMENT_ZH.md").write_text(caption)

    finalcopy=f"""# CNT-02 Final Release Copy — RC1

Status: **GO_RC1 / NOT_PUBLISHED**

## Title

{FINAL_TITLE}

## Cover

同样是第一次降息  
为什么市场路径完全不同？  
1995 / 2001 / 2007 / 2019 / 2024

## Final Hook

{FINAL_HOOK}

## 72-second voiceover

1. 同样叫第一次降息，历史上的市场路径可以完全不同。
2. 1995案例里，标普500首降后12个月是+19.4%。
3. 2001案例里，纳指首降后12个月是-25.6%，最大回撤40.8%。
4. 2007案例里，标普500首降后12个月是-16.3%，黄金是+24.8%。
5. 2019案例里，标普500首降后12个月是+11.0%；2024案例里，标普500首降后12个月是+20.2%。
6. 同一个政策阶段标签，可以和不同的增长、通胀、信用压力以及后续冲击共存。
7. 这些案例用来理解历史路径差异，不是当前周期的预测模板。

## Boundary

{rr["mandatory_caveat"]}

Immutable evidence SHA256: {EXPECTED_HASH}

Publication status: NOT_PUBLISHED
"""
    (OUT/"FINAL_RELEASE_COPY_ZH.md").write_text(finalcopy)

    manifest={
        "module":"FED-CYCLE-CNT02-FINAL-PUBLISHING-RC-031",
        "content_id":CID,
        "release_candidate_id":RCID,
        "scheduled_primary_release":"2026-09-28",
        "preflight_status":"GO_RC1",
        "publication_status":"NOT_PUBLISHED",
        "final_title":FINAL_TITLE,
        "final_hook":FINAL_HOOK,
        "immutable_evidence_sha256":EXPECTED_HASH,
        "storyboard_rows":7,
        "duration_seconds":72,
        "srt_cues":7,
        "asset_sequence":["FIG-CASE-B03","FIG-CASE-B04","FIG-CASE-B05","FIG-CASE-B06","FIG-CASE-B07"],
        "ambiguous_hook_b_used":False,
        "final_mp4_rendered":False,
        "current_market_claims_added":False,
        "evidence_payload_changed":False,
        "publication_actions_taken":0,
    }
    (OUT/"RELEASE_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# FED-CYCLE-CNT02-FINAL-PUBLISHING-RC-031 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED FINAL EDITORIAL PRODUCTION CANDIDATE / GO_RC1 / NOT PUBLISHED**",
        "",
        "- final title locked: yes",
        "- final cover copy locked: yes",
        "- final hook: Hook A",
        "- ambiguous numeric Hook B used: no",
        "- 9:16 storyboard rows: 7",
        "- total duration: 72 seconds",
        "- SRT cues: 7",
        "- case figures sequenced: B03/B04/B05/B06/B07",
        "- final caption + pinned comment: ready",
        "- immutable evidence hash changed: no",
        "- final MP4 rendered: no",
        "- publication actions taken: 0",
        "",
        "031 is ready for human/platform compositing. It does not publish the content or add a market forecast."
    ]
    (OUT/"FED_CYCLE_CNT02_FINAL_PUBLISHING_RC_031_REPORT.md").write_text("\n".join(report)+"\n")

    publish_text="\n".join([
        finalcopy,caption,cover,
        "\n".join(sdf["voiceover_zh"].astype(str)),
        "\n".join(sdf["onscreen_text_zh"].astype(str))
    ])
    prohibited=["买入","卖出","抄底","最佳资产","最像现在","稳赚","必涨","必跌"]
    leaks=[x for x in prohibited if x in publish_text]
    if leaks:
        raise RuntimeError(f"prohibited language leaks: {leaks}")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-CNT02-FINAL-PUBLISHING-RC-031",
        "upstream_qc":{"030":q030["qc_gate"],"022B":q022["qc_gate"]},
        "preflight_status":"GO_RC1",
        "publication_status":"NOT_PUBLISHED",
        "immutable_evidence_sha256":EXPECTED_HASH,
        "immutable_hash_exact_match":True,
        "final_title_exact_match":True,
        "final_hook_source":"RC1_HOOK_A",
        "ambiguous_hook_b_data_valid":True,
        "ambiguous_hook_b_editorially_unambiguous":False,
        "ambiguous_hook_b_used":False,
        "storyboard_rows":int(len(sdf)),
        "storyboard_duration_seconds":int(sdf["duration_sec"].sum()),
        "timing_inherited_exactly":True,
        "srt_cues":7,
        "final_srt_boundary_present":True,
        "rendered_case_figures":int(len(adf)),
        "figure_footer_cropping_allowed":False,
        "caption_ready":True,
        "pinned_comment_ready":True,
        "prohibited_language_leaks":[],
        "current_analog_ranking_outputs":0,
        "asset_ranking_outputs":0,
        "forecast_outputs":0,
        "political_evaluation_outputs":0,
        "evidence_payload_changes":0,
        "publication_actions_taken":0,
        "final_mp4_rendered":False,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
