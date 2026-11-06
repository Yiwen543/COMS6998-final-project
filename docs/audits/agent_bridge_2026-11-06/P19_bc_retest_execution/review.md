# P19 — 同IP已知benchmark B/C复测保存证据后审

**PASS_WITH_LIMITS。未发现当前可证实的实质阻塞。** 本次一次性执行、资源与描述性pilot结果可接受；复测已完成，不据未用retry额度继续生成。不是新隐藏集/统计优势/纯语义因果或DUT、oracle、monitor一般正确性证明。

精确E01 phase SHA `60b31b2a07b8dffe8d6be1ecda97fefff1dafa02650716a7e56c1fda71946a3d`，manifest SHA `e518db3d81c0316b14e482b9f8d03aca02e4e228528d8de34d33feee6de470a5`。该manifest以仓库root为路径基准；3284成员全部匹配，R03预先绑定的963源/依赖全部匹配，含旧scores与角色边界。实际HEAD `2de33e981d2fffc9739d2ca049fbae1774de1aad`，index不变。新报告只写P19，未改原始结果或旧P18报告。

## API、费用与时间

六个generation的独立response ID、HTTP200、completed、明确model=gpt-6.1-sol/tier=default、input/output/total及cache/reasoning子集逐项核验。0远程count、0retry；请求重建为固定endpoint所用payload，仅包含已批准messages/schema与model/low/default/30m/output8192等字段，没有tools/conversation/previous_response等附加项。所有实际input<=64000、output<=8192；本地ESTIMATE不冒充provider count。key不在请求JSON/argv/模型messages中，六个API child日志为空；本审查未读secret或做网络探测。服务端/整台主机的全局秘密不存在性不在证明范围。

| arm（各一个session、三轮） | input | output | input+output | reasoning子集 | 保守费用上界USD |
|---|---:|---:|---:|---:|---:|
| B |116529|7134|123663|598|0.758621|
| C |127168|6747|133915|602|0.810750|
| 合计 |243697|13881|257578|1200|1.569371|

cached input均0；reasoning已包括在output，不再相加。C total tokens比B多10252（+8.2902727574%），不声称统计显著或纯Egraph因果。

逐条重放12条RESERVE/SETTLE journal并按每次实际usage整数向上复算，峰值`settled+open/unknown reserves`为 **USD7.207377**，全过程<=USD20。每笔先预留USD5.910168再可信结算，最终commitment/settled_upper=USD1.569371、unresolved=0。**USD35.461008是六笔gross reservation流水，USD33.891637是未消耗预留释放，均不是花费或退款。实际invoice仍UNKNOWN。** 预留/费用上界以既定model/default/30m/noextras合同为前提，不是支付平台发票。

主执行worker summary为177.967504334s，父监督含清理为177.994570459s；在同一3600s窗内，未重置。保存收据有6API child、12compile（6Yosys+6Iverilog）、990monitor replay/204444cycles：其中18开发replay/1380cycles，972评分replay/203064cycles；全部return0，无timeout/mandatory error。没有新DUT/native/formal/G1/crossIP执行。父receipt的child_inventory_complete=false保留；没有由本次短成功运行推出硬实时或完整子树/未触发kill路径保证。

## 提示隔离、冻结与独立日志评分核对

从冻结源码AST读取SYSTEM/PINS/schema并重建header，再用固定public packet+仅本组上一候选与开发feedback重建六次messages，逐条与实际request/prompt/hash相等。两个session ID分离；schedule B1/C1/C2/B2/B3/C3一致，B1即raw首轮。C唯一packet增量仍是egraph_feedback，无reference/hidden/grader/其他会话结果/技能注入。隐含模型预训练知识不由此证明未知；benchmark本来已公开。

六个snapshot、release以及candidate/rawresponse/compiled绑定均匹配；两组final都是最后compiled round3。固定源码调用顺序及保存mtime与“六轮全部freeze/release后才grade”一致。mtime不是独立可信时间戳，但未见与冻结合同冲突。原summary中的actual_API_requests/actual_generation_tokens=null及event顶层通用UNKNOWN_ON_FAILURE派发标记不改写；本审查的6/257578来自内嵌成功provider响应、usage、独立ID、子进程收据与journal，而非将失败未知置0。

**独立Python解析972份gzip MON日志与冻结rows/标签**，重算六slot checks、alarms、unknown、完整采样顺序和末尾marker、输入/日志SHA及case级检测规则；没有导入或执行生产者grader/runtime，也没有再启动monitor。与保存score一致：

- 六轮各18correct-control通过；162总case=18correct+144fault，raw12个fault ID全部保留。
- 六轮都为11类case-union检出：9类ordinary safety（106/106 eligible pairs；其中68 fully resolved），加2类response-completion的末尾marker未归因检出（20/20）。不能把case可归类当成候选slot的类别语义证明。
- input-completion **0/10 eligible N01 pairs**，这10对含oracle unknown且有早报警，不升级为completion成功；每轮38oracleunknown完整保留，candidateunknown=0、marker-only safety=0。
- **N10是mutant ID，不是分母10**：其12个reference记录均PASS、没有eligible故障义务，不能获得故障/128completion信用；raw12仍留，observed union是11。
- B/C三个轮次检测结果相同。可说本次单session/arm、已知固定benchmark复测中未观察到C额外检错收益；不能推出所有IP、未饱和任务或一般LLM验证均无益。

P17有限G1结论只复用，不因本结果关闭128/unbounded/DUT/oracle/generalmonitor/旧74witness、同样本归因、H1/H2/L1/F1/P05-N1、recovery planned等历史范围。旧controller-done-generation-grade-v2、controller-final-v1及live-final-v1 scores均仍匹配预登记source清单；没有改旧分数。

## 复核范围与保全

Hallmark主SKILL沿用同版先前实际读取，本轮重读review-finish；用于固定证据、事实/推论分离、只列实质风险及有界收敛，不运行UI/Together脚本。技术依据为JSON/AST/整数/journal/gzip独立解析。初始元数据查看误把目录交给文件SHA函数，IsADirectoryError/exit1已记；修正读取phase.json后成功，不是生产者故障或实验重试。

实际命令、输入/输出哈希与逐轮/逐请求结果见review.json、evidence.json、independent-analysis.json及journal-recalculation.json。本轮0API/网络/secret/compile/replay/native/G1/安装/Git改动/producer消息。接受仅为本次保存证据和有限描述性结果；不签发任何新的执行、轮次或预算。
