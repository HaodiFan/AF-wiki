---
title: "2026-04-24-feat-architecture-evolution-plan"
tags:
  - area/docs
  - wiki/af
---
# AF-wiki Architecture Evolution Plan

> Purpose: capture the next-stage architecture evolution for AF-wiki by absorbing the most useful ideas from GBrain **without** replacing AF-wiki's current LeadFlow / area-first markdown architecture.
> Status: proposed
> Created: 2026-04-24

## Executive summary

AF-wiki should **not** be turned into GBrain.

The right direction is:
- keep AF-wiki as the **human-readable, markdown-first, area-oriented second brain**
- add a lightweight **index / query / maintenance / automation sidecar layer**
- selectively borrow GBrain's strengths where they fit AF's actual workflow

In one sentence:

**AF-wiki remains the information-governance layer; a new sidecar runtime adds searchability, structure, and maintenance intelligence.**

---

## Current AF-wiki strengths to preserve

These are already correct and should stay canonical:

1. **Markdown as durable source of truth**
   - notes remain readable, editable, and versioned in Git
   - human inspection stays easy

2. **LeadFlow top-level architecture**
   - `areas/` for ongoing responsibilities
   - `resources/` for shared lead/research flow
   - `projects/` for bounded work
   - `archive/` for legacy and superseded material

3. **Area-first navigation and ownership**
   - `areas/index.md` as the registry
   - each area owns its own local schema and internal logic

4. **Two-stage research pipeline**
   - quick capture in `resources/leads/`
   - deep dive in `resources/research/`
   - promotion into the appropriate durable owner later

5. **Current-vs-target clarity**
   - `START-HERE.md`, root `SCHEMA.md`, and area schemas make the current usable structure explicit

These are not problems to solve; they are the foundation to build on.

---

## What GBrain is good at that AF-wiki can borrow

GBrain is strong not because its folders are better, but because it adds a strong runtime layer around memory.

The most valuable capabilities to borrow are:

1. **Automatic indexing**
   - changed markdown becomes queryable quickly

2. **Hybrid retrieval**
   - keyword + structural metadata + optional embeddings

3. **Structured entity and relationship extraction**
   - especially useful for work notes, people, orgs, decisions, and recurring topics

4. **Maintenance automation**
   - stale notes, broken links, orphan pages, incomplete flows

5. **Periodic briefings / operational summaries**
   - summarize what changed, what is stale, and what needs attention

6. **Progressive structuring**
   - start from text files, but derive machine-usable structure from them over time

---

## Design principle for AF-wiki evolution

The governing principle is:

> **Do not replace the markdown wiki with a database. Derive a lightweight machine layer from the markdown wiki.**

That means:
- markdown remains canonical
- database/index/search artifacts are derived and rebuildable
- the machine layer improves lookup, consistency checks, and cross-area synthesis
- directory structure remains optimized for human understanding, not for database normalization

---

# Target architecture: four-layer model

## Layer 1 — Canonical Markdown Knowledge Layer

This is the existing AF-wiki repo.

Canonical structure remains:

```text
AF-wiki/
├── inbox/
├── areas/
├── projects/
├── resources/
├── archive/
├── dashboards/
├── templates/
├── START-HERE.md
├── index.md
├── SCHEMA.md
└── log.md
```

This layer remains:
- human-readable
- git-versioned
- the source of truth

No database should become more authoritative than this layer.

---

## Layer 2 — Derived Index and Query Layer

Add a sidecar layer that scans markdown and builds queryable structure.

### Current repo status
- Initial sidecar wrappers now live under `infra/`
- `infra/indexing/af_wiki_sync.py` is the current canonical wrapper for markdown -> SQLite sync
- `infra/jobs/af_wiki_doctor.py` is the current Phase 1 doctor entrypoint for compact audit summaries
- `infra/jobs/af_wiki_briefing.py` is the first lightweight briefing entrypoint

### Goal

Turn AF-wiki from “well-organized files” into “well-organized files that are also easy to search, summarize, and audit.”

