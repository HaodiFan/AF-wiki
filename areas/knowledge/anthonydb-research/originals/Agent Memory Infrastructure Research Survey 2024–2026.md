# Agent Memory Infrastructure Research Survey 2024–2026

## Meta
- type: `deepresearch`
- domain: `research`
- spark: `on`
- created: 2026-04-06
- source: KG/raw/legacy-notes/Agent Memory Infrastructure Research Survey 2024–2026.md

## Content
## Introduction

LLM agents have moved from “single-shot” question answering toward long-running, tool-using, environment-interacting systems. In that shift, **memory stops being an optional add-on** and becomes foundational infrastructure: it mediates _state_, _continuity_, _experience reuse_, _personalization_, and _lifelong improvement_ under tight latency and context budgets. Recent benchmarks explicitly evaluate these long-term capabilities—e.g., **LoCoMo** collects very long, multi-session conversations (reported up to ~300 turns and ~9k tokens on average across many sessions) to test long-horizon conversational memory, temporal reasoning, and summarization. 

Even with longer context windows, long-context behavior is unreliable: “lost-in-the-middle” effects show models often use information better near the beginning or end of long inputs, with degraded performance when relevant facts sit in the middle.  This partly explains why memory infrastructures increasingly emphasize **selective retrieval, compression, structure, and control loops** rather than “just feed the whole history.”

At the same time, memory introduces new failure modes: hallucinated or stale memories, incorrect consolidation, privacy leakage, and adversarial poisoning/injection. Dedicated benchmarks now measure these risks explicitly (e.g., HaluMem studies hallucinations across extraction/updating/QA stages). 

