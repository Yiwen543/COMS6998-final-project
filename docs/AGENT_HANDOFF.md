# Working handoff — 2026-11-04, context checkpoint 25

Maintainer-only recovery index. Never include this file, skills, private controls
or calibration witnesses in experimental prompts. Never copy or print keys.

Latest active task COMPLETED: fresh WBXBAR B/C under frozen reference checker.
Live process47235 finishedexit0; no active process, stagedOpenAIkey deleted.
Current report docs/wbxbar_reference_bc_2026-11-04.md; root
results/wbxbar_reference_bc_20261104 (NB below). No further key/API call needed.

- Registration configs/wbxbar_reference_bc_v1.json SHA a5a59617cbdf5db6a64ce86c084b36fc6156d325cf096c77f2de6ef8132b6420.
- Freeze configs/wbxbar_reference_bc_freeze_v1.json SHA 094ff2a54540e73d73186c7cf0a6746089bac570637bbd5ecb2c420ed67f23ae.
- Same reviewed checker682fcf01eb44079cc9814aa66b551cfe40e45756f05fea8d82bbdc703c117a1d;
  no GPT checker edits. Same DUT/spec/driver/17target8groups/2845denominator and
  3x6x64+8seed, exactgpt-6.1-sol low,32000input/16384output,120stimeout,1retrycap.
- New separate scripts wbxbar_reference_experiment.py, prepare/run/audit/report_
  wbxbar_reference_bc.py are frozen with tests/test_wbxbar_reference_bc.py.
  Existing shared renderer/schema/driver/compiler/adapter reused unchanged.
  Eightoffline tests pass; mock/replay42batches each agree, seed/driver matchold.
- NB/live-v1 complete:36generation+36countrequests,0failed/retries,2compiles,
  42simulations/8400cycles;699656input+73798output=773454totalAPI tokens.
  Cached84240 and reasoning1824 are subsets, never added. All6sessionUUIDsfresh.
- All6 firsthit17/17 at round1,80physicalcycles/2executions. Final line82/86,
  branch79/88,expr282/321 alltie. B finaltoggle1952/1936/1952 (mean1946.67),
  C1952/1946/1928(mean1942). C intermediate meantoggleleads26.67 atR2 and12.67
  atR3, notpersistent; firstmeansboth1885.33. Do not claimCuniformlyworse.
- B firsttokens18981/18991/18936(mean18969.33);C27189/27195/27189(mean27191),
  C+43.341885%. TotalB371806/C401648 (+8.026229%). FinalmeanROI B.346960/C.321182.
  Targetwallmeans25.363/25.141s overlap; no clearlatencybenefit. Smalln,no placebo,
  no significance/no isolatedsemanticclaim. Cgroups8 firstcall then0 next5 eachrep.
- All36generatedbatches/final6UNRESOLVED,6seed scopedpass,0failures/assumptions.
  FinalunknownB15/11/8,C16/15/21,total86 (starvation49/postabort23/sameedge11/
  pending3). Allroundunknown343 repeatedrecords,notdistinctdefects. No newdefect
  adjudication. All8400rows processed,8197nonresetchecked,0resource/suspension.
  K5/C1-C4/F1-F8 exclusions remain; K13notactivatedC1/B3,unresolvedother4.
- NB/live-audit-v1.json passes36prompts/counters,42freshcheckerexecutions,
  58selftests; audit2.166074s no newmodel/sim. Supplemental postrun
  scripts/audit_wbxbar_reference_accounting.py verifies perrowcost/ROI, sourcehash
  789180af4ec55fbfc2c794b1c0f615c3bdc5eb9cfdb7243ff27cea21422ede19; NB/live-accounting-audit-v1.json passes.
  Two negativecontrols rejectfalseROI/unknown-as-pass in temporarycopies.
- Live wall819.620187s,compile15.457057s,simulation1.927009s(overlapping), reused
  egraphpreprocessing0new. Offline and audit costs separate. No API dollarprice
  inferred. report/rounds/endpoints/diagnostics/reference-result +PNG/PDFcurves inlive-v1;
  bothplotsvisuallychecked. NB/live-comparison-v1.json holds descriptivecalculations.
- Report/README/PROJECT_STATUS/status updated. Alloldfreezes stillverify. No
  commit/push requested. Nexttask requires userdirection/newprereg; do not rerun
  models or tweakbudget to seekCadvantage. Known-easy rawtarget stillnondiscriminating.

Previous completed phase (historical replay-only freeze is NOT live permission):

Latest recovery pointer: separately registered WBXBAR reference-checker replay
and independent measurement audit PASSED. No model process or new B/C run.
Current report: docs/wbxbar_reference_replay_2026-11-04.md.
Evidence root results/wbxbar_reference_replay_20261104 (RB below).

- Registration configs/wbxbar_reference_replay_v1.json SHA256
  35b7066816433d4784a2c331ed16d5026c84469bf6e3a1368e424ab0023e61aa.
- Freeze configs/wbxbar_reference_replay_freeze_v1.json SHA256
  8d3c0b11b8635f281db56d1d4880a30a473cfff876dab1ef884bf557573cb140.
- RB/frozen-checker is byte-for-byte Claude documentation-v1/candidate;
  checker SHA256 682fcf01eb44079cc9814aa66b551cfe40e45756f05fea8d82bbdc703c117a1d.
  Separate compatible authorship.json records provenance only; GPT changed no
  checker/contract/selftest/property behavior. Prior scoped gate remains valid.
- New scripts freeze_wbxbar_reference_replay.py and audit_wbxbar_reference_replay.py
  are BOUND by new freeze: do not silently edit. Reused replay_wbxbar_cancel.py.
  report_wbxbar_reference_replay.py generates metrics/final/property CSV + hashes.
- RB/replay-v1 and audit-v1 complete: all42 saved batches/8360 physical cycles,
  all2845 raw identities AND hit values, public pins and transport unchanged.
  Both original live and prior cancellation replay pins/counters match. All895
  preserved historical files still match. No new compile/API/stimulus/extra tail.
- Checker freshly reexecuted42 times in audit;58 selftests pass. Six scoped seed
  passes, all36 generated-round batches and all6 final sessions UNRESOLVED.
  All59 repeated old alarms (18final) uniquely map by cycle/slave to post-abort
  unknowns; no independent new DUT-defect adjudication. Never call them59 defects.
- Final unknown records104 (previous32): starvation65/post_abort26/same_edge9/
  pending2/unexplained_mapped_err2. New record granularity is not model efficacy.
  All8360 rows processed;8116 nonreset checked;0suspended/postdeath/exhaustions/
  inputboundaries/terminationboundaries/assumptionviolations. Scope exclusions
  K5/C1-C4/F1-F8 and accepted non-normative read-ACK assumption remain.
- Coverage unchanged: all6 hit17/17 targets round1 (8semanticgroups); final line82/86,
  branch79/88,expr282/321,toggle1952/2350 exceptrep3-B1940. Known-easy control;
  no new C benefit. Rep3-B384finalcycles,others392; cumulativecycles8360 unchanged.
- Extra costs:42simulations,0compiles,0API;simulation1.628692s included inreplay
  3.472051s, separate audit2.238581s. Do not replace original live metrics.
- Three integrity/correspondence tests pass; test tampered trace/counters and
  historical drift fail closed; attribution permits unmatched/ambiguous alarms.
- RB/report-v1 holds all42 metrics/final6/propertyscope CSVs and input hashes.
  One local pre-registration relative-path failure retained; no simulation retry.
- No new key needed. Prior retained key was removed after scoped validation.
  Next: consider a separately registered fresh B/C under new checker, original
  3x6x64+8seed/model budget and explicit unknown outcomes. Replay-only freeze
  blocks live trials. Do not treat retrospective labels as fresh B/C evidence.

The remainder retains development history; use the current pointer above rather
than treating earlier failed readiness statements as the latest status.

## Active conformance follow-up

User now asks to close cancellation timing, ownership ambiguity and unsupported
cross-slave forwarding order, then rerun B/C only after gates pass. New prereg
configs/wbxbar_conformance_gate_v1.json SHA256
`d957119caa1405b628caf50e7ffd90f81fb890484f04036da9ce5858f925f5f6`; original DUT,
driver, target/denominator and3×6×64+8seed budget retained. Current report:
docs/wbxbar_conformance_gate_2026-11-04.md. Evidence root
results/wbxbar_conformance_gate_20261104 (BASE for this paragraph).

Offline proof-only characterization ran in boundary-v1: previous sampled edge
allmasterCYC=0 => current slaveCYC/STB=0, unbounded base+induction PASS, no input
assumptions. Stronger instantaneous negative FAIL atstep4 as expected, 2 covers
PASS. This is NOT cancellation completion, buffer-empty or stale-restart proof.
No functional checker written by GPT; no DUT/coverage edits. Old freezes verified.
Tools SBYv0.70-9-g79fc9ed,Yosys0.70+309 bd3168b1a,Z3 4.15.5. BASE/validation.json.

