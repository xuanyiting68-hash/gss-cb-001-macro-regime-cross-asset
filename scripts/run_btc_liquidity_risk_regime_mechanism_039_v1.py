#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"btc_liquidity_risk_regime_mechanism_039_v1"
OUT.mkdir(parents=True,exist_ok=True)

LOCK=ROOT/"research"/"BTC_LIQUIDITY_RISK_REGIME_MECHANISM_039_LOCK.md"
SPEC=ROOT/"data"/"public"/"BTC_MECHANISM_SOURCE_SPEC_20260926.csv"
LIT=ROOT/"data"/"public"/"BTC_MECHANISM_LITERATURE_REGISTRY_20260926.csv"
Q038=ROOT/"results"/"cross_asset_evidence_upgrade_rollup_038_v1"/"QC.json"

LAST_COMPLETE=pd.Period("2026-08",freq="M")
FIRST_ANALYSIS=pd.Period("2014-11",freq="M")

ERAS=[
    ("ERA_1_EARLY",pd.Period("2014-11",freq="M"),pd.Period("2017-12",freq="M")),
    ("ERA_2_INSTITUTIONALIZATION",pd.Period("2018-01",freq="M"),pd.Period("2021-12",freq="M")),
    ("ERA_3_POST_2022",pd.Period("2022-01",freq="M"),pd.Period("2026-08",freq="M")),
]

MECHANISMS=[
    "NASDAQ_RET",
    "DXY_RET",
    "DFII10_CHANGE_PP",
    "VIX_CHANGE",
    "NFCI_CHANGE",
    "WALCL_3M_PCT",
    "M2SL_3M_PCT",
]

STATE_DEFS={
    "NASDAQ_RET":("NASDAQ_UP","NASDAQ_DOWN_OR_FLAT"),
    "DXY_RET":("DXY_UP","DXY_DOWN_OR_FLAT"),
    "DFII10_CHANGE_PP":("REAL_YIELD_UP","REAL_YIELD_DOWN_OR_FLAT"),
    "VIX_CHANGE":("VIX_UP","VIX_DOWN_OR_FLAT"),
    "NFCI_CHANGE":("NFCI_TIGHTENING","NFCI_EASING_OR_FLAT"),
    "WALCL_3M_PCT":("WALCL_EXPANDING_3M","WALCL_CONTRACTING_OR_FLAT_3M"),
    "M2SL_3M_PCT":("M2_EXPANDING_3M","M2_CONTRACTING_OR_FLAT_3M"),
}

ALLOWED_EVIDENCE={
    "SUPPORTED_DESCRIPTIVE",
    "LIMITED_DESCRIPTIVE",
    "INSUFFICIENT_VARIATION",
    "SIGN_STABLE_ALL_ERAS",
    "ERA_DEPENDENT",
    "INSUFFICIENT_ERA_SUPPORT",
    "TIME_VARIATION_DIAGNOSTIC",
    "LITERATURE_CONTEXT",
    "NOT_TESTED_DIRECTLY",
    "CAUSAL_CLAIM_NOT_IDENTIFIED",
}

def read_pass(path:Path):
    q=json.loads(path.read_text())
    if q.get("qc_gate")!="PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def fetch_bytes(url:str, timeout:int=120)->tuple[bytes,int]:
    err=None
    for attempt in range(4):
        try:
            req=urllib.request.Request(
                url,
                headers={
                    "User-Agent":"Mozilla/5.0 gss-cb-001-btc-mechanism/1.0",
                    "Accept":"*/*",
                },
            )
            with urllib.request.urlopen(req,timeout=timeout) as resp:
                raw=resp.read()
            if len(raw)<100:
                raise RuntimeError(f"short response: {len(raw)} bytes")
            return raw,attempt+1
        except Exception as exc:
            err=exc
            if attempt<3:
                time.sleep(2*(attempt+1))
    raise RuntimeError(f"fetch failed after retries: {url}: {err}")

def fetch_yahoo(symbol:str):
    enc=urllib.parse.quote(symbol,safe="")
    urls=[
        f"https://query1.finance.yahoo.com/v8/finance/chart/{enc}?period1=0&period2=1893456000&interval=1d&events=history&includeAdjustedClose=true",
        f"https://query2.finance.yahoo.com/v8/finance/chart/{enc}?period1=0&period2=1893456000&interval=1d&events=history&includeAdjustedClose=true",
    ]
    errs=[]
    for url in urls:
        try:
            raw,attempt=fetch_bytes(url,timeout=120)
            obj=json.loads(raw.decode("utf-8"))
            result=obj.get("chart",{}).get("result")
            if not result:
                raise RuntimeError(str(obj.get("chart",{}).get("error")))
            block=result[0]
            ts=block.get("timestamp") or []
            quote=(block.get("indicators",{}).get("quote") or [{}])[0]
            vals=quote.get("close") or []
            if not ts or len(ts)!=len(vals):
                raise RuntimeError("timestamp/close length mismatch")
            df=pd.DataFrame({
                "date":pd.to_datetime(ts,unit="s",utc=True).tz_convert(None).normalize(),
                "value":pd.to_numeric(vals,errors="coerce"),
            }).dropna().sort_values("date").drop_duplicates("date",keep="last")
            return df,{
                "url":url,"method":"YAHOO_FINANCE_CHART_JSON","price_field":"close",
                "sha256":sha(raw),"raw_bytes":len(raw),"fetch_attempt":attempt,
            }
        except Exception as exc:
            errs.append(f"{url}: {exc!r}")
    raise RuntimeError(" | ".join(errs))

