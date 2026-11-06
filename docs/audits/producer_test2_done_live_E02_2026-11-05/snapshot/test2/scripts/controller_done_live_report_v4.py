"""P01 reporting correction only, retaining the v3 report and scientific results."""
import argparse
import json
from pathlib import Path
from common import ROOT, BASE, dump, sha
from controller_done_live_report_v3 import render as base_render


def render(audit,diagnostic,disclosure,out):
    d=json.loads(disclosure.read_text())
    for n,h in d['input_sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Disclosure input changed: '+n)
    if d['status']!='P01_R1_REPORTING_ANALYSIS_READY_FOR_P02':raise ValueError('Disclosure analysis missing')
    base_render(audit,out,diagnostic)
    p=out/'report.md';text=p.read_text().replace('# test2 trace_done 控制器：真实 B/C 运行与最终审计 v3','# test2 trace_done 控制器：真实 B/C 结果与P01披露修订 v4',1)
    opening='''本v4仅修订分析与报告，处理独立审查P01-R1；旧v3报告、所有候选、分数、原始形式状态和oracle均保留。P01结论为CHANGES_REQUIRED，本修订仍待P02独立复核，不能由生产者自行宣布独立通过。没有新DUT、formal、monitor回放或付费调用。

'''
    text=text.replace('## 结果与可支持的结论',opening+'## 结果与可支持的结论',1)
    table=['| 组 | DUT | native BMC FAIL | 物理选定报警复现 | 未复现／仍未决 | 已检查较早前缀FAIL | 未记录参考判定 |', '|---|---|---:|---:|---:|---:|---:|']
    for r in d['BMC_chain_summary']:
        table.append('| '+' | '.join(str(r[k]) for k in ['arm','DUT_kind','native_BMC_FAIL','physical_alarm_reproduced','not_reproduced','reference_prefix_FAIL','reference_verdict_not_recorded'])+' |')
    x=d['x_representation_example'];root=BASE/'results/controller-done-live-formal-v2/C2_semantic/rep1/correct/P4-bmc'
    candidate=BASE/'results/controller-done-live-v2/C2_semantic/rep1/round6/compiled/candidate.sv';smt=root/'work/model/design_smt2.smt2';physical=root/'physical/result.json';prep=root/'work/model/design_prep.ys'
    section=f'''## P01-R1：native、物理报警与参考判定分层

540项native结果仍是75PASS、104FAIL、361TIMEOUT。**104个FAIL分为94个BMC FAIL、7个prove FAIL、3个cover FAIL**。这三种模式的FAIL不能混算为检出的故障；prove失败不等于可达反例，cover未达到不等于断言误报。

**94份BMC FAIL＝20份选定报警物理复现＋74份未复现**。20份在保存的literal输入双模拟器回放中复现了选定slot报警，冻结Claude checker对它们的**较早物理前缀**均判FAIL；这仍不是选定pre(S)同采样／同类别的参考确认。74份均保持unresolved，全部来自C，包含**7份正确DUT、67份mutant**；物理报警没有复现，不等于参考oracle返回UNKNOWN，也不能称为已确认的物理候选误报。由于bridge在参考调用前拒收这些报警，本批74份没有记录参考verdict。

{chr(10).join(table)}

这里的20份和74份都不能扩展为总体monitor正确性结论。B/C物理较早前缀FAIL类型union仍为B3／C7（逐重复3/0/3与7/6/0），只作次级诊断；固定轨迹11/11、原input0/10及全部成本和未知都不变。**native FAIL数量和运行时间差不能只解释为候选能力差异**，还受表示、求解和物理映射限制影响。

### 已确认的一个X→anyseq实例

在C会话1最终候选P4中，[candidate.sv:73]({candidate}:73)使用四态未知检测：

```systemverilog
{x['candidate_line_73'].strip()}
```

保存的[design_prep.ys]({prep}:12)包含 `setundef -undriven -anyseq`。[SMT第85–89行]({smt}:85)将一个相关位声明为 `$auto$setundef...` 生成的 `formal_top#16` anyseq；[SMT第1229行]({smt}:1229)把该位用于第73行的case-equality比较：

```smt2
{x['smt_lines_85_89'][0]}
{x['smt_line_1229']}
```

因此该保存实例中的字面X检测并非原样保持四态SV意义：它在SMT里与不受约束的二态anyseq位比较。对应[物理结果]({physical})明确保留 `unresolved`／“Formal selected-slot alarm not reproduced at observed failing physical pre sample”。这是已确认的**一个具体表示限制实例**；**不能把全部74份未复现一概归于这个根因**。原始SV、prep、SMT、物理结果SHA均绑定在disclosure分析manifest中，native结果不删除、不改判PASS。

### 自动审计能力与独立复核边界

P01-R2/R3属于仍开放的自动代码能力缺口：audit_v3尚未独立闭合全部VCD→literal输入→双物理PRE/POST→rows→MON→参考前缀链，也未完成returned事件与calls的逐条双向唯一绑定。P01已独立核验本批全部94条保存见证链、188份物理执行、94份MON，以及36calls／144ledger事件，未发现本批错配。这支持本批保存数据，**不等于自动审计代码已修复或拥有未来篡改检测能力**。详见[P01审查]({ROOT/'docs/audits/agent_bridge_2026-11-05/P01/review.md'})；本v4不声称关闭R2/R3代码缺口。

历史H1/H2（旧252条未决漏标及旧offline acceptance分类范围）保留，不作为当前v4主分数错误。共享冷缓存L1也保留：26次构建共30.548166s，当前最慢final652.091561s&lt;720s且NOT_RUN_TOTAL_CAP=0，说明本批没有预算截断；**不能由此排除任何时间顺序影响**。未来试验须在结果前登记预构建／缓存及共享预处理成本条件，本批冻结日程不改。

'''
    text=text.replace('## 成本、审计与文件',section+'## 成本、审计与文件',1)
    text+='\n本次披露复现：`controller_done_formal_disclosure_v1.py --output NEW_DIR`仅解析保存证据；`controller_done_live_report_v4.py --audit ... --diagnostic ... --disclosure NEW_DIR/analysis.json --output NEW_REPORT_DIR`生成新报告。精确实际命令与E02快照见producer E02阶段交接；提供命令不表示启动了新native实验。\n'
    p.write_text(text)
    sources=[Path(__file__).resolve(),BASE/'scripts/controller_done_live_report_v3.py',BASE/'scripts/controller_done_formal_disclosure_v1.py',BASE/'scripts/controller_done_live_audit_v3.py']
    dump(out/'manifest.json',dict(report_sha256=sha(p),audit_sha256=sha(audit),diagnostic_sha256=sha(diagnostic),disclosure_sha256=sha(disclosure),
        disclosure_manifest_sha256=sha(disclosure.parent/'manifest.json'),source_sha256={str(s.relative_to(ROOT)):sha(s) for s in sources},
        input_sha256=d['input_sha256'],new_API_calls=0,new_native_experiments=0,old_scores_changed=False,independent_review='P01_R1_REVISED_P02_PENDING'))
    dump(out/'review-status.json',dict(status='P01_R1_REVISED_P02_PENDING',independent_acceptance_claimed=False,R2_R3_automatic_code_gaps='OPEN_BATCH_INDEPENDENTLY_CHECKED'))
    return p


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('audit','diagnostic','disclosure','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();print(render(a.audit.resolve(),a.diagnostic.resolve(),a.disclosure.resolve(),a.output.resolve()))
