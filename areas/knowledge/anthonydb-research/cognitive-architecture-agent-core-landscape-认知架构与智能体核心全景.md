---
title: Cognitive Architecture Agent-Core Landscape / 认知架构与智能体核心全景
aliases:
  - cognitive-architecture-agent-core-landscape
  - 认知架构与智能体核心全景
  - 智能体核心全景
languages:
  - en
  - zh
---
# Cognitive Architecture Agent-Core Landscape / 认知架构与智能体核心全景

> Curated historical research note.
> 历史研究策展稿，含中英双语摘要。
> Imported on / 归档时间: 2026-04-20

## Source / 原文

Archived in current wiki / 当前 wiki 原文:
- [[originals/Cognitive Architecture Agent Core 研究]]

## Chinese Summary / 中文摘要

### 保留原因

- 这篇笔记不是纯文献罗列，而是把不同传统下“agent core”到底指什么做了一个紧凑的比较框架。
- 它还用 Claude Code 这种现代 tool-calling agent 作为基线，方便把经典认知架构和今天的 agent runtime 放到同一张图里看。

### 核心结论

1. “智能体核心”并不是一个跨传统稳定不变的概念，不同架构对核心的定义差异很大。
2. Claude Code 可以作为现代基线：`policy = model call`、`working memory = messages`、`action branch = tool use`、`environment update = tool results`。
3. 历史上的关键分叉包括：`Soar / ACT-R` 的显式控制循环、`LIDA` 的认知广播、`CLARION` 的双层知识系统、`HTM` 的时间学习底座，以及 `0-Architecture` 的演化式功能内核。
4. 研究优先级本身也值得保留：先深挖 `Soar / ACT-R / CLARION / LIDA`，再看 `HTM`，`0-Architecture` 先留在理论层。
5. 这篇笔记的长期价值是比较语言，而不是直接实现指南。

### 当前价值

- 它能把“模型 + 工具循环”系统和经典认知控制系统区分开来，避免用一套错误 taxonomy 硬套所有 agent。
- 当你以后从更概念层重新看 agent-core 设计时，这会是一篇很稳的桥接笔记。

### 后续动作

- 如果后面要在 wiki 里单独建立 agent-core 地图，这篇应该作为 anchor note 之一。

## English Notes

## Why kept

- This note is not just a literature dump.
- It gives a compact taxonomy of what different traditions mean by "agent core," using Claude Code as a modern tool-calling baseline.

## Retained takeaways

1. "Agent core" is not a stable concept across traditions.
   The old note explicitly argues that different architectures define the core in fundamentally different ways.

2. Claude Code is a useful modern baseline:
   - policy = model call
   - working memory = messages
   - action branch = tool use
   - environment update = tool results
   This makes it a clean reference point for modern tool-calling agents.

3. The key historical architecture split is:
   - `Soar` / `ACT-R`: explicit control-loop cores
   - `LIDA`: cognitive broadcast loop
   - `CLARION`: dual-layer knowledge/event system
   - `HTM`: online temporal learning substrate
   - `0-Architecture`: evolving functional kernel

4. The note's own first-round conclusion is still useful as a research priority order:
   - deep-dive first: `Soar`, `ACT-R`, `CLARION`, `LIDA`
   - then `HTM`
   - keep `0-Architecture` at the theory layer until code artifacts become clearer

5. The durable value here is comparative language, not direct implementation guidance.
   It helps distinguish "model-tool loop" systems from classical cognitive-control systems without forcing them into one false taxonomy.

## Why it matters to the current wiki

- This is a strong bridge note between current agent engineering and classical cognitive architecture research.
- It should remain useful whenever you revisit agent-core design from a deeper conceptual angle rather than only from product/runtime comparisons.

## Suggested follow-up

- If you later build a more formal agent-core map in this wiki, this note should become one of the anchor references.
