# P18 方法补充：父级澄清后允许最小 R02 准备

**METHOD_FEASIBLE_FOR_MINIMAL_R02；不是LIVE_ACCEPTED或EXECUTE。** 父级本次明确纠正：64000是我方先前方案的技术参数，不是用户提出的不可变硬帽。因此，上次对“宣称派发前64k硬保证”的拒绝保留为历史；现在可把64k登记为本地准入目标、返回真实usage的合格性验收条件，**不再等待64k放宽批准或已作废的async选择**。用户明确的USD20、60min、8192输出、max12generation、同IP/B/C范围不变。

该结论依据本轮父级澄清，不伪造新的用户批准。R01原注册、countfee阻塞准备及上次检查点不改写；R02新增一个技术规则/来源记录，绑定原用户授权和这条澄清，并事前公开说明零count、本地ESTIMATE及超目标处理。

## 财务方法与适用性

在官方服务遵守gpt-6.1-sol low、Standard/default、implicit30m、max_output8192（包括不可见/reasoning）、无附加收费工具/SDK自动重试的请求合同下，以完整1,050,000 context作为输入保守界（不因其还须容纳输出而扣减）：

`R = ceil_microUSD((1050000×5 + 8192×15)×1.1) = 5,910,168 microUSD`。

这里5/15是长context下30m写入/输出的最高适用USD/M费率，region10%全额计入。30m写费替代普通input费，不相加；cached/reasoning是子集不重复。context是模型整体容量，不是64000服务端输入拒绝参数。该reserve是费用上界，不是合格性判断或invoice。[既有官方模型依据](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、[缓存依据](https://developers.openai.com/api/docs/guides/prompt-caching)沿用上一轮已成功查阅资料，本轮未重复联网。

最低充分实现是一个串行、持久累计账本：

1. 每次可能收费的dispatch前，先核`settled_upper + unknown_full_reserves + open_reserves + R <=20,000,000 microUSD`以及generation/retry/剩余wall帽，再把本次计数和reservation持久化；失败则无派发、保留NOT_RUN，不读取key来探测。并发/崩溃/父子进程不能重复使用同一余量；无需通用框架，但实际单调度路径必须成立。
2. timeout、派发不确定、缺/错usage、model/tier或cache合同不可信时，不释放该笔R，保留原始证据并按本轮规则halt；没有下一条请求来试探。0远程count是未调用，不是把countprice写0。
3. 仅对完整可信且合格的响应，可用`U = ceil((55×input_tokens +165×output_tokens)/10)`微美元结算，即全部input按最高$5/M、output按$15/M，再乘1.1。不依赖缓存优惠也安全；缓存字段未知仍原样UNKNOWN，不能因此声称usage完整。先记录R，再记录U及R-U未消耗预留，不能重复settle或称旧花费退款。
4. 所有API仅generation，max12含失败/重试，SDK retries=0。请求明确default/30m、无hostedtools/隐式付费调用、无server conversation等未登记隐式输入；同一60min绝对deadline覆盖API、compile/replay、parse、cleanup。预算拒绝不创建新池/新60min或重置任何已消费量。

证明只需预算不变量：可信成功费用`C<=U`，每笔失败/未知在指定服务合同下`C<=R`；在派发前确保上述总和不超过20M，结算只用可信U替换该笔R，就保持API费用总上界。该上界不声称对不同model/tier、12h、额外工具、未计重试或服务违反已固定合同仍自动有效；发现这些情况必须停止、不得改为低价结算。正式预检须检查请求allowlist与费率绑定，不是只相信配置摘要。

最坏未知三笔保留USD17.730504，第四笔前拒绝。按最简单的始终最高费率，64000/8192完整成功一笔U=USD0.487168，12笔U合计USD5.846016；若每笔都可信及时结算，足以做正常计划。12只是最大帽，不承诺失败时一定做满。实际invoice仍UNKNOWN。

## 64k目标及研究合同

派发前本地估计大于64000就拒绝；符合本地目标才进入财务/时间/密钥/派发gate。将估计器版本、payload哈希和估计值标ESTIMATE，历史provider count不重标fresh。返回实际input>64000、output>8192、缺usage/身份不符/cache意外：记录并halt，不作为合格候选/轮次/主结果，不让后续C继续修到合格；原响应、费用、失败/未运行分母保留。实际input超目标时，最简单是保留整笔R、不做精细释放。

本地ESTIMATE现在仅影响准入目标/验收规则，不承担USD20证明；因此没有确定token上界不再阻塞**新方法准备**，也不能声称它提供了真实服务端64000硬限。B/C共用估计/超目标政策、相同公开common/raw包与C-only Egraph增量、ownhistory、六个snapshot全部冻结后score/两final选择、旧unknown分母与P17 G1复用都不变。不缩包/截断来迎合C结果，不把已公开benchmark复测称新隐藏集或新科学证明。

## 最小后续范围与当前停点

**可由producer准备独立R02**：移除远程count调用，加入上述动态reserve/settlement、ESTIMATE与usage超目标停止，保留原score/release与必要deadline保护；少量纯离线检查只覆盖新分支。无需新增G1或tokenizer资格工程、无需再问64k批准。本报告不审核当前未封存代码，R01仍countfee-blocked，不能拿本方法结论签发R01 live。

R02最终仍须精确seal、独立P18、价格/请求/账本/60min停止的必要源级核验与root精确EXECUTE，才可按原用户授权进入live。凭据走已约定安全路径，不重复索钥匙、不读secret；本轮未复查credential metadata。若封存实现不能确保inclusiveUSD20或其他用户硬限，beforeSDK/key/API停止并给具体原因；不能以收敛为由弱化。

Hallmark引用上一轮同版实际SKILL/review-finish读取记录及上次已核对SHA，**本轮未新读**；用于分离历史拒绝/新规则、方法可行/代码接受、实质风险/最小修改，无UI流程/脚本。算术及持久化核验记录见本补充JSON；不运行producer代码、API、count、key、compile/sim/native或Git写入，不给producer发消息。
