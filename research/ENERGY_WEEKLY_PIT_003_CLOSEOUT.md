# ENERGY-WEEKLY-PIT-003 — Closeout
Date: 2026-09-24
Status: **QC PASS / FULL STRICT-PIT RELEASE CLOCK / NO OUTCOME EVIDENCE / NOT DEPLOYABLE**

## Result

A full official EIA weekly petroleum release clock is now available for 2002-2026.

Final accepted registry:
- 1,250 historical rows for 2002-2025;
- 1,288 rows total through 2026-09-18;
- 0 duplicate week ends;
- 0 invalid release lags;
- release lag range 5-10 days;
- median release lag 5 days;
- 99.84% mapping coverage of the common four-series physical grid;
- 22/22 previously curated event-scoped release mappings reproduced exactly;
- 14 official 2025-2026 holiday exceptions parsed;
- all three hard holiday anchors pass;
- 2025 post-TWIP WPSR coverage = 100%.

Two common physical week ends remain unmapped and are preserved as gaps rather than imputed.

## Source-transition correction

The initial requirement that TWIP extend through December 2025 was invalid because EIA ended TWIP after the 2025-10-29 release.

v1.1 therefore froze the official source transition:
- TWIP through week ending 2025-10-24;
- WPSR schedule thereafter.

## Holiday-parser correction

The first post-transition run failed to parse official holiday exceptions because of an over-escaped date parser.

v1.2 corrected only the schedule parser before downstream outcome execution.

The final accepted registry explicitly reproduces:
- 2025-11-07 -> 2025-11-13;
- 2025-12-19 -> 2025-12-29;
- 2026-09-04 -> 2026-09-10.

## Research consequence

Weekly petroleum observations can now be treated as available on their actual release date rather than their week-ending date.

This removes a major look-ahead risk from subsequent weekly/daily energy-state research.

## Boundary

**TIMING / PROVENANCE INFRASTRUCTURE ONLY / NO FORECAST PERFORMANCE / NOT CAUSAL / NOT DEPLOYABLE**
