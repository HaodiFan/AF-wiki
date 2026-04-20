# Fitness Area Index

> AF fitness area navigation and operating entrypoint
> Last updated: 2026-04-20

## Purpose
这个页面是 `areas/fitness/` 的入口页。

它的作用：
- 告诉我这个 area 里的当前有效文件在哪
- 规定日常读取顺序，避免只读到局部文件就误判“没记录”
- 说明训练、饮食、计划版本、周总结分别该写到哪里
- 明确防漏记审计规则，减少“你说过但下次我却没找到”的情况
- 给出 fitness 相关任务的默认 skill / workflow 路由

## Recommended read order
当问题与 fitness 相关时，优先按这个顺序进入：
1. `areas/fitness/index.md`（本页）
2. `areas/fitness/SCHEMA.md`
3. `areas/fitness/00-profile.md`
4. `areas/fitness/01-goals.md`
5. `areas/fitness/02-current-plan.md`
6. `areas/fitness/03-decision-rules.md`
7. 最近一个 `areas/fitness/20-weeks/*.md`
8. 最近一个 `areas/fitness/10-checkins/*.md`
9. 若问题涉及饮食策略，再读 `areas/fitness/30-nutrition/`
10. 若问题涉及历史选重或动作参考，再读 `areas/fitness/30-strategy/historical-strength-reference.md`
11. 若问题涉及计划沿革，再读 `areas/fitness/plan-versions/` 与 `areas/fitness/99-change-log.md`

## First read / current operating notes
- `SCHEMA.md` — fitness 记录结构与更新协议
- `00-profile.md` — 稳定背景、偏好、器械约束
- `01-goals.md` — 当前目标与评估方向
- `02-current-plan.md` — 当前生效计划
- `10-checkins/2026-04.md` — 当月 check-in
- `20-weeks/2026-W16.md` — 周级总结
- `20-weeks/2026-W17-plan.md` — 当前周计划
- `30-strategy/historical-strength-reference.md` — 历史力量参考
- `99-change-log.md` — 重要变更记录

## Routing note
- 日常教练、记录和计划调整优先使用 `ai-fitness-coach-cn`
- 结构级调整优先使用 `personal-tracking-memory-architecture`

## Core files
- `SCHEMA.md` — fitness 记录结构与更新协议
- `00-profile.md` — 稳定偏好、限制、长期背景
- `01-goals.md` — 当前目标
- `02-current-plan.md` — 当前生效计划
- `03-decision-rules.md` — 决策规则
- `10-checkins/` — 日度滚动记录
- `20-weeks/` — 每周复盘与偏差总结
- `30-nutrition/` — 当前饮食策略与复用模板
- `30-strategy/` — 历史力量参考、模板、策略沉淀
- `plan-versions/` — 历史计划版本归档
- `99-change-log.md` — 重大调整日志

## What goes where
### 1) Daily facts
以下内容优先写进 `10-checkins/YYYY-MM.md`：
- 当天练了什么 / 没练什么
- 时长、消耗、心率、强度
- 动作明细
- 早餐 / 午餐 / 晚餐 / 加餐 / 训练后 / 睡前补给
- 当天状态、恢复、睡眠、体重

### 2) Weekly summary
以下内容优先写进 `20-weeks/YYYY-Www.md`：
- 这周完成了哪些训练
- 偏离计划的地方
- 饮食整体模式
- 恢复观察
- 下周调整决策

### 3) Active plan
以下内容优先写进 `02-current-plan.md`：
- 当前正在执行的训练结构
- 当前营养目标
- 当前恢复规则
- 当前关键调整说明

### 4) Historical plan versions
若训练计划发生版本级变化：
- 当前版本写进 `02-current-plan.md`
- 旧版本归档进 `plan-versions/`
- 同时在 `99-change-log.md` 记变更原因

## Anti-miss audit rules
为了避免以后漏判，遇到“今天记全了吗 / 我是不是说过 / 还缺什么”这类问题时，必须按下面检查：

1. 先合并当前聊天里同一天已经说过的事实
2. 再核对该日期在 `10-checkins` 是否已写入
3. 再核对对应 `20-weeks` 是否有更晚或更细的补充
4. 再参考 `02-current-plan.md` 判断这一天理论上应出现哪些训练/饮食槽位
5. 输出时明确区分：
   - 已在 wiki 中
   - 当前聊天已提到但未写入 wiki
   - 仍缺失 / 待确认

## Same-day update rule
如果同一天的信息是分多轮发来的：
- 不要新开第二个零散日期块
- 要回到同一个日期块里持续合并
- 训练摘要层和动作层都要保留
- 餐次层要标明哪些已知、哪些未知、哪些待确认

## Evaluation rule
如果用户问“今日评测 / 今天整体怎么样”：
- 先检查今天原计划是什么
- 再检查今天实际训练和饮食记录
- 再判断计划符合度
- 如果缺任何关键项，要明确写“待补充”，不能直接说没有记录

## Current known structural note
- 根级 `index.md` 存在，是整个 AF wiki 的总导航
- `areas/index.md` 是 ongoing domains 的总注册表
- `wiki/index.md` 属于旧层，不应默认作为当前 active fitness 入口
