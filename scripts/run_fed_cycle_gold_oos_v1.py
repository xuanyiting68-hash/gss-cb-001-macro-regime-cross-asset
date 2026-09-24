#!/usr/bin/env python3
"""
FED-CYCLE-GOLD-OOS-008
Episode-forward out-of-sample audit of real-time growth incremental value.

Reference:
research/FED_CYCLE_GOLD_OOS_008_LOCK.md
"""
from __future__ import annotations

import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_gold_oos_v1"
OUT.mkdir(parents=True, exist_ok=True)

PANEL_FILE = ROOT / "results" / "fed_cycle_state_panel_v2" / "MONTHLY_STATE_PANEL.csv"
RT_FILE = ROOT / "results" / "fed_cycle_vintage_audit_v1" / "PANEL_REALTIME_IPT.csv"

BROAD_ORDER = ["B01","B02","B03","B04","B05","B06","B07"]
TEST_EPISODES = ["B04","B05","B06","B07"]

MODEL_FEATURES = {
    "B1_GOLD_HISTORY": [
        "GOLD_RET_3M_LAGGED",
        "GOLD_RET_6M_LAGGED",
        "GOLD_VOL_6M_LAGGED",
    ],
    "B2_GOLD_PLUS_CYCLE_AGE": [
        "GOLD_RET_3M_LAGGED",
        "GOLD_RET_6M_LAGGED",
        "GOLD_VOL_6M_LAGGED",
        "CYCLE_AGE_MONTHS",
    ],
    "M3_PLUS_REALTIME_IPT": [
        "GOLD_RET_3M_LAGGED",
        "GOLD_RET_6M_LAGGED",
        "GOLD_VOL_6M_LAGGED",
        "CYCLE_AGE_MONTHS",
        "RT_IPT_YOY",
    ],
    "D4_PLUS_CURRENT_INDPRO": [
        "GOLD_RET_3M_LAGGED",
        "GOLD_RET_6M_LAGGED",
        "GOLD_VOL_6M_LAGGED",
        "CYCLE_AGE_MONTHS",
        "INDPRO_YOY",
    ],
}
TARGET = "GOLD_FWD_6M_RET"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


STATE_MOD = load_module(
    ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py",
    "state_panel_v2_oos",
)


def hierarchical_weights(df):
    """
    Each broad episode total weight 1.
    Within broad episode, each mechanical cycle total weight equal.
    Within cycle, rows equal.
    """
    w = pd.Series(index=df.index, dtype=float)
    for bid, gb in df.groupby("broad_episode_id"):
        cycles = sorted(gb["cycle_id"].unique())
        ncyc = len(cycles)
        for cid in cycles:
            idx = gb.index[gb["cycle_id"] == cid]
            w.loc[idx] = 1.0 / ncyc / len(idx)
    return w.astype(float)


def wmean(x, w):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    return float(np.sum(w * x) / np.sum(w))


def wstd(x, w):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    mu = wmean(x, w)
    return float(math.sqrt(max(0.0, np.sum(w * (x - mu) ** 2) / np.sum(w))))


def fit_wls(train, features, target, weights):
    X = train[features].to_numpy(float)
    y = train[target].to_numpy(float)
    w = weights.loc[train.index].to_numpy(float)

    mus = np.array([wmean(X[:,j], w) for j in range(X.shape[1])], dtype=float)
    sds = np.array([wstd(X[:,j], w) for j in range(X.shape[1])], dtype=float)
    active = sds > 1e-12

    Xz = np.zeros_like(X, dtype=float)
    if active.any():
        Xz[:,active] = (X[:,active] - mus[active]) / sds[active]

    Z = np.column_stack([np.ones(len(Xz)), Xz])
    sw = np.sqrt(w)
    coef, *_ = np.linalg.lstsq(Z * sw[:,None], y * sw, rcond=None)

    return {
        "features": list(features),
        "mus": mus,
        "sds": sds,
        "active": active,
        "coef": coef,
    }


def predict_wls(model, test):
    features = model["features"]
    X = test[features].to_numpy(float)
    Xz = np.zeros_like(X, dtype=float)
    active = model["active"]
    if active.any():
        Xz[:,active] = (
            X[:,active] - model["mus"][active]
        ) / model["sds"][active]
    Z = np.column_stack([np.ones(len(Xz)), Xz])
    return Z @ model["coef"]


