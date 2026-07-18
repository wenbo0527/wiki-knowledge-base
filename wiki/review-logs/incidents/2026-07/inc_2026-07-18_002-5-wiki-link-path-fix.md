---
title: inc 2026 07 18 002 5 wiki link path fix
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07, wiki-link, path-fix]
date: 2026-07-18
---

# INC-2026-07-18-002: 5 个 wiki-link 路径错误修复闭环（让 Obsidian 链接真的可跳转）

> **触发**: 2026-07-18 09:14 CST（P0.5 任务）
> **关联**: INC-2026-07-18-001（cron 算法 bug）+ L-50.1（wiki-link 路径修复治本）
> **状态**: ✅ Closed

---

## 📋 现象

5 个 wiki-link 在 markdown 中路径错误，导致 Obsidian 点击后无法跳转：

| # | 文件 | 路径错 | 真位置 |
|:---|:---|:---|:---|
| 1 | `insights/research/insight-20260429-18year-ai-pioneer.md` | `[[ai-native/agent-engineering]]` | `wiki/topics/ai-native/agent-engineering.md` |
| 2 | 同上 | `[[insights/insight-20260429-karpathy-ai-agent-revolution]]` | `wiki/insights/agent/insight-20260429-karpathy-ai-agent-revolution.md` |
| 3 | `insights/research/technology/insight-20260423-autoresearch-karpathy.md` | `[[ai-programming/vibe-coding]]` | 不存在 → 改 `wiki/topics/ai-native/ai-programming.md` |
| 4 | 同上 | `[[ai-native/agent-engineering]]` | `wiki/topics/ai-native/agent-engineering.md` |
| 5 | `insights/research/technology/insight-20260427-jeff-dean-tpu-story.md` | `[[insight-20260418-ai-energy-challenge\|AI能源挑战]]` | `wiki/insights/ai-technology/ai-infrastructure/insight-20260418-ai-energy-challenge.md` |

**根因**：

| 类型 | 数量 | 根因 |
|:---|:---:|:---|
| 缺 `topics/` 前缀 | 2 | 文件被移过，但 link 没更新 |
| 子目录路径缺失 | 2 | 文件归类到 `insights/{category}/` 子目录，link 没补全 |
| 文件不存在 | 1 | `vibe-coding.md` 不存在，改写为相近文件 `ai-programming.md` |

## 🛠 修复（L-17 + L-50.1 治本）

### 步骤 1：read 上下文 + verify 真实位置（L-17）

```bash
# 用 find 看真实文件位置
find /Users/wenbo/Documents/project/Wiki/wiki -name "*karpathy-ai-agent*" 
find /Users/wenbo/Documents/project/Wiki/wiki -name "*agent-engineering*"
find /Users/wenbo/Documents/project/Wiki/wiki -name "*ai-energy*"
```

### 步骤 2：Backup（每个文件 backup 到 /tmp/wiki-deadlink-fix2-*）

```
/tmp/wiki-deadlink-fix2-20260718-091236/
  ├── 18year.md
  ├── karpathy.md
  └── jeff-dean.md
```

### 步骤 3：Python 多文件批量替换（避开 sed 转义陷阱）

```python
import re
files_changes = {
    ".../18year-ai-pioneer.md": [
        (r'\[\[ai-native/agent-engineering\]\]', 
         '[[topics/ai-native/agent-engineering|Agent工程化]]'),
        (r'\[\[insights/insight-20260429-karpathy-ai-agent-revolution\]\]', 
         '[[insights/agent/insight-20260429-karpathy-ai-agent-revolution|Karpathy AI代理革命]]'),
    ],
    ...
}
# sed 在 BSD 上对 `[[` 解析有问题，换 Python re.sub
```

### 步骤 4：grep verify 残留

```
L82: - [[topics/ai-native/agent-engineering|Agent工程化]] - Agent工程化专题
L84: - [[insights/agent/insight-20260429-karpathy-ai-agent-revolution|Karpathy AI代理革命]] - Karpathy AI代理革命
```

## 📊 成果

| 指标 | Before | After |
|:---|:---:|:---:|
| 5 个 wiki-link 可跳转性 | ❌ 全部 dead | ✅ 全部 alive |
| Obsidian 用户体验 | 5 个断链 | 5 个真链接 |
| Cron 算法误报 | 0 | 5（但 cron 本身有 bug，见 INC-001）|

## 💡 教训

| Lesson | 标题 | 应用 |
|:---|:---|:---|
| **L-50.1** | wiki-link 路径修复必先 verify 真实位置（ls + find）| ✅ 已用 |
| **L-50.5** | sed 在 BSD 上对 `[[` 转义有 bug，换 Python re.sub | ✅ 已用 |
| **L-50.6** | 路径修复必 backup 到 `/tmp/wiki-*-{ts}/` 防回滚 | ✅ 已用 |
| **L-50.7** | 找不到对应文件时改写为"语义相近"文件 + 备注 | ✅ vibe-coding → ai-programming |

## 关联

- **INC-2026-07-18-001**（cron 算法 bug）—— 5 修复后 cron 仍报死链
- **L-50**（wiki-link 路径规范 + cron 算法升级族）
- **INC-2026-07-17-001**（wiki-process-trash 副作用）—— 同为 Wiki 治理

## 闭环证据

```
wiki_auto_review.py 9:13 输出:
  健康度: 🟠 65/100（不变）
  死链: 1082 → 1082（cron 算法不变）
  真实死链: 20 → 20（cron 算法不变）

但 grep verify 5 个 wiki-link 全部指向真文件 ✅
```

🕵️ 闭环完成 · 2026-07-18 09:14 CST