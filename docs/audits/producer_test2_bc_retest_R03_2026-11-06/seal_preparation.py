"""Seal only the narrow P18-R1 repair, with old sealed evidence reused."""
from pathlib import Path
import ast,hashlib,json,shutil,subprocess,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
SOURCE=ROOT/'test2/retest_v3';REG=ROOT/'test2/configs/controller_done_bc_retest_v3.json'
RESULT=ROOT/'test2/results/controller-done-bc-retest-preparation-v3'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as stream:stream.write(json.dumps(value,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def copy(path,dest):
    dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists(),dest;shutil.copy2(path,dest)

def main():
    assert not (HERE/'snapshot-manifest.json').exists(),'ALREADY_SEALED'
    before=load(HERE/'before.json');reg=load(REG);oldreg=load(ROOT/'test2/configs/controller_done_bc_retest_v2.json')
    assert git('rev-parse','HEAD').decode().strip()==before['HEAD']
    assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==before['index_entries_sha256']
    assert not git('diff','--cached','--name-only')
    for path,digest in before['protected'].items():assert sha(ROOT/path)==digest,path
    for name,digest in before['R02_source'].items():assert sha(ROOT/'test2/retest_v2'/name)==digest,name
    for version in [1,2,3]:
        for suffix in ['', '-supervision']:assert not (ROOT/f'test2/results/controller-done-bc-retest-v{version}{suffix}').exists()
    assert sha(HERE/'prior-P18-R02-review.json')=='380dc2deabf0a8972d5c1db46b0475ab8a1b0c241b89ff66657f329e31a36d9b'
    assert sha(HERE/'prior-P18-missing-tier.input.json')=='cebd20c71be9b5b0d3b0acf7a002761d0f526f61aeda5f26f73f700c33c6a97f'
    probes=load(RESULT/'tier-probes-attempt1/summary.json');assert (probes['tests'],probes['failures'],probes['errors'])==(4,0,0)
    for path,digest in probes['executed_source_sha256'].items():assert sha(ROOT/path)==digest,path
    changes={}
    for name in ['resources.py','api.py','gates.py','pipeline.py','cli.py','release.py','supervision.py']:
        old=ROOT/'test2/retest_v2'/name;new=SOURCE/name;actual=new.read_text()
        expected=old.read_text().replace('controller_done_bc_retest_v2.json','controller_done_bc_retest_v3.json').replace('BC_RETEST_EXECUTE_V2','BC_RETEST_EXECUTE_V3').replace('BC_RETEST_V2_EXACT_PRECHECK','BC_RETEST_V3_EXACT_PRECHECK')
        if name=='resources.py':expected=expected.replace("record.get('returned_service_tier') in [None,'default']","record.get('returned_service_tier')=='default'")
        assert actual==expected,name;ast.parse(actual)
        changes[name]=dict(R02_sha256=sha(old),R03_sha256=sha(new),byte_identical=sha(old)==sha(new),allowed_delta='Strict returned tier equality only' if name=='resources.py' else 'Mechanical registration/review/EXECUTE version reference,or identical')
    allowed_reg_keys={'id','status','run_root','source_manifest','preparation_manifest','repair_of'}
    assert {k:v for k,v in reg.items() if k not in allowed_reg_keys}=={k:v for k,v in oldreg.items() if k not in allowed_reg_keys}
    oldmembers=load(ROOT/'test2/retest_v2/source-manifest.json')['files']
    assert all(sha(ROOT/path)==digest for path,digest in oldmembers.items())
    oldsnapshot=ROOT/'docs/audits/producer_test2_bc_retest_R02_2026-11-06/snapshot-manifest.json'
    members=load(oldsnapshot)['files'];assert all(sha(oldsnapshot.parent/path)==digest for path,digest in members.items())
    write(HERE/'delta-verification.json',dict(status='PASS',runtime_files=changes,registration_changed_keys=sorted(k for k in set(oldreg)|set(reg) if oldreg.get(k)!=reg.get(k)),only_functional_change='Require explicit returned tier default',R02_source_dependencies_verified=len(oldmembers),R02_sealed_members_verified=len(members),mismatch_count=0,prior_counterexample_and_review_preserved=True,probes=probes,base_suites_and_G1_rerun=False,actual_API_network_key_SV_process_signal=0))

    # Bind a preserved old reviewer record, not the filename used by a later review.
    files=dict(oldmembers)
    additions=[*SOURCE.glob('*.py'),SOURCE/'README.md',REG,Path(__file__),HERE/'before.json',HERE/'delta-verification.json',HERE/'review-prompt.md',HERE/'prior-P18-R02-review.json',HERE/'prior-P18-missing-tier.input.json',ROOT/'test2/retest_v2/source-manifest.json',oldsnapshot,ROOT/'docs/audits/producer_test2_bc_retest_R02_2026-11-06/phase.json',RESULT/'tier-probes-attempt1/summary.json']
    for path in additions:
        name=path.relative_to(ROOT).as_posix();assert 'build/private/' not in name;files[name]=sha(path)
    assert 'docs/audits/agent_bridge_2026-11-06/P18_bc_retest_preflight/review.json' not in files
    manifest=SOURCE/'source-manifest.json'
    write(manifest,dict(status='P18_R1_REPAIR_PREPARED_PENDING_DELTA_PRECHECK_EXECUTE',files=dict(sorted(files.items())),credentials_excluded=True,shared_mutable_docs_excluded=True,scope='Maintainer execution/grading dependencies,not candidate prompt inputs',base_evidence='R02 and prior P18 checks reused where identical,no base/G1/fullmock rerun',prior_review='Preserved prior-P18-R02-review.json;mutable upstream review path excluded'))

    header='''
## Current same-IP B/C retest — R03 tier repair prepared, pending P18 delta (2026-11-06)

P18 returned CHANGES_REQUIRED on sealed R02: P18-R1 found that a missing/null
returned service tier could qualify and settle its reservation. This was a
synthetic counterexample, not an actual API incident or proof of overspending.
R02, its counterexample and old scores remain unchanged. A verbatim prior review
copy is retained under the new R03 audit, separate from later reviewer records.

New `test2/retest_v3/` and `test2/configs/controller_done_bc_retest_v3.json` require
explicit returned tier'default'. Missing/null/nondefault now halt before candidate
acceptance/compile/next request, preserve provider JSON and the full USD5.910168
reservation, and have no SETTLE journal. Explicit default64000/8192 still settles
the USD0.487168 conservative upper, not an invoice/refund. Four new narrow probes
PASS,0fail/0error,0.175137584s. They are synthetic caller/settlement checks, not
new model samples, real compilation or scientific scores. R01/R02 base18+1/full
mock/G1 were not rerun. All runtime changes apart from tier equality are mechanical
namespace references; release/supervision are byte-identical to R02.

Zero remote counts/local ESTIMATE64k, model/settings, USD20/max12/output8192/3600s,
singlepass12compile/990monitorreplays/204444cycles and same published benchmark
B/C1sessionx3rounds remain unchanged. No DUT/native/physics/formal/G1 allowance,
new hidden set, placebo or C benefit is implied. Claude reference, fixed stimuli,
raw12/N10/38unknown and all historical failures remain unchanged.

Exact phase/report/source/delta/review prompt and snapshot manifest:
`docs/audits/producer_test2_bc_retest_R03_2026-11-06/`. Existing P18 must accept
the exact R03 hashes, then root issues BC_RETEST_EXECUTE_V3 for the one new run
root. No live action occurs during this preparation. Key retained, no new key or
budget request; API/network/keycontent/SV/supervisedprocess0, no install/commit/
push. Actual HEAD2de33e981d2fffc9739d2ca049fbae1774de1aad, staged entries unchanged,
new work uncommitted/unpushed. Older complete document bodies follow unchanged.
'''
    shared={}
    for name in ['HANDOFF.md','PROJECT_STATUS.md']:
        path=ROOT/'docs'/name;old=path.read_bytes();copy(path,HERE/'before/docs'/name)
        first,rest=old.split(b'\n',1);assert sha(path)==hashlib.sha256(old).hexdigest()
        path.write_bytes(first+b'\n'+header.encode()+b'\n'+rest);copy(path,HERE/'snapshot/docs'/name)
        shared[name]=dict(before_sha256=hashlib.sha256(old).hexdigest(),after_sha256=sha(path),entire_old_body_retained=path.read_bytes().endswith(rest))
    phase=dict(phase='BC_RETEST_R03_P18_R1_TIER_REPAIR',status='PREPARED_PENDING_EXACT_P18_DELTA_PRECHECK_AND_ROOT_EXECUTE',actual_HEAD=before['HEAD'],registration=str(REG.relative_to(ROOT)),registration_sha256=sha(REG),source_manifest=str(manifest.relative_to(ROOT)),source_manifest_sha256=sha(manifest),preparation_manifest=str((HERE/'snapshot-manifest.json').relative_to(ROOT)),repair='P18-R1 explicit returned tier default',prior_R02_review_status='CHANGES_REQUIRED',prior_R02_review=str((HERE/'prior-P18-R02-review.json').relative_to(ROOT)),prior_R02_review_sha256=sha(HERE/'prior-P18-R02-review.json'),tests=dict(cases=4,failures=0,errors=0,seconds=probes['seconds'],scope=probes['scope']),base_suites_and_G1_rerun=False,only_behavior_change='Tighten returned_service_tier None/default membership to explicit default equality',unrelated_old_configuration_and_evidence_unchanged=True,normal_generations=6,max_generations=12,remote_counts=0,API_ceiling_micro_usd=20000000,per_dispatch_full_reserve_micro_usd=5910168,explicit_default_64000_8192_upper_micro_usd=487168,invalid_tier_settlement_events=0,local_pass_caps=reg['local'],total_wall_seconds=3600,API_network_keycontent_SV_process_signal_calls=0,credential_retained=True,credential_content_read_or_hashed=False,actual_invoice_usd=None,independent_delta_precheck=None,EXECUTE=None,live_root_exists=False,index_entries_unchanged=True,shared_document_additions=shared,offline_preparation_elapsed_seconds=time.time()-before['started_epoch'],next='P18_EXACT_DELTA_REVIEW_THEN_ROOT_EXECUTE_V3_BEFORE_ONE_NEW_STAGE')
    for key in ['financial_policy','cost_basis','method_addendum','user_zero_count_confirmation']:
        phase[key]=reg[key];phase[key+'_sha256']=reg[key+'_sha256']
    write(HERE/'phase.json',phase)
    report='''# R03 P18-R1 repair — live not executed

R03 fixes the sole material finding in the exact R02 review: returned tier must
be explicitly default. Missing/null/other tiers no longer qualify or settle.
The R02 CHANGES_REQUIRED review and its null-tier counterexample are retained,
including verbatim copies in this directory. No real API/overspend was observed.

| New narrow probe | Result |
|---|---|
| Missing service_tier field | Halt before candidate acceptance/compile/next request; raw JSON retained;5910168microUSD reserve;0SETTLE |
| Explicit null tier | Same refusal and full reservation retention; null remains distinguishable from missing in raw provider JSON |
| Nondefault flex tier | Same refusal and full reservation retention |
| Explicit default,64000input/8192output | Qualifies response/settles487168microUSD upper;unused5423000released;not invoice/refund or SV correctness |

Four new probes PASS/0fail/0error,0.175137584s. Rejected caller paths retain six
NOT_RUN snapshots and972unresolved metadata records without compiler/monitor
replay or scientific grading. These are fixtures, not live model samples.
No18+1/full mock/G1/base suite was rerun. The executed-source copies match final
runtime/probe source and registration. Mechanical comparison permits only new
registration/review/EXECUTE namespaces plus the strict tier equality. Release
and supervision remain byte-identical. R02's203sealedmembers/943dependencies are
hash-verified unchanged; no old score, failure, unknown or denominator is edited.

All other method/finance/runtime limits remain: fixed B/raw and C/raw+E-graph,
one independent session/arm x3rounds on the old published benchmark; zero remote
counts; local64k ESTIMATE and actual-response qualification threshold; output8192,
max12generations,20USD API ceiling,5910168microUSD full-context dispatch reserve,
total3600s including cleanup. Same local onepass12compile/990replays/204444cycles,
0newDUT/native/setup/formal/G1/crossIP. The Claude oracle, stimulus, monitor ABI,
raw12/N10/38unknown and all prior outcomes remain. No new hidden study, placebo,
E-graph benefit, actual transport/timing/billing or hard realtime proof is claimed.

Preparation made0API/network/auth/keycontent/SV/supervisedprocess calls, with no
installation, commit or push. Key stays staged; no new budget/key is requested.
The source manifest includes the preserved prior-review snapshot, not the mutable
P18 current reviewer filename. Read phase.json,delta-verification.json and the
review prompt for exact hashes and scope. Only an accepted exact R03 delta review
plus root BC_RETEST_EXECUTE_V3 can enable the one new live root. R02 cannot run.
'''
    with (HERE/'report.md').open('x') as stream:stream.write(report)
    for path in [*SOURCE.glob('*'),REG]:
        if path.is_file():copy(path,HERE/'snapshot'/path.relative_to(ROOT))
    for path in RESULT.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:copy(path,HERE/'evidence'/path.relative_to(RESULT))
    members={p.relative_to(HERE).as_posix():sha(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    write(HERE/'snapshot-manifest.json',dict(status='R03_REPAIR_PREPARED_PENDING_P18_DELTA_EXECUTE',files=dict(sorted(members.items())),file_count=len(members),path_base='This manifest parent',excluded=['snapshot-manifest.json(selfhash)','Credentials/environment/cache','No duplicate old immutable dependency tree'],scope='Narrow P18-R1 newsource/probes/additive docs;not live results'))
    assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==before['index_entries_sha256']
    print(json.dumps(dict(status=phase['status'],registration_sha256=sha(REG),source_manifest_sha256=sha(manifest),preparation_manifest_sha256=sha(HERE/'snapshot-manifest.json'),phase_sha256=sha(HERE/'phase.json'),source_members=len(files),preparation_members=len(members)),indent=2))

if __name__=='__main__':main()
