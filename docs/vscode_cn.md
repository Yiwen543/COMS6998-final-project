# 在 VS Code 中运行 EDA 和 Agent

打开仓库根目录的 COMS6998-final-project.code-workspace。这个工作区只指向实际 GitHub 本地仓库 COMS6998-final-project。

在菜单“终端 → 运行任务”中选择：

1. **检查 EDA 环境**：列出实际工具版本，检查覆盖率选项。
2. **运行 EDA 闭环验证**：构建 egg 和 Verilator，运行 initial/refined/exhaustive，用 Icarus 交叉检查，再输出 Yosys JSON。此任务不调用模型、不需要 API key。也可以直接按 Shift+Command+B。
3. **预览 Agent 请求**：选择 A/B/C/D，将实际 API 请求保存到文件，不发送。
4. **单轮 Agent**：选择反馈组和模型，在密码输入框中输入自己的 API key，进行最多一次模型请求、最多四个新增输入向量的真实仿真测试。密钥仅传给该任务进程，不写入设置或实验文件。
5. **Agent 离线测试**：不需要 API key。
6. **完整测试**：还会运行 egg 语义测试和 Icarus checker 控制测试。
7. **运行 CVDP 多模块 EDA 对照**：运行三个新增模块。
8. **预览 CVDP Agent 请求**：选择模块，检查请求。
9. **单轮 CVDP Agent**：选择模块、反馈组和模型，调用一次 API。

每次 EDA/Agent 运行创建新的 results/vscode/时间戳目录，避免覆盖既有实验。latest-step1.json、latest-preview.json、latest-smoke.json 指向最近一次成功的输出位置。

Verilator 的 GNU Make 构建不支持含空格的目录。项目会把三份构建输入按原始相对路径复制到 /private/tmp 下无空格的临时目录，并在 build-inputs.json 中记录哈希。源码、实验配置和结果仍在 OneDrive 项目目录；临时编译目录可由系统清理。

运行日志、原始覆盖率、checker 结果和 Agent 回执应分别查看。原始 Arbiter 存在已知规格缺陷，checker 报错代表检测到了问题；不要把缺陷数量与重复触发次数混淆。

早期 Arbiter 上 C/D 表示相同；扩展规则后反馈可以不同，但新增 CVDP 模块中 C/D 确定性刺激仍相同，尚未证明 e-graph 独有优势。进行四组批量研究前，应扩展能够区分这些表示的样例。

终端也可以运行：

```sh
python3 scripts/vscode_task.py doctor
python3 scripts/vscode_task.py step1
python3 scripts/vscode_task.py preview --group C
python3 scripts/vscode_task.py test-all
```

模型运行在 OpenAI API，EDA 工具在本机运行。真实模型调用需要你账户可用的 API key；ChatGPT/VS Code 的登录状态不能代替该环境变量。
