---
title: Opencode System Architecture Patterns / Opencode 系统架构模式
aliases:
  - opencode-system-architecture-patterns
  - Opencode系统架构模式
  - Opencode System Architecture Patterns
languages:
  - en
  - zh
tags:
  - area/knowledge
  - collection/anthonydb-research
  - topic/agent-systems
  - type/research-note
  - wiki/af
---
# Opencode System Architecture Patterns / Opencode 系统架构模式

> Curated historical research note.
> 历史研究策展稿，含中英双语摘要。
> Imported on / 归档时间: 2026-04-20

## Source / 原文

Archived in current wiki / 当前 wiki 原文:
- [[originals/Opencode System Arch - 20260125]]

## Topics / Concepts

- [[../topics/opencode-architecture|Opencode Architecture / Opencode 架构]]
- [[../topics/workflow-runtime|Workflow Runtime / 工作流运行时]]
- [[../topics/agent-runtime|Agent Runtime / 智能体运行时]]

## Chinese Summary / 中文摘要

### 保留原因

- 原笔记虽然短，但它抓住了一条很耐用的工程范式演进链，而不是某个一次性的实现细节。
- 对 agent runtime、工具系统和多端产品来说，它提供了一个判断复杂度升级时该换哪一层架构的紧凑框架。

### 核心结论

1. 这篇隐含着一条清晰的架构梯子：单体源码 -> 多 repo + 版本包 -> submodule/subtree 过渡 -> monorepo workspace -> build graph -> artifact-centric -> schema-first -> pipeline/workflow-centric runtime。
2. workspace 解决的是源码共置问题，但并不自动解决构建编排问题，下一步要进入 target/dependency 视角。
3. 一旦有多个 app 和共享包需要稳定组装，真正的协调单位就会从目录结构变成 build target 关系。
4. schema-first 的意义在于把共享真相放进显式 contract，再由它生成前后端与 runtime 需要的类型和模型。
5. pipeline-centric 系统把“可执行工作流”本身当主产物，这对 agent 系统尤其重要。
6. 这篇最值得保留的地方是，它把源码组织、构建可重复性、契约定义和 runtime 编排拆成了不同成熟层，而不是混成一个问题。

### 当前价值

- 对未来 `areas/work/` 的工程笔记、OpenClaw 风格 runtime，以及任何混合 tools、flows 和 generated contracts 的系统都很有参考价值。
- 它还能帮 AF 在讨论架构演化时，避免把问题压缩成“monorepo vs multi-repo”这种过窄二分。

### 后续动作

- 可以把 AF 当前各 repo 和 runtime 想法映射到这条梯子上，看现在真正缺的是哪一层成熟度。

## English Notes

## Why kept

- The original note is terse, but it captures a durable engineering-paradigm progression rather than a one-off implementation detail.
- It is useful as a compact architecture lens for agent runtimes, tool systems, and multi-surface products that outgrow simple repo layouts.
- The note complements current AF work because it explains how coordination pressure shifts the primary system boundary from source files to contracts and workflows.

## Retained takeaways

1. The source implicitly describes an architecture ladder:
   - monolithic source tree
   - multi-repo plus versioned packages
   - submodule or subtree as transitional coordination
   - monorepo workspace as source graph
   - build graph or target-based system
   - artifact-centric packaging
   - schema or contract-first generation
   - pipeline or workflow-centric runtime

2. Moving to a workspace solves source co-location, but does not by itself solve build orchestration.
   The next step is explicit dependency and target management rather than only "put everything in one repo."

3. Build-graph thinking matters once multiple apps and shared packages must be assembled predictably.
   The real unit of coordination becomes target relationships, not just directory structure.

4. Schema-first systems shift shared truth into explicit contracts.
   Flow, step, and node schemas can generate types and models across runtimes, reducing drift between frontend, backend, and runtime layers.

5. Pipeline-centric systems treat executable workflow as the primary artifact.
   This is especially relevant for agent systems, where the durable boundary is often a flow, step graph, or execution protocol rather than a traditional app module tree.

6. The note is best read as a progression of coordination strategies under growing system complexity.
   Source organization, build reproducibility, contract definition, and runtime orchestration are separate maturity layers rather than one design choice.

## Why it matters to the current wiki

- This is a good reference note for future work in `areas/work/`, OpenClaw-style runtimes, and any system that mixes tools, flows, generated contracts, and multiple delivery surfaces.
- It gives AF a reusable vocabulary for discussing architecture evolution without collapsing every decision into "monorepo vs multi-repo."

## Suggested follow-up

- Map current AF repos and runtime ideas onto this ladder to identify which maturity layer is actually needed now.
- When work-area notes start to grow, split source-layout choices from schema/runtime-orchestration choices instead of treating them as one problem.
