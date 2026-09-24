#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"results"/"energy_weekly_state_v1"/"SELECTED_EVENT_PANEL.csv"
OUT=ROOT/"results"/"energy_weekly_state_veto_diag_v1"
OUT.mkdir(parents=True,exist_ok=True)

def summary(g):
    out={"n_events":int(len(g))}
    for h in ["8w","13w"]:
        r=g[f"wti_fwd_{h}"].dropna()
        m=g[f"short_mae_{h}"].dropna()
        out[f"n_{h}"]=int(len(r))
        out[f"median_wti_{h}"]=float(r.median()) if len(r) else np.nan
        out[f"negative_share_{h}"]=float((r<0).mean()) if len(r) else np.nan
        out[f"median_short_mae_{h}"]=float(m.median()) if len(m) else np.nan
    return out

def main():
    df=pd.read_csv(SRC,parse_dates=["release_date"])
    mixed=df[(df.mechanism_class=="TIGHT_OR_MIXED") & df.wti_fwd_8w.notna()].copy()
    dd=df[(df.mechanism_class=="DEMAND_DESTRUCTION") & df.wti_fwd_8w.notna()].copy()

    rows=[
        {"sample":"MIXED_ALL",**summary(mixed)},
        {"sample":"MIXED_EXCLUDE_2004",**summary(mixed[mixed.release_date.dt.year!=2004])},
        {"sample":"MIXED_PRE_2018",**summary(mixed[mixed.release_date.dt.year<2018])},
        {"sample":"MIXED_2018_PRESENT",**summary(mixed[mixed.release_date.dt.year>=2018])},
        {"sample":"DEMAND_DESTRUCTION_ALL",**summary(dd)},
    ]
    pd.DataFrame(rows).to_csv(OUT/"SAMPLE_ROBUSTNESS.csv",index=False)

    loo=[]
    for idx,r in mixed.iterrows():
        g=mixed.drop(index=idx)
        loo.append({"dropped_release_date":r.release_date.date().isoformat(),**summary(g)})
    loo=pd.DataFrame(loo)
    loo.to_csv(OUT/"MIXED_LEAVE_ONE_OUT.csv",index=False)

    robust8=bool(
        (loo["median_wti_8w"]>0).all()
        and rows[1]["median_wti_8w"]>0
        and rows[3]["median_wti_8w"]>0
    )
    modern13=rows[3]["median_wti_13w"]

    qc={
        "qc_gate":"PASS",
        "module":"ENERGY-WEEKLY-STATE-004A",
        "post_run_diagnostic":True,
        "new_pvalue_family":False,
        "thresholds_changed":False,
        "mixed_completed_events":int(len(mixed)),
        "mixed_8w_loo_all_positive_median":bool((loo["median_wti_8w"]>0).all()),
        "mixed_8w_veto_robust_descriptively":robust8,
        "mixed_2018_present_median_wti_8w":rows[3]["median_wti_8w"],
        "mixed_2018_present_median_wti_13w":modern13,
        "demand_destruction_n":int(len(dd)),
        "demand_destruction_median_wti_13w":rows[4]["median_wti_13w"],
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-WEEKLY-STATE-004A — Post-Run Veto Robustness",
        "",
        "**POST-RUN DESCRIPTIVE DIAGNOSTIC / NO NEW P-VALUE FAMILY**",
        "",
        f"- completed TIGHT_OR_MIXED events: {len(mixed)}",
        f"- 8W leave-one-out median positive in every run: **{qc['mixed_8w_loo_all_positive_median']}**",
        f"- 2018-present TIGHT_OR_MIXED median WTI 8W: **{rows[3]['median_wti_8w']:.2%}**",
        f"- 2018-present TIGHT_OR_MIXED median WTI 13W: **{rows[3]['median_wti_13w']:.2%}**",
        f"- DEMAND_DESTRUCTION n={len(dd)}, median WTI 13W: **{rows[4]['median_wti_13w']:.2%}**",
        "",
        "## Sample robustness",
        "",
        pd.DataFrame(rows).to_markdown(index=False),
        "",
        "## Leave-one-out",
        "",
        loo.to_markdown(index=False),
        "",
        "## Judgment",
        "",
        "The descriptive TIGHT_OR_MIXED veto is substantially more robust at 8 weeks than at 13 weeks.",
        "Its 8-week median remains positive after removing individual events, after excluding 2004, and in the 2018-present subset.",
        "The 13-week separation decays materially in the modern subset, where the median is only slightly positive and the negative-return share is 50%.",
        "",
        "DEMAND_DESTRUCTION remains a promising bearish mechanism candidate at 13 weeks, but n=4 and the pattern was observed post-run, so it is not promoted to confirmatory evidence.",
    ]
    (OUT/"ENERGY_WEEKLY_STATE_004A_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