def fetch_fred(series_id:str,url:str):
    raw,attempt=fetch_bytes(url,timeout=120)
    df=pd.read_csv(io.BytesIO(raw))
    if len(df.columns)<2:
        raise RuntimeError(f"bad FRED CSV for {series_id}")
    date_col=df.columns[0]
    value_col=series_id if series_id in df.columns else df.columns[1]
    x=df[[date_col,value_col]].copy()
    x.columns=["date","value"]
    x["date"]=pd.to_datetime(x["date"],errors="coerce")
    x["value"]=pd.to_numeric(x["value"],errors="coerce")
    x=x.dropna(subset=["date","value"]).sort_values("date").drop_duplicates("date",keep="last")
    return x,{
        "url":url,"method":"FRED_DIRECT_CSV","price_field":"",
        "sha256":sha(raw),"raw_bytes":len(raw),"fetch_attempt":attempt,
    }

def monthly_mean(df:pd.DataFrame)->pd.DataFrame:
    x=df.copy()
    x["period"]=x["date"].dt.to_period("M")
    return x.groupby("period",as_index=False)["value"].mean().sort_values("period")

def monthly_last(df:pd.DataFrame)->pd.DataFrame:
    x=df.copy()
    x["period"]=x["date"].dt.to_period("M")
    return x.groupby("period",as_index=False)["value"].last().sort_values("period")

def corr_sign(x):
    if pd.isna(x):
        return "NA"
    if x>0: return "POSITIVE"
    if x<0: return "NEGATIVE"
    return "ZERO"

def pearson_spearman(df,xcol,ycol):
    z=df[[xcol,ycol]].dropna()
    if len(z)<3:
        return len(z),np.nan,np.nan
    p=float(z[xcol].corr(z[ycol],method="pearson"))
    # Spearman without scipy: Pearson correlation of average ranks.
    rx=z[xcol].rank(method="average")
    ry=z[ycol].rank(method="average")
    s=float(rx.corr(ry,method="pearson"))
    return len(z),p,s

def era_for(period:pd.Period)->str:
    for name,start,end in ERAS:
        if start<=period<=end:
            return name
    return "OUTSIDE_FROZEN_ERAS"

def state_support(n_a:int,n_b:int)->str:
    m=min(n_a,n_b)
    if m>=18: return "SUPPORTED_DESCRIPTIVE"
    if m>=9: return "LIMITED_DESCRIPTIVE"
    return "INSUFFICIENT_VARIATION"

def med(x):
    x=pd.to_numeric(x,errors="coerce").dropna()
    return float(x.median()) if len(x) else np.nan

def share_pos(x):
    x=pd.to_numeric(x,errors="coerce").dropna()
    return float((x>0).mean()) if len(x) else np.nan

def fmt_corr(v):
    return "NA" if pd.isna(v) else f"{v:+.3f}"

def fmt_pct(v):
    return "NA" if pd.isna(v) else f"{v*100:+.1f}%"

def build_scope_assoc(panel,scope,era=None):
    z=panel if era is None else panel[panel["ERA"]==era]
    rows=[]
    for mech in MECHANISMS:
        n,p,s=pearson_spearman(z,"BTC_RET",mech)
        rows.append({
            "scope":scope,"mechanism":mech,"paired_months":n,
            "pearson":p,"spearman":s,
            "pearson_sign":corr_sign(p),"spearman_sign":corr_sign(s),
            "causal_status":"NONE",
        })
    return pd.DataFrame(rows)

def build_state_contrasts(panel):
    scopes=[("FULL_SAMPLE",None)]+[(name,name) for name,_,__ in ERAS]
    out=[]
    for scope,era in scopes:
        z=panel if era is None else panel[panel["ERA"]==era]
        for mech in MECHANISMS:
            a,b=STATE_DEFS[mech]
            zz=z[["BTC_RET",mech]].dropna().copy()
            za=zz[zz[mech]>0]
            zb=zz[zz[mech]<=0]
            ma=med(za["BTC_RET"]); mb=med(zb["BTC_RET"])
            out.append({
                "scope":scope,"mechanism":mech,
                "state_a":a,"state_b":b,
                "n_a":len(za),"n_b":len(zb),
                "median_btc_ret_a":ma,"median_btc_ret_b":mb,
                "positive_btc_share_a":share_pos(za["BTC_RET"]),
                "positive_btc_share_b":share_pos(zb["BTC_RET"]),
                "oriented_median_diff_a_minus_b":ma-mb if pd.notna(ma) and pd.notna(mb) else np.nan,
                "support_status":state_support(len(za),len(zb)),
                "causal_status":"NONE",
            })
    return pd.DataFrame(out)

def rolling36(panel):
    rows=[]
    for mech in MECHANISMS:
        for i in range(35,len(panel)):
            w=panel.iloc[i-35:i+1]
            z=w[["BTC_RET",mech]]
            if z.notna().all().all() and len(z)==36:
                corr=float(z["BTC_RET"].corr(z[mech]))
                rows.append({
                    "mechanism":mech,
                    "window_start":str(w.iloc[0]["month"]),
                    "window_end":str(w.iloc[-1]["month"]),
                    "paired_months":36,
                    "pearson_36m":corr,
                    "status":"TIME_VARIATION_DIAGNOSTIC",
                })
    return pd.DataFrame(rows)

