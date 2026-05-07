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

## Original Files In Wiki

- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/LLMs/2024/DeepSeek_V3.pdf|DeepSeek_V3.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/LLMs/2025/DeepSeek-R1 Incentivizing Reasoning Capability in LLMs via.pdf|DeepSeek-R1 Incentivizing Reasoning Capability in LLMs via.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/DeepResearch/PretrainingDatasetsTrend.pdf|PretrainingDatasetsTrend.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/LLMs/2025/Humanitys Last Exam.pdf|Humanitys Last Exam.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/LLMs/2024/LLMs for Spreadsheet and Table Construction - Landscape and Data.pdf|LLMs for Spreadsheet and Table Construction - Landscape and Data.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/LLMs/2024/Cognitive LLMs Towards Integrating Cognitive Architectures and Large.pdf|Cognitive LLMs Towards Integrating Cognitive Architectures and Large.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/LLMs/2024/TELEClass Taxonomy Enrichment and LLM-Enhanced.pdf|TELEClass Taxonomy Enrichment and LLM-Enhanced.pdf]]

## Related topics

- [[agent-core|Agent Core]]
- [[function-calling-and-tool-use|Function Calling and Tool Use]]
- [[llm-safety-interpretability|LLM Safety and Interpretability]]
- [[self-evolving-ai-systems|Self-Evolving AI Systems]]

## Open questions

- Which capabilities should be attributed to the base model, and which to the surrounding harness?
- How should reasoning benchmarks be interpreted when agents can use tools and memory?
- Which LLM weaknesses are best addressed through data, inference-time control, runtime design, or evals?
