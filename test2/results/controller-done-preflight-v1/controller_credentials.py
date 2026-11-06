"""User-authorized credential retention across this reference repair/review task."""
import json
import os
from pathlib import Path
import tempfile
from common import ROOT, dump, sha
import reference_role


def invoke(role, packet, out):
    staged = ROOT / 'build/private/anthropic-crosscheck-key'
    if not staged.is_file() or staged.stat().st_mode & 0o077:
        raise RuntimeError('Missing staged key or unsafe permissions')
    # Keep the immutable caller's cleanup policy on a per-call0600 working copy;
    # the user's main staged file stays until this concrete task is complete.
    with tempfile.TemporaryDirectory(prefix='controller-key-', dir=staged.parent) as directory:
        working = Path(directory) / 'key'
        fd = os.open(working, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(staged.read_bytes())
        old = reference_role.KEY_FILE
        reference_role.KEY_FILE = working
        try:
            return reference_role.invoke(role, packet, out)
        finally:
            reference_role.KEY_FILE = old
            if out.exists():
                dump(out / 'credential-policy.json', {
                    'authorization': 'User2026-11-05: retain the staged key between reference repairs/reviews until task completion',
                    'main_staged_key_retained': staged.exists(), 'working_copy_removed_on_exit': True,
                    'adapter_sha256': sha(Path(__file__))})
