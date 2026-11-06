# P18 — 精确 R02 零远程 count 执行前复核

**CHANGES_REQUIRED：暂不签发EXECUTE。** 方法与已审基础路径可以复用；发现一处最小合同修订，未要求新增资格框架、改输入目标或重跑旧测试。

## P18-R1 — 未知返回tier被当作可信成功并释放预留

**Medium，material=true，阻塞本版本live接受。** 精确位置：`test2/retest_v2/resources.py:34`，`trusted_success`允许`returned_service_tier in [None,'default']`；`api.py`的provider normalization在字段缺失时同样得到None，随后`pipeline.APIClient.generate`会接受响应并调用settle。

独立深拷贝并预先保存的反例：`R02-preseal-changed-evidence/missing_tier.input.json`。它仅将正常合成响应的returned_service_tier改为null，其他identity/usage有效（64000/8192）。实际结果为ACCEPT，settled_upper=487168微美元，commitment从5910168降为487168，释放5423000；未halt。这个审查副本的resources.py SHA `4b0ab6f57877205e669633eeeab9e2aebf47bd47ae74530a91ca294b4a6f9200`与最终R02封存逐字节匹配，反例不是漂移目标。

预期：按本阶段“full model/tier/usage validation后才可信结算，unknown保留整笔并halt”的约定，缺失/空tier必须拒绝候选合格性，不结算或释放原R。影响是把未核实的服务类型当作已核实default，违反已登记的unknown处理/服务可比性与结算条件。**本例没有真实请求或已发生超支证据，不能宣称已突破USD20**；最高费率结算本身也不是问题，问题是未满足结算前提。

最小修订：在新封存修订中要求明确返回`default`，None/缺失不得推断为default；保留原R02，不就地改封存。只需补缺失/None tier的轻量负例（halt、不编译/不继续C、原始响应保留、R不释放），保留正常default结算487168与显式非default拒绝的正负对照。重新绑定最终source/reg/prep和review/EXECUTE，不需要再询问64k批准、扩大预算或重跑19项基础/G1/全部18项。

## 已核对范围

精确R02 phase SHA `b55ecedd8950fb6ae208df379f5e3605942c9407af410be92e637444e0ec37b1`，manifest SHA `9e5fba11c236434ff67397f9ec577fc1313f36133620d7846b8cc0a3753bdd04`；203封存成员、943来源/依赖全部匹配。完整7项caller identity见review.json。R01基础checkpoint复用，未重跑其6组探针/19integration或G1。

- 64k规则已由父级澄清及用户实际zero-count confirmation明确为ESTIMATE准入目标/actualusage合格上限，不再阻塞为“缺服务端64k硬限”。两个初始完整payload估算46876/52466，含system/schema，标注非exact、非服务端硬帽；费用证明独立于估算，无远程count preflight。
- reserve5910168微美元在网络/密钥读取前持久化；APIchild重验ledger/lease/payload/独占claim。整数向上settlement、累计commitment、失败整笔保留、actual>64000/output>8192拒绝路径可见。新独立小probe验证有效baseline与unknown input、超目标、bool input、超output、12h及flex拒绝；上述None tier是唯一已证实反例。没有运行真实API或账单，动态USD20上界仍以指定服务/费率合同为前提。
- HTTP为stdlib HTTPS固定host/path、CA/hostname/CERT_REQUIRED、单POST/no retry/no redirect，无SDK安装；假connection的302只记录一次POST并关闭，不读取错误body、不发网络。key只在实际门禁后读取并进入Authorization header，不进argv/日志；本轮未读取key。
- providerJSON已解析成功但normalization失败时保存原始字典，unknown费用不归零；18项旧targeted与新增1项provider delta分开保存，最终api.py有delta，不冒称同一次最终19项全跑，本轮未重跑它们。
- release.py与supervision.py相对已审R01逐字节相同。两session ownhistory、六snapshot释放后统一旧grader、162case/38unknown、最后有效轮次、旧分母与取消NOT_RUN继续沿用。R02 pipeline改为本地准入而非count，未引入hidden评分反馈；P17只复用有限G1结论。

本版本尚有P18-R1，故新的live_root及supervision目录保持不存在。即使修复该点，仍须新精确封存和相符review/EXECUTE；方法可行或fake成功不自动执行。共享3600s/工作3590s/父停止3595s、owned PGID/单次claim等基础保护不是OS硬实时或完整子树证明；新HTTPsockettimeout也不单独等于整个阶段限时。

## 证据与限制

反例及执行源码/输入/输出SHA见`evidence.json`和`R02-preseal-changed-evidence/`。其中preseal探针后来逐项确认与最终封存相同，不用它冒充其他版本；8个响应fixture+1个假HTTP302检查，0真实工具/网络/key/SV。初始源文件查看误查不存在的http_transport.py（exit1），实际HTTP在api.py，无遗漏生产代码；这不是产品故障。未审实际API返回/真实资源执行或新科学效果。

Hallmark沿用此前同版真实SKILL/review-finish读取，本轮未新读；用于固定材料、定位/排序唯一实质问题及最小修订，无完整UI流程/脚本。技术结论来自精确代码、独立合成反例与保存证据。所有旧方法/base/R01/R02/失败/unknown保留；只写P18 reviewer目录，不给producer发消息，不改source/shared docs/index，不commit/push。
