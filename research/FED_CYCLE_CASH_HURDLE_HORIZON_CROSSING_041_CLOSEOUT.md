# FED-CYCLE-CASH-HURDLE-HORIZON-CROSSING-041 — CLOSEOUT

Status: **QC PASS / DISCRETE-HORIZON OPPORTUNITY-COST MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**.

The frozen 3M/6M/12M design has 232 asset-event rows, 696 horizon rows, 32 asset-phase summaries and 256 asset-phase-pattern rows (all eight bit patterns, including zero-share cells). All five upstream modules pass QC. The 12M matched cash and asset-vs-cash results reproduce 040 within 1e-12, and the 12M boolean flags match exactly. All 37 frozen macro event keys are present; asset identity, episode weights and evidence tiers are preserved. No external source download occurs.

## Findings with scope

- Across 232 historical asset-event rows, 3M has 133 positive nominal endpoints and 18 of those remain below matched cash; 6M has 138 positive nominal endpoints and 27 remain below matched cash; 12M has 136 positive nominal endpoints and 30 remain below matched cash.
- The observed-horizon pattern counts are 000: 87, 001: 11, 010: 5, 011: 14, 100: 19, 101: 4, 110: 15, 111: 77. Thus 25 rows fail at 3M but beat cash at 12M; 39 rows beat cash at 3M or 6M but fail at 12M. These overlapping asset-event rows are not independent tests.
- Nasdaq FIRST_CUT weighted median relative to cash is approximately +2.5% at 3M, -2.2% at 6M and -3.4% at 12M, an example of endpoint-horizon sensitivity. This is a descriptive conditional historical median, not an investable phase rule.
- VUSTX_LONG_TREASURY_PROXY FIRST_HIKE weighted median relative to cash is approximately -3.8%, -5.4%, -3.6% at 3M/6M/12M respectively. Proxy identity is explicit and historical medians are not forecasts.
- VGSIX_REIT_PROXY remains LIMITED_PROXY_DESCRIPTIVE and BTC_USD remains LIMITED_DESCRIPTIVE. A pattern statistic does not improve their underlying sample support.

The bit patterns observe only three fixed horizons. `first_observed_beating_horizon` and `last_observed_below_cash_horizon` cannot locate a crossover between endpoints. Mechanical federal-funds cash excludes deposit spread, tax and fees. Phase labels condition the comparison; they are not identified policy shocks. No new p-values, horizon optimization, ranking, allocation weights or trading instruction were produced.

Canonical artifacts: `scripts/run_fed_cycle_cash_hurdle_horizon_crossing_041_v1.py`, `.github/workflows/fed-cycle-cash-hurdle-horizon-crossing-041-v1.yml`, and `results/fed_cycle_cash_hurdle_horizon_crossing_041_v1/`.
