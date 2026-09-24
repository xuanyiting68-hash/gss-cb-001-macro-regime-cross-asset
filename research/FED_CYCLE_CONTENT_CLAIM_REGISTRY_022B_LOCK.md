# FED-CYCLE-CONTENT-CLAIM-REGISTRY-022B — LOCK

Date locked: 2026-09-25

## Purpose

Create the canonical reusable claim layer for the public Fed-cycle / cross-asset research program.

The registry is the single source of truth for claims reused in:
- short-form video;
- long-form video;
- deep articles;
- image cards / charts;
- PandaAI explanations;
- myth-vs-evidence content.

022B **does not create new empirical evidence**. It packages already-QC-passed 021, 022, 022A, 017, 019 and 020 evidence into stable, source-linked content claims.

## Frozen claim universe

Exactly **47 claims** in v1.

### A. CORE_PHASE_DISTRIBUTION — 20 claims

Five core assets x four Fed-cycle anchors:
- DXY
- GOLD
- NASDAQ
- SP500
- WTI

Phases:
- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Each claim may state only the exact 021 historical descriptive metrics:
- broad-episode-weighted +12M endpoint;
- 12M MDD;
- trough month;
- anchor-to-full-recovery KM median where supported;
- sample/support status.

Stable ID pattern:
`CLM-PHASE-{ASSET}-{PHASE}`

### B. HISTORICAL_CASE — 6 claims

- B02: structure claim only — three mechanical sub-cycles; do not synthesize a fictitious single cycle.
- B03-B07: one FIRST_CUT case-path summary per broad episode using exact 022 Gold/SP500/Nasdaq/WTI rows.

Stable ID:
`CLM-CASE-{BROAD_EPISODE_ID}`

### C. HISTORICAL_CONTEXT — 18 claims

Copy the validated 022A claims without altering factual content.

Stable IDs:
`CLM-CTX-{ORIGINAL_022A_CLAIM_ID}`

All anti-hindsight metadata must be preserved.

### D. METHOD_GUARDRAIL / SYNTHESIS — 3 claims

1. `CLM-GUARD-019`:
   simple binary predetermined pre-FIRST_CUT state rule not supported.

2. `CLM-GUARD-020`:
   continuous pre-FIRST_CUT stress levels do not rescue the small-sample timing-rule hypothesis; branch stopped.

3. `CLM-SYNTH-017-FIRSTCUT-RECOVERY`:
   among the five fully supported core assets, FIRST_CUT anchor-to-full-recovery is slower than PAUSE in 3/5, equal in 2/5, faster in 0/5.

Total = 20 + 6 + 18 + 3 = 47.

## Required fields

Every registry row must expose:

- claim_id
- claim_family
- claim_status
- title_short
- canonical_wording
- asset
- phase
- broad_episode_id
- metric_payload
- sample_descriptor
- support_status
- evidence_class
- evidence_time
- source_modules
- source_files
- official_source_urls
- allowed_wording
- prohibited_wording
- freshness_rule
- figure_key
- content_tags
- causal_status
- oos_status
- deployment_status

## Claim status

All v1 rows are:
`CANONICAL_PUBLIC_SAFE`

unless an upstream claim is explicitly limited/diagnostic. For the 20 phase claims, only the five core four-phase assets are used, so support must be supported.

## Evidence-time rules

- CORE_PHASE_DISTRIBUTION: `DESCRIPTIVE_PATH`
- HISTORICAL_CASE: `DESCRIPTIVE_PATH` except B02 structure is `RETROSPECTIVE_CHRONOLOGY`
- HISTORICAL_CONTEXT: inherit 022A claim_time_class
- METHOD_GUARDRAIL / SYNTHESIS: `RESEARCH_CONCLUSION`

Do not collapse these classes.

## Content tags

Allowed controlled vocabulary:
- VIDEO_HOOK
- SHORT_VIDEO
- LONG_VIDEO
- DEEP_ARTICLE
- IMAGE_CARD
- MYTH_VS_EVIDENCE
- CASE_STUDY
- PANDAAI
- METHODS
- CURRENT_CONTEXT_GUARDRAIL

Tags are routing metadata only, not evidence.

## Freshness rules

- historical path claims: `STATIC_UNLESS_UPSTREAM_REBUILT`
- historical context claims: `STATIC_SOURCE_AUDIT`, except B07 current NBER chronology = `REVERIFY_BEFORE_CURRENT_USE`
- method guardrails: `STATIC_UNLESS_NEW_PREREGISTERED_EVIDENCE`

## Figure keys

022B assigns a stable intended figure dependency but does not create the figures.

Patterns:
- `FIG-PHASE-{ASSET}-{PHASE}`
- `FIG-CASE-{BROAD_EPISODE_ID}`
- `FIG-CTX-{ORIGINAL_CLAIM_ID}`
- `FIG-GUARD-019`
- `FIG-GUARD-020`
- `FIG-RECOVERY-FIRSTCUT-VS-PAUSE`

These keys feed the later Figure Registry.

## Prohibited operations

022B must NOT:
- create new returns, drawdowns or recovery estimates;
- calculate new p-values;
- create asset rankings or a "best asset";
- select a current historical analog;
- convert a historical claim into a current trading recommendation;
- change official-source wording in a way that removes timing/hindsight caveats;
- convert 019/020 negative evidence into a timing score;
- import private-paper inputs.

## QC gates

PASS requires:
1. exactly 47 unique claim IDs;
2. exactly 20 CORE_PHASE_DISTRIBUTION claims;
3. exactly 6 HISTORICAL_CASE claims;
4. exactly 18 HISTORICAL_CONTEXT claims;
5. exactly 3 guardrail/synthesis claims;
6. all five core assets have exactly four phase claims;
7. all 022A context claim IDs map 1:1;
8. B02 claim explicitly preserves 3 sub-cycles;
9. B04 context preserves September 11 as POST_ANCHOR_SHOCK;
10. B06 context preserves COVID as POST_ANCHOR_SHOCK;
11. B07 current NBER claim has REVERIFY_BEFORE_CURRENT_USE;
12. no blank source/evidence/wording boundary fields;
13. no causal/OOS/deployment promotion;
14. no private-paper inputs;
15. no new inference or p-values.

## Interpretation boundary

The registry is a publishing/retrieval control layer.

A claim's presence in the registry means:
> this wording is traceable to a QC-passed evidence object and is allowed within the stated boundary.

It does **not** mean:
> the claim is causal, predictive, deployable, or an investment recommendation.
