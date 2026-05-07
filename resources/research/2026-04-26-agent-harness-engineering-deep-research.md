---
title: "2026-04-26-agent-harness-engineering-deep-research"
tags:
  - area/resources
  - topic/agent-harness
  - topic/agent-systems
  - type/research-note
  - wiki/af
---
# Harness Engineering 深度研究报告

本文以所给知乎综述为线索，但证据尽量回到原始来源交叉验证。结论先行：截至 2026 年 4 月，Harness Engineering 还不是一个已经完全标准化的单一定义，而是一组正在快速收敛的工程实践。最狭义的版本强调“把复发错误工程化地消灭”，最广义的版本把它视为“模型之外的一切”，而最有操作性的工业定义，则是“围绕 agent 建立约束、上下文、工具、反馈与演化闭环的控制层”。你给出的定义——“通过将错误固化为规则，持续改造运行环境，使 Agent 长期不再犯同类错误”——与这些来源的公共交集高度一致。citeturn1view2turn5view2turn1view4turn25view0turn1view3

## 术语与边界重建

截至目前，公开语境里至少存在四种彼此相关但重心不同的定义。最早公开把这套做法命名为 harness engineering 的是 entity["people","Mitchell Hashimoto","hashicorp cofounder"]，他的定义非常窄：每当 agent 犯错，就花时间工程化一个方案，让它不要再犯同样的错。entity["company","Anthropic","ai company"] 的工程文则把 *agent harness* 和 *evaluation harness* 明确区分开：前者让模型成为 agent，后者负责把任务、grader、trial、transcript 和结果统计串起来。entity["company","LangChain","ai tooling company"] 给出的是最宽边界：**Agent = Model + Harness**，如果某部分不是模型，它原则上都属于 harness。entity["people","Martin Fowler","software author"] 在 entity["company","Thoughtworks","technology consultancy"] 的语境里又把它收窄为一种“guides + sensors”的治理系统，用 feedforward 和 feedback 来建立对 coding agent 的信任。citeturn1view2turn5view2turn1view4turn10view2turn25view0

因此，研究这个主题时，最重要的不是追问“唯一正确的定义”，而是先分清语义层级。**狭义的 Harness Engineering** 指“错误驱动的规则化演化”；**中义的 harness** 指“让模型成为 agent 的控制层”；**广义的 harness** 指“模型之外的所有工作系统”；**评测语境中的 harness** 则专指跑 eval 的基础设施。把这几层混在一起，讨论一定会乱。citeturn1view2turn5view2turn1view4turn12view0

和它最容易混淆的，是 prompt engineering 与 context engineering。entity["company","OpenAI","ai company"] 的官方指南把 prompt engineering 定义为“为模型写有效指令”；Anthropic 把 context engineering 定义为“在推理时策展和维护最优 tokens 集合”的策略；到了 harness engineering，重心已经不再是“写什么指令”或“塞什么信息”，而是“这个系统怎样运行、怎样约束、怎样反馈、怎样复现、怎样随着失败持续被改写”。简言之：**prompt 是写法，context 是配餐，harness 是制度与控制面。** citeturn26view1turn26view0turn5view2turn19search3

如果把这种差异翻译成工程类比，prompt 更像一句操作说明，context 更像工作记忆的装载策略，而 harness 更像把“调速器、操作系统和 CI 门禁”叠在一起的控制层。这个类比并非原文逐字定义，而是基于几个公开共同点做出的工程推断：Fowler 明确把 harness 写成 guides 与 sensors 的组合，并用 cybernetic governor 比喻它；Anthropic 反复把 harness 落在 agent loop、tools、tasks、transcripts 与 grading 基础设施上；OpenAI 则把人的主要工作重新定义为“设计环境、指定意图、构建反馈回路”。这些都指向同一个结论：**Harness 是控制系统，不是执行系统。** citeturn25view0turn25view3turn5view2turn1view3turn14view4

