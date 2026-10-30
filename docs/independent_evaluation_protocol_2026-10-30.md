# Independent evaluation roles for the next natural-IP study

This protocol addresses the concern that one GPT agent might select the DUT,
construct feedback, generate stimulus, and then judge its own result. The
completed [FIFO pilot](sfifo_stress_abpc_result_2026-10-30.md) shows a useful
separation: Claude's **pre-outcome** review found a B-derived target threshold,
weak cycle slack, model-visible hints and a calibration-dependent C filter.
Those were fixed before the formal run. Claude's blind and revealed
post-outcome reviews then recomputed costs and challenged interpretation.
The original Verilator counters, Yosys equivalence proof, Z3 guard checks and
public-I/O checker remained the sources of record.

| Responsibility | Recommended owner | Independent gate |
| --- | --- | --- |
| Functional specification and legal input assumptions | Human review of upstream documentation, with separate checker author | Versioned contract and explicit ambiguity list |
| DUT selection and target | Outcome-blind static screen plus separate B-only development gate | Claude pre-outcome review before file-hash freeze; record every screened candidate and rejection |
| Checker and fixed JSON driver | Engineer or Claude Code in an isolated implementation branch | Human review, separately written behavioral passing control, single-fault mutants, selected formal properties; freeze checker/driver hashes |
| Typed guard extraction and C feedback renderer | Deterministic Yosys/Rust egg/Z3 pipeline; either model may write code before freeze | Z3 pair checks, rewrite proofs, complete activation/event/source mapping, original-counter preservation, unsupported-case report, prompt-isolation tests |
| Experimental stimulus | Fixed GPT Responses model in independent A/B/P/C sessions | Exact JSON schema, unchanged budget/model/settings, per-call logs; no checker/RTL edits |
| Coverage and functional truth | Verilator raw DUT counters and specification checker; SymbiYosys/Yosys for formal claims | Offline replay, source-counter identity checks, proof logs and witnesses; no LLM verdict replaces these |
| Outcome analysis | Deterministic CSV/plot script plus Claude blind aggregate audit, then read-only revealed file audit | Independent recomputation of target cost and defect categories, documented dispositions for disagreements |

Claude can implement an **independent evaluation script** that reads immutable
JSONL and `.dat` files, recomputes metrics and classifies checker/formal
outcomes in a separate branch. Compare its outputs with the existing analyzer
before interpreting treatment labels. Let it write checker or semantic-parser
code only **before** the experiment is frozen, and validate that code against
independent controls. Giving Claude live control of C's semantic feedback
while B uses a deterministic template would change two factors at once:
feedback semantics and a second model's prompting decisions. That would not
isolate the E-graph effect. Likewise, Claude should not quietly generate
stimulus in only one arm.

If cross-model robustness is desired, run a separately preregistered 2×2
extension: generator model (GPT versus Claude) crossed with feedback (B versus
C), using the same fixed DUT/checker/driver and equal per-model budgets.
An auditor that has seen the outcome should not select targets or alter
checkers for that same trial. For the next natural held-out IP, select and
freeze a specification-clear controller/FIFO with several proven,
source-distinct late groups; count all original raw locations, and keep every
failed or target-missing repetition. A constructed variant is useful as a
mechanism stress test but cannot support natural-design generalization.
