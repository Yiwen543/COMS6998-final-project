"""Driver boundaries and corrupt-transport rejection; no checker expectations."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from wbxbar_exploratory_driver import validate,parse

BASE=ROOT/'results/wbxbar_exploratory_bc_20261104/driver-v1'


class OfferDriverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((BASE/'compiled/manifest.json').read_text())
        cls.actions=json.loads((BASE/'actions.json').read_text())

    def parse_case(self,name,log=None):
        log=log if log is not None else (BASE/name/'verilator/simulation.log').read_text()
        return parse(log,self.actions[name],self.manifest['inputs'],self.manifest['outputs'])

    def test_pending_is_not_automatic_completion(self):
        rows,counts=self.parse_case('pending_prefix')
        self.assertEqual(len(rows),9)
        self.assertFalse(counts['delivery_complete'])
        self.assertEqual(counts['outstanding'],1)

    def test_error_and_reset_discard_are_not_successful_returns(self):
        _,error=self.parse_case('error_burst_restart')
        self.assertEqual((error['accepted'],error['responses'],error['error_aborted_accepted']),(5,2,3))
        _,reset=self.parse_case('reset_pending_restart')
        self.assertEqual((reset['accepted'],reset['responses'],reset['reset_discarded_accepted']),(2,1,1))

    def test_error_has_counted_low_cycle_gap(self):
        rows,_=self.parse_case('error_burst_restart')
        errors=[r['cycle'] for r in rows[:-1] if r['pre']['i_mcyc']&r['pre']['o_merr']]
        self.assertTrue(errors)
        for n in errors:self.assertFalse(rows[n+1]['pre']['i_mcyc']&1)

    def test_corrupt_abort_pin_rejected(self):
        name='error_burst_restart';rows,_=self.parse_case(name)
        cycle=next(r['cycle']+1 for r in rows[:-1] if r['pre']['i_mcyc']&r['pre']['o_merr'])
        lines=(BASE/name/'verilator/simulation.log').read_text().splitlines()
        i=next(i for i,line in enumerate(lines) if line.startswith('PRE '+str(cycle)+' '))
        fields=lines[i].split();field=2+self.manifest['inputs'].index('i_mcyc')
        fields[field]=format(int(fields[field],16)|1,'x');lines[i]=' '.join(fields)
        with self.assertRaisesRegex(ValueError,'JSON/pin mismatch'):
            self.parse_case(name,'\n'.join(lines))

    def test_offers_in_reset_rejected(self):
        values=copy.deepcopy(self.actions['pending_prefix']);values[8].update(rst=1,offer=1)
        with self.assertRaisesRegex(ValueError,'during reset'):validate(values)

    def test_replay_prefix_preserves_actual_pins(self):
        prefix,_=self.parse_case('pending_prefix')
        longer,_=self.parse_case('reset_pending_restart')
        self.assertEqual(prefix,longer[:len(prefix)])


if __name__=='__main__':unittest.main()
