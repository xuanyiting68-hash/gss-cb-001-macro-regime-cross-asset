#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_housing_lag_chain_034_v1"
OUT.mkdir(parents=True,exist_ok=True)

SPEC=ROOT/"data"/"public"/"HOUSING_LAG_CHAIN_SOURCE_SPEC_20260926.csv"
HOUSE_METRICS=ROOT/"results"/"fed_cycle_cross_asset_expansion_v1"/"HOUSING_PHASE_METRICS.csv"
HOUSE_SUMMARY=ROOT/"results"/"fed_cycle_cross_asset_expansion_v1"/"HOUSING_PHASE_SUMMARY.csv"
HOUSE_RECOVERY=ROOT/"results"/"fed_cycle_recovery_extension_v1"/"HOUSING_RECOVERY_METRICS.csv"
Q014=ROOT/"results"/"fed_cycle_cross_asset_expansion_v1"/"QC.json"
Q015=ROOT/"results"/"fed_cycle_recovery_extension_v1"/"QC.json"
Q032=ROOT/"results"/"fed_cycle_four_phase_investor_atlas_032_v1"/"QC.json"

HORIZONS=[3,6,12,24]
FINANCING=["MORTGAGE30US","DGS10","MORTGAGE_SPREAD_PP"]
ACTIVITY=["HOUST","PERMIT","HSN1F"]