![What Is a Vector Database? An Illustrative Guide](https://images.openai.com/static-rsc-1/c2GuD5Dfwqf7ck6ceEaBcKgxO-qb-PpGob2mkZ_3CLfqF95EA--qGmXvLbVLdAtiv-UIOP4LraL-tpvdkcIPn9e1kIRc2Jn29bhHqoX9UwuH0q4MI64fQE27U1ECDYRrAEJ9viq_ZQzEeI66ET8BZw)![Knowledge Graph Definition 101: How Nodes and Edges Connect Data](https://images.openai.com/static-rsc-1/vJDgvWTueAWz_KkcRhjST32Sr4-89e72jWCUr0H0EG1-MP46Xd0actji-OfaMGXuUjr6-fAG4Npi55lNGxRGR8CQbyMZ-PIDKn96mC6_vx4GNcaKEmZ0t-Wm7MoYw_gm8mw6hAXEUJsRPPE3kCbetA)![2 Atkinson and Shiffrin memory model. (From Atkinson, R. C. and... |  Download Scientific Diagram](https://images.openai.com/static-rsc-1/xLANf8hrdGSfhPVgBzwsCG01g3w5rZmlWTunj4kwhHmpe7fACDdbmNptX6x8N_orfQmGNi4-nh5nFwuxk5bBuzqkEYNz-Ncmp3smqFZGnwTmViPVK6yJVlbtQkyQB_GWLWV2SO8vY7Jn8z7PjU72jA)![Atkinson-Shiffrin 3-stage model of human memory. | Download Scientific  Diagram](https://images.openai.com/static-rsc-1/qxVwhynTzy4vfMf0LNVAL8VvZU4ZWFZsp-rFWSptKr0qfdLdNaWmeNfVc7gkNUawoV6qau1qNVBhP0xEuV0tkI8RYXMuMyJcl_7fK7VooHYsTIZPE3ktuAmbofiLV7e92722K76lUctrznOZYtvYwQ)

## Research landscape

A useful way to map 2024–early 2026 research is to treat “agent memory” as a **design space** across (a) representation and (b) control.

### Representation families

First, memory representations are diversifying beyond plain vector retrieval.

**Retrieval memory (embedding-first)** remains common: store chunks of interactions (“memories”) and retrieve top‑k by similarity. This is the baseline that many systems extend or critique. Benchmarks like LongMemEval explicitly measure multi-session reasoning, temporal reasoning, and knowledge updates—capabilities that frequently break under naive similarity retrieval and chronological noise. 

**Structured memory** uses explicit schemas—entities, relations, timestamps, causal links, profiles, preferences, tasks, tools—often with graph storage and query. For example, Zep frames agent memory as a **temporal knowledge graph architecture** and reports evaluation on memory benchmarks, pitching improvements in latency and temporal reasoning over earlier baselines. 

**Graph-based “connectivity” memory** is a broader thread: when evidence is distributed across time, _connectivity_ becomes as important as _retrievability_. AriadneMem (2026) argues that long-term memory fails on (i) **disconnected evidence** (multi-hop requires bridging facts across time) and (ii) **state updates** (new facts contradict or supersede old facts). It proposes a two-phase design: offline construction with filtering/extraction/coarsening and online structural reasoning via graph bridge discovery and topology-aware synthesis. 

**Reflective memory** treats memory not just as storage but as a substrate for self-critique, summarization, belief update, and experience abstraction. Systems like MemR³ operationalize this into a retrieval controller that can choose between retrieve/reflect/answer while tracking evidence gaps. 

**Hierarchical memory** separates short-term working state from longer-term stores (episodic logs, summaries, skills, profiles). MemGPT is a canonical OS-inspired example: it explicitly manages **memory tiers** and “paging” to extend effective context, influencing many later “memory OS / memory layer” proposals. 

**World-model-oriented memory** appears when agents must act in environments (web, embodied, enterprise tools). Here, memory stores not only “what was said” but “how the world transitions.” AMA-Bench (2026) argues that many memory benchmarks are dialogue-centric, while real agent memory is a stream of **agent–environment interactions** with machine-generated representations; it introduces trajectories + QA to test long-horizon memory in agentic applications and proposes a causality-graph + tool-augmented retrieval baseline (AMA-Agent). 

### Control families

In parallel, the field is shifting from “retrieve-then-answer” to **closed-loop memory control**:

- **Retrieval control**: deciding whether to retrieve, what to retrieve, and when to stop (MemR³). 
- **Memory construction control**: deciding at what granularity to store, how to denoise and segment, and how to consolidate (SeCom; SimpleMem; THEANINE). 
- **Utility control**: learning which memories/skills are useful via feedback (MemRL). 
- **Meta-control**: evolving the memory architecture itself (MemEvolve). 

Finally, multiple surveys attempt to systematize the growing space of “memory mechanisms in LLM agents,” reflecting that the literature has become large and fragmented. 

## Architecture patterns that dominate 2024–2026 work

This section distills recurring architecture patterns into a practical “reference catalog,” emphasizing design trade-offs relevant to building memory as infrastructure (not just a research demo).

### Context-window memory

**Pattern:** keep short-term state directly in the prompt (recent turns; scratchpad; running summary).  
**Why it persists:** lowest engineering overhead; no external state.  
**Why it fails:** cost scales with history, and long-context reliability is brittle (“lost-in-the-middle”). 

**Infrastructure implications:** treat this as a _cache tier_, not a durable memory. Persist only what is needed for immediate planning; offload durable state elsewhere.

### External retrieval memory

**Pattern:** store memory items externally (often as text + embedding + metadata), retrieve top‑k per query, stuff into prompt.  
**Representative baselines:** many LongMemEval / LoCoMo systems; MemoryBank’s “memory retrieval + updating” paradigm is an influential early instance for personalization. 

**Key failure modes highlighted by modern benchmarks:**

- multi-session reasoning and temporal reasoning require more than “nearest neighbor similarity” 
- hallucinations and error accumulation can occur during extraction/updating steps 
- retrieval noise grows with memory scale, motivating compression/segmentation/control loops 

**Infrastructure implications:** you need explicit memory operations (ADD/UPDATE/DELETE), provenance, time, and validation—not just “append + retrieve.”

### Reflection memory

**Pattern:** add an explicit reflection loop that turns episodic interactions into distilled summaries, insights, or “lessons,” which then influence future behavior.  
**Representative systems / mechanisms:**

- MemR³ makes retrieval itself agentic: retrieve/reflect/answer with an evidence-gap tracker. 
- Reflective Memory Management (RMM) proposes both prospective and retrospective reflections across granularities for long-term dialogue memory. 
- Hindsight (2025) argues current systems blur evidence vs inference and proposes structured networks plus retain/recall/reflect operations. 

**Infrastructure implications:** reflection should be treated as a **managed background job** with compute budgets, auditing, and rollback, because reflective updates can corrupt memory if they hallucinate.

### Graph memory

**Pattern:** represent memory as a graph (entities, events, relations, time edges, causal edges). Retrieval becomes hybrid: embedding search + graph traversal and multi-hop assembly.

Important threads:

- **Graph-first retrieval for sensemaking**: GraphRAG builds an entity graph + community summaries to answer global questions over large corpora; while not “agent memory” per se, it strongly influences agent memory designs where _global understanding_ and _structure_ matter. 
- **Temporal KG for agent memory**: Zep positions a temporally-aware KG engine (“Graphiti”) as a memory service to support dynamic knowledge integration and temporal reasoning. 
- **Graph to resolve disconnected evidence**: AriadneMem explicitly targets multi-hop bridging and state updates via offline coarsening + online bridge discovery. 
- **Zettelkasten-style agentic memory graphs**: A‑Mem creates atomic notes with tags/keywords/attributes and dynamically links and evolves them. 

**Infrastructure implications:** graphs improve multi-hop and temporal coherence but demand:

- schema design (what is a node? event? entity? belief?)
- versioning and conflict resolution for updates
- efficient hybrid retrieval pipelines

### World-model memory

**Pattern:** memory is a substrate for predicting/controlling environment dynamics—not just remembering dialogue.  
Examples:

- AMA-Bench shows dialogue-only benchmarks fail to reflect agentic trajectories; their findings point to missing causality/objective state information and propose causality graphs + tool-augmented retrieval. 
- World-model augmented web agents integrate a world model into action generation and closed-loop correction (not strictly “memory,” but tightly coupled with persistent state and transition modeling). 
- Voyager’s “skill library” functions as procedural memory for embodied lifelong learning, showing how memory can store reusable behaviors. 

**Infrastructure implications:** you need memory types tailored to action: state snapshots, tool traces, causal graphs, and reusable procedures. Treat “memory” as part of the policy loop.

## Memory lifecycle and learning mechanisms

A converging theme is that **memory must have an explicit lifecycle**—and that lifecycle must be engineered like a production data system.

### A canonical lifecycle pipeline

A practical synthesis from recent systems is:

1. **Observation capture** (dialogue, tool calls, environment state, outcomes)
2. **Filtering / gating** (noise removal, entropy/novelty gating)
3. **Encoding** (atomic entries, structured extraction, event segmentation)
4. **Storage** (tiered stores: raw logs, episodic atoms, semantic summaries, skills)
5. **Indexing** (semantic, temporal, entity/task/provenance indexes)
6. **Retrieval & assembly** (hybrid retrieval + budgeted context construction)
7. **Reflection / consolidation** (summaries, belief updates, skill distillation)
8. **Forgetting / pruning / versioning** (decay, conflict resolution, deletions)

Recent papers make parts of this pipeline explicit:

- **SimpleMem** formalizes a three-stage pipeline (semantic structured compression; recursive consolidation; adaptive query-aware retrieval), aiming at high information density and reduced inference-time tokens. 
- **SeCom** studies memory granularity (turn/session/summarization) and proposes segment-level memory with compression-based denoising (using prompt compression tools as denoisers) to improve retrieval accuracy and semantic quality. 
- **THEANINE** argues that “outdated memories” can still be useful for modeling user changes; it uses temporal + cause-effect linking into “timelines” and introduces a counterfactual evaluation scheme (TeaFarm) to evaluate memory use in response generation. 
- **Mem0** frames memory as a scalable architecture that dynamically extracts, consolidates, and retrieves salient info from ongoing conversations. 
- **MemOS** elevates memory to a first-class operational resource, proposing lifecycle management (generation/organization/utilization/evolution) plus unified interfaces and governance. 

### Learning mechanisms: from experience to reusable knowledge

A major 2025–2026 trend is shifting memory from “record” to “learning substrate,” especially for procedural knowledge.

**Reflection learning and experience abstraction.** ExpeL (AAAI 2024) frames agents as experiential learners: gather experiences through trial and error, extract natural language insights, and reuse successful experiences as in-context examples at test time. 

**Retrieval control as an agentic policy.** MemR³ interprets memory usage as a closed-loop decision process (retrieve/reflect/answer), maintaining explicit evidence and gap state. 

**RL over memory utility.** MemRL (2026) proposes runtime reinforcement learning over episodic memory: after semantic prefiltering, it selects memories based on learned Q-values (utility), updated via environment feedback—explicitly addressing the stability–plasticity dilemma by keeping the backbone model frozen while memory evolves. 

**Procedural memory distillation.** ReMe (2025) targets procedural “how-to” memory, criticizing passive accumulation. It proposes multi-faceted distillation (success patterns + failure triggers), context-adaptive reuse, and utility-based refinement (add/prune) and reports strong results on agentic benchmarks. 

**Meta-evolution of memory systems.** MemEvolve (2025) argues that hand-designed memory architectures are static bottlenecks. It proposes a meta-evolution framework that evolves both (i) memory content and (ii) the memory architecture itself, and introduces a unified codebase (EvolveLab) to standardize the design space. 

## Reference architecture for Agent Memory Infrastructure

This section converts the research landscape into a **production-oriented reference architecture**—i.e., what to build if “memory is infrastructure.”

### Design goals derived from benchmarks and systems

Benchmarks imply explicit target capabilities:

- **Information extraction** from long history (store only what matters, accurately). 
- **Multi-session reasoning** and **multi-hop connectivity** (link evidence across time). 
- **Temporal reasoning** and **knowledge updates** (represent change; don’t overwrite blindly). 
- **Selective forgetting** (remove or downweight stale/incorrect memories). 
- **Robustness to hallucination and poisoning** (validate memory ops; isolate attack surfaces). 

### A layered architecture

Below is a concrete, infrastructure-style decomposition:

**1) Capture layer (event sourcing)**  
Store a complete, append-only record of:

