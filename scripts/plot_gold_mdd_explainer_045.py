#!/usr/bin/env python3
"""Replot canonical 004 gold monthly average path as a legible MDD explainer."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "gold_mdd_explainer_045"
OUT.mkdir(parents=True, exist_ok=True)
PATH = ROOT / "results" / "fed_cycle_phase_clock_v1"
PATHS = pd.read_csv(PATH / "PHASE_PATHS.csv")
METRICS = pd.read_csv(PATH / "PHASE_CYCLE_ASSET_METRICS.csv")
IDS = [("T07_1999", "1999 first hike: the 11.6% median example"),
       ("T10_2022", "2022 first hike: positive finish, 14.1% MDD"),
       ("T01_1983", "1983 first hike: 24.4% MDD")]


def build(cid):
    g = PATHS[(PATHS.asset == "GOLD") & (PATHS.anchor == "FIRST_HIKE") &
              (PATHS.cycle_id == cid)].sort_values("event_month")
    assert list(g.event_month) == list(range(1, 13))
    metric = METRICS[(METRICS.asset == "GOLD") & (METRICS.anchor == "FIRST_HIKE") &
                     (METRICS.cycle_id == cid)]
    assert len(metric) == 1
    val = 100 * np.r_[1., 1. + g.cum_return.to_numpy(float)]
    x = np.r_[-1, np.arange(1, 13)]
    dd = 1 - val / np.maximum.accumulate(val)
    trough = int(np.argmax(dd))
    peak = int(np.argmax(val[:trough + 1]))
    assert abs(float(np.max(dd)) - float(metric.iloc[0].mdd_12m)) < 1e-12
    assert abs(float(val[-1]/100 - 1) - float(metric.iloc[0].ret_12m)) < 1e-12
    return x, val, peak, trough, float(max(dd)), metric.iloc[0]


def draw(ax, cid, title, big=False):
    x, val, peak, trough, mdd, metric = build(cid)
    ax.axvspan(-.45, .45, color="#e8edf3", alpha=.85, zorder=0)
    ax.axhline(100, color="#718096", linestyle="--", linewidth=1)
    ax.plot(x[1:], val[1:], "-o", lw=2.8 if big else 2.2, ms=5, color="#17456b")
    ax.plot(x[:2], val[:2], ":", lw=1.6, color="#17456b")
    ax.scatter([x[0]], [val[0]], s=60, color="#17456b", zorder=5)
    ax.scatter([x[peak]], [val[peak]], s=90, color="#e0a128", zorder=6)
    ax.scatter([x[trough]], [val[trough]], s=90, color="#b23a3e", zorder=6)
    ax.scatter([x[-1]], [val[-1]], s=90, color="#288966", zorder=6)
    # Exact price levels are monthly averages normalized to 100 at M-1.
    ax.annotate(f"peak {val[peak]:.1f}", (x[peak], val[peak]),
                xytext=(0, 12), textcoords="offset points", ha="center", fontsize=10)
    ax.annotate(f"trough {val[trough]:.1f}", (x[trough], val[trough]),
                xytext=(0, -21), textcoords="offset points", ha="center", fontsize=10)
    ax.annotate(f"finish {val[-1]:.1f}", (x[-1], val[-1]),
                xytext=(-3, 10), textcoords="offset points", ha="right", fontsize=10)
    ax.text(.03, .05, f"MDD {mdd*100:.1f}%  |  12M final {metric.ret_12m*100:+.1f}%",
            transform=ax.transAxes, fontsize=13 if big else 11,
            bbox=dict(facecolor="white", edgecolor="#d2d8dd", alpha=.95, boxstyle="round,pad=.35"))
    ax.set_title(title, loc="left", weight="bold", fontsize=13 if big else 12)
    ax.set_xlim(-1.8, 13)
    ax.set_xticks([-1, 1, 4, 7, 10, 12], ["M-1", "M+1", "M+4", "M+7", "M+10", "M+12"])
    ax.set_ylabel("Monthly average, M-1 = 100")
    ax.grid(alpha=.17)
    return {"cycle_id":cid, "baseline":100., "peak_index":int(x[peak]),
            "peak_indexed_price":round(float(val[peak]),5), "trough_index":int(x[trough]),
            "trough_indexed_price":round(float(val[trough]),5),
            "mdd_pct":round(100*mdd,5), "endpoint_pct":round(100*float(metric.ret_12m),5)}


def main():
    all_gold = METRICS[(METRICS.asset == "GOLD") & (METRICS.anchor == "FIRST_HIKE")].copy()
    assert len(all_gold) == 10 and all_gold.broad_episode_id.nunique() == 7
    rows = all_gold[["cycle_id", "broad_episode_id", "anchor_date", "baseline_period", "episode_weight",
                     "ret_12m", "mdd_12m", "mdd_trough_month"]].sort_values("anchor_date").copy()
    rows["ret_12m"] *= 100
    rows["mdd_12m"] *= 100
    rows.rename(columns={"ret_12m":"nominal_12m_price_change_pct", "mdd_12m":"monthly_path_mdd_12m_pct"}).to_csv(
        OUT / "GOLD_FIRST_HIKE_ALL_TEN.csv", index=False, float_format="%.10g")
    fig = plt.figure(figsize=(16, 8), layout="constrained")
    grid = GridSpec(2, 2, figure=fig, width_ratios=[1.35, 1], height_ratios=[1, 1])
    ax = [fig.add_subplot(grid[:, 0]), fig.add_subplot(grid[0, 1]), fig.add_subplot(grid[1, 1])]
    checks = [draw(a, *entry, big=(i==0)) for i, (a, entry) in enumerate(zip(ax, IDS))]
    ax[0].set_ylim(88, 119)
    ax[1].set_ylim(84, 111)
    ax[2].set_ylim(68, 107)
    fig.suptitle("How a final gain can hide a large peak-to-trough drawdown", fontsize=17, weight="bold")
    fig.supxlabel("Gold World Bank monthly averages; event month M0 intentionally omitted. Not OHLC candles.", fontsize=11)
    chart_file = OUT / "GOLD_FIRST_HIKE_MDD_SEE_THE_PATH.png"
    fig.savefig(chart_file, dpi=165)
    plt.close(fig)
    # Geometry and text remain fixed; reducing the color palette keeps the artifact compact.
    with Image.open(chart_file) as rendered:
        rendered.convert("RGB").quantize(colors=128, method=Image.Quantize.FASTOCTREE).save(
            chart_file, optimize=True)
    assert abs(checks[0]["mdd_pct"] - 11.57556) < .00001
    (OUT / "QC.json").write_text(json.dumps({"status":"PASS_VISUAL_ONLY","source":"canonical 004 PHASE_PATHS and PHASE_CYCLE_ASSET_METRICS",
        "all_first_hike_mechanical_legs":len(all_gold),"broad_episodes":all_gold.broad_episode_id.nunique(),
        "chosen_cases":["1999 weighted median MDD example","2022 positive endpoint / large MDD","1983 largest MDD"],
        "checks":checks,"no_ohlc":True,"no_new_trading_inference":True},indent=2)+"\n")
    print(checks)


if __name__ == "__main__":
    main()
