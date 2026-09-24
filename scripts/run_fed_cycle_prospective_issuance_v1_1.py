#!/usr/bin/env python3
"""
FED-CYCLE-PROSPECTIVE-ISSUANCE-013 v1.1
Tamper-evident append-only registry wrapper around the frozen v1 issuer.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "fed_cycle_prospective_gcf_v1"
REGISTRY = OUT / "PREDICTION_REGISTRY.csv"
CHAIN = OUT / "REGISTRY_CHAIN.csv"
INTEGRITY = OUT / "REGISTRY_INTEGRITY.json"
QC_FILE = OUT / "REGISTRY_INTEGRITY_QC.json"

GENESIS_LITERAL = "FED_CYCLE_GCF012_REGISTRY_GENESIS_V1"
GENESIS_HASH = hashlib.sha256(GENESIS_LITERAL.encode("utf-8")).hexdigest()

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

ISSUER = load_module(
    ROOT / "scripts" / "run_fed_cycle_prospective_issuance_v1.py",
    "frozen_issuance_v1",
)
COLS = list(ISSUER.PREDICTION_COLUMNS)

def file_sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_registry():
    if not REGISTRY.exists():
        raise RuntimeError("Prediction registry missing")
    with REGISTRY.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLS:
            raise RuntimeError("Prediction registry schema mismatch")
        rows = list(reader)
    ids = [r["prediction_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate prediction IDs")
    return rows

def payload(row):
    return json.dumps([row.get(c, "") for c in COLS], ensure_ascii=False, separators=(",", ":"))

def chained_hash(prev_hash, row):
    return hashlib.sha256((prev_hash + "|" + payload(row)).encode("utf-8")).hexdigest()

def read_chain():
    if not CHAIN.exists():
        return None
    with CHAIN.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        expected = ["sequence","prediction_id","previous_row_hash","row_hash"]
        if reader.fieldnames != expected:
            raise RuntimeError("Registry-chain schema mismatch")
        return list(reader)

def write_empty_chain():
    with CHAIN.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow(["sequence","prediction_id","previous_row_hash","row_hash"])

def write_integrity(registry_sha, row_count, tail_hash):
    obj = {
        "schema_version": "GCF012_REGISTRY_CHAIN_V1",
        "genesis_literal": GENESIS_LITERAL,
        "genesis_hash": GENESIS_HASH,
        "registry_sha256": registry_sha,
        "registry_row_count": row_count,
        "chain_row_count": row_count,
        "tail_row_hash": tail_hash,
    }
    INTEGRITY.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")

def verify(rows, chain, integrity):
    if len(rows) != len(chain):
        raise RuntimeError("Registry/chain row-count mismatch")
    prev = GENESIS_HASH
    for i, (row, link) in enumerate(zip(rows, chain), start=1):
        if int(link["sequence"]) != i:
            raise RuntimeError("Chain sequence mismatch")
        if link["prediction_id"] != row["prediction_id"]:
            raise RuntimeError("Chain prediction ID mismatch")
        if link["previous_row_hash"] != prev:
            raise RuntimeError("Chain previous-hash mismatch")
        expected = chained_hash(prev, row)
        if link["row_hash"] != expected:
            raise RuntimeError("Chain row hash mismatch")
        prev = expected
    if integrity["registry_row_count"] != len(rows):
        raise RuntimeError("Integrity registry-row count mismatch")
    if integrity["chain_row_count"] != len(chain):
        raise RuntimeError("Integrity chain-row count mismatch")
    if integrity["tail_row_hash"] != prev:
        raise RuntimeError("Integrity tail hash mismatch")
    if integrity["registry_sha256"] != file_sha(REGISTRY):
        raise RuntimeError("Registry exact-file SHA mismatch")
    return prev

def initialize_if_allowed(rows):
    chain = read_chain()
    if INTEGRITY.exists() or chain is not None:
        if not (INTEGRITY.exists() and chain is not None):
            raise RuntimeError("Partial registry-integrity state")
        integrity = json.loads(INTEGRITY.read_text(encoding="utf-8"))
        tail = verify(rows, chain, integrity)
        return chain, integrity, tail, False
    if rows:
        raise RuntimeError("Cannot initialize integrity around non-empty registry")
    write_empty_chain()
    write_integrity(file_sha(REGISTRY), 0, GENESIS_HASH)
    chain = read_chain()
    integrity = json.loads(INTEGRITY.read_text(encoding="utf-8"))
    tail = verify(rows, chain, integrity)
    return chain, integrity, tail, True

def append_chain_link(sequence, prediction_id, prev_hash, row_hash):
    with CHAIN.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([sequence, prediction_id, prev_hash, row_hash])

def main():
    before_rows = read_registry()
    before_chain, before_integrity, before_tail, initialized = initialize_if_allowed(before_rows)
    before_payloads = [payload(r) for r in before_rows]
    before_sha = file_sha(REGISTRY)

    # The frozen issuer either refuses or appends exactly one row.
    ISSUER.main()

    after_rows = read_registry()
    growth = len(after_rows) - len(before_rows)
    if growth not in (0, 1):
        raise RuntimeError(f"Invalid registry growth: {growth}")

    # Existing rows are immutable.
    if [payload(r) for r in after_rows[:len(before_rows)]] != before_payloads:
        raise RuntimeError("Pre-existing prediction row changed")

    tail = before_tail
    if growth == 1:
        new_row = after_rows[-1]
        if any(r["prediction_id"] == new_row["prediction_id"] for r in before_rows):
            raise RuntimeError("Appended prediction ID is not new")
        new_hash = chained_hash(tail, new_row)
        append_chain_link(len(after_rows), new_row["prediction_id"], tail, new_hash)
        tail = new_hash

    chain_after = read_chain()
    write_integrity(file_sha(REGISTRY), len(after_rows), tail)
    integrity_after = json.loads(INTEGRITY.read_text(encoding="utf-8"))
    verified_tail = verify(after_rows, chain_after, integrity_after)

    qc = {
        "qc_gate": "PASS",
        "module": "FED-CYCLE-PROSPECTIVE-ISSUANCE-013-v1.1",
        "integrity_initialized_this_run": initialized,
        "registry_sha_before": before_sha,
        "registry_sha_after": file_sha(REGISTRY),
        "registry_rows_before": len(before_rows),
        "registry_rows_after": len(after_rows),
        "registry_growth": growth,
        "chain_rows_after": len(chain_after),
        "genesis_hash": GENESIS_HASH,
        "tail_hash_after": verified_tail,
        "prior_rows_immutable": True,
        "full_chain_recomputed": True,
        "forecast_performance_evaluated": False,
        "research_specification_changed": False,
        "deployment_status": "NOT_DEPLOYABLE",
    }
    QC_FILE.write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qc, indent=2))

if __name__ == "__main__":
    main()
