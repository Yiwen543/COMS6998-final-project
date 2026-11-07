# P21：旧证据与预算方法预审检查点

结论：**可以向用户提交有条件的预算提案；尚未验收新设计精确版本，更未授权 EXECUTE。** 新设计目录在本次检查时尚不存在，这是 producer 正在准备的状态，不作为失败。实际 HEAD 为 `034a5a8db63f38878148aaac15ea69dbc150d29a`。仅写本 reviewer 目录。

## 已核事实与复用边界

- 独立解析旧 12 行 target CSV：原版 B/C 均值 74890.6667/73738.3333 token，C −1.53869%；语法变体 70271.6667/66377，C −5.54230%。2/6 只是按 repetition 索引较早达标，模型输出并非随机种子配对。旧模型是 GPT-6 Sol，新拟 GPT-6.1 Sol；不应合并为同模型重复实验。
- 旧共同 seed 两版均 13/41 line，非 round0 已达标；保存 ceiling 为 41/41 line、14/14 branch、344/408 toggle。新实验仍应在调用前记录同一 seed 的 round0：若已达目标，记录零调用达标，不能归为某 arm 收益。
- 旧 runner `scripts/run_queue_bc_pilot.py:383` 的四轮循环没有目标触发停止；`:170–189` 从记录截取首次达标累计成本。旧 target-cost 是保存轨迹的前缀成本，新计划是真实达标即停；描述时分开，不重跑旧实验。
- `scripts/queue_feedback.py:22–23,45` 与 `examples/heldout_queue/verif/tb_queue_pilot.sv:7` 限三 valid items。公开 spec 的 DEPTH/阈值表述不足以独立推出该数值；第四 word 的 64 toggle 未达继续保留。`scripts/queue_reference.py:1` 明示只是 directed calibration。Claude 的两次旧 review 不是 oracle 作者证据（`docs/claude_queue_crosscheck.md:5`、旧 disposition:3,13）。
- 已数出保存的 22 对 Z3 proof 记录；166-cell 结果及 source joins 是已有报告证据，本轮未重新证明。适用范围仍是保存的确切来源、二态 guard/登记转换，不扩为完整 RTL 四态或时序保证。
- **具体复用注意：** 旧 config 七个文件绑定，六个当前匹配；engine 当前 `egraph/src/main.rs` SHA `3912ebe6cbf44b56fd1e6dd050ff5293ad2c3ac03768ef2216020016f5e8145b`，不同于旧登记 `800b1f0f550d0e864ff5c1b7849bfcb07fed74786f56932415b28abfc56c9a93`。独立 `git show 66051b681d3f75e0e68370271a743e637820ac1b:egraph/src/main.rs` 恰得旧 SHA。这是历史/当前版本边界，不证明旧结果错误；新 inventory 不得称当前 engine 与旧登记相同。最小做法：绑定保存的旧 guard/proof 产物及确切历史来源，或显式登记新 engine 后只对受变更影响的部分另行验证；本轮不执行。

## 最小设计条件（待固定草案核对，不预判草案缺陷）

1. 三 arm 共享 RTL/spec/三项合法输入合同/ABI/seed/raw coverage/schema/自身 history/模型参数/轮次与 action 上限。Yosys arm 仅多结构信息；egg arm 在相同结构包上多已验证 guard。普通 arm 的 raw coverage 不能偷偷附带专属结构摘要。首轮就接受 treatment；后续摘要为空要如实保存。信息包更长是实际成本的一部分，这三 arm 识别的是整套信息干预的效果，不能单独证明“纯等价语义”的因果作用；无需为此增加第四 arm。
2. 每个 form 内比较三组各 3 独立 session，无共享生成 history/候选。预定交错顺序避免时间顺序混杂；相同 session 编号不代表 provider 配对。两 forms 是同一 IP，分别报告，尤其不合并 16/40 expression 原始百分比。
3. 相同目标与停止规则，失败/未达/unknown 留在全部 session 分母；不只对成功者均值宣称效率。报告达标率、首次达标轮、累计 tokens/费用上界、sim/cycles/wall 和删失状态。区分共享 setup、每 arm preprocessing、实际 replay seed 成本，明示摊销。未产生有效 stimulus 的 invalid JSON 消耗 normal round，不免费重试。
4. 新 Claude author 只看 published spec + **事先公开采用的**窄合同 + observation ABI，不看 DUT/旧 checker/egg/coverage/候选。不同 fresh Codex property author 只看相同合同/ABI，不看 golden；producer 只做 infrastructure；experimental GPT 只生成 stimulus；我只复核。两位作者都不是目前已经完成。窄合同要明确 reset/clear/enable 优先级、合法边界、同时读写空/非空语义、valid q 的观察时点；almost flags 若未确定就保留观测/unknown，不静默补阈值。
5. 最少新作者工作：一份可供两种语法形式共用的 Claude reference + 一份不同作者的 property artifact，及小范围正/负/unknown 合同控制和独立 review。旧 DUT/spec、driver/ABI、raw coverage/source joins、保存 guard proofs 可有条件复用；旧 checker 不能改名当新独立 golden。无需搬 test2 G1/540 formal 工程。

