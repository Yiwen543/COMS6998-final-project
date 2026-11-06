import copy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from controller_done_model_v1 import BoundedModel,MAX_GENERATIONS,RESERVE_PER_GENERATION
from pilot_model import ModelResponseError
import controller_done_generate_v1 as runner

CFG=dict(model='gpt-6.1-sol',reasoning_effort='low',timeout_seconds=120,max_output_tokens=8192)


class GenerationV1Tests(unittest.TestCase):
    def client(self,n=100):
        c=Mock();c.responses.input_tokens.count.return_value=SimpleNamespace(input_tokens=n)
        c.responses.create.return_value=SimpleNamespace(model='gpt-6.1-sol',id='unit_fake_response',status='completed',incomplete_details=None,
            service_tier='default',usage=dict(input_tokens=n,output_tokens=20,total_tokens=n+20,input_tokens_details=dict(cached_tokens=10),output_tokens_details=dict(reasoning_tokens=4)),output_text=json.dumps(runner.plumbing(3)))
        return c

    def model(self,t,client,**kw):return BoundedModel(CFG,runner.SCHEMA,'controller_done_monitor',Path(t)/'dispatch.jsonl',client=client,**kw)

    def test_standard_tier_no_store_same_schema_and_known_usage(self):
        with tempfile.TemporaryDirectory() as t:
            c=self.client();m=self.model(t,c);msgs=[dict(role='user',content='unit')];m.count_input_tokens(msgs);r=m.generate(msgs,{})
            kw=c.responses.create.call_args.kwargs
            self.assertEqual(kw['service_tier'],'default');self.assertFalse(kw['store']);self.assertEqual(kw['max_output_tokens'],8192);self.assertEqual(kw['prompt_cache_retention'],'in_memory')
            self.assertEqual(kw['text'],c.responses.input_tokens.count.call_args.kwargs['text']);self.assertEqual(r['usage']['total_tokens'],120)

    def test_overcap_or_changed_payload_never_dispatches_generation(self):
        for n,changed in ((64001,False),(100,True)):
            with tempfile.TemporaryDirectory() as t:
                c=self.client(n);m=self.model(t,c);m.count_input_tokens(['unit'])
                with self.assertRaises(ValueError):m.generate(['changed'] if changed else ['unit'],{})
                self.assertEqual(c.responses.create.call_count,0);self.assertEqual(m.dispatched()['generations'],0)

    def test_actual_usage_mismatch_halts_and_preserves_paid_usage(self):
        with tempfile.TemporaryDirectory() as t:
            c=self.client();c.responses.create.return_value.usage['input_tokens']=101;c.responses.create.return_value.usage['total_tokens']=121;m=self.model(t,c);m.count_input_tokens(['unit'])
            with self.assertRaises(ModelResponseError) as error:m.generate(['unit'],{})
            self.assertEqual(error.exception.record['usage']['input_tokens'],101)
            with self.assertRaises(ValueError):m.count_input_tokens(['unit'])
            self.assertEqual(c.responses.input_tokens.count.call_count,1);self.assertEqual(m.dispatched()['generations'],1)

    def test_missing_usage_is_unknown_not_zero(self):
        with tempfile.TemporaryDirectory() as t:
            c=self.client();c.responses.create.return_value.usage=None;m=self.model(t,c);m.count_input_tokens(['unit'])
            with self.assertRaises(ModelResponseError) as error:m.generate(['unit'],{})
            self.assertIsNone(error.exception.record['usage']['total_tokens']);self.assertIsNotNone(m.halted)

    def test_returned_model_or_tier_and_invalid_subset_halt(self):
        for field in ('model','tier','cached'):
            with tempfile.TemporaryDirectory() as t:
                c=self.client();response=c.responses.create.return_value
                if field=='model':response.model='other'
                elif field=='tier':response.service_tier='priority'
                else:response.usage['input_tokens_details']['cached_tokens']=101
                m=self.model(t,c);m.count_input_tokens(['unit'])
                with self.assertRaises(ModelResponseError):m.generate(['unit'],{})
                self.assertIsNotNone(m.halted)

    def test_transport_failure_retains_dispatch_and_quota_across_reload(self):
        with tempfile.TemporaryDirectory() as t:
            c=self.client();c.responses.create.side_effect=RuntimeError('unit transport failure');m=self.model(t,c,max_generations=1);m.count_input_tokens(['unit'])
            with self.assertRaises(RuntimeError):m.generate(['unit'],{})
            m=self.model(t,c,max_generations=1);m.count_input_tokens(['unit'])
            with self.assertRaises(ValueError):m.generate(['unit'],{})
            self.assertEqual(c.responses.create.call_count,1)
            events=[json.loads(s) for s in (Path(t)/'dispatch.jsonl').read_text().splitlines()];self.assertEqual(sum(e['event']=='generation_dispatched' for e in events),1)

    def test_precount_cannot_be_reused_for_a_second_attempt(self):
        with tempfile.TemporaryDirectory() as t:
            c=self.client();m=self.model(t,c);m.count_input_tokens(['unit']);m.generate(['unit'],{})
            with self.assertRaises(ValueError):m.generate(['unit'],{})
            self.assertEqual(c.responses.create.call_count,1)

    def test_existing_authorizations_do_not_open_new_generation(self):
        with tempfile.TemporaryDirectory() as t,patch.object(runner,'model',side_effect=AssertionError('key/model must not be accessed')):
            with self.assertRaises(ValueError):runner.execute('live',Path(t)/'live')

    def test_preflight_prompt_payloads_unchanged_and_reserve_bounded(self):
        from controller_done_loop_v2 import count_messages
        self.assertEqual(runner.count_messages(),count_messages());self.assertLessEqual(MAX_GENERATIONS*RESERVE_PER_GENERATION,30)

    def test_offline_injected_API_halt_freezes_all36_without_phantom_calls(self):
        from controller_release_live import verify_release
        with tempfile.TemporaryDirectory() as t:
            out=Path(t)/'unit_fake_live';c=self.client();c.responses.create.return_value.usage.update(input_tokens=101,total_tokens=121)
            model=BoundedModel(CFG,runner.SCHEMA,'controller_done_monitor',out/'api-dispatch.jsonl',client=c)
            freeze=Path(t)/'unit-freeze.json';grant=Path(t)/'unit-grant.json';freeze.write_text('{}');grant.write_text('{}')
            with patch.object(runner,'live_gate'),patch.object(runner,'model',return_value=model),patch.object(runner,'LIVE_FREEZE',freeze),patch.object(runner,'APPROVAL',grant):result=runner.execute('live',out)
            self.assertEqual(result['frozen_rounds'],36);self.assertEqual(len(verify_release(out)),36)
            self.assertEqual(result['generation_requests'],1);self.assertEqual(result['count_requests'],1)
            self.assertEqual(c.responses.create.call_count,1);self.assertEqual(c.responses.input_tokens.count.call_count,1)
            finals=json.loads((out/'final-candidates.json').read_text());self.assertTrue(all(c['status']=='invalid' for c in finals['candidates']))


if __name__=='__main__':unittest.main()
