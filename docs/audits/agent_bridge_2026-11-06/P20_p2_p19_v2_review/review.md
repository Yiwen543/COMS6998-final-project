# P20 — P2/P19 v2 两页成品审查

**PASS_WITH_LIMITS。未发现当前可证实的实质问题，无需修改成品。** 格式、成品可读性、pilot图与保存证据一致；真实教师/TA反馈原文及回应仍pending，所以不能称课程内容四项全部完成，也未提交课程平台。

精确PDF SHA `8b9bba7b62d2c8490768a7e226af4c8859adc3e59344cd3b7528e111eb740075`；TeX/ZIP/data/figure及producer phase/manifest绑定见review.json。实际HEAD `745172e194885038a29b6d788bf2954ee02830ba`，49封存成员、349旧文件、15核心来源绑定均匹配，index不变。没有把旧HEAD当当前值，没有改旧P2或研究结果。

- 独立pdfinfo/文字提取确认2页USLetter612×792pt；conference/10pt/letterpaper、双栏、原4section名称、B5/三成员姓名UNI/2026Nov9 11:59PM ET正确。IEEEtran.cls与本地官方ZIP内class同SHA `da751920…a3bd7`，没有重定义正文页宽/字号。
- 实际查看render-v2两页PNG及主图PNG，并结合PDF文字核对：标题、双栏阅读、图注、轴/图例与数字清晰，未见裁切、重叠或缺字。最终build-v2 PDF与交付PDF字节相同，渲染receipt/PNG受seal绑定；未重渲染或编译。overfull0/underfull4不构成修改理由。
- ZIP CRC检查通过，9个成员与latex/目录逐字节匹配，无重复/绝对/上级跳转路径。主图PDF包含正确11/12、9+2未归因、N10无eligiblefailure和123663/133915，数据与P19接受记录吻合；独立算术C+8.2902727574%，不是独立重复均值/误差条。
- 新复测1session/arm×3round、6calls，B116529+7134=123663，C127168+6747=133915；reasoning/cache不重复相加。每轮162=18correct+144fault、raw12/union11、38oracleunknown、inputcompletion0/10 N01、N10为mutantID均披露。case-union/finite marker为UNATTRIBUTED，不升级category/general/128/unbounded证明；无额外C检错收益的描述有界。
- 页2明确 **combined** conservative usage-based cost upper USD1.569371是B+C合计且非invoice；177.995s含cleanup、12candidate compiles/990monitor replay/204444cycles是固定观察回放，不是新DUT/native。旧cohort单列3session/arm×6round=36calls，740643/813649（+9.8571106457%）；旧一个B final unresolved40而非38与audit一致，旧540状态75/104/361及74未复现保留，不合并cohort或用少轮总tokens称效率提升。
- proposal原stimulus coverage与test2 fixed-stimulus monitor转移明确；不是officialCVDP/Pass@1。当前原型确实completed，旧catalog/tier反例未抹除。G1限P17有限接受；跨IP暂停，futurepaperplan不是新实施/费用授权。真实课堂反馈缺口与内部review/用户方向明确区分，保留pending与未提交声明。

Hallmark主SKILL及review-finish本轮均实际读取，用于固定成品、证据/推论区分、视觉可读性及只列实质问题；完整网页/UI流程、脚本/Together不适用且未执行。PDF skill用于只读格式/文字/视觉审查，未author，不运行marker。

命令与哈希见checks.json/evidence.json。审查脚本首轮的格式正则误拒普通`includegraphics[width=\textwidth]`（exit1），修为仅拒页宽重定义后通过（exit0）；原脚本保留，非文稿缺陷。没有新研究/API/count/compile/replay/formal/G1/跨IP/install/key读取/Git写入/shared-doc改动/producer消息。后续metadata/既有授权发布由root处理，本报告不作课程提交或新实验授权。
