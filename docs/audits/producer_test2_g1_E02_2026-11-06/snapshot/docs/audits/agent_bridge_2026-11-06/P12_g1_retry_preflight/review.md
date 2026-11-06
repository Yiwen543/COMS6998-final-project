# P12 — R03 G1 受限续行执行前复核

**PASS_WITH_LIMITS；当前未发现可证实的执行阻塞。** 仅接受精确R03准备版本。协调端可随后在原授权剩余额度内交付精确EXECUTE；本复核不自动执行、不新建额度、不代表G1资格通过。

## 精确输入与实际差异

实际HEAD：`c25180848ebfe9a1f49da0aa5f579cac913e6428`，不代表全部dirty工作树成果。packet、phase、manifest、registration/source/decision绑定均独立核验；649封存成员、48来源绑定、2382保护文件前后均0失配，current与snapshot一致，Git index指纹未变。51份review-owned复制输入前后不变，真实R03 pool/attempt.lock均未创建。

输入身份完整SHA见review.json.input_identity；manifest为169e27b1180a9e3a866559b48864b2352ec4a5715230d315e4abfc4e158e2f59。旧E01终止池、P11原件及原grant/decision均绑定。24语义/参考材料及observations.py与R02一致；job argv/order只做路径规范化，唯一删除setup-make。caps/tool pins不变。复用P10/P10B有限语义推导，无旧实验重跑。

## 逐项验收

| 项目 | 判定与证据 |
|---|---|
| P11-R1权限依赖 | R03预检范围关闭。runtime.py:36–49、60–78、90–132：注册入口inventory_probe=None，无ps/run扫描；AST仅见Popen。optional PermissionError/OSError/timeout分别记录unavailable/incomplete，正常root exit由poll/wait确定。 |
| 必需保护 | runtime.py:65–78、90–132：自身PGID探测/kill/wait/poll失败保留PROTECTION_UNRESOLVED并halt；独立探针随后再次请求均无新Popen，预留不退款。pending timeout仍使用原deadline。无完整子树或硬实时保证。 |
| P10-R1 | budget.py:77–91、107–142及runtime.py:52–61：慢save/mkdir/log/最近precheck跨界均0 mock Popen；保留CHARGED_NOT_DISPATCHED/NOT_RUN与持久halt。未重置clock。 |
| P10-R2 | observations.py字节未变；新鲜14项包括完整16ns观察接受、14ns尾段按VCD_TIME_COVERAGE_MISSING拒绝、缺头/未知/缺信号/未来native候选拒绝。无波形回放。 |
| 累计预算 | allocation.py:59–102、budget.py:14–53：执行前核对不可变旧pool/grant/phase/P11/decision及终止状态，setup1/实测0.04572445806115866s与charge2分列；最多7setup/1198s，work1193s。假旧用量0、扩大窗口/祖先漂移均拒绝。 |
| 最后持久化越界 | budget.py:152–178、runner.py:188–202：修复后的独立完整main收尾对照，正常exit0；末次save推进1199s时，磁盘completed=true/halted=true/charged1201，特定halt原因FINAL_PERSISTENCE_EXCEEDED_CUMULATIVE_WALL_CAP，runner exit1。未以别的异常掩盖。 |
| 新门禁与独占 | runner.py:32–72、83–88及continuation_contracts.py:39–54：新P12身份+新manifest/reg/source+continuation+旧pool；完整review_gate独立baseline接受、7个旧/错误身份负例拒绝。固定lock/pool独占创建，不支持任意多路径/并发资源池泛化。 |

源码SHA：runtime d34cc3a9c01ae55fdf3fd97c55116f0287e74ef8d8ad94e851e9607e2cdd7d7f；budget 257dc9da8130c0b5a5ca1f09096524004a422193bb120a8b73c59b8072f107ab；runner 73f0aee7ad26cc761d894a97d52f7f7981f766c7a77483d75ac86dafef2c4485；其他逐源SHA见review.json/evidence-manifest.json。

