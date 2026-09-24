# FED-CYCLE-VINTAGE-AUDIT-007 — Event Contrast Revision Impact
Date: 2026-09-24
Status: **POST-RUN DESCRIPTIVE IMPACT AUDIT / NO NEW INFERENCE**

## Trigger

The real-time IPT audit changes one of the ten frozen FIRST_HIKE growth labels:

- 2022: current-vintage WEAK -> real-time STRONG.

STATE-001 previously reported descriptive STRONG-vs-WEAK Gold medians using the current-vintage growth label.

This audit recalculates those same descriptive medians under the real-time label to quantify the impact of the single state flip.

## Frozen calculation

Use the existing ten FIRST_HIKE rows and unchanged Gold outcomes from:

`results/fed_cycle_state_v1/STATE_EVENT_PANEL.csv`

Compare two classifications:

1. original `GROWTH_STATE`;
2. `realtime_growth_state` from VINTAGE-AUDIT-007.

For each classification and each group STRONG / WEAK report:

- n;
- Gold +6M median return;
- Gold +12M median return;
- Gold +24M median return;
- Gold 24M MDD median.

Also report STRONG minus WEAK median differences.

No p-values, threshold changes, horizon changes or new group definitions.

## Interpretation

This is a descriptive revision-impact calculation only.

It may show whether the old STATE-001 event-level growth contrast is robust or fragile to real-time data revisions.

It does not create confirmatory evidence, causality, forecasting value or deployment value.
