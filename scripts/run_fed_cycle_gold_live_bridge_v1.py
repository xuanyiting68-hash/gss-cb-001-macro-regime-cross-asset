#!/usr/bin/env python3
"""
FED-CYCLE-GOLD-LIVE-BRIDGE-011
Feature-transport audit: GC=F daily close monthly mean vs World Bank Gold monthly.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_gold_live_bridge_v1"
OUT.mkdir(parents=True, exist_ok=True)

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

STATE = load_module(
    ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py",
    "state_for_gold_bridge",
)
PATHMOD = load_module(
    ROOT / "scripts" / "run_fed_cycle_path_v1.py",
    "path_for_gold_bridge",
)

MIN_COMMON = 240

GATES = {
    "level_median_abs_rel_gap_max": 0.020,
    "level_p95_abs_rel_gap_max": 0.050,
    "ret3_corr_min": 0.980,
    "ret3_median_abs_diff_max": 0.015,
    "ret3_sign_agreement_min": 0.950,
    "ret6_corr_min": 0.980,
    "ret6_median_abs_diff_max": 0.020,
    "ret6_sign_agreement_min": 0.950,
    "vol6_corr_min": 0.900,
    "vol6_median_abs_diff_max": 0.006,
    "era_sign_agreement_min": 0.900,
}

def add_features(df: pd.DataFrame, price_col: str, prefix: str):
    x = df.copy().sort_values("period").reset_index(drop=True)
    p = x[price_col].astype(float)
    lr = np.log(p).diff()
    x[f"{prefix}_RET_3M"] = p / p.shift(3) - 1.0
    x[f"{prefix}_RET_6M"] = p / p.shift(6) - 1.0
    x[f"{prefix}_VOL_6M"] = lr.rolling(6).std(ddof=1)
    return x

def corr(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if len(a) < 3:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])

def sign_agreement(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.mean(np.sign(a) == np.sign(b)))

def main():
    ref, ref_prov = STATE.load_gold()
    ref = ref.rename(columns={"price": "WB_PRICE"})

    daily, yahoo_meta = PATHMOD.fetch_yahoo_chart("GC=F")
    duplicate_daily_dates = int(daily["date"].duplicated().sum())
    if duplicate_daily_dates:
        raise RuntimeError(f"Duplicate GC=F daily dates: {duplicate_daily_dates}")

    daily["period"] = daily["date"].dt.to_period("M")
    proxy = (
        daily.groupby("period")
        .agg(GCF_PRICE=("value", "mean"), GCF_N_DAILY=("value", "count"))
        .reset_index()
    )
    proxy = proxy[proxy["GCF_N_DAILY"] >= 10].copy()

    ref_f = add_features(ref, "WB_PRICE", "WB")
    proxy_f = add_features(proxy, "GCF_PRICE", "GCF")

    d = ref_f.merge(proxy_f, on="period", how="inner", validate="one_to_one")
    needed = [
        "WB_PRICE","GCF_PRICE",
        "WB_RET_3M","GCF_RET_3M",
        "WB_RET_6M","GCF_RET_6M",
        "WB_VOL_6M","GCF_VOL_6M",
    ]
    d = d.dropna(subset=needed).copy()
    d["ABS_REL_LEVEL_GAP"] = np.abs(d["GCF_PRICE"] / d["WB_PRICE"] - 1.0)
    d["ABS_RET3_DIFF"] = np.abs(d["GCF_RET_3M"] - d["WB_RET_3M"])
    d["ABS_RET6_DIFF"] = np.abs(d["GCF_RET_6M"] - d["WB_RET_6M"])
    d["ABS_VOL6_DIFF"] = np.abs(d["GCF_VOL_6M"] - d["WB_VOL_6M"])

    common_n = int(len(d))
    min_daily = int(d["GCF_N_DAILY"].min()) if common_n else 0

    metrics = {
        "common_feature_complete_months": common_n,
        "first_common_month": str(d["period"].min()) if common_n else "",
        "last_common_month": str(d["period"].max()) if common_n else "",
        "min_proxy_daily_obs_per_month": min_daily,
        "level_median_abs_rel_gap": float(d["ABS_REL_LEVEL_GAP"].median()),
        "level_p95_abs_rel_gap": float(d["ABS_REL_LEVEL_GAP"].quantile(0.95)),
        "ret3_corr": corr(d["WB_RET_3M"], d["GCF_RET_3M"]),
        "ret3_median_abs_diff": float(d["ABS_RET3_DIFF"].median()),
        "ret3_sign_agreement": sign_agreement(d["WB_RET_3M"], d["GCF_RET_3M"]),
        "ret6_corr": corr(d["WB_RET_6M"], d["GCF_RET_6M"]),
        "ret6_median_abs_diff": float(d["ABS_RET6_DIFF"].median()),
        "ret6_sign_agreement": sign_agreement(d["WB_RET_6M"], d["GCF_RET_6M"]),
        "vol6_corr": corr(d["WB_VOL_6M"], d["GCF_VOL_6M"]),
        "vol6_median_abs_diff": float(d["ABS_VOL6_DIFF"].median()),
    }

    era_defs = [
        ("2000_2009", "2000-01", "2009-12"),
        ("2010_2019", "2010-01", "2019-12"),
        ("2020_PRESENT", "2020-01", "2099-12"),
    ]
    era_rows = []
    for era, lo, hi in era_defs:
        lo_p = pd.Period(lo, freq="M")
        hi_p = pd.Period(hi, freq="M")
        g = d[(d["period"] >= lo_p) & (d["period"] <= hi_p)].copy()
        row = {
            "era": era,
            "n_months": int(len(g)),
            "ret3_sign_agreement": (
                sign_agreement(g["WB_RET_3M"], g["GCF_RET_3M"]) if len(g) else np.nan
            ),
            "ret6_sign_agreement": (
                sign_agreement(g["WB_RET_6M"], g["GCF_RET_6M"]) if len(g) else np.nan
            ),
        }
        era_rows.append(row)
    era = pd.DataFrame(era_rows)

    gate_rows = [
        ("coverage_common_months", metrics["common_feature_complete_months"] >= MIN_COMMON,
         metrics["common_feature_complete_months"], f">={MIN_COMMON}"),
        ("level_median_abs_rel_gap", metrics["level_median_abs_rel_gap"] <= GATES["level_median_abs_rel_gap_max"],
         metrics["level_median_abs_rel_gap"], f"<={GATES['level_median_abs_rel_gap_max']}"),
        ("level_p95_abs_rel_gap", metrics["level_p95_abs_rel_gap"] <= GATES["level_p95_abs_rel_gap_max"],
         metrics["level_p95_abs_rel_gap"], f"<={GATES['level_p95_abs_rel_gap_max']}"),
        ("ret3_corr", metrics["ret3_corr"] >= GATES["ret3_corr_min"],
         metrics["ret3_corr"], f">={GATES['ret3_corr_min']}"),
        ("ret3_median_abs_diff", metrics["ret3_median_abs_diff"] <= GATES["ret3_median_abs_diff_max"],
         metrics["ret3_median_abs_diff"], f"<={GATES['ret3_median_abs_diff_max']}"),
        ("ret3_sign_agreement", metrics["ret3_sign_agreement"] >= GATES["ret3_sign_agreement_min"],
         metrics["ret3_sign_agreement"], f">={GATES['ret3_sign_agreement_min']}"),
        ("ret6_corr", metrics["ret6_corr"] >= GATES["ret6_corr_min"],
         metrics["ret6_corr"], f">={GATES['ret6_corr_min']}"),
        ("ret6_median_abs_diff", metrics["ret6_median_abs_diff"] <= GATES["ret6_median_abs_diff_max"],
         metrics["ret6_median_abs_diff"], f"<={GATES['ret6_median_abs_diff_max']}"),
        ("ret6_sign_agreement", metrics["ret6_sign_agreement"] >= GATES["ret6_sign_agreement_min"],
         metrics["ret6_sign_agreement"], f">={GATES['ret6_sign_agreement_min']}"),
        ("vol6_corr", metrics["vol6_corr"] >= GATES["vol6_corr_min"],
         metrics["vol6_corr"], f">={GATES['vol6_corr_min']}"),
        ("vol6_median_abs_diff", metrics["vol6_median_abs_diff"] <= GATES["vol6_median_abs_diff_max"],
         metrics["vol6_median_abs_diff"], f"<={GATES['vol6_median_abs_diff_max']}"),
    ]

    for _, r in era.iterrows():
        if int(r["n_months"]) >= 24:
            gate_rows.extend([
                (
                    f"era_{r['era']}_ret3_sign",
                    float(r["ret3_sign_agreement"]) >= GATES["era_sign_agreement_min"],
                    float(r["ret3_sign_agreement"]),
                    f">={GATES['era_sign_agreement_min']}",
                ),
                (
                    f"era_{r['era']}_ret6_sign",
                    float(r["ret6_sign_agreement"]) >= GATES["era_sign_agreement_min"],
                    float(r["ret6_sign_agreement"]),
                    f">={GATES['era_sign_agreement_min']}",
                ),
            ])

    gates = pd.DataFrame(gate_rows, columns=["gate","pass","observed","threshold"])
    all_pass = bool(gates["pass"].all())
    bridge_status = (
        "PROXY_FEATURE_BRIDGE_CANDIDATE"
        if all_pass else
        "PROXY_BRIDGE_NOT_SUPPORTED"
    )

    hard_fail = (
        common_n < MIN_COMMON
        or min_daily < 10
        or duplicate_daily_dates != 0
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-GOLD-LIVE-BRIDGE-011",
        "candidate_proxy": "GC=F_COMEX_CONTINUOUS_FUTURES_PROXY",
        "reference": "WORLD_BANK_GOLD_MONTHLY_VIA_DATASETS_GOLD_PRICES",
        "common_feature_complete_months": common_n,
        "first_common_month": metrics["first_common_month"],
        "last_common_month": metrics["last_common_month"],
        "min_proxy_daily_obs_per_month": min_daily,
        "duplicate_proxy_daily_dates": duplicate_daily_dates,
        "engineering_gates_total": int(len(gates)),
        "engineering_gates_passed": int(gates["pass"].sum()),
        "bridge_status": bridge_status,
        "forecast_targets_loaded": False,
        "forecast_performance_evaluated": False,
        "proxy_to_reference_calibration_fitted": False,
        "raw_yahoo_json_committed": False,
        "oos008_evidence_inherited": False,
        "deployment_status": "NOT_DEPLOYABLE",
    }

    d_out = d.copy()
    d_out["period"] = d_out["period"].astype(str)
    d_out.to_csv(OUT / "MONTHLY_FEATURE_BRIDGE_PANEL.csv", index=False)
    pd.DataFrame([metrics]).to_csv(OUT / "BRIDGE_METRICS.csv", index=False)
    era.to_csv(OUT / "ERA_STABILITY.csv", index=False)
    gates.to_csv(OUT / "ENGINEERING_GATES.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")

    pd.DataFrame([
        {
            "source_object": "Reference Gold monthly",
            "source": ref_prov["source"],
            "url": ref_prov["url"],
            "source_commit": ref_prov.get("source_commit", ""),
            "sha256": ref_prov["sha256"],
            "raw_committed": False,
        },
        {
            "source_object": "Candidate daily Gold proxy",
            "source": "Yahoo Finance public chart history",
            "url": yahoo_meta["url"],
            "source_commit": "",
            "sha256": yahoo_meta["sha256"],
            "raw_committed": False,
        },
    ]).to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)

    # Diagnostics only.
    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    ax.scatter(d["WB_RET_3M"] * 100.0, d["GCF_RET_3M"] * 100.0, s=12, alpha=0.65)
    lo = min((d["WB_RET_3M"] * 100.0).min(), (d["GCF_RET_3M"] * 100.0).min())
    hi = max((d["WB_RET_3M"] * 100.0).max(), (d["GCF_RET_3M"] * 100.0).max())
    ax.plot([lo, hi], [lo, hi], linewidth=1)
    ax.set_xlabel("World Bank Gold 3M return (%)")
    ax.set_ylabel("GC=F monthly-mean 3M return (%)")
    ax.set_title("Gold live-source bridge: 3M feature agreement")
    fig.tight_layout()
    fig.savefig(OUT / "01_ret3_feature_bridge.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    ax.scatter(d["WB_RET_6M"] * 100.0, d["GCF_RET_6M"] * 100.0, s=12, alpha=0.65)
    lo = min((d["WB_RET_6M"] * 100.0).min(), (d["GCF_RET_6M"] * 100.0).min())
    hi = max((d["WB_RET_6M"] * 100.0).max(), (d["GCF_RET_6M"] * 100.0).max())
    ax.plot([lo, hi], [lo, hi], linewidth=1)
    ax.set_xlabel("World Bank Gold 6M return (%)")
    ax.set_ylabel("GC=F monthly-mean 6M return (%)")
    ax.set_title("Gold live-source bridge: 6M feature agreement")
    fig.tight_layout()
    fig.savefig(OUT / "02_ret6_feature_bridge.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    lines = [
        "# FED-CYCLE-GOLD-LIVE-BRIDGE-011 — Report",
        "",
        "**DATA-TRANSPORT / MEASUREMENT-EQUIVALENCE AUDIT / NO FORECAST PERFORMANCE EVIDENCE**",
        "",
        f"- QC: **{qc['qc_gate']}**",
        f"- bridge status: **{bridge_status}**",
        f"- common feature-complete months: {common_n}",
        f"- overlap: {metrics['first_common_month']} to {metrics['last_common_month']}",
        "",
        "## Bridge metrics",
        "",
        pd.DataFrame([metrics]).to_markdown(index=False),
        "",
        "## Frozen engineering gates",
        "",
        gates.to_markdown(index=False),
        "",
        "## Era stability",
        "",
        era.to_markdown(index=False),
        "",
        "## Interpretation boundary",
        "",
        "- GC=F is a COMEX continuous futures proxy, not spot Gold.",
        "- No mapping/calibration was fitted to improve agreement.",
        "- No Gold forecast target or M3 forecast error was loaded.",
        "- A bridge pass would justify only a separately versioned prospective measurement specification.",
        "- OOS-008 evidence is not automatically inherited.",
        "- Deployment remains prohibited.",
    ]
    (OUT / "FED_CYCLE_GOLD_LIVE_BRIDGE_011_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    if hard_fail:
        raise SystemExit("FED-CYCLE-GOLD-LIVE-BRIDGE-011 audit QC failed")

    print(json.dumps(qc, indent=2))

if __name__ == "__main__":
    main()
