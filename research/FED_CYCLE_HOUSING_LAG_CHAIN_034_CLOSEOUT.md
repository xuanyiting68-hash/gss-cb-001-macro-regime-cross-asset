# FED-CYCLE-HOUSING-LAG-CHAIN-034 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / HOUSING FINANCING-ACTIVITY-PRICE LAG MAP / POST-RUN ORDERING AUDIT / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

034 extends the canonical national house-price results with financing and housing-activity context while preserving the slow-moving housing clock.

## Data architecture

Canonical house-price outcomes are copied exactly from 014/015:
- CSUSHPINSA
- 6M / 12M / 24M price change
- DECLINE_24M
- trough month
- recovery timing where observed

New public source snapshots:
- MORTGAGE30US — Freddie Mac 30Y fixed mortgage rate
- DGS10 — 10Y Treasury yield
- HOUST — housing starts
- PERMIT — building permits
- HSN1F — new one-family home sales

The source registry freezes retrieval timestamps and raw SHA256 hashes.

Raw source histories are not committed.

## Frozen transformation

Financing:
- calendar-month mean
- baseline = M-1
- +3/+6/+12/+24m changes in percentage points

Housing activity:
- official monthly SAAR
- trailing 3-month average
- baseline = trailing 3M average ending M-1
- +3/+6/+12/+24m changes
- trough/peak within 0..24m

House price:
- canonical 014/015 values only
- no recomputation
- path-risk metric remains DECLINE_24M

## Core phase results

### FIRST_HIKE

- 30Y mortgage 12M median change: +1.14pp
- forward mortgage pressure month median: M12
- cycle-window absolute mortgage peak median: M11
- cycle mortgage peak before-or-same as activity trough: 67%
- PERMIT 12M: -3.9%, trough M13
- HOUST 12M: -0.1%, trough M15
- new-home sales 12M: -6.7%, trough M12
- Case-Shiller 12M / 24M: +5.3% / +11.8%
- median 24M price decline: ~0%

Interpretation:
Housing activity can weaken materially while the national price index remains positive. The 2022 episode makes this especially visible.

### LAST_HIKE

- mortgage 12M: -1.01pp
- cycle-window mortgage peak median: M0
- mortgage peak before-or-same as activity trough: 100%
- PERMIT 12M: -4.3%, trough M18
- HOUST 12M: -6.7%, trough M12
- new-home sales 12M: +5.2%, trough M2
- house price 12M / 24M: +3.5% / +7.3%
- positive-decline price trough median: M17

Interpretation:
By LAST_HIKE, financing rates can already be turning down while starts/permits remain weak much later.

### PAUSE_START

- mortgage 12M: -1.01pp
- cycle-window mortgage peak median: M-1
- mortgage peak before-or-same as activity trough: 100%
- PERMIT 12M: -0.3%, trough M17
- HOUST 12M: -4.4%, trough M10
- new-home sales 12M: +3.6%, trough M1
- house price 12M / 24M: +3.8% / +5.5%

Interpretation:
Different activity measures can diverge materially. A pause is not the moment all housing indicators bottom together.

### FIRST_CUT

- mortgage 12M: -0.53pp
- preregistered forward-window mortgage-pressure median: M11
- cycle-window absolute mortgage peak median: M-7
- cycle mortgage peak before-or-same as activity trough: 100%
- PERMIT 12M: +3.9%, trough M11
- HOUST 12M: +0.6%, trough M10
- new-home sales 12M: +2.8%, trough M9
- house price 12M / 24M: +5.2% / +12.7%

The M11 forward-window pressure statistic must not be interpreted as the cycle mortgage peak. The post-run anchor-reset audit shows the absolute mortgage-rate peak is typically before the FIRST_CUT anchor.

## Paired ordering evidence

The first run showed that subtracting phase-level median months can misrepresent the actual episode ordering.

Therefore a transparent post-run diagnostic was added without overwriting the preregistered results.

