#!/usr/bin/env python3
"""Post-release descriptive analysis and independent artifact accounting only."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import statistics
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'test2/scripts'))
from common import dump,sha
from controller_loop_live import live_gate,REG,load,verify_task
from controller_release_live import verify_release,ARMS


def execute():
    out=Path(__file__).resolve().parent;run=ROOT/'test2/results/controller-live-v1';final=ROOT/'test2/results/controller-final-v1'
    original=verify_release(run);live_gate();verify_task(load(REG))
    replay_root=ROOT/'test2/results/controller-live-replay-v1';replayed=verify_release(replay_root)
    for a in original:
        b=next(b for b in replayed if (a['arm'],a['repetition'],a['round'])==(b['arm'],b['repetition'],b['round']))
        for name in ('prompt.json','response.json','development-feedback.json','compiled/candidate.sv'):
            assert sha(run/a['directory']/name)==sha(replay_root/b['directory']/name)
    completion=load(final/'completion.json');assert sha(final/'scores.json')==completion['scores_sha256']
    scores=load(final/'scores.json');calls=[json.loads(s) for s in (run/'calls.jsonl').read_text().splitlines()]
    assert len(scores['rounds'])==36 and all(r['metrics']['suite_sound_on_fixed_controls'] and len(r['metrics']['distinct_mutants_killed'])==11 and r['metrics']['valid_mutant_trace_kills']==106 for r in scores['rounds'])
    assert len(calls)==36 and all(r['accepted_response'] for r in calls)
    assert all(r['input_token_count']==r['usage']['input_tokens']<=64000 and r['usage']['output_tokens']<=8192 for r in calls)
    assert all(r['requested_model']==r['returned_model']=='gpt-6.1-sol' for r in calls)
    faults=load(ROOT/'test2/tasks/axis_length_fifo_v1/private/mutant-catalog-v1.json')['faults']
    strata={f['id']:f['stratum'] for f in faults};rows=[]
    for f in scores['formal']:
        jobs=f['jobs'];confirmed=sorted({j['source'] for j in jobs if j['source']!='correct' and j.get('witness',{}).get('classification')=='reference_confirmed_DUT_violation_on_this_trace'})
        rows.append(dict(arm=f['arm'],repetition=f['repetition'],statuses=dict(Counter(j['status'] for j in jobs)),
                         correct_modes={m:dict(Counter(j['status'] for j in jobs if j['source']=='correct' and j['mode']==m)) for m in ('bmc','prove','cover')},
                         mutant_statuses=dict(Counter(j['status'] for j in jobs if j['source']!='correct')),
                         confirmed_mutant_types=confirmed,confirmed_mutant_type_count=len(confirmed),
                         strata={s:sorted(mid for mid in confirmed if strata[mid]==s) for s in load(REG)['strata_before_outcomes']},
                         witness_classes=dict(Counter(j['witness']['classification'] for j in jobs if 'witness' in j)),
                         wall_seconds=f.get('wall_seconds'),jobs=len(jobs)))
    assert len(rows)==6 and all(r['jobs']==90 for r in rows)
    arms={}
    for arm in ARMS:
        records=[r for r in calls if r['arm']==arm];fs=[f for f in rows if f['arm']==arm]
        totals=[sum(r['usage']['total_tokens'] for r in records if r['repetition']==rep) for rep in (1,2,3)]
        first=[sum(r['usage']['total_tokens'] for r in records if r['repetition']==rep and r['round']==1) for rep in (1,2,3)]
        arms[arm]=dict(tokens_by_session=totals,mean_tokens=statistics.mean(totals),first_target_tokens=first,
                       mean_first_target_tokens=statistics.mean(first),input_tokens=sum(r['usage']['input_tokens'] for r in records),output_tokens=sum(r['usage']['output_tokens'] for r in records),
                       cached_input_tokens=sum(r['usage']['cached_input_tokens'] for r in records),reasoning_output_tokens=sum(r['usage']['reasoning_output_tokens'] for r in records),
                       mean_simulation_kills_per_1000_tokens=statistics.mean(11000/t for t in totals),
                       formal_confirmed_types_by_session=[f['confirmed_mutant_type_count'] for f in fs],
                       mean_formal_confirmed_types=statistics.mean(f['confirmed_mutant_type_count'] for f in fs),
                       pooled_formal_confirmed_types=sorted(set().union(*(set(f['confirmed_mutant_types']) for f in fs))),
                       formal_stratum_counts={s:[len(f['strata'][s]) for f in fs] for s in load(REG)['strata_before_outcomes']})
    raw_checks=0;cycles=0;raw_bytes=0
    for p in (final/'simulation').rglob('result.json'):
        r=load(p);compressed=p.parent/'replay.log.gz';data=gzip.decompress(compressed.read_bytes())
        assert sha(compressed)==r['compressed_log_sha256']
        assert hashlib.sha256(data).hexdigest()==r['raw_log_sha256']==r['execution']['log_sha256']
        assert r['complete'] and len(r['properties'])==6
        raw_checks+=1;cycles+=r['cycles'];raw_bytes+=len(data)
    assert raw_checks==5832 and cycles==1124640
    old=load(ROOT/'test2/configs/live_freeze_v1.json');assert len(old['files'])==3486
    assert all(sha(ROOT/n)==h for n,h in old['files'].items())
    migration=load(ROOT/'docs/audits/migration_2026-11-04.json')
    assert all(sha(ROOT/n)==h for n,h in migration['functional_files_before'].items())
    assert sha(ROOT/'test2/results/live-final-v1/scores.json')=='33003b33a7172d29704f85fa84da10bdbb30aebe78b72d400a4f97b73a2ef338'
    assert sha(ROOT/'test2/reference/frozen-v1/checker.py')=='53cff0d05aa9c48a71aec72cecfba265a13fe4baa2a4d9a72b3cef4d6b201337'
    assert sha(ROOT/'test2/results/controller-token-count-v1/producer.py')==load(ROOT/'test2/results/controller-token-count-v1/summary.json')['runner_sha256']
    delta=(arms[ARMS[1]]['mean_tokens']/arms[ARMS[0]]['mean_tokens']-1)*100
    audit=dict(status='passed',producer_sha256=sha(__file__),release_sha256=sha(run/'release.json'),scores_sha256=sha(final/'scores.json'),
               live_freeze_sha256=sha(ROOT/'test2/configs/controller_live_freeze_v1.json'),formal=rows,arms=arms,C_token_change_percent=delta,
               formal_mode_counts={m:dict(Counter(j['status'] for f in scores['formal'] for j in f['jobs'] if j['mode']==m)) for m in ('bmc','prove','cover')},
               statuses=dict(Counter(j['status'] for f in scores['formal'] for j in f['jobs'])),
               raw_simulation_replays_verified=raw_checks,raw_cycles_verified=cycles,raw_log_bytes_verified=raw_bytes,
               old_frozen_files_verified=3486,migration_functional_files_verified=len(migration['functional_files_before']),
               all36_original_and_replay_candidates_intact=True,original_scores_unchanged=True,
               source_obligation_inspection_is_exploratory=True,API_dollar_cost_not_computed=True)
    dump(out/'analysis.json',audit)
    lines=['# 新控制器 B/C 分层评估','',f'本轮完成36次生成、0重试，合计1,878,181 input+output tokens。固定刺激；全部36候选先冻结，再做隐藏评分。C平均总tokens比B增加{delta:.3f}%。','',
           '## 模拟与成本','', 'B/C各3次重复×6轮，全部从首轮即达到11/11可观测故障、106/106合格组合；正确控制无报警或候选未知值。12种原始故障全部保留，M08在固定语料没有独立确认违规。所有三层结果均持平：boundary_guard 4/4、handshake_reset 3/3（原始4）、payload_status 4/4。每轮固定预算下，未观察到模拟正确控制、有效检错率或更早达标的C增益。','',
           '| 组 | 总tokens/次重复 | 首轮达标tokens | 平均最终11种故障/1000tokens |','|---|---|---|---:|']
    for a,d in arms.items():lines.append(f'| {a} | {d["tokens_by_session"]} | {d["first_target_tokens"]} | {d["mean_simulation_kills_per_1000_tokens"]:.6f} |')
    lines+=['','token ROI使用所有生成尝试的input+output；cached input和reasoning output是子集，不重复相加。另有44次计数请求（含首次表示超限的4次）；美元账单成本未计算。实际token上限与usage逐次一致。','',
            '## 固定短时形式检查','', '| 组 | 重复 | 正确源BMC | 正确源prove | activation cover | 独立确认故障种类 /12原始 | 故障类型 | wall秒 |','|---|---:|---|---|---|---:|---|---:|']
    for r in rows:
        m=r['correct_modes'];lines.append(f'| {r["arm"]} | {r["repetition"]} | {m["bmc"]} | {m["prove"]} | {m["cover"]} | {r["confirmed_mutant_type_count"]} | {", ".join(r["confirmed_mutant_types"]) or "无"} | {r["wall_seconds"]:.2f} |')
    lines+=['','形式分层（每个单元为3次重复的独立确认故障类型数）：','', '| 组 | boundary_guard /4 | handshake_reset /4 | payload_status /4 | 去重并集 |','|---|---|---|---|---|']
    for a,d in arms.items():
        st=d['formal_stratum_counts'];lines.append(f'| {a} | {st["boundary_guard"]} | {st["handshake_reset"]} | {st["payload_status"]} | {", ".join(d["pooled_formal_confirmed_types"])} |')
    b=arms[ARMS[0]];c=arms[ARMS[1]]
    finding='按每次重复的独立确认故障均值，C高于B' if c['mean_formal_confirmed_types']>b['mean_formal_confirmed_types'] else '本轮固定短时形式结果未显示C平均独立确认故障数更高'
    lines+=['',f'{finding}：每次重复均值B={b["mean_formal_confirmed_types"]:.3f}，C={c["mean_formal_confirmed_types"]:.3f}。这项结果反映给定monitor实现与5秒故障BMC预算下的可判定性；全组并集与逐次波动见表。尚无候选完成全部六槽的正确源证明，不能把这些反例数解释为完整monitor正确性的证明。C重复3的P2状态通道阻塞稳定性在10秒上限内完成BMC24及prove；这是单次重复中的局部证明结果，B组没有单槽prove完成。其余槽状态逐项保留。','',
            f'总状态：{audit["statuses"]}；分模式：{audit["formal_mode_counts"]}。所有90×6任务均保留；TIMEOUT/未达到activation均不改为通过。cover PASS只证明激活可达；BMC PASS仅有限步；prove与归纳失败分开。','',
            '## 天花板与形式瓶颈','',
            '当前固定语料的类型和组合检错指标同时饱和，无法区分更完整的规格覆盖。只读源码审查发现C重复2最终候选未实现128周期尾段完成检查，依然得到当前满分；这是所选性质集合的覆盖缺口，不是回改原有评分。完整证据在obligation-audit.json，未为该发现新增执行测试。','',
            '资格阶段的三项局部接口证明不等于本轮完整候选证明。新形式桥保留全部公共输出以便独立参考复核反例，候选还有数千位私有状态。恒真深度24/5秒控制也曾超时；日志显示求解在后续步的假设/断言展开阶段耗时。完整锥、记忆体与状态表示可能增加开销；各因素的独立贡献尚未测定。128周期尾段条件在24步中也存在激活窗口限制。不能将全部超时归因于LLM语义质量。','',
            '## 下一项最小任务','',
            '先做新的、API-free资格登记：建立逐项规格义务×独立负控制矩阵，分开呈现valid的安全性与延迟/丢失响应的有限完成性；同时用固定控制和预选冻结monitor拆解保留输出/反例复核造成的形式开销，要求完整深度的恒真/恒假控制有效。保持本轮所有冻结、分数、超时和源代码不变。通过这些区分力与形式门禁后再考虑付费B/C；不继续在现有满分集上重复生成。','',
            '限制：仅3次重复/组、一个已检查过的IP家族；没有token匹配placebo，结论只涉及整个C反馈包，不能单独归因于E-graph语义。形式固定顺序为B后C，墙钟超时对本机负载敏感，差异是描述性结果。参考为独立有限轨迹checker，保留其未知/诊断/重置pre与连续性范围限制；没有完整soundness或设计正确性证明。源码义务审查为探索性诊断，未替换预登记主指标。','',
            f'复核：36个原始冻结与真实响应回放一致；{raw_checks}份评分日志的gzip、原始SHA与完整性均通过，合计{cycles}周期。旧3486文件、旧checker与旧scores及迁移时{audit["migration_functional_files_verified"]}个功能文件哈希保持不变。']
    (out/'analysis.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:audit[k] for k in ('status','statuses','formal_mode_counts','C_token_change_percent','arms')},indent=2))


if __name__=='__main__':execute()
