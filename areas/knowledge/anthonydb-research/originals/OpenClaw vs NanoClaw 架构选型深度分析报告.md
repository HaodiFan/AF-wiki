---
title: "OpenClaw vs NanoClaw 架构选型深度分析报告"
tags:
  - area/knowledge
  - collection/anthonydb-research
  - source/anthonydb
  - topic/agent-systems
  - type/original
  - wiki/af
---
# OpenClaw vs NanoClaw 架构选型深度分析报告

## Meta
- type: `dive-in`
- domain: `engineering`
- spark: `on`
- created: 2026-03-12
- source: KG/raw/legacy-notes/OpenClaw vs NanoClaw 架构选型深度分析报告.md

## Content
# OpenClaw vs NanoClaw 架构选型深度分析报告

## 关联笔记

- OpenClaw 代码分析总览
- [[OpenClaw vs nanobot：后端、runtime 与产品能力差异总览|后端 / runtime / 产品能力]]
- Dive in / OpenClaw vs nanobot

## 关键词

- `architecture selection`
- `deployment fit`
- `cost control`
- `memory`
- `agent core`

> 生成日期: 2026-03-12
> 基于源码级分析，覆盖 agent core 设计、企业部署、增量开发、成本控制、配置体系、memory 迭代六大维度

---

## 目录

