# P21 最终设计与预算提案复核

**PASS_WITH_LIMITS — 可以向用户呈现这份具体的新增 $15 API 预算提案；不是 live / EXECUTE 验收。** 本次固定设计内未发现仍需阻塞预算提案的明确实质缺陷。未发现问题不证明运行器、oracle 或实际资源限制正确。

## 精确范围与证据

四份 producer 草案、共同合同、property v2 两份文件共 **7/7** 匹配交接 SHA；预算来源另核匹配。实际 HEAD `034a5a8db63f38878148aaac15ea69dbc150d29a`。检查结束仍匹配同一版本。

精确输入及额外36项当前 source bindings、历史 engine/frontend 两个只读 Git 对象、72个排程槽和12个旧 session 的 line/joint 前缀复算，见 `final-delta-evidence.json`。执行 reviewer 自有 `check_final_design.py` exit0；没有运行 producer 的77项检查，也不以其 PASS 代替独立复核。此前 `legacy-evidence.json` / `budget-evidence.json` 中已核的 usage、定价假设及 reserve 算术复用，没有重跑旧实验。

## 逐项判定

| 项目 | 本轮结论与边界 |
| --- | --- |
| 三 arm 公平信息 | `plan.md:12–20` / `plan.json.arms,common_prompt_policy` 清楚区分共同 RTL/contract/raw counters/自身 history、结构增量和 cached guard 增量。baseline 已有 raw case-selector joins，不冒称完全无 Yosys 信息。结构与 guard 每轮持续存在；超字节帽停止，不截断完整语义。报告整包效应，保留 context 长度混杂，不要求第四 arm。 |
| guard 来源 | `plan.json.appendices` 要求完整 guard、typed atoms、event context、source membership；read/write 分开、无跨 form 信息和 hit transfer。appendix 尚未构建，2KiB 能否容纳全部所需信息仍待核，不预称合格。 |
| 角色与 allowlist | `plan.json.roles`、property v2 role-inputs 将 Claude golden、不同 Codex property、producer、实验 stimulus GPT、reviewer 分离；作者只看同一 spec/contract/未来 ABI，不互读 golden/property 实现、不读 DUT/旧 checker/egg/结果。v2 是实际保存的规则草案，不是可执行 monitor；输入分离有 receipt/协调端报告支持，本轮未重审完整线程访问史。Claude 仍 NOT_CALLED。 |
| P21-C2 输入域冲突 | **文档层修复成立。** 共同 contract 和 v2 P6 同时允许 n=0..3 的 enabled R/W；非空 dequeue+append、空态逻辑仍空且 q 不评分一致。C_eff=3 明示采用假设；排除 clear-disabled、almost 仅观察继续保留。先前专属 simultaneous 分支被禁止的问题已去除；不等于实测 joint target 可达，ABI 和 bounded smoke 仍 pending。 |
| 目标和结果口径 | 新 primary 是 41/41 line AND14/14 branch AND≥344/408 toggle。旧 line-only、retrospective joint、新实际 early-stop 三者明确分开。按保存48行 CSV 独立核12个 session 的首次达标轮、tokens/cycles：原版 joint B/C 74890.6667/73738.3333；变体77982/69693.6667。line 索引比较2较早/4平，joint3较早/3平，均非随机种子配对或预登记新实验结果。 |
| session/停止/unknown | 72槽恰为2 forms×3 arms×3 sessions×4 rounds，无重复/遗漏且 round-major；独立性是设计意图，不由静态排程证明 provider 随机独立。round0、真正首次达标停止、invalid 消耗正常 round、失败/未达/unknown/删失和全部费用保留均明确。两 forms 仍一个 IP，16/40 expression 不混合；无跨 IP/统计显著性/纯语义因果承诺。 |
| P21-C1 旧源漂移 | **复用边界已正确披露，非消除漂移。** 当前 engine/frontend 与旧版不同；两个历史 Git object SHA 精确匹配 inventory。计划仅复用保存的 extraction/guard/proof 与 unchanged DUT，不能据旧22项 proof 验证当前 engine，166-cell 结果亦保留二态/登记转换限制。新 source-to-packet 绑定待实现。 |
| 本地工作量 | 静态算术一致：main≤72 sim roots/1152 replay cycles；另seed≤2/12、private smoke≤2/44，合计≤76/1208；2个 Verilator observer build，≤2 Yosys结构命令，0新egg/Z3/G1。≤9个保存观察 controls /18次独立 checker evaluation 是拟议资格范围，非已通过；不增加第二 simulator 或新通用 framework。 |

## 预算提案可用的准确口径

- **新增 API 预计 $4–7；拟硬帽 $15，尚未批准。** 旧 $20 不继承。GPT正常≤72、每 session至多1 transport retry总≤18，因此生成≤90；Claude初次及最多一次修订≤2，总 paid dispatch≤92。invalid JSON/非法动作不获免费 repair；这些上限不保证预算下完成全部槽位。
- 复用本 P21 已独立核对的算术：72/90场景 generation estimate $4.2241815 / $5.2802365；GPT/Claude派发预留 5,842,584 /5,680,224 µUSD。价格依据是协调端保存并已打开官方来源的 `30fb95…` 文件，本 reviewer 无新增网络定价查询。假设的 model/tier/output/cache期限/费率和无额外服务必须在未来实际调用前绑定；Claude目标≤$1和上述范围均是预测。
- 双 provider 共用单一 commitment ledger；可信 primary usage/model/tier/计费类别才 settle，unknown 保留整笔 reserve；0 remote count 表示零请求。64k为本地准入/actual验收目标，不是服务端硬帽，越目标保存费用后 halt、不合格。实际 invoice、维护 Codex 费用继续 UNKNOWN。
- 60分钟为共享未来在线硬停止，3590秒停止工作留cleanup窗口；offline2–4小时、review0.5–1小时、live10–30分钟只是工作量预测，未实测。本轮没有验收时钟、child cleanup 或真实账本实现。
- 用户尚未批准 $15；**预算批准须先于任何付费 Claude 作者调用**，不能把“准备 golden”视为免审批的前置支出。实际 stimulus 开始还要等独立作者、ABI/controls、packets和薄运行器的既定验收完成。文档通过本身不增加任何权限。

## 实际剩余项与检查限制

仅保留计划已列范围：具体 ABI；新 golden 及 property implementation/小 controls；cached guard/结构 packet 的精确来源与容量；raw counter 与窄合同兼容的小 smoke；新薄 runner 的 early stop/隔离/删失/单账本/deadline；新预算批准。不要把这些 pending 项误作已验收，也无需为此扩大 G1/形式语义工程。已有凭据保留政策不变；本轮无 key 读取/stat/hash/清理。

Hallmark沿用**同一P21已实际读取**的 SKILL/review-finish，源 SHA与读取证据保留在 `hallmark-usage.json`。本次增量没有重新读取；实际使用固定输入批评、准确定位、最小修订原则，并把“已保存草案/未来实现/实际执行”分开。网页/UI workflow、脚本、Together均未执行；技术判断来自 JSON/CSV/SHA/源语义核对。额外读取有两次输出截断，未将截断视为已审；遗漏部分以字段摘要及独立解析检查收敛，未打印完整排程/大历史档案。

本轮新增研究/API/count/编译/仿真/proof/install/凭据访问/Git mutation/producer消息均0。所有旧 checkpoint/addenda、作者草案和 producer 文件保持原样。**范围到此收敛：PASS_WITH_LIMITS 只支持呈现预算提案，不能签发 live EXECUTE。**
