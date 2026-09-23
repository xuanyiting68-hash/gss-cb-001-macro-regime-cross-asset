# P0-A v3 — Public Statistical Re-Audit Protocol
Date: 2026-09-23
Status: RE-AUDIT SPECIFICATION / PUBLIC-SAFE SUMMARY

## Why the re-audit was necessary

Earlier work had already repaired several implementation issues and reproduced the same numerical outputs, but code-level review found that computational replication alone did not guarantee valid inference.

The public re-audit therefore addresses four core problems:

1. bootstrap p-values must be generated under the null rather than from an uncentered resampling distribution;
2. HAC/Newey–West inference must be computed on the full chronological panel;
3. regime returns should be compared with unconditional Gold drift rather than only with zero;
4. Gold horizon definitions require a weekday robustness check because the research feed includes non-standard observation days.

## Primary estimand

For each regime and horizon:

`regime excess = E[forward return | regime] - E[forward return]`

This is the key investment-relevant question: does the regime add information beyond Gold's unconditional drift?

## Confirmatory families

### Family A
8 regimes × 3 horizons = 24 regime-excess tests.

BH-FDR at 10%.

### Family B
Effect-coded factorial model with seven non-intercept terms across 3 horizons:

- Real Yield
- Broad USD
- Oil
- RY × USD
- RY × Oil
- USD × Oil
- RY × USD × Oil

21 tests, BH-FDR at 10%.

## Dependence-aware inference

Primary:
- chronological OLS;
- HAC covariance;
- horizon-linked lag rules.

Bootstrap robustness:
- resample contiguous chronological blocks;
- explicitly impose the null for bootstrap p-values;
- do not compress calendar time by concatenating only observations from one regime.

## Horizon robustness

Primary public convention:
- weekday/market-day observations;
- 5 / 20 / 60 observation horizons.

Robustness:
- original observation calendar;
- explicitly label those as observation-step horizons.

## Current audited result

The 2026-09-23 re-audit found:

- 0/24 regime-excess tests survived BH-FDR 10%;
- weekday robustness also produced 0/24;
- 0/21 non-intercept factorial terms survived BH-FDR;
- null block-bootstrap family produced 0/24 confirmed results.

Some Oil-down and individual regime patterns remain descriptively interesting, but they do not constitute confirmatory evidence.

## Current classification

**DESCRIPTIVELY INTERESTING / CONFIRMATORY EVIDENCE INSUFFICIENT / NOT DEPLOYABLE**

## Deployment rule

No trading/deployment claim unless the research also passes:

- multiple-testing gate;
- economically meaningful excess over unconditional drift;
- subperiod stability;
- non-overlap robustness;
- walk-forward OOS;
- realistic signal timing;
- turnover/cost/risk evaluation.

This public repository does not distribute the underlying vendor research feed.