Seven new synthetic scenarios196rows expose v4: cross-slave early forwarding with
ordered retirement rejected; wrong retirement/data rejected; five ambiguous cases
unresolved, including later data corruption and unaccepted address. Results in
baseline-v4. All inputs structurally legal, no old checker assumption violations;
control interpretations still need Claude independent review.

The first read-only Claude design call COMPLETED (not active87447). Exact
claude-opus-5-5, low, tool-free, $0.623196/92456tokens/114.44s; 4uncachedinput+
81724cachecreation+10728output, thinking3455 is output subset. Key deleted.
BASE/claude-design-v1 preserves response/metadata/design/wrapper-original.py.
Original wrapper exited1 because readiness was explanatory string, not boolean;
prompt did not explicitly type it. API succeeded; no paid format retry or bool
coercion. Updated wrapper preserves readiness text but never grants permission.

Design proposes hypothesis histories, local checking and ghost formal identities.
Integration issues D1-D7: unknown alternatives/pass semantics, unsound candidate
symmetry without FIFO order, component dependency beyond identity, ghost mapping
quantification, restart-safe cancellation vs quiet bounds/epoch alias, ERR unknowns
and finite-counter scope, forward-order control classification. Three prose read
constants differ from fixture (actual9876fedc/88887777/88887776). Do not edit raw
model result or assume all questions are proved bugs; independent review required.

Fresh review packet BASE/design-review-packet-v1 is139048bytes, hashed, contains
public spec/design/7complete synthetic scenarios plus old live-aborted identity
control/D1-D7; excludes DUT, actual trajectories, B/C outcomes, proof results.
7 offline tests pass in tests/test_wbxbar_conformance.py (no API/simulator calls).
Fresh independent design review COMPLETED, session16619 exit0. Result explicitly
ready_for_implementation:false; no model/schema failure. claude-opus-5-5,
89882tokens/$0.511626/46.81s, key deleted. Review found5blocking architecture
issues plusERR/cancel/orphan/order issues. R8 uncertainty itself misreads live
identity: m0cycle7,m1cycle12,slavecycle14 alladdr6,SEL5,data23456781,mask00450081.
Review is not infallible; R6 ERR implication needsguards, R5 quantifiers stillneed
precise semantics. No checker implementation or livefreeze justified yet.

Added prepare_wbxbar_design_revision.py: five more hand synthetic scenarios
A-B-A positions/order, overlap ambiguity and changeddata, repeatedaborts.
Oldv4 run revision-new-controls-v1 has no assumptionviolations; outputs notnew
approvedlabels. New design-revision-packet-v1 contains fullpublicspec, rawdesign,
rawreview, all69old+7new+5new=81controls/2227rows, losslessvectorencoding, exact
identityfacts. Byte120482. No DUT, actualoutcomes or proofresult. Ten offline
transport/integrity tests pass (no API/simulation). No GPT golden/checker edits.

Revision pair COMPLETED, session20158 exit0. Author105635tokens/$1.129866/
367.37s, reviewer74010tokens/$0.488801/84.87s. First4calls total361983tokens/
$2.753489. Keysdeleted. Design drops symmetry/partition, uses exact global histories,
arbitraryprecisionepochs and explicitlimitunresolved; all81caseassessments exist.
Review ready_for_implementation:false: heldunacceptedERR starvationunknown;
env>violation mayhideearlierfault; K13inferred/prohibitedlatencyguess; SEL/read
payloadidentity scope; usefulnonvacuouscontrols; suspendedscope metric; K5exclusions.
Review F6 offbyone is FALSE: raw and losslessdecode accept6/10/14, forward16,
slaveACK17, masterACK18 (not17). No data altered. R6/F3 K6 cannotautomaticallyjudge
inactiveCYCrawACK either; needsauthorclauses. No functionalchecker implemented.

New generic exactdesignpatch script scripts/patch_wbxbar_conformance_design.py.
Seven newsyntheticcases: stalledunacceptedERR/ACK, wrongdata thenlaterinvalidinput
andcleanprefixbaseline, stallreadirrelevantdata/write disabledenabledlanes.
Packet BASE/design-patch-packet-v1: all88cases lossless,129560bytes, previousfull
design/review+publicspec+mechanicalpreedgeeventledgers+reviewfactualcorrections.
No actualDUTtraces, RTL, targets/proofresult. ExactJSONpath/before/afterpatches
only, append7assessments, rejectoldcaseloss ornonmatchingpatch. Thirteen offline
transporttests pass. Previous18test validationlog was10current+8old; now13current.
No claims that thiscertifiesa checker. Existingfreezehashesunchanged.

Design exactpatch pair COMPLETED, session60415 exit0. 14ClaudeexactJSONpatches+
7assessments applied, no GPT semantic edits. Author80180tokens/$0.522021/75.84s;
review75692tokens/$0.431991/39.10s. Latestreview design-patch-v1/review.json still
ready_for_implementation:false. Sixphasecalls total517855tokens/$3.707501;
BASE/claude-costs.json andstatus.json nowrecordall6. No activecall. Keydeleted.

Latestreview accepts prefix-invalidtimeboundary, payloadmask, no-prune/resource
reporting, K5exclusions and inferredK13. RemainingR1: olderliveentry plusheld
unacceptedrequest ERR cannotforceoldestretirement; mustretainpossible_no_retire
starvationbranch or genuineoldretirebranch. R2: finalacceptanceedge andwithdrawal
edge ERR requireexplicitqualification (mayalreadyoverlapK13). Publicsource gives
no phase/timing so doNOTinventgraceperiod. ThisreviewcorrectlyreadledgerACK18.
Allformaltargets stillunimplemented; public-pinobserveronlyproof notfullIPproof.

Prepared three new syntheticERRboundaries via savedprovenance builder
BASE/prepare-patch-v2.py, output BASE/design-patch-packet-v2. All88oldrows preserved,
now91cases,136936bytes. Old-live+held: acceptedread6/fwd8/slaveACK12/masterACK13,
secondrequestheld9..14stall1, ERR10. Acceptanceedge:held6/7,accept+ERR8.
Withdrawal:held6..8 thenCYC0 andERR9. No expectedlabels imposed. Packet asks
Claude tocheckactualenvvalidity, avoidredundantK13fix, ensure newlynamedunknown
starvationtagspropagate instead ofaccidentalpass. Fullspec/previousdesign+review,
all91losslesscontrols andpreedgeledgers; NOactualDUT/pilot/target/proofresult.
Genericexisting patch_wbxbar_conformance_design.py run canusev2packetunchanged;
verify packet andexactbefore patches; preserveall88oldassessments,append3.

14offlineconformance tests pass; 8oldcancellation tests passedearlier unchanged.
The v2 attempt COMPLETED FAILED authentication: session61813 exit1, provider
HTTP401 InvalidAPIkey, no model design, no independentreview. CLI terminalresult
reports0tokens/$0 (modelUsageempty); original wrappermetadata lacksusage because
it exits onprocessfailure beforeparsing. Preserved originalstream/metadata and
saved author/recovered-error-result.json, design-patch-v2/failure-accounting.json.
Keydeleted. Costsrecord6completedmodelresponses plus1failedattempt; total7process
attempts, unchanged517855tokens/$3.707501. No inference/newchecker/B/C occurred.

The firstretry alsoFAILED, session32077 exit1, DIFFERENTreason: localCLI invalid
X-Api-Key header nonASCII, noHTTPstatus/modelresponse, terminal0usage/$0.
Preserved design-patch-v2-retry1/author/recovered-error-result.json and
failure-accounting.json. Noindependentreview. Keydeleted. Accounting now6completed
responses+2failedprocessattempts, same517855tokens/$3.707501 beforecurrentrun.

Fixed scripts/stage_anthropic_crosscheck_key.py torejectnonASCII/badexpected
sk-ant-alnumunderscorehyphen inputbeforefilewrite. Noecho, 0600/0700 unchanged,
nooverwrite. Successsayslocalformatonly, notproviderAuth. Newtests
 tests/test_anthropic_key_staging.py:3tests pass, 14conformancetestsfreshpass.
Initialtestfalsepositiveforpublicsk-ant-prefixfixed (notsecretleak). Helpernotbound
byexperimental freezes; originalfrozenhashesstillpass. Noactualcheckeredit.

