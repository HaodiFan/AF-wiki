---
title: "Hermes Memory × AF-wiki Integration Architecture / Hermes 记忆与 AF-wiki 集成架构"
type: topic
area: knowledge
status: active
aliases:
  - Hermes Memory Integration
  - AF-wiki Memory Architecture
  - Holographic Memory Integration
tags:
  - area/knowledge
  - topic/agent-memory
  - topic/hermes-agent
  - topic/personal-knowledge-systems
  - type/topic
  - wiki/af
---
# Hermes Memory × AF-wiki Integration Architecture / Hermes 记忆与 AF-wiki 集成架构

## Definition

This note defines how Hermes Agent memory should integrate with AF-wiki.

The key rule is:

- **AF-wiki remains the canonical, human-readable source of truth**
- **Hermes built-in memory remains a compact routing and preference layer**
- **Holographic memory, if enabled, should be treated as a derived retrieval/index layer rather than a second canonical knowledge base**

In other words, the goal is not to move AF-wiki into Hermes memory, but to let Hermes use memory systems to navigate, summarize, and retrieve from AF-wiki more effectively.

## Why this matters

- It avoids creating two competing "truth sources" for long-term memory.
- It preserves the existing AF-wiki design principle that markdown remains canonical.
- It lets Hermes answer faster and more consistently without replacing the wiki's curation workflow.
- It fits the current AF-wiki evolution baseline: `sync + doctor + briefing` before heavier semantic infrastructure.

## Current architecture decision

### 1. AF-wiki as canonical memory

AF-wiki owns:

- durable personal context
- long-term plans
- retained knowledge notes
- area-specific operating context
- curated research outputs
- stable definitions, maps, and topic relationships
- auditable historical reasoning and change logs

Canonical rule:

- if a fact matters enough to be inspected, edited, versioned, or audited by a human, AF-wiki should own it

### 2. Hermes built-in memory as lightweight preference/routing memory

Hermes built-in memory should store only compact, stable facts that reduce repeated steering.

Examples:

- user response-style preferences
- stable repo / wiki locations
- durable routing preferences
- environment facts that are repeatedly useful
- a small number of operating conventions

Rule:

- built-in memory should remain small, declarative, and high-value
- it should not become a shadow wiki

### 3. Holographic memory as derived retrieval memory

If Holographic memory is enabled, it should be treated as:

- a derived fact index
- a fast recall layer
- an entity / relation / probe layer
- an optional reasoning accelerator for facts already grounded in AF-wiki

It should **not** be treated as a second primary place where durable knowledge is authored.

## Recommended three-layer model

```text
AF-wiki markdown
  -> canonical knowledge / plans / schemas / curated notes

Hermes built-in memory
  -> compact user preferences and durable routing facts

Holographic memory
  -> derived fact store indexed from selected AF-wiki notes
```

This means:

- **wiki = truth**
- **built-in memory = compact orientation**
- **holographic = retrieval acceleration**

## Operational priority order

When Hermes needs context, the preferred order is:

1. **Built-in memory** for compact user preferences and stable routing rules
2. **AF-wiki** for long-term content, domain context, and canonical knowledge
3. **Holographic memory** for faster probe / related / reason style recall over facts derived from AF-wiki

Interpretation:

- memory should help Hermes know **where to look**
- AF-wiki should remain the place that defines **what is true**
- Holographic memory should help Hermes recover **what is likely relevant** more quickly

## What should be synchronized into Holographic memory

Only durable, reusable facts should be synchronized.

### Good candidates

#### Fitness

- `areas/fitness/00-profile.md`
- `areas/fitness/01-goals.md`
- `areas/fitness/02-current-plan.md`
- `areas/fitness/03-decision-rules.md`

Use cases:

- profile facts
- goal state
- stable plan assumptions
- durable decision rules

#### Work

- `areas/work/00-active-context.md`

Use cases:

- stable operating assumptions
- recurring work context
- team / role / responsibility anchors

