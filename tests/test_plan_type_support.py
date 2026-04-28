import json
import sqlite3
import subprocess
from pathlib import Path

ROOT = Path('/home/AF-wiki')
SYNC_CMD = ['python3', 'infra/indexing/af_wiki_sync.py']
DOCTOR_CMD = ['python3', 'infra/jobs/af_wiki_doctor.py', '--skip-refresh']
DB_PATH = ROOT / 'data' / 'fitness.db'


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def test_sync_marks_mixed_plan_types_and_preserves_fitness_plan_slots():
    sync = run(SYNC_CMD)
    assert sync.returncode == 0, sync.stderr or sync.stdout

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        'select version_label, status, source_note, plan_type from plan_versions order by source_note'
    ).fetchall()
    by_source = {row['source_note']: dict(row) for row in rows}

    assert by_source['areas/fitness/02-current-plan.md']['plan_type'] == 'architecture_memory'
    assert by_source['areas/fitness/plan-versions/2026-04-11-fat-loss-plan-v1.md']['plan_type'] == 'fitness_training'
    assert by_source['areas/fitness/plan-versions/2026-04-24-archived-fat-loss-plan-v1.md']['plan_type'] == 'fitness_training'

    fallback_fitness = conn.execute(
        """
        select pv.id, pv.source_note, count(ps.id) as slot_count
        from plan_versions pv
        left join plan_slots ps on ps.plan_version_id = pv.id
        where pv.plan_type = 'fitness_training'
        group by pv.id, pv.source_note
        order by case when pv.status = 'active' then 0 else 1 end, pv.effective_date desc, pv.id desc
        limit 1
        """
    ).fetchone()
    assert fallback_fitness is not None, 'expected a fallback fitness_training plan row'
    assert fallback_fitness['slot_count'] == 7
    assert fallback_fitness['source_note'].endswith('2026-04-11-fat-loss-plan-v1.md')


def test_doctor_reports_active_fitness_plan_source():
    doctor = run(DOCTOR_CMD)
    assert doctor.returncode == 0, doctor.stderr or doctor.stdout
    payload = json.loads(doctor.stdout)
    assert payload['active_fitness_plan']['plan_type'] == 'fitness_training'
    assert payload['active_fitness_plan']['slot_count'] == 7
    assert payload['active_fitness_plan']['source_note'].endswith('2026-04-11-fat-loss-plan-v1.md')


def test_sync_adds_bilingual_shadow_columns_and_keeps_existing_days_queryable():
    sync = run(SYNC_CMD)
    assert sync.returncode == 0, sync.stderr or sync.stdout

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    expected_columns = {
        'days': {'notes_zh', 'notes_en'},
        'training_sessions': {'theme_zh', 'theme_en', 'intensity_zh', 'intensity_en', 'evaluation_zh', 'evaluation_en', 'recovery_notes_zh', 'recovery_notes_en'},
        'exercises': {'exercise_name_zh', 'exercise_name_en', 'raw_text_zh', 'raw_text_en'},
        'meals': {'meal_slot_zh', 'meal_slot_en', 'foods_text_zh', 'foods_text_en', 'notes_zh', 'notes_en'},
        'plan_versions': {'summary_zh', 'summary_en', 'plan_type'},
        'plan_slots': {'slot_name_zh', 'slot_name_en', 'details_zh', 'details_en'},
    }
    for table_name, required in expected_columns.items():
        columns = {row['name'] for row in conn.execute(f'PRAGMA table_info({table_name})')}
        missing = required - columns
        assert not missing, f'{table_name} missing columns: {missing}'

    day = conn.execute(
        "select date, notes_zh, notes_en from days where date = '2026-04-23'"
    ).fetchone()
    assert day is not None

    meal = conn.execute(
        "select meal_slot, meal_slot_zh, meal_slot_en, foods_text_zh, foods_text_en from meals where date = '2026-04-23' and meal_slot = 'Lunch'"
    ).fetchone()
    assert meal is not None
    assert meal['meal_slot'] == 'Lunch'
