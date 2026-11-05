#!/usr/bin/env python3
"""Certify the fixed controller scope with existing adapters, no model access."""
import argparse
import json
from pathlib import Path
from common import ROOT, BASE, dump, sha
import probe_natural_frontends as frontend
import real_parent_screen as parent
from event_scope_semantics import EventAdapter, EventBitVectors
from probe_write_scopes import verify

SCOPE = BASE / 'configs/controller_qualification_v2.json'


def configuration(top):
    return next(c for c in json.loads(SCOPE.read_text())['candidates'] if c['top'] == top)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise FileExistsError('Refusing to overwrite qualification evidence')
    c = configuration('frame_task')
    verify(c)
    stage = 'frontend'
    try:
        with parent.replace(frontend, configuration=configuration, verify=verify):
            frontend.probe(c['top'], out)
        (out / 'scope.json').write_bytes(SCOPE.read_bytes())
        with parent.replace(parent, SCOPE=SCOPE, configuration=configuration,
                            ParentAdapter=EventAdapter, ParentBitVectors=EventBitVectors):
            if any(r['returncode'] for r in json.loads((out / 'probe.json').read_text())['runs']):
                raise RuntimeError('Frontend rejected source')
            stage = 'preserve_definitions'
            parent.preserve(c['top'], out)
            stage = 'independent_definition_proof'
            proof = parent.prove(c['top'], out, out / 'proof')
            if proof['status'] != 'pass':
                raise RuntimeError('Definition proof incomplete: ' + proof['status'])
            stage = 'raw_inventory'
            parent.inventory(c['top'], out, out / 'inventory')
            stage = 'semantic_source_mapping'
            parent.screen(c['top'], out, out / 'screen', out / 'proof')
        screen = json.loads((out / 'screen/screen.json').read_text())
        dump(out / 'decision.json', {'status': 'semantic_gate_pass' if screen['static_count_gate_pass'] else 'semantic_gate_rejected',
             'nontrivial_groups': screen['nontrivial_static_candidates'],
             'raw_denominator': screen['raw_dut_denominator'], 'source_hashes': c['source_hashes'],
             'registration_sha256': sha(SCOPE), 'script_sha256': sha(Path(__file__)),
             'candidate_calls_allowed': False, 'reference_calls_allowed': False})
        print((out / 'decision.json').read_text())
    except Exception as error:
        out.mkdir(parents=True, exist_ok=True)
        dump(out / 'failure.json', {'stage': stage, 'error_type': type(error).__name__,
                                   'detail': str(error)[:1000], 'registration_sha256': sha(SCOPE)})
        raise


if __name__ == '__main__':
    main()