### Recommended implementation direction

Start with **SQLite** as the first derived index.

Why SQLite first:
- low operational burden
- local and fast
- enough for metadata, links, statuses, and even FTS
- easier to maintain than a full Postgres/pgvector stack at this stage

### Recommended locations

Preferred implementation choices:
- repo-visible scripts/config under `infra/`
- derived runtime cache outside the repo or under a clearly derived folder

For example:

```text
AF-wiki/
├── infra/
│   ├── indexing/
│   ├── search/
│   ├── jobs/
│   └── schema/
```

And/or a local cache such as:

```text
~/.af-wiki-cache/
```

### Initial derived objects

A minimum viable index should track:

- notes
  - path
  - title
  - area
  - layer (`area`, `resource`, `project`, `archive`, etc.)
  - note type (`lead`, `research`, `checkin`, `plan`, `decision`, etc.)
  - updated timestamp
- wikilinks / backlinks
- status fields for leads / research notes / operational notes
- lightweight entity mentions
- optional tags or inferred topic buckets

### Example minimum tables

- `notes`
- `links`
- `entities`
- `entity_mentions`
- `note_status`

### What this unlocks

Examples of future queries:
- which leads have not advanced for 21+ days?
- which research notes do not link back to an originating lead?
- which work topics have appeared repeatedly across multiple files?
- which notes are active in both `areas/work/` and `areas/knowledge/`?
- which daily fitness records are missing expected same-day supporting notes?

---

## Layer 3 — Selective Structure / Graph Layer

AF-wiki should not blindly adopt a universal entity graph for everything.

Instead, add structure **where it naturally helps**.

## 3A. Work area: strongest candidate for GBrain-style structuring

`areas/work/` is currently a scaffold and is the best place to borrow from GBrain.

### Why

Work memory naturally involves:
- people
- organizations
- projects
- meetings
- decisions
- recurring threads

These are the exact kinds of objects that benefit from structure and relationship extraction.

### Recommended gradual expansion

When real content volume justifies it, `areas/work/` can grow toward:

```text
areas/work/
├── SCHEMA.md
├── index.md
├── 00-active-context.md
├── people/
├── orgs/
├── projects/
├── meetings/
├── decisions/
├── threads/
└── 99-change-log.md
```

Important:
- this should be **usage-driven**, not prebuilt all at once
- only create subfolders when recurring notes actually appear

### Suggested promotion rules

Examples:
- a frequently recurring person may become `areas/work/people/<name>.md`
- a long-running external organization may become `areas/work/orgs/<name>.md`
- an important recurring discussion may become `areas/work/threads/<topic>.md`
- a consequential judgment may become `areas/work/decisions/YYYY-MM-DD-<slug>.md`

This would turn the work area into a true **operational memory layer** rather than only a thin context page.

---

## 3B. Knowledge area: topic graph, not CRM graph

`areas/knowledge/` should not copy GBrain's people/company-heavy model.

The more useful structure here is:
- topics / concepts
- source -> synthesis -> retained note progression
- lead -> research -> promoted note chain
- related-topic mapping

### Recommended capabilities

1. **Lead/research/promotion state model**
   - `captured`
   - `queued`
   - `researching`
   - `promoted`
   - `archived`

2. **Canonical backlink rules**
   - each research note should link back to its source lead
   - promoted notes should reference the research note or originating lead

3. **Topic maps**
   - introduce durable topic indexes once volume justifies them
   - examples: agents, memory infra, AI products, org design, research workflows

This makes the knowledge area more queryable without forcing it into an unnatural CRM shape.

---

## Layer 4 — Maintenance, Audit, and Briefing Layer

This is the most practical place to borrow GBrain-style operational intelligence.

The first version should be **simple cron + scripts**, not a complex autonomous runtime.

### Core idea

Add repeatable maintenance commands that continuously improve wiki quality.

### Initial maintenance functions

1. **Index refresh**
   - scan markdown
   - refresh SQLite index
   - update links and statuses

