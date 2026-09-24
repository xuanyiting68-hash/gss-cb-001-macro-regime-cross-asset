#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
P4=ROOT/"results"/"fed_cycle_phase_clock_v1"
P15=ROOT/"results"/"fed_cycle_recovery_extension_v1"
P16=ROOT/"results"/"fed_cycle_supported_recovery_map_v1"
OUT=ROOT/"results"/"fed_cycle_total_risk_clock_v1"
OUT.mkdir(parents=True,exist_ok=True)

def weighted_quantile(values,weights,q=0.5):
    v=np.asarray(values,float); w=np.asarray(weights,float)
    m=np.isfinite(v)&np.isfinite(w)&(w>0)
    v,w=v[m],w[m]
    if len(v)==0:return np.nan
    o=np.argsort(v);v,w=v[o],w[o]
    c=np.cumsum(w)/w.sum()
    return float(v[np.searchsorted(c,q,side="left")])

def weighted_km_total(g,level):
    obs=f"recovery{level}_observed"
    total=f"anchor_to_recovery{level}_months"
    censor="anchor_to_censor_months"
    d=g.copy()
    d["duration"]=np.where(
        d[obs].astype(bool),
        pd.to_numeric(d[total],errors="coerce"),
        pd.to_numeric(d[censor],errors="coerce"),
    )
    d=d.dropna(subset=["duration"]).copy()
    d["duration"]=d.duration.astype(int)
    surv=1.0
    rows=[{
        "time_months":0,
        "at_risk_weight":float(d.episode_weight.sum()),
        "event_weight":0.0,
        "censor_weight":0.0,
        "survival_not_recovered":1.0,
    }]
    for t in sorted(d.duration.unique()):
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

def build_source():
    allowed=pd.read_csv(P16/"SUPPORTED_RECOVERY_CELLS.csv")
    allowed=allowed[allowed.recovery_level=="100%"][["asset","anchor"]].drop_duplicates()
    allowed_keys=set(map(tuple,allowed[["asset","anchor"]].to_records(index=False)))

    core=pd.read_csv(P4/"PHASE_CYCLE_ASSET_METRICS.csv")
    core=core[core.asset.isin(["GOLD","NASDAQ","SP500","WTI"])].copy()
    core["drawdown"]=pd.to_numeric(core.mdd_12m,errors="coerce")
    core["trough_month"]=pd.to_numeric(core.mdd_trough_month,errors="coerce")
    core["source_module"]="PHASE_CLOCK_004"

    market=pd.read_csv(P15/"MARKET_RECOVERY_METRICS.csv")
    market=market[market.asset=="DXY"].copy()
    market["drawdown"]=pd.to_numeric(market.mdd_12m,errors="coerce")
    market["trough_month"]=pd.to_numeric(market.mdd_trough_month,errors="coerce")
    market["source_module"]="RECOVERY_EXTENSION_015"

    housing=pd.read_csv(P15/"HOUSING_RECOVERY_METRICS.csv")
    housing=housing[housing.asset=="US_HOUSE_PRICE"].copy()
    housing["drawdown"]=pd.to_numeric(housing.decline_24m,errors="coerce")
    housing["trough_month"]=pd.to_numeric(housing.trough_month_24m,errors="coerce")
    housing["source_module"]="RECOVERY_EXTENSION_015"

    keep=[
        "asset","anchor","cycle_id","broad_episode_id","anchor_date","episode_weight",
        "drawdown","trough_month",
        "recovery50_months","recovery100_months",
        "recovery50_observed","recovery100_observed",
        "recovery_censor_months","source_module"
    ]
    allrows=pd.concat([core[keep],market[keep],housing[keep]],ignore_index=True)

    main=allrows[
        allrows.apply(lambda r:(r.asset,r.anchor) in allowed_keys,axis=1)
    ].copy()
    return main,allowed_keys

