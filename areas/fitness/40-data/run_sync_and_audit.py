#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/AF-wiki')
SYNC_SCRIPT = ROOT / 'areas' / 'fitness' / '40-data' / 'sync_markdown_to_sqlite.py'
AUDIT_SCRIPT = ROOT / 'areas' / 'fitness' / '40-data' / 'audit_fitness_completeness.py'


def run_step(label: str, command: list[str]) -> int:
    print(f'==> {label}')
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        print(f'FAILED: {label}', file=sys.stderr)
        return result.returncode
    print(f'OK: {label}\n')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='Run fitness markdown sync and completeness audit.')
    parser.add_argument('--skip-sync', action='store_true', help='Only run the audit step')
    args = parser.parse_args()

    if not args.skip_sync:
        rc = run_step('sync markdown -> sqlite', ['python3', str(SYNC_SCRIPT)])
        if rc != 0:
            return rc

    rc = run_step('audit sqlite completeness', ['python3', str(AUDIT_SCRIPT)])
    if rc != 0:
        return rc

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
