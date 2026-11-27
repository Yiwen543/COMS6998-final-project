# 复核运行归档

从仓库根目录运行。复用实验使用的 Python 3.12 和 Python Z3 4.16.0 环境，审计不需要申请模型额度或重新编译 Rust。若重新搭建本地环境，可用：

```bash
python3.12 -m venv /tmp/txn-audit-venv
/tmp/txn-audit-venv/bin/python -m pip install 'z3-solver==4.16.0.0'
/tmp/txn-audit-venv/bin/python scripts/audit_egg_txn.py \
  --archive /path/to/frame-txn-run.tar.gz --output /tmp/frame-txn-audit.json
```

`--run-dir /path/to/run` 可直接复核目录；压缩包须以一次完整运行目录为唯一顶层目录，超过 32 MiB 解压文件内容的归档请使用目录模式。默认语料为 `results/milestone3/frame-faults`。省略 `--output` 将 JSON 打印到终端。

`audit_egg_txn.py` 从原始固定 Icarus 波形重建 ghost 历史，重算每次有效候选的九项评分，从域和参考/候选端点重建全位宽 XOR 查询，校验每个 SAT 反例的完整原始引脚与历史赋值。审计独立汇总三个开发设计和三条轨迹，并按相同规则选择开发反例或符号反例，逐字重建发给模型的内容、响应 schema、共享的无辅助初稿及每组自己的后继对话。ordinary 和 egg 的相同候选必须收到同一份充分文字；egg 提供的每份证书需重放其绑定、规则和路径。报告将各阶段保存的所有证书与真正传入下一次请求的证书分开。会话最后一次回复后的反馈单独归档。

物理记录中 `unknown_both` 表示参考与候选在其各自可能补全中都无法确定，`ineligible` 表示复位、失去可观测性等原因使该义务在这个样本不可评分。二者都公开计数。合格要求九项有类型查询全部等价，且可比样本的多报、漏报和单方不可确定差异 `unknown_mismatch` 都为零。共同未知样本及不可评分样本不提供义务通过的观测证据。

真实格式报告核对每个回包 ID、状态、模型和 input/output/total。全局 `provider_total_counting_initial_once` 每个 trial 只计一次共享初稿。会话明细同时列出到首次合格的分支增量及含初稿的合计；初稿已经合格时增量为零，预算内未达标时为 `null`。逐轮原始 usage 保留 cached 与 reasoning 等子计数。fixture 的 provider usage 为 `null`，归档复核自身不产生 API 调用。离线审计可以验证回执之间的内部一致性，供应商的实际账单以原始服务记录为准。

完整两轮 fixture 可直接用于运行定向回归。未指定该目录时，也可设置 `EGG_TXN_BINARY` 为已构建的 `egg_cube_proofs` 路径，测试将临时生成小型 fixture。测试包括给盲生成插入答案、替换跨组历史、同步污染公开反例及下一请求、套用旧证明、弱化符号域、重复回包、重复计费，以及保留满分或无法解析的初稿。

```bash
EGG_TXN_AUDIT_RUN=/path/to/two-round-fixture \
  /tmp/txn-audit-venv/bin/python -m unittest discover -s tests -p 'test_egg_txn_audit.py' -v
```
