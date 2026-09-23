# FED-CYCLE-PATH-001 — Data-Source Amendment 1
Date: 2026-09-24
Status: **FROZEN PRE-OUTCOME DATA-ACQUISITION AMENDMENT**

## Trigger

The first GitHub Actions execution failed before any asset outcome was computed or committed.

The failure was mechanical: the Stooq daily-download endpoint returned a JavaScript browser-verification page to the GitHub-hosted runner rather than CSV data.

No event-path, return, drawdown, volatility or recovery result had been produced when this amendment was made.

## Amendment

Replace the two Stooq acquisition endpoints with Yahoo Finance public chart-history endpoints:

- Gold: `XAUUSD=X` — Gold 1 oz / USD spot-price proxy;
- S&P 500: `^GSPC` — S&P 500 cash index.

The research objects, event definitions, horizons, drawdown/recovery definitions, QC gates and interpretation boundaries are unchanged.

## Redistribution boundary

Yahoo historical market data are treated as redistribution-uncertain.

Therefore:

- raw downloaded JSON bytes are used only transiently;
- raw bytes are hashed for provenance;
- raw market-history files are not committed;
- only derived event metrics, normalized paths, source metadata, hashes, QC files and figures may enter the public repository.

## Gold interpretation boundary

`XAUUSD=X` is used as the daily spot-price proxy for Gold in USD.

If the endpoint does not provide enough history to meet the already-frozen Gold support gate, the run must fail. The study must not silently substitute an ETF, miner index or futures contract after seeing outcomes.

## Audit trail

Superseded acquisition attempt:

- source: Stooq `xauusd` / `^spx`;
- result: JavaScript verification response on GitHub runner;
- workflow run: `fed-cycle-path-v1 #1`;
- outcome status: **NO ASSET OUTCOMES COMPUTED / NO RESULTS COMMITTED**.

This is a source-access correction, not a post-result specification change.
