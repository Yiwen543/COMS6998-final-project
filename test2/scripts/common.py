"""test2 paths and artifact I/O. No credentials or reference logic."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parent
sys.path.insert(0, str(ROOT / 'scripts'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')

def clean_env():
    return {k: v for k, v in os.environ.items()
            if not any(s in k.upper() for s in ('KEY', 'TOKEN', 'SECRET', 'PASSWORD'))}

def run(argv, log, timeout=60, cwd=ROOT):
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    try:
        p = subprocess.run([str(x) for x in argv], cwd=cwd, env=clean_env(),
                           text=True, capture_output=True, timeout=timeout)
        log.write_text(p.stdout + p.stderr)
        result = {'argv': [str(x) for x in argv], 'returncode': p.returncode,
                  'status': 'complete' if p.returncode == 0 else 'error'}
    except subprocess.TimeoutExpired as e:
        def text(x): return x.decode(errors='replace') if isinstance(x, bytes) else (x or '')
        log.write_text(text(e.stdout) + text(e.stderr))
        result = {'argv': [str(x) for x in argv], 'returncode': None, 'status': 'timeout'}
    result.update(seconds=time.perf_counter()-started, log_sha256=sha(log))
    return result
