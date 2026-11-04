"""Credential-free independent controls for the Claude-authored READB checker."""
import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from run_midterm_fixed import sha
from run_spi_checker_author import validate_source
from independent_i2c_read_controls import controls


def worker(candidate, base, out):
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    auth = json.loads((candidate/'authorship.json').read_text())
    for name, digest in auth['artifact_sha256'].items():
        if sha(candidate/name) != digest:
            raise ValueError('Checker authorship hash drift')
    def module(path):
        source = path.read_text(); validate_source(source); ns = {}
        exec(compile(source, str(path), 'exec'), ns)
        return ns
    check = module(candidate/'checker.py')['check_rows']
    try:
        selftests = module(candidate/'selftest.py')['run'](check)
    except Exception as e:
        selftests = {'error_type': type(e).__name__, 'detail': str(e)}
    cases = controls()
    for path in sorted((base/'driver-v2').glob('*.trace.json')):
        cases['dut_'+path.name.split('.')[0]] = json.loads(path.read_text())
    event_cases = []
    for name, family in [('multi_read','multi_byte_read'), ('rcont_chain','rcont_chain'),
                         ('read_restart','read_then_restart'), ('read_stretch','read_stretch_recovery')]:
        for prefix in ['', 'dut_']:
            good = prefix+name
            bad = copy.deepcopy(cases[good])
            next(r for r in bad if r['pre']['rx_valid'])['pre']['rx_data'] ^= 1
            fault = 'corrupt_first_rx_'+good; cases[fault] = bad
            event_cases.append({'name': fault, 'baseline': good, 'family': family})
    results = {}
    for name, rows in cases.items():
        try: results[name] = check(rows)
        except Exception as e: results[name] = {'verdict':'checker_exception','exception':type(e).__name__, 'detail':str(e)}
    clean = lambda r: r.get('verdict') == 'pass' and not r.get('failures') and not r.get('assumption_violations')
    for item in event_cases:
        good, bad = results[item['baseline']], results[item['name']]
        item.update(baseline_clean=clean(good),
            baseline_event=any(e.get('kind') == 'success' and e.get('family') == item['family'] for e in good.get('events',[])),
            failure_detected=bool(bad.get('failures')),
            success_rejected=not any(e.get('kind') == 'success' and e.get('family') == item['family'] for e in bad.get('events',[])))
        item['credited_detection'] = item['baseline_clean'] and item['failure_detected'] and item['success_rejected']
    result = {'checker_sha256':sha(candidate/'checker.py'), 'author_selftests':selftests,
              'cases':results, 'event_controls':event_cases,
              'negative_controls':{n:{'failure_detected':bool(results[n].get('failures')),
                  'baseline':baseline,'baseline_clean':clean(results[baseline]),
                  'credited_detection':clean(results[baseline]) and bool(results[n].get('failures'))}
                  for n,baseline in [('rx_corrupt','ordinary_read'),('rx_duplicate','ordinary_read'),
                     ('rx_missing','ordinary_read'),('wrong_boundary_ack','rcont_chain'),('premature_pop','ordinary_read')]},
              'trace_inputs':{p.name:sha(p) for p in sorted((base/'driver-v2').glob('*.trace.json'))},
              'pending_controls':{n:results[n].get('verdict') == 'pending' for n in
                  ['zero_partial','truncated_read','dut_zero_count_partial']}}
    out.mkdir(parents=True, exist_ok=False)
    (out/'evaluator-source.py').write_bytes(Path(__file__).read_bytes())
    (out/'control-generator-source.py').write_bytes(Path(__file__).with_name('independent_i2c_read_controls.py').read_bytes())
    (out/'evaluation.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'private-controls.json').write_text(json.dumps({n:r for n,r in cases.items() if not n.startswith('dut_')},indent=2)+'\n')
    print(json.dumps({'selftests':selftests,'verdicts':{n:r.get('verdict') for n,r in results.items()},
                      'negative_controls':result['negative_controls'], 'pending_controls':result['pending_controls']}))


def evaluate(candidate, base, out):
    env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ('KEY','TOKEN','SECRET','CREDENTIAL','PASSWORD'))}
    script=Path(__file__).resolve()
    with tempfile.TemporaryDirectory(prefix='i2c-read-controls-') as cwd:
        code='import sys;sys.path.insert(0,'+repr(str(script.parent))+');from evaluate_i2c_read_checker import worker;from pathlib import Path;worker(*map(Path,sys.argv[1:]))'
        p=subprocess.run([sys.executable,'-I','-c',code,str(candidate),str(base),str(out)],
                         cwd=cwd,env=env,text=True,capture_output=True,timeout=60)
    if p.returncode: raise RuntimeError(p.stderr)
    return p.stdout


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['candidate','base','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();print(evaluate(a.candidate.resolve(),a.base.resolve(),a.output.resolve()))
