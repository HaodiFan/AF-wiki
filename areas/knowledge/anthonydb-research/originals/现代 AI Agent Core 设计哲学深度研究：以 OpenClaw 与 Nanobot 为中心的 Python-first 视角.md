# 现代 AI Agent Core 设计哲学深度研究：以 OpenClaw 与 Nanobot 为中心的 Python-first 视角

## Meta
- type: `dive-in`
- domain: `engineering`
- spark: `on`
- created: 2026-04-06
- source: KG/raw/legacy-notes/现代 AI Agent Core 设计哲学深度研究：以 OpenClaw 与 Nanobot 为中心的 Python-first 视角.md

## Content
# 现代 AI Agent Core 设计哲学深度研究：以 OpenClaw 与 Nanobot 为中心的 Python-first 视角

## 关联笔记

- OpenClaw 代码分析总览
- [[OpenClaw vs NanoClaw 架构选型深度分析报告|OpenClaw vs NanoClaw 架构选型]]
- Dive in / OpenClaw vs nanobot

## 关键词

- `agent core`
- `python-first`
- `gateway`
- `tool policy`
- `ecosystem comparison`

## 执行摘要

本报告把“Agent Core”视为一套**持续运行的自治系统内核**：它把外部事件（消息/定时器/系统信号）转化为一段可审计的执行轨迹（推理→工具调用→状态持久化→回复/动作），并通过**会话隔离、工具策略、记忆与编排**把“LLM 的一次推理”升级为“可长期运营的代理”。在当前（截至 2026 年初）主流开源生态中，OpenClaw 与 Nanobot 代表了两种强对比的 agent core 哲学：前者强调**“网关即控制面 + 类型化工具 + 强配置/策略 + 可扩展生态”**，后者强调**“极简 Python 内核 + 可读可改 + MCP 外接工具 + 文件化记忆”**。

从设计哲学角度，OpenClaw 的突出特征是把“个人助理”做成一个**长生命周期 Gateway（守住所有消息面）**，并用 WebSocket 类型化协议把客户端（CLI/桌面/Web 控制台）、设备节点（node）与 agent runtime 连接起来；它把工具、沙箱、审批、会话、记忆、插件都做成**可配置且可运行时观察**的控制平面能力，从而更像“自托管的 agent 操作栈”。

Nanobot（此处聚焦 HKUDS/nanobot）则刻意把核心缩到“约 4k 行 agent 核心代码”，以 Python async 事件循环 + 工具注册表 + 文件化记忆 + Session 管理为骨架；同时用 MCP（Model Context Protocol）把外部工具服务器纳入“原生工具”，避免把扩展性绑定在某一种语言插件 SDK 上。它的关键价值在于：**让研究者/工程师能在几百行级别的文件中读懂并重写 agent loop、记忆整合、技能加载与工具边界**。

对开发者的结论性建议是：如果你要构建“面向真实用户、跨渠道、长期在线”的个人/团队助理，OpenClaw 的控制面、策略与安全模型（尤其是会话隔离、工具策略与沙箱/审批链）提供了大量“可直接落地的工程答案”；如果你的目标是“Python-first 的可控内核（易改、易审计、易做学术/产品实验）”，Nanobot 提供了清晰的最小实现与 MCP 友好的扩展路径。

## OpenClaw 的 Agent Core 设计哲学与关键机制

### 网关中心主义：把“多消息面 + 控制面 + 设备节点”收敛为一个长期运行的 Gateway

OpenClaw 的架构起点不是“一个 Python 库/一个函数”，而是一个**单实例、长生命周期的 Gateway（daemon）**：它作为所有消息面的唯一所有者，并向控制面客户端暴露 WebSocket API；同一个 WS 端点也承载“节点设备（role: node）”连接，以声明式能力（caps/commands）提供诸如设备侧 canvas、摄像头/屏幕录制、位置等命令。文档明确了“一个 host 一个 Gateway”“控制面客户端默认连接 `127.0.0.1:18789`”“WS 帧 JSON + 校验、事件推送”等关键决策点，体现出 OpenClaw 把 agent core 当作“可运维系统”而非“脚本”。

这一设计哲学的直接收益是：  
OpenClaw 将“消息接入、权限与配对、会话键映射、事件流、可视化 UI、自动化调度”集中到控制面，降低了 agent runtime 需要直接理解“渠道差异”的负担；同时它也更利于把 agent 变成“家庭/个人基础设施”，因为所有输入输出与权限边界都被 Gateway 统一治理。

### 权威 agent loop：以“会话串行化 + typed tool stream”保持状态一致性

OpenClaw 的 agent loop 被定义为一次“真实 run 的权威路径”：输入→上下文组装→模型推理→工具执行→流式输出→持久化。该 loop 的关键工程承诺是：**同一 session 的 run 串行化**（避免并发工具/写入导致的会话竞态），并通过事件桥接把底层 runtime 的 assistant/tool/lifecycle 以流形式输出。文档还描述了队列模式（例如 steer：在工具调用之间注入新消息并跳过剩余工具）来处理“人类在 agent 执行中的插话”。这类设计属于典型“在线自治系统”场景的硬需求：一致性优先于吞吐。

