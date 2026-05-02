---
title: Self-Evolving AI Systems / 自演化 AI 系统
type: topic
area: knowledge
status: active
aliases:
  - Self-Evolving AI Systems
  - Self-Evolving LLMs
  - Recursive Self Improvement
  - 自演化 AI 系统
tags:
  - area/knowledge
  - topic/self-evolving-ai
  - type/topic
  - wiki/af
---
# Self-Evolving AI Systems / 自演化 AI 系统

## Definition

Self-evolving AI systems are AI systems that can modify, improve, evaluate, or extend parts of their own behavior, tools, data, prompts, code, or operating environment over time.

In this wiki, the topic is connected to harness engineering because durable self-improvement requires constraints, evals, traces, and rollback mechanisms rather than unconstrained self-modification.

## Why it matters

- It is a long-term research direction for agent systems that improve through feedback loops.
- It forces a clear distinction between self-editing, self-evaluation, self-training, and runtime adaptation.
- It depends on [[agent-harness-engineering|Agent Harness Engineering]] and [[workflow-runtime|Workflow Runtime]] for guardrails and reproducibility.

## Original Files In Wiki

- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/AI4Science/Self-Evolving_LLMs/2024/Self-Evolving AI Systems - A Long-Term Research Roadmap.pdf|Self-Evolving AI Systems - A Long-Term Research Roadmap.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/AI4Science/Self-Evolving_LLMs/2024/Self-Evolving LLMs - Paradigms and Progress.pdf|Self-Evolving LLMs - Paradigms and Progress.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/AI4Science/Self-Evolving_LLMs/2024/Self-Evolving LLM 全景式调研报告 - Gödel Machine 理论指导下的 AI.pdf|Self-Evolving LLM 全景式调研报告 - Gödel Machine 理论指导下的 AI.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/AI4Science/Self-Evolving_LLMs/2024/递归自我改进 AI 研究时间线 (2024–2025).pdf|递归自我改进 AI 研究时间线 (2024–2025).pdf]]
- [[areas/knowledge/source-documents/baidu-sync/DeepResearch/ASI_Progress_DeepResearch_2025.pdf.pdf|ASI_Progress_DeepResearch_2025.pdf.pdf]]

## Related topics

- [[agent-harness-engineering|Agent Harness Engineering]]
- [[agent-runtime|Agent Runtime]]
- [[workflow-runtime|Workflow Runtime]]
- [[llm-safety-interpretability|LLM Safety and Interpretability]]

## Open questions

- Which self-improvement loops can be safely automated, and which require human approval?
- What eval coverage is needed before a system can update its own harness or tools?
- How should regressions be detected across long-running self-evolution cycles?
