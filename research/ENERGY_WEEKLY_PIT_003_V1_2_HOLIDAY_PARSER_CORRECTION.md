# ENERGY-WEEKLY-PIT-003 v1.2 — Holiday-Schedule Parser Correction
Date: 2026-09-24
Status: **POST-RUN TIMING DEFECT CORRECTION / BEFORE ANY DOWNSTREAM OUTCOME EXECUTION**

## Trigger

The v1.1 source-transition run passed its original computational gates, but post-run readback showed:

`schedule_exception_rows_2025_2026 = 0`

This contradicts the official EIA WPSR schedule, which explicitly lists holiday-shifted releases in both 2025 and 2026.

Therefore the v1.1 PASS is not accepted as the final timing registry.

## Root cause

The holiday parser's generated regular expression was over-escaped and did not recognize official schedule date cells.

No price outcome or event classification was inspected in discovering this defect.

## Correction

Parse official schedule date cells with generic date conversion and require explicit known official anchors.

Hard anchors:

- week ending 2025-11-07 -> release 2025-11-13;
- week ending 2025-12-19 -> release 2025-12-29;
- week ending 2026-09-04 -> release 2026-09-10.

Also require at least 10 official holiday-exception rows across the 2025-2026 schedule.

## Unchanged

No change to:
- TWIP archive release dates;
- common weekly physical grid;
- future event definition;
- physical/flow rules;
- outcome horizons;
- statistical tests.

## Evidence boundary

**TIMING QC CORRECTION ONLY / NO OUTCOME EVIDENCE / v1.1 PASS QUARANTINED**
