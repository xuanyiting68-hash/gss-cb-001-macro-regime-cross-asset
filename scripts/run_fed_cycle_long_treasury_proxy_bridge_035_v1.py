#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_long_treasury_proxy_bridge_035_v1"
OUT.mkdir(parents=True,exist_ok=True)

Q014=ROOT/"results"/"fed_cycle_cross_asset_expansion_v1"/"QC.json"
Q032=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"/"QC.json"
SPEC=ROOT/"data"/"public"/"LONG_TREASURY_PROXY_SOURCE_SPEC_20260926.csv"

AS_OF=pd.Timestamp("2026-09-26")
LAST_COMPLETE_MONTH=AS_OF.to_period("M")-1
PHASES=["FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"]
PROXY_ID="VUSTX_LONG_TREASURY_PROXY"

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

EXP=load_module(ROOT/"scripts"/"run_fed_cycle_cross_asset_expansion_v1.py","exp014_for_035")

def direction(v):
    if pd.isna(v):
        return "NA"
    if v>0.02:
        return "POSITIVE"
    if v<-0.02:
        return "NEGATIVE"
    return "NEUTRAL"

def weighted_median(values,weights):
    return EXP.weighted_quantile(values,weights,0.5)

def common_weights(df):
    out=df.copy()
    counts=out.groupby(["anchor","broad_episode_id"])["cycle_id"].transform("count")
    out["common_episode_weight"]=1.0/counts
    return out

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
        "mdd_trough_month_24m":int(np.argmax(dd)) if float(dd.max())>1e-15 else np.nan
    }

