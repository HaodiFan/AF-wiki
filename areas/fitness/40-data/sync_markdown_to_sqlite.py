#!/usr/bin/env python3
import argparse
import json
import re
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path('/home/AF-wiki')
FITNESS_DIR = ROOT / 'areas' / 'fitness'
DB_PATH = ROOT / 'data' / 'fitness.db'
CHECKINS_PATH = FITNESS_DIR / '10-checkins' / '2026-04.md'
CURRENT_PLAN_PATH = FITNESS_DIR / '02-current-plan.md'
PLAN_VERSION_DIR = FITNESS_DIR / 'plan-versions'

DATE_RE = re.compile(r'^## (\d{4}-\d{2}-\d{2})(?: \(([^)]+)\))?$')
SESSION_RE = re.compile(r'^#### Session (\d+)')
KV_RE = re.compile(r'^- ([^:]+):\s*(.*)$')
MEAL_HEADER_RE = re.compile(r'^- ([A-Za-z /-]+):\s*$')
LIST_ITEM_RE = re.compile(r'^-\s+(.*)$')
PLAN_DAY_RE = re.compile(r'^### ([A-Za-z]+) — (.+)$')
PLAN_META_RE = re.compile(r'^- ([^:]+):\s*(.*)$')

WEEKDAY_ORDER = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7,
}


def parse_duration_seconds(text: str) -> Optional[int]:
    text = text.strip()
    if not text or 'not precisely' in text.lower():
        return None
    parts = [p.strip() for p in text.split('/')]
    first = parts[0]
    match = re.search(r'(\d+):(\d+)', first)
    if not match:
        return None
    return int(match.group(1)) * 60 + int(match.group(2))


def parse_float(text: str) -> Optional[float]:
    if not text:
        return None
    m = re.search(r'-?\d+(?:\.\d+)?', text.replace(',', ''))
    return float(m.group(0)) if m else None


def normalize_key(text: str) -> str:
    return text.strip().lower().replace(' ', '_').replace('/', '_').replace('-', '_')


@dataclass
class Exercise:
    name: str
    raw_text: str
    set_order: int
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    weight_value: Optional[float] = None
    reps: Optional[int] = None
    duration_seconds: Optional[int] = None
    distance_m: Optional[float] = None
    pace_text: Optional[str] = None
    raw_text_zh: Optional[str] = None
    raw_text_en: Optional[str] = None


@dataclass
class Session:
    session_index: int
    metrics: dict = field(default_factory=dict)
    exercises: List[Exercise] = field(default_factory=list)
    theme_zh: Optional[str] = None
    theme_en: Optional[str] = None
    intensity_zh: Optional[str] = None
    intensity_en: Optional[str] = None
    evaluation_zh: Optional[str] = None
    evaluation_en: Optional[str] = None
    recovery_notes_zh: Optional[str] = None
    recovery_notes_en: Optional[str] = None


@dataclass
class Meal:
    slot: str
    foods_text: Optional[str] = None
    estimated_calories: Optional[float] = None
    estimated_protein_g: Optional[float] = None
    notes: Optional[str] = None
    slot_zh: Optional[str] = None
    slot_en: Optional[str] = None
    foods_text_zh: Optional[str] = None
    foods_text_en: Optional[str] = None
    notes_zh: Optional[str] = None
    notes_en: Optional[str] = None


@dataclass
class DayRecord:
    date: str
    event_type: str = 'daily'
    title_suffix: Optional[str] = None
    summary_lines: List[str] = field(default_factory=list)
    coaching_lines: List[str] = field(default_factory=list)
    sessions: List[Session] = field(default_factory=list)
    meals: List[Meal] = field(default_factory=list)


