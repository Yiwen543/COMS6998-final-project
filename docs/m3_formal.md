# Arbiter 同步复位的跨边沿形式验证

规格要求复位在时钟上升沿生效。已有定向回归发现，当一次有效授权之后在低电平阶段拉高复位时，原始 RTL 会提前清零。本实验让 Z3 在输入空间中搜索这个时序违例，再用 Icarus 驱动原始 RTL 重放所找到的输入。已知缺陷只计一次。该实验用于检查验证质量，未用于测量 egg 的加速倍数。[规格](../examples/arbiter/docs/specification.md) · [原始 RTL](../examples/arbiter/rtl/fixed_priority_arbiter.sv)

## 性质与边界

每个 SMT 状态对应一个半周期，初始状态时钟为低，随后交替高低。复位必须覆盖第一个上升沿。请求、override 和复位可以在进入低电平时变化，并保持到上升沿之后。启动完成后，如果上一个高电平采样有有效授权、复位为低，而当前进入低电平且复位变高，则三个输出 `{grant, valid, grant_index}` 必须保持上一次采样值。该性质只检查这个触发条件下的复位保持行为。

Harness 直接实例化 DUT。Yosys 的 `clk2fflogic` 对时钟边沿和异步复位建模，因此低电平采样能够观察提前清零。另一个查询保留相同输入假设和转换关系，单独用 `cover` 搜索触发场景，防止因前件不可达而出现空洞通过。控制版本只把敏感列表改为 `@(posedge clk)`，脚本在临时目录中生成它。两项设计使用相同的位宽、性质、假设和搜索深度。[性质与 cover](../examples/arbiter/formal/reset_hold.sv)

## 实测结果

| 设计 | Z3 对触发场景的 cover | 安全性质 | 同一反例的 Icarus 重放 |
|---|---|---|---|
| 原始 RTL | 状态 4 可达 | BMC 在状态 4 发现反例 | 低电平复位后，`grant/valid/index` 从 `01/1/0` 提前变为 `00/0/0` |
| 同步复位控制 | 状态 4 可达 | 状态 0–7 的 BMC 通过，同一模型和假设下时间归纳通过 | 同一采样前后均为 `01/1/0` |

求解器给出的输入依次经历三个阶段。状态 0–1 的 `reset=1` 覆盖第一个上升沿。状态 2–3 的 `reset=0, req=0x0f, priority_override=0x01` 在第二个上升沿产生有效授权。状态 4 时钟落低，`reset=1, req=0, priority_override=0`。真实 RTL 的立即清零与同步复位规格冲突。原始反例有五个半周期采样、两个时钟上升沿。归纳结论仅覆盖控制版本的上述复位性质和两态离散时钟模型。多比特 override 的功能、任意亚周期脉冲、四态语义以及整个 DUT 的正确性仍在结论范围之外。[原生 Yosys 反例](../results/milestone3/formal/counterexample.yw) · [结果及逐状态输入](../results/milestone3/formal/summary.json)

## 环境与复现

测量环境为 Debian 13 x86-64、Python 3.12.14、Yosys 0.52（包含 `yosys-smtbmc`）、Z3 4.16.0 和 Icarus 12.0（包含 `vvp`）。在 Debian 13 可用以下命令配置和运行。Python 脚本仅用标准库，虚拟环境安装的 wheel 提供 `z3` 命令。

```sh
sudo apt-get update
sudo apt-get install yosys iverilog python3-venv
python3 -m venv /tmp/m3-formal-venv
. /tmp/m3-formal-venv/bin/activate
python -m pip install z3-solver==4.16.0.0
python scripts/check_m3_formal.py --output /tmp/m3-formal-results
cat /tmp/m3-formal-results/summary.json
```

`check_m3_formal.py` 校验 DUT 的 SHA-256，分别生成两种设计的 SMT2，运行 BMC、cover 及控制版本的归纳检查，最后解码原生 Yosys 反例。Icarus testbench 按原有次序逐半周期驱动所有输入，检查激活点和清零前后的输出。两次重放分别针对原始 RTL 和控制版本。任一引擎异常、超时、未触发 cover、重放状态缺失或结论不符都会使脚本失败。脚本成功后写出 `counterexample.yw` 和 `summary.json`。具体反例的自由输入可能随求解器版本改变。[运行脚本](../scripts/check_m3_formal.py) · [重放 testbench](../examples/arbiter/formal/replay_reset_hold.sv)
