#!/usr/bin/env python3
"""One registered Claude-only auxiliary-selftest repair; no GPT oracle patch."""
import json
from common import BASE, ROOT, sha
from reference_role import invoke

TASK = BASE / 'tasks/axis_length_fifo_v1'

if __name__ == '__main__':
    stage = json.loads((TASK / 'reference/repair-stage-v1.json').read_text())
    for name, expected in stage['files'].items():
        if sha(ROOT / name) != expected:
            raise ValueError('Repair packet changed')
    print(json.dumps(invoke('author', TASK / 'reference/author-repair-packet-v1',
                            TASK / 'reference/author-repair-v1')))