def main():
    q014=read_pass(Q014); q032=read_pass(Q032)
    srcspec=pd.read_csv(SPEC)
    if set(srcspec["symbol"])!={"TLT","VUSTX"}:
        raise RuntimeError("source spec changed")

    fetched={}
    prov=[]
    for r in srcspec.itertuples(index=False):
        df,meta=EXP.fetch_yahoo(r.symbol,adjusted=True)
        fetched[r.asset_id]={"df":df,"meta":meta}
        prov.append({
            "asset_id":r.asset_id,"symbol":r.symbol,"role":r.role,
            "source":r.source,"source_context_url":r.source_context_url,
            "price_history_url":meta["url"],"acquisition_method":meta["method"],
            "price_field":meta["price_field"],
            "retrieved_utc":datetime.now(timezone.utc).isoformat(),
            "sha256":meta["sha256"],"raw_bytes":meta["raw_bytes"],
            "rows_total":len(df),"first_date":str(df["date"].min().date()),
            "last_date":str(df["date"].max().date()),"raw_committed":False
        })
    preg=pd.DataFrame(prov)
    if len(preg)!=2 or preg["sha256"].str.len().ne(64).any():
        raise RuntimeError("source provenance failure")
    vfirst=pd.Timestamp(preg.loc[preg["asset_id"]==PROXY_ID,"first_date"].iloc[0])
    if vfirst>pd.Timestamp("1986-06-30"):
        raise RuntimeError(f"VUSTX history begins too late: {vfirst}")
    preg.to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)

    # Monthly average, with incomplete current month excluded from validation/evidence.
    monthly={}
    for aid,obj in fetched.items():
        m=EXP.monthly_average(obj["df"])
        m=m[m["period"]<=LAST_COMPLETE_MONTH].copy()
        monthly[aid]=m

    tlt=monthly["TLT"].set_index("period")["value"].astype(float)
    vus=monthly[PROXY_ID].set_index("period")["value"].astype(float)
    tr=tlt.pct_change(fill_method=None).rename("tlt_monthly_ret")
    vr=vus.pct_change(fill_method=None).rename("vustx_monthly_ret")
    ov=pd.concat([tr,vr],axis=1,join="inner").dropna()
    if ov.empty:
        raise RuntimeError("no monthly overlap")
    pearson=float(ov["tlt_monthly_ret"].corr(ov["vustx_monthly_ret"],method="pearson"))
    spearman=float(ov["tlt_monthly_ret"].corr(ov["vustx_monthly_ret"],method="spearman"))
    beta,intercept=np.polyfit(ov["tlt_monthly_ret"].to_numpy(),ov["vustx_monthly_ret"].to_numpy(),1)
    ov["abs_return_diff"]=abs(ov["vustx_monthly_ret"]-ov["tlt_monthly_ret"])

    overlap_diag=pd.DataFrame([{
        "matched_return_months":len(ov),
        "first_return_month":str(ov.index.min()),
        "last_return_month":str(ov.index.max()),
        "last_complete_month_required":str(LAST_COMPLETE_MONTH),
        "pearson_monthly_return":pearson,
        "spearman_monthly_return":spearman,
        "descriptive_beta_vustx_on_tlt":float(beta),
        "descriptive_intercept":float(intercept),
        "median_abs_monthly_return_diff":float(ov["abs_return_diff"].median()),
        "mean_abs_monthly_return_diff":float(ov["abs_return_diff"].mean()),
        "current_partial_month_used":False
    }])
    overlap_diag.to_csv(OUT/"MONTHLY_OVERLAP_DIAGNOSTICS.csv",index=False)

    cycles=EXP.load_cycles()
    if any(pd.to_datetime(cycles["first_hike"]).dt.year>=2026):
        raise RuntimeError("current 2026 candidate leaked into frozen cycles")

    assets={
        "TLT":{"df":monthly["TLT"],"label":"TLT target","source":"fresh Yahoo adjusted close"},
        PROXY_ID:{"df":monthly[PROXY_ID],"label":"VUSTX long-duration Treasury proxy","source":"fresh Yahoo adjusted close"}
    }
    met,_=EXP.build_market(cycles,assets)
    common=met[met["asset"]=="TLT"].merge(
        met[met["asset"]==PROXY_ID],
        on=["anchor","cycle_id","broad_episode_id","anchor_date"],
        suffixes=("_tlt","_vustx"),
        validate="one_to_one"
    )
    if common.empty:
        raise RuntimeError("no common phase events")
    common=common_weights(common)

    common["ret12_diff"]=common["ret_12m_vustx"]-common["ret_12m_tlt"]
    common["abs_ret12_diff"]=abs(common["ret12_diff"])
    common["mdd_diff"]=common["mdd_12m_vustx"]-common["mdd_12m_tlt"]
    common["abs_mdd_diff"]=abs(common["mdd_diff"])
    common["ret12_sign_agree"]=(np.sign(common["ret_12m_vustx"])==np.sign(common["ret_12m_tlt"])).astype(float)
    common.to_csv(OUT/"COMMON_EVENT_BRIDGE_PANEL.csv",index=False)

    event_sign_agree=float(common["ret12_sign_agree"].mean())
    event_ret_corr=float(common["ret_12m_tlt"].corr(common["ret_12m_vustx"]))
    event_abs_ret_med=float(common["abs_ret12_diff"].median())
    mdd_corr=float(common["mdd_12m_tlt"].corr(common["mdd_12m_vustx"]))
    mdd_abs_med=float(common["abs_mdd_diff"].median())

    # Common-sample phase summaries.
    ps=[]
    for anchor in PHASES:
        g=common[common["anchor"]==anchor].copy()
        if g.empty:
            continue
        w=g["common_episode_weight"].to_numpy(float)
        tlt12=weighted_median(g["ret_12m_tlt"],w)
        vus12=weighted_median(g["ret_12m_vustx"],w)
        tltmdd=weighted_median(g["mdd_12m_tlt"],w)
        vusmdd=weighted_median(g["mdd_12m_vustx"],w)
        ps.append({
            "anchor":anchor,"n_common_events":len(g),"n_common_broad_episodes":g["broad_episode_id"].nunique(),
            "tlt_weighted_median_ret_12m":tlt12,
            "vustx_weighted_median_ret_12m":vus12,
            "ret12_abs_diff":abs(vus12-tlt12),
            "tlt_direction":direction(tlt12),"vustx_direction":direction(vus12),
            "direction_agree":direction(tlt12)==direction(vus12),
            "tlt_weighted_median_mdd_12m":tltmdd,
            "vustx_weighted_median_mdd_12m":vusmdd,
            "mdd_abs_diff":abs(vusmdd-tltmdd)
        })
    psum=pd.DataFrame(ps)
    if len(psum)!=4 or set(psum["anchor"])!=set(PHASES):
        raise RuntimeError("common phase summary must contain four phases")
    psum.to_csv(OUT/"COMMON_PHASE_BRIDGE_SUMMARY.csv",index=False)

    phase_med_abs=float(psum["ret12_abs_diff"].median())
    phase_max_abs=float(psum["ret12_abs_diff"].max())
    phase_dir_all=bool(psum["direction_agree"].all())

    gates=[
        ("G1","overlap_months_ge_240",len(ov),">=240",len(ov)>=240),
        ("G2","pearson_monthly_ge_0.95",pearson,">=0.95",pearson>=0.95),
        ("G2","spearman_monthly_ge_0.95",spearman,">=0.95",spearman>=0.95),
        ("G3","beta_in_0.75_1.25",float(beta),"[0.75,1.25]",0.75<=beta<=1.25),
        ("G3","abs_intercept_le_0.0025",abs(float(intercept)),"<=0.0025",abs(intercept)<=0.0025),
        ("G4","event_ret12_sign_agreement_ge_0.85",event_sign_agree,">=0.85",event_sign_agree>=0.85),
        ("G4","event_ret12_corr_ge_0.90",event_ret_corr,">=0.90",event_ret_corr>=0.90),
        ("G4","event_ret12_median_abs_diff_le_0.05",event_abs_ret_med,"<=0.05",event_abs_ret_med<=0.05),
        ("G5","event_mdd_corr_ge_0.80",mdd_corr,">=0.80",mdd_corr>=0.80),
        ("G5","event_mdd_median_abs_diff_le_0.04",mdd_abs_med,"<=0.04",mdd_abs_med<=0.04),
        ("G6","four_phase_direction_agreement",int(phase_dir_all),"true",phase_dir_all),
        ("G6","phase_median_abs_ret12_diff_le_0.04",phase_med_abs,"<=0.04",phase_med_abs<=0.04),
        ("G6","phase_max_abs_ret12_diff_le_0.07",phase_max_abs,"<=0.07",phase_max_abs<=0.07),
    ]
    ga=pd.DataFrame(gates,columns=["gate_family","test","observed","threshold","pass"])
    bridge_pass=bool(ga["pass"].all())
    bridge_status="BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION" if bridge_pass else "BRIDGE_FAIL_NO_HISTORY_EXTENSION"
    ga["bridge_status"]=bridge_status
    ga.to_csv(OUT/"BRIDGE_GATE_AUDIT.csv",index=False)

    # Full VUSTX history metrics; never label as TLT.
    proxy_met=met[met["asset"]==PROXY_ID].copy()
    proxy_met["asset_id"]=PROXY_ID
    proxy_met["bridge_status"]=bridge_status
    proxy_met["evidence_status"]="PROXY_EXTENSION_ACTIVE" if bridge_pass else "NOT_PROMOTED_BRIDGE_FAIL"
    proxy_met.to_csv(OUT/"VUSTX_EXTENDED_PHASE_METRICS.csv",index=False)

    sums=[]
    for anchor,g in proxy_met.groupby("anchor"):
        w=g["episode_weight"].to_numpy(float)
        nlegs=g["cycle_id"].nunique(); nb=g["broad_episode_id"].nunique()
        if bridge_pass:
            support="SUPPORTED_PROXY_DESCRIPTIVE" if nlegs>=5 and nb>=4 else ("LIMITED_PROXY_DESCRIPTIVE" if nb>=2 else "INSUFFICIENT_SUPPORT")
        else:
            support="NOT_PROMOTED_BRIDGE_FAIL"
        valid=g.dropna(subset=["mdd_trough_month"])
        late=(
            valid.loc[valid["mdd_trough_month"].between(7,12),"episode_weight"].sum()/valid["episode_weight"].sum()
            if len(valid) and valid["episode_weight"].sum()>0 else np.nan
        )
        sums.append({
            "asset_id":PROXY_ID,"anchor":anchor,"n_legs":int(nlegs),"n_broad_episodes":int(nb),
            "support_status":support,"bridge_status":bridge_status,
            "weighted_median_ret_3m":weighted_median(g["ret_3m"],w),
            "weighted_median_ret_6m":weighted_median(g["ret_6m"],w),
            "weighted_median_ret_12m":weighted_median(g["ret_12m"],w),
            "weighted_median_mdd_12m":weighted_median(g["mdd_12m"],w),
            "weighted_median_mdd_trough_month":weighted_median(valid["mdd_trough_month"],valid["episode_weight"]) if len(valid) else np.nan,
            "weighted_late_trough_share_7_12":late
        })
    ext_sum=pd.DataFrame(sums).set_index("anchor").loc[PHASES].reset_index()
    ext_sum.to_csv(OUT/"VUSTX_EXTENDED_PHASE_SUMMARY.csv",index=False)

    # Secondary 24M diagnostics on full proxy history.
    pmap=dict(zip(monthly[PROXY_ID]["period"],monthly[PROXY_ID]["value"].astype(float)))
    r24=[]
    anchor_cols={"FIRST_HIKE":"first_hike","LAST_HIKE":"last_hike","PAUSE_START":"pause_start","FIRST_CUT":"first_cut"}
    for anchor,col in anchor_cols.items():
        tmp=[]
        for _,cyc in cycles.iterrows():
            dt=cyc[col]
            if pd.isna(dt):
                continue
            m=liquid_24(pmap,dt)
            if m is not None:
                tmp.append((cyc,pd.Timestamp(dt),m))
        counts={}
        for cyc,_,_ in tmp:
            bid=cyc["broad_episode_id"]; counts[bid]=counts.get(bid,0)+1
        for cyc,dt,m in tmp:
            r24.append({
                "asset_id":PROXY_ID,"anchor":anchor,"cycle_id":cyc["cycle_id"],
                "broad_episode_id":cyc["broad_episode_id"],"anchor_date":dt,
                "episode_weight":1.0/counts[cyc["broad_episode_id"]],
                **m,"diagnostic_status":"SECONDARY_24M_DESCRIPTIVE",
                "bridge_status":bridge_status
            })
    d24=pd.DataFrame(r24)
    d24.to_csv(OUT/"VUSTX_24M_DIAGNOSTICS.csv",index=False)

    sidx=ext_sum.set_index("anchor")
    def pp(v): return f"{v*100:+.1f}%"
    def mm(v): return "NA" if pd.isna(v) else f"M{int(round(v))}"

    qrows=[
        ("TSY-Q01","Did the proxy bridge pass?",bridge_status,"BRIDGE"),
        ("TSY-Q02","How similar are monthly TLT and VUSTX returns?",f"Matched months {len(ov)}; Pearson {pearson:.3f}; Spearman {spearman:.3f}; beta {beta:.3f}; monthly intercept {intercept:+.5f}.","BRIDGE"),
        ("TSY-Q03","Do common Fed-cycle event outcomes agree?",f"12M event sign agreement {event_sign_agree:.0%}; return correlation {event_ret_corr:.3f}; median absolute 12M-return difference {event_abs_ret_med*100:.2f}pp; MDD correlation {mdd_corr:.3f}.","BRIDGE"),
        ("TSY-Q04","What does the longer proxy show at FIRST_HIKE?",f"VUSTX proxy 12M median {pp(sidx.loc['FIRST_HIKE','weighted_median_ret_12m'])}; MDD {sidx.loc['FIRST_HIKE','weighted_median_mdd_12m']*100:.1f}%; trough {mm(sidx.loc['FIRST_HIKE','weighted_median_mdd_trough_month'])}; support {sidx.loc['FIRST_HIKE','support_status']}.","PHASE"),
        ("TSY-Q05","What does it show at LAST_HIKE?",f"12M median {pp(sidx.loc['LAST_HIKE','weighted_median_ret_12m'])}; MDD {sidx.loc['LAST_HIKE','weighted_median_mdd_12m']*100:.1f}%; trough {mm(sidx.loc['LAST_HIKE','weighted_median_mdd_trough_month'])}.","PHASE"),
        ("TSY-Q06","What does it show at PAUSE_START?",f"12M median {pp(sidx.loc['PAUSE_START','weighted_median_ret_12m'])}; MDD {sidx.loc['PAUSE_START','weighted_median_mdd_12m']*100:.1f}%; trough {mm(sidx.loc['PAUSE_START','weighted_median_mdd_trough_month'])}.","PHASE"),
        ("TSY-Q07","What does it show at FIRST_CUT?",f"12M median {pp(sidx.loc['FIRST_CUT','weighted_median_ret_12m'])}; MDD {sidx.loc['FIRST_CUT','weighted_median_mdd_12m']*100:.1f}%; trough {mm(sidx.loc['FIRST_CUT','weighted_median_mdd_trough_month'])}.","PHASE"),
        ("TSY-Q08","Can pre-2002 proxy returns be called TLT returns?","No. Pre-2002 observations remain VUSTX_LONG_TREASURY_PROXY even if the engineering bridge passes.","BOUNDARY"),
        ("TSY-Q09","Does a bridge pass imply a bond forecast?","No. The bridge validates historical measurement similarity only; phase medians remain descriptive distributions.","BOUNDARY"),
        ("TSY-Q10","What should PandaAI show?","Show proxy label, bridge status/gates, sample support, phase return/path-risk distributions and explicit non-forecast boundary. Never relabel proxy history as TLT.","PANDAAI"),
    ]
    pd.DataFrame(qrows,columns=["question_id","question_en","answer","evidence_layer"]).to_csv(OUT/"LONG_TREASURY_INVESTOR_QUESTIONS.csv",index=False)

    if bridge_pass:
        narrative=[
            "# Long-Duration Treasury Proxy Bridge — 035",
            "",
            "## Bridge result",
            "",
            f"**{bridge_status}**",
            "",
            f"TLT与VUSTX在完整重叠月的月收益相关性：Pearson {pearson:.3f}，Spearman {spearman:.3f}；描述性beta {beta:.3f}，intercept {intercept:+.5f}。",
            "",
            f"共同Fed事件的12M收益方向一致率 {event_sign_agree:.0%}，事件12M收益相关 {event_ret_corr:.3f}，MDD相关 {mdd_corr:.3f}。",
            "",
            "因此可以把VUSTX作为**长期美债duration proxy**扩展1987+历史，但不能把1986–2001的VUSTX叫做TLT。",
            "",
            "## 四阶段长历史代理",
            "",
        ]
        for a,label in [("FIRST_HIKE","加息启动"),("LAST_HIKE","最后一次加息"),("PAUSE_START","暂停"),("FIRST_CUT","第一次降息")]:
            r=sidx.loc[a]
            narrative += [
                f"### {a}｜{label}",
                "",
                f"- 12M中位：{pp(r.weighted_median_ret_12m)}",
                f"- 12M MDD中位：{r.weighted_median_mdd_12m*100:.1f}%",
                f"- MDD低点月中位：{mm(r.weighted_median_mdd_trough_month)}",
                f"- 样本：{int(r.n_legs)} legs / {int(r.n_broad_episodes)} broad episodes",
                f"- evidence：{r.support_status}",
                "",
            ]
        narrative += [
            "## 边界",
            "",
            "这个桥接解决的是**历史测量长度**，不是预测问题。VUSTX与TLT费用、结构、久期和执行载体并不完全相同；bridge pass只允许我们研究更长的long-duration Treasury proxy分布。",
        ]
    else:
        failed=", ".join(ga.loc[~ga["pass"],"test"].tolist())
        narrative=[
            "# Long-Duration Treasury Proxy Bridge — 035",
            "",
            f"**{bridge_status}**",
            "",
            f"未通过的冻结gate：{failed}",
            "",
            "因此VUSTX不会被用于升级长期美债Fed-cycle证据；TLT仍保留原有LIMITED_DESCRIPTIVE状态。",
        ]
    (OUT/"LONG_TREASURY_SYNTHESIS_ZH.md").write_text("\n".join(narrative)+"\n")

    schema={
        "module":"FED-CYCLE-LONG-TREASURY-PROXY-BRIDGE-035",
        "bridge_status":bridge_status,
        "proxy_asset_id":PROXY_ID,
        "target_asset_id":"TLT",
        "allowed_if_bridge_pass":[
            "historical_proxy_phase_distribution","proxy_path_risk","proxy_sample_support"
        ],
        "prohibited_outputs":[
            "pre2002_tlt_label","expected_return","best_bond_phase","bond_buying_instruction"
        ],
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"PANDAAI_LONG_TREASURY_SCHEMA.json").write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# FED-CYCLE-LONG-TREASURY-PROXY-BRIDGE-035 — REPORT",
        "",
        "## Status",
        "",
        f"**{bridge_status} / MEASUREMENT BRIDGE / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- overlap monthly returns: {len(ov)}",
        f"- Pearson monthly return: {pearson:.4f}",
        f"- Spearman monthly return: {spearman:.4f}",
        f"- descriptive beta: {beta:.4f}",
        f"- common event rows: {len(common)}",
        f"- event 12M sign agreement: {event_sign_agree:.1%}",
        f"- event 12M correlation: {event_ret_corr:.4f}",
        f"- event MDD correlation: {mdd_corr:.4f}",
        f"- all frozen bridge tests pass: {bridge_pass}",
        "",
        "No pre-2002 VUSTX observation is labeled TLT.",
    ]
    (OUT/"FED_CYCLE_LONG_TREASURY_PROXY_BRIDGE_035_REPORT.md").write_text("\n".join(report)+"\n")

    # QC.
    if str(ov.index.max())!=str(LAST_COMPLETE_MONTH):
        raise RuntimeError(f"bridge last month is not last complete month: {ov.index.max()}")
    if any(pd.to_datetime(cycles["first_hike"]).dt.year>=2026):
        raise RuntimeError("current 2026 candidate leak")
    if bridge_pass and not (ext_sum["support_status"]=="SUPPORTED_PROXY_DESCRIPTIVE").all():
        raise RuntimeError("passing bridge did not yield supported proxy summaries")
    if not bridge_pass and (ext_sum["support_status"]!="NOT_PROMOTED_BRIDGE_FAIL").any():
        raise RuntimeError("failed bridge promoted proxy evidence")
    if (proxy_met["asset_id"]!="VUSTX_LONG_TREASURY_PROXY").any():
        raise RuntimeError("proxy identity lost")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-LONG-TREASURY-PROXY-BRIDGE-035",
        "upstream_qc":{"014":q014["qc_gate"],"032":q032["qc_gate"]},
        "bridge_status":bridge_status,
        "source_rows":int(len(preg)),
        "source_hashes_complete":bool(preg["sha256"].str.len().eq(64).all()),
        "vustx_first_date":str(vfirst.date()),
        "last_complete_bridge_month":str(ov.index.max()),
        "partial_current_month_used":False,
        "overlap_monthly_returns":int(len(ov)),
        "pearson_monthly_return":pearson,
        "spearman_monthly_return":spearman,
        "descriptive_beta":float(beta),
        "descriptive_intercept":float(intercept),
        "common_event_rows":int(len(common)),
        "event_ret12_sign_agreement":event_sign_agree,
        "event_ret12_correlation":event_ret_corr,
        "event_ret12_median_abs_difference":event_abs_ret_med,
        "event_mdd_correlation":mdd_corr,
        "event_mdd_median_abs_difference":mdd_abs_med,
        "phase_direction_all_agree":phase_dir_all,
        "phase_median_abs_ret12_difference":phase_med_abs,
        "phase_max_abs_ret12_difference":phase_max_abs,
        "all_bridge_tests_pass":bridge_pass,
        "proxy_extended_rows":int(len(proxy_met)),
        "pre2002_rows_labeled_tlt":0,
        "yield_change_substituted_for_total_return":False,
        "best_phase_outputs":0,
        "expected_return_forecasts":0,
        "bond_buying_recommendations":0,
        "new_pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
