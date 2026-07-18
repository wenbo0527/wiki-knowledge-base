---
title: inc 2026 07 18 007 batch insight subdir fix 685
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07, deadlink-fix, batch, largest]
date: 2026-07-18
---

# INC-2026-07-18-007: B 任务 · 批量补 insight-YYYYMMDD 子目录（685 处 · 最大单批修复）

> **触发**: 2026-07-18 16:37 CST（A 完成后立即启动）
> **关联**: INC-2026-07-18-006 + L-50.4 + L-50.8
> **状态**: ✅ Closed（685 处替换 across 229 files · 总死链 692→351 = -49.3%）

---

## 📋 现象

v3 算法揭穿 703 死链中，`insight-YYYYMMDD-*` 类 289 处（占 41.7%），全是**缺子目录前缀**。

## 🔍 死链模式

| 模式 | 数量 | 缺什么 |
|:---|:---:|:---|
| `insight-20260417-harness-engineering` | 18 | `insights/ai-technology/agent-engineering/` |
| `insight-20260418-digital-employee-industry` | 12 | `insights/ai-technology/agent-engineering/` |
| `insight-20260419-harness-engineering` | 12 | `insights/agent/` |
| ... 121 个独立 link | ... | ... |

**可批量改写：119 个（找到真位置）**

## 🛠 修复（L-50.4 治本 · 全自动批处理）

### 算法：filename → 真位置映射

```python
# 1. 构建 filename → 真路径映射（保留路径最深的）
filename_to_path = {}
for p in all_pages:
    base = basename(p)[:-3]  # 去 .md
    if base not in filename_to_path or rel.count('/') > filename_to_path[base].count('/'):
        filename_to_path[base] = rel

# 2. 收集所有死链
dead_to_real = {}
for path in all_pages:
    for match in re.findall(r'\[\[([^\]]+)\]\]', content):
        link = match.split('|')[0].strip()
        if is_dead(link) and link in filename_to_path:
            real = filename_to_path[link][:-3]  # 去 .md
            dead_to_real[link] = real

# 3. 批量替换
for dead, real in dead_to_real.items():
    pattern = r'\[\[' + re.escape(dead) + r'(\|[^\]]*)?\]\]'
    content = re.sub(pattern, lambda m: f'[[{real}{m.group(1) or ""}]]', content)
```

## 📊 成果

| 指标 | Before B | After B | 变化 |
|:---|:---:|:---:|:---:|
| **总死链** | **692** | **351** | **-341 (-49.3%)** |
| insight- 类 | 289 | 1 | **-288** |
| 健康度 | 🟠 65/100 | 🟠 65/100 | label 公式 bug |

**累计修复（A+B）**：703 → 351 = **-352 (-50.1%)**

## 🆕 剩余 351 死链分类（前 10）

| 来源 | 死链 | 性质 |
|:---|:---|:---|
| us-china-tech-stocks | `Investment/China-A-Share` | 无目标文件 |
| us-china-tech-stocks | `Tech-Industry/AI-Investment` | 无目标文件 |
| free-energy-principle | `Concepts/Bayesian-Thinking` | 无目标文件 |
| adele-ai-performance × 2 | `AI Native/AI-Evaluation` + `Concepts/AI-System-Reliability` | 无目标 |
| vibe-analyzing-asktable | `Fintech/Data Analysis` | 无目标 |
| lsdm × 2 | 同 adele | 无目标 |
| power-book-workplace | `Concepts/Free-Energy-Principle` | 无目标 |
| gravitino-metadata-lake | `Concepts/Data-Governance` | 无目标 |

**剩余全是"无对应文件"型**（概念没独立页面 / 散在 insight 里）

## 💡 教训

| Lesson | 标题 | 应用 |
|:---|:---|:---|
| **L-50.9** 🆕 | 批量死链修复必构建"filename → 真路径"映射，避免手动查 121 个 link | ✅ 已用 |
| **L-50.10** 🆕 | `dead_to_real` 字典 = dead link → 真相对路径（含子目录）| ✅ 已用 |
| **L-50.11** 🆕 | 批量替换前必须 backup 到独立目录（保留时间戳）| ✅ 已用 |
| **L-50.4** | 真死链 = 路径错位 + 引用方修改（批量可改）| ✅ 已用 |
| **L-50.8** | wiki-link regex 必允许可选别名 | ✅ 已用 |

## 备份

`/tmp/wiki-insight-subdir-fix-20260718-163710/` （含 229 个 backup 文件）

## 关联

- **INC-2026-07-18-006**（A 任务 AI Native/ 13 处）
- **INC-2026-07-18-005**（P1.5-2 9 真死链）
- **INC-2026-07-18-004**（P1.5 算法升级 v1→v2→v3）
- **L-50** 族系（cron 算法 + wiki-link 路径修复）

## 自我归因

这次 B 任务的"filename → 真路径映射"思路是关键——121 个独立 link 不用手动查每个，按文件名自动匹配真位置。这是 L-17 + L-50.4 的实践升级。

🕵️ 闭环完成 · 2026-07-18 16:38 CST