---
type: lead
status: captured
priority: high
source_type: article
captured_on: 2026-05-25
tags:
  - lead
  - hermes-agent
  - self-evolving-ai
  - dspy
  - gepa
  - iclr
  - article
  - wechat
---
# Hermes Agent 自演化登上 ICLR 2026 Oral：DSPy + GEPA 算法揭秘——让 Agent 自己进化的工程实现

## Basic Info
- Type: lead
- Title: Hermes Agent 自演化登上 ICLR 2026 Oral：DSPy + GEPA 算法揭秘——让 Agent 自己进化的工程实现
- Captured on: 2026-05-25
- Status: captured
- Priority: high
- Source type: article
- Source: 用户提供的公众号文章全文
- Seen via: Feishu DM

## Why it caught my attention
- 这是一个高信号 lead，因为它把 Hermes Agent 的“自演化”能力明确框定为一个可工程实现的方法论，而不只是产品卖点。
- 文中把 DSPy 与 GEPA 放在同一个叙事框架中，适合作为后续研究 Agent self-evolution、prompt optimization、harness optimization 的入口。
- 它同时连接产品、研究、评测、prompt engineering 和 runtime / harness 设计，具备较高的知识图谱连接价值。

## Summary
- 文章核心主张：Hermes Agent 的自演化机制可以理解为在不重训底层模型的前提下，对 prompt、tool description、skill、system prompt 乃至受测试约束的代码层做搜索与优化，让 agent 在使用中持续变强。
- 算法叙事核心是 DSPy + GEPA：DSPy 负责把 prompt 工程变成可编程优化问题，GEPA 负责多目标遗传搜索与 Pareto 最优前沿选择。
- 文章强调 Hermes 的差异化在于：优化对象不仅是 prompt，还包括 skill、tool description、system prompt，甚至可能扩展到受测试保护的代码演化。
- 文中还提出若干开放问题，例如跨模型迁移性、进化上限、自演化失控风险等。

## Keywords
- Hermes Agent
- self-evolution
- DSPy
- GEPA
- Genetic-Pareto Prompt Evolution
- prompt optimization
- agent harness
- agent runtime
- tool description evolution
- skill evolution
- ICLR 2026 Oral

## Research questions
- 文章中的关键事实（ICLR 2026 Oral、仓库名、实验结果）与官方来源是否完全一致？
- Hermes 的自演化更适合被归类为 prompt optimization、agent harness engineering，还是 runtime-level self-improvement？
- 哪些结论值得沉淀成 durable topic，哪些仅适合作为文章叙事保留？
- 是否需要后续补一篇 deep research note，对 DSPy、GEPA、Hermes self-evolution 和同类方案做系统对比？

## Next action
- 已从该 lead 提炼并沉淀 topic note：[[../../areas/knowledge/topics/hermes-agent-self-evolution|Hermes Agent Self-Evolution / Hermes Agent 自演化]]
- 如后续需要，可继续补官方 source verification、OpenReview / GitHub / DSPy 文档链接，或升级为 deep research。

## Links
- Promoted topic: [[../../areas/knowledge/topics/hermes-agent-self-evolution|Hermes Agent Self-Evolution / Hermes Agent 自演化]]
- Related project/area/resource: [[../../areas/knowledge/topics/self-evolving-ai-systems|Self-Evolving AI Systems / 自演化 AI 系统]]
- Related project/area/resource: [[../../areas/knowledge/topics/agent-harness-engineering|Agent Harness Engineering / 智能体 Harness Engineering]]
- Related project/area/resource: [[../../areas/knowledge/topics/agent-runtime|Agent Runtime / 智能体运行时]]

## Raw notes
- 用户要求：“这个文章录入，关于自进化”
- 后续纠正定位：“这篇属于lead”
- 说明：topic note 用于沉淀可复用知识；本文作为来源文章本身，应保留为 lead。
