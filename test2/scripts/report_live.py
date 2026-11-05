#!/usr/bin/env python3
"""Read-only post-run audit, descriptive tables and plots. Does not revise candidates."""
import argparse
import collections
import csv
import json
from pathlib import Path
import re
import statistics
from common import BASE,ROOT,dump,sha
from runner import live_gate
from final_score import verify_candidates,verify_reference
from feedback import messages

def readl(p):return [json.loads(s) for s in p.read_text().splitlines() if s]
def write_csv(path,rows):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['no_rows'])
        writer.writeheader();writer.writerows(rows)

def fixed_coverage():
    """Coverage is fixed input evidence, never a candidate-monitor reward."""
    table=[];targets=[]
    root=BASE/'results/preflight-v2/correct_stress/verilator'
    for split,names in [('development',('basic','boundary','wrap_reset')),
                        ('final',('final_boundary','final_wrap_reset','final_mixed'))]:
        corpora=[]
        for name in names:
            ps=json.loads((root/name/'coverage.json').read_text());corpora.append(ps)
            for p in ps:
                if p['type']=='branch' and p['outcome']=='if' and p['line'] in (91,161,96,129,179):
                    targets.append({'split':split,'trace':name,'source':p['source'],'line':p['line'],
                        'column':p['column'],'outcome':p['outcome'],'hits':p['hits']})
        ids=lambda ps:[{k:v for k,v in p.items() if k!='hits'} for p in ps]
        assert all(ids(ps)==ids(corpora[0]) for ps in corpora)
        union=[dict(p,hits=sum(ps[i]['hits'] for ps in corpora)) for i,p in enumerate(corpora[0])]
        for name,ps in list(zip(names,corpora))+[('union_of_fixed_traces',union)]:
            for typ in ('line','branch','expr','toggle'):
                selected=[p for p in ps if p['type']==typ]
                table.append({'split':split,'trace':name,'type':typ,
                    'covered_counters':sum(p['hits']>0 for p in selected),'denominator':len(selected),
                    'raw_counter_hit_sum':sum(p['hits'] for p in selected)})
    return table,targets

