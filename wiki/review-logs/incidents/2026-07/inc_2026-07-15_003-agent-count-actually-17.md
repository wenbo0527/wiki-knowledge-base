---
title: inc 2026 07 15 003 agent count actually 17
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-15
---

# INC-2026-07-15-003: Agent 真实数量 17 个（报告"30 个"是错的）

> **揭穿**: 7-15 09:32 文博指出"Agent 数量也不对"  
> **9:37 verify 后**: `openclaw agents list` 返回 **17 个 agent**（main 派蒙 + 16 个其他）  
> **报告错版**: `wiki/review-logs/reports/wiki-project-status-report-20260715.md` §3.4 / §5.5 / §8.2 写"30 个 Agent"（用 `ls | wc -l` 误算，混入了 .md .json 配置文件）

---

## 现象

报告 `wiki-project-status-report-20260715.md` §3.4 写：

> **30 个 Agent**（按 SOUL/AGENTS 完整度）

但 7-15 09:32 文博指出数量不对。

## 根因（双层）

### 🔴 错算 1：用 `ls | wc -l` 数目录时混入了 .md .json 配置文件

`ls /Users/wenbo/.openclaw/workspace/agents/` 返回 30 个条目
但其中：
- 9 个 agent 目录（nick_fury/zhongli/agatha/...）
- 21 个 **配置文件**（SOUL.md / AGENTS.md / openclaw.json / tasks.json / rss_all_sources_final.json / SKILL.md / IDENTITY.md / NOTICE_FOR_NICK_FURY.md / multi_agent_config_guide.md / openclaw.json.backup_20260305_091716 ...）

**直接用 `ls | wc -l` = 30 是错的**（混了配置和 agent）

### 🔴 错算 2：未调 `openclaw agents list` API 实测

正确方式：`openclaw agents list` 返回真正的 agent 列表（含 main 派蒙）

## 真实全量（9:37 verify）

`openclaw agents list` 实测返回 **17 个 agent**：

| # | agent_id | 名字 | Workspace | 角色分类 |
|:---|:---|:---|:---|:---|
| 1 | **main** | 🎭 派蒙 (Paimon) | workspace-agents/paimon | 调度中心 |
| 2 | **nick_fury** | 🕵️ 尼克·弗瑞 | workspace/agents/nick_fury | 情报分析 |
| 3 | **zhongli** | 🛡️ 钟离 (Zhongli) | workspace-agents/zhongli | 架构 |
| 4 | **tony_stark** | 🦾 托尼·斯塔克 | workspace-agents/tony_stark | 产品 |
| 5 | **agatha** | ✍️ 阿加莘 (Agatha) | workspace/agents/agatha | 写作/编辑 |
| 6 | **content_expert** | 📚 内容专家 | workspace-agents/content_expert | 内容 |
| 7 | **interaction_expert** | 🔍 交互测试专家 / UX Guardian | workspace-agents/interaction_expert | 测试/UX |
| 8 | **laoliu** | 🔍 老六 | workspace/agents/laoliu | 测试/UX |
| 9 | **risk_query** | 🎯 问小数 (RiskQuery) | workspace-agents/risk_query | 业务专家 |
| 10 | **xiaoerzi** | 🔬💹 小二子 | workspace/agents/xiaoerzi | 业务专家 |
| 11 | **maimai** | 💖 麦麦 | workspace/agents/maimai | 业务专家 |
| 12 | **smith** | 🔨 smith | workspace-agents/smith | 工具 |
| 13 | **data_community_pm** | 📋 Data Community PM | workspace-agents/data_community_pm | 数字社区团队 |
| 14 | **data_community_arch** | 🏛️ Data Community Architect | workspace-agents/data_community_arch | 数字社区团队 |
| 15 | **data_community_dev** | 🛠️ Data Community Developer | workspace-agents/data_community_dev | 数字社区团队 |
| 16 | **data_community_qa** | 🧪 Data Community QA & DevOps | workspace-agents/data_community_qa | 数字社区团队 |
| 17 | **data_community_doc** | 📚 Data Community Documenter | workspace-agents/data_community_doc | 数字社区团队 |

## 按角色分类（修正版）

| 角色 | 数量 | Agent |
|:---|:---:|:---|
| **调度中心** | 1 | 派蒙 (main) |
| **核心三巨头** | 3 | Nick Fury / Tony Stark / Zhongli |
| **写作/编辑** | 2 | 阿加莘 / 内容专家 |
| **测试/UX** | 2 | 交互测试专家 / 老六 |
| **业务专家** | 3 | 问小数 (RiskQuery) / 小二子 / 麦麦 |
| **工具** | 1 | smith |
| **数字社区团队** | 5 | data_community_pm/arch/dev/qa/doc |
| **合计** | **17** | （2 次揭穿报告错） |

## 按 workspace 位置分类

| 位置 | 数量 |
|:---|:---:|
| `/Users/wenbo/.openclaw/workspace/agents/` | 9 |
| `/Users/wenbo/.openclaw/workspace-agents/` | 15（含 6 个 data_community 团队 + wenbo + doubao-pro-128k 不在 list） |
| `/Users/wenbo/.openclaw/agents/`（base config） | 19（含 2 个 inactive） |
| **`openclaw agents list` 真实活跃** | **17** |

## 报告修正

| 维度 | 错版（9:15）| 正版（9:37）|
|:---|:---|:---|
| Agent 总数 | 30 | **17** |
| Nick 团队 | 5 高活跃 + 5 中活跃 + 20 待激活 | **重新评估 17 个** |
| 活跃度分布 | 待激活 20 个 | 需以 `openclaw agents list` 为准 |

## 教训（L-38 沉淀）

详见 `lesson-2026-07-15-agent-count-must-use-openclaw-api.md`

### L-38 核心

**Agent 数量必须用 `openclaw agents list` API 实测，不能用 `ls | wc -l` 数目录**。

反例：9:15 报告用 `ls /Users/wenbo/.openclaw/workspace/agents/ | wc -l` 算 30，混入 .md .json 配置文件 + 跨多个 workspace 目录。

正例：9:37 修正用 `openclaw agents list` → 17 个真实活跃 agent。

## 修复方向

- ✅ 写 INC-003 归档
- ✅ L-38 沉淀
- ✅ 报告 §3.4 / §5.5 / §8.2 修正
- 🟡 AGENTS.md v3.2 周日升级时纳入 L-38
- 🟡 评估"20 个待激活"是否需要重新数

## 状态

- [x] INC-003 创建（9:37）
- [x] L-38 沉淀
- [x] 报告修正（9:38）
- [ ] Close

---

*INC 完稿: 2026-07-15 09:37 CST*
*接单人: 尼克·弗瑞 🕵️*
*关联: 报告 `wiki-project-status-report-20260715.md` §3.4 / §5.5 / §8.2 已修正*