def main():
    q038=read_pass(Q038)
    spec=pd.read_csv(SPEC)
    lit=pd.read_csv(LIT)
    if len(spec)!=8:
        raise RuntimeError(f"expected 8 source rows, got {len(spec)}")
    if len(lit)!=2 or set(lit["status"])!={"LITERATURE_CONTEXT"}:
        raise RuntimeError("literature registry drift")

    retrieved=datetime.now(timezone.utc).isoformat()
    raw={}
    prov=[]

    # Market sources.
    market_symbols={
        "BTC_USD":"BTC-USD",
        "NASDAQ":"^IXIC",
        "DXY":"DX-Y.NYB",
    }
    for sid,symbol in market_symbols.items():
        df,meta=fetch_yahoo(symbol)
        raw[sid]=df
        srow=spec[spec["series_id"]==sid].iloc[0]
        prov.append({
            "series_id":sid,"layer":srow["layer"],"source":srow["source"],
            "source_url":meta["url"],"frequency":srow["frequency"],
            "transformation":srow["transformation"],"analysis_variable":srow["analysis_variable"],
            "retrieved_utc":retrieved,"sha256":meta["sha256"],"raw_bytes":meta["raw_bytes"],
            "fetch_attempt":meta["fetch_attempt"],"rows_total":len(df),
            "first_date":str(df["date"].min().date()),"last_date":str(df["date"].max().date()),
            "raw_committed":False,"critical_note":srow["critical_note"],
        })

    # FRED sources.
    for sid in ["DFII10","VIXCLS","NFCI","WALCL","M2SL"]:
        srow=spec[spec["series_id"]==sid].iloc[0]
        df,meta=fetch_fred(sid,srow["source_url"])
        raw[sid]=df
        prov.append({
            "series_id":sid,"layer":srow["layer"],"source":srow["source"],
            "source_url":meta["url"],"frequency":srow["frequency"],
            "transformation":srow["transformation"],"analysis_variable":srow["analysis_variable"],
            "retrieved_utc":retrieved,"sha256":meta["sha256"],"raw_bytes":meta["raw_bytes"],
            "fetch_attempt":meta["fetch_attempt"],"rows_total":len(df),
            "first_date":str(df["date"].min().date()),"last_date":str(df["date"].max().date()),
            "raw_committed":False,"critical_note":srow["critical_note"],
        })

    registry=pd.DataFrame(prov).sort_values("series_id")
    if len(registry)!=8 or registry["sha256"].str.len().ne(64).any():
        raise RuntimeError("source registry/hash failure")
    btc_first=pd.Timestamp(registry.loc[registry["series_id"]=="BTC_USD","first_date"].iloc[0])
    if not (pd.Timestamp("2014-09-01")<=btc_first<=pd.Timestamp("2014-09-30")):
        raise RuntimeError(f"unexpected BTC source start {btc_first}")
    if not registry.loc[registry["series_id"]=="M2SL","critical_note"].str.contains("2020",regex=False).all():
        raise RuntimeError("M2 definition caveat missing")
    registry.to_csv(OUT/"SOURCE_REGISTRY.csv",index=False)

    # Build monthly level series.
    m={}
    for sid in ["BTC_USD","NASDAQ","DXY"]:
        x=monthly_mean(raw[sid])
        m[sid]=x.set_index("period")["value"].astype(float)
    for sid in ["DFII10","VIXCLS","NFCI","WALCL"]:
        x=monthly_mean(raw[sid])
        m[sid]=x.set_index("period")["value"].astype(float)
    x=monthly_last(raw["M2SL"])
    m["M2SL"]=x.set_index("period")["value"].astype(float)

    periods=pd.period_range(pd.Period("2014-10",freq="M"),LAST_COMPLETE,freq="M")
    panel=pd.DataFrame({"period":periods})
    for sid in ["BTC_USD","NASDAQ","DXY","DFII10","VIXCLS","NFCI","WALCL","M2SL"]:
        panel[sid+"_LEVEL"]=panel["period"].map(m[sid])

    # Transformations must be calculated from source series before analysis-start filtering.
    transforms=pd.DataFrame(index=periods)
    transforms["BTC_RET"]=m["BTC_USD"].pct_change(fill_method=None)
    transforms["NASDAQ_RET"]=m["NASDAQ"].pct_change(fill_method=None)
    transforms["DXY_RET"]=m["DXY"].pct_change(fill_method=None)
    transforms["DFII10_CHANGE_PP"]=m["DFII10"].diff()
    transforms["VIX_CHANGE"]=m["VIXCLS"].diff()
    transforms["NFCI_CHANGE"]=m["NFCI"].diff()
    transforms["WALCL_3M_PCT"]=m["WALCL"].pct_change(3,fill_method=None)
    transforms["M2SL_3M_PCT"]=m["M2SL"].pct_change(3,fill_method=None)
    for col in MECHANISMS+["BTC_RET"]:
        panel[col]=panel["period"].map(transforms[col])

    panel=panel[(panel["period"]>=FIRST_ANALYSIS)&(panel["period"]<=LAST_COMPLETE)].copy()
    panel["month"]=panel["period"].astype(str)
    panel["ERA"]=panel["period"].apply(era_for)
    panel["M2_POST_MAY2020_DEFINITION"]=panel["period"]>=pd.Period("2020-05",freq="M")
    panel=panel[
        ["month","ERA","M2_POST_MAY2020_DEFINITION",
         "BTC_USD_LEVEL","BTC_RET",
         "NASDAQ_LEVEL","NASDAQ_RET",
         "DXY_LEVEL","DXY_RET",
         "DFII10_LEVEL","DFII10_CHANGE_PP",
         "VIXCLS_LEVEL","VIX_CHANGE",
         "NFCI_LEVEL","NFCI_CHANGE",
         "WALCL_LEVEL","WALCL_3M_PCT",
         "M2SL_LEVEL","M2SL_3M_PCT"]
    ].reset_index(drop=True)
    panel.to_csv(OUT/"BTC_MECHANISM_MONTHLY_PANEL.csv",index=False)

    if panel.iloc[0]["month"]!="2014-11" or panel.iloc[-1]["month"]!="2026-08":
        raise RuntimeError("analysis endpoints drift")
    if set(panel["ERA"])!={x[0] for x in ERAS}:
        raise RuntimeError("era labels incomplete")

    # Associations.
    full=build_scope_assoc(panel,"FULL_SAMPLE")
    full.to_csv(OUT/"BTC_FULL_SAMPLE_ASSOCIATIONS.csv",index=False)
    era_frames=[]
    for name,_,__ in ERAS:
        era_frames.append(build_scope_assoc(panel,name,name))
    era_assoc=pd.concat(era_frames,ignore_index=True)
    era_assoc.to_csv(OUT/"BTC_FIXED_ERA_ASSOCIATIONS.csv",index=False)

    stability=[]
    for mech in MECHANISMS:
        g=era_assoc[era_assoc["mechanism"]==mech].copy()
        enough=bool((g["paired_months"]>=24).all()) and len(g)==3
        signs=list(g["pearson_sign"])
        if not enough:
            status="INSUFFICIENT_ERA_SUPPORT"
        elif len(set(signs))==1:
            status="SIGN_STABLE_ALL_ERAS"
        else:
            status="ERA_DEPENDENT"
        stability.append({
            "mechanism":mech,
            "era_1_n":int(g.loc[g["scope"]=="ERA_1_EARLY","paired_months"].iloc[0]),
            "era_1_pearson":float(g.loc[g["scope"]=="ERA_1_EARLY","pearson"].iloc[0]),
            "era_2_n":int(g.loc[g["scope"]=="ERA_2_INSTITUTIONALIZATION","paired_months"].iloc[0]),
            "era_2_pearson":float(g.loc[g["scope"]=="ERA_2_INSTITUTIONALIZATION","pearson"].iloc[0]),
            "era_3_n":int(g.loc[g["scope"]=="ERA_3_POST_2022","paired_months"].iloc[0]),
            "era_3_pearson":float(g.loc[g["scope"]=="ERA_3_POST_2022","pearson"].iloc[0]),
            "pearson_signs":"|".join(signs),
            "era_stability_status":status,
        })
    stab=pd.DataFrame(stability)
    if not set(stab["era_stability_status"]).issubset({"SIGN_STABLE_ALL_ERAS","ERA_DEPENDENT","INSUFFICIENT_ERA_SUPPORT"}):
        raise RuntimeError("bad era stability status")
    stab.to_csv(OUT/"BTC_ERA_STABILITY.csv",index=False)

    # State contrasts.
    contrasts=build_state_contrasts(panel)
    contrasts.to_csv(OUT/"BTC_STATE_CONTRASTS.csv",index=False)

    # Post-run amendment: audit whether full-sample state support is also
    # comparable within every preregistered era.
    support_audit=[]
    for mech in MECHANISMS:
        full_row=contrasts[(contrasts["scope"]=="FULL_SAMPLE")&(contrasts["mechanism"]==mech)].iloc[0]
        eg=contrasts[(contrasts["scope"]!="FULL_SAMPLE")&(contrasts["mechanism"]==mech)].copy()
        if len(eg)!=3:
            raise RuntimeError(f"state-support era rows missing for {mech}")
        supported=int((eg["support_status"]=="SUPPORTED_DESCRIPTIVE").sum())
        limited=int((eg["support_status"]=="LIMITED_DESCRIPTIVE").sum())
        insufficient=int((eg["support_status"]=="INSUFFICIENT_VARIATION").sum())
        if insufficient>0:
            comp="WEAK_STATE_COMPARABILITY"
        elif limited>0:
            comp="PARTIAL_STATE_COMPARABILITY"
        else:
            comp="ROBUST_STATE_COMPARABILITY"
        support_audit.append({
            "mechanism":mech,
            "full_sample_support":full_row["support_status"],
            "era_1_min_state_count":int(min(
                eg.loc[eg["scope"]=="ERA_1_EARLY","n_a"].iloc[0],
                eg.loc[eg["scope"]=="ERA_1_EARLY","n_b"].iloc[0])),
            "era_2_min_state_count":int(min(
                eg.loc[eg["scope"]=="ERA_2_INSTITUTIONALIZATION","n_a"].iloc[0],
                eg.loc[eg["scope"]=="ERA_2_INSTITUTIONALIZATION","n_b"].iloc[0])),
            "era_3_min_state_count":int(min(
                eg.loc[eg["scope"]=="ERA_3_POST_2022","n_a"].iloc[0],
                eg.loc[eg["scope"]=="ERA_3_POST_2022","n_b"].iloc[0])),
            "supported_eras":supported,
            "limited_eras":limited,
            "insufficient_eras":insufficient,
            "cross_era_state_comparability":comp,
            "diagnostic_status":"POST_RUN_STATE_SUPPORT_AUDIT",
        })
    state_audit=pd.DataFrame(support_audit)
    state_audit.to_csv(OUT/"BTC_STATE_SUPPORT_AUDIT.csv",index=False)

    # Rolling 36m diagnostic.
    roll=rolling36(panel)
    if len(roll)==0:
        raise RuntimeError("no rolling 36M windows")
    roll.to_csv(OUT/"BTC_ROLLING_36M_CORRELATIONS.csv",index=False)
    rs=[]
    for mech in MECHANISMS:
        g=roll[roll["mechanism"]==mech].copy()
        if len(g)==0:
            rs.append({
                "mechanism":mech,"rolling_windows":0,"median_pearson_36m":np.nan,
                "min_pearson_36m":np.nan,"max_pearson_36m":np.nan,
                "positive_window_share":np.nan,"latest_window_end":"","latest_pearson_36m":np.nan,
                "status":"TIME_VARIATION_DIAGNOSTIC",
            })
        else:
            last=g.iloc[-1]
            rs.append({
                "mechanism":mech,"rolling_windows":len(g),
                "median_pearson_36m":float(g["pearson_36m"].median()),
                "min_pearson_36m":float(g["pearson_36m"].min()),
                "max_pearson_36m":float(g["pearson_36m"].max()),
                "positive_window_share":float((g["pearson_36m"]>0).mean()),
                "latest_window_end":last["window_end"],
                "latest_pearson_36m":float(last["pearson_36m"]),
                "status":"TIME_VARIATION_DIAGNOSTIC",
            })
    rsum=pd.DataFrame(rs)
    rsum.to_csv(OUT/"BTC_ROLLING_CORRELATION_SUMMARY.csv",index=False)

    # Evidence matrix.
    ev=[]
    full_idx=full.set_index("mechanism")
    stab_idx=stab.set_index("mechanism")
    roll_idx=rsum.set_index("mechanism")
    full_con=contrasts[contrasts["scope"]=="FULL_SAMPLE"].set_index("mechanism")
    state_audit_idx=state_audit.set_index("mechanism")
    for mech in MECHANISMS:
        f=full_idx.loc[mech]
        s=stab_idx.loc[mech]
        r=roll_idx.loc[mech]
        sc=full_con.loc[mech]
        sa=state_audit_idx.loc[mech]
        ev.append({
            "mechanism":mech,
            "evidence_status":s["era_stability_status"],
            "full_paired_months":int(f["paired_months"]),
            "full_pearson":f["pearson"],
            "full_spearman":f["spearman"],
            "era_1_pearson":s["era_1_pearson"],
            "era_2_pearson":s["era_2_pearson"],
            "era_3_pearson":s["era_3_pearson"],
            "full_state_support":sc["support_status"],
            "full_state_median_diff_a_minus_b":sc["oriented_median_diff_a_minus_b"],
            "cross_era_state_comparability":sa["cross_era_state_comparability"],
            "era_1_min_state_count":sa["era_1_min_state_count"],
            "era_2_min_state_count":sa["era_2_min_state_count"],
            "era_3_min_state_count":sa["era_3_min_state_count"],
            "rolling_36m_min":r["min_pearson_36m"],
            "rolling_36m_max":r["max_pearson_36m"],
            "rolling_36m_latest":r["latest_pearson_36m"],
            "interpretation_boundary":"Contemporaneous association/time variation only; no causal or predictive ranking.",
        })
    evdf=pd.DataFrame(ev)
    if not set(evdf["evidence_status"]).issubset(ALLOWED_EVIDENCE):
        raise RuntimeError("evidence matrix status outside lock")
    evdf.to_csv(OUT/"BTC_MECHANISM_EVIDENCE_MATRIX.csv",index=False)

    lit.to_csv(OUT/"BTC_LITERATURE_CONTEXT.csv",index=False)

    # Myth audit: design-aware, no causal overclaim.
    nas_st=stab_idx.loc["NASDAQ_RET","era_stability_status"]
    dxy_st=stab_idx.loc["DXY_RET","era_stability_status"]
    rr_st=stab_idx.loc["DFII10_CHANGE_PP","era_stability_status"]
    wal_st=stab_idx.loc["WALCL_3M_PCT","era_stability_status"]
    myth_rows=[
        {
            "myth_id":"BTC-MYTH-01",
            "claim":"Bitcoin is always uncorrelated with stocks.",
            "audit_result":"Historical BTC-Nasdaq association is measured directly and varies by fixed era; it should not be treated as a permanent zero-correlation property.",
            "evidence_status":nas_st,
            "source":"BTC_FIXED_ERA_ASSOCIATIONS.csv",
        },
        {
            "myth_id":"BTC-MYTH-02",
            "claim":"Bitcoin is established here as digital gold.",
            "audit_result":"039 does not include a direct Bitcoin-vs-Gold equivalence test, so this label is not established by the design.",
            "evidence_status":"NOT_TESTED_DIRECTLY",
            "source":"039 design boundary",
        },
        {
            "myth_id":"BTC-MYTH-03",
            "claim":"Fed tightening always hurts Bitcoin.",
            "audit_result":"039 contains real-yield, financial-conditions and balance-sheet proxies but no identified monetary-policy shock. A universal causal Fed claim is not identified.",
            "evidence_status":"CAUSAL_CLAIM_NOT_IDENTIFIED",
            "source":"BTC_MECHANISM_EVIDENCE_MATRIX.csv + design boundary",
        },
        {
            "myth_id":"BTC-MYTH-04",
            "claim":"A stronger dollar always means Bitcoin falls.",
            "audit_result":"The BTC-DXY sign is audited across three fixed eras rather than assumed; a fixed universal rule requires sign stability that the era table must show.",
            "evidence_status":dxy_st,
            "source":"BTC_ERA_STABILITY.csv",
        },
        {
            "myth_id":"BTC-MYTH-05",
            "claim":"Higher real yields always hurt Bitcoin.",
            "audit_result":"The BTC-real-yield association is audited across fixed eras; 039 does not impose the textbook sign.",
            "evidence_status":rr_st,
            "source":"BTC_ERA_STABILITY.csv",
        },
        {
            "myth_id":"BTC-MYTH-06",
            "claim":"Fed balance-sheet expansion mechanically causes Bitcoin gains.",
            "audit_result":"WALCL is a balance-sheet-scale proxy and the analysis is contemporaneous association only; mechanical causality is not identified.",
            "evidence_status":"CAUSAL_CLAIM_NOT_IDENTIFIED",
            "source":"BTC_STATE_CONTRASTS.csv + design boundary",
        },
        {
            "myth_id":"BTC-MYTH-07",
            "claim":"M2 growth is a clean Bitcoin liquidity signal.",
            "audit_result":"M2 is a broad money-stock context variable, has a 2020 definition/composition caveat, and 039 does not treat it as an identified liquidity shock or forecast signal.",
            "evidence_status":"CAUSAL_CLAIM_NOT_IDENTIFIED",
            "source":"SOURCE_REGISTRY.csv + BTC_STATE_CONTRASTS.csv",
        },
    ]
    myths=pd.DataFrame(myth_rows)
    if not set(myths["evidence_status"]).issubset(ALLOWED_EVIDENCE):
        raise RuntimeError("myth evidence status outside lock")
    myths.to_csv(OUT/"BTC_MECHANISM_MYTH_AUDIT.csv",index=False)

    # Question registry.
    era_idx=era_assoc.set_index(["mechanism","scope"])
    def era_vals(mech):
        return (
            era_idx.loc[(mech,"ERA_1_EARLY"),"pearson"],
            era_idx.loc[(mech,"ERA_2_INSTITUTIONALIZATION"),"pearson"],
            era_idx.loc[(mech,"ERA_3_POST_2022"),"pearson"],
        )
    n1,n2,n3=era_vals("NASDAQ_RET")
    d1,d2,d3=era_vals("DXY_RET")
    rr1,rr2,rr3=era_vals("DFII10_CHANGE_PP")
    v1,v2,v3=era_vals("VIX_CHANGE")
    nf1,nf2,nf3=era_vals("NFCI_CHANGE")
    w1,w2,w3=era_vals("WALCL_3M_PCT")
    m1,m2,m3=era_vals("M2SL_3M_PCT")

    def state_full(mech):
        return full_con.loc[mech]
    qs=[
        ("BTC-Q01","Has Bitcoin's Nasdaq association changed across fixed eras?",
         f"Pearson by era: {fmt_corr(n1)} / {fmt_corr(n2)} / {fmt_corr(n3)}; status {stab_idx.loc['NASDAQ_RET','era_stability_status']}.","RISK_BETA"),
        ("BTC-Q02","Is Bitcoin consistently inversely associated with the U.S. dollar?",
         f"BTC-DXY Pearson by era: {fmt_corr(d1)} / {fmt_corr(d2)} / {fmt_corr(d3)}; status {stab_idx.loc['DXY_RET','era_stability_status']}.","USD"),
        ("BTC-Q03","Is the real-yield association stable?",
         f"BTC-DFII10-change Pearson by era: {fmt_corr(rr1)} / {fmt_corr(rr2)} / {fmt_corr(rr3)}; status {stab_idx.loc['DFII10_CHANGE_PP','era_stability_status']}.","REAL_YIELD"),
        ("BTC-Q04","Does BTC behave differently when VIX is rising?",
         f"Full-sample BTC median difference VIX_UP minus VIX_DOWN_OR_FLAT: {fmt_pct(state_full('VIX_CHANGE')['oriented_median_diff_a_minus_b'])}; support {state_full('VIX_CHANGE')['support_status']}.","VIX"),
        ("BTC-Q05","Does BTC behave differently when NFCI is tightening?",
         f"Full-sample BTC median difference NFCI_TIGHTENING minus EASING_OR_FLAT: {fmt_pct(state_full('NFCI_CHANGE')['oriented_median_diff_a_minus_b'])}; support {state_full('NFCI_CHANGE')['support_status']}.","NFCI"),
        ("BTC-Q06","Are WALCL-expansion months systematically different for BTC?",
         f"Full-sample median difference WALCL_EXPANDING_3M minus CONTRACTING_OR_FLAT: {fmt_pct(state_full('WALCL_3M_PCT')['oriented_median_diff_a_minus_b'])}; support {state_full('WALCL_3M_PCT')['support_status']}; cross-era state comparability {state_audit_idx.loc['WALCL_3M_PCT','cross_era_state_comparability']}. This is not causal.","WALCL"),
        ("BTC-Q07","Are M2-expansion months systematically different for BTC?",
         f"Full-sample median difference M2_EXPANDING_3M minus CONTRACTING_OR_FLAT: {fmt_pct(state_full('M2SL_3M_PCT')['oriented_median_diff_a_minus_b'])}; full-sample support {state_full('M2SL_3M_PCT')['support_status']}, but cross-era state comparability {state_audit_idx.loc['M2SL_3M_PCT','cross_era_state_comparability']} (ERA1/ERA2 have zero contracting-or-flat months); retain the 2020 M2 definition caveat.","M2"),
        ("BTC-Q08","Which mechanism signs are stable across all three fixed eras?",
         ", ".join(stab.loc[stab["era_stability_status"]=="SIGN_STABLE_ALL_ERAS","mechanism"].tolist()) or "None.","ERA_STABILITY"),
        ("BTC-Q09","Which mechanisms are era-dependent?",
         ", ".join(stab.loc[stab["era_stability_status"]=="ERA_DEPENDENT","mechanism"].tolist()) or "None.","ERA_STABILITY"),
        ("BTC-Q10","Does the 36M rolling Nasdaq correlation simply rise after 2020?",
         f"039 does not pre-register a monotonic trend test. The fixed 36M diagnostic spans {roll_idx.loc['NASDAQ_RET','min_pearson_36m']:+.3f} to {roll_idx.loc['NASDAQ_RET','max_pearson_36m']:+.3f}; latest {roll_idx.loc['NASDAQ_RET','latest_pearson_36m']:+.3f}.","ROLLING_DIAGNOSTIC"),
        ("BTC-Q11","Is 'Bitcoin is always uncorrelated with stocks' supported?",
         f"No fixed zero-correlation property is assumed. Nasdaq era correlations are {fmt_corr(n1)}, {fmt_corr(n2)}, {fmt_corr(n3)}; literature context also documents stronger crypto-equity interconnectedness over time.","RISK_BETA"),
        ("BTC-Q12","Is 'Bitcoin is digital gold' established by this design?",
         "No. 039 does not directly test BTC against Gold and therefore cannot establish a digital-gold equivalence.","BOUNDARY"),
        ("BTC-Q13","Is 'Fed tightening always hurts Bitcoin' established?",
         "No causal Fed claim is identified. 039 uses contemporaneous market/macro proxies, not a monetary-policy shock series.","BOUNDARY"),
        ("BTC-Q14","Is 'balance-sheet expansion mechanically causes BTC gains' established?",
         "No. WALCL is a Fed balance-sheet-scale proxy; same-month/3M associations do not identify mechanical causality.","BOUNDARY"),
        ("BTC-Q15","What should PandaAI surface?",
         "Era-specific BTC associations, state contrasts, rolling 36M time variation, sample support, source freshness, M2 definition caveat and explicit non-causal/non-forecast boundaries.","PANDAAI"),
    ]
    qdf=pd.DataFrame(qs,columns=["question_id","question_en","answer","evidence_layer"])
    if len(qdf)!=15:
        raise RuntimeError("question registry row count")
    qdf.to_csv(OUT/"BTC_INVESTOR_QUESTION_REGISTRY.csv",index=False)

    # Chinese synthesis.
    stable=stab[stab["era_stability_status"]=="SIGN_STABLE_ALL_ERAS"]["mechanism"].tolist()
    dep=stab[stab["era_stability_status"]=="ERA_DEPENDENT"]["mechanism"].tolist()
    lines=[
        "# Bitcoin Liquidity / Risk-Regime Mechanism Map — 039",
        "",
        "## 结论框架",
        "",
        "Bitcoin只有真实的2014+公开历史，所以039不再假装补更多Fed周期，而是问：它与风险资产、美元、实际利率、市场压力、金融条件和货币/资产负债表变量的关系，是否会随时代变化。",
        "",
        "所有结果都是**同月历史关联**，不是因果冲击，也不是下一月预测。",
        "",
        "## 1. Bitcoin × Nasdaq：风险资产属性是否强化？",
        "",
        f"固定时代 Pearson：2014-11–2017-12 {fmt_corr(n1)}；2018–2021 {fmt_corr(n2)}；2022–2026-08 {fmt_corr(n3)}。Era status：{stab_idx.loc['NASDAQ_RET','era_stability_status']}。",
        "",
        f"36个月滚动相关范围 {roll_idx.loc['NASDAQ_RET','min_pearson_36m']:+.3f} 到 {roll_idx.loc['NASDAQ_RET','max_pearson_36m']:+.3f}，最新窗口 {roll_idx.loc['NASDAQ_RET','latest_pearson_36m']:+.3f}。",
        "",
        "这可以和IMF关于疫情前后crypto-equity interconnectedness上升的文献背景对照，但仓库结果仍以本项目数据为准。",
        "",
        "## 2. Bitcoin × 美元",
        "",
        f"BTC-DXY时代相关：{fmt_corr(d1)} / {fmt_corr(d2)} / {fmt_corr(d3)}；状态 {stab_idx.loc['DXY_RET','era_stability_status']}。",
        "",
        "因此不能先验把“美元涨=BTC跌”当作固定恒等式；是否稳定必须由三个固定时代的符号与状态对比共同判断。",
        "",
        "## 3. Bitcoin × 10Y实际利率",
        "",
        f"BTC与DFII10月变化相关：{fmt_corr(rr1)} / {fmt_corr(rr2)} / {fmt_corr(rr3)}；状态 {stab_idx.loc['DFII10_CHANGE_PP','era_stability_status']}。",
        "",
        "这只是市场实际利率共变，不是identified monetary-policy shock。JIMF 2023 的因果研究使用更严格的货币政策识别，并发现Bitcoin的政策反应本身也随时间改变。",
        "",
        "## 4. VIX / NFCI：压力与金融条件",
        "",
        f"VIX时代相关：{fmt_corr(v1)} / {fmt_corr(v2)} / {fmt_corr(v3)}；NFCI时代相关：{fmt_corr(nf1)} / {fmt_corr(nf2)} / {fmt_corr(nf3)}。",
        "",
        f"全样本状态对比中，VIX_UP minus VIX_DOWN_OR_FLAT 的BTC月收益中位差为 {fmt_pct(state_full('VIX_CHANGE')['oriented_median_diff_a_minus_b'])}；NFCI_TIGHTENING minus EASING_OR_FLAT 为 {fmt_pct(state_full('NFCI_CHANGE')['oriented_median_diff_a_minus_b'])}。",
        "",
        "## 5. WALCL / M2：不能直接叫“流动性因果”",
        "",
        f"WALCL 3M变化的时代相关：{fmt_corr(w1)} / {fmt_corr(w2)} / {fmt_corr(w3)}；M2 3M变化：{fmt_corr(m1)} / {fmt_corr(m2)} / {fmt_corr(m3)}。",
        "",
        "WALCL只是Fed资产负债表规模代理；M2是广义货币存量，而且2020年H.6/Regulation D变化带来定义/构成 caveat。相关关系不能直接翻译成“印钱导致BTC上涨”。",
        "",
        f"状态样本的跨时代可比性：WALCL = {state_audit_idx.loc['WALCL_3M_PCT','cross_era_state_comparability']}；M2 = {state_audit_idx.loc['M2SL_3M_PCT','cross_era_state_comparability']}。特别是M2在前两个固定时代没有任何3个月收缩/持平状态，因此全样本+4.2%的状态差不能写成跨时代规律。",
        "",
        "## 6. Era stability",
        "",
        f"- 三个时代Pearson符号一致：{', '.join(stable) if stable else 'None'}",
        f"- 三个时代符号发生变化：{', '.join(dep) if dep else 'None'}",
        "",
        "符号稳定也不等于因果稳定，更不等于可预测；符号变化则直接反对把该机制写成跨时代固定规律。",
        "",
        "## PandaAI 应该怎样用",
        "",
        "展示：当前机制变量、历史同月关联、固定时代差异、36M滚动相关、状态对比、样本支持、数据更新时间和证据边界。",
        "",
        "禁止：dominant liquidity score、expected BTC return、Fed-causes-BTC叙事、最佳regime、买卖指令。",
    ]
    (OUT/"BTC_MECHANISM_SYNTHESIS_ZH.md").write_text("\n".join(lines)+"\n")

    schema={
        "module":"BTC-LIQUIDITY-RISK-REGIME-MECHANISM-039",
        "history_boundary":"GENUINE_BTC_HISTORY_ONLY",
        "analysis_start":"2014-11",
        "analysis_end":"2026-08",
        "mechanisms":MECHANISMS,
        "fixed_eras":[{"name":n,"start":str(s),"end":str(e)} for n,s,e in ERAS],
        "required_outputs":[
            "full_sample_association","fixed_era_association","era_stability",
            "state_contrast","rolling_36m_time_variation","support","source_freshness","boundary"
        ],
        "prohibited_outputs":[
            "dominant_mechanism_score","expected_btc_return","optimized_lag",
            "identified_fed_liquidity_shock","best_regime","buy_sell_instruction",
            "synthetic_btc_history"
        ],
        "m2_definition_caveat_required":True,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"PANDAAI_BTC_MECHANISM_SCHEMA.json").write_text(json.dumps(schema,indent=2,ensure_ascii=False)+"\n")

    report=[
        "# BTC-LIQUIDITY-RISK-REGIME-MECHANISM-039 — REPORT",
        "",
        "## Status",
        "",
        "**DESCRIPTIVE BITCOIN MECHANISM / ERA MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        f"- analysis months: {len(panel)}",
        f"- first analysis month: {panel.iloc[0]['month']}",
        f"- last analysis month: {panel.iloc[-1]['month']}",
        f"- source series: {len(registry)}",
        f"- mechanisms: {len(MECHANISMS)}",
        f"- full association rows: {len(full)}",
        f"- fixed-era association rows: {len(era_assoc)}",
        f"- state contrast rows: {len(contrasts)}",
        f"- state-support audit rows: {len(state_audit)}",
        f"- rolling 36M rows: {len(roll)}",
        f"- era-dependent mechanisms: {len(dep)}",
        f"- sign-stable mechanisms: {len(stable)}",
        "",
        "No synthetic Bitcoin history, p-value, mechanism ranking, optimized lag, expected-return forecast or causal Fed claim is generated.",
    ]
    (OUT/"BTC_LIQUIDITY_RISK_REGIME_MECHANISM_039_REPORT.md").write_text("\n".join(report)+"\n")

    # QC.
    expected_eras={
        "ERA_1_EARLY":38,
        "ERA_2_INSTITUTIONALIZATION":48,
        "ERA_3_POST_2022":56,
    }
    era_counts=panel.groupby("ERA").size().to_dict()
    if era_counts!=expected_eras:
        raise RuntimeError(f"fixed era row counts drift: {era_counts}")
    if len(full)!=7 or len(era_assoc)!=21:
        raise RuntimeError("association row counts")
    if len(contrasts)!=28:
        raise RuntimeError(f"state contrast rows expected 28, got {len(contrasts)}")
    if set(full["mechanism"])!=set(MECHANISMS):
        raise RuntimeError("mechanism family drift")
    if not (contrasts["support_status"].isin({"SUPPORTED_DESCRIPTIVE","LIMITED_DESCRIPTIVE","INSUFFICIENT_VARIATION"})).all():
        raise RuntimeError("state support status drift")
    if len(state_audit)!=7:
        raise RuntimeError("state-support audit row count")
    m2audit=state_audit[state_audit["mechanism"]=="M2SL_3M_PCT"].iloc[0]
    if m2audit["cross_era_state_comparability"]!="WEAK_STATE_COMPARABILITY":
        raise RuntimeError("M2 cross-era state-support audit changed unexpectedly")
    if not (roll["paired_months"]==36).all():
        raise RuntimeError("rolling window drift")
    if panel["month"].str.startswith("2026-09").any():
        raise RuntimeError("partial September leak")
    if panel["month"].str.startswith("2014-10").any():
        raise RuntimeError("partial-baseline October return leak")

    qc={
        "qc_gate":"PASS",
        "module":"BTC-LIQUIDITY-RISK-REGIME-MECHANISM-039",
        "upstream_qc":{"038":q038["qc_gate"]},
        "btc_source_start":str(btc_first.date()),
        "first_analysis_month":"2014-11",
        "last_analysis_month":"2026-08",
        "analysis_months":int(len(panel)),
        "partial_sep_2026_used":False,
        "inception_partial_sep_2014_used_as_return_month":False,
        "source_rows":int(len(registry)),
        "source_hashes_complete":bool(registry["sha256"].str.len().eq(64).all()),
        "missing_interpolation_used":False,
        "fixed_era_counts":era_counts,
        "mechanism_variables":MECHANISMS,
        "full_association_rows":int(len(full)),
        "fixed_era_association_rows":int(len(era_assoc)),
        "era_stability_rows":int(len(stab)),
        "state_contrast_rows":int(len(contrasts)),
        "state_support_audit_rows":int(len(state_audit)),
        "state_support_post_run_amendment":True,
        "state_cutoff":"ZERO_EXACT",
        "state_support_thresholds":{"supported_min_each":18,"limited_min_each":9},
        "rolling_window_months":36,
        "rolling_window_optimized":False,
        "rolling_rows":int(len(roll)),
        "m2_structural_definition_caveat_retained":True,
        "walcl_identified_liquidity_shock":False,
        "mechanism_ranking_created":False,
        "expected_btc_return_forecast_created":False,
        "optimized_lag_created":False,
        "causal_monetary_policy_claim_created":False,
        "synthetic_btc_history_created":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
