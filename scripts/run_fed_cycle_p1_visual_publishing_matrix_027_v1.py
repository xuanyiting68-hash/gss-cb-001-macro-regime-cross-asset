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
from PIL import Image, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_p1_visual_publishing_matrix_027_v1"
FIGDIR = OUT / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

Q024 = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "QC.json"
FIGREG = ROOT / "results" / "fed_cycle_figure_registry_024_v1" / "FIGURE_REGISTRY.csv"
Q025 = ROOT / "results" / "fed_cycle_p0_visual_evidence_pack_v1" / "QC.json"
R025 = ROOT / "results" / "fed_cycle_p0_visual_evidence_pack_v1" / "RENDER_MANIFEST.csv"
Q026 = ROOT / "results" / "fed_cycle_content_production_library_026_v1" / "QC.json"
CONTENT = ROOT / "results" / "fed_cycle_content_production_library_026_v1" / "CONTENT_OBJECTS.csv"
CLAIMS = ROOT / "results" / "fed_cycle_content_claim_registry_022b_v1" / "CLAIM_REGISTRY.csv"
POLICY = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "CASEBOOK_POLICY_SEQUENCE.csv"
CASE_ASSETS = ROOT / "results" / "fed_cycle_historical_casebook_v1" / "CASEBOOK_ASSET_PHASE_METRICS.csv"
CONTEXT = ROOT / "results" / "fed_cycle_historical_context_022a_v1" / "CONTEXT_CLAIMS.csv"

P1_KEYS = [
    "FIG-CASE-B02",
    "FIG-CASE-B03",
    "FIG-CTX-B04_CTX_02",
    "FIG-CTX-B04_CTX_03",
    "FIG-CTX-B05_CTX_03",
    "FIG-CTX-B06_CTX_02",
    "FIG-CTX-B06_CTX_03",
]

CHANNELS = [
    "DOUYIN_TIKTOK_SHORT",
    "XIAOHONGSHU_CAROUSEL",
    "WECHAT_LONGFORM",
    "PANDAAI_EXPLANATION",
]

PUBLISHING_SUPPLEMENTAL_FIGURES = {
    "CNT-01-FIRST-CUT-NOT-THE-BOTTOM": [],
    "CNT-02-SAME-LABEL-DIFFERENT-PATHS": ["FIG-CASE-B03"],
    "CNT-03-GOLD-VS-EQUITIES": [],
    "CNT-04-HINDSIGHT-TRAPS": [
        "FIG-CTX-B04_CTX_02","FIG-CTX-B04_CTX_03","FIG-CTX-B05_CTX_03",
        "FIG-CTX-B06_CTX_02","FIG-CTX-B06_CTX_03",
    ],
    "CNT-05-RECOVERY-CLOCK": [],
    "CNT-06-1987-MULTI-LEG": ["FIG-CASE-B02"],
}

VARIANTS = {
    "SVG_RESEARCH": {"figsize": (12, 7), "suffix": "__research.svg", "dpi": 100, "width": 1200, "height": 700},
    "PNG_16_9": {"figsize": (16, 9), "suffix": "__16x9.png", "dpi": 100, "width": 1600, "height": 900},
    "PNG_1_1": {"figsize": (12, 12), "suffix": "__1x1.png", "dpi": 100, "width": 1200, "height": 1200},
}

plt.rcParams["svg.hashsalt"] = "fed-cycle-p1-visual-publishing-matrix-027"
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "DejaVu Sans"

def read_pass(path: Path):
    q = json.loads(path.read_text())
    if q.get("qc_gate") != "PASS":
        raise RuntimeError(f"upstream QC not PASS: {path}")
    return q

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

def footer(fig, key, claims, disclaimer, square=False):
    fig.text(0.02, 0.036 if square else 0.025, f"{key} | Claims: {claims}", fontsize=7.2, va="bottom")
    fig.text(0.02, 0.012 if square else 0.006,
             textwrap.fill(disclaimer, 100 if square else 145), fontsize=6.6, va="bottom")

