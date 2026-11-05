import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from controller_prepare import TASK, PUBLIC, DRIVER, datasets, normalize, parse
from controller_hidden import mutations
from controller_packet import packet, pack_coverage, unpack_coverage, identity
from controller_reference_evaluate import controls, alignment_controls
import controller_credentials


class ControllerTaskTests(unittest.TestCase):
    def test_fixed_sets_are_deterministic_and_separate(self):
        a, b = datasets()
        self.assertEqual((a, b), datasets())
        self.assertFalse({json.dumps(x) for x in a.values()} & {json.dumps(x) for x in b.values()})
        for traces, tail in [(a, 32), (b, 128)]:
            for actions in traces.values():
                self.assertLessEqual(len(actions), 512)
                self.assertTrue(all(x['reset'] == x['offer'] == 0 and x['data_ready'] == x['status_ready'] == 1
                                    for x in actions[-tail:]))

    def test_transport_parser_preserves_x_and_rejects_forged_source(self):
        log = ('PRE 0 1 0 0 0 1 1 0 x 0 x 0 x x x x\n'
               'POST 0 0 x 0 x 0 x x x x\nQUEUE 0 0 0\n')
        actions = [{'reset': 1, 'offer': 0, 'data': 0, 'last': 0, 'data_ready': 1, 'status_ready': 1}]
        rows, pending = parse(log, actions)
        self.assertEqual(pending, 0)
        self.assertEqual(rows[0]['post']['m_data'], -1)
        with self.assertRaises(ValueError):
            parse(log.replace('PRE 0 1 0 0 0', 'PRE 0 1 1 0 0'), actions)

    def test_cross_sim_comparison_ignores_only_unspecified_payload(self):
        log = ('PRE 0 1 0 0 0 1 1 0 0 0 0 0 0 0 0 0\n'
               'POST 0 0 0 0 0 0 0 0 0 0\nQUEUE 0 0 0\n')
        action = {'reset': 1, 'offer': 0, 'data': 0, 'last': 0, 'data_ready': 1, 'status_ready': 1}
        rows, _ = parse(log, [action])
        other = copy.deepcopy(rows)
        other[0]['post']['m_data'] = -1
        self.assertEqual(normalize(rows), normalize(other))
        other[0]['post']['m_valid'] = -1
        self.assertNotEqual(normalize(rows), normalize(other))

    def test_slang_certified_groups_have_original_distinct_mappings(self):
        root = TASK / 'qualification/typed-v4'
        proof = json.loads((root / 'proof/proof.json').read_text())
        self.assertEqual(proof['status'], 'pass')
        self.assertFalse(proof['unsafe_free_combinational_values'])
        screen = json.loads((root / 'screen/screen.json').read_text())
        groups = [g for g in screen['groups'] if g['nontrivial_static_candidate']]
        self.assertGreaterEqual(len(groups), 1)
        for group in groups:
            self.assertGreaterEqual(len({(m['source'], m['line'], m['column']) for m in group['members']}), 2)
            self.assertTrue(all(m['guard_sat'] == m['guard_not_sat'] == 'sat' for m in group['members']))

    def test_new_faults_are_single_site_and_keep_pending_eligibility(self):
        source = (PUBLIC / 'rtl/axis_frame_length_adjust.v').read_text()
        faults = mutations(source)
        self.assertEqual(len(faults), 12)
        self.assertEqual({s: sum(f[1] == s for f in faults) for s in ['boundary_guard', 'handshake_reset', 'payload_status']},
                         {'boundary_guard': 4, 'handshake_reset': 4, 'payload_status': 4})
        self.assertEqual(len({text for _, _, text, _ in faults}), 12)
        for _, _, text, _ in faults:
            self.assertEqual(sum(a != b for a, b in zip(source.splitlines(), text.splitlines())), 1)

    def test_shared_packet_roundtrip_and_role_isolation(self):
        b, c = packet('B2_raw'), packet('C2_semantic')
        semantic = c.pop('egraph_feedback')
        self.assertEqual(b, c)
        self.assertEqual(len(semantic['groups']), 4)
        self.assertEqual(b['raw_coverage']['counter_count'], 3168)
        text = json.dumps(b)
        for forbidden in ['heldout_01', 'mutant-catalog', 'checker_source', 'reference/author', 'M01.v']:
            self.assertNotIn(forbidden, text)

    def test_finite_controls_cover_independent_channels_and_unknown_priority(self):
        c = controls()
        self.assertEqual(len(c), 15)
        for key in ['legal_both_stalled', 'legal_status_before_data', 'legal_status_after_data', 'legal_reset_cancels_responses']:
            self.assertEqual(c[key]['expected_verdict'], 'PASS')
            rows = c[key]['rows']
            self.assertTrue(all(r['inputs']['rst'] == r['inputs']['s_valid'] == 0 and
                                r['inputs']['m_ready'] == r['inputs']['h_ready'] == 1 for r in rows[-32:]))
        self.assertEqual(c['definite_failure_plus_unknown']['expected_verdict'], 'FAIL')
        self.assertEqual(c['source_changes_while_blocked']['expected_verdict'], 'INVALID_INPUT')

    def test_selected_fifo_local_formal_profile_and_source_gate(self):
        root = TASK.parent / 'axis_length_fifo_v1'
        s = json.loads((root / 'qualification/formal-v2/summary.json').read_text())
        self.assertEqual([r['status'] for r in s['results'][:2]], ['PASS', 'FAIL'])
        self.assertEqual(len(s['results']), 11)
        self.assertTrue(all(r['status'] == 'PASS' for r in s['results'][2:]))
        proof = json.loads((root / 'qualification/typed-v5/proof/proof.json').read_text())
        self.assertEqual(proof['status'], 'pass')
        self.assertEqual(len(proof['definition_checks']), 168)

    def test_rejected_direct_core_failure_is_preserved_in_both_simulators(self):
        formal = json.loads((TASK / 'qualification/formal-v1/summary.json').read_text())
        self.assertEqual([r['status'] for r in formal['results'] if r['property'] == 'status_stall' and r['mode'] != 'cover'], ['FAIL', 'FAIL'])
        for sim in ('iverilog', 'verilator'):
            rows = json.loads((TASK / 'qualification/status-witness-replay-v1' / sim / 'rows.json').read_text())
            row = rows[6]
            self.assertEqual((row['pre']['h_valid'], row['inputs']['h_ready']), (1, 0))
            self.assertEqual((row['pre']['h_original_length'], row['post']['h_original_length']), (2, 1))

    def test_alignment_controls_and_packets_keep_strict_scope(self):
        c = alignment_controls()
        self.assertEqual(len(c), 20)
        for name in ['spurious_stalled_data_then_reset', 'spurious_stalled_status_then_reset', 'pre_not_justified_by_current_input']:
            self.assertEqual(c[name]['expected_verdict'], 'FAIL')
        self.assertEqual(c['final_tail_32_not_128']['expected_verdict'], 'UNRESOLVED')
        b, sem = packet('B2_raw', True), packet('C2_semantic', True)
        sem.pop('egraph_feedback')
        self.assertEqual(b, sem)
        self.assertIn('min_tail=32', b['observer_contract'])

    def test_user_key_retention_survives_inner_review_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staged = root / 'build/private/anthropic-crosscheck-key'
            staged.parent.mkdir(parents=True)
            staged.write_bytes(b'fake-test-value')
            staged.chmod(0o600)
            out = root / 'call'
            def inner(role, packet, output):
                output.mkdir()
                working = controller_credentials.reference_role.KEY_FILE
                self.assertNotEqual(working, staged)
                self.assertEqual(working.read_bytes(), b'fake-test-value')
                working.unlink()
                return {'status': 'test-only'}
            with mock.patch.object(controller_credentials, 'ROOT', root), mock.patch.object(controller_credentials.reference_role, 'invoke', inner):
                controller_credentials.invoke('review', root, out)
            self.assertEqual(staged.read_bytes(), b'fake-test-value')
            self.assertEqual(list(staged.parent.iterdir()), [staged])

    def test_user_key_retention_survives_inner_call_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staged = root / 'build/private/anthropic-crosscheck-key'
            staged.parent.mkdir(parents=True)
            staged.write_bytes(b'fake-test-value')
            staged.chmod(0o600)
            def inner(role, packet, output):
                output.mkdir()
                raise RuntimeError('expected test failure')
            with mock.patch.object(controller_credentials, 'ROOT', root), mock.patch.object(controller_credentials.reference_role, 'invoke', inner):
                with self.assertRaises(RuntimeError):
                    controller_credentials.invoke('author', root, root / 'call')
            self.assertEqual(staged.read_bytes(), b'fake-test-value')
            self.assertEqual(list(staged.parent.iterdir()), [staged])

    def test_reviewed_reference_freeze_preserves_raw_denominators(self):
        root = TASK.parent / 'axis_length_fifo_v1'
        frozen = root / 'reference/frozen-v2'
        data = json.loads((frozen / 'freeze.json').read_text())
        repo = TASK.parents[2]
        for name, expected in data['artifact_sha256'].items():
            self.assertEqual(hashlib.sha256((repo / name).read_bytes()).hexdigest(), expected, name)
        self.assertFalse(data['candidate_generation_allowed'])
        self.assertEqual((data['author_selftests'], data['independent_controls'], data['correct_trace_controls']), (50, 20, 18))
        for sim in ('iverilog', 'verilator'):
            obs = data['fault_observability_by_simulator'][sim]
            self.assertEqual((obs['raw_faults'], obs['raw_fault_trace_pairs'], obs['sampled_eligible_pairs']), (12, 72, 53))
            self.assertEqual(len(obs['observable_faults']), 11)
            self.assertEqual(obs['not_activated_or_unresolved_faults_retained'], ['M08'])


if __name__ == '__main__':
    unittest.main()