2. **Wiki doctor / maintain**
   - broken links
   - orphan notes
   - stale leads
   - research notes without source backlinks
   - area scaffolds missing expected files
   - outdated active context notes

3. **Periodic briefing**
   - recent high-signal changes
   - stale backlog items
   - cross-area topics worth promotion
   - work area active entities / threads
   - maintenance items needing cleanup

### Why this matters

This improves trust in the system without changing the primary authoring workflow.

---

# Area-specific recommendations

## Fitness

Fitness is already relatively mature and should borrow **less** from GBrain than the other areas.

### Recommended improvements

- consistency checks across same-day records
- plan vs actual comparison helpers
- completeness auditing
- lightweight historical indexing

### Avoid

- over-graphing fitness notes
- forcing entity-centric structure where tracking-centric structure already works better

Fitness should become more reliable and queryable, not more complex.

---

## Knowledge

The priority is not a huge new folder tree; it is a better **research-flow closure**.

### Recommended improvements

- explicit state machine for lead -> research -> retained note progression
- stronger backlinking between stages
- topic maps and promotion audit rules
- searchable index across leads, research notes, and retained knowledge

This helps the knowledge area evolve from a good collection into a better compounding research system.

---

## Work

This is the highest-value target for structural evolution.

### Recommended improvements

- gradually add note types for people, orgs, meetings, decisions, threads
- index recurring names and topics from `00-active-context.md` and future work notes
- create a future briefing workflow for work memory
- support entity-aware queries across work context

This is the area that can benefit the most from GBrain-like operational memory patterns.

---

# Recommended implementation phases

## Phase 1 — Sidecar Index + Doctor (highest priority)

### Goal

Improve queryability and maintenance without disturbing current wiki structure.

### Deliverables

- a local index refresh command
- SQLite schema for derived metadata
- wikilink extraction
- a `doctor` / `maintain` command with a small set of checks

### Example checks

- broken links
- orphan notes
- stale leads
- research notes missing source backlinks
- area folders missing expected entry files

### Why first

This gives immediate practical value at low risk.

---

## Phase 2 — Work and Knowledge Structure Upgrade

### Goal

Add structure where it actually helps.

### Deliverables

- gradual expansion rules for `areas/work/`
- state model for lead/research/promotion
- topic-map support for `areas/knowledge/`
- reporting across `resources/` and area promotion boundaries

### Why second

Once indexing exists, the system can support higher-quality structural evolution.

---

## Phase 3 — Semantic / Hybrid Retrieval

### Goal

Add stronger retrieval only after structure and workflows are stable.

### Deliverables

- optional embeddings for note bodies
- keyword + semantic hybrid search
- entity-aware ranking
- related-note recommendations

### Why third

Embeddings are useful, but not the first bottleneck. Structure and lifecycle clarity come first.

---

# Suggested initial commands / capabilities

These do not need to exist yet; they define the intended direction.

## Sync / index
- `af-wiki sync`
- scans markdown and refreshes derived index

## Health / maintenance
- `af-wiki doctor`
- reports structural and lifecycle issues

## Query
- `af-wiki query "..."`
- searches notes, metadata, and later embeddings

## Briefing
- `af-wiki briefing`
- summarizes recent changes, stale items, and likely next actions

---

# Success criteria

The evolution is successful if AF-wiki becomes:

1. **more queryable** without losing markdown simplicity
2. **more reliable** through automated audits
3. **better at cross-area synthesis**
4. **stronger in work memory** without overengineering other areas
5. **better at lead -> research -> promotion closure**
6. **incrementally more machine-readable** while staying human-first

---

# Final architectural stance

AF-wiki should not compete with GBrain by becoming a full agent memory operating system.

Instead, AF-wiki should evolve into:

> **a human-first LeadFlow second brain with a lightweight derived runtime for indexing, maintenance, and selective structure.**

That approach keeps the current strengths of AF-wiki while borrowing the highest-leverage ideas from GBrain.
