# FED Cycle Content Pack Index — 022B

These are routing bundles, not finished scripts. Every factual statement should still resolve to a canonical CLAIM_ID.

## PACK-01-FIRST-CUT-NOT-THE-BOTTOM — First cut does not mean path risk is finished

Claims:

- `CLM-PHASE-DXY-FIRST_CUT` — DXY × FIRST_CUT historical path
- `CLM-PHASE-GOLD-FIRST_CUT` — GOLD × FIRST_CUT historical path
- `CLM-PHASE-NASDAQ-FIRST_CUT` — NASDAQ × FIRST_CUT historical path
- `CLM-PHASE-SP500-FIRST_CUT` — SP500 × FIRST_CUT historical path
- `CLM-PHASE-WTI-FIRST_CUT` — WTI × FIRST_CUT historical path
- `CLM-SYNTH-017-FIRSTCUT-RECOVERY` — First cut did not shorten full recovery versus pause
- `CLM-GUARD-019` — Binary pre-cut timing rule not supported
- `CLM-GUARD-020` — Continuous pre-cut levels did not rescue timing
- `CLM-CASE-B04` — B04 FIRST_CUT four-asset path
- `CLM-CASE-B05` — B05 FIRST_CUT four-asset path
- `CLM-CASE-B06` — B06 FIRST_CUT four-asset path
- `CLM-CASE-B07` — B07 FIRST_CUT four-asset path

Boundary: preserve each claim's evidence-time, support, freshness and prohibited-wording fields.

## PACK-02-SAME-LABEL-DIFFERENT-PATHS — Same FIRST_CUT label, very different historical paths

Claims:

- `CLM-CASE-B03` — B03 FIRST_CUT four-asset path
- `CLM-CASE-B04` — B04 FIRST_CUT four-asset path
- `CLM-CASE-B05` — B05 FIRST_CUT four-asset path
- `CLM-CASE-B06` — B06 FIRST_CUT four-asset path
- `CLM-CASE-B07` — B07 FIRST_CUT four-asset path

Boundary: preserve each claim's evidence-time, support, freshness and prohibited-wording fields.

## PACK-03-GOLD-VS-EQUITIES — Gold versus U.S. equities across cycle phases and cases

Claims:

- `CLM-PHASE-GOLD-FIRST_HIKE` — GOLD × FIRST_HIKE historical path
- `CLM-PHASE-GOLD-LAST_HIKE` — GOLD × LAST_HIKE historical path
- `CLM-PHASE-GOLD-PAUSE_START` — GOLD × PAUSE_START historical path
- `CLM-PHASE-GOLD-FIRST_CUT` — GOLD × FIRST_CUT historical path
- `CLM-PHASE-SP500-FIRST_HIKE` — SP500 × FIRST_HIKE historical path
- `CLM-PHASE-SP500-LAST_HIKE` — SP500 × LAST_HIKE historical path
- `CLM-PHASE-SP500-PAUSE_START` — SP500 × PAUSE_START historical path
- `CLM-PHASE-SP500-FIRST_CUT` — SP500 × FIRST_CUT historical path
- `CLM-PHASE-NASDAQ-FIRST_HIKE` — NASDAQ × FIRST_HIKE historical path
- `CLM-PHASE-NASDAQ-LAST_HIKE` — NASDAQ × LAST_HIKE historical path
- `CLM-PHASE-NASDAQ-PAUSE_START` — NASDAQ × PAUSE_START historical path
- `CLM-PHASE-NASDAQ-FIRST_CUT` — NASDAQ × FIRST_CUT historical path
- `CLM-CASE-B04` — B04 FIRST_CUT four-asset path
- `CLM-CASE-B05` — B05 FIRST_CUT four-asset path
- `CLM-CASE-B06` — B06 FIRST_CUT four-asset path
- `CLM-CASE-B07` — B07 FIRST_CUT four-asset path

Boundary: preserve each claim's evidence-time, support, freshness and prohibited-wording fields.

