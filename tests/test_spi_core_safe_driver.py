import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from spi_core_safe_interface import action,seed,validate,TransportOracle,parse,CMD,TX
from spi_core_safe_runtime import BASE,checked_stage,SafeExecutionError

class SafeTransportTests(unittest.TestCase):
    def test_valid_and_entire_payload_hold_despite_new_requests(self):
        o=TransportOracle();a=action(cmd_offer=1,write=1,length=7,tx_offer=1,tx_data=123,tx_be=5)
        p=o.drive(a);o.advance({'ready':0,'tx_ready':0})
        for _ in range(4):
            q=o.drive(action(cmd_offer=1,read=1,length=31,tx_offer=1,tx_data=999,tx_be=15))
            self.assertEqual({k:q[k] for k in (*CMD,*TX,'valid','tx_valid')},{k:p[k] for k in (*CMD,*TX,'valid','tx_valid')})
            o.advance({'ready':0,'tx_ready':0})
        q=o.drive(action());s=o.advance({'ready':1,'tx_ready':1})
        self.assertEqual((s['cmd_accept_id'],s['tx_accept_id']),(0,0));self.assertEqual(s['cmd_pending'],4)

    def test_identical_successive_offers_are_distinct_and_accept_once(self):
        o=TransportOracle();ids=[]
        for i in range(5):
            o.drive(action(cmd_offer=int(i<2),write=1,tx_offer=int(i<2),tx_data=99,tx_be=15))
            s=o.advance({'ready':1,'tx_ready':1});ids.append(s['cmd_accept_id'])
        self.assertEqual(ids,[0,1,-1,-1,-1]);self.assertEqual(s['cmd_accepted'],2)

    def test_independent_channels_and_reset_conservation(self):
        o=TransportOracle();o.drive(action(cmd_offer=1,read=1,tx_offer=1,tx_data=11,tx_be=1))
        s=o.advance({'ready':1,'tx_ready':0});self.assertEqual(s['cmd_pending'],0);self.assertEqual(s['tx_pending'],1)
        o.drive(action(cmd_offer=1,read=1,tx_offer=1,tx_data=22,tx_be=1));o.advance({'ready':0,'tx_ready':0})
        pins=o.drive(action(rst_n=0));s=o.advance({'ready':1,'tx_ready':1})
        self.assertEqual((s['cmd_cancelled'],s['tx_cancelled']),(1,2))
        self.assertEqual((s['cmd_accepted'],s['tx_accepted']),(1,0));self.assertFalse(pins['valid'] or pins['tx_valid'])

    def test_no_ready_means_pending_and_no_implicit_progress(self):
        o=TransportOracle()
        for i in range(64):
            o.drive(action(cmd_offer=int(i==0),read=1));s=o.advance({'ready':0,'tx_ready':0})
        self.assertEqual((o.cycle,s['cmd_pending'],s['cmd_accepted']),(64,1,0))

    def test_unused_payload_does_not_drive_coverage(self):
        o=TransportOracle();p=o.drive(action(length=200,tx_data=777,cpol=1));o.advance({'ready':1,'tx_ready':1})
        self.assertTrue(all(p[k]==0 for k in (*CMD,*TX)))

    def test_width_reset_and_old_valid_fields_rejected(self):
        validate({'actions':seed()+[action()]},392,initial=True)
        for kw in ({'cmd_offer':2},{'rst_n':0,'cmd_offer':1,'read':1},{'tx_data':2**32},{'cmd_offer':1},{'enable':0}):
            with self.assertRaises(ValueError):validate({'actions':[action(**kw)]},64)
        bad=action();bad['valid']=bad.pop('cmd_offer')
        with self.assertRaises(ValueError):validate({'actions':[bad]},64)

    def test_actual_sv_extra_acceptance_or_withdrawal_is_rejected(self):
        folder=BASE/'preflight-v3/calibration_partial_then_csid_switch/verilator'
        log=(folder/'simulation.log').read_text();aa=json.loads((folder/'requests.json').read_text())['actions']
        rows,states=parse(log,aa)
        # Extra acceptance in accounting must fail independently of DUT checker.
        line=next(s for s in log.splitlines() if s.startswith('QUEUE 8 '))
        values=line.split();values[4]='999'
        with self.assertRaises(ValueError):parse(log.replace(line,' '.join(values)),aa)
        # Request intent differs although an extra command could be legal at pins.
        corrupted=copy.deepcopy(aa);corrupted[12].update(cmd_offer=1,read=1)
        with self.assertRaises(ValueError):parse(log,corrupted)

    def test_errors_keep_stage_and_message(self):
        for name in ('transport','coverage','checker_worker'):
            with tempfile.TemporaryDirectory() as d:
                def fail():raise ValueError('deliberate offline test failure')
                with self.assertRaises(SafeExecutionError) as raised:checked_stage(Path(d),name,fail)
                self.assertEqual(raised.exception.stage,name)
                record=json.loads((Path(d)/'failure.json').read_text())
                self.assertEqual(record['stage'],name);self.assertIn('deliberate',record['detail'])

if __name__=='__main__':unittest.main()
