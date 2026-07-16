---
title: PAIMON SKILL HANDBOOK
author: 尼克·弗瑞 🕵️
product_domain: PD-CODE
doc_type: 其他
tags: [code-examples, skills]
date: 2026-04-30
---

# 📋 派蒙Skill维护工作手册

> **执行人**: 派蒙（Paimon）🤝
> **监督人**: 尼克·弗瑞 🕵️
> **生效日期**: 2026-04-30

---

## 🎯 派蒙的职责

作为Agent团队的大总管，派蒙负责**Skill日常维护的监督与协调**。

---

## 📅 日常任务

### 每周一 09:00 - 异常检查

**目的**: 发现零调用或高频失败的Skill，及时通知维护者

**执行步骤**:

```
Step 1: 读取调用日志
   路径: ~/.nickfury/logs/skill-usage.log

Step 2: 检查零调用Skill
   命令: grep "triggered=true" ~/.nickfury/logs/skill-usage.log | awk -F'skill=' '{print $2}' | awk -F' ' '{print $1}' | sort | uniq -c | sort -rn
   
Step 3: 识别异常
   - 连续7天零调用的Skill → 标记为🟡待改进
   - 调用失败率>50%的Skill → 立即通知维护者

Step 4: 生成周报
   格式: 飞书消息发送给文博
```

**周报格式**:

```
📊 Skill周报 - YYYY-MM-DD

【异常情况】
- 🟡 待改进: skill-name (连续X天零调用)
- 🔴 高频失败: skill-name (失败率XX%)

【本周调用TOP3】
1. skill-name: X次
2. skill-name: X次
3. skill-name: X次

【建议行动】
- [ ] 通知维护者优化skill-name
- [ ] 其他建议
```

---

### 每月最后周一 - 评分复审

**目的**: 评估所有Skill的四维评分，更新评分报告

**执行步骤**:

```
Step 1: 读取评分标准
   路径: Wiki/wiki/code-examples/skills/SKILL_EVALUATION.md

Step 2: 逐个Skill评估
   使用评分卡: Wiki/wiki/code-examples/skills/SKILL_SCORE_CARD.md

Step 3: 更新评分报告
   路径: Wiki/wiki/code-examples/skills/SKILL_SCORING_REPORT.md

Step 4: 识别需要优化的Skill
   - 分数<75的Skill → 列入优化计划
   - 连续3个月<60的Skill → 建议废弃/合并
```

**四维评分标准**:

| 维度 | 问题 | 权重 | 得分标准 |
|:---|:---|:---:|:---|
| **能自动化** | Skill能自动执行吗？ | 25% | 有scripts/=20-25, references/=15-19, 无=10-14 |
| **有人使用** | 最近30天调用几次？ | 25% | 每周>5次=20-25, 3-5次=15-19, 1-2次=10-14 |
| **功能独特** | 有其他Skill替代吗？ | 25% | 唯一=20-25, 主要独特=15-19, 有重叠=10-14 |
| **持续评估** | 能定期复审优化吗？ | 25% | <500行+更新=20-25, <500行=15-19, >500行=<10 |

---

### 每季度末周 - 去留决策

**目的**: 决定废弃/合并/新建哪些Skill

**执行步骤**:

```
Step 1: 汇总季度数据
   - 月度评分趋势
   - 调用频率变化
   - 维护者反馈

Step 2: 初步建议
   - 连续3个月零调用 → 建议废弃
   - 功能重复 → 建议合并
   - 缺失能力 → 建议新建

Step 3: 通知文博决策
   发送: 季度决策建议报告
```

---

## 🔧 快速参考

### Skill清单（当前14个）

| Skill | 评分 | 状态 | 维护者 |
|-------|:---:|:---:|:---|
| requirement-breakdown | 80 | 🔵优秀 | 尼克 |
| requirement-understanding | 78 | 🔵优秀 | 尼克 |
| requirement-supplement | 76 | 🔵优秀 | 尼克 |
| spec-driven | 71 | 🔵优秀 | 尼克 |
| wiki-maintenance | 75 | 🔵优秀 | 尼克 |
| agent-daily-report | 71 | 🔵良好 | 派蒙 |
| code-review | 63 | 🟡良好 | 托尼 |
| claude-code-orchestrator | 58 | 🟡待优化 | 尼克 |
| prd-generation | 55 | 🟠待优化 | 尼克 |
| neo4j-product-domain-repair | 61 | 🟡良好 | 钟离 |
| product-breakdown | 47 | 🟠待优化 | 托尼 |
| feishu-sync | 50 | 🟠待优化 | 尼克 |
| health-check | 50 | 🟠待优化 | 钟离 |
| risk-query-tester | 55 | 🟠待优化 | 钟离 |

### 废弃Skill（已归档）

| Skill | 废弃日期 | 原因 |
|-------|----------|------|
| git-workflow | 2026-04-30 | 合并到spec-driven |
| task-planning | 2026-04-30 | 合并到spec-driven |
| tony-zhongli-collaboration | 2026-04-30 | 功能被覆盖 |

### 关键路径

| 用途 | 路径 |
|:---|:---|
| 调用日志 | `~/.nickfury/logs/skill-usage.log` |
| 评分标准 | `Wiki/wiki/code-examples/skills/SKILL_EVALUATION.md` |
| 评分报告 | `Wiki/wiki/code-examples/skills/SKILL_SCORING_REPORT.md` |
| 评分卡 | `Wiki/wiki/code-examples/skills/SKILL_SCORE_CARD.md` |
| 调用统计脚本 | `~/.nickfury/scripts/skill-usage-tracker.sh` |

---

## 🚨 紧急情况处理

### 情况1: Skill执行失败率>80%

```
1. 立即通知维护者
2. 临时标记为🔴暂停使用
3. 通知文博
```

### 情况2: 发现完全重复的Skill

```
1. 记录重复的Skill列表
2. 分析哪个更优
3. 通知尼克执行合并
```

### 情况3: 文博要求紧急评估

```
1. 按四维评分标准快速评估
2. 24小时内输出评估报告
3. 建议保留/合并/废弃
```

---

## 📊 报告模板

### 周报模板（飞书发送）

```
📊 Skill周报 - {日期}

【异常情况】
- 🟡 待改进: {skill-name} (连续X天零调用)
- 🔴 高频失败: {skill-name} (失败率XX%)

【本周调用TOP3】
1. {skill-name}: X次
2. {skill-name}: X次
3. {skill-name}: X次

【本周完成】
- [ ] 异常检查完成
- [ ] 其他任务

【下周计划】
- [ ] 月度复审（如果是月末周）
- [ ] 其他计划
```

### 月报模板（飞书发送）

```
📊 Skill月报 - {月份}

【本月评估】
- 总Skill数: X个
- 🟢卓越: X个
- 🔵优秀: X个
- 🟡良好: X个
- 🟠待改进: X个
- 🔴暂停: X个

【优化完成】
- [ ] 优化项1
- [ ] 优化项2

【下月计划】
- [ ] 计划项1
- [ ] 计划项2
```

---

## ✅ 派蒙检查清单

### 每周一

- [ ] 读取调用日志
- [ ] 检查零调用Skill
- [ ] 检查高频失败Skill
- [ ] 发送周报给文博

### 每月最后周一

- [ ] 执行四维评分复审
- [ ] 更新评分报告
- [ ] 识别待优化Skill
- [ ] 发送月报给文博

### 每季度末周

- [ ] 汇总季度数据
- [ ] 制定去留建议
- [ ] 通知文博决策

---

*派蒙任务手册 v1.0*
*创建: 2026-04-30*
*下次更新: 2026-05-26*
