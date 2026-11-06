# P18 同轮基础路径检查点 — R01固定来源

**基础范围PASS_WITH_LIMITS；不是R01或R02 live接受。** 未发现本次已审基础路径中可证实的实质阻塞。R01仍countfee-blocked；R02未审，最终review.json留待精确封存与新财务/HTTP实现验收，不能凭本文件签发EXECUTE。

精确R01 manifest SHA `f11203621b0cec51861d423c360d7e95f9bbecee904921dd9dfc82d5a406fa32`。12326封存成员及916个snapshot来源依赖逐项SHA匹配。只读R01 snapshot，不把活跃R02混入，也不要求当前共享HANDOFF与老snapshot相同。

- `pipeline.py:130–165`按B1/C1/C2/B2/B3/C3分别维护两session状态，`old.messages`只将本组上一候选/开发反馈加入固定公开包；没有把grader/reference/hidden/raw评分或skills传给模型。两个冻结packet的共同字段逐项相等，C只多`egraph_feedback`。
- `release.py:20–45`在六个snapshot齐备、两session分离之后释放，再调用统一旧grader；两个final各选最后一个compiled轮次。新增纯合成release检查确认缺一轮拒绝、重复释放拒绝、候选冻结后变动拒绝、最终轮次B3/C2选择正确。合成文件非SV或模型输出。
- 旧`controller_done_grade_v4.py`/`controller_done_case_v4.py`的162-case inventory与raw12/N10/unknown语义未改；保存的完整mock/replay各六轮均有162cases及38oracleunknown。由冻结records与三个公开开发轨迹复算每pass上限12compile、990monitorreplay、204444cycles，非新增DUT/native。缺失/坏证据保留unresolved，不以候选自评替代oracle。`Halt(BaseException)`越过旧grader的Exception吞错；终止后保留六轮/972 plannedcase的未完成状态，不能称全评分完成。
- `supervision.py`/`cli.py`为同一start传递3600s总窗、3590s工作截止和3595s父进程强制清理点；API/local children继承唯一stagePGID。新增纯假对象分别核验正常返回及到3595后的TERM/等待/within-total路径；没有启动进程、发信号、睡眠或证明OS硬实时。`child()`将单项上限取剩余work，并在返回后拒绝过期；慢文件系统/OS不可抢占及未覆盖异常路径仍是限制，不据此扩建通用调度框架。
- R01的API child在key/SDK前查实际gate、open reservation、消息/schema/price、clock与lease/父worker/PGID，再用独占claim防重复。独立小fixture确认匹配元数据可解析，错payload/clock/group及重复claim拒绝。fixture中mode=live仅用于函数分支，路径和记录均显式SYNTHETIC，不是API调用证据，也不是R02新定价资格。

生产者保存证据：最初18项含1失败、修后19项通过、最终6项guard通过，分开保留。19项之后api/cli/pipeline发生已披露的lease等delta，因此不冒称最终源码“一次25项全通过”；本轮也未重跑19项或旧pipeline。新增审查6组小检查PASS。首轮审查副本少拷gates.py，import失败exit1，未到测试；源码/副本保留于base_checks_attempt1.py/base-evidence。补齐审查副本后base_checks.py运行exit0，结果在base-evidence-attempt2/summary.json，非生产者缺陷。

**R02尚待核验**：最终source/reg/prep/costbasis/policy身份；0远程count/stdlibHTTPS固定endpoint、不redirect/不retry；保守5910168微美元派发前预留与可信usage结算、unknown/超目标halt；实际网络前最后截止检查、key边界、父子清理；基础文件与本R01版本若有改动须精确diff。不能因此基础checkpoint关闭这些事项或给R01签发live。P17仅复用有限资格，不重跑G1，不扩跨IP。

Hallmark使用此前同版SKILL/review-finish真实读取（hallmark-method-usage.json），本轮未重读；应用于固定材料/事实与计划区分、只列实质问题与最小修改。无UI流程/脚本/Together。技术依据为源码、保存数据、哈希和独立纯离线小fixture。写入仅P18 reviewer目录，无API/key/实物/安装/Git写入/producer消息。
