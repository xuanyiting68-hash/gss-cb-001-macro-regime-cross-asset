# FED-CYCLE-PROSPECTIVE-ISSUANCE-013 v1.1 — Registry Integrity Amendment
Date: 2026-09-24
Status: **FROZEN BEFORE ANY REAL PREDICTION ROW EXISTS**

## 1. Trigger

The v1 issuer correctly prevents duplicate IDs and writes only by append.

Post-run audit identified one remaining integrity gap:

an external/manual edit of a previously committed prediction row should be detected before a later issuance.

The current prediction registry has zero data rows, so this amendment is frozen before any real prospective prediction exists.

## 2. Scope

This amendment changes only registry-integrity auditing.

It does **not** change:

- GCF-012 model/spec hashes;
- historical training data;
- Gold proxy definition;
- RTDSM definition;
- 2-hike / 50 bp eligibility;
- issue-time rule;
- target;
- forecast horizon;
- model coefficients;
- success/evidence criteria.

## 3. Genesis state

For an empty registry, create:

- `REGISTRY_CHAIN.csv` with header only;
- `REGISTRY_INTEGRITY.json`.

Genesis tail hash:

SHA256 of the literal UTF-8 string:

`FED_CYCLE_GCF012_REGISTRY_GENESIS_V1`

The integrity file records:

- schema version;
- exact registry-file SHA256;
- row count;
- current tail hash;
- chain row count.

## 4. Pre-run verification

Before invoking the frozen v1 issuer:

1. verify prediction-registry schema;
2. compute exact registry-file SHA256;
3. require it to match the previously stored integrity SHA256;
4. require registry row count = chain row count;
5. recompute every chain link from canonical registry-row contents;
6. require the recomputed tail hash to match the stored tail hash.

Any mismatch fails closed before issuance.

If integrity files are absent:
- initialization is permitted only when the prediction registry has zero data rows;
- a non-empty unchained registry is a hard failure.

## 5. Row hash

For each newly issued prediction row:

- canonical payload = JSON array of registry field values in frozen registry-column order;
- `row_hash = SHA256(previous_row_hash + "|" + canonical_payload)`.

The chain stores:

- sequence number;
- prediction ID;
- previous row hash;
- row hash.

The chain does not replace the prediction registry.

## 6. Post-run append verification

After the frozen v1 issuer returns successfully:

- registry growth must be exactly 0 or 1 row;
- every pre-existing row must be byte-for-value identical in canonical field order;
- if one row was appended, its prediction ID must be new;
- append exactly one corresponding chain record;
- recompute full chain;
- update exact registry-file SHA256 and tail hash.

A change to any prior row is a hard failure.

## 7. Commit boundary

The workflow commits together:

- prediction registry;
- registry chain;
- integrity state;
- integrity QC;
- ordinary issuance readiness/QC/status.

This provides tamper-evident research provenance inside the public repository.

It is not a cryptographic signature and does not protect against a malicious actor who can deliberately rewrite all repository history and recompute every hash. Repository permissions and Git history remain separate controls.

## 8. Expected current run

Because the 2026 cycle is still 1 hike / 25 bp:

- v1 issuer should append zero prediction rows;
- v1.1 should initialize and verify the genesis state;
- chain rows = 0;
- prediction rows = 0.

## 9. Evidence boundary

**AUDIT INTEGRITY HARDENING ONLY / NO NEW FORECAST EVIDENCE / NOT DEPLOYABLE**
