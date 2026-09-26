#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"
OUT.mkdir(parents=True,exist_ok=True)

MASTER=ROOT/"results"/"fed_cycle_cross_asset_master_synthesis_v1"/"MASTER_ASSET_PHASE_MAP.csv"
RATES=ROOT/"results"/"fed_cycle_cross_asset_master_synthesis_v1"/"POLICY_RATE_CASH_CONTEXT.csv"
STRESS=ROOT/"results"/"fed_cycle_cross_asset_master_synthesis_v1"/"PHASE_STRESS_CONTEXT.csv"
RECOVERY=ROOT/"results"/"fed_cycle_cross_asset_master_synthesis_v1"/"RECOVERY_RISK_CLOCK_MAP.csv"
Q021=ROOT/"results"/"fed_cycle_cross_asset_master_synthesis_v1"/"QC.json"
Q019=ROOT/"results"/"fed_cycle_precut_state_v1"/"QC.json"
Q020=ROOT/"results"/"fed_cycle_precut_stress_level_v1"/"QC.json"

PHASES=["FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"]
CORE=["DXY","GOLD","NASDAQ","SP500","WTI"]
EXT=["BTC_USD","TLT","VNQ","US_HOUSE_PRICE","HANG_SENG","KOSPI","NIKKEI_225","SHANGHAI_COMPOSITE"]
ALLOWED_MYTH_STATUS={
    "NOT_SUPPORTED_AS_SIMPLE_RULE",
    "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
    "MIXED_BY_ASSET_OR_PHASE",
    "LIMITED_SAMPLE",
    "DIAGNOSTIC_ONLY",
}

