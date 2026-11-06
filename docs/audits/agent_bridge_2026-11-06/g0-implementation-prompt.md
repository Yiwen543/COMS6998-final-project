继续 COMS6998 test2，在当前 D01 完成后的空闲安全检查点执行以下新授权的有界 G0 维护阶段。用户已明确同意 G0 适配器及轻量 fixture 测试，不需要再次询问。D01 原文及 P07/E05/draft 的历史 false 许可均保持不变；新增独立授权记录和新实现版本，不能就地改变旧许可或冻结证据。

<transcript_evidence>
助手：“你是否同意同时实施 G0 适配器并运行轻量 fixture 测试？这一步不会重跑旧实验或调用付费 API。”
用户：“同意的，如果需要使用付费api也可以找我发送”
</transcript_evidence>

先读 AGENTS.md、test2/AGENTS.md、紧凑 HANDOFF/STATUS 和封存 D01 接口。D01 phase SHA=675b772099469ad64603093569e0796aa814d24f73feeadcb24026df8b193ee2，manifest SHA=be07ee63e34dba49cee48750a6cfe230c61994b71925f8a9a85e406829288983。D01 正在由既有复核聊天 P08 独立审查，不要自行宣布它独立通过；您的维护实现可以继续，纸面审查发现实质问题时再在安全点处理。

授权范围：使用已有本地 Python/依赖，在全新、未被旧 freeze 绑定的 source/test/result namespace 实现 G0 离线 adapter/显式 schema，以及小型、非敏感、可复现的纯合成 JSON/text fixture 测试。实现内容按 D01 定义并明确支持矩阵：新格式版本/严格类型/nullability/身份和上下文/SHA/原始字节绑定/严格串行 request-terminal-call/parent count/资源限制/持续全局 resource_halt/NOT_RUN与missing usage的区分/immutable manifest-release和路径边界。输出完整性、科学归因、成本已知性三个独立维度；不能把摘要一致提升为 DUT/monitor correctness。原始链在 G0 可只做声明范围内的 artifact/phase/slot/width/来源绑定；若尚无独立 raw parser、独立标签或科学参考，明确 NOT_EVALUATED/UNRESOLVED，不伪装通用科学验证或完成 G1。

对 D01 44 个失败案例给出覆盖映射：能在纯合成元数据层实测的做有意义正例/拒绝/未决测试；依赖实际 native/物理/独立 oracle 的部分标 UNIMPLEMENTED 或 OUT_OF_SCOPE 并拒绝相应科学升级，不生成 SV/波形/真实 rows 来补齐。模板必须拒绝充当真实 grant/release；未知 usage/费用/invoice 保持 null+UNKNOWN。不能补造历史缺失 request/context，不能借旧硬编码 run/P01 锚认证新 run；并发/交错未支持时 fail closed。授权输入只能被离线验证，不得产生 dispatch、请求或凭据行为。路径不得越界、覆盖旧目录或借 symlink逃逸。

测试需覆盖跨 round/attempt/session 的持续 halt（count/generation/retry 都不能绕过）、重复/孤儿/缺失身份、context/prompt/schema/response/SHA篡改、非法派发顺序、有效NOT_RUN、缺usage仍未决、上限/模型/tier/cost子集、输出namespace覆盖及release失败路径。保留真实执行的精确 fixture 与结果绑定（深拷贝避免测试原件被后续变更）；P04原件响应绑定不一致应保留原样，只使用明确新 canonical fixture 证明回归，不声称旧原件原样 PASS。不为恢复上下文重跑旧实验或完整旧 suite。允许本次新 G0 的轻量 unit/fixture 测试；必要的保存文件只读解析必须声明只是离线复用。

硬边界：不运行 G1；不启动仿真/formal/monitor/旧 pipeline；不构造公开 SV controls/harness/科学波形或新实验数据；不调用任何 API、count/generation 或网络；不读取/配置/恢复 key或凭据；不安装、不删除旧结果、不改独立 Claude checker/旧分数/旧脚本冻结/旧 manifest，不commit/push。新维护记录仅 implementation=true、light_synthetic_fixture_tests=true，其余上述权限false。用户愿意提供 API key 不是付费调用授权；未来确需 API 时先报告具体服务、用途、预计请求数/模型/tokens/费用与时间上限、安全配置办法，等待针对具体调用的新确认，不要求聊天发送密钥，当前不处理凭据。

完成后封存新的 I01（或唯一新编号）phase.json/snapshot-manifest.json：实际 Git HEAD/worktree、所有 source/tests/fixtures/results与输入 SHA、支持与未支持矩阵、44项映射、真实命令/exit/失败与修订、原始负结果和资源用量、本次授权范围。共享 HANDOFF/STATUS 仍由您唯一写入，紧凑更新并保留旧正文。仅报告“实现及自测完成、待独立复核”，不要自签独立验收。保持冻结的 D01/E05/P05/P06/P07/旧分数及原始科学证据。后续由协调端将精确封存版本交给既有复核聊天；不新建代理或聊天。
