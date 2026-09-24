# FED-CYCLE-GOLD-OOS-008 — Post-Run Benchmark Sanity Audit
Date: 2026-09-24
Status: **POST-RUN DIAGNOSTIC / DOES NOT CHANGE THE FROZEN OOS GATE**

## Trigger

OOS-008 passes its predeclared gate because M3:

- lowers episode-equal MSE versus B2;
- beats B2 in 3/4 OOS broad episodes;
- has positive OOS R² versus B0.

The B2 benchmark itself performs poorly versus the historical-mean B0 benchmark.

Therefore a post-run sanity audit is required so the final interpretation does not cherry-pick only the most favorable comparator.

## Fixed readback diagnostics

Using already committed OOS predictions and metrics only, with no refitting:

1. compare M3 to B0 on MSE and MAE:
   - aggregate episode-equal metric difference;
   - number of episode wins;
2. compare M3 to B1 Gold-history benchmark;
3. compare M3 to D4 current-vintage diagnostic;
4. report episode-equal signed forecast bias;
5. report M3 prediction range versus realized target range.

No model, feature, fold, target, or evidence gate is changed.

## Interpretation

The frozen evidence label remains mechanically determined by the preregistered gate.

This sanity audit controls the language used in the closeout:

- if M3 barely beats B0 or is metric-sensitive, describe the OOS value as weak/preliminary;
- do not promote a large percentage improvement versus a poor benchmark into a strong forecasting claim.
