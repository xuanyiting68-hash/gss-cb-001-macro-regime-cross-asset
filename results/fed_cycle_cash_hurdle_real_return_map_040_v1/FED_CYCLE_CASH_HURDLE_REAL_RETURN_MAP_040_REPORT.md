# FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040 — REPORT

## Status

**QC PASS / EVENT-MATCHED CASH-HURDLE + EX-POST REAL-RETURN MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## Method boundary

- Asset nominal endpoints and MDD are inherited from canonical public modules.
- The primary cash hurdle adds the anchor-month official monthly effective federal-funds rate to canonical 014 post12 cash, exactly aligning the t-1 to t+12 asset endpoint grid.
- CPI purchasing-power adjustment uses current-vintage CPIAUCSL from baseline month t-1 to endpoint t+12.
- The 37 event-level rate/CPI inputs are frozen in-repo under AMENDMENT 02 to remove live-network dependence.
- No p-values, ranking, optimizer, expected-return forecast or trade instruction are generated.

## Fixed-order phase map

### FIRST_HIKE

- GOLD [CORE_SUPPORTED] — nominal +3.1%, vs matched cash -2.4%, real -2.8%, MDD +11.6%, beats-cash share 48%, beats-inflation share 33%.
- SP500 [CORE_SUPPORTED] — nominal +8.0%, vs matched cash +2.5%, real +5.8%, MDD +5.9%, beats-cash share 55%, beats-inflation share 62%.
- NASDAQ [CORE_SUPPORTED] — nominal +6.5%, vs matched cash -0.8%, real +4.4%, MDD +12.2%, beats-cash share 48%, beats-inflation share 55%.
- WTI [CORE_SUPPORTED] — nominal +22.4%, vs matched cash +17.8%, real +19.9%, MDD +18.8%, beats-cash share 78%, beats-inflation share 78%.
- DXY [CORE_SUPPORTED] — nominal +3.0%, vs matched cash -2.5%, real +1.0%, MDD +8.2%, beats-cash share 36%, beats-inflation share 62%.
- VUSTX_LONG_TREASURY_PROXY [SUPPORTED_PROXY_DESCRIPTIVE] — nominal +1.0%, vs matched cash -3.6%, real -0.9%, MDD +10.7%, beats-cash share 33%, beats-inflation share 33%.
- VGSIX_REIT_PROXY [LIMITED_PROXY_DESCRIPTIVE] — nominal +2.5%, vs matched cash -3.4%, real -1.2%, MDD +11.5%, beats-cash share 50%, beats-inflation share 50%.
- BTC_USD [LIMITED_DESCRIPTIVE] — nominal -38.4%, vs matched cash -40.1%, real -41.9%, MDD +12.4%, beats-cash share 50%, beats-inflation share 50%.

### LAST_HIKE

- GOLD [CORE_SUPPORTED] — nominal -2.8%, vs matched cash -8.2%, real -5.6%, MDD +9.1%, beats-cash share 43%, beats-inflation share 43%.
- SP500 [CORE_SUPPORTED] — nominal +16.7%, vs matched cash +10.9%, real +13.9%, MDD +4.2%, beats-cash share 69%, beats-inflation share 69%.
- NASDAQ [CORE_SUPPORTED] — nominal +15.6%, vs matched cash +9.2%, real +12.3%, MDD +4.0%, beats-cash share 64%, beats-inflation share 69%.
- WTI [CORE_SUPPORTED] — nominal +5.0%, vs matched cash -0.7%, real +2.6%, MDD +19.6%, beats-cash share 50%, beats-inflation share 67%.
- DXY [CORE_SUPPORTED] — nominal -1.3%, vs matched cash -8.1%, real -4.7%, MDD +5.2%, beats-cash share 14%, beats-inflation share 21%.
- VUSTX_LONG_TREASURY_PROXY [SUPPORTED_PROXY_DESCRIPTIVE] — nominal +9.9%, vs matched cash +0.9%, real +5.2%, MDD +3.3%, beats-cash share 61%, beats-inflation share 78%.
- VGSIX_REIT_PROXY [LIMITED_PROXY_DESCRIPTIVE] — nominal +18.8%, vs matched cash +14.1%, real +16.0%, MDD +4.3%, beats-cash share 100%, beats-inflation share 100%.
- BTC_USD [LIMITED_DESCRIPTIVE] — nominal +34.8%, vs matched cash +31.7%, real +31.6%, MDD +7.2%, beats-cash share 100%, beats-inflation share 100%.

