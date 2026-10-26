"""Check access to Claude Opus 5.5 without displaying or storing the API key.

Run in the same terminal where ANTHROPIC_API_KEY was exported. This makes one
small Messages API request and prints only status, error type, and model ID.
"""

from __future__ import annotations

import json
import os
import ssl
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MODEL = "claude-opus-5-5"
API_VERSION = "2026-10-21"
URL = "https://api.anthropic.com/v1/messages"


def verified_tls_context() -> ssl.SSLContext:
    """Use a real CA bundle when framework Python's default path is absent."""
    try:
        import certifi
    except ImportError:
        system_bundle = Path("/etc/ssl/cert.pem")
        if system_bundle.is_file():
            return ssl.create_default_context(cafile=str(system_bundle))
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


def main() -> int:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        print("NOT TESTED: ANTHROPIC_API_KEY is absent in this terminal.")
        return 2

    payload = json.dumps(
        {
            "model": MODEL,
            "max_tokens": 16,
            "messages": [{"role": "user", "content": "Reply READY"}],
        }
    ).encode("utf-8")
    request = Request(
        URL,
        data=payload,
        method="POST",
        headers={
            "x-api-key": key,
            "anthropic-version": API_VERSION,
            "content-type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=25, context=verified_tls_context()) as response:
            body = json.load(response)
            status = response.status
    except HTTPError as exc:
        try:
            body = json.load(exc)
            error_type = body.get("error", {}).get("type", "unknown")
        except (ValueError, AttributeError):
            error_type = "unknown"
        print(f"UNAVAILABLE: HTTP {exc.code}; error_type={error_type}; model={MODEL}")
        return 1
    except URLError as exc:
        print(f"NOT TESTED: network_error={type(exc.reason).__name__}; model={MODEL}")
        return 3

    returned_model = body.get("model", "missing")
    if status == 200 and returned_model == MODEL:
        print(f"AVAILABLE: HTTP {status}; requested_model={MODEL}; returned_model={returned_model}")
        return 0
    print(f"UNVERIFIED: HTTP {status}; requested_model={MODEL}; returned_model={returned_model}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