Retry2 author SUCCEEDED: session29549 exited1 onlybecause strictpatchguard.
BASE/design-patch-v2-retry2/author metadata complete, exactclaude-opus-5-5,
80763tokens/$0.482771/53.34s. Threepatches/threeassessments. Patches0/1exactmatch;
patch2 named arrayindex8 butbeforetext exactly/uniquelymatchesindex9 in SAMEarray.
Originalindex8 is Per-slave response count <= forwards. Strictfailure preserved.
Keycleaned; no reviewerthen. Noauthorretry. Derived patches-location-corrected.json
onlychangespathindex8->9, ALLbefore/aftertext andaddedassessmentsunchanged.
design-location-corrected.json has91cases andretainsper-slaveindex8; audit in
location-correction-audit.json. This is explicittransportcorrectionforreviewONLY,
notGPTgoldensemantics. 15conformance tests pass includingrawfailure+uniquematch+
exactreconstruction. No functionalchecker changed.

CandidateHR branches oldliveERRretirement vsnonretiringunknownstarvation evenwhen
oldliveexists; acceptanceedgeB1keepsnewentry/B2cancelsit; withdrawalusesexistingK13.
Genericunknownclasspropagationupdated. Stillneedsfreshreview. Costledgernow7model
responses+2credentialfailedattempts (9processattempts),598618tokens/$4.190272;
transportrejectionseparate, don'tdoublecountmodelcost.

Fresh ERR-boundary review COMPLETED, session11479 exit0. Exactclaude-opus-5-5,
79271tokens/$0.445611/33.72s. Review ready_for_implementation:true, verified
HR/acceptance/withdrawal, oldlive+heldbranch, prefixvalidity and locationcorrection.
RC1nonblocking: repeatedHR ERRs withinoneheldrequestare NEVERjudged, allunknown;
reportexplicitly. Keydeleted. This is designreadiness only, NOT checkerproof or
liveB/C permission. Formalobligations remainunimplemented. Conformancephase now
8completedresponses+2credentialfailures=10processattempts; 677889tokens/$4.635883.
One stricttransportrejectionalreadycountedinmodelusage. BASE/status.json and
claude-costs.json updated; no duplicatecost. All91controlsavailable.

NEXT ACTIVE PHASE: results/wbxbar_reference_checker_20261104 (REFBASE).
New scripts/prepare_wbxbar_reference_checker.py preparesverifiedpublicspec+reviewed
clauses+priorv4files, WITHHOLDS fullcontroltraces/control_assessments andB/Coutcomes.
REFBASE/spec-packet-v1 bytes83498, hashesbindscope/design/review/oldchecker/helper.
Existing run_spi_checker_author.invoke reused, oneClaudeauthorsonly$4/600s,
check_rows(rows,limits=None), limitsdevselftests onlydefaults4096/64/256; original
livecalleronlyrows. Output4standardfiles/pureimports/selftest.run. NoGPTrulecode.
New tests/test_wbxbar_reference_commission.py 3tests pass. Conformance15tests and
credentialstaging3tests pass. Newmanifestkeepsoriginal3x6x64+8seed andgpt-6.1-sol.

Userreplied “WBXBAR checker 实现密钥已就绪”; authorized ONEcandidate call,$4CLI.
Author COMPLETED session63186 exit0; no active process. REFBASE/claude-author-v1
contains artifacts DIRECTLY (not candidate/subfolder). Exactclaude-opus-5-5 low,
544.524s,$1.498306,100600tokens=4uncached+34242cachecreation+66354output;
41968thinkingalreadyoutputsubset. Keydeleted. Never duplicate generation.
checkerSHA aabd8f399a5fcc7ff53c42cfc381d4d4fd8e260ff73235c72aa7df1d366637f2.
NoGPTedits to any fourgenerated artifacts. Separate REFBASE/claude-costs.json;
preceding design phase accounting unchanged at677889tokens/$4.635883.

New scripts/wbxbar_reference_controls.py built controls-v1:91reviewedsynthetic+
36heldbackmetamorphic=127normal and6limitcontrols. Portswap andprepend3resetrows
on18cases preservefunctionalinterfaces; labelsfromrevieweddesign. Fullprivate
traces withheld fromauthor. NoDUTtrajectory/goldenanswer/modelstimulus.

scripts/evaluate_wbxbar_reference_checker.py evaluation-v1 COMPLETED exit0:
39/39authorselftests,127/127normal,6/6limitagreements. Actualnormalclassifications
46scopedpass,46syntheticviolation,33unresolved,2invalidinput. These arenotactual
DUTfindings. CPU30s/parent60s isolatedworkers, no credential env. Limitsdefault
4096/64/256 unchanged; optionaldevlimits exerciseexhaustion,pinchecksafterlimit,
resetresumption without erasingunknown. No new simulation/GPTcall/replay.
Full cases.json/limits.json/summary.json preserved; agreementNOTcertification.

New scripts/prepare_wbxbar_reference_review.py prepares code-review-packet-v1:
fullpublicspec,reviewedcontract,4artifacts,ALL133fulltraces+ALL133rawresults using
vector/dictionarydelta compression. Roundtrips pass. Firstlocal150kcap rejected
269636bytes BEFORE API; this fullcodeaudit expressly raises LOCALpacketcapto300k
(unchanged B/C token/$4reviewbudget), keepingall evidence. Authorresponse reports
1Mtokencontextwindow; reviewer requestnotyettested. No data truncated.
Nine tests/test_wbxbar_reference*.py tests pass:authorshipisolation/provenance,
controltransforms,allpacketroundtrips,tamperreject,onecall+cleanup. validation.json
bindsevidence. README/PROJECT_STATUS/currentconformancereport updated.

Fresh readonly code review COMPLETED session64249 exit0; exactclaude-opus-5-5,
47.357s/$0.724751/131997tokens=4uncached+127675cachecreation+4318output,
2657thinkingalreadyoutputsubset. REFBASE/code-review-v1/review.json explicitly
ready_for_replay_registration:false. Revieweronlystatic+spotchecks, nofulltrace
execution. Keydeleted; no activeprocess. Implementationphasecostsnow2calls,
232597tokens/$2.223057; prior designphase677889/$4.635883 separate unchanged.

ReviewF1 tagslostatexhaustion andepochrecordmissingatdeath;F2no perclauseactivation
count/not_activated;F3history16/witness8 truncationundisclosed;F4sameedgecount
semanticsneeddecision;F5self-declaredcontractblockers B2alreadyforwarded, undefined
read/control scopeetc needresolution. No reviewerpermission tofreeze/replay/B/C.

Added scripts/probe_wbxbar_reference_review.py,9syntheticfocusedprobes. review-repro-v1
retainedoriginalbuilder-source.py. LastHRsameedgefixtureincorrectSEL15vsaccepted5
causedK4mismatch; fixedONLYforwardidentity inreview-repro-v2, allother8casesunchanged.
Bothversionrawinput/output retained. V2all9 noinfraerrors; onlyintentionalenvcase
hasassumptionviolation. NoDUT/APIcall forprobes. Confirmedpossible_starvation_err@8
survivescleanworkbutlostatexhaust@15/death@19; epochsabsent. Idleconditionalclauses
allchecked_not_refuted.90historiesdisplay16. CorrectedHR8accept+forwardERRthenACK
isunknown/nofailure. F4reviewfactualcaution:K6naccusesx<c (priorrows),K4includes
currentaccept; donotparrotreviewerclaimbothusecurrent. DuplicateACKpairedinvalid
othermastercaseatrow13 demonstratesmixed_same_edge; noGPTgoldenlabelimposed.

New scripts/repair_wbxbar_reference_checker.py prepares repair-packet-v1,134350bytes:
publicspec,revieweddesign,current4Claudefiles,rawreview+all9focusedcontrols/results.
Full133heldbackcontrolset/actualDUT/B-Cresults withheldfromauthor. Promptasks
explicitcontractdecisions includingretaining historical/refutedvsfeasible tags,
perclauseactivation/scope, truncationcounts, eachF4F5policy. Exact{file,before,after}
patchesonly, pure-sourcevalidation, noGPTsemanticediting, noautolive. Onecall$4/600s,
oldcandidateuntouched. This authorized call now COMPLETED session76824 exit0.
Exactclaude-opus-5-5,$0.513766,101.270s,68587tokens=4uncached+57194cachecreation+
11389output;5895thinkingalreadyoutputsubset. Keydeleted.23exactClaudepatches applied
withoutGPTsourcecorrections. Candidate repair-v1/candidate checkerSHA
66759fe3a5c6d8544c2e2d199d7a95f5d851a785057e45dfbb42ad08f1c438c3.
properties.json unchanged. No activeprocess. Implementationphase3calls now
301184tokens/$2.736823 (prior designphase separate677889/$4.635883).

