# Content Card — Real Yield、USD、Oil 到底谁在主导 Gold？
Content ID: FED_CYCLE_STATE_CONTENT_003
Evidence: FED-CYCLE-STATE-001
Status: **PUBLIC-SAFE / DESCRIPTIVE-ASSOCIATIONAL ONLY / NOT A DRIVER RANKING**

## Hook

“同样是美联储加息，为什么黄金有时涨、有时跌？到底是 Real Yield、美元还是油价在主导？”

现在这组长历史研究给出的答案是：

**还不能排出一个‘主导者’。**

## What the data can currently distinguish

FIRST_HIKE sample = 10 mechanical tightening legs.

### Inflation level

HIGH CPI (>3%), n=5:
- Gold +12M median **-11.76%**
- 24M MDD median **22.54%**

LOW_OR_MODERATE, n=5:
- +12M **+6.54%**
- MDD **13.66%**

The contrast keeps the same sign under leave-one-leg-out checks.

But CPI history is current-vintage, not strict ALFRED PIT.

### Inflation direction

RISING, n=7:
- +12M **+3.07%**
- MDD **14.09%**

FALLING_OR_FLAT, n=3:
- +12M **-11.76%**
- MDD **19.91%**

So “inflation high” and “inflation rising” are not the same state.

### WTI direction

RISING, n=5:
- +12M Gold median **+3.62%**

FALLING_OR_FLAT, n=3:
- **-2.58%**

This is only a mechanism candidate, not evidence that oil causes Gold to rise.

## Why Real Yield cannot be ranked yet

- 10Y nominal-minus-CPI real-rate proxy: **9 positive vs 1 nonpositive**
- actual 10Y TIPS real yield `DFII10`: only **3** FIRST_HIKE observations

There is not enough cross-event support to estimate a long-history real-yield state contrast.

## Why the USD result is a trap

USD source bridge passes with **95.74%** six-month direction agreement and the FIRST_HIKE split is 5:5.

Naively:

- USD RISING group +12M Gold median: **+3.62%**
- USD FALLING/FLAT: **-11.76%**

But:

- all FALLING/FLAT cases are **1983-1988**
- all RISING cases are **1994-2022**

That is **perfect era separation**.

So this cannot be sold as “USD up = Gold up.” The USD label is entangled with historical era.

## Safe conclusion

**NOT YET VERIFIED:** Real Yield, USD and Oil cannot currently be ranked as the dominant post-hike Gold driver.

**MECHANISM CANDIDATES:** inflation level/direction, growth and energy direction deserve a better-powered within-cycle panel test.

## Mandatory disclosure

- 10 FIRST_HIKE legs only;
- no causal identification;
- no raw p-values;
- FDR not run;
- OOS not applicable;
- current-vintage CPI/INDPRO/NFCI are not strict PIT vintages;
- USD contrast is era-confounded;
- real-yield support is insufficient;
- not a trading signal.

## Evidence files

- `research/FED_CYCLE_STATE_001_LOCK.md`
- `results/fed_cycle_state_v1/STATE_EVENT_PANEL.csv`
- `results/fed_cycle_state_v1/STATE_CONTRASTS.csv`
- `results/fed_cycle_state_v1/STATE_LOO_STABILITY.csv`
- `results/fed_cycle_state_v1/STATE_TEMPORAL_CONFOUNDING_AUDIT.csv`
- `research/FED_CYCLE_STATE_001_CLOSEOUT.md`
