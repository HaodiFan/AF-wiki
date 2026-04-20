# Areas Index

> Purpose: register every active area module, explain what it owns, and define the default routing logic for area-specific skills and workflows.
> Last updated: 2026-04-20

## Area rules

`areas/` is the responsibility layer of LeadFlow.

Rules:
- each area is an ongoing module
- each area can define its own internal structure
- each area must expose at least:
  - `SCHEMA.md`
  - `index.md`
  - `99-change-log.md`
- adding a new area means creating `areas/<name>/`, defining its local schema, then registering it here

## Current areas

### Fitness
- Path: `areas/fitness/`
- Purpose: training, nutrition, recovery, weekly review, and decision memory
- Primary schema: [[fitness/SCHEMA]]
- Preferred skills:
  - `ai-fitness-coach-cn`
  - `personal-tracking-memory-architecture`

### Knowledge
- Path: `areas/knowledge/`
- Purpose: retained technical reading notes, article corpora, and ongoing knowledge curation
- Primary schema: [[knowledge/SCHEMA]]
- Preferred skills:
  - `wechat-article-wiki-ingest`
  - `second-brain-wiki-architecture`

### Work
- Path: `areas/work/`
- Purpose: ongoing work context, work-facing operating assumptions, and future work module expansion
- Primary schema: [[work/SCHEMA]]
- Preferred skills:
  - `second-brain-wiki-architecture`
  - area-specific work skills can be added later

## How to add a new area

1. Create `areas/<name>/`
2. Add:
   - `SCHEMA.md`
   - `index.md`
   - `99-change-log.md`
3. Define what the area owns and what it should not own
4. Add preferred skills or workflows in that area's `SCHEMA.md`
5. Register the new area here

## Routing rule for second-brain orchestration

When a high-level second-brain skill needs to act in this repo:
1. read this file first
2. choose the target area
3. read `areas/<area>/SCHEMA.md`
4. route to that area's preferred skill when one exists

This keeps the area layer dynamic without making the root wiki structure ambiguous.
