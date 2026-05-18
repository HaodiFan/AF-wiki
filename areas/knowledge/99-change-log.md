---
title: "99-change-log"
tags:
  - area/knowledge
  - type/log
  - wiki/af
---
# Knowledge Area Change Log

## [2026-05-18] refactor | raw sources moved to local source vault
- Moved PDFs, scans, full OCR, and AnthonyDB raw originals out of the Git-tracked wiki model
- Added `source-manifests/` with source IDs, local source-vault paths, hashes, sizes, and topic routing
- Replaced `Original Files In Wiki` references with `Source References`
- Updated knowledge rules so GitHub keeps curated knowledge, not original source material

## [2026-05-18] ingest | historical handwritten notebooks recorded
- Added `historical-notebooks/` as a retained collection for historical handwritten/OCR learning notes
- Moved Notebook 1 and Notebook 2 OCR Markdown into the local source vault
- Moved `notebook2.pdf` into the local source vault
- Added a Notebook 1 scan manifest instead of bulk-copying the 1.9 GB raw scan bundle
- Linked the collection into the knowledge index and routed its clusters to existing topic nodes

## [2026-04-26] ingest | Ontology research recorded
- Added the full-text `Ontology在现代AI系统中的演化与应用` research note under `resources/research/`
- Promoted `Ontology / 本体` as a durable knowledge topic
- Linked ontology into the Agent Systems map and related runtime, tool-use, and data-management topics

## [2026-04-26] graph | Obsidian tags and source-note graph support
- Added frontmatter tags across knowledge Markdown notes
- Created 103 tagged sidecar notes under `areas/knowledge/source-notes/baidu-sync/`
- Enabled Obsidian graph display for tags, attachments, and orphan nodes

## [2026-04-26] archive | BaiduSync source documents moved into knowledge area
- Copied 103 source documents from `/Users/anthonyf/Desktop/BaiduSync` into `areas/knowledge/source-documents/baidu-sync/`
- Preserved source folder layout inside the wiki
- Replaced the central corpus-index archive with topic-level integration in the knowledge area

## [2026-04-26] ingest | Harness Engineering research notes recorded
- Added two full-text research notes under `resources/research/`
- Promoted `Agent Harness Engineering` and `Wire Harness Engineering` as knowledge topics
- Linked the agent-harness note into the Agent Systems map and Agent Runtime topic

## [2026-04-25] graph | Knowledge Graph v1 topic/map layer
- Added `topics/` and `maps/` as the durable knowledge graph layer
- Created the first Agent Systems topic map and seven topic nodes
- Clarified lead -> research -> topic -> map promotion rules
- Updated templates for lead, research, topic, and map notes

## [2026-04-20] archive | historical originals copied into current wiki
- Added `anthonydb-research/originals/` as the raw-source layer for curated historical imports
- Kept curated notes and original notes as separate archive layers

## [2026-04-20] ingest | historical second-pass research curation
- Added two more durable imports from the fruit-fly and Opencode clusters
- Kept only methodology and architecture-pattern notes
- Continued to skip digest, overview, and troubleshooting-heavy materials

## [2026-04-20] ingest | historical research curated into knowledge area
- Added `anthonydb-research/` as a curated historical-research collection
- Imported only high-density research notes into the current wiki archive
- Explicitly skipped keypoints, navigation, quick-reference, and obvious digest-style materials

## [2026-04-20] create | Knowledge promoted to first-class area
- Moved retained article notes from `resources/knowledge/` to `areas/knowledge/`
- Established `SCHEMA.md` and `index.md` for the knowledge area
- Clarified that weak-signal leads remain in `resources/leads/`
