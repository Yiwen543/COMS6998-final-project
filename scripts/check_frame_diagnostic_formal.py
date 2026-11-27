#!/usr/bin/env python3
"""Render generated diagnostics independently and verify them on the pinned frame_task RTL."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from check_frame_live_candidate_formal import execute, render_candidate, verify
from egg_frame_formal import ASSETS, PROPERTIES, ROOT, SOURCES
from egg_frame_terms import REFERENCES, abstract, parse_term
from egg_frame_diagnostic import check_engine


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(generated, fixture, destination):
    source = json.loads(generated.read_bytes())
    if set(source['properties']) != set(REFERENCES):
        raise ValueError('unexpected generated property inventory')
    terms = {}
    for name, reference in REFERENCES.items():
        data = source['properties'][name]
        abstract_source, atoms = abstract(parse_term(reference))
        if data['reference'] != reference or data['source'] != abstract_source:
            raise ValueError(f'{name}: generated file differs from fixed reference')
        checked = check_engine(reference, abstract_source, atoms, data['engine'])
        if not checked['accepted'] or data['extracted'] != checked['extracted']:
            raise ValueError(f'{name}: missing accepted, independently rechecked generated DNF')
        terms[name] = checked['typed_expression']
    assertions = ''.join(f'{name}: assert(!({render_candidate(terms[name])}));\n' for name in PROPERTIES)
    manifest = json.loads((ROOT / 'scripts/m3_controller_replay_manifest.json').read_text())
    prior = json.loads((ROOT / 'results/milestone3/frame-formal/summary.json').read_text())
    with tempfile.TemporaryDirectory() as temporary:
        work = Path(temporary)
        hashes = {}
        for rel in SOURCES:
            raw = (fixture / rel).read_bytes()
            hashes[rel] = sha(raw)
            if hashes[rel] != manifest['sha256'][rel] or hashes[rel] != prior['source_sha256'][rel]:
                raise ValueError(f'fixture differs: {rel}')
            (work / Path(rel).name).write_bytes(raw)
        harness = (ASSETS / 'frame_properties.sv').read_bytes()
        if sha(harness) != prior['harness_sha256']:
            raise ValueError('formal harness differs')
        (work / 'frame_properties.sv').write_bytes(harness)
        result_dir = work / 'result'
        result = verify(work, result_dir, {'terms': terms, 'assertions': assertions, 'responses': {}})
        del result['responses_sha256']  # this is generated locally, not a provider response
        summary = {**result, 'source_only_generated_sha256': sha(generated.read_bytes()),
                   'upstream_commit': manifest['commit'], 'source_sha256': hashes,
                   'harness_sha256': sha(harness), 'api_calls': 0,
                   'tools': {tool: execute([tool, flag], work).splitlines()[0]
                             for tool, flag in [('yosys', '-V'), ('z3', '--version')]}}
        (result_dir / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        shutil.copytree(result_dir, destination)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generated', type=Path, required=True)
    parser.add_argument('--fixture', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.generated, args.fixture, args.output)
    print(f"{len(result['assertions'])} generated monitors: {result['bounded_safety']}; holds induction: {result['temporal_induction']}")
