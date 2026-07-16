---
title: insight 20260513 spec driven development sdd
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-coding]
date: 2026-05-23
---

# Spec-Driven Development (SDD)：AI编程时代的工程方法论革命

能力框架: capability-requirement-decision #capability-tech-understanding
标签: #SDD #Spec-Driven-Development #AI编程 #工程方法论

> **来源**: Get笔记 - AI链接笔记
> **原文标题**: Spec-Driven Development (SDD)：AI编程时代的工程方法论革命
> **评级**: ⭐⭐⭐⭐⭐ (5/5)
> **日期**: 2026-05-13
> **Tags**: #requirement-decision #tech-understanding #SDD #AI编程

---

## 一、核心定义

### 一句话定义

> **Spec-Driven Development (SDD)**：将规格说明（Specification）作为唯一真实来源（Single Source of Truth），代码作为其派生产物。

### 核心思想

**先定义WHAT（做什么），再让AI实现HOW（怎么做）**

### 时代背景

2025年多个方向同时收敛至SDD：
- **反面参照**：Karpathy的Vibe Coding暴露"不管代码只管vibes"的问题
- **工具支持**：GitHub Spec Kit、AWS Kiro、OpenSpec、阿里QoderWork

---

## 二、"5人7天"震撼实验

### 项目成果

5人团队在7天内完成传统20人数周工作量，成功上线产品**QoderWork**。

### 时间线

| 天数 | 核心任务 |
|:---|:---|
| **DAY 0** | 零代码日 - 定义边界、拆解模块、撰写Spec、汇入Repo Wiki |
| **DAY 1-2** | 架构开发，框架与容器同步推进 |
| **DAY 3-4** | Spec迭代 + AI自动生成代码并提交PR |
| **DAY 5-6** | 自举式测试（用产品测试自身） |
| **DAY 7** | 正式发布 |

### 关键洞察

> **5人能驾驭AI并行推进多任务而不失控的关键在于DAY 0制定的Spec。**

---

## 三、SDD完整流程

### 四阶段模型

```
Specify → Plan → Implement → Validate
   ↓        ↓         ↓          ↓
  人定义   人+AI     AI实现    人+AI验证
  WHAT    方案      HOW       验证
```

| 阶段 | 主导者 | 核心产出 | 关键动作 |
|:---|:---|:---|:---|
| **Specify** | 人 | spec.md | 定义问题、边界、成功标准 |
| **Plan** | 人+AI | plan.md | 架构选型、模块划分 |
| **Implement** | AI | 代码+测试 | 按plan逐任务实现 |
| **Validate** | 人+AI | 测试报告 | 自动化测试+人工Review |

### 三文件体系

| 文件 | 内容 | 作用 |
|:---|:---|:---|
| **spec.md** | 需求规格 | 唯一真实来源，回答"做什么"和"为什么做" |
| **plan.md** | 架构方案 | 基于spec生成的技术方案 |
| **tasks.md** | 任务清单 | 将plan拆解为可执行原子任务 |

### constitution.md (项目宪法)

定义不可违背的约束条件：
- API设计规范
- 安全要求
- 代码质量标准
- 基础设施约束

---

## 四、好Spec的六要素

| 要素 | 作用 | 示例 |
|:---|:---|:---|
| **Problem Statement** | 定义"为什么做" | "当前系统不支持细粒度权限控制" |
| **Success Metrics** | 定义"做到什么程度算完" | "P95 < 50ms，覆盖20+权限类型" |
| **User Stories** | 定义"谁在什么场景下用" | "作为管理员，我可以创建自定义角色" |
| **Acceptance Criteria** | 定义"怎么验证" | "单用户多角色，权限取并集" |
| **Non-Goals** | 定义"什么不做" | "本期不做跨组织权限委托" |
| **Constraints** | 定义"技术约束" | "必须兼容现有OAuth2.0流程" |

### 粒度控制标准

> "用不同技术栈实现这个Spec，Spec是否仍然有效？"

有效则为合理粒度，否则可能混入了实现细节。

---

## 五、SDD vs Vibe Coding

### "三个月墙"现象

Vibe Coding项目通常经历：
- **1-3个月**：高产出
- **4-9个月**：停滞
- **10-15个月**：崩溃

**原因**：AI上下文窗口无法容纳大型项目全貌

### 核心差异对比

| 维度 | Vibe Coding | SDD |
|:---|:---|:---|
| **核心假设** | AI能理解意图 | AI需要明确规格 |
| **启动速度** | 极快 | 较慢 |
| **可维护性** | 差 | 好 |
| **安全性** | 差（45%漏洞率） | 较好 |
| **适用规模** | <1000行 | 中大型项目 |

### 混合策略建议

| 阶段 | 方法 | 目的 |
|:---|:---|:---|
| **探索阶段** | Vibe Coding | 快速试错 |
| **决定实施后** | 补Spec固化发现 | 固化决策 |
| **正式开发** | 严格SDD | 可维护性 |

---

## 六、工具生态对比

| 工具 | 定位 | Agent支持 | 核心特点 |
|:---|:---|:---|:---|
| **Spec Kit** | Agent-agnostic框架 | 8+ | 三文件体系+constitution |
| **OpenSpec** | 轻量迭代工具 | 25+ | 轻量、快速迭代 |
| **Kiro (AWS)** | SDD-native IDE | 内置 | 完整IDE集成 |
| **QoderWork** | Quest执行引擎 | Qoder生态 | Spec+Quest并行执行 |

**选择建议**：
- 通用项目 → Spec Kit (43.7k Star)
- 轻量快速迭代 → OpenSpec
- AWS生态 → Kiro
- 并行执行效率 → QoderWork

---

## 七、实战数据

### 成功案例

| 指标 | 数据 |
|:---|:---|
| **API变更周期缩短** | 75%（金融领域） |
| **LLM代码错误减少** | 50%（人工精炼Spec后） |
| **规模化实践** | Stripe交付1,300个AI PR |

### 失败案例警示

| 问题 | 数据 |
|:---|:---|
| **AI生成代码安全漏洞** | 45%（无Spec约束时） |
| **代码重复率增长** | 4年增长4倍（GitClear） |

---

## 八、核心价值

### Microsoft评价

> **"SDD is version control for your thinking"**

SDD管理的是思考的演变历史：
- 功能决策
- 边界定义
- 成功标准

### 关键洞察

> 当代码可被AI秒级重写时，真正有价值的是代码背后的决策。

---

## 九、对文博Agent团队的启示

### 当前问题

| 问题 | 说明 |
|:---|:---|
| **缺乏规格固化** | 依赖文档和会议，缺乏工程化落地 |
| **多Agent协作混乱** | 无统一规格导致接口不一致 |

### 建议实践

1. **引入SDD流程**：Specify → Plan → Implement → Validate
2. **建立三文件体系**：spec.md / plan.md / tasks.md
3. **制定constitution.md**：定义不可违背的约束
4. **区分探索 vs 实施**：Vibe Coding探索，SDD固化

---

*🕵️ 尼克·弗瑞 | 情报分析师*
*来源: Get笔记 | 2026-05-13*
