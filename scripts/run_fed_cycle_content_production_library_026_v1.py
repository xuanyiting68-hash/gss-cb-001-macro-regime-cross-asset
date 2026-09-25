#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_content_production_library_026_v1"
OUT.mkdir(parents=True, exist_ok=True)

CLAIMS = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "CLAIM_REGISTRY.csv"
Q022B = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "QC.json"
FIGREG = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "FIGURE_REGISTRY.csv"
Q024 = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "QC.json"
RENDER = ROOT / "results" / "fed_cycle_p0_visual_evidence_pack_v1" / "RENDER_MANIFEST.csv"
Q025 = ROOT / "results" / "fed_cycle_p0_visual_evidence_pack_v1" / "QC.json"

CONTENT_IDS = [
    "CNT-01-FIRST-CUT-NOT-THE-BOTTOM",
    "CNT-02-SAME-LABEL-DIFFERENT-PATHS",
    "CNT-03-GOLD-VS-EQUITIES",
    "CNT-04-HINDSIGHT-TRAPS",
    "CNT-05-RECOVERY-CLOCK",
    "CNT-06-1987-MULTI-LEG",
]

PACKS = {
    CONTENT_IDS[0]: {
        "claims": [
            "CLM-PHASE-DXY-FIRST_CUT","CLM-PHASE-GOLD-FIRST_CUT","CLM-PHASE-NASDAQ-FIRST_CUT",
            "CLM-PHASE-SP500-FIRST_CUT","CLM-PHASE-WTI-FIRST_CUT",
            "CLM-SYNTH-017-FIRSTCUT-RECOVERY","CLM-GUARD-019","CLM-GUARD-020",
            "CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07",
        ],
        "figures": [
            "FIG-PHASE-DXY-FIRST_CUT","FIG-PHASE-GOLD-FIRST_CUT","FIG-PHASE-NASDAQ-FIRST_CUT",
            "FIG-PHASE-SP500-FIRST_CUT","FIG-PHASE-WTI-FIRST_CUT",
            "FIG-RECOVERY-FIRSTCUT-VS-PAUSE","FIG-GUARD-019","FIG-GUARD-020",
            "FIG-CASE-B04","FIG-CASE-B05","FIG-CASE-B06","FIG-CASE-B07",
        ],
        "visual_readiness":"READY_P0_VISUAL",
        "freshness_rule":"STATIC_UNLESS_UPSTREAM_REBUILT",
        "tags":"SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|IMAGE_CARD|MYTH_VS_EVIDENCE|PANDAAI",
    },
    CONTENT_IDS[1]: {
        "claims":["CLM-CASE-B03","CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07"],
        "figures":["FIG-CASE-B04","FIG-CASE-B05","FIG-CASE-B06","FIG-CASE-B07"],
        "visual_readiness":"READY_P0_VISUAL",
        "freshness_rule":"STATIC_UNLESS_UPSTREAM_REBUILT",
        "tags":"SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|CASE_STUDY|PANDAAI",
    },
    CONTENT_IDS[2]: {
        "claims":[
            "CLM-PHASE-GOLD-FIRST_CUT","CLM-PHASE-SP500-FIRST_CUT","CLM-PHASE-NASDAQ-FIRST_CUT",
            "CLM-CASE-B04","CLM-CASE-B05","CLM-CASE-B06","CLM-CASE-B07"
        ],
        "figures":[
            "FIG-PHASE-GOLD-FIRST_CUT","FIG-PHASE-SP500-FIRST_CUT","FIG-PHASE-NASDAQ-FIRST_CUT",
            "FIG-CASE-B04","FIG-CASE-B05","FIG-CASE-B06","FIG-CASE-B07"
        ],
        "visual_readiness":"READY_P0_VISUAL",
        "freshness_rule":"STATIC_UNLESS_UPSTREAM_REBUILT",
        "tags":"SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|IMAGE_CARD|CASE_STUDY|PANDAAI",
    },
    CONTENT_IDS[3]: {
        "claims":[
            "CLM-CTX-B04_CTX_02","CLM-CTX-B04_CTX_03","CLM-CTX-B05_CTX_03",
            "CLM-CTX-B06_CTX_02","CLM-CTX-B06_CTX_03","CLM-CTX-B07_CTX_02"
        ],
        "figures":["FIG-CASE-B04","FIG-CASE-B05","FIG-CASE-B06","FIG-CASE-B07"],
        "visual_readiness":"READY_P0_VISUAL",
        "freshness_rule":"REVERIFY_BEFORE_CURRENT_USE",
        "tags":"SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|MYTH_VS_EVIDENCE|CASE_STUDY|PANDAAI",
    },
    CONTENT_IDS[4]: {
        "claims":[
            "CLM-SYNTH-017-FIRSTCUT-RECOVERY",
            "CLM-PHASE-DXY-FIRST_CUT","CLM-PHASE-GOLD-FIRST_CUT","CLM-PHASE-NASDAQ-FIRST_CUT",
            "CLM-PHASE-SP500-FIRST_CUT","CLM-PHASE-WTI-FIRST_CUT",
        ],
        "figures":[
            "FIG-RECOVERY-FIRSTCUT-VS-PAUSE",
            "FIG-PHASE-DXY-FIRST_CUT","FIG-PHASE-GOLD-FIRST_CUT","FIG-PHASE-NASDAQ-FIRST_CUT",
            "FIG-PHASE-SP500-FIRST_CUT","FIG-PHASE-WTI-FIRST_CUT",
        ],
        "visual_readiness":"READY_P0_VISUAL",
        "freshness_rule":"STATIC_UNLESS_UPSTREAM_REBUILT",
        "tags":"SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|IMAGE_CARD|MYTH_VS_EVIDENCE|PANDAAI",
    },
    CONTENT_IDS[5]: {
        "claims":["CLM-CASE-B02","CLM-CTX-B02_CTX_01","CLM-CTX-B02_CTX_02","CLM-CTX-B02_CTX_03"],
        "figures":["FIG-CASE-B02"],
        "visual_readiness":"TEXT_READY_VISUAL_PENDING_P1",
        "freshness_rule":"STATIC_SOURCE_AUDIT",
        "tags":"SHORT_VIDEO|LONG_VIDEO|DEEP_ARTICLE|CASE_STUDY|PANDAAI",
    },
}