def effective_sources(key: str) -> str:
    if key == "FIG-CASE-B02":
        return (
            "results/fed_cycle_historical_casebook_v1/CASEBOOK_POLICY_SEQUENCE.csv|"
            "results/fed_cycle_historical_context_022a_v1/CONTEXT_CLAIMS.csv|"
            "results/fed_cycle_content_claim_registry_022b_v1/CLAIM_REGISTRY.csv"
        )
    if key == "FIG-CASE-B03":
        return (
            "results/fed_cycle_historical_casebook_v1/CASEBOOK_POLICY_SEQUENCE.csv|"
            "results/fed_cycle_historical_casebook_v1/CASEBOOK_ASSET_PHASE_METRICS.csv|"
            "results/fed_cycle_historical_context_022a_v1/CONTEXT_CLAIMS.csv"
        )
    if key.startswith("FIG-CTX-"):
        return (
            "results/fed_cycle_historical_context_022a_v1/CONTEXT_CLAIMS.csv|"
            "results/fed_cycle_content_claim_registry_022b_v1/CLAIM_REGISTRY.csv"
        )
    raise RuntimeError(f"no source mapping for {key}")

def b02_figure(spec, figsize, policy, context):
    pg = policy[policy["broad_episode_id"] == "B02"].copy()
    cg = context[context["broad_episode_id"] == "B02"].copy()
    cycles = ["T03_1987", "T04_1987", "T05_1988"]
    if set(pg["cycle_id"]) != set(cycles):
        raise RuntimeError("B02 cycle universe changed")

    fig = plt.figure(figsize=figsize)
    square = figsize[0] == figsize[1]
    gs = fig.add_gridspec(2,1,height_ratios=[2.1,1.1],left=0.08,right=0.96,top=0.86,bottom=0.16,hspace=0.34)
    ax = fig.add_subplot(gs[0,0])

    ymap = {c:i for i,c in enumerate(cycles)}
    for c in cycles:
        z=pg[pg["cycle_id"]==c].copy()
        z["event_date"]=pd.to_datetime(z["event_date"])
        y=ymap[c]
        ax.hlines(y, z["event_date"].min(), z["event_date"].max(), linewidth=2)
        for r in z.itertuples(index=False):
            marker={"FIRST_HIKE":"^","LAST_HIKE":"s","PAUSE_START":"o","FIRST_CUT":"v"}.get(r.event_type,"o")
            ax.scatter(r.event_date,y,marker=marker,s=70)
            ax.text(r.event_date,y+0.13,f"{r.event_type}\n{r.event_date.date()}",ha="center",fontsize=7)

    black_monday = pd.Timestamp("1987-10-19")
    ax.axvline(black_monday, linestyle="--", linewidth=1)
    ax.text(black_monday, 2.42, "Black Monday\n1987-10-19", ha="center", va="bottom", fontsize=8)
    ax.set_yticks([0,1,2], cycles)
    ax.set_ylim(-0.45,2.75)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=4,maxticks=8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.tick_params(axis="x",labelsize=7)
    ax.set_title("Three preserved mechanical policy sub-cycles — no synthetic single path")

    ax2=fig.add_subplot(gs[1,0])
    ax2.axis("off")
    y=0.93
    for r in cg.itertuples(index=False):
        t=textwrap.shorten(str(r.claim_text), width=145 if not square else 100, placeholder="…")
        ax2.text(0.01,y,f"[{r.claim_time_class}] {r.event_date_or_period}: {t}",transform=ax2.transAxes,fontsize=7.3,va="top")
        y-=0.27
    ax2.text(0.99,0.03,
             "Boundary: B02 = T03_1987 + T04_1987 + T05_1988; no fabricated four-asset aggregate and no synthetic FIRST_HIKE→FIRST_CUT path.",
             transform=ax2.transAxes,ha="right",fontsize=7.4)

    fig.suptitle("B02 1987–1989 — multi-leg policy structure and market-stress context", y=0.96, fontweight="bold")
    footer(fig,spec["figure_key"],spec["linked_claim_ids"],spec["required_disclaimer"],square)
    return fig