## 工作量与费用提案

已独立解析旧 48 个 calls 的 usage，只输出汇总：input 944948 / output 11774 / total 956722；cached 357911 与 reasoning 5889 是子集，不重复相加。预算输入 SHA `30fb95c89f8e137d633d0e89a90fc67bda2958a4061259b7f3b8e0bcdcdfa3b5`，官方价格来源由协调端读取并记录，本 reviewer 未联网复查费率。

在该保存价格假设下，独立 Decimal 重算：72 次规划 1,483,083 tokens，按所有 input 的短上下文 30m write 价格加 10% 为 **$4.2241815**；90 次为 **$5.2802365**。Yosys 每相关请求 +1000 input 是规划余量，非保证；新模型/新 reference 可改变 usage。Claude 初次加一次修订 ≤2 calls 的 ≤$1 也是目标。**总预计 $4–7、新增 API 硬帽 $15 均是待批准提案，非已花费或已授权**；维护 Codex 费用/实际 invoice UNKNOWN。

- 正常 18 sessions ×4 rounds ≤72 generation；每 session 至多一次 transport retry，≤18额外，合计 ≤90；Claude ≤2，合计 paid dispatch ≤92。不能继承旧 config 的 `max_retries=2`，否则会扩大上限。
- 若仍每轮最多新增4 cycles，未重试的四轮 session replay 累计上界为 10+14+18+22=64 cycles；18 sessions 为最多72轮 replay /1152 cycles。独立 seed-only、编译、作者 controls/校准、任何失败或 retry 的额外工作另计，具体 caps 待草案列明；这不是本轮执行许可。
- 满上下文逐派发 reserve 重算为 GPT **5,842,584 µUSD**、Claude **5,680,224 µUSD**，仅在保存的 Standard/缓存期限/输出上限/长上下文及区域费率假设完整覆盖、无额外工具/自动重试时成立。两 provider 必须共用一个 $15 commitment 账本；派发前持久预留，未知失败不退，可信 usage 才按覆盖实际类别的保守上界 settle，整数向上。零 count 是零请求，不是免费 count。input 本地估计不是服务端硬帽；预算不足时 NOT_RUN，不能保证92次都完成。
- $15 + 最近 BC usage upper $1.569371 = $16.569371 只是两项口径相加，非全项目账单；不继承旧 $20。无须现在实现新框架或远程 count。离线准备预计2–4小时、review/分析0.5–1小时、live10–30分钟/拟硬停60分钟均是协调端规划，非实测承诺。

## 检查与限制

`check_legacy.py` 最终 exit0（CSV/JSON/七绑定与历史版本）；`check_budget.py` exit0（48 calls usage/两场景/整数 reserve）；`git rev-parse HEAD`、历史 engine `git show` exit0。首次 checker 对“当前七绑定全匹配”的断言 exit1，已保留 `check_legacy_attempt1.py` 和 `attempt1-error.json`，随后改为报告真实 drift，未改任何历史源。早期 `rg/ls` 设计目录不存在 exit1/2，仅表示尚在准备。一次过大只读输出被接口截断，相关必要片段随后小范围重读；不将截断部分当已核验。

Hallmark SKILL 与 review-finish 本轮实际读取，SHA 及用途见 `hallmark-usage.json`：用于固定证据、定位/排序实质问题、最小修订，避免把偏好当缺陷。完整 UI workflow、scripts、Together 均未执行；RTL/统计/费用结论来自独立源读与算术。所有新 API/count/toolchain/sim/formal/install/key/Git mutation 为0。未审新设计固定输入、未验运行器、未证明统计功效、未批准新付费或执行；收到固定草案后仅需一次增量收敛核对。
