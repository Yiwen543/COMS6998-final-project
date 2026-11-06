"""One-shot offline R02 source/evidence seal;does not execute any experiment."""
from pathlib import Path
import ast,hashlib,json,shutil,subprocess,time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PREP=ROOT/'test2/results/controller-done-bc-retest-preparation-v2'
SOURCE=ROOT/'test2/retest_v2'
REG=ROOT/'test2/configs/controller_done_bc_retest_v2.json'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:stream.write(json.dumps(data,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def index_entries_sha():return hashlib.sha256(subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT)).hexdigest()
def copy(path,destination):
    destination.parent.mkdir(parents=True,exist_ok=True)
    assert not destination.exists(),destination
    shutil.copy2(path,destination)

def main():
    assert not (HERE/'snapshot-manifest.json').exists(),'ALREADY_SEALED'
    baseline=load(HERE/'before.json');reg=load(REG)
    assert git('rev-parse','HEAD')==baseline['HEAD']
    assert index_entries_sha()==baseline['index_sha256']
    assert not git('diff','--cached','--name-only')
    for name,digest in baseline['protected'].items():assert sha(ROOT/name)==digest,name
    for name,digest in baseline['R01_source'].items():assert sha(ROOT/'test2/retest_v1'/name)==digest,name
    protected=load(HERE/'protected-verification.json');assert protected['status']=='PASS'
    assert all(row['mismatch_count']==0 for row in protected['checks'])
    for row in protected['checks']:assert sha(ROOT/row['manifest'])==row['manifest_sha256']
    for name in ['release.py','supervision.py']:assert sha(SOURCE/name)==baseline['R01_source'][name]
    for name in ['controller-done-bc-retest-v1','controller-done-bc-retest-v2']:
        assert not (ROOT/'test2/results'/name).exists(),'LIVE_ROOT_EXISTS'
        assert not (ROOT/'test2/results'/(name+'-supervision')).exists(),'LIVE_CONTROL_ROOT_EXISTS'
    first=load(PREP/'targeted-attempt1/summary.json');delta=load(PREP/'provider-delta-attempt1/summary.json')
    assert (first['tests'],first['failures'],first['errors'])==(18,0,0)
    assert (delta['tests'],delta['failures'],delta['errors'])==(1,0,0)
    changed_after_18=[]
    for name,digest in first['executed_source_sha256'].items():
        if sha(ROOT/name)!=digest:changed_after_18.append(name)
    assert set(changed_after_18)=={'test2/retest_v2/api.py','test2/retest_v2/targeted_tests.py'}
    for name,digest in delta['executed_source_sha256'].items():assert sha(ROOT/name)==digest,name
    for path in SOURCE.glob('*.py'):ast.parse(path.read_text())

    admissions=load(PREP/'targeted-attempt1/test_09_complete_initial_payload_estimates_are_not_exact_counts/check.json')['complete_initial_payload_admissions']
    write(HERE/'local-admissions.json',dict(status='LOCAL_ESTIMATES_ONLY',complete_payload=admissions,remote_count_requests=0,not_exact_count=True,not_input_server_hardcap=True,no_packet_trimming=True))
    checks=dict(initial_18=dict(path=str((PREP/'targeted-attempt1').relative_to(ROOT)),tests=18,failures=0,errors=0,seconds=first['seconds']),final_provider_delta=dict(path=str((PREP/'provider-delta-attempt1').relative_to(ROOT)),tests=1,failures=0,errors=0,seconds=delta['seconds']),changed_after_18=changed_after_18,explanation='Extract normalization into pure provider_result;preserve raw JSON on malformed nested structures;new single test covers valid and malformed branches. First18 not rerun;not one final19 suite.',R01_reused_only=dict(fullmock_replay_tests=19,guard_tests=6,initial_failed_test_retained=True),fullmock_rerun=False,G1_rerun=False,actual_API_key_process_SV=0)
    write(HERE/'checks-and-deltas.json',checks)

    # Reuse old frozen members without duplicating 130MB of old data again.
    files=dict(load(ROOT/'test2/retest_v1/source-manifest.json')['files'])
    additions=[*SOURCE.glob('*.py'),SOURCE/'README.md',SOURCE/'prompt-boundary.json',REG,Path(__file__),HERE/'before.json',HERE/'protected-verification.json',HERE/'index-verification-correction.json',HERE/'local-admissions.json',HERE/'checks-and-deltas.json',HERE/'review-prompt.md',ROOT/'test2/retest_v1/source-manifest.json',ROOT/'docs/audits/producer_test2_bc_retest_R01_2026-11-06/snapshot-manifest.json',ROOT/'docs/audits/producer_test2_bc_retest_R01_2026-11-06/phase.json',PREP/'targeted-attempt1/summary.json',PREP/'provider-delta-attempt1/summary.json']
    additions += [ROOT/reg[key] for key in ['financial_policy','method_addendum','cost_basis','original_authorization','user_zero_count_confirmation']]
    for path in additions:
        name=path.relative_to(ROOT).as_posix();assert 'build/private/' not in name and '__pycache__' not in name
        files[name]=sha(path)
    source_manifest=SOURCE/'source-manifest.json'
    write(source_manifest,dict(status='OFFLINE_PREPARED_PENDING_EXACT_PRECHECK_EXECUTE',files=dict(sorted(files.items())),credentials_excluded=True,shared_mutable_docs_excluded=True,old_dependencies_reused='All916 R01 source members retained with identical hashes;old900member freeze verified separately.',scope='Maintainer execution/grading dependencies,not a candidate promptallowlist',billing='Zero counts,fullcontext reserve,only trusted upper settlement;exact precheck and EXECUTE required'))

    header='''
## Current same-IP B/C retest — R02 zero-count prepared, no live execution (2026-11-06)

The user confirmed the zero remote count method: 64k is a local ESTIMATE target
and actual-response qualification threshold, not a server input hard cap. R02
uses unchanged public B/raw and C/raw+verified E-graph packets, one independent
session per arm, three rounds, B1,C1,C2,B2,B3,C3. This is a known published old
benchmark retest, not a fresh hidden set. Old DUT, Claude reference, fixed stimuli,
ABI, raw12/N10/38unknown and all historical results remain unchanged.

Complete first-request estimates: B46876/C52466 (system+packet+schema included).
Remote counts0; counts are not assumed free. Before each generation reserve
USD5.910168 using the reviewed model context bound. Only complete trusted qualified
usage may settle to a conservative actual-usage upper; failed/unknown/incomplete/
over64k results retain full reserve and halt. Dispatch commitments never exceed
USD20. Up to12 generations/output8192/total3600s; local singlepass remains at most
12compile/990monitor replays/204444cycles, no new DUT/native/setup/formal/G1 jobs.
Six snapshots freeze before shared grading, including invalid/NOT_RUN cases.

New `test2/retest_v2/` and `test2/configs/controller_done_bc_retest_v2.json` are
prepared for exact independent code precheck, then a separate root EXECUTE.
Stdlib HTTPS needs no installation; explicit existing CA/hostname verification,
one fixed POST, no redirects/automatic retry. Real transport/supervisor/SV were
not exercised here. R02 has18 pure checks PASS plus1 final provider-JSON retention
delta PASS; these are separate source-bound runs, not a final19-test full suite.
The six-round stub does no compilation/replay and produces no scientific scores.
R01 full mock/replay and G1 were not rerun; sealed R01 remains unchanged.

Preparation: `docs/audits/producer_test2_bc_retest_R02_2026-11-06/phase.json`,
`report.md`, `review-prompt.md`, `snapshot-manifest.json`. The earlier verifier
used the wrong base for R01 relative paths; corrected hash checks show0mismatches
for12326 archived files/916 dependencies/900 old frozen members. The verifier
error is retained in protected-verification.json. Staged key retained; no content
read/hash, no API/network/SV/paid call, no install/commit/push. Actual HEAD remains
2de33e981d2fffc9739d2ca049fbae1774de1aad; new work is uncommitted/unpushed.

Next: existing P18 audits exact R02 hashes and deltas. Live is blocked until the
accepted exact review and root EXECUTE; key staging is not EXECUTE. Do not request
the key again, rerun completed mock/G1 for context, alter old freezes, or claim C
benefit from this preparation. All earlier document bodies follow unchanged.
'''
    docs={}
    for name in ['HANDOFF.md','PROJECT_STATUS.md']:
        path=ROOT/'docs'/name;body=path.read_bytes();copy(path,HERE/'before/docs'/name)
        firstline,rest=body.split(b'\n',1);assert sha(path)==hashlib.sha256(body).hexdigest()
        path.write_bytes(firstline+b'\n'+header.encode()+b'\n'+rest)
        copy(path,HERE/'snapshot/docs'/name)
        docs[name]=dict(before_sha256=hashlib.sha256(body).hexdigest(),after_sha256=sha(path),entire_old_body_retained=path.read_bytes().endswith(rest),old_suffix_sha256=hashlib.sha256(rest).hexdigest())

    phase=dict(phase='BC_RETEST_R02_ZERO_COUNT_OFFLINE_PREPARATION',status='PREPARED_PENDING_EXACT_INDEPENDENT_PRECHECK_AND_EXECUTE',actual_HEAD=git('rev-parse','HEAD'),registration=str(REG.relative_to(ROOT)),registration_sha256=sha(REG),source_manifest=str(source_manifest.relative_to(ROOT)),source_manifest_sha256=sha(source_manifest),snapshot_manifest=str((HERE/'snapshot-manifest.json').relative_to(ROOT)),normal_generations=6,max_generations=12,remote_count_requests_max=0,local_input_target=64000,local_target_is_server_hardcap=False,actual_input_over_target='Retainresponse/cost,halt,notqualified',output_max=8192,API_ceiling_micro_usd=20000000,per_dispatch_full_reserve_micro_usd=5910168,trusted_settlement_formula_micro_usd='(55*input_tokens+165*output_tokens+9)//10',qualified_max12_upper_micro_usd=5846016,three_unknown_reserves_micro_usd=17730504,actual_invoice_usd=None,API_requests=0,remote_count_requests=0,SDK_clients_constructed=0,credential_content_read_or_hashed=False,new_credential_metadata_probe=False,credential_retained=True,credential_status_scope='Userconfirmedstaged;R01metadatarecordreused;no content read',network_auth_probes=0,real_SV_or_supervised_process_signal_calls=0,local_pass_caps=reg['local'],global_runtime_wall_seconds=3600,local_admissions=admissions,tests=checks,old_protected_verification=str((HERE/'protected-verification.json').relative_to(ROOT)),independent_exact_precheck=None,EXECUTE=None,actual_live_root_exists=False,index_unchanged=index_entries_sha()==baseline['index_sha256'],shared_document_additions=docs,partial_preparation_seconds=time.time()-baseline['started_epoch'],partial_time_scope='Offline preparation elapsed since R02 baseline,not future live60min or invoice',next='EXISTING_P18_EXACT_CODE_PRECHECK_THEN_ROOT_EXECUTE_ONLY')
    for key in ['financial_policy','method_addendum','cost_basis','original_authorization','user_zero_count_confirmation']:
        phase[key]=reg[key];phase[key+'_sha256']=reg[key+'_sha256']
    write(HERE/'phase.json',phase)
    report='''# R02 preparation result — live not executed

The zero remote count B/C retest adapter is prepared for exact independent code
precheck and root EXECUTE. User method confirmation is bound separately from
execution permission. No real API, network/auth probe, credential content read or
hash, SystemVerilog/native/physical experiment, installation, commit or push ran.

| Item | Evidence and scope |
|---|---|
| Public request admission | Whole first payload B106948bytes/estimate46876; C120923bytes/estimate52466. Includes system+schema. ESTIMATE only; later own-history requests are checked independently. |
| Finance | Reserve5910168 microUSD before each dispatch; only fully trusted qualified responses settle upper. 64000input/8192output upper487168; six2923008/twelve5846016. Not invoice or expected bill. |
| Unknown/failure | Full reserve retained; halt without another probe. Three unresolved reserves17730504 make fourth inadmissible; actual runner halts at its first fatal unknown. |
| New tests | Initial18PASS/0fail/0error in0.229398166s. After provider normalization extraction, one new delta PASS in0.001718542s; only api.py/testharness changed. Not one final-source19 suite. |
| Narrow schedule stub | Six frozen snapshots and two finals; zero remote count/compile/replay/cycles. Grade is NOT_SCORED_STUB, not a scientific result. |
| Cancellation stub | Six snapshots retained; all972planned case pairs unresolved, full reservation retained. No grader replay. |
| TLS/HTTP | Existing CA128entries, CERT_REQUIRED and hostname verification; fake one-POST and redirect/error controls. No real network/timeout validation. |
| Reused evidence | Historical R01 repaired19-test full mock/replay and six guard checks, not rerun. G1 P17 finite acceptance remains closed, no G1 rerun or new allowance. |
| Preservation | Correct-base hash checks:12326 R01 archive files,916 source dependencies,900 old frozen members,0mismatches. Old outcomes/unknowns/negative scores remain. |

The first archive verifier mistakenly resolved audit-relative entries against the
repository, reporting12326 missing paths. This was a verifier path-base error,
not evidence of deleted files. The mistake and corrected checks are retained in
protected-verification.json; correction was hash inspection only. The initial
seal also compared the semantic ls-files baseline hash to raw .git/index bytes,
failing before any seal/source/doc outputs. Original semantic hashes match.
index-verification-correction.json corrects the earlier mistaken raw-drift
interpretation; the failed script/record are retained. No index reset/rewrite.

`supervision.py` and `release.py` are byte-identical to R01. New changes are zero
count admission, fixed stdlib HTTPS, persistent reservation/settlement accounting,
explicit method/cost/user-confirmation gates and provider JSON retention. Parent
window remains3600s including cleanup; local onepass<=12compile/990replay/204444
cycles,0newDUT/native/setup/version jobs. Actual supervisor, network and SV paths
are unexercised in this preparation. No hard realtime or detached-child census
claim. Unknown cache/reasoning subsets do not become zero cost.

Old benchmark inputs are published. The Claude reference and GPT candidate roles,
all raw12/N10/38oracleunknown and scoring semantics remain unchanged. No hidden
evaluation data/reference enters provider inputs; the maintainer dependency
manifest is not a candidate packet. No placebo is registered, so a later B/C
comparison concerns the whole feedback package and one session per arm only.
This preparation establishes neither monitor correctness nor an E-graph benefit.

See phase.json and checks-and-deltas.json for exact source and evidence paths;
source-manifest.json binds execution dependencies. The preparation manifest binds
the saved source/evidence copies. Review-prompt.md lists exact review and EXECUTE
identities. API remains fail-closed until both exist. The staged key is retained
and must not be requested repeatedly or read during review. Old R01 stays sealed.
'''
    with (HERE/'report.md').open('x') as stream:stream.write(report)

    for path in [*SOURCE.glob('*'),REG]:
        if path.is_file():copy(path,HERE/'snapshot'/path.relative_to(ROOT))
    for key in ['financial_policy','method_addendum','cost_basis','original_authorization','user_zero_count_confirmation']:
        path=ROOT/reg[key];copy(path,HERE/'snapshot'/path.relative_to(ROOT))
    for path in PREP.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:copy(path,HERE/'evidence'/path.relative_to(PREP))
    members={str(path.relative_to(HERE)):sha(path) for path in HERE.rglob('*') if path.is_file() and '__pycache__' not in path.parts}
    write(HERE/'snapshot-manifest.json',dict(status='PREPARED_PENDING_EXACT_PRECHECK_EXECUTE',files=dict(sorted(members.items())),file_count=len(members),path_base='This manifest parent',excluded=['snapshot-manifest.json(selfhash)','__pycache__','All credential/environment/cache files','No duplicate copy of immutable old130MB dependencies'],scope='R02source/evidence and additive doc snapshots;old dependency bytes reused by hash,not experiments rerun'))
    assert index_entries_sha()==baseline['index_sha256']
    result=dict(phase_sha256=sha(HERE/'phase.json'),preparation_manifest_sha256=sha(HERE/'snapshot-manifest.json'),source_manifest_sha256=sha(source_manifest),registration_sha256=sha(REG),files=len(members),status=phase['status'])
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
