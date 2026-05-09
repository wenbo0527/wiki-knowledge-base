# 📚 Postmortem & Lessons Learned 最佳实践参考

> 整理自: Google SRE / Pragmatic Engineer / Atlassian / incident.io
> 更新: 2026-05-07

---

## 1. 行业标准流程（8步）

```
1. 检测到故障
2. 声明 Incident
3. 缓解中（保持沟通）
4. 已缓解
5. 冷却期（24-48h，不要立即复盘）
6. 分析/复盘/根因分析
7. 评审（更大范围 review）
8. 跟踪 Action Items
```

---

## 2. Blameless 原则

### 核心思想

> **"记录问题是为了改进系统，不是找责任人"**
> **"Anyone on the team could have made the same mistake"**

### ❌ 错误做法

```
- "为什么你不这样做？"
- "这是谁的错？"
- "你应该一开始就..."
```

### ✅ 正确做法

```
- "这个问题是怎么一步步发生的？"
- "当时这样做为什么是合理的？"
- "下次如何改进系统/流程？"
```

---

## 3. 高效复盘会议指南

| 步骤 | 时长 | 内容 |
|:---|:---:|:---|
| 1. 对齐背景 | 5min | 确保大家对事实有共识 |
| 2. 时间线还原 | 10min | 按时间顺序走一遍 |
| 3. 根因分析 | 15min | 问"How"不问"Why" |
| 4. 做得好的地方 | 5min | 正面肯定 |
| 5. Action Items | 10min | 具体可执行 |
| **总计** | ~45min | |

### 注意事项

```
✅ 提前发送议程和材料
✅ 录制会议（方便缺席者回看）
✅ 实时记录，不要事后补
✅ 承认做得好的地方
❌ 不要在现场才开始分析
❌ 不要把会议开成批斗会
```

---

## 4. 5 Whys 的局限与替代

### 传统 5 Whys 的问题

```
问题: 服务器宕机
Why?  因为数据库连接池耗尽
Why?  因为查询太慢
Why?  因为没有索引
Why?  因为开发忘记加
Why?  因为...（开始找责任人）

❌ 容易变成找责任人
❌ 容易错过其他根因
```

### 何况分析法（蟋蟀大法）

```
问题: 服务器宕机

问: "这个系统当时是怎么设计的？"
  → 单点数据库，无冗余

问: "为什么当时这样设计是合理的？"
  → 因为初期用户少，成本考虑

问: "现在用户量增加了，哪些地方会出问题？"
  → 数据库、缓存、API限流...

✅ 聚焦系统脆弱性，而非个人责任
```

---

## 5. Action Items 的正确处理方式

### 传统做法（有问题）

```
❌ 生成大量 Action Items
❌ 把"学习"变成"任务管理"
❌ 任务写完就忘了
❌ 没人追踪完成情况
```

### Better Practice

```
✅ Action Items 要具体、可执行、有负责人
✅ 优先级排序（不要超过3-5个）
✅ 定期追踪（周会检查）
✅ 完成才算，完不成要说明原因
```

### Action Item 模板

```markdown
- [ ] [具体行动] - 负责人 - 截止日期
- [ ] [不要写"研究X"要写"实现X方案"]
```

---

## 6. 工具推荐

| 工具 | 用途 | 特点 |
|:---|:---|:---|
| **incident.io** | Incident管理 | 专用平台 |
| **Jeli.io** | 复盘分析 | 专注于学习 |
| **Blameless.com** | 全流程平台 | SRE专用 |
| **Notion/Obsidian** | 轻量级 | 我们正在用 |
| **Google Docs** | 协作编写 | 实时协同 |

---

## 7. 我们团队的适配

### 与业界标准对比

| 业界实践 | 我们适配 | 说明 |
|:---|:---|:---|
| Incident声明 | `incidents/`目录 | 问题发现即记录 |
| 冷却期 | 延迟写Lesson | 问题解决后再沉淀 |
| Blameless | Lessons无责归因 | 归因到系统/流程 |
| Action Items | `_registry.md` | 追踪闭环 |
| 分享学习 | `lessons/by-agent/` | 跨Agent复用 |

### 我们的特点

```
✅ 多Agent协作（尼克/钟离/派蒙/文博）
✅ 有飞书通知渠道
✅ 有Wiki知识库
✅ 有Neo4j图数据库（需求拆解）

⚠️ 需要注意：
- 冷却期要适合AI工作流（可以短一些）
- 每个Agent独立记录，但共享Lessons
- 文博是最终审核者
```

---

## 8. 常见误区

| 误区 | 真相 |
|:---|:---|
| "写完文档就学习了" | 错！文档是被阅读才能产生价值 |
| "写文档是为了归档" | 错！是为了复用和学习 |
| "聚焦在生成Action Items" | 错！聚焦在学习本身 |
| "立即开始复盘" | 错！需要冷却期 |
| "5 Whys能解决所有问题" | 错！它有局限性 |

---

## 9. 延伸阅读

| 来源 | 链接 |
|:---|:---|
| Google SRE Book | https://sre.google/sre-book/postmortem-culture/ |
| Pragmatic Engineer | blog.pragmaticengineer.com/postmortem-best-practices |
| Atlassian Handbook | atlssian.com/incident-management/handbook/postmortems |
| incident.io Blog | incident.io/blog/sre-incident-postmortem-best-practices |

---

*整理: 尼克·弗瑞 | 参考: Google SRE / Pragmatic Engineer / Atlassian*
