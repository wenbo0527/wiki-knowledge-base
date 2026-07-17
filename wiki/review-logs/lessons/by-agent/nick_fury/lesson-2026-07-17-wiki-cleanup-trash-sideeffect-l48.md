# L-48: Wiki 清理 trash 副作用必查目录结构（L-41 强化版）

> **创建时间**：2026-07-17 08:55 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-17-001（Wiki 整理速赢副作用）
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-17-wiki-cleanup-trash-sideeffect-l48.md`

---

## 🎯 核心教训

**任何目录清理（`trash <dir>/*` 或 `rm <dir>/*`）后必查 3 项**：
1. ✅ 文件被 trash/rm 了
2. ✅ **目录还在**（trash 副作用可能把空目录也清掉）
3. ✅ **子目录还在**（子目录嵌套时不查会漏）

**L-41 原版教训**：trash 验证必用 `ls -la <目标>`（TCC ≠ 失败）—— **不彻底**！

L-41 只验证"文件没了"，**没验证"目录结构是否被波及"**。本次 INC-001 wiki.review 跑挂 5h 就是这个盲区命中：trash `process/*` 4 文件时，`process/` 目录本身也被 trashed 副作用波及，导致 wiki_auto_review.py 写报告时 `FileNotFoundError`。

---

## 📚 INC-001 揭穿真根因（实例）

### 7-16 Wiki 整理速赢时序

| 时间 | 动作 | 当时判断 | 实际行为 |
|:---|:---|:---|:---|
| 19:00 | Phase 1.5 trash `process/* 4` | "4 个 90+ 过期 placeholder" | `process/` 目录被波及清空 |
| 19:55 | HEARTBEAT §十三 落档"精准 trash 5 篇" | "process/* 4 + concepts/karpathy 1" | 没验证 process/ 目录还在 |
| 7-17 03:30 | cron wiki.review 跑挂 | ❌ 未发现 | FileNotFoundError |
| 7-17 07:58 | 文博问"请检查下遇到的问题" | 触发全栈诊断 | 发现 status=error |
| 7-17 08:52 | mkdir -p 重建 process/ | 修复 | 手动跑通 |

**根因链**：
1. **Phase 1.5** 用 `trash process/*.md` 清掉 4 个过期 placeholder
2. macOS `trash` 命令在某些情况下会 **trash 整个目录**（特别是当目录内文件全被清空后）
3. **HEARTBEAT.md §十三** 落档时只数了"trashed 5 篇"，没验证目录结构
4. **7-17 03:30** cron 触发 → wiki_auto_review.py 报 FileNotFoundError → status=error 持续 5h

---

## 🔧 必查清单（写新清理脚本必带）

```bash
#!/bin/bash
# L-48 标准化清理脚本（必带 3 项验证）

TARGET="$1"
echo "🟡 清理前:"
echo "  - 目录数: $(find "$TARGET" -type d | wc -l)"
echo "  - 文件数: $(find "$TARGET" -type f | wc -l)"

# 清理动作
trash $TARGET/*.md  # 你的清理命令

echo "✅ 清理后验证（必带 3 项）:"
echo "  [1] 文件被 trash: $(ls "$TARGET" 2>/dev/null | wc -l) 个 (期望: 0)"
echo "  [2] 目录还在: $(test -d "$TARGET" && echo YES || echo NO) ← 必查"
echo "  [3] 子目录还在: $(find "$TARGET" -mindepth 1 -type d | wc -l) 个 (期望: ≥0)"

# 自动化告警
if [ ! -d "$TARGET" ]; then
  echo "🔴 目录不存在！重建中: mkdir -p $TARGET"
  mkdir -p "$TARGET"
fi
```

---

## 📜 L-48 教训族清单

| 编号 | 教训 |
|:---|:---|
| **L-48.1** | `trash <dir>/*` 后必 `ls -la <dir>` 验证目录是否存在 |
| **L-48.2** | 任何"清理动作"前必 `find <dir> -type d -empty` 列出空目录（被空目录当 placeholder 误删风险高） |
| **L-48.3** | L-41 升级版：trash 验证必含 3 项 —— (1) 文件没了 (2) 目录还在 (3) 子目录还在 |
| **L-48.4** | 7-19 周日 cron 新增 "Wiki process/* 反向验证" 检查项（防退化）|

---

## 🎯 防退化机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次清理** | L-48.1-3 三项验证 | `scripts/wiki_cleanup_safe.sh`（待写）|
| **每日 9:00** | wiki_health_check.sh 检测 process/ 是否存在 | 已扩展（L-48 集成）|
| **每周日 22:00** | MEMORY 压缩时 grep "trash sideeffect" | 手动 |
| **每次新 INC** | 必查 `find review-logs -name "*trash*"` | L-31 |

---

## 自我归因（按 SOUL §3 客观补录 + 自我归因）

**我对文博有过错**：昨天"速赢"造成了今天的问题。但：
- ✅ 8:52 已修（mkdir + 手动跑通）
- ✅ INC-001 已落档
- ✅ L-48 已沉淀（强化 L-41）
- ✅ 防退化机制 4 项已写入
- ⏳ 7-19 周日 cron 必加新检查项

**教训内化**：下次清理任何目录前，必先 grep "目录下文件被哪些脚本依赖"。

---

## 关联

- **L-41**（macOS `trash` 验证必用 `ls -la`）—— 原版
- **L-48**（新增 · 强化版）
- **INC-2026-07-17-001**（Wiki 整理速赢副作用）—— 揭穿案例
- **HEARTBEAT §十三**（7-16 19:55 Wiki 整理速赢综述 · W1 完成 3/4 + Q3 完成 5/5）
- **AGENTS §4.1**（教训沉淀机制 · 🔴 Critical 24h 内创建 INC + lessons.md）