基于这些来源，本文采用的**最小定义**是：Harness Engineering 是一种围绕 agent 建立的外部控制层，它以**错误**为起点，把失败抽象成**规则**，把规则嵌回**环境**，再通过后续运行与评测完成持续**演化**。这一定义既保留了 Mitchell Hashimoto 那种“不要再犯同样错误”的狭义精神，也覆盖了 Anthropic、OpenAI、LangChain 与 Fowler 在公开实践里已经展开的系统结构。citeturn1view2turn5view2turn1view3turn1view4turn25view3

## 错误驱动闭环

在这个语境里，error 不是泛泛的“结果不够好”，而是**可以在 transcript、tool call、环境状态或评测结果中被定位的失败**。公开案例里至少能看到四类负样本：其一是任务级错误，例如 Anthropic 观察到 long-running agent 会尝试 one-shot 整个项目、在局部有进展后过早宣布完成；其二是机械/工具级错误，例如 hashline 实验证明很多模型并不是不会修 bug，而是败在 edit interface 的机械表达上；其三是状态级错误，例如跨 session 之后不知道之前做了什么、环境留下半成品；其四是规范与架构级错误，例如 OpenAI 所说的 drift、对仓库中既有坏模式的复制、越过依赖边界或错误理解数据形状。citeturn16view0turn16view2turn5view5turn14view0turn13view3

一个成熟的 harness 不会把这些失败只当成人工 review 的输入，而会把它们变成可积累的留痕对象。Anthropic 在 eval 语境里把 transcript 定义为一次 trial 的完整记录，包括输出、tool calls、reasoning、intermediate results 与其他交互；在 long-running harness 里又把 progress file、git log、feature list 和 init script 变成跨 session 的显式工件。LangChain 则把 trace、latency、token counts、cost 和 tool behavior 统一存进 LangSmith，用错误分析 agent 读取 traces，再反向修改 harness。换句话说，**记录失败** 在这里不是辅助动作，而是主工程对象。citeturn5view2turn16view1turn16view2turn11view0

从“记录”到“规则”，公开做法也很一致。Mitchell Hashimoto 的第一反应是更新 AGENTS.md 或增加程序化工具；OpenAI 的反应是把“缺了什么——工具、guardrails、documentation”回写到仓库里，并让专门的 linters、CI jobs 和 recurring cleanup 来机械地守住它；Anthropic 的反应是把 feature requirements 写成结构化 JSON，把“不要删改测试”“只改 passes 字段”“先验证后标完成”等行为约束嵌进环境；LangChain 的反应则是把 trace 中反复出现的失败模式，改写成 checklist middleware、loop detection middleware 和 self-verification 提示。这里真正发生的事，是把“经验”编译成“制度”。citeturn1view2turn14view4turn14view0turn16view1turn16view2turn11view0

从“规则”到“系统化防复发”，关键在验证环节。Anthropic 强调 eval 至少要有 task、trial、grader、outcome、transcript，并因为模型输出有方差而需要多次 trials；它也明确警告，没有 eval 的团队会陷入 reactive debugging。LangChain 在 harness-only 改进实验里用 held-out benchmark 与 trace analysis 反复迭代，并特别强调要防止针对个别任务过拟合。OpenAI 的做法则更偏产品工程：把文档一致性、依赖边界、局部 observability 与 recurring cleanup 变成常态化机制，让回归在进入更高代价阶段前被发现。于是，最稳固的闭环并不是简单的“错误→提示修补”，而是下面这条链路：citeturn5view2turn27search14turn11view0turn14view3turn25view4

错误  
↓ 观测与留痕（transcript / trace / progress file / git）  
↓ 归因与聚类  
↓ 规则化（AGENTS.md / tool schema / linter / structural test / context hook）  
↓ 回灌环境  
↓ 多 trial / held-out eval / shadow run 验证  
↓ 若仍失败，继续迭代

这也是你给出的定义里“错误、规则、环境、演化”四个词能够真正落地的地方：它们不是抽象名词，而是一个工程循环里的四个部件。citeturn1view2turn5view2turn11view0turn15view3turn29view0