def audit_generation(run):
    live_gate(BASE/'configs/live_freeze_v1.json');verify_reference();verify_candidates(run)
    calls=readl(run/'calls.jsonl');rounds=readl(run/'rounds.jsonl')
    config=json.loads((BASE/'configs/registration_v1.json').read_text())
    expected={(a,p,r) for a in config['arms'] for p in (1,2,3) for r in range(1,7)}
    assert {(r['arm'],r['repetition'],r['round']) for r in rounds}==expected and len(rounds)==36
    latest={};feedback={};table=[];sums=collections.defaultdict(lambda:collections.Counter())
    for r in rounds:
        key=(r['arm'],r['repetition']);triple=(*key,r['round'])
        d=run/r['arm']/f'rep{r["repetition"]}'/f'round{r["round"]}'
        attempt=[c for c in calls if (c['arm'],c['repetition'],c['round'])==triple]
        assert 1<=len(attempt)<=2
        prompt=messages(r['arm'],BASE/'results/preflight-v2',r['round'],latest.get(key),feedback.get(key))
        assert prompt==json.loads((d/'prompt.json').read_text())
        for c in attempt:
            assert c['prompt_sha256']==sha(d/'prompt.json')
            assert c['settings']==config
            if c.get('input_token_count') is not None:assert c['input_token_count']<=32000
            if c.get('accepted_response'):assert c['requested_model']==c['returned_model']=='gpt-6.1-sol'
            u=c.get('usage') or {}
            if u.get('input_tokens') is not None:
                assert u['input_tokens']<=32000 and u['output_tokens']<=8192
                assert u['total_tokens']==u['input_tokens']+u['output_tokens']
                assert (u.get('cached_input_tokens') or 0)<=u['input_tokens']
                assert (u.get('reasoning_output_tokens') or 0)<=u['output_tokens']
                sums[key].update({k:u[k] or 0 for k in ('input_tokens','output_tokens','cached_input_tokens','reasoning_output_tokens')})
            sums[key]['generation_requests']+=int(c.get('generation_request_issued',False))
            sums[key]['count_requests']+=int(c.get('count_request_issued',False))
            sums[key]['generation_and_count_seconds']+=c['attempt_wall_seconds']
        accepted=[c for c in attempt if c.get('accepted_response')]
        if accepted:latest[key]=accepted[-1]['parsed']
        feedback[key]=r['feedback']
        samples=0;checks=0;alarms=0;unknown=0
        for name,dev in r['feedback'].get('development',{}).items():
            assert name in ('basic','boundary','wrap_reset')
            measured=json.loads((d/name/'result.json').read_text())
            raw=json.loads((d/name/'samples.json').read_text());samples+=measured['cycles']
            assert measured['samples']==len(raw)
            for j,p in enumerate(measured['properties']):
                a=sum(x['active'][5-j]=='1' and x['ok'][5-j] in '01' for x in raw)
                e=sum(x['active'][5-j]=='1' and x['ok'][5-j]=='0' for x in raw)
                z=sum(x['active'][5-j] not in '01' or (x['active'][5-j]=='1' and x['ok'][5-j] not in '01') for x in raw)
                assert (a,e,z)==(p['checks'],len(p['failures']),len(p['unknown']))
                checks+=a;alarms+=e;unknown+=z
        assert samples==r['replayed_cycles']
        sums[key]['compile_seconds']+=r.get('compile_seconds',0)
        sums[key]['monitor_replay_seconds']+=r.get('monitor_replay_seconds',0)
        sums[key]['replayed_cycles']+=r['replayed_cycles']
        sums[key]['monitor_replays']+=r['monitor_replays']
        sums[key]['compile_attempts']+=r['compile_attempts']
        sums[key]['development_wall_seconds']+=r['wall_seconds']
        total=sums[key]['input_tokens']+sums[key]['output_tokens']
        table.append({'arm':key[0],'repetition':key[1],'round':r['round'],
                      'status':r['feedback']['status'],'definite_property_comparisons':checks,
                      'alarm_records':alarms,'unknown_records':unknown,'cumulative_api_tokens':total,
                      'cumulative_replay_cycles':sums[key]['replayed_cycles'],
                      'cumulative_active_seconds':sums[key]['generation_and_count_seconds']+sums[key]['development_wall_seconds']})
    assert len({c['session_id'] for c in calls})==6
    manifest=json.loads((run/'final-candidates.json').read_text())
    for c in manifest['candidates']:
        successful=[r for r in rounds if r['arm']==c['arm'] and r['repetition']==c['repetition'] and r['feedback']['status']=='compiled']
        if successful:
            assert Path(c['candidate_dir']).parent.name==f'round{successful[-1]["round"]}'
    return calls,table,sums

