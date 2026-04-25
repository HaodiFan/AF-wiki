# Knowledge Area Schema

> Purpose: manage ongoing technical reading, retained article notes, and curated knowledge assets that belong to AF's continuous knowledge-development area.
> Owner: AF
> Last updated: 2026-04-25

## Why this is an area

This is not just a storage bucket.
It is an ongoing responsibility:
- capture what is worth retaining
- preserve article-level notes
- curate and connect technical knowledge over time

Weak-signal items still belong in `resources/leads/`.
Only retained or curated knowledge notes belong here.

## Preferred skill routing

- `wechat-public-account-reader`:
  - use for `mp.weixin.qq.com` link extraction and wiki intake
  - save URL-only or blocked extractions as leads first
  - promote into research, retained article notes, topics, or maps only when the lifecycle rules justify it
- `second-brain-wiki-architecture`:
  - use when reorganizing the knowledge area, splitting collections, or normalizing the area's structure

## Current structure

```text
knowledge/
├── SCHEMA.md
├── index.md
├── maps/
├── topics/
├── anthonydb-research/
├── wechat-public-account-articles.md
├── wechat-articles/
└── 99-change-log.md
```

## Knowledge graph lifecycle

The knowledge graph is not the first capture layer.

Use this lifecycle:

```text
resources/leads/ -> resources/research/ -> areas/knowledge/topics/ -> areas/knowledge/maps/
```

### 1. Lead capture

Use `resources/leads/` when you see a term, article, product, repo, or idea that might matter later but is not yet researched.

Example:
- seeing the term "非理性繁荣 / Irrational Exuberance" with no time to dive in should create a lead, not a topic node

### 2. Research note

Use `resources/research/` when you investigate a captured lead and collect findings, sources, key points, or a provisional verdict.

Each research note should link back to its source lead.

### 3. Topic promotion

Promote into `areas/knowledge/topics/` only when the concept is durable enough to be part of the graph.

Promotion threshold:
- the concept is reusable across future reasoning
- the concept connects multiple notes
- the concept belongs on a map
- the concept needs a stable definition, related topics, and open questions

Do not create a topic node for every interesting term.

### 4. Map curation

Use `areas/knowledge/maps/` for curated entry points over topic clusters.

A map should connect durable topic nodes and a small set of anchor notes. It should not be a dumping ground for every related title.

## Ownership rules

### This area owns
- retained article entry pages
- per-article fallback notes or extracted notes
- topic-level knowledge collections that are part of continuous knowledge curation
- curated historical research imports that are dense enough to remain useful after migration
- durable topic nodes in `topics/`
- curated topic maps in `maps/`

### This area does not own
- weak-signal leads that have not been curated yet
- cross-area backlog management
- one-off project notes that belong to a finite project

## Workflow rule

1. Capture weak signals in `resources/leads/`
2. Track follow-up status in `dashboards/research-backlog.md`
3. When a note becomes worth retaining, promote it into `areas/knowledge/`
4. Keep the collection entry page and note corpus linked
5. Promote a concept into `topics/` only after it passes the topic threshold
6. Add it to a `maps/` entry only when it improves a curated graph view

## Expansion rule

When this area grows, add new collections alongside the current WeChat corpus, for example:
- historical research imports from older vaults
- topic-specific note sets
- synthesis notes
- curated reading maps

Do not force the knowledge area to copy the fitness area's numeric tracking layout.
This area should keep a structure that matches knowledge curation work.

## Obsidian graph rule

The default graph should emphasize:
- `areas/knowledge/topics/`
- `areas/knowledge/maps/`
- curated research notes
- retained article notes

The default graph should hide:
- `areas/knowledge/anthonydb-research/originals/`
- unresolved historical `KP - ...` links
- orphan notes
- scaffold files such as `index`, `SCHEMA`, and `99-change-log`
