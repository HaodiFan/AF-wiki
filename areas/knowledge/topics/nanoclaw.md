---
title: NanoClaw / Nanobot
type: topic
area: knowledge
status: active
aliases:
  - NanoClaw
  - Nanobot
  - nanobot
  - KP - NanoClaw
  - KP - nanobot
tags:
  - area/knowledge
  - topic/agent-systems
  - topic/nanoclaw
  - type/topic
  - wiki/af
---
# NanoClaw / Nanobot

## Definition

NanoClaw / Nanobot represents the minimal-loop, Python-first agent-core pattern in this wiki.

The key idea is a small, readable async loop with direct tool iteration, simple file-based memory, low overhead, and high local hackability.

## Why it matters

- It is the fastest path for prototyping agent behavior before operational complexity justifies a runtime platform.
- It provides a contrast with [[openclaw|OpenClaw]] and gateway/control-plane designs.
- It keeps the focus on core loop clarity, local modification, and low coordination cost.

## Connected notes

- [[../anthonydb-research/openclaw-vs-nanoclaw-architecture-selection-OpenClaw与NanoClaw架构选型|OpenClaw vs NanoClaw Architecture Selection]] — primary retained comparison note.

## Related topics

- [[agent-core|Agent Core]]
- [[agent-runtime|Agent Runtime]]
- [[agent-memory|Agent Memory]]
- [[openclaw|OpenClaw]]

## Open questions

- How long can a minimal-loop agent stay maintainable before session, policy, and observability concerns force a runtime upgrade?
- Which parts of a minimal-loop design should remain intentionally explicit instead of abstracted away?
