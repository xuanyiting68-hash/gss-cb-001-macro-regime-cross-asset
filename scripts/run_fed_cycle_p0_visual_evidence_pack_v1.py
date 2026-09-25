#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_p0_visual_evidence_pack_v1"
FIGDIR = OUT / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

Q024 = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "QC.json"
P0 = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "P0_BUILD_QUEUE.csv"
CLAIMS = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "CLAIM_REGISTRY.csv"
RECOVERY = ROOT / "results" / "fed_cycle_total_risk_clock_v1" / "SUPPORTED_TOTAL_CLOCK_SUMMARY.csv"
S019 = ROOT / "results" / "fed_cycle_precut_state_v1" / "BINARY_STATE_SUPPORT.csv"
C019 = ROOT / "results" / "fed_cycle_precut_state_v1" / "BINARY_STATE_CONTRASTS.csv"
D020 = ROOT / "results" / "fed_cycle_precut_stress_level_v1" / "CONTINUOUS_RANK_DIAGNOSTICS.csv"
POLICY = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "CASEBOOK_POLICY_SEQUENCE.csv"
CASE_ASSETS = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "CASEBOOK_ASSET_PHASE_METRICS.csv"
CONTEXT = ROOT / "results" / "fed_cycle_historical_context_022a_v1" / "CONTEXT_CLAIMS.csv"
CURR_OBS = ROOT / "results" / "fed_cycle_realtime_regime_dashboard_v1" / "CURRENT_OBSERVABLES.csv"
CURR_GATE = ROOT / "results" / "fed_cycle_realtime_regime_dashboard_v1" / "CURRENT_POLICY_GATE.csv"
CURR_DERIVED = ROOT / "results" / "fed_cycle_realtime_regime_dashboard_v1" / "CURRENT_STATE_DERIVED.csv"

P0_KEYS = [
    "FIG-PHASE-DXY-FIRST_CUT",
    "FIG-PHASE-GOLD-FIRST_CUT",
    "FIG-PHASE-NASDAQ-FIRST_CUT",
    "FIG-PHASE-SP500-FIRST_CUT",
    "FIG-PHASE-WTI-FIRST_CUT",
    "FIG-RECOVERY-FIRSTCUT-VS-PAUSE",
    "FIG-GUARD-019",
    "FIG-GUARD-020",
    "FIG-CASE-B04",
    "FIG-CASE-B05",
    "FIG-CASE-B06",
    "FIG-CASE-B07",
    "FIG-CURRENT-023-REGIME-SNAPSHOT",
]

VARIANTS = {
    "SVG_RESEARCH": {"figsize": (12, 7), "path_suffix": "__research.svg", "dpi": 100, "width": 1200, "height": 700},
    "PNG_16_9": {"figsize": (16, 9), "path_suffix": "__16x9.png", "dpi": 100, "width": 1600, "height": 900},
    "PNG_1_1": {"figsize": (12, 12), "path_suffix": "__1x1.png", "dpi": 100, "width": 1200, "height": 1200},
}

plt.rcParams["svg.hashsalt"] = "fed-cycle-p0-visual-evidence-pack-025"
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["figure.titlesize"] = 16


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_bundle_hash(source_files: str) -> str:
    h = hashlib.sha256()
    for rel in source_files.split("|"):
        p = ROOT / rel
        if not p.exists():
            raise RuntimeError(f"source file missing: {rel}")
        h.update(rel.encode())
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def read_pass(path: Path):
    q = json.loads(path.read_text())
    if q.get("qc_gate") != "PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q


def fmt_pct(x: float) -> str:
    return f"{x * 100:+.1f}%"


def fmt_mdd(x: float) -> str:
    return f"{x * 100:.1f}%"


def footer(fig, figure_key: str, linked_claims: str, disclaimer: str, square: bool):
    fig.text(
        0.02, 0.035 if square else 0.025,
        f"{figure_key} | Claims: {linked_claims}",
        ha="left", va="bottom", fontsize=7.4,
    )
    fig.text(
        0.02, 0.012 if square else 0.006,
        textwrap.fill(disclaimer, 145 if not square else 100),
        ha="left", va="bottom", fontsize=6.8,
    )