- user messages
- agent thoughts (optional; often excluded for safety/compliance)
- tool calls (inputs/outputs)
- environment observations
- outcomes / reward signals (if available)

This layer enables replays, audits, and offline construction. Systems like AriadneMem and SimpleMem explicitly separate offline construction from online reasoning and benefit from asynchronous pipelines. 

**2) Memory construction layer (write path)**  
A controlled pipeline that transforms raw events into memory objects. Modern work suggests **memory granularity and denoising** are first-order concerns:

- Segmenting long sessions into coherent units (SeCom) 
- Filtering low-information content (entropy-aware gating in SimpleMem/AriadneMem-style pipelines) 
- Extracting structured facts and events (Bi-Mem’s fact-level extraction; graph clustering) 
- Generating _typed_ memory objects: facts, preferences, tasks, skills, beliefs (Hindsight’s “networks” concept is one example) 

**Key infrastructure API:** `ADD`, `UPDATE`, `DELETE`, `MERGE`, `LINK`, `VERSION`.  
This emphasis aligns with “memory OS” framings such as MemGPT and MemOS. 

**3) Storage layer (multi-store)**  
In practice, a single database rarely suffices. A “best current” synthesis is a **multi-store**:

- **Raw log store** (cheap, immutable; for replay and forensic debugging)
- **Vector store** (semantic retrieval)
- **Graph store** (entities, temporal edges, causality; multi-hop)
- **Profile store** (user/agent profile, stable preferences)
- **Skill / procedure store** (code snippets, tool recipes; aligns with Voyager-style skill libraries and procedural memory approaches) 

