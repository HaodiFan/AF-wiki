# Fitness Memory Schema

> Purpose: preserve enough history to help adjust training plans, recommend next actions, and track progress over time without turning the record into noise.
> Owner: AF
> Last updated: 2026-04-18

## Design principles
- Separate **stable facts** from **fast-changing logs**.
- Keep each note focused on one purpose.
- Record only information that can affect future decisions.
- Prefer summaries over raw chat transcripts.
- Every weekly or plan update should roll into the appropriate canonical note.

## Folder structure

fitness/
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
│   └── meal-templates.md
└── 99-change-log.md

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
- training split
- weekly structure
- current nutrition targets
- recovery expectations
- current adjustment notes
- effective date

Important rule:
- This file should reflect the **current truth**, not the whole history.
- When the plan changes, overwrite this file and log the change in `99-change-log.md`.

## 03-decision-rules.md
Stores reusable decision logic I should apply when advising next steps.

Examples:
- if user is unsure what to train next, prioritize undertrained muscle groups and recovery status
- if protein is below target, first adjust easiest high-protein meal slot
- if fatigue is high and training density increased, prefer recovery or lower-intensity work
- if recent training already hit shoulders/arms heavily, avoid redundant shoulder-arm day unless recovery is confirmed

This is the most important file for planning continuity.

## 10-checkins/YYYY-MM.md
Short rolling log for body state and daily/near-daily updates.

Typical entries:
- body weight
- energy
- soreness
- sleep
- appetite
- notable training performance
- adherence issues

Keep concise. Only record things relevant to decisions.

## 20-weeks/YYYY-Www.md
Weekly structured summary.

Sections:
- completed training
- missed training
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

## 99-change-log.md
Append-only log of major changes.

Log:
- plan changes
- goal changes
- important discoveries
- recurring problems
- strategy shifts

Use short dated bullets.

---

# Update protocol

When new information arrives, classify it first:

1. **Stable identity / preference / objective?**
   -> update `00-profile.md` or `01-goals.md`

2. **Current plan changed?**
   -> overwrite `02-current-plan.md`
   -> append reason to `99-change-log.md`

3. **Decision heuristic discovered?**
   -> update `03-decision-rules.md`

4. **Daily condition or one-off event?**
   -> add to monthly check-in note

5. **Weekly training/diet summary?**
   -> add to weekly note in `20-weeks/`

6. **Reusable nutrition pattern?**
   -> add to nutrition note

---

# Compression rules

To keep the memory sustainable:
- Do not store every meal forever unless it affects planning.
- Compress daily events into weekly summaries.
- Preserve exceptions, trends, and decisions — not noise.
- Current plan files should stay short and directly usable.

---

# Final chosen structure

The final decision is to use a **6-layer fitness memory system**:

1. **Profile layer** — who you are as a trainee
2. **Goal layer** — what you are trying to achieve now
3. **Current plan layer** — what you should be doing now
4. **Decision rule layer** — how I should reason when helping you
5. **Check-in / weekly history layer** — what actually happened
6. **Change log layer** — what changed and why

This structure is chosen because it supports both:
- long-term continuity
- fast decision-making when you ask “what should I do next?”
