# 在线 B/C 对照与 token 复核

本轮复核了 M2 冻结 controller 的六个真实 Responses API 回包。B 三轮合计 123,663 tokens，C 为 133,915，多 10,252（8.2903%）。增加量来自输入。C 共多用 10,639 个输入 token，输出减少 387 个。两组最终都检测到 11/12 个原始故障类型，其中 9 类为普通安全属性，2 类仅有有限轨迹末端的 case 级证据。每轮每组 18 个正确对照通过，38 个参考结果未知的组合保留在清单里。每组仅一个会话，且语料已公开。[分轮账本](../results/milestone3/online-usage/audit.json) · [历史评分](https://github.com/Yiwen543/COMS6998-final-project/tree/e94172a1bd5e9b138b5fc3da01554edb3052ce52/test2/results/controller-done-bc-retest-v3/grade)

| 组别 | 三轮输入 | 三轮输出 | 输入 + 输出 | 输入中的缓存读取 | 输出中的 reasoning tokens |
|---|---:|---:|---:|---:|---:|
| B · 公开规格、RTL、原始计数与本组开发反馈 | 116,529 | 7,134 | 123,663 | 0 | 598 |
| C · 在 B 的材料上加入已验证关系 | 127,168 | 6,747 | 133,915 | 0 | 602 |

原始六个回包总数为 **257,578 tokens**。表中最后两列已包含在输入或输出内。上游顶层 `actual_generation_tokens` 为 `null`，原作者将逐请求记录作为计量依据。复核脚本检查响应 ID 的唯一性、实验顺序、provider 模型与状态、原始 `usage`、每次调用的标准化计数和逐笔账本，并校验响应数与支出上界。历史用量折算上界为 $1.569371，实际发票字段为空。990 次 monitor 回放共消费 204,444 个已冻结的观测周期，历史记录的新 DUT 仿真数为 0。[固定提交的原始观测与账本](https://github.com/Yiwen543/COMS6998-final-project/tree/e94172a1bd5e9b138b5fc3da01554edb3052ce52/test2/results/controller-done-bc-retest-v3)

M3 本轮新模型调用数为 0。该表只复核历史 monitor 生成实验。新测的 guard 耗时、SMT 长度、开发本项目的 Codex 会话用量都不参与计算。没有 M3 新一轮的 provider token、检测率或费用观测值。

## 离线复核

在 M3 仓库根目录运行。第一条使用随交付保存的压缩原文，在离线环境也可核验。第二条仅从 GitHub 固定提交重新获取三份公开文件。两个命令校验相同的 SHA-256，要求全新的输出路径，生成 `audit.json` 和压缩原文副本。Python 只需标准库。[复核脚本](../scripts/audit_m3_online_usage.py)

```bash
python3 scripts/audit_m3_online_usage.py \
    --source-dir results/milestone3/online-usage --output /tmp/coms-history-offline
python3 scripts/audit_m3_online_usage.py --output /tmp/coms-history-download
cmp /tmp/coms-history-offline/audit.json /tmp/coms-history-download/audit.json
```

## 新在线实验入口

保留上游 `test2/retest_v3/cli.py`。它测试的是相同公开 controller 上的**被动监视器生成**。B 与 C 分别维护自己的上一版候选和开发反馈。三轮交错顺序为 B1、C1、C2、B2、B3、C3，六个候选全部冻结后统一评分。模型为 `gpt-6.1-sol`、reasoning effort 为 `low`、返回 tier 为 `default`。每次输出上限 8,192 tokens，本地按完整 payload 的 UTF-8 长度估算 64,000 输入准入阈值，另核对回包中的真实用量。注册配置为零远程计数、零 SDK 自动重试、每轮最多一次人工失败重试、总共最多 12 次生成和 3,600 秒。历史实验共发送六次，零重试。[注册配置](https://github.com/Yiwen543/COMS6998-final-project/blob/e94172a1bd5e9b138b5fc3da01554edb3052ce52/test2/configs/controller_done_bc_retest_v3.json) · [真实入口](https://github.com/Yiwen543/COMS6998-final-project/blob/e94172a1bd5e9b138b5fc3da01554edb3052ce52/test2/retest_v3/cli.py)

下面的准备命令在新目录检出固定提交，保留已有语料和参考评分。上游 live 程序要求固定名称的结果目录和 supervision 目录都尚不存在。稀疏检出从新工作区排除这两个已发表的输出。仓库较大，磁盘和首次下载时间需要单独计入。

```bash
rev=e94172a1bd5e9b138b5fc3da01554edb3052ce52
git clone --no-checkout --filter=blob:none \
    https://github.com/Yiwen543/COMS6998-final-project.git /tmp/coms-controller-online
cd /tmp/coms-controller-online
git sparse-checkout set --no-cone '/*' \
    '!/test2/results/controller-done-bc-retest-v3/' \
    '!/test2/results/controller-done-bc-retest-v3-supervision/'
git checkout --detach "$rev"
python3 -B test2/retest_v3/cli.py --help
python3 -B - <<'PY'
import sys
sys.path.insert(0, "test2/retest_v3")
from pipeline import local_admissions
for arm, row in local_admissions().items():
    print(arm, row["UTF8bytes"], row["value"], row["payload_sha256"])
PY
```

本轮使用固定提交的 34 个 Python 模块与两份公开 prompt packet 跑通了以上 CLI 帮助和首轮 payload 构造。B1、C1 序列化后分别为 106,948、120,923 字节。完整 payload 哈希与历史回包记录逐一吻合。本地输入估算分别为 46,876、52,466，provider 当时实报 36,945、40,574。这一步可独立验证发送前的提示材料。后续轮次的输入取决于本次实际生成和评分。[提示和传输实现](https://github.com/Yiwen543/COMS6998-final-project/tree/e94172a1bd5e9b138b5fc3da01554edb3052ce52/test2/retest_v3)

以后需要新测量时，在上述独立检出中配置能访问该模型的 OpenAI Responses 账户，并确认价格和本次预算。固定的上游 harness 使用 $20 预算上限、仅属主可读写的 `build/private/midterm-openai-key`（权限 0600，父目录 0700），以及经注册配置校验的 `BC_RETEST_EXECUTE_V3` 执行记录和相应 review。新的运行须使用当次确认的执行记录。原始实验还依赖 `yosys`、`iverilog`、`vvp` 在其固定搜索路径 `/opt/homebrew/bin:/usr/bin:/bin` 中可用。本轮环境未配置该 harness 的 API 凭据。运行的 CLI 检查未读取密钥或发起身份验证。准备就绪后，以下是上游实际发起付费调用的入口。

```bash
python3 -B test2/retest_v3/cli.py --mode live \
    --output test2/results/controller-done-bc-retest-v3 \
    --execute "${M3_EXECUTE_JSON:?set the path to this run's execution record}"
```

每次新运行应从其独立输出目录汇总 `calls.jsonl`、`ledger.json`、`summary.json` 和 `grade/scores.json`。失败、未评分轮和 provider 缺失用量需单列。上述归档复核脚本锁定 M2 文件哈希，新运行的结果应保留自己的来源清单与哈希。原样重跑测量同一公开实验的重复性。比较新的 indexed egg 对在线质量的影响，需要指定改变了哪些实际发送的证据，并用同一输入预算及相同评分规则重新比较。
