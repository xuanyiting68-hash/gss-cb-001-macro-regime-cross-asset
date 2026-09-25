#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_platform_native_production_pack_028_v1"
OUT.mkdir(parents=True, exist_ok=True)

CONTENT = ROOT / "results" / "fed_cycle_content_production_library_026_v1" / "CONTENT_OBJECTS.csv"
Q026 = ROOT / "results" / "fed_cycle_content_production_library_026_v1" / "QC.json"
PUB = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1" / "PUBLISHING_MATRIX.csv"
READY = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1" / "PACKAGE_VISUAL_READINESS.csv"
Q027 = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1" / "QC.json"
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

def read_pass(path: Path):
    q=json.loads(path.read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def crow(claims,cid):
    z=claims[claims["claim_id"]==cid]
    if len(z)!=1:
        raise RuntimeError(f"claim missing/duplicate {cid}")
    return z.iloc[0]

def payload(claims,cid):
    return json.loads(crow(claims,cid)["metric_payload"])

def pct(x):
    return f"{float(x)*100:+.1f}%"

def mdd(x):
    return f"{float(x)*100:.1f}%"

def split_pipe(s):
    if pd.isna(s) or not str(s).strip():
        return []
    return [x for x in str(s).split("|") if x]

def content_row(content,cid):
    z=content[content["content_id"]==cid]
    if len(z)!=1: raise RuntimeError(cid)
    return z.iloc[0]

def build_evidence_values(claims):
    phase={}
    for asset in ["DXY","GOLD","NASDAQ","SP500","WTI"]:
        phase[asset]=payload(claims,f"CLM-PHASE-{asset}-FIRST_CUT")
    cases={b:payload(claims,f"CLM-CASE-{b}") for b in ["B03","B04","B05","B06","B07"]}
    return phase,cases

def shot_plans(content,claims):
    phase,cases=build_evidence_values(claims)
    sp,nq,au,wti=phase["SP500"],phase["NASDAQ"],phase["GOLD"],phase["WTI"]
    b03,b04,b05,b06,b07=(cases[x] for x in ["B03","B04","B05","B06","B07"])
    return {
        CONTENT_IDS[0]:[
            ("HOOK","第一次降息，就等于市场已经见底了吗？历史路径并不支持这么简单的结论。","首降 = 见底？先看路径",None),
            ("EVIDENCE",f"首降后，标普500历史+12个月终点收益中位数是{pct(sp['ret_12m'])}，但12个月最大回撤中位数仍有{mdd(sp['path_risk_value'])}。",f"S&P 500：+12M {pct(sp['ret_12m'])} / MDD {mdd(sp['path_risk_value'])}","FIG-PHASE-SP500-FIRST_CUT"),
            ("EVIDENCE",f"纳指的+12个月中位数是{pct(nq['ret_12m'])}，最大回撤中位数{mdd(nq['path_risk_value'])}，低点中位在第{int(nq['trough_month'])}个月。",f"Nasdaq：+12M {pct(nq['ret_12m'])} / MDD {mdd(nq['path_risk_value'])}","FIG-PHASE-NASDAQ-FIRST_CUT"),
            ("EVIDENCE",f"WTI的路径又不同：+12个月中位数{pct(wti['ret_12m'])}，最大回撤中位数{mdd(wti['path_risk_value'])}。",f"WTI：+12M {pct(wti['ret_12m'])} / MDD {mdd(wti['path_risk_value'])}","FIG-PHASE-WTI-FIRST_CUT"),
            ("SYNTHESIS","从恢复时钟看，五个完整支持资产里，首降相对暂停阶段是3个更慢、2个相同、0个更快。","Recovery Clock：3慢 / 2同 / 0快","FIG-RECOVERY-FIRSTCUT-VS-PAUSE"),
            ("METHOD","而019和020两轮事前状态检验，都没有验证出稳定的见底计时规则。","简单状态变量 ≠ 已验证底部计时器","FIG-GUARD-020"),
            ("BOUNDARY","所以第一次降息是政策阶段标签，不是市场底部时间戳。以上是历史描述，不是对当前市场底部或未来收益的预测。","历史描述 ≠ 当前预测",None),
        ],
        CONTENT_IDS[1]:[
            ("HOOK","同样叫第一次降息，历史上的市场路径可以完全不同。","同一个FIRST_CUT，不同路径",None),
            ("EVIDENCE",f"1995案例里，标普500首降后+12个月是{pct(b03['SP500']['ret_12m'])}。",f"1995：S&P 500 {pct(b03['SP500']['ret_12m'])}","FIG-CASE-B03"),
            ("EVIDENCE",f"2001案例里，纳指+12个月是{pct(b04['NASDAQ']['ret_12m'])}，最大回撤{mdd(b04['NASDAQ']['mdd_12m'])}。",f"2001：Nasdaq {pct(b04['NASDAQ']['ret_12m'])} / MDD {mdd(b04['NASDAQ']['mdd_12m'])}","FIG-CASE-B04"),
            ("EVIDENCE",f"2007案例里，标普500+12个月{pct(b05['SP500']['ret_12m'])}，黄金却是{pct(b05['GOLD']['ret_12m'])}。",f"2007：S&P {pct(b05['SP500']['ret_12m'])} / Gold {pct(b05['GOLD']['ret_12m'])}","FIG-CASE-B05"),
            ("EVIDENCE",f"2019案例里标普500是{pct(b06['SP500']['ret_12m'])}；2024案例里是{pct(b07['SP500']['ret_12m'])}。","2019 与 2024：又是不同路径","FIG-CASE-B06"),
            ("SYNTHESIS","同一个政策阶段标签，可以和不同的增长、通胀、信用压力以及后续冲击共存。","政策标签不是完整市场状态","FIG-CASE-B07"),
            ("BOUNDARY","这些案例用来理解路径差异，不是挑一个单一历史模板去套当前周期。","案例 ≠ 当前预测模板",None),
        ],
        CONTENT_IDS[2]:[
            ("HOOK","降息周期里，黄金和美股会一起走吗？历史上并不总是如此。","Gold vs Equities：同阶段，不同路径",None),
            ("EVIDENCE",f"首降后黄金+12个月中位数{pct(au['ret_12m'])}，最大回撤中位数{mdd(au['path_risk_value'])}。",f"Gold：+12M {pct(au['ret_12m'])} / MDD {mdd(au['path_risk_value'])}","FIG-PHASE-GOLD-FIRST_CUT"),
            ("EVIDENCE",f"标普500对应是{pct(sp['ret_12m'])}和{mdd(sp['path_risk_value'])}；纳指是{pct(nq['ret_12m'])}和{mdd(nq['path_risk_value'])}。","S&P / Nasdaq：终点与路径风险不同","FIG-PHASE-SP500-FIRST_CUT"),
            ("CASE",f"2001首降后，黄金是{pct(b04['GOLD']['ret_12m'])}，纳指却是{pct(b04['NASDAQ']['ret_12m'])}。",f"2001：Gold {pct(b04['GOLD']['ret_12m'])} vs Nasdaq {pct(b04['NASDAQ']['ret_12m'])}","FIG-CASE-B04"),
            ("CASE",f"2007首降后，黄金是{pct(b05['GOLD']['ret_12m'])}，标普500是{pct(b05['SP500']['ret_12m'])}。",f"2007：Gold {pct(b05['GOLD']['ret_12m'])} vs S&P {pct(b05['SP500']['ret_12m'])}","FIG-CASE-B05"),
            ("SYNTHESIS","这说明Fed阶段只能提供背景，资产自身暴露和后续冲击仍然重要。","同阶段 ≠ 同方向",None),
            ("BOUNDARY","这里不做资产优劣排名，也不是当前配置建议或市场预测。","跨资产比较 ≠ 排名/配置建议",None),
        ],
        CONTENT_IDS[3]:[
            ("HOOK","研究历史周期最危险的错误之一，是把后来才知道的事情塞回过去。","Hindsight Bias：时间戳也是证据",None),
            ("EVIDENCE","2001年1月首降时，后来NBER认定的2001年3月经济峰值还在未来，官方认定更晚。","2001衰退定年：RETROSPECTIVE","FIG-CTX-B04_CTX_02"),
            ("EVIDENCE","9·11发生在2001年1月首降之后，不能把它当成当时政策决定的原始理由。","9·11：POST_ANCHOR_SHOCK","FIG-CTX-B04_CTX_03"),
            ("EVIDENCE","2007年的衰退起点同样是后来由NBER事后定年，不能倒灌到9月首降当时。","2007衰退定年：RETROSPECTIVE","FIG-CTX-B05_CTX_03"),
            ("EVIDENCE","2019年7月首降时的官方语境是全球发展和较低通胀压力；2020衰退定年属于后来信息。","2020衰退：RETROSPECTIVE","FIG-CTX-B06_CTX_02"),
            ("EVIDENCE","COVID是2019年首降之后的新冲击，不能被写成2019年7月的降息理由。","COVID：POST_ANCHOR_SHOCK","FIG-CTX-B06_CTX_03"),
            ("BOUNDARY","所以历史研究要区分当时可知、事后定年和后续冲击。这不是对当前是否会衰退的预测。","当时可知 ≠ 后来才知道",None),
        ],
        CONTENT_IDS[4]:[
            ("HOOK","一年后是正收益，不代表持有过程中没有深回撤，也不代表很快恢复。","收益终点 ≠ 持有路径",None),
            ("EVIDENCE",f"首降后标普500+12个月中位数{pct(sp['ret_12m'])}，但最大回撤中位数仍有{mdd(sp['path_risk_value'])}。",f"S&P：+12M {pct(sp['ret_12m'])} / MDD {mdd(sp['path_risk_value'])}","FIG-PHASE-SP500-FIRST_CUT"),
            ("EVIDENCE",f"纳指+12个月中位数{pct(nq['ret_12m'])}，最大回撤中位数{mdd(nq['path_risk_value'])}。",f"Nasdaq：+12M {pct(nq['ret_12m'])} / MDD {mdd(nq['path_risk_value'])}","FIG-PHASE-NASDAQ-FIRST_CUT"),
            ("EVIDENCE",f"黄金从政策锚点到完全恢复的历史中位时间是{int(au['anchor_to_full_recovery_months'])}个月。",f"Gold full recovery：{int(au['anchor_to_full_recovery_months'])}个月","FIG-PHASE-GOLD-FIRST_CUT"),
            ("EVIDENCE",f"WTI对应的完全恢复中位时间是{int(wti['anchor_to_full_recovery_months'])}个月。",f"WTI full recovery：{int(wti['anchor_to_full_recovery_months'])}个月","FIG-PHASE-WTI-FIRST_CUT"),
            ("SYNTHESIS","五个完整支持资产里，FIRST_CUT相对PAUSE是3个更慢、2个相同、0个更快。","Recovery Clock：3慢 / 2同 / 0快","FIG-RECOVERY-FIRSTCUT-VS-PAUSE"),
            ("BOUNDARY","所以终点收益、途中回撤和恢复时间必须分开理解。以上是历史风险分布，不是未来恢复时间预测。","三种风险对象，不能混成一个收益率",None),
        ],
        CONTENT_IDS[5]:[
            ("HOOK","1987到1989，并不是一条干净的“加息—暂停—降息”直线。","1987–89：不是一个标准单周期",None),
            ("STRUCTURE","我们的机械周期定义里，B02由T03_1987、T04_1987和T05_1988三个独立子周期构成。","T03 / T04 / T05 三个子周期","FIG-CASE-B02"),
            ("CONTEXT","1987年10月的Black Monday发生在这些子周期之间。","Black Monday：1987-10-19","FIG-CASE-B02"),
            ("CONTEXT","随后Fed的流动性支持属于明确的金融稳定语境。","Liquidity response = 金融稳定语境","FIG-CASE-B02"),
            ("METHOD","如果为了讲故事把它们压成一条FIRST_HIKE到FIRST_CUT直线，会把不同政策腿和冲击混在一起。","不要人为构造 synthetic cycle","FIG-CASE-B02"),
            ("SYNTHESIS","这个案例最重要的不是某个收益数字，而是先把周期边界和时间线划对。","周期定义本身就是研究的一部分","FIG-CASE-B02"),
            ("BOUNDARY","这是历史结构说明，不是对当前Fed周期的类比或预测。","历史结构 ≠ 当前类比预测",None),
        ],
    }

def make_shotlist(content,claims):
    plans=shot_plans(content,claims)
    rows=[]
    timing=[(0,7),(7,18),(18,29),(29,40),(40,51),(51,62),(62,72)]
    for cid in CONTENT_IDS:
        c=content_row(content,cid)
        plan=plans[cid]
        if len(plan)!=7: raise RuntimeError(f"shot count changed {cid}")
        for i,(role,vo,screen,fig) in enumerate(plan,1):
            s,e=timing[i-1]
            rows.append({
                "content_id":cid,
                "shot_no":i,
                "start_sec":s,
                "end_sec":e,
                "role":role,
                "voiceover_zh":vo,
                "onscreen_text_zh":screen,
                "figure_key":fig or "",
                "claim_ids":c["claim_ids"],
                "freshness_rule":c["freshness_rule"],
                "subtitle_text_zh":vo,
                "source_caveat_action":"closing card + caption" if role=="BOUNDARY" else "retain figure footer when evidence figure shown",
                "canvas":"9:16_PRODUCTION_PLAN_ONLY",
                "final_mp4_rendered":False,
            })
    return pd.DataFrame(rows)

def carousel_specs(content,claims):
    phase,cases=build_evidence_values(claims)
    sp,nq,au,wti=phase["SP500"],phase["NASDAQ"],phase["GOLD"],phase["WTI"]
    cards={
        CONTENT_IDS[0]:[
            ("COVER","第一次降息 = 市场见底？","先把终点收益、途中回撤和恢复时间拆开看。",""),
            ("EVIDENCE",f"标普500：+12个月中位数{pct(sp['ret_12m'])}","但12个月最大回撤中位数仍有"+mdd(sp["path_risk_value"]),"FIG-PHASE-SP500-FIRST_CUT"),
            ("EVIDENCE",f"纳指：+12个月{pct(nq['ret_12m'])}","最大回撤中位数"+mdd(nq["path_risk_value"])+f"，低点中位第{int(nq['trough_month'])}个月","FIG-PHASE-NASDAQ-FIRST_CUT"),
            ("EVIDENCE",f"WTI：+12个月{pct(wti['ret_12m'])}","最大回撤中位数"+mdd(wti["path_risk_value"]),"FIG-PHASE-WTI-FIRST_CUT"),
            ("SYNTHESIS","恢复时钟更关键","FIRST_CUT相对PAUSE：3个更慢、2个相同、0个更快。","FIG-RECOVERY-FIRSTCUT-VS-PAUSE"),
            ("METHOD","简单状态也没给出稳定底部时钟","019/020没有验证出稳健的事前底部计时规则。","FIG-GUARD-020"),
            ("SOURCE_BOUNDARY","结论边界","FIRST_CUT是政策阶段标签，不是市场底部时间戳。历史研究/教育内容，不是当前预测或投资建议。",""),
        ],
        CONTENT_IDS[1]:[
            ("COVER","同样叫“第一次降息”","为什么1995、2001、2007、2019、2024走得完全不同？",""),
            ("EVIDENCE","1995：非衰退式案例","把1994–95作为一条独立历史路径看，而不是“软着陆模板”。","FIG-CASE-B03"),
            ("EVIDENCE","2001：科技股路径很弱",f"Nasdaq +12个月{pct(cases['B04']['NASDAQ']['ret_12m'])}，MDD {mdd(cases['B04']['NASDAQ']['mdd_12m'])}。","FIG-CASE-B04"),
            ("EVIDENCE","2007：股票与黄金分化",f"S&P 500 {pct(cases['B05']['SP500']['ret_12m'])}；Gold {pct(cases['B05']['GOLD']['ret_12m'])}。","FIG-CASE-B05"),
            ("EVIDENCE","2019：后续又出现全新冲击",f"S&P 500 +12个月{pct(cases['B06']['SP500']['ret_12m'])}。","FIG-CASE-B06"),
            ("EVIDENCE","2024：又是一条不同路径",f"S&P 500 +12个月{pct(cases['B07']['SP500']['ret_12m'])}。","FIG-CASE-B07"),
            ("SOURCE_BOUNDARY","不要挑一个历史模板硬套今天","案例用于理解路径差异，不是“最像当前周期”的排名。",""),
        ],
        CONTENT_IDS[2]:[
            ("COVER","黄金和美股会一起走吗？","同一个Fed阶段，不等于同一条资产路径。",""),
            ("EVIDENCE","Gold 首降历史分布",f"+12个月{pct(au['ret_12m'])}；MDD {mdd(au['path_risk_value'])}。","FIG-PHASE-GOLD-FIRST_CUT"),
            ("EVIDENCE","S&P 500 首降历史分布",f"+12个月{pct(sp['ret_12m'])}；MDD {mdd(sp['path_risk_value'])}。","FIG-PHASE-SP500-FIRST_CUT"),
            ("EVIDENCE","Nasdaq 首降历史分布",f"+12个月{pct(nq['ret_12m'])}；MDD {mdd(nq['path_risk_value'])}。","FIG-PHASE-NASDAQ-FIRST_CUT"),
            ("CASE","2001：Gold vs Nasdaq",f"{pct(cases['B04']['GOLD']['ret_12m'])} vs {pct(cases['B04']['NASDAQ']['ret_12m'])}。","FIG-CASE-B04"),
            ("CASE","2007：Gold vs S&P",f"{pct(cases['B05']['GOLD']['ret_12m'])} vs {pct(cases['B05']['SP500']['ret_12m'])}。","FIG-CASE-B05"),
            ("SOURCE_BOUNDARY","跨资产比较 ≠ 资产排名","历史路径分化不等于当前配置建议。",""),
        ],
        CONTENT_IDS[3]:[
            ("COVER","历史研究最大的陷阱：后见之明","后来知道的事，不能倒灌进当时。",""),
            ("EVIDENCE","2001衰退定年","2001年3月峰值是后来NBER事后认定；1月首降时并未知晓。","FIG-CTX-B04_CTX_02"),
            ("EVIDENCE","9·11","发生在2001年1月首降之后，是POST_ANCHOR_SHOCK。","FIG-CTX-B04_CTX_03"),
            ("EVIDENCE","2007衰退定年","2007年12月峰值是后来官方定年，不是9月首降时的已知标签。","FIG-CTX-B05_CTX_03"),
            ("EVIDENCE","2020衰退定年","2019年7月首降时，2020衰退日期尚未发生、也未被官方认定。","FIG-CTX-B06_CTX_02"),
            ("EVIDENCE","COVID","是2019年首降之后的新冲击，不能改写成当时的降息理由。","FIG-CTX-B06_CTX_03"),
            ("SOURCE_BOUNDARY","时间戳也是证据","区分当时可知、事后定年、后续冲击；不是当前衰退预测。",""),
        ],
        CONTENT_IDS[4]:[
            ("COVER","只看一年后涨跌，为什么不够？","真正影响持有体验的是路径和恢复时钟。",""),
            ("EVIDENCE","S&P 500：终点 vs MDD",f"+12个月{pct(sp['ret_12m'])}；MDD {mdd(sp['path_risk_value'])}。","FIG-PHASE-SP500-FIRST_CUT"),
            ("EVIDENCE","Nasdaq：终点 vs MDD",f"+12个月{pct(nq['ret_12m'])}；MDD {mdd(nq['path_risk_value'])}。","FIG-PHASE-NASDAQ-FIRST_CUT"),
            ("EVIDENCE","Gold：完全恢复时钟",f"锚点到完全恢复KM中位数：{int(au['anchor_to_full_recovery_months'])}个月。","FIG-PHASE-GOLD-FIRST_CUT"),
            ("EVIDENCE","WTI：完全恢复时钟",f"锚点到完全恢复KM中位数：{int(wti['anchor_to_full_recovery_months'])}个月。","FIG-PHASE-WTI-FIRST_CUT"),
            ("SYNTHESIS","FIRST_CUT vs PAUSE","五个完整支持资产：3慢、2同、0快。","FIG-RECOVERY-FIRSTCUT-VS-PAUSE"),
            ("SOURCE_BOUNDARY","三个风险对象要分开","终点收益、途中回撤、完全恢复时间都不是未来预测。",""),
        ],
        CONTENT_IDS[5]:[
            ("COVER","1987–1989不是一个标准单周期","先把政策腿和事件边界划对。",""),
            ("STRUCTURE","三个机械子周期","T03_1987、T04_1987、T05_1988分别保留。","FIG-CASE-B02"),
            ("CONTEXT","Black Monday的位置","1987-10-19发生在这些政策子周期之间。","FIG-CASE-B02"),
            ("CONTEXT","Fed流动性支持","这是金融稳定语境，不能等同于资产底部信号。","FIG-CASE-B02"),
            ("METHOD","为什么不能合成一条线","不同政策腿和市场冲击会被错误混在一起。","FIG-CASE-B02"),
            ("SYNTHESIS","周期边界本身就是研究的一部分","先定义清楚事件，再比较资产。","FIG-CASE-B02"),
            ("SOURCE_BOUNDARY","不是当前类比模板","历史结构说明，不是对当前Fed周期的预测。",""),
        ],
    }
    rows=[]
    for cid in CONTENT_IDS:
        c=content_row(content,cid)
        for i,(role,head,body,fig) in enumerate(cards[cid],1):
            rows.append({
                "content_id":cid,
                "card_no":i,
                "role":role,
                "headline_zh":head,
                "body_zh":body,
                "figure_key":fig,
                "claim_ids":c["claim_ids"],
                "freshness_rule":c["freshness_rule"],
                "source_boundary_required":role=="SOURCE_BOUNDARY",
            })
    return pd.DataFrame(rows)

def article_texts(content,claims):
    phase,cases=build_evidence_values(claims)
    sp,nq,au,wti=phase["SP500"],phase["NASDAQ"],phase["GOLD"],phase["WTI"]
    b03,b04,b05,b06,b07=(cases[x] for x in ["B03","B04","B05","B06","B07"])

    articles={}
    articles[CONTENT_IDS[0]]=f"""# 第一次降息之后，市场就已经见底了吗？历史数据不支持这么简单的结论

很多市场叙事会把“第一次降息”直接翻译成“风险已经结束”。这种说法的问题，不是它永远错误，而是它把三个完全不同的对象压成了一个：**一年后的终点收益、持有过程中的最大回撤、以及从政策锚点到完全恢复所需要的时间。**

> [图：FIG-PHASE-SP500-FIRST_CUT]

在支持样本中，FIRST_CUT 之后标普500的+12个月终点收益中位数为 **{pct(sp['ret_12m'])}**，但12个月最大回撤中位数仍有 **{mdd(sp['path_risk_value'])}**，回撤低点中位出现在第 **{int(sp['trough_month'])}** 个月。换句话说，“一年后是正收益”并不意味着从第一天开始就是一条平滑上行路径。

> [图：FIG-PHASE-NASDAQ-FIRST_CUT]

纳指也呈现类似的路径问题：+12个月中位数为 **{pct(nq['ret_12m'])}**，最大回撤中位数为 **{mdd(nq['path_risk_value'])}**，低点中位同样出现在第 **{int(nq['trough_month'])}** 个月。对实际持有人而言，路径风险和终点收益必须分开讨论。

> [图：FIG-PHASE-WTI-FIRST_CUT]

WTI进一步说明，不同资产在同一政策阶段可以有完全不同的表现：FIRST_CUT 后+12个月中位数为 **{pct(wti['ret_12m'])}**，最大回撤中位数为 **{mdd(wti['path_risk_value'])}**。因此，“Fed开始降息”不能被机械翻译成一个跨资产统一信号。

## 恢复时钟比“涨没涨”更严格

> [图：FIG-RECOVERY-FIRSTCUT-VS-PAUSE]

五个完整支持资产中，FIRST_CUT 相对 PAUSE_START 的锚点到完全恢复时钟，表现为 **3个更慢、2个相同、0个更快**。这不是说降息“导致”恢复变慢；它只说明，在这组历史样本里，“第一次降息后恢复一定更快”并没有得到支持。

## 能不能用事前状态变量找底？

> [图：FIG-GUARD-019]
>
> [图：FIG-GUARD-020]

项目进一步冻结了019和020两轮检验，尝试用事前可知的增长、收益率曲线、金融条件、Baa利差、VIX等变量解释FIRST_CUT之后的风险资产低点时机。结果并没有形成稳定、composition-robust 的底部计时规则，因此这一小样本 timing-rule 分支已经停止，而不是继续加变量“优化到显著”。

## 结论

FIRST_CUT 更适合被理解为一个**政策阶段标签**，而不是市场底部的时间戳。历史上，终点收益、途中回撤、低点时机和完全恢复时间可以同时指向不同的信息。

### 来源与证据
Claims: {content_row(content,CONTENT_IDS[0])['claim_ids']}

Figures: {content_row(content,CONTENT_IDS[0])['figure_keys']}

### 边界
本文为历史研究/教育内容。历史分布不构成当前市场预测、确定性底部判断、资产排序或投资建议。
"""

    articles[CONTENT_IDS[1]]=f"""# 同样叫“第一次降息”，为什么历史上的市场路径差这么多？

如果只看 FIRST_CUT 这个标签，1995、2001、2007、2019、2024似乎属于同一类事件：Fed从此前的紧缩或高利率状态转向第一次降息。但只要把资产路径和当时信息环境放回去，就会发现这些案例并不是同一种市场状态。

> [图：FIG-CASE-B03]

1995案例中，标普500首降后+12个月为 **{pct(b03['SP500']['ret_12m'])}**。NBER当前 chronology 并未把1994–95认定为衰退期，但这是一项事后历史分类，不能倒过来把1995包装成一个“保证软着陆”的模板。

> [图：FIG-CASE-B04]

2001案例显著不同。纳指首降后+12个月为 **{pct(b04['NASDAQ']['ret_12m'])}**，12个月最大回撤达到 **{mdd(b04['NASDAQ']['mdd_12m'])}**。而且2001年后续路径还包含9·11这一发生在首降之后的重大冲击，因此不能把完整一年路径全部归因于1月的政策动作。

> [图：FIG-CASE-B05]

2007案例中，标普500首降后+12个月为 **{pct(b05['SP500']['ret_12m'])}**，黄金则为 **{pct(b05['GOLD']['ret_12m'])}**。当时住房和信用压力已经可见，但后来被NBER认定的衰退峰值和完整危机规模，并不是9月首降时已经正式知道的事实。

> [图：FIG-CASE-B06]

2019案例里，标普500+12个月为 **{pct(b06['SP500']['ret_12m'])}**。然而这一观察窗口后来遇到COVID，后者是首降后才出现的新冲击，不能被写成2019年7月降息的原始理由。

> [图：FIG-CASE-B07]

2024案例里，标普500首降后+12个月为 **{pct(b07['SP500']['ret_12m'])}**。这又是一条不同的路径。

## 真正该比较的是什么？

比“第一次降息”四个字更重要的，是当时的增长、通胀、信用环境、金融条件、资产估值与后续新冲击。政策标签提供了时间锚点，但不等于完整的市场状态。

### 来源与证据
Claims: {content_row(content,CONTENT_IDS[1])['claim_ids']}

Figures: FIG-CASE-B03|FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07

### 边界
这些案例用于理解历史路径差异，不用于挑选“最像当前”的单一历史模板，也不构成当前周期预测。
"""

    articles[CONTENT_IDS[2]]=f"""# 降息周期里，黄金和美股会一起走吗？历史上并不总是如此

跨资产研究最容易出现的误区之一，是把一个宏观政策标签直接转换成“所有资产应该同方向”。FIRST_CUT 的历史样本并不支持这种简单映射。

> [图：FIG-PHASE-GOLD-FIRST_CUT]

黄金在 FIRST_CUT 后的+12个月终点收益中位数为 **{pct(au['ret_12m'])}**，最大回撤中位数为 **{mdd(au['path_risk_value'])}**。

> [图：FIG-PHASE-SP500-FIRST_CUT]

标普500对应的+12个月中位数为 **{pct(sp['ret_12m'])}**，最大回撤中位数为 **{mdd(sp['path_risk_value'])}**。

> [图：FIG-PHASE-NASDAQ-FIRST_CUT]

纳指对应为 **{pct(nq['ret_12m'])}** 和 **{mdd(nq['path_risk_value'])}**。即使只看历史中位数，三个资产的终点与路径风险也不是同一个对象。

## 2001：黄金与科技股明显分化

> [图：FIG-CASE-B04]

2001首降后，黄金+12个月为 **{pct(b04['GOLD']['ret_12m'])}**，纳指为 **{pct(b04['NASDAQ']['ret_12m'])}**。这类分化提醒我们，黄金的避险/实际利率敏感性与科技股的增长/估值暴露并不相同。

## 2007：又是另一种分化

> [图：FIG-CASE-B05]

2007首降后，黄金+12个月为 **{pct(b05['GOLD']['ret_12m'])}**，标普500为 **{pct(b05['SP500']['ret_12m'])}**。信用和住房压力逐步升级，使这段历史与2001、2019或2024不能简单互换。

## 结论

Fed阶段可以作为宏观背景，但不能自动生成一个“资产排行榜”。真正的跨资产分析需要同时考虑路径风险、增长暴露、信用压力、通胀与后续冲击。

### 来源与证据
Claims: {content_row(content,CONTENT_IDS[2])['claim_ids']}

Figures: {content_row(content,CONTENT_IDS[2])['figure_keys']}

### 边界
本文不评价哪个资产“最好”，也不提供当前配置建议或收益预测。
"""

    articles[CONTENT_IDS[3]]=f"""# 研究历史周期最容易犯的错：把后来才知道的事，假装成当时已经知道

宏观历史研究里，数据本身重要，**时间戳同样重要**。一个事实今天成立，不代表它在当时已经被市场、政策制定者或研究者知道。

> [图：FIG-CTX-B04_CTX_02]

2001年1月第一次降息时，后来被NBER认定的2001年3月经济峰值还没有发生，更不可能已经被官方确认。把后来确定的衰退日期倒灌回1月，会把事后信息伪装成实时信息。

> [图：FIG-CTX-B04_CTX_03]

同样，9·11发生在2001年1月首降八个多月之后。它可以解释为什么后续12个月资产路径包含新的重大冲击，但不能成为1月首降的原始理由。

> [图：FIG-CTX-B05_CTX_03]

2007年9月第一次降息时，住房和信用压力已经可见；但后来NBER认定的2007年12月经济峰值，是之后才作出的官方历史定年。把“当时已经看到的信用压力”和“后来确认的衰退日期”混为一谈，会制造后见偏差。

> [图：FIG-CTX-B06_CTX_02]

2019年7月首降时，官方语境包括全球发展和较低的通胀压力，而2020年衰退的起止日期属于后来信息。

> [图：FIG-CTX-B06_CTX_03]

COVID更是一个首降后出现的新冲击。它可以改变2019–2020的资产路径，却不能被回写成2019年7月政策决定的理由。

## 三种时间层

这个项目把历史信息明确分成：
- CONTEMPORANEOUS_POLICY_CONTEXT：当时可知/当时表达的政策语境；
- RETROSPECTIVE_DATING：后来才完成的官方历史定年；
- POST_ANCHOR_SHOCK：政策锚点之后才发生的新冲击。

这不是格式问题，而是识别问题。只有保留时间层，才不会让历史看起来“比当时更容易预测”。

### 来源与证据
Claims: {content_row(content,CONTENT_IDS[3])['claim_ids']}

Figures: FIG-CTX-B04_CTX_02|FIG-CTX-B04_CTX_03|FIG-CTX-B05_CTX_03|FIG-CTX-B06_CTX_02|FIG-CTX-B06_CTX_03

Freshness: REVERIFY_BEFORE_CURRENT_USE

### 边界
本文讨论的是历史信息时序和证据纪律，不是对当前美国经济是否会进入衰退的预测。
"""

    articles[CONTENT_IDS[4]]=f"""# 只看一年后涨跌还不够：真正影响持有体验的是“恢复时钟”

投资结果经常被压缩成一个数字：“一年后涨了多少？”但从风险管理角度，至少还有两个问题同样重要：中间最大亏损过多少，以及多久才能从政策锚点之后的回撤里完全恢复。

> [图：FIG-PHASE-SP500-FIRST_CUT]

FIRST_CUT 后，标普500+12个月终点收益中位数为 **{pct(sp['ret_12m'])}**，但最大回撤中位数仍有 **{mdd(sp['path_risk_value'])}**。

> [图：FIG-PHASE-NASDAQ-FIRST_CUT]

纳指+12个月中位数为 **{pct(nq['ret_12m'])}**，最大回撤中位数为 **{mdd(nq['path_risk_value'])}**。如果只看最终收益，就会漏掉持有过程中真实经历的路径风险。

> [图：FIG-PHASE-GOLD-FIRST_CUT]

黄金从政策锚点到完全恢复的Kaplan-Meier中位时间为 **{int(au['anchor_to_full_recovery_months'])}个月**。

> [图：FIG-PHASE-WTI-FIRST_CUT]

WTI对应为 **{int(wti['anchor_to_full_recovery_months'])}个月**。

> [图：FIG-RECOVERY-FIRSTCUT-VS-PAUSE]

把 FIRST_CUT 与 PAUSE_START 比较，在五个完整支持资产里，完全恢复时钟表现为 **3个更慢、2个相同、0个更快**。这不是因果结论，而是历史支持样本的描述性比较。

## 为什么恢复时钟重要？

对不同持有期和风险承受能力的人，一样的最终收益可能意味着完全不同的过程。终点收益回答“最后在哪里”，MDD回答“途中最坏到哪里”，恢复时钟回答“回到锚点要多久”。这三个问题不能互相替代。

### 来源与证据
Claims: {content_row(content,CONTENT_IDS[4])['claim_ids']}

Figures: {content_row(content,CONTENT_IDS[4])['figure_keys']}

### 边界
历史恢复时钟不是未来恢复时间预测，也不构成买卖或配置建议。
"""

    articles[CONTENT_IDS[5]]=f"""# 为什么1987—1989不能被压成“一次标准加息周期”？

研究历史周期时，一个看似基础的问题往往决定后面的所有统计是否可信：**周期边界到底怎么定义？**

> [图：FIG-CASE-B02]

在本项目的机械周期定义里，1987–1989的B02不是一条单一的“FIRST_HIKE → LAST_HIKE → PAUSE → FIRST_CUT”标准路径，而是三个分别保留的机械子周期：
- T03_1987
- T04_1987
- T05_1988

## Black Monday位于子周期之间

1987年10月19日的Black Monday发生在这些子周期之间。它是一个重大市场压力事件，但不能因为它非常重要，就把周围不同的政策腿全部合并成一个统一周期。

随后Fed公开表达提供流动性的准备，并采取操作支持市场功能。这属于金融稳定语境，不等于一个经过验证的资产底部信号。

## 为什么“合成一个周期”会污染研究？

如果人为构造一个从1987年初一路跨到1989年中的单一政策路径，就会同时改变：
- FIRST_HIKE/ FIRST_CUT的配对；
- 周期长度；
- 资产锚点；
- 后续回撤与恢复统计；
- 对Black Monday位置的解释。

这也是为什么B02在案例库里被明确标成COMPOSITE_MULTI_LEG，而不是为了讲故事方便被压成一条线。

## 更一般的研究启示

历史研究不只是把价格数据放进公式。事件定义、政策腿划分、时间戳、当时可知信息与事后信息的分离，本身就是研究设计的一部分。

### 来源与证据
Claims: {content_row(content,CONTENT_IDS[5])['claim_ids']}

Figure: FIG-CASE-B02

### 边界
本文是历史结构与研究设计说明，不把1987–1989作为当前Fed周期的类比模板，也不构成当前市场预测。
"""
    return articles

def panda_templates(content,ready):
    result=[]
    for cid in CONTENT_IDS:
        c=content_row(content,cid)
        rr=ready[ready["content_id"]==cid].iloc[0]
        result.append({
            "content_id":cid,
            "intent_examples":[
                c["primary_title_zh"],
                json.loads(c["hooks_json"])[0],
            ],
            "claim_ids":split_pipe(c["claim_ids"]),
            "figure_keys":split_pipe(rr["canonical_visual_keys"]),
            "freshness_rule":c["freshness_rule"],
            "answer_structure":[
                "direct_answer",
                "historical_evidence",
                "figure_references_optional",
                "support_and_freshness",
                "what_evidence_does_not_prove",
                "mandatory_boundary",
            ],
            "required_caveat":c["mandatory_caveat"],
            "forbidden_transformations":[
                "historical_median_to_personalized_trade_instruction",
                "closest_current_analog_ranking",
                "best_asset_ranking",
                "deterministic_bottom_date",
                "unsupported_causal_Fed_claim",
            ],
            "current_data_rule":"If current state is requested, retrieve the latest valid append-only current snapshot; do not treat 2026-09-25 snapshot as live by default.",
            "evidence_status":"HISTORICAL_DESCRIPTIVE_CONTENT_OBJECT",
            "causal_status":"NONE",
            "deployment_status":"NOT_DEPLOYABLE",
        })
    return result

def main():
    q026=read_pass(Q026); q027=read_pass(Q027); q022b=read_pass(Q022B); q024=read_pass(Q024)
    content=pd.read_csv(CONTENT)
    pub=pd.read_csv(PUB)
    ready=pd.read_csv(READY)
    claims=pd.read_csv(CLAIMS)
    figreg=pd.read_csv(FIGREG)
    render=pd.concat([pd.read_csv(R025),pd.read_csv(R027)],ignore_index=True)

    if list(content["content_id"])!=CONTENT_IDS:
        raise RuntimeError("026 content order/universe changed")
    if len(pub)!=24 or pub["content_id"].nunique()!=6:
        raise RuntimeError("027 publishing matrix changed")
    if not (ready["new_visual_readiness"]=="VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE").all():
        raise RuntimeError("027 package visual readiness incomplete")

    claim_set=set(claims["claim_id"])
    fig_set=set(figreg["figure_key"])
    rendered_set=set(render["figure_key"])
    for _,r in content.iterrows():
        for cid in split_pipe(r["claim_ids"]):
            if cid not in claim_set: raise RuntimeError(f"missing claim {cid}")
    for _,r in ready.iterrows():
        for fk in split_pipe(r["canonical_visual_keys"]):
            if fk not in fig_set or fk not in rendered_set:
                raise RuntimeError(f"visual not rendered/registered {fk}")

    # Douyin / TikTok.
    shots=make_shotlist(content,claims)
    if shots["content_id"].nunique()!=6 or len(shots)!=42:
        raise RuntimeError("expected 6 x 7 shot rows")
    for cid,g in shots.groupby("content_id",sort=False):
        if not (6<=len(g)<=9): raise RuntimeError(f"shot count {cid}")
        g=g.sort_values("shot_no")
        if not (g["start_sec"].tolist()==sorted(g["start_sec"].tolist())):
            raise RuntimeError("shot start order")
        if any(g["start_sec"].iloc[i] < g["end_sec"].iloc[i-1] for i in range(1,len(g))):
            raise RuntimeError(f"overlapping shots {cid}")
        if g.iloc[-1]["role"]!="BOUNDARY":
            raise RuntimeError(f"last shot not boundary {cid}")
    if shots["final_mp4_rendered"].any():
        raise RuntimeError("028 must not claim final MP4")
    shots.to_csv(OUT/"DOUYIN_TIKTOK_SHOTLISTS_ZH.csv",index=False)

    caps=["# 028 抖音 / TikTok 发布文案\n"]
    for cid in CONTENT_IDS:
        c=content_row(content,cid)
        hooks=json.loads(c["hooks_json"])
        caps += [
            f"## {cid}",
            "",
            f"**封面：** {c['primary_title_zh']}",
            "",
            f"**开头：** {hooks[0]}",
            "",
            f"**Caption：** {c['short_video_script_zh']} {c['mandatory_caveat']}",
            "",
            f"**证据图：** {ready.loc[ready['content_id']==cid,'canonical_visual_keys'].iloc[0]}",
            "",
            f"**Freshness：** {c['freshness_rule']}",
            "",
        ]
    (OUT/"DOUYIN_TIKTOK_CAPTIONS_ZH.md").write_text("\n".join(caps)+"\n")

    # Xiaohongshu.
    car=carousel_specs(content,claims)
    if car["content_id"].nunique()!=6 or len(car)!=42:
        raise RuntimeError("expected 6 x 7 carousel cards")
    for cid,g in car.groupby("content_id",sort=False):
        if not (6<=len(g)<=9): raise RuntimeError(f"carousel count {cid}")
        if int((g["role"]=="COVER").sum())!=1: raise RuntimeError(f"cover count {cid}")
        if int((g["role"]=="SOURCE_BOUNDARY").sum())<1: raise RuntimeError(f"source boundary missing {cid}")
        if g.sort_values("card_no").iloc[-1]["role"]!="SOURCE_BOUNDARY":
            raise RuntimeError(f"last card must be source boundary {cid}")
    car.to_csv(OUT/"XIAOHONGSHU_CAROUSELS_ZH.csv",index=False)

    xhs=["# 028 小红书发布文案\n"]
    for cid in CONTENT_IDS:
        c=content_row(content,cid)
        xhs += [
            f"## {cid}",
            "",
            f"**标题：** {c['primary_title_zh']}",
            "",
            f"**正文：** {c['short_video_script_zh']}",
            "",
            f"**结尾：** {c['mandatory_caveat']}",
            "",
            f"**Freshness：** {c['freshness_rule']}",
            "",
        ]
    (OUT/"XIAOHONGSHU_CAPTIONS_ZH.md").write_text("\n".join(xhs)+"\n")

    # Long-form.
    articles=article_texts(content,claims)
    if set(articles)!=set(CONTENT_IDS): raise RuntimeError("article universe mismatch")
    article_md=["# 028 公众号 / 深度长文成稿库",""]
    for cid in CONTENT_IDS:
        article_md += [f"<!-- CONTENT_ID: {cid} -->","",articles[cid].strip(),"","---",""]
    article_text="\n".join(article_md)+"\n"
    for cid in CONTENT_IDS:
        if f"CONTENT_ID: {cid}" not in article_text:
            raise RuntimeError(f"article marker missing {cid}")
    if article_text.count("### 来源与证据")!=6:
        raise RuntimeError("source appendices missing")
    if article_text.count("### 边界")!=6:
        raise RuntimeError("article boundaries missing")
    if article_text.count("[图：")<6:
        raise RuntimeError("figure markers missing")
    (OUT/"WECHAT_DEEP_ARTICLES_ZH.md").write_text(article_text)

    # PandaAI.
    templates=panda_templates(content,ready)
    if len(templates)!=6:
        raise RuntimeError("PandaAI template count")
    (OUT/"PANDAAI_EXPLANATION_TEMPLATES.json").write_text(
        json.dumps({"module":"FED-CYCLE-PLATFORM-NATIVE-PRODUCTION-PACK-028","templates":templates},
                   indent=2,ensure_ascii=False)+"\n"
    )

    # Index.
    idx=[]
    for cid in CONTENT_IDS:
        c=content_row(content,cid)
        visual=ready.loc[ready["content_id"]==cid,"canonical_visual_keys"].iloc[0]
        idx.extend([
            {"content_id":cid,"platform":"DOUYIN_TIKTOK","artifact":"DOUYIN_TIKTOK_SHOTLISTS_ZH.csv|DOUYIN_TIKTOK_CAPTIONS_ZH.md","claim_ids":c["claim_ids"],"figure_keys":visual,"freshness_rule":c["freshness_rule"],"publication_status":"PRODUCTION_READY_NOT_PUBLISHED"},
            {"content_id":cid,"platform":"XIAOHONGSHU","artifact":"XIAOHONGSHU_CAROUSELS_ZH.csv|XIAOHONGSHU_CAPTIONS_ZH.md","claim_ids":c["claim_ids"],"figure_keys":visual,"freshness_rule":c["freshness_rule"],"publication_status":"PRODUCTION_READY_NOT_PUBLISHED"},
            {"content_id":cid,"platform":"WECHAT_LONGFORM","artifact":"WECHAT_DEEP_ARTICLES_ZH.md","claim_ids":c["claim_ids"],"figure_keys":visual,"freshness_rule":c["freshness_rule"],"publication_status":"PRODUCTION_READY_NOT_PUBLISHED"},
            {"content_id":cid,"platform":"PANDAAI","artifact":"PANDAAI_EXPLANATION_TEMPLATES.json","claim_ids":c["claim_ids"],"figure_keys":visual,"freshness_rule":c["freshness_rule"],"publication_status":"PRODUCTION_READY_NOT_DEPLOYED"},
        ])
    idxdf=pd.DataFrame(idx)
    if len(idxdf)!=24: raise RuntimeError("platform index rows")
    idxdf.to_csv(OUT/"PLATFORM_NATIVE_INDEX.csv",index=False)

    # Safety/content-boundary lexical audit across publishable copy.
    publish_text="\n".join([
        "\n".join(shots["voiceover_zh"].astype(str)),
        "\n".join(car["headline_zh"].astype(str)),
        "\n".join(car["body_zh"].astype(str)),
        article_text,
        (OUT/"DOUYIN_TIKTOK_CAPTIONS_ZH.md").read_text(),
        (OUT/"XIAOHONGSHU_CAPTIONS_ZH.md").read_text(),
    ])
    prohibited=["必涨","必跌","买入","卖出","最佳资产","最像当前","稳赢"]
    leaks=[x for x in prohibited if x in publish_text]
    if leaks: raise RuntimeError(f"prohibited publishing language: {leaks}")

    # CNT-04 freshness.
    if content_row(content,CONTENT_IDS[3])["freshness_rule"]!="REVERIFY_BEFORE_CURRENT_USE":
        raise RuntimeError("CNT-04 freshness lost")

    report=[
        "# FED-CYCLE-PLATFORM-NATIVE-PRODUCTION-PACK-028 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED PLATFORM-NATIVE PRODUCTION COPY / 6 PACKAGES / NOT PUBLISHED / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "- Douyin/TikTok shot plans: 6",
        "- total short-video shots: 42",
        "- final MP4 files rendered: 0",
        "- Xiaohongshu carousels: 6",
        "- total carousel cards: 42",
        "- full WeChat/deep-article drafts: 6",
        "- PandaAI explanation templates: 6",
        "- platform-native index rows: 24",
        "",
        "All evidence values come from 026/022B canonical claims; historical event facts remain 022A sourced. No new empirical estimation is performed.",
        "",
        "028 makes editorial production operational but does not publish posts, render final video files or provide investment recommendations.",
    ]
    (OUT/"FED_CYCLE_PLATFORM_NATIVE_PRODUCTION_PACK_028_REPORT.md").write_text("\n".join(report)+"\n")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-PLATFORM-NATIVE-PRODUCTION-PACK-028",
        "upstream_qc":{"022B":q022b["qc_gate"],"024":q024["qc_gate"],"026":q026["qc_gate"],"027":q027["qc_gate"]},
        "content_packages":6,
        "douyin_tiktok_plans":int(shots["content_id"].nunique()),
        "douyin_tiktok_shot_rows":int(len(shots)),
        "shots_per_package":{cid:int(len(g)) for cid,g in shots.groupby("content_id")},
        "nonoverlap_monotonic_shots":True,
        "boundary_last_shot_packages":6,
        "final_mp4_rendered":False,
        "xiaohongshu_carousels":int(car["content_id"].nunique()),
        "xiaohongshu_card_rows":int(len(car)),
        "carousel_cover_rule_pass":True,
        "carousel_source_boundary_rule_pass":True,
        "wechat_full_articles":6,
        "wechat_figure_markers_present":True,
        "wechat_source_appendices":6,
        "wechat_boundary_sections":6,
        "pandaai_templates":len(templates),
        "platform_index_rows":int(len(idxdf)),
        "all_claim_refs_exist":True,
        "all_rendered_figure_refs_valid":True,
        "cnt04_reverify_before_current_use":True,
        "numeric_source_mode":"026_OR_022B_CANONICAL_ONLY",
        "prohibited_language_leaks":[],
        "political_evaluation_outputs":0,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