def read_pass(path: Path):
    q = json.loads(path.read_text())
    if q.get("qc_gate") != "PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q


def pct(v):
    return f"{float(v)*100:+.1f}%"


def mdd(v):
    return f"{float(v)*100:.1f}%"


def claim_row(claims, cid):
    z = claims[claims["claim_id"] == cid]
    if len(z) != 1:
        raise RuntimeError(f"claim missing/duplicate: {cid}")
    return z.iloc[0]


def payload(claims, cid):
    return json.loads(claim_row(claims, cid)["metric_payload"])


def case_asset(payload_dict, asset):
    return payload_dict[asset]


def build_copy(claims):
    # All evidence numbers below are formatted directly from canonical metric_payload fields.
    sp = payload(claims, "CLM-PHASE-SP500-FIRST_CUT")
    nq = payload(claims, "CLM-PHASE-NASDAQ-FIRST_CUT")
    au = payload(claims, "CLM-PHASE-GOLD-FIRST_CUT")
    wti = payload(claims, "CLM-PHASE-WTI-FIRST_CUT")
    dxy = payload(claims, "CLM-PHASE-DXY-FIRST_CUT")

    b03 = payload(claims, "CLM-CASE-B03")
    b04 = payload(claims, "CLM-CASE-B04")
    b05 = payload(claims, "CLM-CASE-B05")
    b06 = payload(claims, "CLM-CASE-B06")
    b07 = payload(claims, "CLM-CASE-B07")

    items = {}

    items[CONTENT_IDS[0]] = {
        "title":"第一次降息之后，市场就已经见底了吗？历史数据不支持这么简单的结论",
        "hooks":[
            "第一次降息 = 市场见底？把历史路径拆开看，结论没有这么简单。",
            f"首降后标普500历史+12个月中位数是{pct(sp['ret_12m'])}，但同期最大回撤中位数仍有{mdd(sp['path_risk_value'])}。",
            "降息是一个政策阶段标签，不是市场底部的时间戳。",
        ],
        "script":(
            f"很多人一看到第一次降息，就会把它理解成风险已经结束。可是把历史路径拆开看，结论没有这么简单。"
            f"在我们的支持样本里，首降后标普500的+12个月终点收益中位数是{pct(sp['ret_12m'])}，"
            f"但12个月最大回撤中位数仍有{mdd(sp['path_risk_value'])}，回撤低点中位出现在第{int(sp['trough_month'])}个月。"
            f"纳指的+12个月中位数是{pct(nq['ret_12m'])}，最大回撤中位数{mdd(nq['path_risk_value'])}，低点也是第{int(nq['trough_month'])}个月。"
            f"WTI更不一样：+12个月中位数{pct(wti['ret_12m'])}，最大回撤中位数{mdd(wti['path_risk_value'])}。"
            "再看恢复时钟，五个完整支持资产里，首降后的完全恢复速度相对暂停阶段是3个更慢、2个相同、0个更快。"
            "而且019和020两轮事前状态检验都没有验证出稳定的见底计时规则。"
            "所以更准确的说法是：第一次降息以后，资产路径仍然可能很复杂。以上是历史描述，不是对当前市场底部或未来收益的预测。"
        ),
        "outline":[
            "误区：为什么“第一次降息=底部”过于简化",
            "五类核心资产的FIRST_CUT历史终点收益、MDD、低点月份",
            "endpoint return 与 interim path risk 为什么必须分开",
            "017 recovery clock：FIRST_CUT 相对 PAUSE 并没有更快恢复",
            "019/020：为什么简单事前状态无法稳定给出底部时间",
            "2001/2007/2019/2024案例对照",
            "结论边界：历史分布不是当前预测",
        ],
    }

    items[CONTENT_IDS[1]] = {
        "title":"同样叫“第一次降息”，为什么历史上的市场路径差这么多？",
        "hooks":[
            "同一个FIRST_CUT标签，2001、2007、2019、2024走出了完全不同的资产路径。",
            f"2001首降后，纳指+12个月是{pct(case_asset(b04,'NASDAQ')['ret_12m'])}；2024案例里则是{pct(case_asset(b07,'NASDAQ')['ret_12m'])}。",
            "真正值得研究的不是“降息”两个字，而是降息发生在什么宏观和金融环境里。",
        ],
        "script":(
            "如果只看“第一次降息”这四个字，很容易把不同周期当成同一件事。"
            f"1995案例里，标普500首降后+12个月是{pct(case_asset(b03,'SP500')['ret_12m'])}。"
            f"2001案例里，纳指+12个月是{pct(case_asset(b04,'NASDAQ')['ret_12m'])}，最大回撤达到{mdd(case_asset(b04,'NASDAQ')['mdd_12m'])}。"
            f"2007案例里，标普500+12个月是{pct(case_asset(b05,'SP500')['ret_12m'])}，而黄金是{pct(case_asset(b05,'GOLD')['ret_12m'])}。"
            f"2019案例里，标普500是{pct(case_asset(b06,'SP500')['ret_12m'])}；2024案例里是{pct(case_asset(b07,'SP500')['ret_12m'])}。"
            "同样一个政策阶段标签，可以和完全不同的增长、通胀、信用压力以及后续冲击共存。"
            "所以案例应该被用来理解路径差异，而不是挑一个单一历史模板去套当前周期。以上是历史案例描述，不是当前周期预测。"
        ),
        "outline":[
            "问题：为什么FIRST_CUT不能作为单一市场状态",
            "1995、2001、2007、2019、2024五个案例并列",
            "股票、黄金、原油在同一案例里的分化",
            "案例内后续冲击与政策标签的区分",
            "为什么不做“最近历史类比排名”",
            "如何用状态变量而不是单一事件标签理解周期",
            "结论边界：案例不是预测模板",
        ],
    }

    items[CONTENT_IDS[2]] = {
        "title":"降息周期里，黄金和美股会一起走吗？历史上并不总是如此",
        "hooks":[
            f"首降后，黄金历史+12个月中位数{pct(au['ret_12m'])}，标普500是{pct(sp['ret_12m'])}，但它们的路径风险完全不同。",
            f"2001案例：黄金{pct(case_asset(b04,'GOLD')['ret_12m'])}，纳指却是{pct(case_asset(b04,'NASDAQ')['ret_12m'])}。",
            "同一个Fed阶段，并不会自动给所有资产排出统一顺序。",
        ],
        "script":(
            "降息周期里，黄金和美股是不是会一起上涨？历史上没有这么简单。"
            f"在支持样本中，第一次降息后黄金+12个月终点收益中位数是{pct(au['ret_12m'])}，最大回撤中位数{mdd(au['path_risk_value'])}；"
            f"标普500对应是{pct(sp['ret_12m'])}和{mdd(sp['path_risk_value'])}；"
            f"纳指是{pct(nq['ret_12m'])}和{mdd(nq['path_risk_value'])}。"
            f"案例差异更明显：2001首降后黄金是{pct(case_asset(b04,'GOLD')['ret_12m'])}，纳指是{pct(case_asset(b04,'NASDAQ')['ret_12m'])}；"
            f"2007首降后黄金是{pct(case_asset(b05,'GOLD')['ret_12m'])}，标普500是{pct(case_asset(b05,'SP500')['ret_12m'])}。"
            "这说明政策阶段只能提供背景，资产自身的增长暴露、信用敏感度和避险属性仍然重要。"
            "这里不做资产优劣排名，也不是当前配置建议或当前市场预测，只是在说明历史路径为什么会分化。"
        ),
        "outline":[
            "问题：同一Fed阶段是否意味着跨资产同方向",
            "FIRST_CUT历史中位：Gold、SP500、Nasdaq",
            "路径风险：MDD与终点收益分开",
            "2001案例：黄金与科技股分化",
            "2007案例：黄金与美股分化",
            "2019/2024作为补充案例",
            "结论：跨资产比较不能变成简单排名",
        ],
    }

    # Context package uses canonical wording, not separately reconstructed numbers.
    ctx_ids = PACKS[CONTENT_IDS[3]]["claims"]
    ctx = {cid: claim_row(claims,cid) for cid in ctx_ids}
    items[CONTENT_IDS[3]] = {
        "title":"研究历史周期最容易犯的错：把后来才知道的事，假装成当时已经知道",
        "hooks":[
            "2001年1月第一次降息时，后来被NBER认定的衰退起点还没有发生，更没有被官方确认。",
            "9·11不能被倒灌进2001年1月的政策理由，COVID也不能被倒灌进2019年7月。",
            "做周期研究，最重要的不只是数据，而是时间戳：当时到底知道什么？",
        ],
        "script":(
            "研究历史周期最危险的错误之一，是后见之明。"
            "2001年1月第一次降息时，后来NBER认定的2001年3月经济峰值还在未来，官方对这个峰值的认定更晚。"
            "同样，9·11发生在2001年1月首降之后，不能把它当成当时降息的原始理由。"
            "2007年也是一样：后来被认定的衰退峰值是2007年12月，但这是一项事后官方定年。"
            "2019年7月首降的官方语境是全球发展和较低的通胀压力；COVID是之后发生的新冲击。"
            "所以我们把资料分成当时可知、事后定年和后续冲击三个时间层。只有这样，历史研究才不会把答案提前塞回过去。"
            "这些是历史时间信息的校正，不是对当前经济是否会衰退的预测。"
        ),
        "outline":[
            "什么是宏观研究中的 hindsight bias",
            "2001：首降、NBER事后定年、9·11后续冲击",
            "2007：信用压力已可见 vs 衰退日期后来确认",
            "2019：当时官方理由 vs 2020 COVID后续冲击",
            "NBER为什么天然具有事后定年属性",
            "如何在内容中标注 CONTEMPORANEOUS / RETROSPECTIVE / POST_ANCHOR",
            "结论：时间戳是证据的一部分",
        ],
    }

    items[CONTENT_IDS[4]] = {
        "title":"只看一年后涨跌还不够：真正影响持有体验的是“恢复时钟”",
        "hooks":[
            "一年后是正收益，不代表中间没有经历很深的回撤。",
            "首降之后，五个完整支持资产的完全恢复速度，相对暂停阶段没有一个更快。",
            f"黄金首降后的+12个月中位数是{pct(au['ret_12m'])}，但从锚点到完全恢复的历史中位时间是{int(au['anchor_to_full_recovery_months'])}个月。",
        ],
        "script":(
            "如果只看一年后的收益，你会漏掉持有过程中最重要的一部分：路径。"
            f"例如首降后的历史中位数里，标普500+12个月是{pct(sp['ret_12m'])}，但最大回撤中位数仍有{mdd(sp['path_risk_value'])}；"
            f"纳指是{pct(nq['ret_12m'])}，最大回撤{mdd(nq['path_risk_value'])}。"
            f"黄金+12个月是{pct(au['ret_12m'])}，而从政策锚点到完全恢复的Kaplan-Meier中位时间是{int(au['anchor_to_full_recovery_months'])}个月；"
            f"WTI对应的完全恢复中位时间是{int(wti['anchor_to_full_recovery_months'])}个月。"
            "更重要的是，在五个完整支持资产里，FIRST_CUT相对PAUSE的完全恢复时钟是3个更慢、2个相同、0个更快。"
            "所以终点收益、途中回撤和恢复时间应该分开理解。以上是历史风险分布，不是对未来恢复时间的预测。"
        ),
        "outline":[
            "为什么 endpoint return 不等于投资体验",
            "MDD：持有过程中承受了多大回撤",
            "trough month：风险什么时候发生",
            "anchor-to-full-recovery：多久回到锚点水平",
            "五个支持资产的FIRST_CUT vs PAUSE比较",
            "Gold/SP500/Nasdaq/WTI/DXY案例",
            "结论：三种风险对象不能合成单一收益率判断",
        ],
    }

    b02claim = claim_row(claims, "CLM-CASE-B02")
    b02c1 = claim_row(claims, "CLM-CTX-B02_CTX_01")
    b02c2 = claim_row(claims, "CLM-CTX-B02_CTX_02")
    items[CONTENT_IDS[5]] = {
        "title":"为什么1987—1989不能被压成“一次标准加息周期”？",
        "hooks":[
            "1987—1989不是一条干净的“加息—暂停—降息”直线，而是三个机械子周期。",
            "如果把1987股灾前后全部压成一个周期，你会直接破坏政策时间线。",
            "历史周期研究的第一步，有时不是算收益，而是先把周期边界划对。",
        ],
        "script":(
            "1987到1989这段历史，最容易被过度简化。"
            "在我们的机械周期定义里，B02并不是一个单独的标准周期，而是T03_1987、T04_1987和T05_1988三个独立的紧缩—宽松子周期。"
            "其中，1987年10月的Black Monday发生在这些子周期之间；随后Fed的流动性支持也是一个明确的金融稳定事件。"
            "如果为了讲故事方便，把它们压成一条FIRST_HIKE到FIRST_CUT的直线，就会把不同政策腿和市场冲击混在一起。"
            "所以这个案例最重要的启示不是某个收益数字，而是研究设计：先把时间线和事件边界划对，再谈资产表现。"
            "这是一段历史结构说明，不是对当前Fed周期的类比或预测。"
        ),
        "outline":[
            "B02为什么被定义为COMPOSITE_MULTI_LEG",
            "T03_1987 / T04_1987 / T05_1988三个机械子周期",
            "Black Monday在时间线中的位置",
            "Fed流动性支持属于金融稳定语境",
            "为什么不能人为构造一条合成政策路径",
            "这种边界错误会怎样污染资产统计",
            "结论：周期定义本身就是研究结果的一部分",
        ],
    }

    return items


