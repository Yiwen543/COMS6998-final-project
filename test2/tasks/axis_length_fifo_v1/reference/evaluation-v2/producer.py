#!/usr/bin/env python3
"""Run a Claude-authored pure reference on fixed rows; no GPT replacement oracle."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
from common import ROOT, BASE, dump, sha
from run_spi_checker_author import validate_source
from controller_prepare import OUTPUTS

TASK = BASE / 'tasks/axis_length_fifo_v1'


def finite_fixture(inputs, outputs, status):
    # Explicit finite examples only. No arbitrary-trace expected-state evaluator.
    zero = dict(zip(OUTPUTS, [1, 0, 0, 0, 0, 0, 0, 0, 0]))
    rows = []
    previous = dict(zero)
    def append(inp, post):
        nonlocal previous
        rows.append({'cycle': len(rows), 'inputs': inp, 'pre': dict(previous), 'post': dict(post)})
        previous = dict(post)
    def inp(**kw):
        return {**dict(rst=0, s_valid=0, s_data=0, s_last=0, m_ready=1, h_ready=1), **kw}
    append(inp(rst=1), zero)
    append(inp(rst=1), zero)
    for i, byte in enumerate(inputs):
        post = dict(zero)
        if i == len(inputs)-1:
            post.update(m_valid=1, m_data=outputs[0], m_last=int(len(outputs)==1),
                        h_valid=1, h_pad=status[0], h_truncate=status[1],
                        h_length=status[2], h_original_length=status[3])
        append(inp(s_valid=1, s_data=byte, s_last=int(i==len(inputs)-1)), post)
    for i in range(len(outputs)):
        post = dict(zero)
        if i+1 < len(outputs):
            post.update(m_valid=1, m_data=outputs[i+1], m_last=int(i+2==len(outputs)))
        append(inp(), post)
    for _ in range(32):
        append(inp(), zero)
    return rows


def controls():
    exact = finite_fixture([11, 22, 33, 44], [11, 22, 33, 44], (0, 0, 4, 4))
    pad = finite_fixture([17], [17, 0, 0, 0], (1, 0, 4, 1))
    truncate = finite_fixture(list(range(10)), list(range(8)), (0, 1, 8, 10))
    result = {name: {'rows': rows, 'expected_verdict': 'PASS', 'require_drained': True}
              for name, rows in [('legal_exact', exact), ('legal_pad', pad), ('legal_truncate', truncate)]}
    bad = copy.deepcopy(exact)
    bad[5]['post']['m_data'] = 99
    bad[6]['pre']['m_data'] = 99
    result['wrong_payload'] = dict(rows=bad, expected_verdict='FAIL', require_drained=True)
    bad = copy.deepcopy(pad)
    bad[2]['post']['h_length'] = 5
    bad[3]['pre']['h_length'] = 5
    result['wrong_status'] = dict(rows=bad, expected_verdict='FAIL', require_drained=True)
    unknown = copy.deepcopy(exact)
    unknown[5]['post']['m_data'] = -1
    unknown[6]['pre']['m_data'] = -1
    result['unknown_payload'] = dict(rows=unknown, expected_verdict='UNRESOLVED', require_drained=True)
    malformed = copy.deepcopy(exact)
    del malformed[3]['post']['m_valid']
    result['missing_field'] = dict(rows=malformed, expected_verdict='INVALID_INPUT', require_drained=True)
    start = 6  # first output-consumption row in the explicit four-byte example
    stall = copy.deepcopy(exact)
    held = copy.deepcopy(stall[start])
    held['inputs'].update(m_ready=0, h_ready=0)
    held['post'] = dict(held['pre'])
    stall.insert(start, held)
    result['legal_both_stalled'] = dict(rows=stall, expected_verdict='PASS', require_drained=True)
    late = copy.deepcopy(exact)
    status_keys = ['h_valid', 'h_pad', 'h_truncate', 'h_length', 'h_original_length']
    header = {k: exact[start]['pre'][k] for k in status_keys}
    for i in range(start, start+6):
        late[i]['inputs']['h_ready'] = 0
        late[i]['pre'].update(header)
        late[i]['post'].update(header)
    late[start+6]['pre'].update(header)
    # Preserve the specified32-cycle quiet tail after extending status pressure.
    late += [copy.deepcopy(late[-1]), copy.deepcopy(late[-1])]
    result['legal_status_after_data'] = dict(rows=late, expected_verdict='PASS', require_drained=True)
    early = copy.deepcopy(exact)
    held = copy.deepcopy(early[start])
    held['inputs']['m_ready'] = 0
    held['post'] = dict(held['pre'])
    held['post']['h_valid'] = 0
    early[start]['pre']['h_valid'] = 0
    early.insert(start, held)
    result['legal_status_before_data'] = dict(rows=early, expected_verdict='PASS', require_drained=True)
    reset = copy.deepcopy(exact[:start])
    r = copy.deepcopy(exact[start])
    r['inputs'].update(rst=1, s_valid=0)
    r['post'] = dict(exact[0]['post'])
    reset.append(r)
    for _ in range(32):
        reset.append(dict(cycle=0, inputs=dict(exact[-1]['inputs']), pre=dict(r['post']), post=dict(r['post'])))
    result['legal_reset_cancels_responses'] = dict(rows=reset, expected_verdict='PASS', require_drained=True)
    bad_input = copy.deepcopy(exact)
    bad_input[3]['pre']['s_ready'] = 0
    result['source_changes_while_blocked'] = dict(rows=bad_input, expected_verdict='INVALID_INPUT', require_drained=True)
    fail_unknown = copy.deepcopy(result['wrong_payload']['rows'])
    fail_unknown[5]['post']['h_length'] = -1
    fail_unknown[6]['pre']['h_length'] = -1
    result['definite_failure_plus_unknown'] = dict(rows=fail_unknown, expected_verdict='FAIL', require_drained=True)
    extra = copy.deepcopy(exact)
    extra[-2]['post'].update(header)
    extra[-1]['pre'].update(header)
    result['extra_status'] = dict(rows=extra, expected_verdict='FAIL', require_drained=True)
    gap = copy.deepcopy(exact)
    gap[3]['cycle'] = 900
    result['cycle_gap'] = dict(rows=gap, expected_verdict='INVALID_INPUT', require_drained=True)
    for name, control in result.items():
        if name == 'cycle_gap':
            continue
        for i, row in enumerate(control['rows']):
            row['cycle'] = i
    return result


def alignment_controls():
    result = controls()
    for channel in ('data', 'status'):
        rows = finite_fixture([], [], (0, 0, 0, 0))
        rows += [copy.deepcopy(rows[-1]), copy.deepcopy(rows[-1])]
        rows[3]['inputs']['rst'] = 1
        if channel == 'data':
            rows[2]['inputs']['m_ready'] = 0
            rows[2]['pre'].update(m_valid=1, m_data=91, m_last=1)
            rows[2]['post'].update(m_valid=1, m_data=91, m_last=1)
            rows[3]['pre'].update(m_valid=1, m_data=91, m_last=1)
        else:
            rows[2]['inputs']['h_ready'] = 0
            header = dict(h_valid=1, h_pad=1, h_truncate=0, h_length=4, h_original_length=1)
            rows[2]['pre'].update(header)
            rows[2]['post'].update(header)
            rows[3]['pre'].update(header)
        result['spurious_stalled_'+channel+'_then_reset'] = dict(rows=rows, expected_verdict='FAIL', require_drained=True)
    rows = finite_fixture([17], [17, 0, 0, 0], (1, 0, 4, 1))
    rows[2]['pre'].update(m_valid=1, m_data=17, m_last=0)
    result['pre_not_justified_by_current_input'] = dict(rows=rows, expected_verdict='FAIL', require_drained=True)
    rows = finite_fixture([11, 22, 33, 44], [11, 22, 33, 44], (0, 0, 4, 4))
    result['final_tail_32_not_128'] = dict(rows=copy.deepcopy(rows), expected_verdict='UNRESOLVED', require_drained=True, min_tail=128)
    rows += [copy.deepcopy(rows[-1]) for _ in range(96)]
    result['final_tail_128'] = dict(rows=rows, expected_verdict='PASS', require_drained=True, min_tail=128)
    for name, c in result.items():
        if name != 'cycle_gap':
            for i, row in enumerate(c['rows']):
                row['cycle'] = i
    return result


def module(path, name):
    validate_source(path.read_text())
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def evaluate(candidate, out, contract_v2=False):
    out.mkdir(parents=True, exist_ok=False)
    checker = module(candidate / 'checker.py', 'controller_claude_checker')
    selftest = module(candidate / 'selftest.py', 'controller_claude_selftest')
    selftests = selftest.run(checker)
    fixtures = alignment_controls() if contract_v2 else controls()
    dump(TASK / 'private' / ('reference-controls-v3.json' if contract_v2 else 'reference-controls-v2.json'), fixtures)
    reports = {}
    for name, c in fixtures.items():
        kwargs = {'min_tail': c.get('min_tail', 32)} if contract_v2 else {}
        reports['control/'+name] = checker.check_rows(c['rows'], require_drained=c['require_drained'], **kwargs)
    paths = list((TASK / 'qualification/observations-v2').glob('*/*/rows.json'))
    paths += list((TASK / 'private/observations').glob('*/*/rows.json'))
    paths += list((TASK / 'private/mutant-observations-v1').glob('*/*/*/rows.json'))
    for path in paths:
        key = str(path.relative_to(TASK))
        kwargs = {'min_tail': 128 if key.startswith('private/') else 32} if contract_v2 else {}
        reports[key] = checker.check_rows(json.loads(path.read_text()), require_drained=True, **kwargs)
    dump(out / 'evaluations.json', {'selftests': selftests, 'cases': reports,
         'checker_sha256': sha(candidate / 'checker.py')})
    control_ok = all(reports['control/'+n]['verdict'] == c['expected_verdict'] for n, c in fixtures.items())
    baseline = {k: v['verdict'] for k, v in reports.items() if not k.startswith('control/') and
                'mutant-observations' not in k}
    summary = {'status': 'evaluated_not_independently_reviewed', 'selftests': selftests,
               'finite_controls_match': control_ok, 'baseline_verdicts': baseline,
               'cases': len(reports), 'live_allowed': False}
    dump(out / 'summary.json', summary)
    print(json.dumps(summary, indent=2))
    payload = {'specification': (TASK / 'public' / ('specification_v2.md' if contract_v2 else 'specification.md')).read_text(),
               'interface': (TASK / 'public' / ('observer_contract_v2.md' if contract_v2 else 'observer_contract.md')).read_text(),
               'checker_source': (candidate / 'checker.py').read_text(),
               'selftest_source': (candidate / 'selftest.py').read_text(),
               'contract': (candidate / 'contract.md').read_text(), 'selftest_results': selftests,
               'independent_complete_controls': {name: {**c, 'actual_result': reports['control/'+name]} for name, c in fixtures.items()},
               'simulation_summary': summary,
               'limits': ['Finite examples/local formal checks do not prove full checker soundness.',
                          'No DUT source, hidden mutation sites, final trajectories or candidate outcomes supplied.',
                          'Reject if accepted-prefix, independent-channel, reset-epoch or unknown precedence checks are unsound.']}
    text = '''Independently review this Claude-authored reference against only the spec/interface and finite evidence.
Do not rewrite code or use tools. Return JSON only with decision (accept_with_scope or reject),
findings (severity,issue,evidence), accepted_scope and required_changes. Distinguish blockers from limitations.
Do not call simulation agreement, finite examples or local interface proofs complete functional truth.
PACKET:\n''' + json.dumps(payload, separators=(',', ':'), sort_keys=True)
    packet = TASK / 'reference' / ('review-packet-v2' if contract_v2 else 'review-packet-v1')
    packet.mkdir(exist_ok=False)
    (packet / 'prompt.txt').write_text(text)
    dump(packet / 'manifest.json', {'prompt_sha256': sha(packet / 'prompt.txt'),
         'checker_sha256': sha(candidate / 'checker.py'), 'evaluation_sha256': sha(out / 'evaluations.json')})


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--candidate', type=Path, default=TASK / 'reference/author-v1')
    p.add_argument('--output', type=Path, default=TASK / 'reference/evaluation-v1')
    p.add_argument('--contract-v2', action='store_true')
    a = p.parse_args()
    evaluate(a.candidate.resolve(), a.output.resolve(), a.contract_v2)
