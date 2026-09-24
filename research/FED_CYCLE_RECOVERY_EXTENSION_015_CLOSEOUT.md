# FED-CYCLE-RECOVERY-EXTENSION-015 — Closeout
Date: 2026-09-24
Status: **QC PASS / RECOVERY RISK-SET SUPPORT CORRECTED / DESCRIPTIVE / NOT CAUSAL**

## 1. Purpose

Extend PHASE-CLOCK-004 drawdown/recovery accounting to:
- TLT;
- VNQ;
- BTC_USD;
- DXY;
- U.S. national house prices.

The 2026 live cycle is excluded.

## 2. Recovery definition

Liquid assets:
- 12M drawdown-identification window;
- prior-peak-to-trough maximum drawdown;
- 50% recovery = half the peak-to-trough loss repaired;
- 100% recovery = return to the prior peak;
- search up to 60 months from trough;
- right-censor if not recovered.

Housing:
- same logic using the frozen 24M housing drawdown window.

## 3. QC

- 68 liquid-market recovery rows;
- 28 housing recovery rows;
- exact reproduction of 014 MDD/decline values;
- exact reproduction of 014 trough months;
- zero recovery-order violations;
- zero 2026 leakage;
- zero support-label violations;
- raw source histories not committed.

QC: **PASS**.

## 4. v1.1 support correction

The initial 015 output inherited the full phase-cell support label.

Post-run audit correctly identified that recovery evidence must be supported by the narrower positive-drawdown risk set.

v1.1 therefore adds:
- positive_drawdown_episodes;
- positive_drawdown_broad_episodes;
- recovery_support_status.

Recovery values are unchanged.

## 5. DXY — supported recovery evidence

All four DXY phase cells retain 7 broad episodes in the positive-drawdown risk set.

Weighted KM full-recovery medians:
- FIRST_HIKE: **11 months**;
- LAST_HIKE: **12 months**;
- PAUSE_START: **8 months**;
- FIRST_CUT: **6 months**.

50% recovery:
- FIRST_HIKE 6m;
- LAST_HIKE 4m;
- PAUSE_START 4m;
- FIRST_CUT 5m.

Right-censoring remains material in several cells.

Interpretation:
the dollar-index proxy usually repairs half of a phase drawdown within several months, but full prior-peak recovery can take much longer and is not monotonic across cycle phases.

## 6. TLT — limited but economically interesting

Recovery support is limited to 3 broad episodes.

Full-recovery KM medians:
- FIRST_HIKE: **30m**;
- LAST_HIKE: **3m**;
- PAUSE_START: **2m**;
- FIRST_CUT: **3m**.

The contrast is large, but cannot be promoted beyond LIMITED_RECOVERY_DESCRIPTIVE.

Episode detail matters:
- 2022 FIRST_HIKE remains right-censored within current support;
- 2015 FIRST_HIKE took 30m to full recovery;
- 2004 FIRST_HIKE recovered much faster.

## 7. VNQ — limited listed-REIT recovery

Recovery support is limited to 2-3 broad episodes.

Full-recovery medians:
- FIRST_HIKE 21m;
- LAST_HIKE 2m;
- PAUSE_START 2m;
- FIRST_CUT 12m.

This suggests a potentially important rate-cycle asymmetry, but the history is too short for a stable rule.

## 8. BTC — limited

Only two broad episodes exist.

Full-recovery medians are 2-4 months across the four phase labels.

This fast recovery statistic coexists with very large drawdowns, including roughly 59% in the 2022 FIRST_HIKE path.

Therefore recovery speed must not be read without drawdown depth.

## 9. Direct housing

Phase-cell support is broad, but recovery support differs because many historical housing phase paths had essentially no drawdown.

### Supported recovery cell
LAST_HIKE:
- 5 positive-drawdown episodes / 5 broad episodes;
- 50% recovery median 2m;
- 100% recovery median 3m;
- 1 right-censored case.

### Limited recovery cells
FIRST_HIKE:
- 4 positive-drawdown episodes / 4 broad;
- full recovery median 2m.

PAUSE_START:
- 4 / 4;
- full recovery median 2m.

FIRST_CUT:
- only 3 / 3;
- 50% recovery median 4m;
- full recovery median **28m**;
- one right-censored case.

The 28m FIRST_CUT figure is economically important but must remain LIMITED_RECOVERY_DESCRIPTIVE.

## 10. Integrated implication

Recovery speed is not a simple monotonic function of policy easing.

Across the better-supported 004 core assets and the supported 015 cells:
- equities often recover more quickly around LAST_HIKE/PAUSE than FIRST_CUT;
- Gold FIRST_HIKE recovery is slow;
- WTI LAST_HIKE recovery is slow;
- DXY full recovery remains multi-month across all phases;
- national housing can exhibit very long recovery tails around recession-associated first-cut episodes even when the cross-cycle median price path is positive.

## 11. Boundary

**DESCRIPTIVE RECOVERY CLOCK / RIGHT-CENSORING PRESERVED / SUPPORT-LABELED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
