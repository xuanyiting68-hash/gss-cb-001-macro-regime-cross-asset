#!/usr/bin/env python3
"""Frozen 043: retrospective IMF world grain benchmarks around canonical Fed anchors."""
from __future__ import annotations

import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "commodity_fed_cycle_phase_043"
OUT.mkdir(parents=True, exist_ok=True)
IDS = {"WHEAT": "PWHEAMTUSDM", "CORN": "PMAIZMTUSDM", "SOYBEANS": "PSOYBUSDM"}
ANCHORS = {"FIRST_HIKE": "first_hike", "LAST_HIKE": "last_hike",
           "PAUSE_START": "pause_start", "FIRST_CUT": "first_cut"}


def quantile(v, w, q):
    v, w = np.asarray(v, float), np.asarray(w, float)
    ix = np.argsort(v)
    v, w = v[ix], w[ix]
    return float(v[np.searchsorted(np.cumsum(w) / sum(w), q, side="left")])


def acquire():
    prices, provenance = {}, {}
    for name, ident in IDS.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={ident}"
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0 public research"}), timeout=45) as f:
            raw = f.read()
        df = pd.read_csv(io.BytesIO(raw))
        df.columns = ["date", "value"]
        df.date = pd.to_datetime(df.date)
        df.value = pd.to_numeric(df.value, errors="coerce")
        df = df[df.date <= pd.Timestamp("2026-09-27")]
        assert len(df) > 400 and df.date.is_unique and df.value.gt(0).all()
        assert df.date.dt.to_period("M").tolist() == list(pd.period_range(df.date.min(), df.date.max(), freq="M"))
        prices[name] = dict(zip(df.date.dt.to_period("M"), df.value))
        provenance[name] = {"series": ident, "url": url, "sha256_raw_acquisition": hashlib.sha256(raw).hexdigest(),
                            "first_month": str(df.date.min().to_period("M")),
                            "last_month": str(df.date.max().to_period("M")), "observations": len(df),
                            "units": "USD/metric ton, nominal IMF world benchmark; not futures return"}
    return prices, provenance