另一个很“系统化”的点是：`agent` RPC 会立刻返回 `{runId, acceptedAt}`，而 `agent.wait` 则等待生命周期结束/错误/超时，体现出 OpenClaw 把 agent 运行当作“作业系统”来建模，天然适配控制台、自动化、长任务。

### 工具调用模型：类型化工具、分层策略与可插拔插件工具

OpenClaw 明确推进“从旧式 skill（shelling）到 first-class tools（typed）”的迁移：browser/canvas/nodes/cron 等被定义为一等工具（typed、无 shelling），并通过工具策略决定哪些工具会被发送给模型。

工具策略是分层的：（1）全局 allow/deny；（2）profile（minimal/coding/messaging/full）作为基线 allowlist；（3）按 provider 或 provider/model 的进一步收紧；（4）group:* 作为工具组展开。这一套策略体系的哲学非常明确：把“LLM 的能力边界”从 prompt 迁移到**可验证、可运维、可审计的配置层**。

在扩展性上，OpenClaw 的插件不仅能加命令、RPC，还能注册“JSON-schema agent tools”。插件必须提供 `openclaw.plugin.json`（用于发现与配置校验，且不执行插件代码），缺失/无效会阻断配置校验；这体现出对“插件供应链风险”的工程化响应：在 runtime 执行前先强约束插件形态与配置合法性。

### 会话与持久化：Gateway 作为真相源、JSONL 记录、DM 安全隔离

OpenClaw 明确把 Gateway 视为 session state 的 source of truth，并对 DM 默认聚合配置给出安全警告：如果 bot 会接收多人的 DM，默认把所有 DM 合并到 main 会话会产生跨用户隐私泄露风险，因此建议启用 `dmScope`（例如 per-channel-peer）实现“按人/按渠道隔离”。这属于 agent core 级别的根本安全问题：**上下文隔离不正确会直接导致信息泄露**，且无法靠 prompt 完全修复。

在持久化形态上，OpenClaw 的 session transcript 以 JSONL 存储在 `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`，并强调 session id 由 OpenClaw 稳定选择。相比一些“只存摘要/只存向量”的框架，这种设计更强调可审计、可迁移与可工具化处理。

### 记忆哲学：文件即真相、插件化检索、向量与混合搜索

OpenClaw 的记忆哲学非常“文件系统派”：记忆是 agent workspace 的 Markdown；模型不会“凭空记住”，只会记住写入磁盘的内容。默认布局包含 daily log（`memory/YYYY-MM-DD.md`）与可选长期记忆（`MEMORY.md`，且只在 main/private session 加载，不进群聊上下文）。这与“把记忆交给向量库”不同：它先定义**可读写的真相源文件**，再提供检索索引作为加速层。

检索层面，OpenClaw 提供 `memory_search` 与 `memory_get` 工具，并支持向量索引、混合检索与可选后端（例如实验性的 QMD sidecar）。文档还详细解释了 embedding provider 的自动选择逻辑（local/openai/gemini/voyage/mistral 等）与本地向量加速（sqlite-vec）等工程细节，说明其目标是“可运行、可运维的本地记忆检索系统”，而不是停留在概念层。

### 安全与沙箱：把“硬约束”放在策略/沙箱/审批链，而非 system prompt

OpenClaw 的系统提示词里明确提醒：安全 guardrails 仅是 advisory，不能作为 enforcement；真正的硬约束来自工具策略、exec approvals、沙箱与渠道 allowlist。这个表述本身就是一种成熟的 agent core 哲学：**不要把安全寄托在 LLM 的自觉上**。

沙箱方面，OpenClaw 允许用 Docker 容器运行工具以降低 blast radius，并区分 mode（off/non-main/all）、scope（session/agent/shared）、workspaceAccess（none/ro/rw）。尤其是 `workspaceAccess:"none"` 默认让工具只能看到 `~/.openclaw/sandboxes` 下的沙箱工作区，从而显著限制路径逃逸；而 `non-main` 让“群聊/公共 session”进 Docker，“私聊主会话”仍在 host，给出一种典型的“私密/公共双姿态运行”方案。

在“逃逸口”治理上，OpenClaw 把 sandbox、tool policy、elevated（仅 exec 的 host 逃逸）做了清晰区分，且原则是“deny 永远优先、tool policy 是硬停止、/exec 不能覆盖 deny”。此外 exec approvals 在执行宿主侧强制执行（gateway host 或 node host），并在需要时走审核流，体现出“把危险动作的最终裁决放在本地可信 UI/宿主”。

