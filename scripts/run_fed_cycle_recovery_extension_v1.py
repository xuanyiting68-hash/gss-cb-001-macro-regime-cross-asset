#!/usr/bin/env python3
"""
FED-CYCLE-RECOVERY-EXTENSION-015
Extend PHASE-CLOCK-004 recovery accounting to 014 assets.
"""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_recovery_extension_v1"
OUT.mkdir(parents=True,exist_ok=True)

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

CROSS=load_module(ROOT/"scripts"/"run_fed_cycle_cross_asset_expansion_v1.py","cross014_for_rec015")
PHASE=load_module(ROOT/"scripts"/"run_fed_cycle_phase_clock_v1.py","phase004_for_rec015")
STATE=load_module(ROOT/"scripts"/"run_fed_cycle_state_panel_v2.py","state_for_rec015")

MARKETS=("TLT","VNQ","BTC_USD","DXY")

def generic_km(g, drawdown_col, level):
    obs=f"recovery{level}_observed"
    dur=f"recovery{level}_months"
    d=g[pd.to_numeric(g[drawdown_col],errors="coerce")>1e-15].copy()
    if d.empty:
        return pd.DataFrame()
    d["duration"]=np.where(
        d[obs].astype(bool),
        pd.to_numeric(d[dur],errors="coerce"),
        pd.to_numeric(d["recovery_censor_months"],errors="coerce"),
    )
    d=d.dropna(subset=["duration"]).copy()
    d["duration"]=d["duration"].astype(int)
    surv=1.0
    rows=[{
        "time_months":0,
        "at_risk_weight":float(d["episode_weight"].sum()),
        "event_weight":0.0,
        "censor_weight":0.0,
        "survival_not_recovered":1.0,
    }]
    for t in sorted(d["duration"].unique()):
        risk=float(d.loc[d.duration>=t,"episode_weight"].sum())
        ev=float(d.loc[(d.duration==t)&d[obs].astype(bool),"episode_weight"].sum())
        cens=float(d.loc[(d.duration==t)&(~d[obs].astype(bool)),"episode_weight"].sum())
        if risk>0 and ev>0:
            surv*=1.0-ev/risk
        rows.append({
            "time_months":int(t),
            "at_risk_weight":risk,
            "event_weight":ev,
            "censor_weight":cens,
            "survival_not_recovered":float(surv),
        })
    return pd.DataFrame(rows)

def recovery_summary(metrics, drawdown_col, asset_col="asset"):
    curves=[]; rows=[]
    for (asset,anchor),g in metrics.groupby([asset_col,"anchor"]):
        nlegs=int(g.cycle_id.nunique())
        nbroad=int(g.broad_episode_id.nunique())
        positive=int((pd.to_numeric(g[drawdown_col],errors="coerce")>1e-15).sum())
        for level in (50,100):
            km=generic_km(g,drawdown_col,level)
            if km.empty:
                median=np.nan
            else:
                hit=km[km.survival_not_recovered<=0.5+1e-12]
                median=int(hit.iloc[0].time_months) if len(hit) else np.nan
                km["asset"]=asset
                km["anchor"]=anchor
                km["recovery_level"]=f"{level}%"
                curves.append(km)
            rows.append({
                "asset":asset,
                "anchor":anchor,
                "recovery_level":f"{level}%",
                "n_legs":nlegs,
                "n_broad_episodes":nbroad,
                "support_status":CROSS.support_label(nlegs,nbroad),
                "positive_drawdown_episodes":positive,
                "observed_recoveries":int(g[f"recovery{level}_observed"].astype(bool).sum()),
                "right_censored":int((~g[f"recovery{level}_observed"].astype(bool)&(pd.to_numeric(g[drawdown_col],errors="coerce")>1e-15)).sum()),
                "weighted_km_median_months":median,
            })
    c=pd.concat(curves,ignore_index=True) if curves else pd.DataFrame()
    return c,pd.DataFrame(rows)