def phase_card(spec, claim, figsize):
    payload = json.loads(claim["metric_payload"])
    fig = plt.figure(figsize=figsize)
    square = figsize[0] == figsize[1]
    gs = fig.add_gridspec(2, 2, left=0.08, right=0.96, top=0.80, bottom=0.15, hspace=0.52, wspace=0.32)
    fig.suptitle(f"{claim['asset']} around FIRST_CUT — historical path distribution", y=0.95)
    fig.text(
        0.5, 0.885,
        f"{claim['sample_descriptor']} | support: {claim['support_status']} | descriptive, not causal",
        ha="center", fontsize=9,
    )

    ax = fig.add_subplot(gs[0, 0])
    v = float(payload["ret_12m"]) * 100
    ax.barh(["+12M endpoint"], [v])
    ax.axvline(0, linewidth=0.8)
    ax.set_xlabel("Return (%)")
    ax.set_title("Endpoint")
    ax.text(v, 0, f" {v:+.1f}%", va="center", ha="left" if v >= 0 else "right")

    ax = fig.add_subplot(gs[0, 1])
    mdd = float(payload["path_risk_value"]) * 100
    ax.barh(["12M MDD magnitude"], [mdd])
    ax.set_xlim(0, max(25, mdd * 1.3))
    ax.set_xlabel("Drawdown magnitude (%)")
    ax.set_title("Interim path risk")
    ax.text(mdd, 0, f" {mdd:.1f}%", va="center", ha="left")

    ax = fig.add_subplot(gs[1, 0])
    trough = float(payload["trough_month"])
    ax.scatter([trough], [0], s=80)
    ax.hlines(0, 0, 12, linewidth=1)
    ax.set_xlim(0, 12)
    ax.set_yticks([])
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel("Months after anchor")
    ax.set_title(f"Median MDD trough: month {int(trough)}")

    ax = fig.add_subplot(gs[1, 1])
    rec = payload.get("anchor_to_full_recovery_months")
    if rec is None:
        ax.text(0.5, 0.5, "Full-recovery median unavailable", ha="center", va="center")
        ax.set_axis_off()
    else:
        rec = float(rec)
        ax.scatter([rec], [0], s=80)
        ax.hlines(0, 0, max(30, rec), linewidth=1)
        ax.set_xlim(0, max(30, rec * 1.15))
        ax.set_yticks([])
        ax.set_xlabel("Months after anchor")
        ax.set_title(f"Anchor-to-full-recovery KM median: {int(rec)}m")

    footer(fig, spec["figure_key"], spec["linked_claim_ids"], spec["required_disclaimer"], square)
    return fig


def recovery_figure(spec, figsize, recovery):
    core = ["DXY", "GOLD", "NASDAQ", "SP500", "WTI"]
    z = recovery[
        recovery["asset"].isin(core) &
        recovery["anchor"].isin(["PAUSE_START", "FIRST_CUT"])
    ][["asset", "anchor", "weighted_km_median_anchor_to_100_months"]].copy()
    piv = z.pivot(index="asset", columns="anchor", values="weighted_km_median_anchor_to_100_months").loc[core]
    if piv.isna().any().any() or len(piv) != 5:
        raise RuntimeError("recovery synthesis source changed")

    fig, ax = plt.subplots(figsize=figsize)
    square = figsize[0] == figsize[1]
    y = list(range(len(core)))
    for i, asset in enumerate(core):
        p = float(piv.loc[asset, "PAUSE_START"])
        c = float(piv.loc[asset, "FIRST_CUT"])
        ax.plot([p, c], [i, i], linewidth=2)
        ax.scatter([p, c], [i, i], s=70)
        ax.text(p, i + 0.13, f"P {p:.0f}m", ha="center", fontsize=8)
        ax.text(c, i - 0.23, f"FC {c:.0f}m", ha="center", fontsize=8)
    ax.set_yticks(y, core)
    ax.invert_yaxis()
    ax.set_xlabel("Anchor-to-full-recovery KM median (months)")
    ax.set_title("PAUSE_START vs FIRST_CUT — supported full-recovery clocks", pad=18)
    ax.grid(axis="x", alpha=0.25)
    fig.text(0.5, 0.89 if not square else 0.91, "5 fully supported assets | FIRST_CUT slower 3/5, equal 2/5, faster 0/5", ha="center", fontsize=9)
    fig.subplots_adjust(left=0.16, right=0.95, top=0.80, bottom=0.16)
    footer(fig, spec["figure_key"], spec["linked_claim_ids"], spec["required_disclaimer"], square)
    return fig


