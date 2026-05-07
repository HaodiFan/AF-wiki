---
type: lead
status: captured
priority: medium
source_type: article
captured_on: 2026-05-01
tags:
  - lead
  - paper
  - agent
  - harness
  - engineering
  - arxiv
  - lead-paper
---
# Agentic Harness Engineering (AHE) paper

## Basic Info
- Type: lead
- Title: Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses
- Captured on: 2026-05-01
- Status: captured
- Priority: medium
- Source type: article
- Source: https://arxiv.org/abs/2604.25850
- Seen via: 用户阅读 arXiv 论文时要求记录

## Why it caught my attention
- 这篇论文更像一篇 lead / agenda-setting paper，而不只是一个局部技巧实验。
- 它把问题上提到 coding-agent harness engineering，并提出一个可复用的自动演化闭环，值得后续跟进。
- 论文结论对 agent 系统设计有方向性：收益主要来自 tools、middleware、long-term memory，而不是 system prompt。

## Keywords
- agentic harness engineering
- AHE
- coding-agent harness
- observability
- terminal-bench
- swe-bench
- long-term memory
- tool and middleware design

## Research questions
- AHE 的三层 observability（component / experience / decision）各自如何落到具体 harness 组件与日志结构？
- 这套闭环对我们自己的 agent harness / wiki / memory 设计，有哪些可借鉴的最小可行迁移点？
- 论文里的提升，哪些来自 benchmark-specific adaptation，哪些是真正可迁移的 harness engineering 经验？

## Note on scope
- 这篇 paper lead 主要负责记录“为什么值得跟进”以及它触发了哪些后续研究方向。
- 由这篇论文引申出的更通用 key points 和每个 key point 后面的研究性展开，已经单独沉淀到：[[resources/research/2026-05-01-ahe-paper-to-agent-systems-takeaways]].

## Next action
- 后续如继续深读，可继续扩展对应 deep research note，并回链此 lead。
- 可结合现有 `harness engineering` lead，进一步整理成一个更系统的 topic / map。

## Links
- Related deep research: [[resources/research/2026-05-01-ahe-paper-to-agent-systems-takeaways]]
- Related project/area/resource: [[dashboards/research-backlog]]
- Related lead: [[resources/leads/2026-04-26-harness-engineering]]
- Related topic: [[areas/knowledge/topics/agent-runtime]]
- Related map: [[areas/knowledge/maps/agent-systems-map]]
- Promoted topic:

## Raw notes
- arXiv ID: 2604.25850v3
- Published: 2026-04-28
- Updated: 2026-04-30
- Authors: Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Xuanjing Huang, Hang Yan, Zhenhua Han, Tao Gui
- Abstract takeaway: 论文提出 AHE（Agentic Harness Engineering），通过 component / experience / decision observability 驱动 coding-agent harness 自动演化。
- Quick verdict: 先按 weak-signal lead 记录；当前判断是「是个 lead paper」。
