"""CVDP adapter safety, independent oracle examples, and generic stimulus contracts."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from agent_core import response_schema, validate_batch
from cvdp_modules import FIELDS, NAMES, candidates, check, environment, initial, targets, verify_source
from cvdp_simulator import CVDPSimulator
from coverage import join
from predicates import parse, evaluate


class CVDPTests(unittest.TestCase):
    def test_source_provenance_and_concrete_guard_domains(self):
        for name in NAMES:
            self.assertEqual(verify_source(name)['dataset_sha256'],
                             '2007f4311ed731a985a4ed9187479ad2cfc2462bc4013eba0d72a9f35642fdcf')
            seen = set()
            for v in candidates(name):
                seen.add(tuple(sorted(environment(name, v).items())))
            self.assertEqual(len(seen), {'barrel_shifter': 2, 'caesar_cipher': 5,
                                        'universal_shift_register': 16}[name])
        for name, target_id in [('caesar_cipher', 'lower_path'),
                                ('universal_shift_register', 'case_default')]:
            t = next(t for t in targets(name) if t['id'] == target_id)
            self.assertFalse(any(evaluate(parse(t['compact']), environment(name, v))
                                 for v in candidates(name)))

    def test_known_shift_and_cipher_oracle_examples(self):
        vectors = [{'data_in': 36, 'shift_bits': 1, 'left_right': 1},
                   {'data_in': 128, 'shift_bits': 1, 'left_right': 0}]
        self.assertEqual(check('barrel_shifter', vectors, [[72], [64]])['functional_errors'], 0)
        self.assertEqual(check('barrel_shifter', vectors, [[0], [1]])['functional_errors'], 2)
        vectors = [{'input_char': c, 'key': k} for c, k in [(65, 3), (90, 1), (122, 15), (33, 3)]]
        self.assertEqual(check('caesar_cipher', vectors, [[68], [65], [111], [33]])['functional_errors'], 0)
        self.assertEqual(check('caesar_cipher', vectors, [[65], [90], [122], [33]])['functional_errors'], 3)

    def test_stateful_oracle_catches_broken_shift_and_serial_output(self):
        vectors = [dict(zip(FIELDS['universal_shift_register'], row)) for row in
                   [(1, 0, 0, 0, 0), (0, 3, 0, 0, 129), (0, 1, 1, 1, 0),
                    (0, 2, 0, 0, 0), (0, 0, 1, 0, 0)]]
        good = [[0, 0], [129, 1], [3, 0], [129, 1], [129, 1]]
        self.assertEqual(check('universal_shift_register', vectors, good)['functional_errors'], 0)
        bad = copy.deepcopy(good)
        bad[2] = [2, 0]
        bad[4] = [129, 0]
        self.assertEqual(check('universal_shift_register', vectors, bad)['functional_errors'], 2)

    def test_module_schema_rejects_wrong_ports_bools_and_ranges(self):
        for name in NAMES:
            ts = targets(name)
            v = {**initial(name)[0], 'target_id': 'spec_probe'}
            self.assertEqual(validate_batch({'note': '', 'vectors': [v]}, ts, 4, FIELDS[name]), [v])
            schema = response_schema(ts, 4, FIELDS[name])
            self.assertEqual(set(schema['properties']['vectors']['items']['required']), set(v))
            for field in FIELDS[name]:
                for bad in (True, FIELDS[name][field] + 1, -1):
                    with self.assertRaises(ValueError):
                        validate_batch({'note': '', 'vectors': [{**v, field: bad}]}, ts, 4, FIELDS[name])
            with self.assertRaises(ValueError):
                validate_batch({'note': '', 'vectors': [{**v, 'invented_port': 0}]}, ts, 4, FIELDS[name])

    def test_simulation_trace_requires_completion_order_and_known_outputs(self):
        self.assertEqual(CVDPSimulator.parse_trace('TRACE 0 3\nDONE 1\n', 1), [[3]])
        for log in ('TRACE 0 x\nDONE 1\n', 'TRACE 1 3\nDONE 1\n', 'TRACE 0 3\n'):
            with self.assertRaises(ValueError):
                CVDPSimulator.parse_trace(log, 1)

    def test_source_join_does_not_accept_counter_from_another_module(self):
        target = targets('barrel_shifter')[0]
        point = {'source': 'other.sv', 'line': target['line'], 'type': target['counter_type'],
                 'outcome': target['counter_outcome'], 'hits': 1}
        with self.assertRaises(ValueError):
            join([target], {'targets': [{'id': target['id']}]}, [point])
