---
title: agile project management guide
author: 尼克·弗瑞 🕵️
product_domain: PD-SOURCE
doc_type: 其他
tags: [sources]
date: 2026-04-28
---

# 📋 敏捷项目管理知识库

> **整理者**: 尼克·弗瑞
> **日期**: 2026-04-28
> **用途**: 托尼·斯塔克参考 / 产品管理知识体系构建
> **标签**: #敏捷 #Scrum #Kanban #项目管理 #方法论

---

## 📌 核心概念

### 敏捷宣言（2001年）

| 价值 | 相对 |
|------|------|
| **个体与互动** > 流程与工具 | 但不意味后者无价值 |
| **可工作软件** > 详尽文档 | 但不意味无文档 |
| **客户合作** > 合同谈判 | 但不意味无合同 |
| **响应变化** > 遵循计划 | 但不意味无计划 |

### 12条原则

1. 尽早且持续交付有价值的软件
2. 欢迎需求变化，即使在开发后期
3. 频繁交付可工作软件（周为单位）
4. 业务人员与开发者每日合作
5. 以激励的人为核心，建立信任
6. 面对面沟通是最有效的
7. 可工作软件是进度的主要衡量
8. 保持可持续的开发速度
9. 追求技术卓越和设计改进
10. **简洁**：减少不必要的work
11. 自组织团队产生最好的设计
12. 定期反思并调整行为

---

## 🏗️ 敏捷框架体系

### 一、Scrum框架

#### 核心角色

| 角色 | 职责 | 团队规模 |
|------|------|----------|
| **Product Owner** | 价值最大化、待办列表管理 | 1人 |
| **Scrum Master** | 流程保障、障碍移除 | 1人 |
| **开发团队** | 交付可工作软件 | 3-9人 |

#### 核心活动

| 活动 | 时长 | 参与者 | 目的 |
|------|------|--------|------|
| **Sprint Planning** | 2-8h | 全团队 | 确定Sprint目标 |
| **Daily Standup** | 15min | 全团队 | 同步进展、识别障碍 |
| **Sprint Review** | 1-4h | 全团队+利益相关者 | 演示可工作软件 |
| **Sprint Retrospective** | 1.5-3h | 全团队 | 过程改进 |

#### Sprint生命周期

```
Backlog → Sprint Planning → Sprint Backlog → Daily Standup → Increment → Review → Retrospective
                    ↑                                                      ↓
                    ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

#### 工件

| 工件 | 说明 |
|------|------|
| **Product Backlog** | 产品的所有需求列表 |
| **Sprint Backlog** | 当前Sprint要完成的工作 |
| **Increment** | Sprint期间完成的可交付物 |

---

### 二、Kanban方法

#### 核心原则

1. **可视化工作流**
2. **限制在制品（WIP）**
3. **管理流动**
4. **明确流程策略**
5. **反馈循环**
6. **协作改进**

#### 看板可视化

```
| 待办 (To Do) | 进行中 (In Progress) | 测试 (Testing) | 完成 (Done) |
|-------------|---------------------|----------------|-------------|
|    [任务A]   |       [任务D]        |    [任务G]     |   [任务J]   |
|    [任务B]   |       [任务E]        |                |   [任务K]   |
|    [任务C]   |       [任务F]        |                |   [任务L]   |
|   WIP: ∞    |      WIP: 3         |    WIP: 2      |   WIP: ∞   |
```

#### WIP限制计算

```
最佳WIP = (单个工作项平均时间 / 交付周期) × 团队成员数
或者：WIP = 团队成员数 + 1 到 2 × 团队成员数
```

---

### 三、SAFe（Scaled Agile Framework）

#### 层级结构

```
Portfolio (投资组合)
    ↓
Large Solution (大型解决方案)
    ↓
Essential SAFe (核心SAFe)
    ↓
