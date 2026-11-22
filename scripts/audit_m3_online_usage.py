#!/usr/bin/env python3
"""Reconcile the six archived controller Responses API calls against their ledger."""
import argparse
import gzip
import hashlib
import json
import tempfile
from pathlib import Path
from urllib.request import urlopen

from fetch_m3_reference import COMMIT, REPOSITORY

RUN = "test2/results/controller-done-bc-retest-v3"
HASHES = {
    "calls.jsonl": "ce5a53715363042a88d8ac29d5b326fafd147fcad947a0841d868928315d913d",
    "ledger.json": "afde54da71e13a988ccc7c8de36f7f180f841b67d048fd2a4074e9dcb35660ac",
    "summary.json": "8cf6c221a572c3ea6cf2fd0ec4714102404a88723ec86727a222166b707f453d",
}
SCHEDULE = [("B2_raw", 1), ("C2_semantic", 1), ("C2_semantic", 2),
            ("B2_raw", 2), ("B2_raw", 3), ("C2_semantic", 3)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_sources(directory):
    sources = {}
    for name, sha256 in HASHES.items():
        if directory is None:
            url = f"https://raw.githubusercontent.com/{REPOSITORY}/{COMMIT}/{RUN}/{name}"
            with urlopen(url, timeout=30) as response:
                data = response.read()
        else:
            path = directory / name
            data = path.read_bytes() if path.exists() else gzip.decompress((directory / (name + ".gz")).read_bytes())
        require(hashlib.sha256(data).hexdigest() == sha256, f"{name}: SHA-256 mismatch")
        sources[name] = data
    return sources


def reconcile(sources):
    calls = [json.loads(line) for line in sources["calls.jsonl"].splitlines()]
    ledger = json.loads(sources["ledger.json"])
    summary = json.loads(sources["summary.json"])
    events = ledger["events"]
    require(ledger["mode"] == summary["mode"] == "live" and ledger["completed"], "incomplete live archive")
    require(len(events) == len(calls) == len(SCHEDULE) == summary["confirmed_provider_responses"]
            == summary["API_dispatch_attempts"] == ledger["api_provider_confirmed_requests"]
            == ledger["api_dispatch_attempts"], "dispatch/response counts disagree")
    require(summary["remote_count_requests"] == ledger["counts_reserved"] == 0, "unexpected count requests")
    rows, totals, seen = [], {}, set()
    for call, event, (arm, round_number) in zip(calls, events, SCHEDULE):
        tag = f"{arm} round {round_number}"
        provider = call["provider_response"]
        raw = provider["usage"]
        require(call["mode"] == "live" and call["accepted_response"] and call["attempt"] == 1
                and call["arm"] == arm == event["context"]["arm"]
                and call["round"] == round_number == event["context"]["round"], f"{tag}: dispatch identity mismatch")
        require(not event["simulated"] and call["status"] == provider["status"] == "completed" and
                call["returned_model"] == provider["model"] == "gpt-6.1-sol" and
                call["returned_service_tier"] == provider["service_tier"] == "default", f"{tag}: provider mismatch")
        response_id = provider["id"]
        require(response_id and response_id == call["response_id"] == event["result"]["response_id"]
                and response_id not in seen, f"{tag}: duplicate or inconsistent response ID")
        seen.add(response_id)
        require(raw == call["raw_usage"] == event["result"]["provider_response"]["usage"], f"{tag}: raw usage drift")
        usage = {k: raw[k] for k in ("input_tokens", "output_tokens", "total_tokens")}
        usage["cached_input_tokens"] = raw["input_tokens_details"]["cached_tokens"]
        usage["reasoning_output_tokens"] = raw["output_tokens_details"]["reasoning_tokens"]
        require(all(type(v) is int and v >= 0 for v in usage.values()) and
                usage["input_tokens"] + usage["output_tokens"] == usage["total_tokens"] and
                usage["cached_input_tokens"] <= usage["input_tokens"] and
                usage["reasoning_output_tokens"] <= usage["output_tokens"], f"{tag}: invalid token accounting")
        require(usage == call["usage"] == event["usage"], f"{tag}: ledger usage drift")
        rows.append({"arm": arm, "round": round_number, **usage})
        aggregate = totals.setdefault(arm, {k: 0 for k in usage})
        for key, value in usage.items():
            aggregate[key] += value
    upper = sum(e["settled_upper_micro_usd"] for e in events)
    require(upper == ledger["settled_upper_micro_usd"] == summary["settled_upper_micro_usd"], "cost upper mismatch")
    total = sum(arm["total_tokens"] for arm in totals.values())
    if summary["actual_generation_tokens"] is not None:
        require(total == summary["actual_generation_tokens"], "summary usage drift")
    return {"scope": "Historical provider responses on the published M2 controller", "new_api_requests": 0,
            "source": {"repository": REPOSITORY, "commit": COMMIT, "path": RUN, "sha256": HASHES},
            "calls": rows, "by_arm": totals, "reconstructed_total_tokens": total,
            "archived_summary_actual_generation_tokens": summary["actual_generation_tokens"],
            "settled_upper_micro_usd": upper, "actual_invoice_usd": summary["actual_invoice_usd"],
            "monitor_replays": summary["monitor_replays"], "new_DUT_simulations_in_archive": summary["new_DUT_simulations"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, help="read pinned .json[l] or .gz locally; default fetches public files")
    parser.add_argument("--output", type=Path, required=True, help="fresh directory for report and compressed source copies")
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        parser.error("output must be a new directory")
    sources = load_sources(args.source_dir)
    report = reconcile(sources)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.output.parent) as tmp:
        staged = Path(tmp) / "audit"
        staged.mkdir()
        for name, data in sources.items():
            (staged / (name + ".gz")).write_bytes(gzip.compress(data, mtime=0))
        (staged / "audit.json").write_text(json.dumps(report, indent=2) + "\n")
        staged.rename(args.output)
    print(f"{len(report['calls'])} archived responses, {report['reconstructed_total_tokens']} tokens")


if __name__ == "__main__":
    main()
