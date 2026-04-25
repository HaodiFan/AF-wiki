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


def test_sync_marks_mixed_plan_types_and_preserves_fitness_active_slots():
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

    active_fitness = conn.execute(
        """
        select pv.id, pv.source_note, count(ps.id) as slot_count
        from plan_versions pv
        left join plan_slots ps on ps.plan_version_id = pv.id
        where pv.status = 'active' and pv.plan_type = 'fitness_training'
        group by pv.id, pv.source_note
        """
    ).fetchall()
    assert active_fitness, 'expected an active fitness_training plan row'
    assert active_fitness[0]['slot_count'] == 7


def test_doctor_reports_active_fitness_plan_source():
    doctor = run(DOCTOR_CMD)
    assert doctor.returncode == 0, doctor.stderr or doctor.stdout
    payload = json.loads(doctor.stdout)
    assert payload['active_fitness_plan']['plan_type'] == 'fitness_training'
    assert payload['active_fitness_plan']['slot_count'] == 7
    assert payload['active_fitness_plan']['source_note'].endswith('2026-04-11-fat-loss-plan-v1.md')
