---
title: Agent Runtime / 智能体运行时
type: topic
area: knowledge
status: active
aliases:
  - Agent Runtime
  - 智能体运行时
  - agent runtime
---
# Agent Runtime / 智能体运行时

## Definition

Agent runtime is the operational layer that hosts agent execution: sessions, tools, memory access, policies, checkpoints, observability, approval, sandboxing, and workflow orchestration.

It is broader than agent core. The core chooses actions; the runtime makes those actions durable, governed, observable, and repeatable.

## Why it matters

- Most architecture tradeoffs appear when a prototype must become a long-running system.
- Runtime design decides whether a system feels like a script, a local assistant, a workflow engine, or a platform.
- It connects [[agent-core|Agent Core]], [[agent-memory|Agent Memory]], and [[workflow-runtime|Workflow Runtime]] into one engineering lens.

## Connected notes

- [[../anthonydb-research/openclaw-vs-nanoclaw-architecture-selection-OpenClaw与NanoClaw架构选型|OpenClaw vs NanoClaw Architecture Selection]] — gateway/control-plane versus minimal-loop runtime comparison.
- [[../anthonydb-research/opencode-system-architecture-patterns-Opencode系统架构模式|Opencode System Architecture Patterns]] — runtime maturity ladder from source layout to pipeline-centric execution.
- [[../anthonydb-research/agent-memory-infrastructure-survey-2024-2026-智能体记忆基础设施综述|Agent Memory Infrastructure Survey]] — memory infrastructure requirements for long-running agents.

## Related topics

- [[agent-core|Agent Core]]
- [[agent-memory|Agent Memory]]
- [[openclaw|OpenClaw]]
- [[nanoclaw|NanoClaw]]
- [[opencode-architecture|Opencode Architecture]]
- [[workflow-runtime|Workflow Runtime]]

## Open questions

- When does a local agent need runtime governance instead of a simple tool loop?
- Which runtime state should be source-controlled markdown, SQLite, checkpoint state, or external service state?
