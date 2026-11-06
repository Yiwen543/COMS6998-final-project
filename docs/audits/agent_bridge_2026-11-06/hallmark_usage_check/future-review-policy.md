# 后续独立复核的 Hallmark 使用与披露政策

来源：用户明确偏好“尽量每轮独立复核都用到hallmark”，由协调端交接至既有复核线程。适用于此协作后续每一轮；不追溯改写已封存历史。

## 每轮准备

1. 明确复核对象和授权范围，考虑Hallmark的适用部分。
2. 尽量在本轮阅读当前SKILL.md。若复用确切同版本的已读内容，校验来源/哈希并引用先前读取凭据；read_this_round=false，不冒称新读取。
3. Hallmark不可读取时记录事实与影响；不靠安装存在、skill列表、名字、普通agent或其他skill充当读取/应用证据。
4. 按适用性继续专项技术复核，不为了“使用Hallmark”增加无关UI操作或扩大范围。

当前可复用读取锚：
- hallmark_usage_check/reviewer-findings.json → hallmark.read_evidence。
- /Users/yiwenchen/.codex/skills/hallmark/SKILL.md，v2.0.0，SHA256 25a1ff92d925b2389e8409f42fb8ad7e033fceca8b5d1f07ed4ca4c28da53dc3。
- 此锚只证明本次实际读取；历史安装pin407fa689f4a276f2fd389208d271d0fef08f5058不代替未来字节核验。

## 适用性

网页、UI或可交互报告界面：可按用户任务和权限采用Hallmark设计audit，读取references/redesign.md及相关gates，记录实际对象/页面/证据、分层问题、准确位置和最小修订。只有真实执行的步骤才记为已执行。设计audit不能证明底层实验数字或代码正确。

RTL、formal语义、研究设计、freeze/数据、费用/资源/归因、Python adapter等技术审查：查阅后明确其UI流程不适用。可参考实际有关的“真实材料与不可捏造事实、按证据报告问题”等部分，但逐项写用途；不把通用纪律或普通独立技术审查重新命名为完整Hallmark流程。

纯文档/上下文/技能核查：允许记录“读取用于适用性核查”，与“按Hallmark审计项目”分开。不存在合适应用时，如实记not_applicable_reason并继续已授权技术方法。

## 每轮输出字段

以下是字段约定，不是已经发生的测量：

```json
{
  "hallmark": {
    "considered": true,
    "read_this_round": null,
    "source": null,
    "source_sha256": null,
    "version": null,
    "read_evidence": null,
    "prior_read_reference": null,
    "applied_for": [],
    "workflow_executed": false,
    "scripts_executed": false,
    "not_applicable_reason": null,
    "technical_review_methods": [],
    "limits": []
  }
}
```

- read_this_round：有实际阅读凭据才填true；确知本轮未新读填false并列prior_read_reference；证据不完整为null/UNKNOWN。
- read_evidence：工具名及参数、可用的调用/消息ID或真实命令、路径、返回版本与SHA。没有稳定ID就说明，不能编造。
- applied_for：列具体实际应用的内容和产物位置；只有计划未执行必须另标planned，不能填成已应用。
- workflow_executed：说明哪些设计audit步骤真实完成；非完整流程写partial和具体范围，不能笼统宣布Hallmark通过。
- scripts_executed：未执行填false；执行时另列脚本/参数/退出码/输入输出SHA，失败也保留。
- technical_review_methods/limits：始终独立列出RTL/形式、数据/资源、代码、反例或文档等专业检查及未检查项，不能让Hallmark名称替代证据。

## 权限与历史

用户偏好不是Together/API、付费、key、安装、构建、截图或实验的通行授权。只在对应任务授权范围内执行必要步骤；不为了制造使用记录运行Hallmark脚本、改设计、建立后台任务或新agent/chat。不读secret、不注入候选prompt或独立Claude oracle包。

本次仅允许这三份记录，不修改shared HANDOFF/STATUS。未来阶段若仅因范围不适用而未执行UI流程，应说明原因，不制造无必要的审批或阻塞。

冻结的旧复核不回填Hallmark字段。本次回溯结论按证据保留未知；新的读取不能证明旧的使用。没有新证据，不改变任何旧技术结论或科学未决。
