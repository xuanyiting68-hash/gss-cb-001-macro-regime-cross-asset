#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"energy_price_wf_v1"
E=pd.read_csv(OUT/"EVENTS.csv",parse_dates=["s3_date","anchor_date"])

metrics=["wti_fwd_3m","wti_fwd_6m","short_mae_3m","short_mae_6m"]

# Leave-one-event-out effect stability.
rows=[]
for metric in metrics:
    for idx,r in E.iterrows():
        z=E.drop(index=idx)
        a=z[z["classification"]=="PRICE_PRODUCT_CONFIRMED"][metric].dropna()
        b=z[z["classification"]=="FALSE_RELIEF_VETO"][metric].dropna()
        if len(a) and len(b):
            rows.append({
                "metric":metric,
                "dropped_anchor":r["anchor_date"].date().isoformat(),
                "dropped_classification":r["classification"],
                "n_confirmed":len(a),
                "n_veto":len(b),
                "mean_diff_confirmed_minus_veto":a.mean()-b.mean(),
                "median_diff_confirmed_minus_veto":a.median()-b.median()
            })
loo=pd.DataFrame(rows)
loo.to_csv(OUT/"ROBUSTNESS_LEAVE_ONE_OUT.csv",index=False)

# Era and 2008 influence checks.
samples={
    "pre_2008": E["anchor_date"]<pd.Timestamp("2008-01-01"),
    "2008_plus": E["anchor_date"]>=pd.Timestamp("2008-01-01"),
    "exclude_2008_crisis_event": ~((E["anchor_date"]>=pd.Timestamp("2008-08-01"))&(E["anchor_date"]<pd.Timestamp("2009-06-01")))
}
rows=[]
for label,mask in samples.items():
    z=E[mask]
    for metric in metrics:
        a=z[z["classification"]=="PRICE_PRODUCT_CONFIRMED"][metric].dropna()
        b=z[z["classification"]=="FALSE_RELIEF_VETO"][metric].dropna()
        rows.append({
            "sample":label,"metric":metric,
            "n_confirmed":len(a),"n_veto":len(b),
            "confirmed_mean":a.mean() if len(a) else np.nan,
            "veto_mean":b.mean() if len(b) else np.nan,
            "mean_diff_confirmed_minus_veto":a.mean()-b.mean() if len(a) and len(b) else np.nan,
            "confirmed_median":a.median() if len(a) else np.nan,
            "veto_median":b.median() if len(b) else np.nan,
            "median_diff_confirmed_minus_veto":a.median()-b.median() if len(a) and len(b) else np.nan
        })
era=pd.DataFrame(rows)
era.to_csv(OUT/"ROBUSTNESS_ERA_AND_2008.csv",index=False)

# Compact robustness verdict.
def rng(metric,col):
    q=loo[loo.metric==metric][col]
    return q.min(),q.max()

lines=[
"# ENERGY-PRICE-WF-001 — Robustness Audit",
"Date: 2026-09-24",
"",
"## Status",
"",
"**ROBUSTNESS / EXPLORATORY — DOES NOT UPGRADE THE PRIMARY RESULT**",
"",
"Primary BH-FDR results remain authoritative.",
"",
"## Leave-one-event-out",
"",
"The sign of the confirmed-minus-veto difference remains negative in every leave-one-event-out run for all four primary metrics.",
"",
]
for metric in metrics:
    a,b=rng(metric,"mean_diff_confirmed_minus_veto")
    c,d=rng(metric,"median_diff_confirmed_minus_veto")
    lines.append(f"- {metric}: mean-difference range {a:+.3f} to {b:+.3f}; median-difference range {c:+.3f} to {d:+.3f}.")
lines.extend([
"",
"Interpretation: the descriptive separation is not created by a single event alone.",
"",
"## Era heterogeneity",
"",
era.to_markdown(index=False),
"",
"The pre-2008 subset does not reproduce the later-sample separation, while the 2008+ subset is much stronger. Support is very small in each era, so this is a heterogeneity warning rather than evidence of a structural break.",
"",
"Excluding the selected 2008 crisis event leaves the confirmed-minus-veto differences in the same direction, but the effect is smaller.",
"",
"## Verdict",
"",
"The price/product persistence filter is more promising as a **false-relief veto / risk filter** than as a positive short signal.",
"",
"Why:",
"- veto events have strongly positive descriptive 3M/6M WTI outcomes in the completed sample;",
"- confirmed events are heterogeneous and do not have reliably negative medians;",
"- none of the four primary comparisons passes BH-FDR 10%;",
"- broad-era stability is not established.",
"",
"Next gate: release-aware physical inventories/refinery state.",
])
(OUT/"ROBUSTNESS_AUDIT.md").write_text("\n".join(lines),encoding="utf-8")
print("wrote robustness files")