需要强调的是，这类生态也确实面临供应链与社会工程攻击：近期公开报道提及 ClawHub 出现恶意 skills 诱导用户手动执行终端命令，从而植入恶意软件；学术界也开始针对 OpenClaw 类工具调用链做 token 消耗攻击与轨迹安全审计研究。这些现实事件反过来说明：agent core 的安全设计必须覆盖“插件/技能内容注入 + 工具策略 + 执行边界 + 成本攻击”。

## Nanobot 的 Agent Core 设计哲学与关键机制

### 项目定位：极简可读的 Python agent core，而非“平台级控制面”

HKUDS/nanobot 的自我定位非常明确：超轻量（核心 agent 代码约 4k 行）、便于研究与改造、启动快、资源占用低。它在 README 中直接对比“99% smaller than Clawdbot”，本质上是对“大而全平台”路线的反向取舍：把核心做成最小闭环，方便快速迭代。

从目录结构看，Nanobot 把 agent core 关键部件都放在 Python 包内：`agent/loop.py`（loop）、`agent/context.py`（prompt builder）、`agent/memory.py`（持久记忆）、`agent/skills.py`（技能加载）、`agent/tools/`（内置工具），再配合 `channels/`（接入层）、`bus/`（消息路由）、`cron/`、`heartbeat/`、`session/` 与 `providers/`。这是一种典型的“单进程内核 + 组件化外围”的 Python 工程组织。

此外需说明：市面上也存在另一个同名但不同路线的 nanobot（例如 `nanobot-ai/nanobot` 更偏“构建 MCP agents/工具宿主”）；本报告的“深挖”以 HKUDS/nanobot 的 agent core 为主，并在对比中只把其它 nanobot 作为命名歧义提示。

### Agent loop：async 事件循环、任务派发与工具迭代上限

Nanobot 在 `AgentLoop` 的类注释里清晰定义 loop 的五步：接收消息→构建上下文（history/memory/skills）→调用 LLM→执行工具→发送响应。其 `run()` 方法以 asyncio 循环消费 inbound bus，并把普通消息派发为 task，以便支持 `/stop` 取消同 session 的 active tasks；同时以全局 `_processing_lock` 包裹 `_dispatch`，实现“在进程级别串行处理消息”的保守一致性策略。

在核心“工具-模型迭代”环上，Nanobot 显式设置 `max_iterations`（默认 40）与工具结果截断上限（`_TOOL_RESULT_MAX_CHARS = 16_000`），并在达到迭代上限时返回提示。这种硬上限是 agent core 的必要“熔断器”，否则系统很容易在工具调用循环中失控（成本与风险均不可控）。

### 工具模型：Python ToolRegistry + 可选 Cron/Spawn + MCP 动态接入

Nanobot 的工具体系以 `ToolRegistry` 为中心：启动时 `_register_default_tools()` 注册文件读写编辑/目录列举、shell exec、web_search/web_fetch、message、spawn（子代理）、以及在启用 cron_service 时注册 CronTool。其工具注册还显式支持 `restrict_to_workspace`：当开启时，把文件工具的 allowed_dir 绑定到 workspace，实现“工具级路径边界”。

MCP 的接入是 Nanobot 在扩展性上的关键哲学：它在 loop 启动时尝试 `_connect_mcp()`，通过 `connect_mcp_servers` 将配置的 MCP servers 自动发现并注册为 agent 工具；连接使用 AsyncExitStack 管理生命周期，失败则记录错误并在下一条消息时重试。此处的核心价值是“把扩展工具的复杂性外包给标准协议”，从而避免在 Python 内核里固化一套庞大的插件 SDK。

README 也明确给出 MCP 配置形态：支持 stdio（command+args）与 HTTP（url+headers），可为慢服务器设置 `toolTimeout`，且 MCP 工具会在启动时自动发现并注册，LLM 可像使用内置工具一样调用。

### 记忆与持久化：两层文件记忆 + token 驱动的“归档式整合”

Nanobot 的记忆系统的设计重点在于“最小但闭环”的持久化：`MemoryStore` 维护 `memory/MEMORY.md`（长期事实）与 `memory/HISTORY.md`（可 grep 的日志）。当需要整合时，它会调用 provider 的 `chat_with_retry`，并强制要求模型调用 `save_memory` 工具返回 `history_entry` 与 `memory_update`（完整更新后的长期记忆 Markdown）；随后写入文件，并记录日志。这个设计与 OpenClaw 的“文件为真相”一致，但结构更简化（不做 daily log 分层），且把“整合策略”实现为一段可读的 Python 逻辑。

更关键的是 Nanobot 的**token 驱动归档**：`maybe_consolidate_by_tokens()` 会估算 session prompt tokens；当估算超过 context window，就以“用户回合边界”为切分点，循环把旧消息 chunk 归档进记忆，直到估算降到 context window 的一半（target = window//2），并更新 `session.last_consolidated`。这是一种非常实用的“廉价 compaction 策略”：把大量历史对话迁移到可检索的 HISTORY/MEMORY，而不是持续膨胀上下文窗口。