Completed evaluation-original via evaluate_wbxbar_reference_checker.py:
127/127normal+6/6limitexpectedclassifications agree; AUTHOR SELFTEST45/46ONLY.
Failed mixed_same_edge_explicit oldexpectation input_or_scope_invalid versusnewP4
K6 count dut_violation +mixed_same_edge. all_control_agreements:false; workerexit0
is NOT gatepass. Alloldlabels/selftests retained, no GPT edits.
Completed evaluation-focused9controls via isolated limit-worker;noinfraerrors.
UnknownHR@8 nowretainedatexhaust@15; deadhistory@19getsdiscarded_epoch_evidence,
explicit suspended/dead epochrecords. Idleclausesnot_activated.90historiesreported
16shown/74omitted; witnessesexplicittruncatedcounts. Rawclause_activationsadded
butperclausechecked/unknown/suspendedCOUNTSSTILLMISSING; activationsincrementwhile
associationchecker suspended, notactualchecks. P1-P5 proposedonly,needfreshreview.

repair-v1/diagnose-selftest.py isolated diagnostic preservesauthor_mixedfulltrace
andold/newoutputs inselftest-diagnostic.json. Adds tag_then_mixed_same_edge:
unknownERR@8, wrongdata +othermasterinvalidheldaddr@19. Globalinputinvalid+
mixed_same_edge, butnewdiscarded_epoch_evidence calls oldhistoriesconcretelyrefuted,
unknown@8absentfromopenunknowns. Exposecontradiction to independentreview; don't
assertnewnormativepolicyasGPT. Bothdiagnosticsnondut,nogoldenlabels,noreplay.

New scripts/review_wbxbar_reference_repair.py preparedrepair-review-packet-v1
367250bytes,localcap500000(fullcurrentcode/reporting growth; B/Ctokenbudgetand
$4reviewbudgetUNCHANGED). Complete144traces/results=127+6+9+2; failedselftest,
rawreview,P1-P5,publicspec/approveddesign,current4files,diagnosticprioroutputs.
Roundtrips pass. No calibration/B-Cdata. New tests/test_wbxbar_reference_repair_review.py
3tests; total16test_wbxbar_reference*.py pass (transport/provenance only, AUTHORtest
stillfails). Positive mockreview cannotoverridefalseofflinegate. Currentpacket
verified, originalscope/DUT/checkerdriverhashes intact. offline-audit.json saved.
README/PROJECT_STATUS/conformancereport/costs/status updated. No commit/push.

Fresh repair review COMPLETED session75935 exit0. repair-review-v1/review.json
ready_for_replay_registration:false. Exactclaude-opus-5-5,34.050s,$0.910961,
173598tokens=4uncached+170729cachecreation+2865output; thinking0reported. Keydeleted.
Implementationphase4calls474782tokens/$3.647784; designphase unchanged separate.
No activeprocess,no checkeredits; authorfunctionalselftest still45/46.

ReviewR2/P4acceptsACK-specificK6pin-only andsaysoldACKselfteststale. ERR-drivenK6
countdependscurrentHR andmustremainmixedatinvalidboundary (conservativepolicy).
R3requireopenvalid-prefixtagswhendeath@invalidboundaryreclassifiedmixed; cannot
claimrefuted. R4discloseactualvsprojectedhistories,pre/post-expansionsnapshot,
dying-row omissionsperevent. R5needsperclause/subobligationactivations,actually
checked,suspended,postdeath,unknowncount; separateassociation-freecounts. R6P3
accepted. R7acceptsB2-forwarded,undefinedDUTcontrol,firstrowK13scopeddecisions;
undefinedslavereaddatagapremains. CAUTIONreviewR7callsproposalassociation-free
butstillusesanyhistory, soflagfactualdependence,doNOTblindlyadopt. R8syncdocs.
Reviewstatic/spotchecked; notall144decoded, noformalcertificate/replaypermission.

Added2syntheticERRcompanions inrepair-followup-controls-v1: author_mixedACK->ERR
at3; cleanbaselinerestoresothermasterheldidentity. Currentbothdut_violation, invalid
onealsoenv+mixed; reviewerrequiresinvalidERRbeinputinvalid+mixed whilevalidbaseline
remainsdutviolation. Inputs/outputs/command/hashesretained; zeroDUT/APIcalls.

New scripts/followup_wbxbar_reference_checker.py builds followup-packet-v1,
161938bytes,13fullfocused+diagnostic+ERRtraces/results (9+2+2). Exactpublicspec,
approveddesign,currentcandidate,rawfreshreview,failedselftestincluded. Full133
independentcontrolsandactualB/Cdatawithheld. NoGPTfunctionalrules. Supportsmanifest
parentcandidate andexactClaude{file,before,after} patches viaexistingapply_exact;
boundedonecall$4/600s,pure-sourcevalidation,keycleanup,nolivepermission.
New tests/test_wbxbar_reference_followup.py3tests, total19reference testsPASS:
all13roundtrips,deterministicERRrebuild,tamperreject,exactparentmockpatchnooverwrite,
cleanupandnolive. README/report/status/costs/handoffupdated; oldhashesverified.

Checkpoint18: followup author COMPLETED, session63631 exit0. One exact
claude-opus-5-5 low/toolsdisabled call, 202.954s/$0.840561/94109tokens =
4uncachedinput+69437cachecreation+24668output; 14453thinking is output subset.
Keydeleted. 35exactClaude patches, no transport correction or GPT functional edits.
REFBASE/followup-v1/candidate checker SHA
99d12449ef9c3ff11757ca6651b5d953ddc9e37c2920f469879a0ba68a6b6776.
Implementation phase now5calls568891tokens/$4.488345; prior design phase separate.

evaluation-original:127/127normal+6/6limit classifications agree, workererrors[].
Author selftests53/54; mixed_death_keeps_prefix_tag_open FAIL. Do not treat
evaluator process exit0 as gatepass. All13focused cases run with explicit limits
in focused-inputs.json (MAX_HYP1 only taggedexhaustion), outputs in
evaluation-focused. ACK/ERR companions now follow reviewer scope. New actual
subobligation accounting exists, but K11_env omitted: raw33/measured0 on exhaustion.
Old P1/P4 proposals/status list in contract still conflict with executable rules.

Real remaining prefix bug: author-test-diagnostic.json has4diagnostics. _tag_mixed
rows0..7 retain possible_starvation_err@3. Addinginvalidrow8 causes inputinvalid,
prefix_unresolved, unresolved[]; histories are active, no membershipdeath.
boundary onlyflushes row-start tags when deathreclassifiedmixed. Genericinvalid
boundary still loses valid-prefix uncertainty. Preserve failing fixture/expectation;
do not moveinvalidedge to manufacture pass. diagnose-author-test.py reproduces in
isolated CPU30s worker. Earlier3diagnostic output preserved as
author-test-diagnostic-initial.json. PublicFIFOundefinedread live/orphan controls
pass but new normative rule needs freshreview. offline-audit.json records all.

New scripts/prepare_wbxbar_boundary_completion.py creates completion-packet-v1:
212753bytes,17complete traces/results+limits (13focused+4diagnostics), fullcurrent
candidate/spec/approveddesign/latestreview. Full133independentinputs andactualB-C
withheld. Exactparent followup-v1/candidate, onecall$4CLI600s, nofreeze/replay/live.
PacketSHA321294c9eba19c12ae8d3e7b973e31193744bf941e3e31b0b41dcbbfd732cc09;
promptSHAd8c701a044be843591c2048830b9fdfb1d37f4c23659349255e987881ef98db6.
tests/test_wbxbar_reference_completion.py adds2checks:17losslessroundtrips/limits
and exact35patchreconstruction+failedtestpreservation.21reference testsPASS,
validation-tests-followup.log. verify(completionpacket) andoriginalscopehashesPASS.

Checkpoint19: completion author COMPLETED, session70941 exit0. Onecall exact
claude-opus-5-5,low,notools,noretry;34.111s/$0.528926/94539tokens =
4uncached+90786cachecreation+3749output;1522thinkingalreadyoutputsubset. Keydeleted.
10exactClaude patches, noGPTfunctional changes. checkerSHA
093baceb5d79d1bc87dd805c43584fef06428396c0f6b5e4be97a1d37891bdf3.
Selftest file byte-identical to followup-v1 parent; now54/54PASS. Original127normal
and6limit classifications agree. Full evaluation-original preserved. Implementation
phase6calls663430tokens/$5.017271; designphase unchanged separate.

