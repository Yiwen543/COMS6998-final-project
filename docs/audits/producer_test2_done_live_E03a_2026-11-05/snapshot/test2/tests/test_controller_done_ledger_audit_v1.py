"""Adversarial offline ledger fixtures, independent of the historical 36x4 shape."""
import copy
import sys
import tempfile
import hashlib
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from controller_done_ledger_audit_v1 import validate_ledger, Evidence


def fixture():
    usage = dict(input_tokens=10, output_tokens=2, total_tokens=12, cached_input_tokens=3, reasoning_output_tokens=1)
    policy = dict(model='model', service_tier='default', input_tokens=20, output_tokens=8,
                  max_precounts=4, max_generations=4, manual_failure_retries_per_round=1,
                  per_generation_conservative_reserve_usd=.1, generation_reserve_usd=.4,
                  count_fee_reserve_usd=.1, total_stage_spending_ceiling_usd=.5)
    ctx = dict(arm='B', repetition=1, round=1, mode='live', session_id='own')
    c = dict(ctx, attempt=1, count_request_issued=True, generation_request_issued=True,
             accepted_response=True, prompt_sha256='file-sha', status='completed', input_token_count=10,
             requested_model='model', returned_model='model', response_id='resp-1',
             requested_service_tier='default', returned_service_tier='default', usage=usage,
             raw_usage=dict(input_tokens=10, output_tokens=2, total_tokens=12,
                            input_tokens_details=dict(cached_tokens=3, cache_write_tokens=7,
                                                     cache_write_tokens_details=dict(ttl_30m_tokens=7, ttl_12h_tokens=0)),
                            output_tokens_details=dict(reasoning_tokens=1)), parsed={'body':'x'})
    ev = [dict(event='count_dispatched', messages_sha256='message-sha', model='model', schema_sha256='schema'),
          dict(event='count_returned', messages_sha256='message-sha', input_tokens=10),
          dict(event='generation_dispatched', messages_sha256='message-sha', input_tokens_counted=10,
               max_output_tokens=8, requested_service_tier='default', reserve_usd=.1, cumulative_reserve_usd=.1, context=ctx.copy()),
          dict(event='generation_returned', response_id='resp-1', returned_model='model', returned_service_tier='default', usage=copy.deepcopy(usage))]
    snap = {('B',1,1):dict(ctx, prompt_sha256='file-sha', messages_sha256='message-sha', response={'body':'x'})}
    return [c], ev, snap, policy


