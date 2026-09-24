#!/usr/bin/env python3
"""
Post-run descriptive event-contrast impact audit for
FED-CYCLE-VINTAGE-AUDIT-007.
"""
from pathlib import Path
import json
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"fed_cycle_vintage_audit_v1"
EVENT=ROOT/"results"/"fed_cycle_state_v1"/"STATE_EVENT_PANEL.csv"
REV=OUT/"EVENT_REVISION_AUDIT.csv"

METRICS=[
    "gold_ret_6m","gold_ret_12m","gold_ret_24m","gold_mdd_24m"
]

def summarize(df,label_col,classification):
    rows=[]
    for state in ["STRONG","WEAK"]:
        g=df[df[label_col]==state].copy()
        row={
            "classification":classification,
            "growth_state":state,
            "n":int(len(g)),
        }
        for col in METRICS:
            row[f"median_{col}"]=float(g[col].median()) if len(g) else np.nan
        rows.append(row)
    s=pd.DataFrame(rows)
    strong=s[s["growth_state"]=="STRONG"].iloc[0]
    weak=s[s["growth_state"]=="WEAK"].iloc[0]
    diff={
        "classification":classification,
        "growth_state":"STRONG_MINUS_WEAK",
        "n":np.nan,
    }
    for col in METRICS:
        diff[f"median_{col}"]=float(strong[f"median_{col}"]-weak[f"median_{col}"])
    return pd.concat([s,pd.DataFrame([diff])],ignore_index=True)

def main():
    e=pd.read_csv(EVENT)
    r=pd.read_csv(REV)
    d=e.merge(
        r[["cycle_id","realtime_growth_state","state_flip"]],
        on="cycle_id",how="left",validate="one_to_one"
    )
    if len(d)!=10 or d["realtime_growth_state"].isna().any():
        raise RuntimeError("Expected ten complete event rows with realtime growth labels")

    current=summarize(d,"GROWTH_STATE","CURRENT_VINTAGE")
    realtime=summarize(d,"realtime_growth_state","REALTIME_IPT")
    out=pd.concat([current,realtime],ignore_index=True)

    current_diff=out[
        (out["classification"]=="CURRENT_VINTAGE")
        &(out["growth_state"]=="STRONG_MINUS_WEAK")
    ].iloc[0]
    rt_diff=out[
        (out["classification"]=="REALTIME_IPT")
        &(out["growth_state"]=="STRONG_MINUS_WEAK")
    ].iloc[0]

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-VINTAGE-AUDIT-007-EVENT-CONTRAST-IMPACT",
        "event_rows":int(len(d)),
        "state_flips":int(d["state_flip"].astype(bool).sum()),
        "current_strong_n":int((d["GROWTH_STATE"]=="STRONG").sum()),
        "current_weak_n":int((d["GROWTH_STATE"]=="WEAK").sum()),
        "realtime_strong_n":int((d["realtime_growth_state"]=="STRONG").sum()),
        "realtime_weak_n":int((d["realtime_growth_state"]=="WEAK").sum()),
        "current_12m_strong_minus_weak":float(current_diff["median_gold_ret_12m"]),
        "realtime_12m_strong_minus_weak":float(rt_diff["median_gold_ret_12m"]),
        "current_mdd_strong_minus_weak":float(current_diff["median_gold_mdd_24m"]),
        "realtime_mdd_strong_minus_weak":float(rt_diff["median_gold_mdd_24m"]),
        "inference_status":"NONE_DESCRIPTIVE_POSTRUN",
        "causal_status":"NONE",
        "oos_status":"NOT_A_FORECASTING_MODEL",
        "deployment_status":"NOT_DEPLOYABLE",
    }

    out.to_csv(OUT/"EVENT_GROWTH_CONTRAST_REVISION_AUDIT.csv",index=False)
    (OUT/"EVENT_CONTRAST_IMPACT_QC.json").write_text(json.dumps(qc,indent=2),encoding="utf-8")

    report=[
      "# FED-CYCLE-VINTAGE-AUDIT-007 — Event contrast revision impact",
      "",
      "**POST-RUN DESCRIPTIVE IMPACT AUDIT / NO NEW INFERENCE**",
      "",
      out.to_markdown(index=False),
      "",
      "Only the growth-state label is changed. Gold outcomes, horizons and the 2% threshold remain frozen.",
    ]
    (OUT/"EVENT_CONTRAST_IMPACT_REPORT.md").write_text("\n".join(report),encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