17focused cases rerun with same limits; originalinvalidboundary nowretainsERR@3.
5additional postgeneration boundary probes prepared withoutchangingchecker:
missinginput/missingpost/noncontiguous/undefinedinput preserveERR@3; undefinedDUT
o_mstall=None at8 yieldsdut_violation+unjudgeable_row butLOSESpriorERR@3. Fixed
integer drivercannotemitNone; doesNOTautomaticallywaivereportinggap. Independent
reviewmustadjudicate repairversusscope; donotsuppressgenuineundefinedoutputfailure.
K11exhaustion raw=eligible=checked33;schema/reset3.20explicitlyunmeasured. All155
results pass arithmeticactivationpartitionchecks, notproofcorrectinstrumentation.
candidatecontractsupersedesoldP1/P4,not_activatedlisted; publicFIFOundefinedread
assumption stillneedsreview. offline-audit.json hasoriginal_control_gate true,
overallreadiness false. OriginalDUT/driver/targets2845denominator/budgetunchanged.

New scripts/prepare_wbxbar_completion_review.py prepares completion-review-packet-v1
withall155fulltraces/results/limits andcurrentcode/spec/priorreview/authorrationale;
noactualDUT/pilotresults. 150ordinarytracesuseoldlosslessencoding,5malformedboundary
tracesrawpreservemissingfields/noncontiguouscycles. Genericdictionaryresultpaths
internedlosslessly via pack_review_results/unpack_review_results (localnewbuilder,
noedits tofrozenpackinghelpers). Prompt409079bytes<500000cap; onefreshreview$4/600s.
FirstpackattemptKeyError andsecond524664size rejection retainedincompletion-v1;
zeroAPIcalls. Interimtestsfailed2formissingunbuiltpacket; final24PASS in
validation-tests-completion.log. Newtestfile test_wbxbar_reference_completion_review.py
checks155roundtrips/limits, exact10patchrebuild+unchangedselftest, tamperrejection.
verify(newreviewpacket),candidatehashes,originalscopePASS; keyabsent.

Checkpoint20: fresh completion review COMPLETED, session99955 exit0, schema valid,
readinessFALSE. Oneexactclaude-opus-5-5 low/notools/noretrycall,23.715s/$1.027671/
200342tokens=4uncached+198607cachecreation+1731output;0thinking. Keydeleted.
Implementation totals7calls863772tokens/$6.044942; designphase separate unchanged.
All4candidatehashesunchanged;54selftests+133originalclassification resultsretained.

completion-review-v1/review.json N1/N2 reject undefinedDUT termination reporting:
possible_starvation_err@3 lost,K6checked_not_refuted;pending2perhistory absent,
prefixnull,K12notactivated. Independentlychecked against identical0..7prefix and
row8pd-only result. KeepgenuineK10DUTviolation. Onepath/tworelatedreportingfindings,
notconfirmednewDUTdefects. N3acceptsenv/schema/mixedflush,N4acceptsdelimitedK11,
N5acceptspinFIFOreadassumptiononlyscoped/nonnormative,ACK-onlyP4accepted.
Reviewerexplicitlyselectivelydecodedboundary/focused/limitcases, NOTall155;
staticreviewnotproof. integration-audit.jsonrecordslimitandconfirmedfacts.

New scripts/prepare_wbxbar_termination_repair.py creates3supplementarycontrols via
extra_controls(): appendpdterminationafterresourceexhaustion(MAX_HYP1) orvalid
membershipfailure, appendignoredresetsuffixafterpd-onlyrow8. Evaluatedunchanged
candidateinCPUboundedworker; originaltagalreadyflushedat8retainedafterexhaust,
oldmembershipfailure19retained, suffixunprocessed. NoAPI/simulatorcalls.
termination-controls-v1/{inputs,outputs,command}.json andworker.log preserveevidence.

termination-packet-v1 ready205642bytes,9rawcases+losslessresults,fullcurrentcode/
publicspec/approvedcontract/freshreview. Full133independentcontrols,DUT,actualB/C
withheld. RequestsClaudeonlytargetedpd-pathreportrepair+meaningfulselftests; mustnot
mislabelDUTterminationasenv/reset/batchend, doublecountpreviouslyflushedtags orerase
priorfaults. All155old+3new mustrerunandfreshreviewbeforefreeze. NoGPTfunctionalcode.
PacketSHAfda33983268b68496562490f447bd500d229ddbccfdde0e30c57d16cf1a7e550;
promptSHAaacc84805eb9625fd848e7c78c04eba95f2fd6d473dbd7985e018dd47eb22d06.
tests/test_wbxbar_reference_termination.py adds2evidencechecks; total26reference
testsPASSinvalidation-tests-termination.log. Candidateandoriginalscopehashesverified.

Checkpoint21: termination author COMPLETED, session9955 exit0.12exactClaudepatches,
noGPTfunctional edits. Exactclaude-opus-5-5low/notools/noretry;51.791s/$0.628751/
108684tokens=4uncached+102991cachecreation+5689output;2187thinkingoutputsubset.
Keydeleted. Phase8calls972456tokens/$6.673693; earlierdesigncostseparateunchanged.
NewcheckerSHA682fcf01eb44079cc9814aa66b551cfe40e45756f05fea8d82bbdc703c117a1d.
58/58selftests,prior54ASTtestexpressionsidentical,4newtests.127normal+6limitagree,
25focused/supplementaryrerunpreservinglimits,0infraerrors. All158newresultsretained.

N1/N2observationsnowpass: ERR@3retainedonce,pending2perhistoryatstartrow8disclosed,
K6/K12unresolved,prefix_unresolved,K10failure+unjudgeable_rowstillpresent.
termination_boundary8/reason distinctfrominput_validity_boundarynull;closure
terminated_unjudgeable_dut_outputnotreset/batchend. Suspendtagnotduplicated,
validfault19retained,reset suffixunprocessed.154nonterminationJSONresultsidentical
afterremovingonly2newnullterminationfields;4terminationresultschanged.158scope
partitionsarithmeticallyconsistent. offline-audit.jsondoesNOTcertifychecker.
Remainingreviewquestion: K12pendingatterminationunresolvedbutnotbatchendactivation;
unknown_tag_records countsTAG_CLAUSEhistorytags,notallunresolveddiagnostics.
Freshreviewmustassessmetricdocumentation/scope,noGPTgoldenrulefix.

Versioned REFBASE/termination-v1/prepare-review.py (notnewlibrary) reusesoldpacking
andgenericread-onlyrunner. termination-review-packet-v1 ready418586bytes<500000,
all158completeNEWresults/traces+limits,fullcurrentcode/spec/priorreview/decisions,
actualDUT/B-Cwithheld. PacketSHA1bbe7d1649ff18219aa1a13b07596925b68d62c152dc3fabe7384a3859c09d98;
promptSHAc98d7e9037b1222aee04d1a3a6b6e3649e4c6664cdadd39333c296868c0d3e05.
tests/test_wbxbar_reference_termination_review.py adds2tests(all158roundtrip,
exactpatches+54oldASTtests),total28PASSvalidation-tests-termination-review.log.

Checkpoint22: user explicitly authorized retaining staged key until checker is
reviewed/validated, with necessary continued use. Do not applyoldper-calldeletion
whilethatcycleactive. New scripts/review_wbxbar_retained_key.py reuseverifiedpacket/
existingboundedcall butretainskey; nofrozenwrapperedits. test_wbxbar_retained_key.py
verifiesretentiononsuccess/failureandnopermissionfrommodelopinion.

Terminationreview COMPLETED,session17113exit0: ready_for_replay_registrationTRUE.
Exactclaude-opus-5-5low/notools/noretry;36.317s/$1.082866/206641tokens=
4uncached+203326cachecreation+3311output;984thinkingoutputsubset. T1/N1/N2accepted,
T3suspend/dead/suffixaccepted,T6precedenceaccepted. T2/T4/T5nonblockingdocsneeded:
closed_atlastprocessedvsboundaryunjudged;rows_beyond_input_boundaryunprocessed;
unknown_tag_recordstagclassesnotallunknowns. Reviewselectivelydecodedcases,notproof.

User's same retainedkey used for documentationonlyClaudeauthor+freshdocsreview
via scripts/clarify_wbxbar_contract.py. This permitsONLYcontract.md exactpatch,
rejectscode/test/propertieschanges beforesecondcall. Offline mock initiallyfound
missingcontract_decisions schemafield; correctedBEFOREpaidcalls. Twoformaltests
test_wbxbar_contract_documentation.pyPASS; originalmockfailurewaslocal/noAPI.
Livepair COMPLETED,session96557exit0. Author18.740s/$0.155661/25982tokens;
review22.520s/$0.193146/32117tokens. Sameexactmodel,budgets$4/600each,noretries.
documentation-v1/review.json ready_for_contract_addendumTRUE.1exactClaudecontract
patch,all3functionalartifactshashidentical. FinalcontractSHA
5de9e47953e147600381c1028b21ebeea8427f7c24471302e8d350c39f351868;
checker remains682fcf01eb44079cc9814aa66b551cfe40e45756f05fea8d82bbdc703c117a1d.

