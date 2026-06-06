#!/usr/bin/env python3
"""Sync durable facts from AF-wiki fitness.db into Hermes holographic memory.

Design goals:
- Keep AF-wiki markdown + fitness.db canonical
- Derive only high-signal, durable facts for agent recall
- Safe default is --dry-run
- Write through Holographic MemoryStore API when applying so entity links / HRR rebuilds happen

Usage examples:
  python3 infra/indexing/fitness_db_to_holographic.py --dry-run
  python3 infra/indexing/fitness_db_to_holographic.py --apply
  python3 infra/indexing/fitness_db_to_holographic.py --apply --memory-db ~/.hermes/memory_store.db
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path("/home/AF-wiki")
FITNESS_DB = ROOT / "data" / "fitness.db"
DEFAULT_MEMORY_DB = Path.home() / ".hermes" / "memory_store.db"
STATE_PATH = ROOT / "infra" / "indexing" / ".fitness_db_to_holographic_state.json"
HERMES_REPO = Path("/root/.hermes/hermes-agent")


@dataclass
class Fact:
    content: str
    category: str
    tags: str
    source_key: str
    hash: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write facts into holographic memory")
    mode.add_argument("--dry-run", action="store_true", help="print planned facts without writing (default)")
    p.add_argument("--fitness-db", default=str(FITNESS_DB), help="path to AF-wiki fitness.db")
    p.add_argument("--memory-db", default=str(DEFAULT_MEMORY_DB), help="path to holographic memory_store.db")
    p.add_argument("--limit", type=int, default=0, help="optional max number of facts to process")
    return p.parse_args()


def stable_hash(*parts: str) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def normalize_ws(text: str | None) -> str:
    return " ".join((text or "").split()).strip()


def trunc(text: str, limit: int = 500) -> str:
    text = normalize_ws(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def make_fact(content: str, *, category: str, tags: Sequence[str], source_key: str) -> Fact:
    normalized = trunc(content)
    return Fact(
        content=normalized,
        category=category,
        tags=",".join(tags),
        source_key=source_key,
        hash=stable_hash(source_key, normalized),
    )


def fetch_all(conn: sqlite3.Connection, sql: str, params: Sequence | None = None) -> list[sqlite3.Row]:
    cur = conn.execute(sql, params or [])
    return cur.fetchall()


def extract_plan_facts(conn: sqlite3.Connection) -> list[Fact]:
    facts: list[Fact] = []

    active_context_plans = fetch_all(
        conn,
        """
        SELECT id, version_label, effective_date, status, source_note, summary, plan_type,
               summary_zh, summary_en
        FROM plan_versions
        WHERE status = 'active'
        ORDER BY id DESC
        """,
    )
    for row in active_context_plans:
        label = normalize_ws(row[1]) or "unnamed plan"
        source_note = normalize_ws(row[4]) or "unknown-source"
        plan_type = normalize_ws(row[6]) or "unknown"
        effective_date = normalize_ws(row[2])
        summary = normalize_ws(row[5]) or normalize_ws(row[8]) or normalize_ws(row[7])
        parts = [f"Active fitness-area plan context: {label}", f"type={plan_type}"]
        if effective_date:
            parts.append(f"effective_date={effective_date}")
        parts.append(f"source_note={source_note}")
        if summary:
            parts.append(f"summary={summary}")
        facts.append(
            make_fact(
                "; ".join(parts),
                category="user_pref",
                tags=["area:fitness", "kind:active_plan_context", f"plan_type:{plan_type}", f"source:{source_note}"],
                source_key=f"plan_versions:active_context:{row[0]}",
            )
        )

    fitness_plans = fetch_all(
        conn,
        """
        SELECT pv.id, pv.version_label, pv.effective_date, pv.status, pv.source_note, pv.summary, pv.plan_type,
               pv.summary_zh, pv.summary_en, COUNT(ps.id) AS slot_count
        FROM plan_versions pv
        LEFT JOIN plan_slots ps ON ps.plan_version_id = pv.id
        WHERE pv.plan_type = 'fitness_training'
        GROUP BY pv.id, pv.version_label, pv.effective_date, pv.status, pv.source_note, pv.summary, pv.plan_type,
                 pv.summary_zh, pv.summary_en
        ORDER BY CASE WHEN pv.status = 'active' THEN 0 ELSE 1 END, pv.effective_date DESC, pv.id DESC
        """,
    )
    if not fitness_plans:
        return facts

    row = fitness_plans[0]
    label = normalize_ws(row[1]) or "unnamed fitness plan"
    source_note = normalize_ws(row[4]) or "unknown-source"
    plan_type = normalize_ws(row[6]) or "fitness_training"
    effective_date = normalize_ws(row[2])
    summary = normalize_ws(row[5]) or normalize_ws(row[8]) or normalize_ws(row[7])
    slot_count = row[9] or 0
    parts = [f"Active training plan for fitness execution: {label}", f"type={plan_type}", f"slot_count={slot_count}"]
    if effective_date:
        parts.append(f"effective_date={effective_date}")
    parts.append(f"source_note={source_note}")
    if summary:
        parts.append(f"summary={summary}")
    facts.append(
        make_fact(
            "; ".join(parts),
            category="user_pref",
            tags=["area:fitness", "kind:active_training_plan", f"plan_type:{plan_type}", f"source:{source_note}"],
            source_key=f"plan_versions:active_training:{row[0]}",
        )
    )

    slots = fetch_all(
        conn,
        """
        SELECT weekday, weekday_order, slot_name, details, slot_name_zh, slot_name_en, details_zh, details_en
        FROM plan_slots
        WHERE plan_version_id = ?
        ORDER BY weekday_order, id
        """,
        [row[0]],
    )
    for slot in slots:
        weekday = normalize_ws(slot[0])
        slot_name = normalize_ws(slot[2]) or normalize_ws(slot[5]) or normalize_ws(slot[4]) or "unnamed slot"
        details = normalize_ws(slot[3]) or normalize_ws(slot[7]) or normalize_ws(slot[6])
        content = f"Active training plan weekday slot: {weekday} -> {slot_name}"
        if details:
            content += f"; details={details}"
        facts.append(
            make_fact(
                content,
                category="user_pref",
                tags=[
                    "area:fitness",
                    "kind:training_plan_slot",
                    f"plan_type:{plan_type}",
                    f"source:{source_note}",
                    f"weekday:{weekday.lower()}" if weekday else "weekday:unknown",
                ],
                source_key=f"plan_slots:training:{row[0]}:{weekday}:{slot_name}",
            )
        )
    return facts


def split_summary_sentences(text: str | None) -> list[str]:
    value = normalize_ws(text)
    if not value:
        return []
    parts = [segment.strip() for segment in value.replace("\n", " ").split(". ")]
    out: list[str] = []
    for part in parts:
        cleaned = normalize_ws(part.rstrip("."))
        if cleaned:
            out.append(cleaned)
    return out


def pick_day_note_highlights(notes: str | None, limit: int = 2) -> list[str]:
    lines = [line.strip() for line in (notes or "").splitlines() if line.strip()]
    preferred_prefixes = (
        "Overall status:",
        "Plan adherence:",
        "Training completion:",
        "Nutrition completion:",
        "Main implication:",
        "Recovery / notes:",
        "Main gap / correction:",
    )
    picked: list[str] = []
    for prefix in preferred_prefixes:
        for line in lines:
            if line.startswith(prefix):
                value = normalize_ws(line.split(":", 1)[1] if ":" in line else line)
                if value and value not in picked:
                    picked.append(value)
                    break
        if len(picked) >= limit:
            return picked[:limit]

    for sentence in split_summary_sentences(notes):
        if sentence not in picked:
            picked.append(sentence)
        if len(picked) >= limit:
            break
    return picked[:limit]


def extract_day_summary_facts(conn: sqlite3.Connection) -> list[Fact]:
    facts: list[Fact] = []
    rows = fetch_all(
        conn,
        """
        SELECT date, plan_slot, actual_training_status, nutrition_status, notes, source_note
        FROM days
        WHERE notes IS NOT NULL AND trim(notes) != ''
        ORDER BY date DESC
        LIMIT 14
        """,
    )
    for row in rows:
        date, plan_slot, training_status, nutrition_status, notes, source_note = row
        base_parts = [
            f"Fitness day on {date}",
            f"training_status={normalize_ws(training_status) or 'unknown'}",
            f"nutrition_status={normalize_ws(nutrition_status) or 'unknown'}",
        ]
        if normalize_ws(plan_slot):
            base_parts.append(f"plan_slot={normalize_ws(plan_slot)}")
        facts.append(
            make_fact(
                "; ".join(base_parts),
                category="user_pref",
                tags=["area:fitness", "kind:day_status", f"date:{date}", f"source:{normalize_ws(source_note) or 'fitness.db'}"],
                source_key=f"days:{date}:status",
            )
        )

        for idx, highlight in enumerate(pick_day_note_highlights(notes, limit=2), start=1):
            facts.append(
                make_fact(
                    f"Fitness day note on {date}: {highlight}",
                    category="user_pref",
                    tags=["area:fitness", "kind:day_note_highlight", f"date:{date}", f"source:{normalize_ws(source_note) or 'fitness.db'}"],
                    source_key=f"days:{date}:highlight:{idx}",
                )
            )
    return facts


def extract_session_pattern_facts(conn: sqlite3.Connection) -> list[Fact]:
    facts: list[Fact] = []
    rows = fetch_all(
        conn,
        """
        SELECT id, date, type, theme, intensity, exertion_level, evaluation, recovery_notes, source_note
        FROM training_sessions
        ORDER BY date DESC, session_index DESC, id DESC
        LIMIT 12
        """,
    )
    for row in rows:
        sid, date, stype, theme, intensity, exertion, evaluation, recovery, source_note = row
        parts = [f"Fitness training session on {date}"]
        if normalize_ws(stype):
            parts.append(f"type={normalize_ws(stype)}")
        if normalize_ws(theme):
            parts.append(f"theme={normalize_ws(theme)}")
        if normalize_ws(intensity):
            parts.append(f"intensity={normalize_ws(intensity)}")
        if normalize_ws(exertion):
            parts.append(f"exertion={normalize_ws(exertion)}")
        if normalize_ws(evaluation):
            parts.append(f"evaluation={normalize_ws(evaluation)}")
        if normalize_ws(recovery):
            parts.append(f"recovery={normalize_ws(recovery)}")
        facts.append(
            make_fact(
                "; ".join(parts),
                category="user_pref",
                tags=[
                    "area:fitness",
                    "kind:training_session",
                    f"date:{date}",
                    f"session_type:{normalize_ws(stype) or 'unknown'}",
                    f"source:{normalize_ws(source_note) or 'fitness.db'}",
                ],
                source_key=f"training_sessions:{sid}",
            )
        )
    return facts


def extract_meal_pattern_facts(conn: sqlite3.Connection) -> list[Fact]:
    facts: list[Fact] = []
    rows = fetch_all(
        conn,
        """
        SELECT date, meal_slot, foods_text, estimated_protein_g, notes, source_note
        FROM meals
        WHERE notes IS NOT NULL AND trim(notes) != ''
        ORDER BY date DESC, id DESC
        LIMIT 12
        """,
    )
    for row in rows:
        date, meal_slot, foods_text, protein_g, notes, source_note = row
        note = normalize_ws(notes)
        if not note:
            continue
        parts = [f"Fitness meal note on {date}", f"meal_slot={normalize_ws(meal_slot) or 'unknown'}"]
        if normalize_ws(foods_text):
            parts.append(f"foods={normalize_ws(foods_text)}")
        if protein_g is not None:
            parts.append(f"estimated_protein_g={protein_g}")
        parts.append(f"note={note}")
        facts.append(
            make_fact(
                "; ".join(parts),
                category="user_pref",
                tags=[
                    "area:fitness",
                    "kind:meal_note",
                    f"date:{date}",
                    f"meal_slot:{normalize_ws(meal_slot).lower().replace(' ', '_') or 'unknown'}",
                    f"source:{normalize_ws(source_note) or 'fitness.db'}",
                ],
                source_key=f"meals:{date}:{meal_slot}:{normalize_ws(source_note) or 'fitness.db'}",
            )
        )
    return facts


def dedupe_facts(facts: Iterable[Fact]) -> list[Fact]:
    seen: set[str] = set()
    out: list[Fact] = []
    for fact in facts:
        key = fact.hash
        if key in seen:
            continue
        seen.add(key)
        out.append(fact)
    return out


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"facts": {}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def extract_all_facts(fitness_db: Path) -> list[Fact]:
    conn = sqlite3.connect(str(fitness_db))
    conn.row_factory = sqlite3.Row
    try:
        facts: list[Fact] = []
        facts.extend(extract_plan_facts(conn))
        facts.extend(extract_day_summary_facts(conn))
        facts.extend(extract_session_pattern_facts(conn))
        facts.extend(extract_meal_pattern_facts(conn))
        return dedupe_facts(facts)
    finally:
        conn.close()


def apply_facts_via_memory_store(memory_db: Path, facts: Sequence[Fact]) -> tuple[int, int]:
    import sys

    sys.path.insert(0, str(HERMES_REPO))
    from plugins.memory.holographic.store import MemoryStore  # type: ignore

    store = MemoryStore(db_path=str(memory_db))
    conn = store._conn
    existing = {row[0]: row[1] for row in conn.execute("SELECT content, category FROM facts")}
    inserted = 0
    updated = 0

    for fact in facts:
        if fact.content in existing:
            current_category = existing[fact.content]
            conn.execute(
                "UPDATE facts SET category = ?, tags = ?, updated_at = CURRENT_TIMESTAMP WHERE content = ?",
                (fact.category or current_category, fact.tags, fact.content),
            )
            updated += 1
            continue
        store.add_fact(fact.content, category=fact.category, tags=fact.tags)
        inserted += 1

    conn.commit()
    return inserted, updated


def main() -> int:
    args = parse_args()
    dry_run = not args.apply
    fitness_db = Path(args.fitness_db).expanduser()
    memory_db = Path(args.memory_db).expanduser()

    if not fitness_db.exists():
        raise SystemExit(f"fitness DB not found: {fitness_db}")

    facts = extract_all_facts(fitness_db)
    if args.limit > 0:
        facts = facts[: args.limit]

    state = load_state()
    known = state.setdefault("facts", {})
    changed = [fact for fact in facts if known.get(fact.hash) != fact.content]

    if dry_run:
        print(f"mode=dry-run fitness_db={fitness_db} memory_db={memory_db} total_facts={len(facts)} changed_facts={len(changed)}")
        for fact in changed[:25]:
            print(f"- [{fact.category}] {fact.content} | tags={fact.tags}")
        if len(changed) > 25:
            print(f"... {len(changed) - 25} more changed facts")
        return 0

    memory_db.parent.mkdir(parents=True, exist_ok=True)
    inserted, updated = apply_facts_via_memory_store(memory_db, changed)
    for fact in changed:
        known[fact.hash] = fact.content
    save_state(state)
    print(json.dumps({
        "mode": "apply",
        "fitness_db": str(fitness_db),
        "memory_db": str(memory_db),
        "total_facts": len(facts),
        "changed_facts": len(changed),
        "inserted": inserted,
        "updated": updated,
        "state": str(STATE_PATH),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