Temporal KGs (Zep) and memory graphs (A‑Mem, AriadneMem) strongly suggest that **time should be first-class**, not just metadata. 

**4) Indexing layer (read optimization)**  
Indexes should be multi-dimensional:

- semantic (embeddings)
- temporal (event time, ingestion time, validity windows)
- entity (canonical IDs, aliasing)
- task/tool (what tool was used; what API schema)
- provenance (where did this come from? user said vs agent inferred)

SeCom’s results suggest that better segmentation + denoising improves not only retrieval quality but the semantic integrity of retrieved context. 

**5) Retrieval & context construction layer (online read path)**  
Instead of “top‑k retrieval,” newer systems add:

- **query classification** (is the query about preferences? schedule? multi-hop?)
- **budgeted evidence assembly** (token-aware selection)
- **hybrid retrieval**: vector + graph traversal + timeline slicing
- **abstention / uncertainty** when evidence is missing or contradictory (LongMemEval explicitly evaluates abstention). 

Graph-based retrieval is particularly helpful when questions require global sensemaking or multi-hop assembly (GraphRAG; AriadneMem). 

**6) Memory controller (closed-loop policy)**  
This is the component that makes memory “agentic.” It decides:

- retrieve vs reflect vs answer (MemR³) 
- how deep to retrieve / whether to expand search
- when to run background consolidation
- when to rewrite or prune memory
- how to incorporate feedback signals (MemRL) 

