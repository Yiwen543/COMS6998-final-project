"""Offline integrity and fail-closed role transport; no model/simulator calls."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_wbxbar_conformance_design as review
import run_wbxbar_conformance_design as author
import prepare_wbxbar_design_revision as revision
import patch_wbxbar_conformance_design as exact_patch
from prepare_spi_core_checker_review import vector_unpack
from prepare_wbxbar_conformance_role import BASE, verify_packet
from probe_wbxbar_cancel_boundary import verify_scope


class ConformanceTransportTests(unittest.TestCase):
    def test_original_boundary_and_role_packets_still_match(self):
        verify_scope()
        verify_packet(BASE / 'claude-design-packet-v1')
        manifest = review.verify(BASE / 'design-review-packet-v1')
        self.assertLessEqual(manifest['bytes'], 150000)
        self.assertEqual(manifest['planned_calls'], 1)

    def test_review_retains_all_synthetic_pins_and_no_actual_results(self):
        original = json.loads((BASE / 'claude-design-packet-v1/packet.json').read_text())
        packet = json.loads((BASE / 'design-review-packet-v1/packet.json').read_text())
        self.assertEqual(packet['synthetic_controls'], original['synthetic_controls'])
        self.assertEqual(packet['specification'], original['specification'])
        self.assertEqual(set(packet), {
            'role', 'specification', 'proposed_design', 'synthetic_controls',
            'additional_existing_synthetic_case', 'integration_questions',
            'exact_fixture_corrections', 'isolation'})
        controls = json.loads((BASE.parent / 'wbxbar_abort_contract_20261104/controls-v1/private-inputs.json').read_text())
        extra = packet['additional_existing_synthetic_case']
        self.assertEqual(extra['rows'], controls[extra['name']])
        self.assertEqual(set(extra), {'name', 'rows', 'note'})
        self.assertEqual({q['id'] for q in packet['integration_questions']},
                         {f'D{i}' for i in range(1, 8)})

    def test_review_prompt_tampering_fails_before_a_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'packet'
            shutil.copytree(BASE / 'design-review-packet-v1', folder)
            with (folder / 'prompt.txt').open('a') as stream:
                stream.write(' altered')
            with patch.object(review, 'call') as call:
                with self.assertRaisesRegex(ValueError, 'Review packet drift'):
                    review.run(folder, Path(tmp) / 'output')
                call.assert_not_called()

    def test_design_format_error_is_not_a_failed_api_or_permission(self):
        meta = json.loads((BASE / 'claude-design-v1/metadata.json').read_text())
        result = json.loads((BASE / 'claude-design-v1/design-validation.json').read_text())
        self.assertEqual(meta['status'], 'complete')
        self.assertEqual(set(meta['model_usage']), {'claude-opus-5-5'})
        usage = meta['usage']
        # Anthropic cache creation/read are additive to uncached input;
        # thinking and per-iteration duplicates are not additive.
        total = sum(usage.get(k, 0) for k in (
            'input_tokens', 'cache_creation_input_tokens',
            'cache_read_input_tokens', 'output_tokens'))
        self.assertEqual(total, 92456)
        self.assertIsInstance(result['readiness_raw'], str)
        self.assertIs(result['automatic_implementation_permission'], False)
        self.assertIs(result['live_B_allowed'], False)
        self.assertIs(result['live_C_allowed'], False)

    def fake_call(self, response):
        def run(prompt, output, env, role):
            output.mkdir()
            return response
        return run

    def test_review_readiness_never_grants_live_and_cleans_key(self):
        for readiness in (True, False, 'true', 1, None):
            with self.subTest(readiness=readiness), tempfile.TemporaryDirectory() as tmp:
                key = Path(tmp) / 'fake-key'
                key.write_text('offline-fixture-only')
                key.chmod(0o600)
                response = {'findings': [], 'corrected_contract_requirements': [],
                            'required_design_changes': [], 'ready_for_implementation': readiness}
                with patch.object(review, 'KEY_FILE', key), patch.object(review, 'call', self.fake_call(response)):
                    result = review.run(BASE / 'design-review-packet-v1', Path(tmp) / 'output')
                self.assertIs(result['automatic_live_permission'], False)
                self.assertEqual(result['schema_valid'], type(readiness) is bool)
                self.assertEqual(result['model_readiness'], readiness if type(readiness) is bool else None)
                self.assertFalse(key.exists())

    def test_failed_review_cleans_key_and_does_not_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / 'fake-key'
            key.write_text('offline-fixture-only')
            key.chmod(0o600)
            with patch.object(review, 'KEY_FILE', key), patch.object(review, 'call', side_effect=RuntimeError('offline failure')) as call:
                with self.assertRaisesRegex(RuntimeError, 'offline failure'):
                    review.run(BASE / 'design-review-packet-v1', Path(tmp) / 'output')
                call.assert_called_once()
            self.assertFalse(key.exists())

    def test_author_text_readiness_does_not_coerce_to_true(self):
        response = json.loads((BASE / 'claude-design-v1/design.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / 'fake-key'
            key.write_text('offline-fixture-only')
            key.chmod(0o600)
            with patch.object(author, 'KEY_FILE', key), patch.object(author, 'call', self.fake_call(response)):
                result = author.run(BASE / 'claude-design-packet-v1', Path(tmp) / 'output')
            self.assertIsNone(result['model_ready_for_implementation'])
            self.assertIs(result['automatic_implementation_permission'], False)
            self.assertFalse(key.exists())

    def test_revision_preserves_every_control_and_identity(self):
        folder = BASE / 'design-revision-packet-v1'
        manifest = revision.verify(folder)
        body = json.loads((folder / 'packet.json').read_text())
        traces = revision.all_controls()
        self.assertEqual(len(traces), 81)
        self.assertEqual(manifest['rows'], sum(map(len, traces.values())))
        for name, packed in body['synthetic_traces']['values'].items():
            decoded = vector_unpack(packed, body['synthetic_traces']['columns'])
            self.assertEqual([{k: v for k, v in r.items() if k != 'action'} for r in decoded], traces[name])
        facts = {r['cycle']: r for r in body['exact_identity_facts']}
        for cycle in (7, 12, 14):
            self.assertEqual(facts[cycle]['address'], 6)
            self.assertEqual(facts[cycle]['data'], 0x23456781)
            self.assertEqual(facts[cycle]['enabled_lane_bits'], 0x00450081)
        self.assertFalse(manifest['implementation_allowed'])

    def test_paired_revision_is_bounded_and_never_grants_permission(self):
        design = {k: [] for k in ('clause_matrix', 'ownership_algorithm', 'formal_obligations', 'control_assessments', 'unresolved')}
        design['ready_for_independent_review'] = True
        result = {'findings': [], 'required_changes': [], 'ready_for_implementation': True}
        replies = iter((design, result))
        def fake(prompt, output, env, role):
            output.mkdir()
            return next(replies)
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / 'fake-key'
            key.write_text('offline-fixture-only')
            key.chmod(0o600)
            with patch.object(revision, 'KEY_FILE', key), patch.object(revision, 'call', side_effect=fake) as call:
                status = revision.run(BASE / 'design-revision-packet-v1', Path(tmp) / 'output')
                self.assertEqual(call.call_count, 2)
            self.assertTrue(status['model_readiness'])
            self.assertFalse(status['automatic_implementation_permission'])
            self.assertFalse(status['live_B_allowed'])
            self.assertFalse(key.exists())

    def test_revision_review_failure_cleans_key_and_does_not_retry(self):
        design = {k: [] for k in ('clause_matrix', 'ownership_algorithm', 'formal_obligations', 'control_assessments', 'unresolved')}
        design['ready_for_independent_review'] = True
        def fake(prompt, output, env, role):
            output.mkdir()
            if output.name == 'review':
                raise RuntimeError('offline second call failed')
            return design
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / 'fake-key'
            key.write_text('offline-fixture-only')
            key.chmod(0o600)
            with patch.object(revision, 'KEY_FILE', key), patch.object(revision, 'call', side_effect=fake) as call:
                with self.assertRaisesRegex(RuntimeError, 'offline second call failed'):
                    revision.run(BASE / 'design-revision-packet-v1', Path(tmp) / 'output')
                self.assertEqual(call.call_count, 2)
            self.assertFalse(key.exists())

    def test_exact_patch_packet_and_pre_edge_ledger(self):
        folder = BASE / 'design-patch-packet-v1'
        manifest = exact_patch.verify(folder)
        body = json.loads((folder / 'packet.json').read_text())
        originals = revision.all_controls()
        originals.update(exact_patch.additions())
        self.assertEqual(manifest['cases'], 88)
        for name, packed in body['synthetic_traces']['values'].items():
            decoded = vector_unpack(packed, body['synthetic_traces']['columns'])
            self.assertEqual([{k: v for k, v in r.items() if k != 'action'} for r in decoded], originals[name])
        events = body['pre_edge_event_ledgers']['new_epoch/two_aborts_then_identical_restart']
        self.assertEqual([e['cycle'] for e in events if e['event'] == 'master_ack_pin'], [18])
        self.assertEqual([e['cycle'] for e in events if e['event'] == 'slave_accept'], [16])
        self.assertEqual([e['cycle'] for e in body['pre_edge_event_ledgers']['new_starvation/unaccepted_err'] if e['event'] == 'master_accept'], [])

    def patch_fixture(self):
        body = json.loads((BASE / 'design-patch-packet-v1/packet.json').read_text())
        response = {'patches': [], 'control_assessments_additions': [
            {'name': name, 'expected_status': 'offline-fixture-only',
             'justified_clauses': [], 'unresolved_scope': 'not a golden label'}
            for name in body['new_control_names']], 'rationale': [], 'ready_for_review': True}
        return body, response

    def test_exact_patch_mismatch_and_deleted_controls_rejected(self):
        body, response = self.patch_fixture()
        original = body['previous_design']
        response['patches'] = [{'path': ['ready_for_independent_review'], 'before': False, 'after': True}]
        with self.assertRaisesRegex(ValueError, 'before mismatch'):
            exact_patch.apply_patches(original, response, body['new_control_names'])
        self.assertIs(original['ready_for_independent_review'], True)
        response['patches'] = [{'path': ['control_assessments'], 'before': original['control_assessments'], 'after': []}]
        with self.assertRaisesRegex(ValueError, 'lost or duplicated'):
            exact_patch.apply_patches(original, response, body['new_control_names'])

    def test_patch_pair_bounded_and_no_live_permission(self):
        body, response = self.patch_fixture()
        result = {'findings': [], 'required_changes': [], 'ready_for_implementation': True}
        replies = iter((response, result))
        def fake(prompt, output, env, role):
            output.mkdir()
            return next(replies)
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / 'fake-key'
            key.write_text('offline-fixture-only')
            key.chmod(0o600)
            with patch.object(exact_patch, 'KEY_FILE', key), patch.object(exact_patch, 'call', side_effect=fake) as call:
                status = exact_patch.run(BASE / 'design-patch-packet-v1', Path(tmp) / 'output')
                self.assertEqual(call.call_count, 2)
                materialized = json.loads((Path(tmp) / 'output/design.json').read_text())
                self.assertEqual(len(materialized['control_assessments']), 88)
            self.assertFalse(status['automatic_implementation_permission'])
            self.assertFalse(status['live_B_allowed'])
            self.assertFalse(status['live_C_allowed'])
            self.assertFalse(key.exists())

    def test_err_boundary_packet_preserves_old_evidence(self):
        folder = BASE / 'design-patch-packet-v2'
        manifest = exact_patch.verify(folder)
        old = json.loads((BASE / 'design-patch-packet-v1/packet.json').read_text())
        new = json.loads((folder / 'packet.json').read_text())
        self.assertEqual(manifest['cases'], 91)
        self.assertEqual(new['synthetic_traces']['columns'], old['synthetic_traces']['columns'])
        for name, packed in old['synthetic_traces']['values'].items():
            self.assertEqual(new['synthetic_traces']['values'][name], packed)
        ledger = new['pre_edge_event_ledgers']
        expected = {'err_boundary/old_live_and_held_request': ([6], [10], [13]),
                    'err_boundary/acceptance_edge': ([8], [8], []),
                    'err_boundary/cyc_withdrawal_edge': ([], [9], [])}
        for name, counts in expected.items():
            for kind, cycles in zip(('master_accept', 'master_err_pin', 'master_ack_pin'), counts):
                self.assertEqual([e['cycle'] for e in ledger[name] if e['event'] == kind], cycles)
            decoded = vector_unpack(new['synthetic_traces']['values'][name], new['synthetic_traces']['columns'])
            self.assertEqual(exact_patch.event_ledger(decoded), ledger[name])
            self.assertTrue(all(not (r['pre']['i_mstb'] & ~r['pre']['i_mcyc']) for r in decoded))

    def test_err_patch_location_repair_preserves_all_semantic_text(self):
        folder = BASE / 'design-patch-v2-retry2'
        body = json.loads((BASE / 'design-patch-packet-v2/packet.json').read_text())
        raw = json.loads((folder / 'patches.json').read_text())
        resolved = json.loads((folder / 'patches-location-corrected.json').read_text())
        with self.assertRaisesRegex(ValueError, 'before mismatch'):
            exact_patch.apply_patches(body['previous_design'], raw, body['new_control_names'])
        parent = body['previous_design']['ownership_algorithm']['resource_limits']['still_valid_after_exhaustion']
        self.assertEqual([i for i, value in enumerate(parent) if value == raw['patches'][2]['before']], [9])
        for original, corrected in zip(raw['patches'], resolved['patches']):
            self.assertEqual(original['before'], corrected['before'])
            self.assertEqual(original['after'], corrected['after'])
        normalized = json.loads(json.dumps(raw))
        normalized['patches'][2]['path'][-1] = 9
        self.assertEqual(normalized, resolved)
        design = exact_patch.apply_patches(body['previous_design'], resolved, body['new_control_names'])
        self.assertEqual(design, json.loads((folder / 'design-location-corrected.json').read_text()))
        self.assertEqual(design['ownership_algorithm']['resource_limits']['still_valid_after_exhaustion'][8], parent[8])


if __name__ == '__main__':
    unittest.main()
