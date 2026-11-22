#!/usr/bin/env python3
"""Fetch the three saved guard inputs used in the fast-v1 benchmark."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from urllib.request import urlopen


REPOSITORY = "Yiwen543/COMS6998-final-project"
COMMIT = "e94172a1bd5e9b138b5fc3da01554edb3052ce52"
# (local name, upstream path, Git blob ID, SHA-256 of the original bytes)
INPUTS = [
    ("controller.json", "test2/tasks/axis_length_fifo_v1/qualification/typed-v5/screen/egg-input.json",
     "db4821f0b45d8d2aa97b0a125a883fd53a1a875a", "00de8c887f9205c4cc79dbc235a3fc00c9793f27e8796fbea25f5093461c17a0"),
    ("spi.json", "results/real_parent_screen_20261104/spi_host_core_v2/screen-v2/egg-input.json",
     "b5058a31ba6f8e1a31d0f73fa04967345e847d5c", "21bbd7bbed879d2c1644ff8d1732ea8138230025f594d40b4eae27fa00610f97"),
    ("i2c.json", "results/i2c_event_candidate_20261104/egg-input.json",
     "071b774bfe61edd1a6f81b3db4ced2fb41027b7d", "ff1036be2856f540d54ee7d8f1587d8b25edb2c80682023985c671c3460940d8"),
]


def fetch(output):
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output path already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        staged = Path(tmp) / "verified"
        staged.mkdir()
        files = {}
        for name, path, blob_id, sha256 in INPUTS:
            url = f"https://raw.githubusercontent.com/{REPOSITORY}/{COMMIT}/{path}"
            with urlopen(url, timeout=30) as response:
                data = response.read()
            actual_sha256 = hashlib.sha256(data).hexdigest()
            actual_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if actual_sha256 != sha256 or actual_blob != blob_id:
                raise ValueError(f"Integrity check failed for {path}")
            (staged / name).write_bytes(data)
            files[name] = {"path": path, "blob_id": blob_id, "sha256": sha256, "bytes": len(data)}
        manifest = {"repository": f"https://github.com/{REPOSITORY}", "ref": "main",
                    "commit": COMMIT, "files": files}
        (staged / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        staged.rename(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="new directory to create")
    args = parser.parse_args()
    try:
        fetch(args.output)
    except (OSError, ValueError) as err:
        parser.exit(1, f"{err}\n")
