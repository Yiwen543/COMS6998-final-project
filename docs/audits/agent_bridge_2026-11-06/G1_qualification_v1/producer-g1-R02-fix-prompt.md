在当前idle安全点继续G1授权范围内的最小修订。独立P10正式CHANGES_REQUIRED，R01不可EXECUTE。两个具体阻塞已复现，均未运行任何真实compiler/native/physical工具；当前资源池不存在，真实额度消耗0。用户已批准本次G1实现/执行/独立复核，不需再次索取同一授权或key。此轮只修执行前基础设施，未看任何G1工具outcomes，也不是第二个已执行profile。

P10证据目录 docs/audits/agent_bridge_2026-11-06/P10_g1_registration/；review.json SHA cca7589786545675331ba1daa163d4e5cc757795aa8ac57972404e7463ee73e1；review.md SHA 9edcb094e704007eb0db1836fbb1214d5d9f1d7cedf222761781a79434a8d62b。协调端核验其全部evidence-manifest成员无差异。请先读两条findings及准确源行/fixture/SHA。P10独立手算16类标签均无失配，fresh14mocks通过，7次独立探针确认2缺陷。Hallmark本轮已实际读取并应用fixed-input/ranked/located/minimal-revision部分，非完整UI流程。

P10-R1(P1) budget.py:49,72–73/runtime.py:13,23,26：fake clock1194，reservation-save模拟耗时7，返回elapsed1201时limit=-6，runtime仍调用mockedPopen1次后才halt。应当0次。最小修订：保留已消费reservation，不返还、不新pool；persist完成后重新检查绝对work/globaldeadline和剩余可用timeout，目录/log准备完成后、Popen最邻近边界再检查。过期/非正/不足时persistent halt，charged-but-not-dispatched/NOT_RUN有明确终结证据，绝不先派发再补判停。不得延长原时钟、挪setup计时或靠超时后kill来代替派发前拒绝。增加纯fake-clock回归覆盖reserve/save跨界、mkdir/log跨界、already-expired和normal基线；无真实sleep/child工具。保留普通timeout/原deadline绑定通过路径。

P10-R2(P2) observations.py:81,97,101/runner.py:116,146：analytic-preflight/full-observer-vcd-truncated-before-post15.vcd仅至14ns，却为15ns row取lasttick<=row而被ACCEPT。完整16ns counterpart应ACCEPT，原始truncated应按缺尾/超出记录跨度拒绝或不资格，不能延续EOF值到未来。请对每个required row/selected sample检查记录VCD时间跨度，保留missing/truncated原始原因和余下NOT_RUN，不伪造样本/重采样。直接用原保存complete与truncated fixture的精确深拷贝回归，保持输入SHA和结果绑定，拒绝理由必须确为coverage horizon；未知值/缺信号等既有拒绝仍正确。

版本/保全：R01 phase/manifest、test2/g1_v1全部source/tests/config/labels/results及P10输入/探针/报告一律保持字节不变；旧G0/P01-P09/Oracle/score/freezes/raw/history不改。建立唯一新R02源/registration/result namespace（例如test2/g1_v2与g1_qualification_registration_v2.json、g1-qualification-v2；具体名称自行一致化）。SV控制、原输入/数学标签、profile/flags/job顺序及全部帽本来已获限定分析接受，原则上内容SHA保持不变；只更新必要基础设施/manifest路径和source bindings。若额外改动必须列出理由/前后SHA，不扩大控制语义或科学scope。不必加固P05-N1等backlog或非阻塞建议。

允许仅必要的新G1纯Pythonmock/解析回归，保存每次真实执行source、final-mutated fixtures、result/argv/exit/失败及耗时；不重跑旧cohort/旧测试/实验/companion审计，不运行任何SV编译/native/simulator/solver/版本探针来恢复上下文。本次仍实际工具0、pool尚未创建。原user grant bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab及32native(depth8/10s)/32physical(1024cycles,2s each)/32compile(20s each)/1200s总执行池不变；之后只有最终accepted exact R02一个版本执行，不能R01/R02各给一份额度。无API/count/generation/Claude/key/network/install/删除/commit/push。

封存新的 docs/audits/producer_test2_g1_R02_2026-11-05/phase.json与snapshot-manifest（路径冲突另唯一版本）及准确source/config/input/P10证据/回归SHA。共享HANDOFF/STATUS仅新增紧凑修订入口、旧正文逐字保留。保持R01和P10的历史CHANGES_REQUIRED，不自签独立通过。交付R02后停在安全点，由协调端送既有reviewer做P10B增量复核；其review.phase应以P10开头并input_identity明确绑定新producer manifest与registration，以满足新runner的exact gate。接受后同一用户授权EXECUTE，不重复问用户。

