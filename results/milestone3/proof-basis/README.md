# Controller 证书缩减

对固定的 AXIS Controller，保持 148 个目标的全部代表表达式、78 个目标等价类、87 个可共享验证的分组和证明连通性，普通结构算法只需重新认证 **44/281** 条规则。如果还需要保留先前每一条具名证明的原文，沿 egg 证明提取依赖，**50/281** 条规则在本次实验中足够。

| 策略 | 重新送入 Z3 的规则 | 目标等价类 | 同作用域分组 | 与原始一致的代表式 | 与原始逐字相同的证明 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 全部规则 | 281 | 78 | 87 | 148/148 | 70/70 |
| 收集所有原始 egg 证明依赖 | 50 | 78 | 87 | 148/148 | 70/70 |
| 普通结构算法 | 44 | 78 | 87 | 148/148 | 61/70 |
| 移除全部设计专用规则，仅保留六条通用布尔规则 | 0 | 128 | 132 | 82/148 | 0/70 |

普通算法先把原表达式按通用布尔规则规范化，依输入顺序保留未被先前项蕴含的等式。每次合并后，在原有子项上计算同余闭包。这个过程先留下 46 条，随后逆序检查每条是否已被其他边蕴含，得到 44 条。保留验证分组与代表表达式所需的全局最少规则数仍未知，44 是已复核的上界。临时移除某一条证书的结果也不能直接累加为批量缩减结果。

每组缩减后的具名规则分别由 Z3 重跑原有 QF_BV 义务，随后仅用该组规则在新进程中运行 egg 并逐步校验输出证明。两种缩减都保留了原有的 70 对证明端点。普通结构算法的九条证明改用了其他有效的推导。原始 70 条证明共引用 50 个不同的设计专用规则名。按当前校验器“每个被引用的名称都必须有已验证证书”的约定，这 50 条对重现并审核这批原文都是必要的，重跑也表明它们足够。

**原 RTL 校验。** 完整实验另外为每种配置检查 148 个“原始表达式 XOR 新代表式”的 QF_BV 查询，四组均全部 UNSAT。三条公开开发轨迹共做三次新的原 RTL 回放，176 个物理边沿，排除每条轨迹首次复位前的观测后共 173 个样本。每种配置的 25,604 个代表式真值均与原 RTL 探针一致。100 个目标获得相同的最早命中，48 个在有限样本中未命中。零规则对照的轨迹答案同样一致，但它丢失了原目标等价关系。完整实验还与先前记录逐项核对所有原 DUT 覆盖计数和独立 checker 输出。六处未解析的原生计数器映射按原样保留。

## 复现

先按仓库的 Milestone 3 环境说明安装 Python、Z3、Verilator 5.050、C++ 工具链和锁定版本的 Rust 依赖。在仓库根目录执行以下命令。每个输出目录都应为新路径。

```sh
export CARGO_TARGET_DIR=/tmp/m3-basis-cargo
cargo build --release --locked --manifest-path egraph/Cargo.toml --bin guard_proofs_fast
BIN="$CARGO_TARGET_DIR/release/guard_proofs_fast"
FIXTURE=/tmp/m3-basis-controller
python3 scripts/m3_controller_replay.py --fetch "$FIXTURE"
python3 scripts/m3_controller_basis.py --fixture "$FIXTURE" --binary "$BIN" \
  --output /tmp/m3-basis-full
```

`m3_controller_replay.py` 验证固定提交的 14 个文件，并提供原 RTL 的构建与回放。`m3_controller_certificates.py` 把保留的规则绑定至原始查询和目标上下文，核对其 UNSAT 结果。`m3_proof_dependencies.py` 校验 egg 每个推导步骤所用的方向、位置和规则名。`m3_controller_basis.py` 比较四种配置，并在每个配置的输出目录中写入可直接交给 egg 的 `egg-input.json`、完整图 `egg.json` 和代表式审计查询 `representatives.smt2`。

对于完全相同的快照，也可以只重新认证已发布的子集。这条路径实际提交 44 或 50 个规则义务。它校验已锁定输入的摘要，重新运行 egg，校验证明并匹配以全量实验为基准的目标指纹。证明依赖配置另外核对原文摘要。只有整套检查通过才发布输出目录。

```sh
python3 scripts/m3_controller_basis.py --fixture "$FIXTURE" --binary "$BIN" \
  --qualify ordinary_forest --output /tmp/m3-basis-44
python3 scripts/m3_controller_basis.py --fixture "$FIXTURE" --binary "$BIN" \
  --qualify proof_dependencies --output /tmp/m3-basis-50
```

完整实验的额外审计查询、初次取得全量证书及构建全量图的成本，都应与后续固定快照的规则复核成本分开计。表内数量描述复核义务。本实验没有进行配对计时，也没有测量新 RTL、变更后的规则或新环境上的加速比。

[完整分组结果与规则名单](summary.json) · [44 条复核记录](ordinary_forest-qualification.json) · [50 条复核记录](proof_dependencies-qualification.json)
