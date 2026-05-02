---
title: "DB-ARCHITECTURE"
tags:
  - area/fitness
  - topic/data-management
  - topic/fitness
  - wiki/af
---
# AF Fitness Database Architecture

> Purpose: add a normalized SQLite-backed storage layer for canonical fitness records, while keeping Markdown as the human intake and review surface.
> Status: proposed architecture approved by user on 2026-04-23
> Last updated: 2026-04-28

## Core principle
- SQLite becomes the canonical structured store for fitness data.
- Markdown becomes the human-facing intake, review, and narrative layer.
- New facts should be parsed from markdown/chat into SQLite, then optionally rendered back into markdown summaries.
- For historically important fitness and diet records, the structured layer should support bilingual storage so one-time backfill and future updates can preserve both Chinese and English renderings when available.

## Why this split
Markdown is good for:
- quick capture
- human review
- flexible notes
- coaching summaries

SQLite is better for:
- completeness audits
- regex-free structured queries
- cross-day joins
- plan-vs-actual checks
- missing-field detection
- future automation and dashboards
- preserving normalized bilingual fields without forcing daily markdown to become overly rigid

## Proposed storage model
Database location:
- `/home/AF-wiki/data/fitness.db`

Markdown role:
- `areas/fitness/10-checkins/` stays as daily/monthly intake + readable summary
- `areas/fitness/20-weeks/` stays as weekly review layer
- strategy/plan/profile markdown stays as human-readable operating docs

## Canonical direction
Preferred long-term flow:
1. User reports facts in chat
2. Assistant normalizes them into SQLite tables
3. Assistant updates markdown summary/intake views as needed
4. Audits and recommendations query SQLite first, then use markdown for narrative context
5. When the user provides or approves bilingual wording, store both language variants in structured fields instead of overwriting one with the other

## Suggested tables
### days
One row per date.
Fields:
- date
- plan_slot
- actual_training_status
- nutrition_status
- notes
- notes_zh
- notes_en

### training_sessions
One row per training session.
Fields:
- id
- date
- type
- theme
- theme_zh
- theme_en
- duration_seconds
- calories_total
- calories_active
- avg_hr
- max_hr
- intensity
- intensity_zh
- intensity_en
- exertion_level
- evaluation
- evaluation_zh
- evaluation_en
- recovery_notes
- recovery_notes_zh
- recovery_notes_en
- source_note

### exercises
One row per exercise line or exercise set-group.
Fields:
- id
- session_id
- exercise_name
- exercise_name_zh
- exercise_name_en
- set_order
- weight_value
- reps
- duration_seconds
- distance_m
- pace_text
- raw_text
- raw_text_zh
- raw_text_en

### meals
One row per meal slot.
Fields:
- id
- date
- meal_slot
- meal_slot_zh
- meal_slot_en
- foods_text
- foods_text_zh
- foods_text_en
- estimated_calories
- estimated_protein_g
- notes
- notes_zh
- notes_en
- source_note

### meal_items
Optional finer-grained food rows.
Fields:
- id
- meal_id
- food_name
- food_name_zh
- food_name_en
- quantity_text
- calories
- protein_g
- notes

### plan_versions
Fields:
- id
- version_label
- effective_date
- status
- plan_type
- source_note
- summary
- summary_zh
- summary_en

### plan_slots
Fields:
- id
- plan_version_id
- weekday
- slot_name
- slot_name_zh
- slot_name_en
- details
- details_zh
- details_en

### audits
Fields:
- id
- date
- training_completeness
- nutrition_completeness
- missing_fields
- checked_at

## Migration policy
- Existing markdown remains in place.
- Historical records can be backfilled incrementally.
- Do not block daily use on full backfill.
- Start with current active month and recent week first.
- User-approved historical bilingual restoration can be done as a one-time backfill; afterwards, future sync/update flows should keep bilingual structured fields aligned.

## Operational rule
Until a sync tool exists, markdown and SQLite may temporarily diverge.
So the next implementation step should be a sync script that:
1. creates the schema
2. imports existing markdown records
3. supports idempotent upsert for future updates
4. powers completeness audits from SQL queries
5. preserves bilingual text fields when markdown/chat provides them or when later backfill enriches the DB

## Current implementation
- Sync script: `/home/AF-wiki/areas/fitness/40-data/sync_markdown_to_sqlite.py`
- Audit script: `/home/AF-wiki/areas/fitness/40-data/audit_fitness_completeness.py`
- Combined runner: `/home/AF-wiki/areas/fitness/40-data/run_sync_and_audit.py`
- Audit output: `/home/AF-wiki/areas/fitness/40-data/latest-audit.json`
- Database file: `/home/AF-wiki/data/fitness.db`
- Current scope: imports `10-checkins/2026-04.md`, `02-current-plan.md`, and archived markdown plan versions
- Usage: `python3 /home/AF-wiki/areas/fitness/40-data/sync_markdown_to_sqlite.py`
- Audit usage: `python3 /home/AF-wiki/areas/fitness/40-data/audit_fitness_completeness.py`
- Combined usage: `python3 /home/AF-wiki/areas/fitness/40-data/run_sync_and_audit.py`
- Current behavior: recreates/upserts canonical daily records, event records, meals, training sessions, exercises, and plan slots from markdown sources, then audits day-level training/nutrition completeness from SQL
- 2026-04-28 direction: schema/sync should evolve to include bilingual shadow fields for day notes, sessions, exercises, meals, and plan summaries so historical one-time backfill and future updates stay consistent
