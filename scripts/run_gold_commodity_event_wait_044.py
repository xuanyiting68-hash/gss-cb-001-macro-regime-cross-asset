#!/usr/bin/env python3
"""044: exact-matched descriptive gold/grain diagnostics; no price data redistributed."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/gold_commodity_event_wait_044"
OUT.mkdir(exist_ok=True, parents=True)


def wq(x, w):
    i = np.argsort(np.asarray(x, float))
    v = np.asarray(x, float)[i]
    z = np.asarray(w, float)[i]
    return float(v[np.searchsorted(np.cumsum(z) / sum(z), .5, side="left")])


def main():
    core = pd.read_csv(ROOT / "results/fed_cycle_phase_clock_v1/PHASE_CYCLE_ASSET_METRICS.csv")
    gold = core[(core.asset == "GOLD") & (core.anchor == "FIRST_HIKE")].copy()
    assert len(gold) == 10 and gold.broad_episode_id.nunique() == 7
    grain = pd.read_csv(ROOT / "results/commodity_fed_cycle_phase_043/GRAIN_PHASE_EVENT_METRICS.csv")
    grain = grain[(grain.asset == "CORN") & (grain.anchor == "FIRST_HIKE")].copy()
    assert len(grain) == 5 and grain.broad_episode_id.nunique() == 5
    # One gold leg per grain leg; the gold and grain event dates must be identical.
    match = gold.merge(grain, on="cycle_id", validate="one_to_one", suffixes=("_gold", "_corn"))
    assert len(match) == 5 and (match.anchor_date_gold == match.anchor_date_corn).all()
    panel = match[["cycle_id", "broad_episode_id_gold", "anchor_date_gold",
                   "ret_12m_gold", "mdd_12m_gold", "mae_12m_gold",
                   "ret_12m_corn", "mdd_12m_corn", "mfe_12m_corn"]].copy()
    panel.columns = ["cycle_id", "broad_episode_id", "anchor_date", "gold_12m_price_pct",
                     "gold_12m_mdd_pct", "gold_12m_mae_pct", "corn_12m_price_pct",
                     "corn_12m_mdd_pct", "corn_12m_mfe_pct"]
    for c in panel.columns[3:]:
        panel[c] *= 100
    panel = panel.sort_values("anchor_date")
    panel.to_csv(OUT / "MATCHED_GOLD_CORN_FIRST_HIKE.csv", index=False, float_format="%.8g")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout="constrained")
    full_gold = gold.sort_values("anchor_date").copy()
    labels = [str(s)[:7] for s in full_gold.anchor_date]
    pos = np.arange(len(labels))
    axes[0].bar(pos-.19, full_gold.ret_12m*100, width=.38, label="Gold 12M price change")
    axes[0].bar(pos+.19, -full_gold.mdd_12m*100, width=.38, label="Gold 12M MDD shown below 0")
    axes[0].axhline(0, color="black", lw=.6)
    axes[0].set_xticks(pos, labels, rotation=50)
    axes[0].set_title("10 first-hike gold legs: endpoint vs. path loss")
    axes[0].legend(fontsize=7, loc="lower right", frameon=False)
    pos2 = np.arange(len(panel))
    axes[1].bar(pos2-.18, panel.gold_12m_price_pct, width=.36, label="Gold price")
    axes[1].bar(pos2+.18, panel.corn_12m_price_pct, width=.36, label="Global corn spot")
    axes[1].axhline(0, color="black", lw=.6)
    axes[1].set_xticks(pos2, [s[-4:] for s in panel.cycle_id])
    axes[1].set_title("Exact-matched 1994–2022 first-hike 12M endpoints")
    axes[1].legend(fontsize=7, frameon=False)
    for ax in axes:
        ax.set_ylabel("Percent (%)")
        ax.grid(axis="y", alpha=.15)
    fig.suptitle("Historical monthly price changes, not executable trading returns", fontsize=11)
    fig.savefig(OUT / "GOLD_ENDPOINT_VS_DRAWDOWN_MATCHED_CORN.png", dpi=160)
    plt.close(fig)
    by_leg_negative = int((gold.ret_12m < 0).sum())
    weighted_negative = float(np.average(gold.ret_12m < 0, weights=gold.episode_weight))
    cross = pd.read_csv(ROOT / "results/fed_cycle_phase_clock_v1/PHASE_COMPARISON.csv")
    cross = cross[(cross.asset == "GOLD") & (cross.anchor == "FIRST_HIKE")].iloc[0]
    med_return = wq(gold.ret_12m, gold.episode_weight)
    med_mdd = wq(gold.mdd_12m, gold.episode_weight)
    assert np.isclose(med_return, cross.weighted_median_ret_12m, atol=1e-12)
    assert np.isclose(med_mdd, cross.weighted_median_mdd_12m, atol=1e-12)
    assert np.isclose(gold.episode_weight.sum(), 7)
    assert (panel.corn_12m_price_pct < 0).all()
    assert abs(panel.loc[panel.cycle_id == "T10_2022", "corn_12m_price_pct"].iloc[0] + 2.635782993) < .000001
    qc = {"status": "PASS_DESCRIPTIVE_ONLY", "gold_first_hike_legs": len(gold),
          "gold_broad_episodes": 7, "gold_negative_legs": by_leg_negative,
          "gold_weighted_negative_share": weighted_negative,
          "gold_weighted_median_nominal_12m_pct": 100*med_return,
          "gold_weighted_median_mdd_pct": 100*med_mdd,
          "gold_largest_individual_mdd_pct": 100*gold.mdd_12m.max(),
          "matched_rows": len(panel), "matched_gold_positive_corn_negative": int(
              ((panel.gold_12m_price_pct > 0) & (panel.corn_12m_price_pct < 0)).sum()),
          "limitations": ["post-1994 subgroup is diagnostic and only five independent broad episodes",
                          "index/futures/commodity spot metrics are not directly tradable",
                          "no publication-time OOS net-cost gold-vs-corn trade test"]}
    (OUT / "QC.json").write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n")
    print(qc)
    print(panel.to_string(index=False))


if __name__ == "__main__":
    main()
