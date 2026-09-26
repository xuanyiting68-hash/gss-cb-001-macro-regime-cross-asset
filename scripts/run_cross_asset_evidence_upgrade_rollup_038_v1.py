#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"cross_asset_evidence_upgrade_rollup_038_v1"
OUT.mkdir(parents=True,exist_ok=True)

Q032=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"/"QC.json"
Q033=ROOT/"results"/"fed_cycle_gold_mechanism_decomposition_033_v1"/"QC.json"
Q034=ROOT/"results"/"fed_cycle_housing_lag_chain_034_v1"/"QC.json"
Q035=ROOT/"results"/"fed_cycle_long_treasury_proxy_bridge_035_v1"/"QC.json"
Q036=ROOT/"results"/"fed_cycle_listed_reit_proxy_bridge_036_v1"/"QC.json"
Q037=ROOT/"results"/"fed_cycle_reit_deep_history_dual_bridge_037_v1"/"QC.json"

MASTER032=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"/"EXTENSION_ASSET_ATLAS.csv"
CORE032=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"/"CORE_FOUR_PHASE_ATLAS.csv"
VUSTX=ROOT/"results"/"fed_cycle_long_treasury_proxy_bridge_035_v1"/"VUSTX_EXTENDED_PHASE_SUMMARY.csv"
VGSIX=ROOT/"results"/"fed_cycle_listed_reit_proxy_bridge_036_v1"/"VGSIX_EXTENDED_PHASE_SUMMARY.csv"
FRESX=ROOT/"results"/"fed_cycle_reit_deep_history_dual_bridge_037_v1"/"FRESX_EXTENDED_PHASE_SUMMARY.csv"

PHASES=["FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"]

