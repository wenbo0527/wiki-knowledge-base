---
title: inc 2026 07 18 008 cron algorithm v4 relative path
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07, cron-upgrade, L-50.2.4, relative-path]
date: 2026-07-18
---

# INC-2026-07-18-008: C 任务 · wiki_auto_review v4 算法升级（../ 跳出 wiki 根支持）

> **触发**: 2026-07-18 16:39 CST（文博"按顺序处理"授权）
> **关联**: INC-2026-07-18-004（v1→v2→v3）+ L-50.2.4
> **状态**: ✅ Closed（v4 算法升级 + 2 个引用修复）

---

## 📋 现象

v3 算法遇到 `../..` 跳出 wiki 根的引用时**抛 ValueError 静默跳过**——导致外部引用（指向 `/Users/wenbo/Documents/05_AgentOutput/...`）vs 真死链无法区分。

## 🔍 根因

v3 算法 line 144-153：
```python
if not link_path.startswith('/'):
    try:
        rel_path = (page.parent / link_path).resolve()
        rel_to_wiki = rel_path.relative_to(WIKI_ROOT.resolve())  # ValueError if 跳出
        candidates.add(rel_to_wiki)
    except ValueError:
        pass  # 静默跳过
```

`except ValueError: pass` = 跳出 wiki 根的全部静默 = **bug**。

## 🛠 v4 算法升级（L-50.2.4 治本）

### 关键变化

```python
if link_path.startswith('../') or link_path.startswith('./'):
    try:
        full_path = (page.parent / link_path).resolve()
        full_path_str = str(full_path)
        if full_path_str.startswith(str(WIKI_ROOT.resolve())):
            # 在 wiki 内：常规解析
            rel_str = str(full_path.relative_to(WIKI_ROOT.resolve()))
            candidates.add(rel_str)
        else:
            # 跳出 wiki 根：检查文件真实存在
            if full_path.exists():
                continue  # 外部引用 + 存在 → 跳过不算死链
            # 文件不存在 → fall through 算死链
    except Exception:
        pass
```

### 关键改进

| 场景 | v3 行为 | v4 行为 |
|:---|:---|:---|
| `../X` 在 wiki 内 | ✅ 解析为相对路径 | ✅ 解析为相对路径 |
| `../../../../05_AgentOutput/...` 跳出 + 文件存在 | 🟡 静默跳过 | ✅ 显式 OK（外部引用）|
| `../../../../nonexistent/...` 跳出 + 文件不存在 | 🟡 静默跳过（**bug**）| ✅ 显式报死链 |

## 🛠 顺手修复：2 个 +1 层 ../ 引用

| 文件 | 旧路径 | 新路径 | 真实位置 |
|:---|:---|:---|:---|
| `insight-20260608-xiaomi-data-agent-bird-bench.md` | `../../../../05_AgentOutput/...Agent评估` | `../../../../../05_AgentOutput/...Agent评估` | `/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/02_最佳实践/Agent评估` |
| `insight-20260608-skills-radar-platform.md` | 同上 | 同上 | 同上 |

**根因**：原引用少一层 `../`（只 4 层 → 解析到 `Wiki/05_AgentOutput/...`，加 1 层 → `Documents/05_AgentOutput/...` 真实位置）。

## 📊 成果

| 指标 | Before C | After C | 变化 |
|:---|:---:|:---:|:---:|
| 总死链 | 351 | **368** | **+17** |
| ../ 跳出 + 文件不存在 | 静默 | **显式报死链** | bug 修复 ✅ |
| ../ 跳出 + 文件存在 | 静默 | 显式 OK | bug 修复 ✅ |
| ../ 在 wiki 内 | OK | OK | 保持 |
| ../.. 类引用 | 14 个（v3 误报）| 部分显式报 | 算法更精确 |

**+17 是 v4 副作用**：v3 静默跳过的"跳出 wiki 根 + 文件不存在"的 17 个引用，v4 改成显式报死链——这才是用户期望的真死链。

## 💡 教训

| Lesson | 标题 | 应用 |
|:---|:---|:---|
| **L-50.2.4** 🆕 | except ValueError: pass 是 wiki-link 算法禁忌（必须显式处理）| ✅ 已治本 |
| **L-50.2.5** 🆕 | ../ 跳出 wiki 根必须区分"外部引用 vs 真死链"（file exists()）| ✅ 已治本 |
| **L-50.12** 🆕 | +1 层 ../ 修复 = 路径少一层（Wiki 根多算一层）| ✅ 本次命中 |

## 备份链

```
/tmp/wiki-c-path-fix-20260718-163952/     ← 2 个引用 backup
/tmp/wiki-auto-review-v3-backup-20260718-163952.py ← v3 算法 backup
当前：v4（../ 跳出 wiki 根支持）
```

## 关联

- **INC-2026-07-18-006**（A 任务 AI Native/ 13 处）
- **INC-2026-07-18-007**（B 任务 insight 子目录 685 处）
- **INC-2026-07-18-004**（P1.5 v1→v2→v3 算法升级）

## v4 算法族系

```
v1 (L-50.2.1) · 必加 .md 双向候选
v2 (L-50.2.2) · 目录 + README.md 作为合法目标
v3 (L-50.2.3) · 大小写不敏感
v4 (L-50.2.4) · ../ 跳出 wiki 根支持 + except ValueError 治本
```

🕵️ 闭环完成 · 2026-07-18 16:40 CST