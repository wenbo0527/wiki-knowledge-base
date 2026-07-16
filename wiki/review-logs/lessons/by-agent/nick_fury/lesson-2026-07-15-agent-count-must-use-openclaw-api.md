---
title: lesson 2026 07 15 agent count must use openclaw api
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# L-38: Agent 数量必用 `openclaw agents list` API 实测

> **教训族**: INC-2026-07-15-003 治本
> **类别**: 报告质量 / OpenClaw API / 计数方法
> **创建**: 2026-07-15 09:37
> **关联**: INC-2026-07-15-003 / L-37 / AGENTS.md §0.5

---

## 反例（9:15 报告 · wiki-project-status-report-20260715.md §3.4 / §5.5）

**错算方法**：
```bash
ls /Users/wenbo/.openclaw/workspace/agents/ | wc -l
# 输出: 30 ← 错了
```

**实际 30 包含**：
- 9 个 agent 目录（nick_fury/zhongli/agatha/...）
- 21 个 **配置文件**（SOUL.md / AGENTS.md / openclaw.json / tasks.json / rss_all_sources_final.json / SKILL.md / IDENTITY.md / NOTICE_FOR_NICK_FURY.md / multi_agent_config_guide.md / openclaw.json.backup_20260305_091716 / openclaw.json.backup_20260305_171020 / openclaw_complete_config.json / openclaw_complete_config_v2.json / openclaw_config_patch.json / feishu_config.json / feishu_setup_steps.md / feishu_usage_guide.md / models.json / setup_guide.md / configuration_retry.md / configuration_steps.md）

**业务影响**：
- 报告"30 个 Agent" 实际只有 17 个真实活跃
- 错误分类"5 高活跃 + 5 中活跃 + 20 待激活"——20 个"待激活"是配置文件
- 给文博判断团队规模造成误导

## 正例（9:37 修正）

**正确方法**：
```bash
openclaw agents list
```

**返回 17 个真实活跃 agent**：
- main (派蒙) + nick_fury + zhongli + tony_stark + agatha
- content_expert + interaction_expert + laoliu
- risk_query + xiaoerzi + maimai
- smith
- data_community_pm/arch/dev/qa/doc (5 个)

## 治本 SOP（Agent 数量 / 列表 必检）

### ✅ 必用命令

| 场景 | 命令 |
|:---|:---|
| **看 agent 列表 + 数量** | `openclaw agents list` |
| **看 agent 状态** | `openclaw agents list \| grep -E 'Workspace\|Identity'` |
| **看活跃 session** | `openclaw tasks list` |
| **看 launchd 状态** | `launchctl list \| grep <agent>` |

### ❌ 反例

| 错误命令 | 后果 |
|:---|:---|
| `ls /Users/wenbo/.openclaw/workspace/agents/ \| wc -l` | 混入 .md .json 配置文件（30 ≠ 9）|
| `ls -d /Users/wenbo/.openclaw/workspace-agents/*/ \| wc -l` | 跨 workspace 目录重复（15 ≠ 9）|
| `find /Users/wenbo/.openclaw -name "agent" -type d` | 找到 base config 目录（19）≠ 真实活跃（17）|
| 凭 MEMORY.md / TOOLS.md 印象 | 配置可能过时 |

### 数据源对比

| 数据源 | 数字 | 含义 |
|:---|:---:|:---|
| `openclaw agents list` | **17** | ✅ 真实活跃 agent |
| `~/.openclaw/workspace/agents/*/` | 9 | 部分 agent workspace |
| `~/.openclaw/workspace-agents/*/` | 15 | 另一部分 agent workspace（含 5 个 data_community 团队）|
| `~/.openclaw/agents/*/` | 19 | base config 目录（含 2 个 inactive）|
| MEMORY.md 印象 | "3 个核心" | 2026-04-30 早期版本，过时 |

## 关联教训

- **L-13** (OpenClaw 原生优先) — 用 openclaw API 而非 ls
- **L-37** (报告必 verify 实时 API) — 通用方法论
- **L-38** (Agent 数量必用 openclaw agents list) — **本条 · 特定领域**

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次报告 Agent 数量** | `openclaw agents list` | 必检 |
| **每周日 22:00** | Agent 状态盘点（含活跃度）| c3 cron 升级 |
| **新加 Agent** | `openclaw agents list` 验证注册成功 | 手动 |

---

*Lesson 完稿: 2026-07-15 09:37 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-003 ✅ 应急已闭环*
