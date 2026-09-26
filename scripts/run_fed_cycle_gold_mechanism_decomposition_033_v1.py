#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_gold_mechanism_decomposition_033_v1"
OUT.mkdir(parents=True,exist_ok=True)

STATE_CON=ROOT/"results"/"fed_cycle_state_v1"/"STATE_CONTRASTS.csv"
STATE_LOO=ROOT/"results"/"fed_cycle_state_v1"/"STATE_LOO_STABILITY.csv"
USD_STATE=ROOT/"results"/"fed_cycle_state_v1"/"USD_STATE_CONTRASTS.csv"
Q001=ROOT/"results"/"fed_cycle_state_v1"/"QC.json"

PRIMARY=ROOT/"results"/"fed_cycle_state_panel_v2"/"PRIMARY_TESTS.csv"
SECONDARY=ROOT/"results"/"fed_cycle_state_panel_v2"/"SECONDARY_DIAGNOSTICS.csv"
USD_ROB=ROOT/"results"/"fed_cycle_state_panel_v2"/"USD_ROBUSTNESS_AUDIT.csv"
Q002=ROOT/"results"/"fed_cycle_state_panel_v2"/"QC.json"

MASTER=ROOT/"results"/"fed_cycle_cross_asset_master_synthesis_v1"/"MASTER_ASSET_PHASE_MAP.csv"
Q004=ROOT/"results"/"fed_cycle_phase_clock_v1"/"QC.json"
STRESS=ROOT/"results"/"fed_cycle_stress_trough_alignment_v1"/"SUPPORTED_TIMING_PAIRS.csv"
Q018=ROOT/"results"/"fed_cycle_stress_trough_alignment_v1"/"QC.json"
Q032=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"/"QC.json"
LIT=ROOT/"data"/"public"/"GOLD_MECHANISM_LITERATURE_REGISTRY_20260926.csv"

PHASES=["FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"]
ALLOWED_STATUS={
    "SUPPORTED_DESCRIPTIVE",
    "SECONDARY_DIAGNOSTIC",
    "INSUFFICIENT_SUPPORT",
    "NO_STABLE_ASSOCIATION",
    "LITERATURE_CONTEXT",
}

