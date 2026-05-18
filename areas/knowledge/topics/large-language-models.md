---
title: Large Language Models / 大语言模型
type: topic
area: knowledge
status: active
aliases:
  - LLM
  - LLMs
  - Large Language Models
  - 大语言模型
tags:
  - area/knowledge
  - topic/llm
  - type/topic
  - wiki/af
---
# Large Language Models / 大语言模型

## Definition

Large language models are foundation models trained primarily on language and related multimodal data, used for generation, reasoning, tool use, retrieval, coding, evaluation, and agentic workflows.

In this wiki, LLMs are treated as the model substrate underneath agent core, runtime, memory, and harness design.

## Why it matters

- It keeps model-level capability separate from [[agent-core|Agent Core]] and [[agent-runtime|Agent Runtime]].
- It anchors research on reasoning, pretraining data, evaluation, safety, and domain-specific application.
- It connects general model progress to practical agent-system architecture.

## Source References

- `baidu-sync:af6f10bceaf5` — DeepSeek_V3.pdf
- `baidu-sync:ec03320bb577` — DeepSeek-R1 Incentivizing Reasoning Capability in LLMs via.pdf
- `baidu-sync:f6f877e5a8c6` — PretrainingDatasetsTrend.pdf
- `baidu-sync:60432948ca7f` — Humanitys Last Exam.pdf
- `baidu-sync:1516a96b30f6` — LLMs for Spreadsheet and Table Construction - Landscape and Data.pdf
- `baidu-sync:d56d59d20fc6` — Cognitive LLMs Towards Integrating Cognitive Architectures and Large.pdf
- `baidu-sync:d46e1aa8510b` — TELEClass Taxonomy Enrichment and LLM-Enhanced.pdf

## Related topics

- [[agent-core|Agent Core]]
- [[function-calling-and-tool-use|Function Calling and Tool Use]]
- [[llm-safety-interpretability|LLM Safety and Interpretability]]
- [[self-evolving-ai-systems|Self-Evolving AI Systems]]

## Open questions

- Which capabilities should be attributed to the base model, and which to the surrounding harness?
- How should reasoning benchmarks be interpreted when agents can use tools and memory?
- Which LLM weaknesses are best addressed through data, inference-time control, runtime design, or evals?