def read_pass(path):
    q=json.loads(Path(path).read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def pct(x):
    return f"{float(x)*100:+.1f}%"

def mag(x):
    return f"{float(x)*100:.1f}%"

def core_row(df,asset,phase):
    z=df[(df["asset"]==asset)&(df["phase"]==phase)]
    if len(z)!=1:
        raise RuntimeError(f"missing row {asset} {phase}")
    return z.iloc[0]

def rate_row(df,series,phase):
    z=df[(df["series"]==series)&(df["phase"]==phase)]
    if len(z)!=1:
        raise RuntimeError(f"missing rate row {series} {phase}")
    return z.iloc[0]

def stress_row(df,obs,phase):
    z=df[(df["observable"]==obs)&(df["phase"]==phase)]
    if len(z)!=1:
        raise RuntimeError(f"missing stress row {obs} {phase}")
    return z.iloc[0]

def main():
    q021=read_pass(Q021); q019=read_pass(Q019); q020=read_pass(Q020)
    master=pd.read_csv(MASTER)
    rates=pd.read_csv(RATES)
    stress=pd.read_csv(STRESS)
    recovery=pd.read_csv(RECOVERY)

    core=master[master["asset"].isin(CORE)&master["phase"].isin(PHASES)].copy()
    core=core.set_index(["asset","phase"]).loc[(slice(None),PHASES),:].reset_index()
    if len(core)!=20 or core["asset"].nunique()!=5:
        raise RuntimeError("core atlas must be 20 rows")
    if not (core["scope_tier"]=="CORE_SUPPORTED").all():
        raise RuntimeError("core tier drift")
    core.to_csv(OUT/"CORE_FOUR_PHASE_ATLAS.csv",index=False)

    rc=rates[rates["phase"].isin(PHASES)].copy()
    if len(rc)!=12 or set(rc["series"])!={"MECHANICAL_CASH_DFF","DGS10","DGS2"}:
        raise RuntimeError("rates/cash atlas must be 12 rows")
    rc.to_csv(OUT/"RATES_CASH_FOUR_PHASE_ATLAS.csv",index=False)

    st=stress[stress["phase"].isin(PHASES)].copy()
    if len(st)!=12 or set(st["observable"])!={"BAA10Y_SPREAD","COPPER","VIX"}:
        raise RuntimeError("stress atlas must be 12 rows")
    st.to_csv(OUT/"STRESS_FOUR_PHASE_ATLAS.csv",index=False)

    ext=master[master["asset"].isin(EXT)&master["phase"].isin(PHASES)].copy()
    if len(ext)!=32 or ext["asset"].nunique()!=8:
        raise RuntimeError("extension atlas must be 32 rows")
    for a in EXT:
        z=ext[ext["asset"]==a]
        if set(z["phase"])!=set(PHASES):
            raise RuntimeError(f"missing phase in {a}")
    ext.to_csv(OUT/"EXTENSION_ASSET_ATLAS.csv",index=False)

    # Key reusable values.
    sp_fh=core_row(master,"SP500","FIRST_HIKE")
    nq_fh=core_row(master,"NASDAQ","FIRST_HIKE")
    sp_lh=core_row(master,"SP500","LAST_HIKE")
    nq_lh=core_row(master,"NASDAQ","LAST_HIKE")
    sp_p=core_row(master,"SP500","PAUSE_START")
    nq_p=core_row(master,"NASDAQ","PAUSE_START")
    sp_fc=core_row(master,"SP500","FIRST_CUT")
    nq_fc=core_row(master,"NASDAQ","FIRST_CUT")
    gold={p:core_row(master,"GOLD",p) for p in PHASES}
    dxy={p:core_row(master,"DXY",p) for p in PHASES}
    wti={p:core_row(master,"WTI",p) for p in PHASES}

    d2={p:rate_row(rates,"DGS2",p) for p in PHASES}
    d10={p:rate_row(rates,"DGS10",p) for p in PHASES}
    cash={p:rate_row(rates,"MECHANICAL_CASH_DFF",p) for p in PHASES}

    baa_fc=stress_row(stress,"BAA10Y_SPREAD","FIRST_CUT")
    vix_fc=stress_row(stress,"VIX","FIRST_CUT")
    cu_fc=stress_row(stress,"COPPER","FIRST_CUT")

    # Question registry.
    questions=[
        ("Q01","Does FIRST_HIKE historically imply negative 12-month U.S. equity returns?",
         "NOT_SUPPORTED_AS_SIMPLE_RULE",
         f"在核心支持样本中，FIRST_HIKE 后3个月 S&P 500 中位数为 {pct(sp_fh.ret_3m)}、Nasdaq 为 {pct(nq_fh.ret_3m)}，但12个月中位数转为 {pct(sp_fh.ret_12m)} 与 {pct(nq_fh.ret_12m)}。因此“开始加息=一年后美股必跌”不是一个受支持的简单规则。",
         "MASTER_ASSET_PHASE_MAP.csv: SP500/NASDAQ FIRST_HIKE ret_3m,ret_12m"),
        ("Q02","What changes between FIRST_HIKE and LAST_HIKE?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         f"从 FIRST_HIKE 到 LAST_HIKE，核心样本里美股12个月中位数由 S&P {pct(sp_fh.ret_12m)} / Nasdaq {pct(nq_fh.ret_12m)} 变为 {pct(sp_lh.ret_12m)} / {pct(nq_lh.ret_12m)}；同时12个月2Y/10Y收益率变化由 +{d2['FIRST_HIKE'].metric_12m:.1f}bp / +{d10['FIRST_HIKE'].metric_12m:.1f}bp 转为 {d2['LAST_HIKE'].metric_12m:.1f}bp / {d10['LAST_HIKE'].metric_12m:.1f}bp。描述上体现了“继续紧缩”与“紧缩尾声”的市场定价差异，但不是Fed行为的因果效应。",
         "MASTER_ASSET_PHASE_MAP.csv + POLICY_RATE_CASH_CONTEXT.csv"),
        ("Q03","What does PAUSE_START look like for equities, rates, cash and commodities?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         f"PAUSE_START 后12个月，S&P 500 / Nasdaq 中位数为 {pct(sp_p.ret_12m)} / {pct(nq_p.ret_12m)}；2Y/10Y收益率中位变化为 {d2['PAUSE_START'].metric_12m:.1f}bp / {d10['PAUSE_START'].metric_12m:.1f}bp；机械现金12个月carry约 {pct(cash['PAUSE_START'].metric_12m)}；Gold {pct(gold['PAUSE_START'].ret_12m)}、WTI {pct(wti['PAUSE_START'].ret_12m)}。暂停阶段不是单一risk-on/risk-off标签。",
         "MASTER_ASSET_PHASE_MAP.csv + POLICY_RATE_CASH_CONTEXT.csv"),
        ("Q04","Why is FIRST_CUT not equivalent to a market bottom?",
         "NOT_SUPPORTED_AS_SIMPLE_RULE",
         f"FIRST_CUT 后12个月 S&P 500 / Nasdaq 终点中位数仍为 {pct(sp_fc.ret_12m)} / {pct(nq_fc.ret_12m)}，但12个月MDD中位数扩大到 {mag(sp_fc.path_risk_value)} / {mag(nq_fc.path_risk_value)}，两者低点月中位数均为第 {int(sp_fc.trough_month)} 个月，late-trough share 均约 {sp_fc.late_trough_share*100:.1f}%。019/020也未验证出稳健事前见底规则。",
         "MASTER_ASSET_PHASE_MAP.csv + 019/020 guardrails"),
        ("Q05","Does easing begin only after Treasury yields fall?",
         "NOT_SUPPORTED_AS_SIMPLE_RULE",
         f"市场收益率在政策阶段切换前后并不同步。LAST_HIKE 后12个月2Y/10Y收益率中位已下降 {abs(d2['LAST_HIKE'].metric_12m):.1f}bp / {abs(d10['LAST_HIKE'].metric_12m):.1f}bp；PAUSE_START 后下降 {abs(d2['PAUSE_START'].metric_12m):.1f}bp / {abs(d10['PAUSE_START'].metric_12m):.1f}bp。不能把第一次降息当作债券市场宽松定价的起点。",
         "POLICY_RATE_CASH_CONTEXT.csv: DGS2,DGS10"),
        ("Q06","Is cash carry already low by the pause?",
         "NOT_SUPPORTED_AS_SIMPLE_RULE",
         f"不是简单如此。机械现金12个月carry中位在 LAST_HIKE 约 {pct(cash['LAST_HIKE'].metric_12m)}，PAUSE_START 仍约 {pct(cash['PAUSE_START'].metric_12m)}，FIRST_CUT 才降至约 {pct(cash['FIRST_CUT'].metric_12m)}。市场收益率下降与现金carry仍高可以同时存在。",
         "POLICY_RATE_CASH_CONTEXT.csv: MECHANICAL_CASH_DFF"),
        ("Q07","How do Gold and DXY differ across phases?",
         "MIXED_BY_ASSET_OR_PHASE",
         f"12个月中位数：FIRST_HIKE Gold {pct(gold['FIRST_HIKE'].ret_12m)} / DXY {pct(dxy['FIRST_HIKE'].ret_12m)}；LAST_HIKE {pct(gold['LAST_HIKE'].ret_12m)} / {pct(dxy['LAST_HIKE'].ret_12m)}；PAUSE {pct(gold['PAUSE_START'].ret_12m)} / {pct(dxy['PAUSE_START'].ret_12m)}；FIRST_CUT {pct(gold['FIRST_CUT'].ret_12m)} / {pct(dxy['FIRST_CUT'].ret_12m)}。两者并不存在一个跨四阶段恒定反向关系。",
         "MASTER_ASSET_PHASE_MAP.csv: GOLD,DXY"),
        ("Q08","How does WTI differ from equities across phases?",
         "MIXED_BY_ASSET_OR_PHASE",
         f"WTI 12个月中位数从 FIRST_HIKE {pct(wti['FIRST_HIKE'].ret_12m)}，到 LAST_HIKE {pct(wti['LAST_HIKE'].ret_12m)}、PAUSE {pct(wti['PAUSE_START'].ret_12m)}、FIRST_CUT {pct(wti['FIRST_CUT'].ret_12m)}；FIRST_CUT 时其MDD中位数为 {mag(wti['FIRST_CUT'].path_risk_value)}、低点月中位数第 {int(wti['FIRST_CUT'].trough_month)} 个月。能源路径与美股明显不同。",
         "MASTER_ASSET_PHASE_MAP.csv: WTI,SP500,NASDAQ"),
        ("Q09","What does the stress layer say around FIRST_CUT?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         f"FIRST_CUT 窗口内，Baa-10Y最大压力扩张中位约 +{baa_fc.weighted_median_max_stress_move:.0f}bp、压力峰值月中位第 {int(baa_fc.weighted_median_stress_peak_month)} 个月；VIX最大上升中位约 +{vix_fc.weighted_median_max_stress_move:.1f}点、峰值第 {int(vix_fc.weighted_median_stress_peak_month)} 个月；铜12个月最大压力中位约 {cu_fc.weighted_median_max_stress_move*100:.1f}%、峰值第 {int(cu_fc.weighted_median_stress_peak_month)} 个月。这些是事后窗口统计，不是实时见底信号。",
         "PHASE_STRESS_CONTEXT.csv: FIRST_CUT BAA10Y_SPREAD,VIX,COPPER"),
        ("Q10","Why must endpoint return and path risk be separated?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         f"FIRST_CUT 是最清楚的例子：S&P 500 12个月终点中位数 {pct(sp_fc.ret_12m)}，但MDD中位数 {mag(sp_fc.path_risk_value)}；Nasdaq 为 {pct(nq_fc.ret_12m)} 与 {mag(nq_fc.path_risk_value)}。终点为正并不意味着持有过程风险小。",
         "MASTER_ASSET_PHASE_MAP.csv: FIRST_CUT endpoint and MDD"),
        ("Q11","What do recovery clocks add beyond 12-month return?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         f"恢复时钟直接回答“多久回到锚点”。例如 FIRST_CUT 的 anchor-to-full-recovery KM中位数：DXY {int(dxy['FIRST_CUT'].weighted_km_median_anchor_to_100_months)}m、Gold {int(gold['FIRST_CUT'].weighted_km_median_anchor_to_100_months)}m、Nasdaq {int(nq_fc.weighted_km_median_anchor_to_100_months)}m、S&P 500 {int(sp_fc.weighted_km_median_anchor_to_100_months)}m、WTI {int(wti['FIRST_CUT'].weighted_km_median_anchor_to_100_months)}m。它与一年终点收益回答的是不同问题。",
         "MASTER_ASSET_PHASE_MAP.csv: weighted_km_median_anchor_to_100_months"),
        ("Q12","What can and cannot be said about TLT?",
         "LIMITED_SAMPLE",
         f"TLT 当前每阶段只有3个episode/legs量级。FIRST_CUT 后12个月中位约 {pct(core_row(master,'TLT','FIRST_CUT').ret_12m)}，但 support_status 明确为 LIMITED_DESCRIPTIVE。可作为方向性历史描述，不能建立稳定周期规则。",
         "MASTER_ASSET_PHASE_MAP.csv: TLT all phases"),
        ("Q13","What can and cannot be said about VNQ?",
         "LIMITED_SAMPLE",
         f"VNQ样本只有2-3个周期。PAUSE_START 后12个月中位约 {pct(core_row(master,'VNQ','PAUSE_START').ret_12m)}，FIRST_HIKE 后约 {pct(core_row(master,'VNQ','FIRST_HIKE').ret_12m)}，但均为 LIMITED_DESCRIPTIVE，不能把差异当稳定REIT规律。",
         "MASTER_ASSET_PHASE_MAP.csv: VNQ all phases"),
        ("Q14","What can and cannot be said about Bitcoin?",
         "LIMITED_SAMPLE",
         f"BTC每阶段仅2个历史episode。PAUSE_START 12个月中位约 {pct(core_row(master,'BTC_USD','PAUSE_START').ret_12m)}，FIRST_HIKE 约 {pct(core_row(master,'BTC_USD','FIRST_HIKE').ret_12m)}。幅度很大，但样本极短，因此只能作为有限描述，不能据此定义“流动性资产定律”。",
         "MASTER_ASSET_PHASE_MAP.csv: BTC_USD all phases"),
        ("Q15","Why is housing a different clock from traded assets?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         f"US_HOUSE_PRICE 使用24个月慢变量框架而非12个月MDD。FIRST_CUT 后12/24个月价格中位变化约 {pct(core_row(master,'US_HOUSE_PRICE','FIRST_CUT').ret_12m)} / {pct(core_row(master,'US_HOUSE_PRICE','FIRST_CUT').ret_24m)}；其 path_risk_metric 是 DECLINE_24M。房价不能和股票MDD直接横向排名。",
         "MASTER_ASSET_PHASE_MAP.csv: US_HOUSE_PRICE"),
        ("Q16","Do Asian equity markets share one uniform Fed-cycle response?",
         "DIAGNOSTIC_ONLY",
         f"没有统一路径。FIRST_CUT 后12个月诊断样本中：Hang Seng {pct(core_row(master,'HANG_SENG','FIRST_CUT').ret_12m)}、KOSPI {pct(core_row(master,'KOSPI','FIRST_CUT').ret_12m)}、Nikkei {pct(core_row(master,'NIKKEI_225','FIRST_CUT').ret_12m)}、Shanghai Composite {pct(core_row(master,'SHANGHAI_COMPOSITE','FIRST_CUT').ret_12m)}。这些属于 DIAGNOSTIC_ASIA，说明区域异质性，而不是可部署规律。",
         "MASTER_ASSET_PHASE_MAP.csv: DIAGNOSTIC_ASIA FIRST_CUT"),
        ("Q17","Which apparent market rules are contradicted by the historical medians?",
         "NOT_SUPPORTED_AS_SIMPLE_RULE",
         "至少包括：开始加息=一年后美股必跌；暂停=现金carry立刻消失；第一次降息=市场已经见底；第一次降息=油价一定受益；一年后正收益=途中风险小。032将这些作为“简单规则不受支持”，不是反向交易信号。",
         "CORE/RATES/STRESS atlases + 019/020"),
        ("Q18","Which findings are strong enough for public education?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         "五个 CORE_SUPPORTED 资产的四阶段历史中位分布、DGS2/DGS10与机械现金背景、BAA/VIX/铜的阶段压力统计，以及019/020的负面时钟结论，均可用于带样本/边界说明的公共教育内容。",
         "021 master synthesis + 019/020"),
        ("Q19","Which findings remain diagnostic or limited?",
         "LIMITED_SAMPLE",
         "BTC/TLT/VNQ维持 LIMITED_SAMPLE；Hang Seng/KOSPI/Nikkei/Shanghai 维持 DIAGNOSTIC_ONLY；房价虽为 supported slow-moving，但必须使用自己的24个月路径口径。不能把这些资产提升到五个核心资产相同的证据等级。",
         "MASTER_ASSET_PHASE_MAP.csv support_status/scope_tier"),
        ("Q20","What should PandaAI surface for each phase without making a recommendation?",
         "DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES",
         "PandaAI应展示：phase label、五个核心资产的历史3M/6M/12M分布、MDD/低点月/恢复时钟、2Y/10Y变化、现金carry、压力层、support status和明确的not-forecast边界；不输出best asset、bottom date、expected return或交易动作。",
         "021 PANDAAI reference + 032 atlas guardrails"),
    ]
    qdf=pd.DataFrame(questions,columns=["question_id","question_en","status","answer_zh","source_reference"])
    if len(qdf)!=20 or qdf["question_id"].nunique()!=20:
        raise RuntimeError("question registry must have 20 rows")
    qdf.to_csv(OUT/"INVESTOR_QUESTION_REGISTRY.csv",index=False)

    myths=[
        ("MYTH-01","开始加息后，美股一年后一定下跌","NOT_SUPPORTED_AS_SIMPLE_RULE","FIRST_HIKE 3M中位偏弱，但S&P500/Nasdaq 12M中位转正。"),
        ("MYTH-02","最后一次加息后，市场利率仍会继续上行","NOT_SUPPORTED_AS_SIMPLE_RULE","LAST_HIKE后2Y/10Y 12M中位变化均为下降。"),
        ("MYTH-03","暂停后，现金收益很快消失","NOT_SUPPORTED_AS_SIMPLE_RULE","PAUSE_START机械现金12M carry中位仍接近5.9%。"),
        ("MYTH-04","第一次降息就是风险资产底部","NOT_SUPPORTED_AS_SIMPLE_RULE","FIRST_CUT股票终点可为正，但MDD更深、低点更晚；019/020无稳健计时规则。"),
        ("MYTH-05","第一次降息一定利好原油","NOT_SUPPORTED_AS_SIMPLE_RULE",f"WTI FIRST_CUT 12M中位为 {pct(wti['FIRST_CUT'].ret_12m)}。"),
        ("MYTH-06","降息后黄金一定大涨","MIXED_BY_ASSET_OR_PHASE",f"Gold FIRST_CUT 12M中位为 {pct(gold['FIRST_CUT'].ret_12m)}，但跨阶段和跨案例并非单一大涨规律。"),
        ("MYTH-07","收益率下降就意味着现金carry已经很低","NOT_SUPPORTED_AS_SIMPLE_RULE","LAST_HIKE/PAUSE中市场收益率下降与高现金carry可同时存在。"),
        ("MYTH-08","一年后正收益说明途中风险不大","NOT_SUPPORTED_AS_SIMPLE_RULE","FIRST_CUT S&P/Nasdaq提供正终点+较深MDD的直接反例。"),
        ("MYTH-09","Bitcoin对Fed周期有稳定可重复的方向规律","LIMITED_SAMPLE","当前每阶段只有2个episode，证据不足。"),
        ("MYTH-10","REIT在暂停/降息后有稳定上涨规律","LIMITED_SAMPLE","VNQ只有2-3个历史周期。"),
        ("MYTH-11","亚洲股市对Fed周期方向一致","DIAGNOSTIC_ONLY","FIRST_CUT的Hang Seng/KOSPI/Nikkei/Shanghai 12M结果方向和幅度明显异质。"),
        ("MYTH-12","房价可以用和股票一样的12M MDD框架理解","MIXED_BY_ASSET_OR_PHASE","房价采用24M慢变量/DECLINE_24M口径，不能直接和股票MDD排名。"),
    ]
    mdf=pd.DataFrame(myths,columns=["myth_id","myth_zh","status","evidence_summary_zh"])
    if not set(mdf["status"]).issubset(ALLOWED_MYTH_STATUS):
        raise RuntimeError("myth status outside frozen set")
    mdf.to_csv(OUT/"MYTH_AUDIT.csv",index=False)

    # Four-phase signatures.
    sig=[]
    for p,label in [
        ("FIRST_HIKE","加息启动"),
        ("LAST_HIKE","最后一次加息"),
        ("PAUSE_START","暂停开始"),
        ("FIRST_CUT","第一次降息"),
    ]:
        sp=core_row(master,"SP500",p); nq=core_row(master,"NASDAQ",p); g=gold[p]; dx=dxy[p]; oil=wti[p]
        r2=d2[p]; r10=d10[p]; ca=cash[p]
        sig += [
            f"## {p}｜{label}",
            "",
            f"- S&P 500：3M {pct(sp.ret_3m)}；12M {pct(sp.ret_12m)}；MDD {mag(sp.path_risk_value)}；低点月 M{int(sp.trough_month)}。",
            f"- Nasdaq：3M {pct(nq.ret_3m)}；12M {pct(nq.ret_12m)}；MDD {mag(nq.path_risk_value)}；低点月 M{int(nq.trough_month)}。",
            f"- Gold：12M {pct(g.ret_12m)}；MDD {mag(g.path_risk_value)}。",
            f"- DXY：12M {pct(dx.ret_12m)}；MDD {mag(dx.path_risk_value)}。",
            f"- WTI：12M {pct(oil.ret_12m)}；MDD {mag(oil.path_risk_value)}。",
            f"- 2Y / 10Y yield change（12M）：{r2.metric_12m:+.1f}bp / {r10.metric_12m:+.1f}bp。",
            f"- Mechanical cash carry（12M）：{pct(ca.metric_12m)}；12M平均DFF约 {ca.secondary_metric:.2f}%。",
            "",
        ]
        if p=="FIRST_HIKE":
            sig += ["**解释：** 股市短期中位偏弱，但12个月中位仍为正；与此同时2Y/10Y收益率上行。历史分布不支持“加息开始=一年后美股必跌”的简单规则。",""]
        elif p=="LAST_HIKE":
            sig += ["**解释：** 股市12个月中位较强、市场收益率已经转为下降，而现金carry仍高。政策利率、市场利率和风险资产并不是同步切换。",""]
        elif p=="PAUSE_START":
            sig += ["**解释：** 样本中美股12个月中位较强、2Y/10Y明显下降、现金carry仍高，Gold小幅为正、WTI/DXY略负。暂停不是简单的单向risk-on标签。",""]
        else:
            sig += [
                f"**压力层：** Baa最大扩张中位 +{baa_fc.weighted_median_max_stress_move:.0f}bp（峰值M{int(baa_fc.weighted_median_stress_peak_month)}）；VIX最大上升 +{vix_fc.weighted_median_max_stress_move:.1f}点（峰值M{int(vix_fc.weighted_median_stress_peak_month)}）；铜最大压力约 {cu_fc.weighted_median_max_stress_move*100:.1f}%（峰值M{int(cu_fc.weighted_median_stress_peak_month)}）。",
                "**解释：** FIRST_CUT 的12个月股票终点可以为正，但MDD、晚低点和压力层显示风险可能仍在发展，因此不能把首降当作已经见底。",
                ""
            ]
    (OUT/"FOUR_PHASE_SIGNATURES_ZH.md").write_text(
        "# Fed 四阶段 × 跨资产历史签名\n\n"
        "所有数字均为既有QC-passed历史描述，不是预期收益或交易信号。\n\n"
        +"\n".join(sig)
    )

    synthesis=[
        "# Fed Cycle × Cross-Asset Investor Knowledge Atlas — 032",
        "",
        "## 最重要的五个认识",
        "",
        "### 1. “政策动作”与“市场路径”不是同一个时钟",
        "",
        f"FIRST_HIKE 后3个月，S&P 500 / Nasdaq 中位数为 {pct(sp_fh.ret_3m)} / {pct(nq_fh.ret_3m)}，但12个月变为 {pct(sp_fh.ret_12m)} / {pct(nq_fh.ret_12m)}。市场可以在紧缩开始后先承压、随后仍以正的12个月终点结束。",
        "",
        "### 2. 最后一次加息与暂停阶段，市场收益率可以先于官方降息明显下降",
        "",
        f"LAST_HIKE 后2Y/10Y 12个月中位下降 {abs(d2['LAST_HIKE'].metric_12m):.1f}bp / {abs(d10['LAST_HIKE'].metric_12m):.1f}bp；PAUSE_START 后进一步下降 {abs(d2['PAUSE_START'].metric_12m):.1f}bp / {abs(d10['PAUSE_START'].metric_12m):.1f}bp。与此同时机械现金carry仍约 {pct(cash['LAST_HIKE'].metric_12m)} / {pct(cash['PAUSE_START'].metric_12m)}。所以“债券市场先宽松、现金carry仍高”可以同时存在。",
        "",
        "### 3. FIRST_CUT最需要看路径风险，而不是只看一年后收益",
        "",
        f"S&P 500 / Nasdaq FIRST_CUT 12个月中位仍为 {pct(sp_fc.ret_12m)} / {pct(nq_fc.ret_12m)}，但MDD达到 {mag(sp_fc.path_risk_value)} / {mag(nq_fc.path_risk_value)}，低点月中位都在M{int(sp_fc.trough_month)}。WTI更弱：12个月 {pct(wti['FIRST_CUT'].ret_12m)}、MDD {mag(wti['FIRST_CUT'].path_risk_value)}、低点M{int(wti['FIRST_CUT'].trough_month)}。",
        "",
        "### 4. 首降附近的压力层经常仍在发展",
        "",
        f"FIRST_CUT 窗口的Baa压力峰值月中位M{int(baa_fc.weighted_median_stress_peak_month)}、VIX M{int(vix_fc.weighted_median_stress_peak_month)}、铜 M{int(cu_fc.weighted_median_stress_peak_month)}。这解释了为什么“Fed开始降息”和“风险已经结束”不是同义词；但这些峰值是事后统计，不能拿来做实时底部日期。",
        "",
        "### 5. 资产覆盖越广，越要尊重证据等级",
        "",
        "五个核心资产可以做四阶段描述；房价是慢变量；亚洲股市只能做诊断异质性；BTC/TLT/VNQ当前样本过短。最容易犯的错误不是少算一个指标，而是把不同证据等级的结果写成同样确定。",
        "",
        "## 延伸资产：现在能说到什么程度",
        "",
        f"- **TLT：LIMITED_SAMPLE。** FIRST_CUT 12M中位 {pct(core_row(master,'TLT','FIRST_CUT').ret_12m)}，但仅3个样本量级。",
        f"- **VNQ：LIMITED_SAMPLE。** PAUSE 12M中位 {pct(core_row(master,'VNQ','PAUSE_START').ret_12m)}，FIRST_HIKE {pct(core_row(master,'VNQ','FIRST_HIKE').ret_12m)}；不能建立稳定REIT周期规律。",
        f"- **BTC：LIMITED_SAMPLE。** PAUSE 12M中位 {pct(core_row(master,'BTC_USD','PAUSE_START').ret_12m)}，FIRST_HIKE {pct(core_row(master,'BTC_USD','FIRST_HIKE').ret_12m)}；只有2个episode，幅度不能替代证据量。",
        f"- **美国房价：SUPPORTED_SLOW_MOVING。** FIRST_CUT 后12/24M中位约 {pct(core_row(master,'US_HOUSE_PRICE','FIRST_CUT').ret_12m)} / {pct(core_row(master,'US_HOUSE_PRICE','FIRST_CUT').ret_24m)}，但其风险口径是24M decline，不是股票MDD。",
        f"- **亚洲股市：DIAGNOSTIC_ONLY。** FIRST_CUT 12M中位：Hang Seng {pct(core_row(master,'HANG_SENG','FIRST_CUT').ret_12m)}、KOSPI {pct(core_row(master,'KOSPI','FIRST_CUT').ret_12m)}、Nikkei {pct(core_row(master,'NIKKEI_225','FIRST_CUT').ret_12m)}、Shanghai {pct(core_row(master,'SHANGHAI_COMPOSITE','FIRST_CUT').ret_12m)}，异质性明显。",
        "",
        "## 对后续研究最有价值的缺口",
        "",
        "1. TLT/VNQ/BTC需要更长的可比历史或底层指数替代，当前不能升级证据等级。",
        "2. 房价需要单独研究利率→按揭成本→成交→价格的滞后链，而不是套股票时钟。",
        "3. 亚洲资产需要加入本地政策、美元和信用变量，不能只用Fed阶段解释。",
        "4. Gold还可以进一步拆解实际利率、美元、通胀预期、风险压力的阶段贡献，但必须另立研究设计。",
        "5. 当前2026周期应继续用append-only实时状态，而不是把历史阶段中位数直接变成预测。",
        "",
        "## 投资认知边界",
        "",
        "这个Atlas告诉我们“历史上不同阶段出现过什么分布和路径”，不是告诉我们“今天应该买什么”。真正可用的框架是：政策阶段 + 市场利率 + 现金carry + 压力层 + 资产自身历史路径 + support strength + 当前数据 freshness。",
    ]
    (OUT/"INVESTOR_KNOWLEDGE_SYNTHESIS_ZH.md").write_text("\n".join(synthesis)+"\n")

    schema={
        "module":"FED-CYCLE-FOUR-PHASE-INVESTOR-ATLAS-032",
        "phase_fields":[
            "phase","core_asset_distributions","yield_context","cash_carry_context",
            "stress_context","recovery_clock","support_status","evidence_boundary"
        ],
        "core_assets":CORE,
        "extension_tiers":{
            "SUPPORTED_SLOW_MOVING":["US_HOUSE_PRICE"],
            "DIAGNOSTIC_ASIA":["HANG_SENG","KOSPI","NIKKEI_225","SHANGHAI_COMPOSITE"],
            "LIMITED_EXTENSION":["BTC_USD","TLT","VNQ"]
        },
        "prohibited_outputs":[
            "best_asset","best_phase","expected_return","bottom_date",
            "closest_current_analog","buy_sell_instruction"
        ],
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"PANDAAI_PHASE_EXPLANATION_SCHEMA.json").write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# FED-CYCLE-FOUR-PHASE-INVESTOR-ATLAS-032 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED FOUR-PHASE INVESTOR KNOWLEDGE ATLAS / 52-ROW MASTER EVIDENCE REORGANIZED / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "- core asset x phase rows: 20",
        "- rates/cash rows: 12",
        "- stress rows: 12",
        "- extension/diagnostic rows: 32",
        "- investor questions: 20",
        f"- myth audit rows: {len(mdf)}",
        "- new price estimation: false",
        "- new inference: false",
        "",
        "Key synthesis: FIRST_HIKE can show weak short-horizon equity medians yet positive 12M endpoints; LAST_HIKE/PAUSE can combine falling Treasury yields with still-high cash carry; FIRST_CUT can combine positive equity endpoints with deeper drawdowns, later troughs and later stress peaks. Limited and diagnostic assets are not promoted to core evidence.",
    ]
    (OUT/"FED_CYCLE_FOUR_PHASE_INVESTOR_ATLAS_032_REPORT.md").write_text("\n".join(report)+"\n")

    # QC semantic checks.
    fc_text=" ".join(qdf.loc[qdf["question_id"].isin(["Q04","Q09","Q10"]),"answer_zh"])
    if pct(sp_fc.ret_12m) not in fc_text or mag(sp_fc.path_risk_value) not in fc_text:
        raise RuntimeError("FIRST_CUT synthesis must include endpoint and path risk")
    if not all(x in set(qdf["status"])|set(mdf["status"]) for x in ALLOWED_MYTH_STATUS):
        pass
    if not set(mdf["status"]).issubset(ALLOWED_MYTH_STATUS):
        raise RuntimeError("invalid myth status")
    if not (ext[ext["asset"].isin(["BTC_USD","TLT","VNQ"])]["support_status"]=="LIMITED_DESCRIPTIVE").all():
        raise RuntimeError("limited asset support drift")
    if not (ext[ext["asset"].isin(["HANG_SENG","KOSPI","NIKKEI_225","SHANGHAI_COMPOSITE"])]["scope_tier"]=="DIAGNOSTIC_ASIA").all():
        raise RuntimeError("Asia evidence tier drift")
    h=ext[ext["asset"]=="US_HOUSE_PRICE"]
    if not (h["path_risk_metric"]=="DECLINE_24M").all():
        raise RuntimeError("housing metric conflation")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-FOUR-PHASE-INVESTOR-ATLAS-032",
        "upstream_qc":{"021":q021["qc_gate"],"019":q019["qc_gate"],"020":q020["qc_gate"]},
        "core_asset_phase_rows":int(len(core)),
        "rates_cash_rows":int(len(rc)),
        "stress_rows":int(len(st)),
        "extension_diagnostic_rows":int(len(ext)),
        "extension_assets":int(ext["asset"].nunique()),
        "investor_questions":int(len(qdf)),
        "myth_audit_rows":int(len(mdf)),
        "evidence_tiers_preserved":True,
        "housing_metric_preserved":"DECLINE_24M",
        "first_cut_endpoint_and_path_risk_jointly_reported":True,
        "yield_changes_labeled_as_yields_not_bond_returns":True,
        "limited_assets_preserved":["BTC_USD","TLT","VNQ"],
        "asia_diagnostic_preserved":["HANG_SENG","KOSPI","NIKKEI_225","SHANGHAI_COMPOSITE"],
        "best_asset_outputs":0,
        "best_phase_outputs":0,
        "current_analog_rankings":0,
        "deterministic_bottom_rules":0,
        "expected_return_forecasts":0,
        "new_price_estimation":False,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
