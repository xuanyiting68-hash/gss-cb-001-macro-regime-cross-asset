#!/usr/bin/env python3
"""
Post-result mechanism diagnostic for ENERGY-PHYSICAL-WF-001 v1.1.

This is explicitly hypothesis-generating. It does not alter the frozen
primary four-test family and does not create new confirmatory tests.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"energy_physical_wf_v1_1"
PANEL=OUT/"PHYSICAL_EVENT_PANEL.csv"

x=pd.read_csv(PANEL,parse_dates=["s3_date","price_anchor_month","decision_date","exec_date"])

complete=x[(x["strict_pit"]=="AVAILABLE") & x["wti_fwd_3m"].notna()].copy()
pc=complete[complete["price_layer_classification"]=="PRICE_PRODUCT_CONFIRMED"].copy()
pc["physical_subgroup"]=np.where(pc["p4a_data_only"]==True,"P4A_DATA_ONLY","PRICE_CONFIRMED_NON_P4A")

metrics=["wti_fwd_3m","wti_fwd_6m","short_mae_3m","short_mae_6m"]
rows=[]
for group,g in pc.groupby("physical_subgroup"):
    for m in metrics:
        z=g[m].dropna()
        rows.append({
            "physical_subgroup":group,
            "metric":m,
            "n":len(z),
            "mean":z.mean(),
            "median":z.median(),
            "negative_share":(z<0).mean() if m.startswith("wti_fwd") and len(z) else np.nan,
        })
within=pd.DataFrame(rows)
within.to_csv(OUT/"DIAGNOSTIC_WITHIN_PRICE_CONFIRMED.csv",index=False)

# Inventory-improvement count among frozen price-confirmed episodes.
rows=[]
for count,g in pc.groupby("inventory_improving_count"):
    for m in ["wti_fwd_3m","wti_fwd_6m"]:
        z=g[m].dropna()
        rows.append({
            "inventory_improving_count":int(count),
            "metric":m,
            "n":len(z),
            "mean":z.mean(),
            "median":z.median(),
            "negative_share":(z<0).mean() if len(z) else np.nan,
        })
inventory=pd.DataFrame(rows)
inventory.to_csv(OUT/"DIAGNOSTIC_INVENTORY_COUNT.csv",index=False)

eventcols=[
    "s3_date","price_anchor_month","decision_date","price_layer_classification",
    "inventory_improving_count","refinery_util_baseline","refinery_util_decision",
    "refinery_worsening","physical_classification","wti_fwd_3m","wti_fwd_6m",
    "short_mae_3m","short_mae_6m"
]
pc[eventcols].sort_values("decision_date").to_csv(
    OUT/"DIAGNOSTIC_PRICE_CONFIRMED_EVENTS.csv",index=False
)

p4a=pc[pc["physical_subgroup"]=="P4A_DATA_ONLY"]
non=pc[pc["physical_subgroup"]=="PRICE_CONFIRMED_NON_P4A"]

def f_pct(v):
    return "NA" if pd.isna(v) else f"{100*v:+.2f}%"

lines=[
"# ENERGY-PHYSICAL-WF-001 v1.1 — Mechanism Diagnostic",
"Date: 2026-09-24",
"",
"## Status",
"",
"**POST-RESULT / HYPOTHESIS-GENERATING / NOT A NEW CONFIRMATORY FAMILY**",
"",
"The frozen primary result remains the four-test P4A_DATA_ONLY vs PHYSICAL_VETO_DATA_ONLY family.",
"",
"## Within the frozen price-confirmed episodes",
"",
f"- Completed price-confirmed episodes with strict PIT: {len(pc)}.",
f"- P4A_DATA_ONLY: {len(p4a)}.",
f"- Price-confirmed but non-P4A: {len(non)}.",
"",
within.to_markdown(index=False),
"",
"### Direct diagnostic",
"",
]
if len(p4a):
    lines += [
        f"- P4A 3M WTI median: {f_pct(p4a.wti_fwd_3m.median())}; positive share: {100*(p4a.wti_fwd_3m>0).mean():.1f}%.",
        f"- P4A 6M WTI median: {f_pct(p4a.wti_fwd_6m.median())}; positive share: {100*(p4a.wti_fwd_6m>0).mean():.1f}%.",
    ]
if len(non):
    lines += [
        f"- Non-P4A price-confirmed 3M median: {f_pct(non.wti_fwd_3m.median())}.",
        f"- Non-P4A price-confirmed 6M median: {f_pct(non.wti_fwd_6m.median())}.",
    ]
lines += [
"",
"Under the current rule, inventory normalization does not behave like a downside-confirmation variable. In the three P4A_DATA_ONLY episodes, WTI is positive at both 3M and 6M after the release-aware decision date.",
"",
"That does **not** establish the opposite rule. Support is only three events. It falsifies the narrow interpretation that 'more inventories relative to seasonal normal + no refinery worsening' is by itself a reliable falling-WTI confirmation.",
"",
"## Inventory-improvement-count diagnostic",
"",
inventory.to_markdown(index=False),
"",
"Among the small price-confirmed sample, a larger inventory-improvement count is not monotonically associated with more-negative WTI outcomes.",
"",
"## Mechanism interpretation",
"",
"Inventory accumulation is economically ambiguous. Stocks can rise because supply recovered, because imports/production rose, because refinery demand weakened, because final demand weakened, or because firms rebuilt inventories while demand and risk premia remained strong.",
"",
"The next research design therefore needs **flows**, not only stocks:",
"",
"- product supplied (gasoline, distillate, jet) as demand/use proxies;",
"- refinery crude inputs / throughput;",
"- domestic crude production;",
"- crude imports/net imports;",
"- later, independently frozen geopolitical/shipping shock tags.",
"",
"## Evidence verdict",
"",
"**The v1.1 physical-stock rule does not add validated downside timing information.**",
"",
"Do not tune the v1.1 thresholds to rescue it. Preserve it as a negative/falsification result and treat any flow-decomposition model as a new post-lock hypothesis.",
]
(OUT/"MECHANISM_DIAGNOSTIC.md").write_text("\n".join(lines),encoding="utf-8")
print({
    "completed_price_confirmed":len(pc),
    "p4a":len(p4a),
    "non_p4a":len(non),
    "p4a_3m_median":float(p4a.wti_fwd_3m.median()) if len(p4a) else None,
    "p4a_6m_median":float(p4a.wti_fwd_6m.median()) if len(p4a) else None,
})
