# 复核 proof-carrying 实验归档

从仓库根目录运行。审计针对一个完整的 `egg_frame_pc_loop.py` 输出目录，或以该目录为唯一顶层目录的 `.tar.gz`。使用生成归档时的实验代码和同一份固定波形。Python 3.12 和 `z3-solver==4.16.0.0` 足以执行审计，重放已经保存的证明无需重新编译 Rust、运行仿真或连接模型服务。

```bash
python3.12 -m venv /tmp/frame-pc-audit-venv
/tmp/frame-pc-audit-venv/bin/python -m pip install 'z3-solver==4.16.0.0'
/tmp/frame-pc-audit-venv/bin/python scripts/audit_egg_frame_pc.py \
  --archive /path/to/run.tar.gz --output /tmp/frame-pc-audit.json
```

目录输入使用 `--run-dir /path/to/run`。归档读取器接受最多 32 MiB 的解压后文件内容，大归档使用目录输入。`--corpus` 默认选择仓库中的 `results/milestone3/frame-faults`。`--binary` 可选，仅在报告中记录本机可执行文件的 SHA-256，归档中的原始二进制哈希单独保存。`--output` 只接受新文件，省略后输出到终端。

1. 校验波形哈希与冻结起始候选。从全部 PRE 样本重算每个候选的物理评分，用原规格和当轮表达式重建全位宽 XOR，在 Z3 中逐项比较解析后的实际断言 AST（不把随意提交的 `assert false` 当成合法 UNSAT 回执），并独立核对求解状态。若已存 SAT 模型与本机求解器给出的合法赋值不同，逐位回放归档的模型。不同平台可产生不同的模型或 SMT 排版；AST 和候选绑定必须相同，纯粹空白或 let 打印变化不影响核对。
2. 根据原版和两个开发设计重新选择公开观察，逐组重建最小充分文字、候选侧诊断及反馈正文。匹配的候选必须获得相同的基础反馈、原始语义回执，以及 ordinary 和 egg 共有的诊断。逐字重建初始请求、每组自己的后继对话及响应 schema；模型能看到自己的前一轮输出和当时实际发送的反馈。留出的四个设计仅进入物理评分。
3. 按归档配置分派 DNF 和 cube 两种证明复核器，重新绑定当轮候选与观察值，重放具名改写及其完整路径，校验公开证书。报告分别列出所有归档阶段的证书状态与实际送入请求的状态。最后一次响应之后产生的评分和反馈已归档，但后面没有新的请求消耗它们。资源受限、超时等记录保留各自状态；从归档可以核查返回结构、结论与输入的绑定，机器当时实际花费的时间依赖原运行记录。
4. 用响应重算会话、首次验证成功轮和各组 token 汇总。真实格式要求独立 `resp_` 回包 ID、同一返回模型、HTTP 成功及完整计数。每条 `live_session_usage` 给出逐轮原始 usage 与 service tier，`usage_to_first_verified` 为截至首次成功轮的累计 input/output/total，预算内未成功则为 `null`。缓存和推理 token 已包含在父计数中。fixture 的该字段和 `provider_usage` 为 `null`，调用次数为 0。离线复核验证归档内部一致性，服务侧账单取决于供应商原始台账。

回归测试用真实语料生成小型确定性 fixture，另在内存中构造合成的回包封装检验计数路径。以下命令的二进制路径应指向编译好的 DNF 引擎。测试包括同时篡改证明与请求、复用其他候选的证明、替换本组历史、夹带留出信息、重复回包和伪造用量。

```bash
EGG_FRAME_PC_BINARY=/path/to/egg_diagnostic_forms \
  /tmp/frame-pc-audit-venv/bin/python -m unittest discover -s tests -p 'test_egg_frame_pc_audit.py' -v
```
