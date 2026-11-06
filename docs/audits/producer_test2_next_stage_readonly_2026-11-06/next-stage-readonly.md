# 同 IP 下一阶段：有界只读核查

状态更新：P17已PASS_WITH_LIMITS，已登记公开有限G1接受；本文仍只是下一阶段方案。
独立接受记录：docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/G1-final-acceptance-p17.json。
旧E04/PENDING输出保持原样，当前接受由P17与独立closure表达；新stage尚未获资源/API批准。
本轮只读取限定 proposal/P2摘要、protocol、配置、脚本和冻结数据元信息；
仅新增本文件，未改 E04、封存源或共享文档，未运行实验/API/版本查询/密钥检查。

## 1. raw test 的含义仍不明确

限定检索未发现独立命名的 raw test 注册或入口。现有 raw 用于 B 的原始覆盖反馈、
原始工具输出，也可能指 proposal 的刺激生成路径；不能自行解释成 A 或旧 formal 重跑。
这不是搜索全部历史后的全局不存在断言。父级应先澄清用户意图，再执行依赖该定义的工作。

经审阅 P2 摘要中的正式 proposal 问题是覆盖率/成本的刺激生成对照；test2 则固定刺激、
生成被动 monitor，评价有效检错/正确报警/unknown/成本。后者不能提高固定 DUT 覆盖率，
不能冒充原刺激研究。现有 P2 已有历史 pilot/图，新调用不是补造 P2 结果的必要条件。

## 2. 可复用的现有事实

- 同 IP：AXI frame-length-adjust FIFO，DATA_WIDTH8、MIN4/MAX8、FIFO32/8；
  `controller_done_study_v1.json::sources` 四份 RTL/top 哈希已核对一致。
- Claude frozen-v2 checker SHA：
  `b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee`。
  仅复用原 two-state/check_rows、accepted lengths1..12、dev尾32/final尾128范围；
  trace_done 是最终 post 元数据，无额外 DUT 输入/时钟。G1不扩大 oracle 范围。
  完全不改范围时预计额外 Claude 调用0；超范围须另备独立作者/复核包，不由 GPT 补 oracle。
- 原 driver：`axis_length_fifo_v1/public/driver.sv`，SHA
  `589ade00da15ae6c9383bd4eb6decda7537fa23e13e6ca59edf97c4e2e0ed56c`。
  monitor 编译/回放来自 `controller_monitor_done.py`、`controller_done_runtime.py`；
  原 cycle0 采样合同与 G1 toy 不同，不应静默修改成 G1 时序。
- public/prompt-packets-v2 审计记录 B/C common equal、raw_counter_count=3168、
  dev230cycles、C附加4groups；不是新覆盖率测量。`controller_done_packet.py` 显式
  allowlist仅含 spec/observer/RTL/三条dev观察和计数，不含reference/private/final。
- input freeze SHA：`d3e2373a00e86a13fffb92ee22216e70f08c35517f4a7a6542d2c7238a55c0f3`；
  evaluation freeze SHA：`8495938a07ab5938b31e20127a9ff2986f76428d6150016ede49d139e490ff32`。
  本轮核对其625绑定文件及原reference freeze，仅哈希，不重跑。
  162条记录的基础设施status complete不等于oracle全知/全PASS；原38unknowncontexts、
  raw12types及N10未确认可观测保留。旧final数据已使用并发布，复用只能称已知benchmark复测，
  不能称新的隐藏泛化集。reference源码未加载入上下文，仅核对哈希。

## 3. 最小有用新 pilot（未实现/未授权）

建议 B/C各1独立会话×3轮，共6候选、2final，全6轮冻结后评分。固定DUT/checker/
模型与每次cap，B=raw/common，C=B+verifiedEgraph，自有history，不反馈hidden结果。
这是工程复测/早轮成本探索，样本量不支持统计优势；无token-matched placebo时只比较反馈包，
不能归因纯语义。若用户要新 C-benefit 研究，应先准备同IP新的固定隐藏集及物理可达资格，
不得把旧final集悄悄当新heldout；该新数据阶段尚未实现，具体费用/物理预算UNKNOWN。

