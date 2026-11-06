"""Read-only, serialized saved API ledger validation. No model/tool execution.

PASS means saved ledger consistency, never provider billing completeness or monitor
correctness. Transport/usage gaps remain UNRESOLVED. CLI refuses output overwrite.
"""
import argparse
import ast
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def identity(row):
    return tuple(row[k] for k in ('arm', 'repetition', 'round'))


def validate_ledger(calls, events, snapshots, policy, schema_digest):
    """Validate one *serialized* producer ledger, including rejected attempts.

    Count terminals and generation terminals lack context in this historical
    format. Bind by the strict serialized state machine, then require generation
    dispatch context and each call to match the frozen round/session/prompt.
    Concurrent/interleaved event ledgers are unsupported and rejected.
    """
    cursor = counts = generations = 0
    seen_calls, response_ids, accepted = set(), set(), set()
    attempts = Counter()
    rows, unresolved, totals = [], [], Counter()

    def take(kind):
        nonlocal cursor
        need(cursor < len(events), 'missing event: ' + kind)
        event = events[cursor]
        need(event.get('event') == kind, 'expected ' + kind + ' at event ' + str(cursor))
        cursor += 1
        return event

    def terminal(returned, error):
        nonlocal cursor
        if cursor == len(events) or events[cursor].get('event') == 'count_dispatched':
            return None  # caller must retain the missing terminal as unresolved
        name = events[cursor].get('event')
        if name in (returned, error):
            cursor += 1
            return events[cursor - 1]
        return None  # resource_halt is consumed after the attempt

    for index, call in enumerate(calls):
        key = identity(call)
        need(key in snapshots, 'call round has no frozen snapshot')
        snap = snapshots[key]
        need(all(call.get(k) == snap.get(k) for k in ('mode', 'session_id')), 'call session/mode mismatch')
        need(call.get('prompt_sha256') == snap['prompt_sha256'], 'call prompt file digest mismatch')
        attempt = call.get('attempt')
        need(type(attempt) is int and attempt == attempts[key] + 1, 'duplicate/nonconsecutive attempt identity')
        need(attempt <= policy['manual_failure_retries_per_round'] + 1, 'retry cap exceeded')
        uid = key + (attempt,)
        need(uid not in seen_calls and key not in accepted, 'duplicate attempt or attempt after acceptance')
        seen_calls.add(uid)
        attempts[key] += 1
        need(type(call.get('count_request_issued')) is bool and type(call.get('generation_request_issued')) is bool, 'request flags missing/nonboolean')
        need(type(call.get('accepted_response')) is bool, 'acceptance flag missing/nonboolean')
        need(call.get('status') in ('completed', 'model_response_error', 'request_or_infrastructure_error', 'input_cap_exceeded_no_generation', 'not_run_resource_halt'), 'unsupported call status')
        need((call.get('status') == 'completed') == call['accepted_response'], 'completion/acceptance status mismatch')
        item = dict(call_index=index, identity=list(uid), session_id=call['session_id'], status=call.get('status'), usage_status='NOT_DISPATCHED', actual_tokens=None)
        count = None
        if call['count_request_issued']:
            counts += 1
            need(counts <= policy['max_precounts'], 'count quota exceeded')
            dispatched = take('count_dispatched')
            need(dispatched.get('messages_sha256') == snap['messages_sha256'], 'count prompt/context digest mismatch')
            need(dispatched.get('model') == policy['model'], 'count model mismatch')
            need(dispatched.get('schema_sha256') == schema_digest, 'count schema mismatch')
            done = terminal('count_returned', 'count_error')
            if done and done['event'] == 'count_returned':
                count = done.get('input_tokens')
                need(type(count) is int and count > 0, 'invalid returned count')
                need(done.get('messages_sha256') == snap['messages_sha256'], 'returned count digest mismatch')
                need(call.get('input_token_count') == count, 'call count mismatch')
            elif done:
                need(call.get('error_type') == done.get('error_type'), 'count error mismatch')
                unresolved.append(dict(identity=list(uid), reason='count transport failure; count fee UNKNOWN'))
            else:
                unresolved.append(dict(identity=list(uid), reason='count terminal missing; provider count/fee UNKNOWN'))
        need(not call['generation_request_issued'] or count is not None, 'generation without valid same-attempt precount')
        if call['generation_request_issued']:
            generations += 1
            need(generations <= policy['max_generations'], 'generation quota exceeded')
            dispatched = take('generation_dispatched')
            context = dispatched.get('context', {})
            need(all(context.get(k) == call.get(k) for k in ('arm', 'repetition', 'round', 'mode', 'session_id')), 'dispatch/call context mismatch')
            need(dispatched.get('messages_sha256') == snap['messages_sha256'], 'generation prompt digest mismatch')
            need(dispatched.get('input_tokens_counted') == count <= policy['input_tokens'], 'generation input count/cap mismatch')
            need(dispatched.get('max_output_tokens') == policy['output_tokens'], 'generation output cap mismatch')
            need(dispatched.get('requested_service_tier') == policy['service_tier'], 'dispatch requested tier mismatch')
            reserve = Decimal(str(policy['per_generation_conservative_reserve_usd']))
            need(Decimal(str(dispatched.get('reserve_usd'))) == reserve, 'per-call reserve mismatch')
            need(Decimal(str(dispatched.get('cumulative_reserve_usd'))).quantize(Decimal('.00000001')) == (generations * reserve).quantize(Decimal('.00000001')), 'cumulative reserve mismatch')
            need(generations * reserve <= Decimal(str(policy['generation_reserve_usd'])), 'generation monetary reserve exceeded')
            done = terminal('generation_returned', 'generation_error')
            if done and done['event'] == 'generation_returned':
                rid = done.get('response_id')
                need(isinstance(rid, str) and rid and rid not in response_ids, 'missing/duplicate response identity')
                response_ids.add(rid)
                for field in ('response_id', 'usage', 'returned_model', 'returned_service_tier'):
                    need(field in call and call[field] == done.get(field), 'returned/call mismatch: ' + field)
                need(call.get('requested_model') == call.get('returned_model') == policy['model'], 'returned/requested model mismatch')
                need(call.get('requested_service_tier') == policy['service_tier'], 'call requested tier mismatch')
                need(call.get('returned_service_tier') in (None, policy['service_tier']), 'returned tier mismatch')
                usage = call.get('usage')
                base = ('input_tokens', 'output_tokens', 'total_tokens')
                known = isinstance(usage, dict) and all(type(usage.get(k)) is int and usage[k] >= 0 for k in base)
                if known:
                    need(usage['input_tokens'] == count and usage['output_tokens'] <= policy['output_tokens'], 'usage/count/output cap mismatch')
                    need(usage['total_tokens'] == usage['input_tokens'] + usage['output_tokens'], 'usage arithmetic mismatch')
                    for subset, total in [('cached_input_tokens', 'input_tokens'), ('reasoning_output_tokens', 'output_tokens')]:
                        value = usage.get(subset)
                        need(value is None or type(value) is int and 0 <= value <= usage[total], 'usage subset mismatch: ' + subset)
                    raw = call.get('raw_usage')
                    if isinstance(raw, dict):
                        need(all(raw.get(k) == usage[k] for k in base), 'raw/normalized usage mismatch')
                        inp, out = raw.get('input_tokens_details') or {}, raw.get('output_tokens_details') or {}
                        need(inp.get('cached_tokens') == usage.get('cached_input_tokens'), 'raw cached subset mismatch')
                        need(out.get('reasoning_tokens') == usage.get('reasoning_output_tokens'), 'raw reasoning subset mismatch')
                        write = inp.get('cache_write_tokens')
                        if write is not None:
                            need(type(write) is int and 0 <= write <= usage['input_tokens'] - (usage.get('cached_input_tokens') or 0), 'raw cache write invalid')
                            detail = inp.get('cache_write_tokens_details')
                            if isinstance(detail, dict):
                                need(detail.get('ttl_12h_tokens', 0) == 0, 'unexpected long cache write')
                                need(sum(detail.values()) == write, 'cache write detail sum mismatch')
                    else:
                        unresolved.append(dict(identity=list(uid), reason='raw usage unavailable; cache accounting UNKNOWN'))
                    item.update(usage_status='KNOWN', actual_tokens=usage['total_tokens'])
                    totals.update({k: usage[k] for k in base})
                else:
                    need(not call['accepted_response'] and call.get('status') != 'completed', 'successful response missing actual usage')
                    item['usage_status'] = 'UNKNOWN_NOT_ZERO'
                    unresolved.append(dict(identity=list(uid), reason='returned response lacks valid actual usage'))
            else:
                need(not call['accepted_response'] and call.get('status') != 'completed', 'successful call missing generation returned')
                need(call.get('usage') is None and call.get('response_id') is None, 'terminal missing/error but call claims returned data')
                if done:
                    need(call.get('error_type') == done.get('error_type'), 'generation error mismatch')
                    need(done.get('usage_status') == 'UNKNOWN_NOT_ZERO', 'generation error must preserve unknown usage')
                item['usage_status'] = 'UNKNOWN_NOT_ZERO'
                unresolved.append(dict(identity=list(uid), reason='generation error or terminal missing; usage UNKNOWN_NOT_ZERO'))
        else:
            need(not call['accepted_response'] and call.get('usage') is None, 'undispatched call claims accepted/usage data')
        while cursor < len(events) and events[cursor].get('event') == 'resource_halt':
            item.setdefault('resource_halts', []).append(events[cursor].get('reason'))
            cursor += 1
            need(not call['accepted_response'], 'accepted response with resource halt')
        if call['accepted_response']:
            need(call.get('status') == 'completed' and call.get('parsed') == snap['response'], 'accepted response/snapshot mismatch')
            accepted.add(key)
        rows.append(item)
    need(cursor == len(events), 'unmatched/orphan ledger events')
    need(set(attempts) == set(snapshots), 'snapshot has no call attempt')
    need(all((snap['response'] is not None) == (key in accepted) for key, snap in snapshots.items()), 'snapshot response has no unique accepted call')
    reserve = generations * Decimal(str(policy['per_generation_conservative_reserve_usd']))
    need(reserve + Decimal(str(policy['count_fee_reserve_usd'])) <= Decimal(str(policy['total_stage_spending_ceiling_usd'])), 'stage reserve exceeded')
    return dict(status='UNRESOLVED' if unresolved else 'PASS', call_rows=len(calls), event_rows=len(events), dispatched_counts=counts, dispatched_generations=generations, unique_returned_responses=len(response_ids), known_usage_token_totals=dict(totals), missing_generation_usage=sum(r['usage_status']=='UNKNOWN_NOT_ZERO' for r in rows), unresolved=unresolved, attempts=rows, provider_invoice_usd=None, count_endpoint_actual_usd=None, claim_scope='Serialized saved-ledger consistency only; no provider invoice or scientific result validation.')