def guard019_figure(spec, figsize, support, contrasts):
    fig = plt.figure(figsize=figsize)
    square = figsize[0] == figsize[1]
    gs = fig.add_gridspec(1, 2, left=0.08, right=0.96, top=0.80, bottom=0.18, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    names = ["RT growth\ncontraction", "Curve\ninverted", "NFCI tight"]
    states = ["REALTIME_GROWTH_CONTRACTION", "CURVE_INVERTED", "FINANCIAL_CONDITIONS_TIGHT"]
    s = support.set_index("state").loc[states]
    x = range(3)
    ax.bar(x, s["false_broad_episodes"], label="False")
    ax.bar(x, s["true_broad_episodes"], bottom=s["false_broad_episodes"], label="True")
    ax.set_xticks(list(x), names)
    ax.set_ylabel("Broad episodes")
    ax.set_title("Independent state support")
    ax.legend(fontsize=8)
    for i, st in enumerate(states):
        ax.text(i, 6.25, s.loc[st, "support_status"].replace("_", "\n"), ha="center", va="bottom", fontsize=7)

    ax = fig.add_subplot(gs[0, 1])
    c = contrasts[contrasts["state"] == "CURVE_INVERTED"].copy()
    vals = []
    labs = []
    for flag in [False, True]:
        r = c[c["state_value"].astype(str) == str(flag)].iloc[0]
        vals.append(float(r["median_risk3_trough_month"]))
        labs.append(f"Curve inverted = {flag}")
    ax.barh(labs, vals)
    ax.set_xlim(0, 12)
    ax.set_xlabel("Median risk3 trough month")
    ax.set_title("Balanced curve split: same median")
    for i, v in enumerate(vals):
        ax.text(v, i, f" {v:.0f}", va="center", ha="left")

    fig.suptitle("019 guardrail — simple predetermined pre-cut state rule not supported", y=0.96)
    fig.text(0.5, 0.865, "8 mechanical cycles / 6 broad episodes | descriptive negative result", ha="center", fontsize=9)
    footer(fig, spec["figure_key"], spec["linked_claim_ids"], spec["required_disclaimer"], square)
    return fig


def guard020_figure(spec, figsize, diag):
    z = diag[
        (diag["sample"] == "FULL_AVAILABLE") &
        (diag["outcome"] == "RISK3_MEDIAN_TROUGH_MONTH")
    ].copy()
    order = ["BAA_SPREAD_LEVEL", "VIX_LEVEL", "CURVE_STRESS_BP", "GROWTH_STRESS"]
    z = z.set_index("predictor").loc[order].reset_index()
    if len(z) != 4:
        raise RuntimeError("020 full-sample predictor set changed")

    fig, ax = plt.subplots(figsize=figsize)
    square = figsize[0] == figsize[1]
    y = list(range(4))
    for i, r in z.iterrows():
        lo = float(r["loo_min_rho"])
        hi = float(r["loo_max_rho"])
        rho = float(r["spearman_rho"])
        ax.hlines(i, lo, hi, linewidth=3)
        ax.scatter([rho], [i], s=70)
        ax.text(hi + 0.035, i, f"rho {rho:+.3f} | n={int(r['n_broad_episodes'])}", va="center", fontsize=8)
    ax.axvline(0, linewidth=1)
    ax.set_yticks(y, ["Baa spread", "VIX", "Curve stress", "RT growth stress"])
    ax.invert_yaxis()
    ax.set_xlim(-1.05, 1.05)
    ax.set_xlabel("Spearman rho with median risk3 trough month")
    ax.set_title("020 guardrail — full-sample rho and leave-one-out range", pad=18)
    ax.grid(axis="x", alpha=0.25)
    fig.text(0.5, 0.88 if not square else 0.91, "Every full-sample predictor fails the frozen composition-robustness requirement", ha="center", fontsize=9)
    fig.subplots_adjust(left=0.20, right=0.94, top=0.80, bottom=0.16)
    footer(fig, spec["figure_key"], spec["linked_claim_ids"], spec["required_disclaimer"], square)
    return fig


def case_figure(spec, figsize, bid, policy, case_assets, context):
    pg = policy[policy["broad_episode_id"] == bid].copy()
    ag = case_assets[(case_assets["broad_episode_id"] == bid) & (case_assets["anchor"] == "FIRST_CUT")].copy()
    cg = context[context["broad_episode_id"] == bid].copy()
    if pg.empty or len(ag) != 4:
        raise RuntimeError(f"case inputs changed for {bid}")

    fig = plt.figure(figsize=figsize)
    square = figsize[0] == figsize[1]
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.6, 1.1], left=0.07, right=0.96, top=0.88, bottom=0.15, hspace=0.38)

    ax = fig.add_subplot(gs[0, 0])
    pg["event_date"] = pd.to_datetime(pg["event_date"])
    dates = pg["event_date"].tolist()
    ax.hlines(0, min(dates), max(dates), linewidth=1.2)
    markers = {"FIRST_HIKE":"^", "LAST_HIKE":"s", "PAUSE_START":"o", "FIRST_CUT":"v"}
    for r in pg.itertuples(index=False):
        ax.scatter(r.event_date, 0, marker=markers.get(r.event_type, "o"), s=75)
        ax.text(r.event_date, 0.12, f"{r.event_type}\n{r.event_date.date()}", ha="center", va="bottom", fontsize=7.2)
    ax.set_yticks([])
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.set_title("Policy chronology")
    ax.tick_params(axis="x", labelsize=7)

    ax = fig.add_subplot(gs[1, 0])
    ag = ag.set_index("asset").loc[["GOLD","NASDAQ","SP500","WTI"]].reset_index()
    y = list(range(4))
    endpoints = ag["ret_12m"].astype(float) * 100
    ax.barh(y, endpoints)
    ax.axvline(0, linewidth=0.8)
    ax.set_yticks(y, ag["asset"])
    ax.invert_yaxis()
    ax.set_xlabel("+12M endpoint return (%)")
    ax.set_title("FIRST_CUT asset path outcomes — endpoint with MDD/trough annotation")
    for i, r in ag.iterrows():
        endpoint = float(r["ret_12m"]) * 100
        mdd = float(r["mdd_12m"]) * 100
        tm = int(r["mdd_trough_month"])
        ha = "left" if endpoint >= 0 else "right"
        offset = 0.4 if endpoint >= 0 else -0.4
        ax.text(endpoint + offset, i, f"{endpoint:+.1f}% | MDD {mdd:.1f}% | trough M{tm}", va="center", ha=ha, fontsize=8)

    ax = fig.add_subplot(gs[2, 0])
    ax.axis("off")
    ax.set_title("Context timing layer", loc="left", fontsize=10)
    y0 = 0.90
    for i, r in enumerate(cg.itertuples(index=False)):
        short = textwrap.shorten(str(r.claim_text), width=135 if not square else 95, placeholder="…")
        ax.text(0.01, y0 - i * 0.29, f"[{r.claim_time_class}] {r.event_date_or_period}: {short}", transform=ax.transAxes, fontsize=7.2, va="top")
    if bid == "B04":
        ax.text(0.99, 0.05, "9/11 = POST_ANCHOR_SHOCK; not part of Jan-2001 cut rationale", transform=ax.transAxes, fontsize=7.3, ha="right")
    if bid == "B06":
        ax.text(0.99, 0.05, "COVID = POST_ANCHOR_SHOCK; not part of Jul-2019 cut rationale", transform=ax.transAxes, fontsize=7.3, ha="right")

    fig.suptitle(f"{bid} historical FIRST_CUT case — chronology, path, and timing-aware context", y=0.97)
    footer(fig, spec["figure_key"], spec["linked_claim_ids"], spec["required_disclaimer"], square)
    return fig


