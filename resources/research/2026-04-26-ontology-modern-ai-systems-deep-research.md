---
title: "Ontology在现代AI系统中的演化与应用"
type: research
status: done
source_lead:
topics:
  - ontology
  - agent-systems
  - data-management
promotes_to:
  - areas/knowledge/topics/ontology
tags:
  - area/resources
  - topic/ontology
  - topic/agent-systems
  - topic/data-management
  - type/research-note
  - wiki/af
---
# Ontology在现代AI系统中的演化与应用

## 引言

今天重新讨论 Ontology，不是因为“语义建模”这个词突然变新了，而是因为企业级 AI 已经从“生成答案”走向“参与决策与执行”。entity["company","OpenAI","ai lab"] 与 entity["company","Anthropic","ai safety company"] 的官方文档都把当代 agent 描述为能够规划、调用工具、保有状态并执行多步任务的应用；而 entity["company","Palantir Technologies","data software company"] 则进一步把 Ontology 定义为同时整合数据、逻辑、动作与安全的系统，使人和 AI agent 都能围绕同一套“业务世界”协作。换句话说，瓶颈开始从“模型会不会思考”转向“系统有没有稳定、可控、可执行的世界表示层”。citeturn29view0turn29view3turn29view1turn22view0turn22view1

更重要的是，这个方向已经不再只是单一厂商叙事。entity["company","dbt Labs","analytics company"] 的 Semantic Layer 文档把机器可读的指标与实体关系视作 AI 查询的结构化“ontology”；entity["company","Snowflake","cloud data company"] 已把 semantic views 与 “agent context layer” 作为 AI-ready 数据架构的一部分；Open Semantic Interchange 甚至试图把语义层对象标准化为跨工具可交换的格式。这说明“把语义、治理与 agent 接口合并”为一个中间层，正在从 Palantir 式的产品能力，演变成整个行业的架构方向。citeturn16search3turn16search7turn16search2turn16search6turn16search14turn16search16

## 从存在论到机器可执行语义

在哲学传统里，ontology 讨论的是“世界里究竟有什么”以及这些存在属于哪些基本范畴。围绕 entity["people","亚里士多德","greek philosopher"] 的 categories 传统，Stanford Encyclopedia of Philosophy 把 category system 概括为对“最高种类”的盘点；更近的 Stanford 条目则指出，信息系统中的 ontology 与哲学共享“范畴研究”的内核，但目标转向以形式语法与语义把这些范畴记录、交换和推理。citeturn36search2turn36search8turn36search0

进入计算机科学之后，Gruber 的经典定义把 ontology 描述为“an explicit specification of a conceptualization”，重点不在数据库表长什么样，而在某个领域中哪些对象、关系与约束被共同承认并可被机器处理。随后，entity["organization","W3C","web standards body"] 把 RDF/OWL 体系标准化：OWL 2 明确支持 classes、properties、individuals 与 data values，并为形式语义、推理 profile 与 RDF 交换提供统一基础；其中 OWL 2 QL 甚至专门强调可以借助标准关系数据库技术回答查询，说明“本体”从来不等于“必须使用图数据库”。citeturn27view0turn26view0turn26view1

但语义网时代的 ontology 主要仍是**描述性**基础设施。它的核心价值在于共享词汇、形式约束与可推理语义，而不是把企业动作、权限、写回与工作流一起编码进去。学界对这一阶段的总结也很清楚：ontology engineering 已广泛应用于生物医学、金融、工程与法律等领域，但它仍然是困难过程，维护、演化、版本管理与跨团队一致性依然是长期难题。citeturn26view5turn27view1turn27view4

下表综合了经典知识工程文献、entity["company","Google","search company"] 官方 Knowledge Graph 文档，以及数据库/本体比较研究，可作为 CTO 判断三个名词边界的实用框架。citeturn27view0turn26view4turn30view0turn30view1turn30view4

