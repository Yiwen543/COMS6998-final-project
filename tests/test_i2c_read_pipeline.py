import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from i2c_read_fixture import action,seed,validate_actions
from calibrate_i2c_reads import batches
from independent_i2c_read_controls import controls
from prepare_i2c_compact_review import pack,unpack
from legacy_guard_probe import LegacyAdapter
from run_midterm_fixed import sha


class I2CReadPipeline(unittest.TestCase):
    def test_read_schema_boundaries(self):
        validate_actions({'actions':seed()+[action(push=1,read=1,byte=0,stop=1)]})
        for a in [action(push=1,read=1,nak_ok=1),action(push=1,read=1,rcont=1,stop=1),
                  action(target_data=256),action(read=True),action(checker=0)]:
            with self.assertRaises(ValueError):validate_actions({'actions':seed()+[a]})
        with self.assertRaises(ValueError):validate_actions({'actions':[action()]*65},64,False)

    def test_private_calibration_reproducible(self):
        b=ROOT/'results/i2c_read_candidate_20261104/driver-v2'
        for name,actions in batches().items():
            self.assertEqual(actions,json.loads((b/(name+'.actions.json')).read_text())['actions'])
            validate_actions({'actions':actions})

    def test_two_simulators_and_raw_denominator(self):
        b=ROOT/'results/i2c_read_candidate_20261104'
        for name in batches():
            self.assertEqual(json.loads((b/f'driver-v2/{name}.trace.json').read_text()),
                             json.loads((b/f'icarus-v2/{name}.trace.json').read_text()))
            self.assertTrue(json.loads((b/f'driver-v2/{name}.json').read_text())['environment_valid'])
        screen=json.loads((b/'source-screen.json').read_text())
        self.assertEqual(screen['raw_denominator'],1277)
        self.assertEqual(screen['mapped']+screen['unresolved'],268)
        for f,h in screen['raw_files_sha256'].items():self.assertEqual(sha(ROOT/f),h)
        self.assertFalse(screen['B_allowed'])
        self.assertEqual(screen['groups_beyond_ordinary_read'],0)

    def test_varied_external_target_data(self):
        b=ROOT/'results/i2c_read_candidate_20261104/driver-v2'
        rows=json.loads((b/'multi_read_varied.trace.json').read_text())
        self.assertEqual([r['pre']['rx_data'] for r in rows if r['pre']['rx_valid']],[0xA6,0x3C])
        # This is a driver-data sanity control, not the independent DUT oracle.

    def test_role_boundary_budget_and_old_freeze(self):
        from run_i2c_checked import verify_freeze
        self.assertTrue(verify_freeze()['offline_checker_qualified'])
        b=ROOT/'results/i2c_read_candidate_20261104'
        packet=json.loads((b/'spec-packet/packet.json').read_text())
        for token in ['state_q','tcount_q','claude-v1','driver-v1','equivalent_pairs']:
            self.assertNotIn(token,json.dumps(packet))
        old=json.loads((ROOT/'configs/i2c_event_screen.json').read_text())
        new=json.loads((ROOT/'configs/i2c_read_screen.json').read_text())
        self.assertEqual(old['development_budget'],new['development_budget'])

    def test_lossless_controls(self):
        for rows in controls().values():self.assertEqual(rows,unpack(pack(rows)))

    def test_rejected_author_version_retained(self):
        p=ROOT/'results/i2c_read_candidate_20261104/claude-v1'
        self.assertFalse(json.loads((p/'review.json').read_text())['ready_for_offline_gate'])
        e=json.loads((p/'controls/evaluation.json').read_text())
        self.assertEqual(e['checker_sha256'],sha(p/'candidate/checker.py'))
        self.assertEqual(e['cases']['ordinary_read']['verdict'],'fail')
        self.assertTrue(all(not x['credited_detection'] for x in e['event_controls']))

    def test_published_checker_and_classification_limit(self):
        from run_i2c_read_checked import verify_freeze
        manifest=verify_freeze()
        self.assertTrue(manifest['offline_checker_qualified'])
        self.assertFalse(manifest['formal_B_eligible'])
        self.assertFalse(manifest['defect_classification_qualified'])
        p=ROOT/'results/i2c_read_candidate_20261104/claude-v2'
        e=json.loads((p/'controls-qualified/evaluation.json').read_text())
        self.assertEqual(e['checker_sha256'],sha(ROOT/'examples/heldout_i2c_read/checker.py'))
        self.assertTrue(all(x['credited_detection'] for x in e['event_controls']))
        self.assertTrue(all(x['credited_detection'] for x in e['negative_controls'].values()))
        self.assertFalse(e['negative_controls']['extra_stop_during_read']['correct_dut_failure_classification'])
        self.assertTrue(all(e['pending_controls'].values()))

    def test_environment_and_pre_event_gate(self):
        from i2c_read_gate import gate_result
        b=ROOT/'results/i2c_read_candidate_20261104'
        e=json.loads((b/'claude-v2/controls-qualified/evaluation.json').read_text())
        rows=json.loads((b/'driver-v2/multi_read.trace.json').read_text())
        checked=e['cases']['dut_multi_read'];original=copy.deepcopy(checked)
        self.assertTrue(gate_result({'environment_valid':True},rows,checked)['scoped_pass'])
        self.assertFalse(gate_result({'environment_valid':False},rows,checked)['scoped_pass'])
        rows[20]['pre']['sda_unstable']=1
        r=gate_result({'environment_valid':True},rows,checked)
        self.assertFalse(r['scoped_pass']);self.assertEqual(r['credited_events'],[])
        self.assertEqual(checked,original)

    def test_legacy_probe_preserves_source_and_edge_context(self):
        p=ROOT/'results/natural_ip_followup_20261104/axi_dma_rd/ast.json'
        ast=json.loads(p.read_text());original=copy.deepcopy(ast)
        adapter=LegacyAdapter(ast,'axi_dma_rd').extract()
        self.assertEqual(ast,original)
        contexts={tuple(t['event_context']) for t in adapter.targets}
        self.assertIn(('combinational:implicit_all',),contexts)
        self.assertIn(('PosEdge:clk',),contexts)
        self.assertTrue(any('SSA required' in u['reason'] for u in adapter.unsupported))


if __name__=='__main__':unittest.main()
