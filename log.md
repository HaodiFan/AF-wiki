# AF Wiki Log

## [2026-04-24] schema | Evo-memory baseline promoted to root navigation
- Updated `SCHEMA.md` to reflect the active 2026-04-24 evo-memory baseline for future wiki upgrades
- Kept markdown as canonical while making sidecar index / doctor / selective structure the default evolution direction
- Confirmed root navigation continues to point users first to planning docs and sidecar runtime entrypoints

## [2026-04-24] infra | Added Phase 1 sidecar command skeleton
- Added `infra/README.md` as the entrypoint for the derived runtime layer
- Added `infra/indexing/af_wiki_sync.py` as the canonical sync wrapper for the current markdown -> SQLite pipeline
- Added `infra/jobs/af_wiki_doctor.py` as the first compact doctor command over the fitness audit output
- Added `infra/jobs/af_wiki_briefing.py` as the first lightweight briefing command combining recent log context with audit status
- Kept markdown as canonical while moving command entrypoints toward the evo plan's sidecar layout

## [2026-04-24] docs | Added architecture evolution plan
- Added `docs/2026-04-24-feat-architecture-evolution-plan.md` to capture how AF-wiki should absorb selected GBrain strengths without replacing the current LeadFlow / markdown-first architecture
- Linked the new evolution-plan doc from `index.md` and `START-HERE.md` so it becomes part of the canonical navigation
- Defined a four-layer evolution model: canonical markdown layer, derived index/query layer, selective structure layer, and maintenance/briefing layer
- Prioritized Phase 1 around sidecar indexing and wiki doctor capabilities before heavier semantic retrieval work

## 2026-04-27
- Fitness/Nutrition: completed chest + triceps + core strength session (50:37, 319 kcal total / avg HR 111 bpm); breakfast, lunch, and pre/post-workout banana intake are grounded, while dinner remains explicitly unconfirmed
- Overall evaluation: training closure is clear, but recovery closure still depends on dinner or later protein intake

## 2026-04-26
- Fitness: completed a lighter recovery-style swim session in Shanghai (38:59, 500 m, 218 kcal total / 155 kcal active, avg HR 132 bpm)
- Nutrition: breakfast was light biscuits + 1 corn; lunch was beef 180 g + dried sweet potato 300 g; dinner was cod burger + 1 corn
- Overall evaluation: this day is not blank; training and all three meal slots are grounded, but the intake still looks somewhat carb-heavy and not maximally protein-efficient

## 2026-04-25
- Fitness: completed shoulders + arms + core strength session (42:36, 361 kcal total / 294 kcal active, avg HR 126 bpm)
- Nutrition: breakfast was light biscuits + 1 Snickers bar; lunch was original-flavor braised beef 250 g; dinner remains explicitly unconfirmed
- Overall evaluation: this day is not blank; training is complete and grounded, but the nutrition side is still front-light with dinner evidence missing

## 2026-04-24
- Fitness: no confirmed session recovered yet; training status remains explicitly unconfirmed rather than inferred as either completed or rest
- Nutrition: lunch was explicitly skipped; dinner was cheese potato pancake, chicken soup, sticky rice, sugar garlic, chicken wings, and fried chicken pieces; breakfast remains unrecovered
- Overall evaluation: this day is not blank; diet facts are grounded while training still needs confirmation, and energy distribution was clearly front-light / dinner-heavy

## 2026-04-23
- Fitness: no training performed; this is a confirmed intentional rest day rather than an unlogged workout gap
- Nutrition: breakfast was 3 eggs + 1 bowl of milk; lunch was 肉肉大米 hamburger-steak meal; dinner was beef + 1 bowl rice + green vegetables + bell pepper
- Overall evaluation: this day is not blank; rest status and three meals are both grounded, though exact portions/macros remain unquantified

## 2026-04-22
- Fitness/Nutrition: completed a moderate-intensity swim session (23:49 total / 22:51 active, 325 m, 13 laps in a 25 m pool, 141 kcal total / 105 kcal active, avg HR 133 bpm, exertion level 5), mainly breaststroke with one mixed-stroke segment; breakfast was 3 eggs + 1 cup of milk, pre-workout intake included 1 banana before swimming, and lunch was 200 g sirloin steak + 1 corn cob + 1 bottle of sparkling water
- Overall evaluation: today's swim is aligned with the active Tuesday swimming slot and counts as a real aerobic session, though it landed shorter than the plan's nominal 40-60 min target; daytime recovery intake is grounded, while dinner remains explicitly unconfirmed

