# FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010 — Closeout
Date: 2026-09-24
Status: **QC PASS / SOURCE TIMING REPAIR REQUIRED / NO NEW FORECAST EVIDENCE / NOT DEPLOYABLE**

## 1. Question

Can the exact OOS-008 Gold and real-time IPT input contract be used prospectively under SHADOW-009 while issuing the forecast before any part of the target month is observed?

## 2. Frozen requirement

For forecast month M:

- Gold features must use information through M-1;
- RT-IPT must follow the frozen M-2/M-14 same-vintage rule with vintage no later than M-1;
- the forecast must be issued before M begins;
- no source substitution is allowed inside this audit.

## 3. Gold source timing result

Recent uncensored monthly introductions audited: **6**.

All **6/6** required monthly Gold observations first appeared in the public `datasets/gold-prices` history only after the following month had already begun.

Observed release lag relative to the next-month start:

- minimum: **51.7 hours**;
- maximum: **107.7 hours**.

Audited observation months:

- 2026-02;
- 2026-03;
- 2026-05;
- 2026-06;
- 2026-07;
- 2026-08.

Every audited row fails the strict pre-target-availability rule.

Therefore:

**the exact historical OOS-008 Gold source contract is not live-transportable under the current no-target-observation issuance rule.**

This is an operational timing failure, not a forecast-performance failure.

## 4. Why the lag is economically meaningful

The modern Gold series is sourced from World Bank Commodity Markets.

The World Bank series defines Gold as London afternoon fixing / benchmark Gold, averaged across daily rates within the month.

The World Bank monthly commodity release is published after the relevant month has ended. The current public Commodity Markets page shows the latest August 2026 prices published on 2026-09-02 and the next update scheduled for 2026-10-02.

That publication convention is incompatible with using the completed M-1 World Bank monthly average in a forecast that must be locked before month M starts.

## 5. RTDSM current readiness

At audit time:

- next-month probe: 2026-10;
- required IPT observation: 2026-08;
- selected latest eligible workbook vintage: 2026-08;
- computed RT-IPT YoY available: **False**;
- workbook vintage count: 766;
- parsed cells: 477,136.

This is classified as:

`CURRENT_SOURCE_REFRESH_PENDING`

rather than a permanent structural failure because the Philadelphia Fed workbook can update later.

## 6. Public benchmark-source constraint

An exact same-definition daily Gold bridge is not trivial:

- FRED removed ICE Benchmark Administration / LBMA Gold Price daily series from its services in January 2022;
- LBMA states that IBA/LBMA benchmark use and redistribution can require licensing;
- historical benchmark tables were moved away from unrestricted public tables in late 2025, while delayed daily display remains available subject to benchmark-use terms.

Therefore the project must not silently reconstruct the World Bank Gold monthly benchmark from an assumed free LBMA feed.

## 7. Research consequence

OOS-008 remains:

**PRELIMINARY OOS CANDIDATE / WEAK AND BENCHMARK-SENSITIVE / NOT DEPLOYABLE.**

SHADOW-009 remains:

**ARMED / ZERO PROSPECTIVE PREDICTIONS.**

No B08 forecast can be issued under the exact historical input contract until a separate timing repair is frozen.

## 8. Next research step

Freeze a separate **Gold live-source bridge audit**.

The first candidate may use a public, already-supported market proxy such as continuous COMEX Gold futures (`GC=F`) with raw bytes not committed.

That bridge must be tested only for feature-transport equivalence:

- monthly price aggregation;
- 3M return;
- 6M return;
- 6M volatility;
- sign and magnitude agreement;
- era stability.

It must not test forecast outcomes or retune M3.

Even if such a proxy passes engineering-equivalence gates, it is a **new prospective measurement specification** and does not automatically inherit OOS-008's historical OOS evidence.

## 9. Evidence boundary

**DATA/TIMING FACT / SOURCE-TRANSPORT FAILURE / NO CAUSAL CLAIM / NO FORECAST PERFORMANCE CLAIM / NOT DEPLOYABLE**
