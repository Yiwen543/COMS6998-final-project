"""Lossless, size-checked read-only review packet; publish only after validation."""
import argparse
import copy
import json
from pathlib import Path
from prepare_spi_core_checker_review import vector_pack, vector_unpack
from prepare_wbxbar_checker_role import verify_packet
from run_midterm_fixed import sha


def prepare(role, controls, evaluation, packet, output):
    verify_packet(packet)
    auth = json.loads((role / 'candidate/authorship.json').read_text())
    for name, digest in auth['artifact_sha256'].items():
        if sha(role / 'candidate' / name) != digest: raise ValueError('Checker was edited')
    summary = json.loads((evaluation / 'summary.json').read_text())
    for name, digest in summary['hashes'].items():
        if sha(Path(name)) != digest: raise ValueError('Evaluation provenance drift')
    data = json.loads((evaluation / 'private-inputs.json').read_text())
    chosen_dut = ['isolated_m0_d0_w0','isolated_m0_d2_w0','isolated_m1_d1_w1',
                  'burst_m0_d0_n7','burst_m1_d1_n7','error_m0_d0_w0',
                  'release_reacquire_m1_d1','disjoint_concurrent_s0_n7']
    selected = {k:v for k,v in data.items() if not k.startswith('dut/') or k[4:] in chosen_dut}
    first = next(iter(selected.values()))[0]
    columns = [(kind, name) for kind in ('pre','post') for name in first[kind]]
    packed = {}
    for name, rows in selected.items():
        padded = [{**row, 'action': {}} for row in rows]
        packed[name] = vector_pack(padded, columns)
        if vector_unpack(packed[name], columns) != padded: raise ValueError('Lossless roundtrip failed')
    brief = copy.deepcopy(summary)
    brief.pop('hashes')
    for row in brief['cases'].values():
        for key in ('failures','assumption_violations','events','unresolved'):
            values = row.get(key, [])
            row[key+'_total'] = len(values)
            row[key] = values[:3]
    body = {'role': 'Fresh independent read-only reviewer; checker author and this integration role are separate.',
        'task': 'Assess ONLY checker adequacy for the documented exploratory public-pin scope. No stimulus/B/C results or target selection are supplied. Do not modify checker or inputs. Return ready_for_offline_gate, findings, limitations; readiness concerns checker only, NOT a live-run freeze. The final experimental driver is still pending.',
        'specification': json.loads((packet / 'packet.json').read_text()),
        'candidate': {name: (role / 'candidate' / name).read_text() for name in auth['artifact_sha256']},
        'evaluation': brief,
        'controls_manifest': json.loads((controls / 'manifest.json').read_text()),
        'trace_encoding': {'columns': columns, 'description': 'Each first vector is the complete first row in column order. Each [repeat, changes] applies [column_index,value] updates repeat times, incrementing cycle once each time. Unchanged fields persist. Empty action dictionaries are packing-only. Full roundtrip checked locally.',
            'traces': packed, 'all_hand_controls_included': True, 'actual_dut_traces_included': chosen_dut,
            'actual_dut_trace_count_evaluated': 44, 'selection': 'Eight representative DUT traces shown in full; diagnostics/counts retained for all 44. These are not golden outputs.'},
        'review_questions': [
            'Are independent positive traces legal and do single-fault controls isolate a meaningful DUT requirement? Do not demand a checker repair to satisfy an invalid control.',
            'A stale ACK while master CYC=0 is ignored by the declared contract. Distinguish unqualified inactive output from a stale ACK injected into a new accepted transaction; the latter is detected.',
            'The checker currently permits timeout/starvation ERR whenever no slave ACK exists, without timing eligibility. The early_unexplained_error control returns ERR one cycle after first activity on a mapped request, with no slave response and OPT_TIMEOUT=16. Is that control justified and is permissive error handling a blocking gap or an explicit acceptable scope exclusion? Cite spec basis; do not invent an exact implementation counter.',
            'For identical requests the checker suspends functional checks until reset and marks unresolved. Verify there is no scoped-pass escape through ambiguity, unsupported input or premature error.',
            'Review reset/cycle abort epochs, simultaneous acceptance/response, pending batches, ordering and data preservation. Identify additional required independent controls, even if supplied selftests pass.',
            'Do not equate 44 clean observed DUT traces or ten clean hand positives with whole-IP formal correctness. No selected-target reachability or live comparison is certified by this review.'],
        'independence': 'No DUT implementation, guard/equivalence/source-target data, experimental prompts or B/C outcomes. Reviewer may inspect checker implementation and private validation traces only.'}
    prefix = 'Read-only independent checker/driver audit. Do not modify artifacts. Return JSON with ready_for_offline_gate, findings, limitations. Check event false positives, independent controls, spec justification and isolation. No claim of formal proof.\n'
    encoded = json.dumps(body)
    if len((prefix+encoded).encode()) > 150000: raise ValueError('Review packet byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
    (output / 'manifest.json').write_text(json.dumps({'status': 'prepared_not_published',
        'prompt_bytes': len((prefix+encoded).encode()), 'packet_sha256': sha(output/'packet.json'),
        'checker_sha256': sha(role/'candidate/checker.py'), 'script_sha256': sha(Path(__file__)),
        'lossless_trace_roundtrips': len(packed)}, indent=2) + '\n')
    return body


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ('role','controls','evaluation','packet','output'):
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    body = prepare(*[getattr(args,n).resolve() for n in ('role','controls','evaluation','packet','output')])
    if args.publish:
        target = args.role / 'review-packet.json'
        if target.exists(): raise ValueError('Review already published')
        temporary = args.role / 'review-packet.pending'
        temporary.write_text(json.dumps(body, separators=(',', ':')) + '\n')
        temporary.rename(target)
        print('Review packet published after hash/size/roundtrip checks.')
