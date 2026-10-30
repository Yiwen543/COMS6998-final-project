#!/usr/bin/env python3
"""Copy two outcome-blind CVDP IP candidates from the hash-pinned dataset.

Only original RTL and the supplied specification are copied. Benchmark stimulus,
testbenches, patches, and any solution material are deliberately excluded.
Existing files are verified, never silently overwritten.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "docs/midterm-candidate-lock.json").read_text())
DATASET = ROOT / ".cache" / LOCK["dataset_file"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_verified(path: Path, data: bytes) -> None:
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"Refusing to overwrite modified candidate file: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> None:
    raw = DATASET.read_bytes()
    if sha(raw) != LOCK["dataset_sha256"]:
        raise ValueError("Pinned dataset SHA-256 mismatch")
    rows = raw.splitlines(keepends=True)
    for candidate in LOCK["candidates"]:
        line = rows[candidate["record_line"] - 1]
        if sha(line) != candidate["record_sha256"]:
            raise ValueError(f"Pinned record SHA-256 mismatch: {candidate['id']}")
        record = json.loads(line)
        if record["id"] != candidate["id"] or record["categories"] != candidate["categories"]:
            raise ValueError("Pinned record ID or category changed")
        folder = ROOT / "examples" / candidate["slug"]
        for field, digest in candidate["fields"].items():
            area, name = field.split("/", 1)
            if area not in ("harness", "context"):
                raise ValueError(f"Unexpected field area: {area}")
            data = record[area][name].encode()
            if sha(data) != digest:
                raise ValueError(f"Source hash mismatch: {field}")
            destination = folder / ("rtl" if name.endswith((".sv", ".v")) else "docs") / Path(name).name
            write_verified(destination, data)
        provenance = {
            "id": candidate["id"], "categories": candidate["categories"],
            "dataset": "nvidia/cvdp-benchmark-dataset",
            "dataset_revision": LOCK["dataset_revision"],
            "dataset_file": LOCK["dataset_file"],
            "dataset_sha256": LOCK["dataset_sha256"],
            "record_line": candidate["record_line"],
            "record_sha256": candidate["record_sha256"],
            "fields": candidate["fields"],
            "status": "candidate; no checker or C-versus-B result yet",
        }
        write_verified(folder / "provenance.json", (json.dumps(provenance, indent=2) + "\n").encode())
        write_verified(folder / "LICENSE", (ROOT / "examples/heldout_queue/LICENSE").read_bytes())
        notice = ("Copyright 2025 NVIDIA Corporation.\n"
                  "Original CVDP example RTL: Apache-2.0; specification: CC BY 4.0.\n"
                  f"Copied verbatim from pinned dataset record {candidate['id']}.\n"
                  "These task fixtures are not verified golden implementations.\n")
        write_verified(folder / "NOTICE", notice.encode())
        print(f"Verified {candidate['id']} -> {folder.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
