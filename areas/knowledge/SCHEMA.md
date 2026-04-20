# Knowledge Area Schema

> Purpose: manage ongoing technical reading, retained article notes, and curated knowledge assets that belong to AF's continuous knowledge-development area.
> Owner: AF
> Last updated: 2026-04-20

## Why this is an area

This is not just a storage bucket.
It is an ongoing responsibility:
- capture what is worth retaining
- preserve article-level notes
- curate and connect technical knowledge over time

Weak-signal items still belong in `resources/leads/`.
Only retained or curated knowledge notes belong here.

## Preferred skill routing

- `wechat-article-wiki-ingest`:
  - use for `mp.weixin.qq.com` link ingestion, fallback note creation, and article-corpus maintenance
- `second-brain-wiki-architecture`:
  - use when reorganizing the knowledge area, splitting collections, or normalizing the area's structure

## Current structure

```text
knowledge/
├── SCHEMA.md
├── index.md
├── wechat-public-account-articles.md
├── wechat-articles/
└── 99-change-log.md
```

## Ownership rules

### This area owns
- retained article entry pages
- per-article fallback notes or extracted notes
- topic-level knowledge collections that are part of continuous knowledge curation

### This area does not own
- weak-signal leads that have not been curated yet
- cross-area backlog management
- one-off project notes that belong to a finite project

## Workflow rule

1. Capture weak signals in `resources/leads/`
2. Track follow-up status in `dashboards/research-backlog.md`
3. When a note becomes worth retaining, promote it into `areas/knowledge/`
4. Keep the collection entry page and note corpus linked

## Expansion rule

When this area grows, add new collections alongside the current WeChat corpus, for example:
- topic-specific note sets
- synthesis notes
- curated reading maps

Do not force the knowledge area to copy the fitness area's numeric tracking layout.
This area should keep a structure that matches knowledge curation work.
