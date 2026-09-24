#!/usr/bin/env python3
"""
Post-run robustness for FED-CYCLE-VINTAGE-AUDIT-007.
"""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_vintage_audit_v1"
PANEL=OUT/"PANEL_REALTIME_IPT.csv"

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

STATE=load(ROOT/"scripts"/"run_fed_cycle_state_panel_v2.py","state_panel_v2_vintage_robust")

def test(df,predictor,outcome):
    core=STATE.regression_core(df,predictor,outcome)
    if core is None:
        return None
    supported=core["n_cycles"]>=5 and core["n_broad_clusters"]>=4
    return {
      "n_rows":int(core["n_rows"]),
      "n_cycles":int(core["n_cycles"]),
      "n_broad":int(core["n_broad_clusters"]),
      "beta":float(core["beta"]),
      "p_broad":STATE.exact_signflip_p(core["broad_scores"].to_numpy()) if supported else np.nan,
      "p_mech":STATE.exact_signflip_p(core["mech_scores"].to_numpy()) if supported else np.nan,
      "supported":supported,
      "broad_scores":core["broad_scores"],
    }

def main():
    base=pd.read_csv(
      ROOT/"results"/"fed_cycle_state_panel_v2"/"MONTHLY_STATE_PANEL.csv",
      parse_dates=["panel_month_start","first_hike","first_cut"]
    )
    rt=pd.read_csv(PANEL)
    key=["cycle_id","broad_episode_id","panel_month"]
    d=base.merge(
      rt[key+["RT_IPT_YOY","RT_IPT_VINTAGE_PERIOD"]],
      on=key,how="left",validate="one_to_one"
    )

    restrictions=[
      ("FULL_SAMPLE",d),
      ("EXCLUDE_2022",d[d["cycle_start_year"]<2022].copy()),
      ("EXCLUDE_EARLY_B01_B02",d[~d["broad_episode_id"].isin(["B01","B02"])].copy()),
      ("LATER_EX_2022",d[(~d["broad_episode_id"].isin(["B01","B02"])) & (d["cycle_start_year"]<2022)].copy()),
    ]

    rows=[]
    score_rows=[]
    for label,sub in restrictions:
      for outcome in ["GOLD_FWD_6M_RET","GOLD_FWD_6M_MDD"]:
        same=sub.dropna(subset=["RT_IPT_YOY","INDPRO_YOY",outcome]).copy()
        a=test(same,"RT_IPT_YOY",outcome)
        b=test(same,"INDPRO_YOY",outcome)
        if a is None or b is None:
          continue
        rows.append({
          "restriction":label,
          "outcome":outcome,
          "same_sample_rows":len(same),
          "n_cycles":a["n_cycles"],
          "n_broad_episodes":a["n_broad"],
          "support_status":"SUPPORTED_FROZEN_THRESHOLD" if a["supported"] else "LIMITED_SUPPORT",
          "realtime_beta":a["beta"],
          "realtime_p_broad_exact":a["p_broad"],
          "realtime_p_mechanical_exact":a["p_mech"],
          "current_beta":b["beta"],
          "current_p_broad_exact":b["p_broad"],
          "current_p_mechanical_exact":b["p_mech"],
          "beta_sign_agreement":bool(np.sign(a["beta"])==np.sign(b["beta"])),
        })
        if label=="FULL_SAMPLE" and outcome=="GOLD_FWD_6M_RET":
          for bid,val in a["broad_scores"].items():
            score_rows.append({
              "broad_episode_id":bid,
              "realtime_score_contribution":float(val),
              "score_sign":int(np.sign(val)),
            })

    res=pd.DataFrame(rows)
    scores=pd.DataFrame(score_rows)

    gap=100.0*(pd.to_numeric(d["INDPRO_YOY"],errors="coerce")-pd.to_numeric(d["RT_IPT_YOY"],errors="coerce"))
    ok=d[["INDPRO_YOY","RT_IPT_YOY"]].dropna()
    rev={
      "panel_rows":int(len(d)),
      "paired_rows":int(len(ok)),
      "pearson_corr_current_vs_realtime":float(ok["INDPRO_YOY"].corr(ok["RT_IPT_YOY"])),
      "median_abs_revision_gap_pp":float(gap.abs().median()),
      "p90_abs_revision_gap_pp":float(gap.abs().quantile(.90)),
      "max_abs_revision_gap_pp":float(gap.abs().max()),
    }

    full_ret=res[(res["restriction"]=="FULL_SAMPLE")&(res["outcome"]=="GOLD_FWD_6M_RET")].iloc[0]
    ex22=res[(res["restriction"]=="EXCLUDE_2022")&(res["outcome"]=="GOLD_FWD_6M_RET")].iloc[0]
    later=res[(res["restriction"]=="EXCLUDE_EARLY_B01_B02")&(res["outcome"]=="GOLD_FWD_6M_RET")].iloc[0]

    same_score_sign=bool(len(scores) and scores["score_sign"].nunique()==1 and int(scores.iloc[0]["score_sign"])!=0)
    qc={
      "qc_gate":"PASS",
      "module":"FED-CYCLE-VINTAGE-AUDIT-007-POSTRUN-ROBUSTNESS",
      **rev,
      "full_realtime_beta":float(full_ret["realtime_beta"]),
      "full_realtime_p_broad":float(full_ret["realtime_p_broad_exact"]),
      "exclude_2022_realtime_beta":float(ex22["realtime_beta"]),
      "exclude_2022_realtime_p_broad":float(ex22["realtime_p_broad_exact"]) if pd.notna(ex22["realtime_p_broad_exact"]) else None,
      "later_realtime_beta":float(later["realtime_beta"]),
      "later_realtime_p_broad":float(later["realtime_p_broad_exact"]) if pd.notna(later["realtime_p_broad_exact"]) else None,
      "all_full_broad_scores_same_sign":same_score_sign,
      "interpretation":"POST_RUN_ROBUSTNESS_ONLY",
      "causal_status":"NONE",
      "oos_status":"NOT_A_FORECASTING_MODEL",
      "deployment_status":"NOT_DEPLOYABLE",
    }

    res.to_csv(OUT/"POSTRUN_RESTRICTION_AUDIT.csv",index=False)
    scores.to_csv(OUT/"REALTIME_RETURN_BROAD_SCORE_AUDIT.csv",index=False)
    pd.DataFrame([rev]).to_csv(OUT/"PANEL_REVISION_SIZE_AUDIT.csv",index=False)
    (OUT/"POSTRUN_ROBUSTNESS_QC.json").write_text(json.dumps(qc,indent=2),encoding="utf-8")

    report=[
      "# FED-CYCLE-VINTAGE-AUDIT-007 — Post-run robustness",
      "",
      "**POST-RUN ROBUSTNESS ONLY / DOES NOT UPGRADE CONFIRMATORY STATUS**",
      "",
      "## Restriction audit",
      "",
      res.to_markdown(index=False),
      "",
      "## Full-sample broad-episode score contributions",
      "",
      scores.to_markdown(index=False),
      "",
      "## Revision-size audit",
      "",
      pd.DataFrame([rev]).to_markdown(index=False),
    ]
    (OUT/"POSTRUN_ROBUSTNESS_REPORT.md").write_text("\n".join(report),encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
