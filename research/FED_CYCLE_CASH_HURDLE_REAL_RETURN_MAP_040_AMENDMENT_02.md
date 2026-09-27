# FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040 — AMENDMENT 02

Date: 2026-09-27
Type: reproducibility / acquisition transport amendment
Status: post-lock, after repeated GitHub-hosted runner network stalls

## Trigger

Three GitHub Actions diagnostic runs reached the 040 script step but stalled on external FRED HTTP acquisition. The failure mode is external transport/runtime dependence, not a research-QC failure.

An independent audit had already computed the frozen formulas before this amendment. Therefore this amendment is deliberately constrained to transport and provenance only; it does not authorize changing any observed value to improve a result.

## Change

Freeze the exact 37 canonical phase × cycle event inputs needed by 040 into:

`data/public/CASH_HURDLE_REAL_RETURN_EVENT_INPUTS_20260927.csv`

Each row contains:
- canonical anchor / cycle / broad-episode identity;
- anchor month;
- official monthly FEDFUNDS value;
- frozen baseline and endpoint CPIAUCSL values;
- FRED source URLs;
- vintage note.

The values are transcribed from the official FRED published monthly tables captured on 2026-09-27.

The runner must:
1. hash the frozen event-input file;
2. validate exactly the 37 canonical event keys;
3. validate that baseline = anchor month - 1 and endpoint = anchor month + 12;
4. combine the frozen anchor-month FEDFUNDS value with canonical 014 post12 cash carry:
   `matched_cash = (1 + cash014_post12) * (1 + FEDFUNDS_anchor/100/12) - 1`;
5. compute matched CPI inflation:
   `CPI_endpoint / CPI_baseline - 1`.

This is algebraically the same matched cash grid frozen in the lock because canonical 014 already compounds months t+1..t+12 and the added official monthly rate supplies month t.

## Unchanged

No change to asset/phase samples, event dates, episode weights, return/MDD inputs, formulas, evidence tiers, thresholds, support labels, interpretation rules, or prohibited outputs.

## Provenance boundary

The event-input table is a small public-safe derived/transcribed dataset, not redistributed bulk vendor data.

FRED remains the authoritative source:
- FEDFUNDS: https://fred.stlouisfed.org/series/FEDFUNDS
- CPIAUCSL: https://fred.stlouisfed.org/series/CPIAUCSL

Current-vintage CPI remains ex-post and must not be described as point-in-time policy information.
