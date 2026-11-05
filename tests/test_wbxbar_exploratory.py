"""Isolation and admission checks; no live model calls or credentials."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import prepare_wbxbar_checker_role as prep
import run_wbxbar_checker_roles as runner
from run_midterm_fixed import sha


class ExploratoryPreparationTests(unittest.TestCase):
    def test_only_difficulty_admission_relaxed(self):
        scope, _ = prep.verify_scope()
        old = json.loads((ROOT / scope['parent']['path']).read_text())
        for key in ('development_budget', 'model_limits', 'roles'):
            self.assertEqual(scope[key], old[key])
        self.assertEqual(len(scope['targets']), 8)
        self.assertEqual(len({tuple(m) for g in scope['targets'] for m in g['source_counter_identities']}), 17)
        self.assertEqual(scope['arms'], ['B', 'C'])
        self.assertTrue(scope['checker_commission_allowed'])
        self.assertFalse(scope['live_B_allowed'] or scope['live_C_allowed'])

    def test_author_does_not_receive_targets_or_implementation(self):
        body = prep.packet()
        self.assertEqual(set(body), {'role','scope','authority','parameters','interface','requested_obligations','isolation'})
        text = json.dumps(body)
        for forbidden in ('mindex', 'mgrant', 'eclass', 'isolated_m0', 'results/',
                          'always @', 'assign ', '17 counters', '8 groups', 'B_allowed'):
            self.assertNotIn(forbidden, text)
        for source in body['authority']:
            if source['source'].endswith('.v'):
                self.assertTrue(all(e['end_line'] <= 39 for e in source['excerpts']))

    def test_public_ports_match_elaboration(self):
        ports = json.loads((ROOT / 'results/wbxbar_conditional_20261104/screen-v2/netlist.json').read_text())['modules']['wbxbar']['ports']
        for direction, declared in prep.PORTS.items():
            expected = {k: len(v['bits']) for k,v in ports.items()
                        if k != 'i_clk' and v['direction'] == direction[:-1]}
            self.assertEqual(declared, expected)

    def test_packet_edit_fails_before_transport(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            prep.prepare(base / 'packet')
            self.assertEqual(prep.verify_packet(base / 'packet')['status'], 'prepared_not_called')
            prompt = base / 'packet/prompt.txt'
            prompt.write_text(prompt.read_text() + '\nAdded undocumented requirement.')
            with patch.object(runner.transport, 'run') as transport:
                with self.assertRaisesRegex(ValueError, 'drift'):
                    runner.run(base / 'packet', base / 'out')
                transport.assert_not_called()

    def test_rehashed_extra_author_field_still_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder) / 'packet'
            prep.prepare(base)
            data = json.loads((base / 'packet.json').read_text())
            data['private_calibration'] = 'forbidden'
            (base / 'packet.json').write_text(json.dumps(data))
            manifest = json.loads((base / 'manifest.json').read_text())
            manifest['packet_sha256'] = sha(base / 'packet.json')
            (base / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'allowlisted'):
                prep.verify_packet(base)

    def test_scoped_wrapper_restores_transport_without_model_call(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            prep.prepare(base / 'packet')
            original = runner.transport.call
            def fail_transport(*args):
                self.assertIsNot(runner.transport.call, original)
                raise RuntimeError('offline injected failure')
            with patch.object(runner.transport, 'run', side_effect=fail_transport):
                with self.assertRaisesRegex(RuntimeError, 'offline injected'):
                    runner.run(base / 'packet', base / 'out')
            self.assertIs(runner.transport.call, original)


if __name__ == '__main__':
    unittest.main()
