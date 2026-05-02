---
title: OpenClaw vs NanoClaw Architecture Selection / OpenClaw 与 NanoClaw 架构选型
aliases:
  - openclaw-vs-nanoclaw-architecture-selection
  - OpenClaw与NanoClaw架构选型
  - OpenClaw vs NanoClaw Architecture Selection
languages:
  - en
  - zh
tags:
  - area/knowledge
  - collection/anthonydb-research
  - topic/agent-systems
  - type/research-note
  - wiki/af
---
# OpenClaw vs NanoClaw Architecture Selection / OpenClaw 与 NanoClaw 架构选型

> Curated historical research note.
> 历史研究策展稿，含中英双语摘要。
> Imported on / 归档时间: 2026-04-20

## Source / 原文

Archived in current wiki / 当前 wiki 原文:
- [[originals/OpenClaw vs NanoClaw 架构选型深度分析报告]]
- [[originals/现代 AI Agent Core 设计哲学深度研究：以 OpenClaw 与 Nanobot 为中心的 Python-first 视角]]

## Topics / Concepts

- [[../topics/openclaw|OpenClaw]]
- [[../topics/nanoclaw|NanoClaw / Nanobot]]
- [[../topics/agent-runtime|Agent Runtime / 智能体运行时]]
- [[../topics/agent-core|Agent Core / 智能体核心]]

## Chinese Summary / 中文摘要

### 保留原因

- 这两篇保留的是实打实的工程取舍，而不是浅层产品比较。
- 它们对今天判断 agent runtime 的形态、部署姿态、安全边界以及 Python-first core 的适用场景依然有价值。

### 核心结论

1. NanoClaw / Nanobot 代表的是 **minimal loop kernel** 哲学：Python async loop 可读、工具迭代简单、文件型记忆直接、资源开销低、本地改造容易。
2. OpenClaw 代表的是 **gateway / control-plane** 哲学：长生命周期 gateway、typed tools、更强策略层、session 序列化、更好的可观测性，以及更明确的 sandbox / approval / control-plane 分离。
3. 真正的问题不是谁抽象上“更好”，而是你需要什么控制面。
4. 一个很稳的工程结论是混合路线可行：早期先用最小内核快速试验，复杂度上来后再向 control-plane 架构迁移。
5. 更通用的经验包括：按 session/lane 串行化工作、先做工具策略约束再暴露给模型、把文件当真相源、把记忆压缩与整理做成显式动作。
6. 这篇还保留了一套更广的 runtime taxonomy：gateway-centric assistant、minimal loop kernel、graph/state orchestration、multi-agent orchestration framework、domain-specific agent platform。

### 当前价值

- 这篇是后面评估 OpenClaw 类系统、本地助手和 Python-first agent core 时的比较基线。
- 它把“源码差异”提升成了“架构语言”，更利于后续决策。

### 后续动作

- 如果之后再看 OpenClaw、NanoClaw、Codex 风格 runtime 或 Claude Code 衍生方案，可以补一篇 current-state comparison。

## English Notes

## Why kept

- These notes preserve real engineering tradeoffs rather than shallow product comparison.
- They are still useful when thinking about agent runtime shape, deployment posture, safety boundaries, and where Python-first cores fit.

## Retained takeaways

1. NanoClaw / Nanobot represents the **minimal loop kernel** philosophy.
   The important properties are:
   - readable Python async loop
   - simple tool iteration
   - file-based memory
   - low resource footprint
   - easier local modification

2. OpenClaw represents the **gateway / control-plane** philosophy.
   The important properties are:
   - long-lived gateway
   - typed tools and stronger policy layers
   - session serialization
   - better observability and operability
   - more explicit sandbox / approval / control-plane separation

3. The real choice is not "which one is better in abstract."
   It is "which control surface do you need":
   - pick NanoClaw when you need a fast, hackable, Python-first core
   - pick OpenClaw when you need a long-running, policy-rich, multi-session platform

4. The hybrid strategy is structurally sensible:
   - prototype and iterate quickly on the minimal kernel
   - move toward the control-plane architecture when scaling operational complexity

5. The most reusable engineering lessons are independent of either project:
   - serialize work per session or lane
   - enforce tool policy before exposing tools to the model
   - treat files as the truth source, with retrieval/indexing as an acceleration layer
   - keep memory compaction/consolidation explicit

6. A broader taxonomy from the historical notes is still useful:
   - gateway-centric personal assistant runtimes
   - minimal loop kernels
   - graph/state orchestration runtimes
   - multi-agent orchestration frameworks
   - domain-specific agent platforms

## Why it matters to the current wiki

- This is a durable comparison baseline for future runtime choices, especially when evaluating OpenClaw-like systems, local assistants, or Python-first agent cores.
- It also gives a clean bridge from source-level code comparison to architecture-level decision language.

## Suggested follow-up

- Add a current-state comparison note if you later revisit OpenClaw, NanoClaw, Codex-style runtimes, or Claude Code derivatives.