## Harness 作为控制层的架构

把几家公开实践拼起来看，工业上最稳定的抽象不是“LLM + prompt”，而是 **intent/spec → harness control plane → model/agent runtime → environment → sensors/evals → harness update loop**。LangChain 说“if you’re not the model, you’re the harness”；Anthropic 说 agent harness 负责处理输入、编排 tool calls、返回结果；Fowler 说 harness 用 guides 与 sensors 做 feedforward 和 feedback；OpenAI 与 Microsoft 则把 docs、workspace、observability、cleanup 和 self-improvement loop 都明确纳入系统设计。由此可见，harness 最合理的位置是 **control plane**，不是 business logic，也不是底层算力。citeturn1view4turn5view2turn25view0turn1view3turn29view0

一个足够通用的控制层架构，可以写成下面这样。这不是某家公司逐字公开的图，而是基于多篇原始来源归纳出的工业公约数。citeturn1view3turn5view0turn25view0turn29view0turn17search0turn17search1

用户意图 / 产品规格  
↓  
任务展开器 / Planner  
↓  
Harness 控制层  
- Context Assembler：装配最小、高信号上下文  
- Rule Loader：加载 AGENTS、docs、skills、contracts  
- Tool & Sandbox Broker：暴露工具、隔离工作区、权限边界  
- Middleware / Hooks：pre-check、loop detection、policy checks  
- Sensors：tests、linters、browser、logs、metrics、review agents  
- Trace & Eval Recorder：记录 transcript、cost、latency、outcome  
- Replay / Diff：重放、对比、回归检查  
- Evolution Loop：把失败编译成下一版 harness  
↓  
模型 / Agent  
↓  
代码仓库 / Devbox / 应用 / 监控栈  
↺  
反馈回到 Harness

这里有四个边界特别值得分清。**Runtime** 是 agent loop 本身，负责调用模型和工具；**infrastructure** 是 devbox、sandbox、observability stack、CI 等支撑设施；**sandbox** 是权限与可见性的边界；**harness** 则把这三者连同规则、上下文装配、反馈传感器与演化逻辑一起组织成“可治理系统”。因此，说“harness = runtime”太窄，说“harness = infra”又太宽。更准确的说法是：**runtime、infra、sandbox 都可能是 harness 的组成部分，但 harness 的核心是控制与调节，而不是单独某个执行组件。** citeturn5view2turn17search0turn15view0turn29view0turn25view1

Fowler 对这个控制层给出了一个非常实用的细分：feedforward 与 feedback，外加 computational 与 inferential 两种控制。前者对应先验引导，后者对应后验纠偏；前者可由 AGENTS.md、skills、architecture docs 等承担，后者可由 linters、tests、log inspection、AI code review、LLM-as-judge 等承担；计算型控制更快、更确定，推断型控制更贵、也更不稳定。这个拆分非常重要，因为它解释了为什么 harness 不能只靠 prompt：**可扩展的控制层，最终必须有越来越多可机械执行的反馈传感器。** citeturn25view0turn25view1turn25view2turn25view4

Anthropic 对评测面的拆分也值得保留：agent harness 负责把模型变成 agent，evaluation harness 负责端到端跑 tasks、记录 trials、打分并汇总结果。前者是“运行时控制层”，后者是“验证与门禁层”。企业一旦把这两者混为一谈，就会出现两个典型误区：要么只造 eval，不解决 runtime failure；要么只堆 runtime，不建立 regression gate。citeturn5view2

## 真实案例与大厂实践

公开资料里，最完整、最能代表“大厂/大团队如何定义与使用 harness”的材料，当前集中在 OpenAI、Anthropic、Stripe、Microsoft 以及 LangChain 这几条线索上。它们并不提供统一术语，但都把核心问题落在同一件事上：**如何让 agent 在复杂环境里获得可控的自主性。** citeturn1view3turn5view0turn17search2turn29view0turn11view0

