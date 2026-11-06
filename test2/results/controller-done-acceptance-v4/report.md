# trace_done controller study: offline qualification and acceptance

2026-11-05，实际 Git main HEAD `c25180848ebfe9a1f49da0aa5f579cac913e6428`。审计状态 `accepted_offline_with_scope`。新模型/API 调用均为0；没有安装、提交、推送或读取密钥。旧交接的00e0dd9是历史 HEAD。

## 已实现及边界

新登记 `controller_done_study_v1.json` SHA256 `68ef21cc901f735bafe2509040ff7ee47d5afc6c56e1643650fe1aece005abb7` 早于新数据测量。新 task `axis_length_done_v1` 保持四份 DUT RTL、规格及 Claude frozen-v2 checker 完全不变。独立 checker SHA256 `b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee`；其可复用范围仍是 byte/MIN4/MAX8、每帧1..12接收字节、复位清空及独立数据/状态通道。GPT 没有编写或修补 oracle。

新 runtime 复用旧原型的被动编译器/头部，另行接入提示包、逐轮编译、开发反馈、六个 own-history 会话、36轮快照、saved-response replay 及独立评分。旧冻结运行器不改。`trace_done` 只在最后一个 post 可见，其余所有 pre/post 为0；没有新 DUT 输入或额外上升沿。终点检查由已更新状态加组合逻辑启用。

B=完整原始 RTL 覆盖反馈，C=B+原有已验证 E-graph 源码语义反馈。两臂共同部分逐字段相等，包含完整 RTL/规格/开发观测/3168个独立源计数器，采用可逆字典和观测 RLE，不筛选计数器。C只有四组已验证组合反馈；其位宽、guard和来源保留。未把组合等价证明说成时序证明。没有 placebo；将来 B/C 结论只能属于整个反馈包。

## 固定新数据与物理证据

开发种子6998201..3，三条74/78/78周期；隐藏输入种子6999301..6，各214周期，其中128周期为尾段。开发最小尾段32，最终128。种子、动作、来源、单行故障哈希和工具版本均保存。12个新故障哈希与旧目录无重合，但同属已研究 IP/规格，不能宣称未见 IP 泛化。隐藏动作、参考实现、故障、判定和轨迹均不进入候选提示；显式 public allowlist 加实际提示哈希受审计。

新物理资格实际26次 DUT build、162次模拟器运行、33844周期。正确 DUT 18/18参考 PASS，9组双模拟器有效信号一致。故障全集12类/144个模拟器轨迹对；11类至少有参考失败，N10所有12对未暴露，保留在原始分母。N02/N03各有2对参考 PASS。38个故障对的 definite FAIL 同时带 oracle unknown；不能改成完整通过。evaluation-freeze 在任何新 candidate 运行前封存。

实际 Coverage-3 为3168=110line+176branch+248expr+2634toggle，开发集并集仍有1970个计数器未命中。每条分别2119/2062/2044未命中。计数器来源/分母逐项保留；行为义务、故障召回、合成控制和等价类均不称为 RTL 覆盖率。此轮只审计/复用原有语义证书，不声称刚重跑 E-graph 证明。

## 完整离线路径结果

36轮 mock +36轮 saved-response replay 均完成，全36轮冻结先于隐藏评分；最后 compile-valid 轮选择，无隐藏结果修补。两臂使用完全相同的人工 plumbing 序列：第一轮总报警、第二轮不激活、3..5轮总通过、第6轮终点输入/数据帧/状态帧债务检查。它不是 LLM candidate/oracle，也不能用于推断 C 收益。

两套独立评分各5832次 monitor replay、1218384周期；开发各108次/8280周期。全36轮提示、源码、开发反馈与评分一致。最终各会话正确控制均无报警/unknown；检出 N01/N02/N03。严格分层如下（每个最终程序，类别可重叠）：

| 指标 | 原始资格对 | definite 检出 | fully resolved 检出 |
|---|---:|---:|---:|
| 呈现 valid 的 sampled safety |106|10|0|
| 无先前 sampled violation 的响应完成性 |20|20|20|
| 最终仍呈现但未被接收输入 |10|10|0|

N01同时属于 safety/输入完成性，且有未知尾段上下文；不得把10个 definite 检出写成10个完整通过。N02/N03为独立已决响应完成性。所有38个未决上下文、未观测 N10、原始144对、正确源和故障源上的参考 PASS 报警均单独保留。第一轮错误报警与第二轮 vacuity 不获检错分；6会话到达全部11类的目标均 `NOT_REACHED`。实际 token/美元和 token ROI 是未知，不能将 mock 零 API 调用解释成免费高效率。

## 形式日程与成本

固定 cone profile 由基础设施控制确定，未看 C 哪个配置更好。深度24/z3；每最终程序正确源6槽×bmc/prove/cover，每job10秒，12故障×6槽BMC每job5秒，共90job、540 solver-seconds及720秒总体预算；六程序共540job。B/C交错，无臂特定重试。新见证桥保留输入/对可用 SMT 输出做对照，直接定位 active/ok 失败状态，双物理模拟器还原后用未改变的 Claude checker 判真实前缀。缺字段、X、不同步或预算耗尽均未决。额外加固将剩余总预算传递给物理编译、物理仿真和候选回放；预算辅助测试与新版7个控制已验证。

