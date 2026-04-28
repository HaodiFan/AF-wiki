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
  - refreshes both `/home/AF-wiki/README.md` and `/home/HaodiFan-profile/README.md` recent-update sections from the last 7 days of fitness check-ins

## Design rule
- Markdown remains canonical.
- Infra scripts are wrappers / derived-runtime utilities.
- The initial Phase 1 scope is intentionally small: sync + doctor + briefing.