def split_bilingual_text(text: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    if not text:
        return None, None
    value = text.strip()
    if not value:
        return None, None
    separators = ['｜', '||', ' / ', ' // ']
    for separator in separators:
        if separator in value:
            left, right = [part.strip() for part in value.split(separator, 1)]
            if left and right:
                left_has_cjk = bool(re.search(r'[\u4e00-\u9fff]', left))
                right_has_cjk = bool(re.search(r'[\u4e00-\u9fff]', right))
                if left_has_cjk and not right_has_cjk:
                    return left, right
                if right_has_cjk and not left_has_cjk:
                    return right, left
                return left, right
    has_cjk = bool(re.search(r'[\u4e00-\u9fff]', value))
    if has_cjk:
        return value, None
    return None, value


def parse_exercise_line(line: str, order: int) -> Exercise:
    body = line[2:].strip()
    if ' — ' in body:
        name, detail = body.split(' — ', 1)
    else:
        name, detail = body, ''
    weight_value = None
    reps = None
    duration_seconds = None
    distance_m = None
    pace_text = None

    wxr = re.search(r'(\d+(?:\.\d+)?)\s*x\s*(\d+)', detail)
    if wxr:
        weight_value = float(wxr.group(1))
        reps = int(wxr.group(2))
    else:
        duration_match = re.search(r'(\d+)\s*sec', detail)
        if duration_match:
            duration_seconds = int(duration_match.group(1))
        dist_match = re.search(r'(\d+(?:\.\d+)?)\s*m', detail)
        if dist_match:
            distance_m = float(dist_match.group(1))
        pace_match = re.search(r"(\d+'\d+\"\s*/\s*100\s*m)", detail)
        if pace_match:
            pace_text = pace_match.group(1)
        bare_rep = re.fullmatch(r'(\d+)(?:,\s*\d+)*', detail.strip())
        if bare_rep:
            parts = [int(x.strip()) for x in detail.split(',') if x.strip().isdigit()]
            reps = parts[0] if len(parts) == 1 else None

    name_zh, name_en = split_bilingual_text(name.strip())
    detail_zh, detail_en = split_bilingual_text(detail.strip())

    return Exercise(
        name=name.strip(),
        raw_text=detail.strip(),
        set_order=order,
        name_zh=name_zh,
        name_en=name_en,
        weight_value=weight_value,
        reps=reps,
        duration_seconds=duration_seconds,
        distance_m=distance_m,
        pace_text=pace_text,
        raw_text_zh=detail_zh,
        raw_text_en=detail_en,
    )


def parse_checkins(path: Path) -> List[DayRecord]:
    lines = path.read_text(encoding='utf-8').splitlines()
    records: List[DayRecord] = []
    current: Optional[DayRecord] = None
    current_section = None
    current_session: Optional[Session] = None
    current_meal: Optional[Meal] = None
    exercise_order = 0

    def finalize_meal():
        nonlocal current_meal
        if current and current_meal:
            current.meals.append(current_meal)
            current_meal = None

    def finalize_session():
        nonlocal current_session, exercise_order
        if current and current_session:
            current.sessions.append(current_session)
            current_session = None
            exercise_order = 0

    def finalize_record():
        finalize_meal()
        finalize_session()
        if current:
            records.append(current)

    for raw in lines:
        line = raw.rstrip()
        m = DATE_RE.match(line)
        if m:
            finalize_record()
            date, suffix = m.groups()
            event_type = 'daily' if suffix is None else suffix.strip()
            current = DayRecord(date=date, event_type=event_type, title_suffix=suffix)
            current_section = None
            current_session = None
            current_meal = None
            continue
        if not current:
            continue
        if line.startswith('### '):
            finalize_meal()
            finalize_session()
            current_section = line[4:].strip().lower()
            continue
        sm = SESSION_RE.match(line)
        if sm:
            finalize_session()
            current_session = Session(session_index=int(sm.group(1)))
            current_section = 'training'
            continue
        if line == 'Exercises:':
            current_section = 'exercises'
            continue
        if current_section == 'day summary' and line.startswith('- '):
            current.summary_lines.append(line[2:].strip())
            continue
        if current_section == 'coaching interpretation' and line.startswith('- '):
            current.coaching_lines.append(line[2:].strip())
            continue
        if current_section == 'training' and current_session:
            km = KV_RE.match(line)
            if km:
                key, value = km.groups()
                normalized_key = normalize_key(key)
                normalized_value = value.strip()
                current_session.metrics[normalized_key] = normalized_value
                zh_value, en_value = split_bilingual_text(normalized_value)
                if normalized_key == 'theme':
                    current_session.theme_zh = zh_value
                    current_session.theme_en = en_value
                elif normalized_key == 'intensity':
                    current_session.intensity_zh = zh_value
                    current_session.intensity_en = en_value
                elif normalized_key == 'evaluation':
                    current_session.evaluation_zh = zh_value
                    current_session.evaluation_en = en_value
                elif normalized_key in {'recovery___finish', 'recovery___notes'}:
                    current_session.recovery_notes_zh = zh_value
                    current_session.recovery_notes_en = en_value
            continue
        if current_section == 'exercises' and current_session and line.startswith('- '):
            exercise_order += 1
            current_session.exercises.append(parse_exercise_line(line, exercise_order))
            continue
        if current_section == 'meals / intake':
            mh = MEAL_HEADER_RE.match(line)
            if mh:
                finalize_meal()
                slot = mh.group(1).strip()
                slot_zh, slot_en = split_bilingual_text(slot)
                current_meal = Meal(slot=slot, slot_zh=slot_zh, slot_en=slot_en)
                continue
            if current_meal:
                km = KV_RE.match(line.strip())
                if km:
                    key, value = km.groups()
                    key = normalize_key(key)
                    normalized_value = value.strip()
                    zh_value, en_value = split_bilingual_text(normalized_value)
                    if key == 'foods':
                        current_meal.foods_text = normalized_value
                        current_meal.foods_text_zh = zh_value
                        current_meal.foods_text_en = en_value
                    elif key == 'calories':
                        current_meal.estimated_calories = parse_float(normalized_value)
                    elif key == 'protein':
                        current_meal.estimated_protein_g = parse_float(normalized_value)
                    elif key == 'notes':
                        current_meal.notes = normalized_value
                        current_meal.notes_zh = zh_value
                        current_meal.notes_en = en_value
                continue
    finalize_record()
    return records


def extract_plan_meta(lines: List[str]) -> dict:
    meta = {}
    for line in lines:
        m = PLAN_META_RE.match(line)
        if m:
            meta[normalize_key(m.group(1))] = m.group(2).strip()
    for field in ['version_label', 'active_version_label', 'current_status', 'main_rationale', 'source_note']:
        if field in meta:
            zh_value, en_value = split_bilingual_text(meta[field])
            meta[f'{field}_zh'] = zh_value
            meta[f'{field}_en'] = en_value
    return meta


def infer_plan_type(path: Path, lines: List[str], meta: dict) -> str:
    explicit = meta.get('plan_type')
    if explicit:
        return explicit
    text = '\n'.join(lines).lower()
    if path.name == '02-current-plan.md' and 'architecture-evolution' in text:
        return 'architecture_memory'
    if 'weekly structure' in text or 'current training structure' in text:
        return 'fitness_training'
    if 'monday —' in text or 'tuesday —' in text or 'saturday —' in text:
        return 'fitness_training'
    return 'generic'


def parse_plan_file(path: Path, status_override: Optional[str] = None) -> Tuple[dict, List[dict]]:
    lines = path.read_text(encoding='utf-8').splitlines()
    meta = extract_plan_meta(lines)
    meta['plan_type'] = infer_plan_type(path, lines, meta)
    sections = []
    current_day = None
    bullets: List[str] = []
    in_structure = False
    for line in lines:
        if line.startswith('## Current training structure') or line.startswith('## Weekly structure'):
            in_structure = True
            continue
        if line.startswith('## ') and not (line.startswith('## Current training structure') or line.startswith('## Weekly structure')):
            if current_day:
                sections.append({'weekday': current_day[0], 'slot_name': current_day[1], 'details': '\n'.join(bullets)})
                current_day = None
                bullets = []
            in_structure = False
        if in_structure:
            m = PLAN_DAY_RE.match(line)
            if m:
                if current_day:
                    sections.append({'weekday': current_day[0], 'slot_name': current_day[1], 'details': '\n'.join(bullets)})
                current_day = (m.group(1), m.group(2).strip())
                bullets = []
                continue
            if current_day and line.startswith('- '):
                bullets.append(line[2:].strip())
    if current_day:
        sections.append({'weekday': current_day[0], 'slot_name': current_day[1], 'details': '\n'.join(bullets)})
    for section in sections:
        slot_zh, slot_en = split_bilingual_text(section['slot_name'])
        details_zh, details_en = split_bilingual_text(section['details'])
        section['slot_name_zh'] = slot_zh
        section['slot_name_en'] = slot_en
        section['details_zh'] = details_zh
        section['details_en'] = details_en
    meta['status'] = status_override or meta.get('status', 'active')
    return meta, sections


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript('''
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS sync_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at TEXT DEFAULT CURRENT_TIMESTAMP,
        source_note TEXT,
        summary_json TEXT
    );

    CREATE TABLE IF NOT EXISTS days (
        date TEXT PRIMARY KEY,
        plan_slot TEXT,
        actual_training_status TEXT,
        nutrition_status TEXT,
        notes TEXT,
        notes_zh TEXT,
        notes_en TEXT,
        source_note TEXT,
        last_synced_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS day_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        event_type TEXT NOT NULL,
        title_suffix TEXT,
        details TEXT,
        source_note TEXT,
        UNIQUE(date, event_type, title_suffix)
    );

    CREATE TABLE IF NOT EXISTS training_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        session_index INTEGER,
        type TEXT,
        theme TEXT,
        theme_zh TEXT,
        theme_en TEXT,
        duration_seconds INTEGER,
        calories_total REAL,
        calories_active REAL,
        avg_hr REAL,
        max_hr REAL,
        intensity TEXT,
        intensity_zh TEXT,
        intensity_en TEXT,
        exertion_level TEXT,
        evaluation TEXT,
        evaluation_zh TEXT,
        evaluation_en TEXT,
        recovery_notes TEXT,
        recovery_notes_zh TEXT,
        recovery_notes_en TEXT,
        raw_metrics_json TEXT,
        source_note TEXT,
        UNIQUE(date, session_index, source_note)
    );

    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL REFERENCES training_sessions(id) ON DELETE CASCADE,
        set_order INTEGER,
        exercise_name TEXT,
        exercise_name_zh TEXT,
        exercise_name_en TEXT,
        raw_text TEXT,
        raw_text_zh TEXT,
        raw_text_en TEXT,
        weight_value REAL,
        reps INTEGER,
        duration_seconds INTEGER,
        distance_m REAL,
        pace_text TEXT
    );

    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        meal_slot TEXT NOT NULL,
        meal_slot_zh TEXT,
        meal_slot_en TEXT,
        foods_text TEXT,
        foods_text_zh TEXT,
        foods_text_en TEXT,
        estimated_calories REAL,
        estimated_protein_g REAL,
        notes TEXT,
        notes_zh TEXT,
        notes_en TEXT,
        source_note TEXT,
        UNIQUE(date, meal_slot, source_note)
    );

    CREATE TABLE IF NOT EXISTS plan_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version_label TEXT,
        effective_date TEXT,
        status TEXT,
        plan_type TEXT,
        source_note TEXT UNIQUE,
        summary TEXT,
        summary_zh TEXT,
        summary_en TEXT
    );

    CREATE TABLE IF NOT EXISTS plan_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_version_id INTEGER NOT NULL REFERENCES plan_versions(id) ON DELETE CASCADE,
        weekday TEXT,
        weekday_order INTEGER,
        slot_name TEXT,
        slot_name_zh TEXT,
        slot_name_en TEXT,
        details TEXT,
        details_zh TEXT,
        details_en TEXT,
        UNIQUE(plan_version_id, weekday, slot_name)
    );

    CREATE TABLE IF NOT EXISTS audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        training_completeness TEXT,
        nutrition_completeness TEXT,
        missing_fields TEXT,
        checked_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(date, checked_at)
    );
    ''')
    migration_map = {
        'days': ['notes_zh TEXT', 'notes_en TEXT'],
        'training_sessions': [
            'theme_zh TEXT', 'theme_en TEXT', 'intensity_zh TEXT', 'intensity_en TEXT',
            'evaluation_zh TEXT', 'evaluation_en TEXT', 'recovery_notes_zh TEXT', 'recovery_notes_en TEXT'
        ],
        'exercises': ['exercise_name_zh TEXT', 'exercise_name_en TEXT', 'raw_text_zh TEXT', 'raw_text_en TEXT'],
        'meals': ['meal_slot_zh TEXT', 'meal_slot_en TEXT', 'foods_text_zh TEXT', 'foods_text_en TEXT', 'notes_zh TEXT', 'notes_en TEXT'],
        'plan_versions': ['plan_type TEXT', 'summary_zh TEXT', 'summary_en TEXT'],
        'plan_slots': ['slot_name_zh TEXT', 'slot_name_en TEXT', 'details_zh TEXT', 'details_en TEXT'],
    }
    for table_name, column_defs in migration_map.items():
        existing_columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()}
        for column_def in column_defs:
            column_name = column_def.split()[0]
            if column_name not in existing_columns:
                conn.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_def}')
    conn.commit()


