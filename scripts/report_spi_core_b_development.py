"""Report completed B development; retain not-reached trials and raw metrics."""
import argparse
import csv
import json
import os
from pathlib import Path

from run_midterm_fixed import ROOT,sha


def report(folder):
    s=json.loads((folder/'summary.json').read_text())
    if s['metadata']['status']!='completed':raise ValueError('Run incomplete; inspect preserved ledger')
    f=json.loads((folder/'freeze.json').read_text());rows=s['rows']
    if s['metadata']['freeze_sha256']!=sha(folder/'freeze.json'):raise ValueError('Freeze copy changed')
    compact=[]
    for r in rows:
        row={k:r[k] for k in ('mode','repetition','round','status','api_tokens','new_branch_points',
            'token_roi_new_branch_points_per_1000','attempts','failed_attempts','simulator_executions',
            'executed_cycles_including_replays','unique_generated_cycles','simulation_seconds',
            'round_wall_seconds','repetition_wall_seconds','failure_diagnostic_count')}
        row.update(groups_complete=sum(g['all_hit'] for g in r['groups']),groups_total=len(r['groups']),
            checker_verdict=r['checker']['verdict'],assumption_count=len(r['checker'].get('assumption_violations',[])),
            unresolved_count=len(r['checker'].get('unresolved',[])),
            distinct_failure_categories=';'.join(r['distinct_failure_categories']))
        for k,v in r['coverage'].items():row.update({k+'_covered':v['covered'],k+'_total':v['total']})
        compact.append(row)
    with (folder/'rounds.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(compact[0]));writer.writeheader();writer.writerows(compact)
    target_cost=[]
    for rep in range(1,f['development_budget']['repetitions']+1):
        rr=[r for r in rows if r['repetition']==rep]
        raw_first=next((r for r in rr if r['status']=='simulated' and all(g['all_hit'] for g in r['groups'])),None)
        first=next((r for r in rr if r['status']=='simulated' and not r['checker'].get('assumption_violations')
                    and all(g['all_hit'] for g in r['groups'])),None)
        target_cost.append({'repetition':rep,'target':'all frozen source groups completely hit',
            'raw_first_hit_round':raw_first['round'] if raw_first else None,
            'qualified_target_requires_legal_inputs':True,
            'reached':first is not None,'first_round':first['round'] if first else None,
            'api_tokens':first['api_tokens'] if first else None,
            'executed_cycles':first['executed_cycles_including_replays'] if first else None,
            'unique_generated_cycles':first['unique_generated_cycles'] if first else None,
            'simulator_executions':first['simulator_executions'] if first else None,
            'wall_seconds':first['repetition_wall_seconds'] if first else None,
            'final_groups_complete':sum(g['all_hit'] for g in rr[-1]['groups']),
            'final_verdict':rr[-1]['checker']['verdict'],
            'right_censored_at_round':None if first else f['development_budget']['rounds']})
    (folder/'target_cost.json').write_text(json.dumps(target_cost,indent=2)+'\n')
    os.environ.setdefault('MPLCONFIGDIR',str(folder/'mplconfig'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MaxNLocator,FuncFormatter
    fig,axes=plt.subplots(2,4,figsize=(16,7),layout='constrained')
    fields=[('api_tokens','API input + output tokens'),('executed_cycles_including_replays','Executed cycles (replays included)'),
            ('simulator_executions','Simulator executions'),('repetition_wall_seconds','Repetition wall time (s)')]
    for col,(field,label) in enumerate(fields):
        for rep in range(1,4):
            rr=[r for r in compact if r['repetition']==rep]
            if any(r[field] is None for r in rr):continue
            axes[0,col].plot([r[field] for r in rr],[r['groups_complete'] for r in rr],marker='o',label=f'B rep {rep}')
            axes[1,col].plot([r[field] for r in rr],[100*r['branch_covered']/r['branch_total'] for r in rr],marker='o')
            illegal=[r for r in rr if r['assumption_count']]
            axes[0,col].scatter([r[field] for r in illegal],[r['groups_complete'] for r in illegal],marker='x',color='red',s=75,zorder=5)
            axes[1,col].scatter([r[field] for r in illegal],[100*r['branch_covered']/r['branch_total'] for r in illegal],marker='x',color='red',s=75,zorder=5)
        axes[0,col].axhline(len(f['targets']),color='gray',linestyle='--',linewidth=1)
        axes[0,col].set_ylim(0,len(f['targets'])+1);axes[1,col].set_ylim(0,101)
        for ax in axes[:,col]:
            ax.set_xlabel(label);ax.grid(alpha=.25);ax.xaxis.set_major_locator(MaxNLocator(4,integer=field=='simulator_executions'))
            if field=='api_tokens':ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1000:g}k'))
    axes[0,0].set_ylabel('Complete source groups');axes[1,0].set_ylabel('Raw DUT branch counters hit (%)')
    axes[0,0].legend();fig.suptitle('Original SPI core: independent B development ('+s['mode']+'); red x = input violation')
    fig.savefig(folder/'cost_curves.png',dpi=170);fig.savefig(folder/'cost_curves.pdf');plt.close(fig)
    meta=s['metadata'];total=meta['api_usage']['input_tokens']+meta['api_usage']['output_tokens']
    legal_costs=[c for c in target_cost if c['reached']]
    cost_description='；'.join(f"重复 {c['repetition']}：{c['unique_generated_cycles']} 个新周期、{c['api_tokens']:,} tokens" for c in legal_costs) or '无合法达标试次'
    first_lengths='；'.join(f"重复 {r['repetition']}：{r['unique_generated_cycles']} 周期" for r in rows if r['round']==1)
    remaining_single=sorted({g['eclass'] for r in rows if sum(not z['all_hit'] for z in r['groups'])==1 for g in r['groups'] if not g['all_hit']})
    single_description=f"单独剩余的组编号为 {remaining_single}。"
    if set(remaining_single).issubset({51,56}) and remaining_single:
        single_description+='这些组分别涉及 FULLCYC / Dual 模式，并非都要求复杂恢复序列。'
    text=['# SPI core：独立 B 开发试跑结果（2026-11-04）','',
        f"模式：**{s['mode']}**。原登记的开发门槛：**{'通过' if s['gate']['pass'] else '未通过'}**。本轮只有 B，不能推断 C 优于或不如 B。",'',
        '独立 Claude v4 checker 与 GPT 固定 JSON driver 已通过 [有限冻结检查](spi_core_checker_freeze_2026-11-04.md)。'+
        '原版 OpenTitan core 包含真实子模块，17 组可达、seed-zero 的源目标中 8 组非平凡；3,107 个原始 DUT counter 全保留。'+
        '同一 SPI 家族已有开发历史，不能称为独立 held-out IP。','',
        f"固定版本 `{f['dut_revision']}`；仓库基线 commit `{f['repository_commit']}`，另附工作区实际文件 SHA-256。"+
        f"checker `{f['checker_sha256']}`；配置 SHA-256 `{meta['freeze_sha256']}`。",'',
        '预算没有变化：3 次重复 × 6 轮 × 最多 64 新周期，seed 8 周期；gpt-6.1-sol、low，输入 32,000 / 输出 16,384 tokens，'+
        '每请求 timeout 120 s、最多一次重试。无会话串用、无 solver/generated witness 或校准泄漏；独立重复不保证模型确定性。','',
        '| 重复 | 首轮未全部命中组 | 最后未命中组 | 后续组进展 | 完整/输入合法 | 最终 checker | 全部目标首次命中 |',
        '|---|---:|---:|---|---|---|---|']
    for d,c in zip(s['gate']['repetitions'],target_cost):
        reach=str(c['first_round']) if c['reached'] else 'not reached (legal inputs)'
        if not c['reached'] and c['raw_first_hit_round'] is not None:reach+=f"; raw hit round {c['raw_first_hit_round']}"
        text.append(f"| {d['repetition']} | {d['first_round_unhit_groups']} | {d['final_unhit_groups']} | {d['later_group_progress']} | {d['complete']}/{d['legal']} | {d['final_verdict']} | {reach} |")
    text += ['', '目标命中只看各个原始 source counter；等价组里每个源点都必须实际命中。'+
             '未达目标的试次保留，不能从成本平均中删除。开发 gate 另外要求三个重复都完整且输入合法，'+
             '至少两个重复首轮还剩两组，至少两个重复在后续轮次取得组进展。DUT failure 不等同于错误 testbench。','',
             '| 重复 | line | branch | expr | toggle | 输入+输出 token | 仿真次数 | 实际周期 | DUT 失败诊断/类别数 | 输入违规 |',
             '|---|---|---|---|---|---:|---:|---:|---|---:|']
    for rep in range(1,4):
        r=[r for r in rows if r['repetition']==rep][-1]
        cov=['%s/%s'%(r['coverage'][k]['covered'],r['coverage'][k]['total']) for k in ['line','branch','expr','toggle']]
        text.append(f"| {rep} | {' | '.join(cov)} | {r['api_tokens']} | {r['simulator_executions']} | {r['executed_cycles_including_replays']} | {r['failure_diagnostic_count']}/{len(r['distinct_failure_categories'])} | {len(r['checker'].get('assumption_violations',[]))} |")
    if any(r['checker'].get('assumption_violations') for r in rows):
        seen={};observations=0
        for r in rows:
            for a in r['checker'].get('assumption_violations',[]):
                observations+=1;seen[(r['repetition'],a.get('cycle'),a.get('category'))]=a
        text += ['',f'输入违规跨累计重放共出现 {observations} 条诊断，对应 {len(seen)} 个不同的（重复、周期、类别）记录；不能算成多个 DUT 缺陷。', '']
        for (rep,cycle,category),a in seen.items():
            text.append(f"- repetition {rep}，cycle {cycle}，`{category}`：{a.get('detail','')}。")
            trace=json.loads((folder/f'rep{rep}'/f"round{f['development_budget']['rounds']}"/'trace.json').read_text())
            if category=='cmd_transport' and 0<cycle<len(trace):
                before,after=trace[cycle-1],trace[cycle]
                text.append(f"  保存轨迹：cycle {cycle-1} valid={before['action']['valid']}、pre.ready={before['pre']['ready']}；"+
                            f"cycle {cycle} valid={after['action']['valid']}、pre.ready={after['pre']['ready']}。")
    text += ['',f"生成 API 调用 {meta['api_generation_calls']} 次，计数请求 {meta['api_count_requests']} 次；"+
             f"API 输入 {meta['api_usage']['input_tokens']:,}、输出 {meta['api_usage']['output_tokens']:,}，合计 **{total:,} tokens**。"+
             f"未知用量尝试 {meta['api_usage']['unknown_usage_attempts']}。cached/reasoning 是子项，不重复相加；未凭空估算 API 美元费用。",'',
             f"编译 {meta['compilations']} 次 / {meta['compile_seconds']:.2f} s；仿真 {meta['simulation_executions']} 次 / {meta['simulation_seconds']:.2f} s；"+
             f"实际执行 {meta['executed_cycles']:,} 周期（含 seed 和累计重放）；端到端 {meta['elapsed_seconds']:.2f} s。"+
             '语义预处理复用已冻结证据，本轮新增为 0；其历史成本不能从整个项目成本中删除。checker 建设和 mock 成本另记。','',
             'Token ROI 定义：相对共同 seed 新命中的 DUT branch counter 数 / API 输入加输出 token × 1,000；'+
             '每轮原始数值保存在 CSV。图中每条线是一个独立重复，wall time 不含该重复之前的编译，'+
             '完整 run wall time 在 metadata 单列。红色 × 标记输入违规的 raw counter 观测，保留但不作合法达标。重复很少，只作描述，不做显著性或泛化声明。','',
             f"![逐重复成本曲线](../{folder.relative_to(ROOT)}/cost_curves.png)",'',
             '需要保留的局限：普通轨迹已经覆盖多数目标，TX/RX 时间事件共用一个组合 stall group；'+
             '即使 B gate 通过，也只说明没有在原预算的首轮立即饱和，并不保证 C 有收益。'+
             'RX 采样不稳定、未完成命令均保留 inconclusive，软件复位/dummy 在此次范围之外。'+
             '公开文档的 byte-order 合同是登记的项目解释，未获上游勘误确认。','',
             ('下一步可准备冻结的 A/B/C/token-matched placebo 对照，仍需独立方法审阅及明确 live 调用预算；本脚本没有自动启动 C。'
              if s['gate']['pass'] else '本次不启动正式 A/B/C/placebo。保留原预算与失败原因；不能根据本结果缩短预算或删除不理想的重复。'),'',
             '## 对下一轮的诊断', '',
             f'合法达标成本：{cost_description}。首轮实际新周期为：{first_lengths}。'+
             '轮次差异必须结合预算使用情况解释，不能直接等同于 IP 的固有深度。'+single_description+
             '这比旧 FSM 首轮全满更有可测空间，但还不是 C 优势的证据。','',
             '输入违规与原始覆盖率是不同量。高 raw branch 命中不能使违反握手合同的刺激变成合法；'+
             '出现 cmd_transport 问题时，需要核验相邻周期的 valid/payload 与 pre.ready，区别 DUT 错误和刺激错误。'+
             '逐周期开环 JSON 对握手预测的要求，是需要与 e-graph 效果分开分析的因素。','',
             '建议另行预登记一个协议安全的固定 driver 版本：模型提交 command/TX offer，driver 只负责保持 valid/payload 到实际 handshake，'+
             '所有等待周期都消耗同一 64 周期预算，超出预算保持 pending，不暗中补 drain 或执行额外周期。'+
             'GPT 实现 driver，Claude 独立审阅接口合同；原 Claude checker 的 expected-output 逻辑不由 GPT 修改。'+
             '先重新验证双仿真器、正反控制与计账，再用相同预算做新的独立 B 开发试跑。'+
             '这是明确的新实验版本，不修补本次模型答案、不覆盖当前结果，也不能仅挑一个成功重跑替代失败重复。'+
             '其后 C 只补充与 B 同一覆盖页对应的已证明关系，placebo 按自身轨迹的 shadow-C 实际 API token 计数匹配。','',
             f"证据：[`summary.json`](../{folder.relative_to(ROOT)}/summary.json)、[`rounds.csv`](../{folder.relative_to(ROOT)}/rounds.csv)、"+
             f"[`target_cost.json`](../{folder.relative_to(ROOT)}/target_cost.json)，同目录有逐调用/逐轮 JSONL、提示词、完整动作、trace 和 coverage.dat。",'',
             '```sh',f'.venv/bin/python scripts/report_spi_core_b_development.py --input {folder.relative_to(ROOT)}','```','']
    audit_path=folder/'audit.json'
    if audit_path.exists():
        a=json.loads(audit_path.read_text())
        text += ['## 保存结果的独立计账核查','',
            f"18 个 prompt 与本重复先前执行证据精确重建一致；{a['all_batches_raw_counts_and_trace_checked']} 次原始覆盖文件、动作与 trace 核对通过。"+
            '输入/输出 usage 与各轮累计和总账一致，原始分母身份不变。模型和 checker 正确性不由这些完整性检查证明。','',
            f"额外观察：{len(a['raw_magnitude_decreases'])} 处 counter 的原始 magnitude 在相邻独立进程的累计 replay 间减少，"+
            '本次均减少 2；没有任何非零覆盖点变为零。最初核查误把原始 magnitude 必然单调作为断言，随后修正核查口径，原始计数从未改写。'+
            '组合计数与 simulator evaluation/settle 活动有关，并不等于硬件周期次数；终止与继续执行的边界活动是可能来源，未做额外因果隔离实验。'+
            '全部差值保存在 audit.json / counter_decrease_observations.json。覆盖比例仍只用该轮真实 hits>0，不能用跨进程 max 或求和替代。','',
            f"核查状态：{a['status']}；暂存 OpenAI key 已删除：{a['openai_staged_key_removed']}。",'',
            '```sh',f'.venv/bin/python scripts/verify_spi_core_b_run.py --input {folder.relative_to(ROOT)}','```','']
    (ROOT/'docs/spi_core_b_development_2026-11-04.md').write_text('\n'.join(text))
    print(json.dumps({'gate':s['gate']['pass'],'mode':s['mode'],'tokens':total,'report':'docs/spi_core_b_development_2026-11-04.md'}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);a=p.parse_args();report(a.input.resolve())
