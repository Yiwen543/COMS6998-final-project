# 自主离线资格与端到端复现

本轮没有API调用、新LLM重复或旧评分改写。所有旧DUT/独立Claude参考/候选/冻结保留。新控制与形式配置均另行登记。

## 可验证范围

- 原DUT/规格/被动monitor回放/API适配器/原始Coverage-3/typed+egg管线已审计；原始计数分母3168，开发三迹全部未命中1989点，明细在audit/uncovered-source-points.json。
- 各迹实际line/branch/expr/toggle分母及命中见audit/audit.json；行为义务不是RTL覆盖率，固定刺激的覆盖不会被生成monitor提高。
- 语义复核：{'status': 'fresh_ground_rules_and_egg_replay_passed', 'definition_checks_audited_not_rerun': 168, 'supported': 148, 'mapped': 142, 'unresolved': 6, 'raw_targets': 152, 'ground_rule_queries': 5882, 'ground_rules_verified': 281, 'qfbv_seconds': 0.48412750009447336, 'egg_engine_sha256': '1bded1623286dd2e0a37d8fc0f6e3e56edc32ba077dc2a6c3aef657a8a0bb4b5', 'egg_seconds': 2.0841243751347065, 'egg_iterations': 10, 'egg_stop_reason': 'Some(Saturated)', 'C_groups': 4, 'selected_source_points': 8, 'unhit_selected_points': 0, 'scope': 'Two-state static definitions vs Yosys cells, shared Slang frontend. FF Q and memory read cuts free; no memory/state invariants, reachability, four-state or sequential equivalence.'}。168项typed定义证书本轮核对，未重跑其整个前端；新鲜QF_BV/egg状态单列。
- LLM适配器代码与历史实际Responses/usage已核对，本轮未做网络连通性测试；离线资格入口不需要key。

## 规格义务控制

32个显式合成控制，标签{'INVALID_INPUT': 3, 'FAIL': 17, 'PASS': 9, 'UNRESOLVED': 3}；1044次候选回放、145152周期。invalid不执行候选，UNRESOLVED不计通过。样例由原独立checker判定；未证明所有样例在原DUT物理可达。因此“参考接受样例上报警”仅是规格一致性诊断，不自动称为原DUT误报。

| 组 | 重复 | 未检出的参考FAIL控制 | 参考接受控制上的报警/未知样例 |
|---|---:|---|---|
| B2_raw | 1 | input_never_accepted | 无 |
| B2_raw | 2 | input_never_accepted | 无 |
| B2_raw | 3 | input_never_accepted | 无 |
| C2_semantic | 1 | input_never_accepted | 无 |
| C2_semantic | 2 | input_never_accepted, missing_both_response, missing_data_response, missing_status_response | 无 |
| C2_semantic | 3 | input_never_accepted | 无 |

C重复2漏检丢失数据/状态/双响应的有限完成性，验证了旧满分指标的区分力限制；全部候选漏检一直阻塞到有限结束的输入。旧ABI没有结束标记，最后一种情况不能简单归咎于LLM。

## 形式资格与表示敏感性

| 诊断 | 配置 | 模式 | 原始状态 | 秒 | SMT2字节 |
|---|---|---|---|---:|---:|
| always_true | retained | bmc | TIMEOUT | 6.894 | 195663 |
| always_true | cone | bmc | PASS | 0.429 | 112733 |
| always_false | cone | bmc | FAIL | 0.387 | 113449 |
| always_false | retained | bmc | FAIL | 0.431 | 196373 |
| B2_raw-rep1-P0 | retained | bmc | TIMEOUT | 11.724 | 199362 |
| B2_raw-rep1-P0 | cone | bmc | PASS | 0.808 | 115795 |
| B2_raw-rep1-P0 | cone | prove | PASS | 0.747 | 115795 |
| B2_raw-rep1-P0 | retained | prove | TIMEOUT | 11.933 | 199362 |
| B2_raw-rep1-P0 | retained | cover | PASS | 0.646 | 198156 |
| B2_raw-rep1-P0 | cone | cover | PASS | 0.570 | 114589 |
| C2_semantic-rep3-P2 | retained | bmc | PASS | 6.993 | 202496 |
| C2_semantic-rep3-P2 | cone | bmc | TIMEOUT | 11.287 | 167137 |
| C2_semantic-rep3-P2 | cone | prove | TIMEOUT | 11.286 | 167137 |
| C2_semantic-rep3-P2 | retained | prove | PASS | 7.188 | 202496 |
| C2_semantic-rep3-P2 | retained | cover | PASS | 0.618 | 200439 |
| C2_semantic-rep3-P2 | cone | cover | PASS | 0.477 | 117213 |
| mutant-anchor-M02 | cone | bmc | FAIL | 1.337 | 202846 |
| mutant-anchor-M02 | retained | bmc | FAIL | 1.777 | 239142 |