def main():
    d,allowed_keys=build_source()
    # Only positive drawdown episodes define a recovery clock.
    d=d[pd.to_numeric(d.drawdown,errors="coerce")>1e-15].copy()
    d=d.dropna(subset=["trough_month"]).copy()

    if (pd.to_datetime(d.anchor_date).dt.year>=2026).any():
        raise RuntimeError("current 2026 row entered total risk clock")

    for level in (50,100):
        obs=f"recovery{level}_observed"
        rec=f"recovery{level}_months"
        total=f"anchor_to_recovery{level}_months"
        d[total]=np.where(
            d[obs].astype(bool),
            pd.to_numeric(d.trough_month,errors="coerce")+pd.to_numeric(d[rec],errors="coerce"),
            np.nan,
        )
    d["anchor_to_censor_months"]=(
        pd.to_numeric(d.trough_month,errors="coerce")
        +pd.to_numeric(d.recovery_censor_months,errors="coerce")
    )

    too_early=0
    for level in (50,100):
        obs=d[f"recovery{level}_observed"].astype(bool)
        total=pd.to_numeric(d[f"anchor_to_recovery{level}_months"],errors="coerce")
        too_early+=int((obs&(total<pd.to_numeric(d.trough_month,errors="coerce"))).sum())
    both=d[d.recovery50_observed.astype(bool)&d.recovery100_observed.astype(bool)].copy()
    order_bad=int((
        pd.to_numeric(both.anchor_to_recovery100_months,errors="coerce")
        <pd.to_numeric(both.anchor_to_recovery50_months,errors="coerce")
    ).sum())

    d.to_csv(OUT/"SUPPORTED_EVENT_TOTAL_CLOCK.csv",index=False)

    curves=[]; summary=[]
    for (asset,anchor),g in d.groupby(["asset","anchor"]):
        w=g.episode_weight.astype(float)
        trough_med=weighted_quantile(g.trough_month,w,0.5)
        late=float(g.loc[g.trough_month>=7,"episode_weight"].sum()/w.sum())
        base={
            "asset":asset,
            "anchor":anchor,
            "positive_drawdown_episodes":int(len(g)),
            "positive_drawdown_broad_episodes":int(g.broad_episode_id.nunique()),
            "weighted_median_trough_month":trough_med,
            "weighted_late_trough_share_month7plus":late,
        }
        out=dict(base)
        for level in (50,100):
            km=weighted_km_total(g,level)
            hit=km[km.survival_not_recovered<=0.5+1e-12]
            med=int(hit.iloc[0].time_months) if len(hit) else np.nan
            out[f"weighted_km_median_anchor_to_{level}_months"]=med
            out[f"observed_{level}_recoveries"]=int(g[f"recovery{level}_observed"].astype(bool).sum())
            out[f"censored_{level}_recoveries"]=int((~g[f"recovery{level}_observed"].astype(bool)).sum())
            km["asset"]=asset; km["anchor"]=anchor; km["recovery_level"]=f"{level}%"
            curves.append(km)
        summary.append(out)

    summary=pd.DataFrame(summary)
    summary.to_csv(OUT/"SUPPORTED_TOTAL_CLOCK_SUMMARY.csv",index=False)
    pd.concat(curves,ignore_index=True).to_csv(OUT/"SUPPORTED_TOTAL_CLOCK_KM.csv",index=False)

    four=[]
    for asset,g in summary.groupby("asset"):
        if set(g.anchor)=={"FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"}:
            x=g.set_index("anchor")
            four.append({
                "asset":asset,
                "trough_first_hike":x.loc["FIRST_HIKE","weighted_median_trough_month"],
                "trough_last_hike":x.loc["LAST_HIKE","weighted_median_trough_month"],
                "trough_pause_start":x.loc["PAUSE_START","weighted_median_trough_month"],
                "trough_first_cut":x.loc["FIRST_CUT","weighted_median_trough_month"],
                "total100_first_hike":x.loc["FIRST_HIKE","weighted_km_median_anchor_to_100_months"],
                "total100_last_hike":x.loc["LAST_HIKE","weighted_km_median_anchor_to_100_months"],
                "total100_pause_start":x.loc["PAUSE_START","weighted_km_median_anchor_to_100_months"],
                "total100_first_cut":x.loc["FIRST_CUT","weighted_km_median_anchor_to_100_months"],
                "first_cut_minus_pause_total100":(
                    x.loc["FIRST_CUT","weighted_km_median_anchor_to_100_months"]
                    -x.loc["PAUSE_START","weighted_km_median_anchor_to_100_months"]
                ),
            })
    four=pd.DataFrame(four)
    four.to_csv(OUT/"FOUR_PHASE_TOTAL_CLOCK_COMPARISON.csv",index=False)

    first_cut_slower=int((four.first_cut_minus_pause_total100>0).sum())
    equal=int((four.first_cut_minus_pause_total100==0).sum())
    faster=int((four.first_cut_minus_pause_total100<0).sum())

    qc={
        "qc_gate":"FAIL" if too_early or order_bad else "PASS",
        "module":"FED-CYCLE-TOTAL-RISK-CLOCK-017",
        "supported_asset_anchor_cells":int(len(summary)),
        "fully_supported_four_phase_assets":sorted(four.asset.tolist()),
        "total_duration_before_trough_violations":too_early,
        "total_recovery_order_violations":order_bad,
        "first_cut_slower_than_pause_total100_count":first_cut_slower,
        "first_cut_equal_pause_total100_count":equal,
        "first_cut_faster_than_pause_total100_count":faster,
        "new_price_estimation":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# FED-CYCLE-TOTAL-RISK-CLOCK-017",
        "",
        "**SUPPORTED EVENT-LEVEL ANCHOR→TROUGH→RECOVERY CLOCK**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        "",
        "## Supported total clock",
        "",
        summary.to_markdown(index=False),
        "",
        "## Four-phase comparison",
        "",
        four.to_markdown(index=False),
        "",
        "The total recovery duration is estimated event-by-event and then aggregated; it is not the sum of two separately computed medians.",
        f"FIRST_CUT total 100% recovery is slower than PAUSE_START for {first_cut_slower} fully supported assets, equal for {equal}, faster for {faster}.",
    ]
    (OUT/"FED_CYCLE_TOTAL_RISK_CLOCK_017_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

    if qc["qc_gate"]!="PASS":
        raise SystemExit("FED-CYCLE-TOTAL-RISK-CLOCK-017 QC failed")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
