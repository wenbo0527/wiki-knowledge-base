# Lesson L-24 / L-25 / L-26 / L-27 · 2026-07-03

> 沉淀自 INC-2026-07-03-002（科技日报 RSS 5 篇精选 9 天真空）

## L-24: 唯一脚本不唯一

**教训**：听到产品名必须 `grep "🎯 目的"` + 看 `cwd` + 看历史日志，确认实际跑的是哪个版本。

**踩坑**：
- `daily_pipeline.py` 在两个目录（`scripts/` 和 `skills/rss-intelligence/scripts/`），产品定义不同
- RSS collection JSON 也在两个位置（`data/topic_collection/` vs `Documents/Nick/...`）
- 文博和我都误以为"RSS 没跑"——实际跑了，只是路径不同

**落地**：
- AGENTS.md §3.1 脚本白名单扩充：每个脚本标注 `cwd` + `path_manager` 路径
- 写新脚本前必看 `path_manager.py` 的 `BASE_PATH` 统一路径

## L-25: 脚本瘦身必清 plist ⭐⭐⭐（P0）

**教训**：脚本瘦身 / 删脚本 / 移动脚本前，**必须** `launchctl unload + grep plist 引用 + 删除/修改 plist`。

**踩坑**：
- 7-1 改造（scripts 39 → 20）时，删除了 19 个脚本，但**没检查 plist 引用**
- 留下了 **8 个死 plist**（49 天没发现！）
- 每天 launchd 跑都失败，但没任何告警（stderr log 默默积累）

**L-16 grep 全集铁律**：
```bash
# 任何脚本瘦身 / 改造前必跑
for f in ~/Library/LaunchAgents/com.nickfury.*.plist; do
  [[ "$f" == *.bak ]] && continue
  name=$(basename "$f" .plist)
  script=$(plutil -extract ProgramArguments.1 raw "$f" 2>/dev/null)
  if [ ! -e "$script" ]; then
    echo "🔴 $name | 脚本不存在: $script"
  fi
done
```

**落地**：
- AGENTS.md §3.1 / §4.0 加"L-16 脚本瘦身铁律"
- 写新脚本 / 改 plist 前必跑这个 grep

## L-26: 0 篇必须 raise（升级为红色告警）⭐⭐

**教训**：数据型任务的"0 篇"绝对不能静默通过 success status。

**踩坑**：
- daily_pipeline.py 之前：`top_articles = []` 但 `status = 'success'` → 双重欺骗
- daily_tech_report.py 之前：🟡 黄色 = 误以为系统正常
- 9 天真空期间，文博以为 RSS 没跑，实际是精选为空

**修复**：
```python
if not top5:
    # L-26 铁律: 0 篇升级为 🔴 红色, 显示数据详情
    return None, (
        f"🔴 RSS 0 篇科技文章（intelligence.json 30 天内科技类 category 为空，"
        f"共 {len(data)} 篇文章, 30 天内 fetched {len(recent)} 篇）"
    ), []
```

**落地**：
- SOUL §9.1 加"L-26 铁律 5: 0 篇必须 raise, 不许静默 success"
- analyzer_v2.py + daily_tech_report.py + daily_pipeline.py 全面加 L-26

## L-27: "30 天"要对齐业务维度

**教训**：`published` ≠ `fetched_at` ≠ `analyzed_at` 是 3 个不同维度，写代码前必须先问"哪个 30 天"。

**踩坑**：
- `get_high_priority_insights(days=30)` 之前按 `published` 30 天过滤
- RSS feed 的 `published` 是源站日期，常延迟几周
- 6 月份 29 条"重点关注"对应文章 published 在 4-5 月 → 全部被过滤 → 0 条返回

**3 个维度对应用法**：
| 维度 | 含义 | 适用场景 |
|:---|:---|:---|
| `published` | 源站发布日期 | RSS feed 抓取后筛旧 |
| `fetched_at` | 我抓到的时间 | 推送"近期抓的"科技日报 |
| `analyzed_at` | 我分析的时间 | 推送"近期分析"的投资简报 |

**修复**：
- `daily_tech_report.py` 用 `fetched_at`（"近期抓的"）
- `analyzer_v2.py` 用 `analyzed_at`（"近期分析的"）
- 7-1 老代码用 `published` → 全错位

**落地**：
- AGENTS.md §3.1 加"L-27 维度对齐"
- 写代码前必 grep `filter_recent_articles` / `published` / `fetched_at` 确认用哪个维度

---

## 关联

- INC-2026-07-03-002（主源）
- INC-2026-07-01-001（morning-rss-etf-push 失败 · 7-1 改造未清 plist 的前因）
- INC-2026-07-02-001（lark-cli launchd 推送失败 · 同日不同问题）

## 维护

- **写于**：2026-07-03 09:15
- **作者**：尼克·弗瑞 🕵️
- **下次复盘**：7-5（周日 · MEMORY.md 整理）