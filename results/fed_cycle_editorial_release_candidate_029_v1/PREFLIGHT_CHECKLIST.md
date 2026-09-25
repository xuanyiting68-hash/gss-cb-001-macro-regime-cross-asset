# 029 Pre-Publication Evidence / Freshness Checklist

A release is GO only if every required item passes. Otherwise status is HOLD.

1. Confirm the repository main branch still contains every referenced CLAIM_ID.
2. Confirm every referenced FIGURE_KEY exists and the intended rendered file is present.
3. Confirm the release candidate immutable_evidence_sha256 matches the frozen RC1 payload.
4. Confirm all evidence numbers in copy match the canonical 026/022B payload.
5. Confirm the title/hook A/B variant changes presentation only, not factual meaning.
6. Confirm freshness_rule.
7. If REVERIFY_BEFORE_CURRENT_USE, re-audit the affected official source before publishing.
8. Do not present the 2026-09-25 current snapshot as live data unless a fresh append-only snapshot has been created.
9. Confirm historical timing labels: CONTEMPORANEOUS / RETROSPECTIVE / POST_ANCHOR remain correct.
10. Confirm no buy/sell, return-promise, best-asset, deterministic-bottom or current-analog-ranking wording appears.
11. Confirm mandatory caveat remains in the platform-appropriate location.
12. Confirm the source block remains accessible to editor/reviewer and can be surfaced to the audience when appropriate.
13. Confirm no private-paper inputs or unpublished academic results entered the copy.
14. Confirm evidence_payload_changed = FALSE.

If any check fails, HOLD the release and fix the editorial asset or rebuild upstream evidence. Do not silently alter the canonical factual payload.
