# P18 — R03 精确修订增量预检

**PASS_WITH_LIMITS，scope `BC_RETEST_V3_EXACT_PRECHECK`。** P18-R1在精确R03版本关闭；可由root按原授权签发相符的唯一`BC_RETEST_EXECUTE_V3`并进行一次已批准的同IP复测，无需再向用户索取相同权限。本报告不是EXECUTE，未启动实际调用。

R03 phase SHA `78125b2fa85eadecbab7b5dedb6ad1ad4357a057ce25cb8c55e81a0eb66c0832`；manifest SHA `b4fcdc5d5c8656e90785294814502af31f78c32839ab266e55414a16d6e9aca6`。151封存成员、963来源依赖全部匹配；新reg/source及四项不变policy身份完整绑定于review-R03.json。

`test2/retest_v3/resources.py:34`现在只接受明确`default`。独立复用旧反例内容、深拷贝并在执行前保存四个provider fixture：缺失tier、null、flex均在response合同层拒绝并halt，raw JSON保留，commitment5910168、settlement/release0、journal只有RESERVE；default64000/8192仍接受并结算487168微美元，未消耗预留5423000明确不是invoice/refund。四项独立检查exit0，不是重跑生产者四项；生产者保存的caller级四项证据另核源码绑定。调用链资格检查先于settle/候选接受，相关caller除命名空间外未变，故复用既有caller审查，不再跑全套。

所有七个runtime文件逐项diff：resources只有tier equality功能变化，其余仅V2→V3注册/执行scope/path替换；release.py与supervision.py完全相同。注册仅id/status/run_root/source_manifest/preparation_manifest/repair_of改变，API/价格/时间/score/prompt约束未变。V3 gate仍要求七项精确identity及独立接受，旧V2 scope/receipt不适用；lease/独占claim/公开包/ownhistory/六snapshot冻结后score/162cases/38unknown、父子PGID/同一deadline路径复用原核验。

财务/方法接受范围沿用：0远程count而非count免费；每次可能收费派发前持久预留USD5.910168；可信符合合同响应才按最高费率结算，失败/未知/超目标不释放并停止。USD20 inclusive、max12generation、output8192含reasoning、60min含cleanup不变。64k为ESTIMATE目标/实际usage验收，不宣称服务端硬帽。指定model/default/30m、无附加工具/自动重试是已审费用上界的合同前提；发票仍UNKNOWN。

旧`review.json`的R02 CHANGES_REQUIRED及反例全部保留，SHA仍`380dc2deabf0a8972d5c1db46b0475ab8a1b0c241b89ff66657f329e31a36d9b`，不改写历史。新live_root与supervision目录不存在；本审查无真实API/key/network/SV/ps/process/signal/安装/Git写入。没有重跑R01/R02基础套件、18+1targeted或G1。

Hallmark沿用此前同版实际SKILL/review-finish读取，本轮未新读；用于固定输入、仅验实质修订、保留历史及事实/计划分离。无UI流程/脚本，技术结论来自精确diff、SHA与四个纯离线fixture。接受只覆盖该一次复测执行前条件，不是实际B/C结果、账单证明、OS硬实时/全子树保证、general correctness或新增研究权限。实际结果、失败/NOT_RUN与全部费用仍须保存和后审。

证据、输入/执行源/输出SHA与实际命令见evidence-R03.json及R03-delta-evidence/；未发现当前可证实的新增实质问题。
