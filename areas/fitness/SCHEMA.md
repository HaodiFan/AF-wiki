# Fitness Memory Schema

> Purpose: preserve enough history to help adjust training plans, recommend next actions, and track progress over time without turning the record into noise.
> Owner: AF
> Last updated: 2026-04-20

## Design principles
- Separate **stable facts** from **fast-changing logs**.
- Keep each note focused on one purpose.
- Record only information that can affect future decisions.
- Prefer summaries over raw chat transcripts.
- Let the system carry both **summary metrics** and **detail-level records** when both matter for future coaching.
- Every weekly or plan update should roll into the appropriate canonical note.

## Folder structure

```text
fitness/
├── SCHEMA.md
├── 00-profile.md
├── 01-goals.md
├── 02-current-plan.md
├── 03-decision-rules.md
├── 10-checkins/
│   ├── 2026-04.md
│   └── ...
├── 20-weeks/
│   ├── 2026-W16.md
│   └── ...
├── 30-nutrition/
│   ├── current-nutrition-strategy.md
│   ├── meal-templates.md
│   └── meal-history/
├── 30-strategy/
│   ├── historical-strength-reference.md
│   └── templates/
│       └── daily-checkin-template.md
├── plan-versions/
└── 99-change-log.md
```

---

# File definitions

## 00-profile.md
Stores relatively stable background information.

Fields:
- training goal type: fat loss / recomposition / muscle gain / maintenance
- known constraints
- preferred exercise types
- disliked exercise types
- preferred planning style
- recovery notes
- equipment preference / availability

Update only when these truths actually change.

## 01-goals.md
Stores current active goals and evaluation metrics.

Sections:
- primary goal
- secondary goals
- current target ranges
- what success looks like this month
- what to deprioritize

This is the decision anchor for all future recommendations.

## 02-current-plan.md
Stores the latest approved plan only.

Sections:
- version label
- effective date
- training split
- weekly structure
- current nutrition targets
- recovery expectations
- current adjustment notes

Important rule:
- This file should reflect the **current truth**, not the whole history.
- When the plan changes, overwrite this file and log the change in `99-change-log.md`.
- Historical full versions belong in `plan-versions/`.

## 03-decision-rules.md
Stores reusable decision logic I should apply when advising next steps.

Examples:
- if user is unsure what to train next, prioritize undertrained muscle groups and recovery status
- if protein is below target, first adjust easiest high-protein meal slot
- if fatigue is high and training density increased, prefer recovery or lower-intensity work
- if recent training already hit shoulders/arms heavily, avoid redundant shoulder-arm day unless recovery is confirmed
- if the user dislikes lower-body focus, keep minimum effective lower-body work distributed unless the goal requires more

This is the most important file for planning continuity.

## 10-checkins/YYYY-MM.md
Short rolling log for body state and daily/near-daily updates.

Each date should support **three possible layers**, recorded together when available:

### A. Day summary layer
- overall training status
- body weight
- energy
- soreness
- sleep
- appetite
- adherence / recovery notes

### B. Training session layer
For each session, preserve both summary metrics and exercise details when available.

Suggested fields:
- type: strength / swim / cardio / recovery
- theme: chest+triceps+core / back+biceps / easy swim / etc.
- duration
- calories / active calories
- avg HR / peak HR
- subjective intensity
- short evaluation
- exercises:
  - movement name
  - weight
  - reps
  - sets
  - distance / pace / time if cardio or swim

### C. Meal / intake layer
Track by meal slot when available:
- breakfast
- lunch
- dinner
- snack
- post-workout
- pre-sleep

For each meal, capture what is known:
- foods
- estimated weight
- calories
- protein
- notes (estimated, label-based, sauce included, etc.)

Keep concise, but do **not** collapse away useful training metrics or meal-level facts that will improve later evaluations.

## 20-weeks/YYYY-Www.md
Weekly structured summary.

Sections:
- completed training
- missed training / intentional rest
- weekly food pattern
- recovery observations
- main deviations from plan
- decisions for next week

This is the main bridge between raw events and plan adjustments.

## 30-nutrition/current-nutrition-strategy.md
Stores the currently active nutrition strategy.

Sections:
- calorie target
- protein target
- fat target
- carb strategy
- meal timing strategy
- default correction rules

## 30-nutrition/meal-templates.md
Stores reusable meal patterns that have worked.

Examples:
- training day dinner template
- high-protein pre-sleep snack template
- lower-fat correction day template

## 30-nutrition/meal-history/
Stores archived meal plans or dated nutrition notes that are useful historically but are **not** automatically treated as confirmed intake.

Use this for:
- meal planning drafts
- projected day totals
- old dinner decision branches

Ground-truth rule:
- confirmed eaten meals in check-ins override meal plans if they conflict.

## 30-strategy/
Stores reusable strategy notes that are not just one-day logs.

Current examples:
- historical strength reference
- future training templates
- movement substitution guides

## 30-strategy/templates/daily-checkin-template.md
Stores the preferred markdown template for future daily logging so incoming chat data can be normalized into one stable format.

## plan-versions/
Stores archived historical current-plan versions.

Rule:
- each meaningful plan revision gets its own file
- `02-current-plan.md` should always point to the active truth

## 99-change-log.md
Append-only log of major changes.

Log:
- plan changes
- goal changes
- important discoveries
- recurring problems
- strategy shifts
- schema changes that affect how the system stores data

Use short dated bullets.

---

# Update protocol

When new information arrives, classify it first:

1. **Stable identity / preference / objective?**
   -> update `00-profile.md` or `01-goals.md`

2. **Current plan changed?**
   -> overwrite `02-current-plan.md`
   -> archive prior version if needed in `plan-versions/`
   -> append reason to `99-change-log.md`

3. **Decision heuristic discovered?**
   -> update `03-decision-rules.md`

4. **Daily condition or one-off event?**
   -> add to monthly check-in note

5. **Weekly training/diet summary?**
   -> add to weekly note in `20-weeks/`

6. **Reusable nutrition pattern?**
   -> add to nutrition note

7. **Reusable training reference / template / cleaned archive?**
   -> add to `30-strategy/`

---

# Compression rules

To keep the memory sustainable:
- Do not store every meal forever unless it affects planning.
- Preserve trends, exceptions, decisions, and useful reference ranges.
- Compress daily events into weekly summaries when possible.
- Current plan files should stay short and directly usable.
- For daily check-ins, keep summary + exercise + meal layers compatible instead of forcing everything into one flat bullet style.

---

# Final chosen structure

The final decision is to use a **layered fitness memory system**:

1. **Profile layer** — who you are as a trainee
2. **Goal layer** — what you are trying to achieve now
3. **Current plan layer** — what you should be doing now
4. **Decision rule layer** — how I should reason when helping you
5. **Check-in / weekly history layer** — what actually happened
6. **Strategy / archive layer** — reusable references, historical strength ranges, templates, and plan history
7. **Change log layer** — what changed and why

This structure is chosen because it supports both:
- long-term continuity
- fast decision-making when you ask “what should I do next?”
- richer daily evaluation when your real-world data includes both device summaries and exercise/meal details