### PAUSE_START

- GOLD [CORE_SUPPORTED] — nominal +4.9%, vs matched cash -1.3%, real +1.9%, MDD +7.6%, beats-cash share 29%, beats-inflation share 57%.
- SP500 [CORE_SUPPORTED] — nominal +24.6%, vs matched cash +13.2%, real +20.3%, MDD +4.2%, beats-cash share 71%, beats-inflation share 71%.
- NASDAQ [CORE_SUPPORTED] — nominal +28.1%, vs matched cash +16.6%, real +23.8%, MDD +4.0%, beats-cash share 71%, beats-inflation share 71%.
- WTI [CORE_SUPPORTED] — nominal -4.6%, vs matched cash -10.4%, real -8.1%, MDD +18.0%, beats-cash share 33%, beats-inflation share 33%.
- DXY [CORE_SUPPORTED] — nominal -1.3%, vs matched cash -7.5%, real -4.7%, MDD +6.3%, beats-cash share 14%, beats-inflation share 14%.
- VUSTX_LONG_TREASURY_PROXY [SUPPORTED_PROXY_DESCRIPTIVE] — nominal +15.1%, vs matched cash +6.8%, real +10.5%, MDD +3.9%, beats-cash share 100%, beats-inflation share 100%.
- VGSIX_REIT_PROXY [LIMITED_PROXY_DESCRIPTIVE] — nominal +21.4%, vs matched cash +14.1%, real +17.0%, MDD +4.3%, beats-cash share 75%, beats-inflation share 100%.
- BTC_USD [LIMITED_DESCRIPTIVE] — nominal +116.7%, vs matched cash +104.6%, real +110.7%, MDD +11.5%, beats-cash share 100%, beats-inflation share 100%.

### FIRST_CUT

- GOLD [CORE_SUPPORTED] — nominal +4.1%, vs matched cash -0.0%, real +2.2%, MDD +5.4%, beats-cash share 43%, beats-inflation share 57%.
- SP500 [CORE_SUPPORTED] — nominal +11.0%, vs matched cash +2.1%, real +8.2%, MDD +14.0%, beats-cash share 55%, beats-inflation share 55%.
- NASDAQ [CORE_SUPPORTED] — nominal +6.0%, vs matched cash -3.4%, real +1.0%, MDD +17.5%, beats-cash share 50%, beats-inflation share 55%.
- WTI [CORE_SUPPORTED] — nominal -16.9%, vs matched cash -24.3%, real -20.9%, MDD +22.2%, beats-cash share 33%, beats-inflation share 33%.
- DXY [CORE_SUPPORTED] — nominal -1.3%, vs matched cash -6.5%, real -3.9%, MDD +5.2%, beats-cash share 29%, beats-inflation share 36%.
- VUSTX_LONG_TREASURY_PROXY [SUPPORTED_PROXY_DESCRIPTIVE] — nominal +6.0%, vs matched cash +1.8%, real +4.2%, MDD +4.5%, beats-cash share 61%, beats-inflation share 67%.
- VGSIX_REIT_PROXY [LIMITED_PROXY_DESCRIPTIVE] — nominal -4.8%, vs matched cash -7.9%, real -8.5%, MDD +8.3%, beats-cash share 25%, beats-inflation share 50%.
- BTC_USD [LIMITED_DESCRIPTIVE] — nominal +1.8%, vs matched cash +0.5%, real +0.6%, MDD +14.9%, beats-cash share 100%, beats-inflation share 100%.

## Cross-cutting diagnostic

- event rows with positive nominal endpoint: 136
- positive nominal but failed matched cash hurdle: 30
- positive nominal but failed matched inflation hurdle: 14

These are row counts, not independent statistical observations; broad-episode weighting remains the summary convention.

## Boundary

A positive nominal endpoint is not automatically an opportunity-cost win, a purchasing-power win, or a low-risk path.
Historical medians are not expected returns and are not allocation instructions.
