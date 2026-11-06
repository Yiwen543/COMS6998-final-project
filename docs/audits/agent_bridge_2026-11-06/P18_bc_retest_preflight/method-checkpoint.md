# P18 方法检查点：零 count 与最小用户决定

状态：**METHOD_ONLY / LIVE_BLOCKED**。本轮仅持久化上一轮结论及新增授权边界，不重查官方资料、重做算术、审未封存代码或执行实验。不是正式P18接受，也不是EXECUTE。

## 保留的方法结论

在请求固定gpt-6.1-sol、Standard/default、implicit30m、output8192（含reasoning）、region10%保守计价、无附加收费工具且SDK retries=0的合同条件下，完整模型context保守reserve **USD5.910168/可能收费dispatch** 成立。模型context为1,050,000，是整体context容量，不是可自定的64000输入拒绝帽。财务预留覆盖大输入的可能收费，不使大输入自动符合研究合同。

0 remote count是**没有调用收费未知的endpoint**，不等于count免费。逐dispatch先持久化整数微美元预留；全部失败/timeout/未知usage保留全额，不当0或退款。只有身份、tier和usage可信时才能以保守cost_upper替换临时reservation，完整保存替换journal；actual invoice仍UNKNOWN。预算与max12generation、retry帽、60min共享截止时间均不刷新。上轮已算得3笔未知USD17.730504，第四笔USD23.640672，故第四笔前拒绝；这些是上轮算术证据，本轮未重算。

现有“本地tokenizer＋margin＋返回usage后检查”**未证明派发前input<=64000**。max_output_tokens只限输出；truncation=disabled是模型context检查；上轮查询的官方Responses接口及本地SDK未见适用64000的服务端输入硬限。没有新证据改变这一结论。当前仍须beforeSDK/key/dispatch停止，不用真实请求探测。

## 最小需要用户明确决定的条件

**可以作为有条件的后续实现范围，但须用户明确批准新登记，不能由本审查代批。** 用户需要明确同意以下物质变更：

> 为一个新版本，将64000从“派发前必须保证的真实输入token硬限”，改为“本地估算准入目标，并用返回的真实usage作合格性验收”。允许估算误差导致某次实际输入超过64000；这类响应不能作为合格候选/结果，保留原响应与费用并按预登记规则halt，后续未做项记NOT_RUN。服务实际context容量沿用指定模型，财务用完整context预留控制风险。0远程count、USD20含全部费用、output8192、max12generation、每轮retry帽、同一60min及原同IP实验范围保持不变。

这里“允许误差导致超限派发”必须明说；仅同意估算、重新开始流程或实际usage超限后丢弃，都不能默认为已放宽原硬帽。若用户仍要求每次派发的真实input必须<=64000，这条简化不成立。

同意后仍只是允许准备这个**新版本**：须保存R01及所有失败/未知；明确估算方法、payload哈希及ESTIMATE标签；B/C使用相同准入/超限规则，不凭C结果选margin，不偷偷删system/schema/材料或自动截断；actual input>64000、output>8192、身份/usage不可信不得继续资格信用。不能因为用户批准输入规则就跳过sealed P18、精确EXECUTE、实际动态预算控制与安全credential gate。密钥不经聊天、日志或模型上下文；本轮未读secret，未重新检查其存在性。

更少改动、真正保留原64k硬限的路线：**沿用R01 provider count，仅补足count单价/可证费用上界**，将count/generation/retry全部纳入USD20并保留派发前精确input检查。现阶段该费用证据仍缺，不能先发一次count探测。另一理论路线是已存在且可核验的完整请求token上界或适用server输入拒绝参数；目前没有这两种新证据，不为此再建通用tokenizer证明框架。

## 当前边界与中断保全

上轮写入工具在环境不可用时未返回成功，随后执行cell7被终止，未声称落盘成功。稳定重连后的本轮有界检查发现P18目录不存在（ls exit1）；因此创建本检查点作为首次**已核验**落盘，不补造上轮文件/执行记录。

协调端报告真实runroot/EXECUTE不存在、actualAPI0；22个ledger为prep/mock/replay或显式SYNTHETIC_ROOT，mode=live字符串不是实际调用证明。本轮引用该报告，不重新扫描ledger或读取key。尚无sealed R01 identity，不评价漂移实现；等待协调端单独交接。

Hallmark引用上一轮本会话对SKILL.md与review-finish的实际tools.skills__read记录；**本轮未重新语义读取**。适用处为区分事实/推论、只保留实质阻塞和最小修订；无UI流程/脚本/Together。官方依据沿用上一轮成功读取的[模型页](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、[计数指南](https://developers.openai.com/api/docs/guides/token-counting)、[缓存指南](https://developers.openai.com/api/docs/guides/prompt-caching)、[Responses参考](https://developers.openai.com/api/reference/ruby/resources/responses/methods/create)，本轮未重新联网或改变原费率证据。
