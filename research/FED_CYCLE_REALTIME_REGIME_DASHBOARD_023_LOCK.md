# FED-CYCLE-REALTIME-REGIME-DASHBOARD-023 — LOCK

Date locked: 2026-09-25
Snapshot clock: 2026-09-25T06:08:00Z / 2026-09-25 16:08 Australia/Sydney

## Purpose

Build a release-aware current-state dashboard that links the 2026 policy/macro/financial-condition snapshot to already-QC-passed historical evidence without selecting a single historical analog or issuing an investment recommendation.

023 is a **current-state evidence dashboard**, not a forecasting model.

## Current policy-state ontology

The current 2026 edge run is inherited from the frozen prospective Fed chain:

- candidate FIRST_HIKE: 2026-09-16;
- observed hikes: 1;
- cumulative tightening: 25 bp;
- target range after the action: 3.75%-4.00%;
- frozen prospective qualification rule: >=2 hikes AND >=50 bp;
- current qualification: FALSE;
- prospective broad episode if later qualified: B08.

Canonical current label:

`EDGE_TIGHTENING_CANDIDATE__NOT_YET_QUALIFIED`

Do not relabel the current run as a fully qualified historical broad tightening episode.

## Frozen current-observable set

### Policy / front end
- target lower bound;
- target upper bound;
- effective federal funds rate (EFFR).

### Treasury / inflation expectations
- DGS2;
- DGS10;
- derived 10Y-2Y curve in bp;
- T5YIE;
- T10YIE.

### Financial stress / credit
- VIXCLS;
- BAA10Y;
- NFCI.

### Real economy / inflation
- UNRATE;
- INDPRO year-over-year;
- headline PCE inflation year-over-year;
- core PCE inflation year-over-year.

No additional indicator may be added in v1 after the lock.

## Source hierarchy

1. Federal Reserve Board for the 2026-09-16 FOMC decision and target range.
2. FRED / source institutions for current public observations:
   - Federal Reserve Board / H.15;
   - Federal Reserve Bank of New York;
   - Federal Reserve Bank of Chicago;
   - BEA;
   - BLS;
   - CBOE-derived FRED series.

Each observation must store:
- observation period/date;
- value;
- unit;
- source update date;
- next release date where known;
- source URL;
- retrieval/snapshot clock;
- freshness classification.

## Frozen freshness classes

- `CURRENT_LATEST_RELEASE`: latest available release as of the snapshot clock.
- `CURRENT_WITH_KNOWN_PUBLICATION_LAG`: latest available observation, with a known publication lag explicitly surfaced.
- `STALE_FAIL`: source is older than the latest known release or violates the snapshot clock.

023 must fail closed if any required input is STALE_FAIL.

## Derived state fields

Only the following deterministic transformations are allowed:

1. `TARGET_MIDPOINT = (lower + upper)/2`
2. `CURVE_10Y2Y_BP = (DGS10 - DGS2) * 100`
3. `CURVE_STATE`:
   - INVERTED if < 0
   - NON_INVERTED if >= 0
4. `NFCI_STATE`:
   - TIGHTER_THAN_AVERAGE if > 0
   - LOOSER_THAN_AVERAGE if < 0
   - AVERAGE if = 0
5. `PCE_ABOVE_2_FLAG` and `CORE_PCE_ABOVE_2_FLAG`
6. `INDPRO_YOY_SIGN` = POSITIVE / ZERO / NEGATIVE

No optimized thresholds, composite scores, similarity distances or current-cycle analog ranking are allowed.

## Historical reference layer

023 may link the current mechanical FIRST_HIKE candidate to the following 022B claims for **historical context only**:

- CLM-PHASE-DXY-FIRST_HIKE
- CLM-PHASE-GOLD-FIRST_HIKE
- CLM-PHASE-NASDAQ-FIRST_HIKE
- CLM-PHASE-SP500-FIRST_HIKE
- CLM-PHASE-WTI-FIRST_HIKE
- CLM-GUARD-019
- CLM-GUARD-020

It must also expose the qualification caveat:

> the 2026 run has not yet met the frozen prospective broad-cycle rule, so FIRST_HIKE historical distributions are reference distributions, not an assertion that B08 is qualified or that one historical case is the correct analog.

## Frozen output objects

1. `CURRENT_OBSERVABLES.csv`
2. `CURRENT_POLICY_GATE.csv`
3. `CURRENT_STATE_DERIVED.csv`
4. `HISTORICAL_REFERENCE_CLAIMS.csv`
5. `DASHBOARD_STATE.json`
6. `FED_CYCLE_REALTIME_REGIME_DASHBOARD_023_REPORT.md`
7. `QC.json`

## Prohibited operations

023 must NOT:

- issue a prospective return forecast;
- append a row to the 013 prediction registry unless the 013 frozen gate itself qualifies;
- select a "closest" or "best" historical analog;
- calculate a similarity score;
- rank assets;
- turn FIRST_HIKE historical medians into allocation instructions;
- use ex-post stress peaks as current timing signals;
- change 019/020 negative timing conclusions;
- use revised historical data to claim real-time historical predictability;
- import any private-paper inputs.

## QC gates

PASS requires:

1. 013 current cycle gate still reads exactly one hike / 25 bp / qualifies FALSE unless the authoritative prospective chain has genuinely changed;
2. all frozen current observables present;
3. every observation date/period is <= snapshot clock;
4. every source update date is <= snapshot clock;
5. no required input is STALE_FAIL;
6. target range matches the official 2026-09-16 Fed action;
7. derived curve arithmetic exact within tolerance;
8. current policy label remains EDGE_TIGHTENING_CANDIDATE__NOT_YET_QUALIFIED;
9. exactly seven 022B historical-reference/guardrail CLAIM_IDs linked;
10. no analog/similarity/ranking field;
11. no forecast output;
12. no p-values;
13. private-paper inputs = false;
14. causal status = NONE;
15. OOS status = NOT_A_FORECASTING_MODEL;
16. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

023 answers:

> What policy, rates, inflation-expectation, financial-condition and real-economy information was publicly available as of the snapshot clock, and which already-QC-passed historical evidence objects are relevant as context?

023 does not answer:

> Which historical episode 2026 will follow, which asset is best, where the market will bottom, or what should be bought/sold now?