### 上下文构建：bootstrap files、技能摘要与“运行时元数据非指令”标记

Nanobot 的 `ContextBuilder` 也采取类似 OpenClaw 的 workspace bootstrap 注入：默认读取 `AGENTS.md`、`SOUL.md`、`USER.md`、`TOOLS.md` 并拼接进 system prompt；同时注入 memory context 与 active skills 内容，并生成可 progressive loading 的技能摘要（告诉模型需要时用 read_file 读 SKILL.md）。

值得注意的是它对“运行时元数据污染”的显式防御：它构造一个 `_RUNTIME_CONTEXT_TAG = "[Runtime Context — metadata only, not instructions]"`，并把当前时间、时区、channel/chat_id 等信息拼进用户消息的前缀；并且为了兼容某些 provider 对“连续同 role 消息”的限制，它会把 runtime_ctx 与 user_content 合并为 single user message。这个细节体现了 Nanobot 的工程倾向：**以最小机制解决真实 provider 兼容性问题**。

### 技能模型：SKILL.md、可用性检查与对 OpenClaw 元数据的兼容

Nanobot 的技能同样以 SKILL.md 作为单位，优先加载 workspace skills，再加载 builtin skills；并支持在 skills frontmatter 中声明依赖（bins/env）做可用性过滤。它还构建 XML skills summary，标注 available=true/false 与缺失依赖，帮助模型在需要时决策“先装依赖还是换方案”。

一个对比 OpenClaw 很关键的点是：Nanobot 的 `_parse_nanobot_metadata` 明确“支持 nanobot 与 openclaw keys”，也就是说它在技能元数据层面努力兼容 OpenClaw 生态的标注方式。这是一种“以兼容换迁移成本”的设计哲学：让用户能复用/迁移部分 skills 资产，而不必重写全部描述与元数据。

### 安全姿态：默认 deny、路径限制开关、危险命令模式阻断，但明确承认局限

Nanobot 的 SECURITY.md 强调了“生产环境必须配置 allowFrom”，并指出版本差异：在 v0.1.4.post3 及更早版本，空 allowFrom 等同于允许所有用户；从 v0.1.4.post4 起，空 allowFrom 默认 deny all，若要放开需显式 `["*"]`。这属于典型 agent core 安全“默认立场”修正：从 permissive default 转为 secure default。

在工具边界上，Nanobot 提供 `tools.restrictToWorkspace`（README 的 Security 段落）与 file tools 的路径穿越保护，并对 exec 工具列出阻断的危险模式（如 `rm -rf /`、fork bomb、mkfs 等），同时明确建议：不要以 root 运行、使用受限用户、审计日志、对敏感系统谨慎部署。

但它也坦率列出已知局限：无内建 rate limiting、配置明文存 key、会话自动过期不足、命令过滤有限、审计能力有限。这种“把局限写在安全文档里”的做法，本身就是一种负责任的工程哲学：不把 agent core 伪装成“天然安全”。

## 对比矩阵与分类学

### 关键维度对比的定性“象限图”

下图用两条轴做一个工程化抽象：横轴“系统复杂度/平台化程度”，纵轴“自治/长任务能力”。这是**定性**而非基准测试；目的是帮助你把不同 agent core 的设计哲学放到同一张地图上理解。

Show code

（象限图的依据：OpenClaw 的 Gateway 控制面与策略栈；Nanobot 的极简内核与 MCP 接入；LangGraph 的“低层编排与长生命周期状态”定位；多 Agent 编排框架的定位：CrewAI/AutoGen/MetaGPT；软件工程代理平台 OpenHands（原 OpenDevin）。）

### 比较分析数据表

说明：

- “运行复杂度”偏向系统形态（daemon/平台 > 库 > 脚本）。
- “自治性”偏向是否天然支持长任务/多步工具链闭环。
- “Python 友好度”考虑核心实现语言、扩展方式、Python 集成摩擦。
- “代码规模”仅在有明确来源时填写（否则标“未明确/不稳定”）。

