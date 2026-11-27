# 删除两条 De Morgan 规则对证明长度的影响

在配对的离线 cube 实验中，三个 profile 各有两轮请求。每个 profile 的第一轮收到 5 个待解释样本，第二轮收到 3 个。此次复核保留全部 24 个请求位置，共有 14 个不同的受限公式。原有 19 条规则中的两条 De Morgan 规则向内展开否定，此次仅删除这两条。每个输入继续用相同的最小充分条件将候选式限制到实际样本，唯一目标仍为 `true`。

| 结果 | 原有 19 条 | 保留 17 条 |
| --- | ---: | ---: |
| 有完整回放证明 | 24/24 | 24/24 |
| 完整证明符合反馈预算 | 20/24 | 20/24 |
| historical 符合预算 | 6/8 | 6/8 |
| mixed 符合预算 | 8/8 | 8/8 |
| corner 符合预算 | 6/8 | 6/8 |

四个超限位置均为 `header_hold`。historical 的同一证明出现两次，均为 56 步、7,195 字符。corner 的同一证明也出现两次，均为 50 步、6,900 字符。原实验的 24 份最终证明均未引用 De Morgan。删除规则后，有四个位置改选了其他有效推导，只有其中两个位置的步数下降。两种配置都采用最多 32 步且最多 6,000 个序列化 JSON 字符的完整反馈预算。此次复核没有调用模型，也没有把新生成的证明重新发送给模型。

## 重跑

使用原实验的 Python 环境（含 `z3-solver`）与 Rust 工具链，从仓库根目录执行。输入压缩包应是配对 cube 的离线实验记录，也可用 `--run-dir` 指向解压后含 `config.json` 的目录。

```sh
cargo build --release --locked --manifest-path egraph/Cargo.toml --bin egg_cube_proofs
python scripts/check_frame_pc_cube_rule_ablation.py \
  --archive path/to/cube-fixture.tar.gz \
  --binary "${CARGO_TARGET_DIR:-egraph/target}/release/egg_cube_proofs" \
  --output /tmp/cube-rule-ablation
```

脚本核对每份原反馈确实出现在对应请求中，独立回放原证书，再对相同输入运行 17 条规则。两组都核对精确改写位置、方向、替换子树和完整目标。输出包括逐条受限公式、两组成本与回放步骤、新规则组的原始 egg 图、来源哈希和预算。[汇总](summary.json) · [24 条逐项记录](cases.jsonl)