现有配置事实：OpenAI SDK Responses，`https://api.openai.com/v1`，`gpt-6.1-sol/low`，
Standard/default、store=false、implicit30mcache、每次64k输入/8192输出/120s，SDKretry0。
这是历史配置，不是重新核实的当前服务/价格推荐。新pilot如保留一次失败重试：
6正常/12最多generation，4预检counts+每attempt1count=10正常/16最多count requests；
generation最多768000输入+98304输出=866304tokens。count费用另计。
**当前美元费用UNKNOWN**，须核实当前官方价格/服务并新批具体收费stage；旧USD20已用于旧cohort，
不是新额度。未查询凭据状态；需要时只用原终端隐藏暂存流程，不在聊天收key。

现有脚本无法只改JSON直接跑小样本，必要新版本最小改动（本轮未做）：
1. generate_v2 的 literal3reps×6rounds；release/verify 的36snapshot/6session硬断言，
   final选取和新run路径均参数化，所有invalid/NOT_RUN也冻结。
2. 新请求/token/费用授权与ledger；BoundedModel虽支持较小request-count参数，旧caller、
   authorization与17.5USD guard/费率仍绑定旧72次，不能直接复用旧许可。
3. postprocess改为读取新release，去掉旧live-post硬编码目录/WAIT_ALL36/自动formal540。
   只做针对新日程的prompt隔离、mock/replay验证，不把旧36轮结果说成新测试。
   ABI/oracle/硬件/labels无需因此修改，不建立无关G2–G5框架。

## 4. 可精确计算的本地上限（复用现有数据时）

每个6snapshot cohort pass，假设全部候选可编译且所有轮评分；失败只降低实际工作量：

| 类别 | 上限 |
| --- | ---: |
| monitor compile roots，Yosys+Icarus，各60s |12（6+6）|
| development monitor replay roots，各15s |18|
| all-round score monitor replay roots，各15s |972（6×162）|
| monitor replay 合计 |990|
| monitor attempted cycles |204444|
| 新DUT物理仿真 / formal-native / 版本查询 |0 / 0 / 0|

静态计算：dev长度74+78+78=230；每候选162case共33844rows、最长214cycles；
6×(230+33844)=204444。每候选correct18case、rawfault144pair，unknown分母不删。
这都是candidate monitor在已保存DUT观察上的回放，不能计作新DUT可达性/RTL覆盖率。
逐调用timeout和=12×60+990×15=15570s，并非已落实的全局wall硬界或预计耗时；
新stage还应明确全局wall/cleanup政策。本文不授权实际执行。

若保留旧完整post的saved-response重新编译/dev回放和第二次fresh评分，总计24compile、
1980monitor replay、408888cycles；若另登记哈希相同日志的只读重评分，可省第二次工具pass，
但不是独立trial。额外mock/replay工具pass也要单列，不藏进live成本。

最小pilot建议先不附加formal。两final沿用旧日程将额外产生180个逻辑SBYjob
（36correct+144mutant，depth24、10/5s solver、720s/final整体），还含frontend/solver子进程
及FAIL后的物理见证，不能把180叫全部OS进程或已完整核定的native/witness成本。
该投影仍不证明128completion；不得自动重跑旧540或74未复现witness。

## 5. 授权边界与推荐顺序

P17接受后，可先在现有离线维护范围做旧all-round分数/实际tokens/time-to-target分析、
保留unknown/invalid分母，澄清rawtest，并准备上述小pilot登记和必要适配。
这些只是建议，本文没有实施。G1资格不自动解决旧74witness或证明C收益。

G1的setup8/native32/physical33已耗尽，不能借用/重置。新同IP阶段应单独明示本地compile/
monitor replay/DUT/native/cycles日程，不能声称来自G1余额；若要追加G1或做未获范围的
新formal/数据资格，先报告具体增量并获批准。对付费API，新的服务/模型/请求数/token/$
批准始终必需。一般离线、可撤销准备无需重复索取同一G1授权。跨IP继续暂停。

来源锚点：docs/MILESTONE2.md:54/92/137；docs/EXPERIMENT_PROTOCOL.md done-track；
controller_done_study_v1.json、controller_done_generation_v2.json；
generate_v2.py:114/140/149/152/166；controller_release_live.py:37/67；
controller_monitor_done.py:14/38、controller_done_runtime.py:25；
controller_done_grade_v4.py:22/49、controller_done_model_v2.py:8/17/28/60；
controller_done_formal_v3.py:22/73、controller_done_live_post_v2.py:14。
