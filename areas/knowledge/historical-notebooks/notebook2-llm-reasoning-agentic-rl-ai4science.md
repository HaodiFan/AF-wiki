---
title: "Notebook 2 - LLM Reasoning, Agentic RL, OS Agents, and AI4Science"
type: retained-note
area: knowledge
collection: historical-notebooks
status: retained
aliases:
  - Notebook 2 LLM Agent Notes
  - 历史学习笔记 2 摘要
tags:
  - area/knowledge
  - collection/historical-notebooks
  - topic/agent-systems
  - topic/llm
  - type/retained-note
  - wiki/af
---
# Notebook 2 - LLM Reasoning, Agentic RL, OS Agents, and AI4Science

## Source

- Full OCR source ID: `historical:notebook2-ocr`
- Original PDF source ID: `historical:notebook2-pdf`
- Source vault paths: `fulltext/historical-notebooks/notebook2-ocr.md`, `raw/historical-notebooks/notebook2.pdf`

## One-line Read

Notebook 2 is the frontier follow-up to Notebook 1: it tracks the path from reasoning data and DeepSeek-style RL to OS agents, agentic RL, memory/tool-use capabilities, AI4Science workflows, and a small quantum/Python appendix.

## Retained Knowledge Clusters

### Reasoning Data and Inference-Time Control

- Reasoning task types are grouped as logical, mathematical, representation, and causal reasoning.
- The control dimensions are granularity, reward signal, search mode, and verifier/self-check.
- The notes explicitly compare training-time scaling and inference-time computation through the AlphaGo analogy.
- Human-like reasoning behaviors are treated as observable policy behaviors: analysis, decomposition, completion, alternative proposal, self-evaluation, and self-correction.

Current routing: [[../topics/large-language-models|Large Language Models]], [[../topics/llm-safety-interpretability|LLM Safety and Interpretability]].

### DeepSeek R1 and RL Training Pipeline

- R1-Zero pain points are recorded as endless rejection, poor readability, and language mixing under GRPO.
- The retained pipeline is cold-start SFT, reasoning-oriented RL, rejection sampling plus supervised data, retraining from base, and additional RL across reasoning and general tasks.
- GRPO is captured as group-relative reward without a critic, using group mean/std for advantage normalization.
- Reward notes separate accuracy reward and format reward, with an explicit warning that process reward models can be vulnerable to reward hacking.

Current routing: [[../topics/large-language-models|Large Language Models]], [[../topics/self-evolving-ai-systems|Self-Evolving AI Systems]].

### AI4Science Workflow

- The scientific loop is decomposed into literature search, research idea generation, unimodal/multimodal context generation, experimentation, and peer review.
- Hypothesis generation is tracked through long-context retrieval, refinement strategies, multi-agent debate, Chain of Ideas, and evaluation criteria such as novelty, relevance, significance, and verifiability.
- Automated experimentation examples include GVIM, Prof-Agent, AIDE, SELA, APEx, OpenHands, AI-ML-Agent, MLAgent-Bench, and Agent-As-a-Judge.
- The core limitation is precise: LLM-generated ideas may be novel but infeasible, underspecified, prompt-sensitive, and prone to rediscovering known work.

Current routing: [[../topics/ai4science|AI4Science]], [[../topics/workflow-runtime|Workflow Runtime]], [[../topics/function-calling-and-tool-use|Function Calling and Tool Use]].

### OS Agents and GUI Grounding

- OS Agent is framed as foundation model plus agent framework.
- GUI-capable MLLM adaptation is treated as a resolution and grounding problem, with notes on CogAgent, Aria-UI, Ferret-UI, Iris, and MakeFlow.
- Training stages are separated into continual pretraining, SFT, imitation learning, and RL.
- Key data tasks include grounding, screen understanding, OCR, screen descriptions, next-action reasoning, and outcome prediction.

Current routing: [[../maps/agent-systems-map|Agent Systems Map]], [[../topics/agent-core|Agent Core]], [[../topics/agent-runtime|Agent Runtime]], [[../topics/multimodal-ai|Multimodal AI]].

### Agentic RL Capabilities

- Agentic RL is distinguished from traditional RL because the action space is token sequences and the environment includes tools and APIs.
- Planning patterns are split into RL as an extended guide and RL as the integral driver.
- Tool-use routes include prompt engineering, SFT-based tool use, and tool-integrated RL.
- Memory is split into RAG-style memory, token-level memory, and structured memory; future direction is RL-trained structured memory.

Current routing: [[../topics/agent-memory|Agent Memory]], [[../topics/function-calling-and-tool-use|Function Calling and Tool Use]], [[../topics/self-evolving-ai-systems|Self-Evolving AI Systems]].

### Benchmarks, Secondary Notes, and Appendices

- Agent environments and benchmarks include WebShop, MiniWeb, WebArena, VisualWebArena, WAREX, WAIT, BrowserGym, and Windows Agent Arena.
- Karpathy talk notes preserve concepts around cognitive core, distillation, sparse attention, computer use, motivation, and continuous learning.
- Quantum notes cover NISQ, quantum advantage, hybrid quantum-classical algorithms, QNN/QAOA/quantum kernels, quantum error correction, and the quantum stack.
- Python appendix records `@dataclass(init=False)` and the Python typing timeline.

Current routing: [[../topics/quantum-computing|Quantum Computing]] and the historical collection.

## Why This Stays Retained

- It is directly aligned with the current AF-wiki agent-system map.
- It bridges model training, runtime design, tool use, memory, evaluation, and AI4Science in one source thread.
- It is a compact historical snapshot of the reasoning/RL/agent frontier and should be retrievable when designing agent harnesses or AI research workflows.

## Open Normalization Tasks

- Extract a focused GRPO/RLHF note if reasoning-training work becomes active.
- Promote OS-agent GUI grounding into a dedicated retained note if browser/desktop agent work becomes central.
- Convert AI4Science automated experimentation notes into a workflow-runtime research note if the topic moves from reading to implementation.
