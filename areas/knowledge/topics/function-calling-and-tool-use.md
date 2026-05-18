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

## Source References

- `baidu-sync:afa55696a16f` — Toolformer Language Models Can Teach Themselves to Use Tools.pdf
- `baidu-sync:69765c615a48` — Gorilla Large Language Model Connected with Massive APIs.pdf
- `baidu-sync:d573ace33b8f` — ToolLLM Large Language Models Can Master 16000+ Real-world APIs.pdf
- `baidu-sync:b5dadcc148f7` — WebGPT Browser-assisted question-answering with human feedback.pdf
- `baidu-sync:c3c85cee356b` — Fastino Function Calling Datasets.pdf
- `baidu-sync:acddc702990a` — AI4Science中function calling数据集与自动化实验系统调研.pdf

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
