# Hallmark 使用回溯与适用性核查

**不能声称过去每轮都使用了 Hallmark。** 已确认成功安装；所检查的 P01–P09 复核产物没有留下 Hallmark 读取或具体应用记录。未见记录不等于绝对证明从未读取，早期轮次保留未知。

本轮确实读取 Hallmark，仅用于适用性核查与未来记录政策。**这不是“按 Hallmark 完成项目审计”，也不补算为任何历史轮次使用。**

## 当前技能与读取凭据

- 实际调用：functions.exec → tools.skills__read，参数 package=e0/hallmark；返回 SKILL.md，frontmatter version=2.0.0。本接口未暴露可引用的稳定调用ID，故不编造ID。
- 本地文件：/Users/yiwenchen/.codex/skills/hallmark/SKILL.md。
- 当前 SHA256：25a1ff92d925b2389e8409f42fb8ad7e033fceca8b5d1f07ed4ca4c28da53dc3。
- 当前 git-blob SHA1：d27771723e827baa5e2b34d01492783a42df9174。
- 另外只读 references/redesign.md 的设计audit说明，SHA256：cd3fc1dd10af22bb0374b41340fbab8f2b3be997ea5b63716da3d44ba0bb0552，重点29–42行。
- 历史安装凭据：P01/previous_review/snapshot.json 的 skill_install，记录Nutlope/hallmark、ref407fa689f4a276f2fd389208d271d0fef08f5058、187文件、exact_source_match_verified=true，以及 Hallmark_scripts_executed=false。
- 此次没有重新连接上游或逐文件核验187文件，故历史pin不是当前整棵安装树的全新验证。configs/agent_skills.lock.json未包含Hallmark项；历史记录说明未改项目lock，本轮也未改。

Hallmark主要面向网页/UI生成、重设计和设计audit。其audit分支以现有页面/截图、设计gate、分层问题、file:line及最小修订建议为依据；不修改项目设计。它不提供RTL/形式语义、实验公平性、冻结/数据、资源/费用、科学归因或Python adapter验证方法，不能代替这些专项技术审查。

## 逐轮证据

| 阶段 | 安装 | 该轮实际读取 | 适用部分应用/完整设计流程 | Hallmark脚本 |
|---|---|---|---|---|
| 初次复核（P01之前） | 成功安装的明确记录 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 明确记录未执行 |
| P01 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P02 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P03 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P04 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P05 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P06 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P07 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P08 | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P08a | 可引用此前安装记录；非本轮使用证据 | 未找到该轮读取凭据，未知 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |
| P09 | 可引用此前安装记录；非本轮使用证据 | 最近完成turn未见调用；记录完整性有限 | 未找到具体Hallmark应用/流程证据 | 未找到执行证据；未知 |

每轮精确来源路径、SHA和技术方法见 reviewer-findings.json/historical_rounds。上述“未知”不是“确定未使用”。

初次安装记录能证明安装和当时未跑脚本，不能单独证明读取或应用。原用户请求/提到Hallmark、技能列表中出现、普通独立agent或其他技能都不能算作使用证据。初次技术审查的历史多agent上下文，本轮未重新取其原始agent记录，也不算Hallmark证据。

P03核查了PPTX、Notes、PDF、现成渲染、图表及研究结论；这些可证明演示内容技术复核，不足以证明Hallmark视觉audit。

## 有界线程核对

只列出最近线程以定位既有“复核 test2 项目”，再用read_thread读取当前与紧邻上一轮P09，共两turn，不追cursor、不翻全历史：

- 线程01a1ad99-e41d-70c5-8167-fdba3b17e000，host=durable。
- P09完成turn：01a1aede-87a1-707a-a87d-0cf1b3bb1ea0，返回56条记录；排除userMessage后未见Hallmark提及/调用。
- 当前turn：01a1aef2-e20e-776b-ac65-40ee163a1a6a，当时仅返回userMessage，虽本轮已实际读取技能，说明当前turn反映有缺失/延迟。不能把接口“未见”当绝对证明。
- 协调端另报告P07/P08/P08a/P09可见非user记录未见Hallmark/SKILL.md调用；这是明确归属的协调端观察，不冒称为本轮逐条重取的完整历史。

本轮检查22份选定复核/来源索引文件，P01–P09的20份review.md/json均无Hallmark使用字段或文字；两份更早索引仅snapshot有安装记录。文字命中统计只是索引线索，不等于执行证明。

## 本轮是否使用

- considered=true；read_this_round=true。
- applied_for：判断技能适用边界，制定真实、可追溯的未来使用披露。
- workflow_executed=false；scripts_executed=false。
- 没有网页/UI目标；没有按Hallmark执行项目设计audit。
- 未运行theme/capture/sloplint/build/截图脚本，未调用Together/API、网络、key、安装或项目测试/实验。

## 后续政策与保全

用户“尽量每轮独立复核都用到hallmark”已写入 future-review-policy.md，适用于后续独立复核。每轮记录是否考虑、是否本轮读取、具体源码/hash/凭据或先前读取引用、实际用途、流程与脚本执行、未适用原因及专项方法/限制。复用先前读取时不得标成新读取。

22份历史记录在本轮写入前后SHA不变；只新增本目录 reviewer-findings.md/json 和 future-review-policy.md。不改写P01–P09/P08a、sidecar、source/results、shared HANDOFF/STATUS，也不联系或打断producer。没有重跑任何旧测试、实验或审计。一次早期rg误找不存在的findings.md，随后读取真实findings.json，未补造旧文件。