class LedgerAuditTests(unittest.TestCase):
    def audit(self, f):
        return validate_ledger(*f, 'schema')

    def test_small_success_not_hardcoded_cohort(self):
        r=self.audit(fixture());self.assertEqual(r['status'],'PASS');self.assertEqual(r['known_usage_token_totals']['total_tokens'],12)

    def test_missing_returned_rejected_for_success(self):
        f=fixture();f[1].pop();self.assertRaisesRegex(ValueError,'missing generation returned',self.audit,f)

    def test_duplicate_returned_is_orphan(self):
        f=fixture();f[1].append(copy.deepcopy(f[1][-1]));self.assertRaisesRegex(ValueError,'orphan',self.audit,f)

    def test_duplicate_call_identity(self):
        f=fixture();f[0].append(copy.deepcopy(f[0][0]));self.assertRaises(ValueError,self.audit,f)

    def test_cross_session_dispatch(self):
        f=fixture();f[1][2]['context']['session_id']='other';self.assertRaisesRegex(ValueError,'context',self.audit,f)

    def test_call_session_mismatch(self):
        f=fixture();f[0][0]['session_id']='other';self.assertRaisesRegex(ValueError,'session',self.audit,f)

    def test_prompt_digest_and_schema(self):
        for index,field in [(0,'messages_sha256'),(1,'messages_sha256'),(2,'messages_sha256'),(0,'schema_sha256')]:
            with self.subTest(index=index,field=field):
                f=fixture();f[1][index][field]='wrong';self.assertRaises(ValueError,self.audit,f)

    def test_response_usage_model_tier_count_mismatches(self):
        for field,value in [('response_id','wrong'),('usage',{}),('returned_model','wrong'),('returned_service_tier','priority')]:
            with self.subTest(field=field):
                f=fixture();f[1][3][field]=value;self.assertRaisesRegex(ValueError,'returned/call',self.audit,f)
        f=fixture();f[1][1]['input_tokens']=11;self.assertRaisesRegex(ValueError,'count',self.audit,f)

    def test_both_sides_wrong_model_or_tier_still_rejected(self):
        for field in ['returned_model','returned_service_tier']:
            f=fixture();f[0][0][field]=f[1][3][field]='wrong';self.assertRaises(ValueError,self.audit,f)

    def test_subset_arithmetic_and_raw_usage(self):
        for field,value in [('cached_input_tokens',11),('reasoning_output_tokens',3),('total_tokens',13)]:
            f=fixture();f[0][0]['usage'][field]=f[1][3]['usage'][field]=value;self.assertRaises(ValueError,self.audit,f)
        f=fixture();f[0][0]['raw_usage']['input_tokens']=99;self.assertRaisesRegex(ValueError,'raw',self.audit,f)

    def test_resource_caps_reserve(self):
        for change in ['quota','reserve','output','retry']:
            f=fixture()
            if change=='quota':f[3]['max_generations']=0
            if change=='reserve':f[1][2]['cumulative_reserve_usd']=.2
            if change=='output':f[1][2]['max_output_tokens']=9
            if change=='retry':f[0][0]['attempt']=2
            self.assertRaises(ValueError,self.audit,f)

    def test_long_cache_write_not_silently_accepted(self):
        f=fixture();f[0][0]['raw_usage']['input_tokens_details']['cache_write_tokens_details']={'ttl_12h_tokens':7};self.assertRaisesRegex(ValueError,'long cache',self.audit,f)

    def test_failed_generation_missing_usage_is_unknown_not_zero(self):
        f=fixture();c=f[0][0];c.update(status='request_or_infrastructure_error',accepted_response=False,error_type='TimeoutError');
        for k in ['usage','raw_usage','response_id','parsed']:c.pop(k)
        f[2][('B',1,1)]['response']=None;f[1][3]=dict(event='generation_error',error_type='TimeoutError',usage_status='UNKNOWN_NOT_ZERO')
        r=self.audit(f);self.assertEqual(r['status'],'UNRESOLVED');self.assertIsNone(r['attempts'][0]['actual_tokens']);self.assertEqual(r['missing_generation_usage'],1);self.assertEqual(r['known_usage_token_totals'],{})

    def test_failed_count_does_not_require_four_events(self):
        f=fixture();c=f[0][0];c.update(status='request_or_infrastructure_error',accepted_response=False,generation_request_issued=False,error_type='TimeoutError')
        for k in ['usage','raw_usage','response_id','parsed','input_token_count']:c.pop(k)
        f[2][('B',1,1)]['response']=None;f[1][:]=[f[1][0],dict(event='count_error',error_type='TimeoutError')]
        r=self.audit(f);self.assertEqual(r['status'],'UNRESOLVED');self.assertEqual(r['dispatched_generations'],0)

    def test_transport_error_without_terminal_remains_unresolved(self):
        f=fixture();c=f[0][0];c.update(status='request_or_infrastructure_error',accepted_response=False)
        for k in ['usage','raw_usage','response_id','parsed']:c.pop(k)
        f[2][('B',1,1)]['response']=None;f[1].pop();self.assertEqual(self.audit(f)['status'],'UNRESOLVED')

    def test_returned_rejected_response_without_usage_is_unknown(self):
        f=fixture();c=f[0][0];c.update(status='model_response_error',accepted_response=False,usage=None);f[1][3]['usage']=None;c.pop('raw_usage');f[2][('B',1,1)]['response']=None
        self.assertEqual(self.audit(f)['status'],'UNRESOLVED')

    def test_accepted_response_without_usage_rejected(self):
        f=fixture();f[0][0]['usage']=f[1][3]['usage']=None;self.assertRaisesRegex(ValueError,'missing actual usage',self.audit,f)

    def test_unknown_status_or_missing_call_cannot_pass(self):
        f=fixture();f[0][0]['status']='unknown';self.assertRaisesRegex(ValueError,'unsupported call status',self.audit,f)
        f=fixture();f[0].clear();f[1].clear();self.assertRaisesRegex(ValueError,'no call',self.audit,f)

    def test_success_after_transport_retry(self):
        good=fixture();f=copy.deepcopy(good);c=f[0][0];c.update(status='request_or_infrastructure_error',accepted_response=False,error_type='TimeoutError')
        for k in ['usage','raw_usage','response_id','parsed']:c.pop(k)
        f[1][3]=dict(event='generation_error',error_type='TimeoutError',usage_status='UNKNOWN_NOT_ZERO')
        retry=copy.deepcopy(good[0][0]);retry['attempt']=2;f[0].append(retry)
        ev=copy.deepcopy(good[1]);ev[2]['cumulative_reserve_usd']=.2;f[1].extend(ev)
        r=self.audit(f);self.assertEqual(r['status'],'UNRESOLVED');self.assertEqual(r['dispatched_generations'],2);self.assertEqual(r['known_usage_token_totals']['total_tokens'],12)

    def test_duplicate_response_id_across_distinct_sessions(self):
        f=fixture();second=fixture();c=second[0][0];c.update(arm='C',session_id='other')
        second[1][2]['context'].update(arm='C',session_id='other');second[1][2]['cumulative_reserve_usd']=.2
        snap=second[2].pop(('B',1,1));snap.update(arm='C',session_id='other');f[2][('C',1,1)]=snap
        f[0].append(c);f[1].extend(second[1]);self.assertRaisesRegex(ValueError,'response identity',self.audit,f)

    def test_file_missing_truncated_modified_and_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);e=Evidence(root);p=root/'saved.json';p.write_text('{"a":1}')
            h=hashlib.sha256(p.read_bytes()).hexdigest();e.bind(root,{'saved.json':h})
            p.write_text('{"a":2}');self.assertRaisesRegex(ValueError,'hash mismatch',e.bind,root,{'saved.json':h})
            p.write_text('{"a":');self.assertRaises(ValueError,e.load,p)
            self.assertRaises(OSError,e.load,root/'missing.json')
            self.assertRaisesRegex(ValueError,'allowlist',e.path,root,'../escape.json')
            self.assertRaisesRegex(ValueError,'allowlist',e.path,root,'build/private/key')

    def test_noninterleaving_contract_rejects_orphan_count(self):
        f=fixture();f[1].insert(1,copy.deepcopy(f[1][0]));self.assertRaises(ValueError,self.audit,f)


if __name__=='__main__':unittest.main()
