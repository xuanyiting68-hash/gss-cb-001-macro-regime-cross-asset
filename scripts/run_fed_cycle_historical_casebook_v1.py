#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_historical_casebook_v1"
OUT.mkdir(parents=True, exist_ok=True)

EPISODES = {
    "B02": {"label": "1987-1989 tightening/easing sequence", "structure": "COMPOSITE_MULTI_LEG"},
    "B03": {"label": "1994-1995 tightening/easing cycle", "structure": "SINGLE_MECHANICAL_CYCLE"},
    "B04": {"label": "1999-2001 tightening/easing cycle", "structure": "SINGLE_MECHANICAL_CYCLE"},
    "B05": {"label": "2004-2007 tightening/easing cycle", "structure": "SINGLE_MECHANICAL_CYCLE"},
    "B06": {"label": "2015-2019 tightening/easing cycle", "structure": "SINGLE_MECHANICAL_CYCLE"},
    "B07": {"label": "2022-2024 tightening/easing cycle", "structure": "SINGLE_MECHANICAL_CYCLE"},
}
EP_IDS = list(EPISODES)
ASSETS = ["GOLD", "SP500", "NASDAQ", "WTI"]
PHASES = ["FIRST_HIKE", "LAST_HIKE", "PAUSE_START", "FIRST_CUT"]

CYCLES = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_TIGHTENING_CYCLES.csv"
EVENTS = ROOT / "results" / "fed_cycle_path_v1_1" / "FED_CYCLE_EVENTS.csv"
Q001 = ROOT / "results" / "fed_cycle_path_v1_1" / "QC.json"
PHASE_METRICS = ROOT / "results" / "fed_cycle_phase_clock_v1" / "PHASE_CYCLE_ASSET_METRICS.csv"
Q004 = ROOT / "results" / "fed_cycle_phase_clock_v1" / "QC.json"
STRESS_METRICS = ROOT / "results" / "fed_cycle_stress_layer_v1" / "STRESS_CYCLE_PHASE_METRICS.csv"
Q005 = ROOT / "results" / "fed_cycle_stress_layer_v1" / "QC.json"
PAIR = ROOT / "results" / "fed_cycle_stress_trough_alignment_v1" / "PAIR_TIMING_PANEL.csv"
Q018 = ROOT / "results" / "fed_cycle_stress_trough_alignment_v1" / "QC.json"
PRECUT = ROOT / "results" / "fed_cycle_precut_state_v1" / "PRECUT_STATE_CYCLE_PANEL.csv"
Q019 = ROOT / "results" / "fed_cycle_precut_state_v1" / "QC.json"
RATES = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "RATE_PHASE_METRICS.csv"
CASH = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "CASH_PHASE_METRICS.csv"
Q014 = ROOT / "results" / "fed_cycle_cross_asset_expansion_v1" / "QC.json"

UPSTREAM_QC = [Q001, Q004, Q005, Q018, Q019, Q014]


def read_qc():
    out = []
    for p in UPSTREAM_QC:
        q = json.loads(p.read_text())
        if q.get("qc_gate") != "PASS":
            raise RuntimeError(f"Upstream QC not PASS: {p}")
        out.append(q.get("module") or q.get("version") or p.parent.name)
    return out


def common_meta(df: pd.DataFrame, evidence_time: str, source_module: str) -> pd.DataFrame:
    z = df.copy()
    z["evidence_time"] = evidence_time
    z["source_module_casebook"] = source_module
    z["causal_status"] = "NONE"
    z["oos_status"] = "NOT_A_FORECASTING_MODEL"
    z["deployment_status"] = "NOT_DEPLOYABLE"
    return z


def build_cycle_map(phase: pd.DataFrame) -> pd.DataFrame:
    m = (
        phase[phase["broad_episode_id"].isin(EP_IDS)][["cycle_id", "broad_episode_id"]]
        .drop_duplicates()
        .sort_values(["broad_episode_id", "cycle_id"])
    )
    if m["cycle_id"].duplicated().any():
        raise RuntimeError("cycle maps to multiple broad episodes")
    return m


