#!/usr/bin/env python3
"""
ENERGY-WEEKLY-STATE-004
Strict-PIT weekly price rollover x stock-flow mechanism test.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"energy_weekly_state_v1"
OUT.mkdir(parents=True,exist_ok=True)

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

PRICE=load_module(ROOT/"scripts"/"run_energy_price_walkforward.py","price_weekly_state")
FLOW=load_module(ROOT/"scripts"/"run_energy_flow_decomposition_v2.py","flow_weekly_state")

PIT_QC=ROOT/"results"/"energy_weekly_pit_v1"/"QC.json"
PIT_REG=ROOT/"results"/"energy_weekly_pit_v1"/"WPSR_RELEASE_REGISTRY.csv"

DAILY={
    "WTI":"DCOILWTICO",
    "GAS":"DGASUSGULF",
    "HEAT":"DHOILNYH",
    "JET":"DJFUELUSGULF",
}
WEEKLY={
    "CRUDE_STOCK":"WCESTUS1",
    "GAS_STOCK":"WGTSTUS1",
    "DIST_STOCK":"WDISTUS1",
    "REFINERY_UTIL":"WPULEUS3",
    "GAS_DEMAND":"WGFUPUS2",
    "DIST_DEMAND":"WDIUPUS2",
    "JET_DEMAND":"WKJUPUS2",
    "REFINERY_INPUT":"WCRRIUS2",
    "FIELD_PROD":"WCRFPUS2",
    "CRUDE_IMPORTS":"WCRIMUS2",
}
PRIMARY=[
    ("wti_fwd_8w","return"),
    ("wti_fwd_13w","return"),
    ("short_mae_8w","mae"),
    ("short_mae_13w","mae"),
]

def expanding_z_prior(s,min_prior=52):
    prior=s.shift(1)
    mu=prior.expanding(min_periods=min_prior).mean()
    sd=prior.expanding(min_periods=min_prior).std(ddof=1)
    return (s-mu)/sd

def build_daily_panel():
    frames=[]; provenance=[]
    for name,sid in DAILY.items():
        z,sha,url,method=PRICE.fetch_series(sid)
        z=z.rename(columns={"value":name})[["date",name]]
        frames.append(z)
        provenance.append({
            "name":name,"series_id":sid,"url":url,"sha256":sha,
            "acquisition_method":method,"frequency":"daily",
        })
    p=frames[0]
    for z in frames[1:]:
        p=p.merge(z,on="date",how="inner")
    p=p.dropna().sort_values("date").drop_duplicates("date",keep="last").reset_index(drop=True)
    p=p[(p[list(DAILY)]>0).all(axis=1)].copy()
    return p,pd.DataFrame(provenance)

def build_release_price_panel(reg,daily):
    rows=[]
    for _,r in reg.iterrows():
        release=pd.Timestamp(r.release_date).normalize()
        x=daily[daily.date<release]
        if len(x)<64:
            continue
        last=x.iloc[-1]
        row={
            "week_end":pd.Timestamp(r.week_end).normalize(),
            "release_date":release,
            "price_asof_date":pd.Timestamp(last.date).normalize(),
        }
        for name in DAILY:
            vals=x[name].to_numpy(float)
            row[f"{name}_r5"]=float(np.log(vals[-1]/vals[-6])*100.0)
            row[f"{name}_r63"]=float(np.log(vals[-1]/vals[-64])*100.0)
        rows.append(row)
    p=pd.DataFrame(rows).sort_values("release_date").reset_index(drop=True)
    for name in DAILY:
        p[f"{name}_z63"]=expanding_z_prior(p[f"{name}_r63"],52)
    p["pressure_score"]=p[[f"{x}_z63" for x in DAILY]].mean(axis=1,skipna=False)
    p["pressure_q90_prior"]=p.pressure_score.shift(1).expanding(min_periods=52).quantile(0.90)
    p["EXTREME"]=p.pressure_score>p.pressure_q90_prior
    p["recent_extreme_4"]=p.EXTREME.astype(int).rolling(4,min_periods=1).max().astype(bool)
    p["products_down_count"]=(p[["GAS_r5","HEAT_r5","JET_r5"]]<0).sum(axis=1)
    p["ROLLOVER_RAW"]=p.recent_extreme_4 & (p.WTI_r5<0) & (p.products_down_count>=2)

    selected=[]
    last=None
    for _,r in p.iterrows():
        flag=bool(r.ROLLOVER_RAW)
        ok=False
        if flag and (last is None or (r.release_date-last).days>91):
            ok=True; last=r.release_date
        selected.append(ok)
    p["SELECTED"]=selected
    return p

def seasonal_gap(df,we):
    return FLOW.seasonal_gap(df,pd.Timestamp(we))

def mechanism_for_event(event,reg,weekly):
    we=pd.Timestamp(event.week_end).normalize()
    idx=reg.index[reg.week_end==we]
    if len(idx)!=1:
        return {"mechanism_class":"DATA_INCOMPLETE","mechanism_complete":False}
    i=int(idx[0])
    if i<4:
        return {"mechanism_class":"DATA_INCOMPLETE","mechanism_complete":False}
    bwe=pd.Timestamp(reg.iloc[i-4].week_end).normalize()

    row={"baseline_week_end":bwe,"mechanism_complete":True}
    delta={}
    names=[
        "CRUDE_STOCK","GAS_STOCK","DIST_STOCK",
        "GAS_DEMAND","DIST_DEMAND","JET_DEMAND",
        "REFINERY_INPUT","FIELD_PROD","CRUDE_IMPORTS",
    ]
    for name in names:
        bv,bg,bn=seasonal_gap(weekly[name],bwe)
        cv,cg,cn=seasonal_gap(weekly[name],we)
        if not (np.isfinite(bg) and np.isfinite(cg)):
            row["mechanism_complete"]=False
        d=float(cg-bg) if np.isfinite(bg) and np.isfinite(cg) else np.nan
        delta[name]=d
        row.update({
            f"{name.lower()}_baseline_gap":bg,
            f"{name.lower()}_event_gap":cg,
            f"{name.lower()}_delta_gap_4rel":d,
            f"{name.lower()}_prior_years_event":cn,
        })

    inv=sum(np.isfinite(delta[x]) and delta[x]>0 for x in ["CRUDE_STOCK","GAS_STOCK","DIST_STOCK"])
    demand=sum(np.isfinite(delta[x]) and delta[x]<0 for x in ["GAS_DEMAND","DIST_DEMAND","JET_DEMAND"])
    throughput=bool(np.isfinite(delta["REFINERY_INPUT"]) and delta["REFINERY_INPUT"]<0)
    upstream=sum(np.isfinite(delta[x]) and delta[x]>0 for x in ["FIELD_PROD","CRUDE_IMPORTS"])
    row.update({
        "inventory_improving_count":int(inv),
        "demand_weak_count":int(demand),
        "throughput_weak":throughput,
        "upstream_supply_up_count":int(upstream),
    })
    if not row["mechanism_complete"]:
        cls="DATA_INCOMPLETE"
    elif demand>=2 and throughput:
        cls="DEMAND_DESTRUCTION"
    elif inv>=2 and upstream>=1 and (not throughput) and demand<=1:
        cls="SUPPLY_NORMALIZATION"
    else:
        cls="TIGHT_OR_MIXED"
    row["mechanism_class"]=cls
    return row

def outcomes(event,daily):
    release=pd.Timestamp(event.release_date).normalize()
    x=daily[daily.date>release][["date","WTI"]].dropna().reset_index(drop=True)
    out={}
    if x.empty:
        return out
    p0=float(x.iloc[0].WTI)
    out["execution_date"]=pd.Timestamp(x.iloc[0].date).normalize()
    out["execution_wti"]=p0
    for label,nobs in [("4w",20),("8w",40),("13w",65)]:
        if len(x)<=nobs:
            out[f"wti_fwd_{label}"]=np.nan
            out[f"short_mae_{label}"]=np.nan
            out[f"short_mfe_{label}"]=np.nan
            continue
        path=x.iloc[:nobs+1].WTI.astype(float)/p0-1.0
        out[f"wti_fwd_{label}"]=float(path.iloc[-1])
        out[f"short_mae_{label}"]=float(path.max())
        out[f"short_mfe_{label}"]=float(-path.min())
    return out

def perm_p_two_sided(a,b,seed=20260924,n_mc=100000):
    a=np.asarray(a,float); b=np.asarray(b,float)
    obs=float(np.median(a)-np.median(b))
    vals=np.concatenate([a,b]); n=len(a); N=len(vals)
    combos=math.comb(N,n)
    ge=0; total=0
    if combos<=200000:
        for idx in itertools.combinations(range(N),n):
            mask=np.zeros(N,dtype=bool); mask[list(idx)]=True
            stat=float(np.median(vals[mask])-np.median(vals[~mask]))
            ge+=abs(stat)>=abs(obs)-1e-15; total+=1
        p=ge/total
        method="EXACT_LABEL_PERMUTATION"
    else:
        rng=np.random.default_rng(seed)
        for _ in range(n_mc):
            perm=rng.permutation(N)
            stat=float(np.median(vals[perm[:n]])-np.median(vals[perm[n:]]))
            ge+=abs(stat)>=abs(obs)-1e-15; total+=1
        p=(ge+1)/(total+1)
        method=f"MC_LABEL_PERMUTATION_{n_mc}"
    return obs,float(p),method

def bh(p):
    p=np.asarray(p,float); out=np.full(len(p),np.nan)
    valid=np.isfinite(p); pv=p[valid]
    if not len(pv): return out
    order=np.argsort(pv); ranked=pv[order]; m=len(ranked)
    q=ranked*m/np.arange(1,m+1)
    q=np.minimum.accumulate(q[::-1])[::-1]; q=np.minimum(q,1.0)
    tmp=np.empty_like(q); tmp[order]=q; out[valid]=tmp
    return out

def loo_sign_stable(a,b):
    a=list(map(float,a)); b=list(map(float,b))
    obs=np.median(a)-np.median(b)
    if obs==0 or len(a)<2 or len(b)<2: return False
    s=np.sign(obs)
    vals=[]
    for i in range(len(a)):
        vals.append(np.sign(np.median(a[:i]+a[i+1:])-np.median(b))==s)
    for i in range(len(b)):
        vals.append(np.sign(np.median(a)-np.median(b[:i]+b[i+1:]))==s)
    return bool(all(vals))

def main():
    pit=json.loads(PIT_QC.read_text(encoding="utf-8"))
    if pit.get("qc_gate")!="PASS" or not pit.get("schedule_anchor_all_pass",False):
        raise SystemExit("ENERGY-WEEKLY-PIT-003 final timing QC not acceptable")

    reg=pd.read_csv(PIT_REG,parse_dates=["week_end","release_date"]).sort_values("release_date").reset_index(drop=True)
    daily,dprov=build_daily_panel()
    rp=build_release_price_panel(reg,daily)

    weekly={}; wprov=[]
    for name,sid in WEEKLY.items():
        z,m=FLOW.parse_eia_xls(sid)
        weekly[name]=z
        wprov.append({"name":name,**m})

    selected=rp[rp.SELECTED].copy()
    rows=[]
    for _,e in selected.iterrows():
        row=e.to_dict()
        row.update(mechanism_for_event(e,reg,weekly))
        row.update(outcomes(e,daily))
        rows.append(row)
    ev=pd.DataFrame(rows)

    # Primary frozen family.
    tests=[]
    for metric,kind in PRIMARY:
        a=ev.loc[ev.mechanism_class=="SUPPLY_NORMALIZATION",metric].dropna().astype(float)
        b=ev.loc[ev.mechanism_class=="TIGHT_OR_MIXED",metric].dropna().astype(float)
        rec={"metric":metric,"kind":kind,"n_supply_normalization":len(a),"n_tight_or_mixed":len(b)}
        if len(a)>=5 and len(b)>=5:
            diff,p,method=perm_p_two_sided(a,b)
            rec.update({
                "status":"SUPPORTED",
                "median_supply_normalization":float(a.median()),
                "median_tight_or_mixed":float(b.median()),
                "median_difference_sn_minus_mixed":diff,
                "p_two_sided":p,
                "permutation_method":method,
                "loo_sign_stable":loo_sign_stable(a.tolist(),b.tolist()),
            })
        else:
            rec.update({
                "status":"INSUFFICIENT_SUPPORT",
                "median_supply_normalization":float(a.median()) if len(a) else np.nan,
                "median_tight_or_mixed":float(b.median()) if len(b) else np.nan,
                "median_difference_sn_minus_mixed":np.nan,
                "p_two_sided":np.nan,
                "permutation_method":"",
                "loo_sign_stable":False,
            })
        tests.append(rec)
    tests=pd.DataFrame(tests)
    tests["bh_q_10pct"]=bh(tests.p_two_sided.to_numpy(float))
    tests["bh_fdr_10pct_pass"]=tests.bh_q_10pct<=0.10

    # Descriptive group metrics.
    desc=[]
    for grp,g in ev.groupby("mechanism_class"):
        for metric in ["wti_fwd_4w","wti_fwd_8w","wti_fwd_13w","short_mae_4w","short_mae_8w","short_mae_13w"]:
            x=g[metric].dropna().astype(float)
            desc.append({
                "mechanism_class":grp,"metric":metric,"n":len(x),
                "mean":float(x.mean()) if len(x) else np.nan,
                "median":float(x.median()) if len(x) else np.nan,
                "negative_share":float((x<0).mean()) if len(x) and metric.startswith("wti_fwd") else np.nan,
            })
    desc=pd.DataFrame(desc)

    # Era counts and 13w medians.
    era_rows=[]
    if len(ev):
        ev["era"]=pd.cut(
            ev.release_date,
            bins=[pd.Timestamp("2001-12-31"),pd.Timestamp("2009-12-31"),pd.Timestamp("2017-12-31"),pd.Timestamp("2100-01-01")],
            labels=["2002_2009","2010_2017","2018_PRESENT"],
        )
        for (era,grp),g in ev.groupby(["era","mechanism_class"],observed=True):
            era_rows.append({
                "era":str(era),"mechanism_class":grp,"n":len(g),
                "median_wti_fwd_13w":float(g.wti_fwd_13w.median()) if g.wti_fwd_13w.notna().any() else np.nan,
                "median_short_mae_13w":float(g.short_mae_13w.median()) if g.short_mae_13w.notna().any() else np.nan,
            })
    eras=pd.DataFrame(era_rows)

    # QC.
    price_timing_bad=int((ev.price_asof_date>=ev.release_date).sum()) if len(ev) else 0
    exec_timing_bad=int((ev.execution_date<=ev.release_date).sum()) if len(ev) and "execution_date" in ev else 0
    duplicates=int(ev.release_date.duplicated().sum()) if len(ev) else 0
    spacings=ev.release_date.sort_values().diff().dt.days.dropna() if len(ev) else pd.Series(dtype=float)
    spacing_bad=int((spacings<=91).sum())
    mapped_bad=int((~ev.week_end.isin(reg.week_end)).sum()) if len(ev) else 0
    source_dups={name:int(z.week_end.duplicated().sum()) for name,z in weekly.items()}

    counts=ev.mechanism_class.value_counts().to_dict() if len(ev) else {}
    supported=int((tests.status=="SUPPORTED").sum())
    survivors=int(tests.bh_fdr_10pct_pass.fillna(False).sum())

    hard_fail=(
        price_timing_bad or exec_timing_bad or duplicates or spacing_bad or mapped_bad
        or any(v!=0 for v in source_dups.values())
        or int(daily.date.duplicated().sum())!=0
    )
    qc={
        "qc_gate":"FAIL" if hard_fail else "PASS",
        "module":"ENERGY-WEEKLY-STATE-004",
        "pit_clock_qc":"PASS",
        "release_rows_considered":int(len(rp)),
        "rollover_raw_rows":int(rp.ROLLOVER_RAW.sum()),
        "selected_events":int(len(ev)),
        "first_selected_release":str(ev.release_date.min().date()) if len(ev) else None,
        "last_selected_release":str(ev.release_date.max().date()) if len(ev) else None,
        "mechanism_counts":counts,
        "primary_tests_supported":supported,
        "primary_bh_fdr_10pct_survivors":survivors,
        "price_timing_violations":price_timing_bad,
        "execution_timing_violations":exec_timing_bad,
        "selected_event_duplicate_dates":duplicates,
        "selected_event_spacing_violations":spacing_bad,
        "release_registry_mapping_violations":mapped_bad,
        "weekly_source_duplicate_dates":source_dups,
        "daily_price_duplicate_dates":int(daily.date.duplicated().sum()),
        "event_thresholds_tuned_after_results":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }

    pd.concat([dprov,pd.DataFrame(wprov)],ignore_index=True,sort=False).to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)
    rp.to_csv(OUT/"RELEASE_PRICE_STATE_PANEL.csv",index=False)
    ev.to_csv(OUT/"SELECTED_EVENT_PANEL.csv",index=False)
    tests.to_csv(OUT/"PRIMARY_TESTS.csv",index=False)
    desc.to_csv(OUT/"MECHANISM_DESCRIPTIVES.csv",index=False)
    eras.to_csv(OUT/"ERA_DIAGNOSTICS.csv",index=False)
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,default=str)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-WEEKLY-STATE-004 — Strict-PIT Weekly Mechanism Test",
        "",
        "**INDEPENDENT WEEKLY STRICT-PIT / ASSOCIATIONAL / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- release-state rows: {len(rp)}",
        f"- raw price-rollover rows: {int(rp.ROLLOVER_RAW.sum())}",
        f"- de-clustered selected events: {len(ev)}",
        f"- mechanism counts: {counts}",
        f"- supported frozen primary tests: {supported}/4",
        f"- BH-FDR 10% survivors: {survivors}/4",
        "",
        "## Frozen primary family",
        "",
        tests.to_markdown(index=False),
        "",
        "## Mechanism descriptives",
        "",
        desc.to_markdown(index=False),
        "",
        "## Era diagnostics",
        "",
        eras.to_markdown(index=False) if len(eras) else "No era rows.",
        "",
        "Interpretation must distinguish supply normalization from demand destruction and mixed/tight states. A null or low-support result is preserved.",
    ]
    (OUT/"ENERGY_WEEKLY_STATE_004_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    if hard_fail:
        raise SystemExit("ENERGY-WEEKLY-STATE-004 computational QC failed")
    print(json.dumps(qc,indent=2,default=str))

if __name__=="__main__":
    main()
