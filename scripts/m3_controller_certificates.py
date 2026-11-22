"""Recheck each supplied Controller rule against its original, pinned QF_BV obligation."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess


MANIFEST = Path(__file__).with_name("m3_controller_replay_manifest.json")


def verify_rules(screen_dir, z3="z3"):
    sources = json.loads(MANIFEST.read_text())["sha256"]
    hashes = {name: sources[f"qualification/typed-v5/screen/{name}"]
              for name in ("egg-input.json", "pairs.smt2", "query-order.json")}
    files = {}
    for name, expected in hashes.items():
        data = (Path(screen_dir) / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"Controller certificate source changed: {name}")
        files[name] = data.decode()
    payload = json.loads(files["egg-input.json"])
    order = json.loads(files["query-order.json"])
    prefix, *queries = files["pairs.smt2"].split("(push)\n")
    if len(order) != len(queries):
        raise ValueError("archived query index has wrong length")
    by_pair = {tuple(ids): block for ids, block in zip(order, queries)}
    targets = {t["id"]: t for t in payload["targets"]}
    definitions = set(prefix.splitlines())
    for name, target in targets.items():
        if f"(define-fun {name} () Bool {target['compact']})" not in definitions:
            raise ValueError(f"unbound guard definition: {name}")
    proof_queries = [prefix]
    names = []
    for rule in payload["verified_rules"]:
        a, b = rule["source_ids"]
        block = by_pair[a, b]
        if block.splitlines() != [f"(assert (xor {a} {b}))", "(check-sat)", "(pop)"]:
            raise ValueError(f"wrong archived query for {a}, {b}")
        for key, target in (("left", targets[a]), ("right", targets[b])):
            if rule[key] != target["compact"] or rule["event_context"] != target["event_context"]:
                raise ValueError(f"rule/context mismatch: {rule['name']}")
        proof_queries.append("(push)\n" + block)
        names.append(rule["name"])
    response = subprocess.run([z3, "-in", "-smt2"], input="".join(proof_queries),
                              text=True, capture_output=True, check=True, timeout=120)
    statuses = response.stdout.splitlines()
    if len(statuses) != len(names) or any(status != "unsat" for status in statuses):
        raise ValueError(f"inconclusive or invalid certificates: {dict(Counter(statuses))}")
    return {"targets": len(targets), "archive_queries": len(order), "rule_queries": len(names),
            "results": dict(zip(names, statuses)), "sha256": hashes,
            "z3": subprocess.check_output([z3, "--version"], text=True).strip()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("screen_dir", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_rules(args.screen_dir), indent=2))
