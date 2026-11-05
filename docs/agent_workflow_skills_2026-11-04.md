# Maintainer skills and context recovery — 4 November 2026

Installed four upstream skills at fixed GitHub revisions in
`/Users/yiwenchen/.codex/skills/`. They are for the coding/maintenance agent;
they are not added to experimental GPT or Claude prompts. Installed skills become
available for normal selection on the next turn. Their reviewed instructions
were applied manually in this turn to establish the workflow below.

## Selection and actual use

- [context-compression](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/9ff0c99108b36d3b886defd825d8ac1f47dba374/skills/context-compression/SKILL.md): maintain an incremental, readable handoff preserving intent, constraints, artifacts, observed state and next action. Applied by creating [AGENT_HANDOFF.md](AGENT_HANDOFF.md), checking its numeric claims and exact paths against local evidence, and adding a resume entry in [AGENTS.md](../AGENTS.md).
- [karpathy-guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md): explicit assumptions, minimal implementation, focused edits and verifiable success criteria. This is a community interpretation of Karpathy's observations, not an official Karpathy-authored package. Applied here by limiting repository edits to four new workflow/record files; no research scripts or frozen artifacts were edited.
- [verification-before-completion](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/verification-before-completion/SKILL.md): verify before making a completion claim. Applied by comparing all eight installed files with GitHub Git blob hashes, checking declared skill names, validating handoff facts/paths, and freshly invoking the existing SPI freeze verifier.
- [caveman](https://github.com/JuliusBrussee/caveman/blob/2e068f735253cce28256744804785f01887d9646/skills/caveman/SKILL.md): concise conversation with exact technical details retained. Applied to chat updates. It is a communication style, not a correctness checker; code, comments, reports, hypotheses, prompts and proof evidence are not compressed by it. Detailed explanations remain appropriate when requested.

## Installation and verification

[agent_skills.lock.json](../configs/agent_skills.lock.json) contains upstream
repositories, commit SHAs, paths, exact file blob hashes and the installation
method. The built-in `skill-installer` helper was used. Python ZIP download
failed with `CERTIFICATE_VERIFY_FAILED`; its supported Git method then installed
all four successfully. TLS verification was not disabled and no shell startup
or certificate settings were changed.

The four `SKILL.md` files and package file listings were reviewed. Optional
context-compression evaluator scripts were installed as upstream files but were
not run or configured. No Caveman CLI, proxy, plugin hooks or telemetry service
was installed. No project data was sent to the skill repositories. No model API
key or model API invocation was needed.

Fresh local checks confirmed:

1. All 8 installed file contents match the pinned upstream Git blob SHA-1 values;
   each skill directory has exactly the expected file set and skill name.
2. Handoff paths exist; preregistration SHA-256, fixed 3×6×64/8-cycle budget,
   384-cycle calibration bound, candidate states and `m_stall` blocker match the
   scope/audit artifacts. This is a limited recovery check, not a benchmark of
   summarization quality or an independent LLM evaluation.
3. `spi_core_safe_experiment.verify_freeze()` passes. The original DUT/checker/
   driver/targets/denominator freeze is unchanged. Earlier 31-test results are
   labeled historical in the handoff; this documentation task did not rerun a
   research experiment or claim new B/C results.

## Operating boundary

On resume, read the short handoff first, then the relevant source/report section.
Retrieve full logs only when needed. At a phase boundary, merge new observations
into the appropriate handoff sections; retain negative results and uncertainty.
Do not repeatedly summarize summaries without consulting their source artifacts.

These skills cannot expand the host model's context window, force host compaction,
or guarantee fewer coding errors. Reduced rereading and better constraint retention
are intended workflow benefits, not measured findings from this project. Correctness
still depends on concrete tests, counterexamples, source/proof validation and the
independent checker process. Do not change experimental feedback or token budgets
because maintainer skills were installed.
