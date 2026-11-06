# P15 — R04 E03 实际执行保存证据复核

**整体CHANGES_REQUIRED；证据完整性/执行资源记录PASS_WITH_LIMITS；G1资格BLOCKED / NOT_QUALIFIED。**

本轮确认一个最小分类语义缺陷；没有把native FAILED变成整体PASS，也未发现本批新的非预期RTL缺陷证据。QC01是原登记已知负控制；其物理pair及其余14控制仍未运行，不能排除后续问题。

## 精确封存与已发生执行

开始时只诊断已关闭raw pool；E03 phase/manifest出现后固定并核验：phase **c7b99fd6a11a47a4204b2fb22c0f0ebb57c81bb4ca1c1ba864b57977f2601325**，manifest **9511046040fb38358f1fc70bfe88742a45a5c8957a427744675c929ae1df4325**。571成员/96source绑定/4485保护历史文件一致，current仍匹配；HEAD实际2de33e981d2fffc9739d2ca049fbae1774de1aad，index未改。

最终pool SHA2364e80999aaea35eb3e5da06e31d48331ee6be6b061c09bb3f92738bca8d1b8；EXECUTE fadb3e7fd5534d63309b42c7492a8b57915025010f4832c4ca9c27a0ddcc2e7e；P14/R04源与登记精确相符。pool halted/completed，entry exit1，不可reset/resume。

原79个新job只运行7个：3compile、2native、2physical；5个root exit0、2个native exit1，均进程正常返回而非timeout。其余72 NOT_RUN。原QC00 compile1/native2是E02复用，不计新执行。7份实际receipt/日志/plan/ledger逐一一致，原绝对deadline与单项20/10/2秒帽保持，未见mandatory进程保护错误或ps调用；inventory仍不完整，不提供全子树或OS硬实时证明。

## QC00：首拍修复获得有限实际支持

两sim各8行均与原冻结表及各自VCD逐字段/phase/step一致：首拍a=b=0000,rst1,en0,valid0,active0,ok1；后续四周期/4posedge也一致。pre1000/5000/9000/13000，edge2000/6000/10000/14000，post3000/7000/11000/15000，结束16000ps。没有跳首行/X补0/额外上升沿。

这支持**修复在实际QC00双sim/固定输入路径有效**，加上严格绑定的E02 native前缀，形成一个有限公开控制结果；不证明其他15QC、general correctness、128周期或原74项未复现根因。

## P15-R1 — cover FAILED误分NOT_REACHED，P2/material=true

位置`test2/g1_v4/runner.py:63–67`（SHA46c29b45fd9e4afa9a342bd4ec4c99219f08596cd38826d8f06b24d734a71e1f），后续137–139触发冻结预期冲突。

QC01-cover stdout SHA24b2e9a6b0def95bc74a517f150ab88ded18b7d736ddbc4baea21f9146cb2256明确同时包含：

| 层次 | 保存事实 |
|---|---|
| process exit |1|
| raw tool status |FAILED|
| activation cover |Reached step2|
| assertion |failed step2|
| 旧derived标签 |NOT_REACHED（错误，原件保留）|

固定工具源码yosys-smtbmc（SHA0192f63913bdff347912602315504d5a6ed9e3ff8fbf0dbcdc7c33e5b66681d9）covermode在1950行报告reach，1955–1968检查trace断言并因失败跳出，然后未走到设置PASSED的分支；末尾按FAILED退出1。仅**静态读源码**，没有执行工具。独立解析native BMC/cover VCD均见sampled_cycle1、active1/ok0/q0，与原public QC01负控制一致，两VCD字节也相同，不能当两种独立缺陷。

因此是调用者taxonomy过粗：tool FAILED并不必然表示cover未达。QC01 `common.sv:36`刻意ok=0，formal源16/17行同时assert与cover，原手算期望已经是BMC FAIL且activation可达；本批不支持把它重新描述为未知真实DUT bug。

**最小修订/验收：**另建解析与报告版本，分列raw exit/status、registered cover identity/reached_steps、assertion status/steps、unknown/error。精确旧log必须得FAILED/1 +REACHED2 +assertionFAILED2，不变成overall PASS或NOT_REACHED。完整明确未达与缺日志/截断/错误/timeout要分开，后者保留UNKNOWN/ERROR。新登记明确公开负控制的activation与assertion期望：原source可直接解释其差别，不是仅把旧PASS改成NOT_REACHED迎合结果。旧labels/报告/错误原件保持历史，新增解释版本/表与独立检查；hardware/flags无需为此修改。

## 同上限内的最小继续方案

当前累计setup8/compile6/native4/physical3/cycles12；本次setup0/compile3/native2/physical2/cycles8。actual累计checkpoint11.770645541138947s、charged14.572948167100549s，本窗口6.572940208s；不退款或强行改成相同取样时刻。剩setup0/compile26/native28/physical30/cycles1012。

只改解析/报告时，可在新显式登记中复用：E02 QC00 native+编译；E03两个shared physical build、QC00双sim、QC01编译/SMT及BMC/cover原始证据。覆盖源码/输入/假设/depth8/flags/tool pin及二进制/SMT/日志/receipt/VCD的精确hash与依赖；新report标REUSED_FROM_E02/E03、new_execution=false，所有原费用仍继承。不能复用最初E02坏physical，也不能把QC01-cover的raw FAILED改成PASS。

| 后续新增 | 数量 | 完成后累计 |
|---|---:|---:|
| setup |0|8|
| compile（QC02–15）|14|20|
| native（QC02–15 BMC+cover）|28|32|
| physical（QC01两次+QC02–15双sim）|30|33|
| physical cycles |120|132|

**上述精确复用成立时，不需新增计数quota。** 可在后续continuation用累计保守charge15s覆盖既有charged14.572948...，分配至多1185s（work1180），仍累计1200s；这是待新登记的示例，不是本review的执行授权。数量可行不保证实际结果/OS时间。

如果shared physical binaries不能复用，重建2项则新增compile16/累计22，仍≤32，无需编译帽增加但时间照计。若必须重跑本可复用的native，每丢失1项复用就比剩28多1项，需明确相应native帽修订；丢QC00或QC01一对需+2（累计34），全丢四项需+4。若QC00两个physical不能复用，完整物理需累计35，需帽+2。setup无余量，任何新query须单独分配，不能自动发生。

当前R04固定gate/Allocation祖先及closed pool不能直接续跑；新版本仅为此解析修订和最小明确reuse清单，继承E01/E02/E03所有累计用量与hash，独立预检后协调EXECUTE。不要重跑已完成hardware job来修一个报告标签，不扩大为通用框架或新研究。

## 范围与交付

逐证据/资源/可复用条件见saved-analysis.json、continuation-feasibility.json、review.json及evidence.json。QC01 physical和QC02–15仍NOT_RUN；QC07/15空泛、QC12/13四态限制、QC14运输保持。旧unknown/timeout/score/P04/P05/P06/P05-N1/F1/H1/H2/L1、selected样本、billing和128限制不关闭。

Hallmark本轮实际获取SKILL并读review-finish，同版SHA/read evidence在hallmark-usage.json；实际用于固定材料独立critique、raw/derived分层、实质问题定位与最小继续范围。网页workflow/scripts=false；技术判断来自RTL/native/VCD/资源证据。

有界只读命令、inspect_saved.py和finalize_p15.py exit0；无reviewer harness错误、无旧套件或新mock。0实际compile/sim/native/version/ps/signal/API/key/network/install/commit/push，不改producer/E03/旧证据/shared/index，不发producer消息。G1尚未通过，raw/B-C/跨IP不启动。