## 验证数量、命令与审查者错误

- Producer保存111次pure case invocation含1失败，最终源28+14=42通过；旧attempt2原tool退出码UNKNOWN，保存summary/log确定失败，不补造exit1。
- Reviewer复制后新鲜运行同两小模块42项，均exit0/0fail；未运行旧R01/R02/G0套件。命令入口run_fresh_suites.py及两个内部suite exit均保存。
- 独立探针初次31次，其中29个非收尾探针有效；2个初版收尾夹具漏放标签文件而提前FileNotFound。正常基线失败，越界夹具虽“匹配失败”但原因错误，**两者均排除验收证据**。原文件/输出/exit1全部保留。
- 新finalization_probes_v2.py仅重验修正的2个对照，均符合预期。因此独立共33次调用、31个有效独立检查；不是33个首次即成功。最终越界fixture SHA6b2b3783ac52aba5f0c5c57d8955757cc1487919b862d80223a30525b9f60c56；正常fixture SHAe24a9309c84b8adb7dd83b4be4bbe74056c3575014ac0585b2484849a9b2ce4c。逐fixture/result SHA在各summary和证据manifest。
- 首次输入检查另有reviewer封存路径映射错误：checklist实际在包根，不在递归snapshot；修正映射后两次0失配，初次exit1/result保留。不是源输入缺失。

完整命令和退出码见commands-and-incidents.json。全部Python以PYTHONDONTWRITEBYTECODE=1执行，真实G1工具/version/compile/BMC/sim/ps/signal/API/network/key/安装均0；运行器中的进程与sleep全mock。实际OS保障不由fake结果扩大。

## P12-N1 — 非阻塞来源范围说明

severity=P3，material=false。phase.json的actual_R03_resources.network=0及commands-and-checks中的0仅按**受控G1准备路径**解释。P12a已记录同turn转向旧PPT、网页读取和辅助记录写入；42PPT当时无漂移。不能将整turn描述成仅G1/完全无network。该事件已于idle恢复，不重审或推断PPT覆盖/API调用。建议后续closure sidecar引用P12a并明确上述scope；不改封存原件、不为此阻塞代码预检。完整full-turn耗时未测，不填0；producer partial authoring/recovery span与G1执行耗时分列。

## Hallmark、路由与保留限制

本轮实际新读Hallmark SKILL.md与review-finish.md，SHA与此前版本一致；用于固定材料独立critique、事实/意图区分、定位/排序与最小修订，本报告上述三处有对应应用。workflow/scripts=false，未运行网页/UI/Together。技术结论来自源码、SHA和独立纯fake，详见hallmark-usage.json。

接受后仅可路由G1_EXECUTE_CONTINUATION_AFTER_P12精确收据，绑定本review SHA及R03 manifest/reg/source/decision/predecessor。不再询问同任务重试许可；不把评审本身当EXECUTE，不修改/重开E01池、不退款。累计原32compile/32BMC+cover(depth8/10s)/32physical(2s、≤32cycles/run、1024total)/1200s仍有效，当前至多7setup、1198s。18逻辑编译根作业不等于18OS进程；make版本NOT_REPROBED。

G1仍NOT_QUALIFIED：R03无真实控制结果；E01/P11失败与未知不改。无完整PID清点/任意脱离进程组后代约束、OS绝对实时或通用多进程并发事务保证。QC07/15空泛、QC12/13四态限制、QC14运输、128completion/general correctness、74未复现、selected样本/类别、F1/H1/H2/L1、P04证据订正、P05/P06限定范围、P05-N1、billing UNKNOWN和R0/R1/R2 planned均保留。未扩大到G2/API/数据/候选/付费。

只写P12自有目录，未联系producer/创建agent或chat，未改source/shared/results/index。完整保全和命令见JSON；本轮到此停止。