**OpenAI** 的 Codex 实验最强烈地说明：Harness 不是“配件”，而是主工程对象。他们从空仓库起步，在约五个月内构建并交付一个内部 beta，所有代码——应用逻辑、测试、CI、文档、observability 与内部工具——都由 Codex 写出；人的工作不再主要是手写代码，而是“设计环境、指定意图、建立反馈回路”。后续仓库又被改造成 agent-first 结构：短 AGENTS.md 只做目录，真实知识放在结构化 docs 中；UI、logs、metrics、traces 被接成 agent 可读的本地观测栈；架构边界通过 custom linters 与 structural tests 机械执行；随着 drift 增长，再通过 golden principles 与 recurring cleanup 做“垃圾回收”。这不是“模型突然学会写百万行代码”的故事，而是“团队把仓库、工具和反馈面工程化到足以支撑 agent”。citeturn1view3turn14view4turn13view1turn14view3turn14view0turn15view0turn13view3

**Anthropic** 的贡献，在于它把词汇、问题分解和长任务设计都公开写清楚了。它明确区分 agent harness 与 evaluation harness；又在 long-running harness 里证明，仅靠 compaction 不够，必须显式管理跨 context-window 的状态交接，所以引入 initializer agent、progress file、feature list JSON、init.sh 与 Git handoff；随后又在更进一步的 application-building harness 里引入 planner、generator、evaluator 三个角色，并用 contract 与可验证标准把 generator 的产出交给 evaluator 审核。这里最关键的认识是：**harness 不只是“给工具和记忆”，还必须决定任务如何分块、状态如何交接、完成标准如何外部化。** citeturn5view2turn5view0turn16view1turn16view2turn16view3turn16view4turn16view5

**entity["company","Stripe","payments company"]** 的公开材料虽然在正文抓取得不如 OpenAI/Anthropic 完整，但搜索摘要已经足够传递其设计重点：Minions 是 Stripe 自研 coding agents，每周合并超过一千个 pull requests，代码虽经人工 review，但从头到尾由 agents 编写；单次运行从与工程师同类的 isolated devbox 启动，devbox 预热后约 10 秒可用，并与生产资源和互联网隔离；同时 Toolshed 作为共享 capability layer，把新增工具一次性提供给多类 agent 系统。也就是说，Stripe 把 harness 的重心放在**标准化工作环境、严格隔离边界与统一能力中介层**上。它要解决的首先不是“如何提示模型”，而是“如何把 agent 放进一台合适、可并行、可约束、可扩展的机器里”。citeturn17search2turn17search0turn17search1

**entity["company","Microsoft","technology company"]** 的 Azure SRE Agent 进一步把 harness 从 coding 场景推广到运维调查场景，而且是明确使用了 harness engineering 这个术语。其核心设计包括：把 source code、runbooks、query schema、past investigation notes 全部 materialize 成文件系统世界；用 context hooks 注入 connectors、repositories、knowledge map 与 resource topology；用 pruning 与 auto-compact 管理长会话预算；用 parallel subagents 并行探索多个假设；再让 agent 通过日常监控任务为自己的错误聚类、定位根因并提交修复 PR。团队报告，两周内相关错误被压下超过 80%。这几乎是“agent 调查自己并修自己”的教科书式 harness outer loop。citeturn29view0

**LangChain** 提供的是最清楚的“工具厂商视角”。他们在固定模型 `gpt-5.2-codex` 不变的条件下，仅通过改 harness，把 Terminal Bench 2.0 成绩从 52.8 提到 66.5，从榜单 Top 30 外提升到 Top 5；方法不是换模型，而是 trace-driven 改进：读取 LangSmith traces、找错误模式、加 self-verification、加 pre-completion checklist、加 local context middleware、加 loop detection middleware、再分配 reasoning budget。这里的信息量很大：**今天很多 agent 的上限，先由 harness 设定，再由模型补足。** citeturn11view0

