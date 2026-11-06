<!-- ppt-master-schema: design-spec/v1 -->
# COMS6998 Midterm - Design Spec

## I. Project Information
| Item | Value |
|---|---|
| Project Name | COMS6998 E-graph RTL verification midterm |
| Canvas Format | PPT 16:9 |
| Page Count | 6 |
| Primary Language | en-US |
| Target Audience | COMS6998 instructors and classmates |
| Communication Intent | Explain question, prototype, controlled comparison and preliminary evidence |
| Desired Audience Outcome | Understand what is implemented and give targeted Nov 9 P2 feedback |
| Core Message / Ask / Action | A reproducible prototype exists; general E-graph benefit is not established |
| Delivery Context | Nov 6 classroom midterm, three speakers, under six minutes |
| Artifact Afterlife | Editable PPTX, portable PDF and six-page rehearsal script |
| Reading Mode | presentation |
| Content Strategy | brief |
| Design Style | Custom blue-white academic |
| AI Image Acquisition Path | not applicable; no images |
| Generation Mode | continuous; user delegated design confirmation |
| Spec Refinement | disabled |
| Speaker Notes | enabled; user explicitly requested per-slide speech |
| Custom Animations | disabled; all motion omitted under delegated design |
| Narration Audio | disabled |
| Created Date | 2026-11-05 |

## II. Canvas Specification
| Item | Value |
|---|---|
| Format | PPT 16:9 |
| Dimensions | 1280 x 720 |
| viewBox | 0 0 1280 720 |
| Margins | 64 px |
| Content Area | x64–1216, y56–638 |

## III. Visual Theme
### Theme Style
- **Mode**: custom
- **Mode Behavior**: Research question, implemented mechanism, comparison, evidence, limitations and proposed next step; claim-led titles with academic qualification.
- **Visual Style**: custom
- **Visual Style Behavior**: Original blue-white academic composition; clear baselines, editable diagrams and data marks, generous whitespace, minimal chrome, no decorative images.
- **Theme**: Frozen experiment and accountable evidence.
- **Tone**: Clear, technical and candid.
### Color Scheme
| Role | Color |
|---|---|
| Background | #FFFFFF |
| Secondary Background | #F4F7FC |
| Primary | #132A49 |
| Accent / B | #245DB5 |
| Secondary Accent / C | #008B8B |
| Body Text | #132A49 |
| Secondary Text | #5D6B7C |
| Divider | #D8E1EC |
| Unresolved | #A86612 |

## IV. Typography System
### Font Plan
| Role | Primary | Fallback |
|---|---|---|
| Title | Arial | sans-serif |
| Body | Arial | sans-serif |
- **Title Stack**: Arial
- **Body Stack**: Arial
### Font Size Hierarchy
| Purpose | Size |
|---|---|
| Title | 44 px |
| Body | 28 px |
| Subtitle | 28 px |
| Annotation | 20 px |
| Chart Label | 24 px |
| Footer | 16 px |
| Display | 64 px |

## V. Layout Principles
- Deck-wide hierarchy: question or claim first, supporting mechanism/evidence second, material qualification last.
- Composition tendency: vary cover, wide pipeline, paired comparison, graph pages and spacious close.
- Cross-page continuity: B blue, C teal, unknown amber; stable top kicker and lower source strip.
- Spacing posture: compact diagram labels but broad margins and explicit separation of distinct research tracks.
- Spacing anchors: page margin 64 px; block gap 24 px; gutter 32 px; corner radius 0 px; body leading 38 px.

## VI. Icon Usage Specification
- **Primary Bundled Library**: none
| Icon | Usage |
|---|---|

## VII. Visualization Reference List
| Page | Family | Template | Usage |
|---|---|---|---|
| P04 | chart | grouped_bar_chart | Compare mean tokens to target by RTL form and arm |
| P05 | chart | horizontal_bar_chart | Compare full-cohort API token totals by arm |

## VIII. Image Resource List
| Key | Path | Source | Status | Usage |
|---|---|---|---|---|

## IX. Content Outline

#### Slide 01 - Question and proposal
- **Audience move**: Understand the question and motivation
- **Relationships**: Contrast raw syntax with verified semantic grouping; group objectives under one research question.
- **Composition**: Question-led cover with three metric anchors.
- **Title**: Can semantic feedback improve LLM RTL verification?
- **Core Message**: Test whether verified E-graph feedback improves cost efficiency and monitor quality.
- **Content**: Proposal: supplement raw coverage with verified equivalent guard groups. Evaluate coverage efficiency, defect detection, and correctness. Coverage is not correctness; an E-graph class is not an RTL coverage point. Show full team names.
- **Fact IDs**: F01,F07

#### Slide 02 - Implementation and prototype
- **Audience move**: Understand what was actually implemented
- **Relationships**: Order the frozen generation/tool/feedback loop; contrast the two tracks; separate oracle from candidate.
- **Composition**: Wide tool pipeline over two distinct experiment lanes.
- **Title**: One tool loop, two verification tasks
- **Core Message**: The prototype compiles, measures and independently checks generated artifacts.
- **Content**: Spec + RTL -> GPT generation -> compile + EDA -> measured feedback -> next round. Rust egg plus a typed/guard-aware front end and Z3 check restricted two-state combinational groups. Track S generates JSON stimuli and measures actual RTL coverage; Track M/test2 fixes stimuli and generates passive SV monitors. Claude independent reference is separate from GPT candidates. Icarus/Verilator physical checks and Yosys/SMT formal diagnostics. Unsupported and four-state/sequential cases remain limited.
- **Fact IDs**: F01,F04,F08