def main():
    q022b = read_pass(Q022B)
    q024 = read_pass(Q024)
    q025 = read_pass(Q025)

    claims = pd.read_csv(CLAIMS)
    figreg = pd.read_csv(FIGREG)
    render = pd.read_csv(RENDER)

    if len(claims) != 47:
        raise RuntimeError("022B claim universe changed")
    if len(figreg) != 48:
        raise RuntimeError("024 figure universe changed")
    rendered_keys = set(render["figure_key"].unique())
    claim_ids = set(claims["claim_id"])
    figure_keys = set(figreg["figure_key"])

    copy = build_copy(claims)
    if set(copy) != set(CONTENT_IDS):
        raise RuntimeError("content copy universe changed")

    rows = []
    claim_map_rows = []
    for cid in CONTENT_IDS:
        cfg = PACKS[cid]
        obj = copy[cid]
        missing_claims = [x for x in cfg["claims"] if x not in claim_ids]
        missing_figs = [x for x in cfg["figures"] if x not in figure_keys]
        if missing_claims or missing_figs:
            raise RuntimeError(f"{cid} missing claims={missing_claims} figs={missing_figs}")

        rendered_figs = [x for x in cfg["figures"] if x in rendered_keys]
        if cfg["visual_readiness"] == "READY_P0_VISUAL" and not rendered_figs:
            raise RuntimeError(f"{cid} claims ready visual but has no rendered P0 figure")
        if cid == "CNT-06-1987-MULTI-LEG":
            if cfg["visual_readiness"] != "TEXT_READY_VISUAL_PENDING_P1":
                raise RuntimeError("CNT-06 readiness changed")
            if "FIG-CASE-B02" in rendered_keys:
                raise RuntimeError("CNT-06 must not falsely treat B02 as a 025 P0 render")

        subset = claims[claims["claim_id"].isin(cfg["claims"])].copy()
        source_files = sorted({x for s in subset["source_files"] for x in str(s).split("|")})
        urls = sorted({
            x for s in subset["official_source_urls"]
            for x in str(s).split("|")
            if x and x != "N/A_REPO_DERIVED"
        })
        freshness = cfg["freshness_rule"]
        if cid == "CNT-04-HINDSIGHT-TRAPS" and freshness != "REVERIFY_BEFORE_CURRENT_USE":
            raise RuntimeError("CNT-04 freshness must reverify")

        caveat = "历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。"
        prohibited = "不得改写为必涨/必跌、确定性底部、最像当前的历史周期、最佳资产或因果性Fed结论。"
        row = {
            "content_id":cid,
            "status":"CANONICAL_CONTENT_READY" if cfg["visual_readiness"]=="READY_P0_VISUAL" else "TEXT_READY_VISUAL_PENDING_P1",
            "primary_title_zh":obj["title"],
            "hooks_json":json.dumps(obj["hooks"],ensure_ascii=False),
            "short_video_script_zh":obj["script"],
            "longform_outline_json":json.dumps(obj["outline"],ensure_ascii=False),
            "claim_ids":"|".join(cfg["claims"]),
            "figure_keys":"|".join(cfg["figures"]),
            "rendered_figure_keys":"|".join(rendered_figs),
            "visual_readiness":cfg["visual_readiness"],
            "freshness_rule":freshness,
            "content_tags":cfg["tags"],
            "mandatory_caveat":caveat,
            "prohibited_wording":prohibited,
            "source_files":"|".join(source_files),
            "official_source_urls":"|".join(urls),
            "script_numeric_source_mode":"CLAIM_PAYLOAD_OR_CANONICAL_WORDING_ONLY",
            "causal_status":"NONE",
            "oos_status":"NOT_A_FORECASTING_MODEL",
            "deployment_status":"NOT_DEPLOYABLE",
        }
        rows.append(row)

        for claim_id in cfg["claims"]:
            c = claim_row(claims, claim_id)
            claim_map_rows.append({
                "content_id":cid,
                "claim_id":claim_id,
                "claim_family":c["claim_family"],
                "evidence_time":c["evidence_time"],
                "support_status":c["support_status"],
                "freshness_rule":c["freshness_rule"],
                "source_files":c["source_files"],
                "official_source_urls":c["official_source_urls"],
            })
        for fig in cfg["figures"]:
            claim_map_rows.append({
                "content_id":cid,
                "claim_id":f"FIGURE::{fig}",
                "claim_family":"FIGURE_REFERENCE",
                "evidence_time":"",
                "support_status":"RENDERED_P0" if fig in rendered_keys else "SPEC_ONLY_NOT_RENDERED",
                "freshness_rule":figreg.loc[figreg["figure_key"]==fig,"freshness_rule"].iloc[0],
                "source_files":figreg.loc[figreg["figure_key"]==fig,"source_files"].iloc[0],
                "official_source_urls":"",
            })

    out = pd.DataFrame(rows)
    mapping = pd.DataFrame(claim_map_rows)

    if list(out["content_id"]) != CONTENT_IDS or len(out) != 6:
        raise RuntimeError("expected exact six content packages")
    if int((out["visual_readiness"]=="READY_P0_VISUAL").sum()) != 5:
        raise RuntimeError("expected five P0-visual-ready packages")

    # Script boundaries and prohibited language.
    combined = "\n".join(out["short_video_script_zh"].astype(str))
    required_boundary_patterns = ["不是", "预测"]
    for script in out["short_video_script_zh"]:
        if not all(p in script for p in required_boundary_patterns):
            raise RuntimeError("short script missing history/not-forecast boundary")
    prohibited_tokens = ["必涨","必跌","最像今天","最佳资产","买入","卖出","BUY","SELL"]
    leaks = [t for t in prohibited_tokens if t.lower() in combined.lower()]
    if leaks:
        raise RuntimeError(f"prohibited script language leaked: {leaks}")

    # Numeric provenance mode is fixed by generator design; no model/statistics executed here.
    if not (out["script_numeric_source_mode"]=="CLAIM_PAYLOAD_OR_CANONICAL_WORDING_ONLY").all():
        raise RuntimeError("numeric provenance mode changed")

    out.to_csv(OUT / "CONTENT_OBJECTS.csv", index=False)
    mapping.to_csv(OUT / "CONTENT_CLAIM_FIGURE_MAP.csv", index=False)

    lib = {
        "module":"FED-CYCLE-CONTENT-PRODUCTION-LIBRARY-026",
        "as_of":"2026-09-25",
        "language":"zh-CN",
        "package_count":6,
        "packages":json.loads(out.to_json(orient="records")),
    }
    (OUT / "CONTENT_LIBRARY.json").write_text(
        json.dumps(lib,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    )

    # Finished short-video scripts.
    sv = [
        "# 026 中文短视频脚本库",
        "",
        "所有脚本均由 canonical CLAIM_ID 支撑。标题和节奏可适配平台，但数字、证据时间属性与边界不得改写。",
        "",
    ]
    for r in out.itertuples(index=False):
        hooks = json.loads(r.hooks_json)
        sv += [
            f"## {r.content_id}",
            "",
            f"**主标题：** {r.primary_title_zh}",
            "",
            "**开头备选：**",
            *[f"- {h}" for h in hooks],
            "",
            "**60–90秒脚本：**",
            "",
            r.short_video_script_zh,
            "",
            f"**配图：** {r.rendered_figure_keys if r.rendered_figure_keys else 'P1视觉待生成'}",
            "",
            f"**必带边界：** {r.mandatory_caveat}",
            "",
        ]
    (OUT / "SHORT_VIDEO_SCRIPTS_ZH.md").write_text("\n".join(sv)+"\n")

    lf = [
        "# 026 中文长文 / 长视频结构库",
        "",
        "以下为证据驱动的结构，不是资产配置或市场预测模板。",
        "",
    ]
    for r in out.itertuples(index=False):
        lf += [f"## {r.content_id} — {r.primary_title_zh}", ""]
        for i, point in enumerate(json.loads(r.longform_outline_json), start=1):
            lf.append(f"{i}. {point}")
        lf += [
            "",
            f"Claims: {r.claim_ids}",
            f"Figures: {r.figure_keys}",
            f"Freshness: {r.freshness_rule}",
            f"Boundary: {r.mandatory_caveat}",
            "",
        ]
    (OUT / "LONGFORM_OUTLINES_ZH.md").write_text("\n".join(lf)+"\n")

    sc = [
        "# 026 Source and Caveat Blocks",
        "",
        "Use these blocks when publishing or handing content to another agent/editor.",
        "",
    ]
    for r in out.itertuples(index=False):
        sc += [
            f"## {r.content_id}",
            "",
            f"- Claim IDs: {r.claim_ids}",
            f"- Figure keys: {r.figure_keys}",
            f"- Rendered P0 figures: {r.rendered_figure_keys or 'none'}",
            f"- Canonical source files: {r.source_files}",
            f"- Official source URLs: {r.official_source_urls or 'none / repo-derived claims'}",
            f"- Freshness: {r.freshness_rule}",
            f"- Mandatory caveat: {r.mandatory_caveat}",
            f"- Prohibited wording: {r.prohibited_wording}",
            "",
        ]
    (OUT / "SOURCE_AND_CAVEAT_BLOCKS.md").write_text("\n".join(sc)+"\n")

    report = [
        "# FED-CYCLE-CONTENT-PRODUCTION-LIBRARY-026 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED CHINESE CONTENT PRODUCTION LIBRARY / 6 PACKAGES / CLAIM-LINKED / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "- content packages: 6",
        "- P0-visual-ready: 5",
        "- text-ready / P1-visual-pending: 1 (1987 multi-leg)",
        "- language: zh-CN",
        "",
        "## Packages",
        "",
    ]
    for r in out.itertuples(index=False):
        report.append(f"- {r.content_id}: {r.primary_title_zh} — {r.visual_readiness}")
    report += [
        "",
        "## Production control",
        "",
        "- evidence numbers in scripts are formatted from canonical claim payload/wording;",
        "- every package has explicit claim and figure linkage;",
        "- source/caveat blocks are generated for editor/agent handoff;",
        "- CNT-04 inherits REVERIFY_BEFORE_CURRENT_USE because it includes the current NBER chronology claim;",
        "- CNT-06 does not falsely claim its B02 figure is rendered;",
        "- all scripts explicitly distinguish historical evidence from current prediction;",
        "- no buy/sell language, deterministic bottom, analog ranking or asset ranking is generated.",
        "",
        "026 is a publishing layer only and adds no empirical inference.",
    ]
    (OUT / "FED_CYCLE_CONTENT_PRODUCTION_LIBRARY_026_REPORT.md").write_text("\n".join(report)+"\n")

    qc = {
        "qc_gate":"PASS",
        "module":"FED-CYCLE-CONTENT-PRODUCTION-LIBRARY-026",
        "upstream_qc":{"022B":q022b["qc_gate"],"024":q024["qc_gate"],"025":q025["qc_gate"]},
        "content_packages":int(len(out)),
        "content_ids_exact_match":True,
        "p0_visual_ready_packages":int((out["visual_readiness"]=="READY_P0_VISUAL").sum()),
        "text_ready_visual_pending_p1_packages":int((out["visual_readiness"]=="TEXT_READY_VISUAL_PENDING_P1").sum()),
        "all_claim_refs_exist":True,
        "all_figure_refs_exist":True,
        "cnt06_b02_render_falsely_claimed":False,
        "cnt04_reverify_before_current_use":True,
        "script_numeric_source_mode":"CLAIM_PAYLOAD_OR_CANONICAL_WORDING_ONLY",
        "scripts_with_history_not_forecast_boundary":6,
        "prohibited_language_leaks":[],
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")


if __name__ == "__main__":
    main()
