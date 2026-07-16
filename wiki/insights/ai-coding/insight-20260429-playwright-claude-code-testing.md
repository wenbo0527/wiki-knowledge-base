---
title: insight 20260429 playwright claude code testing
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-coding]
date: 2026-05-23
---

# 洞察：Playwright CLI × Claude Code 企业级自动化测试实践

> 原始链接: https://mp.weixin.qq.com/s/v20wKu5m0f0ivQQimwFREw
能力框架: capability-value-closed-loop capability-requirement-decision

> **洞察编号**：insight-20260429-playwright-claude-code-testing
> **来源**：JAVA日知录 微信公众号 (2026-04-24)
> **原始链接**：https://mp.weixin.qq.com/s/v20wKu5m0f0ivQQimwFREw
> **价值评级**：⭐⭐⭐⭐ (4/5)
> **标签**：#ClaudeCode #Playwright #VibeCoding #HarnessEngineering #AI测试
> **维护人**：尼克·弗瑞
> **更新日期**：2026-04-29

---

## 核心洞察

### 1. 三Skill架构：创建→执行→自优化的完整闭环

这是 Harness Engineering 思想在测试领域的完整实现：

```
┌─────────────────────────────────────────────────────────────┐
│  Skill 1: adding-playwright-cli-tests                      │
│  输入: 自然语言测试意图                                       │
│  输出: 标准化 .md 用例文件                                    │
│  效果: 新增场景时间 半天 → 十几分钟                            │
├─────────────────────────────────────────────────────────────┤
│  Skill 2: 批量执行调度                                       │
│  输入: 所有用例列表                                           │
│  执行: haiku 子Agent并发执行（而非opus/sonnet）               │
│  输出: PASS/FAIL + Tool/Token/耗时指标                       │
│  效果: 回归效率质的飞跃                                       │
├─────────────────────────────────────────────────────────────┤
│  Skill 3: parse-agent-log.py + Agent优化                     │
│  输入: jsonl执行日志                                         │
│  分析: 提取浪费模式（冗余snapshot/超时/waitForTimeout）        │
│  输出: 优化建议 → 人工确认 → 迭代验证                         │
│  效果: 4轮迭代后 Tool -64%, Token -58%, 耗时 -65%            │
└─────────────────────────────────────────────────────────────┘
```

**关键洞察**：测试执行不需要opus/sonnet的深度推理能力，haiku速度快10倍、成本低98%，完全满足需求。

---

### 2. CRITICAL RULES：把文档变成契约

Agent自由发挥是Harness的核心挑战。这篇文章给出了具体解法：

```markdown
CRITICAL RULES:
• 不要对.yml快照文件使用Read工具（用Grep更快，Read浪费Token）
• close后立刻停止，不要再拓展任何操作
• 不要使用waitForTimeout，用waitForURL或waitForSelector
• .md里已写的命令一字不改直接执行，不要重写或内联
• 不要自起名目进行ls/find/glob文件系统探索
```

效果：**Tool调用从20+降到9次**，执行变得非常干净。

> 文档只是"建议"，不是"契约"。只有强制约束，才能让执行路径稳定、成本可预测。

---

### 3. Batch分组 + 前置依赖：让.md用例模块化

长流程（几十步，跨两个系统）的处理方式：

```
Batch分组：按语义将命令分组
├── Batch 1: 导航 + 填写项目基本信息
├── Batch 2: 完成项目计划 + TB iframe新增任务
└── Batch 3: 提交验证

前置依赖抽离：
├── 00-login-feedback.md       → 可复用登录模块
└── 00-oa-approve-prerequisite.md → 可复用OA审批模块

复杂JS外置：
└── scripts/04-step2-basic-info.js → 前端操作脚本模块化
```

用例本身只保留"业务流程骨架"，通用步骤和复杂逻辑下沉到可复用模块。

---

### 4. haiku替代opus/sonnet：成本意识驱动架构决策

**传统认知**：复杂任务需要最强模型

**本文实践**：测试执行是机械操作，haiku完全胜任：
- 速度快10倍
- 成本低98%
- opus/sonnet留给Skill 1（创建）和Skill 3（优化分析）

这是**成本敏感型AI应用的典型决策模式**。

---

## 与现有体系的关系

### 补充了 Claude Code 并行开发指南的实战案例

当前 Wiki 的 `claude-code-parallel-dev.md` 侧重理论框架，这篇文章提供了**真实企业级六阶段演进**的完整过程：

| Wiki现有内容 | 本文补充 |
|-------------|---------|
| Subagents + Agent Teams | **haiku子Agent并发执行**的具体实现 |
| Git Worktree | **Batch分组 + 前置依赖**的模块化方式 |
| Routines | **CRITICAL RULES**作为执行契约 |

### 补充了 Harness Engineering 的具体失败模式和解决方

| 失败模式 | 解决方案 |
|---------|---------|
| Agent自由发挥（需求蔓延） | CRITICAL RULES强制约束 |
| 测试资产无法沉淀 | .md + .js文件版本化管理 |
| 执行路径不可重复 | 命令原样执行，不重写 |
| 成本不可预测 | Skill 3自动分析+优化 |
| 跨系统传参 | localStorage方案 |

### 补充了 Vibe Coding 的具体案例

文章完整展示了**从"测试小白手动跑第一条命令"到"全自动化架构"**的演进过程，是Vibe Coding在企业测试场景落地的最佳实践之一。

---

## 实践要点

### 企业落地路径

```
阶段1（1-2周）：手动跑通第一个用例
  → 验证playwright-cli + Claude Code可行

阶段2（1周）：编写.md用例 + CRITICAL RULES
  → 建立标准化用例格式

阶段3（2周）：Batch分组 + 前置依赖
  → 支持复杂长流程

阶段4（1周）：Skill 1自动化用例生成
  → 把经验固化为Skill

阶段5（2周）：Skill 2并发执行
  → haiku子Agent批量执行

阶段6（持续）：Skill 3自优化
  → 指标驱动持续优化
```

### 关键技术决策

| 决策 | 理由 |
|------|------|
| haiku替代opus执行 | 成本低98%，速度10x，测试是机械操作 |
| .md替代.spec.ts | 人机双可读，版本化管理，跨团队复用 |
| Grep替代Read快照文件 | Token节省50%+ |
| waitForURL替代waitForTimeout | 避免网络波动导致的30%失败率 |
| localStorage传参 | 跨系统（DPMS + OA）数据传递 |

---

## 关联文件

- 源文件存档：`sources/references/playwright-claude-code-testing-20260424.md`
- Claude Code并行开发指南：`topics/ai-programming/claude-code-parallel-dev.md`
- Harness Engineering专题：`topics/ai-native/agent-engineering.md`
- Vibe Coding专题：`topics/ai-programming/vibe-coding/`

---

## 参考链接

- 原文：https://mp.weixin.qq.com/s/v20wKu5m0f0ivQQimwFREw
- Playwright CLI：https://playwright.dev/
- Claude Code：https://claude.ai/code
