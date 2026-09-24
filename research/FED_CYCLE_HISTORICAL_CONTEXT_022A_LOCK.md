# FED-CYCLE-HISTORICAL-CONTEXT-022A — LOCK

Date locked: 2026-09-25

## Purpose

Add independently sourced public historical context to the six-case 022 casebook without altering its canonical policy chronology or market outcomes.

022A is a **source registry and context-claim layer**, not a new empirical model.

## Episode universe

Exactly B02-B07, inherited from 022.

## Source hierarchy

Preferred:
1. Federal Reserve Board contemporaneous FOMC statements / minutes / transcripts / monetary policy reports;
2. NBER Business Cycle Dating Committee chronology and announcements;
3. Federal Reserve History for retrospective institutional/event context.

Avoid using secondary financial media as a canonical source when an official source is available.

## Claim-time taxonomy

Each external context claim must be tagged:

- `CONTEMPORANEOUS_POLICY_CONTEXT`: information or rationale publicly/officially recorded at or near the policy event.
- `RETROSPECTIVE_DATING`: later official dating or retrospective classification; must never be presented as known at the anchor.
- `POST_ANCHOR_SHOCK`: a material shock that occurred after the anchor; must not be back-projected into the original policy rationale.
- `RETROSPECTIVE_EVENT_CONTEXT`: later official historical synthesis of an event already observed at the time.

## Frozen claim rules

A claim row must contain:
- broad_episode_id;
- claim_id;
- event_date or period;
- relationship_to_first_cut;
- claim_time_class;
- concise paraphrased claim;
- source institution;
- source title;
- source URL;
- source publication/announcement date when available;
- contemporaneous_known flag;
- hindsight_warning;
- allowed_content_use;
- forbidden_inference.

No long quotes are stored.

## Required context checks

022A must explicitly encode:

1. B02: October 1987 market crash and Fed liquidity response; do not treat B02 as a single mechanical cycle.
2. B03: July 1995 easing rationale from the FOMC; recession status only from later NBER chronology.
3. B04: January 2001 weakness rationale; March 2001 recession date is retrospective; September 11 is a later shock inside the post-cut path.
4. B05: September 2007 credit/housing rationale; December 2007 recession date is retrospective.
5. B06: July 2019 global-development/muted-inflation rationale; COVID shock and February 2020 recession peak occurred later and must not be attributed to the July 2019 cut rationale.
6. B07: September 2024 inflation/labor-risk rebalancing rationale; as of the 2026-09-25 source audit NBER's most recent recognized peak remains February 2020.

## Prohibited claims

022A must not:
- say a recession was contemporaneously known before NBER or contemporaneous evidence supports that;
- say the Fed caused later recession/asset paths;
- say a later shock was anticipated by an earlier cut;
- use retrospective event labels as live indicators;
- rank policy decisions;
- import private paper material.

## QC gates

PASS requires:
- all six episodes covered;
- every row has a source URL and source institution;
- every row has a claim-time class;
- every RETROSPECTIVE_DATING / POST_ANCHOR_SHOCK row has a non-empty hindsight warning;
- B04 includes September 11 as POST_ANCHOR_SHOCK;
- B06 includes COVID as POST_ANCHOR_SHOCK;
- B04/B05 recession dating rows are retrospective, not contemporaneous;
- no causal/OOS/deployment claims;
- no private-paper inputs.

## Integration rule

022 remains canonical for dates and asset metrics.

022A may enrich a story, but if an external narrative conflicts with 022's audited chronology, the conflict must be surfaced rather than silently overwritten.