Docsreview2nonblockingnotes retained explicitly inreport/scoped-validation:
D3invalid_limits canmakeallrowsunprocessedwithoutbothboundaryfields;
D4same_edge_response_after_abort isdirectK13emission,notflush,butfiltercountsit.
Noendlessrepairneeded; governingformulas/filterarecorrect,reviewaccepted.
Currentturn3calls264740tokens/$1.431673;implementationphase11calls1237196tokens/
$8.105366,earlierdesignseparate. No functional edits ornewDUTsim/GPTstimuli.

Finalscoped-validation.json binds4finalhashes,bothreviews,patch,evaluationaudit.
58selftests/133originalclassifications/158cases applicable becauseexecutablefiles
unchanged; documentationversionNOTpresentedasnewsimulation. Fresh31testsPASS
validation-tests-scoped-gate.log (28reference+1retention+2documentation). Original
scopehashesverified. Onlyafteracceptedreviewsand31checks,keyunlinked; cleanup in
credential-cleanup-after-validation.json. Keyabsentverified. No pendingkeyrequest.
Scopegatepassed/readyforreplayregistration,formal_certificatefalse; nofreeze/replay/
liveB-Cyet. C1-C4/F1-F8 andK5exclusions plusalldeclaredlimitsmuststayvisible.

NEXT: separately register/freeze replay ofSAVEDB-Cactions with finalcandidate and
scoped-validationhashes; preservestimuli/driver/DUT/2845counters/17targets/budgets/
oldresults. Reattribute beforeconsideringnewB-C. Do notclaimformalconformance or
efficacygain. NoAPIneededforthisreplaysetup. No commit/push performed.

## Completed follow-up: cancellation contract revision

The user-authorized Claude revision, new freeze and exact saved-action replay are
COMPLETE. No active exec/model call; no pending credential request. User staged
Anthropic once for this pair; both calls succeeded and the key was deleted. No
OpenAI key or stimulus-generation call. Do not rerun models or original pilot.

Current report: `docs/wbxbar_cancel_contract_2026-11-04.md`.
Evidence: `results/wbxbar_abort_contract_20261104/` (abbreviated BASE below).
Registration `configs/wbxbar_cancel_contract_v1.json` SHA256
`ed3e6213e2f4c4155895f780b7f926cd7adc85ac1f92d1c3d78f38546083b5f8` binds258 old
files; original experiment, checker, stimuli, prompts, coverage and costs preserved.

Claude v4 exact patches changed only checker.py, selftest.py, properties.json,
contract.md under BASE/claude-v4/candidate. GPT never edited checker. Author packet
128745bytes: full relevant pinned B4 pages, public summaries, old Claude code and
six synthetic examples. No DUT executable/actual traces/live outcomes/targets.
Fresh read-only review packet147770bytes includes all69 lossless control traces,
source, contract and evaluations. No actual pilot traces or rankings. Both actual
models claude-opus-5-5. Author84859tokens/$0.520906/63.77s; review71958tokens/
$0.439976/57.70s. Total156817tokens/$0.960882, cache/reasoning subsets accounted
correctly in BASE/claude-costs.json. Exec33713 completed exit0; never poll/relaunch.

Controls-v1 preserves46 old and23 new synthetic scenarios. Immutable v3 matched
58/69:10 false violations and1 false scoped pass on live/aborted identity ambiguity.
V4 in evaluation-v1 matches69/69, with22/22 author selftests. Independent controls
include16 detections against clean baselines and11 against unresolved baselines
(separately accounted). All11 previous mismatches resolve to uncertainty, not
unearned completion. Original normative controls and ordinary live ordering stay.

Fresh review claude-v4/review.json is limited-ready. V4 can attribute any unique
unconsumed matching aborted request as unresolved; consume identity once, record
accept/abort/forward, never completion credit. Reset clears identities, not emitted
uncertainty. Same-master identical entries retain multiplicity; cross-master/live-
aborted ambiguity stays unresolved. No invented cancellation timing or survivor set.
F6 warning: cross-slave live forwarding order remains an inherited inference; not
an authoritative DUT-fault oracle. Limited replay freeze explicitly retains this
warning; no new live experiment authorized. F7 old negative/stale_after_reset is
an exclusion witness, not credited detection. Review wording “all checks” during
ambiguity is too broad: ownership-related checks pause; basic protocol checks run.
Not whole-IP proof; liveness/exact cancellation timing remain outside scope.

Replay-only freeze `configs/wbxbar_cancel_replay_freeze_v1.json` SHA256
`c099939dabc20bb61a077efcdc89dbe044830d5600e534f8092a93299937f692`.
V4 checker SHA256
`64a5b7ab5da5fb46fa610e040589f8063b20ddbe806349ccc1a29e026f6a3468`.
Freeze was made BEFORE revised checker saw live pilot traces. Original binary
reused, no compilation, zero new model stimuli. `replay-v1/`:42executions/8360cycles,
1.6262s simulator process/2.5587s wall. Exec8944 completed exit0.
Every pin/transport ledger and all2845 original source counters per batch match.
All36 model rounds unresolved; six seeds scoped_pass. Final B1/B2/B3 old diagnostic
counts1/3/2, C1/C2/C3 7/5/0; all revised diagnostics zero, allfinals unresolved.
Final unresolved records32 =19post_abort_forward +11ownership_ambiguous +2pending.
No new assumption violations. Zero confirmed new DUT defect types.

`replay-audit-v1/audit.json` passes fresh recomputation and checker execution on42
batches with no additional DUT/API call. `diagnostic-correspondence.json` matches
all59 repeated old alarms (18 final instances) uniquely by cycle AND slave to
explicit post_abort_forward records. None merely disappears behind ambiguity.
Old/new comparison CSV/JSON in replay-v1; all rawold verdicts preserved. Rawcoverage
and B/C cost conclusions unchanged. This is post-hoc reliability correction;
old trajectories used old feedback, so not a new causal B/C effectiveness trial.

New helpers: scripts/wbxbar_multi_abort_controls.py,
prepare_wbxbar_cancel_contract.py, run_wbxbar_cancel_roles.py,
wbxbar_cancel_validation.py, replay_wbxbar_cancel.py,
audit_wbxbar_cancel_replay.py; tests/test_wbxbar_cancel.py.
No original hash-bound runtime changed. Initial glob/oversized review/pypdf/test
assumption failures are documented, zeroAPI/simulator cost. Current docs, README,
PROJECT_STATUS and BASE/status.json updated. No commit/push.

Final checks complete: 8 integration tests pass (offline-tests-v2.log), helper compilation and git diff --check pass, frozen/original hashes match, report links exist, scoped secret-pattern scan clean and both staged keys absent. BASE/final-validation.json records these checks. Current task complete; no active work or pending key request.
Any later conformance extension must separately address public inference/ambiguity
and preserve role separation. Do not automatically start new B/C generation.
Reproduce read-only audit with new output: `.venv/bin/python
scripts/audit_wbxbar_cancel_replay.py --run
results/wbxbar_abort_contract_20261104/replay-v1 --output build/wbxbar-cancel-audit-new`.
This adds only checker re-execution. Repeating full simulation is unnecessary for
prose edits and would add separately accounted42executions/8360cycles.

## Previous pilot completion

The user authorized a separately registered exploratory WBXBAR B/C pilot with
relaxed difficulty admission, followed by one anonymous read-only Claude failure
attribution call (CLI budget $4). Both are complete. No active exec/model calls
remain. OpenAI and Anthropic staged keys were deleted. Do not launch a duplicate pilot, change its frozen checker code, or silently reinterpret
historical verdicts. New follow-up authority and its separate version are above. No commit or push occurred.

Main report: `docs/wbxbar_exploratory_bc_result_2026-11-04.md`.
Preparation history: `docs/wbxbar_exploratory_bc_2026-11-04.md`.
Evidence root: `results/wbxbar_exploratory_bc_20261104/`.
Baseline commit: `50d7ee83d61989017e28e981420cd58f4c5f0787`, plus hash-bound
uncommitted implementation. Many unrelated untracked files; never clean/reset.

## Measured result

