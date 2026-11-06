"""Seal actual saved E01 outputs; no API, scoring, compile or replay invocation."""
from pathlib import Path
from collections import Counter
import hashlib,json,shutil,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
RUN=ROOT/'test2/results/controller-done-bc-retest-v3';CONTROL=Path(str(RUN)+'-supervision')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:stream.write(json.dumps(value,indent=2)+'\n')
def copy(path,dest):
    dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists(),dest;shutil.copy2(path,dest)

def main():
    assert not (HERE/'snapshot-manifest.json').exists(),'ALREADY_SEALED'
    entry=load(HERE/'entry.json');summary=load(RUN/'summary.json');ledger=load(RUN/'ledger.json');parent=load(CONTROL/'parent-receipt.json');score=load(RUN/'grade/scores.json');registration=ROOT/'test2/configs/controller_done_bc_retest_v3.json';reg=load(registration)
    paths=dict(registration=registration,source_manifest=ROOT/reg['source_manifest'],preparation_manifest=ROOT/reg['preparation_manifest'],review=ROOT/'docs/audits/agent_bridge_2026-11-06/P18_bc_retest_preflight/review-R03.json',EXECUTE=ROOT/'docs/audits/agent_bridge_2026-11-06/BC_retest_v1/execute-receipt-r03.json')
    for key,path in paths.items():assert sha(path)==entry[key+'_sha256'],key
    assert parent['returncode']==0 and not parent['deadline_forced_stop'] and not parent['mandatory_errors'] and parent['within_total_wall']
    assert summary['status']==score['status']=='COMPLETE_WITH_UNRESOLVED_RETAINED' and ledger['completed'] and ledger['halted'] is None
    assert (ledger['generations_reserved'],ledger['counts_reserved'],ledger['compile_calls'],ledger['monitor_replays'],ledger['monitor_cycles'])==(6,0,12,990,204444)
    assert ledger['financial_commitment_micro_usd']==ledger['settled_upper_micro_usd']==1569371 and ledger['unresolved_reservations_micro_usd']==0
    assert len(score['rounds'])==6 and score['inventory_cases']==162 and score['release_sha256']==sha(RUN/'release.json')
    assert score['registration_sha256']==sha(ROOT/'test2/configs/controller_done_scoring_v4.json')
    release=load(RUN/'release.json')
    for name,digest in release['files'].items():assert sha(RUN/name)==digest,name
    snapshots=load(RUN/'all-round-candidates.json')['rounds'];assert len(snapshots)==6
    for row in snapshots:
        path=RUN/row['snapshot'];assert sha(path)==row['sha256'];snap=load(path)
        for name,digest in snap['files'].items():assert sha(RUN/name)==digest,name
    calls=[json.loads(line) for line in (RUN/'calls.jsonl').read_text().splitlines() if line.strip()]
    assert [(r['arm'],r['round']) for r in calls]==[tuple(r) for r in reg['schedule']]
    assert all(r['accepted_response'] and r['returned_service_tier']=='default' and r['attempt']==1 and not r['count_request_issued'] for r in calls)
    for row in calls:
        u=row['usage'];assert type(u['input_tokens']) is int and 0<u['input_tokens']<=64000 and u['output_tokens']<=8192 and u['total_tokens']==u['input_tokens']+u['output_tokens']
    source=load(paths['source_manifest']);assert all(sha(ROOT/name)==digest for name,digest in source['files'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();index=hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT)).hexdigest()
    assert head==entry['actual_HEAD'] and index==entry['index_entries_sha256'] and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT)

    rounds=[{k:v for k,v in row.items() if k!='cases'} for row in score['rounds']]
    arm_usage={}
    for arm in ['B2_raw','C2_semantic']:
        rows=[r for r in calls if r['arm']==arm];events=[e for e in ledger['events'] if e['context']['arm']==arm]
        arm_usage[arm]=dict(generation_requests=len(rows),tokens={k:sum(r['usage'][k] for r in rows) for k in ['input_tokens','output_tokens','total_tokens','cached_input_tokens','reasoning_output_tokens']},settled_upper_micro_usd=sum(e['settled_upper_micro_usd'] for e in events),actual_invoice_usd=None)
    total_tokens=sum(a['tokens']['total_tokens'] for a in arm_usage.values());assert total_tokens==257578==score['costs']['actual_generation_tokens']
    child_rows=[]
    for path in RUN.rglob('*.process.json'):
        data=load(path);argv=data.get('argv',[]);kind='API' if any(str(a).endswith('/api.py') for a in argv) else Path(argv[0]).name
        child_rows.append(dict(path=str(path.relative_to(ROOT)),kind=kind,status=data['status'],seconds=data['seconds']))
    child_counts=dict(Counter(r['kind'] for r in child_rows));assert child_counts==dict(API=6,yosys=6,iverilog=6,vvp=990)
    assert all(r['status']=='complete' for r in child_rows)
    committed=0;peak=0
    for row in ledger['journal']:
        if row['op']=='RESERVE':committed+=row['micro_usd']
        else:
            assert row['op']=='SETTLE_UPPER_AND_RELEASE_UNUSED';committed-=row['unused_reservation_released_micro_usd']
        peak=max(peak,committed);assert committed<=20000000
    assert committed==ledger['financial_commitment_micro_usd']
    token_delta=(arm_usage['C2_semantic']['tokens']['total_tokens']/arm_usage['B2_raw']['tokens']['total_tokens']-1)*100
    cost_delta=(arm_usage['C2_semantic']['settled_upper_micro_usd']/arm_usage['B2_raw']['settled_upper_micro_usd']-1)*100
    analysis=dict(status='PRODUCER_SAVED_EVIDENCE_SUMMARY_PENDING_P19',rounds=rounds,selected_endpoints=score['selected_endpoints'],finals=load(RUN/'final-candidates.json')['candidates'],usage_by_arm=arm_usage,total_actual_generation_tokens=total_tokens,C_vs_B_total_tokens_pct=token_delta,C_vs_B_cost_upper_pct=cost_delta,finance=dict(ceiling_micro_usd=20000000,per_dispatch_full_reserve_micro_usd=5910168,settled_upper_micro_usd=ledger['settled_upper_micro_usd'],unresolved_full_reserves_micro_usd=0,peak_outstanding_commitment_micro_usd=peak,gross_historical_reservations_micro_usd=ledger['total_reservations_micro_usd'],unused_reservations_released_micro_usd=ledger['unused_reservation_released_micro_usd'],actual_invoice_usd=None,release_is_not_refund=True),runtime=dict(parent_elapsed_seconds=parent['elapsed_seconds'],worker_elapsed_seconds=summary['global_elapsed_seconds'],grade_wall_seconds=score['costs']['wall_seconds'],child_counts=child_counts,sum_child_wall_seconds_by_kind={kind:sum(r['seconds'] for r in child_rows if r['kind']==kind) for kind in child_counts},CPU_and_memory='UNKNOWN_NOT_MEASURED',child_inventory_complete=parent['child_inventory_complete'],timing_components_overlap_do_not_add_to_stage_wall=True),scope=dict(raw_fault_types=12,raw_fault_pairs_per_round=144,correct_controls_per_round=18,case_pairs_per_round=162,total_case_pairs=972,N10='Mutant ID,not a denominator10;12referencePASS/noeligiblefaultpairs',input_completion='0/10eligibleN01pairs,allwithoracleunknown;notN10',oracle_unknown_pairs_per_round=38,oracle_unknown_by_type=rounds[0]['oracle_unknown_by_type'],ordinary_safety_types=9,end_marker_case_UNATTRIBUTED_types=2,raw_union_definite_types=11,not_fresh_hidden_benchmark=True,not_pure_semantic_placebo_comparison=True,new_DUT_native_formal_jobs=0,no_proof_of_general_monitor_correctness=True))
    write(HERE/'analysis.json',analysis);write(HERE/'child-resource-summary.json',dict(counts=child_counts,receipts=child_rows,CPU_memory_unknown=True))
    bindings={key:dict(path=str(path.relative_to(ROOT)),sha256=sha(path)) for key,path in paths.items()}
    bindings.update(release=dict(path=str((RUN/'release.json').relative_to(ROOT)),sha256=sha(RUN/'release.json')),grade=dict(path=str((RUN/'grade/scores.json').relative_to(ROOT)),sha256=sha(RUN/'grade/scores.json')),ledger=dict(path=str((RUN/'ledger.json').relative_to(ROOT)),sha256=sha(RUN/'ledger.json')),parent=dict(path=str((CONTROL/'parent-receipt.json').relative_to(ROOT)),sha256=sha(CONTROL/'parent-receipt.json')))
    write(HERE/'bindings.json',bindings)
    for key,path in paths.items():copy(path,HERE/'exact-inputs'/path.relative_to(ROOT))

    header=f'''
## Current same-IP B/C retest — E01 actual run complete, pending P19 (2026-11-06)

Exact R03 review PASS_WITH_LIMITS and root EXECUTE enabled one actual live entry;
it returned0 in{parent['elapsed_seconds']:.3f}s, no halt/timeout/mandatory error.
Six actual generations (B/C each1session x3rounds),0count/0retry; all six compile
and development pass, then freeze before one shared-v4 grade. Both final choices
are round3. All rounds have identical outcomes: raw union11/12types; nine ordinary
safety types and two end-marker finite case types UNATTRIBUTED. N10 is the mutant
ID with12referencePASS/noeligiblefaultpairs, not denominator10. Input completion
is0/10eligible N01pairs withoracleunknown. All38oracleunknown/round remain, with
raw12types/144faultpairs plus18correct controls/162total pairs. All18correct
controls pass perround; this is not general monitor correctness or128cycleproof.

B tokens123663 (input116529/output7134), C133915 (input127168/output6747),
C+{token_delta:.6f}% with identical detections. Input+output total257578 includes
reasoning subsets;do not addcached/reasoning again. No C benefit observed in this
single-session published-corpus retest;no freshhidden/generalization or placebo
claim. Conservative settled cost upperUSD1.569371 (B0.758621/C0.810750), not invoice;
unresolved cost reserves0, peak outstandingUSD{peak/1e6:.6f} below20. Gross historical
reserve sum35.461008 is not simultaneous commitment or spend;unused release is
not a refund. Actual provider invoice remainsUNKNOWN.

Onepass actual12compile(6Yosys+6Iverilog),990monitorreplays/204444cycles
(18dev/1380cycles +972grade/203064cycles);0newDUT/native/formal/G1/crossIP jobs.
All1008child receipts complete;CPU/memory/fullchildcensus remainunknown. Stage
wall includes cleanup;component timings overlap and must not be double-added.
No extra score/compile/replay or API was run after the stage. Key retained;
auditor never reads/hashes its contents. Old freezes/source/scores/index remain.

Actual immutable evidence and pending independent acceptance:
`docs/audits/producer_test2_bc_retest_E01_2026-11-06/phase.json`,report.md,
analysis.json,bindings.json,snapshot-manifest.json;actual outputs under
`test2/results/controller-done-bc-retest-v3`. Next existing P19 reviews saved
evidence only, then root may arrange separately authorized publication. No
automatic new model/solver/replay run or Git mutation. Actual HEAD{head}, all
current work uncommitted/unpushed. Older complete document bodies follow unchanged.
'''
    shared={}
    for name in ['HANDOFF.md','PROJECT_STATUS.md']:
        path=ROOT/'docs'/name;old=path.read_bytes();copy(path,HERE/'before/docs'/name);first,rest=old.split(b'\n',1)
        assert sha(path)==hashlib.sha256(old).hexdigest();path.write_bytes(first+b'\n'+header.encode()+b'\n'+rest);copy(path,HERE/'snapshot/docs'/name)
        shared[name]=dict(before_sha256=hashlib.sha256(old).hexdigest(),after_sha256=sha(path),entire_old_body_retained=path.read_bytes().endswith(rest))
    phase=dict(phase='BC_RETEST_E01_ACTUAL_R03_EXECUTION',status='EXECUTED_COMPLETE_UNRESOLVED_RETAINED_PENDING_P19',entry_count=1,entry_exit_code=0,run_root=str(RUN.relative_to(ROOT)),supervision_root=str(CONTROL.relative_to(ROOT)),actual_HEAD=head,index_entries_unchanged=True,registration_sha256=entry['registration_sha256'],source_manifest_sha256=entry['source_manifest_sha256'],preparation_manifest_sha256=entry['preparation_manifest_sha256'],review_sha256=entry['review_sha256'],EXECUTE_sha256=entry['EXECUTE_sha256'],API_generation_dispatches=6,confirmed_provider_responses=6,remote_count_calls=0,retries=0,actual_generation_tokens=total_tokens,usage_by_arm=arm_usage,settled_upper_micro_usd=1569371,unresolved_cost_reserves_micro_usd=0,actual_invoice_usd=None,peak_outstanding_commitment_micro_usd=peak,compile_roots=12,monitor_replays=990,monitor_cycles=204444,new_DUT_native_formal_G1_crossIP_jobs=0,stage_wall_seconds=parent['elapsed_seconds'],timeouts=0,mandatory_errors=[],planned_snapshots=6,selected_finals=2,grade_rounds=6,planned_case_pairs=972,oracle_unknown_pairs_per_round=38,candidate_unknown_pairs_per_round=[r['candidate_unknown_pairs'] for r in rounds],raw_union_detection_types_per_round=[len(r['union_definite_types_UNATTRIBUTED']) for r in rounds],raw_fault_type_denominator=12,C_extra_detection_benefit_observed=False,C_vs_B_total_tokens_pct=token_delta,source_dependencies_verified=len(source['files']),frozen_release_hashes_verified=True,old_sources_and_scores_overwritten=False,extra_API_score_compile_replay_after_stage=0,credential_retained=True,credential_content_read_or_hashed_by_audit=False,runtime_used_existing_staged_credential=True,independent_P19_acceptance=None,publication_performed=False,shared_document_additions=shared,next='EXISTING_P19_SAVED_EVIDENCE_REVIEW_THEN_ROOT_PUBLICATION_NO_AUTOMATIC_EXPERIMENT')
    write(HERE/'phase.json',phase)
    lines=['# E01 actual B/C known-benchmark retest','',f'The exact authorized R03 entry ran once, exited0 and completed in {parent["elapsed_seconds"]:.3f}s. Independent P19 acceptance remains pending. No extra scoring, compilation, replay, API or Git mutation follows this execution.','', '| Arm / round | Correct controls | Ordinary safety definite pairs | Response finite pairs | Input finite pairs | Raw union types | Oracle unresolved |','|---|---|---|---|---|---|---|']
    for row in rounds:
        cats=row['categories'];lines.append(f'| {row["arm"]} / {row["round"]} | PASS18/18 | {cats["safety"]["definite_pairs"]}/{cats["safety"]["eligible_pairs"]} | {cats["response_completion"]["definite_pairs"]}/{cats["response_completion"]["eligible_pairs"]} | {cats["input_completion"]["definite_pairs"]}/{cats["input_completion"]["eligible_pairs"]} | {len(row["union_definite_types_UNATTRIBUTED"])}/12 | {row["oracle_unknown_pairs"]}/162 |')
    lines += ['', 'The raw denominator is twelve fault types and144fault pairs per candidate, plus18correct controls. Nine types receive ordinary-safety credit; two (N02/N03) receive end-marker case-level finite credit marked UNATTRIBUTED, not category-specific monitor proofs. Safety106/106 is definite evidence; only68/106 is fully resolved because38pairs retain oracle unknown. Response20/20 is fully resolved. These categories overlap and must not be added as disjoint counts. No sample is silently dropped.', '', 'N10 is a mutant identifier, not a denominator of ten. Its twelve frozen reference outcomes are PASS and it has no eligible fault pair. The input-completion0/10 instead concerns N01: those ten cases also have safety FAIL and oracle unknown. N10 is not a newly found LLM failure; the reference is not repaired, unknowns do not become PASS and the raw12 denominator remains.', '', '| Arm | Actual input | Actual output | Total | Conservative usage upper USD |','|---|---:|---:|---:|---:|']
    for arm,item in arm_usage.items():lines.append(f'| {arm} | {item["tokens"]["input_tokens"]} | {item["tokens"]["output_tokens"]} | {item["tokens"]["total_tokens"]} | {item["settled_upper_micro_usd"]/1e6:.6f} |')
    lines += ['', f'C used {token_delta:.6f}% more total tokens, with identical first-round and final outcomes; the conservative dollar upper is {cost_delta:.6f}% higher. Total257578tokens,6generation requests,0remote counts/retries/unknown usage. Reported cached-input tokens0 and reasoning1200 are subsets, not additional totals. Cost upperUSD1.569371 is not a provider invoice. No extra API call queried billing.', '', f'Each dispatch reservedUSD5.910168; ledger journal peak outstandingUSD{peak/1e6:.6f}, belowUSD20. Gross historical reservesUSD35.461008 reflect sequential reuse of released unused reservations, not spend or simultaneous commitments. Settled upperUSD1.569371, unresolved reserves0, unused reservation releaseUSD33.891637. A release is not a refund. Billing assumptions are the exact independently reviewed fixed model/tier/cache/region basis; no arbitrary provider price-drift guarantee is inferred.', '', 'One actual local pass used12compile roots (6Yosys/6Iverilog),990monitor replay roots and204444replayed cycles:18development replays/1380cycles plus972grading replays/203064cycles. These are monitors on frozen DUT observations, not new stimulus generation or new physical DUT executions. All1008child receipts are complete. No timeout, new DUT/native/formal/G1/cross-IP or tool-version query was added. Parent wall177.994570s includes cleanup; worker/grade/child timings overlap, are not CPU measurements and must not be summed as independent stage cost. CPU, memory and exhaustive child census remain unknown.', '', 'The source/registration/model/limits, Claude independent reference, GPT candidate roles, trace_done finalpost ABI and fixed public packets remained frozen. B receives public/raw feedback; C adds only the old verified E-graph package. Each arm has one independent session and three own-history rounds in B1,C1,C2,B2,B3,C3 order. Six candidates froze before the one common scoring pass; both finals select round3. No evaluation score was returned to a candidate. Source and prompt/release hashes are retained for independent inspection.', '', 'This is a retest of a previously published corpus, not a fresh hidden evaluation. Both arms saturate the currently observable type set in round1; this run supplies no extra C detection benefit and has higher C token cost. One trajectory per arm and no token-matched placebo limit causal/statistical interpretation. Passing18finite correct controls does not prove general monitor soundness, unbounded behavior,128cycle completion or E-graph semantic advantage. No formal proof was run for these new monitors.', '', 'A progress message initially associated N10 with input completion; saved-evidence inspection corrected that description above. The raw results were never relabeled. All historical negative outcomes,38unknowns per round, old formal timeouts, G1 limits and earlier scores remain unchanged.', '', 'The original exact command and escalation are in entry.json; output roots cannot be restarted. bindings.json pins the accepted review/EXECUTE, source/reg/preparation, actual ledger/release/grade/parent receipts. analysis.json and child-resource-summary.json derive from saved outputs only. snapshot-manifest.json uses repository-root-relative paths and binds this audit plus every actual run/supervision artifact. Staged credentials, environments and caches are excluded; the auditor never reads/hashes key contents. Key remains staged for the agreed completion policy. Next: existing P19 independently reviews saved evidence, then root handles separately authorized publication. Do not invoke new API/native/score/compile/replay merely to recover context.']
    with (HERE/'report.md').open('x') as stream:stream.write('\n'.join(lines)+'\n')
    paths=[p for base in [HERE,RUN,CONTROL] for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    members={p.relative_to(ROOT).as_posix():sha(p) for p in paths};assert not any('build/private/' in p for p in members)
    write(HERE/'snapshot-manifest.json',dict(status='E01_ACTUAL_EVIDENCE_FROZEN_PENDING_P19',files=dict(sorted(members.items())),file_count=len(members),path_base='Repository root,not manifest parent',excluded=['snapshot-manifest.json(selfhash)','Credentials/environment/cache','No duplicate old immutable dependency tree'],scope='Actual single live entry outputs,allcalls/providerusage/compiled monitors/replaylogs/grade/release/parent and audit records;not new hidden data'))
    assert hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT)).hexdigest()==entry['index_entries_sha256']
    print(json.dumps(dict(status=phase['status'],phase_sha256=sha(HERE/'phase.json'),snapshot_manifest_sha256=sha(HERE/'snapshot-manifest.json'),analysis_sha256=sha(HERE/'analysis.json'),report_sha256=sha(HERE/'report.md'),evidence_members=len(members),cost_upper_USD=1.569371,C_total_tokens_pct=token_delta),indent=2))

if __name__=='__main__':main()
