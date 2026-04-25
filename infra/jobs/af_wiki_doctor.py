#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/AF-wiki')
AUDIT_SCRIPT = ROOT / 'areas' / 'fitness' / '40-data' / 'audit_fitness_completeness.py'
OUTPUT_PATH = ROOT / 'areas' / 'fitness' / '40-data' / 'latest-audit.json'


def run_audit() -> int:
    result = subprocess.run(['python3', str(AUDIT_SCRIPT)], cwd=ROOT)
    return result.returncode


def summarize() -> int:
    if not OUTPUT_PATH.exists():
        print(json.dumps({'error': 'audit output missing', 'path': str(OUTPUT_PATH)}, ensure_ascii=False, indent=2))
        return 1
    data = json.loads(OUTPUT_PATH.read_text(encoding='utf-8'))
    compact = {
        'generated_at': data.get('generated_at'),
        'active_fitness_plan': data.get('active_fitness_plan'),
        'days_checked': data.get('days_checked'),
        'complete_days': data.get('complete_days'),
        'partial_days': data.get('partial_days'),
        'incomplete_days': data.get('incomplete_days'),
        'incomplete_dates': [r['date'] for r in data.get('results', []) if r.get('overall_status') == 'incomplete'],
        'partial_dates': [r['date'] for r in data.get('results', []) if r.get('overall_status') == 'partial'],
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='AF-wiki doctor for current sidecar checks.')
    parser.add_argument('--skip-refresh', action='store_true', help='Do not rerun the audit before summarizing')
    args = parser.parse_args()

    if not args.skip_refresh:
        rc = run_audit()
        if rc != 0:
            return rc
    return summarize()


if __name__ == '__main__':
    raise SystemExit(main())