def compute_day_status(record: DayRecord) -> Tuple[Optional[str], Optional[str], str]:
    training_status = None
    if any('training completion' in line.lower() and 'no training performed' in line.lower() for line in record.coaching_lines):
        training_status = 'rest'
    elif any('intentional rest day' in line.lower() or 'confirmed no-training day' in line.lower() or 'confirmed no training' in line.lower() for line in record.coaching_lines):
        training_status = 'rest'
    elif record.sessions:
        training_status = 'completed'
    elif record.event_type == 'daily':
        training_status = 'unconfirmed'

    meal_slots = {meal.slot.lower() for meal in record.meals}
    if not meal_slots:
        nutrition_status = None
    elif {'breakfast', 'lunch', 'dinner'}.issubset(meal_slots):
        nutrition_status = 'substantially_logged'
    elif 'dinner' in meal_slots or 'breakfast / daytime intake' in meal_slots or 'breakfast' in meal_slots:
        nutrition_status = 'partially_logged'
    else:
        nutrition_status = 'lightly_logged'

    notes = '\n'.join(record.summary_lines + record.coaching_lines).strip()
    return training_status, nutrition_status, notes


def summarize_bilingual_day_notes(record: DayRecord) -> Tuple[Optional[str], Optional[str]]:
    joined = '\n'.join(record.summary_lines + record.coaching_lines).strip()
    return split_bilingual_text(joined)