| 维度 | Ontology | Knowledge Graph | Schema |
|---|---|---|---|
| 核心目标 | 明确领域概念、关系与约束的**含义** | 存储与连接实体事实、关系与实例网络 | 定义数据如何被**存储与组织** |
| 主要关注点 | 语义、约束、可共享词汇、推理 | 实体、边、事实、查询与发现 | 表、列、类型、完整性 |
| 抽象层级 | 通常高于实例层 | 通常实例更重，也可受 ontology 约束 | 系统/应用特定 |
| 可复用性 | 强，倾向跨应用共享 | 中等，常随场景变化 | 弱到中等，常绑定单系统 |
| 与 AI/Agent 的关系 | 提供世界词汇与约束 | 提供上下文图与事实网络 | 提供底层结构，但语义贫乏 |

对企业架构来说，最关键的判断不是“谁更高级”，而是谁承担哪一层责任。Schema 解决“数据是否能放进去”；Knowledge Graph 解决“事实能否关联与查询”；Ontology 解决“这些事实在业务上到底意味着什么，以及哪些推理和约束是合法的”。Palantir 的创新点，正是把最后一层继续推进到了“哪些动作可以执行、由谁执行、如何回写、如何审计”。citeturn26view4turn30view2turn30view4turn22view0

## Operational Ontology 的分水岭

Palantir 官方文档对 Foundry Ontology 的定义非常明确：它是 organization 的 operational layer，坐落在 datasets、virtual tables、models 之上，把工厂、设备、订单、财务交易等数字资产连接到现实世界对象；在很多场景中，它同时被视为组织的 digital twin。其公开基本构成包含 object types、properties、link types 与 action types。citeturn22view2turn1search0turn1search5

Palantir 文档还反复区分两类元素：semantic elements 是 objects、properties、links；kinetic elements 是 actions、functions、dynamic security。更上层的《The Ontology system》则把整个体系概括为 data、logic、action、security 的四元整合，并明确写出：这件事不能靠一个“thin semantic layer”或单体系统完成，而需要 Language、Engine、Toolchain 三部分协同。这里有一个重要细节：Palantir 并没有公开固化一套“semantic / kinetic / dynamic 三层架构”的完整官方分层术语，但它确实公开使用 semantic、kinetic、dynamic security，并在架构层面将之上升为四元一体的 operational system。citeturn22view0turn22view2turn21search6

“Ontology 是组织的 API” 这句话，不应被理解成营销口号，而应被理解成一种接口重写：同一套业务对象与动作，通过 GUI、API、自然语言界面、OSDK 和 agent tools 以统一语义暴露给不同消费者。Palantir 的社区设计文档直接把 Ontology称为“API of your organization”；Palantir 博客又进一步把 GUI、API、NLI 视为同一 ontology language 的不同表达方式；OSDK 则把这套对象、动作与权限直接生成为开发语言里的类型安全 SDK。citeturn34view0turn33view0turn32view0

下表是对“传统 ontology”与“Palantir operational ontology”的关键差异提炼。该表是基于 W3C、Gruber 与 Palantir 官方架构/产品文档的综合判断。citeturn26view0turn27view0turn22view0turn23view0turn25view0turn32view0

| 维度 | 传统计算机本体 | Palantir Operational Ontology |
|---|---|---|
| 核心使命 | 描述与共享领域知识 | 描述并**驱动**企业决策与执行 |
| 基本单位 | 类、属性、个体、约束 | 对象、属性、链接、动作、函数、安全 |
| 默认方向 | 读多写少，偏推理 | 读写闭环，偏运营 |
| 执行能力 | 通常外置在应用层 | action、automation、workflow 内生 |
| 安全模型 | 常外置于系统/IAM | object/action/property/security policy 内嵌 |
| 开发接口 | 以标注、规则、查询为主 | 以 SDK、tool、workflow、agent 为主 |
| 审计与演化 | 需要外部工程补齐 | action log、audit log、schema migration 内建 |

