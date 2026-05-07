---
title: Ontology / 本体
type: topic
area: knowledge
status: active
aliases:
  - Ontology
  - Operational Ontology
  - Semantic Layer
  - Enterprise Ontology
  - 本体
  - 操作型本体
  - 企业本体
  - 语义层
  - 语义中层
tags:
  - area/knowledge
  - topic/ontology
  - topic/agent-systems
  - topic/data-management
  - type/topic
  - wiki/af
---
# Ontology / 本体

## Definition

Ontology is a formal, shared representation of a domain's concepts, relationships, constraints, and allowed meanings. In modern AI systems, the important shift is from descriptive ontology toward operational ontology: a governed semantic layer that exposes business objects, permissions, actions, state, and audit trails to humans, applications, and agents.

For agent systems, ontology is best treated as an external, explicit world model. It is not just a knowledge graph or schema; it defines what the business world means, what state can be read, which actions can be taken, who is allowed to take them, and how the resulting changes are traced.

## Why it matters

- It gives AI agents a stable business-object language instead of a loose list of APIs or SQL tables.
- It can combine semantic meaning, data access, permissions, actions, workflow, and audit into one interface layer.
- It reframes enterprise AI architecture: part of backend domain logic moves upward into a governed semantic/action layer, while lower-level services still handle performance, integration, storage, and specialized execution.
- It is a bridge between [[data-management|Data Management]], [[agent-runtime|Agent Runtime]], [[function-calling-and-tool-use|Function Calling and Tool Use]], and [[workflow-runtime|Workflow Runtime]].

## Key distinctions

| Term | Main responsibility |
|---|---|
| Schema | Defines how data is stored and organized. |
| Knowledge Graph | Stores connected facts, entities, and relationships. |
| Ontology | Defines the domain meaning, constraints, reusable concepts, and valid reasoning. |
| Operational Ontology | Adds actions, permissions, writeback, workflow, agent tools, audit, and runtime state. |

## Connected notes

- [[../../../resources/research/2026-04-26-ontology-modern-ai-systems-deep-research|Ontology在现代AI系统中的演化与应用]] — full-text deep research report.
- [[data-management|Data Management / 数据管理]] — data governance, provenance, compliance, and platform layer beneath ontology.
- [[agent-runtime|Agent Runtime / 智能体运行时]] — runtime layer that consumes ontology objects, actions, state, permissions, and traces.
- [[function-calling-and-tool-use|Function Calling and Tool Use / 函数调用与工具使用]] — narrower tool interface that ontology can subsume or coordinate.
- [[workflow-runtime|Workflow Runtime / 工作流运行时]] — durable execution layer that can be driven by ontology actions.

## Architecture lens

The practical architecture pattern is:

```text
data sources / models / external systems
        -> ontology layer
           (objects + properties + links + actions + logic + security)
        -> UI / apps / agents / automation / SDK
        -> writeback / audit / observability / workflow lineage
```

The minimum useful implementation should separate:

- data/query layer for objects, properties, links, and indexes
- action engine for validation, transactions, side effects, logging, and writeback
- agent adapter for object query, action invocation, retrieval context, application state, citations, and traces

## Open questions

- What is the minimum ontology layer worth building before the maintenance cost outweighs the benefit?
- Which domain logic should move into ontology actions, and which logic should remain in backend services?
- How should ontology schema evolution, data migration, permissions, and agent tool exposure be versioned together?
- Can lightweight semantic-layer standards evolve into operational ontology without recreating a full platform dependency?
