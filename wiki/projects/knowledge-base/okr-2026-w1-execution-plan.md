# Wiki 整理 W1 速赢执行计划（Phase 1）

> 关联 OKR：`okr-2026-h2-q3.md` 的 W1 速赢（候选 4）
> 实施者：尼克·弗瑞 🕵️
> 启动时间：2026-07-16 07:10 CST
> 截止时间：2026-07-30

---

## 🎯 Phase 1 总目标

按 **AGENTS §0.5 + L-31（防写错路径）** 教训：
1. **每个动作都可逆**（trash 兜底 + diff 校验）
2. **每步 grep 验证**（不只是 echo）
3. **完成后立刻更新 `_nick_registry.md`**（路径防真空）

---

## 📋 任务清单（按 L-15 端到端验证顺序）

### Phase 1.1: 删空目录残留 🔵 最安全

```bash
TARGET="/Users/wenbo/Documents/project/Wiki/wiki/review-logs/incidents/{2026-05}"
ls -la "$TARGET" 2>/dev/null && \
  find "$TARGET" -mindepth 1 && \
  echo "⚠️ 非空，不删" || \
  rmdir "$TARGET" 2>/dev/null && echo "✅ 已删"
```

| 验收 | `find review-logs/incidents -empty` 返回空 |
|:---|:---|

### Phase 1.2: 合并 `lessons/by-agent/nick/` → `nick_fury/` 🔵 低风险

```bash
SRC=/Users/wenbo/Documents/project/Wiki/wiki/review-logs/lessons/by-agent/nick
DST=/Users/wenbo/Documents/project/Wiki/wiki/review-logs/lessons/by-agent/nick_fury

# 1. diff 两边
diff <(ls "$SRC") <(ls "$DST")

# 2. 移动不重不漏
for f in "$SRC"/*; do
  bn=$(basename "$f")
  [ ! -f "$DST/$bn" ] && mv "$f" "$DST/" || echo "⚠️ 重复：$bn"
done

# 3. 删源空目录
rmdir "$SRC" 2>/dev/null

# 4. 验证
ls /Users/wenbo/Documents/project/Wiki/wiki/review-logs/lessons/by-agent/ | grep -v nick_fury
```

| 验收 | `nick/` 目录消失，文件全部并入 `nick_fury/` |
|:---|:---|

### Phase 1.3: 合并 `methodologies-v2/` → `methodologies/` 🟡 需 diff

```bash
# 先 diff 内容决定合并策略（可能重命名/补全，不直接覆盖）
diff -rq /Users/wenbo/Documents/project/Wiki/wiki/methodologies \
        /Users/wenbo/Documents/project/Wiki/wiki/methodologies-v2
```

| 验收 | `methodologies/` 包含 v2 内容，v2 目录消失 |
|:---|:---|

### Phase 1.4: 处置 `_archive/empty-files-cleanup-20260604/` 🟡 待判定

```bash
ls -la /Users/wenbo/Documents/project/Wiki/wiki/_archive/empty-files-cleanup-20260604/
```

可能动作：保留 / 整合进 `_archive/INDEX.md` / 整体归档到 `review-logs/archives/`。

### Phase 1.5: 清理 39 篇过期/空文 🟠 trash 风险（可恢复 30 天）

```bash
# 1. 列出 27 篇空文
find /Users/wenbo/Documents/project/Wiki/wiki -name "*.md" -type f -size 0

# 2. 列出 12 篇过期
find /Users/wenbo/Documents/project/Wiki/wiki -name "*.md" -type f -mtime +90

# 3. 全部 trash（macOS 内置 trash 命令不存在则降级到 `mv .Trash`）
which trash && trash <files> || mv <files> ~/.Trash/
```

| 验收 | `find ... \( -size 0 -o -mtime +90 \)` 返回 0 篇 |
|:---|:---|

### Phase 1.6: 更新 `_nick_registry.md` 🔵 纯文本

路径：`Wiki/review-logs/lessons/by-agent/nick_fury/_nick_registry.md`

记录本次 Phase 1 全部动作（含删除/移动清单 → trash 引用）。

### Phase 1.7: 8 个一级主题目录建 `index.md` 🟡 内容创作

| 主题目录 | 内容 |
|:---|:---|
| `insights/` | 878 篇 — 子分类清单 + 关键洞察 5 篇 |
| `concepts/` | 概念库索引 |
| `topics/` | 主题分类入口 |
| `projects/` | 项目追踪板（含 `knowledge-base/` 子目录 OKR）|
| `skills/` | Skill 工作流索引 |
| `tools/` | 工具使用手册 |
| `sources/` | 数据源汇总 |
| `standards/` | 规范/模板库 |

---

## 🚨 防错清单（L-15 / L-16 / L-17 / L-31 应用）

| # | 教训 | 应用 |
|:---:|:---|:---|
| L-15 | 24h 内不验证不能上线 | Phase 1.5 trash 后 24h 内 grep 验证文件是否真不存在 |
| L-16 | 修一类必 grep 全集 | 合并后 grep `lessons/by-agent/` 看有无遗漏 agent 目录 |
| L-17 | 写脚本前必 read 3 行 | Phase 1.3 合并前必 diff 两目录内容 |
| L-31 | 路径错误=等于没写 | 严格按 `AGENTS §0.5` 路径 |
| L-37 | 报告必调实时 API | Phase 1 完成后**重新 `find` 实测** 文档数 |

---

## ⏱ 时间预估

| 任务 | 预估 |
|:---|:---:|
| 1.1 删空目录 | 5 min |
| 1.2 nick 合并 | 10 min |
| 1.3 methodologies 合并 | 15 min（含 diff）|
| 1.4 _archive 处置 | 5 min |
| 1.5 39 篇 trash | 15 min |
| 1.6 registry 更新 | 5 min |
| 1.7 8 个 index.md | 30 min |
| **总计** | **~1.5h** |

---

## 📌 完成后必做

1. ✅ `find Wiki/wiki -name "*.md" | wc -l` → 期望 ≤ 1671 - 39 = **1632**
2. ✅ `find Wiki/wiki -type d -empty` → 期望 0
3. ✅ `find Wiki/wiki/review-logs/lessons/by-agent -mindepth 1 -maxdepth 1 -type d` → 期望无 `nick` 重复
4. ✅ 更新 `_nick_registry.md`
5. ✅ 飞书回执：已完成清单 + 仍需文博决策的项

---

*版本: v1.0*
*制定时间: 2026-07-16 07:10 CST*
*🕵️ 尼克·弗瑞 - 神盾局局长*
