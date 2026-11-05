"""Read immutable author fixtures and evaluate them in an isolated process."""
import copy
import json
from pathlib import Path
import resource
import sys

resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from evaluate_spi_checker_candidate import load_candidate

base = Path(__file__).resolve().parent
checker = load_candidate(base / 'candidate/checker.py')['check_rows']
tests = load_candidate(base / 'candidate/selftest.py')
outputs = {}
for name, args in [('_tag_mixed', ()), ('_undef_read', (False,)), ('_undef_read', (True,))]:
    rows = tests[name](*args)
    result = checker(copy.deepcopy(rows))
    outputs[name + str(args)] = {'rows': rows, 'result': result}
rows = tests['_tag_mixed']()[:8]
outputs['valid_prefix_before_first_invalid_row'] = {'rows': rows, 'result': checker(copy.deepcopy(rows))}
(base / 'author-test-diagnostic.json').write_text(json.dumps(outputs, indent=2) + '\n')
