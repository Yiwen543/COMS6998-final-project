#!/usr/bin/env python3
"""Audit a PC run, independently render its passing replies, and check the pinned RTL."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

import z3

from audit_egg_fifo_live import require
from audit_egg_frame_pc import AuditEvidence, assessment, audit, compact, match
from check_frame_live_candidate_formal import execute, render_candidate, sha, verify
from egg_frame_formal import ASSETS, PROPERTIES, ROOT, SOURCES
from egg_frame_llm import validate
from egg_frame_terms import REFERENCES


def collect(files, evidence):
    # The transcript audit reconstructs config, coverage scores, conversations, receipts
    # and assessments from the fixed profiles, exact response terms and original corpus.
    transcript = audit(files, evidence.directory, cache=evidence)
    candidates, paths = {}, {}
    for path in sorted(name for name in files if name.endswith('/response.json')):
        prefix = path.removesuffix('/response.json')
        receipt = json.loads(files[path])
        assessment_raw = files[f'{prefix}/assessment.json']
        recorded = json.loads(assessment_raw)
        provenance = {
            'response_id': receipt['id'], 'mode': transcript['mode'],
            'request_sha256': sha(files[f'{prefix}/request.json']),
            'response_sha256': sha(files[path]), 'assessment_sha256': sha(assessment_raw),
        }
        paths[prefix] = provenance
        try:
            terms = validate(receipt['output'])
        except ValueError as exc:
            match(recorded, {'verified': False, 'candidate_error': str(exc)}, prefix + ': invalid reply')
            provenance.update(verified=False, candidate_error=str(exc))
            continue
        # Keys include BOTH exact reference and exact candidate. Each cached query was
        # run again by AuditEvidence in this process on full-width unrestricted pins.
        queries = {name: evidence.oracles[REFERENCES[name], terms[name]] for name in PROPERTIES}
        fresh = assessment(queries, evidence.physical(terms))
        match(recorded, fresh, prefix + ': archived grade conflicts with fresh verification')
        key = sha(compact(terms).encode())
        provenance.update(candidate_sha256=key, verified=fresh['verified'],
                          typed_xor={name: q['status'] for name, q in queries.items()})
        if not fresh['verified']:
            continue
        require(all(q['status'] == 'unsat' for q in queries.values()), prefix + ': incomplete equivalence')
        if key not in candidates:
            assertions = ''.join(f'{name}: assert(!({render_candidate(terms[name])}));\n' for name in PROPERTIES)
            candidates[key] = {'terms': terms, 'assertions': assertions, 'queries': queries, 'responses': {}}
        candidates[key]['responses'][prefix] = provenance['response_sha256']
    require(len(paths) == transcript['responses'], 'reply inventory differs from audited run')
    return candidates, paths, transcript


def run(run_dir, fixture, output):
    require(not output.exists(), f'output already exists: {output}')
    files = {p.relative_to(run_dir).as_posix(): p.read_bytes() for p in run_dir.rglob('*') if p.is_file()}
    corpus = ROOT / 'results/milestone3/frame-faults'
    candidates, paths, transcript = collect(files, AuditEvidence(corpus))
    prior = json.loads((ROOT / 'results/milestone3/frame-formal/summary.json').read_bytes())
    manifest = json.loads((ROOT / 'scripts/m3_controller_replay_manifest.json').read_bytes())
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        out = work / 'result'
        out.mkdir()
        inputs = {}
        for name in SOURCES:
            raw = (fixture / name).read_bytes()
            inputs[name] = sha(raw)
            require(inputs[name] == manifest['sha256'][name] == prior['source_sha256'][name],
                    f'fixture source differs: {name}')
            (work / Path(name).name).write_bytes(raw)
        harness = (ASSETS / 'frame_properties.sv').read_bytes()
        require(sha(harness) == prior['harness_sha256'], 'formal harness differs')
        (work / 'frame_properties.sv').write_bytes(harness)
        results = {}
        for key, candidate in candidates.items():
            case = out / key
            results[key] = verify(work, case, candidate)
            results[key]['typed_xor'] = {}
            for prop, q in candidate['queries'].items():
                path = case / f'{prop}.smt2'
                path.write_text(q['smt2'], encoding='utf-8')
                results[key]['typed_xor'][prop] = {'status': q['status'], 'smt2_sha256': sha(path.read_bytes())}
        summary = {
            'method': 'Post-hoc formal check of unique submitted candidate batches passing the replayed PC assessment',
            'mode': transcript['mode'], 'certificate_mode': transcript['certificate_mode'],
            'config_sha256': sha(files['config.json']), 'archive_summary_sha256': sha(files['summary.json']),
            'upstream_commit': manifest['commit'], 'source_sha256': inputs, 'harness_sha256': sha(harness),
            'corpus_sha256': transcript['physical_corpus_sha256'], 'responses': len(paths),
            'verified_responses': sum(p['verified'] for p in paths.values()),
            'unique_verified_candidates': len(results), 'results': results, 'provenance': paths,
            'archived_provider_calls': transcript['provider_api_calls_in_archive'],
            'new_model_calls': 0, 'new_physical_simulations': 0,
            'tools': {tool: execute([tool, flag], work).splitlines()[0]
                      for tool, flag in [('yosys', '-V'), ('z3', '--version')]},
        }
        summary['tools']['z3py'] = z3.get_version_string()
        (out / 'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
        shutil.copytree(out, output)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True, help='full extracted PC transcript directory')
    parser.add_argument('--fixture', type=Path, required=True, help='pinned frame_task fixture directory')
    parser.add_argument('--output', type=Path, required=True, help='new formal results directory')
    args = parser.parse_args()
    report = run(args.run_dir, args.fixture, args.output)
    print(f"{report['verified_responses']}/{report['responses']} {report['mode']} replies passed; "
          f"{report['unique_verified_candidates']} distinct candidate batches checked on RTL.")