而 **hashline** 实验则提供了一个更纯净的隔离实验：同一模型、同类任务，只改 edit interface，16 个模型里多数都明显提升；其中一个模型从 6.7% 提高到 68.3%，另一个模型输出 token 降低 61%。这个案例非常重要，因为它证明“工具接口不是 plumbing，而是负载能力极强的 harness 设计变量”。许多所谓“模型不行”的失败，其实是“模型无法可靠表达改动”。citeturn5view5

把这些案例放在一起，能得到一个非常稳定的大厂式判断：**Harness 不是单个组件，而是一整套针对 agent 运行世界的工程安排——环境、上下文、边界、工具契约、反馈传感器、回归机制与长期清理流程。** 公开实践里，不同团队命名和切分不一样，但“如何让 agent 在你真正的世界里不反复犯错”才是共同主线。citeturn1view3turn5view0turn17search0turn29view0turn11view0

## 与传统 Test Harness 的关系

传统软件工程里的 test harness 定义并不神秘。ISTQB 把它定义成“执行测试所需的 drivers 与 test doubles 的集合”；IBM 的描述则更具体：它准备输入、启动待测代码、捕获输出，并在受控环境里完成调试或验证。也就是说，传统 test harness 的本质一直都是**把待测系统包进一个可控、可观测、可重复的执行壳层里**。citeturn23search2turn23search0turn23search3

AI harness 与它并不是断裂关系，而是一次扩展。没变的东西有四个：第一，仍然需要受控环境；第二，仍然需要输入、执行、捕获、比较这一基本骨架；第三，仍然需要把真实系统替换成更可控的依赖边界；第四，仍然需要让失败可重现。变掉的东西也有四个：第一，输出从确定性变成带方差的多 trial 问题；第二，单次函数调用变成多 turn、会改写环境的 agent loop；第三，传统 stubs/drivers 变成 tools/MCP/sandboxes/skills/progress artifacts；第四，过去 harness 主要为了“执行测试”，现在 harness 还要承担“把未来错误提前挪走”的演化责任。Anthropic 明确区分 evaluation harness 与 agent harness，正好把这层继承关系讲清楚：AI 时代不是没有 test harness 了，而是又多了一层让模型能在环境中持续行动的运行时 harness。citeturn5view2turn23search2turn23search0turn25view0

如果非要一句话概括两者关系，那么最准确的说法是：**AI Harness 是 Test Harness 的外推——从“测试一个组件”扩展到“治理一个会行动、会遗忘、会误用工具、会污染环境的非确定性执行体”。** citeturn23search2turn5view2turn25view2

## 长期演化风险与研究前沿

第一类风险是**规则膨胀与规则冲突**。OpenAI 已经公开写出，“one big AGENTS.md”会失败，因为上下文稀缺、过量指导会变成无指导、单体规则文件会迅速腐烂，而且难以机械验证。Thoughtworks 也专门提醒，context/harness 配置很容易在复制粘贴中产生重复与矛盾，让团队误以为是模型无能，实际上是系统给了混乱信号。这意味着 harness 做到后面，最大问题往往不是“规则不够”，而是“规则太多而且彼此不兼容”。citeturn13view1turn14view3turn26view2

第二类风险是**环境熵增与技术债放大**。OpenAI 明确承认，Codex 会复制仓库里已经存在的模式，包括不均匀或次优模式；团队一度每周五要花 20% 的时间清理 “AI slop”，后来才把 golden principles 与 recurring cleanup 写进系统。Microsoft 也在 agent memory 公开文里承认，Markdown memory 的 staleness 仍未解决：当两个会话写出互相冲突的总结或系统行为变化后，旧条目会开始误导模型。换句话说，harness 不是建完就稳；**它本身也会腐化，需要被治理。** citeturn13view3turn29view0

