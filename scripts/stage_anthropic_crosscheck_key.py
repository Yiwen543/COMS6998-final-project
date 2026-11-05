#!/usr/bin/env python3
"""Hide-stage an Anthropic key for one read-only result audit."""
import getpass
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "build/private/anthropic-crosscheck-key"


def main():
    if DEST.exists():
        raise SystemExit("An Anthropic key is already staged; finish that audit first")
    key = getpass.getpass("ANTHROPIC_API_KEY (input hidden): ").strip()
    if not key:
        raise SystemExit("No key entered")
    if not key.isascii():
        raise SystemExit("Not staged: input contains non-ASCII characters. Paste only the API key, not a confirmation message.")
    if not re.fullmatch(r"sk-ant-[A-Za-z0-9_-]+", key):
        raise SystemExit("Not staged: expected an Anthropic key starting with sk-ant-. Paste only the key, without quotes, spaces or an export command.")
    DEST.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    DEST.parent.chmod(0o700)
    fd = os.open(DEST, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        stream.write(key)
    print("Anthropic key staged with mode 0600; value hidden. Local format check passed; API authentication not tested.")


if __name__ == "__main__":
    main()
