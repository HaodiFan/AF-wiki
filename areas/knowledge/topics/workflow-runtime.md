---
title: Workflow Runtime / 工作流运行时
type: topic
area: knowledge
status: active
aliases:
  - Workflow Runtime
  - 工作流运行时
  - pipeline-centric runtime
  - Pipeline Runtime
---
# Workflow Runtime / 工作流运行时

## Definition

Workflow runtime is the architecture pattern where executable flows, steps, state transitions, checkpoints, and generated contracts become the primary artifact.

In agent systems, this is the point where the unit of coordination shifts from a source tree or script to a durable execution graph.

## Why it matters

- It makes complex agent and tool systems testable, replayable, and governable.
- It clarifies when build graph, schema-first contracts, and runtime orchestration are separate maturity layers.
- It bridges [[opencode-architecture|Opencode Architecture]] and [[agent-runtime|Agent Runtime]].

## Connected notes

- [[../anthonydb-research/opencode-system-architecture-patterns-Opencode系统架构模式|Opencode System Architecture Patterns]] — primary retained note for pipeline/workflow-centric runtime.
- [[../anthonydb-research/openclaw-vs-nanoclaw-architecture-selection-OpenClaw与NanoClaw架构选型|OpenClaw vs NanoClaw Architecture Selection]] — related runtime taxonomy.

## Related topics

- [[agent-runtime|Agent Runtime]]
- [[agent-core|Agent Core]]
- [[opencode-architecture|Opencode Architecture]]
- [[openclaw|OpenClaw]]

## Open questions

- When should an agent workflow become an explicit graph instead of remaining inside a tool loop?
- Which workflow states need checkpointing, replay, and human approval?
