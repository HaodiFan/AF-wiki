---
title: LLM Safety and Interpretability / LLM 安全与可解释性
type: topic
area: knowledge
status: active
aliases:
  - LLM Safety
  - LLM Interpretability
  - AI Safety
  - LLM 安全
  - 可解释性
tags:
  - area/knowledge
  - topic/llm
  - topic/llm-safety
  - type/topic
  - wiki/af
---
# LLM Safety and Interpretability / LLM 安全与可解释性

## Definition

LLM safety and interpretability cover methods for understanding, evaluating, constraining, and defending AI model behavior under ordinary use, adversarial input, autonomous operation, and long-running agent contexts.

This topic is strongly connected to harness design because many safety controls live outside the model: input handling, tool permissions, evals, monitoring, policy checks, and rollback.

## Why it matters

- Agent systems amplify model risks through tools, memory, autonomy, and persistence.
- Interpretability and safety evaluation help decide what can be automated and what needs human review.
- Safety work provides constraints for [[self-evolving-ai-systems|Self-Evolving AI Systems]] and [[agent-harness-engineering|Agent Harness Engineering]].

## Source References

- `baidu-sync:2b1c1876d9c9` — Safety and Interpretability.pdf
- `baidu-sync:51381a099b59` — DECEPTION IN LLM S SELF-PRESERVATION AND AUTONOMOUS.pdf
- `baidu-sync:191230d630fb` — Defending_Against_Prompt_Injection_With_a_Few_DefensiveTokens_2507.07974v1.pdf
- `baidu-sync:c42065375a9d` — O3-MINI VS DEEPSEEK-R1 W HICH ONE IS SAFER.pdf
- `baidu-sync:ce38b2926bc6` — Traceable_Evidence_Enhanced_Visual_Grounded_Reasoning_Evaluation_and_Methodology_2507.07999v1.pdf

## Related topics

- [[agent-harness-engineering|Agent Harness Engineering]]
- [[self-evolving-ai-systems|Self-Evolving AI Systems]]
- [[large-language-models|Large Language Models]]
- [[agent-runtime|Agent Runtime]]

## Open questions

- Which safety controls should be model-level, and which should be runtime or harness-level?
- How should prompt-injection defense be tested across tool-using agents?
- What evidence traces are sufficient for high-stakes agent decisions?