def report(run,final,out):
    if not (final/'summary.json').exists():raise ValueError('Final scoring not complete')
    out.mkdir(parents=True,exist_ok=False)
    calls,rounds,totals=audit_generation(run)
    scores=json.loads((final/'scores.json').read_text());endpoints=[];formal=[];pairs=[];properties=[]
    oracle=json.loads((BASE/'reference/evaluation-v3/evaluations.json').read_text())['cases']
    for c in scores:
        key=(c['arm'],c['repetition']);cost=totals[key]
        tokens=cost['input_tokens']+cost['output_tokens']
        if c['status']!='evaluated':
            endpoints.append({'arm':key[0],'repetition':key[1],'simulator':'invalid','status':c['status'],
                'sound':False,'killed_mutants':0,'api_tokens':tokens});continue
        d=final/key[0]/f'rep{key[1]}'
        for sim,s in c['simulation'].items():
            # Independent direct recomputation from recorded bits and reference
            # outcomes, rather than trusting aggregate score fields alone.
            correct_alarms=0;correct_unknown=0;all_complete=True;detected=set();eligible=set()
            for control in ('correct_stress','correct_original','M01','M02','M03','M04','M05','M06'):
                for case in ('final_boundary','final_wrap_reset','final_mixed'):
                    path=d/sim/control/case
                    raw=json.loads((path/'samples.json').read_text())
                    result=json.loads((path/'result.json').read_text())
                    alarms=[(r['cycle'],r['phase']) for r in raw if any(a=='1' and b=='0' for a,b in zip(r['active'],r['ok']))]
                    unknown=sum(any(a not in '01' or a=='1' and b not in '01' for a,b in zip(r['active'],r['ok'])) for r in raw)
                    if control.startswith('correct'):
                        correct_alarms+=len(alarms);correct_unknown+=unknown;all_complete &= result['complete']
                    else:
                        truth=oracle[f'{control}/{sim}/{case}']
                        scored=next(x for x in s['details'] if x['mutant']==control and x['trace']==case)
                        raw_property_alarms=sum(a=='1' and b=='0' for r in raw for a,b in zip(r['active'],r['ok']))
                        raw_property_unknown=sum(a not in '01' or a=='1' and b not in '01' for r in raw for a,b in zip(r['active'],r['ok']))
                        assert raw_property_alarms==scored['raw_alarm_records']
                        assert scored['eligible']==(truth['verdict']=='FAIL' and bool(truth['failures']))
                        pairs.append({'arm':key[0],'repetition':key[1],'observation_simulator':sim,
                            'mutant':control,'trace':case,'reference_verdict':truth['verdict'],
                            'reference_unknown_retained':truth['verdict']=='UNRESOLVED',
                            'eligible':scored['eligible'],'candidate_complete':result['complete'],
                            'candidate_alarm_records':raw_property_alarms,'candidate_unknown_records':raw_property_unknown,
                            'candidate_unresolved':scored['unresolved'],'valid_kill':scored['valid_kill'],
                            'first_reference_violation':str(truth['failures'][0]) if truth['failures'] else None})
                        if truth['verdict']=='FAIL' and truth['failures']:
                            eligible.add(control);first=truth['failures'][0]
                            onset=first['cycle']*2+(first['phase']=='post')
                            if result['complete'] and any(i*2+(p=='post')>=onset for i,p in alarms):detected.add(control)
            sound=all_complete and correct_alarms==correct_unknown==0
            assert sound==s['suite_sound_on_fixed_controls']
            assert set(s['distinct_mutants_killed'])==(detected if sound else set())
            assert set(s['eligible_mutants'])==eligible
            assert s['api_input_plus_output_tokens']==tokens
            expected_roi=len(s['distinct_mutants_killed'])*1000/tokens
            assert abs(s['distinct_mutant_kills_per_1000_tokens']-expected_roi)<1e-12
            for i,activation in enumerate(s['property_activations']):
                properties.append({'arm':key[0],'repetition':key[1],'observation_simulator':sim,
                    'slot':i,'definite_correct_control_checks':activation,
                    'correct_alarm_records':s['correct_control_alarms_by_property'][i],
                    'unactivated_on_correct_controls':i in s['vacuous_slots']})
            endpoints.append({'arm':key[0],'repetition':key[1],'simulator':sim,'status':c['status'],
                'sound':sound,'correct_alarm_records':s['correct_control_alarm_records'],
                'correct_unknown_records':s['correct_control_unknown_records'],
                'eligible_pairs':s['eligible_mutant_trace_count'],'detected_pairs':s['valid_mutant_trace_kills'],
                'eligible_mutants':len(eligible),'killed_mutants':len(s['distinct_mutants_killed']),
                'mutant_recall':s['observable_mutant_recall'],'api_tokens':tokens,
                'token_roi':expected_roi,'cached_input_tokens':cost['cached_input_tokens'],
                'reasoning_output_tokens':cost['reasoning_output_tokens'],
                'generation_requests':cost['generation_requests'],'count_requests':cost['count_requests'],
                'development_cycles':cost['replayed_cycles'],'development_replays':cost['monitor_replays'],
                'active_development_seconds':cost['generation_and_count_seconds']+cost['development_wall_seconds'],
                'compile_seconds':cost['compile_seconds'],'monitor_replay_seconds':cost['monitor_replay_seconds']})
        assert len(c['formal'])==12
        for row in c['formal']:
            job=d/'formal'/row['control']/row['mode']
            data=json.loads((job/'result.json').read_text());log=(job/'sby.log').read_text()
            assert data['status']==row['status'] and data['depth']==48
            started=[int(x) for x in re.findall(r'Checking assertions in step (\d+)',log)]
            cover_hits=set(re.findall(r'Reached cover statement at (.*)',log))
            witness=row.get('witness_review') or {}
            if row['mode']=='cover':
                meaning='all_registered_activation_covers_reached' if row['status']=='PASS' else 'not_all_covers_reached_within_bound' if row['status']=='FAIL' else 'incomplete_or_error'
            else:
                meaning='assertion_counterexample_requires_reference' if row['status']=='FAIL' else ('unbounded_proof_under_fixed_assumptions' if row['mode']=='prove' else 'no_counterexample_within_completed_bound') if row['status']=='PASS' else 'incomplete_or_error'
            formal.append({'arm':key[0],'repetition':key[1],'control':row['control'],'mode':row['mode'],
                'status':row['status'],'requested_depth':48,'largest_assertion_step_started':max(started) if started else None,
                'cover_statements_reached':len(cover_hits),'seconds':row['seconds'],
                'status_meaning':meaning,
                'witness_status':witness.get('status'),'reference_verdict':witness.get('oracle_verdict'),
                'witness_classification':witness.get('classification')})
    write_csv(out/'rounds.csv',rounds);write_csv(out/'endpoints.csv',endpoints);write_csv(out/'formal.csv',formal)
    write_csv(out/'fault-pairs.csv',pairs);write_csv(out/'property-activations.csv',properties)
    coverage,targets=fixed_coverage()
    write_csv(out/'fixed-coverage.csv',coverage);write_csv(out/'equivalent-source-counts.csv',targets)
    aggregate={}
    for arm in ('B_prime','C_prime'):
        rs=[r for r in endpoints if r['arm']==arm and r['simulator']=='verilator']
        aggregate[arm]={k:{'mean':statistics.mean(r[k] for r in rs),
            'min':min(r[k] for r in rs),'max':max(r[k] for r in rs),
            'sample_sd':statistics.stdev(r[k] for r in rs)} for k in ('killed_mutants','api_tokens','token_roi','active_development_seconds')}
    dump(out/'comparison.json',aggregate)
    costs={'generation':json.loads((run/'summary.json').read_text()),
        'final_evaluation':json.loads((final/'summary.json').read_text()),
        'offline_preflight':json.loads((BASE/'results/preflight-v2/summary.json').read_text()),
        'semantic_preprocessing_seconds':json.loads((BASE/'results/preflight-v2/semantic.json').read_text())['seconds'],
        'generation_by_session':[{'arm':k[0],'repetition':k[1],**dict(v)} for k,v in totals.items()],
        'cost_notes':['cached and reasoning tokens are subsets, not additions',
            'preflight summary is a historical pre-reference stage; use frozen reference eligibility for final scores',
            'fixed DUT simulations occurred offline; model and final stages replay observations in Icarus',
            'formal job wall time, generation wall time and offline cost are separate; some component times overlap']}
    dump(out/'costs.json',costs)
    audit={'status':'passed','prompts_checked':len(rounds),'source_models':sorted({r.get('returned_model') for r in calls if r.get('accepted_response')}),
        'generation_requests':sum(r['generation_request_issued'] for r in calls),'count_requests':sum(r['count_request_issued'] for r in calls),
        'failed_or_retried_attempts':sum(not r.get('accepted_response') for r in calls),
        'api_input_tokens':sum((r.get('usage') or {}).get('input_tokens') or 0 for r in calls),
        'api_output_tokens':sum((r.get('usage') or {}).get('output_tokens') or 0 for r in calls),
        'cached_tokens_are_subset':True,'reasoning_tokens_are_subset':True,
        'raw_fixed_inputs_and_counts_unchanged':True,'reference_freeze_verified':True,
        'candidate_hashes_verified':True,'formal_tasks':len(formal),'formal_statuses':dict(collections.Counter(x['status'] for x in formal)),
        'final_source_sha256':sha(final/'scores.json'),'auditor_sha256':sha(Path(__file__))}
    dump(out/'audit.json',audit)
    plot(out,endpoints,rounds,formal)
    narrative(out,run,final,endpoints,formal,aggregate,costs,audit)
    return audit