def read_pass(path):
    q=json.loads(Path(path).read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def sha256_bytes(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def fetch_csv(url:str)->tuple[pd.DataFrame,dict]:
    last_error=None
    for attempt in range(4):
        try:
            req=urllib.request.Request(
                url,
                headers={
                    "User-Agent":"Mozilla/5.0 housing-lag-chain-research",
                    "Accept":"text/csv,*/*;q=0.8",
                }
            )
            with urllib.request.urlopen(req,timeout=120) as resp:
                raw=resp.read()
            if len(raw)<100:
                raise RuntimeError(f"unexpectedly short FRED response: {len(raw)} bytes")
            df=pd.read_csv(io.BytesIO(raw))
            return df,{"sha256":sha256_bytes(raw),"raw_bytes":len(raw),"fetch_attempt":attempt+1}
        except Exception as exc:
            last_error=exc
            if attempt<3:
                time.sleep(2*(attempt+1))
    raise RuntimeError(f"source fetch failed after retries: {url}: {last_error}")

def weighted_median(values,weights):
    v=np.asarray(values,dtype=float)
    w=np.asarray(weights,dtype=float)
    ok=np.isfinite(v)&np.isfinite(w)&(w>0)
    if not ok.any():
        return np.nan
    v=v[ok]; w=w[ok]
    order=np.argsort(v)
    v=v[order]; w=w[order]
    c=np.cumsum(w)
    cutoff=0.5*w.sum()
    return float(v[np.searchsorted(c,cutoff,side="left")])

def broad_count(df):
    return int(df.loc[df["episode_weight"].notna(),"broad_episode_id"].nunique())

def monthly_from_raw(df,series_id,kind):
    date_col=df.columns[0]
    val_col=series_id if series_id in df.columns else df.columns[1]
    x=df[[date_col,val_col]].copy()
    x.columns=["date","value"]
    x["date"]=pd.to_datetime(x["date"],errors="coerce")
    x["value"]=pd.to_numeric(x["value"],errors="coerce")
    x=x.dropna(subset=["date","value"]).sort_values("date")
    x["period"]=x["date"].dt.to_period("M")
    if kind in {"Weekly","Daily"}:
        m=x.groupby("period",as_index=False)["value"].mean()
    else:
        m=x.groupby("period",as_index=False)["value"].last()
    m["month"]=m["period"].dt.to_timestamp()
    return m[["period","month","value"]]

def value_at(series:pd.Series,period:pd.Period):
    try:
        v=series.loc[period]
    except KeyError:
        return np.nan
    if isinstance(v,pd.Series):
        v=v.iloc[-1]
    return float(v) if pd.notna(v) else np.nan

def financing_metrics(series_id,ser,anchors):
    rows=[]
    for r in anchors.itertuples(index=False):
        anchor_p=pd.Period(pd.Timestamp(r.anchor_date),freq="M")
        base_p=anchor_p-1
        base=value_at(ser,base_p)
        row={
            "series_id":series_id,"anchor":r.anchor,"cycle_id":r.cycle_id,
            "broad_episode_id":r.broad_episode_id,"anchor_date":r.anchor_date,
            "episode_weight":r.episode_weight,"baseline_month":str(base_p),
            "baseline_level":base,
        }
        for h in HORIZONS:
            hp=anchor_p+h
            val=value_at(ser,hp)
            row[f"level_{h}m"]=val
            row[f"change_{h}m_pp"]=val-base if np.isfinite(val) and np.isfinite(base) else np.nan

        window=[]
        for p in pd.period_range(anchor_p,anchor_p+24,freq="M"):
            v=value_at(ser,p)
            if np.isfinite(v) and np.isfinite(base):
                window.append((p.ordinal-anchor_p.ordinal,v-base))
        if window:
            maxp,maxchg=max(window,key=lambda z:z[1])
            minp,minchg=min(window,key=lambda z:z[1])
            row["max_increase_24m_pp"]=maxchg
            row["max_pressure_month_24m"]=int(maxp)
            row["min_change_24m_pp"]=minchg
            row["min_rate_month_24m"]=int(minp)
            row["months_observed_0_24"]=len(window)
        else:
            row["max_increase_24m_pp"]=np.nan
            row["max_pressure_month_24m"]=np.nan
            row["min_change_24m_pp"]=np.nan
            row["min_rate_month_24m"]=np.nan
            row["months_observed_0_24"]=0
        rows.append(row)
    return pd.DataFrame(rows)

def activity_metrics(series_id,ser3,anchors):
    rows=[]
    for r in anchors.itertuples(index=False):
        anchor_p=pd.Period(pd.Timestamp(r.anchor_date),freq="M")
        base_p=anchor_p-1
        base=value_at(ser3,base_p)
        row={
            "series_id":series_id,"anchor":r.anchor,"cycle_id":r.cycle_id,
            "broad_episode_id":r.broad_episode_id,"anchor_date":r.anchor_date,
            "episode_weight":r.episode_weight,"baseline_month":str(base_p),
            "baseline_3m_avg":base,
        }
        for h in HORIZONS:
            hp=anchor_p+h
            val=value_at(ser3,hp)
            row[f"level_3mavg_{h}m"]=val
            row[f"change_{h}m"]=val/base-1 if np.isfinite(val) and np.isfinite(base) and base!=0 else np.nan
        window=[]
        for p in pd.period_range(anchor_p,anchor_p+24,freq="M"):
            v=value_at(ser3,p)
            if np.isfinite(v) and np.isfinite(base) and base!=0:
                window.append((p.ordinal-anchor_p.ordinal,v/base-1))
        if window:
            trough_p,trough=min(window,key=lambda z:z[1])
            peak_p,peak=max(window,key=lambda z:z[1])
            row["min_change_24m"]=trough
            row["trough_month_24m"]=int(trough_p)
            row["max_change_24m"]=peak
            row["peak_month_24m"]=int(peak_p)
            row["months_observed_0_24"]=len(window)
        else:
            row["min_change_24m"]=np.nan
            row["trough_month_24m"]=np.nan
            row["max_change_24m"]=np.nan
            row["peak_month_24m"]=np.nan
            row["months_observed_0_24"]=0
        rows.append(row)
    return pd.DataFrame(rows)

def summarize_financing(df):
    out=[]
    for (sid,anchor),g in df.groupby(["series_id","anchor"],sort=True):
        row={"series_id":sid,"anchor":anchor,"n_legs":len(g),"n_broad_episodes":g["broad_episode_id"].nunique(),"support_status":"SUPPORTED_DESCRIPTIVE"}
        for h in HORIZONS:
            row[f"weighted_median_change_{h}m_pp"]=weighted_median(g[f"change_{h}m_pp"],g["episode_weight"])
        row["weighted_median_max_increase_24m_pp"]=weighted_median(g["max_increase_24m_pp"],g["episode_weight"])
        row["weighted_median_max_pressure_month_24m"]=weighted_median(g["max_pressure_month_24m"],g["episode_weight"])
        row["weighted_median_min_change_24m_pp"]=weighted_median(g["min_change_24m_pp"],g["episode_weight"])
        row["weighted_median_min_rate_month_24m"]=weighted_median(g["min_rate_month_24m"],g["episode_weight"])
        out.append(row)
    return pd.DataFrame(out)

def summarize_activity(df):
    out=[]
    for (sid,anchor),g in df.groupby(["series_id","anchor"],sort=True):
        row={"series_id":sid,"anchor":anchor,"n_legs":len(g),"n_broad_episodes":g["broad_episode_id"].nunique(),"support_status":"SUPPORTED_DESCRIPTIVE"}
        for h in HORIZONS:
            row[f"weighted_median_change_{h}m"]=weighted_median(g[f"change_{h}m"],g["episode_weight"])
        row["weighted_median_min_change_24m"]=weighted_median(g["min_change_24m"],g["episode_weight"])
        row["weighted_median_trough_month_24m"]=weighted_median(g["trough_month_24m"],g["episode_weight"])
        row["weighted_median_max_change_24m"]=weighted_median(g["max_change_24m"],g["episode_weight"])
        row["weighted_median_peak_month_24m"]=weighted_median(g["peak_month_24m"],g["episode_weight"])
        out.append(row)
    return pd.DataFrame(out)

def fmt_pct(x):
    return "NA" if pd.isna(x) else f"{x*100:+.1f}%"

def mag(x):
    return "NA" if pd.isna(x) else f"{x*100:.1f}%"

def fmt_pp(x):
    return "NA" if pd.isna(x) else f"{x:+.2f}pp"

def fmt_month(x):
    return "NA" if pd.isna(x) else f"M{int(round(x))}"

def main():
    q014=read_pass(Q014); q015=read_pass(Q015); q032=read_pass(Q032)
    spec=pd.read_csv(SPEC)
    house=pd.read_csv(HOUSE_METRICS)
    house_summary=pd.read_csv(HOUSE_SUMMARY)
    recovery=pd.read_csv(HOUSE_RECOVERY)

    # Canonical anchor map is exactly the existing 014 housing-event universe.
    anchor_cols=["anchor","cycle_id","broad_episode_id","anchor_date","episode_weight"]
    anchors=house[anchor_cols].drop_duplicates().sort_values(["anchor_date","anchor","cycle_id"]).reset_index(drop=True)
    if len(anchors)!=len(house):
        raise RuntimeError("housing metrics unexpectedly duplicate anchors")
    if any(anchors["anchor_date"].astype(str).str.startswith("2026")):
        raise RuntimeError("current 2026 candidate leaked into historical housing anchors")

    downloaded={}
    registry=[]
    retrieved=datetime.now(timezone.utc).isoformat()
    for s in spec.itertuples(index=False):
        df,meta=fetch_csv(s.source_url)
        m=monthly_from_raw(df,s.series_id,s.frequency)
        downloaded[s.series_id]=m
        registry.append({
            "series_id":s.series_id,"layer":s.layer,"source":s.source,"source_url":s.source_url,
            "frequency":s.frequency,"units":s.units,"transformation":s.transformation,
            "retrieved_utc":retrieved,"sha256":meta["sha256"],"raw_bytes":meta["raw_bytes"],
            "fetch_attempt":meta["fetch_attempt"],"rows_monthly":len(m),"first_month":str(m["period"].min()),"last_month":str(m["period"].max()),
            "raw_committed":False,"critical_note":s.critical_note
        })
    reg=pd.DataFrame(registry)
    if len(reg)!=5 or reg["sha256"].str.len().ne(64).any():
        raise RuntimeError("source registry incomplete")
    if not reg.loc[reg["series_id"]=="MORTGAGE30US","critical_note"].str.contains("2022-11-17",regex=False).all():
        raise RuntimeError("mortgage methodology-change note lost")
    reg.to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)

    # Monthly financing series.
    mort=downloaded["MORTGAGE30US"].set_index("period")["value"]
    dgs10=downloaded["DGS10"].set_index("period")["value"]
    all_periods=mort.index.union(dgs10.index).sort_values()
    spread=pd.Series(index=all_periods,dtype=float)
    for p in all_periods:
        mv=value_at(mort,p); tv=value_at(dgs10,p)
        spread.loc[p]=mv-tv if np.isfinite(mv) and np.isfinite(tv) else np.nan

    fparts=[
        financing_metrics("MORTGAGE30US",mort,anchors),
        financing_metrics("DGS10",dgs10,anchors),
        financing_metrics("MORTGAGE_SPREAD_PP",spread,anchors),
    ]
    fmet=pd.concat(fparts,ignore_index=True)
    fmet.to_csv(OUT/"HOUSING_FINANCING_PHASE_METRICS.csv",index=False)
    fsum=summarize_financing(fmet)
    fsum.to_csv(OUT/"HOUSING_FINANCING_PHASE_SUMMARY.csv",index=False)

    # Activity series use trailing 3M averages.
    aparts=[]
    activity_series={}
    for sid in ACTIVITY:
        m=downloaded[sid].copy().sort_values("period")
        m["value_3mavg"]=m["value"].rolling(3,min_periods=3).mean()
        ser=m.set_index("period")["value_3mavg"]
        activity_series[sid]=ser
        aparts.append(activity_metrics(sid,ser,anchors))
    amet=pd.concat(aparts,ignore_index=True)
    amet.to_csv(OUT/"HOUSING_ACTIVITY_PHASE_METRICS.csv",index=False)
    asum=summarize_activity(amet)
    asum.to_csv(OUT/"HOUSING_ACTIVITY_PHASE_SUMMARY.csv",index=False)

    # Build episode lag-chain panel from exact canonical housing rows.
    panel=house.merge(recovery[
        ["anchor","cycle_id","recovery50_months","recovery100_months","recovery50_observed","recovery100_observed","recovery_censor_months"]
    ],on=["anchor","cycle_id"],how="left",validate="one_to_one")

    def pick_metric(df,sid,cols,prefix):
        z=df[df["series_id"]==sid][["anchor","cycle_id"]+cols].copy()
        z=z.rename(columns={c:f"{prefix}{c}" for c in cols})
        return z

    panel=panel.merge(pick_metric(
        fmet,"MORTGAGE30US",
        ["baseline_level","change_3m_pp","change_6m_pp","change_12m_pp","change_24m_pp","max_increase_24m_pp","max_pressure_month_24m","min_change_24m_pp","min_rate_month_24m"],
        "mortgage_"
    ),on=["anchor","cycle_id"],how="left",validate="one_to_one")

    panel=panel.merge(pick_metric(
        fmet,"DGS10",
        ["baseline_level","change_3m_pp","change_6m_pp","change_12m_pp","change_24m_pp"],
        "dgs10_"
    ),on=["anchor","cycle_id"],how="left",validate="one_to_one")

    panel=panel.merge(pick_metric(
        fmet,"MORTGAGE_SPREAD_PP",
        ["baseline_level","change_3m_pp","change_6m_pp","change_12m_pp","change_24m_pp","max_increase_24m_pp","max_pressure_month_24m"],
        "spread_"
    ),on=["anchor","cycle_id"],how="left",validate="one_to_one")

    for sid,prefix in [("HOUST","houst_"),("PERMIT","permit_"),("HSN1F","sales_")]:
        panel=panel.merge(pick_metric(
            amet,sid,
            ["change_3m","change_6m","change_12m","change_24m","min_change_24m","trough_month_24m","max_change_24m"],
            prefix
        ),on=["anchor","cycle_id"],how="left",validate="one_to_one")

    activity_cols=["permit_trough_month_24m","houst_trough_month_24m","sales_trough_month_24m"]
    panel["activity_median_trough_month_24m"]=panel[activity_cols].median(axis=1,skipna=True)
    panel["activity_after_mortgage_months"]=panel["activity_median_trough_month_24m"]-panel["mortgage_max_pressure_month_24m"]
    panel["price_after_activity_months"]=np.where(
        panel["decline_24m"].fillna(0)>0,
        panel["trough_month_24m"]-panel["activity_median_trough_month_24m"],
        np.nan
    )
    panel["price_after_mortgage_months"]=np.where(
        panel["decline_24m"].fillna(0)>0,
        panel["trough_month_24m"]-panel["mortgage_max_pressure_month_24m"],
        np.nan
    )
    panel["causal_status"]="NONE"
    panel["interpretation_guardrail"]="timing differences are descriptive sequencing, not causal transmission lags"
    panel.to_csv(OUT/"HOUSING_LAG_CHAIN_EPISODE_PANEL.csv",index=False)

    # Phase summary.
    ps=[]
    for anchor,g in panel.groupby("anchor",sort=True):
        row={
            "anchor":anchor,"n_legs":len(g),"n_broad_episodes":g["broad_episode_id"].nunique(),
            "support_status":"SUPPORTED_DESCRIPTIVE",
            "weighted_median_mortgage_change_12m_pp":weighted_median(g["mortgage_change_12m_pp"],g["episode_weight"]),
            "weighted_median_mortgage_max_pressure_month":weighted_median(g["mortgage_max_pressure_month_24m"],g["episode_weight"]),
            "weighted_median_permit_change_12m":weighted_median(g["permit_change_12m"],g["episode_weight"]),
            "weighted_median_permit_trough_month":weighted_median(g["permit_trough_month_24m"],g["episode_weight"]),
            "weighted_median_houst_change_12m":weighted_median(g["houst_change_12m"],g["episode_weight"]),
            "weighted_median_houst_trough_month":weighted_median(g["houst_trough_month_24m"],g["episode_weight"]),
            "weighted_median_sales_change_12m":weighted_median(g["sales_change_12m"],g["episode_weight"]),
            "weighted_median_sales_trough_month":weighted_median(g["sales_trough_month_24m"],g["episode_weight"]),
            "weighted_median_house_price_ret_12m":weighted_median(g["ret_12m"],g["episode_weight"]),
            "weighted_median_house_price_ret_24m":weighted_median(g["ret_24m"],g["episode_weight"]),
            "weighted_median_house_decline_24m":weighted_median(g["decline_24m"],g["episode_weight"]),
            "weighted_median_house_trough_month_positive_declines":weighted_median(
                g.loc[g["decline_24m"]>0,"trough_month_24m"],
                g.loc[g["decline_24m"]>0,"episode_weight"]
            ),
            "positive_price_decline_legs":int((g["decline_24m"]>0).sum()),
            "weighted_median_activity_trough_month":weighted_median(g["activity_median_trough_month_24m"],g["episode_weight"]),
            "weighted_median_activity_after_mortgage_months":weighted_median(g["activity_after_mortgage_months"],g["episode_weight"]),
            "weighted_median_price_after_activity_months_positive_declines":weighted_median(
                g.loc[g["decline_24m"]>0,"price_after_activity_months"],
                g.loc[g["decline_24m"]>0,"episode_weight"]
            ),
            "path_risk_metric":"DECLINE_24M",
            "causal_status":"NONE",
            "oos_status":"NOT_A_FORECASTING_MODEL",
            "deployment_status":"NOT_DEPLOYABLE",
        }
        ps.append(row)
    psum=pd.DataFrame(ps)
    if len(psum)!=4:
        raise RuntimeError("phase lag summary must have four rows")
    psum.to_csv(OUT/"HOUSING_LAG_CHAIN_PHASE_SUMMARY.csv",index=False)

    # Exact canonical price summary check.
    canon=house_summary.set_index("anchor")
    for r in psum.itertuples(index=False):
        c=canon.loc[r.anchor]
        for newv,oldv,name in [
            (r.weighted_median_house_price_ret_12m,c.weighted_median_ret_12m,"ret12"),
            (r.weighted_median_house_price_ret_24m,c.weighted_median_ret_24m,"ret24"),
            (r.weighted_median_house_decline_24m,c.weighted_median_decline_24m,"decline24"),
        ]:
            if not np.isclose(newv,oldv,equal_nan=True,atol=1e-12):
                raise RuntimeError(f"canonical housing summary mismatch {r.anchor} {name}")

    # Case audit B05 bust / B07 2022-23.
    case=panel[panel["broad_episode_id"].isin(["B05","B07"])].copy()
    case["case_label"]=case["broad_episode_id"].map({
        "B05":"2004-07 tightening / housing bust sequence",
        "B07":"2022-23 tightening / price-resilience sequence"
    })
    case["audit_status"]="KEEP_VISIBLE_NOT_AVERAGED_AWAY"
    case.to_csv(OUT/"HOUSING_CASE_AUDIT.csv",index=False)

    # Dynamic question registry.
    psidx=psum.set_index("anchor")
    def p(anchor,col): return psidx.loc[anchor,col]

    qrows=[
        ("H-Q01","How quickly do mortgage rates move after each Fed phase anchor?",
         f"FIRST_HIKE 12M mortgage-rate change median {fmt_pp(p('FIRST_HIKE','weighted_median_mortgage_change_12m_pp'))}; LAST_HIKE {fmt_pp(p('LAST_HIKE','weighted_median_mortgage_change_12m_pp'))}; PAUSE {fmt_pp(p('PAUSE_START','weighted_median_mortgage_change_12m_pp'))}; FIRST_CUT {fmt_pp(p('FIRST_CUT','weighted_median_mortgage_change_12m_pp'))}.","FINANCING"),
        ("H-Q02","Does mortgage-rate pressure peak before housing activity troughs?",
         f"Median mortgage max-pressure month / activity-trough month: FIRST_HIKE {fmt_month(p('FIRST_HIKE','weighted_median_mortgage_max_pressure_month'))} / {fmt_month(p('FIRST_HIKE','weighted_median_activity_trough_month'))}; LAST_HIKE {fmt_month(p('LAST_HIKE','weighted_median_mortgage_max_pressure_month'))} / {fmt_month(p('LAST_HIKE','weighted_median_activity_trough_month'))}; PAUSE {fmt_month(p('PAUSE_START','weighted_median_mortgage_max_pressure_month'))} / {fmt_month(p('PAUSE_START','weighted_median_activity_trough_month'))}; FIRST_CUT {fmt_month(p('FIRST_CUT','weighted_median_mortgage_max_pressure_month'))} / {fmt_month(p('FIRST_CUT','weighted_median_activity_trough_month'))}. These are descriptive timing differences.","LAG_SEQUENCE"),
        ("H-Q03","Which activity series reacts earlier: permits, starts, or new-home sales?",
         f"FIRST_HIKE trough medians: PERMIT {fmt_month(p('FIRST_HIKE','weighted_median_permit_trough_month'))}, HOUST {fmt_month(p('FIRST_HIKE','weighted_median_houst_trough_month'))}, HSN1F {fmt_month(p('FIRST_HIKE','weighted_median_sales_trough_month'))}. Compare phase by phase rather than imposing one universal ordering.","ACTIVITY"),
        ("H-Q04","Does activity generally weaken before national house prices decline?",
         f"Among episodes with positive 24M house-price decline, the phase summaries preserve price-trough timing separately from activity troughs. Median price-after-activity differences are FIRST_HIKE {fmt_month(p('FIRST_HIKE','weighted_median_price_after_activity_months_positive_declines'))}, LAST_HIKE {fmt_month(p('LAST_HIKE','weighted_median_price_after_activity_months_positive_declines'))}, PAUSE {fmt_month(p('PAUSE_START','weighted_median_price_after_activity_months_positive_declines'))}, FIRST_CUT {fmt_month(p('FIRST_CUT','weighted_median_price_after_activity_months_positive_declines'))}.","LAG_SEQUENCE"),
        ("H-Q05","How long after FIRST_HIKE do housing activity and prices reach their worst point?",
         f"FIRST_HIKE activity median trough {fmt_month(p('FIRST_HIKE','weighted_median_activity_trough_month'))}; price trough among positive-decline episodes {fmt_month(p('FIRST_HIKE','weighted_median_house_trough_month_positive_declines'))}.","FIRST_HIKE"),
        ("H-Q06","What changes by LAST_HIKE?",
         f"LAST_HIKE mortgage 12M change {fmt_pp(p('LAST_HIKE','weighted_median_mortgage_change_12m_pp'))}, activity median trough {fmt_month(p('LAST_HIKE','weighted_median_activity_trough_month'))}, house-price 12M median {fmt_pct(p('LAST_HIKE','weighted_median_house_price_ret_12m'))}, 24M {fmt_pct(p('LAST_HIKE','weighted_median_house_price_ret_24m'))}.","LAST_HIKE"),
        ("H-Q07","What changes by PAUSE_START?",
         f"PAUSE mortgage 12M change {fmt_pp(p('PAUSE_START','weighted_median_mortgage_change_12m_pp'))}; HOUST 12M {fmt_pct(p('PAUSE_START','weighted_median_houst_change_12m'))}; PERMIT 12M {fmt_pct(p('PAUSE_START','weighted_median_permit_change_12m'))}; house-price 12M {fmt_pct(p('PAUSE_START','weighted_median_house_price_ret_12m'))}.","PAUSE_START"),
        ("H-Q08","What changes by FIRST_CUT?",
         f"FIRST_CUT mortgage 12M change {fmt_pp(p('FIRST_CUT','weighted_median_mortgage_change_12m_pp'))}; housing activity and house-price paths remain heterogeneous; house-price 12M median {fmt_pct(p('FIRST_CUT','weighted_median_house_price_ret_12m'))}, 24M {fmt_pct(p('FIRST_CUT','weighted_median_house_price_ret_24m'))}.","FIRST_CUT"),
        ("H-Q09","Why can house prices remain positive while housing activity contracts?",
         "Prices are a slow stock/transaction outcome while permits, starts and new-home sales are flow/activity measures. Supply constraints, lock-in, composition and nominal-price stickiness can make activity weaken before national price indexes decline. 034 documents sequencing but does not identify each channel causally.","INTERPRETATION"),
        ("H-Q10","Why can mortgage rates fall before house prices recover?",
         "Mortgage rates and Treasury yields reprice financial conditions quickly; housing transactions and prices adjust through search, inventory, refinancing/lock-in and construction pipelines. The historical lag panel measures timing differences only.","INTERPRETATION"),
        ("H-Q11","How exceptional is 2006-09 relative to other episodes?",
         "B05 is kept as an explicit case audit because it contains the largest canonical housing declines around LAST_HIKE/PAUSE/FIRST_CUT and should not disappear inside phase medians.","CASE_B05"),
        ("H-Q12","What does the 2022-24 episode show about financing pressure versus price resilience?",
         "B07 is separately audited: the 2022 FIRST_HIKE and 2023 LAST_HIKE/PAUSE anchors can show large financing-rate pressure while the national price index remains much more resilient than B05. This is descriptive heterogeneity, not a forecast.","CASE_B07"),
        ("H-Q13","What can be said about housing recovery clocks?",
         "Canonical 015 recovery estimates remain phase- and support-dependent. LAST_HIKE has supported recovery evidence; FIRST_HIKE/PAUSE/FIRST_CUT recovery evidence is more limited. Recovery is only defined for episodes with positive declines.","RECOVERY"),
        ("H-Q14","What cannot be inferred causally from these medians?",
         "The phase anchor is not an identified monetary-policy shock; mortgage rates, activity and prices react to common macro forces. Lag ordering is not a causal transmission coefficient.","BOUNDARY"),
        ("H-Q15","What should PandaAI show for housing without making a house-price forecast?",
         "Show phase, mortgage/DGS10/spread changes, permits/starts/new-sales activity changes and trough months, canonical 12/24M house-price path, decline/recovery support, episode heterogeneity, freshness and explicit non-causal/not-forecast boundaries.","PANDAAI"),
    ]
    qdf=pd.DataFrame(qrows,columns=["question_id","question_en","answer_zh","evidence_layer"])
    if len(qdf)!=15:
        raise RuntimeError("expected 15 housing questions")
    qdf.to_csv(OUT/"HOUSING_INVESTOR_QUESTION_REGISTRY.csv",index=False)

    # Human synthesis.
    lines=[
        "# Housing Lag Chain — 034",
        "",
        "## 核心框架",
        "",
        "住房不是股票。更合适的历史时钟是：**融资价格先变 → 许可/开工/新房销售等活动量调整 → 全国房价更慢地反映**。034只验证这种历史排序是否经常出现，不把它当作Fed因果系数。",
        "",
    ]
    for a,label in [("FIRST_HIKE","加息启动"),("LAST_HIKE","最后一次加息"),("PAUSE_START","暂停"),("FIRST_CUT","第一次降息")]:
        lines += [
            f"## {a}｜{label}",
            "",
            f"- 30Y mortgage 12M变化中位：{fmt_pp(p(a,'weighted_median_mortgage_change_12m_pp'))}",
            f"- mortgage 最大压力月份中位：{fmt_month(p(a,'weighted_median_mortgage_max_pressure_month'))}",
            f"- PERMIT 12M变化 / trough：{fmt_pct(p(a,'weighted_median_permit_change_12m'))} / {fmt_month(p(a,'weighted_median_permit_trough_month'))}",
            f"- HOUST 12M变化 / trough：{fmt_pct(p(a,'weighted_median_houst_change_12m'))} / {fmt_month(p(a,'weighted_median_houst_trough_month'))}",
            f"- New-home sales 12M变化 / trough：{fmt_pct(p(a,'weighted_median_sales_change_12m'))} / {fmt_month(p(a,'weighted_median_sales_trough_month'))}",
            f"- Case-Shiller 12M / 24M：{fmt_pct(p(a,'weighted_median_house_price_ret_12m'))} / {fmt_pct(p(a,'weighted_median_house_price_ret_24m'))}",
            f"- 24M price decline中位：{mag(p(a,'weighted_median_house_decline_24m')) if pd.notna(p(a,'weighted_median_house_decline_24m')) else 'NA'}",
            "",
        ]
    lines += [
        "## 为什么价格比活动慢",
        "",
        "许可、开工和新房销售是流量/活动指标；Case-Shiller是成交房屋价格的慢变量指数。融资成本变化可以先压缩需求和建设活动，但价格还会受库存、卖方锁定效应、区域结构和交易构成影响。因此“成交冷”与“全国价格还没跌”可以同时发生。",
        "",
        "## 两个必须单独看的案例",
        "",
        "**B05（2004-07紧缩→住房危机）**：这是整个样本里最重要的负向住房路径之一，不能被相对温和的其他周期平均掉。",
        "",
        "**B07（2022-23紧缩）**：融资成本冲击很大，但全国房价路径明显比B05更有韧性，说明利率只是住房结果的一部分条件。",
        "",
        "## 投资认知边界",
        "",
        "034提供的是历史slow-moving sequencing：融资条件、活动量和价格可能在不同月份达到压力点。它不能回答某个城市、某套房什么时候应该买，也不能把全国中位数直接搬到悉尼或其他地区。",
    ]
    (OUT/"HOUSING_LAG_CHAIN_SYNTHESIS_ZH.md").write_text("\n".join(lines)+"\n")

    schema={
        "module":"FED-CYCLE-HOUSING-LAG-CHAIN-034",
        "layers":{
            "financing":["MORTGAGE30US","DGS10","MORTGAGE_SPREAD_PP"],
            "activity":["PERMIT","HOUST","HSN1F"],
            "price":["CSUSHPINSA_CANONICAL_014_015"]
        },
        "required_fields":[
            "phase","financing_changes","activity_changes","activity_troughs",
            "price_12m_24m","decline_24m","recovery_support","episode_case_flags",
            "source_snapshot","boundary"
        ],
        "prohibited_outputs":[
            "best_housing_phase","expected_house_price_return","home_buying_timing",
            "causal_transmission_lag","city_level_extrapolation"
        ],
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"PANDAAI_HOUSING_LAG_SCHEMA.json").write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# FED-CYCLE-HOUSING-LAG-CHAIN-034 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED HOUSING FINANCING -> ACTIVITY -> PRICE LAG MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- canonical housing anchors: {len(anchors)}",
        f"- financing event rows: {len(fmet)}",
        f"- activity event rows: {len(amet)}",
        f"- lag-chain episode rows: {len(panel)}",
        f"- phase summary rows: {len(psum)}",
        f"- B05/B07 case-audit rows: {len(case)}",
        f"- investor questions: {len(qdf)}",
        "",
        "Price outcomes are copied from canonical 014/015; new source histories are used only to derive financing/activity context. Housing risk remains DECLINE_24M and timing differences are descriptive, not causal transmission estimates.",
    ]
    (OUT/"FED_CYCLE_HOUSING_LAG_CHAIN_034_REPORT.md").write_text("\n".join(report)+"\n")

    # QC.
    if len(anchors)!=28:
        raise RuntimeError(f"expected 28 canonical housing anchors, got {len(anchors)}")
    if len(fmet)!=28*3 or len(amet)!=28*3 or len(panel)!=28:
        raise RuntimeError("unexpected metric row counts")
    if not (panel["interpretation_guardrail"].str.contains("not causal",case=False,regex=False)).all():
        raise RuntimeError("causal lag guardrail lost")
    if not (psum["path_risk_metric"]=="DECLINE_24M").all():
        raise RuntimeError("housing risk metric changed")
    if not {"B05","B07"}.issubset(set(case["broad_episode_id"])):
        raise RuntimeError("case audit lost B05/B07")
    if reg["last_month"].isna().any():
        raise RuntimeError("source last month missing")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-HOUSING-LAG-CHAIN-034",
        "upstream_qc":{"014":q014["qc_gate"],"015":q015["qc_gate"],"032":q032["qc_gate"]},
        "canonical_anchor_rows":int(len(anchors)),
        "current_2026_candidate_leaks":0,
        "downloaded_source_rows":int(len(reg)),
        "all_source_hashes_recorded":bool(reg["sha256"].str.len().eq(64).all()),
        "mortgage_methodology_change_note_retained":True,
        "activity_trailing_3m_average":True,
        "baseline_month_rule":"M_MINUS_1",
        "interpolation_used":False,
        "canonical_house_price_summary_exact_match":True,
        "housing_path_risk_metric":"DECLINE_24M",
        "financing_event_rows":int(len(fmet)),
        "activity_event_rows":int(len(amet)),
        "lag_chain_episode_rows":int(len(panel)),
        "phase_summary_rows":int(len(psum)),
        "b05_b07_case_audit_rows":int(len(case)),
        "investor_questions":int(len(qdf)),
        "lag_differences_causal":False,
        "best_housing_phase_outputs":0,
        "expected_house_price_forecasts":0,
        "home_buying_recommendations":0,
        "new_pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE"
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