def upsert_day_record(conn: sqlite3.Connection, record: DayRecord, source_note: str) -> dict:
    if record.event_type == 'daily':
        training_status, nutrition_status, notes = compute_day_status(record)
        notes_zh, notes_en = summarize_bilingual_day_notes(record)
        plan_slot = None
        for line in record.summary_lines:
            if line.lower().startswith('plan slot:'):
                plan_slot = line.split(':', 1)[1].strip()
                break
        conn.execute(
            '''INSERT INTO days(date, plan_slot, actual_training_status, nutrition_status, notes, notes_zh, notes_en, source_note, last_synced_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(date) DO UPDATE SET
                 plan_slot=excluded.plan_slot,
                 actual_training_status=excluded.actual_training_status,
                 nutrition_status=excluded.nutrition_status,
                 notes=excluded.notes,
                 notes_zh=excluded.notes_zh,
                 notes_en=excluded.notes_en,
                 source_note=excluded.source_note,
                 last_synced_at=CURRENT_TIMESTAMP''',
            (record.date, plan_slot, training_status, nutrition_status, notes or None, notes_zh, notes_en, source_note),
        )
        conn.execute('DELETE FROM training_sessions WHERE date = ? AND source_note = ?', (record.date, source_note))
        conn.execute('DELETE FROM meals WHERE date = ? AND source_note = ?', (record.date, source_note))
        for session in record.sessions:
            metrics = session.metrics
            cursor = conn.execute(
                '''INSERT INTO training_sessions(
                       date, session_index, type, theme, theme_zh, theme_en, duration_seconds, calories_total, calories_active,
                       avg_hr, max_hr, intensity, intensity_zh, intensity_en, exertion_level, evaluation, evaluation_zh, evaluation_en,
                       recovery_notes, recovery_notes_zh, recovery_notes_en, raw_metrics_json, source_note
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    record.date,
                    session.session_index,
                    metrics.get('type'),
                    metrics.get('theme'),
                    session.theme_zh,
                    session.theme_en,
                    parse_duration_seconds(metrics.get('duration', '')),
                    parse_float(metrics.get('calories', '')),
                    parse_float(metrics.get('active_calories', '')),
                    parse_float(metrics.get('avg_hr', '')),
                    parse_float(metrics.get('hr_range', '').split('-')[-1]) if metrics.get('hr_range') else None,
                    metrics.get('intensity'),
                    session.intensity_zh,
                    session.intensity_en,
                    metrics.get('exertion_level'),
                    metrics.get('evaluation'),
                    session.evaluation_zh,
                    session.evaluation_en,
                    metrics.get('recovery___finish') or metrics.get('recovery___notes') or metrics.get('recovery___finish'),
                    session.recovery_notes_zh,
                    session.recovery_notes_en,
                    json.dumps(metrics, ensure_ascii=False),
                    source_note,
                ),
            )
            session_id = cursor.lastrowid
            for ex in session.exercises:
                conn.execute(
                    '''INSERT INTO exercises(session_id, set_order, exercise_name, exercise_name_zh, exercise_name_en, raw_text, raw_text_zh, raw_text_en, weight_value, reps, duration_seconds, distance_m, pace_text)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (session_id, ex.set_order, ex.name, ex.name_zh, ex.name_en, ex.raw_text, ex.raw_text_zh, ex.raw_text_en, ex.weight_value, ex.reps, ex.duration_seconds, ex.distance_m, ex.pace_text),
                )
        for meal in record.meals:
            conn.execute(
                '''INSERT INTO meals(date, meal_slot, meal_slot_zh, meal_slot_en, foods_text, foods_text_zh, foods_text_en, estimated_calories, estimated_protein_g, notes, notes_zh, notes_en, source_note)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(date, meal_slot, source_note) DO UPDATE SET
                     meal_slot_zh=excluded.meal_slot_zh,
                     meal_slot_en=excluded.meal_slot_en,
                     foods_text=excluded.foods_text,
                     foods_text_zh=excluded.foods_text_zh,
                     foods_text_en=excluded.foods_text_en,
                     estimated_calories=excluded.estimated_calories,
                     estimated_protein_g=excluded.estimated_protein_g,
                     notes=excluded.notes,
                     notes_zh=excluded.notes_zh,
                     notes_en=excluded.notes_en''',
                (record.date, meal.slot, meal.slot_zh, meal.slot_en, meal.foods_text, meal.foods_text_zh, meal.foods_text_en, meal.estimated_calories, meal.estimated_protein_g, meal.notes, meal.notes_zh, meal.notes_en, source_note),
            )
    else:
        details = '\n'.join(record.summary_lines + record.coaching_lines).strip() or None
        conn.execute(
            '''INSERT INTO day_events(date, event_type, title_suffix, details, source_note)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(date, event_type, title_suffix) DO UPDATE SET details=excluded.details, source_note=excluded.source_note''',
            (record.date, record.event_type, record.title_suffix, details, source_note),
        )
    return {'date': record.date, 'event_type': record.event_type, 'sessions': len(record.sessions), 'meals': len(record.meals)}


