---
title: "ADR-0001 Local Source Vault"
type: adr
status: accepted
date: 2026-05-18
tags:
  - type/adr
  - area/knowledge
  - wiki/af
---
# ADR-0001 Local Source Vault

## Decision

AF-wiki GitHub stores only curated knowledge, source manifests, topic maps, and provenance metadata.

Original PDFs, scans, full OCR, and full original reports live outside the repo in a local source vault:

```text
/Users/anthonyf/projects/personal/SnapAF/AF-wiki-sources
```

Tools may override this path through `AF_WIKI_SOURCES`.

## Context

The previous knowledge-area rule copied original source documents into `areas/knowledge/source-documents/`. This made the repo heavy and mixed extracted knowledge with raw material. The BaiduSync import alone added more than 400 MB of source documents, and historical notebook scans/OCR would make the problem larger.

## Consequences

- Topic notes use `Source References` with `source_id`, not links to raw files in the repo.
- `areas/knowledge/source-manifests/sources.jsonl` is the Git-tracked provenance layer.
- Source-vault integrity is checked by size and SHA-256.
- `.gitignore` blocks raw source directories from being committed again.
- Git history must be rewritten once to remove previously committed raw source material from GitHub.

## Non-goals

- Do not use Git LFS for raw sources.
- Do not make GitHub the backup system for private or large original documents.
