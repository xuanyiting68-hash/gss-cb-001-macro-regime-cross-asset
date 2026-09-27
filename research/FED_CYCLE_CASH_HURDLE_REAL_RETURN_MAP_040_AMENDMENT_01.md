# FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040 — AMENDMENT 01

Date: 2026-09-27
Type: acquisition-only implementation amendment
Status: post-lock / pre-result-canonicalization

## Trigger

The frozen 040 runner was executed through GitHub Actions. Two diagnostic attempts stalled while acquiring the direct daily DFF FRED CSV, including after narrowing the requested history to 1983+.

This amendment is made because of data-delivery/runtime behavior, not because of any observed empirical result.

## Change

For the logical DFF monthly-average cash input, use FRED series `FEDFUNDS` as the acquisition source.

FRED defines the monthly Effective Federal Funds Rate series as an average of daily figures. Therefore this is the same monthly-average rate object required by the frozen 040 cash-hurdle formula.

The source registry must record:
- logical input: DFF monthly average;
- acquired FRED series: FEDFUNDS;
- retrieval URL;
- SHA256 of retrieved bytes;
- retrieval timestamp;
- observation range.

## Unchanged

No change to:
- asset universe;
- phase universe;
- event dates;
- baseline/end-point convention;
- t..t+12 matched cash window;
- monthly compounding formula;
- CPIAUCSL purchasing-power formula;
- broad-episode weights;
- evidence tiers;
- support thresholds;
- summary statistics;
- prohibited ranking/forecast/trading outputs;
- QC gates.

The canonical 014 `cash_carry_12m` remains the timing-convention cross-check.

## Research boundary

This is not a post-result specification change and must not be used to improve empirical outcomes. It only replaces a stalled transport path with the official monthly-average representation of the same federal-funds-rate concept.
