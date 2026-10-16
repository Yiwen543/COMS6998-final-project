#!/usr/bin/env python3
"""Optional retrieval of the already-inspected public HF file, hash verified."""
import hashlib
import json
import urllib.request
from pathlib import Path
root = Path(__file__).resolve().parents[1]
lock = json.loads((root/'docs/dataset-lock.json').read_text())
out = root/'build'/lock['file']
out.parent.mkdir(exist_ok=True)
url = f'{lock["url"]}/resolve/{lock["revision"]}/{lock["file"]}'
if out.exists() and hashlib.sha256(out.read_bytes()).hexdigest() == lock['sha256']:
    print(f'Already verified: {out}')
else:
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != lock['sha256']:
        raise SystemExit('Dataset hash mismatch; refusing to save changed content')
    out.write_bytes(data)
    print(f'Downloaded and verified: {out}')
