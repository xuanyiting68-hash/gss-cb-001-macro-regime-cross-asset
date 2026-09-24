#!/usr/bin/env python3
"""
FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003
Monthly FIRST_HIKE risk clock for Gold, S&P 500, Nasdaq and WTI.

Reference:
research/FED_CYCLE_CROSS_ASSET_RISK_CLOCK_003_LOCK.md
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
OUT = ROOT / "results" / "fed_cycle_risk_clock_v1"
OUT.mkdir(parents=True, exist_ok=True)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


STATE_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_state_panel_v2.py", "state_panel_v2")
PATH_MOD = load_module(ROOT / "scripts" / "run_fed_cycle_path_v1_1.py", "path_v1_1")


def monthly_average(df):
    x = df.dropna(subset=["date", "value"]).copy()
    x["period"] = x["date"].dt.to_period("M")
    return x.groupby("period", as_index=False)["value"].mean().sort_values("period")


def weighted_quantile(values, weights, q):
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    ok = np.isfinite(v) & np.isfinite(w) & (w > 0)
    v, w = v[ok], w[ok]
    if len(v) == 0:
        return np.nan
    order = np.argsort(v)
    v, w = v[order], w[order]
    c = np.cumsum(w) / np.sum(w)
    return float(v[np.searchsorted(c, q, side="left")])


def load_assets():
    prov = []
    assets = {}

    gold, gold_meta = STATE_MOD.load_gold()
    assets["GOLD"] = {
        "df": gold.rename(columns={"price": "value"}),
        "label": "Gold monthly World Bank/DataHub",
        "primary": True,
    }
    prov.append(gold_meta)

    sp, sp_acq = PATH_MOD.fetch_yahoo_chart("^GSPC")
    spm = monthly_average(sp)
    assets["SP500"] = {
        "df": spm,
        "label": "S&P 500 cash index monthly average",
        "primary": True,
    }
    prov.append({
        "series_id": "SP500_^GSPC",
        "source": "Yahoo Finance public chart history",
        "url": sp_acq["url"],
        "acquisition_method": sp_acq["acquisition_method"],
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": sp_acq["sha256"],
        "raw_bytes": sp_acq["raw_bytes"],
        "raw_committed": False,
    })

    for name, sid, label, primary in [
        ("NASDAQ", "NASDAQCOM", "Nasdaq Composite monthly average", True),
        ("WTI", "DCOILWTICO", "WTI spot monthly average", True),
        ("USD_BROAD", "DTWEXBGS", "Nominal Broad U.S. Dollar Index monthly average", False),
    ]:
        d, acq = STATE_MOD.fetch_fred(sid)
        dm = monthly_average(d)
        assets[name] = {"df": dm, "label": label, "primary": primary}
        prov.append({
            "series_id": sid,
            "source": "FRED distribution",
            "url": acq["url"],
            "acquisition_method": acq["acquisition_method"],
            "retrieved_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": acq["sha256"],
            "raw_bytes": acq["raw_bytes"],
            "raw_committed": False,
        })
    return assets, pd.DataFrame(prov)


def path_and_recovery(price_map, event_date):
    event_period = pd.Timestamp(event_date).to_period("M")
    baseline_period = event_period - 1
    post_periods = [event_period + k for k in range(1, 25)]
    if baseline_period not in price_map or any(p not in price_map for p in post_periods):
        return None, None

    baseline = float(price_map[baseline_period])
    post = np.array([float(price_map[p]) for p in post_periods], dtype=float)
    vals = np.concatenate([[baseline], post])
    cumret = post / baseline - 1.0

    running_mdd = []
    running_min_ret = []
    new_low = []
    new_mdd = []
    prior_mdd = -1.0

    for k in range(1, 25):
        sub = vals[: k + 1]
        peaks = np.maximum.accumulate(sub)
        dd = 1.0 - sub / peaks
        rmdd = float(dd.max())
        running_mdd.append(rmdd)
        running_min_ret.append(float(np.min(sub / baseline - 1.0)))
        new_low.append(bool(vals[k] < np.min(vals[:k]) - 1e-15))
        new_mdd.append(bool(rmdd > prior_mdd + 1e-15))
        prior_mdd = rmdd

    event_trough_month = int(np.argmin(post) + 1)
    full_peaks = np.maximum.accumulate(vals)
    full_dd = 1.0 - vals / full_peaks
    mdd = float(full_dd.max())

    if mdd <= 1e-15:
        mdd_trough_month = np.nan
        mdd_peak_idx = np.nan
        recovery = {
            "recovery50_months": np.nan,
            "recovery100_months": np.nan,
            "recovery50_observed": False,
            "recovery100_observed": False,
            "recovery_censor_months": np.nan,
        }
    else:
        trough_idx = int(np.argmax(full_dd))
        mdd_trough_month = int(trough_idx)
        peak_idx = int(np.argmax(vals[: trough_idx + 1]))
        mdd_peak_idx = peak_idx

        peak_price = float(vals[peak_idx])
        trough_price = float(vals[trough_idx])
        threshold50 = trough_price + 0.5 * (peak_price - trough_price)
        threshold100 = peak_price

        trough_period = baseline_period if trough_idx == 0 else event_period + trough_idx
        rec = []
        for j in range(0, 61):
            p = trough_period + j
            if p in price_map:
                rec.append((j, float(price_map[p])))
        hit50 = [j for j, v in rec if v >= threshold50]
        hit100 = [j for j, v in rec if v >= threshold100]
        recovery = {
            "recovery50_months": int(hit50[0]) if hit50 else np.nan,
            "recovery100_months": int(hit100[0]) if hit100 else np.nan,
            "recovery50_observed": bool(hit50),
            "recovery100_observed": bool(hit100),
            "recovery_censor_months": int(rec[-1][0]) if rec else np.nan,
        }

    path_rows = []
    for k in range(1, 25):
        path_rows.append({
            "event_month": k,
            "cum_return": float(cumret[k - 1]),
            "running_mdd": float(running_mdd[k - 1]),
            "running_min_return": float(running_min_ret[k - 1]),
            "new_event_low": bool(new_low[k - 1]),
            "new_running_mdd": bool(new_mdd[k - 1]),
        })

    cycle_metrics = {
        "baseline_period": str(baseline_period),
        "ret_12m": float(post[11] / baseline - 1.0),
        "ret_24m": float(post[23] / baseline - 1.0),
        "mdd_24m": mdd,
        "mfe_24m": float(np.max(vals / baseline - 1.0)),
        "event_trough_month": event_trough_month,
        "mdd_trough_month": mdd_trough_month,
        "mdd_peak_index": mdd_peak_idx,
        **recovery,
    }
    return path_rows, cycle_metrics


def build_asset_paths(cycles, assets):
    all_path = []
    all_cycles = []

    broad_counts = cycles.groupby("broad_episode_id")["cycle_id"].count().to_dict()

    for asset, obj in assets.items():
        df = obj["df"].copy()
        price_map = dict(zip(df["period"], df["value"].astype(float)))
        available = []

        for _, cyc in cycles.iterrows():
            p, m = path_and_recovery(price_map, cyc["first_hike"])
            if p is None:
                continue
            available.append((cyc, p, m))

        # Reweight within available legs of each broad episode.
        avail_counts = {}
        for cyc, _, _ in available:
            bid = cyc["broad_episode_id"]
            avail_counts[bid] = avail_counts.get(bid, 0) + 1

        for cyc, p, m in available:
            bid = cyc["broad_episode_id"]
            weight = 1.0 / avail_counts[bid]
            base = {
                "asset": asset,
                "asset_label": obj["label"],
                "primary_asset": bool(obj["primary"]),
                "cycle_id": cyc["cycle_id"],
                "broad_episode_id": bid,
                "cycle_start_year": int(pd.Timestamp(cyc["first_hike"]).year),
                "first_hike": pd.Timestamp(cyc["first_hike"]),
                "episode_weight": weight,
            }
            for row in p:
                all_path.append({**base, **row})
            all_cycles.append({**base, **m})

    return pd.DataFrame(all_path), pd.DataFrame(all_cycles)


def summarize_clock(paths, cycles):
    rows = []
    for asset, gcy in cycles.groupby("asset"):
        gp = paths[paths["asset"] == asset]
        for k in range(1, 25):
            pm = gp[gp["event_month"] == k].copy()
            if pm.empty:
                continue
            w = pm["episode_weight"].to_numpy(float)

            # Cycle-level fixed trough months repeated only once via gcy.
            valid_mdd = gcy.dropna(subset=["mdd_trough_month"]).copy()
            denom_cdf = float(gcy["episode_weight"].sum())
            trough_cdf = float(
                gcy.loc[gcy["event_trough_month"] <= k, "episode_weight"].sum() / denom_cdf
            )
            mdd_cdf = (
                float(valid_mdd.loc[valid_mdd["mdd_trough_month"] <= k, "episode_weight"].sum()
                      / valid_mdd["episode_weight"].sum())
                if len(valid_mdd) else np.nan
            )
            risk = valid_mdd[valid_mdd["mdd_trough_month"] >= k]
            hazard = (
                float(valid_mdd.loc[valid_mdd["mdd_trough_month"] == k, "episode_weight"].sum()
                      / risk["episode_weight"].sum())
                if len(risk) and risk["episode_weight"].sum() > 0 else np.nan
            )

            rows.append({
                "asset": asset,
                "event_month": k,
                "n_legs": int(pm["cycle_id"].nunique()),
                "n_broad_episodes": int(pm["broad_episode_id"].nunique()),
                "weighted_median_cum_return": weighted_quantile(pm["cum_return"], w, 0.5),
                "weighted_q25_cum_return": weighted_quantile(pm["cum_return"], w, 0.25),
                "weighted_q75_cum_return": weighted_quantile(pm["cum_return"], w, 0.75),
                "weighted_median_running_mdd": weighted_quantile(pm["running_mdd"], w, 0.5),
                "weighted_q75_running_mdd": weighted_quantile(pm["running_mdd"], w, 0.75),
                "weighted_new_event_low_share": float(np.average(pm["new_event_low"].astype(float), weights=w)),
                "weighted_new_running_mdd_share": float(np.average(pm["new_running_mdd"].astype(float), weights=w)),
                "event_trough_cdf": trough_cdf,
                "mdd_trough_cdf": mdd_cdf,
                "mdd_trough_hazard": hazard,
            })
    return pd.DataFrame(rows)


def timing_summary(cycles):
    rows = []
    for asset, g in cycles.groupby("asset"):
        w = g["episode_weight"].to_numpy(float)
        mdd_month = pd.to_numeric(g["mdd_trough_month"], errors="coerce")
        valid = np.isfinite(mdd_month)
        gv = g.loc[valid].copy()
        if len(gv):
            wv = gv["episode_weight"].to_numpy(float)
            early = float(gv.loc[gv["mdd_trough_month"].between(1, 6), "episode_weight"].sum() / wv.sum())
            mid = float(gv.loc[gv["mdd_trough_month"].between(7, 12), "episode_weight"].sum() / wv.sum())
            late = float(gv.loc[gv["mdd_trough_month"].between(13, 24), "episode_weight"].sum() / wv.sum())
            med = weighted_quantile(gv["mdd_trough_month"], wv, 0.5)
            q75 = weighted_quantile(gv["mdd_trough_month"], wv, 0.75)
        else:
            early = mid = late = med = q75 = np.nan
        rows.append({
            "asset": asset,
            "n_legs": int(g["cycle_id"].nunique()),
            "n_broad_episodes": int(g["broad_episode_id"].nunique()),
            "weighted_median_mdd_trough_month": med,
            "weighted_q75_mdd_trough_month": q75,
            "mdd_trough_share_early_1_6": early,
            "mdd_trough_share_mid_7_12": mid,
            "mdd_trough_share_late_13_24": late,
            "weighted_median_mdd_24m": weighted_quantile(g["mdd_24m"], w, 0.5),
            "weighted_median_ret_12m": weighted_quantile(g["ret_12m"], w, 0.5),
            "weighted_median_ret_24m": weighted_quantile(g["ret_24m"], w, 0.5),
            "support_status": (
                "PRIMARY_SUPPORTED"
                if g["cycle_id"].nunique() >= 5 and g["broad_episode_id"].nunique() >= 4
                else "DIAGNOSTIC_LIMITED_SUPPORT"
            ),
        })
    return pd.DataFrame(rows)


def weighted_km(g, level):
    observed_col = f"recovery{level}_observed"
    duration_col = f"recovery{level}_months"
    rows = []
    d = g[g["mdd_24m"] > 1e-15].copy()
    if d.empty:
        return pd.DataFrame()

    d["duration"] = np.where(
        d[observed_col].astype(bool),
        pd.to_numeric(d[duration_col], errors="coerce"),
        pd.to_numeric(d["recovery_censor_months"], errors="coerce"),
    )
    d = d.dropna(subset=["duration"]).copy()
    d["duration"] = d["duration"].astype(int)

    surv = 1.0
    rows.append({
        "time_months": 0,
        "at_risk_weight": float(d["episode_weight"].sum()),
        "event_weight": 0.0,
        "censor_weight": 0.0,
        "survival_not_recovered": 1.0,
    })
    for t in sorted(d["duration"].unique()):
        risk = float(d.loc[d["duration"] >= t, "episode_weight"].sum())
        ev = float(d.loc[(d["duration"] == t) & d[observed_col].astype(bool), "episode_weight"].sum())
        cens = float(d.loc[(d["duration"] == t) & (~d[observed_col].astype(bool)), "episode_weight"].sum())
        if risk > 0 and ev > 0:
            surv *= 1.0 - ev / risk
        rows.append({
            "time_months": int(t),
            "at_risk_weight": risk,
            "event_weight": ev,
            "censor_weight": cens,
            "survival_not_recovered": float(surv),
        })
    return pd.DataFrame(rows)


def build_recovery(cycles):
    curves = []
    summary = []
    for asset, g in cycles.groupby("asset"):
        for level in (50, 100):
            km = weighted_km(g, level)
            if km.empty:
                continue
            km["asset"] = asset
            km["recovery_level"] = f"{level}%"
            curves.append(km)
            hit = km[km["survival_not_recovered"] <= 0.5 + 1e-12]
            median = int(hit.iloc[0]["time_months"]) if len(hit) else np.nan
            summary.append({
                "asset": asset,
                "recovery_level": f"{level}%",
                "n_legs": int(g["cycle_id"].nunique()),
                "n_broad_episodes": int(g["broad_episode_id"].nunique()),
                "observed_recoveries": int(g[f"recovery{level}_observed"].astype(bool).sum()),
                "right_censored": int((~g[f"recovery{level}_observed"].astype(bool) & (g["mdd_24m"] > 1e-15)).sum()),
                "weighted_km_median_months": median,
            })
    return (
        pd.concat(curves, ignore_index=True) if curves else pd.DataFrame(),
        pd.DataFrame(summary),
    )


def make_figures(clock, cycles, recovery):
    prim = ["GOLD", "SP500", "NASDAQ", "WTI"]

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    for asset in prim:
        g = clock[clock["asset"] == asset]
        if len(g):
            ax.plot(g["event_month"], g["weighted_median_running_mdd"] * 100, label=asset)
    ax.set_title("FIRST_HIKE risk clock: weighted median running MDD")
    ax.set_xlabel("Complete months after FIRST_HIKE event month")
    ax.set_ylabel("Running maximum drawdown (%)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "01_cross_asset_running_mdd_clock.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    for asset in prim:
        g = clock[clock["asset"] == asset]
        if len(g):
            ax.plot(g["event_month"], g["mdd_trough_hazard"], label=asset)
    ax.set_title("FIRST_HIKE risk clock: empirical MDD-trough hazard")
    ax.set_xlabel("Complete months after FIRST_HIKE event month")
    ax.set_ylabel("Weighted discrete hazard")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "02_cross_asset_mdd_trough_hazard.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    for asset in prim:
        g = recovery[
            (recovery["asset"] == asset)
            & (recovery["recovery_level"] == "100%")
        ]
        if len(g):
            ax.step(g["time_months"], g["survival_not_recovered"], where="post", label=asset)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 1.02)
    ax.set_title("Full-recovery survival after 24M-window MDD trough")
    ax.set_xlabel("Months after MDD trough")
    ax.set_ylabel("Weighted share not yet fully recovered")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "03_cross_asset_full_recovery_survival.png", dpi=170, bbox_inches="tight")
    plt.close(fig)

    gold = cycles[(cycles["asset"] == "GOLD") & cycles["cycle_start_year"].isin([2015, 2022])]
    if len(gold):
        gp = pd.read_csv(OUT / "RISK_CLOCK_PATHS.csv")
        q = gp[(gp["asset"] == "GOLD") & gp["cycle_start_year"].isin([2015, 2022])]
        fig, ax = plt.subplots(figsize=(9.5, 5.5))
        for yr, gg in q.groupby("cycle_start_year"):
            ax.plot(gg["event_month"], gg["cum_return"] * 100, label=str(yr))
        ax.axhline(0, linewidth=0.8)
        ax.set_title("Gold 2015 vs 2022 monthly FIRST_HIKE paths")
        ax.set_xlabel("Complete months after event month")
        ax.set_ylabel("Cumulative return from M-1 baseline (%)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUT / "04_gold_2015_2022_monthly_risk_clock.png", dpi=170, bbox_inches="tight")
        plt.close(fig)


def write_report(timing, recovery_summary, qc):
    primary = timing[timing["support_status"] == "PRIMARY_SUPPORTED"].copy()
    lines = [
        "# FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003 — Report",
        "",
        "**DESCRIPTIVE TIMING DISTRIBUTION / NOT CAUSAL / NOT A FORECASTING MODEL / NOT DEPLOYABLE**",
        "",
        "## QC",
        "",
        f"- QC gate: {qc['qc_gate']}",
        f"- Primary supported assets: {', '.join(qc['primary_supported_assets'])}",
        "- Event month omitted; clock uses months 1-24 after FIRST_HIKE event month.",
        "- Primary aggregation gives each broad episode equal total weight.",
        "",
        "## MDD timing summary",
        "",
        primary.to_markdown(index=False),
        "",
        "## Recovery summary",
        "",
        recovery_summary.to_markdown(index=False),
        "",
        "## Evidence boundary",
        "",
        "- These are historical timing distributions around realized Fed cycle markers.",
        "- They do not imply that Fed hikes caused the trough timing.",
        "- No p-value/FDR family is run.",
        "- OOS is not applicable; this is not a forecasting model.",
        "- Use as a risk clock, not a deterministic market-timing rule.",
    ]
    (OUT / "FED_CYCLE_CROSS_ASSET_RISK_CLOCK_003_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    cycles = STATE_MOD.assign_broad_clusters(STATE_MOD.load_cycles())
    assets, prov = load_assets()
    paths, cycle_metrics = build_asset_paths(cycles, assets)

    clock = summarize_clock(paths, cycle_metrics)
    timing = timing_summary(cycle_metrics)
    recovery, recovery_summary = build_recovery(cycle_metrics)

    # QC.
    primary_supported = timing.loc[
        timing["support_status"] == "PRIMARY_SUPPORTED", "asset"
    ].tolist()
    required_primary = {"GOLD", "SP500", "NASDAQ", "WTI"}

    event_month_bad = int(((paths["event_month"] < 1) | (paths["event_month"] > 24)).sum())
    mdd_bad = int((pd.to_numeric(cycle_metrics["mdd_24m"], errors="coerce") < -1e-12).sum())
    mdd_month = pd.to_numeric(cycle_metrics["mdd_trough_month"], errors="coerce")
    mdd_trough_bad = int((mdd_month.notna() & ~mdd_month.between(1, 24)).sum())

    both = cycle_metrics.dropna(subset=["recovery50_months", "recovery100_months"])
    recovery_bad = int((both["recovery100_months"] < both["recovery50_months"]).sum())

    weight_bad = 0
    for asset, ga in cycle_metrics.groupby("asset"):
        for bid, gb in ga.groupby("broad_episode_id"):
            if abs(float(gb["episode_weight"].sum()) - 1.0) > 1e-10:
                weight_bad += 1

    hard_fail = (
        not required_primary.issubset(set(primary_supported))
        or event_month_bad != 0
        or mdd_bad != 0
        or mdd_trough_bad != 0
        or recovery_bad != 0
        or weight_bad != 0
    )

    qc = {
        "qc_gate": "FAIL" if hard_fail else "PASS",
        "module": "FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003",
        "path_rows": int(len(paths)),
        "cycle_asset_rows": int(len(cycle_metrics)),
        "primary_supported_assets": sorted(primary_supported),
        "event_month_violations": event_month_bad,
        "negative_mdd_violations": mdd_bad,
        "mdd_trough_month_violations": mdd_trough_bad,
        "recovery_order_violations": recovery_bad,
        "broad_episode_weight_sum_violations": weight_bad,
        "event_month_omitted": True,
        "raw_source_histories_committed": False,
        "fdr_status": "NOT_APPLICABLE_DESCRIPTIVE_TIMING_MODULE",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }

    prov.to_csv(OUT / "SOURCE_REGISTRY.csv", index=False)
    paths.to_csv(OUT / "RISK_CLOCK_PATHS.csv", index=False)
    cycle_metrics.to_csv(OUT / "CYCLE_ASSET_METRICS.csv", index=False)
    clock.to_csv(OUT / "RISK_CLOCK_SUMMARY.csv", index=False)
    timing.to_csv(OUT / "MDD_TIMING_SUMMARY.csv", index=False)
    recovery.to_csv(OUT / "RECOVERY_KM.csv", index=False)
    recovery_summary.to_csv(OUT / "RECOVERY_SUMMARY.csv", index=False)
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    # Figures require path CSV for the Gold comparison helper.
    make_figures(clock, cycle_metrics, recovery)
    write_report(timing, recovery_summary, qc)

    if hard_fail:
        raise SystemExit("FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003 QC failed")

    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