This controller can be rule-based at first, but the literature increasingly treats it as a learnable policy.

**7) Governance, safety, and compliance layer**

Memory-as-infrastructure must include controls that classic RAG demos omit:

- **privacy leakage resistance**: attacks that extract memory (“MEXTRA”) demonstrate that storing private interactions creates a distinct privacy surface. 
- **poisoning/injection resistance**: ER‑MIA shows black-box adversarial memory injection can target similarity retrieval to degrade downstream reasoning. 
- **operation-level validation**: HaluMem finds hallucinations can accumulate during extraction/updating and propagate into QA; this implies you need validators, not just end-task evaluation. 

Where policy allows, adopt “defense in depth”: provenance labels (“user-stated” vs “agent-inferred”), memory sandboxing per tool domain, anomaly detection on writes, and audit logs.

### A compact “reference diagram” for implementers

A textual architecture sketch (read path + write path):

**Write path (async):**  
Capture → Filter/Gate → Extract/Segment → Type & Validate → Store (multi-store) → Index → Consolidate/Link → Version/Prune

**Read path (online):**  
Query → Classify → Retrieve (hybrid) → Assemble (budgeted) → Validate conflicts/time → Controller loop (retrieve/reflect?) → Answer (+ optional memory update)

This directly mirrors the “offline construction vs online reasoning” split seen in AriadneMem and the multi-stage compression/consolidation emphasis in SimpleMem. 

## Multi-agent memory and memory governance

Agent systems are increasingly multi-agent (collaboration, delegation, committees). Memory then becomes **shared infrastructure** with access control, synchronization, and conflict resolution.

**Memory sharing as performance scaling.** The “Memory Sharing” framework (2024) proposes sharing memories among multiple agents to improve in-context learning diversity and train/improve retrievers from the growing pool. 

**Coordination and collective intelligence.** A 2025 survey on memory in LLM-based multi-agent systems argues that memory functions as shared cognitive infrastructure for coordination and team evolvement, and that taxonomies for MAS memory are underdeveloped. 

**Governance becomes mandatory**, especially when multiple agents can write into shared stores:

- access and write permissions per agent role
- conflict resolution (whose memory wins?)
- “source-of-truth” separation (facts vs beliefs vs hypotheses) to avoid shared hallucination cascades
- privacy boundaries: shared memory can amplify leakage risk if one agent is compromised 

