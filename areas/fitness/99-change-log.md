---
title: "99-change-log"
tags:
  - area/fitness
  - topic/fitness
  - type/log
  - wiki/af
---
# AF Fitness Change Log

- 2026-04-24: Upgraded active plan memory to the new evo / architecture-evolution direction, making the sidecar index + doctor + selective structure roadmap the main current-plan lens for wiki memory upgrades.
- 2026-04-24: Archived the previous 2026-04-11 fat-loss plan v1 under `areas/fitness/plan-versions/2026-04-24-archived-fat-loss-plan-v1.md` so plan history remains versioned after the new active evo plan took over.
- 2026-04-18: Created sustainable fitness memory structure with profile, goals, current plan, decision rules, check-ins, weekly summaries, nutrition notes, and change log.
- 2026-04-18: Seeded current plan with the previously revised nutrition plan snapshot.
- 2026-04-18: Seeded weekly history with reported training and food notes for 2026-W16.
- 2026-04-18: Installed and adapted `ai-fitness-coach-cn` skill to use AF's fitness history in `/home/AF-wiki/areas/fitness/` for training and nutrition advice.
- 2026-04-18: Added 2026-W17 next-week training plan draft with grocery-planning alignment.
- 2026-04-18: Logged dinner update with beef shank + extra beef (~1.5 jin total) and noted that protein was likely already fully covered for the day.
- 2026-04-18: Replaced rough W16 training history with structured swim/activity metrics for 2026-04-14, 2026-04-15, and 2026-04-18.
- 2026-04-18: Replaced the old current-plan snapshot with the user-supplied fat-loss weekly plan and created archived plan-version storage under areas/fitness/plan-versions/.
- 2026-04-18: Added `30-nutrition/meal-history/`, then corrected the archived salmon-or-beef dinner plan to its actual date (2026-04-10) after the user clarified it was from the previous Thursday.
- 2026-04-19: Logged an ALDI grocery receipt as nutrition-supporting purchase history for the active home meal structure (sweet potato, banana, spinach sprouts, beef shank, bell peppers, broccoli, eggs; total 144.34 CNY).
- 2026-04-20: Logged the actual 2026-04-20 chest + triceps + core strength session with full exercise details, duration 48:31, 414 kcal total / 338 kcal active, avg HR 128 bpm, and difficult intensity so same-day coaching uses the completed workout rather than only dinner intake.
- 2026-04-20: Added the previously missed lunch record for 2026-04-20: five-spice beef shank 256 g plus garden vegetable salad 195 g, about 537 kcal and 77 g protein total.
- 2026-04-20: Added a historical push-day strength log covering bench press, incline press, chest accessory work, triceps work, and core so future recommendations can anchor chest/triceps loading to prior performance.
- 2026-04-20: Expanded the strength archive with a broader historical exercise library across shoulders, chest, back, core, and limited leg work so future recommendations can use prior loads/reps and machine-friendly substitutions.
- 2026-04-20: Created `30-strategy/historical-strength-reference.md` to normalize the historical lifting archive into machine-first exercise references, likely top sets, and ambiguity notes for future programming.
- 2026-04-20: Upgraded `SCHEMA.md` so the fitness wiki explicitly supports summary-layer, exercise-layer, and meal-layer daily records at the same time.
- 2026-04-20: Added `30-strategy/templates/daily-checkin-template.md` as the preferred normalized format for future training + meal logging.
- 2026-04-20: Refactored `10-checkins/2026-04.md` into a more structured format for recent entries while preserving historical archive content.
- 2026-04-20: Created `areas/fitness/index.md` as the fitness-area entrypoint, including read order, file responsibilities, and anti-miss audit rules so future coaching and completeness checks do not rely on a single file.
- 2026-04-23: Added a database-oriented architecture note under `areas/fitness/40-data/` to move toward SQLite as canonical structured storage while keeping markdown as the human-facing intake layer.
- 2026-04-23: Implemented the first SQLite sync pipeline at `areas/fitness/40-data/sync_markdown_to_sqlite.py`, creating `/home/AF-wiki/data/fitness.db` and importing current check-ins plus plan versions into structured tables.
- 2026-04-23: Added a SQL-backed completeness audit pipeline at `areas/fitness/40-data/audit_fitness_completeness.py` that writes `latest-audit.json` for fast day-level training/nutrition completeness checks.
- 2026-04-23: Added `areas/fitness/40-data/run_sync_and_audit.py` as a one-command runner for the markdown->SQLite sync plus completeness audit workflow.