v1资格失败完整保留：它把native断言报告的末状态当成实际报警状态。v2从VCD读取active/ok失败状态，在两个模拟器逐字回放输入，比较保留的SMT输出并复现候选报警；独立参考只判定真实物理前缀，没有补造输出。恒假控制得到参考PASS（候选误报）；M02锚点得到参考FAIL（真实mutant违规）。

输出裁剪提高恒真和B复位性质的可判定性，但让C已知稳定性性质超时；不能声称更小SMT锥必然更快。下表为固定源候选、同深度/时限、交错顺序的另一形式配置，不改旧473TIMEOUT，也不是新的模型效果试验。

| 组 | 重复 | BMC24 | prove | activation cover |
|---|---:|---|---|---|
| B2_raw | 1 | {'PASS': 1, 'TIMEOUT': 5} | {'PASS': 1, 'TIMEOUT': 5} | {'PASS': 5, 'FAIL': 1} |
| B2_raw | 2 | {'PASS': 3, 'TIMEOUT': 3} | {'PASS': 3, 'TIMEOUT': 3} | {'PASS': 6} |
| B2_raw | 3 | {'TIMEOUT': 4, 'PASS': 2} | {'TIMEOUT': 4, 'PASS': 2} | {'TIMEOUT': 4, 'PASS': 2} |
| C2_semantic | 1 | {'PASS': 2, 'TIMEOUT': 4} | {'UNKNOWN': 1, 'TIMEOUT': 4, 'PASS': 1} | {'PASS': 6} |
| C2_semantic | 2 | {'TIMEOUT': 6} | {'TIMEOUT': 6} | {'PASS': 6} |
| C2_semantic | 3 | {'PASS': 2, 'TIMEOUT': 4} | {'PASS': 2, 'TIMEOUT': 4} | {'PASS': 6} |

TIMEOUT/UNKNOWN/ERROR保留；归纳失败不是可达DUT反例。单槽prove仅涉及该性质、固定实现和假设；cover不证明正确性。

## 新接口的可运行离线准备

observer_contract_v3_draft.md与controller_monitor_done.py新增只读trace_done，仅最终post置1，不改DUT输入、不添时钟。4个基础设施控制验证marker时序和最终未接收请求可见；它们不是实验LLM候选，也不是新的GPT参考checker。现有Claude函数/规格保持原样。将来短形式检查的trace_done=0安全性投影不能证明有限完成性。新live继续关闭。

## 复现与限制

复现本完整离线流程（新目录，包含新的本地形式运行）：

```sh
.venv/bin/python -B test2/scripts/controller_offline_pipeline.py --output test2/results/offline-reproduction-NEW --formal all
```

本次入口可显式复用已完成的本轮formal证据；completion.json记录“新控制/回放”与“保存formal证据”分别来自哪里。所有工具版本、源哈希、未覆盖点、原始日志、失败及资源在目录中。不要把离线回放当成新模型重复，或将合成义务/等价类当RTL覆盖。

研究结论仍受一个已检查IP家族、3次生成重复、无token匹配placebo、满分语料和求解表示/墙钟敏感性限制。原模拟B/C首轮11/11、C tokens+6.919%；原短形式信号是描述性的。当前尚无整套monitor完整soundness证明，未来新增付费研究需另行具体登记与授权。