#### Knowledge

- `areas/knowledge/topics/*.md`
- selected synthesis notes
- selected durable map-note summaries

Use cases:

- concept definitions
- related topics
- entity / topic relationships
- open questions worth probing later

#### Governance / routing notes

- `SCHEMA.md`
- `areas/index.md`
- selected `areas/<area>/SCHEMA.md`

Use cases:

- canonical placement rules
- area routing rules
- durable structure decisions

## What should not be synchronized blindly

These should generally stay out of the Holographic fact layer unless intentionally summarized first:

- daily logs in raw form
- transient chat notes
- weak-signal leads that have not been curated
- unfinished scratch research
- large raw article copies
- high-churn numeric tracking details
- temporary plans likely to change within days

Reason:

- otherwise the fact store degrades into a noisy event log instead of a useful durable memory index

## Recommended integration pattern

### Pattern A: AF-wiki primary, memory secondary

This is the default recommendation.

- continue using AF-wiki as the canonical system
- keep Hermes built-in memory enabled for compact stable facts
- use Holographic memory only as an enhancement layer when it clearly improves recall

This pattern fits the current AF-wiki design philosophy and keeps the architecture legible.

### Pattern B: AF-wiki -> Holographic sidecar sync

Preferred technical shape if Holographic memory is adopted:

```text
AF-wiki notes
  -> extract durable facts
  -> normalize category / tags / entities
  -> write into Holographic fact store
```

This makes Holographic memory a **derived index** rather than a competing note system.

## Suggested implementation path

### Phase 1: keep current canonical structure unchanged

No migration of primary content.

Continue with:

- AF-wiki as canonical
- Hermes built-in memory for compact preferences
- sidecar-style infra thinking

### Phase 2: add AF-wiki memory sync as a derived utility

A natural location is:

- `infra/indexing/af_wiki_memory_sync.py`

Suggested responsibility:

- scan selected notes
- extract durable facts
- normalize entities / categories / tags
- write into a Holographic-compatible fact store
- optionally emit a compact sync report

### Phase 3: integrate with doctor / briefing style maintenance

Possible future additions:

- sync status checks in doctor-style tools
- freshness / drift audit between wiki and derived memory
- periodic sync jobs
- compact memory briefing output for Hermes runtime use

## Design rules

### Rule 1: no double-canonical storage

Do not let the same durable fact be independently authored in both AF-wiki and Holographic memory.

Preferred rule:

- author in AF-wiki
- derive into Holographic memory

### Rule 2: memory should compress, not replace

Hermes memory layers should reduce lookup cost and steering overhead.
They should not replace the wiki's curation and governance model.

### Rule 3: synchronization should be selective

Not every note deserves indexing into derived memory.
Only notes that provide repeated leverage should be synchronized.

### Rule 4: wiki lifecycle stays authoritative

The knowledge lifecycle remains:

```text
resources/leads/ -> resources/research/ -> areas/knowledge/topics/ -> areas/knowledge/maps/
```

Derived memory should sit **after** durable promotion, not before it.

## Practical usage model for Hermes

A good working model is:

- use built-in memory to remember the user's stable preferences and architecture choices
- use AF-wiki to ground substantive answers
- use Holographic memory to accelerate entity-based or relation-based recall once a derived sync exists

This keeps Hermes aligned with the existing AF-wiki operating philosophy instead of encouraging a parallel memory universe.

## Related topics

- [[agent-memory|Agent Memory / 智能体记忆]]
- [[agent-core|Agent Core / 智能体核心]]
- [[agent-runtime|Agent Runtime / 智能体运行时]]
- [[data-management|Data Management / 数据管理]]

## Open questions

- What is the minimum useful fact schema for AF-wiki -> Holographic sync?
- Should each area define its own extraction rules, or should there be one common extractor with per-area adapters?
- How should freshness / drift between markdown and derived memory be audited?
- Which Hermes operations should query AF-wiki directly first, and which should consult a derived memory index first?