因此，Palantir Ontology 与传统 OWL/RDF 最大的本质差异，不是“它更像 graph”或“它更像 semantic layer”，而是它把**业务动作**、**权限边界**、**可审计写回**、**AI 工具暴露**纳入了本体定义的中心。传统 ontology 主要回答“世界是什么”；Palantir 的 ontology 还回答“这个世界允许做什么、谁能做、做完如何留下系统状态”。从企业软件视角看，它已经不是知识表示件，而是业务操作系统的中心语义内核。citeturn26view0turn22view0turn23view0turn23view2turn25view0

## Action Layer 如何把语义变成执行

Palantir 对 Action 的定义极其关键：Action 是一个 single transaction，用来一次性改变一个或多个对象的属性、链接乃至对象本身，并可附带 side effect behaviors。官方示例强调，用户不必围绕某个孤立字段手改数据，而是围绕一个完整业务动作执行变更，比如分配员工、通知上下游、验证授权身份。citeturn23view0

这使 Action 与 Function、Service 形成了清晰分工。Function 是可复用的实时或近实时计算逻辑，能够读取对象、遍历链接，甚至执行 ontology edits；Action 则是**业务承诺**的类型化封装，除了实际改写，还自带参数、校验、权限、日志、副作用与用户交互边界；而底层 Service 仍然存在于微服务/数据连接/对象后端层，用于支撑查询、索引、CDC、通知和第三方系统交互。换言之，Function 更像“算什么”，Action 更像“批准并执行什么”，Service 更像“靠什么底层能力执行”。citeturn4search4turn4search20turn22view2turn23view0

对 CTO 而言，Action 的设计原则比定义本身更重要。Palantir 官方反模式文档明确反对 “action sprawl”，主张把 Action 设计成凝聚的 business operation，而不是一堆单属性按钮；社区设计指南也强调 Object Types 和 Actions 要映射自然语言业务概念。至于“幂等性”，Palantir 并未把它作为公开术语写成官方设计原则，但考虑到 Action 具有事务性、可被 agent/automation 调用、还可能触发 webhook 或外部写回，工程上应尽量把 Action 设计成支持重放保护、稳定主键与去重语义的提交单元，否则一旦跨系统重试，很容易产生重复副作用。这一点是基于其事务、side effects 与 action log 机制作出的工程推论。citeturn23view1turn34view0turn14search23turn14search6turn25view0

Palantir 进一步把 Action 接入 Workflow。Automate 可以在满足条件时自动运行 actions；AIP Chatbot/AIP Analyst 也能把 actions 作为 tool 使用；而 action log 会把每一次 action submission 建模成 object type，与被编辑对象建立链接，从而把“谁在何时基于何种上下文做了什么”直接变为可分析数据。换句话说，Action 不是“包装 API”，而是把业务流程本身提升为可组合、可观测、可审计的语义对象。citeturn2search1turn24view0turn24view2turn25view0turn25view3

另外，Palantir 对一致性的处理值得注意。官方文档说明，在应用 Action 过程中，系统会加载对象定义和对象实例的相应版本，以保证 transactionality；而对象同时接受源数据更新与用户 edits 时，又提供 “user edits always win” 或 “most recent value” 等冲突解决策略。这意味着 Action Layer 并非 UI 层快捷按钮，而是真正进入了状态机与一致性控制的范畴。citeturn14search6turn13search10

## Ontology 与 AI Agent 的接口重写

如果用 agent 视角重述，Ontology 最接近的是**外部显式世界模型**，但它不是端到端学习出来的 latent world model，而是可治理、可查询、可执行的 enterprise world state。Palantir 自己把 Ontology 描述为 humans 和 AI agents 的 shared operational world；AIP Analyst 可以在 ontology 上自主搜索、创建 object sets、转换数据、执行函数与 actions；application state 则允许 agent 把对象集、字符串变量与用户当前选择显式纳入推理循环。这个意义上，Ontology 不只是“给 agent 一堆工具”，而是在给 agent 一个**有状态、带约束、可更新的业务环境**。citeturn22view0turn24view2turn24view1

