"""P04-R1 regression plus all inherited v1 binding/failure tests against v2."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
import tempfile
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'scripts'),str(Path(__file__).parent)]
import test_controller_done_ledger_audit_v1 as original_tests
from controller_done_ledger_audit_v1 import validate_ledger as old_validate
from controller_done_ledger_audit_v2 import validate_ledger, Evidence

ROOT=Path(__file__).resolve().parents[2]
AUTHORITY=ROOT/'docs/audits/agent_bridge_2026-11-06/P04_ledger/fixture_records.json'
AUTHORITY_SHA='c12eda95b03c76ef2109aab13f68f59488a3e363e505ef681c3443a4d17414d1'


def reviewer_fixture(bind_response=True):
    raw=AUTHORITY.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=AUTHORITY_SHA:raise ValueError('P04 fixture authority changed')
    f=copy.deepcopy(next(x['fixture'] for x in json.loads(raw)['fixtures'] if x['name']=='API_requests_after_resource_halt'))
    snapshots={tuple(row['key']):row['value'] for row in f['snapshots']}
    if bind_response:snapshots[('B',1,1)]['response']=copy.deepcopy(f['calls'][-1]['parsed'])
    return f['calls'],f['events'],snapshots,f['policy'],f['schema_digest']


def not_run():
    calls,events,snapshots,policy,schema=reviewer_fixture(False)
    c=calls[-1];c.update(status='not_run_resource_halt',count_request_issued=False,generation_request_issued=False,accepted_response=False)
    for k in ('usage','raw_usage','response_id','parsed'):c[k]=None
    return calls,events[:3],snapshots,policy,schema


class LedgerAuditV2Tests(original_tests.LedgerAuditTests):
    # The inherited 22 tests now exercise the new implementation, not old v1.
    def audit(self,f):return validate_ledger(*f,'schema')

    def test_file_missing_truncated_modified_and_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);e=Evidence(root);p=root/'saved.json';p.write_text('{"a":1}')
            h=hashlib.sha256(p.read_bytes()).hexdigest();e.bind(root,{'saved.json':h})
            p.write_text('{"a":2}');self.assertRaisesRegex(ValueError,'hash mismatch',e.bind,root,{'saved.json':h})
            p.write_text('{"a":');self.assertRaises(ValueError,e.load,p)
            self.assertRaises(OSError,e.load,root/'missing.json')
            self.assertRaisesRegex(ValueError,'allowlist',e.path,root,'../escape.json')
            self.assertRaisesRegex(ValueError,'allowlist',e.path,root,'build/private/key')

    def test_exact_P04_saved_counterexample_rejects_on_halt(self):
        with self.assertRaisesRegex(ValueError,'after persistent resource_halt'):validate_ledger(*reviewer_fixture(False))

    def test_P04_bound_copy_reproduces_v1_false_pass_and_v2_rejects(self):
        f=reviewer_fixture();self.assertEqual(old_validate(*copy.deepcopy(f))['status'],'PASS')
        with self.assertRaisesRegex(ValueError,'after persistent resource_halt'):validate_ledger(*f)

    def test_exact_saved_fixture_binding_discrepancy_is_preserved(self):
        # P04's saved snapshot is null, so exact v1 replay differs from its recorded PASS.
        with self.assertRaisesRegex(ValueError,'response/snapshot'):old_validate(*reviewer_fixture(False))

    def test_halt_global_across_round_and_session(self):
        for field,value in [('round',2),('session_id','second-session'),('arm','C')]:
            with self.subTest(field=field):
                calls,events,snaps,policy,schema=reviewer_fixture();c=calls[1];c[field]=value;c['attempt']=1
                ctx=events[5]['context'];ctx[field]=value
                oldkey=('B',1,1);snaps[oldkey]['response']=None;newkey=(c['arm'],c['repetition'],c['round'])
                # Distinct-session test uses another repetition to preserve a unique round key.
                if field=='session_id':c['repetition']=ctx['repetition']=2;newkey=('B',2,1)
                new=copy.deepcopy(snaps[oldkey]);new.update({k:c[k] for k in ('arm','repetition','round','session_id')},response=copy.deepcopy(c['parsed']));snaps[newkey]=new
                with self.assertRaisesRegex(ValueError,'after persistent resource_halt'):validate_ledger(calls,events,snaps,policy,schema)

    def test_posthalt_flags_are_rejected_even_without_dispatch_events(self):
        for flag in ('count_request_issued','generation_request_issued'):
            f=not_run();f[0][-1][flag]=True
            with self.subTest(flag=flag),self.assertRaisesRegex(ValueError,'request flags after persistent resource_halt'):validate_ledger(*f)

    def test_posthalt_dispatch_rejected_even_when_request_flags_false(self):
        for event in ('count_dispatched','generation_dispatched'):
            f=not_run();f[1].append(dict(event=event))
            with self.subTest(event=event),self.assertRaisesRegex(ValueError,'dispatch after persistent resource_halt'):validate_ledger(*f)

    def test_orphan_dispatch_after_last_halted_call_rejected(self):
        f=not_run();f[0].pop();f[1].append(dict(event='count_dispatched'))
        with self.assertRaisesRegex(ValueError,'dispatch after persistent resource_halt'):validate_ledger(*f)

    def test_legal_halt_then_only_NOT_RUN_is_representable(self):
        r=validate_ledger(*not_run());self.assertEqual(r['status'],'PASS');self.assertTrue(r['persistent_resource_halt']);self.assertEqual(len(r['resource_halt_events']),1);self.assertEqual(r['dispatched_counts'],1);self.assertEqual(r['dispatched_generations'],0)
        self.assertIsNone(r['attempts'][-1]['actual_tokens']);self.assertIsNone(r['provider_invoice_usd']);self.assertIsNone(r['count_endpoint_actual_usd'])

    def test_posthalt_payload_or_non_NOT_RUN_status_rejected(self):
        for key,value in [('usage',{}),('raw_usage',{}),('response_id','fake'),('parsed',{'body':'fake'})]:
            f=not_run();f[0][-1][key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'payload/usage after resource_halt'):validate_ledger(*f)
        f=not_run();f[0][-1]['status']='request_or_infrastructure_error'
        with self.assertRaisesRegex(ValueError,'only NOT_RUN'):validate_ledger(*f)

    def test_transport_failure_halt_keeps_missing_usage_unknown(self):
        calls,events,snaps,policy=original_tests.fixture();c=calls[0];c.update(status='request_or_infrastructure_error',accepted_response=False,error_type='TimeoutError');snaps[('B',1,1)]['response']=None
        for k in ('usage','raw_usage','response_id','parsed'):c.pop(k)
        events[3]=dict(event='generation_error',error_type='TimeoutError',usage_status='UNKNOWN_NOT_ZERO');events.append(dict(event='resource_halt',reason='explicit halt after transport error'))
        later=copy.deepcopy(c);later.update(attempt=2,status='not_run_resource_halt',count_request_issued=False,generation_request_issued=False);calls.append(later)
        r=validate_ledger(calls,events,snaps,policy,'schema');self.assertEqual(r['status'],'UNRESOLVED');self.assertTrue(r['persistent_resource_halt']);self.assertEqual(r['known_usage_token_totals'],{});self.assertIsNone(r['attempts'][0]['actual_tokens'])


if __name__=='__main__':unittest.main()
