# ENERGY-WEEKLY-PIT-003 — Full WPSR Release-Clock Registry Lock
Date: 2026-09-24
Status: **FROZEN BEFORE FULL-REGISTRY EXECUTION**

## 1. Purpose

Build a full historical point-in-time event clock for weekly U.S. petroleum data before any new weekly/daily energy outcome study.

The core object is:

`week_end -> actual WPSR release_date`

A weekly observation period is not treated as publicly available until its corresponding official EIA release date.

## 2. Official sources

Primary:

- EIA This Week in Petroleum / Weekly Petroleum Status Report historical archive, 2002-2025;
- EIA official WPSR release schedule for 2026, including holiday exceptions.

Cross-check physical week-ending dates against official EIA weekly historical series:

- WCESTUS1 — commercial crude stocks excluding SPR;
- WGTSTUS1 — total motor gasoline stocks;
- WDISTUS1 — distillate fuel oil stocks;
- WPULEUS3 — refinery utilization.

Raw official downloads are hashed but not committed.

## 3. Historical parser

For 2002-2025:

- parse the year/month release tables exposed on the official EIA weekly petroleum page;
- preserve explicit release date and week-ending date;
- do not impose a universal Wednesday assumption;
- January release rows pointing to prior-December week-ending dates must retain the correct prior year.

For 2026:

- standard release is the Wednesday after the Friday week end;
- scrape the official holiday release schedule and override standard dates when the week-ending date appears in that table.

No manually curated event outcome is consulted.

## 4. Frozen QC

The registry is accepted only if:

- at least 1,200 unique week-ending rows are reconstructed for 2002-2025;
- earliest week end is in calendar year 2002;
- latest 2002-2025 week end is in December 2025;
- no duplicate week-ending dates;
- no duplicate release-date/week-end pairs;
- every release occurs strictly after its week end;
- release lag is between 3 and 12 calendar days;
- median release lag is between 5 and 6 days;
- at least 95% of common 2002-2025 physical-series week-ending dates map to the release registry;
- every mapped week-end agrees exactly across the four physical series' date grids.

2026 coverage is descriptive because the year is incomplete.

## 5. Gap audit

Report:

- release-lag distribution;
- week-ending gap distribution;
- missing physical week ends not represented in the release registry;
- release-registry rows not represented across the common physical grid;
- holiday-shifted releases with lag >5 days.

Large unexplained gaps are preserved rather than imputed.

## 6. No outcomes

This module must not load forward WTI returns, event classifications or future outcome variables.

It is pure timing/provenance infrastructure.

## 7. Downstream rule

Only a QC-passed full release registry may be used by the new weekly/daily strict-PIT energy event engine.

If the full parser fails, downstream weekly confirmation work remains blocked until the clock is repaired.

## 8. Evidence boundary

**DATA TIMING / RELEASE-CLOCK INFRASTRUCTURE / NO FORECAST OR CAUSAL EVIDENCE / NOT DEPLOYABLE**
