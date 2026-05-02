---
title: OpenClaw
type: topic
area: knowledge
status: active
aliases:
  - OpenClaw
  - KP - OpenClaw
tags:
  - area/knowledge
  - topic/agent-systems
  - topic/openclaw
  - type/topic
  - wiki/af
---
# OpenClaw

## Definition

OpenClaw is used in this wiki as the reference point for a gateway-centric, policy-rich agent runtime and control-plane style.

The important concept is not only the project name, but the architecture pattern: long-lived gateway, typed tools, session management, observability, sandboxing, and control-plane separation.

## Why it matters

- It represents the heavier side of the local/personal agent runtime tradeoff.
- It gives a contrast case against [[nanoclaw|NanoClaw]] and minimal-loop designs.
- It is useful when evaluating whether a system needs operational controls before it exposes tools and memory to an agent.

## Connected notes

- [[../anthonydb-research/openclaw-vs-nanoclaw-architecture-selection-OpenClaw与NanoClaw架构选型|OpenClaw vs NanoClaw Architecture Selection]] — primary retained comparison note.
- [[../anthonydb-research/opencode-system-architecture-patterns-Opencode系统架构模式|Opencode System Architecture Patterns]] — related architecture maturity lens.

## Related topics

- [[agent-runtime|Agent Runtime]]
- [[agent-core|Agent Core]]
- [[agent-memory|Agent Memory]]
- [[nanoclaw|NanoClaw]]
- [[workflow-runtime|Workflow Runtime]]

## Open questions

- Which OpenClaw-style controls are necessary for a personal local agent, and which are premature overhead?
- What is the migration path from minimal loop to gateway/control-plane architecture?
