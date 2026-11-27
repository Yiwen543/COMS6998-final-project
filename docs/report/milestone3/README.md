# COMS 6998 B5 — P3 report (November 25, 2026)

This is the completed P3 report using the course-provided `IEEEtran.cls` (unchanged). The main report is **two US Letter pages**, 10 pt, two columns, with the four required P3 sections. It includes the two short references on page 2. The filled report retains the original B5 team names/UNIs and the P3 deadline from the instructor's ZIP.

## Build or upload

- Overleaf: upload the complete source ZIP as a new project, set the main document to `main.tex`, and select **pdfLaTeX**. Click Recompile.
- TeX Live/MacTeX: `latexmk -pdf main.tex` (or `pdflatex main.tex` twice).
- `figure1.pdf` is the vector figure used by the report. No Python or external downloads are needed to compile. To regenerate the figure, install Matplotlib and run `python3 make_figure.py`; `figure_data.json` contains the archived real scoped stages and the Mac nine-property typed-check data, including the source archive SHA-256. It also writes a PNG preview.
- Both references are written directly in `main.tex`; BibTeX is not required. The supplied `IEEEtran_HOWTO.pdf` documents the official class. Author names for the two referenced papers were checked against the linked arXiv records.

## Evidence map (paths in the project repository)

| Report topic | Reproduction and underlying evidence |
| --- | --- |
| P2 comparison and guard acceleration | `docs/milestone3.md`, `docs/milestone3_followup.md`, `results/milestone3/engine/summary.json`, `results/milestone3/rtl-certified/summary.json` |
| Coverage waiver, withdrawal, real RTL edits and temporal reset property | `docs/milestone3_proof_applications.md`, `docs/m3_formal.md`, `results/milestone3/coverage-waiver/`, `results/milestone3/proof-withdrawal/`, `results/milestone3/eco-impact/` |
| FIFO assertions, formal verification, actual LLM run | `docs/egg_fifo_assertions.md`, `docs/egg_fifo_llm_live_results.md` |
| Frame repair, diagnostic extraction and restricted-cube proof feedback | `docs/egg_frame_live_results.md`, `docs/egg_frame_diagnostic_results.md`, `docs/egg_frame_pc_results.md`, `docs/egg_frame_pc_live_results.md` |
| Transaction specs / original RTL BMC / actual API ceiling | `docs/egg_frame_txn_results.md`, `docs/egg_frame_txn_live_results.md`, `results/milestone3/frame-txn-formal/summary.json` |
| Scoped equality and cross-context regression | `docs/egg_txn_context_results.md`, `docs/egg_regression_results.md`, `docs/egg_regression_live_results.md` |
| Dependency-driven proof reuse and Mac/Linux replication | `docs/egg_dependency_reuse_results.md`, `docs/egg_dependency_mac_results.md`, `results/milestone3/frame-txn-dependency-reuse/`, `results/milestone3/frame-txn-dependency-reuse-mac/` |
| Related work / bounded research claim | `docs/egg_related_work_and_research_value.md` |

The report is a synthesis of archived results, not another experiment or a claim of general formal equivalence. The 16-entry/16-bit FIFO holdout, demand-driven construction, explanation selection, persistent worker and new matched feedback trial are explicitly **planned** M4 work, not completed P3 measurements. No specific instructor feedback is inferred beyond the supplied P2 report, post-P2 results and audit.
