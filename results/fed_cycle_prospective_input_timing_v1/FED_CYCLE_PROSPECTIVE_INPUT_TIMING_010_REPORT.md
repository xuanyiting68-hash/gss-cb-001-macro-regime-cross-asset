# FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010 — Report

**TIMING / DATA-PROVENANCE AUDIT ONLY / NO NEW FORECAST PERFORMANCE EVIDENCE**

- QC: **PASS**
- exact OOS-008 live transport status: **SOURCE_TIMING_REPAIR_REQUIRED**
- current next-month source probe: **CURRENT_SOURCE_REFRESH_PENDING**

## Gold release timing

- recent uncensored monthly introductions audited: 6
- introductions arriving after the following month had already begun: 6/6
- release-lag range relative to next-month start: 51.7 to 107.7 hours
- latest source month at run time: 2026-08
- month required for the current next-month probe (2026-10): 2026-09

| observation_period   | first_seen_commit_timestamp_utc   | first_seen_commit_sha                    | file_sha256                                                      | next_month_start_utc      |   release_lag_hours_after_next_month_start | strict_pre_target_available   |
|:---------------------|:----------------------------------|:-----------------------------------------|:-----------------------------------------------------------------|:--------------------------|-------------------------------------------:|:------------------------------|
| 2026-02              | 2026-03-05T11:40:03+00:00         | 2eda8f0b6408852492fd0f6a076022420194d71d | f88f66c6f09a4f63513dbd6491e1a48c0d4d980b9cd6b664a6ac715904e5529e | 2026-03-01T00:00:00+00:00 |                                   107.668  | False                         |
| 2026-03              | 2026-04-03T03:41:38+00:00         | 1f122532465e2f49f959aea09adf4e5abb89f93f | 0b3ae3089c1f49b2000269ab2850599ab2097088ce3c37e9c7f8add52b51837c | 2026-04-01T00:00:00+00:00 |                                    51.6939 | False                         |
| 2026-05              | 2026-06-03T05:57:09+00:00         | e975c00b94fc85a8e0acb8729294fe700377aa65 | a2033cfc1b4ac0d61eb13a991efbf12f767a6106317d93ea7ca3b145af9d1725 | 2026-06-01T00:00:00+00:00 |                                    53.9525 | False                         |
| 2026-06              | 2026-07-03T04:36:30+00:00         | 81736bffbfb3fc411aaa8db1610bcff5f5f6e28d | 2f709329c533e37a3c4e98f59d1aeb74c83d494b84bbf1bac1e72d9ee72f1a5d | 2026-07-01T00:00:00+00:00 |                                    52.6083 | False                         |
| 2026-07              | 2026-08-05T03:54:02+00:00         | 7adbad9e903633c3d4679d8cd0a6f3ae35e8bb0c | 5f6bba02ecfdcacd58359c167f23c83c1c13d5c3b1085722c5126a587fc88ae4 | 2026-08-01T00:00:00+00:00 |                                    99.9006 | False                         |
| 2026-08              | 2026-09-03T05:22:53+00:00         | 2bad0e7dbb364940e6df95c2bafd2bbe4a924072 | 7d7874be55951fcc267547849a52ca69681153dd990c3892de2282acdd1581d9 | 2026-09-01T00:00:00+00:00 |                                    53.3814 | False                         |

The historical Gold source contract fails strict pre-target transport if its required M-1 monthly value is first published after month M has begun.

## RTDSM current readiness

| run_timestamp_utc                | next_forecast_month_probe   | required_ipt_observation_period   | selected_vintage_period   | rt_ipt_yoy_available   | last_workbook_vintage   | workbook_sha256                                                  | landing_page_sha256                                              | workbook_url                                                                                                                                                      |   parsed_cells |   vintage_count |   sheet_count |
|:---------------------------------|:----------------------------|:----------------------------------|:--------------------------|:-----------------------|:------------------------|:-----------------------------------------------------------------|:-----------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------:|----------------:|--------------:|
| 2026-09-24T10:06:32.884777+00:00 | 2026-10                     | 2026-08                           | 2026-08                   | False                  | 2026-08                 | b4a6324162c8745d1a6d7740c936ae6502b00c39961e98370536c506ab55af99 | 2117c29eb414ca869ea252f3117506400b900a1b1dbfd21f096d562029696f0a | https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/real-time-data/data-files/xlsx/iptMvMd.xlsx?sc_lang=en&hash=71A0CD9AD2C8828F0B041196CBFB7E5E |         477136 |             766 |             1 |

A current RTDSM gap is treated as a refresh dependency, not automatically as a permanent structural failure.

## Research decision

- No prediction is issued.
- OOS-008 and PROSPECTIVE-SHADOW-009 remain unchanged.
- If exact Gold source timing fails, a source bridge or target-timing amendment must be separately frozen before testing.
- Any replacement specification starts with no inherited prospective validation evidence.
