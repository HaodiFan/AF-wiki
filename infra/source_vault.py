#!/usr/bin/env python3
"""Utilities for AF-wiki's local source vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = ROOT.parent / "AF-wiki-sources"
MANIFEST_PATH = ROOT / "areas/knowledge/source-manifests/sources.jsonl"
RAW_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".tif",
    ".tiff",
    ".heic",
    ".webp",
}
RAW_PATH_PARTS = {
    "areas/knowledge/source-documents",
    "areas/knowledge/source-fulltext",
    "areas/knowledge/anthonydb-research/originals",
    "areas/knowledge/source-notes/historical-notebooks",
}


def source_root() -> Path:
    return Path(os.environ.get("AF_WIKI_SOURCES", DEFAULT_SOURCE_ROOT)).expanduser()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> list[dict]:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"missing manifest: {MANIFEST_PATH}")
    entries = []
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def audit_sources(args: argparse.Namespace) -> int:
    root = source_root()
    entries = load_manifest()
    missing = []
    mismatched = []

    for entry in entries:
        path = root / entry["source_vault_path"]
        if not path.exists():
            missing.append(entry)
            continue
        size = path.stat().st_size
        if size != entry["size_bytes"]:
            mismatched.append((entry, f"size {size} != {entry['size_bytes']}"))
            continue
        if args.hash and sha256_file(path) != entry["sha256"]:
            mismatched.append((entry, "sha256 mismatch"))

    payload = {
        "source_root": str(root),
        "entries": len(entries),
        "missing": len(missing),
        "mismatched": len(mismatched),
        "hash_checked": bool(args.hash),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if missing:
        print("Missing sources:", file=sys.stderr)
        for entry in missing[:20]:
            print(f"- {entry['source_id']} {entry['source_vault_path']}", file=sys.stderr)
    if mismatched:
        print("Mismatched sources:", file=sys.stderr)
        for entry, reason in mismatched[:20]:
            print(f"- {entry['source_id']} {entry['source_vault_path']}: {reason}", file=sys.stderr)

    return 1 if missing or mismatched else 0


def scan_for_raw(_: argparse.Namespace) -> int:
    cmd = ["git", "ls-files", "--cached", "--others", "--exclude-standard"]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True)
    violations = []
    for raw in result.stdout.splitlines():
        path = raw.strip()
        if not path:
            continue
        suffix = Path(path).suffix.lower()
        if suffix in RAW_EXTENSIONS:
            violations.append(path)
            continue
        if any(path == part or path.startswith(f"{part}/") for part in RAW_PATH_PARTS):
            violations.append(path)

    if violations:
        print("Raw source material is not allowed in AF-wiki Git:", file=sys.stderr)
        for path in violations[:100]:
            print(f"- {path}", file=sys.stderr)
        return 1

    print("No raw source material found in Git-tracked or untracked repo files.")
    return 0


def sync_sources_to_vault(args: argparse.Namespace) -> int:
    root = source_root()
    root.mkdir(parents=True, exist_ok=True)

    if args.source and args.dest:
        source = Path(args.source).expanduser()
        dest = root / args.dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest) if source.is_file() else shutil.copytree(source, dest, dirs_exist_ok=True)
        print(f"synced {source} -> {dest}")
        return 0

    legacy_pairs = [
        (ROOT / "areas/knowledge/source-documents/baidu-sync", root / "raw/baidu-sync"),
        (ROOT / "areas/knowledge/source-documents/historical-notebooks", root / "raw/historical-notebooks"),
        (ROOT / "areas/knowledge/source-notes/historical-notebooks", root / "fulltext/historical-notebooks"),
        (ROOT / "areas/knowledge/anthonydb-research/originals", root / "fulltext/anthonydb-originals"),
    ]
    copied = 0
    for source, dest in legacy_pairs:
        if not source.exists():
            continue
        dest.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rsync", "-a", f"{source}/", f"{dest}/"], check=True)
        print(f"synced {source} -> {dest}")
        copied += 1

    if copied == 0:
        print("No legacy source directories found. Use --source and --dest for explicit imports.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit-sources", help="verify source manifest files exist in the local source vault")
    audit.add_argument("--hash", action="store_true", help="also verify sha256 checksums")
    audit.set_defaults(func=audit_sources)

    scan = sub.add_parser("scan-for-raw", help="fail if raw source material is in the repo")
    scan.set_defaults(func=scan_for_raw)

    sync = sub.add_parser("sync-sources-to-vault", help="copy source material into the local source vault")
    sync.add_argument("--source", help="explicit source file or directory")
    sync.add_argument("--dest", help="destination path relative to AF_WIKI_SOURCES")
    sync.set_defaults(func=sync_sources_to_vault)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
