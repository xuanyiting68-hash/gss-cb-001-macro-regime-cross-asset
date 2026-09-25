# FED-CYCLE-RELEASE-PREFLIGHT-030 — LOCK

Date locked: 2026-09-25

## Purpose

Execute the first release-control preflight against the six frozen 029 RC1 objects.

030 does not publish content and does not alter evidence. It answers:

- Is each RC internally consistent with current public `main`?
- Are its canonical claims and rendered figures present?
- Does its immutable evidence hash still match?
- Is the package due for release?
- Does freshness require an external re-verification before release?

## Frozen assessment date

`2026-09-25`

This is an operational audit date, not a market-data snapshot.

## Frozen release statuses

Only these statuses are allowed:

- `GO_RC1`
  - immutable evidence passes;
  - all internal sources/figures pass;
  - no special freshness re-verification is outstanding;
  - release is within the first scheduled release window.

- `HOLD_REVERIFY`
  - internal evidence passes;
  - package contains `REVERIFY_BEFORE_CURRENT_USE`;
  - required external/current official-source re-audit has not yet been completed for the scheduled release.

- `READY_NOT_DUE`
  - internal evidence passes;
  - no special reverify hold;
  - primary release date is later in the calendar.

- `HOLD_INTERNAL_QC`
  - claim, figure, hash, copy-boundary, or source integrity fails.

030 must never silently upgrade a HOLD to GO.

## First release focus

### CNT-02 SAME_LABEL_DIFFERENT_PATHS

Scheduled PRIMARY:
- 2026-09-28
- Douyin/TikTok

Expected status if all internal gates pass:
`GO_RC1`

Reason:
- freshness is STATIC_UNLESS_UPSTREAM_REBUILT;
- no current-data claim;
- no external reverify requirement.

### CNT-04 HINDSIGHT_TRAPS

Scheduled PRIMARY:
- 2026-10-01
- Douyin/TikTok

Expected status:
`HOLD_REVERIFY`

Reason:
- includes CLM-CTX-B07_CTX_02;
- freshness = REVERIFY_BEFORE_CURRENT_USE;
- NBER-current-chronology statement must be re-audited close to release.

030 does not perform that future-dated re-audit in advance and does not treat the 2026-09-25 source audit as permanently current.

## Internal preflight checks

For every RC:

1. RC exists exactly once in 029.
2. Immutable evidence SHA256 recomputes exactly.
3. Every CLAIM_ID exists in 022B.
4. Every FIGURE_KEY exists in 024.
5. Every FIGURE_KEY has at least one rendered artifact in 025 or 027.
6. Scheduled primary slot exists exactly once.
7. 028 Douyin/TikTok shotlist has exactly seven rows.
8. Shot 7 is BOUNDARY.
9. No final MP4 is claimed.
10. 028 Xiaohongshu package has final SOURCE_BOUNDARY card.
11. Mandatory caveat is non-empty.
12. evidence_payload_changed = FALSE.
13. no private-paper input.
14. no new inference/p-value.
15. causal status = NONE.
16. deployment status = NOT_DEPLOYABLE.

## Release bundle for CNT-02

030 should create a deterministic release bundle manifest containing:

- RC ID;
- primary title;
- selected Hook A;
- seven-shot plan reference;
- exact evidence figure keys;
- preferred PNG_16_9 path for each figure;
- Xiaohongshu card-plan reference;
- WeChat article reference;
- mandatory caveat;
- immutable evidence hash;
- publication status = NOT_PUBLISHED.

No binary asset copying is required; the bundle is a canonical path/reference manifest.

## CNT-04 hold object

030 should create a hold note recording:

- internal QC PASS;
- reason = NBER current chronology requires re-verification;
- earliest action = official-source re-audit near scheduled release;
- no change to historical retrospective/post-anchor claims;
- publication remains HOLD until reverify PASS.

## Frozen outputs

- `RELEASE_PREFLIGHT_STATUS.csv`
- `RC_CNT02_RELEASE_BUNDLE.csv`
- `RC_CNT02_RELEASE_README_ZH.md`
- `RC_CNT04_HOLD_NOTE.md`
- `PREFLIGHT_AUDIT.json`
- `FED_CYCLE_RELEASE_PREFLIGHT_030_REPORT.md`
- `QC.json`

## QC gates

PASS requires:

1. exactly six RC statuses;
2. all six internal preflight gates pass;
3. CNT-02 = GO_RC1;
4. CNT-04 = HOLD_REVERIFY;
5. later static packages = READY_NOT_DUE;
6. CNT-02 immutable hash exact match;
7. CNT-02 exactly seven short-video shots and final BOUNDARY;
8. CNT-02 figure paths all exist in render manifests;
9. CNT-02 publication status remains NOT_PUBLISHED;
10. CNT-04 is not promoted to GO;
11. no current snapshot is treated as live;
12. no external reverify is falsely claimed;
13. no evidence payload changes;
14. no new inference/p-values;
15. private-paper inputs = false;
16. causal status = NONE;
17. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

`GO_RC1` means editorial evidence-control gates pass for the frozen package.

It does not mean the content has been published, that a final MP4 exists, or that any market claim is predictive.
