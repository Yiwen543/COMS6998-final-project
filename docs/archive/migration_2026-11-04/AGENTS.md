# Project agent workflow

These instructions govern repository maintenance, not experimental model prompts.
User instructions and higher-priority policies take precedence.

## Resume with bounded context

Read `docs/AGENT_HANDOFF.md` first. Check its evidence paths and current Git state.
Read only the current report and relevant source slices; use `rg` before loading
large logs. Keep full logs on disk and return decisive fields or error lines.
The handoff is an index, not a replacement for raw evidence. After a substantive
phase, incrementally update its intent, changed/read files, decisions, observed
results, blockers and next action. Keep exact paths, hashes, budgets and negative
results. Never copy API keys or conversation transcripts into these records.

## Apply installed skills selectively

Fixed upstream versions and file hashes: `configs/agent_skills.lock.json`.
Local copies are under `/Users/yiwenchen/.codex/skills/`:

- `context-compression/SKILL.md`: use at phase boundaries and after compaction;
  preserve constraints, evidence links and unresolved issues in the handoff.
- `karpathy-guidelines/SKILL.md`: use for implementation/review; state material
  assumptions, make the smallest necessary change, define observable success.
- `verification-before-completion/SKILL.md`: verify the relevant claim with
  fresh commands before reporting success. Report blocked/untested separately.
- `caveman/SKILL.md`: concise chat only. Preserve technical detail and uncertainty;
  do not shorten code, research reports, schemas, raw evidence or prompts.

Read the relevant skill when needed; do not load every skill on every turn.
Missing skills do not justify guessing their contents or installing substitutes.
These skills do not enlarge the context window or guarantee correct code.

## Preserve experimental independence

Keep original DUT/spec/checker/driver/coverage denominator and preregistered
budgets immutable within a frozen experiment. Changes require a separately
registered version; never tune budgets or targets to favor C. Retain failed
attempts and distinguish repeated diagnostics from distinct defect types.

Claude authors specification-based checkers; GPT/Codex authors fixed drivers and
stimulus. Do not silently repair a Claude checker as GPT. Calibration sequences,
golden answers, this handoff and maintainer skills must not leak into experimental
prompts or specification-only checker packets. Do not auto-inject skills into
either model adapter. Keep role packets and published prompt hashes authoritative.

Require semantic, exact source-mapping, ordinary-operation and independently
checked multistep-reachability gates before B; C follows the unchanged B gate.
User-authorized exception: `configs/wbxbar_exploratory_bc_v1.json` separately
waives ordinary/difficulty admission, three late-event families and the B-before-C
difficulty gate for its exploratory B/C comparison. Preserve the old rejection;
never generalize this exception to other scopes. Independent checker validation,
certified semantics, exact counters, equal budgets and final freeze remain required.
Two-state combinational equivalence is not sequential correctness or reachability.
Equivalent predicates retain separate original source counters; unresolved points
stay in the denominator. Request keys only when the relevant offline gate passes,
using the existing hidden-input staging scripts and cleanup policy.

## Verify and hand off

Run checks proportional to the change. Distinguish syntax/lint, proof, simulation,
checker validity and live-model evidence. Do not rerun costly experiments merely
to edit prose. Inspect diffs; preserve unrelated user work and historical results.
Record exact commands, exit status, scope and evidence paths. Do not claim a
commit, push, checker certification or completed experiment without direct evidence.