### Cycle mortgage peak before-or-same as activity trough
Episode-weighted shares:
- FIRST_HIKE: 67%
- LAST_HIKE: 100%
- PAUSE_START: 100%
- FIRST_CUT: 100%

### Activity trough before-or-same as house-price trough
Restricted to episodes with positive 24M house-price decline:
- FIRST_HIKE: 71%
- LAST_HIKE: 77%
- PAUSE_START: 75%
- FIRST_CUT: 57%

Therefore the broad financing-before-activity ordering is relatively common in this sample, especially later in the tightening cycle, but activity-before-price is not a deterministic law.

The ordering diagnostics remain descriptive; they are not causal transmission estimates.

## B05 versus B07

### B05 — 2004-07 tightening / housing bust

At FIRST_HIKE in 2004:
- house price still rose +16.0% at 12M and +24.4% at 24M;
- activity weakness had not yet become a national price bust.

By LAST_HIKE / PAUSE / FIRST_CUT:
- activity measures had deteriorated deeply;
- house-price 24M paths turned sharply negative;
- FIRST_CUT 2007 house-price 12M ~ -10.2%, 24M ~ -17.0%;
- canonical 24M decline ~18.7%.

The housing bust was a long process, not an immediate FIRST_HIKE response.

### B07 — 2022-23 tightening / price resilience

At FIRST_HIKE 2022:
- mortgage 12M change ~ +2.78pp;
- mortgage max increase within 24m ~ +3.86pp;
- PERMIT 12M ~ -20.5%;
- HOUST 12M ~ -19.8%;
- new-home sales 12M ~ -20.1%;
- national house price 12M still ~ +3.6%;
- national house price 24M ~ +10.4%;
- canonical 24M decline only ~5.0%.

This is a strong descriptive counterexample to a simple “higher mortgage rates mechanically imply immediate national house-price collapse” rule.

It does not identify which supply, inventory, lock-in or composition channels caused the resilience.

## Recovery

The existing 015 recovery layer remains authoritative.

Recovery evidence is conditional on episodes that actually experienced positive declines.

Support differs by phase; it is not appropriate to interpret the phase-level price medians as universal recovery times.

## Post-run diagnostic amendment

The amendment adds:
- episode-level weighted ordering shares;
- absolute mortgage-rate peak in [-12,+24] months;
- paired activity/price timing.

It is explicitly labeled:
`POST_RUN_DIAGNOSTIC__ANCHOR_RESET_AUDIT`

The original preregistered forward-window metrics remain unchanged.

## Reproducibility

Final authoritative workflow:
- run id: `36214958919`
- source commit: `4a5b330f1c9355e8ef9ba9cbb796a8cfb917a498`
- output commit: `2c910b348ba175d52c8cc342471119c7ce7de7da`
- result: SUCCESS

The earlier successful run `36214787413` is superseded for sequencing interpretation by the post-run diagnostic amendment.

## QC

- canonical anchors: 28
- current 2026 candidate leaks: 0
- public downloaded source series: 5
- source SHA256 complete: true
- mortgage methodology change retained: true
- trailing-3M activity transform: true
- baseline: M-1
- interpolation: false
- canonical house-price summary exact match: true
- path-risk metric: DECLINE_24M
- financing event rows: 84
- activity event rows: 84
- lag-chain rows: 28
- phase summary rows: 4
- B05/B07 audit rows: 7
- investor questions: 15
- paired ordering from episode rows: true
- preregistered primary metrics overwritten: false
- causal lag claim: false
- house-price forecast: false
- home-buying recommendation: false
- new p-values: false
- private-paper inputs: false
- causal status: NONE
- OOS: NOT_A_FORECASTING_MODEL
- deployment: NOT_DEPLOYABLE

## Next research gap

The next high-value cross-asset gap is long-duration bonds.

TLT begins only in 2002, leaving the current 014/032 TLT evidence at three episodes.

A next module should test whether a longer-history, public long-duration Treasury proxy can be bridged to TLT without silently inheriting ETF evidence.