|Agent Core|运行复杂度|自治性|编排模型|部署形态|扩展性|安全/隔离哲学|Scaling 视角|代码规模（可证据）|Python 友好度|
|---|---|---|---|---|---|---|---|---|---|
|OpenClaw|高|高|会话 lane 串行 + 控制面作业|长驻 Gateway + WS 控制面|插件（含工具/RPC）+ skills|工具策略/沙箱/审批链为硬约束；DM 隔离|多 agent、每 host 单 Gateway、可远程控制|未明确（显著大于极简内核）|中（核心偏 Node/TS，Python 多走 exec/外部工具）|
|Nanobot（HKUDS）|中|中-高|async loop + 工具迭代上限|单进程 gateway/CLI|Python tools + MCP 工具服务器 + SKILL.md|默认 deny、restrictToWorkspace、危险命令阻断（但承认局限）|多实例（多 config/port/workspace）|核心约 4k 行（声明）|高（纯 Python、易二开）|
|LangGraph|中|中|图（StateGraph）+ 状态/检查点|Python 库 + 可配套 server/CLI|以节点/图组合扩展|依赖宿主应用决定（框架层偏编排）|适合嵌入现有服务与状态存储|未明确|高|
|CrewAI|中|中|多 Agent 角色/任务编排|Python 库/应用|角色、任务、工具可扩展|主要由开发者定义边界|面向“团队化”工作流|未明确|高|
|AutoGPT|中|中-高|经典 loop（计划→执行→回写）|应用/平台化尝试|插件/工具（生态多变）|安全依赖具体实现与部署|社区驱动，形态多演进|未明确|中-高（含 Python）|
|OpenHands（原 OpenDevin）|高|高|软件工程代理平台（代码/命令/浏览）|平台/产品化形态|集成工程工具链|强依赖隔离与审计（运行面较大）|面向工程任务与多人协作|未明确|中（常以服务/平台使用）|
|MetaGPT|高|中-高|SOP 驱动的多角色流水线|Python 框架/应用|角色、SOP、环境|安全取决于工具面与SOP约束|面向复杂任务拆解与角色协作|未明确|高|
|BabyAGI（archive）|低|中|无限 loop：任务生成/执行/排序|脚本原型|原型级扩展|研究/讨论为主（非生产）|不强调|~140 行（archive 描述）|高（非常易读）|
|Agent OS（多源概念）|中-高|中|“对齐/规范注入”或“运行时 server”两类|取决于具体实现|取决于具体实现|取决于具体实现|取决于具体实现|未明确|不稳定（概念多源）|
|AutoGen|中|中-高|多 Agent 对话驱动（human/tool/LLM）|Python/.NET 框架|agent/team/tools 可扩展|对话与工具边界由框架+应用共同定义|适合多 Agent 协作与 HITL|未明确|高|

### Agent Core 架构分类学与映射

在“设计哲学”层面，可以把 agent core（不含具体模型选择）粗略分为五类：

第一类是“控制面/网关中心型（Gateway-centric personal assistant）”。其核心问题是**多消息面治理、会话键与权限边界、可运维与可观察**；OpenClaw 是该类代表，并把 sandbox/exec approvals/工具策略整合进控制面。

第二类是“极简内核型（Minimal loop kernel）”。核心问题是**可读可改的 loop + 工具注册 + 文件化持久化**，便于研究、二开与快速实验；Nanobot 与 BabyAGI（原型）都属于此类，但 Nanobot 更工程化（session、MCP、工具边界、默认 deny）。

第三类是“图/状态编排型（Graph/state orchestration runtime）”。核心问题是**把 agent workflow 变成可组合、可测试、可 checkpoint 的图**，更适用于产品级业务流程嵌入；LangGraph 明确定位为低层编排与长生命周期 stateful agents。

第四类是“多 Agent 协作编排型（Multi-agent orchestration / conversation）”。核心问题是**角色分工、对话/任务协作协议、HITL 与工具协作**；CrewAI、AutoGen、MetaGPT 分别代表“角色任务编排”“对话框架”“SOP 驱动的软件公司流水线”。

第五类是“领域平台型（Domain platform: software engineering / ops）”。核心问题是**把代理嵌入真实工作台（代码、命令、浏览、评测、协作）**；OpenHands（原 OpenDevin）更偏这类。

## 其他主流 Agent Core 的简要架构剖析与“为何选它而不选 OpenClaw”

本节每个条目都按同一逻辑回答：它的 runtime 设计是什么、相对 OpenClaw 的差异是什么、为何开发者会选择它。

**LangGraph（来自 LangChain 生态）**：其核心设计是把 agent workflow 表达为图（StateGraph、节点与边），并强调“低层、专注编排”的定位；它也被描述为用于构建“长生命周期、stateful agents”的运行时，并配套 CLI/Server 形态支持 runs、threads 与 checkpointing/存储等。相较 OpenClaw，它并不自带“多渠道消息网关/配对/设备节点/个人助理控制面”，而是更像一套**可嵌入任意 Python 服务的编排内核**。当你的产品目标是“稳定、可测试、可复现的业务编排（比如多轮审批、条件分支、可回放）”，且你已有 Web 服务与数据库体系时，LangGraph 往往比 OpenClaw 更合适：更轻、更易做单元测试与持续部署，不需要引入 Gateway 治理整个消息面。

**CrewAI**：它明确把自己定位为 Python 多 Agent 编排框架，并强调“从零构建、独立于其它 agent 框架”，面向“角色扮演式多代理自动化”。相对 OpenClaw，它更偏“工作流编排库”，不强绑定“个人助理网关”与“跨渠道控制面”。当你要做的是“团队化任务分解（researcher/writer/reviewer）、企业流程自动化（任务队列、责任边界）”，CrewAI 的抽象往往更贴近问题本身；而 OpenClaw 的优势（多渠道接入、长期在线控制面）可能反而是额外复杂度。

