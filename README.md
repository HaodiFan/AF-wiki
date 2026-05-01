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

<table>
  <thead>
    <tr>
      <th>日期</th>
      <th>维度</th>
      <th>状态</th>
      <th>入口</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3"><strong>04-28</strong></td>
      <td>💪 训练</td>
      <td>back + biceps focused machine session with core finisher力量训练完成。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>🍽️ 营养</td>
      <td>早餐 3 个鸡蛋、午餐vegetarian set meal with 1 bowl of rice + scrambled egg + zucchini + wood ear mushroom + and other mixed vegetables、晚餐partially confirmed via the post-workout 70 g beef portion; any additional dinner foods remain unconfirmed、训练前 牛肉 180 g、训练后 remaining beef 70 g。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>📝 评估</td>
      <td>this is clearly a completed training day rather than a blank day, and recovery protein is now materially covered, but the dinner structure is still only partially closed unless later foods are added。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td rowspan="3"><strong>04-27</strong></td>
      <td>💪 训练</td>
      <td>胸 + 三头 + 核心力量训练完成，<code>50:37</code>，<code>319 kcal</code>，平均心率 <code>111 bpm</code>。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>🍽️ 营养</td>
      <td>早餐 3 个鸡蛋 + 1 个猕猴桃、午餐牛肉 200 g + 玉米 1 根 + 1 bottle of 气泡水、晚餐仍待确认、训练前后各 1 根香蕉。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>📝 评估</td>
      <td>training closure is clear, but recovery closure still depends on dinner or later protein intake。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td rowspan="3"><strong>04-26</strong></td>
      <td>🏊 训练</td>
      <td>游泳完成，<code>38:59</code>，<code>500 m</code>，<code>218 kcal</code>，平均心率 <code>132 bpm</code>。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>🍽️ 营养</td>
      <td>早餐 1 pack of 轻食饼干 + 玉米 1 根、午餐牛肉 180 g + 地瓜干 300 g、晚餐鳕鱼汉堡 + 玉米 1 根。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>📝 评估</td>
      <td>this day is not blank; training and all three meal slots are grounded, but the intake still looks somewhat carb-heavy and not maximally protein-efficient。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td rowspan="3"><strong>04-25</strong></td>
      <td>💪 训练</td>
      <td>肩 + 手臂 + 核心力量训练完成，<code>42:36</code>，<code>361 kcal</code>，平均心率 <code>126 bpm</code>。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>🍽️ 营养</td>
      <td>早餐 轻食饼干 + 1 根士力架、午餐原味卤牛肉 250 g、晚餐仍待确认。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
    <tr>
      <td>📝 评估</td>
      <td>this day is not blank; training is complete and grounded, but the nutrition side is still front-light with dinner evidence missing。</td>
      <td><a href="areas/fitness/10-checkins/2026-04.md">check-in</a></td>
    </tr>
  </tbody>
</table>

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
