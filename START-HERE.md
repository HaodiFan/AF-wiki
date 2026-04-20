# Start Here

> 这是一页给第一次进入 `AF-wiki` 的导览。
> 这次重构之后，仓库的第一层理解方式变成了：**先看 area，再看 area 内部 schema，再看 root schema。**

## 先用一句话理解它

`AF-wiki` 现在是一个按 **动态 area 模块** 组织的 LeadFlow second brain。

目前最重要的不是“resources 里放了什么”，而是：
- 当前有哪些 `areas/`
- 每个 area 的内部结构是什么
- 哪些内容属于 area 自己维护，哪些内容只属于共享 lead/research 流水线

## 第一次看，按这个顺序就够了

1. [[areas/index]]：先看当前有哪些 area，以及每个 area 的 skill routing
2. [[index]]：看当前的主入口都在哪里
3. 选择你真正关心的 area：
   - 健身：[[areas/fitness/index]]
   - 知识：[[areas/knowledge/index]]
   - 工作：[[areas/work/index]]
4. 最后再看 [[SCHEMA]]，理解整个 LeadFlow 的总规则

## 当前最值得先看的 area

### Fitness
- `areas/fitness/`
- 这是当前最完整、最成熟的 area
- 适合先看：
  - [[areas/fitness/00-profile]]
  - [[areas/fitness/02-current-plan]]
  - [[areas/fitness/10-checkins/2026-04]]

### Knowledge
- `areas/knowledge/`
- 这里承接的是持续性的技术阅读与 retained knowledge，而不是弱信号 inbox
- 适合先看：
  - [[areas/knowledge/index]]
  - [[areas/knowledge/wechat-public-account-articles]]

### Work
- `areas/work/`
- 这是刚补上的工作 area 骨架，目前内容还轻
- 适合先看：
  - [[areas/work/index]]
  - [[areas/work/00-active-context]]

## 共享流水线怎么理解

并不是所有东西都塞进 `areas/`。

下面这些仍然是共享层：
- `resources/leads/`：弱信号 capture
- `dashboards/research-backlog.md`：lead backlog
- `resources/research/`：深挖研究笔记 scaffold
- `resources/ideas/`：idea 存放 scaffold

理解方法：
- **ongoing ownership** -> `areas/<name>/`
- **cross-area intake / research flow** -> `resources/`

## 当前状态要分三层理解

### 1. Active
已经真实落地，里面有持续维护的内容：
- `areas/index.md`
- `areas/fitness/`
- `areas/knowledge/`
- `areas/work/`（轻量骨架）
- `inbox/`（轻量骨架）
- `projects/`（轻量骨架）
- `resources/index.md`
- `resources/leads/`
- `resources/research/`（轻量骨架）
- `resources/ideas/`（轻量骨架）
- `dashboards/research-backlog.md`
- `templates/`

### 2. Planned
这些是 LeadFlow 目标架构的一部分，但目前还没有真正建起来，或者只有概念没有内容：
- future areas under `areas/<name>/`

### 3. Legacy / bootstrap
这些存在，但不是今天应该优先阅读的主入口：
- `archive/legacy/fitness-legacy-2026-04-18/`：旧版 fitness 资料
- `wiki/`：更早期的结构化 wiki 骨架草案

## 为什么这次会比之前清楚

之前最容易混淆的一点是：
- 一部分 active 内容在 `areas/fitness/`
- 另一部分 active 内容却在 `resources/knowledge/`

现在这层已经收口成：
- `areas/` 负责持续性的领域模块
- `resources/` 负责共享 capture / research 流水线

所以现在更合理的读法是：

**先看 `areas/index`，再进目标 area；先看 area schema，再看 root schema。**
