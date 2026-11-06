# P08a — 上下文与保全检查

**检查完成；尚未达到需要中断 active producer 的实质风险阈值。** 本结论仅描述检查时点，不是 I01 代码验收。

已观察到同一进行中的 turn 从 G0 交接整理转向旧 presentation 检查；不能仅按“单条异常消息”解释，因为后续可见消息和命令预览也在核对既有 PPT。但**是否有最新用户 steering 仍为 UNKNOWN**，不能据此认定未经授权脱轨。

- 线程：01a1a9f4-6ba6-70c3-9604-45275f4f5965（local），active。
- 当前 turn：01a1aec2-0195-7311-9264-a1f14da017b9，inProgress。
- 先有 G0“最终93项通过、整理44项覆盖映射”的 commentary（msg_0c7d1e3d7b9c26d2016aed447ff93487d2b2f82317c729db0b）。
- 随后有 contextCompaction（01a1aed4-5bf7-7382-a919-d3d572f3e393）。
- 再出现给定 PPT commentary（msg_0c7d1e3d7b9c26d2016aed451135cc87d2a106b3d6520d3bac）。这建立时间顺序，不证明 compaction 是原因。
- 一次 timeoutMs=0 状态快照的最新消息仍为“目录中已有一套完整成品，正在核对文件/Notes/图表”（msg_0c7d1e3d7b9c26d2016aed454b574c87d281da0b1fdfd03990）。
- 支持的 read_thread 返回最近两 turn 的状态/条目，但没有 userMessage 文本；故既不能确认新用户任务，也不能断言没有。未继续翻阅全历史或本地隐藏会话数据库。

## 保全核验

| 对象 | 检查时点结果 |
|---|---|
| P03 manifest | SHA 317d47ac20a5c389235b70a1885c4eddc9ebe8c091c9c0e03ed09cfbdf9c38a1，与封存身份一致 |
| P03 42份演示产物 | 42/42 snapshot 匹配，42/42 当前文件匹配；未发现字节覆盖 |
| P03 8份来源 | 8/8 snapshot 匹配，7/8 当前文件匹配 |
| 唯一当前来源差异 | HANDOFF 当前SHA 48aaa652ba5b5a8360bb77150270f2d1d61c163341f55de5aa8b6dbcc5cec34c，恰为D01已封存版本；属既有共享摘要演进，不是本次PPT破坏证据 |
| I01 scope保护输入 | 41/41 SHA匹配，0失配 |
| P08封存文件 | review.json、review.md和phase-packet仍匹配本轮之前SHA；本轮未写P08 |
| I01交接 | phase.json / snapshot-manifest.json 尚不存在；不能开始正式P09 |
| 实际Git HEAD | c25180848ebfe9a1f49da0aa5f579cac913e6428，不代表未提交成果 |

I01授权记录SHA：1a4884c8d7e2f356b5a2a6232726492a361fbef5410feb46f025bbbcc7a930de。scope SHA：30dd982738342f043c3c049a42e59f9a8841b39bd519815f103fc5c0a7681e98。授权限定G0离线adapter与轻量合成fixture，其他native/API/实验/旧结果删除等仍false。“93项通过”仅为producer既有汇报，未由本轮重跑或独立验收。

## P08a-N1 — 非阻塞上下文偏移疑点

P3，material=false，blocking=false。可见工作方向与尚未封存的I01交接确有偏移；新用户steering与原因未知。后续命令预览主要表现为既有材料读取/核对，部分命令被接口截断，不能据此证明所有操作只读。当前哈希结果未显示产物损害；也没有可证实的覆盖动作，故不建议立即中断或发消息。

最小建议：由协调端在下一idle/safe checkpoint核对真实最新用户任务。有合法新任务则等待其安全点；没有则恢复I01整理并封存。待精确phase/manifest后另做P09，不把本轮变成代码或旧PPT复审。

## 范围与停止

执行一次read_thread（最近两turn）及一次wait_threads（timeout0），只做JSON/SHA和Git HEAD检查。关键命令及exit0、逐项差异和确定性见review.json；精简线程证据见thread-observation.json。不保存完整历史/未封存代码预览。

未运行测试/实验、重做PPT、读取secret、改producer/shared docs/旧结果、向producer发消息或中断它。本次只写P08a目录。检查已完成，立即停止，等待后续精确封存交接。
