---
title: zhongli daoge kb 05 claude code 团队化落地
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-tools]
date: 2026-06-30
---

# #5 Claude Code 团队化落地指南：从个人技巧到可复制工程体系

**源**: 刀哥 KB `2eYxaj0z` | note_id `1902180448843424352` | 2026-02-20 | tags: Claude Code, 团队化
**链接**: https://kb.daode.com/note/1902180448843424352
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐⭐（**CC 架构规范的直接素材**）

---

## 🎯 核心 Insight

**团队使用痛点**：个人体验好，换人不稳定 / 换项目复读 / 质量波动 / 返工率高  
**核心结论**：提示词仅为入门，需将经验沉淀为**可版本化、可评审、可迭代的配置体系**

### 7 大构件体系（从强约束到弱约束）

| 构件 | 定位 | 核心 |
|:---|:---|:---|
| **CLAUDE.md** | 项目级记忆 | 构建流程 / 测试方法 / 目录结构 / 禁区 |
| **rules/** | 底线规则 | 安全 / 测试 / 风格 / Git 工作流 |
| **agents/** | 专用子代理 | 规划师 / 架构师 / 审查 / E2E 测试 |
| **commands/** | 高频流程 | `/plan` `/code-review` 斜杠命令 |
| **skills/** | 可复用方法论 | TDD / 设计模式 / 安全审查清单 |
| **hooks/** | 自动化守卫 | PreToolUse/PostToolUse/Stop 事件 |
| **.mcp.json** | 外部工具接入 | CLI / API 服务 |

**逻辑链**：CLAUDE.md("我们是谁") → rules("必须守什么") → commands("高频怎么做") → hooks("必须发生什么")

### 推荐目录结构

```
your-repo/
├─ CLAUDE.md
└─ .claude/
   ├─ rules/
   ├─ agents/
   ├─ commands/
   ├─ hooks/
   └─ settings.json
```

### 7 天落地路线图

| 天 | 任务 |
|:---:|:---|
| Day 1 | 极简 CLAUDE.md（仅无法推导的关键信息） |
| Day 2 | 基础 rules（security.md / testing.md） |
| Day 3 | `/plan` 命令（强制先规划后编码） |
| Day 4 | `/code-review` 命令（固化审查维度） |
| Day 5 | 提醒型 Hook（"用 tmux 跑耗时命令"） |
| Day 6 | 一致性 Hook（自动格式化、类型检查） |
| Day 7 | 专用 Agent（分离编码与审查） |

### `/plan` 命令核心价值

复述需求 → 风险评估 → 步骤分解 → 等待确认 → 执行编码  
**降低返工成本，减少团队信任损耗，确保"可解释的变更"**

### 常见翻车点

1. CLAUDE.md 过度冗长（**保留关键，动作移 hooks**）
2. 混淆偏好与底线（**rules 只写必须遵守**）
3. Hook 过度阻断（**提醒→一致→阻断渐进**）
4. 敏感信息泄露（**环境变量注入，仓库仅占位**）
5. 盲目照搬外部配置

---

## 🔧 对钟离可借鉴的部分（**直接迁移到我目前的 agent 团队**）

### 借鉴 1: 我目前的 7 大构件现状

| 构件 | 我的现状 | 改进 |
|:---|:---|:---|
| CLAUDE.md | 我的 MEMORY.md ≈ CLAUDE.md，但太冗长（18KB→3KB 后仍 3KB） | 拆：MEMORY.md（核心）+ AGENTS.md（流程）+ HEARTBEAT.md（心跳）= **3 文件分层** |
| rules/ | SOUL.md / USER.md 是软规则 | 写 `rules/security.md` `rules/style.md` 强约束 |
| agents/ | 5 个云端 agent（clarifier 等）+ 6 个本地 | 已经有！✅ 但缺少 agents/ 子代理定义文件 |
| commands/ | ❌ 没有 | 创建 `/plan` `/review` `/commit` 斜杠命令 |
| skills/ | ✅ `~/.openclaw/skills/` 已有 100+ skills | 继续沉淀 |
| hooks/ | ❌ 没有 | 创建 PreToolUse hooks（"修服务器前必 backup"） |
| .mcp.json | ❌ 没集成 | 加 .mcp.json 接入 minimax API / 飞书 |

### 借鉴 2: `/plan` 命令直接落地

**钟离的痛点**：今天 19 个来回中，**至少 5 次返工**（chat box 端点、build 产物路径、cache 策略等都是逐步发现）

**改进**：每个"超过 1h 的实施"前必走 `/plan`：
1. 复述需求（用户确认）
2. 风险评估（3 个潜在失败点）
3. 步骤分解（WBS + Checklist）
4. 等待确认
5. 执行

### 借鉴 3: 写+审分离硬规则（与我的 CC 架构规范一致）

**文中强调**：commands 高频流程 + agents 专用子代理 = 分离"编码"与"审查"  
**我的现状**：已经有"写代码 agent ≠ 审代码 agent"规则，但落地不严

**改进**：每个 PR 必含 `/plan` 输出 + 验收 Checklist（不是空白模板）

---

## 🚦 立即可执行（24h）

- [ ] 把 MEMORY.md 拆成 3 文件：CLAUDE.md(项目) + USER.md(用户) + SOUL.md(角色)
- [ ] 创建 `/plan` 斜杠命令（OpenClaw 命令系统）
- [ ] 给所有 SKILL.md 加 "适用范围 + 验收标准" 段落

## 🟡 本周可执行

- 写 `rules/security.md`（远程服务器操作前必 backup，引用我的"教训 5"）
- 创建 PreToolUse hooks（"ssh root@118.196.79.130" 前自动 backup nginx.conf）
- 给 5 个云端 agent 写 agents/ 子代理定义文件

## ⚠️ 风险

- **"Day 1-7 路线图"太理想化**：实际团队容易"Day 1 卡 3 天"
- **Hook 过度**：阻断型 hook 会让用户体验差，要"提醒型→一致性型→阻断型"渐进
- **盲目复用**：everything-claude-code 仓库的 agent 定义要适配，不直接抄

## 📚 关联 Wiki

- 04: planning-with-files（CLAUDE.md 本身就是稳定前缀）
- 09: CLAUDE.md 全攻略（4 级层级系统）
- 12: Vibe Coding 10 阶段（CLAUDE.md + PROGRESS.md 双文档系统）

---

*🛡️ 钟离 · 18:58 · 2026-06-23*  
*消化: Nick 派单 #5/15 · 与我现有 CC 架构规范高度互补*