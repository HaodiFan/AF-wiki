#!/usr/bin/env python3
"""Sync selected durable AF-wiki notes into a Holographic-style fact store.

Design goals:
- AF-wiki markdown remains canonical
- This script builds a derived retrieval index only
- Safe default is --dry-run
- Minimal dependency surface: stdlib + sqlite3 only

Usage examples:
  python3 infra/indexing/af_wiki_memory_sync.py --dry-run
  python3 infra/indexing/af_wiki_memory_sync.py --apply
  python3 infra/indexing/af_wiki_memory_sync.py --apply --db ~/.hermes/memory_store.db
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path("/home/AF-wiki")
DEFAULT_DB = Path.home() / ".hermes" / "memory_store.db"
STATE_PATH = ROOT / "infra" / "indexing" / ".af_wiki_memory_sync_state.json"

SOURCE_PATHS = [
    ROOT / "SCHEMA.md",
    ROOT / "areas" / "index.md",
    ROOT / "areas" / "fitness" / "00-profile.md",
    ROOT / "areas" / "fitness" / "01-goals.md",
    ROOT / "areas" / "fitness" / "02-current-plan.md",
    ROOT / "areas" / "fitness" / "03-decision-rules.md",
    ROOT / "areas" / "work" / "00-active-context.md",
]
TOPIC_GLOBS = [
    ROOT / "areas" / "knowledge" / "topics" / "*.md",
]

FACT_SCHEMA = """
CREATE TABLE IF NOT EXISTS facts (
    fact_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    content         TEXT NOT NULL UNIQUE,
    category        TEXT DEFAULT 'general',
    tags            TEXT DEFAULT '',
    trust_score     REAL DEFAULT 0.5,
    retrieval_count INTEGER DEFAULT 0,
    helpful_count   INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hrr_vector      BLOB
);
CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
"""

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.*)$")
FRONTMATTER_SPLIT_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
INLINE_CODE_ONLY_RE = re.compile(r"^`[^`]+`/?$")
WIKILINK_ONLY_RE = re.compile(r"^\[\[[^\]]+\]\]$")
PATHY_RE = re.compile(r"^(?:[\w.-]+/)+[\w.-]+/?$")

HIGH_SIGNAL_HEADINGS = {
    "SCHEMA": {
        "Active evo-memory baseline (2026-04-24)",
        "Core design decision",
        "What belongs in `areas/`",
        "What belongs in `resources/`",
        "Area modularity rules",
        "Lead -> research -> area integration flow",
    },
    "areas/index": {
        "Area rules",
        "Current status",
        "How to use this registry",
        "Boundary rules",
        "Routing rule for second-brain orchestration",
    },
}
TOPIC_ALLOWED_HEADINGS = {
    "Definition",
    "Why it matters",
    "Related topics",
    "Open questions",
    "Current architecture decision",
    "Recommended three-layer model",
    "Operational priority order",
    "Recommended integration pattern",
    "Suggested implementation path",
    "Design rules",
    "Practical usage model for Hermes",
}
DROP_PREFIXES = (
    "Current modules:",
    "Future modules can be added as needed.",
    "Examples:",
    "Rule:",
    "Important:",
    "Planned shared usage:",
    "Current canonical usage:",
    "Minimum contract for a new area:",
    "Registry rule:",
    "Local rule:",
    "For the current repo state, read in this order:",
)


@dataclass
class Fact:
    content: str
    category: str
    tags: str
    source: str
    hash: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write facts into the SQLite store")
    mode.add_argument("--dry-run", action="store_true", help="print planned facts without writing (default)")
    p.add_argument("--db", default=str(DEFAULT_DB), help="path to memory_store.db")
    p.add_argument("--limit", type=int, default=0, help="optional max number of facts to process")
    return p.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_SPLIT_RE.sub("", text, count=1)


def stable_hash(*parts: str) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def slug_from_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return rel.removesuffix(".md")


def normalize_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def infer_category(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("areas/fitness/"):
        return "user_pref"
    if rel.startswith("areas/work/"):
        return "project"
    if rel.startswith("areas/knowledge/topics/"):
        return "tool"
    return "general"


def infer_tags(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    tags = [f"source:{rel}"]
    if rel.startswith("areas/fitness/"):
        tags += ["area:fitness", "kind:durable"]
    elif rel.startswith("areas/work/"):
        tags += ["area:work", "kind:durable"]
    elif rel.startswith("areas/knowledge/topics/"):
        tags += ["area:knowledge", "kind:topic"]
    elif rel == "SCHEMA.md":
        tags += ["kind:schema", "scope:root"]
    elif rel == "areas/index.md":
        tags += ["kind:index", "scope:areas"]
    return tags


def is_noise_body(body: str) -> bool:
    b = normalize_whitespace(body)
    if not b:
        return True
    if b.startswith(DROP_PREFIXES):
        return True
    if WIKILINK_ONLY_RE.match(b):
        return True
    if INLINE_CODE_ONLY_RE.match(b):
        return True
    if PATHY_RE.match(b):
        return True
    if b in {"```text", "```", "AF-wiki/"}:
        return True
    if b.startswith("├──") or b.startswith("│") or b.startswith("└──"):
        return True
    if b.startswith("1.") or b.startswith("2.") or b.startswith("3.") or b.startswith("4."):
        return True
    if "[[" in b and len(b) < 40:
        return True
    return False


def allow_heading(slug: str, heading: str | None) -> bool:
    if heading is None:
        return False
    if slug in HIGH_SIGNAL_HEADINGS:
        return heading in HIGH_SIGNAL_HEADINGS[slug]
    if slug.startswith("areas/knowledge/topics/"):
        return heading in TOPIC_ALLOWED_HEADINGS
    return True


def clean_body(body: str) -> str:
    b = normalize_whitespace(body)
    b = b.replace("**", "")
    return b.strip()


def extract_facts_from_markdown(path: Path) -> list[Fact]:
    text = strip_frontmatter(read_text(path))
    category = infer_category(path)
    tags = infer_tags(path)
    slug = slug_from_path(path)

    facts: list[Fact] = []
    current_heading: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        heading_match = HEADING_RE.match(line)
        if heading_match:
            current_heading = normalize_whitespace(heading_match.group(2))
            continue
        if not allow_heading(slug, current_heading):
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            body = clean_body(bullet_match.group(1))
            if is_noise_body(body):
                continue
            fact_text = f"[{slug}]"
            if current_heading:
                fact_text += f" {current_heading}:"
            fact_text += f" {body}"
            facts.append(
                Fact(
                    content=fact_text,
                    category=category,
                    tags=",".join(tags),
                    source=slug,
                    hash=stable_hash(slug, current_heading or "", body),
                )
            )
            continue

        if current_heading and len(line) < 240 and not line.startswith(">"):
            body = clean_body(line)
            if is_noise_body(body):
                continue
            fact_text = f"[{slug}] {current_heading}: {body}"
            facts.append(
                Fact(
                    content=fact_text,
                    category=category,
                    tags=",".join(tags),
                    source=slug,
                    hash=stable_hash(slug, current_heading, body),
                )
            )

    return dedupe_facts(facts)


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


def expand_topic_paths() -> list[Path]:
    paths: list[Path] = []
    for pattern in TOPIC_GLOBS:
        paths.extend(sorted(pattern.parent.glob(pattern.name)))
    return paths


def all_source_paths() -> list[Path]:
    paths = [p for p in SOURCE_PATHS if p.exists()]
    paths.extend(expand_topic_paths())
    return paths


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"facts": {}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def ensure_db(conn: sqlite3.Connection) -> None:
    conn.executescript(FACT_SCHEMA)
    conn.commit()


def upsert_fact(conn: sqlite3.Connection, fact: Fact) -> str:
    row = conn.execute("SELECT fact_id FROM facts WHERE content = ?", (fact.content,)).fetchone()
    if row:
        conn.execute(
            "UPDATE facts SET category = ?, tags = ?, updated_at = CURRENT_TIMESTAMP WHERE fact_id = ?",
            (fact.category, fact.tags, row[0]),
        )
        return "updated"
    conn.execute(
        "INSERT INTO facts (content, category, tags, trust_score) VALUES (?, ?, ?, ?)",
        (fact.content, fact.category, fact.tags, 0.5),
    )
    return "inserted"


def main() -> int:
    args = parse_args()
    dry_run = not args.apply
    paths = all_source_paths()
    extracted: list[Fact] = []
    for path in paths:
        extracted.extend(extract_facts_from_markdown(path))
    extracted = dedupe_facts(extracted)
    if args.limit > 0:
        extracted = extracted[: args.limit]

    state = load_state()
    known = state.setdefault("facts", {})
    changed = [f for f in extracted if known.get(f.hash) != f.content]

    if dry_run:
        print(f"mode=dry-run total_paths={len(paths)} total_facts={len(extracted)} changed_facts={len(changed)}")
        for fact in changed[:20]:
            print(f"- [{fact.category}] {fact.content}")
        if len(changed) > 20:
            print(f"... {len(changed) - 20} more changed facts")
        return 0

    db_path = Path(args.db).expanduser()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    try:
        ensure_db(conn)
        inserted = 0
        updated = 0
        for fact in changed:
            action = upsert_fact(conn, fact)
            if action == "inserted":
                inserted += 1
            else:
                updated += 1
            known[fact.hash] = fact.content
        conn.commit()
    finally:
        conn.close()

    save_state(state)
    print(
        json.dumps(
            {
                "mode": "apply",
                "db": str(db_path),
                "total_paths": len(paths),
                "total_facts": len(extracted),
                "changed_facts": len(changed),
                "inserted": inserted,
                "updated": updated,
                "state": str(STATE_PATH),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
