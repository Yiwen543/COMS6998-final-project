#!/usr/bin/env python3
"""Check official input-token matching without generating model stimulus."""
from __future__ import annotations

import json
import os
import time

from coverage import load
from pilot_model import OpenAIModel
from run_midterm_b_development import KEY_FILE
from run_midterm_fixed import ROOT, sha
from run_sfifo_stress_fixed import SOURCE
from sfifo_fixture import schema
from sfifo_stress_feedback import messages_for
from token_placebo import match_placebo

CONFIG = ROOT / "configs/sfifo_stress_abpc_frozen.json"
SCREEN_DIR = ROOT / "results/midterm_candidate_preflight/sfifo-stress"
OUT = ROOT / "results/sfifo_stress_token_preflight_20261030"


def main():
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:
        raise RuntimeError("Hidden OpenAI key missing or permissions too broad")
    OUT.mkdir(parents=True, exist_ok=False)
    config = json.loads(CONFIG.read_text())
    screen = json.loads((SCREEN_DIR / "screen.json").read_text())
    semantic = json.loads((SCREEN_DIR / "semantic.json").read_text())
    seed = json.loads((SCREEN_DIR / "seed.json").read_text())
    log = (SCREEN_DIR / "seed.sim.log").read_text()
    points = load(SCREEN_DIR / "seed.dat", str(SOURCE.relative_to(ROOT)), include_descendants=True)
    c_messages = messages_for("C", [], seed, log, points, semantic, screen, 1,
                              config["max_new_cycles"])
    try:
        os.environ["OPENAI_API_KEY"] = KEY_FILE.read_text().strip()
        adapter = OpenAIModel(config, schema=schema(), schema_name="sfifo_stress_actions")
        started = time.perf_counter()
        p_messages, evidence = match_placebo(c_messages, adapter.count_input_tokens,
                                              tolerance=config["placebo_tolerance_tokens"])
        evidence["wall_seconds"] = time.perf_counter() - started
        evidence["requested_model"] = config["model"]
        evidence["scope"] = "official count-only preflight; zero model generation calls; excluded from pilot costs"
        evidence["config_sha256"] = sha(CONFIG)
        (OUT / "count-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
        (OUT / "c-prompt.json").write_text(json.dumps(c_messages, indent=2) + "\n")
        (OUT / "p-prompt.json").write_text(json.dumps(p_messages, indent=2) + "\n")
        print(json.dumps(evidence, indent=2))
    finally:
        os.environ.pop("OPENAI_API_KEY", None)


if __name__ == "__main__":
    main()
