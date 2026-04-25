#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import sqlite3
from pathlib import Path

ROOT = Path('/home/AF-wiki')
DB_PATH = ROOT / 'data' / 'fitness.db'
OUTPUT_PATH = ROOT / 'areas' / 'fitness' / '40-data' / 'latest-audit.json'

WEEKDAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
PRIMARY_MEALS = ['Breakfast', 'Lunch', 'Dinner']
OPTIONAL_MEALS = ['Pre-workout snack', 'Post-workout', 'Pre-sleep snack', 'Snack']


def weekday_name(date_text: str) -> str:
    y, m, d = map(int, date_text.split('-'))
    return WEEKDAY_NAMES[dt.date(y, m, d).weekday()]


def expected_plan_slot(day, weekday_plan):
    recorded = day['recorded_plan_slot'] if isinstance(day, dict) and 'recorded_plan_slot' in day else day['plan_slot']
    if recorded:
        return recorded
    return weekday_plan.get('slot_name')


def load_active_plan_map(conn):
    rows = conn.execute('''
        SELECT ps.weekday, ps.slot_name, ps.details
        FROM plan_slots ps
        JOIN plan_versions pv ON pv.id = ps.plan_version_id
        WHERE pv.status = 'active' AND pv.plan_type = 'fitness_training'
        ORDER BY ps.weekday_order
    ''').fetchall()
    return {row['weekday']: {'slot_name': row['slot_name'], 'details': row['details']} for row in rows}


def load_active_fitness_plan(conn):
    row = conn.execute('''
        SELECT pv.id, pv.version_label, pv.plan_type, pv.source_note, COUNT(ps.id) AS slot_count
        FROM plan_versions pv
        LEFT JOIN plan_slots ps ON ps.plan_version_id = pv.id
        WHERE pv.plan_type = 'fitness_training'
        ORDER BY CASE WHEN pv.status = 'active' THEN 0 ELSE 1 END, pv.effective_date DESC, pv.id DESC
        LIMIT 1
    ''').fetchone()
    return row


def classify_training(day, session, exercise_count, weekday_plan):
    missing = []
    status = 'unknown'
    plan_text = ((day['plan_slot'] or '') + ' ' + (weekday_plan.get('slot_name') or '')).lower()
    planned_rest = 'rest' in plan_text or 'recovery' in plan_text
    planned_swim = 'swim' in plan_text or 'swimming' in plan_text

    if day['actual_training_status'] == 'rest':
        status = 'complete'
    elif session:
        required_fields = ['type', 'theme', 'duration_seconds', 'intensity']
        for field in required_fields:
            if not session[field]:
                missing.append(field)
        if exercise_count == 0 and session['type'] != 'swim':
            missing.append('exercise_details')
        status = 'complete' if not missing else 'partial'
    elif day['actual_training_status'] == 'unconfirmed':
        status = 'missing'
        missing.append('training_confirmation')
    elif planned_rest:
        status = 'complete'
    elif planned_swim:
        status = 'missing'
        missing.append('swim_session')
    else:
        status = 'missing'
        missing.append('training_session')

    return status, missing


def classify_nutrition(meals):
    missing = []
    slots = {meal['meal_slot'] for meal in meals}
    normalized_slots = set(slots)
    if 'Breakfast / daytime intake' in normalized_slots:
        normalized_slots.add('Breakfast')

    present_primary = [slot for slot in PRIMARY_MEALS if slot in normalized_slots]
    if len(present_primary) == 3:
        status = 'complete'
    elif len(present_primary) >= 1:
        status = 'partial'
        for slot in PRIMARY_MEALS:
            if slot not in normalized_slots:
                missing.append(slot.lower())
    else:
        status = 'missing'
        missing.extend([slot.lower() for slot in PRIMARY_MEALS])

    if 'Dinner' in normalized_slots and not any('Pre-sleep' in slot for slot in normalized_slots):
        missing.append('pre_sleep_unconfirmed')

    return status, missing, sorted(slots)


def build_audit(conn):
    conn.row_factory = sqlite3.Row
    plan_map = load_active_plan_map(conn)
    active_fitness_plan = load_active_fitness_plan(conn)
    days = conn.execute('SELECT * FROM days ORDER BY date').fetchall()
    results = []

    for day in days:
        date_text = day['date']
        wd = weekday_name(date_text)
        weekday_plan = plan_map.get(wd, {})
        session = conn.execute('SELECT * FROM training_sessions WHERE date = ? ORDER BY session_index LIMIT 1', (date_text,)).fetchone()
        exercise_count = conn.execute('''
            SELECT COUNT(*) AS c
            FROM exercises e JOIN training_sessions s ON s.id = e.session_id
            WHERE s.date = ?
        ''', (date_text,)).fetchone()['c']
        meals = conn.execute('SELECT * FROM meals WHERE date = ? ORDER BY meal_slot', (date_text,)).fetchall()

        training_status, training_missing = classify_training(day, session, exercise_count, weekday_plan)
        nutrition_status, nutrition_missing, meal_slots = classify_nutrition(meals)
        planned_slot = expected_plan_slot(day, weekday_plan)

        overall = 'complete' if training_status == 'complete' and nutrition_status == 'complete' else 'partial'
        if training_status == 'missing' or nutrition_status == 'missing':
            overall = 'incomplete'

        results.append({
            'date': date_text,
            'weekday': wd,
            'planned_slot': planned_slot,
            'recorded_plan_slot': day['plan_slot'],
            'training': {
                'status': training_status,
                'missing_fields': training_missing,
                'session_type': session['type'] if session else None,
                'theme': session['theme'] if session else None,
                'exercise_count': exercise_count,
            },
            'nutrition': {
                'status': nutrition_status,
                'missing_fields': nutrition_missing,
                'meal_slots': meal_slots,
            },
            'overall_status': overall,
        })

    summary = {
        'generated_at': dt.datetime.utcnow().isoformat() + 'Z',
        'database': str(DB_PATH),
        'active_fitness_plan': {
            'version_label': active_fitness_plan['version_label'] if active_fitness_plan else None,
            'plan_type': active_fitness_plan['plan_type'] if active_fitness_plan else None,
            'source_note': active_fitness_plan['source_note'] if active_fitness_plan else None,
            'slot_count': active_fitness_plan['slot_count'] if active_fitness_plan else 0,
        },
        'days_checked': len(results),
        'complete_days': sum(1 for r in results if r['overall_status'] == 'complete'),
        'partial_days': sum(1 for r in results if r['overall_status'] == 'partial'),
        'incomplete_days': sum(1 for r in results if r['overall_status'] == 'incomplete'),
        'results': results,
    }
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default=str(DB_PATH))
    parser.add_argument('--output', default=str(OUTPUT_PATH))
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    report = build_audit(conn)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