def housing_path_recovery(price_map,anchor_date):
    ep=pd.Timestamp(anchor_date).to_period("M")
    basep=ep-1
    postp=[ep+k for k in range(1,25)]
    if basep not in price_map or any(p not in price_map for p in postp):
        return None
    vals=np.array([float(price_map[basep])]+[float(price_map[p]) for p in postp],float)
    peaks=np.maximum.accumulate(vals)
    dd=1.0-vals/peaks
    decline=float(dd.max())
    out={
        "decline_24m":decline,
        "trough_month_24m":np.nan,
        "recovery50_months":np.nan,
        "recovery100_months":np.nan,
        "recovery50_observed":False,
        "recovery100_observed":False,
        "recovery_censor_months":np.nan,
    }
    if decline<=1e-15:
        return out
    trough_idx=int(np.argmax(dd))
    peak_idx=int(np.argmax(vals[:trough_idx+1]))
    out["trough_month_24m"]=trough_idx
    peak=float(vals[peak_idx]); trough=float(vals[trough_idx])
    t50=trough+0.5*(peak-trough); t100=peak
    trough_period=basep if trough_idx==0 else ep+trough_idx
    rec=[]
    for j in range(0,61):
        p=trough_period+j
        if p in price_map:
            rec.append((j,float(price_map[p])))
    if rec:
        h50=[j for j,v in rec if v>=t50]
        h100=[j for j,v in rec if v>=t100]
        out.update({
            "recovery50_months":int(h50[0]) if h50 else np.nan,
            "recovery100_months":int(h100[0]) if h100 else np.nan,
            "recovery50_observed":bool(h50),
            "recovery100_observed":bool(h100),
            "recovery_censor_months":int(rec[-1][0]),
        })
    return out

