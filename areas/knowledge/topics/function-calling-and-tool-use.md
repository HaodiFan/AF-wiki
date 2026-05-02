---
title: Function Calling and Tool Use / 函数调用与工具使用
type: topic
area: knowledge
status: active
aliases:
  - Function Calling
  - Tool Use
  - Tool-Using LLMs
  - 函数调用
  - 工具使用
tags:
  - area/knowledge
  - topic/function-calling
  - topic/tool-use
  - type/topic
  - wiki/af
---
# Function Calling and Tool Use / 函数调用与工具使用

## Definition

Function calling and tool use cover the mechanisms by which LLMs and agents select, call, compose, and verify external tools, APIs, browsers, scientific instruments, or workflow steps.

This topic sits between model capability and runtime design: the model proposes tool actions, while the harness and runtime expose tools safely and verify outcomes.

## Why it matters

- Tool use is one of the main paths from language-only models to useful agents.
- It directly affects [[agent-runtime|Agent Runtime]], [[agent-harness-engineering|Agent Harness Engineering]], and [[workflow-runtime|Workflow Runtime]].
- Data quality and evaluation remain central because tool schemas alone do not guarantee correct tool behavior.

## Original Files In Wiki

- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Function_Calling/2023/Toolformer Language Models Can Teach Themselves to Use Tools.pdf|Toolformer Language Models Can Teach Themselves to Use Tools.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Function_Calling/2023/Gorilla Large Language Model Connected with Massive APIs.pdf|Gorilla Large Language Model Connected with Massive APIs.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Function_Calling/2023/ToolLLM Large Language Models Can Master 16000+ Real-world APIs.pdf|ToolLLM Large Language Models Can Master 16000+ Real-world APIs.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/NLP/Function_Calling/2021/WebGPT Browser-assisted question-answering with human feedback.pdf|WebGPT Browser-assisted question-answering with human feedback.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/AI4Science/Function_Calling/2024/Fastino Function Calling Datasets.pdf|Fastino Function Calling Datasets.pdf]]
- [[areas/knowledge/source-documents/baidu-sync/Research_Papers_Organized/AI4Science/Function_Calling/2024/AI4Science中function calling数据集与自动化实验系统调研.pdf|AI4Science中function calling数据集与自动化实验系统调研.pdf]]

## Related topics

- [[agent-core|Agent Core]]
- [[agent-runtime|Agent Runtime]]
- [[agent-harness-engineering|Agent Harness Engineering]]
- [[ontology|Ontology]]
- [[ai4science|AI4Science]]

## Open questions

- How much tool-routing logic belongs in the model versus the runtime?
- Which tool failures should become schema changes, guardrails, or eval cases?
- How should tool-use datasets reflect multi-step workflows rather than isolated calls?