`live-v1/` contains all 36 scheduled rounds: B/C each 3 repetitions × 6 rounds ×
at most 64 new cycles, plus the common 8-cycle seed. Exact model gpt-6.1-sol,
low reasoning, input 32000/output 16384, timeout 120 seconds, max one retry.
All 36 attempts accepted first try; 36 provider input-count requests. Usage:
697240 input + 73291 output = 770531 tokens. 42 simulations, 8360 executed cycles
including cumulative replay, 2 shared compilations, 827.25 seconds full wall time.
All six sessions hit all 8 groups / 17 source counters in round 1: each takes
80 physical cycles / 2 executions. All final line counts 82/86, branch 79/88,
expr 282/321; denominator 2845 includes 2350 toggle points. Branch is flat after
round 1. B target tokens 18966/18988/18982; C 27146/27184/27259. C mean token cost
to target +43.30%; six-round total +7.21%. Mean first branch ROI B 2.266 vs C 1.581
new branch points per 1000 API input+output tokens. Cached/reasoning are subsets.
C initial toggle mean is 68 counters higher; final median ties at 1952, with
B mean 1948 vs C 1952. Preserve this observation without a significance claim.
No placebo; cannot isolate semantic content from text length or sampling.

Five final frozen checker verdicts are dut_violation, one unresolved. None
reaches checker-complete target attainment. These are retained observations,
not confirmed DUT defects. 59 repeated cumulative-round diagnostics reduce to
18 instances in six final prefixes, not 18 distinct defects. All final input
assumption-violation lists are empty.

## Independent attribution and remaining limitation

`failure-review-packet-v1/`: 149010-byte anonymous packet, 448 complete trace rows,
two representative real failures plus two independent positive controls. No arm
names, coverage rankings, semantic groups, model prompts or costs. Full active
RTL, public authority, driver and frozen checker included for diagnosis only.
Icarus replays agree at meaningful pins and complete checker outputs: 2 additional
simulations / 400 cycles, separate from primary budget.
`failure-review-v1/review.json`: exact claude-opus-5-5, read-only, one call,
89353 tokens, $0.575131, 90.44 seconds. Review left conformance unresolved and
suggested inspecting aborted-queue matching. Both stages are complete.

`scripts/diagnose_wbxbar_checker_state.py` externally traces unchanged Python
checker via sys.settrace. No source, verdict, stimulus or simulation is changed.
`checker-state-diagnosis-v1/state.json`: case 1 failure44 matches master1 accept42
at ab[1][1]; case 2 failure308 matches master1 accept306 at ab[1][1].
`checker-final-diagnosis-v1/state.json`: all 18 final routing diagnostics have
exactly one identity match in a non-head aborted queue position. Current matcher
only checks the first entry for that slave. This identifies a shared attribution
limitation, not proof of legal post-abort forwarding or permission to reorder
live queues. Zero confirmed new DUT defect types. Do not convert these to pass.
Review prose corrections: reset does not clear accumulated unresolved records;
masked-write control forwards 0x1234a978, differing only in a disabled byte from
0x12345678. State-hook evidence gives exact cycles; reviewer indexing approximate.

Six Claude checker-development calls cost $2.459941 / 354236 tokens. Including
this review: seven calls, $3.035072 / 443589 tokens, separate from OpenAI totals.
`status.json` already includes all seven; do not append the final call again.

## Frozen boundary and implementation

Freeze `configs/wbxbar_exploratory_bc_freeze_v1.json` SHA256
`216ef3ea4cf3748c6a65be215bbdca7fb2c2ce832ff4dc745c1386641b5715aa`.
Parent `configs/wbxbar_exploratory_bc_v1.json` SHA256
`1a87bc051af7cff7e0819f463fe93a7cb029efd91171c5aa198afe895798bb31`.
Claude v3 `claude-v3/candidate/checker.py` SHA256
`163fd64a9fe3925b3cd64130c2b9a22e4489c1acfea36b985026c228aa6f3545`.
Original wbxbar.v SHA256
`d3fd1f2d7fb8909c2c2950c666e04c97d704c501c867201aedab5011ee106d2e`.
Historical live_allowed fields certify the original launch, not a recommendation
for new runs after the newly observed checker limitation.

Claude alone authored checker v1–v3 from public spec, own prior code and synthetic
controls. GPT did not edit it. Before live, v3 passed limited independent review;
46 checker-clean driver cases and all 17 target witnesses were verified. Keep
all failed checker versions and unresolved controls. Driver-v1: 48 cases / 96
paired-simulator executions / 7212 cycles. Fixed JSON fields: rst1, offer2,
addr16, data64, we2, sel8, slave_error2. Per-master queues hold request until PRE
handshake; ERR aborts accepted pending, retains unaccepted queue, inserts counted
CYC-low cycle. Reset clears queues; reset+offer invalid. No free drain. Independent
Python pin/transport validation does not define expected functional outputs.

Before live, `configs/wbxbar_prompt_representation_v1.json` registered active
preprocessed RTL with original locations, last64 own actions in lossless RLE and
last16 pin vectors. Full cumulative actions and counters remain on disk and are
replayed. Both arms get all17 targets plus the same rotating48 uncovered raw
points; C adds certified typed guards with reversible atom aliases. Full raw RTL
had exceeded 32k; caps were not raised. C groups disappear after all members hit,
so later rounds provide little semantic treatment and receive suspect checker
feedback. No calibration witnesses or solver stimuli enter model prompts.

## Artifact trail and verified accounting

Runtime: `scripts/wbxbar_experiment.py`, `run_wbxbar_bc.py`,
`prepare_wbxbar_experiment.py`, `wbxbar_exploratory_driver.py`.
Offline audit: `audit_wbxbar_experiment.py`; 31 focused checks and complete
mock-v4/replay-v4 passed, each 36 rounds / 42 executions / 8400 cycles.
Six offline attempts include one failed atom-regex mock; all retained. Offline
costs are not primary live costs. JSON object key-order audit mismatch was
resolved with decoded equality while preserving list order and exact counts.
`runner-validation-v1.json` records this and unchanged prior SPI freezes.

`scripts/audit_wbxbar_live.py` recomputes all 36 raw coverage results, exact source
denominator, rendered prompts, actions, pin/transport ledgers, usage and cycles.
`live-v1/audit.json` passes. `report_wbxbar_bc.py` generated CSVs, endpoint JSON,
descriptive-statistics.json and report.md. Keep frozen generator unchanged.
New presentation-only `plot_wbxbar_costs.py` fixes legend layout and adds toggle
plots, with no measurement changes. `coverage-cost` and `toggle-cost` PNG/PDF
are in live-v1. Source data: calls.jsonl, counts.jsonl, rounds.jsonl and each
round's prompts/actions/trace/raw coverage/checker outputs.

## Next permitted work

Final integrity check completed: fresh 36-round audit is
`build/wbxbar-final-audit-69dylm3u/audit.json` (pass), frozen hashes unchanged,
18 unique non-head aborted matches verified, both staged keys absent, four
post-run helpers compile, and git diff --check exits 0. Toggle plot visually
checked for readable axes/legend. No model or simulator rerun was required.
The preceding pilot task was complete; the newly authorized follow-up is above.
Before a future trial: Claude must independently specify abort/cancellation
attribution, add synthetic multiple-abort/partial-cancellation, duplicate/new-epoch,
reset and byte-mask fault controls, then make a separately reviewed checker
version and freeze. Preserve this pilot and its functional uncertainty. GPT may
provide driver/transport controls, not silently patch the checker. No same-IP
rerun merely to search for C gains. For new effectiveness tasks restore ordinary
exclusion and independent B difficulty admission; retain original budgets.

Read-only reproduction (use fresh output paths):
```
.venv/bin/python scripts/audit_wbxbar_live.py --run results/wbxbar_exploratory_bc_20261104/live-v1 --output build/wbxbar-live-audit.json
.venv/bin/python scripts/diagnose_wbxbar_checker_state.py --packet results/wbxbar_exploratory_bc_20261104/checker-final-diagnostic-inputs-v1 --output build/wbxbar-checker-state-replay
```
Neither invokes a model or simulator. Do not rerun old proof/model experiments
just for prose edits. Prior historical screening evidence follows.

## Constraints that must survive compaction

- Original development budget: **3 repetitions × 6 rounds × at most 64 new
  physical cycles**, plus 8 common seed cycles. No free waiting cycles.
- Model settings: `gpt-6.1-sol`, low reasoning, input cap 32,000, output cap
  16,384, 120-second timeout, at most one retry. Never silently substitute.
- Static gate: at least 3 source-distinct equivalent groups, at least 2
  nontrivial; each has at least 2 mapped original seed-zero source counters.
- Original event gate (waived only in the named exploratory scope): ordinary-operation union must leave selected counters at zero;
  at least 3 distinct event families with disjoint discriminating increments;
  independent-checker-clean calibration within 384 new cycles, with prefix and
  prerequisite/remedy-removal controls. Shared stall/reset/ready is not 3 events.
- Original B gate (descriptive only in the named exploratory scope): at least 2 repetitions leave at least 2 groups unhit after round 1;
  at least 2 repetitions make later progress; all repetitions complete and legal.
  C requires this gate and a separate final freeze. Placebo uses actual token
  matching and its own trajectory. Unsuccessful trials remain in the report.
