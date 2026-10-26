"""Temporarily hand off API credentials from the user's terminal to this workspace.

Run locally in an interactive terminal. The file is under ignored build/, is
mode 0600, and must be removed after the milestone run. Never paste keys into
chat, source files, or command arguments.
"""

from __future__ import annotations

import getpass
import argparse
import json
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "build/private/milestone1-credentials.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace-anthropic", action="store_true",
                        help="Prompt for and replace only the staged Anthropic key")
    args = parser.parse_args()
    if args.replace_anthropic:
        if not DEST.exists() or DEST.stat().st_mode & 0o077:
            raise SystemExit("Secure credential handoff file is missing or permissions are too broad.")
        values = json.loads(DEST.read_text(encoding="utf-8"))
        value = getpass.getpass("New ANTHROPIC_API_KEY (input hidden): ")
        if not value:
            raise SystemExit("No key entered; existing file unchanged.")
        values["ANTHROPIC_API_KEY"] = value
        fd, name = tempfile.mkstemp(prefix="milestone1-", suffix=".json", dir=DEST.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(values, stream)
            os.chmod(name, 0o600)
            os.replace(name, DEST)
        finally:
            if os.path.exists(name):
                os.unlink(name)
        print(f"Anthropic credential replaced at {DEST} (value hidden)")
        return
    if DEST.exists():
        raise SystemExit(f"Credential handoff already exists at {DEST}; remove it only after the current run is finished.")
    values = {}
    for name in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        value = os.environ.get(name) or getpass.getpass(f"{name} (input hidden): ")
        if not value:
            raise SystemExit(f"Missing {name}; no credential file created.")
        values[name] = value
    DEST.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    DEST.parent.chmod(0o700)
    fd = os.open(DEST, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(values, stream)
    print(f"Credential handoff ready: {DEST} (mode 0600; values hidden)")


if __name__ == "__main__":
    main()
