# FED-CYCLE-STATE-001 — Post-Run Confounding Diagnostic Amendment
Date: 2026-09-24
Status: **POST-RUN DIAGNOSTIC / NO STATE OR OUTCOME REDEFINITION**

## Trigger

STATE-001 passed its frozen timing/support QC.

The frozen USD bridge criterion also passed:

- six-month return sign agreement between legacy `TWEXM` and modern `DTWEXAFEGS` in overlap = approximately 95.7%;
- FIRST_HIKE USD-direction groups have at least 3 observations each.

Therefore the lock permits USD state-conditioned **descriptive** summaries.

Before interpreting that comparison as a mechanism candidate, an additional confounding audit is required because the sample spans 1983-2022 and state labels may proxy for historical era.

## Diagnostic 1 — frozen USD contrast

Using the already-defined `USD_DIRECTION_DIAGNOSTIC`:

- `RISING` versus `FALLING_OR_FLAT`;
- outcomes remain the frozen +12M Gold return and 24M Gold MDD;
- support floor remains n>=3 per group;
- leave-one-leg-out sign stability uses the same rule as the primary state family.

No USD threshold or source rule is changed.

## Diagnostic 2 — chronological separation

For every supported primary state and the permitted USD diagnostic:

- record min/max FIRST_HIKE year in state A;
- record min/max FIRST_HIKE year in state B;
- `PERFECT_TIME_SEPARATION = TRUE` if all events in one state occur strictly before all events in the other state.

A perfectly time-separated state cannot be interpreted as a clean within-era mechanism contrast in this n=10 event sample.

This audit does not prove confounding, but it identifies a severe era-identification problem.

## Diagnostic 3 — state support map

Record the exact n by state and the event years in each group.

This prevents phrases such as "real yields explain Gold" when the frozen state has 9:1 support, or "yield curve inversion changes Gold" when the sample has no inverted FIRST_HIKE event.

## Evidence status

The audit is:

**DESCRIPTIVE / ASSOCIATIONAL DIAGNOSTIC / NOT CAUSAL / NO P-VALUES / NOT DEPLOYABLE**

No state variable is ranked as "dominant".