## PACK-04-HINDSIGHT-TRAPS — What was known then versus what was only known later

Claims:

- `CLM-CTX-B04_CTX_02` — B04 context: RETROSPECTIVE_DATING
- `CLM-CTX-B04_CTX_03` — B04 context: POST_ANCHOR_SHOCK
- `CLM-CTX-B05_CTX_03` — B05 context: RETROSPECTIVE_DATING
- `CLM-CTX-B06_CTX_02` — B06 context: RETROSPECTIVE_DATING
- `CLM-CTX-B06_CTX_03` — B06 context: POST_ANCHOR_SHOCK
- `CLM-CTX-B07_CTX_02` — B07 context: RETROSPECTIVE_DATING

Boundary: preserve each claim's evidence-time, support, freshness and prohibited-wording fields.

## PACK-05-RECOVERY-CLOCK — Why endpoint returns and full recovery clocks are different

Claims:

- `CLM-PHASE-DXY-FIRST_HIKE` — DXY × FIRST_HIKE historical path
- `CLM-PHASE-DXY-LAST_HIKE` — DXY × LAST_HIKE historical path
- `CLM-PHASE-DXY-PAUSE_START` — DXY × PAUSE_START historical path
- `CLM-PHASE-DXY-FIRST_CUT` — DXY × FIRST_CUT historical path
- `CLM-PHASE-GOLD-FIRST_HIKE` — GOLD × FIRST_HIKE historical path
- `CLM-PHASE-GOLD-LAST_HIKE` — GOLD × LAST_HIKE historical path
- `CLM-PHASE-GOLD-PAUSE_START` — GOLD × PAUSE_START historical path
- `CLM-PHASE-GOLD-FIRST_CUT` — GOLD × FIRST_CUT historical path
- `CLM-PHASE-NASDAQ-FIRST_HIKE` — NASDAQ × FIRST_HIKE historical path
- `CLM-PHASE-NASDAQ-LAST_HIKE` — NASDAQ × LAST_HIKE historical path
- `CLM-PHASE-NASDAQ-PAUSE_START` — NASDAQ × PAUSE_START historical path
- `CLM-PHASE-NASDAQ-FIRST_CUT` — NASDAQ × FIRST_CUT historical path
- `CLM-PHASE-SP500-FIRST_HIKE` — SP500 × FIRST_HIKE historical path
- `CLM-PHASE-SP500-LAST_HIKE` — SP500 × LAST_HIKE historical path
- `CLM-PHASE-SP500-PAUSE_START` — SP500 × PAUSE_START historical path
- `CLM-PHASE-SP500-FIRST_CUT` — SP500 × FIRST_CUT historical path
- `CLM-PHASE-WTI-FIRST_HIKE` — WTI × FIRST_HIKE historical path
- `CLM-PHASE-WTI-LAST_HIKE` — WTI × LAST_HIKE historical path
- `CLM-PHASE-WTI-PAUSE_START` — WTI × PAUSE_START historical path
- `CLM-PHASE-WTI-FIRST_CUT` — WTI × FIRST_CUT historical path
- `CLM-SYNTH-017-FIRSTCUT-RECOVERY` — First cut did not shorten full recovery versus pause

Boundary: preserve each claim's evidence-time, support, freshness and prohibited-wording fields.

## PACK-06-1987-MULTI-LEG — Why 1987-89 should not be forced into one standard cycle

Claims:

- `CLM-CASE-B02` — 1987-89 is a multi-leg episode
- `CLM-CTX-B02_CTX_01` — B02 context: RETROSPECTIVE_EVENT_CONTEXT
- `CLM-CTX-B02_CTX_02` — B02 context: RETROSPECTIVE_EVENT_CONTEXT
- `CLM-CTX-B02_CTX_03` — B02 context: RETROSPECTIVE_DATING

Boundary: preserve each claim's evidence-time, support, freshness and prohibited-wording fields.

