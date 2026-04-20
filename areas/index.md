# Areas Index

> Canonical registry of active areas in AF LeadFlow
> Last updated: 2026-04-20

## Purpose
这个页面是 `areas/` 的总入口。

它的作用：
- 列出当前 active 的 area
- 给出每个 area 的 canonical entrypoint
- 指定进入某个 area 时的推荐读取顺序
- 避免把旧目录或规划中的结构误当成当前真实入口
- 为 area-specific 技能和工作流提供统一路由入口

## Area rules
`areas/` 是 LeadFlow 的 responsibility layer。

规则：
- each area is an ongoing module
- each area can define its own internal structure
- each mature area should expose at least:
  - `SCHEMA.md`
  - `index.md`
  - `99-change-log.md`
- adding a new area means creating `areas/<name>/`, defining its local schema, then registering it here

## Current status
目前 `areas/` 下真正已经成型并可直接使用的 active area：
- `fitness/`
- `knowledge/`
- `work/`

以下 area 在根级导航或规划中可能被提及，但当前还没有完整入口，暂按 planned or partial 处理：
- `learning/`
- `personal/`

## How to use this registry
当问题涉及某个 ongoing domain 时：
1. 先读 `areas/index.md`（本页）
2. 再进入对应 `areas/<area>/index.md`
3. 再读对应 `areas/<area>/SCHEMA.md`
4. 然后再读该 area 的当前计划、日志、周总结等具体文件

如果某个 area 还没有自己的 `index.md` 或 `SCHEMA.md`：
- 不要假设它已经完整落地
- 应先按当前真实存在的文件工作
- 如有必要，再补 area 入口文件

## Active area registry
### 1) fitness
- Path: `areas/fitness/`
- Canonical entrypoint: `areas/fitness/index.md`
- Schema: `areas/fitness/SCHEMA.md`
- Main purpose: 训练、饮食、恢复、计划版本、周复盘、历史力量参考
- Preferred skills:
  - `ai-fitness-coach-cn`
  - `personal-tracking-memory-architecture`
- Recommended read order:
  1. `areas/fitness/index.md`
  2. `areas/fitness/SCHEMA.md`
  3. `areas/fitness/00-profile.md`
  4. `areas/fitness/01-goals.md`
  5. `areas/fitness/02-current-plan.md`
  6. `areas/fitness/03-decision-rules.md`
  7. 最近一个 `areas/fitness/20-weeks/*.md`
  8. 最近一个 `areas/fitness/10-checkins/*.md`
  9. 需要时再读 `30-nutrition/`、`30-strategy/`、`plan-versions/`、`99-change-log.md`
- Special handling:
  - 问“今天吃什么 / 今天练什么 / 今天记全了吗”时，必须同时核对 check-ins、weeks、current plan 和当前聊天事实
  - 不能只看单一文件就判断“没记录”

### 2) knowledge
- Path: `areas/knowledge/`
- Purpose: retained technical reading notes, article corpora, and ongoing knowledge curation
- Schema: `areas/knowledge/SCHEMA.md`
- Preferred skills:
  - `wechat-article-wiki-ingest`
  - `second-brain-wiki-architecture`

### 3) work
- Path: `areas/work/`
- Purpose: ongoing work context, operating assumptions, and future work-module expansion
- Schema: `areas/work/SCHEMA.md`
- Preferred skills:
  - `second-brain-wiki-architecture`
  - more area-specific work skills can be added later

## Planned / partial areas
### learning
- Status: planned / partial
- Expected purpose: 学习主题、学习计划、读书/课程/技能追踪
- Canonical entrypoint: not created yet

### personal
- Status: planned / partial
- Expected purpose: 个人生活系统、长期事务、非工作非健身类持续责任
- Canonical entrypoint: not created yet

## Boundary rules
- `areas/` 放 ongoing responsibilities，不放一次性项目
- 一次性目标放 `projects/`
- 通用知识、lead、deep research 放 `resources/`
- 旧结构或历史实验不作为 area 当前入口

## Routing rule for second-brain orchestration
当高层 second-brain skill 需要在本仓库内工作时：
1. 先读本页
2. 选择目标 area
3. 读 `areas/<area>/SCHEMA.md`
4. 如果该 area 有 preferred skill，优先按该 skill 路由

## Structural note
- 根级 `index.md` 是整个 wiki 的总导航
- `areas/index.md` 是 ongoing domains 的总注册表
- 各 area 自己的 `index.md` 才是 area 内部的直接入口
- `wiki/` 下的旧内容如果存在，应视为 legacy/bootstrap，而不是默认当前入口