第三类风险是**上下文污染、资源噪声与成本失真**。Anthropic 反复强调 context 是有限资源，context engineering 的目标是用最小的高信号 tokens 达到所需行为；在 long-running harness 里，他们还指出 compaction 不一定能解决“context anxiety”，有时必须 context reset。另一篇 Anthropic 研究则提醒，agentic coding eval 的基础设施配置本身就能让结果摆动数个百分点，有时甚至超过 leaderboard 间的差距。再加上实际长任务很贵——Anthropic 一次更新后的 long-running harness run 报告大约 4 小时、124 美元——所以企业如果不把预算、sandbox 资源、token policy、timeout policy 当成 harness 一部分，就会误把基础设施差异当成“模型能力差异”。citeturn26view0turn16view3turn27search0turn5view1

第四类风险是**评测门槛提高**。Anthropic 在 eval 指南里已经明确指出，没有 eval 的团队会在用户抱怨后才发现退化，且无法区分真实 regression 与噪声；LangChain 则强调 trace-driven 改进如果不做 held-out 验证，很容易只是在榜单上 hill-climb 而非提高泛化性能。这意味着 harness 变强之后，评测也必须同步升级：单次 demo 成功不再说明问题，必须看多次 trial、真实 outcome、transcript、held-out set 和长期回归轨迹。citeturn27search14turn5view2turn11view0

研究前沿也已经出现。学术上，**Natural-Language Agent Harnesses** 尝试把原本埋在控制代码里的 harness 行为外化为可编辑、可移植的自然语言工件；**Meta-Harness** 更进一步，把“改进 harness”本身自动化，让 proposer agent 读取先前 harness 的源代码、execution traces 与分数，再搜索新的 harness 代码。后者在 TerminalBench-2 上已经报告超过手工基线的结果。也就是说，下一阶段的竞争，不只是“谁会设计 harness”，还会变成“谁能让 harness 自己进化”。citeturn12view0turn12view1

## 企业级落地蓝图

如果把以上公开实践抽象成可落地企业方案，最合理的单元不是一个“大而全 agent 平台”，而是四个耦合但职责清晰的子系统：**错误收集系统、规则编译系统、Harness 版本系统、Agent 运行环境**。这四个部分，分别对应公开实践里的 traces/progress files、AGENTS/docs/linters、eval/held-out gating，以及 devbox/sandbox/tools/observability。citeturn5view2turn16view2turn14view3turn17search0turn29view0

第一，**错误收集系统** 应该把 transcript、tool calls、环境状态、测试结果、UI 证据、logs/metrics/traces 全部落盘，形成一个 Failure Lake。它不是日志仓库的别名，而是按“任务—trial—failure class—cost—artifact”组织的 agent 失败数据库。Anthropic 的 transcript 定义、OpenAI 的 progress/decision logs、LangChain 的 traces、Microsoft 的 daily failure clustering，都是这个子系统的公开原型。citeturn5view2turn15view0turn11view0turn29view0

第二，**规则编译系统** 要把失败变成可执行约束。输入是 clustered failures 与 raw evidence，输出应该是四类工件：规则文件，工具 schema 变更，middleware/hooks 变更，以及新的 deterministic checks。这里尽量遵循一个顺序：能靠工具接口修的，不先写提示；能靠 lint/test/structure 修的，不先依赖 LLM 解释；只有当 deterministic 方式覆盖不了时，才上 inferential reviewer。这个顺序来自 Fowler 的 computational vs inferential 区分，也对应 OpenAI、Anthropic 和 LangChain 的实践。citeturn25view1turn14view0turn16view1turn11view0

第三，**Harness 版本系统** 要像管理 API 或 schema 一样管理 harness。本质上，AGENTS.md、docs、tool specs、middleware、eval suites、sandbox policy 都应是 versioned artifacts。每次修改 harness，都要触发三类验证：回归集、held-out 集和必要的影子流量验证。Anthropic 对多 trial 和 grader 的强调、LangChain 对 overfitting 的警惕、OpenAI 对 docs freshness 与 recurring cleanup 的机械验证，都说明 harness 不是“写完就生效”的配置，而是需要发布、比较和回滚的版本化对象。citeturn5view2turn11view0turn14view3

