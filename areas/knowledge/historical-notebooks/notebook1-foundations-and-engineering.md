---
title: "Notebook 1 - Foundations, CV, Systems, and Engineering"
type: retained-note
area: knowledge
collection: historical-notebooks
status: retained
aliases:
  - Notebook 1 Foundations
  - 历史学习笔记 1 摘要
tags:
  - area/knowledge
  - collection/historical-notebooks
  - type/retained-note
  - wiki/af
---
# Notebook 1 - Foundations, CV, Systems, and Engineering

## Source

- Full OCR source ID: `historical:notebook1-ocr`
- Raw scan source IDs: see [[../source-manifests/historical-notebooks|Historical Notebook Source Manifest]]
- Source vault path: `fulltext/historical-notebooks/notebook1-ocr.md`

## One-line Read

Notebook 1 is a broad foundation notebook: it links early RAG and multimodal model study with CV/OCR, Python runtime internals, distributed systems, blockchain, databases, design patterns, and classic algorithms.

## Retained Knowledge Clusters

### RAG, Knowledge Graphs, and Data Systems

- KG-based RAG failure modes are framed around question-context misinterpretation, relation-mapping errors, ambiguity, specificity errors, and missed constraints.
- RAG methodology notes include REALM, RAFT, BM25, DPR + LLM, beam search, and greedy decoding.
- Big-data stack notes cover HDFS, MapReduce, Hive, Spark/Flink, Oozie/Azkaban, Yarn, Sqoop, Flume, DataX, and Kafka.
- 12306 architecture notes retain the load-balancing and resilience lens: LVS, Nginx, service layer split, OSPF, disaster recovery, node tolerance, and circuit breaking.

Current routing: [[../topics/large-language-models|Large Language Models]], [[../topics/data-management|Data Management]], [[../topics/ontology|Ontology]].

### Multimodal and Foundation Model Basics

- Q-Former pretraining is recorded through ITC, ITG, and ITM, with attention-mask differences across contrastive, generative, and matching tasks.
- Transformer notes include residual + LayerNorm sublayers, MHSA, FFN, sinusoidal position encoding, ViT patching, and basic attention variants.
- Related concepts include knowledge neurons, cognitive architectures, Simpson's paradox, Hodgkin-Huxley dynamics, STDP, universal approximation, SSM/Mamba, and RAG security.

Current routing: [[../topics/multimodal-ai|Multimodal AI]], [[../topics/large-language-models|Large Language Models]], [[../topics/agent-core|Agent Core]].

### Computer Vision, OCR, and Perception

- CV lineage notes include Diffusion, YOLO v1-v5, Faster R-CNN, SSD, FPN/PAN/NAS-FPN, SPP, backbone design, SORT/Deep SORT, Kalman filter, lane detection, SCNN, and data augmentation.
- OCR-specific notes include PP-OCR, CRNN, SRN, PVAM, GSRM, CTC, visual-semantic fusion, and binarization.
- Supporting math and ML notes include KL divergence, metric learning, SIFT, GMM, PCA/SVD, clustering, BIRCH, and distance metrics.

Current routing: no dedicated CV/OCR topic yet. Keep as historical source unless the perception track becomes active again.

### Python Runtime and Engineering Internals

- Python internals notes include allocator layers, compile pipeline, PyObject, PyFrameObject, PyMethod, class construction, MRO, import mechanics, generator/async generator state, GC, GIL, and Timsort.
- Engineering notes include Selenium WebDriver internals, Celery, Redis vs Memcached, TLS JA3/JA3S fingerprints, Flask, HTTP clients, UML, design patterns, bad smells, and refactoring.

Current routing: potential future `Python Internals` topic; for now keep under this retained note.

### Distributed Systems, Blockchain, and Databases

- Distributed and network notes include TCP/IP, OSI, Zookeeper, RASA, industrial IoT, industrial control systems, database basics, and scheduling/coordination patterns.
- Blockchain notes include Bitcoin, digital currency, Merkle trees, public chain vs consortium chain, PBFT vs RAFT, smart contracts, NFT/content ecosystems, and smart-contract runtime.

Current routing: [[../topics/data-management|Data Management]] for data-side material; blockchain remains historical unless it becomes active again.

## Why This Stays Retained

- It preserves Anthony's earlier breadth-first technical map rather than a single research conclusion.
- It gives later agents a traceable source for recurring concepts that may otherwise look disconnected: RAG, CV, Python internals, distributed systems, and algorithms.
- It is useful as historical context for how current agent-system interests emerged from lower-level ML and engineering foundations.

## Open Normalization Tasks

- Split Python runtime notes into a focused retained topic only when they become reusable in current engineering work.
- Extract CV/OCR content into a perception map only if perception work becomes active.
- Convert KG-RAG failure notes into a retrieval/ontology mini-note if needed for current agent-memory design.
