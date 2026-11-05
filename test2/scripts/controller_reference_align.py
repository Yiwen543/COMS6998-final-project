#!/usr/bin/env python3
"""One Claude author/reviewer pair to close recorded reference-contract gaps."""
import argparse
import json
from common import BASE, ROOT, sha
from controller_credentials import invoke

TASK = BASE / 'tasks/axis_length_fifo_v1'

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--role', choices=['author', 'review'], required=True)
    a = p.parse_args()
    stage = json.loads((TASK / 'reference/alignment-stage-v2.json').read_text())
    for name, h in stage['files'].items():
        if sha(ROOT / name) != h:
            raise ValueError('Alignment stage input changed')
    packet = TASK / 'reference' / ('author-strengthen-packet-v1' if a.role=='author' else 'review-packet-v2')
    if a.role == 'review':
        m = json.loads((packet / 'manifest.json').read_text())
        if sha(packet / 'prompt.txt') != m['prompt_sha256']:
            raise ValueError('Review packet changed')
    out = TASK / 'reference' / ('author-strengthen-v1' if a.role=='author' else 'review-v2')
    print(json.dumps(invoke(a.role, packet, out)))
