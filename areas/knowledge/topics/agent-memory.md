---
title: Agent Memory / 智能体记忆
type: topic
area: knowledge
status: active
aliases:
  - Agent Memory
  - 智能体记忆
  - KP - Memory
  - Memory
---
# Agent Memory / 智能体记忆

## Definition

Agent memory is the durable state layer that lets an agent retain, update, retrieve, govern, and reuse information beyond a single context window.

In this wiki, the term covers retrieval memory, structured memory, graph memory, reflective memory, world-model memory, and explicit memory lifecycle operations.

## Why it matters

- It prevents agent architecture discussions from collapsing into "vector DB vs long context."
- It is a core dependency for personal agents, local-first assistants, and long-running workflow runtimes.
- It creates the bridge between [[agent-core|Agent Core]] control loops and [[agent-runtime|Agent Runtime]] infrastructure.

## Connected notes

- [[../anthonydb-research/agent-memory-infrastructure-survey-2024-2026-智能体记忆基础设施综述|Agent Memory Infrastructure Survey]] — primary retained research note for memory taxonomy, lifecycle, governance, and evaluation.
- [[../anthonydb-research/cognitive-architecture-agent-core-landscape-认知架构与智能体核心全景|Cognitive Architecture Agent-Core Landscape]] — relates memory to classical control-loop architectures.
- [[../anthonydb-research/fruit-fly-connectome-to-embodied-simulation-果蝇连接组到具身仿真|Fruit-Fly Connectome to Embodied Simulation]] — adjacent reference for structure priors and memory/control continuity.

## Related topics

- [[agent-core|Agent Core]]
- [[agent-runtime|Agent Runtime]]
- [[openclaw|OpenClaw]]
- [[nanoclaw|NanoClaw]]

## Open questions

- When should memory be represented as files, vectors, structured records, or graph relationships?
- Which memory operations should be explicit user-visible actions versus background maintenance?
- How should personal memory systems handle stale facts, privacy, deletion, and provenance?