def b03_figure(spec, figsize, policy, case_assets, context):
    pg=policy[policy["broad_episode_id"]=="B03"].copy()
    ag=case_assets[(case_assets["broad_episode_id"]=="B03")&(case_assets["anchor"]=="FIRST_CUT")].copy()
    cg=context[context["broad_episode_id"]=="B03"].copy()
    if ag["asset"].nunique()!=4:
        raise RuntimeError("B03 four-asset FIRST_CUT universe changed")

    fig=plt.figure(figsize=figsize)
    square=figsize[0]==figsize[1]
    gs=fig.add_gridspec(3,1,height_ratios=[1.0,1.6,1.0],left=0.07,right=0.96,top=0.87,bottom=0.16,hspace=0.36)

    ax=fig.add_subplot(gs[0,0])
    pg["event_date"]=pd.to_datetime(pg["event_date"])
    ax.hlines(0,pg["event_date"].min(),pg["event_date"].max(),linewidth=1.3)
    for r in pg.itertuples(index=False):
        marker={"FIRST_HIKE":"^","LAST_HIKE":"s","PAUSE_START":"o","FIRST_CUT":"v"}.get(r.event_type,"o")
        ax.scatter(r.event_date,0,marker=marker,s=75)
        ax.text(r.event_date,0.12,f"{r.event_type}\n{r.event_date.date()}",ha="center",fontsize=7.2)
    ax.set_yticks([])
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3,maxticks=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.tick_params(axis="x",labelsize=7)
    ax.set_title("1994–1995 policy chronology")

    ax=fig.add_subplot(gs[1,0])
    ag=ag.set_index("asset").loc[["GOLD","NASDAQ","SP500","WTI"]].reset_index()
    vals=ag["ret_12m"].astype(float)*100
    y=range(4)
    ax.barh(list(y),vals)
    ax.axvline(0,linewidth=0.8)
    ax.set_yticks(list(y),ag["asset"])
    ax.invert_yaxis()
    ax.set_xlabel("+12M endpoint return (%)")
    ax.set_title("FIRST_CUT path evidence")
    for i,r in ag.iterrows():
        endpoint=float(r["ret_12m"])*100
        dd=float(r["mdd_12m"])*100
        tm=int(r["mdd_trough_month"])
        ax.text(endpoint+(0.4 if endpoint>=0 else -0.4),i,
                f"{endpoint:+.1f}% | MDD {dd:.1f}% | trough M{tm}",
                va="center",ha="left" if endpoint>=0 else "right",fontsize=8)

    ax=fig.add_subplot(gs[2,0]); ax.axis("off")
    y0=0.90
    for r in cg.itertuples(index=False):
        t=textwrap.shorten(str(r.claim_text),width=140 if not square else 95,placeholder="…")
        ax.text(0.01,y0,f"[{r.claim_time_class}] {r.event_date_or_period}: {t}",transform=ax.transAxes,fontsize=7.2,va="top")
        y0-=0.27
    ax.text(0.99,0.03,"Retrospective no-recession classification is not a contemporaneous 'soft landing' forecast.",
            transform=ax.transAxes,ha="right",fontsize=7.3)

    fig.suptitle("B03 1994–1995 — first-cut case with transition-era communication context",y=0.96,fontweight="bold")
    footer(fig,spec["figure_key"],spec["linked_claim_ids"],spec["required_disclaimer"],square)
    return fig