def main():
    cycles=CROSS.load_cycles()
    if (pd.to_datetime(cycles.first_hike).dt.year>=2026).any():
        raise RuntimeError("live 2026 cycle leaked into historical cycle table")

    prov=[]; monthly={}
    for name in MARKETS:
        cfg=CROSS.MARKET_ASSETS[name]
        df,meta=CROSS.fetch_yahoo(cfg["symbol"],cfg["adjusted"])
        monthly[name]={"df":CROSS.monthly_average(df),"label":cfg["label"]}
        prov.append(CROSS.make_prov(
            name,"Yahoo Finance public chart history",meta,df,
            "Adjusted close requested" if cfg["adjusted"] else "Close"
        ))

    market014,_=CROSS.build_market(cycles,monthly)
    market_rows=[]
    mdd_diff=[]; trough_bad=0
    for _,r in market014.iterrows():
        pmap=dict(zip(monthly[r.asset]["df"].period,monthly[r.asset]["df"].value.astype(float)))
        _,rec=PHASE.path_and_recovery(pmap,r.anchor_date)
        if rec is None:
            raise RuntimeError(f"recovery path missing {r.asset} {r.anchor} {r.cycle_id}")
        row=r.to_dict()
        # PHASE returns identical 12M drawdown plus recovery fields.
        for k in ["recovery50_months","recovery100_months","recovery50_observed","recovery100_observed","recovery_censor_months"]:
            row[k]=rec[k]
        market_rows.append(row)

        # exact 014 drawdown should match PHASE's metric object; recompute via function result metric.
        _,m=PHASE.path_and_recovery(pmap,r.anchor_date)
        # rec object has no mdd; compare through CROSS liquid metric versus stored r.
        cm=CROSS.liquid_metrics(pmap,r.anchor_date)
        mdd_diff.append(abs(float(cm["mdd_12m"])-float(r.mdd_12m)))
        a=cm["mdd_trough_month"]; btr=r.mdd_trough_month
        if (pd.isna(a) != pd.isna(btr)) or (pd.notna(a) and int(a)!=int(btr)):
            trough_bad+=1

    market=pd.DataFrame(market_rows)
    market_km,market_sum=recovery_summary(market,"mdd_12m","asset")

    # Housing fresh source / same 014 construction.
    hdf,hmeta=STATE.fetch_fred("CSUSHPINSA")
    hmonthly=CROSS.monthly_average(hdf)
    prov.append(CROSS.make_prov(
        "CSUSHPINSA",
        "S&P Cotality Case-Shiller U.S. National Home Price Index via FRED distribution",
        hmeta,hdf,"Copyrighted raw source history not committed"
    ))
    h014,_=CROSS.build_housing(cycles,hmonthly)
    hpmap=dict(zip(hmonthly.period,hmonthly.value.astype(float)))
    hrows=[]; hdiff=[]; htrough_bad=0
    for _,r in h014.iterrows():
        rec=housing_path_recovery(hpmap,r.anchor_date)
        if rec is None: raise RuntimeError("housing recovery path missing")
        row=r.to_dict()
        for k in ["recovery50_months","recovery100_months","recovery50_observed","recovery100_observed","recovery_censor_months"]:
            row[k]=rec[k]
        row["asset"]="US_HOUSE_PRICE"
        hrows.append(row)
        hdiff.append(abs(float(rec["decline_24m"])-float(r.decline_24m)))
        a=rec["trough_month_24m"]; btr=r.trough_month_24m
        if (pd.isna(a)!=pd.isna(btr)) or (pd.notna(a) and int(a)!=int(btr)):
            htrough_bad+=1

    housing=pd.DataFrame(hrows)
    housing_km,housing_sum=recovery_summary(housing,"decline_24m","asset")

    # Recovery order QC.
    order_bad=0
    for df in [market,housing]:
        z=df.dropna(subset=["recovery50_months","recovery100_months"])
        order_bad+=int((pd.to_numeric(z.recovery100_months)<pd.to_numeric(z.recovery50_months)).sum())

    support_bad=0
    for df in [market_sum,housing_sum]:
        for _,r in df.iterrows():
            if r.support_status!=CROSS.support_label(int(r.n_legs),int(r.n_broad_episodes)):
                support_bad+=1

    hard_fail=(
        max(mdd_diff or [0])>1e-12
        or trough_bad!=0
        or max(hdiff or [0])>1e-12
        or htrough_bad!=0
        or order_bad!=0
        or support_bad!=0
    )

    qc={
        "qc_gate":"FAIL" if hard_fail else "PASS",
        "module":"FED-CYCLE-RECOVERY-EXTENSION-015",
        "historical_mechanical_cycles":int(cycles.cycle_id.nunique()),
        "historical_broad_episodes":int(cycles.broad_episode_id.nunique()),
        "market_assets":list(MARKETS),
        "market_metric_rows":int(len(market)),
        "housing_metric_rows":int(len(housing)),
        "max_market_mdd_reproduction_error":float(max(mdd_diff or [0])),
        "market_trough_reproduction_violations":trough_bad,
        "max_housing_decline_reproduction_error":float(max(hdiff or [0])),
        "housing_trough_reproduction_violations":htrough_bad,
        "recovery_order_violations":order_bad,
        "support_label_violations":support_bad,
        "current_2026_cycle_leak_violations":0,
        "raw_source_histories_committed":False,
        "evidence_class":"DESCRIPTIVE",
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }

    pd.DataFrame(prov).to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)
    market.to_csv(OUT/"MARKET_RECOVERY_METRICS.csv",index=False)
    market_sum.to_csv(OUT/"MARKET_RECOVERY_SUMMARY.csv",index=False)
    market_km.to_csv(OUT/"MARKET_RECOVERY_KM.csv",index=False)
    housing.to_csv(OUT/"HOUSING_RECOVERY_METRICS.csv",index=False)
    housing_sum.to_csv(OUT/"HOUSING_RECOVERY_SUMMARY.csv",index=False)
    housing_km.to_csv(OUT/"HOUSING_RECOVERY_KM.csv",index=False)

    core=pd.read_csv(ROOT/"results"/"fed_cycle_phase_clock_v1"/"PHASE_RECOVERY_SUMMARY.csv")
    combined=pd.concat([
        core.assign(source_module="PHASE_CLOCK_004"),
        market_sum.assign(source_module="RECOVERY_EXTENSION_015"),
        housing_sum.assign(source_module="RECOVERY_EXTENSION_015"),
    ],ignore_index=True,sort=False)
    combined.to_csv(OUT/"COMBINED_RECOVERY_REFERENCE.csv",index=False)

    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# FED-CYCLE-RECOVERY-EXTENSION-015 — New-Asset Recovery Clock",
        "",
        "**DESCRIPTIVE / RIGHT-CENSORING PRESERVED / NOT CAUSAL / NOT A FORECAST**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        "",
        "## Liquid-market recovery summary",
        "",
        market_sum.to_markdown(index=False),
        "",
        "## Housing recovery summary",
        "",
        housing_sum.to_markdown(index=False),
        "",
        "## Reading rule",
        "",
        "- Liquid assets use the exact PHASE-CLOCK-004 12M MDD definition and search recovery up to 60 months after trough.",
        "- Housing uses its predeclared 24M drawdown window and then the same prior-peak 50%/100% recovery logic.",
        "- Missing KM medians mean at least half the broad-episode-weighted risk set did not recover within observed/censored support.",
        "- TLT/VNQ/BTC support remains limited where 014 labels it limited.",
    ]
    (OUT/"FED_CYCLE_RECOVERY_EXTENSION_015_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-RECOVERY-EXTENSION-015 QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
