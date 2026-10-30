#!/usr/bin/env python3
"""Stage only an OpenAI key for a short live development trial; never echo it."""
import getpass
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "build/private/midterm-openai-key"


def main():
    if DEST.exists():
        raise SystemExit("Staged key already exists; no overwrite performed")
    value = getpass.getpass("OPENAI_API_KEY (hidden): ")
    if not value:
        raise SystemExit("No key entered")
    DEST.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    DEST.parent.chmod(0o700)
    fd = os.open(DEST, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w") as stream:
        stream.write(value)
    print("OpenAI key staged securely; value hidden")


if __name__ == "__main__":
    main()
