---
title: "03-decision-rules"
tags:
  - area/fitness
  - topic/fitness
  - wiki/af
---
# AF Fitness Decision Rules

## Planning rules
- When AF asks what to do next, use recent training history first, not a generic template.
- Prioritize decisions based on: recovery status, recently trained muscle groups, missed sessions, and current goal.
- Do not recommend repeating heavily trained muscle groups without a recovery check.
- If training history is incomplete, make the best provisional recommendation and label the uncertainty.

## Nutrition rules
- If daily protein is below target, first fix the easiest remaining meal slot.
- If fat intake is already high, prefer leaner protein substitutions before cutting total food volume.
- If carb intake is already high earlier in the day, cap dinner rice to a smaller serving.

## Record-keeping rules
- Stable preferences and goals go into profile/goals files.
- Current truth belongs in the current plan file.
- Weekly behavior belongs in weekly summaries.
- Important changes must also be appended to the change log.
- For future structured querying and completeness audits, prefer a SQLite-backed canonical store for normalized daily facts while keeping markdown as the intake/review surface.
- When historical strength logs are ambiguously formatted, interpret them using normal gym notation first: usually weight then reps, but allow reps-then-weight when the pattern or common exercise notation clearly supports that reading.
- Before saying a day is unrecorded or incomplete, cross-check current chat facts with the date block in `10-checkins`, the corresponding `20-weeks` note, and the current plan.
- If the user adds same-day food or training facts in multiple turns, merge them into one date block and explicitly mark any still-missing meal slots or training details.

## Recommendation style
- Recommendations should be based on historical context and expressed as the next best action, not just abstract analysis.
