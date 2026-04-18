# AF Second Brain Schema

> Purpose: build a durable, evolvable second-brain system that can store knowledge, active plans, learning records, ideas, personal operating context, and focused domains like fitness without mixing everything together.
> Last updated: 2026-04-18

## Core design decision
The wiki should follow a **second-brain architecture**, not a single-topic archive.
Fitness is one domain inside the system, not the system itself.

## Top-level structure

AF-wiki/
├── inbox/                 # quick capture before processing
├── areas/                 # ongoing responsibilities / life domains
│   ├── fitness/
│   ├── learning/
│   ├── work/
│   └── personal/
├── projects/              # finite outcome-driven efforts
├── resources/             # reference knowledge, evergreen notes, topics
├── archive/               # inactive / completed / superseded material
├── dashboards/            # current-state summaries and active control panels
├── templates/             # reusable note templates
├── index.md               # master navigation
├── SCHEMA.md              # this file
└── log.md                 # major structural and knowledge-management changes

This is close to a PARA-style second brain, but adapted for agent-assisted maintenance.

---

## Layer meanings

### 1. Inbox
For fast capture without forcing immediate organization.
Examples:
- raw thoughts
- links to read later
- fleeting ideas
- notes from conversation

Rule:
- inbox is temporary
- items should later be processed into projects, areas, resources, or archive

### 2. Areas
For ongoing responsibilities that need continuous maintenance.
Examples:
- fitness
- learning
- career
- finances
- relationships
- health

Rule:
- areas do not end
- each area should have a stable internal structure
- active personal systems like fitness belong here

### 3. Projects
For efforts with a defined outcome and likely end state.
Examples:
- prepare for a certification
- build a side project
- finish a reading plan
- run an 8-week cut

Rule:
- when a project ends, move it to archive or convert durable knowledge into resources

### 4. Resources
For reusable knowledge and reference material.
Examples:
- concept notes
- topic summaries
- study notes
- frameworks
- permanent insights
- reading notes worth keeping

Rule:
- resources are not action plans
- resources are knowledge assets

### 5. Archive
For completed, inactive, or outdated material.
Examples:
- old plans
- completed projects
- superseded strategies
- stale references no longer in active use

### 6. Dashboards
For high-value entry points that summarize the current state.
Examples:
- today dashboard
- weekly review dashboard
- fitness dashboard
- learning dashboard

Rule:
- dashboards should answer: what matters now?

### 7. Templates
Reusable note structures for consistency.
Examples:
- weekly review
- learning note
- project plan
- fitness check-in
- idea note

---

## Final chosen decision structure
The final structure for this second brain is:

1. **Capture layer** — inbox
2. **Responsibility layer** — areas
3. **Execution layer** — projects
4. **Knowledge layer** — resources
5. **History layer** — archive
6. **Control layer** — dashboards
7. **Consistency layer** — templates

This is the final decision because it supports both:
- broad life knowledge management
- domain-specific systems like fitness
- future agent-assisted planning and retrieval

---

## Fitness placement
Fitness should live under:
- `areas/fitness/`

Because fitness is an ongoing area of life, not a one-off project.
Specific short-term fitness goals can also create linked project notes under:
- `projects/`

Examples:
- `projects/2026-05-cut-phase/`
- `projects/swimming-technique-focus/`

---

## Recommended structure for `areas/fitness/`

areas/fitness/
├── profile.md
├── goals.md
├── current-plan.md
├── decision-rules.md
├── checkins/
├── weeks/
├── nutrition/
├── training/
└── change-log.md

This keeps the fitness memory system intact while placing it inside the broader second-brain architecture.

---

## Recommended structure for learning

areas/learning/
├── dashboard.md
├── current-focus.md
├── study-log/
├── topics/
└── change-log.md

## Recommended structure for ideas

resources/ideas/
├── idea-index.md
├── raw-concepts/
└── developed-concepts/

## Recommended structure for evergreen knowledge

resources/knowledge/
├── concepts/
├── people/
├── frameworks/
└── summaries/

---

## Processing rules
When new information arrives, classify it first:

1. Is it a quick uncategorized capture?
   -> `inbox/`
2. Is it part of an ongoing responsibility?
   -> `areas/<domain>/`
3. Is it tied to a defined goal with an end state?
   -> `projects/`
4. Is it durable reference knowledge?
   -> `resources/`
5. Is it no longer active but worth preserving?
   -> `archive/`
6. Is it a summary/control note?
   -> `dashboards/`
7. Is it a reusable format?
   -> `templates/`

---

## Agent operating rules
- Do not let one domain consume the whole wiki structure.
- Prefer broad navigability over local optimization for one topic.
- Keep current truth separate from historical logs.
- Compress repeated short-term events into weekly or monthly summaries.
- Promote durable insights from logs into resources when they become reusable knowledge.
- When unsure where a note belongs, choose the lowest-friction place first, then refactor later.

---

## Naming rules
- lowercase-hyphenated paths where practical
- short, human-readable file names
- date-prefix only when chronology matters
- avoid deeply nested folders unless the volume justifies them

---

## What this schema optimizes for
- fast capture
- long-term retrieval
- cross-domain thinking
- agent-assisted planning
- low-maintenance evolution
- separation of action, responsibility, and knowledge
