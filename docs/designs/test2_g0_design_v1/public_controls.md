# 16 类公开控制：仅纸面定义

DESIGN_PREPARATION_ONLY。全部定义尚待独立纸面复核；没有 source、waveform、独立运行标签、逐周期输入／输出或可执行 fixture。所有 actual_result=null，三个资格状态均为 NOT_CREATED_OR_NOT_QUALIFIED。以下人工预期是拟议控制意图，不是 GPT 编写的真实 DUT oracle，更不是实际通过结果。机器可读的同一纸面索引见 public_controls.index.json。

共同原则：具体正整数位宽 w、signedness、guard、clock/reset、采样 phase 及支持语言子集必须先独立固定；不从未来 C outcomes 选有利控制或 profile。合成公开控制不是 DUT fault／RTL coverage。形式向量若缩宽，所选 bit 必须真实存在，不补零。无激活不能给义务通过 credit。

## QC00 · 激活的恒真断言

- 目的：检验工具能保留已知真且确实激活的基线。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：POSITIVE。
- 人工预期：在独立固定的有界范围内无报警，激活可观察。
- 需独立确认：具体激活区间、初态／复位屏蔽和预期需独立标签确认。
- 验收／停止：缺少激活证据、phase 不明或出现未解释报警则停止；不把有界无报警称全局正确。
- 不支持范围：不覆盖真实协议、任意状态或 128 周期完成性。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC01 · 复位后的故意恒假断言

- 目的：检验已知负控制的选定报警和传输链。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：NEGATIVE。
- 人工预期：在已声明复位释放和激活前提满足后，应能保留故意错误的区别。
- 需独立确认：具体何种样本有资格激活和负标签须独立确认，本文不指定逐周期刺激。
- 验收／停止：漏掉该区别、借延迟报告时刻替代选定样本或边界不明则停止。
- 不支持范围：这是假断言控制，不是真 DUT 故障或候选误报率结论。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC02 · 显式位宽与赋值截断边界

- 目的：检验声明宽度和截断位置不被转换丢失。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：每个运算位置和赋值结果的 w 先固定；中间宽度／截断位置分开声明；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：POSITIVE。
- 人工预期：仅在相同显式宽度／赋值上下文下比较拟议关系。
- 需独立确认：具体关系、允许算子、边界数值及期望需独立确认；未证明任何新重写。
- 验收／停止：上下文隐式扩宽、截断位置漂移或支持类不一致则停止。
- 不支持范围：不推广至 unsized literal、混合符号性、四态或顺序状态。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC03 · 位宽／截断关系的故意扰动

- 目的：检验工具不会吞掉原本可区分的边界差异。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：沿用 QC02 同一固定宽度和上下文，仅纸面指定一个边界差异；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：NEGATIVE。
- 人工预期：独立选择的非等价扰动应被保留，不能因归一化而抹去。
- 需独立确认：扰动是否在所选定义域确实非等价、是否存在可区分情形须独立确认。
- 验收／停止：无区别却宣称负控制通过、悄悄扩大定义域或转移 counter 命中则停止。
- 不支持范围：不生成 bit 数据，不认定实际可达性或真实 DUT fault。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC04 · 显式 signedness／cast 边界

- 目的：检验有符号解释和转换上下文的保留。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：分别声明每个操作数、比较／运算结果及 cast 前后类型；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：POSITIVE。
- 人工预期：只比较已经独立声明支持的同语义关系。
- 需独立确认：允许 cast、符号扩展／零扩展及预期关系由独立语义标签确认。
- 验收／停止：类型被省略或支持算子产生未解释差异则停止；不支持则留 UNKNOWN。
- 不支持范围：不自动涵盖所有语言 cast 或 mixed-width 表达式。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC05 · 故意混淆 signed／unsigned

- 目的：检验不安全的类型替换不会被当等价。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：明确哪一处解释被纸面替换，其余上下文保持相同；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：NEGATIVE。
- 人工预期：选择独立确认可区分的解释差异；应保留区别或拒绝不支持运算。
- 需独立确认：区别存在的定义域／比较关系需独立标签；不从候选结果选例。
- 验收／停止：错误合并、补类型使结果有利或负标签无依据则停止。
- 不支持范围：不是所有 cast 替换都非等价；没有具体数据或已运行结论。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC06 · 完整 activation guard＋组合关系

- 目的：检验 E-graph/前端不丢 guard 与事件上下文。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：POSITIVE。
- 人工预期：拟议关系只有在完整 guard、同 clock/reset/phase 及已知值域内才比较。
- 需独立确认：guard 和关系的允许定义域、是否激活及独立期望须先确认。
- 验收／停止：剥离 guard、跨状态／事件比较或把等价类当覆盖命中则停止。
- 不支持范围：二态组合检查不证明四态、时序或复位正确性。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC07 · 永不激活／空泛 guard

- 目的：检验 PASS 与义务真正被检查的区别。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：纸面设定本控制在声明范围不激活；实际激活／cover 证据尚未创建；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：INELIGIBLE。
- 人工预期：即使 native 产生无报警／证明状态，也不能获得有效性或完成性 credit。
- 需独立确认：不激活范围、cover 含义与 ineligible 标签需独立确认。
- 验收／停止：把未达到 cover 当不可达证明，或把空泛 PASS 当义务通过则停止。
- 不支持范围：不声称全状态不可达，也不改写任何 native 原始状态。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC08 · 明确 pre/post 的公开采样合同

