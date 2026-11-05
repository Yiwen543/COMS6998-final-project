"""Audit and report the separate safe-offer B run without touching old evidence."""
import argparse
import csv
import json
import os
from pathlib import Path
from coverage import summary as coverage_summary
from inventory_natural_coverage import load_all
from probe_spi_core_events import identity
from real_parent_screen import configuration
from run_midterm_fixed import ROOT,sha
from run_spi_core_b_development import assess,token_totals
from spi_core_safe_experiment import verify_freeze,messages
from spi_core_safe_interface import seed,parse,validate
from spi_core_experiment import group_status

def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []

def audit(folder):
    f=verify_freeze(folder/'freeze.json');s=read(folder/'summary.json');m=s['metadata']
    assert m['status']=='completed' and s['mode']=='live'
    assert sha(folder/'freeze.json')==m['freeze_sha256']
    calls=lines(folder/'calls.jsonl');counts=lines(folder/'counts.jsonl');rows=s['rows']
    assert token_totals(calls)==m['api_usage']
    assert sum(c['generation_requested'] for c in calls)==m['api_generation_calls']
    assert len(counts)==m['api_count_requests'] and assess(rows,f,'live')==s['gate']
    config=configuration('spi_host_core');sources=[str(Path(config['root'])/p) for p in config['sources']]
    denom={tuple(i) for i in f['counter_identities']};batches=0;cycles=0;requested=0;prompts=0
    decreases=[];hit_losses=[]
    for rep in range(1,f['development_budget']['repetitions']+1):
        history=[];repdir=folder/f'rep{rep}';previous_counts=None;prior=None;points=None;trace=None
        rr=[r for r in rows if r['repetition']==rep]
        repcycles=0;repexecutions=0;measurement_round=0
        for rnd in [0,*[r['round'] for r in rr]]:
            row=next((r for r in rr if r['round']==rnd),None)
            batch=repdir/('seed' if rnd==0 else f'round{rnd}')
            if rnd:
                rendered=messages(f,history,prior,points,trace,rnd)
                attempts=[c for c in calls if c['repetition']==rep and c['round']==rnd]
                assert 1<=len(attempts)<=f['model_limits']['max_retries']+1
                accepted=[]
                for i,call in enumerate(attempts):
                    assert call['attempt']==i+1 and read(folder/call['prompt'])==rendered
                    assert sha(folder/call['prompt'])==call['prompt_sha256'];prompts+=1
                    if call['accepted']:
                        assert call['requested_model']==call['returned_model']==f['model_limits']['model']
                        assert call['actions']==validate(call['parsed'],64)
                        assert call['usage']['input_tokens']<=f['model_limits']['input_tokens']
                        assert call['usage']['output_tokens']<=f['model_limits']['output_tokens']
                        accepted.append(call)
                    rendered=[*rendered,{'role':'user','content':'Previous attempt failed. Return only schema-conforming actions within the stated profile and budget.'}]
                assert len(accepted)<=1
                if accepted:history+=accepted[0]['actions']
                assert row['api_usage_cumulative']==token_totals([c for c in calls if c['repetition']==rep and c['round']<=rnd])
            if batch.exists():
                ex=read(batch/'execution.json');batches+=1;repexecutions+=1
                cycles+=ex['executed_cycles'];repcycles+=ex['executed_cycles'];requested+=ex['requested_cycles']
                requests=read(batch/'requests.json')['actions'];assert requests==seed()+history
                if not rnd or row['status']=='simulated':
                    trace,ledger=parse((batch/'simulation.log').read_text(),requests)
                    assert trace==read(batch/'trace.json') and ledger==read(batch/'transport.json')
                    assert len(trace)==ex['executed_cycles']==len(requests)
                    points=load_all(batch/'coverage.dat',sources);assert points==read(batch/'raw-points.json')
                    observed={identity(p):p['hits'] for p in points};assert set(observed)==denom and len(points)==len(denom)
                    if previous_counts is not None:
                        decreases += [{'repetition':rep,'round':rnd,'counter':k,'before':v,'after':observed[k]} for k,v in previous_counts.items() if observed[k]<v]
                        hit_losses += [{'repetition':rep,'round':rnd,'counter':k} for k,v in previous_counts.items() if v>0 and observed[k]==0]
                    previous_counts=observed;prior=read(batch/'result.json');measurement_round=rnd
                    assert prior['coverage']==coverage_summary(points)
                    assert prior['checker']==read(batch/'checker-output.json')['cases']['batch']
                    assert prior['delivery_complete']==(not prior['transport']['pending'])
                    assert prior['verification_complete']==(prior['delivery_complete'] and prior['checker']['verdict']=='pass')
            if rnd:
                assert row['coverage']==prior['coverage'] and row['checker']==prior['checker']
                assert row['transport']==prior['transport'] and row['groups']==group_status(points,f['targets'])
                assert row['measurement_round']==measurement_round
                assert row['measurement_fresh']==(row['status']=='simulated')
                assert row['executed_cycles_including_replays']==repcycles and row['simulator_executions']==repexecutions
    assert batches==m['simulation_executions'] and cycles==m['executed_cycles'] and requested==m['requested_cycles']
    result={'status':'pass','scope':'Saved data integrity/accounting, not proof of checker or DUT correctness.',
        'exact_prompt_reconstructions':prompts,'batches_checked':batches,'actual_cycles':cycles,
        'raw_denominator':len(denom),'api_usage':m['api_usage'],'raw_magnitude_decreases':decreases,'covered_to_zero':hit_losses,
        'new_API_calls':0,'new_simulations':0,'development_gate':s['gate']['pass'],
        'openai_staged_key_removed':not (ROOT/'build/private/midterm-openai-key').exists(),'script_sha256':sha(Path(__file__))}
    (folder/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def report(folder,doc,diagnosis=None):
    a=audit(folder);s=read(folder/'summary.json');f=read(folder/'freeze.json');m=s['metadata'];rows=s['rows']
    compact=[];cost=[]
    for r in rows:
        c={k:r[k] for k in ('repetition','round','status','measurement_fresh','measurement_round','api_tokens',
            'new_branch_points','token_roi_new_branch_points_per_1000','failed_attempts','simulator_executions',
            'executed_cycles_including_replays','unique_generated_cycles','repetition_wall_seconds','simulation_seconds',
            'delivery_complete','verification_complete')}
        c.update(groups_complete=sum(g['all_hit'] for g in r['groups']),checker_verdict=r['checker']['verdict'],
            assumptions=len(r['checker'].get('assumption_violations',[])),failure_diagnostics=r['failure_diagnostic_count'],
            distinct_failure_categories=';'.join(r['distinct_failure_categories']),
            cmd_pending=r['transport']['last']['cmd_pending'],tx_pending=r['transport']['last']['tx_pending'])
        for kind,v in r['coverage'].items():c[kind+'_covered']=v['covered'];c[kind+'_total']=v['total']
        compact.append(c)
    with (folder/'rounds.csv').open('w') as stream:
        w=csv.DictWriter(stream,fieldnames=list(compact[0]));w.writeheader();w.writerows(compact)
    for rep in range(1,f['development_budget']['repetitions']+1):
        rr=[r for r in rows if r['repetition']==rep]
        first=next((r for r in rr if r['status']=='simulated' and not r['checker'].get('assumption_violations') and all(g['all_hit'] for g in r['groups'])),None)
        cost.append({'repetition':rep,'target':'all 17 original groups: every separate source counter hit under legal inputs',
            'reached':bool(first),'first_round':first['round'] if first else None,
            **{k:first[k] if first else None for k in ('api_tokens','unique_generated_cycles','executed_cycles_including_replays','simulator_executions','repetition_wall_seconds','delivery_complete','verification_complete')},
            'right_censored_at_round':None if first else rr[-1]['round']})
    (folder/'target_cost.json').write_text(json.dumps(cost,indent=2)+'\n')
    os.environ.setdefault('MPLCONFIGDIR',str(folder/'mplconfig'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MaxNLocator,FuncFormatter
    fig,axes=plt.subplots(2,4,figsize=(16,7),layout='constrained')
    fields=[('api_tokens','API input + output tokens'),('executed_cycles_including_replays','Executed cycles incl. replay'),
            ('simulator_executions','Simulator executions'),('repetition_wall_seconds','Repetition wall time (s)')]
    for col,(field,label) in enumerate(fields):
        for rep in range(1,4):
            rr=[r for r in compact if r['repetition']==rep and r['measurement_fresh']]
            axes[0,col].plot([r[field] for r in rr],[r['groups_complete'] for r in rr],marker='o',label=f'B rep {rep}')
            axes[1,col].plot([r[field] for r in rr],[100*r['branch_covered']/r['branch_total'] for r in rr],marker='o')
            bad=[r for r in rr if r['assumptions']]
            axes[0,col].scatter([r[field] for r in bad],[r['groups_complete'] for r in bad],marker='x',c='red')
        axes[0,col].axhline(17,color='gray',linestyle='--');axes[0,col].set_ylim(0,18);axes[1,col].set_ylim(0,101)
        for ax in axes[:,col]:
            ax.set_xlabel(label);ax.grid(alpha=.25);ax.xaxis.set_major_locator(MaxNLocator(4,integer=field=='simulator_executions'))
            if field=='api_tokens':ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1000:g}k'))
    axes[0,0].set_ylabel('Complete source groups');axes[1,0].set_ylabel('DUT branch counters hit (%)');axes[0,0].legend()
    fig.suptitle('SPI core: separately registered safe-offer B development; live only')
    fig.savefig(folder/'cost_curves.png',dpi=170);fig.savefig(folder/'cost_curves.pdf');plt.close(fig)
    text=['# SPI core：安全 offer driver 的独立 B 结果（2026-11-04）','',
      f"原预登记门槛：**{'通过' if s['gate']['pass'] else '未通过'}**。本报告只有新的 B 开发数据，不与旧直接引脚 B 合并，不推断 C 收益。",'',
      '[接口登记及独立复核](spi_core_safe_driver_2026-11-04.md)保留原 DUT、Claude v4 checker、17 组目标（8 组非平凡）、3,107 个原始 DUT counter。'+
      '每轮最多 64 个新物理周期；等待握手计入预算，无隐式 drain。三重复、六轮，模型 gpt-6.1-sol/low，输入 32,000、输出 16,384，timeout 120 s，最多一次重试。','',
      '| 重复 | 首轮未全命中组 | 最后未命中组 | 完整/合法 | 最终 checker | 全目标首次合法命中 |','|---|---:|---:|---|---|---|']
    for g,c in zip(s['gate']['repetitions'],cost):
        text.append(f"| {g['repetition']} | {g['first_round_unhit_groups']} | {g['final_unhit_groups']} | {g['complete']}/{g['legal']} | {g['final_verdict']} | {c['first_round'] if c['reached'] else 'not reached'} |")
    text += ['','门槛要求三个重复均完整且输入合法，至少两个重复首轮仍剩两组、至少两个后续取得组进展。'+
        '目标命中看实际源 counter，不把等价源点合并；覆盖目标命中不等于所有已排队事务完成或整个 IP 正确。','',
        '| 重复 | line | branch | expr | toggle | token | 实际周期 | pending cmd/TX | verification_complete |','|---|---|---|---|---|---:|---:|---|---|']
    for rep in range(1,4):
        r=[r for r in compact if r['repetition']==rep][-1]
        cv=[f"{r[k+'_covered']}/{r[k+'_total']}" for k in ('line','branch','expr','toggle')]
        text.append(f"| {rep} | {' | '.join(cv)} | {r['api_tokens']} | {r['executed_cycles_including_replays']} | {r['cmd_pending']}/{r['tx_pending']} | {r['verification_complete']} |")
    text += ['','| 重复 | 最终失败诊断/不同类别 | 最终输入违规 | 最终 unresolved |','|---|---|---:|---|']
    for rep in range(1,4):
        r=[r for r in rows if r['repetition']==rep][-1]
        text.append(f"| {rep} | {r['failure_diagnostic_count']}/{len(r['distinct_failure_categories'])} | {len(r['checker'].get('assumption_violations',[]))} | {json.dumps(r['checker'].get('unresolved',[]),ensure_ascii=False)} |")
    text += ['','失败诊断数与类别数分别保留；类别不是已经独立确认的 DUT 缺陷数量。累计重放可能重复同一诊断。'+
        'producer 队列为空仅说明请求已送入 DUT，accepted-but-incomplete 或 RX 尚未交付仍可能令 checker inconclusive。', '',
        '| 重复 | 首轮实际新周期 | 首轮未全命中组 ID |','|---|---:|---|']
    for r in rows:
        if r['round']==1:text.append(f"| {r['repetition']} | {r['unique_generated_cycles']} | {[g['eclass'] for g in r['groups'] if not g['all_hit']]} |")
    totals=m['api_usage'];total=totals['input_tokens']+totals['output_tokens']
    text += ['',f"生成调用 {m['api_generation_calls']}，计数请求 {m['api_count_requests']}；API 输入 {totals['input_tokens']:,}、输出 {totals['output_tokens']:,}，合计 {total:,} token。未知用量尝试 {totals['unknown_usage_attempts']}。cached/reasoning 是子项，不重复相加。",'',
        f"编译 {m['compilations']} 次 / {m['compile_seconds']:.2f} s；仿真 {m['simulation_executions']} 次 / {m['simulation_seconds']:.2f} s；实际周期 {m['executed_cycles']:,}（含 seed 与全部累计重放）；总 wall time {m['elapsed_seconds']:.2f} s。语义预处理复用已冻结证据，本轮新增为零，历史成本另记。",'',
        'Token ROI = 相对公共 seed 新命中的 DUT branch counter / API 输入加输出 token × 1,000。每轮数值见 CSV。未命中 trial 保留为 not reached；不从均值中删除。图中仅连接成功测量轮，失败轮仍在 JSONL/CSV，不能用陈旧覆盖代替新观测。','',
        f"![成本效率曲线](../{folder.relative_to(ROOT)}/cost_curves.png)",'',
        f"审计重建 {a['exact_prompt_reconstructions']} 个实际 prompt，核对 {a['batches_checked']} 个累计批次的动作、引脚、队列和原始 coverage.dat。原始 counter magnitude 下降记录 {len(a['raw_magnitude_decreases'])} 条，非零变零 {len(a['covered_to_zero'])} 条；保留实际值，不跨进程取 max 或求和。OpenAI 暂存密钥已删除：{a['openai_staged_key_removed']}。",'',
        '局限：同一 SPI 家族已有筛选/开发历史；不是独立 held-out IP。许多组可由普通模式命中，TX/RX 时间事件也共享组合 stall guard，后续进展不等于深状态推理。原 checker 的有限范围、同作者 transport oracle、仅命令通道的完整 faulty-SV 控制限制均保留。三个重复只作描述，不声称统计显著性。','',
        ('下一步可以准备新的匹配 B/C（以及 A/placebo）正式实验；仍须冻结反馈选择、验证公共 transport 信息一致与 C 隔离、按实际 token 匹配 placebo。开发 B 不作为正式 B 控制组，本脚本不调用 C。' if s['gate']['pass'] else '本轮不启动 C。保留原门槛、全部重复与未达到目标的结果；不得缩短预算或选择性重跑来制造 C 的机会。'),'',
        f"冻结 SHA-256 `{m['freeze_sha256']}`；DUT revision `{f['dut_revision']}`；checker `{f['checker_sha256']}`。完整工作树哈希及包版本见 freeze.json / metadata.json。",'',
        f"证据：[summary](../{folder.relative_to(ROOT)}/summary.json)、[CSV](../{folder.relative_to(ROOT)}/rounds.csv)、[目标成本](../{folder.relative_to(ROOT)}/target_cost.json)、[审计](../{folder.relative_to(ROOT)}/audit.json)。",'',
        '```sh',f'.venv/bin/python scripts/report_spi_core_safe_b.py --input {folder.relative_to(ROOT)} --report {doc.relative_to(ROOT)}'+
        (f' --diagnosis {diagnosis.relative_to(ROOT)}' if diagnosis else ''),'```','']
    if diagnosis:
        d=read(diagnosis)
        text += ['## 事后诊断：为什么仍然太快命中','',
            f"普通写、普通三种 speed 和普通 full-cycle 读的校准并集，已经命中 {len(d['ordinary_complete_groups'])}/17 组。"+
            'TX starvation 和 RX backpressure 只额外命中同一个组 315；CSID 切换没有额外源组。'+
            '这是对已经冻结目标的诊断，不据此改本轮目标或重新选择重复。','',
            '组 315 的八个源计数对应多个寄存器在 stall 时保持、clock flop 使能及 CSB 保持。'+
            '它们证明该组合/时序 guard 被执行，不证明“阻塞后恢复并完成事务”。'+
            '组 51 对应 shift-register 的 `full_cyc_i` 与 FSM 的 `full_cyc_o` 两个条件计数，普通 FULLCYC 配置就能触发。'+
            '代码来自真正多模块 IP、存在非平凡等价关系，并不自动形成需要长序列推理的覆盖目标。','',
            '| 重复 | 首轮 stall 组全部命中 | 首轮已完成的 checker 事件 |','|---|---|---|']
        for r in d['first_round_observations']:
            text.append(f"| {r['repetition']} | {r['stall_group_315']['all_hit']} | {r['passed_event_families']} |")
        text += ['','新的协议队列消除了手动预测握手的要求，但它不提供目标刺激。三组在第 2 轮命中目标，'+
            '支持“现有目标区分度不足”的诊断，不能证明 e-graph 无用，也不能用旧/新 B 的未配对差异估计 driver 的因果收益。','',
            '下一轮应另行预登记至少多组能区分具体多步事件的完整 guard，先比较普通操作与恢复/切换校准的源计数增量。'+
            '若自然源码只提供共同 stall 条件，就不能把多个恢复事件当成多个不同语义目标；功能事件覆盖可单独报告，不能冒充原始 DUT branch。'+
            '保留原预算，先验证可达和 checker，再做独立 B 门槛。当前结果没有证明提取算法速度或 C 提示词长度是瓶颈。','',
            '## 失败轨迹的额外复核','',
            f"额外诊断共 {d['diagnostic_executions']} 次 Icarus 执行、{d['diagnostic_executed_cycles']} 周期，复用编译产物、零 API 调用；不计入模型的 B 预算，也不回写其指标。"]
        for r in d['failure_replays']:
            text += ['',f"重复 {r['repetition']} 第 {r['round']} 轮的引脚、队列和 checker 结果与原 Verilator 全部一致。"+
                f"{len(r['failure_diagnostics'])} 条失败诊断分为 {r['distinct_categories']}，输入假设违规 {len(r['assumption_violations'])}。"+
                '这些是诊断类别，不能算成相同数量的独立 DUT 缺陷。保留原 fail；双仿真一致只能排除这次观察的工具差异，'+
                '尚不能判定 DUT、checker 或规格解释中谁有错。']
        text += ['',f"完整诊断证据：[diagnosis.json](../{diagnosis.relative_to(ROOT)})。",'',
            '```sh',f'.venv/bin/python scripts/diagnose_spi_core_safe_b.py --input {folder.relative_to(ROOT)} --output {diagnosis.parent.relative_to(ROOT)}',
            f'.venv/bin/python scripts/report_spi_core_safe_b.py --input {folder.relative_to(ROOT)} --report {doc.relative_to(ROOT)} --diagnosis {diagnosis.relative_to(ROOT)}','```',
            '以上诊断目录已存在；重放请指定新目录，以保留原始诊断证据。','']
    doc.write_text('\n'.join(text));print(json.dumps({'gate':s['gate']['pass'],'tokens':total,'audit':a['status'],'report':str(doc.relative_to(ROOT))}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True)
    p.add_argument('--report',type=Path,default=ROOT/'docs/spi_core_safe_b_development_2026-11-04.md')
    p.add_argument('--diagnosis',type=Path)
    args=p.parse_args();report(args.input.resolve(),args.report.resolve(),args.diagnosis.resolve() if args.diagnosis else None)