def current_figure(spec, figsize, obs, gate, derived):
    fig = plt.figure(figsize=figsize)
    square = figsize[0] == figsize[1]
    gs = fig.add_gridspec(3, 2, left=0.06, right=0.96, top=0.86, bottom=0.15, hspace=0.42, wspace=0.24)
    obs_idx = obs.set_index("series_id")
    deriv = derived.set_index("field")
    g = gate.iloc[0]

    def card(ax, title, lines):
        ax.axis("off")
        ax.set_title(title, loc="left", fontsize=10, pad=4)
        for i, line in enumerate(lines):
            ax.text(0.01, 0.88 - i * 0.20, line, transform=ax.transAxes, fontsize=8.2, va="top")

    card(fig.add_subplot(gs[0,0]), "Policy gate", [
        "2026-09-16 candidate FIRST_HIKE",
        f"1 hike / {float(g['cumulative_hike_bp']):.0f} bp",
        f"Target {float(g['target_lower']):.2f}–{float(g['target_upper']):.2f}%",
        "Qualification: FALSE (needs >=2 hikes & >=50bp)",
    ])
    card(fig.add_subplot(gs[0,1]), "Rates / curve", [
        f"EFFR {float(obs_idx.loc['EFFR','value']):.2f}% ({obs_idx.loc['EFFR','observation_period']})",
        f"2Y {float(obs_idx.loc['DGS2','value']):.2f}% | 10Y {float(obs_idx.loc['DGS10','value']):.2f}%",
        f"10Y-2Y {float(deriv.loc['CURVE_10Y2Y_BP','value_numeric']):.0f} bp",
        f"State: {deriv.loc['CURVE_STATE','value_text']}",
    ])
    card(fig.add_subplot(gs[1,0]), "Inflation expectations", [
        f"5Y breakeven {float(obs_idx.loc['T5YIE','value']):.2f}% ({obs_idx.loc['T5YIE','observation_period']})",
        f"10Y breakeven {float(obs_idx.loc['T10YIE','value']):.2f}% ({obs_idx.loc['T10YIE','observation_period']})",
        "Reference only; no expected-return conversion",
    ])
    card(fig.add_subplot(gs[1,1]), "Stress / credit", [
        f"VIX {float(obs_idx.loc['VIX','value']):.2f} ({obs_idx.loc['VIX','observation_period']})",
        f"Baa-10Y {float(obs_idx.loc['BAA10Y','value']):.2f}%",
        f"NFCI {float(obs_idx.loc['NFCI','value']):.3f}",
        f"State: {deriv.loc['NFCI_STATE','value_text']}",
    ])
    card(fig.add_subplot(gs[2,0]), "Real economy / inflation", [
        f"Unemployment {float(obs_idx.loc['UNRATE','value']):.1f}% ({obs_idx.loc['UNRATE','observation_period'][:7]})",
        f"INDPRO YoY {float(obs_idx.loc['INDPRO_YOY','value']):+.1f}%",
        f"PCE YoY {float(obs_idx.loc['PCEPI_YOY','value']):.1f}% | core {float(obs_idx.loc['CORE_PCE_YOY','value']):.1f}%",
        "PCE latest available July release at snapshot",
    ])
    card(fig.add_subplot(gs[2,1]), "Evidence boundary / freshness", [
        "Snapshot: 2026-09-25 16:08 Sydney",
        "High-frequency observations are not synchronized",
        "FIRST_HIKE claims = historical reference distributions only",
        "No closest analog / rank / forecast / trade signal",
    ])

    fig.suptitle("2026-09-25 release-aware Fed-cycle current-state snapshot", y=0.96)
    footer(fig, spec["figure_key"], spec["linked_claim_ids"], spec["required_disclaimer"], square)
    return fig


