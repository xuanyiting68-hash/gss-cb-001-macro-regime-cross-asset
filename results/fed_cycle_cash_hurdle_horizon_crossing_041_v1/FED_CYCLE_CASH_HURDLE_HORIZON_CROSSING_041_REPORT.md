# 041 Cash-hurdle horizon crossing — report

**QC PASS / DISCRETE 3M–6M–12M DESCRIPTIVE / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

The observed three endpoints do not identify the month of an intervening cash-hurdle crossover. Asset and phase rows remain in frozen order; limited sample tiers are unchanged.

## Whole-panel diagnostics

- 3M: 133 positive nominal event rows; 18 positive nominal rows still below matched cash (out of 232 asset-event rows; overlapping rows are not independent observations).
- 6M: 138 positive nominal event rows; 27 positive nominal rows still below matched cash (out of 232 asset-event rows; overlapping rows are not independent observations).
- 12M: 136 positive nominal event rows; 30 positive nominal rows still below matched cash (out of 232 asset-event rows; overlapping rows are not independent observations).

## Fixed-order asset × phase examples

- GOLD / FIRST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -1.2%, 6M -4.0%, 12M -2.4%; 000 share 48%, 111 share 33%, late improvement 14%, early advantage lost 5%.
- GOLD / LAST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -3.1%, 6M -2.7%, 12M -8.2%; 000 share 48%, 111 share 14%, late improvement 29%, early advantage lost 10%.
- GOLD / PAUSE_START [CORE_SUPPORTED; 7 legs, 7 broad episodes]: cash-relative weighted medians 3M -2.5%, 6M -1.8%, 12M -1.3%; 000 share 43%, 111 share 29%, late improvement 0%, early advantage lost 29%.
- GOLD / FIRST_CUT [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -3.2%, 6M +1.8%, 12M -0.0%; 000 share 48%, 111 share 43%, late improvement 0%, early advantage lost 10%.
- SP500 / FIRST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -2.9%, 6M -0.0%, 12M +2.5%; 000 share 33%, 111 share 14%, late improvement 36%, early advantage lost 12%.
- SP500 / LAST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M +0.4%, 6M +6.5%, 12M +10.9%; 000 share 26%, 111 share 55%, late improvement 14%, early advantage lost 5%.
- SP500 / PAUSE_START [CORE_SUPPORTED; 7 legs, 7 broad episodes]: cash-relative weighted medians 3M +6.3%, 6M +12.5%, 12M +13.2%; 000 share 14%, 111 share 71%, late improvement 0%, early advantage lost 14%.
- SP500 / FIRST_CUT [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M +0.1%, 6M +1.0%, 12M +2.1%; 000 share 31%, 111 share 48%, late improvement 7%, early advantage lost 14%.
- NASDAQ / FIRST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -6.6%, 6M -4.6%, 12M -0.8%; 000 share 40%, 111 share 19%, late improvement 29%, early advantage lost 12%.
- NASDAQ / LAST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -1.0%, 6M +5.1%, 12M +9.2%; 000 share 26%, 111 share 36%, late improvement 29%, early advantage lost 10%.
- NASDAQ / PAUSE_START [CORE_SUPPORTED; 7 legs, 7 broad episodes]: cash-relative weighted medians 3M +7.5%, 6M +15.3%, 12M +16.6%; 000 share 14%, 111 share 71%, late improvement 0%, early advantage lost 14%.
- NASDAQ / FIRST_CUT [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M +2.5%, 6M -2.2%, 12M -3.4%; 000 share 31%, 111 share 43%, late improvement 7%, early advantage lost 19%.
- WTI / FIRST_HIKE [CORE_SUPPORTED; 8 legs, 6 broad episodes]: cash-relative weighted medians 3M +14.8%, 6M +14.6%, 12M +17.8%; 000 share 6%, 111 share 56%, late improvement 22%, early advantage lost 17%.
- WTI / LAST_HIKE [CORE_SUPPORTED; 8 legs, 6 broad episodes]: cash-relative weighted medians 3M +6.4%, 6M -3.9%, 12M -0.7%; 000 share 28%, 111 share 33%, late improvement 0%, early advantage lost 22%.
- WTI / PAUSE_START [CORE_SUPPORTED; 6 legs, 6 broad episodes]: cash-relative weighted medians 3M -13.2%, 6M -5.4%, 12M -10.4%; 000 share 50%, 111 share 17%, late improvement 17%, early advantage lost 17%.
- WTI / FIRST_CUT [CORE_SUPPORTED; 8 legs, 6 broad episodes]: cash-relative weighted medians 3M -5.4%, 6M -0.5%, 12M -24.3%; 000 share 50%, 111 share 17%, late improvement 17%, early advantage lost 17%.
- DXY / FIRST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -2.7%, 6M -4.6%, 12M -2.5%; 000 share 52%, 111 share 14%, late improvement 21%, early advantage lost 12%.
- DXY / LAST_HIKE [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M -0.3%, 6M -3.2%, 12M -8.1%; 000 share 55%, 111 share 14%, late improvement 0%, early advantage lost 31%.
- DXY / PAUSE_START [CORE_SUPPORTED; 7 legs, 7 broad episodes]: cash-relative weighted medians 3M -2.2%, 6M -2.6%, 12M -7.5%; 000 share 71%, 111 share 0%, late improvement 0%, early advantage lost 14%.
- DXY / FIRST_CUT [CORE_SUPPORTED; 10 legs, 7 broad episodes]: cash-relative weighted medians 3M +0.3%, 6M -0.8%, 12M -6.5%; 000 share 36%, 111 share 29%, late improvement 0%, early advantage lost 36%.
- VUSTX_LONG_TREASURY_PROXY / FIRST_HIKE [SUPPORTED_PROXY_DESCRIPTIVE; 8 legs, 6 broad episodes]: cash-relative weighted medians 3M -3.8%, 6M -5.4%, 12M -3.6%; 000 share 61%, 111 share 33%, late improvement 0%, early advantage lost 6%.
- VUSTX_LONG_TREASURY_PROXY / LAST_HIKE [SUPPORTED_PROXY_DESCRIPTIVE; 8 legs, 6 broad episodes]: cash-relative weighted medians 3M +4.2%, 6M +5.7%, 12M +0.9%; 000 share 22%, 111 share 56%, late improvement 6%, early advantage lost 17%.
- VUSTX_LONG_TREASURY_PROXY / PAUSE_START [SUPPORTED_PROXY_DESCRIPTIVE; 6 legs, 6 broad episodes]: cash-relative weighted medians 3M +4.5%, 6M +4.0%, 12M +6.8%; 000 share 0%, 111 share 83%, late improvement 0%, early advantage lost 0%.
- VUSTX_LONG_TREASURY_PROXY / FIRST_CUT [SUPPORTED_PROXY_DESCRIPTIVE; 8 legs, 6 broad episodes]: cash-relative weighted medians 3M +2.3%, 6M +6.2%, 12M +1.8%; 000 share 22%, 111 share 44%, late improvement 17%, early advantage lost 17%.
- VGSIX_REIT_PROXY / FIRST_HIKE [LIMITED_PROXY_DESCRIPTIVE; 4 legs, 4 broad episodes]: cash-relative weighted medians 3M -9.7%, 6M -14.1%, 12M -3.4%; 000 share 50%, 111 share 50%, late improvement 0%, early advantage lost 0%.
- VGSIX_REIT_PROXY / LAST_HIKE [LIMITED_PROXY_DESCRIPTIVE; 4 legs, 4 broad episodes]: cash-relative weighted medians 3M +6.9%, 6M +5.3%, 12M +14.1%; 000 share 0%, 111 share 75%, late improvement 25%, early advantage lost 0%.
- VGSIX_REIT_PROXY / PAUSE_START [LIMITED_PROXY_DESCRIPTIVE; 4 legs, 4 broad episodes]: cash-relative weighted medians 3M +6.0%, 6M +6.5%, 12M +14.1%; 000 share 0%, 111 share 75%, late improvement 0%, early advantage lost 25%.
- VGSIX_REIT_PROXY / FIRST_CUT [LIMITED_PROXY_DESCRIPTIVE; 4 legs, 4 broad episodes]: cash-relative weighted medians 3M -0.3%, 6M -1.7%, 12M -7.9%; 000 share 50%, 111 share 0%, late improvement 25%, early advantage lost 25%.
- BTC_USD / FIRST_HIKE [LIMITED_DESCRIPTIVE; 2 legs, 2 broad episodes]: cash-relative weighted medians 3M -40.3%, 6M -51.8%, 12M -40.1%; 000 share 50%, 111 share 50%, late improvement 0%, early advantage lost 0%.
- BTC_USD / LAST_HIKE [LIMITED_DESCRIPTIVE; 2 legs, 2 broad episodes]: cash-relative weighted medians 3M -27.0%, 6M +49.9%, 12M +31.7%; 000 share 0%, 111 share 50%, late improvement 50%, early advantage lost 0%.
- BTC_USD / PAUSE_START [LIMITED_DESCRIPTIVE; 2 legs, 2 broad episodes]: cash-relative weighted medians 3M +38.2%, 6M +135.6%, 12M +104.6%; 000 share 0%, 111 share 100%, late improvement 0%, early advantage lost 0%.
- BTC_USD / FIRST_CUT [LIMITED_DESCRIPTIVE; 2 legs, 2 broad episodes]: cash-relative weighted medians 3M -11.3%, 6M -11.9%, 12M +0.5%; 000 share 0%, 111 share 50%, late improvement 50%, early advantage lost 0%.

## Interpretation

Each 3M/6M/12M return includes the anchor month t from baseline t-1; mechanical cash adds that month's official FEDFUNDS rate to canonical 014 post-anchor cash. 12M values reproduce 040 to tolerance 1e-12. The pattern describes three discrete observations, not within-month or intervening-month crossing, investable cash rates, expected returns, causal Fed effects or a current allocation rule.
