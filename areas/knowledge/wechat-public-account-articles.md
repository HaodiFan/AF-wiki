# 微信公众号文章入口页

> Purpose: serve as the canonical entry page for retained WeChat article notes in the knowledge area.
> Last rebuilt: 2026-04-20

## Current status

- 这是一组从微信文章线索沉淀出来的 retained notes
- 当前多数条目仍属于“正文未成功抓取时的扩展笔记 / fallback note”
- 弱信号捕获仍应先进入 `resources/leads/`
- 一旦决定保留为知识资产，再落入 `areas/knowledge/`

## Article index

| 日期 | 主题 | 状态 | 笔记 |
|:-----|:-----|:-----|:-----|
| 2026-03-09 | GitHub 狂飙 2.5 万标星，这款「会自愈」的 Python 爬虫框架杀疯了！ | fallback note | [[wechat-articles/2026-03-09-self-healing-python-crawler]] |
| 2026-03-10 | AI发布首个全球科学家社区爆火，硅谷投资圈：科技研究领域的「谷歌地图」来了！ | fallback note | [[wechat-articles/2026-03-10-global-scientist-community]] |
| 2026-03-14 | 设计流程已死，Claude 设计负责人如何理解 AI 时代的设计？ | fallback note | [[wechat-articles/2026-03-14-ai-era-design]] |
| 2026-03-15 | 阿里面试官怒了：Embedding 模型都不会选，BGE 和 GTE 的区别都说不清，你这 RAG 系统能用？ | fallback note | [[wechat-articles/2026-03-15-embedding-bge-vs-gte]] |
| 2026-03-15 | 后训练中的RL已死？MIT新算法挑战传统后训练思维，谢赛宁转发 | fallback note | [[wechat-articles/2026-03-15-post-training-rl]] |
| 2026-03-21 | 专访OpenAI首席科学家：我们离“AI自己做研究”有多远？ | fallback note | [[wechat-articles/2026-03-21-ai-doing-research]] |
| 2026-03-24 | 使用 AI 实现 最新版本 Flutter HTTPS 明文抓包 | fallback note | [[wechat-articles/2026-03-24-flutter-https-capture]] |

## Working rule

1. 公众号链接先判断是弱信号还是值得保留的知识条目
2. 弱信号先放 `resources/leads/`
3. 决定保留时，在这里登记，并创建对应 article note
4. 如果后续拿到正文，可直接覆盖或升级对应 note，而不是新建第二份平行记录

## Follow-up ideas

- 后续可以按主题再建立二级索引，例如：
  - AI research
  - developer tools
  - design / product
  - RAG / retrieval
  - reverse engineering / debugging