def narrative(out,run,final,endpoints,formal,aggregate,costs,audit):
    primary=sorted((r for r in endpoints if r['simulator']=='verilator'),key=lambda r:(r['arm'],r['repetition']))
    budget_delta=(aggregate['C_prime']['api_tokens']['mean']/aggregate['B_prime']['api_tokens']['mean']-1)*100
    matched=all(r['sound'] and r['killed_mutants']==6 for r in primary)
    conclusion=('B′、C′ 的三次重复均检出 6/6 种独立参考确认可观察的注入故障，正确控制均无报警或未知。'
                '本轮未观察到 C′ 的仿真检错收益；相同检出数下，C′ 的实际 token 成本更高。'
                if matched else '结果见逐次表；不得用平均值隐藏失败或未知试次。')
    table=['| 组别 | 重复 | 正确控制报警 | 已检出故障 | 可评分轨迹对检出 | API tokens | 每千 token 检出数 |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for r in primary:
        table.append(f'| {r["arm"]} | {r["repetition"]} | {r["correct_alarm_records"]} | {r["killed_mutants"]}/{r["eligible_mutants"]} | {r["detected_pairs"]}/{r["eligible_pairs"]} | {r["api_tokens"]:,} | {r["token_roi"]:.6f} |')
    formal_table=['| 组别 | bmc/prove PASS | 已找到断言反例 | cover PASS | TIMEOUT | 其他未决/错误 |',
                  '|---|---:|---:|---:|---:|---:|']
    for arm in ('B_prime','C_prime'):
        fs=[r for r in formal if r['arm']==arm]
        formal_table.append(f'| {arm} | {sum(r["status"]=="PASS" and r["mode"]!="cover" for r in fs)} | {sum(r["status"]=="FAIL" and r["mode"]!="cover" for r in fs)} | {sum(r["status"]=="PASS" and r["mode"]=="cover" for r in fs)} | {sum(r["status"]=="TIMEOUT" for r in fs)} | {sum(r["status"] not in ("PASS","FAIL","TIMEOUT") for r in fs)} |')
    reviewed=collections.Counter(r['witness_classification'] for r in formal if r['witness_classification'])
    gen=costs['generation'];end=costs['final_evaluation']
    body=f'''# test2：固定刺激下生成 FIFO monitor 的 B′/C′ pilot

日期：2026-11-04。独立任务登记；不替换既有 stimulus-generation 实验。

## 结论与逐次结果

{conclusion} C′ 平均实际 API input+output tokens 比 B′ 高 **{budget_delta:.3f}%**。
只有一颗 FIFO、六种预置单故障、每组三次重复；这不能证明所有 E-graph 反馈无效。

{chr(10).join(table)}

上表是 Verilator 二值观察的主要评分。Icarus 观察逐次结果、未知与所有未激活对均保留在
[endpoints.csv](endpoints.csv) 与 [fault-pairs.csv](fault-pairs.csv)。两个 observation simulator
标签指原始 DUT 轨迹的生产者；候选 monitor 均由同一个 Icarus replay harness 执行。
同一故障的重复报警、不同轨迹命中与两种仿真器观察不重复算成新的缺陷。

![各次重复的效果与 token 成本](comparison.png)

## 固定边界与角色

- 使用现有 ZipCPU sfifo 的合成等价冗余 stress 变体，8-bit、depth16、同步高电平复位、异步 front read。
  这不是新的自然独立 IP；规格是此前固定的项目合同，不冒称逐字上游规范。
- Claude Opus 5.5 仅依规格与公共观察接口写 Python 参考 checker；全新会话做只读复核。
  GPT-6.1 Sol 写独立 SV 候选 monitor。GPT/Codex 写基础设施与控制，但未改 Claude checker。
  候选是被评分对象，任何候选内部期望值都不能作为参考答案。
- Claude 21 项作者自测、24 项独立有限控制和 24 条正确实现轨迹通过；审阅结论为限定范围接受，
  不是通用 soundness 证明。P6 acceptance 仅为间接检查，未额外获得独立事件检错分。
- 开发集 9/45/42 周期，最终集 61/129/163 周期，各含两个已计数 idle 尾周期；所有组完全相同。
  六个单点故障在调用前登记：读指针步长、一次写入丢失、reset empty 标志、读出地址顺序、
  full 时错误接收写入、同时读写时读指针不前进。最终输入和故障实现没有进入候选提示词。
- 各组 3 独立会话 × 6 轮，六个属性槽，32,000 输入 / 8,192 输出 token 上限，low reasoning，
  120 秒请求超时、至多一次重试。使用最后一个符合 schema/边界且能编译的候选；全部六个
  候选哈希冻结后才开放最终评分。没有根据最终分数选择或修订候选。

## B′/C′ 的信息差

B′ 得到规格、无上游 FORMAL 答案的 RTL、完整固定开发观察、全部 400 个原始覆盖计数，
以及相同策略的编译/开发反馈。C′ 只加经过 egg/Z3 验证的完整 guard 与等价关系。
所有请求与响应逐次保存；候选 API 无文件工具或递归工作区访问。

egg 实际执行五轮有界饱和，30 e-classes、44 e-nodes；六条二值重写反证均 UNSAT。
保留类型和时钟/复位上下文。两组合格非平凡关系对应五个独立原始 branch-if 计数：
91/161 和 96/129/179。两个无法唯一映射的 else 组、两个不支持项明确排除在语义附录外；
原始分母仍保留。二值组合等价不等于四值等价、时序正确或规格正确。

五个源点在 `basic` 都未命中，在固定开发 `boundary` 都已命中；提示词明确标注计数 basis，
没有声称它们在整个开发集未覆盖。开发集覆盖并集为 line22/22、branch22/24、expr14/16、
toggle218/338；最终集为22/22、22/24、14/16、331/338。详见
[fixed-coverage.csv](fixed-coverage.csv) 与 [equivalent-source-counts.csv](equivalent-source-counts.csv)。
这些数值是固定 DUT 证据，不能被候选 monitor 修改，也不是本实验的优化结果。

## 判分与未决

主要“有效检错”先要求候选在正确控制上完整运行、无报警和未知；只对独立 reference 确认
已产生规范违反的 mutant/trace 对计分。报警不得早于首次规范违反。
Verilator 有16/18个可评分对，Icarus有15/18个；两者均覆盖六种故障。
M05 在 final_wrap_reset/final_mixed 未被固定输入激活；Icarus M02/final_boundary 为参考未决，
该对即使候选报警也不给主要检错分。未知参考判决与候选输出未知分列，均不转成 PASS。
每千 token 检出数 = 合格的不同注入故障数 ×1000 / API 报告的 input+output tokens。
这与旧实验的“新覆盖点/token”是不同指标，不能直接数值比较。

## 形式检查单独报告

每候选固定12任务：两个正确控制各 bmc/prove/cover、六个故障各bmc；请求深度48，
每任务60秒，工具启动/清理时间另计。初始必须复位，reset 时禁止同时读写，候选不能加假设。

{chr(10).join(formal_table)}

反例桥接分类：`{dict(reviewed)}`。
解码后的公开引脚轨迹交给同一个冻结 Claude reference 执行；这是该解码轨迹上的规范判决，
并非额外的完整设计证明，也未另行物理仿真所有 symbolic witness。
`cover PASS` 只说明六个 active 信号可达，不说明属性有效或 DUT 正确；active 条件很宽时
容易达到，也不代表 full/empty/wrap 各行为条件都已分别形式覆盖。
TIMEOUT 保持未决；日志中的“开始检查第 k 步”不是完成了 k 步，更不是完成深度48。
`bmc PASS` 也不能记作无界证明。全部状态与实际时间见 [formal.csv](formal.csv)。

![形式任务状态](formal-status.png)

## 成本与可复现证据

- 真实生成 {audit['generation_requests']} 次，token-count 请求 {audit['count_requests']} 次，失败/重试 {audit['failed_or_retried_attempts']} 次。
  输入 {audit['api_input_tokens']:,}、输出 {audit['api_output_tokens']:,} tokens；缓存和 reasoning 均为子项，不再加总。
- 生成阶段墙钟 {gen['wall_seconds']:.3f}s；{gen['compile_attempts']} 次编译工具调用、
  {gen['monitor_replays']} 次观察重放、{gen['replayed_cycles']:,} 个重放周期，新增 DUT 仿真0次。
- 最终评估墙钟 {end['wall_seconds']:.3f}s；{end['compilation_tool_invocations']} 次编译工具调用、
  {end['monitor_replays']} 次重放、{end['replayed_cycles']:,} 个周期；形式{end['formal_tasks']}任务共{end['formal_seconds']:.3f}s。
  分项可能包含于墙钟内，不能重复相加。
- 冻结前离线 DUT 测量为16次编译、96次仿真、7,184周期；语义预处理时间分项见 [costs.json](costs.json)。
  Claude作者与独立复核2次调用，CLI报告费用合计$0.353157；不推算未返回的 OpenAI 美元价格。
- OpenAI SDK2.54.0、Python3.13.9、Verilator5.050、Icarus12.0、Yosys0.70+post、SBY0.70、Z3 CLI5.1.0、egg0.11。
- Git基线 `acd220ace9c02a6b5f0d98bde15bcfaf70ae2a60`；本轮尚未commit/push。
  运行身份以冻结文件和最终候选哈希为准，不冒称未提交文件已属于该commit。
  live freeze SHA256 `{sha(BASE/'configs/live_freeze_v1.json')}`；
  DUT SHA256 `{sha(BASE/'public/sfifo.v')}`；
  reference SHA256 `{sha(BASE/'reference/frozen-v1/checker.py')}`。

[audit.json](audit.json) 重新核对36份渲染提示词、usage、原始采样位与计分、源证据及候选/reference哈希；
[comparison.json](comparison.json) 保留每组均值、范围、样本标准差；不做小样本显著性声称。
编译成功率和开发报警逐轮见 [rounds.csv](rounds.csv)，属性实际激活见 [property-activations.csv](property-activations.csv)。
Mock/replay与真实模型结果分目录；初期跨仿真器 X 严格比较失败及反例解码修订均保留历史记录，
这些修订在 live freeze 前完成，没有按正式结果改 oracle 或评分。

## 局限与下一步

候选普遍建立了完整的预期队列，因此可从规格直接覆盖顺序、容量和复位；组合 guard 关系未必
提供额外必要信息。五个语义源点在开发集中已出现，最终六故障集可能存在天花板。
这是对当前任务的解释假设，不是已证明的因果归因。
没有长度匹配 placebo、独立自然IP或更广隐藏故障集；本轮既不能隔离纯语义效应，也不能证明
E-graph 在任意任务无效。只冻结并评分最终候选，不能追溯声称第一轮就达到了最终检错分数。

下一次应另行登记更有区分力的属性任务与独立故障/合法控制，例如多周期协议顺序、取消/复位
跨事务边界、长延迟数据保存；先做开发可行性验证，再冻结最终集。保留独立参考与固定输入，
可加入 minimal C 和实际 token 匹配 placebo。形式成本可作为单独研究维度，但应在运行前
明确断言分解、归纳辅助和资源配置，不能把本轮超时事后改记通过或换预算补分。

## 复现

以下命令从仓库根执行。输出目录须全新；已有正式结果不可覆盖。

```sh
.venv/bin/python -m unittest discover -s test2/tests -v
.venv/bin/python test2/scripts/report_live.py --run test2/results/live-v1 --final test2/results/live-final-v1 --output test2/results/live-report-reproduction
```

无需新 API 即可重放已保存响应：`runner.py --mode replay --preflight test2/results/preflight-v2
--replay-source test2/results/live-v1 --output test2/results/replay-reproduction`；此结果必须标为重放，
不能计成新的独立模型重复。完整 live 命令与冻结门槛见 `test2/configs/live_freeze_v1.json`。
最终评分命令为 `final_score.py --run test2/results/live-v1 --preflight test2/results/preflight-v2
--output test2/results/final-reproduction --formal`，会再次耗用登记的形式工具时间，勿为改文案重复执行。
'''
    (out/'report.md').write_text(body)

def plot(out,endpoints,rounds,formal):
    import os
    os.environ['MPLCONFIGDIR']=str(out/'plot-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    colors={'B_prime':'#2376b5','C_prime':'#d97a18'}
    fig,axes=plt.subplots(1,3,figsize=(12,3.7))
    primary=[r for r in endpoints if r['simulator']=='verilator']
    for arm in colors:
        rs=[r for r in primary if r['arm']==arm]
        axes[0].scatter([r['api_tokens']/1000 for r in rs],[r['killed_mutants'] for r in rs],label=arm.replace('_',' '),color=colors[arm],s=48)
        axes[1].scatter([0 if arm=='B_prime' else 1]*len(rs),[r['token_roi'] for r in rs],color=colors[arm],s=48)
        for rep in (1,2,3):
            rr=[r for r in rounds if r['arm']==arm and r['repetition']==rep]
            axes[2].plot([r['round'] for r in rr],[r['cumulative_api_tokens']/1000 for r in rr],color=colors[arm],alpha=.55)
    axes[0].set(xlabel='API input + output tokens (thousands)',ylabel='Distinct eligible mutants detected',ylim=(-.3,6.5));axes[0].legend()
    axes[1].set(xticks=[0,1],xticklabels=["B′","C′"],ylabel='Valid mutant kills / 1,000 API tokens')
    axes[2].set(xlabel='Development round',ylabel='Cumulative API tokens (thousands)',xticks=range(1,7))
    for ax in axes:ax.grid(alpha=.2)
    fig.suptitle('Fixed-stimulus monitor pilot: individual repetitions; two-state primary score')
    fig.tight_layout();fig.savefig(out/'comparison.png',dpi=170);fig.savefig(out/'comparison.pdf');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,3.5))
    states=['PASS','FAIL','TIMEOUT','UNKNOWN','ERROR']
    for i,arm in enumerate(colors):
        counts=collections.Counter(r['status'] for r in formal if r['arm']==arm)
        ax.bar([j+(i-.5)*.36 for j in range(len(states))],[counts[s] for s in states],width=.36,color=colors[arm],label=arm.replace('_',' '))
    ax.set(xticks=range(len(states)),xticklabels=states,ylabel='Formal tasks',title='Tool statuses: FAIL meaning depends on bmc/prove versus cover')
    ax.legend();fig.tight_layout();fig.savefig(out/'formal-status.png',dpi=170);fig.savefig(out/'formal-status.pdf');plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('run','final','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();print(json.dumps(report(a.run.resolve(),a.final.resolve(),a.output.resolve()),indent=2))
