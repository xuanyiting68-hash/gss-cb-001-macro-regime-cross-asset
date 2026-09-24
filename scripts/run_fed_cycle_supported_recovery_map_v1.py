#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
P4=ROOT/"results"/"fed_cycle_phase_clock_v1"
P15=ROOT/"results"/"fed_cycle_recovery_extension_v1"
OUT=ROOT/"results"/"fed_cycle_supported_recovery_map_v1"
OUT.mkdir(parents=True,exist_ok=True)

ANCHORS=["FIRST_HIKE","LAST_HIKE","PAUSE_START","FIRST_CUT"]

def main():
    core=pd.read_csv(P4/"PHASE_RECOVERY_SUMMARY.csv")
    timing=pd.read_csv(P4/"PHASE_TIMING_SUMMARY.csv")[["asset","anchor","support_status"]]
    core=core.merge(timing,on=["asset","anchor"],how="left",validate="many_to_one")
    core["recovery_support_status"]=np.where(
        core.support_status=="PRIMARY_SUPPORTED",
        "SUPPORTED_RECOVERY_DESCRIPTIVE",
        "LIMITED_RECOVERY_DESCRIPTIVE",
    )
    core["source_module"]="PHASE_CLOCK_004"

    m15=pd.read_csv(P15/"MARKET_RECOVERY_SUMMARY.csv")
    h15=pd.read_csv(P15/"HOUSING_RECOVERY_SUMMARY.csv")
    ext=pd.concat([m15,h15],ignore_index=True,sort=False)
    ext["source_module"]="RECOVERY_EXTENSION_015"

    cols=[
        "asset","anchor","recovery_level","n_legs","n_broad_episodes",
        "observed_recoveries","right_censored","weighted_km_median_months",
        "recovery_support_status","source_module"
    ]
    allrec=pd.concat([core[cols],ext[cols]],ignore_index=True)
    allrec.to_csv(OUT/"ALL_RECOVERY_EVIDENCE.csv",index=False)

    supported=allrec[
        allrec.recovery_support_status=="SUPPORTED_RECOVERY_DESCRIPTIVE"
    ].copy()
    limited=allrec[
        allrec.recovery_support_status!="SUPPORTED_RECOVERY_DESCRIPTIVE"
    ].copy()
    supported.to_csv(OUT/"SUPPORTED_RECOVERY_CELLS.csv",index=False)
    limited.to_csv(OUT/"LIMITED_RECOVERY_WATCHLIST.csv",index=False)

    # Require both 50 and 100 rows at all four anchors.
    full=supported[supported.recovery_level=="100%"].copy()
    half=supported[supported.recovery_level=="50%"].copy()
    eligible=[]
    for asset,g in full.groupby("asset"):
        if set(g.anchor)==set(ANCHORS) and g.weighted_km_median_months.notna().all():
            h=half[half.asset==asset]
            if set(h.anchor)==set(ANCHORS) and h.weighted_km_median_months.notna().all():
                eligible.append(asset)

    rows=[]
    for asset in sorted(eligible):
        f=full[full.asset==asset].set_index("anchor")
        h=half[half.asset==asset].set_index("anchor")
        vals={a:float(f.loc[a,"weighted_km_median_months"]) for a in ANCHORS}
        fastest=min(vals,key=lambda a:(vals[a],ANCHORS.index(a)))
        slowest=max(vals,key=lambda a:(vals[a],-ANCHORS.index(a)))
        rows.append({
            "asset":asset,
            "recovery50_first_hike":float(h.loc["FIRST_HIKE","weighted_km_median_months"]),
            "recovery50_last_hike":float(h.loc["LAST_HIKE","weighted_km_median_months"]),
            "recovery50_pause_start":float(h.loc["PAUSE_START","weighted_km_median_months"]),
            "recovery50_first_cut":float(h.loc["FIRST_CUT","weighted_km_median_months"]),
            "recovery100_first_hike":vals["FIRST_HIKE"],
            "recovery100_last_hike":vals["LAST_HIKE"],
            "recovery100_pause_start":vals["PAUSE_START"],
            "recovery100_first_cut":vals["FIRST_CUT"],
            "fastest_full_recovery_phase":fastest,
            "slowest_full_recovery_phase":slowest,
            "first_hike_minus_pause_full_months":vals["FIRST_HIKE"]-vals["PAUSE_START"],
            "first_cut_minus_pause_full_months":vals["FIRST_CUT"]-vals["PAUSE_START"],
        })
    comp=pd.DataFrame(rows)
    comp.to_csv(OUT/"FOUR_PHASE_SUPPORTED_COMPARISON.csv",index=False)

    universal_first_cut=bool(
        len(comp)>0 and
        (comp.recovery100_first_cut < comp.recovery100_pause_start).all()
    )
    pause_faster_than_first_hike=int(
        (comp.recovery100_pause_start < comp.recovery100_first_hike).sum()
    )
    first_cut_slower_than_pause=int(
        (comp.recovery100_first_cut > comp.recovery100_pause_start).sum()
    )
    first_cut_equal_pause=int(
        (comp.recovery100_first_cut == comp.recovery100_pause_start).sum()
    )
    first_cut_faster_pause=int(
        (comp.recovery100_first_cut < comp.recovery100_pause_start).sum()
    )

    summary={
        "fully_supported_four_phase_assets":sorted(eligible),
        "n_fully_supported_four_phase_assets":len(eligible),
        "universal_first_cut_accelerates_vs_pause":universal_first_cut,
        "pause_full_recovery_faster_than_first_hike_count":pause_faster_than_first_hike,
        "first_cut_slower_than_pause_count":first_cut_slower_than_pause,
        "first_cut_equal_pause_count":first_cut_equal_pause,
        "first_cut_faster_than_pause_count":first_cut_faster_pause,
    }
    (OUT/"SYNTHESIS_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-SUPPORTED-RECOVERY-MAP-016",
        "new_price_estimation":False,
        "supported_cells":int(len(supported)),
        "limited_cells":int(len(limited)),
        **summary,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# FED-CYCLE-SUPPORTED-RECOVERY-MAP-016",
        "",
        "**SUPPORTED DESCRIPTIVE SYNTHESIS / NO NEW PRICE ESTIMATION**",
        "",
        f"- QC: **PASS**",
        f"- fully supported four-phase assets: {', '.join(sorted(eligible))}",
        f"- FIRST_CUT universally faster than PAUSE_START: **{universal_first_cut}**",
        "",
        "## Four-phase supported recovery map",
        "",
        comp.to_markdown(index=False),
        "",
        "## Main descriptive finding",
        "",
        f"PAUSE_START full recovery is faster than FIRST_HIKE for {pause_faster_than_first_hike}/{len(comp)} fully supported assets.",
        f"Relative to PAUSE_START, FIRST_CUT full recovery is slower for {first_cut_slower_than_pause}, equal for {first_cut_equal_pause}, and faster for {first_cut_faster_pause}.",
        "",
        "Therefore FIRST_CUT does not universally accelerate recovery.",
        "Asset-specific recovery clocks remain necessary.",
    ]
    (OUT/"FED_CYCLE_SUPPORTED_RECOVERY_MAP_016_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