def build_episodes(cycles: pd.DataFrame, cycle_map: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    c = cycles.merge(cycle_map, on="cycle_id", how="inner", validate="one_to_one")
    e = events[events["cycle_id"].isin(c["cycle_id"])].copy()
    rows = []
    for bid in EP_IDS:
        g = c[c["broad_episode_id"] == bid].sort_values("first_hike")
        bases = sorted(
            e[e["cycle_id"].isin(g["cycle_id"])]["event_date_basis"].dropna().astype(str).unique()
        )
        pre1994 = any(pd.to_datetime(g["first_hike"]).dt.year < 1994)
        rows.append({
            "broad_episode_id": bid,
            "content_label": EPISODES[bid]["label"],
            "structure": EPISODES[bid]["structure"],
            "n_mechanical_cycles": int(len(g)),
            "cycle_ids": "|".join(g["cycle_id"].astype(str)),
            "episode_start": g["first_hike"].min(),
            "episode_end": g["first_cut"].max(),
            "event_date_basis_set": "|".join(bases),
            "source_era_caveat": (
                "PRE1994_HISTORICAL_TARGET_RECONSTRUCTION; preserve sub-cycle chronology"
                if pre1994 else
                "MODERN_FOMC_CHRONOLOGY; event/source-effective-date distinctions preserved upstream"
            ),
            "evidence_time": "DESCRIPTIVE_PATH",
            "causal_status": "NONE",
            "oos_status": "NOT_A_FORECASTING_MODEL",
            "deployment_status": "NOT_DEPLOYABLE",
        })
    return pd.DataFrame(rows)


def build_policy_sequence(cycles: pd.DataFrame, events: pd.DataFrame, cycle_map: pd.DataFrame) -> pd.DataFrame:
    c = cycles.merge(cycle_map, on="cycle_id", how="inner", validate="one_to_one")
    keep_events = events[
        events["cycle_id"].isin(c["cycle_id"]) & events["event_type"].isin(PHASES)
    ].copy()
    cols = [
        "cycle_id", "broad_episode_id", "n_hikes", "cumulative_hike_bp",
        "target_before_first_hike", "target_after_last_hike",
    ]
    z = keep_events.merge(c[cols], on="cycle_id", how="left", validate="many_to_one")
    z["phase_label_status"] = "RETROSPECTIVE_CYCLE_ONTOLOGY"
    z = common_meta(z, "DESCRIPTIVE_PATH", "FED-CYCLE-PATH-001-v1.1")
    return z.sort_values(["broad_episode_id", "event_date", "cycle_id", "event_type"]).reset_index(drop=True)


def build_asset_metrics(phase: pd.DataFrame) -> pd.DataFrame:
    z = phase[
        phase["broad_episode_id"].isin(EP_IDS)
        & phase["asset"].isin(ASSETS)
        & phase["anchor"].isin(PHASES)
    ].copy()
    z = common_meta(z, "DESCRIPTIVE_PATH", "PHASE-CLOCK-004")
    z["interpretation_guardrail"] = (
        "post-anchor historical path; not information available at the anchor; "
        "realized Fed phase is not an identified monetary-policy shock"
    )
    return z.sort_values(["broad_episode_id", "cycle_id", "anchor", "asset"]).reset_index(drop=True)


def build_precut(precut: pd.DataFrame) -> pd.DataFrame:
    z = precut[precut["broad_episode_id"].isin(EP_IDS)].copy()
    z = common_meta(z, "REALTIME_KNOWABLE", "PRECUT-STATE-019")
    z["timing_rule_status"] = "SIMPLE_PRECUT_TIMING_RULE_NOT_SUPPORTED"
    z["interpretation_guardrail"] = (
        "predetermined historical context only; 019/020 do not support converting these fields "
        "into a deterministic bottom-timing score"
    )
    return z.sort_values(["broad_episode_id", "first_cut", "cycle_id"]).reset_index(drop=True)


def build_expost(pair: pd.DataFrame) -> pd.DataFrame:
    z = pair[pair["broad_episode_id"].isin(EP_IDS)].copy()
    z = common_meta(z, "EXPOST_ONLY", "STRESS-TROUGH-ALIGNMENT-018")
    z["interpretation_guardrail"] = (
        "both asset trough and stress peak are future-window statistics; not a real-time signal"
    )
    return z.sort_values(
        ["broad_episode_id", "cycle_id", "asset", "stress_observable"]
    ).reset_index(drop=True)


def build_rate_cash(rates: pd.DataFrame, cash: pd.DataFrame) -> pd.DataFrame:
    rr = rates[rates["broad_episode_id"].isin(EP_IDS)].copy()
    rr = rr.rename(columns={
        "series": "series",
        "chg_3m_bp": "metric_3m",
        "chg_6m_bp": "metric_6m",
        "chg_12m_bp": "metric_12m",
        "max_increase_12m_bp": "max_increase_12m",
        "max_decrease_12m_bp": "max_decrease_12m",
    })
    rr["metric_family"] = "TREASURY_YIELD_CHANGE"
    rr["metric_unit"] = "BASIS_POINTS"
    rr["cash_avg_dff_12m"] = pd.NA
    rr["source_module"] = "CROSS-ASSET-EXPANSION-014"
    rr = rr[[
        "broad_episode_id","cycle_id","anchor","anchor_date","episode_weight",
        "series","metric_family","metric_unit","metric_3m","metric_6m","metric_12m",
        "max_increase_12m","max_decrease_12m","cash_avg_dff_12m","source_module"
    ]]

    cc = cash[cash["broad_episode_id"].isin(EP_IDS)].copy()
    cc["series"] = "MECHANICAL_CASH_DFF"
    cc["metric_family"] = "CASH_CARRY"
    cc["metric_unit"] = "DECIMAL_CARRY"
    cc["metric_3m"] = cc["cash_carry_3m"]
    cc["metric_6m"] = cc["cash_carry_6m"]
    cc["metric_12m"] = cc["cash_carry_12m"]
    cc["max_increase_12m"] = pd.NA
    cc["max_decrease_12m"] = pd.NA
    cc["cash_avg_dff_12m"] = cc["avg_dff_12m"]
    cc["source_module"] = "CROSS-ASSET-EXPANSION-014"
    cc = cc[[
        "broad_episode_id","cycle_id","anchor","anchor_date","episode_weight",
        "series","metric_family","metric_unit","metric_3m","metric_6m","metric_12m",
        "max_increase_12m","max_decrease_12m","cash_avg_dff_12m","source_module"
    ]]

    z = pd.concat([rr, cc], ignore_index=True)
    z = common_meta(z, "DESCRIPTIVE_PATH", "CROSS-ASSET-EXPANSION-014")
    z["interpretation_guardrail"] = (
        "historical rate/carry path; do not directly rank against price-return metrics"
    )
    return z.sort_values(
        ["broad_episode_id","cycle_id","anchor","metric_family","series"]
    ).reset_index(drop=True)


def fmt_pct(x):
    return "NA" if pd.isna(x) else f"{100*float(x):+.1f}%"


def fmt_num(x, digits=1):
    return "NA" if pd.isna(x) else f"{float(x):.{digits}f}"


def build_briefs(episodes, policy, assets, precut, expost):
    lines = [
        "# Historical Fed Cycle Casebook — 022 Content Briefs",
        "",
        "These briefs are mechanically grounded in already-QC-passed repository evidence. "
        "They deliberately omit external news/macro narratives; those require separately sourced 022A enrichment.",
        "",
        "**Evidence-time rule:** REALTIME_KNOWABLE = available under upstream timing rules; "
        "DESCRIPTIVE_PATH = what happened after the anchor; EXPOST_ONLY = only visible after the future window unfolded.",
        "",
    ]
    for _, ep in episodes.iterrows():
        bid = ep["broad_episode_id"]
        lines += [
            f"## {bid} — {ep['content_label']}",
            "",
            f"- Structure: **{ep['structure']}**; cycles: {ep['cycle_ids']}.",
            f"- Span: {ep['episode_start']} to {ep['episode_end']}.",
            f"- Source caveat: {ep['source_era_caveat']}.",
        ]

        pg = policy[policy["broad_episode_id"] == bid]
        for cid, cg in pg.groupby("cycle_id", sort=False):
            meta = cg.iloc[0]
            seq = " -> ".join(
                f"{r.event_type} {r.event_date}" for r in cg.itertuples()
            )
            lines.append(
                f"- Policy sub-cycle {cid}: {seq}; {int(meta['n_hikes'])} hikes, "
                f"cumulative {float(meta['cumulative_hike_bp']):.1f} bp."
            )

        pc = precut[precut["broad_episode_id"] == bid]
        for r in pc.itertuples():
            lines.append(
                f"- REALTIME_KNOWABLE before FIRST_CUT {r.first_cut} ({r.cycle_id}): "
                f"10Y-2Y curve {fmt_num(r.CURVE_BP,0)} bp; NFCI {fmt_num(r.NFCI,3)}; "
                f"real-time IPT YoY {fmt_pct(r.RT_IPT_YOY)} using vintage {r.RT_IPT_VINTAGE_PERIOD}. "
                f"This context did **not** validate a deterministic timing rule in 019/020."
            )

        ag = assets[(assets["broad_episode_id"] == bid) & (assets["anchor"] == "FIRST_CUT")]
        if len(ag):
            lines.append("- DESCRIPTIVE_PATH after FIRST_CUT:")
            for cid, cg in ag.groupby("cycle_id", sort=False):
                parts = []
                for r in cg.sort_values("asset").itertuples():
                    parts.append(
                        f"{r.asset} +12M {fmt_pct(r.ret_12m)}, "
                        f"MDD {fmt_pct(r.mdd_12m)}, trough M{int(r.mdd_trough_month)}"
                    )
                lines.append(f"  - {cid}: " + "; ".join(parts) + ".")

        eg = expost[
            (expost["broad_episode_id"] == bid)
            & (expost["stress_observable"] == "VIX")
            & (expost["asset"].isin(["SP500","NASDAQ","GOLD","WTI"]))
        ]
        if len(eg):
            lines.append("- EXPOST_ONLY VIX-stress/trough timing:")
            for r in eg.sort_values(["cycle_id","asset"]).itertuples():
                lines.append(
                    f"  - {r.cycle_id} {r.asset}: asset trough M{int(r.asset_trough_month)}, "
                    f"VIX stress peak M{int(r.stress_peak_month)}, gap {int(r.abs_gap_months)}m."
                )
        else:
            lines.append("- EXPOST_ONLY VIX pairing: unavailable in the frozen stress layer for this older episode.")

        lines += [
            "- Communication boundary: describe chronology/path distributions; do not say the Fed phase caused the asset path or that this case predicts today's bottom.",
            "",
        ]
    return "\n".join(lines) + "\n"


def main():
    upstream = read_qc()
    cycles = pd.read_csv(CYCLES)
    events = pd.read_csv(EVENTS)
    phase = pd.read_csv(PHASE_METRICS)
    pair = pd.read_csv(PAIR)
    precut = pd.read_csv(PRECUT)
    rates = pd.read_csv(RATES)
    cash = pd.read_csv(CASH)

    cycle_map = build_cycle_map(phase)
    episodes = build_episodes(cycles, cycle_map, events)
    policy = build_policy_sequence(cycles, events, cycle_map)
    assets = build_asset_metrics(phase)
    pc = build_precut(precut)
    xp = build_expost(pair)
    rc = build_rate_cash(rates, cash)

    # Frozen support and structure assertions.
    if episodes["broad_episode_id"].tolist() != EP_IDS:
        raise RuntimeError("episode universe changed")
    counts = episodes.set_index("broad_episode_id")["n_mechanical_cycles"].to_dict()
    if counts.get("B02") != 3:
        raise RuntimeError("B02 must contain exactly three mechanical cycles")
    if any(counts.get(b) != 1 for b in ["B03","B04","B05","B06","B07"]):
        raise RuntimeError("B03-B07 must each contain one mechanical cycle")
    if set(assets["asset"]) != set(ASSETS):
        raise RuntimeError("asset casebook universe changed")
    if pc["evidence_time"].isna().any() or xp["evidence_time"].isna().any():
        raise RuntimeError("evidence-time taxonomy null")
    if len(pc) != 8 or pc["broad_episode_id"].nunique() != 6:
        raise RuntimeError("019 realtime casebook support frame changed")

    episodes.to_csv(OUT / "CASEBOOK_EPISODES.csv", index=False)
    policy.to_csv(OUT / "CASEBOOK_POLICY_SEQUENCE.csv", index=False)
    assets.to_csv(OUT / "CASEBOOK_ASSET_PHASE_METRICS.csv", index=False)
    pc.to_csv(OUT / "CASEBOOK_PRECUT_REALTIME_CONTEXT.csv", index=False)
    xp.to_csv(OUT / "CASEBOOK_EXPOST_STRESS_ALIGNMENT.csv", index=False)
    rc.to_csv(OUT / "CASEBOOK_RATE_CASH_CONTEXT.csv", index=False)

    briefs = build_briefs(episodes, policy, assets, pc, xp)
    (OUT / "CASEBOOK_CONTENT_BRIEFS.md").write_text(briefs)

    refs = []
    for bid in EP_IDS:
        refs.append({
            "episode": json.loads(
                episodes[episodes["broad_episode_id"] == bid].to_json(orient="records")
            )[0],
            "policy_sequence": json.loads(
                policy[policy["broad_episode_id"] == bid].to_json(orient="records")
            ),
            "asset_phase_metrics": json.loads(
                assets[assets["broad_episode_id"] == bid].to_json(orient="records")
            ),
            "precut_realtime_context": json.loads(
                pc[pc["broad_episode_id"] == bid].to_json(orient="records")
            ),
            "expost_stress_alignment": json.loads(
                xp[xp["broad_episode_id"] == bid].to_json(orient="records")
            ),
            "rate_cash_context": json.loads(
                rc[rc["broad_episode_id"] == bid].to_json(orient="records")
            ),
        })

    reference = {
        "module": "FED-CYCLE-HISTORICAL-CASEBOOK-022",
        "as_of": "2026-09-25",
        "primary_broad_episodes": EP_IDS,
        "evidence_time_taxonomy": {
            "REALTIME_KNOWABLE": "available at/before the relevant anchor under upstream timing rules",
            "DESCRIPTIVE_PATH": "historical post-anchor path / retrospective cycle chronology",
            "EXPOST_ONLY": "future-window statistic observable only after the path unfolds",
        },
        "timing_rule_guardrail": "019/020 do not support a deterministic FIRST_CUT bottom-timing rule",
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
        "episodes": refs,
    }
    (OUT / "CASEBOOK_REFERENCE.json").write_text(
        json.dumps(reference, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    )

    # Report: keep it research-facing and source-bounded.
    report = [
        "# FED-CYCLE-HISTORICAL-CASEBOOK-022 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED HISTORICAL CASEBOOK / EVIDENCE-LINKED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "022 reorganizes already-QC-passed public evidence into six historical broad-episode cases. "
        "It performs no new inference and adds no external narrative facts.",
        "",
        "## Case universe",
        "",
    ]
    for r in episodes.itertuples():
        report.append(
            f"- {r.broad_episode_id}: {r.content_label}; {r.structure}; "
            f"{r.n_mechanical_cycles} mechanical cycle(s); {r.episode_start} to {r.episode_end}."
        )
    report += [
        "",
        "## Why B02 is special",
        "",
        "B02 contains three separate mechanical tightening legs (T03_1987, T04_1987, T05_1988). "
        "022 preserves their policy anchors and outcomes separately rather than inventing one synthetic policy sequence.",
        "",
        "## Real-time versus ex-post separation",
        "",
        f"- REALTIME_KNOWABLE pre-cut context rows: {len(pc)} across {pc['broad_episode_id'].nunique()} broad episodes.",
        f"- DESCRIPTIVE_PATH asset-phase rows: {len(assets)}.",
        f"- EXPOST_ONLY stress/trough alignment rows: {len(xp)}.",
        f"- rate/cash descriptive rows: {len(rc)}.",
        "",
        "The 019/020 negative result remains binding: curve/NFCI/real-time growth context may be shown as what was visible before the first cut, but not as a validated bottom-timing model.",
        "",
        "## Content use",
        "",
        "022 supports episode timelines and fact-checked story structure. The next enrichment layer (022A) may add independently sourced historical macro/news context, but every external narrative fact must receive provenance and must not overwrite the repository-derived chronology.",
    ]
    (OUT / "FED_CYCLE_HISTORICAL_CASEBOOK_022_REPORT.md").write_text("\n".join(report) + "\n")

    qc = {
        "qc_gate": "PASS",
        "module": "FED-CYCLE-HISTORICAL-CASEBOOK-022",
        "upstream_qc_modules": upstream,
        "new_price_estimation": False,
        "new_inference": False,
        "pvalues_generated": False,
        "primary_broad_episodes": EP_IDS,
        "n_primary_broad_episodes": int(len(episodes)),
        "b02_mechanical_cycles": int(counts["B02"]),
        "b03_b07_single_cycle_violations": int(sum(counts[b] != 1 for b in ["B03","B04","B05","B06","B07"])),
        "policy_sequence_rows": int(len(policy)),
        "asset_phase_rows": int(len(assets)),
        "precut_realtime_rows": int(len(pc)),
        "expost_alignment_rows": int(len(xp)),
        "rate_cash_rows": int(len(rc)),
        "evidence_time_nulls": int(
            episodes["evidence_time"].isna().sum()
            + policy["evidence_time"].isna().sum()
            + assets["evidence_time"].isna().sum()
            + pc["evidence_time"].isna().sum()
            + xp["evidence_time"].isna().sum()
            + rc["evidence_time"].isna().sum()
        ),
        "private_paper_inputs_used": False,
        "timing_rule_guardrail_preserved": True,
        "causal_status": "NONE",
        "oos_status": "NOT_A_FORECASTING_MODEL",
        "deployment_status": "NOT_DEPLOYABLE",
    }
    (OUT / "QC.json").write_text(json.dumps(qc, indent=2) + "\n")


if __name__ == "__main__":
    main()
