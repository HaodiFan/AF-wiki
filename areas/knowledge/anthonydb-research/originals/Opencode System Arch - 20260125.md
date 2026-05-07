---
title: "Opencode System Arch - 20260125"
tags:
  - area/knowledge
  - collection/anthonydb-research
  - source/anthonydb
  - topic/agent-systems
  - type/original
  - wiki/af
---
# Keys

## Meta
- type: `deepresearch`
- domain: `engineering`
- spark: `on`
- created: 2026-01-25
- source: KG/raw/legacy-notes/Opencode System Arch - 20260125.md

## Content
# Keys

## 关联笔记

- Claw 部署日记
- Keypoints

- （单仓库多包）范式
	- Opencode
- SST/IaC
- Nix 打包
- 工程范式
	- 工程范式演化地图
	```
	单体源码
	   ↓
	多 repo + 版本
	   ↓
	submodule（过渡）
	   ↓
	workspace（source graph）
	   ↓
	build graph（target）
	   ↓
	schema-first
	   ↓
	pipeline / agent
	
	```
	- 工程范式例子
```
# Repo
app/
├── controllers/
├── services/
├── models/
├── utils/
├── config/
└── main.py

# Multi-repo + Versioned Packages
#### frontend-repo
frontend/ 
├── src/ 
├── package.json 
└── build/

#### backend-repo
backend/ 
├── app/ 
├── requirements.txt 
└── dist/

#### desktop-repo
desktop/ 
├── resources/ 
│   ├── frontend/ 
│   └── backend/ 
└── electron/

# Submodule / Subtree 范式
desktop/
├── frontend/   (git submodule)
├── backend/    (git submodule)
└── scripts/
    └── build_all.sh

# Monorepo Workspace
repo/
├── apps/
│   ├── frontend/
│   ├── backend/
│   └── desktop/
│
├── packages/
│   ├── schema/
│   ├── protocol/
│   └── plugin-sdk/
│
├── scripts/
│   └── build-desktop.ts
│
├── pnpm-workspace.yaml
└── package.json

# Build Graph / Target-based 范式
repo/
├── frontend/
│   ├── BUILD
│   └── src/
├── backend/
│   ├── BUILD
│   └── app/
├── schema/
│   ├── BUILD
│   └── schema.json
└── WORKSPACE

# Artifact-centric
builder/
├── input/
│   ├── frontend-dist/
│   └── backend-binary/
├── assemble/
│   └── pack.py
└── output/
    └── app.exe

# Schema / Contract-first
repo/
├── schema/
│   ├── flow.json
│   ├── step.json
│   └── node.json
│
├── generated/
│   ├── frontend-types.ts
│   └── backend-models.py
│
├── frontend/
└── backend/

# Pipeline / Workflow-centric
repo/
├── flows/
│   ├── webagent_flow.json
│   └── replay_flow.json
│
├── steps/
│   ├── click.py
│   ├── type.py
│   └── api_call.py
│
├── runtime/
│   └── executor.py


```

## Keypoints
<!-- LLM 提取，每条是一个可连接的知识点 -->
<!-- 如果该 keypoint 在其他 node 也出现过，标注 (also in: node名) -->
- [[KP - Opencode|Opencode]]
- [[KP - backend-repo|backend-repo]]
- [[KP - desktop-repo|desktop-repo]]
- [[KP - frontend-repo|frontend-repo]]
## Links
### hints

### dive-ins