def feature_engineering(panel, gold):
    pmap = dict(zip(gold["period"], gold["price"].astype(float)))
    rows = []

    for idx, r in panel.iterrows():
        m = pd.Period(str(r["panel_month"]), freq="M")
        need = [m-7, m-6, m-5, m-4, m-3, m-2, m-1]
        if any(p not in pmap for p in need):
            raise RuntimeError(f"Missing lagged Gold month for {m}")

        prices = np.array([float(pmap[p]) for p in need], dtype=float)
        log_changes = np.diff(np.log(prices))
        vol6 = float(np.std(log_changes, ddof=1))
        ret3 = float(pmap[m-1] / pmap[m-4] - 1.0)
        ret6 = float(pmap[m-1] / pmap[m-7] - 1.0)

        fh = pd.Timestamp(r["first_hike"]).to_period("M")
        age = int(m.ordinal - fh.ordinal)

        rows.append({
            "_idx": idx,
            "PANEL_PERIOD": str(m),
            "LAST_GOLD_FEATURE_PERIOD": str(m-1),
            "GOLD_RET_3M_LAGGED": ret3,
            "GOLD_RET_6M_LAGGED": ret6,
            "GOLD_VOL_6M_LAGGED": vol6,
            "CYCLE_AGE_MONTHS": age,
            "TARGET_END_PERIOD": str(m+5),
        })

    f = pd.DataFrame(rows).set_index("_idx")
    out = panel.join(f, how="left")
    return out


def episode_metrics(pred, model):
    rows = []
    for bid, g in pred.groupby("broad_episode_id"):
        w = g["eval_weight"].to_numpy(float)
        err = g[f"pred_{model}"].to_numpy(float) - g[TARGET].to_numpy(float)
        rows.append({
            "broad_episode_id": bid,
            "model": model,
            "n_rows": int(len(g)),
            "mse": float(np.average(err**2, weights=w)),
            "mae": float(np.average(np.abs(err), weights=w)),
        })
    return pd.DataFrame(rows)


