import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from spi_host_fixture import FIELDS, OUTPUTS, action, check_rows, validate_actions


def reference_trace():
    """Hand-authored legal 1-byte CPHA0 write, independent of DUT execution."""
    idle = {key: 0 for key in OUTPUTS}
    idle.update(csb=3, ready=1)
    rows = []

    def emit(a, pre, post):
        rows.append({'cycle': len(rows), 'action': a, 'pre': dict(pre), 'post': dict(post)})

    emit(action(rst_n=0), idle, idle)
    emit(action(rst_n=0), idle, idle)
    selected = dict(idle, ready=0, csb=2, active=1, sd_en=1)
    emit(action(valid=1, write=1), dict(idle, wr=1, last_write=1), selected)
    old = selected
    for edge in range(16):
        new = dict(selected, sck=1-(edge % 2))
        emit(action(), old, new)
        old = new
    emit(action(), old, idle)
    return rows


class SpiCheckerTests(unittest.TestCase):
    def test_independent_reference_passes(self):
        result = check_rows(reference_trace())
        self.assertEqual(result['verdict'], 'scoped_pass')
        self.assertEqual(result['accepted_commands'], 1)
        self.assertFalse(result['incomplete_serial_burst'])

    def test_single_trace_faults_detected(self):
        cases = {'asynchronous_reset': (0, 'pre', 'csb', 2),
                 'multiple_chip_selects': (3, 'post', 'csb', 0),
                 'segment_last_flag': (2, 'pre', 'last_write', 0),
                 'unexpected_byte_transfer': (19, 'pre', 'rd', 1),
                 'serial_edge_count': (8, 'post', 'sck', 1)}
        for category, (cycle, side, signal, value) in cases.items():
            rows = reference_trace()
            rows[cycle][side][signal] = value
            self.assertIn(category, check_rows(rows)['distinct_defects'], category)

    def test_failure_counts_not_distinct_defects(self):
        rows = reference_trace()
        rows[0]['pre']['csb'] = 2
        rows[1]['pre']['csb'] = 2
        result = check_rows(rows)
        self.assertEqual(sum(f['category'] == 'asynchronous_reset' for f in result['failures']), 2)
        self.assertEqual(result['distinct_defects'].count('asynchronous_reset'), 1)

    def test_stall_and_bad_driver_are_distinct(self):
        rows = reference_trace()
        rows[3]['pre'].update(tx_stall=1, wr=1)
        self.assertIn('stall_controls_not_suppressed', check_rows(rows)['distinct_defects'])
        rows = reference_trace()
        rows[2]['pre']['ready'] = 0
        result = check_rows(rows)
        self.assertEqual(result['verdict'], 'input_or_scope_invalid')
        self.assertEqual(result['assumption_violations'][0]['category'], 'command_not_held_until_handshake')

    def test_incomplete_batch_is_not_proof_or_false_failure(self):
        result = check_rows(reference_trace()[:8])
        self.assertFalse(result['failures'])
        self.assertTrue(result['incomplete_serial_burst'])

    def test_schema_fail_closed(self):
        invalid = [dict(action(), forged_checker=0), dict(action(), length=1 << 20),
                   dict(action(), speed=3), dict(action(), speed=1, read=1, write=1),
                   dict(action(), rst_n=0, valid=1), dict(action(), enable=True)]
        for a in invalid:
            with self.assertRaises(ValueError):
                validate_actions({'actions': [a]}, 1)
        with self.assertRaises(ValueError):
            validate_actions({'actions': [action()]*3}, 2)


if __name__ == '__main__':
    unittest.main()
