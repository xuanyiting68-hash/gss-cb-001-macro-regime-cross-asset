#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
P5=ROOT/"results"/"energy_weekly_prospective_v1"
D4A=ROOT/"results"/"energy_weekly_state_veto_diag_v1"
P6=ROOT/"results"/"energy_portwatch_v1"
OUT=ROOT/"results"/"energy_risk_synthesis_v1"
OUT.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p): return json.loads(p.read_text(encoding="utf-8"))

def main():
    q5=j(P5/"QC.json")
    q4a=j(D4A/"QC.json")
    q6=j(P6/"QC.json")
    reg=pd.read_csv(P5/"PROSPECTIVE_EVENT_REGISTRY.csv")
    ext=pd.read_csv(P6/"EXTERNAL_CONTEXT_SNAPSHOT.csv")

    if q5.get("qc_gate")!="PASS" or q4a.get("qc_gate")!="PASS" or q6.get("qc_gate")!="PASS":
        raise RuntimeError("upstream QC not PASS")
    if len(reg)!=1 or reg.iloc[0]["event_id"]!="ENERGY005_2026-09-23":
        raise RuntimeError("unexpected prospective registry")
    e=reg.iloc[0]
    if e["realization_status"]!="UNREALIZED":
        raise RuntimeError("current event outcome already realized; synthesis freeze invalid")
    x=ext.iloc[0]

    price_rollover=True
    clean_sn=e["mechanism_class"]=="SUPPLY_NORMALIZATION"
    broad_dd=e["mechanism_class"]=="DEMAND_DESTRUCTION"
    external=bool(x["external_supply_shock_context_present"])
    hist_veto=bool(
        q4a["mixed_8w_loo_all_positive_median"]
        and q4a["mixed_2018_present_median_wti_8w"]>0
    )

    composite=(
        "ROLLOVER_NOT_CONFIRMED__EXTERNAL_SUPPLY_RISK_ACTIVE"
        if price_rollover and not clean_sn and not broad_dd and external and hist_veto
        else "OTHER_FROZEN_STATE_COMBINATION"
    )
    bearish_confirmation="VETO" if composite.startswith("ROLLOVER_NOT_CONFIRMED") else "UNRESOLVED"

    state={
        "module":"ENERGY-RISK-SYNTHESIS-007",
        "event_id":e["event_id"],
        "event_release_date":e["release_date"],
        "prospective_outcome_status":e["realization_status"],
        "price_rollover":price_rollover,
        "frozen_mechanism_class":e["mechanism_class"],
        "clean_supply_normalization":clean_sn,
        "broad_demand_destruction":broad_dd,
        "external_supply_shock_context":external,
        "historical_8w_bearish_confirmation_veto":hist_veto,
        "composite_state":composite,
        "bearish_reversal_confirmation":bearish_confirmation,
        "historical_same_class_n":int(e["historical_same_class_completed_n"]),
        "historical_same_class_median_wti_8w":float(e["historical_same_class_median_wti_8w"]),
        "historical_same_class_median_short_mae_8w":float(e["historical_same_class_median_short_mae_8w"]),
        "modern_same_class_median_wti_8w":float(q4a["mixed_2018_present_median_wti_8w"]),
        "modern_same_class_median_wti_13w":float(q4a["mixed_2018_present_median_wti_13w"]),
        "portwatch_external_context":bool(q6["external_supply_shock_context_present"]),
        "portwatch_active_relevant_disruptions":int(q6["active_relevant_disruptions"]),
        "causal_status":"NONE",
        "directional_forecast_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    state["evidence_hashes"]={
        "prospective_registry_sha256":sha(P5/"PROSPECTIVE_EVENT_REGISTRY.csv"),
        "004a_qc_sha256":sha(D4A/"QC.json"),
        "006_context_sha256":sha(P6/"EXTERNAL_CONTEXT_SNAPSHOT.csv"),
    }
    (OUT/"CURRENT_STATE.json").write_text(json.dumps(state,indent=2)+"\n",encoding="utf-8")

    qc={
        "qc_gate":"PASS",
        "module":"ENERGY-RISK-SYNTHESIS-007",
        "upstream_005_qc":"PASS",
        "upstream_004a_qc":"PASS",
        "upstream_006_qc":"PASS",
        "prospective_outcome_used":False,
        "new_model_fitted":False,
        "thresholds_retuned":False,
        "composite_state":composite,
        "bearish_reversal_confirmation":bearish_confirmation,
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# ENERGY-RISK-SYNTHESIS-007 — Current Evidence State",
        "",
        f"**{composite}**",
        "",
        f"- event: {e['event_id']}",
        f"- price rollover: {price_rollover}",
        f"- clean supply normalization: **{clean_sn}**",
        f"- broad demand destruction: **{broad_dd}**",
        f"- external supply-shock context: **{external}**",
        f"- historical 8W bearish-confirmation veto: **{hist_veto}**",
        f"- bearish reversal confirmation: **{bearish_confirmation}**",
        "",
        "## What this means",
        "",
        "The current evidence supports a rollover state, but not a clean global supply-normalization state.",
        "U.S. inventory improvement coexists with weak refinery throughput, while independent maritime data show an active external supply shock.",
        "Historically, completed TIGHT_OR_MIXED events have not behaved like reliable 8-week bearish confirmations.",
        "",
        "This state blocks overconfident bearish confirmation. It does not create a bullish forecast or a trading instruction.",
        "",
        "## Confidence",
        "",
        "- High: timing/provenance/current mechanism/external-shock facts.",
        "- Moderate descriptive: 8W historical veto reference.",
        "- Unresolved: 13W direction, causal mechanism, current prospective outcome.",
    ]
    (OUT/"CURRENT_STATE_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(qc,indent=2))

if __name__=="__main__":
    main()