def make_figures(ep, summary):
    # B2 vs M3 per-episode MSE
    g = ep[ep["model"].isin(["B2_GOLD_PLUS_CYCLE_AGE","M3_PLUS_REALTIME_IPT"])].copy()
    piv = g.pivot(index="broad_episode_id", columns="model", values="mse").loc[TEST_EPISODES]
    x = np.arange(len(piv))
    width = 0.36
    fig, ax = plt.subplots(figsize=(9.2,5.2))
    ax.bar(x-width/2, piv["B2_GOLD_PLUS_CYCLE_AGE"], width, label="B2 Gold + cycle age")
    ax.bar(x+width/2, piv["M3_PLUS_REALTIME_IPT"], width, label="M3 + real-time IPT")
    ax.set_xticks(x)
    ax.set_xticklabels(piv.index)
    ax.set_ylabel("OOS MSE")
    ax.set_title("Episode-forward OOS MSE: benchmark vs real-time growth")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT/"01_oos_episode_mse_b2_vs_m3.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9.0,5.0))
    s = summary.copy()
    ax.bar(s["model"], s["oos_r2_vs_b0"])
    ax.axhline(0, linewidth=.8)
    ax.set_ylabel("Episode-equal OOS R² vs historical mean")
    ax.set_title("Gold next-6M episode-forward OOS performance")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(OUT/"02_oos_r2_by_model.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


def main():
    panel = pd.read_csv(
        PANEL_FILE,
        parse_dates=["panel_month_start","first_hike","first_cut"],
    )
    rt = pd.read_csv(RT_FILE)

    merge_cols = [
        "cycle_id","broad_episode_id","panel_month",
        "RT_IPT_YOY","RT_IPT_VINTAGE_PERIOD"
    ]
    d = panel.merge(
        rt[merge_cols],
        on=["cycle_id","broad_episode_id","panel_month"],
        how="left",
        validate="one_to_one",
    )

    if len(d) != 165:
        raise RuntimeError(f"Expected 165 merged panel rows, got {len(d)}")

    gold, gold_prov = STATE_MOD.load_gold()
    d = feature_engineering(d, gold)

    needed = sorted(set(
        [TARGET,"RT_IPT_YOY","INDPRO_YOY"]
        + sum(MODEL_FEATURES.values(), [])
    ))
    if d[needed].isna().any().any():
        bad = d[needed].isna().sum()
        raise RuntimeError(f"Missing OOS fields: {bad[bad>0].to_dict()}")

    # Fixed broad ordering.
    unknown = set(d["broad_episode_id"]) - set(BROAD_ORDER)
    if unknown:
        raise RuntimeError(f"Unexpected broad episodes: {unknown}")

    all_preds = []
    coef_rows = []
    fold_qc = []

    for test_bid in TEST_EPISODES:
        test_pos = BROAD_ORDER.index(test_bid)
        train_bids = BROAD_ORDER[:test_pos]

        train = d[d["broad_episode_id"].isin(train_bids)].copy()
        test = d[d["broad_episode_id"] == test_bid].copy()

        if train.empty or test.empty:
            raise RuntimeError(f"Empty train/test for {test_bid}")

        # No target-window overlap with test episode start.
        max_train_target_end = max(
            pd.Period(x, freq="M") for x in train["TARGET_END_PERIOD"]
        )
        min_test_month = min(
            pd.Period(x, freq="M") for x in test["PANEL_PERIOD"]
        )
        outcome_overlap = max_train_target_end >= min_test_month

        # No same/future episode in train.
        bad_train_episode = any(
            BROAD_ORDER.index(b) >= test_pos for b in train["broad_episode_id"].unique()
        )

        train_w = hierarchical_weights(train)
        test_w = hierarchical_weights(test)

        # Each training broad episode total weight exactly 1.
        train_weight_bad = 0
        for bid, gb in train.groupby("broad_episode_id"):
            if abs(float(train_w.loc[gb.index].sum()) - 1.0) > 1e-10:
                train_weight_bad += 1
        test_weight_bad = abs(float(test_w.sum()) - 1.0) > 1e-10

        pred = test[[
            "cycle_id","broad_episode_id","cycle_start_year","panel_month",
            "PANEL_PERIOD","TARGET_END_PERIOD",TARGET
        ]].copy()
        pred["eval_weight"] = test_w.to_numpy(float)

        # B0 weighted historical mean.
        b0 = wmean(train[TARGET].to_numpy(float), train_w.to_numpy(float))
        pred["pred_B0_HIST_MEAN"] = b0

        for model_name, features in MODEL_FEATURES.items():
            model = fit_wls(train, features, TARGET, train_w)
            pred[f"pred_{model_name}"] = predict_wls(model, test)

            for j, feat in enumerate(features):
                coef_rows.append({
                    "test_broad_episode": test_bid,
                    "model": model_name,
                    "feature": feat,
                    "standardized_coefficient": float(model["coef"][j+1]),
                    "feature_active_in_train": bool(model["active"][j]),
                    "train_rows": int(len(train)),
                    "train_broad_episodes": int(train["broad_episode_id"].nunique()),
                })
            coef_rows.append({
                "test_broad_episode": test_bid,
                "model": model_name,
                "feature": "INTERCEPT",
                "standardized_coefficient": float(model["coef"][0]),
                "feature_active_in_train": True,
                "train_rows": int(len(train)),
                "train_broad_episodes": int(train["broad_episode_id"].nunique()),
            })

        pred["test_broad_episode"] = test_bid
        all_preds.append(pred)

        fold_qc.append({
            "test_broad_episode": test_bid,
            "train_broad_episodes": ";".join(train_bids),
            "train_rows": int(len(train)),
            "test_rows": int(len(test)),
            "max_train_target_end": str(max_train_target_end),
            "min_test_panel_month": str(min_test_month),
            "train_target_overlaps_test": bool(outcome_overlap),
            "later_or_same_episode_in_train": bool(bad_train_episode),
            "train_weight_violations": int(train_weight_bad),
            "test_weight_violation": bool(test_weight_bad),
        })

    pred = pd.concat(all_preds, ignore_index=True)
    coef = pd.DataFrame(coef_rows)
    foldqc = pd.DataFrame(fold_qc)

    models = [
        "B0_HIST_MEAN",
        "B1_GOLD_HISTORY",
        "B2_GOLD_PLUS_CYCLE_AGE",
        "M3_PLUS_REALTIME_IPT",
        "D4_PLUS_CURRENT_INDPRO",
    ]

    ep_parts = []
    for model in models:
        ep_parts.append(episode_metrics(pred, model))
    ep = pd.concat(ep_parts, ignore_index=True)

    summary_rows = []
    b0_mse = float(
        ep[ep["model"]=="B0_HIST_MEAN"]["mse"].mean()
    )
    for model in models:
        g = ep[ep["model"]==model].copy()
        mse = float(g["mse"].mean())
        mae = float(g["mae"].mean())
        summary_rows.append({
            "model": model,
            "oos_episodes": int(len(g)),
            "episode_equal_mse": mse,
            "episode_equal_mae": mae,
            "oos_r2_vs_b0": float(1.0 - mse/b0_mse) if b0_mse > 0 else np.nan,
        })
    summary = pd.DataFrame(summary_rows)

    b2 = float(summary.loc[
        summary["model"]=="B2_GOLD_PLUS_CYCLE_AGE","episode_equal_mse"
    ].iloc[0])
    m3 = float(summary.loc[
        summary["model"]=="M3_PLUS_REALTIME_IPT","episode_equal_mse"
    ].iloc[0])
    m3_r2 = float(summary.loc[
        summary["model"]=="M3_PLUS_REALTIME_IPT","oos_r2_vs_b0"
    ].iloc[0])

    b2_ep = ep[ep["model"]=="B2_GOLD_PLUS_CYCLE_AGE"].set_index("broad_episode_id")
    m3_ep = ep[ep["model"]=="M3_PLUS_REALTIME_IPT"].set_index("broad_episode_id")
    beat_flags = {
        bid: bool(m3_ep.loc[bid,"mse"] < b2_ep.loc[bid,"mse"])
        for bid in TEST_EPISODES
    }
    beat_count = int(sum(beat_flags.values()))
    reduction = float((b2-m3)/b2) if b2>0 else np.nan

    evidence_pass = bool(
        m3 < b2
        and beat_count >= 3
        and m3_r2 > 0
    )
    evidence_status = (
        "PRELIMINARY_OOS_CANDIDATE"
        if evidence_pass else
        "OOS_INCREMENTAL_VALUE_NOT_SUPPORTED"
    )

    # RT-IPT standardized coefficients across the four folds.
    rt_coef = coef[
        (coef["model"]=="M3_PLUS_REALTIME_IPT")
        & (coef["feature"]=="RT_IPT_YOY")
    ].copy()

    # Hard QC.
    gold_feature_timing_bad = 0
    rt_vintage_timing_bad = 0
    for _, r in d.iterrows():
        pm = pd.Period(str(r["panel_month"]), freq="M")
        lg = pd.Period(str(r["LAST_GOLD_FEATURE_PERIOD"]), freq="M")
        if lg >= pm:
            gold_feature_timing_bad += 1
        vp = pd.Period(str(r["RT_IPT_VINTAGE_PERIOD"]), freq="M")
        if vp >= pm:
            rt_vintage_timing_bad += 1

    fold_leak_bad = int(foldqc["train_target_overlaps_test"].sum())
    same_future_bad = int(foldqc["later_or_same_episode_in_train"].sum())
    weight_bad = int(foldqc["train_weight_violations"].sum()) + int(foldqc["test_weight_violation"].sum())

    predictor_spec_bad = int(
        set(MODEL_FEATURES["M3_PLUS_REALTIME_IPT"])
        != {
            "GOLD_RET_3M_LAGGED","GOLD_RET_6M_LAGGED",
            "GOLD_VOL_6M_LAGGED","CYCLE_AGE_MONTHS","RT_IPT_YOY"
        }
    )

    hard_fail = (
        len(TEST_EPISODES) != 4
        or pred["broad_episode_id"].nunique() != 4
        or fold_leak_bad != 0
        or same_future_bad != 0
        or weight_bad != 0
        or gold_feature_timing_bad != 0
        or rt_vintage_timing_bad != 0
        or predictor_spec_bad != 0
        or len(rt_coef) != 4
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-GOLD-OOS-008",
        "panel_rows": int(len(d)),
        "oos_test_episodes": TEST_EPISODES,
        "oos_prediction_rows": int(len(pred)),
        "fold_target_overlap_violations": fold_leak_bad,
        "same_or_future_episode_train_violations": same_future_bad,
        "hierarchical_weight_violations": weight_bad,
        "gold_feature_timing_violations": gold_feature_timing_bad,
        "realtime_vintage_timing_violations": rt_vintage_timing_bad,
        "predictor_spec_violations": predictor_spec_bad,
        "m3_vs_b2_mse_reduction": reduction,
        "m3_episode_wins_vs_b2": beat_count,
        "m3_oos_r2_vs_b0": m3_r2,
        "evidence_status": evidence_status,
        "raw_source_histories_committed": False,
        "causal_status": "NONE",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    # Provenance.
    source = pd.DataFrame([
        {
            "source_object": "Gold monthly",
            "source": gold_prov["source"],
            "url": gold_prov["url"],
            "sha256": gold_prov["sha256"],
            "source_commit": gold_prov.get("source_commit",""),
            "raw_committed": False,
        },
        {
            "source_object": "Real-time IPT derived panel",
            "source": "FED-CYCLE-VINTAGE-AUDIT-007",
            "url": "repository://results/fed_cycle_vintage_audit_v1/PANEL_REALTIME_IPT.csv",
            "sha256": "",
            "source_commit": "",
            "raw_committed": False,
        },
    ])

    source.to_csv(OUT/"SOURCE_REGISTRY.csv", index=False)
    d[[
        "cycle_id","broad_episode_id","panel_month","first_hike",
        "GOLD_RET_3M_LAGGED","GOLD_RET_6M_LAGGED","GOLD_VOL_6M_LAGGED",
        "CYCLE_AGE_MONTHS","RT_IPT_YOY","RT_IPT_VINTAGE_PERIOD",
        "INDPRO_YOY",TARGET,"TARGET_END_PERIOD"
    ]].to_csv(OUT/"OOS_FEATURE_PANEL.csv", index=False)
    foldqc.to_csv(OUT/"FOLD_QC.csv", index=False)
    pred.to_csv(OUT/"OOS_PREDICTIONS.csv", index=False)
    coef.to_csv(OUT/"FOLD_COEFFICIENTS.csv", index=False)
    ep.to_csv(OUT/"EPISODE_METRICS.csv", index=False)
    summary.to_csv(OUT/"MODEL_SUMMARY.csv", index=False)
    pd.DataFrame([{
        "comparison": "M3_PLUS_REALTIME_IPT vs B2_GOLD_PLUS_CYCLE_AGE",
        "b2_episode_equal_mse": b2,
        "m3_episode_equal_mse": m3,
        "mse_reduction_fraction": reduction,
        "m3_episode_wins": beat_count,
        "total_oos_episodes": 4,
        "m3_oos_r2_vs_b0": m3_r2,
        "evidence_status": evidence_status,
        **{f"m3_beats_b2_{k}": v for k,v in beat_flags.items()},
    }]).to_csv(OUT/"PRIMARY_OOS_COMPARISON.csv", index=False)
    (OUT/"QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    make_figures(ep, summary)

    report = [
        "# FED-CYCLE-GOLD-OOS-008 — Report",
        "",
        "**TIME-ORDERED EPISODE-FORWARD OOS / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        "## Frozen evidence gate",
        "",
        f"- status: **{evidence_status}**",
        f"- M3 vs B2 episode-equal MSE reduction: {100*reduction:.2f}%",
        f"- M3 episode wins vs B2: {beat_count}/4",
        f"- M3 OOS R² vs B0: {m3_r2:.4f}",
        "",
        "## Model summary",
        "",
        summary.to_markdown(index=False),
        "",
        "## Per-episode metrics",
        "",
        ep.to_markdown(index=False),
        "",
        "## Real-time IPT standardized coefficient by OOS fold",
        "",
        rt_coef.to_markdown(index=False),
        "",
        "## Interpretation boundary",
        "",
        "- no random split;",
        "- every test broad episode is strictly later than all training episodes;",
        "- training outcomes end before the test episode begins;",
        "- no hyperparameter or feature selection;",
        "- current-vintage D4 is diagnostic only and not PIT-deployable;",
        "- maximum positive label is PRELIMINARY_OOS_CANDIDATE because only four independent future broad episodes are available.",
    ]
    (OUT/"FED_CYCLE_GOLD_OOS_008_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    if hard_fail:
        raise SystemExit("FED-CYCLE-GOLD-OOS-008 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