def main():
    prices, provenance = acquire()
    cycles = pd.read_csv(ROOT / "results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv")
    mapping = (pd.read_csv(ROOT / "results/fed_cycle_phase_clock_v1/PHASE_CYCLE_ASSET_METRICS.csv")
               [["cycle_id", "broad_episode_id"]].drop_duplicates())
    assert mapping.cycle_id.is_unique
    cycles = cycles.merge(mapping, on="cycle_id", validate="one_to_one")
    records = []
    for asset, series in prices.items():
        for anchor, col in ANCHORS.items():
            for cyc in cycles.itertuples(index=False):
                date = getattr(cyc, col)
                if pd.isna(date):
                    continue
                m = pd.Timestamp(date).to_period("M")
                months = [m - 1] + [m + i for i in range(1, 13)]
                if any(k not in series for k in months):
                    continue
                arr = np.array([series[k] for k in months])
                dd = 1 - arr / np.maximum.accumulate(arr)
                records.append({"asset": asset, "anchor": anchor, "cycle_id": cyc.cycle_id,
                                "broad_episode_id": cyc.broad_episode_id,
                                "anchor_date": str(pd.Timestamp(date).date()), "baseline_period": str(m-1),
                                "ret_3m": arr[3]/arr[0]-1, "ret_6m": arr[6]/arr[0]-1,
                                "ret_12m": arr[12]/arr[0]-1, "mdd_12m": max(dd),
                                "mae_12m": min(arr/arr[0]-1), "mfe_12m": max(arr/arr[0]-1),
                                "mdd_trough_month": int(np.argmax(dd)) if max(dd)>1e-15 else np.nan,
                                "last_month": str(months[-1])})
    ev = pd.DataFrame(records).sort_values(["asset", "anchor", "anchor_date"])
    assert ev.groupby(["asset", "anchor"]).size().min() >= 4
    assert not ev.duplicated(["asset", "anchor", "cycle_id"]).any()
    # Independent transcription from FRED's published table, checked 2026-09-27.
    # M-1=2022-02 and M+12=2023-03 for the 2022 first-hike anchor.
    check = ev[(ev.asset == "CORN") & (ev.anchor == "FIRST_HIKE") & (ev.cycle_id == "T10_2022")]
    assert len(check) == 1 and check.iloc[0].baseline_period == "2022-02"
    assert abs(check.iloc[0].ret_12m - (284.95740496894420 / 292.67159304511270 - 1)) < 1e-10
    ev["episode_weight"] = 1 / ev.groupby(["asset", "anchor", "broad_episode_id"]).cycle_id.transform("count")
    rows = []
    for (asset, anchor), g in ev.groupby(["asset", "anchor"]):
        w = g.episode_weight
        nb = g.broad_episode_id.nunique()
        row = {"asset": asset, "anchor": anchor, "n_legs": len(g), "n_broad_episodes": nb,
               "support_status": "SUPPORTED_DESCRIPTIVE" if len(g)>=5 and nb>=4 else "LIMITED_DESCRIPTIVE",
               "weighted_negative_12m_share": float(np.average(g.ret_12m<0, weights=w))}
        for key in ["ret_3m", "ret_6m", "ret_12m", "mdd_12m", "mae_12m", "mfe_12m"]:
            for q, label in [(0.1, "q10"), (0.5, "median"), (0.9, "q90")]:
                row[f"weighted_{label}_{key}"] = quantile(g[key], w, q)
        rows.append(row)
        assert np.isclose(w.sum(), nb)
    summary = pd.DataFrame(rows).sort_values(["anchor", "asset"])
    assert len(summary) == 12 and len(ev) == summary.n_legs.sum()
    # Explicit preservation of representative failures and all-sample event rows.
    case = ev[(ev.anchor == "FIRST_HIKE") & ev.cycle_id.isin(
        ["T06_1994", "T08_2004", "T09_2015", "T10_2022"])].copy()
    assert len(case) == 12
    ev.to_csv(OUT / "GRAIN_PHASE_EVENT_METRICS.csv", index=False, float_format="%.10g")
    summary.to_csv(OUT / "GRAIN_PHASE_DISTRIBUTION.csv", index=False, float_format="%.10g")
    case.to_csv(OUT / "FOUR_FIRST_HIKE_CASES.csv", index=False, float_format="%.10g")

    # Two fixed measures; no phase/asset winner implied.
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), layout="constrained")
    phase_order = list(ANCHORS)
    for ax, col, title, cmap in [(axes[0], "weighted_median_ret_12m", "12M price change (%)", "RdBu_r"),
                                  (axes[1], "weighted_median_mdd_12m", "12M maximum drawdown (%)", "YlOrRd")]:
        mat = summary.pivot(index="anchor", columns="asset", values=col).loc[phase_order, list(IDS)] * 100
        im = ax.imshow(mat, cmap=cmap, vmin=(-30 if col.endswith("ret_12m") else 0),
                       vmax=(30 if col.endswith("ret_12m") else 50), aspect="auto")
        ax.set_xticks(range(3), ["Wheat", "Corn", "Soybeans"])
        ax.set_yticks(range(4), ["First hike", "Last hike", "Pause start", "First cut"])
        ax.set_title(title)
        for i in range(4):
            for j in range(3):
                ax.text(j, i, f"{mat.iloc[i,j]:+.1f}" if col.endswith("ret_12m") else f"{mat.iloc[i,j]:.1f}",
                        ha="center", va="center", fontsize=10)
        fig.colorbar(im, ax=ax, shrink=.7)
    fig.suptitle("IMF world grain benchmarks around Fed cycle anchors; retrospective, not tradable returns", fontsize=11)
    fig.savefig(OUT / "GRAIN_PHASE_PRICES_AND_RISK.png", dpi=160)
    plt.close(fig)
    qc = {"status": "PASS_DESCRIPTIVE_ONLY", "run_utc": datetime.now(timezone.utc).isoformat(),
          "sources": provenance, "event_rows": len(ev), "phase_cells": len(summary),
          "support_cells": int((summary.support_status=="SUPPORTED_DESCRIPTIVE").sum()),
          "limited_cells": int((summary.support_status=="LIMITED_DESCRIPTIVE").sum()),
          "event_dates": "canonical 004", "raw_source_rows_committed": False,
          "independent_fred_table_check": "PASS: 2022 corn 284.95740496894420/292.67159304511270-1",
          "limitations": ["current-vintage retrospective", "global spot proxy not futures",
                          "overlapping events", "no PIT, OOS or cost-adjusted test"]}
    (OUT / "QC.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2)+"\n")
    print(summary[["asset", "anchor", "n_legs", "n_broad_episodes", "support_status",
                   "weighted_median_ret_12m", "weighted_median_mdd_12m", "weighted_negative_12m_share"]].to_string(index=False))
    print(case[["asset", "cycle_id", "ret_12m", "mdd_12m"]].to_string(index=False))


if __name__ == "__main__":
    main()