下表是“tool/function calling”与“ontology 作为 agent 接口层”的工程差异总结，主要基于 OpenAI、Anthropic、MCP 与 Palantir 官方文档。citeturn29view0turn29view1turn29view2turn24view0turn24view1

| 维度 | Tool / Function Calling | Ontology 作为 Agent 接口层 |
|---|---|---|
| 暴露给模型的内容 | 函数名、参数 schema、描述 | 业务对象、关系、动作、权限、检索上下文、状态变量 |
| 模型能看到的世界 | 离散工具列表 | 结构化业务世界与允许的状态转换 |
| 状态归属 | 多由应用自行维护 | object sets、application state、context 内建 |
| 安全边界 | 主要靠外部编排与审批 | object/action/property/security policy 深度绑定 |
| 可解释性 | 取决于应用日志 | citations、session trace、action log、observability |
| 失败模式 | 工具选错、参数错、状态丢失 | 建模错误、权限过严/过松、动作语义失真 |

这种差异直接影响可解释性与可控性。Palantir 的 retrieval context 可以在每条消息上**确定性**运行；ontology/document context 能输出 citations；Get Session Trace API 能回放 chatbot 的执行步骤；AIP observability 还能把 agents、functions、actions、automations 统一纳入 tracing、logging 与 run history。相比之下，OpenAI、Anthropic 与 MCP 官方文档都承认：工具本身只是可调用能力，真正的 orchestration、approvals、state ownership 与 human-in-the-loop 需要应用方负责。Ontology 因而把原本散落在 agent framework 之外的“世界语义 + 权限 + 状态 + 审计”往中心收拢。citeturn23view5turn25view1turn25view2turn25view3turn29view0turn29view1turn29view2

从 Memory、State、Execution Layer 三个角度看，Ontology 的价值也更清楚。Memory 不再只是长上下文或向量检索，还包括对象、对象集、action log 与可复用的 workflow history；State 不只是一段 conversation memory，而是 application variables、selected object sets 与 object visibility；Execution 不只是“调一下函数”，而是执行 ontology action 并进入业务状态变更。Palantir 文档甚至已经让 AIP Analyst 支持 memories，说明其目标不是把 agent 作为即时问答器，而是作为持续运行于 operational graph 上的工作单元。citeturn24view1turn24view2turn25view0turn29view0turn5search6turn27view2

## 架构重写与最小可行实现

传统企业软件通常按“DB + Backend + API + Frontend”分层：数据先落到底层存储，再由后端汇聚领域逻辑，最后经 API 暴露给前端和其它系统。Palantir 的公开架构则在此之上插入一个居中的 Ontology system，把 data、logic、action、security 抽象成同一套对象语言，再由应用、自动化、agent、SDK 共同消费。OSDK 的措辞很直接：把 Foundry 当成 backend，用 ontology 的 query、writeback 与 governance 能加速应用开发；换句话说，backend 并没有消失，而是其相当一部分**领域语义与业务编排职责**被上移到了 ontology 层。citeturn22view0turn22view1turn22view2turn32view0

一个更贴近 CTO 决策的文字架构图如下。该图是对 Palantir 公开架构与通用 agent/tool 模式的综合归纳。citeturn22view0turn22view1turn29view0turn29view3

```text
传统架构
数据源 -> ETL/ELT -> DB/Warehouse -> Backend/Service -> API -> Frontend
                                          \
                                           -> Agent/LLM 通过 REST/SQL/工具间接操作

Ontology 驱动架构
数据源 / 模型 / 外部系统
        -> Ontology Layer
           (objects + properties + links + actions + logic + security)
        -> UI / Apps / Agent / Automation / SDK
        -> writeback / audit / observability / workflow lineage
```

因此，更稳妥的判断不是“Backend 会不会被替代”，而是“哪一部分 Backend 会被吞并”。我的结论是：**通用 CRUD、对象聚合、权限拼装、业务工具暴露、部分 workflow 编排，会被 ontology layer 显著吸收；但高性能计算、特殊协议适配、历史系统集成、外部写回连接器、模型运行时与底层服务编排，仍会继续存在于下层服务层。** Palantir 自己也把 Ontology 描述成 Language、Engine、Toolchain 与多种 backend service 的组合，而非单一神奇中台；这恰恰证明 ontology 驱动架构是对现有后端职责的重组，而不是把所有后端代码“消灭”。citeturn22view0turn22view2turn32view0turn33view0

