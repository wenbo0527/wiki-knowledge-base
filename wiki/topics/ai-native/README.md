---
title: README
author: 尼克·弗瑞 🕵️
product_domain: PD-TOPIC
doc_type: 其他
tags: [topics, ai-native]
date: 2026-04-24
---

# AI Programming（AI编程）专题

> 🕵️ 尼克·弗瑞情报整理
> 📅 最后更新：2026-04-14

---

## 专题概述

本专题聚焦于AI辅助编程的最佳实践、工作流程和工具链，涵盖Vibe Coding、Superpowers等主流AI编程方法论。

---

## 核心内容

### 1. Vibe Coding 🆕
**AI结对编程的终极工作流程**

- 📁 [专题主页](./vibe-coding/README.md)
- 📝 [开发经验](./vibe-coding/开发经验.md)
- 🏗️ [通用架构模板](./vibe-coding/通用项目架构模板.md)

**核心理念**：规划驱动 + 上下文固定 + AI协作

### 2. Superpowers Framework
**AI辅助开发工程纪律框架**

- 📁 [Superpowers工作流](./superpowers-framework.md)
- 📝 [PM实践](./superpowers-pm-practices.md)
- 🧪 [TDD Superpowers](./tdd-superpowers.md)

**核心理念**：给AI上工程纪律，从凭感觉到可流程化

### 3. Enterprise Refactoring 🆕
**企业中后台项目重构最佳实践**

- 📁 [专题主页](./enterprise-refactoring/README.md)
- 📝 [Brownfield项目重构](./enterprise-refactoring/brownfield-projects.md)
- 🏛️ [Clean Architecture](./enterprise-refactoring/clean-architecture.md)
- 🔐 [安全编码实践](./enterprise-refactoring/security-coding.md)

**核心理念**：AI作为监督下的初级工程师 + 安全边界定义 + 分层架构约束

### 4. AI代码审查工具 🆕
**AI驱动的代码审查与质量保障**

- 📝 [AI代码审查工具](./code-review-ai.md)

**核心理念**：异构AI团队协作 + 两阶段审查 + 质量门控

### 5. AI时代的TDD实践 🆕
**测试驱动开发与AI的协同模式**

- 📝 [AI-TDD实践](./tdd-ai.md)

**核心理念**：AI生成测试 + 自动验证 + 人类终审

---

## 核心概念对比

| 方法论 | 核心理念 | 适用场景 |
|--------|----------|----------|
| **Vibe Coding** | 规划驱动 + 人机协同 | 快速原型、项目开发 |
| **Superpowers** | 工程纪律 + TDD | 严谨开发、质量把控 |
| **TDD Superpowers** | 测试先行 + 持续验证 | 大型项目、复杂系统 |

---

## 工具链全景图

```
┌─────────────────────────────────────────────────────────────┐
│                        AI 编程工具体系                        │
├─────────────────────────────────────────────────────────────┤
│  IDE/编辑器                                                  │
│  ├── VSCode + Claude/Copilot扩展                            │
│  ├── Cursor                                                 │
│  └── Neovim + LazyVim                                       │
├─────────────────────────────────────────────────────────────┤
│  CLI工具                                                    │
│  ├── Claude Code                                            │
│  ├── Codex CLI                                              │
│  └── Ollama (本地模型)                                       │
├─────────────────────────────────────────────────────────────┤
│  辅助工具                                                    │
│  ├── Mermaid Chart (架构图)                                 │
│  ├── NotebookLM (文档理解)                                   │
│  └── Zread (代码阅读)                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## AI模型分级（2025-2026）

| 梯队 | 模型 | 适用场景 |
|------|------|----------|
| 第一梯队 | Claude Opus 4.5, Codex 5.1-max, GPT-5.2 | 复杂架构设计、大规模代码生成 |
| 第二梯队 | Claude Sonnet 4.5, Kimi K2, GLM-4.6 | 常规开发任务 |
| 第三梯队 | Qwen3, SWE, Grok4 | 简单任务、补全 |

---

## 实践案例

1. **Linus Torvalds项目** - Python可视化vibe coding实践
2. **2万+行代码项目** - AI深度参与的商业项目
3. **出海项目** - vibe coding + coding agent实战
4. **Superpowers工作流** - Andrej Karpathy推崇的工程纪律

---

## 关联专题

- [[topics/tech-ai]] - AI技术总览
- [[ai-native]] - AI Native软件开发
- [[product-management]] - 产品管理（专题06 VIBE CODING）

---

## 🆕 2026-05-14 新增内容

### 规格驱动开发 (SDD)
- 📝 [SDD: AI编程时代工程方法论革命](../insights/insight-20260513-spec-driven-development-sdd.md)
  > "SDD is version control for your thinking" - 当代码可被AI秒级重写时，真正有价值的是代码背后的决策

### 企业级脚手架
- 📝 [企业级AI Coding脚手架工程化落地](../insights/insight-20260514-enterprise-ai-coding-scaffold.md)
  > Landing Zone定义"应该有什么"，脚手架解决"如何低成本复制"，二者关系类似"宪法与印刷厂"

### AI后端平台
- 📝 [InsForge/Modelence AI后端平台解析](../insights/insight-20260512-ai-backend-platform-insforge-modelence.md)
  > 从面向人类开发者转向面向AI代理，标准化、语义化接口让AI生成的代码可直接在生产环境运行

### 代码知识图谱
- 📝 [RepoDoc代码知识图谱文档生成](../insights/insight-20260511-code-knowledge-graph-repo-doc.md)
  > 增量更新可减少70%以上计算资源消耗，语义增强提升文档连贯性

---

## 📊 核心Insight总结

> **"系统 > 提示词"**：
> - Harness是底座，决定可用性
> - SDD是方法论，规格驱动开发
> - Subagent是架构模式，分工优于单干
> - 记忆是持续能力，需要治理

---

## 情报来源

- [vibe-coding-cn](https://github.com/2025Emma/vibe-coding-cn) (19k+ stars)
- [Andrej Karpathy - Superpowers](https://github.com/Kimani54/superpowers)
- [Cursor-Windsurf-Mastery-Handbook](https://github.com/hamodywe/Cursor-Windsurf-Mastery-Handbook) (企业级AI开发手册)
- 知乎社区讨论

---

*🕵️ 情报分析师：尼克·弗瑞*
*最后更新：2026-05-14*

## 自主研究框架 🆕 2026-04-30

**Karpathy Autoresearch - 单GPU自动化研究实验**

- 📝 [Insight: Karpathy Autoresearch](../insights/insight-20260430-karpathy-autoresearch.md)

**核心理念**：AI Agent自主修改→训练→验证→保留/丢弃循环，5分钟/次，睡一觉跑~100次实验

---

## 相关Insights

- AI编程范式迁移：从Vibe Coding到Agentic Engineering (2026-05-12)
- Agent时代架构师核心能力框架：从工具追逐到系统沉淀 (2026-05-12)
- DeerFlow 2.0：字节跳动多智能体系统架构深度解析 (2026-05-12)
- Hermes Agent：自进化AI Agent的突破性实践 (2026-05-13)
- Spec-Driven Development (SDD)：AI编程时代的工程方法论革命 (2026-05-13)
- Subagent：AI协作体系的团队化分工革命 (2026-05-12)
- Terminus-4B：小模型在代码Agent执行任务中的颠覆性潜力研究 (2026-05-14)
- Harness工程：AI Agent可靠开发的系统方法论 (2026-05-12)

<!-- 自动关联的insights将在这里列出 -->