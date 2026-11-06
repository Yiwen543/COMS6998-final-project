# COMS6998 Midterm — Nov 6, 2026

Six English slides, English speech and Chinese preparation notes. Made with [PPT Master](https://github.com/hugohe3/ppt-master) v6.8.0, Hugo He, MIT. Final PPTX uses editable DrawingML text and shapes; chart bars are editable shapes rather than embedded PowerPoint Chart objects. English speech is embedded in each slide's Notes.

## Start here
- COMS6998_Midterm_6_Slides.pptx — classroom editable deck.
- COMS6998_Midterm_6_Slides.pdf — portable, final-PPTX-rendered copy.
- COMS6998_Speaker_Script_EN_ZH_6_Pages.pdf — one page per slide, timed English script plus Chinese preparation notes.
- COMS6998_Speaker_Script_EN_ZH.md — editable script.
- COMS6998_Deck_Preview.png — overview of all six slides.

## Three-person division
| Speaker | Slides | Slot | Preparation responsibility |
|---|---|---|---|
| Chiyu Chen | 1–2 | 0:00–1:40 | Question, proposal and implemented prototype; stimulus/monitor distinction |
| Mingyuan Zheng | 3–4 | 1:40–3:30 | Fair methodology, hidden-set isolation, queue graph and coverage definitions |
| Yiwen Chen | 5–6 | 3:30–5:30 | Latest test2 cost/results, formal limits, P2 analysis and classroom feedback |

Assignments are for presenting/preparing this deck, not a record of historical code ownership. There are 643 English words: about 5:09 at 125 words/min plus roughly 21 seconds of pauses/handoffs. Total target 5:30; six-minute limit. Chinese notes are not spoken. This is an estimate, not a recorded rehearsal.

## Evidence and limitations
Charts derive from saved project evidence; no experiments were rerun. Queue chart: mean API input+output tokens to first reach 41/41 raw emitted line/case counters. One IP in two syntax forms; 2/6 index-matched comparisons earlier for C, four ties; final coverage identical. Model sessions are not deterministic paired RNG trials. Semantic-class grouping does not transfer counter hits. Latest test2 chart: full-cohort input+output tokens across 18 rounds per arm; B740643, C813649, +9.8571%. All final monitors detect 11/11 observable types; raw 12-type denominator retains N10. Unknowns and invalid earlier rounds remain in the research evidence. No token-matched placebo in this cohort: the effect is for the complete feedback package.

Formal: 540 native statuses =75PASS+104FAIL+361TIMEOUT; 104FAIL=94BMC+7prove+3cover. 94BMC=20 physical selected-alarm reproductions+74 unreproduced/unresolved (all C:7 correct/67 mutant). No reference verdict is recorded for those74; these are not confirmed oracle false alarms. B3/C7 is the pooled mutant-type range for an earlier physical-prefix diagnostic, not same-sample/category oracle confirmation, mean replicate improvement or 128-cycle completion proof. One concrete X-to-anyseq mapping issue is confirmed; it is not established as the root cause of all74. P02 PASS_WITH_LIMITS accepts the reporting disclosure scope, not general monitor soundness. R0/R1/R2 controlled recovery comparison remains planned.

Source paths and SHA256 are in source_manifest.json. Selected source hashes were checked unchanged after authoring. The research repository HEAD observed was c25180848ebfe9a1f49da0aa5f579cac913e6428; existing dirty work was preserved. No research code/config/result was edited.

## Authoring and verification
PPT Master: planning spec/lock -> six SVG pages -> numeric chart geometry checks -> final SVG gate (zero blocking/zero advisory findings) -> six English notes -> split notes -> finalize SVG -> native DrawingML export. Final PPTX was converted with LibreOffice and all six resulting pages visually inspected; the six script PDF pages were also inspected. No Microsoft PowerPoint-native opening was performed. The live SVG editor could not start because Flask was unavailable; static previews are included. No paid API calls were made for this presentation.

Authoring sources are in authoring/. Graphs are in graphs/, with exact chart_data.json and queue_target_costs.csv. Main SVG sources are retained, so editing the PPTX is not dependent on reauthoring. To rebuild inside the original project workspace, use the installed PPT Master and the isolated presentation Python environment. Sequence: build_slides.py -> structure_midterm_svg.py -> PPT Master compact_svg_styles.py and stamp_native_fallbacks.py -> finish_midterm_svg.py -> verify_midterm_charts.py -> final SVG checker -> build_speaker_script.py -> total_md_split.py -> finalize_svg.py -> svg_to_pptx.py -t none -a none. All helper scripts use the project location; the PDF script assumes the original parent directory and installed macOS Arial fonts. Rebuilding exports is optional and does not rerun the research.
