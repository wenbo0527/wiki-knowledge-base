---
title:  agent usage guide
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs]
date: 2026-05-09
---

# 📋 Agent团队 Review Logs 使用说明

> 适用Agent: 派蒙、钟离、托尼·斯塔克、尼克·弗瑞
> 文档位置: `/Users/wenbo/Documents/project/Wiki/wiki/review-logs/`

---

## 🎯 快速开始

### 场景1: 发现问题了

```
1. 打开模板: review-logs/_template_incident.md
2. 复制并命名: inc_2026-05-07_001.md
3. 放入目录: review-logs/incidents/YYYY-MM/
4. 更新注册表: review-logs/_registry.md
5. 通知相关Agent（飞书）
```

### 场景2: 问题解决了

```
1. 更新incident状态 → Resolved
2. 移动到: review-logs/incidents/resolved/
3. 写Lesson: review-logs/lessons/by-agent/{你的名字}/
4. 更新注册表
```

---

## 📁 核心文件

| 文件 | 用途 |
|:---|:---|
| `_index.md` | 完整使用指南（详细） |
| `_template_incident.md` | Incident模板 |
| `_template_lesson.md` | Lesson模板 |
| `_registry.md` | 全局注册表（追踪所有问题） |

---

## 🔴 记录Incident

### 必须记录的情况

- 发现影响功能的问题
- 发现阻塞工作的问题
- 发现可能影响其他Agent的问题
- 花了超过30分钟解决的问题

### 如何记录

**文件命名**: `inc_YYYY-MM-DD_NNN.md`
**存放位置**: `review-logs/incidents/YYYY-MM/`

### 模板字段

```markdown
# 🔴 Incident #NNN: [简短标题]

| 字段 | 值 |
|:---|:---|
| **ID** | inc_YYYY-MM-DD_NNN |
| **严重级别** | 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low |
| **状态** | 🔄 Open |
| **发现时间** | YYYY-MM-DD HH:MM |
| **发现者** | {你的名字} |

## 问题描述
[清晰描述发生了什么]

## 影响分析
[影响范围、功能、用户]

## 已尝试的措施
| 时间 | 措施 | 结果 |
|:---|:---|:---|
| HH:MM | 描述 | ✅/❌ |

## 后续行动
- [ ] 行动项 - 负责人
```

---

## 📚 沉淀Lesson

### 值得沉淀的情况

- 问题花了超过1小时解决
- 涉及多个Agent协作
- 有可复用的经验
- 文博要求记录

### 如何记录

**文件命名**: `les_YYYY-MM-DD_NNN.md`
**存放位置**: `review-logs/lessons/by-agent/{你的名字}/`

### 模板字段

```markdown
# 📚 Lesson #NNN: [经验标题]

| 字段 | 值 |
|:---|:---|
| **ID** | les_YYYY-MM-DD_NNN |
| **关联Incident** | inc_YYYY-MM-DD_NNN（可选） |
| **沉淀时间** | YYYY-MM-DD |
| **贡献者** | {你的名字} |

## 教训总结
> [一句话核心教训]

## 问题背景
[这个问题是怎么发生的？]

## 正确做法
### ✅ 应该做的
1. ...
### ❌ 不应该做的
1. ...

## 经验复用
[下次如何避免/应用这个经验]
```

---

## ⚠️ 严重级别定义

| 级别 | 标识 | 定义 | 处理时限 |
|:---:|:---:|:---|:---|
| Critical | 🔴 | 影响核心功能、数据丢失风险 | 即时通知 |
| High | 🟠 | 影响主要功能，有workaround | 2小时 |
| Medium | 🟡 | 影响部分功能 | 24小时 |
| Low | 🟢 | 体验问题/优化建议 | 有空时 |

---

## 🔄 状态流转

```
Open → In Progress → Resolved → Closed
                    ↑
              (遇到阻塞)
                    ↓
               Blocked
```

---

## 💡 关键原则

```
✅ Blameless - 归因系统/流程，不找责任人
✅ 及时记录 - 发现即记录，不依赖记忆
✅ 闭环追踪 - 每个问题都要有结果
✅ 经验复用 - Lessons供其他Agent参考
```

---

## 📞 通知规则

| 级别 | 通知方式 |
|:---|:---|
| 🔴 Critical | 立即飞书通知 + 电话 |
| 🟠 High | 2小时内飞书通知 |
| 🟡 Medium | 当日简报包含 |
| 🟢 Low | Wiki沉淀即可 |

---

*如有问题，联系尼克·弗瑞*
*文档位置: /Users/wenbo/Documents/project/Wiki/wiki/review-logs/*
