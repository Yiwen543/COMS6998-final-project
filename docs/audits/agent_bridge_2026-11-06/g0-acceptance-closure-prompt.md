请在当前空闲安全点完成 G0 元数据收尾，不能再进入实施或下一门禁。I01 精确版本已获既有独立 P09 PASS_WITH_LIMITS，未发现当前可复现的范围内错误接受，无阻塞/非阻塞新发现。无需重跑任何测试、companion、实验或审计来收尾。

接受证据：
- P09 docs/audits/agent_bridge_2026-11-06/P09_g0_implementation/review.json SHA af863e7f8e5ca4d012a773a7d2a1f16736cf85cc08500f9ece45d0784b415850；review.md SHA f8dbd9ae11bb3590b8164641724528c4722e6974fcb6a32e2917723edd3e1a61。
- P09 evidence-manifest.json SHA 01df254c3b1ea5bee0fe56251777a34e5d25583dfd2d698f27ee4e2055df1f4e（2279文件/2link文本）。协调端已核验全部内容与symlink文本，无差异；独立review identity wrapper snapshot-manifest.json也可绑定。
- I01 phase SHA 0b6b49b4ca1ae4ea55d172d08e6d8d5f3b90eb26b5ff44ca24a023c4ff5a5bbe，manifest SHA c49c8c409757322fe49c28142f77cad133fdf9407256e3dcb96ac3ffa2869eb6。8695文件/6link文本与41保护来源无漂移。
- P08纸面接受仍单独限定，review SHA f93d6fb191c851a6457318869521a10ac4a987946aeb95dffe098383625ea6ef；P08-N1缺terminal/匹配errorretry行为在P09独立新探针得到证据，不回改D01、不把producer未存的专门测试写成当时已存。

新建 test2/results/g0-adapter-acceptance-p09-v1/independent-acceptance.json（路径若已存在，另取新版本绝不覆盖），绑定P08与P09各自scope/decision、exact reviews/manifests、I01phase/manifest、finaladapter/schema/tests、coverage map/support matrix及相关input SHA。记录本版只接受origin=SYNTHETIC_FIXTURE、显式身份、严格串行closed-shapes JSON/text元数据能力；不是real/legacy-run gate、授权真实性认证或并发支持，未实现真实VCD/literal/PREPOST/rows/HEX/MON parser/独立标签；science仍NOT_EVALUATED、费用/invoice缺口UNKNOWN。

可准确列独立验证账：fresh93项通过，469 exact saved-byte cases状态复现0差异（首轮8失败保留；6个FileNotFoundError绝对路径随snapshot变化已显式归一化，排除计时后0未解释差异），28独立探针、6CLI控制符合预期。不要合并这些计数成“独立模型试验”或科学样本，不把历史6轮runner结果描述成本轮重跑；producer早先rawPTY收据未存限制保留。P09只读mapping KeyError为review harness事件，不是产品失败；按证据保留不掩盖。

仅由您更新HANDOFF/STATUS顶部紧凑当前接受入口，旧正文逐字保留。新增唯一 docs/audits/producer_test2_g0_C01_2026-11-05/closure.json（若冲突另唯一名），记录实际HEAD/worktree、sidecar与本次元数据SHA和原文保全、受保护证据未变、0tests/API/native/key/actions，并封存本次仅元数据的来源清单。I01/D01原phase/PENDING历史、所有快照和源码、P08/P08a/P09、E05draft/plan/旧grant/旧scores/checker/结果原件均保持字节不变。

保留P04 exactv1REJECT订正及未知序列化原因、P05/P06精确format/cohort限制、P05-N1backlog、F1/selected sample/category/128completion/H1/H2/L1/费用未决。G0实现与复核的维护阶段完成，不授权G1/native/API/数据/count/generation/paid/live。现在不要申请或读取key，不调用服务，不安装、不删除、不commit/push。未来paidAPI须先给具体服务/用途/模型/请求/费用/时间帽与安全配置方案，由用户针对具体调用确认。收尾后报告明确产物与SHA并等待，不自行延伸研究任务或重做PPT。
