"""Fetch the pinned public CVDP screening slice, with a required SHA-256 match."""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "docs/heldout-dataset-lock.json").read_text())
DEST = ROOT / ".cache" / LOCK["file"]


def verified(data):
    return hashlib.sha256(data).hexdigest() == LOCK["sha256"] and len(data.splitlines()) == LOCK["records"]


if __name__ == "__main__":
    if DEST.exists() and verified(DEST.read_bytes()):
        print(f"Already verified: {DEST}")
    else:
        url = f'{LOCK["url"]}/resolve/{LOCK["revision"]}/{LOCK["file"]}'
        with urllib.request.urlopen(url, timeout=120) as response:
            data = response.read()
        if not verified(data):
            raise SystemExit("Pinned CVDP dataset hash/count mismatch; refusing to save")
        DEST.parent.mkdir(parents=True, exist_ok=True)
        DEST.write_bytes(data)
        print(f"Downloaded and verified: {DEST}")