## 2026-04-21
- Fitness/Nutrition: completed a back + biceps focused machine strength session in Shanghai (15:14-15:57, 42:18, 335 kcal total / 268 kcal active, avg HR 123 bpm, HR range 83-143, exertion level 6), with pulldown, seated row, chest-supported row, straight-arm pulldown, curls, face pulls, a small core add-on, and post-session back stretching; breakfast 3 eggs + 1 bowl of milk, lunch grilled beef grain bowl + braised beef + Perrier, dinner beef shank with bell pepper + rice + spinach + pineapple/lychee + yogurt
- Overall evaluation: the active plan expected Tuesday swimming, but substituting into a pull-focused strength day was a reasonable real-time adjustment after Monday's push session; training completion is strong and grounded, and same-day nutrition is now much more complete, though the separate pre-sleep protein slot is still unconfirmed

## 2026-04-20
- Fitness/Nutrition: completed Monday chest + triceps + core strength session (48:31, 414 kcal total / 338 kcal active, avg HR 128 bpm, difficult intensity); breakfast 3 eggs; lunch five-spice beef shank 256 g + garden vegetable salad 195 g (~537 kcal, ~77 g protein); dinner salmon 200 g + broccoli + 2 bell peppers + 1 bowl rice
- Overall evaluation: today matched the active Monday push slot closely and counts as a genuine completed strength day; meal structure was largely on-plan with strong lunch/dinner protein anchors, but the pre-sleep protein slot is still unconfirmed

## [2026-04-20] refactor | Area layer normalized around dynamic modules
- Promoted retained knowledge notes from `resources/knowledge/` into `areas/knowledge/`
- Added `areas/index.md` as the canonical area registry and skill-routing map
- Added `areas/work/` as a first-class work area scaffold
- Instantiated `inbox/`, `projects/`, `resources/research/`, and `resources/ideas/` as lightweight LeadFlow scaffolds
- Clarified that `resources/` is the shared lead/research pipeline rather than a second copy of the area layer
- Rewrote root navigation so the default read order is `START-HERE` -> `areas/index` -> target area
- Expanded `areas/index.md` and added `areas/fitness/index.md` details so fitness has an explicit area entrypoint, read order, and anti-miss audit guidance
---

## [2026-04-20] docs | Clarified current-vs-target navigation
- Added `START-HERE.md` as the first-reader guide
- Updated `README.md` and `index.md` so current active modules are separated from planned architecture
- Updated `SCHEMA.md` to state explicitly that LeadFlow is a target architecture and not every folder already exists
- Marked `wiki/` as an older bootstrap scaffold so it no longer competes with the root-level entry points
---

## [2026-04-19] rename | LeadFlow architecture named
- Named AF's `PARA + Lead` variant as `LeadFlow`
- Updated `/home/AF-wiki/SCHEMA.md`, `/home/AF-wiki/README.md`, `dashboards/recent.json`, and profile-feed wording to use `LeadFlow` instead of generic `PARA`
- Clarified that dashboards, templates, archive, and agent refresh are first-class parts of the system rather than add-ons
---

## [2026-04-19] workflow | Lead -> research pipeline added
- Added `resources/leads/` as the canonical location for quick-capture research leads
- Added `resources/research/` as the canonical location for deep-dive notes linked to original leads
- Added `dashboards/research-backlog.md` to track the lead -> research workflow
- Added `templates/lead-note-template.md` and `templates/deep-research-template.md`
- Updated `index.md` to expose the lead/research workflow in master navigation
---

## [2026-04-18] update | Homepage and wiki index reframed around recent-status display
- Reworked the GitHub profile README to show recent updates by area instead of mainly describing repository usage
- Reworked `/home/AF-wiki/README.md` to lead with `日历与近况` instead of a repo-introduction-heavy structure
- Updated `/home/AF-wiki/index.md` so recent dated updates appear as a first-class entry section
- Established the rule that calendar/recent-updates content is one homepage section, not a separate homepage concept
---

## [2026-04-18] create | Second-brain schema established
- Reframed the wiki from a fitness-only structure to a general second-brain architecture
- Chose top-level structure: inbox, areas, projects, resources, archive, dashboards, templates
- Assigned fitness to `areas/fitness/`
---

## [2026-04-18] archive | Legacy fitness folder archived
- Moved old `/home/AF-wiki/fitness/` to `/home/AF-wiki/archive/legacy/fitness-legacy-2026-04-18`
- Active fitness workspace remains at `/home/AF-wiki/areas/fitness/`
---

## [2026-04-18] ingest | 微信公众号文章记录
- Added `resources/knowledge/wechat-public-account-articles.md`
- Filed 7 article links from Anthony.F's March 2026 微信聊天记录 into the knowledge system
- Updated `index.md` to expose the new resource entry
---

## [2026-04-18] ingest | 微信公众号正文抓取
- Created `resources/knowledge/wechat-articles/` with per-article notes
- Attempted extraction for 7 微信公众号 links and stored available正文 excerpts
- Updated `resources/knowledge/wechat-public-account-articles.md` with article-note links
---