def context_card(spec, figsize, context, claims):
    cid=spec["linked_claim_ids"].replace("CLM-CTX-","")
    z=context[context["claim_id"]==cid]
    if len(z)!=1:
        raise RuntimeError(f"context claim missing: {cid}")
    r=z.iloc[0]
    cr=claims[claims["claim_id"]==spec["linked_claim_ids"]]
    if len(cr)!=1:
        raise RuntimeError(f"claim registry row missing: {spec['linked_claim_ids']}")
    cr=cr.iloc[0]

    fig=plt.figure(figsize=figsize)
    square=figsize[0]==figsize[1]
    ax=fig.add_axes([0.07,0.16,0.88,0.68]); ax.axis("off")
    fig.suptitle(f"{r['broad_episode_id']} context — {r['claim_time_class']}", y=0.95, fontweight="bold")

    ax.text(0.00,0.92,f"Event / period: {r['event_date_or_period']}",fontsize=10,fontweight="bold",transform=ax.transAxes)
    ax.text(0.00,0.82,f"Time class: {r['claim_time_class']}",fontsize=10,transform=ax.transAxes)
    ax.text(0.00,0.72,textwrap.fill(str(r["claim_text"]),105 if not square else 76),
            fontsize=9.2,va="top",transform=ax.transAxes)

    ax.text(0.00,0.39,"Hindsight warning",fontsize=9,fontweight="bold",transform=ax.transAxes)
    ax.text(0.00,0.33,textwrap.fill(str(r["hindsight_warning"]),115 if not square else 82),
            fontsize=8.2,va="top",transform=ax.transAxes)

    ax.text(0.00,0.17,f"Source: {r['source_institution']} — {r['source_title']}",fontsize=7.8,transform=ax.transAxes)
    ax.text(0.00,0.11,textwrap.fill(str(r["source_url"]),135 if not square else 95),fontsize=6.8,transform=ax.transAxes)
    ax.text(0.00,0.03,"Allowed use: "+textwrap.shorten(str(r["allowed_content_use"]),width=150,placeholder="…"),fontsize=7.2,transform=ax.transAxes)

    footer(fig,spec["figure_key"],spec["linked_claim_ids"],spec["required_disclaimer"],square)
    return fig

def build_figure(spec, figsize, policy, case_assets, context, claims):
    key=spec["figure_key"]
    if key=="FIG-CASE-B02":
        return b02_figure(spec,figsize,policy,context)
    if key=="FIG-CASE-B03":
        return b03_figure(spec,figsize,policy,case_assets,context)
    if key.startswith("FIG-CTX-"):
        return context_card(spec,figsize,context,claims)
    raise RuntimeError(key)

def save_variant(fig,key,variant):
    cfg=VARIANTS[variant]
    path=FIGDIR/f"{key}{cfg['suffix']}"
    if variant=="SVG_RESEARCH":
        fig.savefig(path,format="svg",dpi=cfg["dpi"],metadata={"Creator":"FED-CYCLE-P1-VISUAL-PUBLISHING-MATRIX-027","Date":None})
    else:
        fig.savefig(path,format="png",dpi=cfg["dpi"],metadata={"Creator":"FED-CYCLE-P1-VISUAL-PUBLISHING-MATRIX-027"})
    plt.close(fig)
    return path

def parse_list(s):
    if pd.isna(s) or not str(s).strip():
        return []
    return [x for x in str(s).split("|") if x]