**AutoGPT**：作为早期广泛传播的“自治 loop”项目之一，它更像把“计划—执行—反思/回写”的基本思想产品化与社区化。相对 OpenClaw，它不以“统一消息网关 + 强策略控制面”为中心，而以“更通用的自治任务执行”叙事驱动，实践形态也更随社区演化。开发者选择 AutoGPT 的典型原因不是“架构更严谨”，而是“生态/示例多、便于理解自治 loop 的基本工程挑战”，适合做探索性原型或学习对比。

**OpenHands（原 OpenDevin）**：OpenHands 把自己定位为“软件开发代理平台”，强调代理可以修改代码、运行命令、浏览 Web 等，面向的是“像人类开发者一样完成工程任务”的场景。相对 OpenClaw，它把核心放在“工程工作台”而不是“聊天网关控制面”：你更可能把它当作一个面向软件工程的工具平台/服务来用，而不是一个跨渠道个人助理。选择它的原因通常是：你要解决的就是工程任务（代码仓库、命令执行、web 资料），并希望有更完整的 UI/平台体验与工程化集成；OpenClaw 更适合“从聊天入口驱动真实世界任务”的个人助理形态。

**MetaGPT**：其核心哲学是“Software Company as Multi-Agent System”，通过 SOP（标准作业程序）把软件公司流程编码进多角色协作，并提出“Code = SOP(Team)”的理念；论文也强调把人类工作流编码进 prompt 序列以降低错误与提高验证能力。相对 OpenClaw，MetaGPT 的中心不是工具控制面，而是“高层流程与角色协作协议”；它更适合“把复杂需求拆成组织行为”的场景（PRD→设计→开发→测试），而不以跨渠道收件箱与设备节点为优先。选择 MetaGPT 的原因通常是：你要的是“流程化产出与多角色验证”，而不是“个人助理式网关”。

**BabyAGI（archive）**：其价值主要在“把任务生成/优先级/执行做成一个无限 loop 的最小可读原型”，并明确说明它是 pared-down 版本（约 140 行），用于分享想法与讨论；archive README 也直接写出 loop 步骤（取任务→执行→存储→生成新任务并重排）。相对 OpenClaw，它几乎没有控制面、安全策略、沙箱或长期在线治理，适合作为“理解自治任务循环”的教学/研究基线；开发者选择它的理由是“最小可读、便于改成实验平台”，而不是生产落地。

**Agent OS / AgentOS（概念多源）**：这类名字在生态里出现了不同实现与含义。`buildermethods/agent-os` 更像“为 coding agents 注入规范与对齐系统（specs/工作方式）”，强调能与多种工具协同；而 `agents-os/agentos` 则自称“生产级 runtime”，强调内建 memory 管理、安全工具沙箱与多 provider 支持。相对 OpenClaw，它们通常不以“聊天网关控制面”为第一中心：前者偏“对齐与规范化开发流程”，后者偏“运行时 server”。当你的需求是“让编码代理更像你的工程团队（规范、spec、约束）”或者“需要一套纯 Python/服务化 runtime 承接大量会话”，你可能会选这类 AgentOS；但需要注意命名歧义与具体实现差异，不能把“AgentOS”当作单一确定的架构。

**Microsoft AutoGen**：AutoGen 的核心定位是“多 agent 对话框架”，强调 agent 可整合 LLM、工具与人类输入，并通过自动化 agent chat 完成任务；其研究论文也将其描述为通过多 agent 对话组合来构建下一代 LLM 应用。相对 OpenClaw，AutoGen 更像“编排与交互协议层”，并不自带“个人助理网关”那套渠道治理与设备节点体系。你会选择 AutoGen 的典型原因是：你要做的是多 agent 协调/HITL，对话协议与 agent 行为组合是核心，而不是跨渠道收件箱与本地控制面的运维问题。

补充（“其它未指明”）中，一个常见的“介于 AutoGPT 与工程化之间”的选择是 LoopGPT：它自称是对 Auto-GPT 的 Python 包级重实现，强调模块化与可扩展性；当你想保留经典自治 loop 叙事，但又希望更工程化的 Python 结构时，这类项目可能比直接使用 AutoGPT 更顺手。

## 最小化 Python Agent Core 复刻 OpenClaw Essentials

本节目标不是“复刻 OpenClaw 全部”，而是提炼其对 agent core 最关键的、可迁移到 Python 的“本质构件”。这些“本质”来自 OpenClaw 文档中反复出现的工程承诺：

- **Gateway/控制面**将消息面统一治理（哪怕你只做单渠道，也要保留抽象）。
- **权威 loop**：会话串行化、可流式观察、工具事件与生命周期事件分离。
- **工具策略硬约束**（allow/deny/profile/byProvider）与沙箱/审批链，而不是靠 prompt。
- **文件化 workspace 与记忆**作为真相源。
- **定时唤醒机制（cron/heartbeat）**作为自治触发器。

