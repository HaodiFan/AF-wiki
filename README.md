<div align="center">

# 🧠 AF Wiki

**一个按动态 area 模块组织的个人知识系统。**

<sub>LeadFlow 架构 · Area Registry · Agent 辅助维护</sub>

</div>

---

## 👀 第一次看这里

如果你是第一次打开这个仓库，先看 [START-HERE.md](START-HERE.md)。

这次重构后的核心规则是：
- `areas/` 承载持续性的 area 模块
- `resources/` 只承载共享的 lead / research 流水线
- 每个 area 自己维护内部 `SCHEMA.md`
- LeadFlow 的其他顶层层级也都已补成轻量 scaffold

推荐阅读顺序：
[START-HERE.md](START-HERE.md) → [areas/index.md](areas/index.md) → [index.md](index.md) → 目标 area 的 `SCHEMA.md`

---

## 📡 最近动态

| 日期 | 领域 | 动态 |
|:-----|:-----|:-----|
| 04-22 | 💪 Fitness | 完成游泳 22:51（总用时 23:49），325 m / 13 趟，141 kcal，平均心率 133；以蛙泳为主 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-22 | 🍽️ Nutrition | 早餐 3 个鸡蛋 + 牛奶；游泳前香蕉；午餐 200 g 西冷牛排 + 1 根玉米 + 气泡水 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-22 | 📝 Summary | 今天按计划完成中等强度游泳；午餐轻量但蛋白恢复不错，晚餐与睡前补给仍待补 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-21 | 💪 Fitness | 完成背 + 二头力量训练 42:18，335 kcal，平均心率 123 bpm；含面拉、核心和背部拉伸收尾 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-21 | 🍽️ Nutrition | 早餐 3 个鸡蛋 + 奶；午餐煎烤牛肉谷物碗 + 卤牛肉 + 巴黎水；晚餐牛腱子 + 彩椒 + 米饭 + 菠菜 + 菠萝/荔枝 + 酸奶 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-21 | 📝 Summary | 原计划周二游泳，实际改为 pull 向力量训练；训练完成度高，当天饮食已补全到晚餐，睡前蛋白加餐仍待确认 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-20 | 💪 Fitness | 完成胸 + 三头 + 核心力量训练 48:31，414 kcal，平均心率 128 bpm — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-20 | 🍽️ Nutrition | 早餐 3 个鸡蛋；午餐牛腱子 + 沙拉约 537 kcal / 77 g 蛋白；晚餐三文鱼 200 g + 西兰花 + 彩椒 + 米饭 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-20 | 📝 Summary | 今天完成计划内周一 push 日；训练完成度高，饮食主餐结构到位，睡前补给仍待补充确认 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-20 | 🔧 System | area 层收敛为动态模块：knowledge 提升为 area，并补 work area 骨架 — [详情](log.md) |
| 04-19 | 🔧 System | LeadFlow 架构正式命名，并统一仓库与主页文案 — [详情](log.md) |
| 04-18 | 📋 Planning | W17 训练计划改为下肢、游泳、推拉混合，并匹配营养节奏 — [详情](areas/fitness/20-weeks/2026-W17-plan.md) |
| 04-18 | 🏊 Fitness | 游泳 500m，配速 4'37/100m，平均心率 150 bpm — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-18 | 🥩 Nutrition | 晚餐牛腱子加牛肉约 750g，当日蛋白基本已覆盖 — [详情](areas/fitness/10-checkins/2026-04.md) |
| 04-18 | 📚 Knowledge | 收录 7 篇公众号技术文章线索，并建立统一入口页 — [详情](areas/knowledge/wechat-public-account-articles.md) |
| 04-18 | 🔧 System | 首页与总导航改成近期状态优先展示，突出时间线入口 — [详情](log.md) |

## 🏆 Strength PR / 历史最佳纪录

- 统一入口：[historical-strength-reference.md](areas/fitness/30-strategy/historical-strength-reference.md)
- 当前代表性纪录：
  - 卧推：**60 × 5** / **55 × 8**
  - 上斜推：**40 × 10**
  - 坐姿推胸：**30 × 12**
  - 高位下拉：**55 × 8-12**
  - 蝴蝶机夹胸：**35 × 10**
  - 坐姿划船：**45 × 12**

## 🗺️ 当前结构总览

```text
AF-wiki/
├── archive/         ← 历史归档与旧版本保留
├── areas/           ← 动态 area 模块层
│   ├── index.md         area registry + routing
│   ├── fitness/         训练、营养、周计划与 check-in
│   ├── knowledge/       阅读入口与 retained article notes
│   └── work/            工作 area 骨架
├── dashboards/      ← 摘要面板与 backlog
├── resources/       ← 共享 lead / research 流水线
│   ├── leads/           weak-signal capture
│   ├── research/        deep research scaffold
│   └── ideas/           ideas scaffold
├── inbox/           ← quick capture scaffold
├── projects/        ← project layer scaffold
├── templates/       ← 统一模板
├── wiki/            ← 早期 wiki 骨架草案，不是当前主入口
├── START-HERE.md    ← 当前-vs-目标导览
├── index.md         ← 根级导航入口
├── SCHEMA.md        ← LeadFlow 总规则
└── log.md           ← 系统级变更日志
```

| 快速入口 | 当前已落地 | 规划中 / 历史遗留 |
|:-----|:-----|:-----|
| [START-HERE.md](START-HERE.md)<br>[areas/index.md](areas/index.md)<br>[index.md](index.md)<br>[SCHEMA.md](SCHEMA.md)<br>[log.md](log.md) | [areas/fitness/](areas/fitness/) 健身 memory<br>[areas/knowledge/](areas/knowledge/) 技术阅读与 retained knowledge<br>[areas/work/](areas/work/) work area 骨架<br>[resources/leads/](resources/leads/) 研究候选与跟踪<br>[resources/research/](resources/research/) deep research scaffold<br>[resources/ideas/](resources/ideas/) ideas scaffold<br>[inbox/](inbox/) quick capture scaffold<br>[projects/](projects/) project scaffold | [archive/legacy/](archive/legacy/) 旧版 fitness 资料归档<br>[wiki/](wiki/) 更早期骨架草案 |

---

<div align="center">
<sub>🌱 先确定 area，再调用 area 自己的 schema 和 skill。</sub>
</div>