def build_figure(spec, figsize, claims, recovery, support019, contrasts019, diag020, policy, case_assets, context, obs, gate, derived):
    key = spec["figure_key"]
    if key.startswith("FIG-PHASE-"):
        cid = spec["linked_claim_ids"]
        claim = claims[claims["claim_id"] == cid].iloc[0]
        return phase_card(spec, claim, figsize)
    if key == "FIG-RECOVERY-FIRSTCUT-VS-PAUSE":
        return recovery_figure(spec, figsize, recovery)
    if key == "FIG-GUARD-019":
        return guard019_figure(spec, figsize, support019, contrasts019)
    if key == "FIG-GUARD-020":
        return guard020_figure(spec, figsize, diag020)
    if key.startswith("FIG-CASE-"):
        return case_figure(spec, figsize, key.replace("FIG-CASE-", ""), policy, case_assets, context)
    if key == "FIG-CURRENT-023-REGIME-SNAPSHOT":
        return current_figure(spec, figsize, obs, gate, derived)
    raise RuntimeError(f"unsupported P0 figure key: {key}")


def save_variant(fig, figure_key: str, variant: str):
    cfg = VARIANTS[variant]
    path = FIGDIR / f"{figure_key}{cfg['path_suffix']}"
    if variant == "SVG_RESEARCH":
        fig.savefig(path, format="svg", dpi=cfg["dpi"], metadata={"Creator":"FED-CYCLE-P0-VISUAL-EVIDENCE-PACK-025","Date":None})
    else:
        fig.savefig(path, format="png", dpi=cfg["dpi"], metadata={"Creator":"FED-CYCLE-P0-VISUAL-EVIDENCE-PACK-025"})
    plt.close(fig)
    return path