def read_pass(path):
    q=json.loads(Path(path).read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def pct(x): return f"{float(x)*100:+.1f}%"
def mag(x): return f"{float(x)*100:.1f}%"

def one(df, **kwargs):
    z=df.copy()
    for k,v in kwargs.items():
        z=z[z[k]==v]
    if len(z)!=1:
        raise RuntimeError(f"expected one row {kwargs}, got {len(z)}")
    return z.iloc[0]

def main():
    q001=read_pass(Q001); q002=read_pass(Q002); q004=read_pass(Q004); q018=read_pass(Q018); q032=read_pass(Q032)

    scon=pd.read_csv(STATE_CON)
    loo=pd.read_csv(STATE_LOO)
    usds=pd.read_csv(USD_STATE)
    pri=pd.read_csv(PRIMARY)
    sec=pd.read_csv(SECONDARY)
    usdrob=pd.read_csv(USD_ROB)
    master=pd.read_csv(MASTER)
    stress=pd.read_csv(STRESS)
    lit=pd.read_csv(LIT)

    # Gold phase profile.
    gphase=master[(master["asset"]=="GOLD")&(master["phase"].isin(PHASES))].copy()
    if len(gphase)!=4 or set(gphase["phase"])!=set(PHASES):
        raise RuntimeError("Gold phase profile must have four phases")
    gphase.to_csv(OUT/"GOLD_PHASE_PROFILE.csv",index=False)

    # Supported FIRST_HIKE event-state contrasts for primary Gold return, plus USD diagnostic.
    first_supported=scon[
        (scon["outcome"]=="gold_ret_12m")&
        (scon["status"]=="SUPPORTED_DESCRIPTIVE")&
        (scon["state_var"].isin(["INFLATION_LEVEL","INFLATION_DIRECTION","GROWTH_STATE","ENERGY_DIRECTION_STATE"]))
    ].copy()
    if len(first_supported)!=4:
        raise RuntimeError("expected four supported event-state contrasts")
    first_supported=first_supported.merge(
        loo[(loo["outcome"]=="gold_ret_12m")][["state_var","loo_sign_stable"]],
        on="state_var",how="left",validate="one_to_one"
    )
    usd_event=usds[usds["outcome"]=="gold_ret_12m"].copy()
    if len(usd_event)!=1:
        raise RuntimeError("USD event-state diagnostic missing")
    usd_event_out=pd.DataFrame([{
        "state_var":"USD_DIRECTION_DIAGNOSTIC",
        "state_a":usd_event.iloc[0]["state_a"],
        "state_b":usd_event.iloc[0]["state_b"],
        "outcome":"gold_ret_12m",
        "n_a":usd_event.iloc[0]["n_a"],
        "n_b":usd_event.iloc[0]["n_b"],
        "median_a":usd_event.iloc[0]["median_a"],
        "median_b":usd_event.iloc[0]["median_b"],
        "oriented_median_diff_a_minus_b":usd_event.iloc[0]["oriented_median_diff_a_minus_b"],
        "status":usd_event.iloc[0]["status"],
        "loo_sign_stable":usd_event.iloc[0]["loo_sign_stable"],
        "evidence_note":"USD bridge diagnostic; not primary state family."
    }])
    first_supported["evidence_note"]="Primary event-state contrast; current-vintage macro with timing caveats."
    first_out=pd.concat([first_supported,usd_event_out],ignore_index=True,sort=False)
    first_out.to_csv(OUT/"GOLD_FIRST_HIKE_STATE_CONTRASTS.csv",index=False)

    # Monthly secondary diagnostics of direct mechanism candidates.
    wanted=["USD_6M_RET","REAL_RATE_PROXY_PP","DFII10","NFCI","DGS10_LEVEL","CURVE_BP"]
    msec=sec[(sec["outcome"]=="GOLD_FWD_6M_RET") & sec["predictor"].isin(wanted)].copy()
    if len(msec)!=6:
        raise RuntimeError("secondary diagnostic family changed")
    msec.to_csv(OUT/"GOLD_MONTHLY_SECONDARY_DIAGNOSTICS.csv",index=False)

    # Gold stress timing.
    gstress=stress[(stress["asset"]=="GOLD") & stress["stress_observable"].isin(["BAA10Y_SPREAD","COPPER","VIX"])].copy()
    if len(gstress)!=3:
        raise RuntimeError("Gold stress timing must have three rows")
    gstress.to_csv(OUT/"GOLD_STRESS_TIMING_MAP.csv",index=False)

    # Frozen literature.
    if len(lit)!=5 or not (lit["status"]=="LITERATURE_CONTEXT").all():
        raise RuntimeError("literature registry drift")
    lit.to_csv(OUT/"GOLD_MECHANISM_LITERATURE_REGISTRY.csv",index=False)

    # Extract exact inputs.
    infl_level=one(first_supported,state_var="INFLATION_LEVEL")
    infl_dir=one(first_supported,state_var="INFLATION_DIRECTION")
    growth=one(first_supported,state_var="GROWTH_STATE")
    energy=one(first_supported,state_var="ENERGY_DIRECTION_STATE")
    usd_e=usd_event.iloc[0]

    usd_m=one(msec,predictor="USD_6M_RET")
    rrp=one(msec,predictor="REAL_RATE_PROXY_PP")
    dfii=one(msec,predictor="DFII10")
    nfci=one(msec,predictor="NFCI")
    dgs10=one(msec,predictor="DGS10_LEVEL")
    curve=one(msec,predictor="CURVE_BP")

    baa=one(gstress,stress_observable="BAA10Y_SPREAD")
    vix=one(gstress,stress_observable="VIX")
    copper=one(gstress,stress_observable="COPPER")

    # Evidence matrix.
    rows=[
        {
            "mechanism":"INFLATION_LEVEL","status":"SUPPORTED_DESCRIPTIVE",
            "repository_result":f"HIGH median Gold 12M {pct(infl_level.median_a)} vs LOW_OR_MODERATE {pct(infl_level.median_b)}; diff {pct(infl_level.oriented_median_diff_a_minus_b)}.",
            "sample_support":f"n={int(infl_level.n_a)} vs {int(infl_level.n_b)} FIRST_HIKE legs; LOO sign stable={bool(infl_level.loo_sign_stable)}",
            "interpretation":"Higher inflation level at FIRST_HIKE was associated with worse subsequent Gold in this sample; this contradicts a simple high-inflation-is-bullish rule.",
            "boundary":"Event-level descriptive association; macro values are current-vintage/release-lag aware, not strict ALFRED PIT."
        },
        {
            "mechanism":"INFLATION_DIRECTION","status":"SUPPORTED_DESCRIPTIVE",
            "repository_result":f"RISING median Gold 12M {pct(infl_dir.median_a)} vs FALLING_OR_FLAT {pct(infl_dir.median_b)}; diff {pct(infl_dir.oriented_median_diff_a_minus_b)}.",
            "sample_support":f"n={int(infl_dir.n_a)} vs {int(infl_dir.n_b)}; LOO sign stable={bool(infl_dir.loo_sign_stable)}",
            "interpretation":"Inflation direction and inflation level are different states: rising inflation was associated with better Gold than falling/flat even though HIGH inflation level was associated with worse Gold.",
            "boundary":"Descriptive heterogeneity, not a causal inflation beta."
        },
        {
            "mechanism":"GROWTH_STATE","status":"SUPPORTED_DESCRIPTIVE",
            "repository_result":f"STRONG median Gold 12M {pct(growth.median_a)} vs WEAK {pct(growth.median_b)}; diff {pct(growth.oriented_median_diff_a_minus_b)}.",
            "sample_support":f"n={int(growth.n_a)} vs {int(growth.n_b)}; LOO sign stable={bool(growth.loo_sign_stable)}",
            "interpretation":"Weak-growth FIRST_HIKE states were associated with somewhat stronger Gold outcomes than strong-growth states.",
            "boundary":"Small historical event set; no recession forecast."
        },
        {
            "mechanism":"ENERGY_DIRECTION","status":"SUPPORTED_DESCRIPTIVE",
            "repository_result":f"RISING energy median Gold 12M {pct(energy.median_a)} vs FALLING_OR_FLAT {pct(energy.median_b)}; diff {pct(energy.oriented_median_diff_a_minus_b)}.",
            "sample_support":f"n={int(energy.n_a)} vs {int(energy.n_b)}; LOO sign stable={bool(energy.loo_sign_stable)}",
            "interpretation":"Rising energy was associated with better subsequent Gold in the supported event contrast.",
            "boundary":"Energy direction is not identified as the causal driver."
        },
        {
            "mechanism":"USD_DIRECTION_EVENT","status":"SECONDARY_DIAGNOSTIC",
            "repository_result":f"USD RISING median Gold 12M {pct(usd_e.median_a)} vs FALLING_OR_FLAT {pct(usd_e.median_b)}; diff {pct(usd_e.oriented_median_diff_a_minus_b)}.",
            "sample_support":f"n={int(usd_e.n_a)} vs {int(usd_e.n_b)}; LOO sign stable={bool(usd_e.loo_sign_stable)}",
            "interpretation":"The event-level USD diagnostic is counterintuitive relative to the common inverse-USD story and is retained as evidence of confounding/era dependence rather than deleted.",
            "boundary":"USD bridge diagnostic; not promoted to primary mechanism evidence."
        },
        {
            "mechanism":"USD_6M_RET_MONTHLY","status":"SECONDARY_DIAGNOSTIC",
            "repository_result":f"Within-cycle beta per 1SD = {usd_m.beta_per_1sd_within:+.4f} Gold forward-6M return; broad exact p={usd_m.p_broad_exact:.5f}; LOO sign stable={bool(usd_m.loo_broad_sign_stable)}.",
            "sample_support":f"{int(usd_m.n_rows)} monthly rows / {int(usd_m.n_cycles)} cycles / {int(usd_m.n_broad_clusters)} broad clusters; multiplicity={usd_m.multiplicity_status}",
            "interpretation":"USD remains a mechanism candidate but the positive sign does not survive secondary-family multiplicity control and should not be called a confirmed driver.",
            "boundary":"Hypothesis-generating secondary diagnostic; source-era restrictions reduce precision."
        },
        {
            "mechanism":"REAL_RATE_PROXY","status":"SECONDARY_DIAGNOSTIC",
            "repository_result":f"Within-cycle beta per 1SD = {rrp.beta_per_1sd_within:+.4f}; broad exact p={rrp.p_broad_exact:.5f}; LOO sign stable={bool(rrp.loo_broad_sign_stable)}.",
            "sample_support":f"{int(rrp.n_rows)} rows / {int(rrp.n_cycles)} cycles; multiplicity={rrp.multiplicity_status}",
            "interpretation":"This public design does not establish the textbook inverse real-rate/Gold relation; the proxy estimate is positive and statistically weak in this secondary diagnostic.",
            "boundary":"Proxy-based association, not a real-yield causal estimate."
        },
        {
            "mechanism":"DFII10_REAL_YIELD","status":"INSUFFICIENT_SUPPORT",
            "repository_result":f"Within-cycle beta per 1SD = {dfii.beta_per_1sd_within:+.4f}; status={dfii.status}.",
            "sample_support":f"{int(dfii.n_rows)} rows but only {int(dfii.n_cycles)} cycles / {int(dfii.n_broad_clusters)} broad clusters.",
            "interpretation":"Actual 10Y TIPS real-yield history is too short in this Fed-cycle design to support a stable Gold mechanism claim.",
            "boundary":"Do not infer absence of a global real-yield relationship; this design is under-supported."
        },
        {
            "mechanism":"NFCI_FINANCIAL_CONDITIONS","status":"NO_STABLE_ASSOCIATION",
            "repository_result":f"Within-cycle beta per 1SD = {nfci.beta_per_1sd_within:+.4f}; broad exact p={nfci.p_broad_exact:.5f}; LOO sign stable={bool(nfci.loo_broad_sign_stable)}.",
            "sample_support":f"{int(nfci.n_rows)} rows / {int(nfci.n_cycles)} cycles.",
            "interpretation":"NFCI does not show a stable Gold forward-return association in the monthly secondary diagnostic.",
            "boundary":"No signal claim; financial stress may matter conditionally through other channels."
        },
        {
            "mechanism":"STRESS_TIMING_BAA","status":"SUPPORTED_DESCRIPTIVE",
            "repository_result":f"Gold trough median M{int(baa.weighted_median_asset_trough_month)} vs Baa stress peak M{int(baa.weighted_median_stress_peak_month)}; lead median {baa.weighted_median_lead_months:+.0f}m; near-2m share {baa.weighted_near_2m_share:.1%}.",
            "sample_support":f"{int(baa.n_legs)} legs / {int(baa.n_broad_episodes)} broad episodes.",
            "interpretation":"Gold often reaches its trough before credit-stress maxima rather than waiting for the stress peak.",
            "boundary":"Ex-post timing description; not a real-time Gold-entry rule."
        },
        {
            "mechanism":"STRESS_TIMING_VIX","status":"SUPPORTED_DESCRIPTIVE",
            "repository_result":f"Gold trough median M{int(vix.weighted_median_asset_trough_month)} vs VIX stress peak M{int(vix.weighted_median_stress_peak_month)}; lead median {vix.weighted_median_lead_months:+.0f}m; near-2m share {vix.weighted_near_2m_share:.1%}.",
            "sample_support":f"{int(vix.n_legs)} legs / {int(vix.n_broad_episodes)} broad episodes.",
            "interpretation":"Gold timing differs from U.S. equities: its trough can precede later VIX stress maxima by several months.",
            "boundary":"Supports timing heterogeneity, not a safe-haven timing signal."
        },
        {
            "mechanism":"STRESS_TIMING_COPPER","status":"SUPPORTED_DESCRIPTIVE",
            "repository_result":f"Gold trough median M{int(copper.weighted_median_asset_trough_month)} vs copper stress peak M{int(copper.weighted_median_stress_peak_month)}; median lead {copper.weighted_median_lead_months:+.0f}m; near-2m share {copper.weighted_near_2m_share:.1%}.",
            "sample_support":f"{int(copper.n_legs)} legs / {int(copper.n_broad_episodes)} broad episodes.",
            "interpretation":"Copper/Gold timing is closer in the supported sample than Baa/VIX timing, but still cannot be used as a deterministic signal.",
            "boundary":"Descriptive stress alignment only."
        },
    ]
    em=pd.DataFrame(rows)
    if not set(em["status"]).issubset(ALLOWED_STATUS):
        raise RuntimeError("mechanism evidence status outside frozen set")
    em.to_csv(OUT/"GOLD_MECHANISM_EVIDENCE_MATRIX.csv",index=False)

    # Claim registry.
    claims=[]
    for i,r in em.iterrows():
        claims.append({
            "claim_id":f"CLM-GOLD-033-{i+1:02d}",
            "mechanism":r["mechanism"],
            "status":r["status"],
            "claim_zh":r["interpretation"],
            "evidence_text":r["repository_result"],
            "boundary":r["boundary"],
            "source_type":"REPOSITORY_RESULT",
            "causal_status":"NONE",
            "oos_status":"NOT_A_FORECASTING_MODEL",
            "deployment_status":"NOT_DEPLOYABLE",
        })
    for i,r in lit.iterrows():
        claims.append({
            "claim_id":f"CLM-GOLD-033-LIT-{i+1:02d}",
            "mechanism":r["mechanism_context"],
            "status":"LITERATURE_CONTEXT",
            "claim_zh":r["evidence_summary"],
            "evidence_text":r["title"],
            "boundary":"External literature context; does not overwrite repository evidence.",
            "source_type":"EXTERNAL_LITERATURE",
            "causal_status":"LITERATURE_DEPENDENT",
            "oos_status":"NOT_APPLICABLE",
            "deployment_status":"NOT_DEPLOYABLE",
        })
    cdf=pd.DataFrame(claims)
    cdf.to_csv(OUT/"GOLD_MECHANISM_CLAIM_REGISTRY.csv",index=False)

    # Myths.
    myths=pd.DataFrame([
        ["GOLD-MYTH-01","高通胀本身就一定利好黄金","NOT_SUPPORTED_AS_SIMPLE_RULE","FIRST_HIKE事件样本中，高通胀水平组的Gold 12M中位数反而更低；但通胀方向结果又不同，说明level与direction必须拆开。"],
        ["GOLD-MYTH-02","黄金和实际利率永远稳定负相关","INSUFFICIENT_SUPPORT","本仓库实际DFII10只有3个周期，真实利率代理也没有给出稳定的 textbook inverse 关系；外部文献同样存在regime-dependent结果。"],
        ["GOLD-MYTH-03","美元上涨，黄金就一定下跌","NOT_SUPPORTED_AS_SIMPLE_RULE","仓库的event/monthly USD诊断出现正向Gold关系，但只是secondary diagnostic且不通过多重检验；说明简单固定符号不足。"],
        ["GOLD-MYTH-04","金融压力越大，黄金就一定同步上涨","NOT_SUPPORTED_AS_SIMPLE_RULE","Gold在FIRST_CUT样本中的低点常早于Baa/VIX压力峰值，stress timing并不同步。"],
        ["GOLD-MYTH-05","黄金是任何市场、任何期限都稳定的避险资产","CONTEXT_DEPENDENT","文献显示safe-haven定义本身依赖极端市场条件，效果可短暂且跨国家/市场不一致。"],
        ["GOLD-MYTH-06","第一次降息天然是黄金的大行情起点","NOT_SUPPORTED_AS_SIMPLE_RULE","Gold FIRST_CUT 12M历史中位约+4.1%，但Fed phase只是条件标签，不能替代机制状态。"],
    ],columns=["myth_id","myth_zh","status","evidence_summary_zh"])
    myths.to_csv(OUT/"GOLD_MECHANISM_MYTH_AUDIT.csv",index=False)

    # Phase profile summary values.
    gp=gphase.set_index("phase")
    phase_text=[
        "# Gold Mechanism Decomposition — 033",
        "",
        "## 结论先行",
        "",
        "当前公共证据最重要的结论不是“找到了黄金唯一驱动因子”，而是相反：**黄金在Fed周期中的机制明显具有状态依赖，常见单因子叙事在这个设计里都不够稳定。**",
        "",
        "### 1. Fed阶段本身只能做条件标签",
        "",
        f"Gold 12M历史中位数：FIRST_HIKE {pct(gp.loc['FIRST_HIKE','ret_12m'])}、LAST_HIKE {pct(gp.loc['LAST_HIKE','ret_12m'])}、PAUSE {pct(gp.loc['PAUSE_START','ret_12m'])}、FIRST_CUT {pct(gp.loc['FIRST_CUT','ret_12m'])}。四阶段没有形成一个简单的“越宽松越涨”单调序列。",
        "",
        "### 2. “通胀对黄金”必须拆成水平和方向",
        "",
        f"FIRST_HIKE时，高通胀水平组 Gold 12M中位 {pct(infl_level.median_a)}，低/中通胀组 {pct(infl_level.median_b)}；但通胀RISING组 {pct(infl_dir.median_a)}，FALLING_OR_FLAT组 {pct(infl_dir.median_b)}。两组结果方向不同，说明“通胀高”和“通胀在上升”不是同一机制。",
        "",
        "Erb & Harvey 的长期研究同样提醒：黄金在实用投资期限里并不是一个可靠的机械通胀对冲。因此，更合理的研究问题不是“CPI高不高”，而是通胀状态如何与实际利率、增长、美元和压力共同出现。",
        "",
        "### 3. 实际利率：理论重要，但本仓库证据还不够支持单一负相关",
        "",
        f"月度 REAL_RATE_PROXY 对 Gold forward-6M 的within-cycle beta为 {rrp.beta_per_1sd_within:+.4f}/1SD，broad exact p={rrp.p_broad_exact:.3f}；实际 DFII10 仅覆盖 {int(dfii.n_cycles)} 个周期并被标记 INSUFFICIENT_SUPPORT。",
        "",
        "所以当前正确表述是：**真实利率是机制候选，但在本Fed-cycle样本里没有被验证为稳定的反向Gold驱动器。** 这并不证明全市场不存在真实利率关系。Apergis等使用regime-switching模型甚至得到正向关系，进一步说明符号可能依赖状态和模型。",
        "",
        "### 4. 美元：仓库结果与常见直觉冲突，必须保留",
        "",
        f"事件级USD诊断中，USD RISING组 Gold 12M中位 {pct(usd_e.median_a)}，FALLING_OR_FLAT组 {pct(usd_e.median_b)}。月度within-cycle USD beta也是正值 {usd_m.beta_per_1sd_within:+.4f}/1SD，未调整 broad p={usd_m.p_broad_exact:.5f}，但secondary-family FDR没有survivor。",
        "",
        "这不能被写成“美元涨所以黄金涨”。更合理的结论是：当前Fed-cycle样本存在明显era/confounding问题，固定负相关不是可以无条件搬用的规则。外部研究经常找到Gold对弱美元的hedge属性，正因为如此，我们的反常结果更应该被当作机制异质性证据，而不是被删除。",
        "",
        "### 5. 增长和能源状态提供了更稳定的事件级异质性",
        "",
        f"STRONG growth组 Gold 12M中位 {pct(growth.median_a)}，WEAK组 {pct(growth.median_b)}；energy RISING组 {pct(energy.median_a)}，FALLING_OR_FLAT组 {pct(energy.median_b)}。这些对比LOO方向稳定，但仍然只是事件级描述，不能被解释成独立因果贡献。",
        "",
        "### 6. 黄金的压力时钟和美股不一样",
        "",
        f"FIRST_CUT配对中，Gold低点月中位：Baa样本M{int(baa.weighted_median_asset_trough_month)} vs Baa压力峰值M{int(baa.weighted_median_stress_peak_month)}；VIX样本M{int(vix.weighted_median_asset_trough_month)} vs VIX峰值M{int(vix.weighted_median_stress_peak_month)}。这意味着黄金可能在更广泛金融压力达到最大之前就完成一部分价格调整。",
        "",
        "Baur & Lucey / Baur & McDermott 对safe haven的定义也强调：安全港是特定压力条件下的相关性属性，不等于所有压力阶段都持续单边上涨。",
        "",
        "## 现在最适合PandaAI展示的机制框架",
        "",
        "Gold解释卡应该同时展示：",
        "- Fed phase",
        "- inflation level + direction",
        "- growth state",
        "- real-rate evidence status",
        "- USD evidence status",
        "- energy state",
        "- stress timing",
        "- support/multiplicity/PIT caveat",
        "",
        "并明确写：**mechanism map ≠ driver ranking ≠ expected return ≠ trading signal。**",
    ]
    (OUT/"GOLD_MECHANISM_SYNTHESIS_ZH.md").write_text("\n".join(phase_text)+"\n")

    schema={
        "module":"FED-CYCLE-GOLD-MECHANISM-DECOMPOSITION-033",
        "mechanism_families":[
            "INFLATION_LEVEL","INFLATION_DIRECTION","GROWTH_STATE","ENERGY_DIRECTION",
            "USD_DIRECTION","REAL_RATE_PROXY","DFII10_REAL_YIELD","NFCI_FINANCIAL_CONDITIONS",
            "STRESS_TIMING","FED_PHASE"
        ],
        "required_output_fields":[
            "mechanism","evidence_status","repository_result","sample_support",
            "literature_context_optional","boundary"
        ],
        "prohibited_outputs":[
            "dominant_driver_score","best_gold_phase","expected_gold_return",
            "gold_bottom_date","buy_sell_instruction"
        ],
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"PANDAAI_GOLD_MECHANISM_SCHEMA.json").write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# FED-CYCLE-GOLD-MECHANISM-DECOMPOSITION-033 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED GOLD MECHANISM EVIDENCE MAP / MULTI-MECHANISM / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- Gold phase rows: {len(gphase)}",
        f"- supported FIRST_HIKE state contrasts: {len(first_supported)} + 1 USD diagnostic",
        f"- monthly mechanism diagnostics: {len(msec)}",
        f"- Gold stress-timing rows: {len(gstress)}",
        f"- literature context rows: {len(lit)}",
        f"- mechanism evidence rows: {len(em)}",
        f"- mechanism claim rows: {len(cdf)}",
        "",
        "Core conclusion: the public evidence stack does not justify a single-driver Gold story. Inflation level and direction differ; real-yield support is limited; USD diagnostics are counterintuitive and secondary; stress timing differs from U.S. equities; phase labels condition the distribution but do not identify a causal Gold shock.",
    ]
    (OUT/"FED_CYCLE_GOLD_MECHANISM_DECOMPOSITION_033_REPORT.md").write_text("\n".join(report)+"\n")

    # QC
    if not bool(first_supported["loo_sign_stable"].all()):
        raise RuntimeError("supported event contrasts lost LOO stability")
    if usd_m["multiplicity_status"]!="SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM":
        raise RuntimeError("USD monthly diagnostic improperly promoted")
    if dfii["status"]!="INSUFFICIENT_SUPPORT":
        raise RuntimeError("DFII10 support unexpectedly changed")
    if set(lit["status"])!={"LITERATURE_CONTEXT"}:
        raise RuntimeError("literature tagging lost")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-GOLD-MECHANISM-DECOMPOSITION-033",
        "upstream_qc":{"001":q001["qc_gate"],"002":q002["qc_gate"],"004":q004["qc_gate"],"018":q018["qc_gate"],"032":q032["qc_gate"]},
        "gold_phase_rows":int(len(gphase)),
        "supported_first_hike_state_contrasts":int(len(first_supported)),
        "usd_event_diagnostic_rows":int(len(usd_event)),
        "monthly_secondary_diagnostics":int(len(msec)),
        "gold_stress_timing_rows":int(len(gstress)),
        "literature_context_rows":int(len(lit)),
        "mechanism_evidence_rows":int(len(em)),
        "mechanism_claim_rows":int(len(cdf)),
        "supported_event_loo_sign_stable":True,
        "usd_secondary_promoted_to_confirmed_driver":False,
        "usd_secondary_fdr_survivor":False,
        "dfii10_status":"INSUFFICIENT_SUPPORT",
        "real_rate_inverse_rule_claimed":False,
        "inflation_level_direction_separated":True,
        "safe_haven_trading_signal_created":False,
        "mechanism_ranking_created":False,
        "multivariate_score_created":False,
        "expected_return_forecast_created":False,
        "new_pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