def publishing_row(content_row, channel, all_rendered):
    figures=parse_list(content_row["figure_keys"]) + PUBLISHING_SUPPLEMENTAL_FIGURES[content_row["content_id"]]
    dedup=[]
    for f in figures:
        if f not in dedup:
            dedup.append(f)
    rendered=[f for f in dedup if f in all_rendered]
    hooks=json.loads(content_row["hooks_json"])
    hook=hooks[0]
    base={
        "content_id":content_row["content_id"],
        "channel":channel,
        "primary_title_zh":content_row["primary_title_zh"],
        "selected_hook_zh":hook,
        "claim_ids":content_row["claim_ids"],
        "available_figure_keys":"|".join(rendered),
        "freshness_rule":content_row["freshness_rule"],
        "mandatory_caveat":content_row["mandatory_caveat"],
        "prohibited_wording":content_row["prohibited_wording"],
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
    }
    if channel=="DOUYIN_TIKTOK_SHORT":
        base.update({
            "content_basis":"026 60-90 second script",
            "visual_variant":"PNG_16_9_AS_EVIDENCE_INSERT",
            "layout_plan":"9:16 video composition external to 027; insert 16:9 evidence panels without cropping away figure footer",
            "source_placement":"caption/pinned comment or closing source card",
            "caveat_placement":"closing card + caption",
            "platform_status":"SCRIPT_AND_EVIDENCE_READY__9X16_COMPOSITE_NOT_RENDERED",
        })
    elif channel=="XIAOHONGSHU_CAROUSEL":
        base.update({
            "content_basis":"026 title/hooks + long-form evidence order",
            "visual_variant":"PNG_1_1",
            "layout_plan":"5-9 cards: question cover -> 3-6 evidence cards -> boundary/source card",
            "source_placement":"final card + post body",
            "caveat_placement":"final card",
            "platform_status":"CANONICAL_CAROUSEL_INPUTS_READY",
        })
    elif channel=="WECHAT_LONGFORM":
        base.update({
            "content_basis":"026 long-form outline",
            "visual_variant":"SVG_RESEARCH|PNG_16_9",
            "layout_plan":"question -> evidence framework -> figures/cases -> limitations -> source appendix",
            "source_placement":"inline figure provenance + appendix",
            "caveat_placement":"method/limitations section + conclusion",
            "platform_status":"CANONICAL_LONGFORM_INPUTS_READY",
        })
    elif channel=="PANDAAI_EXPLANATION":
        base.update({
            "content_basis":"026 machine-readable content object + CLAIM_ID/FIGURE_KEY retrieval",
            "visual_variant":"SVG_RESEARCH|PNG_1_1",
            "layout_plan":"answer -> evidence claims -> optional figure refs -> freshness/uncertainty -> boundary",
            "source_placement":"machine-readable claim/source metadata",
            "caveat_placement":"response evidence-boundary field",
            "platform_status":"CANONICAL_AGENT_INPUTS_READY",
        })
    else:
        raise RuntimeError(channel)
    return base