第四，**Agent 运行环境** 应坚持“受控但高能力”的原则。经验上最好的公开共识不是把 agent 关进一个几乎不能行动的笼子，而是给它一个高能力、边界清晰的世界：文件系统工作区、最小而高信号的工具集、可搜索的文档层、可查询的 observability 层、可中断和可重放的会话机制，以及严格的权限边界。Stripe 的 devbox 与 Toolshed、Microsoft 的 filesystem world、OpenAI 的 local observability stack，都是这一原则的不同实现。citeturn17search0turn17search1turn29view0turn15view0

一个可行的企业级控制图，可以写成这样：

需求 / 缺陷 / 事故  
↓  
Task Builder  
↓  
Harness Registry  
- rules  
- docs  
- tool contracts  
- middleware  
- eval suites  
↓  
Runtime Plane  
- sandbox / devbox  
- agent loop  
- observability access  
- permissions  
↓  
Outcome + Traces  
↓  
Failure Lake  
↓  
Rule Compiler  
↓  
A/B / held-out / shadow gate  
↓  
发布下一版 Harness

一个最小可运行的仓库结构，可以从下面这样的骨架开始：

```bash
/harness
  /tasks
  /rules
  /docs
  /tools
  /middleware
  /eval
  /traces
  /replay
  /registry
```

而最小的 outer loop，不需要很复杂，关键是把“失败 → 规则 → 验证 → 发布”串起来：

```python
task_run = runtime.execute(task, harness_version)

artifacts = recorder.capture(task_run)

failures = analyzer.cluster(artifacts)

candidate_rules = compiler.propose(failures)

candidate_harness = registry.patch(harness_version, candidate_rules)

report = evaluator.run_suite(candidate_harness, suites=["regression", "heldout"])

if report.pass_gate:
    registry.promote(candidate_harness)
else:
    registry.reject(candidate_harness)
```

对大多数企业来说，真正的 MVP 不是多 agent 编排，而是下面这五件事先做对：一个 progress artifact，一个最小 docs map，一个 deterministic test gate，一个 trace store，一个 harness version history。只有当这五件事稳定后，再去扩展 evaluator agent、shadow harness、自动规则生成，才不会陷入“越自动越失控”。这一点，几乎被所有公开案例共同印证。citeturn1view3turn5view0turn11view0turn17search0turn29view0

最后，把整篇研究压缩成几个最重要的洞察：

- **Harness Engineering 不是“把 prompt 写得更聪明”，而是“把系统改得更不容易再错”。** 这条线最直接来自 Mitchell Hashimoto 的原始命名，也被 OpenAI、Anthropic、Microsoft 的实践外化了。citeturn1view2turn14view4turn29view0
- **今天很多 agent 的瓶颈，不先在模型，而先在 harness。** Hashline 的工具接口实验、LangChain 的 harness-only 提升、OpenAI 的环境设计实验都指向这一点。citeturn5view5turn11view0turn1view3
- **真正可扩展的单位不是“一个神奇 agent”，而是“一个可复用的错误驱动闭环”。** transcript、progress files、linters、held-out evals、cleanup loops，都是这个闭环的不同视角。citeturn5view2turn16view2turn14view3turn25view3
- **工程师角色确实在上移：从 coder 变成 system designer。** OpenAI 几乎是直白地这么写，Fowler 和 Microsoft 也给出了相同方向的公开证据。citeturn1view3turn25view3turn29view0

最稳妥的研究结论因此不是“Harness Engineering 是某个新瓶装旧酒的 buzzword”，而是：它正在把 agent 开发重新拉回软件工程的核心问题——边界、可观测性、回归门禁、状态管理、架构约束和持续清理。Prompt 依然重要，context 依然重要，但一旦系统开始长时间运行、会改写外部世界、会读取工具并反复暴露同类失败，决定成败的就不再是某一句提示词，而是你是否拥有一个足够好的 harness。citeturn26view1turn26view0turn1view3turn5view0turn25view0