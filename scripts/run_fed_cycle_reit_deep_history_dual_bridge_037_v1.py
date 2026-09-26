#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_reit_deep_history_dual_bridge_037_v1"
OUT.mkdir(parents=True,exist_ok=True)

SPEC=ROOT/"data"/"public"/"REIT_DEEP_HISTORY_SOURCE_SPEC_20260926.csv"
Q014=ROOT/"results"/"fed_cycle_cross_asset_expansion_v1"/"QC.json"
Q032=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"/"QC.json"
Q036=ROOT/"results"/"fed_cycle_listed_reit_proxy_bridge_036_v1"/"QC.json"

AS_OF=pd.Timestamp("2026-09-26")
LAST_COMPLETE_MONTH=AS_OF.to_period("M")-1
PHASES=["FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"]

TARGET="VNQ"
REFERENCE="VGSIX_REIT_PROXY"
CANDIDATE="FRESX_REIT_ACTIVE_PROXY"

def read_pass(path):
    q=json.loads(Path(path).read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

EXP=load_module(ROOT/"scripts"/"run_fed_cycle_cross_asset_expansion_v1.py","exp014_for_037")

def weighted_median(values,weights):
    return EXP.weighted_quantile(values,weights,0.5)

def direction(v):
    if pd.isna(v):
        return "NA"
    if v>0.03:
        return "POSITIVE"
    if v<-0.03:
        return "NEGATIVE"
    return "NEUTRAL"

def monthly_diag(ref_ret,cand_ret,ref_name):
    ov=pd.concat(
        [ref_ret.rename("reference_ret"),cand_ret.rename("candidate_ret")],
        axis=1,join="inner"
    ).dropna()
    if ov.empty:
        raise RuntimeError(f"no monthly overlap for {ref_name}")
    pearson=float(ov["reference_ret"].corr(ov["candidate_ret"],method="pearson"))
    spearman=float(ov["reference_ret"].corr(ov["candidate_ret"],method="spearman"))
    beta,intercept=np.polyfit(
        ov["reference_ret"].to_numpy(),
        ov["candidate_ret"].to_numpy(),
        1
    )
    return ov,{
        "reference":ref_name,
        "candidate":CANDIDATE,
        "matched_return_months":len(ov),
        "first_return_month":str(ov.index.min()),
        "last_return_month":str(ov.index.max()),
        "last_complete_month_required":str(LAST_COMPLETE_MONTH),
        "pearson_monthly_return":pearson,
        "spearman_monthly_return":spearman,
        "descriptive_beta_candidate_on_reference":float(beta),
        "descriptive_intercept":float(intercept),
        "median_abs_monthly_return_diff":float((ov["candidate_ret"]-ov["reference_ret"]).abs().median()),
        "mean_abs_monthly_return_diff":float((ov["candidate_ret"]-ov["reference_ret"]).abs().mean()),
        "current_partial_month_used":False,
    }

def add_common_weights(df):
    x=df.copy()
    counts=x.groupby(["anchor","broad_episode_id"])["cycle_id"].transform("count")
    x["common_episode_weight"]=1.0/counts
    return x

def event_bridge(metrics,ref_asset,tag):
    ref=metrics[metrics["asset"]==ref_asset]
    cand=metrics[metrics["asset"]==CANDIDATE]
    common=ref.merge(
        cand,
        on=["anchor","cycle_id","broad_episode_id","anchor_date"],
        suffixes=("_ref","_cand"),
        validate="one_to_one"
    )
    if common.empty:
        raise RuntimeError(f"no common events for {tag}")
    common=add_common_weights(common)
    common["ret12_diff"]=common["ret_12m_cand"]-common["ret_12m_ref"]
    common["abs_ret12_diff"]=common["ret12_diff"].abs()
    common["mdd_diff"]=common["mdd_12m_cand"]-common["mdd_12m_ref"]
    common["abs_mdd_diff"]=common["mdd_diff"].abs()
    common["ret12_sign_agree"]=(np.sign(common["ret_12m_cand"])==np.sign(common["ret_12m_ref"])).astype(float)

    stats={
        "event_rows":len(common),
        "ret12_sign_agreement":float(common["ret12_sign_agree"].mean()),
        "ret12_correlation":float(common["ret_12m_ref"].corr(common["ret_12m_cand"])),
        "ret12_median_abs_difference":float(common["abs_ret12_diff"].median()),
        "mdd_correlation":float(common["mdd_12m_ref"].corr(common["mdd_12m_cand"])),
        "mdd_median_abs_difference":float(common["abs_mdd_diff"].median()),
    }

    phase_rows=[]
    for anchor in PHASES:
        g=common[common["anchor"]==anchor]
        if g.empty:
            continue
        w=g["common_episode_weight"].to_numpy(float)
        rr=weighted_median(g["ret_12m_ref"],w)
        cr=weighted_median(g["ret_12m_cand"],w)
        rm=weighted_median(g["mdd_12m_ref"],w)
        cm=weighted_median(g["mdd_12m_cand"],w)
        phase_rows.append({
            "reference":ref_asset,"candidate":CANDIDATE,
            "anchor":anchor,
            "n_common_events":len(g),
            "n_common_broad_episodes":g["broad_episode_id"].nunique(),
            "reference_weighted_median_ret_12m":rr,
            "candidate_weighted_median_ret_12m":cr,
            "ret12_abs_diff":abs(cr-rr),
            "reference_direction":direction(rr),
            "candidate_direction":direction(cr),
            "direction_agree":direction(rr)==direction(cr),
            "reference_weighted_median_mdd_12m":rm,
            "candidate_weighted_median_mdd_12m":cm,
            "mdd_abs_diff":abs(cm-rm),
        })
    ps=pd.DataFrame(phase_rows)
    if len(ps)!=4 or set(ps["anchor"])!=set(PHASES):
        raise RuntimeError(f"{tag} must have four common phase rows")
    stats.update({
        "phase_direction_all_agree":bool(ps["direction_agree"].all()),
        "phase_median_abs_ret12_difference":float(ps["ret12_abs_diff"].median()),
        "phase_max_abs_ret12_difference":float(ps["ret12_abs_diff"].max()),
    })
    return common,ps,stats

def liquid_24(price_map,anchor_date):
    ep=pd.Timestamp(anchor_date).to_period("M")
    basep=ep-1
    postp=[ep+k for k in range(1,25)]
    if basep not in price_map or any(p not in price_map for p in postp):
        return None
    base=float(price_map[basep])
    post=np.array([float(price_map[p]) for p in postp],dtype=float)
    vals=np.concatenate([[base],post])
    peaks=np.maximum.accumulate(vals)
    dd=1.0-vals/peaks
    return {
        "ret_24m":float(post[23]/base-1.0),
        "mdd_24m":float(dd.max()),
        "mdd_trough_month_24m":int(np.argmax(dd)) if float(dd.max())>1e-15 else np.nan,
    }

def main():
    q014=read_pass(Q014); q032=read_pass(Q032); q036=read_pass(Q036)
    if q036.get("bridge_status")!="BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION":
        raise RuntimeError("036 VGSIX bridge must pass before 037")

    spec=pd.read_csv(SPEC)
    if set(spec["asset_id"])!={TARGET,REFERENCE,CANDIDATE}:
        raise RuntimeError("037 source spec changed")

    fetched={}
    prov=[]
    for r in spec.itertuples(index=False):
        df,meta=EXP.fetch_yahoo(r.symbol,adjusted=True)
        fetched[r.asset_id]={"df":df,"meta":meta}
        prov.append({
            "asset_id":r.asset_id,"symbol":r.symbol,"role":r.role,
            "source":r.source,"source_context_url":r.source_context_url,
            "official_inception":r.official_inception,
            "price_history_url":meta["url"],"acquisition_method":meta["method"],
            "price_field":meta["price_field"],
            "retrieved_utc":datetime.now(timezone.utc).isoformat(),
            "sha256":meta["sha256"],"raw_bytes":meta["raw_bytes"],
            "rows_total":len(df),"first_date":str(df["date"].min().date()),
            "last_date":str(df["date"].max().date()),"raw_committed":False,
        })
    preg=pd.DataFrame(prov)
    if len(preg)!=3 or preg["sha256"].str.len().ne(64).any():
        raise RuntimeError("source provenance incomplete")
    ffirst=pd.Timestamp(preg.loc[preg["asset_id"]==CANDIDATE,"first_date"].iloc[0])
    if ffirst>pd.Timestamp("1986-12-31"):
        raise RuntimeError(f"FRESX history begins too late: {ffirst}")
    preg.to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)

    monthly={}
    returns={}
    for aid,obj in fetched.items():
        m=EXP.monthly_average(obj["df"])
        m=m[m["period"]<=LAST_COMPLETE_MONTH].copy()
        monthly[aid]=m
        s=m.set_index("period")["value"].astype(float)
        returns[aid]=s.pct_change(fill_method=None)

    ov_vnq,diag_vnq=monthly_diag(returns[TARGET],returns[CANDIDATE],TARGET)
    ov_vgsix,diag_vgsix=monthly_diag(returns[REFERENCE],returns[CANDIDATE],REFERENCE)
    pd.DataFrame([diag_vnq]).to_csv(OUT/"VNQ_BRIDGE_MONTHLY.csv",index=False)
    pd.DataFrame([diag_vgsix]).to_csv(OUT/"VGSIX_BRIDGE_MONTHLY.csv",index=False)

    cycles=EXP.load_cycles()
    if any(pd.to_datetime(cycles["first_hike"]).dt.year>=2026):
        raise RuntimeError("current 2026 candidate leaked")

    assets={
        TARGET:{"df":monthly[TARGET],"label":"VNQ target ETF","source":"fresh Yahoo adjusted close"},
        REFERENCE:{"df":monthly[REFERENCE],"label":"VGSIX high-fidelity REIT reference","source":"fresh Yahoo adjusted close"},
        CANDIDATE:{"df":monthly[CANDIDATE],"label":"FRESX active REIT deep-history candidate","source":"fresh Yahoo adjusted close"},
    }
    metrics,_=EXP.build_market(cycles,assets)

    common_vnq,phase_vnq,sv=event_bridge(metrics,TARGET,"VNQ")
    common_vgsix,phase_vgsix,sg=event_bridge(metrics,REFERENCE,"VGSIX")
    common_vnq.to_csv(OUT/"VNQ_COMMON_EVENT_PANEL.csv",index=False)
    common_vgsix.to_csv(OUT/"VGSIX_COMMON_EVENT_PANEL.csv",index=False)
    phase_vnq.to_csv(OUT/"VNQ_COMMON_PHASE_SUMMARY.csv",index=False)
    phase_vgsix.to_csv(OUT/"VGSIX_COMMON_PHASE_SUMMARY.csv",index=False)

    A=[
        ("A1","vnq_overlap_months_ge_240",diag_vnq["matched_return_months"],">=240",diag_vnq["matched_return_months"]>=240),
        ("A2","vnq_pearson_ge_0.92",diag_vnq["pearson_monthly_return"],">=0.92",diag_vnq["pearson_monthly_return"]>=0.92),
        ("A2","vnq_spearman_ge_0.92",diag_vnq["spearman_monthly_return"],">=0.92",diag_vnq["spearman_monthly_return"]>=0.92),
        ("A3","vnq_beta_0.70_1.30",diag_vnq["descriptive_beta_candidate_on_reference"],"[0.70,1.30]",0.70<=diag_vnq["descriptive_beta_candidate_on_reference"]<=1.30),
        ("A3","vnq_abs_intercept_le_0.0040",abs(diag_vnq["descriptive_intercept"]),"<=0.0040",abs(diag_vnq["descriptive_intercept"])<=0.0040),
        ("A4","vnq_event_sign_agreement_ge_0.80",sv["ret12_sign_agreement"],">=0.80",sv["ret12_sign_agreement"]>=0.80),
        ("A4","vnq_event_ret_corr_ge_0.90",sv["ret12_correlation"],">=0.90",sv["ret12_correlation"]>=0.90),
        ("A4","vnq_event_ret_median_abs_diff_le_0.08",sv["ret12_median_abs_difference"],"<=0.08",sv["ret12_median_abs_difference"]<=0.08),
        ("A5","vnq_event_mdd_corr_ge_0.85",sv["mdd_correlation"],">=0.85",sv["mdd_correlation"]>=0.85),
        ("A5","vnq_event_mdd_median_abs_diff_le_0.06",sv["mdd_median_abs_difference"],"<=0.06",sv["mdd_median_abs_difference"]<=0.06),
        ("A6","vnq_four_phase_direction_all_agree",int(sv["phase_direction_all_agree"]),"true",sv["phase_direction_all_agree"]),
        ("A6","vnq_phase_median_abs_ret_diff_le_0.06",sv["phase_median_abs_ret12_difference"],"<=0.06",sv["phase_median_abs_ret12_difference"]<=0.06),
        ("A6","vnq_phase_max_abs_ret_diff_le_0.10",sv["phase_max_abs_ret12_difference"],"<=0.10",sv["phase_max_abs_ret12_difference"]<=0.10),
    ]
    B=[
        ("B1","vgsix_overlap_months_ge_330",diag_vgsix["matched_return_months"],">=330",diag_vgsix["matched_return_months"]>=330),
        ("B2","vgsix_pearson_ge_0.92",diag_vgsix["pearson_monthly_return"],">=0.92",diag_vgsix["pearson_monthly_return"]>=0.92),
        ("B2","vgsix_spearman_ge_0.92",diag_vgsix["spearman_monthly_return"],">=0.92",diag_vgsix["spearman_monthly_return"]>=0.92),
        ("B3","vgsix_beta_0.70_1.30",diag_vgsix["descriptive_beta_candidate_on_reference"],"[0.70,1.30]",0.70<=diag_vgsix["descriptive_beta_candidate_on_reference"]<=1.30),
        ("B3","vgsix_abs_intercept_le_0.0040",abs(diag_vgsix["descriptive_intercept"]),"<=0.0040",abs(diag_vgsix["descriptive_intercept"])<=0.0040),
        ("B4","vgsix_event_sign_agreement_ge_0.85",sg["ret12_sign_agreement"],">=0.85",sg["ret12_sign_agreement"]>=0.85),
        ("B4","vgsix_event_ret_corr_ge_0.90",sg["ret12_correlation"],">=0.90",sg["ret12_correlation"]>=0.90),
        ("B4","vgsix_event_ret_median_abs_diff_le_0.08",sg["ret12_median_abs_difference"],"<=0.08",sg["ret12_median_abs_difference"]<=0.08),
        ("B5","vgsix_event_mdd_corr_ge_0.85",sg["mdd_correlation"],">=0.85",sg["mdd_correlation"]>=0.85),
        ("B5","vgsix_event_mdd_median_abs_diff_le_0.06",sg["mdd_median_abs_difference"],"<=0.06",sg["mdd_median_abs_difference"]<=0.06),
        ("B6","vgsix_four_phase_direction_all_agree",int(sg["phase_direction_all_agree"]),"true",sg["phase_direction_all_agree"]),
        ("B6","vgsix_phase_median_abs_ret_diff_le_0.06",sg["phase_median_abs_ret12_difference"],"<=0.06",sg["phase_median_abs_ret12_difference"]<=0.06),
        ("B6","vgsix_phase_max_abs_ret_diff_le_0.10",sg["phase_max_abs_ret12_difference"],"<=0.10",sg["phase_max_abs_ret12_difference"]<=0.10),
    ]
    audit=pd.DataFrame(A+B,columns=["gate_family","test","observed","threshold","pass"])
    dual_pass=bool(audit["pass"].all())
    status="DUAL_BRIDGE_PASS_SUPPORTED_DEEP_PROXY_EXTENSION" if dual_pass else "DUAL_BRIDGE_FAIL_NO_DEEP_EXTENSION"
    audit["dual_bridge_status"]=status
    audit.to_csv(OUT/"DUAL_BRIDGE_GATE_AUDIT.csv",index=False)

    cand_met=metrics[metrics["asset"]==CANDIDATE].copy()
    cand_met["asset_id"]=CANDIDATE
    cand_met["dual_bridge_status"]=status
    cand_met["evidence_status"]="DEEP_PROXY_EXTENSION_ACTIVE" if dual_pass else "NOT_PROMOTED_DUAL_BRIDGE_FAIL"
    cand_met.to_csv(OUT/"FRESX_EXTENDED_PHASE_METRICS.csv",index=False)

    sums=[]
    for anchor,g in cand_met.groupby("anchor"):
        w=g["episode_weight"].to_numpy(float)
        nlegs=g["cycle_id"].nunique(); nb=g["broad_episode_id"].nunique()
        if dual_pass:
            support="SUPPORTED_DEEP_PROXY_DESCRIPTIVE" if nlegs>=5 and nb>=4 else ("LIMITED_DEEP_PROXY_DESCRIPTIVE" if nb>=2 else "INSUFFICIENT_SUPPORT")
        else:
            support="NOT_PROMOTED_DUAL_BRIDGE_FAIL"
        valid=g.dropna(subset=["mdd_trough_month"])
        late=(
            valid.loc[valid["mdd_trough_month"].between(7,12),"episode_weight"].sum()/valid["episode_weight"].sum()
            if len(valid) and valid["episode_weight"].sum()>0 else np.nan
        )
        sums.append({
            "asset_id":CANDIDATE,"anchor":anchor,
            "n_legs":int(nlegs),"n_broad_episodes":int(nb),
            "support_status":support,"dual_bridge_status":status,
            "weighted_median_ret_3m":weighted_median(g["ret_3m"],w),
            "weighted_median_ret_6m":weighted_median(g["ret_6m"],w),
            "weighted_median_ret_12m":weighted_median(g["ret_12m"],w),
            "weighted_median_mdd_12m":weighted_median(g["mdd_12m"],w),
            "weighted_median_mdd_trough_month":weighted_median(valid["mdd_trough_month"],valid["episode_weight"]) if len(valid) else np.nan,
            "weighted_late_trough_share_7_12":late,
        })
    ext=pd.DataFrame(sums).set_index("anchor").loc[PHASES].reset_index()
    ext.to_csv(OUT/"FRESX_EXTENDED_PHASE_SUMMARY.csv",index=False)

    # 24M diagnostics.
    pmap=dict(zip(monthly[CANDIDATE]["period"],monthly[CANDIDATE]["value"].astype(float)))
    anchor_cols={"FIRST_HIKE":"first_hike","LAST_HIKE":"last_hike","PAUSE_START":"pause_start","FIRST_CUT":"first_cut"}
    rows24=[]
    for anchor,col in anchor_cols.items():
        tmp=[]
        for _,cyc in cycles.iterrows():
            dt=cyc[col]
            if pd.isna(dt): continue
            m=liquid_24(pmap,dt)
            if m is not None: tmp.append((cyc,pd.Timestamp(dt),m))
        counts={}
        for cyc,_,_ in tmp:
            bid=cyc["broad_episode_id"]; counts[bid]=counts.get(bid,0)+1
        for cyc,dt,m in tmp:
            rows24.append({
                "asset_id":CANDIDATE,"anchor":anchor,"cycle_id":cyc["cycle_id"],
                "broad_episode_id":cyc["broad_episode_id"],"anchor_date":dt,
                "episode_weight":1.0/counts[cyc["broad_episode_id"]],
                **m,"diagnostic_status":"SECONDARY_24M_DESCRIPTIVE",
                "dual_bridge_status":status,
            })
    pd.DataFrame(rows24).to_csv(OUT/"FRESX_24M_DIAGNOSTICS.csv",index=False)

    s=ext.set_index("anchor")
    def pct(v): return f"{v*100:+.1f}%"
    def mth(v): return "NA" if pd.isna(v) else f"M{int(round(v))}"

    qrows=[
        ("REITD-Q01","Did the FRESX dual bridge pass?",status,"DUAL_BRIDGE"),
        ("REITD-Q02","How close is FRESX to VNQ monthly?",f"{diag_vnq['matched_return_months']} months; Pearson {diag_vnq['pearson_monthly_return']:.3f}; Spearman {diag_vnq['spearman_monthly_return']:.3f}; beta {diag_vnq['descriptive_beta_candidate_on_reference']:.3f}.","VNQ_BRIDGE"),
        ("REITD-Q03","How close is FRESX to VGSIX monthly?",f"{diag_vgsix['matched_return_months']} months; Pearson {diag_vgsix['pearson_monthly_return']:.3f}; Spearman {diag_vgsix['spearman_monthly_return']:.3f}; beta {diag_vgsix['descriptive_beta_candidate_on_reference']:.3f}.","VGSIX_BRIDGE"),
        ("REITD-Q04","Do Fed-event outcomes agree with VNQ?",f"12M sign {sv['ret12_sign_agreement']:.0%}; return corr {sv['ret12_correlation']:.3f}; MDD corr {sv['mdd_correlation']:.3f}.","VNQ_EVENT"),
        ("REITD-Q05","Do Fed-event outcomes agree with VGSIX?",f"12M sign {sg['ret12_sign_agreement']:.0%}; return corr {sg['ret12_correlation']:.3f}; MDD corr {sg['mdd_correlation']:.3f}.","VGSIX_EVENT"),
        ("REITD-Q06","What does deep history show at FIRST_HIKE?",f"12M {pct(s.loc['FIRST_HIKE','weighted_median_ret_12m'])}; MDD {s.loc['FIRST_HIKE','weighted_median_mdd_12m']*100:.1f}%; trough {mth(s.loc['FIRST_HIKE','weighted_median_mdd_trough_month'])}; support {s.loc['FIRST_HIKE','support_status']}.","PHASE"),
        ("REITD-Q07","What does it show at LAST_HIKE?",f"12M {pct(s.loc['LAST_HIKE','weighted_median_ret_12m'])}; MDD {s.loc['LAST_HIKE','weighted_median_mdd_12m']*100:.1f}%.","PHASE"),
        ("REITD-Q08","What does it show at PAUSE_START?",f"12M {pct(s.loc['PAUSE_START','weighted_median_ret_12m'])}; MDD {s.loc['PAUSE_START','weighted_median_mdd_12m']*100:.1f}%.","PHASE"),
        ("REITD-Q09","What does it show at FIRST_CUT?",f"12M {pct(s.loc['FIRST_CUT','weighted_median_ret_12m'])}; MDD {s.loc['FIRST_CUT','weighted_median_mdd_12m']*100:.1f}%.","PHASE"),
        ("REITD-Q10","Can FRESX be called VNQ?","No. FRESX remains an active real-estate proxy in all historical periods.","BOUNDARY"),
        ("REITD-Q11","Does deep-history support create a forecast?","No. It only strengthens historical descriptive coverage if both bridges pass.","BOUNDARY"),
        ("REITD-Q12","What should PandaAI show?","Show active-proxy label, dual-bridge status, both bridge diagnostics, phase/path distributions, support status and non-forecast boundary.","PANDAAI"),
    ]
    pd.DataFrame(qrows,columns=["question_id","question_en","answer","evidence_layer"]).to_csv(OUT/"REIT_DEEP_HISTORY_INVESTOR_QUESTIONS.csv",index=False)

    if dual_pass:
        lines=[
            "# REIT Deep-History Dual Bridge — 037",
            "",
            f"**{status}**",
            "",
            f"FRESX↔VNQ：Pearson {diag_vnq['pearson_monthly_return']:.3f}，Spearman {diag_vnq['spearman_monthly_return']:.3f}；事件12M收益相关 {sv['ret12_correlation']:.3f}，MDD相关 {sv['mdd_correlation']:.3f}。",
            "",
            f"FRESX↔VGSIX：Pearson {diag_vgsix['pearson_monthly_return']:.3f}，Spearman {diag_vgsix['spearman_monthly_return']:.3f}；事件12M收益相关 {sg['ret12_correlation']:.3f}，MDD相关 {sg['mdd_correlation']:.3f}。",
            "",
            "因此FRESX可以作为**主动管理的深历史上市房地产代理**扩展1987+周期研究，但始终不能写成VNQ历史。",
            "",
            "## 四阶段深历史代理",
            "",
        ]
        for a,label in [("FIRST_HIKE","加息启动"),("LAST_HIKE","最后一次加息"),("PAUSE_START","暂停"),("FIRST_CUT","第一次降息")]:
            r=s.loc[a]
            lines += [
                f"### {a}｜{label}",
                "",
                f"- 12M中位：{pct(r.weighted_median_ret_12m)}",
                f"- 12M MDD中位：{r.weighted_median_mdd_12m*100:.1f}%",
                f"- trough：{mth(r.weighted_median_mdd_trough_month)}",
                f"- 样本：{int(r.n_legs)} legs / {int(r.n_broad_episodes)} broad episodes",
                f"- support：{r.support_status}",
                "",
            ]
        lines += [
            "## 解释边界",
            "",
            "FRESX是主动基金。双桥通过只说明它在重叠历史中对上市房地产/REIT周期暴露足够相似，可用于扩展描述性历史；它不等于VNQ，也不能把主动管理贡献视为零。",
        ]
    else:
        failed=", ".join(audit.loc[~audit["pass"],"test"].tolist())
        lines=[
            "# REIT Deep-History Dual Bridge — 037",
            "",
            f"**{status}**",
            "",
            f"未通过的冻结gate：{failed}",
            "",
            "因此FRESX不会被用于升级1987+ REIT证据。036的VGSIX/VNQ结果保持原状态。",
        ]
    (OUT/"REIT_DEEP_HISTORY_SYNTHESIS_ZH.md").write_text("\n".join(lines)+"\n")

    schema={
        "module":"FED-CYCLE-REIT-DEEP-HISTORY-DUAL-BRIDGE-037",
        "dual_bridge_status":status,
        "target":"VNQ",
        "reference":"VGSIX_REIT_PROXY",
        "deep_proxy":"FRESX_REIT_ACTIVE_PROXY",
        "active_management_caveat":True,
        "prohibited_outputs":[
            "pre2004_vnq_label","expected_reit_return","best_reit_phase",
            "reit_buying_instruction","national_house_price_substitution"
        ],
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"PANDAAI_REIT_DEEP_HISTORY_SCHEMA.json").write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# FED-CYCLE-REIT-DEEP-HISTORY-DUAL-BRIDGE-037 — REPORT",
        "",
        "## Status",
        "",
        f"**{status} / ACTIVE-FUND DUAL MEASUREMENT BRIDGE / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- FRESX first date: {ffirst.date()}",
        f"- VNQ overlap months: {diag_vnq['matched_return_months']}",
        f"- VGSIX overlap months: {diag_vgsix['matched_return_months']}",
        f"- VNQ monthly Pearson: {diag_vnq['pearson_monthly_return']:.4f}",
        f"- VGSIX monthly Pearson: {diag_vgsix['pearson_monthly_return']:.4f}",
        f"- VNQ event return corr: {sv['ret12_correlation']:.4f}",
        f"- VGSIX event return corr: {sg['ret12_correlation']:.4f}",
        f"- all dual gates pass: {dual_pass}",
        "",
        "FRESX remains explicitly labeled as an active listed-real-estate proxy.",
    ]
    (OUT/"FED_CYCLE_REIT_DEEP_HISTORY_DUAL_BRIDGE_037_REPORT.md").write_text("\n".join(report)+"\n")

    if str(ov_vnq.index.max())!=str(LAST_COMPLETE_MONTH) or str(ov_vgsix.index.max())!=str(LAST_COMPLETE_MONTH):
        raise RuntimeError("incomplete current month handling failed")
    if dual_pass and (ext["support_status"]=="NOT_PROMOTED_DUAL_BRIDGE_FAIL").any():
        raise RuntimeError("dual pass incorrectly suppressed deep proxy")
    if not dual_pass and (ext["support_status"]!="NOT_PROMOTED_DUAL_BRIDGE_FAIL").any():
        raise RuntimeError("failed dual bridge promoted evidence")
    if (cand_met["asset_id"]!=CANDIDATE).any():
        raise RuntimeError("FRESX proxy identity lost")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-REIT-DEEP-HISTORY-DUAL-BRIDGE-037",
        "upstream_qc":{"014":q014["qc_gate"],"032":q032["qc_gate"],"036":q036["qc_gate"]},
        "upstream_036_bridge_status":q036.get("bridge_status"),
        "dual_bridge_status":status,
        "source_rows":int(len(preg)),
        "source_hashes_complete":bool(preg["sha256"].str.len().eq(64).all()),
        "fresx_first_date":str(ffirst.date()),
        "partial_current_month_used":False,
        "vnq_bridge":diag_vnq,
        "vgsix_bridge":diag_vgsix,
        "vnq_event_stats":sv,
        "vgsix_event_stats":sg,
        "all_dual_bridge_tests_pass":dual_pass,
        "extended_event_rows":int(len(cand_met)),
        "support_status_by_phase":dict(zip(ext["anchor"],ext["support_status"])),
        "pre2004_rows_labeled_vnq":0,
        "active_management_caveat_retained":True,
        "national_house_price_substituted":False,
        "best_phase_outputs":0,
        "expected_return_forecasts":0,
        "reit_buying_recommendations":0,
        "new_pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