### 最小架构图

Show code

### 设计要点与取舍

在 Python 里复刻 OpenClaw“核心精神”，最重要的不是复制它的渠道数量或 UI，而是复制三点工程纪律：

第一点是“会话 lane 串行化”。OpenClaw 明确将每个 session 的 run 串行化以避免工具/会话竞态；Nanobot 也采用全局 lock + session task 管理的保守策略。你的 Python core 也应把“同一 session 的执行互斥”作为默认，而把并行性放到“不同 session 之间”。

第二点是“工具策略先于工具实现”。OpenClaw 的 tool policy 是硬停止，/exec 不可覆盖 deny；Nanobot 则以 restrictToWorkspace 和危险命令阻断形成最小边界。Python 复刻时，应把 ToolPolicy 设计成独立层，并在向 LLM 暴露 tool schema 前就完成裁剪（避免把禁用工具仍发给模型）。

第三点是“文件化真相源 + 索引/检索是加速层”。OpenClaw 与 Nanobot 都把记忆落在 Markdown 文件上，差异只在层次与检索方式。对 Python 开发者而言，这比“直接上向量库 + 自动写入”更可控：你可以先保证审计与可读，再在检索侧迭代优化。

### 注释式伪代码（Python）

```python
from __future__ import annotations
import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

@dataclass
class InboundEvent:
  session_key: str          # 由 router 统一映射：channel + peer/group + agent_id 等
  channel: str
  chat_id: str
  sender_id: str
  content: str
  attachments: List[Any] = None
  meta: Dict[str, Any] = None

@dataclass
class OutboundEvent:
  channel: str
  chat_id: str
  content: str
  meta: Dict[str, Any] = None

class ToolPolicy:
  """硬约束：在 LLM 看到工具之前，就裁剪工具集合。"""
  def __init__(self, profile: str = "coding", allow: List[str] = None, deny: List[str] = None):
    self.profile = profile
    self.allow = allow or []
    self.deny = deny or []

  def is_allowed(self, tool_name: str) -> bool:
    # deny wins；allow 非空则默认拒绝其它
    if tool_name in self.deny or "*" in self.deny:
      return False
    if self.allow:
      return tool_name in self.allow or "*" in self.allow
    return True

class SessionStore:
  """权威 transcript：建议 JSONL（可审计、可回放）。"""
  async def append(self, session_key: str, record: Dict[str, Any]) -> None: ...
  async def load_history(self, session_key: str, limit: int) -> List[Dict[str, Any]]: ...

class MemoryStore:
  """文件化记忆：先可读可写，再做索引加速。"""
  async def load_context(self) -> str: ...
  async def write(self, text: str) -> None: ...

class ToolRegistry:
  def __init__(self):
    self._tools: Dict[str, Any] = {}

  def register(self, name: str, schema: Dict[str, Any], handler: Callable[..., Any]) -> None:
    self._tools[name] = {"schema": schema, "handler": handler}

  def schemas(self, policy: ToolPolicy) -> List[Dict[str, Any]]:
    out = []
    for name, t in self._tools.items():
      if policy.is_allowed(name):
        out.append(t["schema"])
    return out

  async def execute(self, name: str, args: Dict[str, Any]) -> Any:
    return await self._tools[name]["handler"](args)

class SandboxRunner:
  """可选：把 exec/file/net 等危险工具放进 Docker/容器/受限用户。"""
  async def run_exec(self, argv: List[str], *, approvals: bool) -> Tuple[int, str, str]: ...

class AgentLoop:
  def __init__(self, tools: ToolRegistry, sessions: SessionStore, memory: MemoryStore,
               policy: ToolPolicy, model_call: Callable[..., Any]):
    self.tools = tools
    self.sessions = sessions
    self.memory = memory
    self.policy = policy
    self.model_call = model_call  # 你的 LLM client（支持 tool calling）
    self.max_iters = 40

  async def run_turn(self, ev: InboundEvent) -> OutboundEvent:
    history = await self.sessions.load_history(ev.session_key, limit=200)
    mem_ctx = await self.memory.load_context()

    # 组装 system prompt（包含 workspace、时间、工具说明、记忆提示等）
    system = self._build_system_prompt(mem_ctx=mem_ctx, tool_schemas=self.tools.schemas(self.policy))

    messages = [{"role": "system", "content": system}, *history,
                {"role": "user", "content": ev.content}]

    final_text: Optional[str] = None
    for _ in range(self.max_iters):
      resp = await self.model_call(messages=messages, tools=self.tools.schemas(self.policy))
      if resp.tool_calls:
        for tc in resp.tool_calls:
          if not self.policy.is_allowed(tc.name):
            # 硬拒绝：工具不存在就不该执行
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": f"Denied by tool policy: {tc.name}"})
            continue
          result = await self.tools.execute(tc.name, tc.args)
          messages.append({"role": "tool", "tool_call_id": tc.id, "content": self._truncate(result)})
        continue

      final_text = resp.text
      break

    # 持久化 transcript（包括工具结果、最终回复）
    await self.sessions.append(ev.session_key, {"role": "user", "content": ev.content})
    await self.sessions.append(ev.session_key, {"role": "assistant", "content": final_text or ""})

    return OutboundEvent(channel=ev.channel, chat_id=ev.chat_id, content=final_text or "")

  def _build_system_prompt(self, mem_ctx: str, tool_schemas: List[Dict[str, Any]]) -> str:
    # 学 OpenClaw：system prompt compact、分区固定、明确“硬约束不靠 prompt”
    return f"""You are an agent.
Memory:\n{mem_ctx}\n
Tools:\n{[t['name'] for t in tool_schemas]}
Rules: tool policy is enforced outside the model; never assume tools exist if not listed.
"""

  @staticmethod
  def _truncate(x: Any, limit: int = 16000) -> str:
    s = str(x)
    return s if len(s) <= limit else s[:limit] + "...(truncated)"

class Gateway:
  """控制面最小形态：路由 session + per-session lane 串行化 + cron 注入。"""
  def __init__(self, loop_factory: Callable[[], AgentLoop]):
    self.loop_factory = loop_factory
    self.lanes: Dict[str, asyncio.Lock] = {}

  async def handle(self, ev: InboundEvent) -> OutboundEvent:
    lock = self.lanes.setdefault(ev.session_key, asyncio.Lock())
    async with lock:
      loop = self.loop_factory()
      return await loop.run_turn(ev)
```

