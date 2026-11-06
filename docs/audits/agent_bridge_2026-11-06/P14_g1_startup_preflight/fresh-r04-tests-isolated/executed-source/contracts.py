"""Finite G1 registration contract, not a general JSON Schema engine."""
from collections import Counter
from observations import need


def registration_contract(reg, grant, plan):
    mapping = {'compile_jobs': 'compilation_jobs_total',
        'native_jobs': 'native_BMC_cover_jobs_total',
        'physical_jobs': 'physical_simulator_runs_total',
        'physical_cycles': 'physical_cycles_total',
        'cycles_per_run': 'physical_cycles_per_run_max',
        'wall_seconds': 'execution_wall_seconds_total',
        'compile_timeout': 'compilation_job_timeout_seconds',
        'native_timeout': 'native_job_timeout_seconds',
        'physical_timeout': 'physical_run_timeout_seconds'}
    need(reg['profile'] == 'G1_PUBLIC_SINGLE_PROFILE_V1', 'PROFILE')
    for local, authorized in mapping.items():
        value = reg['caps'][local]
        need(type(value) is int and 0 < value <= grant['caps'][authorized], 'GRANT_CAP:' + local)
    need(reg['native_depth'] == grant['caps']['native_depth'] == 8, 'DEPTH_MUST_BE_EIGHT')
    jobs = plan['jobs']
    need(len({j['id'] for j in jobs}) == len(jobs), 'DUPLICATE_PLAN_JOB')
    counts = Counter(j['kind'] for j in jobs)
    need(counts == {'setup': 8, 'compile': 18, 'native': 32, 'physical': 32}, 'JOB_PLAN_COUNTS')
    for kind in ['setup', 'compile', 'native', 'physical']:
        need(counts[kind] <= reg['caps'][kind + '_jobs'], 'PLANNED_JOB_CAP')
    need(sum(j.get('cycles', 0) for j in jobs) == 128, 'PHYSICAL_RESERVED_CYCLES')
    for n in range(16):
        cid = f'QC{n:02}'
        native = [j for j in jobs if j.get('qc') == cid and j['kind'] == 'native']
        physical = [j for j in jobs if j.get('qc') == cid and j['kind'] == 'physical']
        need([j['mode'] for j in native] == ['bmc', 'cover'], 'NO_PROVE_OR_RETRY')
        need([j['simulator'] for j in physical] == ['icarus', 'verilator'], 'DUAL_SIM_REQUIRED')
        for j in native:
            need(j['argv'][j['argv'].index('-t') + 1] == '8', 'JOB_DEPTH')
        need(all(j['cycles'] == 4 for j in physical), 'REGISTERED_FOUR_CYCLES')
    need(all(reg[key] is False for key in ['API', 'count', 'generation',
        'key_access', 'network', 'installation', 'G2_G3_G4_G5']), 'FORBIDDEN_STAGE_FLAG')
