---
title: "Historical Notebooks / 历史学习笔记"
type: collection
area: knowledge
status: active
aliases:
  - Historical Notebooks
  - 历史学习笔记
  - 手写学习笔记归档
tags:
  - area/knowledge
  - collection/historical-notebooks
  - type/collection
  - wiki/af
---
# Historical Notebooks / 历史学习笔记

## Purpose

This collection records Anthony's historical handwritten/OCR learning notes as retained knowledge sources.

The collection is a source-and-routing layer: repo notes preserve the curated essence and provenance, while full OCR, scans, and PDFs live in the local source vault.

## Curated Entries

- [[notebook1-foundations-and-engineering|Notebook 1 - Foundations, CV, Systems, and Engineering]] — broad foundation notes across RAG, multimodal models, CV/OCR, Python internals, distributed systems, blockchain, and algorithms.
- [[notebook2-llm-reasoning-agentic-rl-ai4science|Notebook 2 - LLM Reasoning, Agentic RL, OS Agents, and AI4Science]] — frontier notes around reasoning data, DeepSeek R1, agentic RL, OS agents, AI4Science, and quantum/Python side notes.

## Source Inventory

- [[../source-manifests/historical-notebooks|Historical Notebook Source Manifest]] — source IDs for Notebook 1 scans, Notebook 2 PDF, and Notebook 1/2 OCR.
- `historical:notebook1-ocr` — full OCR in local source vault.
- `historical:notebook2-ocr` — full OCR in local source vault.
- `historical:notebook2-pdf` — original 34-page PDF in local source vault.

## Topic Routing

| Historical cluster | Current wiki routing |
| --- | --- |
| LLM reasoning, cold-start SFT, GRPO, verifier/self-check | [[../topics/large-language-models|Large Language Models]], [[../topics/llm-safety-interpretability|LLM Safety and Interpretability]] |
| OS agents, GUI grounding, browser/desktop benchmarks | [[../maps/agent-systems-map|Agent Systems Map]], [[../topics/agent-core|Agent Core]], [[../topics/agent-runtime|Agent Runtime]], [[../topics/multimodal-ai|Multimodal AI]] |
| Agentic planning, tool use, memory, self-improvement | [[../topics/function-calling-and-tool-use|Function Calling and Tool Use]], [[../topics/agent-memory|Agent Memory]], [[../topics/self-evolving-ai-systems|Self-Evolving AI Systems]] |
| AI4Science hypothesis generation and automated experimentation | [[../topics/ai4science|AI4Science]], [[../topics/workflow-runtime|Workflow Runtime]] |
| RAG, KG-RAG failure modes, retrieval, data management | [[../topics/large-language-models|Large Language Models]], [[../topics/data-management|Data Management]], [[../topics/ontology|Ontology]] |
| Transformer, Q-Former, ViT, SSM/Mamba, multimodal alignment | [[../topics/multimodal-ai|Multimodal AI]], [[../topics/large-language-models|Large Language Models]] |
| Quantum AI and NISQ concepts | [[../topics/quantum-computing|Quantum Computing]] |

## Import Decisions

- No new topic nodes were created during this import. Existing durable topics already cover the major clusters.
- OCR uncertainty is preserved in the local source vault; curated entries should be treated as navigation and synthesis, not as corrected textbook content.
- Notebook 1 raw scans have been copied into the local source vault and are referenced by `source_id`.

## Follow-up Candidates

- Promote a focused `Python Internals` topic if future work reuses the PyObject, frame, import, MRO, generator, and GIL notes.
- Create a CV/OCR topic map only if the YOLO, FPN, OCR, SRN, CTC, and lane-detection notes become active again.
- Extract a small RAG failure note if KG-RAG reasoning failures become part of the current agent-memory or retrieval architecture work.
