# FED-CYCLE-RECOVERY-EXTENSION-015 v1.1 — Recovery Risk-Set Support Amendment
Date: 2026-09-24
Status: **POST-RUN SUPPORT-LABEL CORRECTION / METRICS UNCHANGED**

## 1. Trigger

The first 015 execution correctly computed drawdown/recovery paths, but inherited the 014 phase-cell support label from all available asset × anchor episodes.

Recovery estimation has a narrower risk set:

only episodes with a positive drawdown open a recovery clock.

Therefore support for a recovery statistic must be based on the positive-drawdown risk set, not the full phase cell.

This amendment changes evidence labeling only.

It does not change:
- drawdown values;
- trough dates;
- 50%/100% recovery definitions;
- Kaplan-Meier calculation;
- censoring;
- historical cycle boundaries;
- any outcome value.

## 2. Recovery risk-set support

For each asset × anchor:

`positive_drawdown_episodes`

= number of mechanical legs with drawdown > numerical tolerance.

`positive_drawdown_broad_episodes`

= number of broad episodes represented among those positive-drawdown legs.

### SUPPORTED_RECOVERY_DESCRIPTIVE
Require both:
- positive_drawdown_episodes >= 5;
- positive_drawdown_broad_episodes >= 4.

### LIMITED_RECOVERY_DESCRIPTIVE
Require:
- positive_drawdown_broad_episodes >= 2;
- but fail the supported threshold.

### INSUFFICIENT_RECOVERY_SUPPORT
- positive_drawdown_broad_episodes < 2.

## 3. Preserve phase-cell support

The existing 014-style `support_status` remains in outputs as the support for the underlying phase cell.

Add a distinct:

`recovery_support_status`

for recovery claims.

Do not use the broader phase-cell label to promote recovery evidence.

## 4. Expected implications

Without changing any numeric recovery estimate:

- TLT/VNQ/BTC remain limited recovery evidence;
- DXY remains supported recovery evidence because all relevant phase cells span >=7 broad episodes in the positive-drawdown risk set;
- housing recovery support may differ by phase:
  - FIRST_HIKE: expected limited;
  - LAST_HIKE: expected supported;
  - PAUSE_START: expected limited;
  - FIRST_CUT: expected limited.

## 5. Evidence boundary

**SUPPORT-LABEL CORRECTION ONLY / RECOVERY METRICS UNCHANGED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