Practically, production multi-agent memory may benefit from a **two-plane design**:

- **private memory plane** (per-agent identity, personal user data, sensitive tools)
- **shared work memory plane** (task artifacts, public facts, team procedures)

This separation is consistent with research emphasis on provenance, role separation, and operational governance in memory OS style proposals (MemOS) and structured memory architectures (Hindsight; Zep). 

## Evaluation benchmarks and how to interpret them

Between 2024 and early 2026, evaluation matured from “does it answer” to **what memory competency does it test** and **where do failures come from**.

### Dialogue-centric long-term memory

- **LoCoMo (ACL 2024)**: multi-session, very long conversations with QA and summarization tasks; results show long-context and RAG approaches can help but still lag humans substantially, especially on temporal reasoning. 
- **LongMemEval**: evaluates five core long-term memory abilities including information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. 
- **REALTALK (2025)**: a 21-day real-world dataset for long-term conversation, addressing concerns that many benchmarks are synthetic. 

### Agent-centric and environment-centric memory

- **MEMTRACK (2025)**: benchmarks long-term memory and state tracking in multi-platform dynamic enterprise environments, highlighting that “memory tools” can increase redundancy if misused and that LLMs struggle with cross-platform context reasoning. 
- **AMA-Bench (2026)**: evaluates long-horizon memory for real agentic trajectories and synthetic scalable horizons; argues existing systems underperform due to missing causality/objective state information and limitations of similarity retrieval; proposes AMA-Agent with causality graph + tool-augmented retrieval. 

### Competency-oriented and failure-mode benchmarks

- **MemoryAgentBench (ICLR 2026 accept; arXiv 2025)**: evaluates memory agents across four competencies: accurate retrieval, test-time learning, long-range understanding, and selective forgetting. 
- **MemoryBench (2025)**: focuses on memory + continual learning via simulated user feedback streams, emphasizing learning from service-time feedback rather than static RC-only evaluation. 
- **HaluMem (2025)**: operation-level hallucination benchmark—explicitly attributes hallucinations to extraction, updating, and QA stages and shows error propagation. 

**Interpretation guidance for builders:**  
Strong results on dialogue benchmarks do not guarantee robustness on agentic environments (MEMTRACK, AMA-Bench). Conversely, systems optimized for agent trajectories may not be best for personalization dialogues. This suggests memory infrastructure should support **pluggable policies** and **typed stores** rather than a single monolithic “memory bank.” 

## Trends, open problems, and an annotated key paper list

### Emerging trends (2024–early 2026)

**Graphification of memory** is accelerating: from GraphRAG-style corpus indexing to agent memory graphs that resolve multi-hop connectivity and time-sensitive updates (A‑Mem, Zep, AriadneMem, AMA-Agent). 

**Offline/online separation** is becoming a core systems pattern: expensive extraction/consolidation runs asynchronously, while online answering uses compact structures and algorithmic reasoning to reduce latency (SimpleMem; AriadneMem). 

**Memory controllers and learnable policies** are replacing fixed heuristics (MemR³; MemRL). 

**Memory OS framing** crystallizes memory as an operational resource with lifecycle and governance (MemGPT → MemOS). 

**Evaluation is aligning with real deployment risks**: privacy extraction (MEXTRA), memory injection/poisoning (ER‑MIA), and operation-level hallucinations (HaluMem). 

### Open research problems (systems + research)

**Trustworthy memory writes.** Many systems still rely on LLM-based extraction/summarization to write memory, which can hallucinate and then persist errors. Operation-level benchmarks show these hallucinations can accumulate during extraction and updating and propagate downstream. 

**Temporal semantics and state updates.** Benchmarks explicitly test knowledge updates and temporal reasoning, and recent systems treat “change over time” as a first-class representation challenge (LongMemEval; THEANINE; Zep; AriadneMem). 

**Disconnected evidence at scale.** Multi-hop reasoning over long histories stresses flat retrieval. AriadneMem’s framing (structure vs connectivity trade-off) suggests infrastructure must encode links—not rely on the LLM to “reconstruct” bridges every time. 