def readq(path):
    q=json.loads(Path(path).read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream not PASS: {path}")
    return q

def main():
    q032,q033,q034,q035,q036,q037=[readq(p) for p in [Q032,Q033,Q034,Q035,Q036,Q037]]

    if q035.get("bridge_status")!="BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION":
        raise RuntimeError("035 bridge pass not preserved")
    if q036.get("bridge_status")!="BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION":
        raise RuntimeError("036 bridge pass not preserved")
    if q037.get("dual_bridge_status")!="DUAL_BRIDGE_FAIL_NO_DEEP_EXTENSION":
        raise RuntimeError("037 fail decision not preserved")

    ext032=pd.read_csv(MASTER032)
    core032=pd.read_csv(CORE032)
    vustx=pd.read_csv(VUSTX)
    vgsix=pd.read_csv(VGSIX)
    fresx=pd.read_csv(FRESX)

    # Canonical evidence-status registry.
    rows=[
        ["GOLD","Gold","CORE_SUPPORTED","CORE_SUPPORTED + MULTI_MECHANISM_MAP_AVAILABLE","033","Phase evidence supported; mechanism map available; no dominant driver ranking.","NONE"],
        ["US_HOUSE_PRICE","U.S. national house price","SUPPORTED_SLOW_MOVING","SUPPORTED_SLOW_MOVING + FINANCING_ACTIVITY_PRICE_TIMING_MAP","034","Case-Shiller slow clock retained; financing/activity ordering is descriptive and path risk remains DECLINE_24M.","DECLINE_24M"],
        ["TLT","TLT target ETF","LIMITED_DESCRIPTIVE","TARGET_ETF_LIMITED_HISTORY","035","Original ETF history remains limited; use VUSTX proxy for supported longer-history duration evidence without relabeling.","MDD_12M"],
        ["VUSTX_LONG_TREASURY_PROXY","Long-duration Treasury proxy","N/A","SUPPORTED_PROXY_DESCRIPTIVE","035","All TLT-VUSTX bridge gates passed; proxy extension supported and separately labeled.","MDD_12M"],
        ["VNQ","VNQ target ETF","LIMITED_DESCRIPTIVE","TARGET_ETF_LIMITED_HISTORY","036","Original VNQ history remains limited.","MDD_12M"],
        ["VGSIX_REIT_PROXY","Listed REIT proxy","N/A","LIMITED_PROXY_DESCRIPTIVE","036","Bridge to VNQ passed but only four broad episodes; do not promote to supported evidence.","MDD_12M"],
        ["FRESX_REIT_ACTIVE_PROXY","Active REIT deep-history candidate","N/A","NOT_PROMOTED_DUAL_BRIDGE_FAIL","037","Highly correlated with VNQ/VGSIX but one frozen VGSIX phase-direction gate failed; deep history blocked.","MDD_12M"],
        ["BTC_USD","Bitcoin USD","LIMITED_DESCRIPTIVE","LIMITED_DESCRIPTIVE","032","Short true history retained; no synthetic backfill.","MDD_12M"],
        ["HANG_SENG","Hang Seng","DIAGNOSTIC_ASIA","DIAGNOSTIC_ASIA","032","Regional diagnostic only.","MDD_12M"],
        ["KOSPI","KOSPI","DIAGNOSTIC_ASIA","DIAGNOSTIC_ASIA","032","Regional diagnostic only.","MDD_12M"],
        ["NIKKEI_225","Nikkei 225","DIAGNOSTIC_ASIA","DIAGNOSTIC_ASIA","032","Regional diagnostic only.","MDD_12M"],
        ["SHANGHAI_COMPOSITE","Shanghai Composite","DIAGNOSTIC_ASIA","DIAGNOSTIC_ASIA","032","Regional diagnostic only.","MDD_12M"],
    ]
    status=pd.DataFrame(rows,columns=["asset_id","asset_label","status_032_or_prior","canonical_status_after_038","source_module","interpretation_boundary","path_risk_metric"])
    status.to_csv(OUT/"ASSET_EVIDENCE_STATUS_V2.csv",index=False)

    # Four-phase extension status table.
    phase_rows=[]
    for df,aid,label,module in [
        (vustx,"VUSTX_LONG_TREASURY_PROXY","Long-duration Treasury proxy","035"),
        (vgsix,"VGSIX_REIT_PROXY","Listed REIT proxy","036"),
        (fresx,"FRESX_REIT_ACTIVE_PROXY","Rejected active REIT proxy","037"),
    ]:
        for p in PHASES:
            r=df[df["anchor"]==p]
            if len(r)!=1:
                raise RuntimeError(f"missing {aid} {p}")
            r=r.iloc[0]
            phase_rows.append({
                "asset_id":aid,
                "asset_label":label,
                "phase":p,
                "source_module":module,
                "support_status":r["support_status"],
                "weighted_median_ret_3m":r["weighted_median_ret_3m"],
                "weighted_median_ret_6m":r["weighted_median_ret_6m"],
                "weighted_median_ret_12m":r["weighted_median_ret_12m"],
                "weighted_median_mdd_12m":r["weighted_median_mdd_12m"],
                "weighted_median_mdd_trough_month":r["weighted_median_mdd_trough_month"],
                "promotion_allowed": aid!="FRESX_REIT_ACTIVE_PROXY",
                "interpretation_guardrail":
                    "proxy history only; never relabel target ETF" if aid!="FRESX_REIT_ACTIVE_PROXY"
                    else "diagnostic only; 037 dual bridge failed; do not use as canonical REIT phase evidence",
            })
    phase=pd.DataFrame(phase_rows)
    phase.to_csv(OUT/"FOUR_PHASE_EXTENSION_STATUS_V2.csv",index=False)

    claims=[
        ["UPG-038-01","Long-duration Treasury evidence is stronger than the original TLT-only layer.","SUPPORTED_PROXY_DESCRIPTIVE","035","Use VUSTX proxy label; do not call pre-2002 history TLT."],
        ["UPG-038-02","FIRST_HIKE long-duration Treasury history shows near-flat 12M endpoint with materially larger interim drawdown.","SUPPORTED_PROXY_DESCRIPTIVE","035","Historical proxy distribution, not expected return."],
        ["UPG-038-03","LAST_HIKE and PAUSE long-duration Treasury proxy medians are stronger than FIRST_HIKE in the extended sample.","SUPPORTED_PROXY_DESCRIPTIVE","035","Do not turn into best-phase ranking."],
        ["UPG-038-04","VGSIX is a very high-fidelity VNQ proxy in overlap history.","BRIDGE_VALID","036","Measurement bridge does not upgrade sample count by itself."],
        ["UPG-038-05","REIT Fed-cycle phase evidence remains limited after the VGSIX extension.","LIMITED_PROXY_DESCRIPTIVE","036","Four broad episodes only."],
        ["UPG-038-06","FRESX cannot be used to promote 1987+ REIT history under the frozen dual bridge.","NOT_PROMOTED_DUAL_BRIDGE_FAIL","037","Do not relax the +/-3% direction gate post-run."],
        ["UPG-038-07","Gold should be explained through multiple mechanisms rather than a single real-rate/USD/inflation driver.","MULTI_MECHANISM_MAP_AVAILABLE","033","No dominant-driver ranking."],
        ["UPG-038-08","Housing requires a slow financing-activity-price clock rather than traded-asset MDD logic.","SUPPORTED_SLOW_MOVING","034","Keep DECLINE_24M and national-index boundary."],
        ["UPG-038-09","Mortgage-rate peaks often precede housing activity troughs, but activity-before-price ordering is not deterministic.","SUPPORTED_DESCRIPTIVE","034","Timing ordering is descriptive, not causal."],
        ["UPG-038-10","Bitcoin remains genuinely short-history in Fed-cycle analysis.","LIMITED_DESCRIPTIVE","032","Deepen by mechanisms/liquidity rather than synthetic backfill."],
    ]
    cdf=pd.DataFrame(claims,columns=["claim_id","claim","status","source_module","boundary"])
    cdf.to_csv(OUT/"CANONICAL_CLAIM_UPGRADE_REGISTRY.csv",index=False)

    schema={
        "module":"CROSS-ASSET-EVIDENCE-UPGRADE-ROLLUP-038",
        "routing":{
            "GOLD":"use_032_phase_plus_033_mechanism_map",
            "US_HOUSE_PRICE":"use_032_phase_plus_034_slow_lag_chain",
            "LONG_DURATION_TREASURY":"use_035_VUSTX_supported_proxy_with_explicit_proxy_label",
            "LISTED_REIT":"use_036_VGSIX_limited_proxy; reject_037_FRESX_deep_extension",
            "BTC_USD":"use_032_limited_phase_history; next research should be mechanism/liquidity",
        },
        "prohibited":[
            "best_asset","best_phase","expected_return","trade_instruction",
            "relabel_proxy_as_target","promote_failed_proxy","synthetic_btc_history"
        ],
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"PANDAAI_EVIDENCE_ROUTING_V2.json").write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n")

    synth=[
        "# Cross-Asset Evidence Upgrade Rollup — 038",
        "",
        "032之后，证据层发生了四个重要变化：",
        "",
        "1. **长期美债：真正升级。** TLT本身仍是短历史ETF，但035把VUSTX验证成高质量long-duration Treasury proxy，扩展到6个broad episodes并达到SUPPORTED_PROXY_DESCRIPTIVE。",
        "2. **REIT：测量桥接成功，但证据仍有限。** VGSIX几乎完美复刻VNQ的重叠历史，但只有4个broad episodes，所以仍是LIMITED_PROXY_DESCRIPTIVE；FRESX虽然长期相关很高，却因预注册双桥的一项方向gate失败而不允许升级1987+历史。",
        "3. **住房：从‘房价结果’升级为‘融资→活动→价格’慢时钟。** mortgage peak通常早于activity trough，但activity trough并不总在price trough之前，因此不能写成固定机械传导链。",
        "4. **黄金：从‘阶段表现’升级为‘多机制地图’。** 通胀水平/方向、增长、能源、美元、实际利率、压力时钟彼此并不支持一个稳定单因子故事。",
        "",
        "因此当前跨资产内容的证据等级已经更清楚：",
        "",
        "- CORE_SUPPORTED：Gold / S&P 500 / Nasdaq / DXY / WTI",
        "- SUPPORTED_PROXY_DESCRIPTIVE：long-duration Treasury via VUSTX",
        "- SUPPORTED_SLOW_MOVING：U.S. national housing",
        "- LIMITED_PROXY_DESCRIPTIVE：listed REIT via VGSIX",
        "- LIMITED_DESCRIPTIVE：Bitcoin and target ETF short-history layers",
        "- DIAGNOSTIC_ONLY：Asia regional equity extensions",
        "- NOT_PROMOTED：FRESX deep-history REIT candidate",
        "",
        "下一步最合理的新增研究不是继续找REIT代理，而是转向Bitcoin的真实2014+机制：美元、实际利率、Nasdaq/risk beta、VIX/NFCI、Fed liquidity / balance-sheet proxies，以及这些关系是否随regime变化。",
    ]
    (OUT/"CROSS_ASSET_EVIDENCE_UPGRADE_038_SYNTHESIS_ZH.md").write_text("\n".join(synth)+"\n")

    report=[
        "# CROSS-ASSET-EVIDENCE-UPGRADE-ROLLUP-038 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED EVIDENCE-STATUS ROLLUP / NO NEW ESTIMATION / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- asset evidence rows: {len(status)}",
        f"- proxy phase rows: {len(phase)}",
        f"- canonical claim upgrades: {len(cdf)}",
        "- 035 bridge pass preserved: true",
        "- 036 bridge pass + limited support preserved: true",
        "- 037 dual-bridge fail preserved: true",
        "- FRESX promotion: false",
        "- Bitcoin synthetic history: false",
    ]
    (OUT/"CROSS_ASSET_EVIDENCE_UPGRADE_ROLLUP_038_REPORT.md").write_text("\n".join(report)+"\n")

    if q035.get("bridge_status")!="BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION":
        raise RuntimeError("035 status drift")
    if not (vustx["support_status"]=="SUPPORTED_PROXY_DESCRIPTIVE").all():
        raise RuntimeError("VUSTX support drift")
    if not (vgsix["support_status"]=="LIMITED_PROXY_DESCRIPTIVE").all():
        raise RuntimeError("VGSIX support drift")
    if not (fresx["support_status"]=="NOT_PROMOTED_DUAL_BRIDGE_FAIL").all():
        raise RuntimeError("FRESX fail promotion drift")
    if status.loc[status["asset_id"]=="BTC_USD","canonical_status_after_038"].iloc[0]!="LIMITED_DESCRIPTIVE":
        raise RuntimeError("BTC status drift")
    if status.loc[status["asset_id"]=="US_HOUSE_PRICE","path_risk_metric"].iloc[0]!="DECLINE_24M":
        raise RuntimeError("housing metric drift")

    qc={
        "qc_gate":"PASS",
        "module":"CROSS-ASSET-EVIDENCE-UPGRADE-ROLLUP-038",
        "upstream_qc":{"032":q032["qc_gate"],"033":q033["qc_gate"],"034":q034["qc_gate"],"035":q035["qc_gate"],"036":q036["qc_gate"],"037":q037["qc_gate"]},
        "asset_evidence_rows":int(len(status)),
        "proxy_phase_rows":int(len(phase)),
        "claim_upgrade_rows":int(len(cdf)),
        "vustx_supported_proxy_preserved":True,
        "vgsix_limited_proxy_preserved":True,
        "fresx_not_promoted_preserved":True,
        "housing_decline_24m_preserved":True,
        "gold_mechanism_ranking_created":False,
        "bitcoin_status":"LIMITED_DESCRIPTIVE",
        "synthetic_bitcoin_history_created":False,
        "best_asset_outputs":0,
        "best_phase_outputs":0,
        "expected_return_forecasts":0,
        "trade_instructions":0,
        "new_estimation":False,
        "new_pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
