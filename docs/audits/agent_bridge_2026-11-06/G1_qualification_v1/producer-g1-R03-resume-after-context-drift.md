当前唯一待办是 G1 R03 权限修复及累计额度续行准备，请恢复此任务。上一轮01a1af6e-580a-7780-9e23-4760a58e04db末尾误恢复历史PPT任务，最终回答PPT；这没有完成R03。PPT是已交付历史材料，不要再读取/编辑/联网处理它。当前推进线程已idle，因此此消息是安全检查点续行，不是打断。

请先读取 docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/producer-g1-R03-retry-preparation-prompt.md、continuation-decision-r03.json，并只读核对本轮已有源码/保存测试。R03尚无phase.json/snapshot-manifest，尚未封存，仍可在新v3准备范围修正；不要修改R01/R02/E01/P10/P10B/P11/原池。

已完成：test2/g1_v3新增allocation/continuation_contracts，owned_process_group_only无真实/bin/ps，累计setup1+剩余7，charge2+当前最多1198秒，18SV和标签保持。已保存 continuation-attempt1 27/27PASS；deadline-horizon-attempt1 14/14PASS。最新 continuation-attempt2 28项中1失败：test_28_final_persistence_crossing_cumulative_cap_cannot_pass，最终save耗时越界未被结束检查捕获。保留全部原结果、失败和执行源快照，精确定位最小修复；补纯mock红绿证据，修复后只跑必要受影响回归。不得将旧27/14通过当作最终版通过。

下一步：完成上述小修复→记录真实限制(不得承诺OS绝对实时保证/完整子进程清单)→封存 R03 新源码/登记/纯mock证据、差异和保护检查，提供phase/manifest及SHA，供已有reviewer P12增量独立复核。先停于P12检查点，不执行版本查询/编译/native/physical，不创建真实池/attempt lock；P12接受后我会按同一用户授权给精确EXECUTE，无需用户重复确认。

不要扩大任务或再增加非必要增强；保留旧失败。不要git add/reset/index/commit/push、API/key/install、旧实验重跑。R03保护基线见docs/audits/producer_test2_g1_R03_2026-11-06/preservation-before.json，当前10000 staged entries不归你修改。共享HANDOFF/STATUS仅你在封存时prepend本轮短状态并保持全部旧body。若上下文压缩，优先恢复此条和R03prompt，当前任务不是PPT，也不是回头重跑整个test2。请完成并尽快交付精确R03封存包。
