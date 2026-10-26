# Independent Claude Code cross-check protocol

**Executed 26 October 2026:** The two-stage protocol was automated in [`run_claude_queue_audit.py`](../scripts/run_claude_queue_audit.py) and completed on the GPT-6 Sol queue result with Claude Code 2.1.310 and `claude-opus-5-5`. The [saved audit and disposition](../results/queue_bc_gpt6sol_20261026/claude_audit_v2/disposition.md) supersede the pending-authentication note at the bottom, which documents the earlier attempt. The CLI uses `--bare`, so it reads `ANTHROPIC_API_KEY` directly and does not require OAuth login. Its first pass has no tools; the second permits only Read, Glob, and Grep. No key is saved in prompts or outputs.

Claude Code is an adversarial **reviewer** of the saved queue pilot, not the coverage oracle. Never give it credentials or permission to edit the DUT, checker, measurement scripts, or saved results. Its opinion cannot replace Verilator counters, checker controls, source-map proofs, or replay.

## Stage 1: blinded outcome interpretation

From the repository root, create the aggregate packet:

```sh
python3 scripts/prepare_claude_queue_audit.py --output build/claude_audit/blind.json
```

Supply the packet alone to Claude Code with tools disabled and independent session persistence disabled. Ask:

> Review this anonymous X/Y matched-pilot evidence as a skeptical methodologist. Check per-round target costs against cumulative rows; compare X and Y within each RTL version on coverage, API tokens, cycles and simulator executions; identify ceiling effects, uncertainty, and limitations. Do not infer which arm used semantic feedback. Do not claim statistical significance. Return specific arithmetic discrepancies, if any, and a concise conclusion. The aggregate packet alone cannot establish checker validity or feedback isolation.

Do not show the report, script source, result directory, or B/C mapping during this first pass. Save the full returned model ID, response, cost, and timestamp. A readable prompt file can be generated from the quoted instruction plus `build/claude_audit/blind.json`; the authenticated CLI may then be invoked noninteractively with `claude -p --tools '' --no-session-persistence --permission-mode plan --max-budget-usd 1.00 --output-format json < build/claude_audit/blind_prompt.txt > build/claude_audit/blind_response.json`. This command requires a working Claude Code login/network connection.

## Stage 2: unblinded artifact audit

Reveal X=B, Y=C only after Stage 1 is saved. Provide read-only access to the frozen `results/queue_bc_live_20261021_unsandboxed/` artifacts, `examples/heldout_queue/` sources and provenance, `docs/heldout_queue_preflight.md`, and `docs/milestone_2026-10-26.md`. Ask Claude to challenge, with file-and-row citations:

1. DUT/spec/checker/driver/coverage denominator/budget equality between B and C within each version.
2. Raw coverage-array identity in corresponding rendered prompts and absence of solver witnesses or reference vectors.
3. Width, signedness, complete activation guards, source joins, supported two-state rewrite proofs, and separation of read/write behavior.
4. Token/retry accounting and cumulative replay cycles/executions; checker-failure coverage flush.
5. The final report's claim of no measured C-over-B gain and its stated limits.

Verify any reported discrepancy using raw files and the existing replay, not by accepting either agent's narrative. Record a resolved/unresolved disposition for each finding. The existing replay and checker tests are the independent quantitative cross-check; Claude is a second qualitative analyst.

At the time this protocol was authored, Claude Code 2.1.126 existed on the machine. The sandboxed auth query and minimal call timed out; a bounded, read-only unsandboxed call then returned HTTP 401: `OAuth access token is invalid`. The user must complete `claude auth login` in their own terminal before retrying. **No Claude review has been performed or claimed.**