class Evidence:
    def __init__(self, root):
        self.root = root.resolve()
        self.files = {}

    def path(self, base, name):
        p = (base / name).resolve()
        need(p.is_relative_to(base.resolve()) and p.is_relative_to(self.root) and not p.is_relative_to(self.root/'build/private'), 'evidence path escapes allowlist')
        return p

    def load(self, path):
        p = path.resolve()
        need(p.is_relative_to(self.root) and not p.is_relative_to(self.root/'build/private'), 'read outside evidence allowlist')
        self.files[str(p.relative_to(self.root))] = digest(p)
        return json.loads(p.read_text())

    def bind(self, base, files):
        for name, expected in files.items():
            p = self.path(base, name)
            actual = digest(p)
            need(actual == expected, 'saved evidence hash mismatch: ' + name)
            self.files[str(p.relative_to(self.root))] = actual


def audit_saved(root, run):
    e = Evidence(root)
    cfg = root/'test2/configs'
    reg = e.load(cfg/'controller_done_generation_v2.json')
    grant = e.load(cfg/'controller_done_generation_authorization_v2.json')
    need(run.resolve() == (root/grant['run_directory']).resolve(), 'saved run outside authorized cohort')
    need(grant['registration_sha256'] == digest(cfg/'controller_done_generation_v2.json'), 'grant registration binding')
    need(grant['freeze_sha256'] == digest(cfg/'controller_done_generation_freeze_v2.json'), 'grant qualification binding')
    e.bind(root, e.load(cfg/'controller_done_generation_freeze_v2.json')['files'])
    rr = e.load(run/'resource-release.json')
    need(rr['authorization_sha256'] == digest(cfg/'controller_done_generation_authorization_v2.json'), 'resource grant binding')
    need(rr['generation_registration_sha256'] == grant['registration_sha256'] and rr['qualification_freeze_sha256'] == grant['freeze_sha256'], 'resource qualification/registration binding')
    e.bind(run, rr['files'])
    release = e.load(run/'release.json')
    e.bind(run, release['files'])
    need(release['mode'] == 'live' and release['all_rounds_frozen'] and not release['candidate_revision_allowed'], 'invalid live release')
    catalog = e.load(run/'all-round-candidates.json')
    snapshots = {}
    for entry in catalog['rounds']:
        p = e.path(run, entry['snapshot'])
        need(digest(p) == entry['sha256'], 'snapshot digest mismatch')
        snap = e.load(p)
        e.bind(run, snap['files'])
        d = e.path(run, snap['directory'])
        prompt, response = e.load(d/'prompt.json'), e.load(d/'response.json')
        key = identity(snap)
        need(key not in snapshots, 'duplicate snapshot identity')
        snapshots[key] = dict(snap, prompt_sha256=digest(d/'prompt.json'), messages_sha256=fingerprint(prompt), response=response, prompt=prompt, feedback=e.load(d/'development-feedback.json'))
    b = reg['budget']
    expected = {(a, rep, n) for a in b['arms'] for rep in range(1, b['repetitions']+1) for n in range(1, b['rounds']+1)}
    need(set(snapshots) == expected, 'registered snapshot inventory mismatch')
    ids = {}
    for arm in b['arms']:
        for rep in range(1, b['repetitions']+1):
            previous = feedback = None
            for n in range(1, b['rounds']+1):
                snap = snapshots[arm, rep, n]
                need(snap['mode'] == 'live', 'snapshot mode mismatch')
                sid = snap['session_id']
                need(ids.setdefault((arm, rep), sid) == sid, 'snapshot session drift')
                payload = json.loads(snap['prompt'][1]['content'])
                need(payload['round'] == n and payload['previous_candidate'] == previous and payload['development_feedback'] == feedback, 'prompt crosses own-history context')
                if snap['response'] is not None:
                    previous = snap['response']
                feedback = snap['feedback']
    need(len(set(ids.values())) == len(ids), 'session ID shared across independent sessions')
    # Parse the exact frozen literal schema, without importing an executable producer.
    schema_path = root/'test2/scripts/monitor.py'
    e.files[str(schema_path.relative_to(root))] = digest(schema_path)
    schema = next(ast.literal_eval(n.value) for n in ast.parse(schema_path.read_text()).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SCHEMA' for t in n.targets))
    def jsonl(p):
        e.files[str(p.relative_to(root))] = digest(p)
        return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]
    policy = reg['API_limits']
    for a, b in [('max_generation_requests', 'max_generations'), ('max_count_requests', 'max_precounts'), ('max_manual_failure_retries','manual_failure_retries_per_round'), ('model','model'), ('service_tier','service_tier'), ('generation_reserve_usd','generation_reserve_usd'), ('count_fee_reserve_usd','count_fee_reserve_usd'), ('total_stage_spending_ceiling_usd','total_stage_spending_ceiling_usd')]:
        need(grant[a] == policy[b], 'grant/resource policy mismatch: '+a)
    need(rr['resource_reserve_per_generation_usd'] == policy['per_generation_conservative_reserve_usd'], 'resource reserve rate binding')
    result = validate_ledger(jsonl(run/'calls.jsonl'), jsonl(run/'api-dispatch.jsonl'), snapshots, policy, fingerprint(schema))
    result['evidence_sha256'] = e.files
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', type=Path, default=ROOT/'test2/results/controller-done-live-v2')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    need(args.run.resolve().is_relative_to(ROOT/'test2/results'), 'run outside saved-result allowlist')
    need(args.out.resolve().is_relative_to(ROOT/'test2/results'), 'output outside versioned-result allowlist')
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    try:
        result = audit_saved(ROOT, args.run.resolve())
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
        result = dict(status='REJECT', error_type=type(error).__name__, reason=str(error))
    result.update(producer_sha256=digest(__file__), head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(), parse_wall_seconds=time.perf_counter()-start, no_api_or_simulator_executed=True)
    (args.out/'audit.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('status','call_rows','event_rows','dispatched_counts','dispatched_generations','parse_wall_seconds','reason')}))
    return 1 if result['status']=='REJECT' else 2 if result['status']=='UNRESOLVED' else 0


if __name__ == '__main__':
    raise SystemExit(main())