如果要实现一个**最小 Ontology 系统**，工程上我建议从三层起步。第一，**数据层**优先采用关系库或对象存储加索引，而不是一开始就押注 graph DB；W3C 的 OWL 2 QL 本就支持借助关系数据库回答查询，而 Palantir 自身也用 object storage、Object Set Service 与 Ontology SQL 来提供高性能查询。第二，**执行层**必须有独立的 action engine，负责参数校验、事务、side effects、日志与回写，不应把“动作”退化回普通 RPC。第三，**AI 接入层**要把 object query、action invocation、retrieval context、application state 与 trace/citation 统一封装成 agent adapter，而不是把 LLM 直接暴露给底层 SQL/REST。citeturn26view0turn22view2turn35view5turn35view4turn23view0turn24view0turn24view1turn25view1turn25view2

性能上，Palantir 的文档也揭示了现实约束：Ontology 查询依赖多模态存储并服务 high-speed queries；Object APIs 往往比在 function context 内部自行遍历链接更快；OntoIogy SQL 直接作用于 object storage；而流式写入要受 Flink checkpoint 的 exactly-once 语义制约，默认 1 秒级检查点成为主要延迟来源，单 object type 的流式索引吞吐还有 2 MB/s 的上限，且部分流式场景不支持 partial-row update。对自建系统来说，这意味着“把一切做成实时图遍历”并不现实；应根据 latency、throughput、consistency 三角做分层设计。citeturn35view4turn13search2turn35view5turn35view3

Schema Evolution 是企业落地的难点，也是 operational ontology 区别于静态 schema 的核心战场。学界早就指出 ontology evolution 不是简单 schema evolution，因为 ontology 有显式语义、更多兼容维度与更复杂的版本管理需求。Palantir 的 OSv2 文档则把这一点工程化了：系统会自动检测 breaking schema changes，阻止直接保存，要求用户先定义 migration；保存后创建新的 schema version，并通过 replacement pipeline 更新索引，待新版本 fully hydrated 后再对外查询可见。这说明 operational ontology 的版本管理，必须同时覆盖语义兼容、数据迁移和运行时切换。citeturn30view5turn27view1turn23view3

## 治理、商业与现实限制

在权限模型上，Palantir 的设计非常值得参考。对象与属性安全策略能在 Ontology 内直接实现 row-level、column-level 乃至 cell-level permissions；新对象类型默认只允许通过 actions 编辑，以避免给用户开放 writeback dataset 的过大可见性；action submission criteria 还可引用 current user、group membership 与其它 Multipass 属性；audit logs 则提供 who、what、when、where 四类核心审计信息。这比传统“数据库行权限 + API 层 IAM + 前端隐藏按钮”的拼装方式更统一，也更适合 agent 参与执行。citeturn23view2turn35view0turn35view1turn25view4

从商业与产品视角看，“为什么看起来目前最像样的是 Palantir？”我的判断是：不是只有 Palantir **能**做，而是只有极少数厂商**同时**具备做到这件事所需的全部约束条件——跨数据源集成、对象后端、事务写回、内嵌安全、工作流工具、SDK、agent tooling、审计与部署系统。Palantir 的官方架构明确把 Ontology 置于 AIP、Foundry、Apollo 共同组成的平台中；而 OSDK、Pilot、AIP Chatbot、Automate、Observability 又把这层语义直接联到开发、应用、自动化、agent 与治理。换言之，Operational Ontology 不是单点特性，而是整个平台组织方式。citeturn22view0turn22view1turn21search9turn21search15turn32view0turn32view1

