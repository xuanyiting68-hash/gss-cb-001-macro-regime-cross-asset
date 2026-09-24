# FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021 — REPORT

## Status

**QC-PASSED SYNTHESIS / DESCRIPTIVE EVIDENCE MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

021 performs no new price estimation and no new significance search. It harmonizes already-QC-passed public outputs while preserving support labels and metric ontologies.

## Canonical coverage

- price-asset phase rows: 52
- unique price assets: 13
- core fully supported four-phase assets: DXY, GOLD, NASDAQ, SP500, WTI
- policy/rate/cash context rows: 12
- phase-stress context rows: 12

## FIRST_CUT core risk-distribution snapshot

- DXY: median +12M endpoint -1.33%; MDD_12M median 5.18%; trough month 8; anchor-to-full-recovery KM median 13.0 months.
- GOLD: median +12M endpoint +4.06%; MDD_12M median 5.43%; trough month 5; anchor-to-full-recovery KM median 22.0 months.
- NASDAQ: median +12M endpoint +6.04%; MDD_12M median 17.48%; trough month 8; anchor-to-full-recovery KM median 15.0 months.
- SP500: median +12M endpoint +10.98%; MDD_12M median 13.99%; trough month 8; anchor-to-full-recovery KM median 14.0 months.
- WTI: median +12M endpoint -16.94%; MDD_12M median 22.23%; trough month 11; anchor-to-full-recovery KM median 20.0 months.

These are historical descriptive distributions. Positive endpoints can coexist with deep interim drawdowns.

## Interpretation guardrails

- Realized Fed phases are cycle markers, not identified monetary-policy shocks.
- 019 and 020 failed to support a simple predetermined FIRST_CUT bottom-timing rule.
- VIX/BAA/copper stress peaks are ex-post window statistics and are not live timing signals.
- TLT/VNQ/BTC remain limited extensions; Asia remains diagnostic; housing uses a distinct 24M slow-moving metric ontology.
- Cash carry and Treasury-yield changes are retained in a separate context table and are not ranked against price returns.

## Product use

PandaAI may use 021 to present: policy phase + historical asset-specific path-risk distribution + recovery clock + support strength + evidence class + uncertainty. It must not output a deterministic bottom date or convert these tables into a trading recommendation.
