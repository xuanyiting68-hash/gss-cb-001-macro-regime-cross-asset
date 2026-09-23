# FED-CYCLE-PATH-001 — Data-Source Amendment 2
Date: 2026-09-24
Status: **FROZEN PRE-OUTCOME DATA-SUPPORT AMENDMENT**

## Trigger

The second GitHub Actions execution also failed before any asset outcome was computed or committed.

Yahoo Finance exposes `XAUUSD=X` as a spot-Gold symbol on its website, but the machine chart-history endpoint returned HTTP 404 for this symbol on the GitHub runner.

At the time of this amendment:

- no Gold event path had been computed;
- no return/drawdown/recovery result had been produced;
- no result file had been committed.

## Daily Gold substitution

For the daily path-risk layer only, replace `XAUUSD=X` with:

- `GC=F` — Yahoo Finance continuous Gold futures history.

This is explicitly a **Gold futures proxy**, not a spot-price series.

The public report and all result labels must preserve that distinction.

## Why not use an unverified historical spot CSV

Long daily Gold histories exist in third-party public repositories, but some do not provide a sufficiently auditable upstream provenance or redistribution basis. They are not imported into this public research module merely to increase cycle count.

The project prefers a narrower, clearly labelled proxy over a longer but provenance-uncertain series.

## Gold support gate

Because the reproducible daily Gold proxy has modern-era coverage, the hard support gate for `FIRST_HIKE` is amended from four to **three independent tightening cycles**.

This is a data-support gate, not a statistical-significance threshold.

It is changed before viewing any asset outcome and does not alter:

- event definitions;
- horizons;
- MDD/MAE/MFE definitions;
- recovery definitions;
- volatility definitions;
- state definitions;
- testing families.

A sample of three cycles is still too small for a universal historical rule and must be labelled as such.

## Required long-history follow-up

A separate module must extend Gold cycle breadth using an openly licensed long-history source at its native frequency rather than pretending monthly data are daily.

Candidate public-safe source:

- DataHub `core/gold-prices`, modern monthly series sourced from World Bank Commodity Markets, ODC-PDDL-1.0.

That future monthly layer is a complementary long-history robustness layer. It must not be silently pooled with daily `GC=F` observations as if they were the same instrument/frequency.

## Audit trail

1. Stooq daily spot acquisition — blocked by browser-verification page.
2. Yahoo `XAUUSD=X` chart endpoint — HTTP 404.
3. Current daily proxy — Yahoo `GC=F`, raw bytes not committed.

Both failed acquisition attempts occurred before asset outcomes were generated.