## 趋势判断与对开发者的建议

### 趋势：工具生态正在“协议化”，MCP 让扩展不再绑定语言与 SDK

Nanobot 把 MCP 放在核心扩展路径上，并强调配置可直接复用；而更广泛的生态也在把“工具接入”从特定框架插件转向标准协议。对新 agent core 开发者而言，这意味着：核心应更关注**工具治理（策略、权限、审计、沙箱）**，而不是工具数量。MCP 这类协议会把工具供给侧做大，也会把供应链风险放大。

### 趋势：安全从“提示词对齐”转向“可验证执行与可证明 guardrail”

OpenClaw 文档反复强调“system prompt guardrails 不等于 enforcement”，而研究界已经开始讨论“proof-of-guardrail”：在可信执行环境中生成可验证证明，表明某个 guardrail 确实参与了生成过程。对未来 agent core 来说，“可验证的策略执行”和“可审计的轨迹”会逐渐成为生产级要求。

### 趋势：成本攻击与轨迹安全成为 agent core 的一等问题

工具链的开放会带来新的攻击面：例如通过 Trojanized skill 诱导工具链反复调用造成 token 耗尽（Clawdrain），或在复杂对话轨迹中触发越权与泄露。对核心开发者而言，“max tool iterations、输出截断、速率限制、按 session 的预算/配额、对工具结果污染的清洗”应当成为内核级默认能力，而不是业务层补丁。Nanobot 的迭代上限与结果截断、OpenClaw 的工具策略与 lane 串行化，都可以视为此趋势下的先行设计。

### 建议：Python-first 构建新 agent core 时的工程优先级

第一优先级是“边界与默认安全姿态”。无论你走 OpenClaw 的平台路线还是 Nanobot 的极简路线，最容易出事故的都是：默认允许所有人 DM、默认工具全开、默认 host 执行无审批、会话隔离错误。OpenClaw 在 DM scope 上给出明确安全警告，Nanobot 则把 allowFrom 默认改为 deny all，并提供 restrictToWorkspace 开关；这些都应成为 Python 新内核的默认模式。

第二优先级是“可审计的持久化”。建议把 transcript 做成 JSONL 这类可回放日志，把 memory 做成 Markdown 这类可读真相源，再在其上叠加检索/向量索引。这样做的好处是：你可以在出现安全/行为问题时用轨迹复盘，而不是只有“向量库里的一堆片段”。

第三优先级是“运行时可观测与可控”。OpenClaw 将 runId、生命周期流、工具流做成控制面输出；Nanobot 也通过 bus 进度消息与 /stop（取消任务）等机制提供基本可控性。Python new core 至少应提供：runId、工具事件、取消、超时、预算与限流的可观测接口，否则系统会在真实使用中迅速变得不可运维。

## Keypoints
<!-- LLM 提取，每条是一个可连接的知识点 -->
<!-- 如果该 keypoint 在其他 node 也出现过，标注 (also in: node名) -->
- [[KP - nanobot|nanobot]]
- [[KP - OpenClaw|OpenClaw]]
- [[KP - 关系分析|关系分析]]
- [[KP - Memory|Memory]]
- [[KP - NanoClaw|NanoClaw]]
- [[KP - Agent Core|Agent Core]]
## Links
### hints

### dive-ins
