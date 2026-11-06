# P10B — R02 执行前增量复核

**PASS_WITH_LIMITS。精确 R02 的 P10-R1/R2 已通过独立增量验收，未发现新的已证实实质风险。** 原 P10/R01 的 CHANGES_REQUIRED 和两个历史 finding 保留，不回写为通过。

本结论只接受执行前基础设施修复。协调端可在原单一用户grant内路由一次精确R02 EXECUTE；本轮没有启动G1、创建资源池或授予新额度，也没有宣称G1资格成功。

## 精确身份与实际差异

| 输入 | SHA256 |
|---|---|
| P10B packet | 9ea1b3a72f54c30fe6b50de4c3eb07b0691f042f6f3a21fa0d29a734c91c774c |
| R02 phase | ae927e87cf7ee8b22ea76c1e29914ebfc27b5691f53e2838b7af73e40a05d7c7 |
| R02 manifest | 7c16e5020ab6212fbd66bdd57ecb272bef56e1bfc6ce4362a661960d331fb201 |
| registration v2 | 85185519c5a6e2a8eaaf843b5b27c9cc312ada2fc8c44af6f915368759d98268 |
| source-manifest v2 | fe972d2863b857ef0deb956df468ad3866301b7349d01d7f08275b6c1e54ffea |
| 原用户grant | bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab |

实际HEAD为c25180848ebfe9a1f49da0aa5f579cac913e6428。138份封存成员、43条source-manifest绑定及清单实际列出的398份旧文件均匹配，当前副本无漂移；不以摘要中其他保护计数替代实际清单。完整身份见input-manifest.json。

先枚举差异，再执行回归：
- budget/runtime新增原始绝对deadline、持久化后与最终Popen前检查、charged-not-dispatched证据。
- observations新增recorded span、state_at/horizon和selected-native时间边界。
- runner改为v2/R02 gate，并显式使用原canonical pool路径；没有按v2另开预算。
- schema/README/registration/source-manifest及新回归为相应元数据变化；job-plan仅路径变化。
- 24份文件逐字节一致：18SV、3输入/标签JSON、support matrix、contracts.py及归档mock_tests.py。tools/caps/profile/grant/depth/原pool完全相同；归一化路径后job顺序与flags一致。因此复用P10的控制数学分析，不重跑旧suite或科学工作。
- shared HANDOFF/STATUS相对R02保存的before版本仅在首行后插入元数据，旧body保留。

## P10-R1：仅在R02中关闭

位置：test2/g1_v2/budget.py:49、:65、:79–112；runtime.py:25、:30–32。budget SHA 77279960bcfd4ed676c636109be197ad8437535848151b0ded1673757b72b385；runtime SHA 61689aad92c17045267fcfc0871cc4eae63c1d8aaeb2044bc44834734a9876f8。

独立探针确认：
- 原P10的1194+7s save反例、mkdir、stdout/stderr open、最接近Popen的最终检查跨界，均0次mock Popen。
- reservation仍计入1次compile，状态NOT_RUN/CHARGED_NOT_DISPATCHED，全局halt、原clock origin和deadline保持；后续派发与同路径新建pool被拒绝。
- 已过期1196s不预留、不派发；清理窗口不足同样拒绝，未向子进程传入负timeout。
- normal只调用一次mock Popen并RETURNED。
- 保存耗时4s后的ordinary timeout仍用原绝对120s deadline，不重置为124s；cleanup unresolved保留并halt。

这证明fake-clock/隔离对象下的逻辑路径，不能升级成实际OS实时调度或全体后代进程清理保证。真实工具调用、sleep、signal均为0。

## P10-R2：仅在R02中关闭

位置：test2/g1_v2/observations.py:91、:97–98、:120、:144。SHA 269a1692eaed9397f0495e6a7b760f2045bdb691967518a72acbb106416ccc47。

直接深拷贝原P10序列化字节，而非重建替代样例：
- 完整16ns原VCD SHA 235ef77a66cff18146ac261bde9a3abedc1fdaa253d609c984f92270c0226c0e：ACCEPT。
- 截断14ns原VCD SHA 25a20fc0821203d747744f9c6dad3b762bb299c1be13baa19a926b13ece8b0da：因VCD_TIME_COVERAGE_MISSING required15000拒绝，非偶然其他错误。
- 原rows SHA 5181cc4468d4334265fef0144202180b6df1fdb6aa4839e4b924bd8127e84fa0保持。
- 缺head、EOF后query、unknown q、缺signal、phase shift分别按预期原因拒绝；没有补造延续或时间步。
- 新鲜suite还覆盖selected-native候选越过记录跨度时拒绝。