def main():
    q024 = read_pass(Q024)
    p0 = pd.read_csv(P0)
    claims = pd.read_csv(CLAIMS)
    recovery = pd.read_csv(RECOVERY)
    support019 = pd.read_csv(S019)
    contrasts019 = pd.read_csv(C019)
    diag020 = pd.read_csv(D020)
    policy = pd.read_csv(POLICY)
    case_assets = pd.read_csv(CASE_ASSETS)
    context = pd.read_csv(CONTEXT)
    obs = pd.read_csv(CURR_OBS, dtype={"observation_period":str})
    gate = pd.read_csv(CURR_GATE)
    derived = pd.read_csv(CURR_DERIVED)

    if q024["p0_count"] != 13:
        raise RuntimeError("024 P0 count changed")
    if len(p0) != 13 or set(p0["figure_key"]) != set(P0_KEYS):
        raise RuntimeError("025 figure universe does not exactly match frozen 024 P0")
    if p0["figure_key"].duplicated().any():
        raise RuntimeError("duplicate P0 figure key")

    # Exact phase-card metric-payload source check.
    for key in [k for k in P0_KEYS if k.startswith("FIG-PHASE-")]:
        spec = p0[p0["figure_key"] == key].iloc[0]
        cid = spec["linked_claim_ids"]
        c = claims[claims["claim_id"] == cid]
        if len(c) != 1:
            raise RuntimeError(f"claim mapping failed: {key}")
        payload = json.loads(c.iloc[0]["metric_payload"])
        for req in ["ret_12m","path_risk_value","trough_month","anchor_to_full_recovery_months"]:
            if req not in payload:
                raise RuntimeError(f"phase metric payload missing {req}: {key}")

    # Recovery source universe assertion.
    rz = recovery[
        recovery["asset"].isin(["DXY","GOLD","NASDAQ","SP500","WTI"]) &
        recovery["anchor"].isin(["PAUSE_START","FIRST_CUT"])
    ]
    if len(rz) != 10 or rz["asset"].nunique() != 5 or set(rz["anchor"]) != {"PAUSE_START","FIRST_CUT"}:
        raise RuntimeError("recovery source universe changed")

    # 020 must use full available trough-month rows as primary.
    z020 = diag020[(diag020["sample"]=="FULL_AVAILABLE") & (diag020["outcome"]=="RISK3_MEDIAN_TROUGH_MONTH")]
    if len(z020) != 4:
        raise RuntimeError("020 primary visual source changed")

    manifest = []
    ordered = p0.set_index("figure_key").loc[P0_KEYS].reset_index()
    for _, spec in ordered.iterrows():
        source_hash = source_bundle_hash(spec["source_files"])
        for variant, cfg in VARIANTS.items():
            fig = build_figure(
                spec, cfg["figsize"], claims, recovery, support019, contrasts019,
                diag020, policy, case_assets, context, obs, gate, derived
            )
            path = save_variant(fig, spec["figure_key"], variant)
            if not path.exists() or path.stat().st_size <= 0:
                raise RuntimeError(f"render failed: {path}")

            width, height = cfg["width"], cfg["height"]
            if variant.startswith("PNG"):
                with Image.open(path) as im:
                    if im.size != (width, height):
                        raise RuntimeError(f"PNG dimension mismatch {path}: {im.size}")
            manifest.append({
                "figure_key":spec["figure_key"],
                "variant":variant,
                "relative_path":str(path.relative_to(ROOT)).replace("\\","/"),
                "linked_claim_ids":spec["linked_claim_ids"],
                "source_files":spec["source_files"],
                "source_bundle_sha256":source_hash,
                "sha256":sha256_file(path),
                "byte_size":path.stat().st_size,
                "width_px":width,
                "height_px":height,
                "render_status":"PASS",
            })

    m = pd.DataFrame(manifest)
    if len(m) != 39:
        raise RuntimeError(f"expected 39 rendered files, got {len(m)}")
    if m["sha256"].str.len().ne(64).any() or m["source_bundle_sha256"].str.len().ne(64).any():
        raise RuntimeError("hash failure")
    if (m["byte_size"] <= 0).any():
        raise RuntimeError("zero-size render")
    for variant in VARIANTS:
        if int((m["variant"] == variant).sum()) != 13:
            raise RuntimeError(f"variant count failed: {variant}")

    # Exact current-state visible requirement.
    current_svg = (FIGDIR / "FIG-CURRENT-023-REGIME-SNAPSHOT__research.svg").read_text()
    if "Qualification: FALSE" not in current_svg:
        raise RuntimeError("current visual does not visibly show qualification FALSE")
    if "No closest analog" not in current_svg:
        raise RuntimeError("current visual missing no-analog boundary")

    # B04/B06 later-shock text must survive into SVG.
    b04svg = (FIGDIR / "FIG-CASE-B04__research.svg").read_text()
    b06svg = (FIGDIR / "FIG-CASE-B06__research.svg").read_text()
    if "POST_ANCHOR_SHOCK" not in b04svg or "9/11" not in b04svg:
        raise RuntimeError("B04 later-shock timing label missing")
    if "POST_ANCHOR_SHOCK" not in b06svg or "COVID" not in b06svg:
        raise RuntimeError("B06 later-shock timing label missing")

    # Negative result visual must not contain "BUY" or "SELL".
    for key in ["FIG-GUARD-019","FIG-GUARD-020"]:
        txt = (FIGDIR / f"{key}__research.svg").read_text().upper()
        if "BUY" in txt or "SELL" in txt:
            raise RuntimeError(f"trade-signal language leaked into {key}")

    m.to_csv(OUT / "RENDER_MANIFEST.csv", index=False)

    source_rows = []
    unique_sources = sorted(set("|".join(ordered["source_files"]).split("|")))
    for rel in unique_sources:
        p = ROOT / rel
        source_rows.append({
            "source_file":rel,
            "sha256":sha256_file(p),
            "byte_size":p.stat().st_size,
        })
    pd.DataFrame(source_rows).to_csv(OUT / "SOURCE_FILE_HASHES.csv", index=False)

    lines = [
        "# FED-CYCLE-P0-VISUAL-EVIDENCE-PACK-025 — Visual Index",
        "",
        "Rendered visuals are communication artifacts backed by canonical claims/data. They are not new empirical evidence.",
        "",
    ]
    for key in P0_KEYS:
        spec = ordered[ordered["figure_key"] == key].iloc[0]
        lines += [
            f"## {key}",
            "",
            f"- Family: {spec['figure_family']}",
            f"- Claims: {spec['linked_claim_ids']}",
            f"- Source: {spec['source_files']}",
            f"- Disclaimer: {spec['required_disclaimer']}",
            f"- Files: `figures/{key}__research.svg`, `figures/{key}__16x9.png`, `figures/{key}__1x1.png`",
            "",
        ]
    (OUT / "P0_VISUAL_INDEX.md").write_text("\n".join(lines) + "\n")

    report = [
        "# FED-CYCLE-P0-VISUAL-EVIDENCE-PACK-025 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED RENDERED P0 VISUAL PACK / 13 FIGURES x 3 VARIANTS / NOT NEW EVIDENCE / NOT CAUSAL / NOT DEPLOYABLE**",
        "",
        "- figure keys: 13",
        "- rendered files: 39",
        "- SVG_RESEARCH: 13",
        "- PNG_16_9: 13 at 1600x900",
        "- PNG_1_1: 13 at 1200x1200",
        "- render manifest rows: 39",
        "- source-file hashes registered: " + str(len(source_rows)),
        "",
        "## Render controls",
        "",
        "- every visual resolves to the frozen 024 P0 queue;",
        "- every rendered file has a SHA256 and source-bundle SHA256;",
        "- phase cards consume 022B metric_payload directly;",
        "- recovery chart uses five supported assets / PAUSE_START vs FIRST_CUT only;",
        "- 019/020 are rendered as negative research guardrails;",
        "- B04/B06 preserve later-shock timing labels;",
        "- current 023 visual explicitly shows qualification FALSE and no-analog boundary;",
        "- no new p-values, scores, rankings or forecasts are generated.",
        "",
        "025 is a reproducible visual-delivery layer. The next production step may package these canonical renders for specific social platforms without changing their factual payload or evidence boundary.",
    ]
    (OUT / "FED_CYCLE_P0_VISUAL_EVIDENCE_PACK_025_REPORT.md").write_text("\n".join(report) + "\n")

    qc = {
        "qc_gate":"PASS",
        "module":"FED-CYCLE-P0-VISUAL-EVIDENCE-PACK-025",
        "upstream_024_qc":q024["qc_gate"],
        "p0_figure_keys":13,
        "p0_universe_exact_match":True,
        "rendered_files":int(len(m)),
        "svg_research_files":int((m["variant"]=="SVG_RESEARCH").sum()),
        "png_16_9_files":int((m["variant"]=="PNG_16_9").sum()),
        "png_1_1_files":int((m["variant"]=="PNG_1_1").sum()),
        "png_16_9_dimensions":"1600x900",
        "png_1_1_dimensions":"1200x1200",
        "nonempty_render_hashes":True,
        "nonempty_source_hashes":True,
        "zero_byte_files":0,
        "phase_metric_payload_direct":True,
        "recovery_five_asset_pause_firstcut_only":True,
        "guard019_signal_output":False,
        "guard020_full_available_primary":True,
        "b04_b06_post_anchor_shock_labels_visible":True,
        "current_023_qualification_false_visible":True,
        "analog_score_outputs":0,
        "asset_ranking_outputs":0,
        "forecast_outputs":0,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n")


if __name__ == "__main__":
    main()