但这并不意味着 Ontology 会被 Palantir 永久垄断。行业正在沿不同路径逼近它：dbt 把 metrics、dimensions、entities 与 relationships 变成 AI query 的结构化层；Snowflake 把 semantic views 做进数据库对象，并提出 agent context layer；OSI 则尝试建立跨厂商语义层交换标准。这些路线今天还大多停留在“分析语义层”而不是“读写闭环操作层”，但它们已经证明：**语义层正在从 BI 配件变成 agent 基础设施。** citeturn16search3turn16search7turn16search2turn16search6turn16search14turn16search16

真实案例层面，Palantir 官方 impact 页面给出了一些方向性证据：entity["company","Airbus","aerospace company"] 的 Skywise 将 schedules、crew shifts、parts、deliveries、defects 集成到单一界面支撑计划；Sonnedix 用 objects、relationships、actions 管理复杂能源生态；entity["company","Swiss Re","reinsurance company"] 用 Foundry 提升风险识别、缓释与预测能力；entity["company","Jacobs","engineering company"] 则把站点优化工作流直接连接到运营场景。这些案例有价值，但也必须看到它们多数是供应商作者叙述，不应被当作独立第三方基准。citeturn17search7turn17search1turn17search5turn17search0

开放问题与限制同样不能回避。第一，ontology engineering 依然困难，且需要持续维护与跨团队共识；第二，错误的建模会导致 system silos、god object、action sprawl 等结构性失败；第三，Operational Ontology 的平台耦合度很高，中央维护、SDK 生成、权限作用域与工作流工具越统一，迁移与替换成本通常也越高——这一点更像一种架构推论，而不是任何厂商会主动强调的卖点；第四，并非所有场景都适合强 operationalization，尤其是高吞吐流式、弱约束探索性分析与快速试验阶段，更轻的 semantic layer 方案可能更经济。citeturn26view5turn23view1turn34view0turn32view0turn35view3

未来趋势大概率会沿三条线并行推进。其一，**开放语义交换**会增强，ontology 不会都锁死在单一平台里；其二，**prompt-to-ontology** 会兴起，Palantir Pilot 已可从自然语言生成 ontology entities、前端代码与种子数据；其三，**LLM 将成为 ontology engineer 的辅助者，而不是替代者**，因为近期系统性综述已经指出，LLM 在 ontology engineering 中目前主要扮演辅助工程师、领域专家助手和评估者，且标准化评测与透明流程仍不足。citeturn16search14turn16search16turn32view1turn28view3turn26view5

## 总结

这份研究报告的核心结论可以压缩为一句话：**Ontology 正在从“描述业务世界的语义资产”演化为“让人和 AI 在同一业务世界里读、想、做、留痕”的操作系统层。** 传统语义网 ontology 奠定了形式语义与共享词汇的基础；Palantir 把它推进为 operational ontology；而整个行业正在用 semantic layer、agent context layer 与开放交换标准把这一路线逐渐外溢。citeturn27view0turn26view0turn22view0turn16search6turn16search14

如果以 CTO 的技术决策视角来落结论，我会给出三个判断。第一，**不要把 Ontology 当作知识图谱项目**，而要把它当作企业 AI 的接口层与状态层。第二，**不要期待 Backend 消失**，而要主动识别哪些领域职责值得上移进 ontology：对象语义、权限、动作、agent 工具暴露、可观测性。第三，**不要一上来追求“大而全本体”**，而应从少量高价值对象、少量高频动作、清晰的权限边界和可审计闭环开始，让 ontology 先服务决策，再扩展服务认知。citeturn22view2turn23view0turn23view2turn32view0turn25view4

面向“下一代 AI 系统架构”，最重要的并不是是否采用 Palantir，而是是否接受这样一个架构前提：**AI 若要可靠进入企业核心流程，必须拥有稳定的业务对象语言、被授权的动作空间、可解释的执行轨迹，以及可持续演化的语义中层。** 在这一点上，Ontology 很可能不会成为所有软件的唯一未来，但它已经非常有机会成为高价值企业 AI 的默认中枢。citeturn22view0turn29view0turn29view1turn29view2turn16search16