Team Agile (团队敏捷)
```

#### 关键实践

| 层级 | 关键活动 |
|------|----------|
| **Portfolio** | 战略主题、Epic投资 |
| **Large Solution** | Solution Train、Architectural Runway |
| **Essential** | PI Planning、ART Sync |
| **Team** | Sprint、Continuous Delivery Pipeline |

---

### 四、LeSS（Large-Scale Scrum）

- **LeSS规则**：一个产品、一个Product Backlog、一个Product Owner
- **多团队协调**：Overall Retrospective、讨厌的会议要减少
- **适用场景**：10-1000人的产品开发

---

### 五、XP（极限编程）

#### 核心实践

| 实践 | 说明 |
|------|------|
| **结对编程** | 两人共同编写代码 |
| **TDD** | 测试先行 |
| **持续集成** | 频繁集成代码 |
| **重构** | 持续改进代码质量 |
| **简单设计** | 只做当前需要 |
| **代码共享** | 团队成员可修改任何代码 |
| **每周40小时** | 保持可持续速度 |
| **现场客户** | 业务人员深度参与 |

---

## 📊 敏捷估算与计划

### 一、故事点估算

#### 斐波那契数列

```
1, 2, 3, 5, 8, 13, 21, 34, 55...
```

#### 估算方法

| 方法 | 说明 | 适用场景 |
|------|------|----------|
| **规划扑克** | 团队讨论+卡片投票 | 大型团队 |
| **T-Shirt尺寸** | XS/S/M/L/XL | 粗略估算 |
| **理想人天** | 纯开发时间 | 小团队 |
| **对比法** | 与已知故事对比 | 任何场景 |

#### 速率计算

```
Sprint速率 = 该Sprint完成的故事点总和
预测 = 平均速率 × 安全系数(0.7-0.8)
```

---

### 二、用户故事

#### 格式

```
作为 [角色]
我想要 [功能]
以便 [收益/价值]
```

#### INVEST原则

| 字母 | 含义 | 说明 |
|------|------|------|
| **I** | Independent | 独立的 |
| **N** | Negotiable | 可协商的 |
| **V** | Valuable | 有价值的 |
| **E** | Estimable | 可估算的 |
| **S** | Small | 足够小的 |
| **T** | Testable | 可测试的 |

---

### 三、DoD（完成定义）

#### Sprint完成标准

```
☐ 代码实现完成
☐ 单元测试通过
☐ 代码审查通过
☐ 功能测试通过
☐ 集成测试通过
☐ 文档更新
☐ 产品负责人验收
```

---

### 四、Sprint计划

#### 输入

1. Product Backlog
2. Sprint目标
3. 团队速率历史
4. 团队容量

#### 输出

1. Sprint Goal
2. Sprint Backlog
3. 团队承诺

---

## 🛠️ 敏捷工具与平台

### 一、开源工具

| 工具 | Stars | 定位 | 特点 |
|------|-------|------|------|
| **planka** | 11,906 | Kanban | 开源Trello替代 |
| **leantime** | 9,595 | 项目管理 | 目标导向、ADHD友好 |
| **kanboard** | 9,565 | Kanban | 简单、极简 |
| **plane** | 48,479 | 全功能 | Jira替代 |

### 二、敏捷辅助工具

| 工具 | Stars | 用途 |
|------|-------|------|
| **git-standup** | 7,826 | 团队日报 |
| **poker_planning** | 2 | 估算扑克 |

---

## 🎯 敏捷与OKR结合

### OKR基本概念

| 概念 | 说明 |
|------|------|
| **Objective** | 定性的目标，鼓舞人心 |
| **Key Results** | 定量的结果，可衡量 |
| **周期** | 通常季度 |

### OKR示例

```
O: 成为行业领先的SaaS产品
KR1: NPS评分达到60+
KR2: 客户留存率达到95%
KR3: 新增企业客户100家
```

### 敏捷+OKR对齐

```
年度OKR
    ↓
季度OKR
    ↓
PI Objectives (SAFe)
    ↓
Sprint Goals (Scrum)
    ↓
具体任务 (Backlog)
```

---

## 🤖 AI与敏捷结合

### BMAD方法论

**BMAD = Breakthrough Method for Agile AI Driven Development**

```
⭐ 45,864 Stars | JavaScript
核心: AI驱动的敏捷开发方法
```

#### 核心特点

1. **AI原生的敏捷流程**
2. **自动检测与记忆集成**
3. **PRD → Architecture → Code的完整流程**
4. **Slash commands**

#### AI在敏捷中的应用

| 场景 | AI应用 |
|------|--------|
| **Backlog排序** | AI辅助优先级决策 |
| **估算辅助** | AI预测工作量 |
| **代码审查** | AI自动审查 |
| **Retrospective分析** | AI识别模式 |
| **任务分配** | AI优化分配 |

---

## 📝 敏捷实践检查清单

### Sprint开始前

- [ ] Sprint Goal明确
- [ ] Backlog已细化（INVEST）
- [ ] 估算已完成
- [ ] 团队容量已确认
- [ ] DoD已定义

### Sprint期间

- [ ] Daily Standup每日进行
- [ ] 阻塞问题及时升级
- [ ] Sprint Burndown更新
- [ ] 新需求不进入当前Sprint

### Sprint结束时

- [ ] 可工作软件已交付
- [ ] Sprint Review已举行
- [ ] 利益相关者反馈已收集
- [ ] Retrospective已举行
- [ ] 改进措施已定义

---

## 📚 参考资源

### GitHub高Stars项目

| 项目 | Stars | 链接 |
|------|-------|------|
| **BMAD-METHOD** | 45,864 | https://github.com/bmad-code-org/BMAD-METHOD |
| **plane** | 48,479 | https://github.com/makeplane/plane |
| **planka** | 11,906 | https://github.com/plankanban/planka |
| **leantime** | 9,595 | https://github.com/Leantime/leantime |
| **kanboard** | 9,565 | https://github.com/kanboard/kanboard |
| **awesome-okr** | 1,763 | https://github.com/domenicosolazzo/awesome-okr |

### 推荐阅读

1. 《Scrum敏捷项目管理》- Mike Cohn
2. 《用户故事地图》- Jeff Patton
3. 《持续交付》- Jez Humble
4. 《敏捷宣言》官网 - agiledatal.org
5. 《SAFe官网》- scaledagileframework.com

---

## 🔄 持续改进循环

```
Plan → Do → Check → Act (PDCA)
  ↑                        ↓
  ←←←←←←←←←←←←←←←←←←←←←←
```

### Retrospective常用方法

| 方法 | 适用场景 |
|------|----------|
| **Start/Stop/Continue** | 通用 |
| **Mad/Sad/Glad** | 情感分析 |
| **4个L** | Loved, Learned, Lacked, Longed For |
| ** Sailboat** | 风力/锚/岩石 |
| **Hot Air Balloon** | 上升力/下降力/障碍 |

---

## ⚠️ 常见敏捷反模式

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| **Scrumfall** | 形式上敏捷，实际瀑布 | 真正拥抱变化 |
| **Sprint过大** | 计划不准确 | 缩短Sprint |
| **WIP无限制** | 上下文切换 | 设置WIP限制 |
| **无障碍会议** | 信息不对称 | SM干预 |
| **Sprint取消** | 计划失败 | 改进计划过程 |
| **团队过载** | 质量下降 | 限制在制品 |

---

*整理自 GitHub 搜索 + 敏捷最佳实践*
*最后更新：2026-04-28*
*整理者：尼克·弗瑞*
