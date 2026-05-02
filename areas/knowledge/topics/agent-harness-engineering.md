---
title: Agent Harness Engineering / 智能体 Harness Engineering
type: topic
area: knowledge
status: active
aliases:
  - Agent Harness Engineering
  - Agent Harness
  - AI agent harness engineering
  - 智能体 Harness Engineering
  - Harness 工程
tags:
  - area/knowledge
  - topic/agent-harness
  - topic/agent-systems
  - type/topic
  - wiki/af
---
# Agent Harness Engineering / 智能体 Harness Engineering

## Definition

Agent harness engineering is the discipline of building the external control layer around an AI agent: constraints, context assembly, tool access, sandboxing, feedback, evaluation, traces, and rule updates that make repeated failures harder to repeat.

It is broader than prompt writing and narrower than the model itself. The useful boundary is: the model acts, while the harness makes action governed, observable, reproducible, and evolvable.

## Why it matters

- It gives a durable way to convert recurring agent failures into rules, tests, tools, and runtime constraints.
- It connects prompt/context engineering to runtime governance, evals, observability, and workflow design.
- It is one of the main practical paths from ad hoc coding-agent use toward reliable long-running agent systems.

## Connected notes

- [[../../../resources/research/2026-04-26-agent-harness-engineering-deep-research|Harness Engineering 深度研究报告 / Agent Harness Engineering]] — full-text research note.
- [[agent-runtime|Agent Runtime / 智能体运行时]] — runtime layer that hosts tools, sessions, memory, observability, and policy.
- [[workflow-runtime|Workflow Runtime / 工作流运行时]] — durable execution graph and replay/checkpoint layer.

## Original Files In Wiki

- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Agent_Research/2024/Advanced AI Agent Research Report.pdf|Advanced AI Agent Research Report.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Agent_Research/2024/Agent Trajectory.pdf|Agent Trajectory.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Agent_Research/2022/ReAct Synergizing Reasoning and Acting in Language Models.pdf|ReAct Synergizing Reasoning and Acting in Language Models.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Function_Calling/2021/WebGPT Browser-assisted question-answering with human feedback.pdf|WebGPT Browser-assisted question-answering with human feedback.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Agent_Research/2025/Traceable_Evidence_Enhanced_Visual_Grounded_Reasoning_Evaluation_and_Methodology_2507.07999v1.pdf|Traceable_Evidence_Enhanced_Visual_Grounded_Reasoning_Evaluation_and_Methodology_2507.07999v1.pdf]]

## Related topics

- [[agent-core|Agent Core]]
- [[agent-runtime|Agent Runtime]]
- [[agent-memory|Agent Memory]]
- [[workflow-runtime|Workflow Runtime]]
- [[llm-safety-interpretability|LLM Safety and Interpretability]]
- [[opencode-architecture|Opencode Architecture]]

## Open questions

- Which failures should become prompt rules, tool changes, structural tests, or runtime policy?
- How should harness updates be evaluated without overfitting to one transcript or one task?
- What belongs in markdown memory versus executable middleware, CI, or tracing infrastructure?