## 证据计数

| 类别 | 结果 |
|---|---|
| producer保存的新R02回归 | 14项；逐项核对保存fixture绑定、执行源码SHA和关键result |
| reviewer新鲜R02回归 | 14/14通过，0错误/失败；约0.02765s |
| 独立clock/VCD探针 | 17/17符合预期，输入最终字节和SHA在验证前保存 |
| 独立metadata gate探针 | 9/9符合预期，未调用runner.main或Budget执行入口 |
| 实际compiler/native/simulator/version/API等 | 0；原资源池仍不存在 |

生产者14个保存结果的状态、理由、Popen数和虚拟时钟与新鲜对应结果一致。原12项mock源码由编辑历史重建的provenance限制保留，没有升级成同时归档或重跑证明。

执行命令均带PYTHONDONTWRITEBYTECODE=1：
- python3 .../P10B_g1_fix/exec_tree/test2/g1_v2/regression_tests.py --record .../P10B_g1_fix/fresh-regressions，exit0。
- python3 .../P10B_g1_fix/independent_probes.py，exit0。
- python3 .../P10B_g1_fix/gate_probes.py，exit0。

diff的exit1仅表示有差异，不是测试失败。完整真实命令、逐例输入/输出/源码SHA见review.json和evidence-manifest.json。重现应使用P10B下新的空review-owned副本布局，不覆盖已有记录。

## 精确gate与下一执行范围

runner.py:19、:47–52绑定registration v2和R02 preparation manifest；:70–71仍使用：
test2/results/g1-qualification-v1/execution-state.json。

9个metadata探针中，精确R02绑定通过；原P10 CHANGES_REQUIRED、旧R01 manifest、旧v1 registration、即便标PASS但仍引用旧identity的review、源码/grant/review哈希漂移、仅有旧receipt key均拒绝。

这些是review-owned复制ROOT上的合成metadata fixture，不是真实项目的执行receipt或实际审批。没有向producer发消息。

协调端若路由EXECUTE，必须使用：
- record_kind=G1_EXECUTE_AFTER_READONLY_P10，stage=EXECUTE；
- 本表精确registration/source-manifest/user-grant SHA；
- **preparation_manifest_sha256**绑定R02，不能用旧r01_manifest_sha256字段；
- p10_review_path指向本轮实际review.json，p10_review_sha256为其最终真实SHA。

输出namespace为test2/results/g1-qualification-v2，预算仍是原共享pool。计划18逻辑compile根、32native（16BMC+16cover）、32双sim runs/128周期；上限仍32/32/32/1024周期/1200s。只有一个profile，无退款/自动重试/刷新pool，post-review新增job额度为0。

## Hallmark与剩余限制

Hallmark considered=true，**read_this_round=false**：准确引用原P10 review.json的实际读取凭据（该文件SHA cca7589786545675331ba1daa163d4e5cc757795aa8ac57972404e7463ee73e1），本轮重验当前SKILL.md SHA 25a1ff92d925b2389e8409f42fb8ad7e033fceca8b5d1f07ed4ca4c28da53dc3及review-finish SHA 9d00de59e71ee2516212140b0512d6d2e90a120d4a328eeba9cb12396ff38d64，均同版，不冒称本轮新读。

实际使用固定输入独立critique来组织actual-diffs与原反例复验；准确定位/排序和最小修订原则用于R1/R2闭环；没有因个人偏好或没有新理由重开已固定的QC数学。workflow_executed=false、scripts_executed=false；没有网页/UI或Together/API。专项结论来自代码/时钟/VCD/gate技术证据，非Hallmark权威。

- 本轮不是G1实际资格成功。SV syntax/frontend/ABI/native/physical输出、真实OS清理尚未执行验证。
- P10-N1逻辑批次计数及非穷尽PID观察仍明确保留；不是18个OS compiler进程的断言。
- QC07/QC15空泛、QC12/QC13四态不支持、QC14运输专用、depth8不证明128/unbounded及所有科学未决不变。
- 原P04 mismatch/causeUNKNOWN、P05/P06限定范围、P05-N1、F1/H1/H2/L1、selected-sample/general correctness、billing UNKNOWN/recovery planned保持。
- 398清单hash不是全部旧4837/7450成员的新审计。整体只读复核耗时未从入口计时，仍null/notzero；与尚未启动的1200s执行钟分开。
- 不授权G2/oracle/API/data/candidate/paid/key/install或旧cohort工作。只有协调端按原grant执行一次精确已接受版本；本复核不autoexecute。

证据索引SHA256：d44422e5349041318054eb0e597431844f14ec5e99e0c866cc3a9310e20af8a6。
