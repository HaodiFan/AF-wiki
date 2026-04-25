# AF Current Fitness Plan

> Effective date: 2026-04-24
> Current status: active plan reflects the latest user-provided plan version, while older plans should be archived under `plan-versions/`

## Current training-plan version
- Active version label: 2026-04-24 architecture-evolution / evo-memory plan v2
- Supersedes: 2026-04-11 fat-loss plan v1 as the main active plan lens for current wiki evolution work
- Versioning rule: when the user changes plans, preserve prior versions in `areas/fitness/plan-versions/` instead of overwriting history
- Coaching / system rule: recommendations should use the active version as the default baseline, but adapt to actual recovery, adherence, and recent completed sessions

## Current plan focus
### Primary objective
- Keep AF-wiki as the human-readable, markdown-first, area-oriented second brain
- Add a lightweight sidecar runtime for indexing, query, maintenance, and automation instead of replacing the wiki with a database-centric system

### Four-layer target model
1. Canonical markdown knowledge layer remains the source of truth
2. Derived index and query layer is built from markdown, with SQLite as the first practical index
3. Selective structure / graph layer is added only where it creates real leverage
4. Maintenance, audit, and briefing layer improves trust and operational visibility through repeatable scripts/jobs

### Area-specific priority for memory upgrade
- Fitness: improve consistency checks, plan-vs-actual comparison helpers, completeness auditing, and lightweight historical indexing; avoid over-complicating the current tracking-first structure
- Work: highest-value target for stronger operational memory, including recurring people / org / meeting / decision / thread note types when usage justifies them
- Knowledge: strengthen lead -> research -> retained-note closure, backlinking, topic maps, and searchable cross-stage indexing

## Recommended implementation phases
### Phase 1 — Sidecar Index + Doctor
- Local index refresh command
- SQLite schema for derived metadata
- Wikilink extraction
- `doctor` / `maintain` command with checks such as broken links, orphan notes, stale leads, missing backlinks, and missing area entry files

### Phase 2 — Work + Knowledge structure upgrade
- Gradual expansion rules for `areas/work/`
- State model for lead / research / promotion
- Topic-map support for `areas/knowledge/`
- Reporting across `resources/` and promotion boundaries

### Phase 3 — Semantic / hybrid retrieval
- Optional embeddings for note bodies
- Keyword + semantic hybrid search
- Entity-aware ranking
- Related-note recommendations

## Current architecture stance
- Markdown remains canonical and human-inspectable
- Database / index artifacts are derived and rebuildable
- The machine layer improves lookup, consistency checks, and cross-area synthesis
- AF-wiki should become more queryable, more reliable, and stronger in work memory without turning into a full agent memory OS

## Suggested future commands
- `af-wiki sync` — scans markdown and refreshes derived index
- `af-wiki doctor` — reports structural and lifecycle issues
- `af-wiki query "..."` — searches notes, metadata, and later semantic layers
- `af-wiki briefing` — summarizes recent changes, stale items, and likely next actions

## Current use of history
- Use recent training and meal history to decide next-step recommendations and plan adjustments inside fitness
- Use the architecture evolution plan as the active guidance for memory / indexing / maintenance upgrades across the broader wiki
- If the user supplies a newer plan, archive the old version instead of collapsing all plans into one rolling note

