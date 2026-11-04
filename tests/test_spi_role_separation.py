import json
import sys
import unittest
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from prepare_spi_checker_role import packet
from run_spi_checker_author import validate_source
from revise_spi_checker_role import prepare_review
from run_midterm_fixed import sha


class SpiRoleBoundaryTests(unittest.TestCase):
    def test_packet_contains_only_spec_and_interface(self):
        data=packet()
        paths=[r['source'] for r in data['authority']]
        self.assertEqual(len(paths),2)
        self.assertTrue(all('/doc/' in p and p.endswith('.md') for p in paths))
        content=json.dumps(data)
        for forbidden in ('def check_rows(', 'def cases(', 'raw_source_hits', 'api_tokens',
                          'always_comb begin', 'module spi_host_fsm'):
            self.assertNotIn(forbidden,content)
        self.assertEqual(data['interface']['input_fields_widths']['length'],20)

    def test_candidate_rejects_io_and_project_imports(self):
        for source in ('import os', 'from spi_host_fixture import check_rows',
                       'x=open("secret")', 'x=eval("1")', 'x=(1).__class__'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                validate_source(source)
        validate_source('from collections import deque\ndef check_rows(rows):\n return {"failures": []}\n')

    def test_budget_not_shortened_and_roles_differ(self):
        cfg=json.loads((ROOT/'configs/spi_host_event_screen.json').read_text())
        previous=json.loads((ROOT/'configs/spi_host_b_development.json').read_text())
        for field in ('repetitions','rounds','max_new_cycles'):
            self.assertEqual(cfg['development_budget'][field],previous[field])
        self.assertIn('claude-opus-5-5',cfg['roles']['checker_author'])
        self.assertIn('gpt-6.1-sol',cfg['roles']['experimental_stimulus'])
        self.assertTrue(cfg['offline_acceptance']['do_not_equate_temporal_events_using_combinational_proofs'])

    def review_fixture(self, root):
        base=root/'base'; revision=base/'revision';candidate=revision/'candidate'
        candidate.mkdir(parents=True)
        files={'checker.py':'def check_rows(rows): return {}\n','properties.json':'[]\n',
               'contract.md':'scoped','selftest.py':'def run(check): return []\n'}
        for name,value in files.items():(candidate/name).write_text(value)
        (candidate/'metadata.json').write_text(json.dumps({'artifact_sha256':{n:sha(candidate/n) for n in files}}))
        for path,data in [('spec-packet/packet.json',{}),('revision-v3/review.json',{}),
                          ('config-switch-reproducer/evidence.json',{})]:
            p=base/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data))
        ev=revision/'evaluation';ev.mkdir()
        for name,value in [('summary.json',{}),('control-accounting.json',{}),
            ('private-validation-inputs.json',{'independent_reference/one_byte_write':[{'cycle':2}],
                                               'calibration/configuration_switch':[]})]:
            (ev/name).write_text(json.dumps(value))
        return base,revision

    def test_review_packet_uses_saved_controls_not_revision_feedback_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);base,revision=self.review_fixture(root)
            prepare_review(base,revision,root/'packet')
            p=json.loads((root/'packet/packet.json').read_text())
            self.assertEqual(p['independent_reference'],[{'cycle':2}])
            self.assertIn('fixed_driver_source',p)

    def test_review_rejects_edited_checker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);base,revision=self.review_fixture(root)
            (revision/'candidate/checker.py').write_text('changed')
            with self.assertRaises(ValueError):prepare_review(base,revision,root/'packet')


if __name__=='__main__':
    unittest.main()
