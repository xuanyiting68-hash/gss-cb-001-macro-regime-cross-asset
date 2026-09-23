# FED-CYCLE-PATH-001 v1 — Quarantine Record
Date: 2026-09-24
Status: **QUARANTINED / TIMING-ONTOLOGY BUG / DO NOT CITE AS RESEARCH RESULT**

## What happened

GitHub Actions run `fed-cycle-path-v1 #3` completed and passed the runner's computational QC. The derived v1 files were committed to `results/fed_cycle_path_v1/` for auditability.

Post-run readback then identified event-timing ontology defects. Therefore the v1 numerical results are retained as an audit artifact but are not admissible research evidence.

## Defect A — target effective date was used as the modern FOMC decision date

The Federal Reserve announced the March 2022 target-range increase on 2022-03-16, while the new range was effective on 2022-03-17.

The v1 runner used the target-series effective date as the event anchor, so the modern event window could be shifted by one calendar day. The same issue can affect other scheduled target changes whose implementation date follows the FOMC decision date.

## Defect B — the scheduled-decision supplement stopped at 2024

The v1 runner supplemented the historical meeting scraper only through 2024.

As a result, ordinary 2025 scheduled FOMC target changes could be unmatched and incorrectly labeled `EMERGENCY_CUT`.

## Defect C — pre-1994 “emergency cut” labels were not conceptually comparable

Before the modern statement/announcement regime, the target-rate series is a historical reconstruction of operational targets rather than a directly comparable contemporaneous FOMC announcement series.

Classifying every reconstructed >=25 bp target decline that did not match a scraped scheduled meeting as an `EMERGENCY_CUT` generated a large number of spurious emergency labels.

## Consequence

The following v1 files are **audit-only** until superseded by a corrected timing run:

`results/fed_cycle_path_v1/*`

Do not propagate v1 numerical outcomes into:

- `docs/EVIDENCE_LEDGER.csv` as positive/negative research evidence;
- PandaAI state logic;
- social-media claims;
- causal or associational conclusions.

## What remains valid from v1

The following implementation components remain useful subject to v1.1 timing correction:

- frozen horizons;
- path-risk metric definitions;
- MDD / MAE / MFE identities;
- volatility and downside-semivol definitions;
- recovery definitions and right-censoring logic;
- public-safe raw-data handling;
- Gold futures-proxy disclosure.

## Required correction

v1.1 must:

1. preserve target effective dates as source fields;
2. map scheduled modern changes to the actual FOMC decision/statement date before constructing event windows;
3. include the 2025-2026 scheduled decision calendar;
4. prevent pre-1994 reconstructed target changes from receiving modern `EMERGENCY_CUT` labels;
5. exclude timing-unresolved unscheduled-cut candidates from outcome calculations;
6. add hard QC assertions for modern scheduled anchors, including the March 2022 first hike.

This quarantine is evidence of the project's rule:

`Computational replication != statistical validity`

and, more specifically here:

`Computational QC != event-ontology validity`.
