---
title: Agent Runtime / 智能体运行时
type: topic
area: knowledge
status: active
aliases:
  - Agent Runtime
  - 智能体运行时
  - agent runtime
tags:
  - area/knowledge
  - topic/agent-runtime
  - topic/agent-systems
  - type/topic
  - wiki/af
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
- [[../../../resources/research/2026-04-26-agent-harness-engineering-deep-research|Harness Engineering 深度研究报告]] — harness as the external control layer around agent runtime behavior.

## Source References

- `baidu-sync:7dd943e650e2` — Agent Trajectory.pdf
- `baidu-sync:e5e86d7fec46` — Advanced AI Agent Research Report.pdf
- `baidu-sync:7ce607afcf73` — UI-TARS-2.pdf
- `baidu-sync:ab88db60c7c3` — PyVision_Agentic_Vision_with_Dynamic_Tooling_2507.07998v1.pdf
- `baidu-sync:5fc26cdd8675` — The_Trust_Fabric_Decentralized_Interoperability_and_Economic_Coordination_for_the_Agentic_Web_2507.07901v1.pdf

## Related topics

- [[agent-core|Agent Core]]
- [[agent-memory|Agent Memory]]
- [[agent-harness-engineering|Agent Harness Engineering]]
- [[ontology|Ontology]]
- [[function-calling-and-tool-use|Function Calling and Tool Use]]
- [[multimodal-ai|Multimodal AI]]
- [[openclaw|OpenClaw]]
- [[nanoclaw|NanoClaw]]
- [[opencode-architecture|Opencode Architecture]]
- [[workflow-runtime|Workflow Runtime]]

## Open questions

- When does a local agent need runtime governance instead of a simple tool loop?
- Which runtime state should be source-controlled markdown, SQLite, checkpoint state, or external service state?