#### Slide 03 - Methodology and baselines
- **Audience move**: Assess fairness and reproducibility
- **Relationships**: Contrast B and C on a common frozen foundation; order generation, freezing and hidden grading.
- **Composition**: Paired B/C panels with shared invariant band and freeze-to-score sequence.
- **Title**: B and C differ in feedback, not the test bench
- **Core Message**: A fixed comparison isolates the whole feedback package.
- **Content**: B = raw coverage plus common development feedback. C = B plus verified E-graph groups. Latest test2: fixed DUT, Claude checker, stimuli, gpt-6.1-sol/low; 3 independent sessions per arm × 6 rounds; 64k input and 8192 output caps each call. Freeze all 36 candidates before hidden scoring; exclude hidden faults, evaluation traces and reference code from prompts. Same caps are not equal realized token spend. No token-matched placebo in this cohort; pure semantic attribution remains open.
- **Fact IDs**: F04,F08

#### Slide 04 - Queue pilot results
- **Audience move**: Interpret the preliminary stimulus result
- **Relationships**: Compare B and C within each RTL form; contrast earlier target attainment and identical endpoints.
- **Composition**: Dominant grouped bar chart with a right-hand result statement.
- **Title**: Queue pilot: a small, mixed efficiency signal
- **Core Message**: C sometimes reached the target earlier, with no final coverage gain.
- **Content**: Original task: generate stimuli. gpt-6-sol, one queue IP in two RTL forms, 3 sessions per arm/form, 4 rounds. Plot mean input+output API tokens to reach 41/41 emitted line/case points: original B74890.667 C73738.333; variant B70271.667 C66377. C earlier by one round in 2/6 index-matched comparisons, four ties. These are not deterministic paired RNG trials. All final runs reached 41/41 line/case, 14/14 branch, 344/408 toggle; no final gain. Small exploratory pilot, no causal/statistical generalization; selected group members already hit after round 1.
- **Fact IDs**: F01,F02
- **Visualization**: queue-target-cost; grouped bars; data=chart_data.json/queue_means; axis 0–80 thousand API tokens.
- **Native-ready**: queue-target-cost=yes

#### Slide 05 - Test2 and formal results
- **Audience move**: Interpret current monitor results and cost
- **Relationships**: Compare equal final fixed-trace detection against total API cost; separate native formal status and physical replay.
- **Composition**: Horizontal token chart at left, two decisive result blocks at right, formal disclosure strip below.
- **Title**: test2: equal final detection, higher C token cost
- **Core Message**: C did not add fixed-trace kills; formal findings remain qualified.
- **Content**: Latest trace_done task: all 6 final monitors passed correct-DUT controls and detected 11/11 observable fault types, with N10 retained in the 12-type raw denominator. B740643 and C813649 total input+output tokens across all 18 rounds/arm: C+9.86%. One invalid earlier round and all unknowns retained. Native formal540=75PASS+104FAIL+361TIMEOUT; 104FAIL=94BMC+7prove+3cover. 94BMC=20 physical selected-alarm reproductions and 74 unreproduced/unresolved, all C. These are not confirmed oracle false alarms. Earlier physical-prefix mutant-type union B3/C7 is a secondary diagnostic only, not same-sample oracle confirmation. Short-depth safety projection is not 128-cycle completion proof.
- **Fact IDs**: F03,F04,F05,F06
- **Visualization**: monitor-token-cost; horizontal bars; data=chart_data.json/test2_totals; axis 0–900 thousand API tokens.
- **Native-ready**: monitor-token-cost=yes

#### Slide 06 - Analysis and P2 plan
- **Audience move**: Give appropriately limited conclusions and actionable feedback
- **Relationships**: Separate established implementation from open causal and semantic questions; order three proposed research steps.
- **Composition**: Spacious conclusion with numbered next-step spine and one feedback question.
- **Title**: Next: remove the ceiling, then test attribution
- **Core Message**: A working pipeline does not yet establish a general E-graph advantage.
- **Content**: Implemented: frozen prompts/candidates, independent grading, mock/replay, actual coverage/token accounting, physical/formal evidence. Evidence: queue mixed and small; latest fixed-trace monitor endpoint tied with C more tokens. Formal prefix union C7/B3 is local and qualified, with 74 unresolved BMC witnesses. Proposed Nov9 P2: unsaturated held-out temporal obligations; token-matched placebo to isolate semantic value; qualify four-state formal/physical mapping and finite completion. R0/R1/R2 controlled recovery comparison remains planned, not demonstrated. Ask class whether temporal completion or semantics-only ablation should take priority.
- **Fact IDs**: F01,F03,F05,F06,F07

## X. Speaker Notes Requirements
- Enabled: six matching English speech segments, grounded in final SVGs; embedded in PPTX.
- Content: explain mechanism, conclusions and limits; no source paths spoken. Chinese explanations and timing are separate rehearsal material, not part of timed speech.
- Target Duration: 5 minutes 30 seconds including handoffs; hard presentation limit 6 minutes.
- Notes Style: clear English conversational academic prose.
- Presentation Purpose: classroom midterm with Nov 9 P2 feedback.
