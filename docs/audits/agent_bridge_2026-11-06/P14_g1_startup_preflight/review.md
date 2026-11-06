# P14 — R04 首拍修复执行前独立复核

**PASS_WITH_LIMITS，无已证实执行阻塞。** 可由协调端随后交付精确R04 EXECUTE，在已批准累计caps内尝试唯一实际R04。**不是G1通过，首拍SV修复仍未实测。**

## 精确输入

phase SHA8189a3e504e59b9baa3d5ef7d2f1d7e0b625be83fb0cbcc0eb4e3608b0ff7fa8；manifest SHAa61cd8744e44eb599abe331079766215a4860d64b07a3080090f8f29e9e97b0a；registration29dcc2a0781927ac1cc624850c9fdda44625fe468544eae881f4ea86e92cfa31；source57e79f812133ec94f340009c18227b8bf773515ea571d0b172c9c59e9abd9705。

512封存binding、来源绑定及4485保护文件当前匹配，原件未改；实际HEAD2de33e981d2fffc9739d2ca049fbae1774de1aad，当前stage0。原10000-stage基线属于发布前历史；使用resumption-baseline/phase的9f597996...索引条目指纹，未回退旧HEAD或改Git。真实v4 pool/lock始终未创建。

## 核心判定

- **时序合理，但效果未实测。** physical_tb.sv:4、18–23（SHA7be66871399b32b36ce91df607e3f5d1f3c653b27cf154b43b7f377f5c49c6ca）：初始step7，正1ps后step0产生实际变化，避开time-zero敏感列表尚未等待的情形；第一轮999ps补偿。独立有理数推导pre1000/5000/9000/13000、posedge2000/6000/10000/14000、post3000/7000/11000/15000、finish16000ps。没有新增posedge、跳首拍、X补0或改标签；QC14 marker仍仅最后post。需实际双sim首拍/全部行/VCD才确认修复。
- **native复用闭合。** native_reuse.py:11–37及native-reuse.json SHA1878bd0ea59e00c67d91f2125cd72031c902283931616de52f0ecdb9a6ccc84b绑定旧E02 source/SMT/argv/tool pins/日志/receipt/report/终止pool。17份native/common SV、23材料及parser不变。QC00编译1+native2明确REUSED_FROM_E02且旧成本已继承，绝不复用旧不合格physical；新32physical仍全运行。原有深度8/有限scope不扩大。
- **实际physical33批准与累计预算。** allocation.py:54–99先核真实approval/amendment/decision、E01/E02已终止池；批准只增physical32→33。新0setup/17compile/30native/32physical128cycles，累计8/20/32/33/132，不是新32/32/33池。保留先前actual5.197697583120316s及charged7.151973249856383s，charge8是保守分配；current1192/work1187，累计1200不重置。完整纯记账探针得到准确累计数，下一physical请求拒绝并halt，之后继续请求也拒绝。
- **真实入口ABI与独占。** runner.py:33–53、70–76和新gate要求P14/精确manifest/reg/source/decision/amendment/旧E02池；独立复制入口使用真实保存批准/复用字节和明确fake P14 receipt，能进入Budget并完成一次fake reservation，随后主动halt；重复copied lock拒绝，ledger不变。硬件执行和host binary digest检查均stub，不能叫实际工具入口验证。
- **必要保护保留。** runtime.py及observations.py与R03相同；Budget逻辑只改attempt_id，绝对deadline、慢持久化/临派发检查、最后save越界halt、PGID/poll/wait/kill及未知保留逻辑未退回。E02真实收据的有限结果可复用为背景，不重跑旧套件。无ps、新权限或setup查询。

## 证据与审查者脚手架错误

生产者最终17项保存检查与封存源绑定；独立干净副本新鲜17/17 PASS，旧16项历史保留。另有6个独立检查（完整plan累计/三种坏继承拒绝/正向入口/重复启动拒绝）。源码及fixture/result SHA在evidence.json。

审查自身两类错误透明保留：第一次错用发布前index基线导致exit1；修正后共享review-copy已有fake pool使17suite中2fail，另漏复制旧observations.py导致1error。它们不是产品失败。第一次源码和日志/summary全部保留；新isolated-suite-copy包含字节相同observer且无fake pool，独立17项exit0，未改producer测试/原件。这两次不能描述成首次即全通过。

Hallmark本轮实际新读SKILL.md及review-finish：用于固定材料独立critique、实质问题定位/最小范围和不稀释失败/未知原则，具体应用为以上三类验收；来源SHA及read evidence在hallmark-usage.json。网页workflow/scripts=false，RTL时序/预算/复用判断由源码和纯离线证据完成。

## 后续边界

本review的phase=P14...、status=PASS_WITH_LIMITS及全部input_identity可供新门禁绑定；协调端还须另发精确EXECUTE。物理预算现在恰够全计划，若再失败，不自动增加或退还已花成本。真实执行后再审原始首行/双sim/状态/费用，届时才能判断公开G1有限资格；不借预检声称general correctness/128cycle/原74原因已解决。QC07/15空泛、QC12/13四态不支持、QC14仅运输与所有历史未决保持。

本轮0真实工具/仿真/API/key/network/install，不占真实pool/lock，不改producer/shared/index、不发消息/commit/push，不审P2/I2C或启动raw/B-C新研究。到此停止。