- Claude authors the independent spec checker; GPT authors driver/stimulus.
  Never expose private calibration, golden answers or B/C outcomes to the
  spec-only checker author. Never put calibration witnesses in model prompts.
- Current semantics: two-state, typed widths/signedness, full guards and original
  clock/reset context. State/memory cuts are free except the separately proved,
  hash-bound WBXBAR activation implication below; no unproved invariant.
  Source counters stay separate even when predicates are equivalent. Unsupported
  mappings remain unresolved and stay in the raw denominator.
- Hidden credentials only through existing staging scripts when needed. Do not
  reuse keys quoted in old chat. Staged key presence is not assumed from history.

## Historical conditional-screen state (before exploratory B/C)

Authoritative audit for that historical screen:
`/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/results/wbxbar_conditional_20261104/validation.json`.

New WBXBAR scope `configs/wbxbar_conditional_index_v1.json` SHA-256:
`7d72cedd06a695ba01c76062a871ffe4aab7f1030e277c21a27a73fbda1b1146`.
Only imported state lemma (N=0,1):
`(!grant[N][2] && mgrant[N]) => unsigned(mindex[N]) <= 2`.
No protocol assumptions or invented index initialization. The stronger mgrant-only
trial fails at step 3; original source skips indexing on the pseudo-slave branch.
Final base/induction and ten nonvacuity covers pass; two deliberately false
properties fail as expected. Do not generalize this to whole-IP correctness.

Historical screen: 109 definition mismatches UNSAT; 91 mapped/34 unresolved; 16
noncanonical level-event targets withheld. Eight groups, six nontrivial, pass
static counts. All 17 distinct member counters are hit by isolated mapped/unmapped
reads. Forty-four ordinary cases / 88 executions / 6,712 cycles match between
Verilator and Icarus; raw denominator 2,845 is unchanged. Ordinary union is
line82/86, branch78/88, expr278/321, toggle1304/2350. No target survives.
At that historical checkpoint the driver had transport validation only, **no specification-output checker**.
No Claude or live B/C ran within that old screen. Its model calls/cost remain zero; the separately registered exploratory pilot above did run.
Fresh audit: 42 tests pass, 310 provenance checks, old SPI/prior evidence unchanged.

The following historical three-candidate audit remains immutable at
`results/transaction_recovery_screen_20261104/validation.json`:

| Fixed candidate | Verified outcome | Gate |
|---|---|---|
| `wbsafety` | 19 definition checks UNSAT; 61 mapped / 9 unresolved; 1,099 counters; 0 eligible groups | static rejected |
| `wbxbar` (old scope) | 108 constructed checks UNSAT, but `m_stall` was unsafe free combinational data | was semantic blocked; superseded only by new scope above |
| `axis_ram_switch` | 512 checks UNSAT; 91 mapped / 4 unresolved; 5,044 counters; 2 eligible groups, 0 nontrivial | static rejected |

RAM switch groups are true/false polarity of `len_reg == 0` at source lines 1016
and 1023. They do not establish three recovery events. Crossbar's earlier blocker
was the unrestricted `request[N][mindex[N]]` at line888, not a confirmed DUT bug.

**Not run in that old scope:** ordinary-operation traffic, multistep
reachability, Claude checker generation, B, C. Model calls/tokens/cost are zero.
18 saved offline attempts include 72 successful frontend calls, 7 inventory
compiles, 7 reset/quiescence executions and 56 cycles. Those are not pilot runs.
Prior audit records 31 passing focused/regression checks and unchanged SPI freeze.
Treat historical test results as historical until relevant checks are rerun.

Preregistration SHA-256:
`efa89c6703c8f0281355e6eae8004e05fb265dd85c0dd4ac5f077daf4ecf4393`.
WB upstream: `ZipCPU/wb2axip@2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b`.
AXIS upstream: `alexforencich/verilog-axis@48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
Two WB candidates share a lineage; RAM switch comes from a previously used family.
Do not claim three wholly independent or unseen upstreams.

## Artifact trail

Current additions (old files and freezes are unchanged):

- `docs/wbxbar_conditional_index_2026-11-04.md` — full report, commands and limits.
- `scripts/prove_wbxbar_index.py` — original-transition observer/SBY tasks.
- `scripts/wbxbar_conditional_semantics.py` — certificate, exact partial select,
  independent undefined bits and only the certified state-domain implication.
- `scripts/wbxbar_domain_proof.py`, `scripts/screen_wbxbar_conditional.py` — scoped
  definition/egg/source adapters; historical runners are untouched.
- `scripts/probe_wbxbar_ordinary.py` — fixed JSON ordinary transport, not a checker.
- `scripts/audit_wbxbar_conditional.py` — raw coverage/trace/provenance replay,
  regression tests and accounting. It writes only this scope's validation/logs.
- `tests/test_wbxbar_conditional.py`, `tests/test_wbxbar_ordinary.py` — 11 new tests.
- `results/wbxbar_conditional_20261104/`: formal-v1 (overbroad failed trial),
  formal-v2 (first actual-domain proof), formal-final (final expanded covers),
  domain-certificate.json, screen-v1 (event-context blocker), screen-v2 (accepted
  static screen), ordinary-v1 (44 cases), validation.json. Preserve failed versions.
  Only formal-final/current screen hashes must match current code; snapshots
  retain older producers. No output directory may be silently overwritten.

Older scope/report:

- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/configs/transaction_recovery_screen_v1.json` — fixed versions, sources, parameters, ordinary policies, gates and budgets.
- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/docs/transaction_recovery_screen_2026-11-04.md` — full results, limitations and commands.
- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/docs/PROJECT_STATUS.md` — broader history; consult only relevant sections.

Implemented in the preceding task; unchanged by skill setup:

- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/scripts/transaction_semantics.py` — `TransactionAdapter`, `TransactionBitVectors`, `ObservationNetlist`; instance bindings, array direction, exact memory cuts and independently bounded selects.
- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/scripts/transaction_counter_mapping.py` — `CounterRegistry`; exact generated C++ membership and specialization metadata, not wildcard guessing; incomplete shared-counter guard unions rejected.
- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/scripts/screen_transaction_recovery.py` — `run`; scoped adapters and evidence, no model/key access.
- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/scripts/audit_transaction_screen.py` — `audit`; provenance, versions, attempts, tests and old-freeze verification.
- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/tests/test_transaction_semantics.py` — array/instance/memory/range/signedness/mutation regression checks.
- `/Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project/tests/test_transaction_counter_mapping.py` — wildcard collision, missing members and identity collision checks.

Final evidence is under `results/transaction_recovery_screen_20261104/*-final`.
Earlier v1…v7 failures are historical; their code hashes need not match the latest
adapter. Raw logs/SMT/egg explanations and ignored generated C++ stay on disk.

Created by skill setup: repository `AGENTS.md`, this handoff,
`configs/agent_skills.lock.json`, and `docs/agent_workflow_skills_2026-11-04.md`.
Installed skills are outside the repository. No runtime hooks, shell startup
changes or model adapter injection are part of the installation.

## Decisions and next action

WBXBAR's original conditional scope remains rejected at ordinary exclusion.
The separately authorized exploratory scope above completed checker development and B/C. Its post-run abort-matching limitation requires a separate checker revision before any new experiment. Reuse the certified
domain approach for future cases, but seek event-specific source predicates for
contention drain, timeout/abort recovery and state-dependent resource release.
Another candidate/adapter extension needs separate preregistration and all gates;
do not change budget/targets after model outcomes. Current key lifecycle and review
status are above; never infer staged-key presence from this note alone.

Prior findings needed to avoid repetition: safe-offer SPI B reached 16/17 groups
in round 1 and all 17 in round 2, failing difficulty; frame-adjuster groups were
all hit by ordinary frames. Prior controlled trials found no repeatable C-over-B
gain. More source code alone is not evidence of a discriminating task.

## Verification commands and recovery probes

From the repository, relevant existing checks are:

```sh
.venv/bin/python scripts/audit_wbxbar_conditional.py
```

The current audit reruns 42 checks and rewrites its own validation artifact; do
not rerun merely for prose edits. The old transaction audit would rewrite old
evidence; avoid it. Formal replay and screen/ordinary reruns require new output
directories; commands are in the current report. Formal tools use bundled Z3
4.15.5; combinational queries use system Z3 5.1.0 (do not conflate versions).

Before continuing, answer from this note and verify against linked evidence:
What budget is fixed? Who may change a checker? Why is crossbar rejected? Which
stages have NOT run? Where are raw counts and hashes? What is the next permitted
action? A missing answer means retrieve the specific source, not invent it.
