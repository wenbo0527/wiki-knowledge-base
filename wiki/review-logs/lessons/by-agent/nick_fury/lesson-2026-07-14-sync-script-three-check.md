---
title: lesson 2026 07 14 sync script three check
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# Lesson L-32: 同步脚本 3 必检——不 hardcode / 不 swallow / 必对账

> 7-14 14:05 沉淀 · nick_fury 🕵️ · INC-2026-07-14-004

---

## 教训主体

**任何"fetcher / 同步 / ETL"类脚本必须满足 3 条铁律**：

| # | 铁律 | 反例（v1.0）| 正例（v2.0）|
|:-:|:---|:---|:---|
| **1** | **不 hardcode** 笔记/资源 ID | `notes = [...5 条固定 ID...]` | fetch API list 最新 |
| **2** | **不 swallow error** | AttributeError + "✅ 同步完成" | raise RuntimeError 立即告知 |
| **3** | **必对账** API vs 本地 | 无对账脚本 | state JSON 记录 synced_note_ids + c3 加增量检查 |

## 反例（INC-2026-07-14-004 触发）

```python
# getnote_ej9_to_wiki.py v1.0 (5-22 ~ 7-14 持续运行 50 天)
notes = [
    ("1908684543306663264", "insight-20260501-watchlist-060.md", ...),  # hardcoded ID
    ("1908591773086224360", "insight-20260430-watchlist-059.md", ...),
    ("1908499020048033248", "insight-20260429-watchlist-058.md", ...),
    ("1908523091191195104", "insight-20260429-cat-wu-interview.md", ...),
    ("1908522166698427616", "insight-20260429-cat-wu-anthropic-team.md", ...),
]
# 没有 is_high_value 过滤
# 没有 try/except (整体 try/except 即可吞错)
```

**3 条全违反**：
1. ❌ 写死笔记 ID（永不拉新）
2. ❌ try/except 整段包裹 → AttributeError 被吞
3. ❌ 无对账脚本（API 20 条 vs Wiki 5 条，差异 15 条没人发现）

## 正例（v2.0）

```python
# getnote_ej9_to_wiki.py v2.0 (7-14 14:02 重构)

# 铁律 1: 不 hardcode - 用 API 拉
notes = fetch_kb_notes(env, kb_id)  # 分页拉所有

# 铁律 2: 不 swallow - 单条 try/except raise 全部错误
for note in notes:
    try:
        ...
    except Exception as e:
        failures.append({"note_id": ..., "error": str(e)})
        # continue 不吞错 - 完整错误记入 failures[]

# 铁律 3: 必对账 - state JSON + c3 cron 检查
state["synced_note_ids"] = list(synced_set.union(new_synced))
state["stats"] = {"fetched": ..., "written": ..., "failures": ...}
save_state(state)
# C-3 cron 加: API total vs Wiki total 数量对比
```

## L-32 grep 检查（修一类必 grep 全集）

```bash
# 任何同步 / fetcher / etl 脚本都应:
# 1) 没有 hardcoded ID (notes = [...固定 ID...])
# 2) 没有 except: pass / except Exception: continue 大包裹
# 3) 有 state JSON 记录"已同步 X 条"
find /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/ \
  \( -name "*sync*" -o -name "*fetcher*" -o -name "*etl*" \) \
  -type f 2>/dev/null | while read f; do
    echo "=== $f ==="
    grep -nE "except.*pass|except.*continue|notes = \[\(" "$f" | head -5
done

# 当前: getnote_ej9_to_wiki.py v2.0 ✅ / daily_note_scan.py 有 except:pass (要在 c3 升级时修)
```

## L-32 防复发机制（已加到 INC-004 后续行动）

| # | 动作 | 优先级 |
|:-:|:---|:---:|
| 1 | c3_daily_check.py 加: `data/getnote_sync_state.json` 的 fetched vs Wiki 实际文件数对比 | 🟠 P1 |
| 2 | 扩展 KB 路由（人工智能+WAIC / 产品大神 / 消费金融 / 产品&运营）| 🟡 P2 |
| 3 | daily_note_scan.py 升级（按 L-32 同样标准）| 🟡 P2 |

## L-32 与 L-28/L-29 关系

| Lesson | 教训层级 | 触发场景 |
|:---|:---|:---|
| L-28 | 数据层 | 数据源多源兜底 |
| L-29 | 验证层 | 自检区分输出/输入真实 |
| **L-32** | **同步层** | **fetcher 脚本 3 必检** |
| L-31 | 路径层 | INC/lesson 必须立即归档 |
| L-30 | 算法层 | 估值 ≠ 价格 |

5 个教训形成"数据/验证/同步/路径/算法"五层质量门，**任何 1 层缺位 → 该类问题重发**。

---

*🕵️ 尼克·弗瑞 · 2026-07-14 14:05*