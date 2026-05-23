# Skill 分类体系 v1.0

> **版本**: v1.0
> **日期**: 2026-05-22
> **制定者**: 派蒙（大总管）
> **维护**: 持续更新

---

## 🎯 分类目标

让每个 Agent 知道自己能用什么 Skill，以及到哪里找。

---

## 📊 分类结构

| 类别 | 说明 | Skill 数量 |
|:-----|:-----|:----------:|
| 🌍 通用 | 所有 Agent 均可使用 | 8 |
| 🎨 内容 | 内容创作相关 | 4 |
| 🔧 技术 | 技术开发相关 | 12 |
| 🔬 调研 | 调研分析相关 | 1 |
| 🏢 基础设施 | 飞书/系统集成 | 6 |
| 🔧 系统工具 | OpenClaw 内置工具 | 6 |

---

## 🌍 通用 Skill（所有 Agent 可用）

| Skill | 用途 | 负责人 | 来源 |
|:------|:-----|:-------|:-----|
| context-eng | 上下文工程，管理 AI agent 的上下文 | 派蒙 | 自建 |
| agent-daily-report | 日报收集机制 | 派蒙 | 自建 |
| agent-task-board | SQLite 任务系统 | Tony | 自建 |
| knowledge_search | Chroma 向量库检索（Wiki/SOP/PRD/模板） | Tony | 自建 |
| taskflow | 任务流编排 | - | 预装 |
| taskflow-inbox-triage | 收件箱分流 | - | 预装 |
| clawhub | Skill 市场搜索/安装 | - | 预装 |
| healthcheck | 安全审计 | - | 预装 |

---

## 🎨 内容 Skill（阿加莘/老六/麦麦）

| Skill | 用途 | 负责人 | 来源 |
|:------|:-----|:-------|:-----|
| brainstorming | 结构化头脑风暴 | Nick | ClawHub |
| humanizer | 消除 AI 生成痕迹 | Nick | ClawHub |
| multi-source-research | 多源研究助手 | Nick | ClawHub |
| requirement-supplement | 需求补充 | Tony | 自建 |

---

## 🔧 技术 Skill（Zhongli/内容专家/交互测试专家）

| Skill | 用途 | 负责人 | 来源 |
|:------|:-----|:-----|
| code-review | 多维度代码审查 | Nick/Zhongli | ClawHub |
| git-workflow | Git 工作流规范 | Zhongli | 自建 |
| frontend-ui | Vue 3 + Arco Design 前端 | Zhongli | 自建 |
| tdd-workflow | 测试先行开发流 | Nick/Zhongli | ClawHub |
| requirement-understanding | 需求理解 v2.1 | Tony | 自建 |
| requirement-breakdown | 需求拆解 | Tony | 自建 |
| spec-driven | 规范驱动开发 v2.0 | Tony | 自建 |
| task-planning | 任务规划与拆分 | Tony | 自建 |
| claude-code-orchestrator | Claude Code 任务编排 | Tony | 自建 |
| prd-generation | PRD 生成 | Tony | 自建 |

---

## 🔬 调研 Skill（Nick/小二子）

| Skill | 用途 | 负责人 | 来源 |
|:------|:-----|:-------|:-----|
| Deep Research | 多源深度调研 | Nick | ClawHub |

---

## 🏢 基础设施 Skill（飞书集成，所有 Agent 通用）

| Skill | 用途 | 负责人 | 来源 |
|:------|:-----|:-------|:-----|
| feishu-doc | 飞书文档读写 | - | 插件 |
| feishu-drive | 飞书云盘管理 | - | 插件 |
| feishu-perm | 飞书权限管理 | - | 插件 |
| feishu-wiki | 飞书知识库导航 | - | 插件 |
| browser-automation | 浏览器自动化 | - | 插件 |
| epic-walkthrough | Epic 走查流程 | Tony | 自建 |

---

## 🔧 系统工具 Skill（OpenClaw 内置）

| Skill | 用途 | 说明 |
|:------|:-----|:-----|
| 1password | 密码管理 | 依赖 1password CLI |
| apple-reminders | 提醒事项 | 依赖 remindctl |
| weather | 天气查询 | 内置 |
| github | GitHub 操作 | 依赖 gh CLI |
| gh-issues | GitHub Issues | 依赖 gh CLI |
| imsg | iMessage | macOS only |
| mcporter | MCP 服务管理 | 内置 |
| node-connect | 节点连接诊断 | 内置 |
| skill-creator | Skill 创建辅助 | 内置 |

---

## 📋 Agent × Skill 映射表

| Agent | 常用 Skill | 专属 Skill |
|:------|:-----------|:-----------|
| **派蒙** | context-eng, agent-daily-report, agent-task-board, clawhub, knowledge_search | agent-daily-report, context-eng |
| **Nick** | Deep Research, multi-source-research, brainstorming, humanizer, code-review | Deep Research, multi-source-research |
| **Tony** | requirement-understanding, requirement-supplement, prd-generation, spec-driven, task-planning | prd-generation, epic-walkthrough |
| **Zhongli** | git-workflow, frontend-ui, code-review, tdd-workflow | frontend-ui, git-workflow |
| **阿加莘** | brainstorming, humanizer, multi-source-research | - |
| **老六** | brainstorming, humanizer | - |
| **麦麦** | brainstorming, humanizer, knowledge_search | - |
| **小二子** | Deep Research, multi-source-research | - |
| **内容专家** | code-review, git-workflow, spec-driven | - |
| **交互测试专家** | frontend-ui, tdd-workflow | - |

---

## 🎯 使用指南

### 1. 查找 Skill
```
路径：~/.openclaw/skills/_registry.md
```

### 2. 申请新 Skill
```
路径：Wiki → 变更申请 → 新 Skill 申请
```

### 3. 报告 Skill 问题
```
路径：review-logs/incidents/
```

---

## 📅 维护记录

| 日期 | 变更 | 执行人 |
|:-----|:-----|:-------|
| 2026-05-22 | 初始版本，38 个 Skill 分类完成 | 派蒙 |

---

*版本: v1.0 | 更新: 2026-05-22*