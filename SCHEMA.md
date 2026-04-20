# AF LeadFlow Schema

> Purpose: define LeadFlow as AF's durable second-brain operating model, with a dynamic `areas/` layer for ongoing responsibilities and a shared `resources/` layer for cross-area lead and research flow.
> Last updated: 2026-04-20

## Read this file the right way

This file describes the **target operating model** and the current structural rules.
It is not a guarantee that every planned folder already exists or already has meaningful content.

For the current repo state, read in this order:
- [[START-HERE]]
- [[areas/index]]
- [[index]]
- the specific `areas/<area>/SCHEMA.md` for the area you want to work in

## Current active footprint

As of `2026-04-20`, the repo is primarily composed of:
- `areas/index.md`
- `areas/fitness/`
- `areas/knowledge/`
- `areas/work/` as a light scaffold
- `inbox/`
- `projects/`
- `resources/index.md`
- `resources/leads/`
- `resources/research/`
- `resources/ideas/`
- `dashboards/research-backlog.md`
- `templates/`
- `archive/legacy/`

The following parts are still **light scaffolds** rather than mature modules:
- `areas/work/`
- `inbox/`
- `projects/`
- `resources/research/`
- `resources/ideas/`

The following parts remain **future growth space**:
- future areas under `areas/<name>/`

The `wiki/` folder is an earlier bootstrap scaffold and should not be confused with the current root-level LeadFlow entry points.

## Core design decision

LeadFlow now uses **two different top-level coordination layers**:

1. **Dynamic area modules** under `areas/`
2. **Shared lead/research pipeline** under `resources/`

This distinction is the main fix for the previous confusion.

### What belongs in `areas/`
Use `areas/` for ongoing responsibility modules that need their **own internal structure**.

Current modules:
- `fitness`
- `knowledge`
- `work`

Future modules can be added as needed.

Important:
- `areas/` is dynamic, not a fixed closed list
- each area can define its own internal schema
- `fitness` does not need to look like `knowledge`
- `knowledge` does not need to look like `work`

### What belongs in `resources/`
Use `resources/` for **shared, cross-area flow**, not as a second copy of the area layer.

Current canonical usage:
- `resources/leads/` for weak-signal capture

Planned shared usage:
- `resources/research/` for deep-dive notes linked back to leads
- `resources/ideas/` for idea incubation if needed

Rule:
- if something is owned by an ongoing domain and will keep being curated there, it belongs in `areas/<domain>/`
- if something is part of the cross-area capture/research pipeline, it belongs in `resources/`

## Area modularity rules

`areas/` is now treated as a **registry of responsibility modules**.

Minimum contract for a new area:
- `areas/<name>/SCHEMA.md`
- `areas/<name>/index.md`
- `areas/<name>/99-change-log.md`

Registry rule:
- `areas/index.md` is the canonical registry of all current area modules
- it should say what each area is for
- it should say which skill or workflow should usually handle that area

Local rule:
- each `areas/<name>/SCHEMA.md` defines that area's internal structure
- each area may recommend different skills or workflows
- second-brain routing should orient at `areas/index.md` first, then descend into the target area's `SCHEMA.md`

## Target top-level structure

```text
AF-wiki/
├── inbox/                 # quick capture before processing
├── areas/                 # dynamic responsibility modules
│   ├── index.md           # registry + routing for all areas
│   ├── fitness/
│   ├── knowledge/
│   ├── work/
│   └── <future-area>/
├── projects/              # finite outcome-driven efforts
├── resources/             # shared cross-area capture/research layer
│   ├── leads/
│   ├── research/
│   └── ideas/
├── archive/               # inactive / completed / superseded material
├── dashboards/            # current-state summaries and active control panels
├── templates/             # reusable note templates
├── START-HERE.md          # current-vs-target orientation
├── index.md               # current canonical navigation
├── SCHEMA.md              # this file
└── log.md                 # major structural changes
```

## Layer meanings

All LeadFlow top-level layers now exist in the repo, but some are only scaffolded.

### 1. Areas
For ongoing responsibilities that need continuous maintenance and their own internal schema.

Examples:
- fitness tracking and coaching memory
- knowledge curation and retained reading notes
- work context and active operating assumptions

Rule:
- areas do not end
- areas are modular
- areas can be added over time

### 2. Resources
For cross-area capture and research flow.

Examples:
- quick leads to investigate later
- deep research notes linked back to leads
- future idea incubation

Rule:
- resources are shared infrastructure, not the owner of every long-lived note
- do not put area-owned modules here just because they sound like "knowledge"

### 3. Projects
For efforts with a defined outcome and likely end state.

Examples:
- prepare for a certification
- build a side project
- run an 8-week cut

### 4. Archive
For completed, inactive, or superseded material.

### 5. Dashboards
For high-value entry points that answer: what matters now?

### 6. Templates
Reusable note structures for consistency.

## Lead -> research -> area integration flow

### Step 1: capture a lead
Use `resources/leads/` when you see something interesting but do not want to research it yet.

### Step 2: maintain the backlog
Use `dashboards/research-backlog.md` to track lead status.

### Step 3: deep dive later
When you choose to study something in depth, create a note in `resources/research/`.

### Step 4: promote to the right owner
If the result becomes durable:
- put it in `areas/<domain>/` if it belongs to an ongoing area
- put it in `projects/` if it belongs to a time-bounded effort
- keep it in shared `resources/` only if it is truly cross-area infrastructure or reference material

For the current repo:
- retained technical reading notes belong in `areas/knowledge/`
- fitness memory belongs in `areas/fitness/`

## Current area modules

### Fitness
Canonical path:
- `areas/fitness/`

Why it is an area:
- it is an ongoing personal responsibility with continuous updates and its own decision memory

### Knowledge
Canonical path:
- `areas/knowledge/`

Why it is an area:
- technical reading, retained article notes, and ongoing knowledge curation are a continuous responsibility, not just a pile of shared resources

### Work
Canonical path:
- `areas/work/`

Why it is an area:
- work context is ongoing and will likely need its own internal operating notes, separate from both projects and personal domains

## Skill routing rule

When a second-brain or orchestration skill needs to act inside this repo:
1. read `areas/index.md`
2. identify the target area
3. read `areas/<area>/SCHEMA.md`
4. follow the preferred skill routing defined there

This is how area-specific structure and area-specific skills stay aligned while the set of areas remains dynamic.
