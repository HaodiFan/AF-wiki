---
title: Agent Memory Infrastructure Survey (2024-2026) / 智能体记忆基础设施综述（2024-2026）
aliases:
  - agent-memory-infrastructure-survey-2024-2026
  - 智能体记忆基础设施综述
  - 智能体记忆基础设施综述（2024-2026）
languages:
  - en
  - zh
tags:
  - area/knowledge
  - collection/anthonydb-research
  - topic/agent-memory
  - topic/agent-systems
  - type/research-note
  - wiki/af
---
# Agent Memory Infrastructure Survey (2024-2026) / 智能体记忆基础设施综述（2024-2026）

> Curated historical research note.
> 历史研究策展稿，含中英双语摘要。
> Imported on / 归档时间: 2026-04-20

## Source / 原文

Archived in current wiki / 当前 wiki 原文:
- [[originals/Agent Memory Infrastructure Research Survey 2024–2026]]

## Topics / Concepts

- [[../topics/agent-memory|Agent Memory / 智能体记忆]]
- [[../topics/agent-runtime|Agent Runtime / 智能体运行时]]

## Chinese Summary / 中文摘要

### 保留原因

- 这是旧资料里研究密度最高的一批笔记之一，不是简单摘要，而是把智能体记忆的设计空间、评测框架、生命周期和治理问题一起铺开。
- 对今天继续评估 agent runtime、memory layer 和长期运行系统依然直接有用。

### 核心结论

1. 记忆应该被当成基础设施，而不是可有可无的附加功能。
2. 设计空间主要分成两条轴：表示方式与控制方式。
3. 长上下文并没有替代记忆架构，问题只是从“能否放进去”变成“能否正确检索、压缩、更新和治理”。
4. 一个成熟的记忆层通常需要显式支持 `ADD / UPDATE / DELETE / MERGE / LINK / VERSION`。
5. 记忆质量和治理不可分割，陈旧记忆、幻觉记忆、投毒和隐私泄露都应被视为一等风险。
6. 评测不能只看检索命中率，还要覆盖对话型记忆、环境/agent 型记忆，以及更新正确性和幻觉等失败模式。

### 当前价值

- 这篇笔记给当前 wiki 提供了一套比较记忆系统的公共词汇，不会把讨论压扁成“向量库 vs 上下文窗口”。
- 后续讨论 OpenClaw、Nanobot、local-first memory 或 personal data center 时，都可以把它当作底层参考。

### 后续动作

- 可以把当前 agent runtime 的 memory model 按这套 taxonomy 重新对照一遍。
- 评估本地优先记忆系统时，要单独把治理部分重新拉出来。

## English Notes

## Why kept

- This is one of the densest research notes in the old vault.
- It is not just a digest: it maps the design space, benchmarks, lifecycle, and governance issues of agent memory infrastructure.
- It remains directly useful for evaluating current agent runtimes and memory systems.

## Retained takeaways

1. Memory should be treated as **infrastructure**, not an optional feature.
   Long-running agents need state continuity, experience reuse, personalization, and bounded-cost retrieval under unreliable long-context behavior.

2. The core design space has two axes:
   - representation: retrieval, structured, graph, reflective, hierarchical, world-model memory
   - control: retrieval control, construction control, utility control, and meta-control

3. Long context does not remove the need for memory architecture.
   The practical problem shifts from "can the model see more tokens" to "can it retrieve, compress, update, and govern state correctly."

4. A useful reference architecture converges on explicit memory operations:
   - `ADD`
   - `UPDATE`
   - `DELETE`
   - `MERGE`
   - `LINK`
   - `VERSION`

5. Memory quality is inseparable from governance.
   The note explicitly treats stale memories, hallucinated memories, poisoning, and privacy leakage as first-class infrastructure risks rather than edge cases.

6. Evaluation should cover more than retrieval accuracy.
   The important benchmark split is dialogue-centric memory, environment/agent-centric memory, and failure-mode benchmarks such as hallucination and update correctness.

## Why it matters to the current wiki

- This note is a durable reference for future work on agents, memory systems, OpenClaw, Nanobot, and similar runtimes.
- It gives a reusable vocabulary for comparing memory implementations without reducing everything to "vector DB vs context window."

## Suggested follow-up

- Compare the memory model of current agent runtimes against this lifecycle and control taxonomy.
- Revisit the governance section when evaluating local-first memory systems or personal data center concepts.
