#!/usr/bin/env python3
"""Import byte-exact reviewed CVDP context RTL from the pinned public dataset."""
import argparse
import hashlib
import json
from pathlib import Path
from agent_core import dump
from predicates import ROOT

SHA256 = '2007f4311ed731a985a4ed9187479ad2cfc2462bc4013eba0d72a9f35642fdcf'
REVISION = '5b807d945f6a99aa645f7e43a64a2115e281b4bf'
SELECTED = {'cvdp_agentic_barrel_shifter_0001': 'barrel_shifter',
            'cvdp_agentic_caesar_cipher_0001': 'caesar_cipher',
            'cvdp_agentic_universal_shift_reg_0003': 'universal_shift_register'}


def prepare(path):
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != SHA256:
        raise ValueError('Dataset hash mismatch; refusing an unreviewed dataset')
    selected = {}
    for row in map(json.loads, content.decode().splitlines()):
        if row['id'] in SELECTED:
            if row['id'] in selected:
                raise ValueError('Duplicate dataset id')
            selected[row['id']] = row
    if set(selected) != set(SELECTED):
        raise ValueError('Missing selected CVDP records')
    files = {}
    for id_, name in SELECTED.items():
        row = selected[id_]
        folder = ROOT / 'examples/cvdp' / name
        for relative, text in row['context'].items():
            if relative.startswith('rtl/'):
                if Path(relative).is_absolute() or '..' in Path(relative).parts:
                    raise ValueError('Invalid source path')
                files[folder / relative] = text.encode()
        files[folder / 'upstream_problem.json'] = (json.dumps(row, indent=2) + '\n').encode()
        provenance = {'id': id_, 'categories': row['categories'],
                      'dataset': 'https://huggingface.co/datasets/nvidia/cvdp-benchmark-dataset',
                      'revision': REVISION,
                      'file': 'cvdp_v1.1.0_agentic_code_generation_no_commercial.jsonl',
                      'dataset_sha256': SHA256,
                      'role': 'unaltered input context RTL; not a golden solution or official ECov task',
                      'rtl_sha256': {k: hashlib.sha256(v.encode()).hexdigest()
                                     for k, v in row['context'].items() if k.startswith('rtl/')}}
        files[folder / 'provenance.json'] = (json.dumps(provenance, indent=2) + '\n').encode()
    return files


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset', required=True, type=Path)
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    files = prepare(a.dataset)
    # Validate the entire import before any writes; never overwrite local changes.
    for path, content in files.items():
        if path.exists() and path.read_bytes() != content:
            raise ValueError(f'Existing file differs from pinned input: {path}')
        if a.check and not path.exists():
            raise ValueError(f'Missing imported file: {path}')
    if not a.check:
        for path, content in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    print(f'Validated {len(SELECTED)} modules, {len(files)} source/provenance files; no RTL repair applied.')

if __name__ == '__main__':
    main()
