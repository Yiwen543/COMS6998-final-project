"""R03 registration/gate contracts; R01 contract remains an unchanged reference."""
from collections import Counter
from observations import need
from allocation import DECISION_SHA, POOL_SHA, load_allocation


def registration_contract(root, reg, grant, plan):
    allocation = load_allocation(root, reg)
    mapping = {'compile_jobs': 'compilation_jobs_total', 'native_jobs': 'native_BMC_cover_jobs_total',
        'physical_jobs': 'physical_simulator_runs_total', 'physical_cycles': 'physical_cycles_total',
        'cycles_per_run': 'physical_cycles_per_run_max', 'wall_seconds': 'execution_wall_seconds_total',
        'compile_timeout': 'compilation_job_timeout_seconds', 'native_timeout': 'native_job_timeout_seconds',
        'physical_timeout': 'physical_run_timeout_seconds'}
    for local, authorized in mapping.items():
        need(type(reg['caps'][local]) is int and 0 < reg['caps'][local] <= grant['caps'][authorized],
             'CUMULATIVE_GRANT_CAP:' + local)
    need(reg['profile'] == 'G1_PUBLIC_SINGLE_PROFILE_V1' and reg['native_depth'] == 8, 'PROFILE_DEPTH')
    jobs = plan['jobs']
    need(len({j['id'] for j in jobs}) == len(jobs), 'DUPLICATE_PLAN_JOB')
    counts = Counter(j['kind'] for j in jobs)
    need(counts == {'setup': 7, 'compile': 18, 'native': 32, 'physical': 32}, 'CONTINUATION_JOB_COUNTS')
    need(all(j['id'] != 'setup-make' for j in jobs), 'MAKE_VERSION_NOT_REPROBED')
    for kind in ['setup', 'compile', 'native', 'physical']:
        need(counts[kind] <= reg['remaining_allocation'][kind + '_jobs'], 'REMAINING_JOB_CAP')
    need(sum(j.get('cycles', 0) for j in jobs) == 128, 'PHYSICAL_RESERVED_CYCLES')
    for n in range(16):
        cid = f'QC{n:02}'
        native = [j for j in jobs if j.get('qc') == cid and j['kind'] == 'native']
        physical = [j for j in jobs if j.get('qc') == cid and j['kind'] == 'physical']
        need([j['mode'] for j in native] == ['bmc', 'cover'], 'NO_PROVE_OR_EXTRA_RETRY')
        need([j['simulator'] for j in physical] == ['icarus', 'verilator'], 'DUAL_SIM_REQUIRED')
        need(all(j['argv'][j['argv'].index('-t') + 1] == '8' for j in native), 'DEPTH_EIGHT')
        need(all(j['cycles'] == 4 for j in physical), 'REGISTERED_FOUR_CYCLES')
    need(all(reg[k] is False for k in ['API', 'count', 'generation', 'key_access',
         'network', 'installation', 'G2_G3_G4_G5']), 'FORBIDDEN_SCOPE')
    return allocation


def gate_contract(gate, review, identities):
    required = ['record_kind', 'stage', 'registration_sha256', 'source_manifest_sha256',
        'user_authorization_sha256', 'preparation_manifest_sha256',
        'continuation_decision_sha256', 'predecessor_pool_sha256']
    need(all(k in gate for k in required), 'MISSING_CONTINUATION_RECEIPT_FIELD')
    need(gate['record_kind'] == 'G1_EXECUTE_CONTINUATION_AFTER_P12' and gate['stage'] == 'EXECUTE',
         'OLD_OR_WRONG_EXECUTE_RECEIPT')
    need(review['status'] in ['PASS', 'PASS_WITH_LIMITS'] and review['phase'].startswith('P12'),
         'P12_ACCEPTANCE_REQUIRED')
    for key in required[2:]:
        need(gate[key] == identities[key], 'GATE_IDENTITY_DRIFT:' + key)
    need(gate['continuation_decision_sha256'] == DECISION_SHA and gate['predecessor_pool_sha256'] == POOL_SHA,
         'WRONG_CONTINUATION_LINEAGE')
    need(review['input_identity']['producer_manifest_sha256'] == identities['preparation_manifest_sha256'] and
         review['input_identity']['registration_sha256'] == identities['registration_sha256'] and
         review['input_identity']['continuation_decision_sha256'] == DECISION_SHA, 'P12_WRONG_INPUTS')
