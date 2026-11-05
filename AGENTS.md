# Repository agent instructions

These rules govern maintenance, never experimental prompts. User instructions take precedence.

## Resume with bounded context

1. Read `docs/HANDOFF.md`, then `docs/PROJECT_STATUS.md`.
2. Read `docs/EXPERIMENT_PROTOCOL.md` before experimental work; consult `docs/DECISIONS.md` for rationale.
3. Use `rg` and bounded source slices. Read relevant summaries before raw JSONL/logs. Do not print giant freeze manifests.
4. `docs/AGENT_HANDOFF.md` is the retained historical recovery log, not a required full-context preload.
5. Update the compact handoff after a substantive phase. Preserve exact paths, hashes, failures and unresolved findings; never copy keys or full conversations.

## Preserve experimental boundaries

- Freeze DUT, specification, checker, driver, source counters, target, inputs, model and resource caps within each registration. Material changes require a new version; never tune against C outcomes.
- Current role boundary: Claude authors/revises the independent specification reference checker; GPT/Codex builds drivers/infrastructure. Experimental GPT generates stimulus in the original track and candidate SV monitors in `test2`. Candidate code never grades itself. Do not silently patch a Claude oracle as GPT.
- Keep calibration witnesses, final data, mutants, reference code and maintainer instructions out of candidate prompts. Use explicit allowlists and saved prompt hashes. Never auto-inject skills.
- Original stimulus qualification requires semantic proof, exact mapping, ordinary-operation exclusion, independent reachability and the registered B development gate before C. WBXBAR has a **local exploratory waiver** in `configs/wbxbar_exploratory_bc_v1.json`; do not generalize it.
- `test2/AGENTS.md` defines the separately authorized fixed-stimulus property task. Its gates differ from the original stimulus-difficulty gate.
- Preserve widths, signedness, complete activation guards, provenance and clock/reset context. Two-state combinational equivalence proves neither four-state nor sequential correctness. Keep every source counter separate; unknown/unreachable-unproven points remain in raw denominators.
- Retain invalid/missing/unresolved/not-reached runs and costs. Separate repeat alarms from distinct defect types, mock/replay from independent live trials, and finite BMC/cover from proof.
- Existing freezes bind code and evidence: check membership before edits. Add a new report/version instead of silently invalidating frozen inputs.

## Work and verify

- Current migration scope is documentation/audit only: no functional edits, paid calls, installation, simulation, long tests, commit or push unless subsequently requested.
- Use hidden-input scripts only when a new live stage is ready and authorized; credentials stay in ignored `build/private/` with restricted permissions and the agreed cleanup policy. Never reuse keys from chat.
- Run verification proportional to a change. Historical test evidence is not a fresh run; state dates, scope, commands and failures honestly. Do not rerun costly experiments to edit prose.
- Preserve unrelated user work and all historical result evidence. Do not equate local `main` with a verified remote push.
- Installed skill lock: `configs/agent_skills.lock.json`. Use context-compression at phase boundaries, karpathy-guidelines for surgical changes, verification-before-completion before claims, and caveman only for concise chat. Do not preload every skill; none enlarges the context window or guarantees correctness.

Previous instructions are preserved byte-for-byte in `docs/archive/migration_2026-11-04/AGENTS.md`.
