# AF Wiki Schema

> Legacy bootstrap schema.
> This file belongs to the earlier `wiki/`-only experiment.
> The current canonical architecture is documented in the root [[SCHEMA]], with navigation starting from [[START-HERE]] and [[index]].

## Domain
General-purpose knowledge wiki for AF, initialized for future source ingestion and topic pages.

## Conventions
- Wiki root: `/home/AF-wiki`
- Use lowercase-hyphenated slugs for page filenames.
- Raw sources live under `sources/` and are immutable once saved.
- Managed wiki pages live under `wiki/`.
- Use `[[wikilinks]]` for internal references.
- Update `wiki/index.md` and append `wiki/log.md` on every ingest, query save, lint, or structural change.
- Surface contradictions explicitly instead of silently overwriting claims.

## Page Types
- Entity page — person, company, product, organization, place
- Concept page — idea, method, architecture, topic
- Summary page — synthesis of one source or one cluster of sources

## Page Template
```markdown
# Page Title

> One-line summary

## Overview

## Key facts / claims
- Claim (→ [[source-summary]])

## Related
- [[other-page]] — why it's related

## Counter-arguments & data gaps
- Open questions or caveats

## Sources
- [Source Title](../sources/filename) — YYYY-MM-DD
```

## Index Policy
- `wiki/index.md` is the entry point and should list every managed page.
- Group entries under Entities, Concepts, and Sources processed.

## Logging Policy
- `wiki/log.md` is append-only.
- Format entries as `## [YYYY-MM-DD] action | subject` followed by a compact summary.