实际 mock 540job完成，298.276秒：504PASS、36未触发的 activation cover FAIL。终点程序在 trace_done=0 下从不激活，因此这些 safety PASS 大量是空激活投影，不证明监视器完整正确，更不能证明128周期完成性。6个程序实测各48.8..50.6秒。这个540job运行使用加固前、正常默认行为相同的源；实际源快照已保存，deadline失败路径随后由单元测试/新版控制验证，未冒称重跑540job。

控制v2七个job保留2TIMEOUT，控制v3七个job保留1TIMEOUT。retained真控制在v2超时而v3通过，说明时限敏感性；规格pad-length控制仍TIMEOUT。cone true/false控制及真实 N05 dual-simulator/独立参考失败见证均通过。三次物理见证每版6次物理运行/30周期，两个版本共12次/60周期。包括v1结果汇总错误前的1个native PASS，本次新增本地形式job共555=508PASS/44FAIL/3TIMEOUT。

资源分项见 resource-ledger.json：162数据物理运行之外另12次见证物理运行；两个开发108+108回放与两个评分5832+5832回放单列；单位测试开销不混入实验总量。命令有并行重叠，因此不把各分量秒数相加冒充总 elapsed。原始31/473个历史超时等旧负结果均未改。

## 验证与保留的失败

当前 test2 全套76项单元/集成测试实际通过，日志 `controller-done-tests-v4.log`，不是全仓库测试。独立审计核对11664份原始 gzip 评分日志、2436768评分周期、每槽 active/ok 位与报警/unknown列表、sealed物理行对应的实际 HEX向量、540个native形式状态和全部旧3486/212/239冻结成员与两份旧分数哈希。Icarus的5832对原始日志因 `$finish` 记录各自编译路径而非字节相同；只替换准确已知 run-root 前缀后全字节相等，每份原始SHA仍独立保留。

失败不删除：formal-controls-v1在一项native PASS后触发Python重复字段 TypeError；修复汇总字段后用v2新目录。初始unit测试错误地期待异常，而编译器已返回拒绝状态，修正测试后保留旧失败日志。acceptance-v1拒绝路径不同的原始日志，v2起显式路径规范化；v3增加原始bit/向量核验，v4核对当前加固源及76项测试。旧结果及未提交工作都保留。

## 复现与下一门禁

现有数据/结果只读复核：`.venv/bin/python -B test2/scripts/controller_done_acceptance.py --output test2/results/<NEW-AUDIT>/acceptance.json`。新输出必须不存在。此命令不重新仿真/求解/调用 API。

组成阶段均已实际通过命令运行：`controller_done_data.py --prepare --measure`（只为首次新数据生产，现有目录不再运行）；`controller_done_loop.py --mode mock`；同脚本 `--mode replay --replay-source ...`；`controller_done_score.py --run ...`分别评分两次；`controller_done_formal.py --controls`、随后 `--run ... --qualification ...`；`python -B -m unittest discover -s test2/tests -v`；上述 acceptance 命令。各命令 stdout 和原始记录在具名结果目录。

新增单命令编排 `controller_done_pipeline.py --output test2/results/<NEW-REPRO>`复用已封存新物理数据，重新执行 mock/replay/评分/形式/测试/审计并保存执行源。编排入口本身尚未整体调用；已验证的是以上分项实际执行路径，不声称刚完成另一遍单命令fresh run。不要为恢复上下文自动执行。

下一项外部门禁是独立 Claude scope review 与4次实际 provider 输入计数；已准备 `reference/scope-v2/{review,author-conditional}` 和 `qualification/api-preflight-v2/proposal.json`。复用范围未扩大；如复核指出确有 oracle 合同缺口，必须单独授权 Claude新版本作者+全新复核，GPT不静默修补。当前作者调用授权0，review/计数也未调用。真实 B/C live 尚无授权文件或新 live freeze；旧授权不复用。后续请求只先申请上述预检，不能默许36轮生成。

拟议预检：Claude-opus-5-5独立无工具review最多1次，CLI硬预算4美元，600秒；输出请求<=3000tokens（无单独硬output-token cap）。OpenAI gpt-6.1-sol仅4次计数、0生成、0输出，检查64k输入门槛；endpoint费用官方未明确列出，预留最多5美元且不宣称免费。合计申请支出预算9美元；实际计数未到前不声称token通过。具体限制、已过门禁、提示SHA及后续未授权36..72请求/64000输入/8192输出的候选预算在proposal。模型价格依据[官方模型页](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、[官方计价页](https://developers.openai.com/api/docs/pricing)，计数接口依据[官方说明](https://developers.openai.com/api/docs/guides/token-counting)，读取日期2026-11-05；这些页面没有确认本账户费用/可用性。隐藏终端暂存只在该付费阶段获批后进行，同阶段保留到完成，不聊天收key。
