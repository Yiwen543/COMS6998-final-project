"""Reproduce one failed author selftest and a tagged mixed-edge boundary."""
import copy
import json
import resource
import sys
from pathlib import Path

resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from evaluate_spi_checker_candidate import load_candidate
from wbxbar_checker_controls import put, settle

base = Path(__file__).resolve().parent.parent
prior = load_candidate(base / 'claude-author-v1/checker.py')['check_rows']
candidate = load_candidate(base / 'repair-v1/candidate/checker.py')['check_rows']
test = load_candidate(base / 'repair-v1/candidate/selftest.py')
traces = {'author_mixed_same_edge': test['_mixed']()}
rows = copy.deepcopy(json.loads((base / 'review-repro-v2/inputs.json').read_text())['tag_then_membership_death']['rows'])
for cycle in (18, 19):
    for port, width, value in [('i_mcyc', 1, 1), ('i_mstb', 1, 1), ('o_mstall', 1, 1),
                              ('i_maddr', 8, 4 if cycle == 18 else 5), ('i_msel', 4, 15)]:
        put(rows, cycle, port, 1, width, value)
traces['tag_then_mixed_same_edge'] = settle(rows)
output = {'scope': 'Diagnostic traces only; no new golden labels or DUT execution.', 'cases': {}}
for name, rows in traces.items():
    output['cases'][name] = {'rows': rows, 'prior': prior(copy.deepcopy(rows)), 'candidate': candidate(copy.deepcopy(rows))}
Path(sys.argv[1]).write_text(json.dumps(output, indent=2) + '\n')
