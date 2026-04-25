#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/home/AF-wiki')
LOG_PATH = ROOT / 'log.md'
AUDIT_PATH = ROOT / 'areas' / 'fitness' / '40-data' / 'latest-audit.json'


def recent_log_lines(limit: int = 6):
    if not LOG_PATH.exists():
        return []
    lines = [line.rstrip() for line in LOG_PATH.read_text(encoding='utf-8').splitlines() if line.strip()]
    return lines[:limit]


def audit_snapshot():
    if not AUDIT_PATH.exists():
        return {'status': 'missing'}
    data = json.loads(AUDIT_PATH.read_text(encoding='utf-8'))
    return {
        'generated_at': data.get('generated_at'),
        'days_checked': data.get('days_checked'),
        'complete_days': data.get('complete_days'),
        'partial_days': data.get('partial_days'),
        'incomplete_days': data.get('incomplete_days'),
    }


def main() -> int:
    payload = {
        'wiki': 'AF-wiki',
        'briefing': {
            'recent_log_head': recent_log_lines(),
            'fitness_audit': audit_snapshot(),
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