1. [Agent Core 设计哲学与区别](#1-agent-core-设计哲学与区别)
2. [企业部署场景分析](#2-企业部署场景分析)
3. [NanoClaw 增量开发优先级](#3-nanoclaw-增量开发优先级)
4. [成本控制对比](#4-成本控制对比)
5. [用户配置与 Agent 自迭代关键文件](#5-用户配置与-agent-自迭代关键文件)
6. [Memory 迭代机制异同](#6-memory-迭代机制异同)
7. [补充选型维度](#7-补充选型维度)
8. [选型决策矩阵](#8-选型决策矩阵)

---

## 1. Agent Core 设计哲学与区别

### 1.1 NanoClaw：极简主义的单循环引擎

**设计哲学**: 一个 agent = 一个 while 循环。所有复杂性都被压缩到 ~470 行 Python 代码中。

**核心流程** (`nanobot/agent/loop.py`):

```python
# 消息主循环 — 整个 agent 的心脏只有这一段
async def run(self) -> None:
    self._running = True
    await self._connect_mcp()
    while self._running:
        try:
            msg = await asyncio.wait_for(self.bus.consume_inbound(), timeout=1.0)
        except asyncio.TimeoutError:
            continue
        if msg.content.strip().lower() == "/stop":
            await self._handle_stop(msg)
        else:
            task = asyncio.create_task(self._dispatch(msg))
            self._active_tasks.setdefault(msg.session_key, []).append(task)
```

```python
# Agent 推理循环 — 工具调用迭代
async def _run_agent_loop(self, session, messages, tools_defs):
    for iteration in range(self.max_iterations):  # 默认 40 次
        response = await self.provider.chat(messages=messages, tools=tools_defs)
        if response.tool_calls:
            results = await self.tool_registry.execute_batch(response.tool_calls)
            messages.extend(results)
            continue
        return response.content  # 没有工具调用则返回
```

**关键设计选择**:

| 设计点 | 选择 | 理由 |
|--------|------|------|
| 并发模型 | `asyncio.Lock` 全局锁 | 简单、可预测，避免竞态 |
| 迭代上限 | 硬编码 40 次 | 防止死循环，足够绝大多数任务 |
| 工具结果截断 | 500 字符 | 防止 context 膨胀 |
| 错误处理 | 不持久化到历史 | 避免毒化后续推理 |
| 子 agent | UUID 跟踪 + 15 次迭代限制 | 轻量后台任务，防止资源泄漏 |

### 1.2 OpenClaw：分层弹性的 Agent 操作系统

**设计哲学**: Gateway + Agent Runtime + Plugin System 三层架构。agent 是操作系统中的"进程"，不是简单的循环。

**核心架构层次**:

```
┌─────────────────────────────────────────┐
│  Gateway Layer (HTTP/WS 控制面)           │
│  ├─ 多 agent 路由                        │
│  ├─ 认证 & 限流                          │
│  └─ Channel 插件管理                     │
├─────────────────────────────────────────┤
│  Agent Runtime (Pi Embedded Runner)      │
│  ├─ 流式消息处理                         │
│  ├─ 自适应 Compaction                    │
│  ├─ 多模型 Failover                      │
│  └─ Context 溢出恢复                     │
├─────────────────────────────────────────┤
│  Plugin / Extension System               │
│  ├─ 43+ Channel 扩展                     │
│  ├─ 52+ Skill 包                         │
│  └─ Memory Backend 可插拔                │
└─────────────────────────────────────────┘
```

**关键执行流** (`src/agents/pi-embedded-runner/run.js`):

```typescript
// OpenClaw 的 agent 执行是 retry-loop 嵌套结构
export async function runEmbeddedPiAgent(params) {
  // 1. 初始化 agent scope (工作空间、模型、技能、memory)
  // 2. 进入 attempt 循环 — 带 compaction 和 overflow recovery
  //    ├─ 每轮执行: 流式 LLM 调用 + 工具拦截
  //    ├─ context 溢出时: 触发 summarizeInStages()
  //    ├─ 模型失败时: auth profile 轮换到备用模型
  //    └─ 工具结果: 经过 sanitize + media 提取 + 安全过滤
  // 3. 会话持久化 (JSONL + 成本追踪)
}
```

**自适应 Compaction** (`src/agents/compaction.ts`):

```typescript
// 根据消息密度动态调整压缩比例
export function computeAdaptiveChunkRatio(messages, contextWindow) {
  const avgTokens = estimateMessagesTokens(messages) / messages.length;
  const avgRatio = (avgTokens * SAFETY_MARGIN) / contextWindow;
  // 当单条消息 > context 10% 时，降低 chunk 比例
  if (avgRatio > 0.1) {
    const reduction = Math.min(avgRatio * 2, BASE_CHUNK_RATIO - MIN_CHUNK_RATIO);
    return Math.max(MIN_CHUNK_RATIO, BASE_CHUNK_RATIO - reduction);
  }
  return BASE_CHUNK_RATIO; // 默认 0.4
}
```

### 1.3 核心区别对照

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **定位** | 轻量 agent 引擎 | Agent 操作系统 |
| **代码规模** | ~2,725 行 (agent core) | ~177,109 行 (全部) |
| **循环模型** | 单 while + asyncio.Lock | 嵌套 attempt + retry + failover |
| **故障恢复** | `max_iterations` 硬限制 | Compaction + overflow recovery + 模型轮换 |
| **工具治理** | 简单 allowlist | 4 层策略 (profile/global/agent/sandbox) |
| **扩展方式** | Python 包 + MCP | TypeScript 插件系统 + extension 包 |
| **会话模型** | `channel:chat_id` 直接映射 | `agent:agentId:provider:id[:channel:topic]` |
| **多 agent** | 子 agent (受限迭代) | 多 agent 独立配置 + 子 agent 嵌套 |
| **可读性** | 极高 (79 行核心循环) | 中等 (多层抽象需跟踪) |

---

## 2. 企业部署场景分析

### 2.1 按企业规模分析

#### 小型团队 (1-10 人)

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| 部署复杂度 | ★☆☆ Docker 一键启动 | ★★★ 需配置 Gateway + 扩展 |
| 上手时间 | 1-2 小时 | 1-2 天 |
| 资源占用 | 1 CPU, 1GB 内存 | 2+ CPU, 2GB+ 内存 |
| 适合场景 | 个人助手、小团队内部 bot | 过于重量级 |
| **推荐** | **✅ NanoClaw** | ❌ |

```yaml
# NanoClaw Docker 部署 — 极简资源声明
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 1G
    reservations:
      cpus: '0.25'
      memory: 256M
```

#### 中型团队 (10-100 人)

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| 多 channel 需求 | 15 个内置 channel | 43+ channel 扩展 |
| 多 agent 管理 | 单 agent + 子任务 | 多 agent 独立配置 |
| 权限控制 | 基本 allowlist | 4 层策略管道 |
| 审计日志 | JSONL 会话文件 | 结构化日志 + 成本追踪 |
| **推荐** | ✅ 如果场景简单 | ✅ 如果需要多 agent 或复杂权限 |

#### 大型企业 (100+ 人)

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| 水平扩展 | ❌ 全局锁限制 | ⚠️ 单实例多 agent，非分布式 |
| 多租户 | ❌ | 部分支持 (多 agent + channel 路由) |
| SSO/SAML | ❌ | 部分 (OAuth, session token) |
| 合规审计 | 手动 JSONL 查询 | 结构化指标 + OTEL 可观测 |
| 模型治理 | 基础 | 模型 failover + 预算 + 配额 |
| **推荐** | ❌ 需要大量定制 | ⚠️ 可用但非企业级 SaaS |

### 2.2 按使用场景分析

#### 场景 A: 中国企业内部 IM bot (钉钉/飞书/企微)

**NanoClaw 优势明显**:
- 内置 6 个中国平台 channel (钉钉、飞书、企微、QQ、MoChat、微信)
- 内置 4 个中国 LLM 网关 (AiHubMix、硅基流动、火山引擎、智谱等)
- Python 生态适合中国 SDK 集成
- 部署简单，运维成本低

#### 场景 B: 多渠道全球化客服/助手

**OpenClaw 更合适**:
- 43+ channel 覆盖全球主流平台
- 30+ 模型供应商 failover 保障可用性
- 会话路由可以将不同 channel 映射到不同 agent

#### 场景 C: 长对话 / 复杂工作流

**OpenClaw 显著领先**:
- 自适应 Compaction 保证长对话不崩溃
- Context 溢出自动恢复
- 多阶段摘要策略保留关键信息
- NanoClaw 的 token 估算 + 50% 目标线较粗糙

#### 场景 D: 快速原型 / 概念验证

**NanoClaw 优势明显**:
- 几小时内可完成从零到上线
- 代码可读性极高，修改成本低
- 依赖少，启动快

---

## 3. NanoClaw 增量开发优先级

如果 NanoClaw 需要追赶 OpenClaw 的能力，以下是按优先级排列的增量路线图：

### P0 — 生产环境必须 (1-2 周)

| 特性 | 当前 NanoClaw 状态 | OpenClaw 参考实现 | 开发量 |
|------|-------------------|------------------|--------|
| **工具策略管道** | 简单 allowlist | 4 层策略 (profile → global → agent → sandbox) | 中 |
| **Context 溢出恢复** | 无 (超限后崩溃) | `overflow-recovery` + 自动重试 | 中 |
| **模型 Failover** | 无 (单模型) | Auth Profile 轮换 + cooldown | 小 |
| **会话成本追踪** | 仅返回 usage dict | 每会话 input/output/cache token + 费用 | 小 |

### P1 — 多用户/团队需求 (2-4 周)

| 特性 | 当前 NanoClaw 状态 | OpenClaw 参考实现 | 开发量 |
|------|-------------------|------------------|--------|
| **多 Agent 配置** | 单 agent | `agents.list[]` 独立工作空间/模型/技能 | 中 |
| **输入队列** | 无 (直接处理) | collect → debounce → cap → summarize | 大 |
| **审批机制** | 无 | 高风险操作审批转发 | 中 |
| **Gateway 控制面** | 无 | HTTP/WS API + Web UI | 大 |

### P2 — 高级特性 (4-8 周)

| 特性 | 当前 NanoClaw 状态 | OpenClaw 参考实现 | 开发量 |
|------|-------------------|------------------|--------|
| **向量 Memory 检索** | 文件级 MEMORY.md | SQLite-vec 混合 BM25+向量搜索 | 大 |
| **自适应 Compaction** | 粗糙 token 估算 | adaptive chunk ratio + 多阶段摘要 | 中 |
| **Context Pruning** | 无 | cache-ttl 模式 + 软/硬清理比例 | 中 |
| **OTEL 可观测** | loguru 日志 | OpenTelemetry diagnostics 扩展 | 中 |

### P3 — 生态扩展 (持续)

| 特性 | 当前 NanoClaw 状态 | OpenClaw 参考实现 | 开发量 |
|------|-------------------|------------------|--------|
| **插件系统** | 简单技能包 | 完整 extension 生命周期 | 大 |
| **更多 Channel** | 15 个 | 43+ 个 | 按需 |
| **更多 Skill** | 8 个 | 52 个 | 按需 |
| **桌面/移动应用** | 无 | macOS, iOS, Android | 极大 |

### 增量开发建议

```
Sprint 1 (Week 1-2):  P0 — 稳定性地基
  → 模型 failover (改动最小，收益最大)
  → context 溢出恢复
  → 会话成本追踪

Sprint 2 (Week 3-4):  P0 → P1 过渡
  → 工具策略管道
  → 多 agent 配置
  → 审批机制

Sprint 3 (Week 5-8):  P2 选择性实现
  → 根据业务场景选择最急需的 2-3 项
  → 自适应 compaction 推荐优先
```

---

## 4. 成本控制对比

### 4.1 NanoClaw 的成本控制

#### Token 层面

```python
# memory.py — 核心成本控制: context window 的 50% 目标线
async def maybe_consolidate_by_tokens(self, session):
    target = self.context_window_tokens // 2  # 目标: 占用不超过一半
    estimated, source = self.estimate_session_prompt_tokens(session)
    if estimated < self.context_window_tokens:
        return  # 未超限，不消耗额外 token 做 consolidation
    # 超限时启动 LLM 驱动的摘要 (这本身消耗 token)
    for round_num in range(self._MAX_CONSOLIDATION_ROUNDS):  # 最多 5 轮
        ...
```

| 机制 | 实现 | 节省效果 |
|------|------|---------|
| 迭代上限 | `max_iterations=40` (主), `15` (子agent) | 防止死循环烧钱 |
| 输出截断 | 工具结果 500 字符, exec 输出 10K 字符 | 减少 context 膨胀 |
| Memory 合并 | 50% context window 目标 | 控制 prompt 大小 |
| 渐进式技能加载 | 仅加载摘要，按需读取全文 | 减少 system prompt token |
| 无速率限制 | 依赖 Provider 自身限流 | 无自有保护 |

**成本盲点**:
- 没有内置成本追踪/预算告警
- Memory consolidation 本身是额外 LLM 调用 (隐性成本)
- 无 prompt cache 优化策略 (仅 Anthropic 支持)
- 用户需手动在 Provider dashboard 监控

#### 基础设施层面

```yaml
# Docker Compose — 极低基础设施成本
resources:
  limits: { cpus: '1', memory: 1G }     # ~$5-15/月 VPS 即可
  reservations: { cpus: '0.25', memory: 256M }
```

### 4.2 OpenClaw 的成本控制

#### Token 层面

```typescript
// session-cost-usage.ts — 精细的成本追踪
const emptyTotals = (): CostUsageTotals => ({
  input: 0, output: 0,
  cacheRead: 0, cacheWrite: 0,      // 独立追踪 prompt cache
  totalTokens: 0, totalCost: 0,
  inputCost: 0, outputCost: 0,
  cacheReadCost: 0, cacheWriteCost: 0,
  missingCostEntries: 0,            // 追踪缺失定价的调用
});
```

| 机制 | 实现 | 节省效果 |
|------|------|---------|
| 自适应 Compaction | 根据消息密度动态调整压缩比 | 智能平衡质量与成本 |
| Prompt Cache 追踪 | 独立 cacheRead/cacheWrite 字段 | 可视化 cache 命中率 |
| Context Pruning | cache-ttl 模式 + softTrim/hardClear | 精确控制 context 大小 |
| 模型 Failover | 可配置从贵模型降级到便宜模型 | 故障时不停服且省钱 |
| 磁盘配额 | 每 agent 可设置磁盘上限 | 防止会话文件无限增长 |
| 输入队列去重 | debounce + cap + summarize | 减少重复消息的 LLM 调用 |
| Tool 结果裁剪 | sanitize + media 分离 | 减少无效 token |

**成本优势**:
- 每次会话都有精确的 USD 成本记录
- 可配置每 agent 的模型 (昂贵任务用强模型，简单用弱模型)
- 多阶段 compaction 比简单截断保留更多信息 (减少重复问答)

#### 基础设施层面

```
# OpenClaw 基础设施成本更高但可控
- 基础服务: 2+ CPU, 2GB+ 内存 (~$20-50/月)
- 可选: SQLite-vec 向量数据库 (内嵌，无额外成本)
- 可选: 外部 embedding 服务 (OpenAI/Gemini 约 $0.02/百万 token)
```

### 4.3 成本对比总结

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **单轮对话成本** | 通常更低 (循环短) | 稍高 (框架开销) |
| **长对话成本** | 可能更高 (粗糙 consolidation) | 更优 (自适应 compaction) |
| **成本可见性** | ❌ 无内置追踪 | ✅ 精确到 USD/会话 |
| **成本控制手段** | 迭代限制 + 截断 | 多层策略 + 去重 + 降级 |
| **基础设施成本** | $5-15/月 | $20-50/月 |
| **运维人力成本** | 低 (代码简单) | 中 (配置复杂) |

---

## 5. 用户配置与 Agent 自迭代关键文件

### 5.1 NanoClaw 配置体系

#### 系统级配置

**`~/.nanobot/config.json`** — 全局配置，agent 启动时加载

```json
{
  "provider": "anthropic",
  "apiKey": "sk-ant-...",
  "model": "anthropic/claude-opus-4-5",
  "maxTokens": 8192,
  "contextWindowTokens": 65536,
  "temperature": 0.1,
  "maxToolIterations": 40,
  "reasoningEffort": "high",
  "channels": {
    "telegram": { "token": "..." },
    "feishu": { "appId": "...", "appSecret": "..." }
  },
  "exec": {
    "timeout": 60,
    "restrictToWorkspace": true
  }
}
```

**调用时机**: `AgentLoop.__init__()` → `config_loader.load()` 启动时一次性加载

#### 工作空间级文件

```
{workspace}/
├── SOUL.md        # 人格定义 — system prompt 最前面
├── USER.md        # 用户画像 — 紧跟 SOUL.md
├── TOOLS.md       # 工具使用约束 — 补充工具行为
├── AGENTS.md      # Agent 元信息与自定义指令
├── memory/
│   ├── MEMORY.md  # 长期记忆 — 每次对话注入
│   └── HISTORY.md # 历史日志 — 可 grep 检索
├── sessions/
│   └── *.jsonl    # 会话持久化 — 按 session_key 存储
└── skills/
    └── {name}/
        └── SKILL.md  # 自定义技能
```

**各文件调用时机**:

```python
# context.py — 系统提示组装顺序
def build_system_prompt(self):
    parts = [
        self._get_identity(),           # SOUL.md (或 IDENTITY.md)
        self._load_bootstrap_files(),   # USER.md + TOOLS.md + AGENTS.md
        self.memory.get_memory_context(), # memory/MEMORY.md
        always_skills,                  # always=true 的技能全文
        skills_summary,                 # 其他技能的摘要列表
    ]
    return "\n\n---\n\n".join(parts)
```

**SOUL.md 示例** — 定义 agent 性格:

```markdown
# Soul

I am nanobot, a personal AI assistant.

## Personality
- Helpful and friendly
- Concise and to the point

## Values
- Accuracy over speed
- User privacy and safety

## Communication Style
- Be clear and direct
- Ask clarifying questions when needed
```

**USER.md 示例** — 定义用户上下文:

```markdown
# User Profile

## Basic Information
- **Name**: Anthony
- **Timezone**: UTC+8
- **Language**: 中文/English

## Preferences
### Communication Style
- Technical
- Bilingual responses preferred
```

#### Agent 自迭代涉及的文件

| 文件 | 自迭代方式 | 触发条件 |
|------|-----------|---------|
| `MEMORY.md` | LLM 调用 `save_memory` 工具自动更新 | token 估算超过 context_window/2 |
| `HISTORY.md` | consolidation 时追加带时间戳条目 | 与 MEMORY.md 同时触发 |
| `sessions/*.jsonl` | 每轮对话追加消息 | 每次 agent 回复后 |

```python
# memory.py — 自迭代的核心: consolidation 触发条件
async def maybe_consolidate_by_tokens(self, session):
    estimated, _ = self.estimate_session_prompt_tokens(session)
    if estimated < self.context_window_tokens:
        return  # 不触发
    # 超限 → LLM 摘要 → 更新 MEMORY.md + HISTORY.md
    # LLM 通过 save_memory 工具返回:
    #   - memory_update: 更新 MEMORY.md 中的事实
    #   - history_entry: 追加到 HISTORY.md 的时间线
```

### 5.2 OpenClaw 配置体系

#### 系统级配置

**`~/.openclaw/openclaw.json`** — JSON5 格式全局配置

```json5
{
  // 多 agent 定义
  agents: {
    defaults: {
      workspace: "~/openclaw-workspace",
      model: "claude-opus-4-5",
      heartbeat: { enabled: true, interval: "30m" },
    },
    list: [
      {
        id: "main",
        name: "主助手",
        workspace: "~/workspace-main",
        model: "claude-opus-4-5",
        skills: { allow: ["github", "coding-agent"] },
        memorySearch: {
          enabled: true,
          extraMemoryPaths: ["~/notes/**/*.md"],
        },
        subagents: { enabled: true },
        sandbox: { enabled: false },
        tools: { profile: "full" },
      },
      {
        id: "coder",
        name: "编码助手",
        workspace: "~/projects",
        model: "claude-sonnet-4-5",
        tools: {
          profile: "full",
          deny: ["web_search"],
        },
      },
    ],
  },

  // 模型配置 — 支持多供应商 failover
  models: [
    { id: "claude-opus", provider: "anthropic", model: "claude-opus-4-5" },
    { id: "gpt4", provider: "openai", model: "gpt-4o" },
    { id: "local", provider: "ollama", model: "llama3" },
  ],

  // Channel 配置
  channels: {
    telegram: { token: "...", dmPolicy: "allowFrom", allowFrom: [...] },
    discord: { token: "...", guilds: [...] },
    slack: { token: "...", appToken: "..." },
  },

  // Gateway 配置
  gateway: {
    mode: "local",
    port: 18789,
    auth: { password: "..." },
  },

  // Memory 配置
  memory: {
    backend: "sqlite-vec",
    embeddings: { provider: "auto" },  // auto: OpenAI → Gemini → Ollama
  },
}
```

**调用时机**: Gateway 启动时加载 → 运行时 watch 变更 → 热重载

#### 工作空间级文件

```
{workspace}/
├── AGENTS.md       # Agent 级自定义指令 — 注入 system prompt
├── IDENTITY.md     # Agent 身份 (可选)
├── HEARTBEAT.md    # 心跳消息模板 (可选)
├── skills/
│   └── {name}/
│       └── SKILL.md  # 自定义技能定义
└── (其他 .md 文件)   # 作为 memory search 源
```

**SKILL.md frontmatter 示例**:

```yaml
---
name: model-usage
description: "Track and display model usage statistics"
metadata:
  openclaw:
    emoji: "📊"
    os: ["darwin", "linux"]
    requires:
      bins: ["sqlite3"]
    install:
      - "brew install sqlite"
---

# Usage Instructions
...
```

#### Agent 自迭代涉及的文件

| 文件 | 自迭代方式 | 触发条件 |
|------|-----------|---------|
| 会话 JSONL | 每轮追加 + usage 元数据 | 每次 agent 回复 |
| Compaction 摘要 | 替换旧历史为压缩摘要 | context 接近模型限制 |
| Memory 向量索引 | `sync()` 增量嵌入新文件 | workspace 文件变更 |
| 磁盘预算 | 旧会话自动清理 | 超过配额时 |

```typescript
// compaction.ts — 自迭代: 多阶段摘要
export async function summarizeInStages(params) {
  const { messages, parts } = params;
  // 1. 将消息按 token 份额切分为 N 块
  const splits = splitMessagesByTokenShare(messages, parts);
  // 2. 每块独立摘要 (保留标识符、决策、TODO)
  const partials = await Promise.all(splits.map(summarizeWithFallback));
  // 3. 合并部分摘要为最终摘要
  return mergePartialSummaries(partials);
}
```

```typescript
// bootstrap-budget.ts — 控制注入 context 的文件预算
// workspace/**/*.md 文件按大小限制注入
// 超出限制的文件被截断并标记警告
```

### 5.3 配置体系对比

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **格式** | JSON (严格) | JSON5 (宽松, 支持注释) |
| **校验** | Pydantic schema | Zod schema |
| **热重载** | ❌ 需重启 | ✅ watch + 热重载 |
| **多 agent 支持** | ❌ 单 agent | ✅ agents.list[] |
| **人格文件** | SOUL.md | IDENTITY.md / AGENTS.md |
| **用户画像** | USER.md | 无独立文件 (写在 AGENTS.md) |
| **工具约束** | TOOLS.md | openclaw.json → tools.profile |
| **模型配置** | config.json 单字段 | models[] 数组 + failover 链 |
| **自迭代文件** | MEMORY.md + HISTORY.md | 会话 JSONL + 向量索引 |

---

## 6. Memory 迭代机制异同

### 6.1 NanoClaw 的 Memory 迭代

**架构**: 文件驱动的两层记忆系统

```
┌─────────────────────────────────────┐
│  Layer 1: MEMORY.md (长期记忆)        │
│  ├─ 人工可编辑的 markdown             │
│  ├─ LLM 通过 save_memory 工具更新     │
│  └─ 每次对话注入 system prompt        │
├─────────────────────────────────────┤
│  Layer 2: HISTORY.md (历史日志)        │
│  ├─ 仅追加的时间线条目                 │
│  ├─ [YYYY-MM-DD HH:MM] 格式          │
│  └─ 用 grep 检索历史对话              │
├─────────────────────────────────────┤
│  Layer 3: Session JSONL (短期记忆)     │
│  ├─ 未合并的消息直接用于 LLM 输入      │
│  ├─ last_consolidated 偏移量跟踪       │
│  └─ 追加式写入，不修改历史消息         │
└─────────────────────────────────────┘
```

**迭代流程详解**:

```python
# memory.py — 完整的 consolidation 流程
async def consolidate_messages(self, chunk: list[dict]) -> bool:
    """将一段旧对话摘要为结构化记忆"""
    # 1. 组装 consolidation prompt
    messages = [
        {"role": "system", "content": CONSOLIDATION_SYSTEM_PROMPT},
        # 包含当前 MEMORY.md 内容
        # 包含待摘要的消息块
    ]
    # 2. LLM 调用 — 使用 save_memory 工具
    response = await self.provider.chat(
        messages=messages,
        tools=[SAVE_MEMORY_TOOL_SCHEMA],
    )
    # 3. 解析工具调用结果
    #    → memory_update: 更新事实到 MEMORY.md
    #    → history_entry: 追加到 HISTORY.md
    # 4. 写入文件
    self._update_memory_file(memory_update)
    self._append_history(history_entry)
```

**关键特点**:
- **人类可读**: MEMORY.md 可直接打开查看/编辑
- **低成本**: 仅在超限时触发，非实时
- **无向量检索**: 依赖 LLM 的上下文理解
- **追加式**: 历史消息永远保留 (利于 Anthropic prompt cache)

### 6.2 OpenClaw 的 Memory 迭代

**架构**: 搜索驱动的混合检索系统

```
┌─────────────────────────────────────────┐
│  Layer 1: 向量 + 关键词混合检索           │
│  ├─ SQLite-vec 存储向量嵌入              │
│  ├─ FTS5 全文搜索索引                    │
│  ├─ BM25 + cosine 加权融合               │
│  └─ 多 embedding provider (自动降级)      │
├─────────────────────────────────────────┤
│  Layer 2: Compaction 摘要 (上下文记忆)     │
│  ├─ 自适应 chunk ratio                   │
│  ├─ 多阶段分块摘要 → 合并                │
│  ├─ 保留: 任务/决策/TODO/标识符           │
│  └─ 替换旧历史 (非追加)                  │
├─────────────────────────────────────────┤
│  Layer 3: 文件级增量同步                  │
│  ├─ workspace/**/*.md 监控               │
│  ├─ 文件变更时增量重新嵌入               │
│  └─ extraMemoryPaths 支持外部目录         │
└─────────────────────────────────────────┘
```

**混合检索实现**:

```typescript
// manager.ts — 混合搜索
async search(query: string): Promise<SearchResult[]> {
  const [bm25Results, vectorResults] = await Promise.all([
    this.ftsSearch(query),      // 关键词匹配
    this.vectorSearch(query),   // 语义相似度
  ]);
  return this.mergeHybridResults(bm25Results, vectorResults);
  // 加权评分: BM25 精确匹配 + 向量语义理解
}

// embeddings.ts — embedding 提供商自动降级链
// auto: OpenAI(text-embedding-3-small) → Gemini → Ollama → 失败
```

**Compaction 与 NanoClaw consolidation 的关键区别**:

```typescript
// OpenClaw: 替换式摘要 — 旧消息被摘要替换
// compaction.ts
const summaries = await summarizeInStages({
  messages: oldMessages,    // 旧消息
  parts: 2,                 // 分两段摘要
});
// 旧消息被 summaries 替换，释放 context 空间

// NanoClaw: 追加式合并 — 旧消息保留在 JSONL 中
// memory.py
session.last_consolidated = end_idx;  // 只移动指针
// 旧消息仍在文件中，但不会发给 LLM
```

### 6.3 Memory 机制对比

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **存储形式** | Markdown 文件 | SQLite 向量数据库 + JSONL |
| **检索方式** | 全量注入 system prompt | BM25 + 向量混合搜索 |
| **语义检索** | ❌ 无 | ✅ 多 embedding provider |
| **人类可读** | ✅ 直接编辑 MEMORY.md | ⚠️ 需工具查询数据库 |
| **摘要策略** | 单轮 LLM 调用 | 多阶段分块 + 合并 |
| **历史保留** | ✅ 追加式 (不删除) | ❌ 替换式 (旧消息被摘要替代) |
| **增量更新** | 仅 consolidation 时 | 文件变更触发增量嵌入 |
| **外部知识** | ❌ 仅对话记忆 | ✅ workspace 文件 + extraMemoryPaths |
| **cache 友好** | ✅ 追加式利于 prompt cache | ⚠️ 替换摘要破坏 cache |
| **scalability** | ❌ 全量注入有大小限制 | ✅ 搜索式按需检索 |
| **成本** | 低 (仅超限时调用 LLM) | 中 (embedding + 搜索 + compaction) |

---

## 7. 补充选型维度

### 7.1 开发语言与生态

| 维度 | NanoClaw (Python) | OpenClaw (TypeScript) |
|------|-------------------|----------------------|
| **AI/ML 生态** | ✅ 原生 Python 生态 | ⚠️ 需 bridge |
| **Web 前端** | ❌ 需额外服务 | ✅ 原生 Web UI |
| **类型安全** | ⚠️ Pydantic + mypy | ✅ TypeScript 静态类型 |
| **异步性能** | ✅ asyncio (成熟) | ✅ Node.js event loop |
| **打包分发** | pip/poetry | npm/pnpm |
| **中国开发者适配** | ✅ Python 在国内更普及 | ⚠️ TS 社区较小 |

### 7.2 安全性

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **命令沙箱** | 正则黑名单 (rm -rf 等) | 可选沙箱隔离 |
| **路径限制** | `restrictToWorkspace` 开关 | 工作空间 + sandbox 双重 |
| **认证** | 无内置 (依赖 channel) | 密码 + session token + 限流 |
| **密钥管理** | 环境变量 / config.json | 加密存储 + OTP + 审批 |
| **工具审批** | ❌ | ✅ 高风险操作审批转发 |

### 7.3 可观测性

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **日志** | loguru 结构化日志 | 结构化日志 + context |
| **指标** | ❌ | token 使用量 + 成本 + 队列深度 |
| **追踪** | ❌ | OTEL diagnostics 扩展 |
| **健康检查** | ❌ | channel 状态探针 + 心跳 |
| **会话审计** | JSONL + grep | JSONL + Web UI + 成本报表 |

### 7.4 测试覆盖

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **测试文件数** | ~30 | ~2,337 |
| **测试框架** | pytest | Jest/Vitest |
| **集成测试** | 基础 | 完善 |
| **可信度** | 中等 | 高 |

### 7.5 社区与生态

| 维度 | NanoClaw | OpenClaw |
|------|----------|----------|
| **技能市场** | ClawHub (基础) | ClawHub (完善) + 远程技能加载 |
| **插件数量** | 8 内置技能 | 52 技能 + 43 扩展 |
| **文档** | 基础 | Mintlify 文档站 |
| **贡献者** | 小团队 | 较大社区 |

---

## 8. 选型决策矩阵

### 快速决策流程

```
你的场景是什么？
│
├─ 个人助手 / 小团队 bot
│   ├─ 需要快速上线 → NanoClaw ✅
│   ├─ 需要中国 IM 集成 → NanoClaw ✅
│   └─ 需要苹果生态集成 → OpenClaw ✅
│
├─ 中型团队内部工具
│   ├─ 单 agent 够用 → NanoClaw ✅
│   ├─ 需要多 agent → OpenClaw ✅
│   └─ 需要权限控制 → OpenClaw ✅
│
├─ 企业级部署
│   ├─ 需要成本追踪 → OpenClaw ✅
│   ├─ 需要可观测性 → OpenClaw ✅
│   └─ 需要长对话稳定性 → OpenClaw ✅
│
└─ 定制开发平台
    ├─ Python 团队 → NanoClaw ✅ (易改)
    ├─ TypeScript 团队 → OpenClaw ✅
    └─ 需要深度定制 agent 核心 → NanoClaw ✅ (代码简单)
```

### 综合评分

| 维度 (权重) | NanoClaw | OpenClaw |
|------------|----------|----------|
| 部署简易度 (15%) | 9/10 | 5/10 |
| 代码可读性 (10%) | 9/10 | 6/10 |
| 长对话稳定性 (15%) | 5/10 | 9/10 |
| 多 agent/多租户 (15%) | 2/10 | 8/10 |
| 成本可控性 (10%) | 5/10 | 8/10 |
| 生态丰富度 (10%) | 4/10 | 9/10 |
| 安全性 (10%) | 4/10 | 8/10 |
| 中国市场适配 (10%) | 8/10 | 6/10 |
| 二次开发效率 (5%) | 9/10 | 5/10 |
| **加权总分** | **5.85** | **7.35** |

### 最终建议

- **选 NanoClaw**: 当你需要一个**快速落地、易于魔改、资源占用低**的 agent 引擎，尤其在中国企业 IM 场景
- **选 OpenClaw**: 当你需要一个**功能完备、久经考验、可观测可运维**的 agent 平台，尤其在多 agent、长对话、成本敏感的场景
- **混合策略**: 用 NanoClaw 做快速原型验证，验证后在 OpenClaw 上规模化部署

---

*本文档基于 2026-03-12 的源码分析生成，后续版本迭代可能改变上述结论。*

## Keypoints
<!-- LLM 提取，每条是一个可连接的知识点 -->
<!-- 如果该 keypoint 在其他 node 也出现过，标注 (also in: node名) -->
- [[KP - OpenClaw|OpenClaw]]
- [[KP - NanoClaw|NanoClaw]]
- [[KP - 关系分析|关系分析]]
- [[KP - Memory|Memory]]
- [[KP - nanobot|nanobot]]
- [[KP - Agent Core|Agent Core]]
## Links
### hints

### dive-ins
