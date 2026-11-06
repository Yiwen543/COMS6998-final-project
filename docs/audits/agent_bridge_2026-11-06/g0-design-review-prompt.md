请继续既有独立复核，只读审查 D01 G0 设计快照，结果仅写入 docs/audits/agent_bridge_2026-11-06/P08_g0_design/。先核验 phase-packet.json 的 D01 phase/manifest SHA 及全部 18 个成员，实际 HEAD 以 Git 为准。优先读取 D01 snapshot 下的设计文档，再按需核验封存来源；不要把正在推进的 live 文档混入本次审查。

复核范围：9 份设计文档、44 个纸面失败案例、16 类公开控制定义；身份/严格串行/全局 halt/资源/unknown 分层、不可执行模板、输入/输出/不可变 release、width/signedness/guard/reset/phase、selected pre(S) 与 reference post(S-1) 边界、独立 Claude oracle 权责、候选可见性。寻找具体矛盾和能造成错误验收的设计漏洞；缺实现或未执行 G1 不算该纸面包伪造通过。保持 P04 原件 mismatch 订正及所有科学未决。P05-N1 仍 backlog，不擅自扩范围。

本次仍限文档/JSON/SHA/Git 检查：不写或执行 adapter/fixture，不重跑旧审计、实验、native、monitor、API，不读 key。用户已经另外批准下一阶段 G0 adapter 与轻量合成 fixture；推进聊天会在独立 namespace 实施，不能因此将 D01 的 false 权限改写或把纸面接受当科学资格。您无需等待实施，也不得评判未封存代码。不要新建 chat/agent；不要修改 shared HANDOFF/STATUS 或 producer 文件。

输出 review.json 与 review.md，明确 PASS_WITH_LIMITS/CHANGES_REQUIRED、每个实质问题的路径和准确证据、影响、最小修订与验收标准。区分阻塞和非阻塞建议；不把未发现问题当完全正确。记录精确输入 SHA/命令/检查数量和未执行项；如有明确实质风险及时反馈协调端，不直接打断 producer。
