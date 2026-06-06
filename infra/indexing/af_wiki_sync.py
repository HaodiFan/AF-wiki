#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYNC_SCRIPT = ROOT / 'areas' / 'fitness' / '40-data' / 'sync_markdown_to_sqlite.py'
MEMORY_SYNC_SCRIPT = ROOT / 'infra' / 'indexing' / 'fitness_db_to_holographic.py'


def run_step(cmd: list[str]) -> int:
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


def main() -> int:
    rc = run_step(['python3', str(SYNC_SCRIPT)])
    if rc != 0:
        return rc
    rc = run_step(['python3', str(MEMORY_SYNC_SCRIPT), '--apply'])
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