def sync_plans(conn: sqlite3.Connection) -> List[dict]:
    plan_sources = [(CURRENT_PLAN_PATH, 'active')] + [(p, 'archived') for p in sorted(PLAN_VERSION_DIR.glob('*.md'))]
    results = []
    for path, default_status in plan_sources:
        meta, slots = parse_plan_file(path, status_override=default_status)
        summary = meta.get('current_status') or meta.get('main_rationale') or meta.get('source_note')
        summary_zh, summary_en = split_bilingual_text(summary)
        if not summary_zh:
            summary_zh = meta.get('current_status_zh') or meta.get('main_rationale_zh') or meta.get('source_note_zh')
        if not summary_en:
            summary_en = meta.get('current_status_en') or meta.get('main_rationale_en') or meta.get('source_note_en')
        cursor = conn.execute(
            '''INSERT INTO plan_versions(version_label, effective_date, status, plan_type, source_note, summary, summary_zh, summary_en)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(source_note) DO UPDATE SET
                 version_label=excluded.version_label,
                 effective_date=excluded.effective_date,
                 status=excluded.status,
                 plan_type=excluded.plan_type,
                 summary=excluded.summary,
                 summary_zh=excluded.summary_zh,
                 summary_en=excluded.summary_en''',
            (
                meta.get('active_version_label') or meta.get('version_label'),
                meta.get('effective_date') or meta.get('recorded_on'),
                meta.get('status', default_status),
                meta.get('plan_type'),
                str(path.relative_to(ROOT)),
                summary,
                summary_zh,
                summary_en,
            ),
        )
        plan_id = conn.execute('SELECT id FROM plan_versions WHERE source_note = ?', (str(path.relative_to(ROOT)),)).fetchone()[0]
        conn.execute('DELETE FROM plan_slots WHERE plan_version_id = ?', (plan_id,))
        for slot in slots:
            conn.execute(
                '''INSERT INTO plan_slots(plan_version_id, weekday, weekday_order, slot_name, slot_name_zh, slot_name_en, details, details_zh, details_en)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    plan_id,
                    slot['weekday'],
                    WEEKDAY_ORDER.get(slot['weekday']),
                    slot['slot_name'],
                    slot.get('slot_name_zh'),
                    slot.get('slot_name_en'),
                    slot['details'],
                    slot.get('details_zh'),
                    slot.get('details_en'),
                ),
            )
        results.append({'source': str(path.relative_to(ROOT)), 'slots': len(slots)})
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkins', default=str(CHECKINS_PATH))
    parser.add_argument('--db', default=str(DB_PATH))
    args = parser.parse_args()

    checkins_path = Path(args.checkins)
    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    init_db(conn)

    checkin_records = parse_checkins(checkins_path)
    checkin_results = [upsert_day_record(conn, r, str(checkins_path.relative_to(ROOT))) for r in checkin_records]
    plan_results = sync_plans(conn)

    summary = {
        'checkin_records': len(checkin_results),
        'daily_records': sum(1 for r in checkin_results if r['event_type'] == 'daily'),
        'event_records': sum(1 for r in checkin_results if r['event_type'] != 'daily'),
        'training_sessions': conn.execute('SELECT COUNT(*) FROM training_sessions').fetchone()[0],
        'exercises': conn.execute('SELECT COUNT(*) FROM exercises').fetchone()[0],
        'meals': conn.execute('SELECT COUNT(*) FROM meals').fetchone()[0],
        'plan_versions': conn.execute('SELECT COUNT(*) FROM plan_versions').fetchone()[0],
        'plan_slots': conn.execute('SELECT COUNT(*) FROM plan_slots').fetchone()[0],
        'plan_sources_synced': plan_results,
    }
    conn.execute('INSERT INTO sync_runs(source_note, summary_json) VALUES (?, ?)', (str(checkins_path.relative_to(ROOT)), json.dumps(summary, ensure_ascii=False)))
    conn.commit()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
