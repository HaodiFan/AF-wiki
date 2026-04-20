# 个人数据中心：可授权全量数据给 MCP 使用的 App

## Basic Info
- Title: 个人数据中心：可授权全量数据给 MCP 使用的 App
- Captured on: 2026-04-19 17:14:18 CST
- Status: todo
- Priority: high
- Source type: conversation
- Source: Feishu DM
- Seen via: 用户即时想法记录

## Why it caught my attention
- 让个人的分散数据源通过统一授权进入一个“个人数据中心”，再暴露给 MCP/agent 使用，有机会成为个人 AI 的基础设施层。
- 如果解决授权、权限边界、可撤销、审计和标准化 schema，这类产品会很有价值。

## Keywords
- MCP
- personal data center
- data authorization
- personal knowledge graph
- agent infrastructure
- identity and permissions

## Research questions
- 这个 App 的核心价值是“数据聚合”还是“给 agent 的可控调用层”？
- 用户如何授权不同数据源：通讯、日历、文档、位置、健康、消费、设备数据？
- MCP 接入时，权限模型如何设计：按数据域、按字段、按时间范围、按工具隔离？
- 如何实现可撤销、审计日志、最小权限和本地优先？
- 数据标准层应该是统一 schema、向量索引、知识图谱，还是事件流？

## Next action
- 后续可扩展成一份产品/架构研究笔记，梳理数据源、授权模型、MCP 接口层和隐私边界。

## Links
- Related deep research:
- Related project/area/resource: resources/leads/

## Raw notes
- 一个 app 可以授权所有数据，这个数据可以被 MCP 使用，形成个人数据中心。
