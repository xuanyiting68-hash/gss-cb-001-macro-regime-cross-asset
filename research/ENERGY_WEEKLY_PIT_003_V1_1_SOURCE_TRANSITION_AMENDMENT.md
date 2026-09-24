# ENERGY-WEEKLY-PIT-003 v1.1 — TWIP-to-WPSR Source-Transition Amendment
Date: 2026-09-24
Status: **FROZEN AFTER TIMING-SOURCE QC FAILURE / BEFORE ANY ENERGY OUTCOME EXECUTION**

## Trigger

The frozen v1 timing audit successfully reconstructed 1,241 official TWIP archive release dates and achieved 99.12% mapping coverage over the common EIA weekly physical grid, but failed one source-continuity assertion: TWIP itself does not extend through December 2025.

EIA discontinued This Week in Petroleum after the October 29, 2025 release. The underlying weekly petroleum data continue through the Weekly Petroleum Status Report (WPSR).

This is a source-regime change, not a research outcome.

## Amendment

Use one continuous official-information clock:

1. **TWIP era through week ending 2025-10-24**
   - release date encoded by the official EIA TWIP archive URL;
   - map to the common physical week-ending grid;
   - no assumed weekday.

2. **Post-TWIP WPSR era beginning week ending 2025-10-31**
   - default official WPSR release is the following Wednesday;
   - override with the official EIA WPSR holiday schedule whenever that week end appears in the schedule;
   - apply the same rule to 2026.

## Additional QC

- The 22 previously curated 2002-2023 event-scoped official release mappings must remain 22/22 exact matches.
- Post-TWIP rows must start strictly after the final TWIP week end.
- All post-TWIP 2025 week ends in the common physical grid must be covered.
- Overall 2002-2025 common-grid coverage remains >=95%.
- No energy price outcome is loaded.

## Unchanged

No change to:
- future event definition;
- physical/flow thresholds;
- price horizons;
- inferential family;
- deployment status.

## Evidence boundary

**TIMING-SOURCE AMENDMENT ONLY / BEFORE OUTCOME EXECUTION / NOT A FORECAST OR CAUSAL RESULT**
