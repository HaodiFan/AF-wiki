---
title: "Source Manifests"
type: index
area: knowledge
status: active
tags:
  - area/knowledge
  - type/index
  - wiki/af
---
# Source Manifests

AF-wiki keeps only curated knowledge, topic maps, and source metadata in Git.

Original PDFs, scans, full OCR, and full original reports live in the local source vault:

- Default source vault: `/Users/anthonyf/projects/personal/SnapAF/AF-wiki-sources`
- Override env var: `AF_WIKI_SOURCES`
- Machine-readable manifest: [[sources.jsonl]]
- Local checksum file: `/Users/anthonyf/projects/personal/SnapAF/AF-wiki-sources/checksums.sha256`

## Current Counts

| Source | Count |
| --- | ---: |
| `anthonydb-originals` | 9 |
| `baidu-sync` | 103 |
| `historical-notebooks` | 15 |

## Rules

- Do not commit PDFs, scans, full OCR, or raw fulltext reports to this repo.
- Use `source_id` and `source_vault_path` for provenance.
- Use `python3 infra/source_vault.py audit-sources` before deleting or rewriting source material.
- Use `python3 infra/source_vault.py scan-for-raw` before committing knowledge-area changes.