- 目的：检验同一个选定观察点在不同表示中的绑定。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：先指定抽象 pre 或 post 的含义及因果边界；不提供时钟波形或 rows。
- 拟议类别：POSITIVE。
- 人工预期：所选观察、原始链和人工合同必须指向同一 phase／事件。
- 需独立确认：具体接口、边沿语义、可比较输出范围须独立标签确认。
- 验收／停止：借另一 phase 的相等值冒充所选样本，或边界不明确则停止。
- 不支持范围：不由较早 reference 前缀确认当前 selected pre。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC09 · 故意的一边沿／phase 偏移

- 目的：检验时序不匹配不会被容忍为正确证据。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：在 QC08 的纸面合同中仅改变观察边界；不产生实际时间序列。
- 拟议类别：NEGATIVE。
- 人工预期：故意偏移必须作为完整性不匹配保留，不能移到有利样本。
- 需独立确认：确认扰动确实改变应绑定边界，而不是无区别的重命名。
- 验收／停止：静默对齐、重采样补造或把偏移归因为 DUT 故障则停止。
- 不支持范围：不评价任意协议的时序真值，不生成新的错误轨迹。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC10 · reset 断言／释放与初态上下文

- 目的：检验各层对复位合同的解释一致。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：显式极性、同步／异步、初态、assert/release 与 clock 的关系，具体值未创建；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：POSITIVE。
- 人工预期：只在同一独立合同中比较预期初始化和观察资格。
- 需独立确认：屏蔽规则、边沿顺序与期望状态由独立标签确认。
- 验收／停止：隐藏初态假设、跨 reset 等价化或未解释差异则停止。
- 不支持范围：不宣布真实 DUT 全复位语义或任意 CDC 正确。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC11 · 故意错置 reset／初态／clock

- 目的：检验上下文改变不会被当作同一检查。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：仅纸面指定一个复位／初态／clock 合同区别，其余绑定不变；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：NEGATIVE。
- 人工预期：保留合同不一致，或明确标为不支持。
- 需独立确认：区别与负标签需要独立确认；不以 C 结果决定偏移。
- 验收／停止：错误接受为同合同、修正标签掩盖区别则停止。
- 不支持范围：没有 reset 波形、RTL 或实测状态。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC12 · literal X→二态 anyseq

- 目的：界定已经发现的形式表示风险类别。
- 前提：language：四态源语义与二态模型必须分开；不声称 literal X 等于 nondeterministic known bit；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：UNKNOWN_OR_UNSUPPORTED。
- 人工预期：未知检测与 unconstrained 二态值不可直接声明等价，原始事实分层保留。
- 需独立确认：独立确认具体转换是否发生、支持范围与未知标签；此处没有新源／模型。
- 验收／停止：若把 X 补 0、把 anyseq 当原样四态 X 或泛化为所有 74 条根因则停止。
- 不支持范围：不重新评判旧 native 状态，不证明四态等价或共同根因。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC13 · case equality／未知检测

- 目的：界定四态谓词的资格边界。
- 前提：language：四态 equality/unknown 检测要有独立语义合同；只列概念，不写 SV 表达式；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：区分 edge 前 pre 与 edge 后 post，所选样本、reference 边界分别记录。
- 拟议类别：UNKNOWN_OR_UNSUPPORTED。
- 人工预期：前端不支持的语义不能拿 native PASS 代替四态正确性。
- 需独立确认：支持子集、X/Z 来源与预期人工分类须独立确认。
- 验收／停止：静默改成二态谓词、丢未知或省略不支持项则停止。
- 不支持范围：不覆盖所有四态运算，不创建新的 oracle 或规范判定。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC14 · 仅 final-post 的 trace_done 运输

- 目的：区分观测元数据与 DUT 时序／完成性。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：marker 仅最终 post 可见，不是 DUT 输入，也不新增 clock。
- 拟议类别：POSITIVE_FOR_TRANSPORT_ONLY。
- 人工预期：纸面接口应保留相同 DUT 输入／边沿数量与 marker 可见性边界。
- 需独立确认：final 的定义、transport 字段和观察资格需独立确认。
- 验收／停止：marker 提前可见、添加 clock／改 DUT 输入或直接宣称完成性通过则停止。
- 不支持范围：只定义运输合同，不证明任何 128 周期义务。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## QC15 · trace_done=0 的短投影完成性

- 目的：防止有限 safety 投影／空泛状态升级为完成性证明。
- 前提：language：未来受限 SystemVerilog／形式模型语义，具体源未创建；本文仅自然语言定义；width：符号 w 为明确正整数；操作数、结果和采样向量宽度须先独立固定，本文不生成位型；signedness：所有操作数及转换显式声明；不能由数值或表达式外观猜测；guard：完整激活条件与来源保留；对空泛 guard 不给有效性 credit；clock_reset：先声明同一 clock/edge/reset/初态及释放合同，不跨时域或复位上下文等价化；phase：明确是 trace_done 不激活的短投影；depth8 只是未来提案帽，不是本轮检查。
- 拟议类别：INELIGIBLE_FOR_COMPLETION。
- 人工预期：保留 native mode/status，但不给 128 周期完成性 credit。
- 需独立确认：义务激活条件、有限截止与 ineligible 分类须独立确认。
- 验收／停止：由 depth8／无 cover／空泛 prove 推出 128 周期通过则停止。
- 不支持范围：不声明完成性、一般 monitor soundness 或新的 liveness 结论。
- 状态：actual_result=null；source_status=waveform_status=independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。

## 资格与权限边界

本轮复核只能检查纸面一致性，不能认定这些控制已资格通过。未来 G1 的一 profile、32 native jobs、depth8 等资源帽仅来自 E05 未授权提案；本包不登记或执行该日程，也不外推 128 周期。创建源码、波形、fixture 或独立标签以及任何工具运行，均须另获相应范围／资源许可。X→anyseq 和未知检测不得声明等价；trace_done 运输不等于完成性。