def main():
    q024=read_pass(Q024); q025=read_pass(Q025); q026=read_pass(Q026)
    figreg=pd.read_csv(FIGREG)
    render025=pd.read_csv(R025)
    content=pd.read_csv(CONTENT)
    claims=pd.read_csv(CLAIMS)
    policy=pd.read_csv(POLICY)
    case_assets=pd.read_csv(CASE_ASSETS)
    context=pd.read_csv(CONTEXT)

    specs=figreg[figreg["figure_key"].isin(P1_KEYS)].copy()
    if len(specs)!=7 or set(specs["figure_key"])!=set(P1_KEYS):
        raise RuntimeError("frozen P1 universe changed")
    if not (specs["priority"]=="P1").all():
        raise RuntimeError("027 contains non-P1 figure")

    ordered=specs.set_index("figure_key").loc[P1_KEYS].reset_index()
    manifest=[]
    for _,spec in ordered.iterrows():
        actual_sources=effective_sources(spec["figure_key"])
        source_hash=source_bundle_hash(actual_sources)
        for variant,cfg in VARIANTS.items():
            fig=build_figure(spec,cfg["figsize"],policy,case_assets,context,claims)
            path=save_variant(fig,spec["figure_key"],variant)
            if path.stat().st_size<=0:
                raise RuntimeError(f"zero-byte render: {path}")
            if variant.startswith("PNG"):
                with Image.open(path) as im:
                    if im.size!=(cfg["width"],cfg["height"]):
                        raise RuntimeError(f"dimension mismatch {path}: {im.size}")
            manifest.append({
                "figure_key":spec["figure_key"],
                "variant":variant,
                "relative_path":str(path.relative_to(ROOT)).replace("\\","/"),
                "linked_claim_ids":spec["linked_claim_ids"],
                "source_files":actual_sources,
                "source_bundle_sha256":source_hash,
                "sha256":sha256_file(path),
                "byte_size":path.stat().st_size,
                "width_px":cfg["width"],
                "height_px":cfg["height"],
                "render_status":"PASS",
            })

    m=pd.DataFrame(manifest)
    if len(m)!=21 or m["figure_key"].nunique()!=7:
        raise RuntimeError("expected 21 renders / 7 figure keys")
    for v in VARIANTS:
        if int((m["variant"]==v).sum())!=7:
            raise RuntimeError(f"variant count changed: {v}")

    # SVG content assertions.
    b02=(FIGDIR/"FIG-CASE-B02__research.svg").read_text()
    for token in ["T03_1987","T04_1987","T05_1988","no synthetic single path"]:
        if token not in b02:
            raise RuntimeError(f"B02 visual missing {token}")
    if "four-asset" in b02.lower() and "no fabricated four-asset" not in b02.lower():
        raise RuntimeError("B02 appears to fabricate four-asset summary")
    b03=(FIGDIR/"FIG-CASE-B03__research.svg").read_text()
    for token in ["GOLD","NASDAQ","SP500","WTI"]:
        if token not in b03:
            raise RuntimeError(f"B03 visual missing asset {token}")

    expected_classes={
        "FIG-CTX-B04_CTX_02":"RETROSPECTIVE_DATING",
        "FIG-CTX-B04_CTX_03":"POST_ANCHOR_SHOCK",
        "FIG-CTX-B05_CTX_03":"RETROSPECTIVE_DATING",
        "FIG-CTX-B06_CTX_02":"RETROSPECTIVE_DATING",
        "FIG-CTX-B06_CTX_03":"POST_ANCHOR_SHOCK",
    }
    for key,cl in expected_classes.items():
        svg=(FIGDIR/f"{key}__research.svg").read_text()
        if cl not in svg:
            raise RuntimeError(f"{key} lost time class {cl}")

    m.to_csv(OUT/"P1_RENDER_MANIFEST.csv",index=False)
    unique_sources=sorted({rel for key in P1_KEYS for rel in effective_sources(key).split("|")})
    pd.DataFrame([
        {"source_file":rel,"sha256":sha256_file(ROOT/rel),"byte_size":(ROOT/rel).stat().st_size}
        for rel in unique_sources
    ]).to_csv(OUT/"P1_SOURCE_FILE_HASHES.csv",index=False)

    # Publishing matrix: six exact packages x four channels.
    if len(content)!=6 or content["content_id"].nunique()!=6:
        raise RuntimeError("026 content universe changed")
    all_rendered=set(render025["figure_key"])|set(m["figure_key"])
    pub=[]
    for _,r in content.iterrows():
        for ch in CHANNELS:
            pub.append(publishing_row(r,ch,all_rendered))
    pubdf=pd.DataFrame(pub)
    if len(pubdf)!=24:
        raise RuntimeError("publishing matrix must have 24 rows")
    if not (pubdf.groupby("content_id")["channel"].nunique()==4).all():
        raise RuntimeError("each content package must have four channels")

    prohibited_field_tokens=["best_asset","closest_analog","forecast_return","political_evaluation","buy_signal","sell_signal"]
    bad=[c for c in pubdf.columns if any(t in c.lower() for t in prohibited_field_tokens)]
    if bad:
        raise RuntimeError(f"prohibited matrix fields: {bad}")
    if not pubdf[pubdf["channel"]=="DOUYIN_TIKTOK_SHORT"]["layout_plan"].str.contains("9:16 video composition external to 027",regex=False).all():
        raise RuntimeError("Douyin/TikTok matrix must disclose no full 9:16 composition")
    cnt02 = pubdf[pubdf["content_id"]=="CNT-02-SAME-LABEL-DIFFERENT-PATHS"]
    if not cnt02["available_figure_keys"].str.contains("FIG-CASE-B03", regex=False).all():
        raise RuntimeError("CNT-02 publishing rows missing newly rendered B03 figure")
    cnt04 = pubdf[pubdf["content_id"]=="CNT-04-HINDSIGHT-TRAPS"]
    for key in PUBLISHING_SUPPLEMENTAL_FIGURES["CNT-04-HINDSIGHT-TRAPS"]:
        if not cnt04["available_figure_keys"].str.contains(key, regex=False).all():
            raise RuntimeError(f"CNT-04 publishing rows missing newly rendered context figure {key}")
    cnt06 = pubdf[pubdf["content_id"]=="CNT-06-1987-MULTI-LEG"]
    if not cnt06["available_figure_keys"].str.contains("FIG-CASE-B02", regex=False).all():
        raise RuntimeError("CNT-06 publishing rows missing newly rendered B02 figure")

    pubdf.to_csv(OUT/"PUBLISHING_MATRIX.csv",index=False)

    # All six canonical packages now have at least one package-specific visual; include new B02/B03/context where relevant.
    readiness=[]
    addmap=PUBLISHING_SUPPLEMENTAL_FIGURES
    for _,r in content.iterrows():
        base=parse_list(r["rendered_figure_keys"])
        combined=[]
        for x in base+addmap[r["content_id"]]:
            if x not in combined:
                combined.append(x)
        if not combined:
            raise RuntimeError(f"visual completion failed {r['content_id']}")
        freshness=r["freshness_rule"]
        readiness.append({
            "content_id":r["content_id"],
            "previous_visual_readiness":r["visual_readiness"],
            "new_visual_readiness":"VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE",
            "canonical_visual_keys":"|".join(combined),
            "new_027_visual_keys":"|".join(addmap[r["content_id"]]),
            "freshness_rule":freshness,
            "platform_native_9x16_video_rendered":False,
            "causal_status":"NONE",
            "deployment_status":"NOT_DEPLOYABLE",
        })
    rdf=pd.DataFrame(readiness)
    if len(rdf)!=6 or not (rdf["new_visual_readiness"]=="VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE").all():
        raise RuntimeError("not all content packages visually complete")
    if rdf.loc[rdf["content_id"]=="CNT-04-HINDSIGHT-TRAPS","freshness_rule"].iloc[0]!="REVERIFY_BEFORE_CURRENT_USE":
        raise RuntimeError("CNT-04 freshness lost")
    rdf.to_csv(OUT/"PACKAGE_VISUAL_READINESS.csv",index=False)

    guide=[
        "# 027 平台发布矩阵与视觉补全指南",
        "",
        "027完成的是 canonical evidence visual + publishing routing，不是最终9:16成片。",
        "",
        "## 抖音 / TikTok",
        "",
        "- 直接使用026的60–90秒脚本。",
        "- 025/027的16:9证据图作为视频内证据插片；不要裁掉图底部CLAIM_ID和免责声明。",
        "- 027未生成最终9:16视频画布；后续成片应在9:16构图中嵌入这些证据图。",
        "- 结尾卡或caption保留“历史研究/教育内容，不构成当前预测或投资建议”。",
        "",
        "## 小红书",
        "",
        "- 使用1:1 PNG作为核心卡片。",
        "- 建议5–9页：问题封面 → 3–6页证据 → 最后一页边界/来源。",
        "- 跨资产内容不得制作‘冠军资产’排序。",
        "",
        "## 公众号 / 深度长文",
        "",
        "- 使用026长文结构。",
        "- 正文用SVG/16:9研究图；图下注明CLAIM_ID / FIGURE_KEY。",
        "- 历史事件必须保留CONTEMPORANEOUS / RETROSPECTIVE / POST_ANCHOR时间标签。",
        "- 文末附来源与研究边界。",
        "",
        "## PandaAI",
        "",
        "- 优先返回claim_id、figure_key、freshness、support和boundary。",
        "- 如果用户问当前状态，必须使用新的append-only current snapshot；不能把2026-09-25快照伪装成实时。",
        "- 不把历史中位数转成个性化买卖建议。",
        "",
        "## 027新增视觉",
        "",
    ]
    for key in P1_KEYS:
        guide.append(f"- {key}")
    (OUT/"PLATFORM_PUBLISHING_GUIDE_ZH.md").write_text("\n".join(guide)+"\n")

    report=[
        "# FED-CYCLE-P1-VISUAL-PUBLISHING-MATRIX-027 — REPORT",
        "",
        "## Status",
        "",
        "**QC-PASSED P1 VISUAL COMPLETION + 24-ROW PUBLISHING MATRIX / NOT NEW EVIDENCE / NOT A FORECAST / NOT DEPLOYABLE**",
        "",
        "- P1 figure keys rendered: 7",
        "- P1 render files: 21",
        "- SVG_RESEARCH: 7",
        "- PNG_16_9: 7",
        "- PNG_1_1: 7",
        "- canonical content packages: 6",
        "- channels per package: 4",
        "- publishing matrix rows: 24",
        "- all six packages canonical-visual-complete: yes",
        "",
        "## New visual coverage",
        "",
        "- B02 multi-leg 1987-89 case;",
        "- B03 1994-95 case;",
        "- 2001 retrospective recession dating;",
        "- September 11 post-anchor shock;",
        "- 2007 retrospective recession dating;",
        "- 2020 retrospective recession dating;",
        "- COVID post-anchor shock.",
        "",
        "## Platform boundary",
        "",
        "Douyin/TikTok rows are script/evidence ready but 027 does not claim a finished 9:16 video render. Xiaohongshu, WeChat and PandaAI routes retain claim/figure/freshness/caveat provenance.",
        "",
        "027 adds no empirical inference and does not rank assets, select a current analog, forecast returns or provide trade instructions.",
    ]
    (OUT/"FED_CYCLE_P1_VISUAL_PUBLISHING_MATRIX_027_REPORT.md").write_text("\n".join(report)+"\n")

    qc={
        "qc_gate":"PASS",
        "module":"FED-CYCLE-P1-VISUAL-PUBLISHING-MATRIX-027",
        "upstream_qc":{"024":q024["qc_gate"],"025":q025["qc_gate"],"026":q026["qc_gate"]},
        "p1_figure_keys":7,
        "p1_universe_exact_match":True,
        "rendered_files":int(len(m)),
        "svg_research_files":int((m["variant"]=="SVG_RESEARCH").sum()),
        "png_16_9_files":int((m["variant"]=="PNG_16_9").sum()),
        "png_1_1_files":int((m["variant"]=="PNG_1_1").sum()),
        "png_16_9_dimensions":"1600x900",
        "png_1_1_dimensions":"1200x1200",
        "nonempty_hashes":bool(m["sha256"].str.len().eq(64).all() and m["source_bundle_sha256"].str.len().eq(64).all()),
        "b02_three_subcycles_visible":True,
        "b02_no_synthetic_path_visible":True,
        "b02_four_asset_summary_fabricated":False,
        "b03_four_assets_visible":True,
        "context_time_classes_preserved":True,
        "post_anchor_shock_cards_visible":True,
        "publishing_matrix_rows":int(len(pubdf)),
        "channels_per_content":4,
        "publishing_matrix_new_p1_figures_routed":True,
        "canonical_visual_complete_packages":int((rdf["new_visual_readiness"]=="VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE").sum()),
        "douyin_tiktok_full_9x16_render_claimed":False,
        "cnt04_reverify_before_current_use":True,
        "analog_score_outputs":0,
        "asset_ranking_outputs":0,
        "forecast_outputs":0,
        "buy_sell_outputs":0,
        "political_evaluation_outputs":0,
        "new_inference":False,
        "pvalues_generated":False,
        "private_paper_inputs_used":False,
        "causal_status":"NONE",
        "deployment_status":"NOT_DEPLOYABLE",
        "render_environment":{"matplotlib":matplotlib.__version__,"pandas":pd.__version__,"pillow":pillow_version},
    }
    (OUT/"QC.json").write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")

if __name__=="__main__":
    main()
