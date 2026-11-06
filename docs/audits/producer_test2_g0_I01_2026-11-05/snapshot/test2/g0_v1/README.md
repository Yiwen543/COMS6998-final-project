# G0 v1 — offline synthetic metadata adapter

本版本依据新 I01 有界维护授权实现及自测，**待独立复核**。它不改变 D01/E05/draft 的历史 false 权限，也不继承旧 USD20。只使用已有 Python 标准库；没有安装依赖、网络、provider client、实际 dispatch、native/DUT/formal/monitor 工具或 checker 执行。

`schema.json` 是本版本自有的有限 closed-shapes 格式，**不是通用 JSON Schema 标准实现**。验证器只接受 `origin=SYNTHETIC_FIXTURE`、显式身份、strict serial、JSON/text artifact 和 offline grant description；不接受历史账本或真实科学 bundle。模型名、tier、reserve 单位和 token 数都是合成记录中的声明，不是模型选择、价格或实际消费证明。

## 实现和明确限制

- `adapter.py` 校验新格式版本、严格类型／nullability、duplicate JSON keys、身份／context、prompt 原字节与规范化摘要、源／配置／工具／pin 描述的 SHA、parent count、串行请求／terminal／call、资源帽及持久全局 halt。
- 全 run 的 halt 不因 retry/round/session 清除。迟到的已派发请求 terminal 可保留真实声明值／未知成本，完整性保留 UNRESOLVED；不会重启 dispatch 或接受候选。合法 NOT_RUN 不填用量，missing usage 和 subset 均不补零。
- 输入 manifest/release 的文件 inventory、哈希、来源和输出拒绝覆盖边界被检查；路径穿越和 symlink 拒绝。输入按稳定本地只读快照使用，不宣称抵抗任意并发文件系统竞态，也不认证 grant/provider 或独立历史执行真实性。
- 观测只检查**合成声明**的 source、phase/reset、slot、width 和参考前缀边界。reference descriptor 是 text stub，不是独立 checker；raw metadata 是 text sentinel，不是 VCD、波形、真实 rows 或 MON。
- **没有原始科学 parser、独立标签、oracle、G1 或完成性验证。** 科学维度固定 NOT_EVALUATED；正确性／selected-alarm／128 completion 的升级声明拒绝。声明 unknown 可以完整性范围内一致，但不算物理报警。
- candidate 输入只做显式 artifact allowlist/visibility/身份约束；不证明 opaque prompt 内容没有隐藏信息，也没有实现真实 own-history renderer。真实 fault/pair/RTL coverage 分母不在本版本内。

精确支持／未支持项见 `support-matrix.json`；D01 44 项映射见 `coverage.md` 和 `test2/results/g0-adapter-i01-v1/coverage-map.json`。范围外项不会被说成已实现或科学通过；P05/P06 的旧限定接受不会认证本版本。P05-N1 旧 helper/backlog 未修改；P04 原件不变，本次使用新的规范绑定 canonical fixture。

P08 已对 D01 纸面设计返回 PASS_WITH_LIMITS；I01 代码仍待 P09 独立复核。P08-N1 的 error／缺 terminal 分支已在现有代码中分开处理，缺 terminal 不解除串行屏障；专门的跨 attempt 缺 terminal／匹配 error 后 retry 组合测试尚无保存证据。详见覆盖映射，不把静态追踪当作新运行通过。

## 新测试与运行证据

最终轻量套件为 `test2/tests/test_g0_adapter_v1.py`，记录在 `test2/results/g0-adapter-i01-v1/attempt6/`：93 项通过，约 0.825 秒。此前 attempt1 的 60 项／8 失败、空引用处理错误、一次被 seal 修复的扰动及后续修订／所有 fixtures/results 都保留，源码版本在 I01 drafts 中。

每个 case 都有独立的 JSON/text bundle、深拷贝的 fixture-binding（含输入 SHA／symlink 描述）、result 和预期状态；验证前后校验输入未被修改。全 run 不读取旧实验来构造 fixture，不生成 SV/harness/波形/真实 rows，不产生新科学样本。临时 output 边界测试与新 CLI 拒绝覆盖记录均有本次新证据；不声称重跑任何历史测试。

CLI 的 `--bundle` 仅离线读取，`--out` 仅在新的 g0 namespace 独占写报告，无法产生实际 provider/tool 调用。完整性 PASS_WITH_SCOPE、UNRESOLVED、REJECT 分别返回退出码 0、2、1。报告不是科学 release 或 execution grant；provider invoice/count fee 持续 UNKNOWN/null。

已执行命令与退出码见 I01 phase 和 `test2/results/g0-adapter-i01-v1/cli-records.json`。复现必须使用新的、尚不存在的 record/output 目录，不能重用已封存 attempt 或覆盖报告。这里只描述入口；除本轮新 G0 轻量维护许可外不提供 G1/服务/新科学执行权。