**Benchmark realism vs controllability.** Dialogue benchmarks are controllable but may not reflect agent–environment memory streams; agentic benchmarks capture realism but are harder to standardize (AMA-Bench; MEMTRACK). 

**Security and privacy governance.** Memory creates persistent attack surfaces. Black-box extraction and injection results imply that “memory governance” is not paperwork—it is a technical requirement (access control, write validation, provenance, anomaly detection). 

### Annotated key paper list (infrastructure-relevant, 2024–early 2026 plus essential precursors)

The table below emphasizes papers that shape **infrastructure decisions**: memory lifecycle, structure, control, benchmarks, and security.

|Paper / System|Authors|Year|Core contribution for Agent Memory Infrastructure|
|---|---|---|---|
|A Survey on the Memory Mechanism of LLM-Based Agents|Zhang et al.|2024|Systematizes memory design/evaluation patterns for LLM agents; useful as a taxonomy baseline.|
|Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo)|Maharana et al.|2024|Introduces LoCoMo benchmark and shows long-context/RAG improvements still lag human performance, especially temporal reasoning.|
|LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory|Wu et al.|2024/2025|Defines five memory abilities (extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention) and standardizes evaluation.|
|HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs|Gutiérrez et al.|2024|Connects KG + Personalized PageRank + LLM extraction to improve integration and multi-hop retrieval; influential for “hippocampus-like” indexing designs.|
|Towards Lifelong Dialogue Agents via Timeline-based Memory Management (THEANINE)|Ong et al.|2024/2025|Uses temporal + cause-effect linking to build memory “timelines,” arguing outdated memories can be useful for modeling change.|
|Memory Sharing for LLM-based Agents|Gao & Zhang|2024|Proposes multi-agent memory sharing to improve ICL diversity and retriever learning; motivates shared memory pools and governance.|
|ExpeL: LLM Agents Are Experiential Learners|Zhao et al.|2024|Experience collection + insight extraction + reuse as in-context examples; a concrete pipeline for “learning from interaction” without fine-tuning.|
|ReadAgent: A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts|Lee et al.|2024|“Gist memory” as a compression/reading strategy; relevant to memory summarization and long-input ingestion.|
|Lost in the Middle: How Language Models Use Long Contexts|Liu et al.|2024|Demonstrates positional degradation in long contexts; motivates retrieval, structure, and budgeted context building.|
|SeCom: On Memory Construction and Retrieval for Personalized Conversational Agents|Pan et al.|2025|Shows memory unit granularity matters; proposes segment-level memory + compression-based denoising to improve retrieval accuracy.|
|Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory|Chhikara et al.|2025|A scalable memory-centric architecture emphasizing extraction, consolidation, retrieval; popularizes “memory layer” framing for production.|
|MemOS: An Operating System for Memory-Augmented Generation in LLMs|Li et al.|2025|Treats memory as first-class resource with lifecycle and governance; aligns with infra needs (APIs, versioning, access control).|
|A-Mem: Agentic Memory for LLM Agents|Xu et al.|2025|Zettelkasten-inspired dynamic linking and evolving memory graphs; pushes “self-organizing memory” pattern.|
|Zep: A Temporal Knowledge Graph Architecture for Agent Memory|Rasmussen et al.|2025|Temporal KG as memory service, stressing dynamic knowledge integration and enterprise temporal reasoning.|
|Reflective Memory Management for Long-term Dialogue Agents|Tan et al.|2025|Integrates forward/backward reflection and multi-granularity summaries; supports an explicit lifecycle view of memory maintenance.|
|MemR³: Memory Retrieval via Reflective Reasoning for LLM Agents|Du et al.|2025|Closed-loop retrieval controller (retrieve/reflect/answer) with evidence-gap tracking; a reusable “retrieval policy wrapper.”|
|MemoryBench: A Benchmark for Memory and Continual Learning in LLM Systems|Ai et al.|2025|Evaluates continual learning from simulated user feedback, beyond RC-style long context tasks.|
|REALTALK: A 21-Day Real-World Dataset for Long-Term Conversation|Lee et al.|2025|Real-world long-term dialogue dataset to test memory/personalization under authentic conditions.|
|MEMTRACK: Evaluating Long-Term Memory and State Tracking in Multi-Platform Agent Environments|Deshpande et al.|2025|Enterprise-style multi-platform benchmark; exposes tool-use redundancy and memory misuse patterns.|
|Evaluating Hallucinations in Memory Systems of Agents (HaluMem)|Chen et al.|2025|Operation-level hallucination benchmark across extraction/updating/QA; highlights error accumulation and propagation.|
|Unveiling Privacy Risks in LLM Agent Memory (MEXTRA)|Wang et al.|2025|Demonstrates black-box memory extraction risks; security/privacy requirements for persistent memory systems.|
|MemoryAgentBench: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions|Hu et al.|2025/2026|Competency-based benchmark: accurate retrieval, test-time learning, long-range understanding, selective forgetting.|
|AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications|Zhao et al.|2026|Agentic-trajectory benchmark; argues memory needs causality/objective state and tool-augmented retrieval; proposes AMA-Agent.|
|SimpleMem: Efficient Lifelong Memory for LLM Agents|Liu et al.|2026|Semantic “lossless” compression + recursive consolidation + query-aware retrieval for efficiency-performance trade-offs.|
|AriadneMem: Threading the Maze of Lifelong Memory for LLM Agents|Zhu et al.|2026|Two-phase pipeline, conflict-aware graph coarsening + algorithmic bridge discovery to resolve disconnected evidence/state updates efficiently.|
|LightMem: Lightweight and Efficient Memory-Augmented Generation|Fang et al.|2025/2026|Human-memory-inspired multi-stage pipeline with lightweight filtering/organization/consolidation for efficiency.|
|MemRL: Self-Evolving Agents via Runtime RL on Episodic Memory|Zhang et al.|2026|Utility-guided memory selection updated via RL feedback; addresses stability–plasticity without weight updates.|
|MemEvolve: Meta-Evolution of Agent Memory Systems|Zhang et al.|2025|Evolves both memory content and architecture; introduces modular design space and evaluation substrate (EvolveLab).|
|ReMe: Remember Me, Refine Me (Procedural Memory)|Cao et al.|2025|Distills success/failure into procedural memory; context-adaptive reuse + utility-based refinement; demonstrates memory can substitute for model scale.|
|Bi-Mem: Bidirectional Construction of Hierarchical Memory|Mao et al.|2026|Inductive + reflective agents to construct and calibrate hierarchical memory; addresses hierarchical memory hallucination/misalignment.|
|ER‑MIA: Black-Box Adversarial Memory Injection Attacks|(authors as listed)|2026|Systematic study of similarity-based retrieval attacks on long-term memory systems; emphasizes security-by-design for memory stores.|

### Practical synthesis: what “next-gen Agent Memory Infrastructure” is converging toward

Across these works, a coherent “north star” emerges:

- Memory is trending toward a **typed, versioned, temporally-aware substrate** (not a flat store). 
- Systems separate **offline construction/consolidation** from **online retrieval/reasoning** to manage cost and latency. 
- The “memory brain” adds **controllers** (retrieve/reflect/answer routing; utility-guided selection) and even **learning policies** (RL, meta-evolution). 
- Evaluation is becoming **competency- and failure-mode-oriented**, and security/privacy are now first-class concerns that directly shape architecture.

## Keypoints
<!-- LLM 提取，每条是一个可连接的知识点 -->
<!-- 如果该 keypoint 在其他 node 也出现过，标注 (also in: node名) -->
- [[KP - Memory|Memory]]
- [[KP - Control families|Control families]]
- [[KP - Research landscape|Research landscape]]
## Links
### hints

### dive-ins
