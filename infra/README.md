---
title: "README"
tags:
  - wiki/af
---
# AF-wiki Infra

Derived runtime / sidecar layer for indexing, maintenance, and briefing.

## Current commands
- `python3 infra/indexing/af_wiki_sync.py`
  - refreshes the current markdown -> SQLite fitness sync
- `python3 infra/jobs/af_wiki_doctor.py`
  - reruns the current fitness audit and prints a compact summary
- `python3 infra/jobs/af_wiki_briefing.py`
  - prints a lightweight operational briefing from `log.md` + latest fitness audit
- `python3 infra/jobs/af_wiki_briefing.py --refresh-all-readmes`
  - refreshes both `AF-wiki/README.md` and `HaodiFan/README.md` recent-update sections from the last 7 days of fitness check-ins
- `python3 infra/source_vault.py audit-sources --hash`
  - verifies that source manifest entries exist in the local source vault and match recorded size/hash
- `python3 infra/source_vault.py scan-for-raw`
  - fails if PDFs, scans, full OCR, or raw source paths are present in the Git repo
- `python3 infra/source_vault.py sync-sources-to-vault`
  - copies legacy or explicit source material into `$AF_WIKI_SOURCES`

## Design rule
- Markdown remains canonical.
- Raw sources live in the local source vault, not in Git.
- Infra scripts are wrappers / derived-runtime utilities.
- The initial Phase 1 scope is intentionally small: sync + doctor + briefing.
