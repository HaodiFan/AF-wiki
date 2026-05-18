---
title: Agent Core / 智能体核心
type: topic
area: knowledge
status: active
aliases:
  - Agent Core
  - 智能体核心
  - KP - Agent Core
tags:
  - area/knowledge
  - topic/agent-core
  - topic/agent-systems
  - type/topic
  - wiki/af
---
# Agent Core / 智能体核心

## Definition

Agent core is the control center that determines how an agent observes state, decides actions, calls tools, updates memory, and continues or stops a loop.

In this wiki, it is treated as a family of design choices rather than one fixed abstraction.

## Why it matters

- It separates product/runtime decisions from deeper control-loop design.
- It gives a shared language for comparing tool-calling agents, classical cognitive architectures, and Python-first local agents.
- It helps decide whether a system needs a minimal loop, a gateway control plane, or a graph/state workflow runtime.

## Connected notes

- [[../anthonydb-research/cognitive-architecture-agent-core-landscape-认知架构与智能体核心全景|Cognitive Architecture Agent-Core Landscape]] — anchor note for agent-core taxonomy.
- [[../anthonydb-research/openclaw-vs-nanoclaw-architecture-selection-OpenClaw与NanoClaw架构选型|OpenClaw vs NanoClaw Architecture Selection]] — engineering comparison of two agent-core/runtime styles.

## Source References

- `baidu-sync:37fc6ef79a66` — A Review of 40 Years in Cognitive Architecture Research Core Cognitive Abilities and Practical Applications.pdf
- `baidu-sync:d56d59d20fc6` — Cognitive LLMs Towards Integrating Cognitive Architectures and Large.pdf
- `baidu-sync:943e6dba58a4` — 认知架构与LLM Agent的再相逢.pdf
- `baidu-sync:f0af1bfe5001` — ReAct Synergizing Reasoning and Acting in Language Models.pdf
- `baidu-sync:1cfb0dbcc682` — HuggingGPT Solving AI Tasks with ChatGPT and its Friends in Hugging Face.pdf
- `baidu-sync:4735406ed058` — definition of AGI.pdf

## Related topics

- [[agent-memory|Agent Memory]]
- [[agent-runtime|Agent Runtime]]
- [[large-language-models|Large Language Models]]
- [[function-calling-and-tool-use|Function Calling and Tool Use]]
- [[openclaw|OpenClaw]]
- [[nanoclaw|NanoClaw]]
- [[workflow-runtime|Workflow Runtime]]

## Open questions

- Which agent-core responsibilities should stay inside a small loop, and which should move into a runtime or control plane?
- How should tool policy, memory updates, and session serialization be split across core and runtime layers?
