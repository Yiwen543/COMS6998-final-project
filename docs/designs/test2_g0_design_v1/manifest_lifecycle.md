# 清单／release 的纸面生命周期

DESIGN_PREPARATION_ONLY。两个 JSON 文件均为 **TEMPLATE_ONLY_NOT_A_VALID_RELEASE**。它们只列字段类型、条件和 `<PLACEHOLDER:...>`，不是运行时 schema 或实例，不能交给旧 runner/validator，更不是用户 grant。JSON 能解析不表示清单、adapter 或实验通过。

## 模板解释

`manifest.template.json` 描述未来输入／产物清单；`release.template.json` 描述未来冻结状态、失败／未决保留和成本边界。`field_descriptors` 不是实际 artifact 列表。`placeholder` 不能被当作 run ID、路径、SHA、grant 或结果；它提示后续获准实现必须采集什么。尚未生成的必需值是待定，而不是有效默认值。真实 unknown 应为 null＋原因，不是占位符；但此模板不是任何真实 unknown 的测量结果。

本设计包／D01 的实际来源 manifest 只证明文档文件及输入来源 SHA，与这些未来实验模板严格分开。它不能授权 native 或认证 monitor／128 周期正确性。

## 未来生命周期（仅规格）

| 阶段 | 必须保留的内容 | 允许的后续变化／拒绝条件 |
|---|---|---|
| 文档模板 | 文档版本、占位标记、false 权限、null 入口 | 只可审查／新文档版本；不转成实际运行记录 |
| 新 registration 草案 | 实际合同、角色、来源、公开／隐藏边界、资源提案 | 先获得新范围及资源授权；草案或旧 grant 不允许执行 |
| 获准的新输入封存 | 独立 grant 身份、源／工具／配置／种子／输入 SHA、支持格式、预先规则 | material 改动须新版本，不能就地替换；无独立锚不能宣称独立历史真实性 |
| 执行中的只追加证据 | 真实请求和 terminal/error、全局 halt、全部 attempted/NOT_RUN/invalid/unknown、原始日志和成本 | 不覆盖、删除或补造旧事件；缺失 terminal 保留缺口；halt 后不再派发 |
| 全轮候选冻结 | 每轮 prompt/response/candidate/feedback/snapshot/可见性和来源绑定 | 在所有预定轮次冻结前不做 hidden 评分；未运行／无效轮次仍在 inventory |
| 评分／native 链冻结 | 原始独立 reference、physical/monitor/native 各层及所选边界、分母／重叠／unknown | 原始 mode/status 不改写；integrity、科学归因、费用已知性分开 |
| 独立接受身份 sidecar | 精确 source/tests/results/input/review/manifests SHA 与范围 | 只新增 sidecar；不回写已冻结清单、旧分数或报告；接受不是新执行授权 |

## 路径与拒绝覆盖

未来新 run/output namespace 必须未占用，先确认输入只读与输出 allowlist。存在的目标目录不得覆盖、清空、拼接另一 run，或借路径符号链接越出范围。输入路径必须规范化并保持可见性边界；任何 secret 目录均不在输入范围。实际实现细节与攻击测试尚未创建。

内容哈希需要带算法、被哈希对象、字节／规范化规则和生成来源。源、配置、工具与 flags、input、prompt、candidate、checker、原始层间 artifact 和 release 必须互相绑定；“两份同一 producer 摘要相同”不构成原始链独立核验。没有历史锚的新增 metadata 可记录当前来源及声明边界，不能宣称独立历史执行或科学归因。

## 失败、分母与成本

每个预定 arm/session/round/attempt 都必须有完成、错误、invalid、NOT_RUN、missing 或 NOT_REACHED 的明确状态。原始故障／pair／未观察／unknown 分母不因结果改变；合成公开控制不是新 DUT fault 或 RTL coverage。candidate 不评分自身。

保存 input/output/total token 与 cached/reasoning subset，另列 count/generation 请求、重试、编译、物理运行／周期、monitor replay、formal mode/时间和复现成本。已知数值按来源保留，缺 usage／费用／invoice 为 null／UNKNOWN，不能用预算预留填充实际消费。NOT_REACHED 有已耗成本；native timeout/unreached cover 不改判通过。正确控制误报、未知、无效、未达到目标分开。

所有未来可执行产物、独立标签、grant、实际路径和 SHA 当前均未产生。任何把占位模板移除标记后直接称为 registration/release 的行为，都违反本设计。
