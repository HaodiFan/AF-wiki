#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/AF-wiki')
SYNC_SCRIPT = ROOT / 'areas' / 'fitness' / '40-data' / 'sync_markdown_to_sqlite.py'


def main() -> int:
    result = subprocess.run(['python3', str(SYNC_SCRIPT)], cwd=ROOT)
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
