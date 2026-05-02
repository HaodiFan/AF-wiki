---
title: Opencode Architecture / Opencode 架构
type: topic
area: knowledge
status: active
aliases:
  - Opencode Architecture
  - Opencode 架构
  - Opencode
  - KP - Opencode
tags:
  - area/knowledge
  - topic/agent-systems
  - topic/opencode-architecture
  - type/topic
  - wiki/af
---
# Opencode Architecture / Opencode 架构

## Definition

Opencode architecture is the wiki topic for source organization, build coordination, contract generation, and runtime/workflow evolution in Opencode-like systems.

The durable point is the architecture ladder: source layout, build graph, artifact packaging, schema-first contracts, and pipeline-centric runtime.

## Why it matters

- It prevents architecture discussions from collapsing into "monorepo vs multi-repo."
- It gives a maturity model for systems that mix apps, tools, generated contracts, and runtime workflows.
- It connects engineering organization choices to [[workflow-runtime|Workflow Runtime]] and [[agent-runtime|Agent Runtime]] design.

## Connected notes

- [[../anthonydb-research/opencode-system-architecture-patterns-Opencode系统架构模式|Opencode System Architecture Patterns]] — primary retained note for the architecture ladder.

## Related topics

- [[workflow-runtime|Workflow Runtime]]
- [[agent-runtime|Agent Runtime]]
- [[openclaw|OpenClaw]]

## Open questions

- Which maturity layer is actually needed for current AF repos: source workspace, build graph, schema contracts, or executable workflow?
- How should generated contracts and runtime flow definitions be versioned?
