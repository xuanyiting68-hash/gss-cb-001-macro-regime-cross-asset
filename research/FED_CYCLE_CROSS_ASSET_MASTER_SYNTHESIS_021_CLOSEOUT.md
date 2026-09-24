# FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021 — CLOSEOUT

Date: 2026-09-25

## Final status

**QC PASS / CANONICAL DESCRIPTIVE EVIDENCE MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

021 is an integration milestone. It performs no new price estimation, no new statistical inference and no new threshold/model search.

## Canonical outputs

- 52 price-asset x phase rows
- 13 unique price assets
- 20 core-supported asset x phase rows
- 12 policy/rate/cash context rows
- 12 phase-stress context rows

Core fully supported four-phase assets:

- DXY
- GOLD
- NASDAQ
- SP500
- WTI

Additional coverage:

- TLT / VNQ / BTC_USD remain limited extensions;
- US_HOUSE_PRICE is supported as a slow-moving 24M descriptive extension, with recovery support not universal across phases;
- Hang Seng / Nikkei 225 / KOSPI / Shanghai Composite remain diagnostic Asia extensions.

## FIRST_CUT core snapshot

Historical broad-episode-weighted medians:

| Asset | +12M endpoint | Path risk | Trough month | Anchor -> full recovery |
|---|---:|---:|---:|---:|
| DXY | -1.33% | 5.18% 12M MDD | 8 | 13m |
| GOLD | +4.06% | 5.43% 12M MDD | 5 | 22m |
| NASDAQ | +6.04% | 17.48% 12M MDD | 8 | 15m |
| SP500 | +10.98% | 13.99% 12M MDD | 8 | 14m |
| WTI | -16.94% | 22.23% 12M MDD | 11 | 20m |

The key descriptive lesson is that endpoint return and interim path risk are different objects. Positive +12M endpoints can coexist with material later drawdowns and long total recovery clocks.

## Product interpretation

021 supports an evidence-linked PandaAI object of the form:

`policy phase + asset-specific historical path-risk distribution + recovery clock + support strength + evidence class + uncertainty`

It does not support:

- deterministic bottom dates;
- a FIRST_CUT timing score;
- causal claims from realized Fed phase labels;
- best/worst asset rankings;
- trading or allocation recommendations.

019 and 020 remain explicit negative guardrails: the available small FIRST_CUT sample does not support a simple predetermined bottom-timing rule.

## Reproducibility audit

Initial workflow run failed only at strict JSON serialization because IEEE NaN values remained in mixed pandas records. The script was corrected to serialize the pandas table through JSON-native null conversion. The second workflow run completed successfully and committed the canonical outputs.

Successful workflow run:
- run id: 36038858462
- source commit: `3c684583a3bedb8f307bc26318ac8dbd232e8ea8`
- output commit: `93f637b26cee061713edd63592647dc71ea11da1`

QC:
- upstream QC modules all PASS;
- duplicate asset x phase rows = 0;
- noncanonical phase violations = 0;
- p-values generated = false;
- private-paper inputs used = false;
- causal-status violations = 0;
- deployment-status violations = 0.

## Next research stage

The synthesis layer is now sufficient to begin a structured historical casebook and content evidence library.

Recommended next empirical/content milestone:

**022 — Historical Fed Cycle Casebook**

Build episode-level timelines for representative cycles using only already-public evidence and independently sourced public macro/market context. Each case should separate:

1. policy phase;
2. inflation/growth/yield-curve state;
3. asset path;
4. stress peak;
5. trough;
6. 50% recovery;
7. full recovery;
8. what was known in real time versus only visible ex post.

The casebook should be designed for both deep research and media reuse, while preserving the 021 evidence boundaries.
