# 🔴 Incident 004: Get 笔记 → Wiki 同步静默失败 50 天（hardcoded + error swallow）

| 字段 | 值 |
|:---|:---|
| **ID** | inc_2026-07-14_004 |
| **严重级别** | 🔴 Critical |
| **状态** | ✅ Closed |
| **发现时间** | 2026-07-14 14:00 |
| **发现者** | wenbo 主动疑问"是否有持续在补充我们的 Wiki" |
| **负责人** | nick_fury |
| **最后更新** | 2026-07-14 14:05 |

---

## 问题描述

文博 14:00 问"GET 笔记我们订阅的知识库中是否有持续在补充我们的 Wiki" → nick_fury 立即排查。

**揭穿**：
- API 端（Get 笔记 EJ9zwkln 知识库）实际有 **20 条笔记**，最新 7-14 #132
- Wiki 端（`/insights/ai-technology/`）最近新增**5-25 至今 50 天 0 条**
- 同步脚本 `getnote_ej9_to_wiki.py` **硬编码 5 条 4-29 ~ 5-1 笔记 ID**，再也不会拉新笔记
- launchd 每天 06:00 触发 → AttributeError 被 swallowed → "✅ 同步完成" 静默吞错 50 天

## 影响分析

| 维度 | 数据 |
|:---|:---|
| **真空天数** | **50 天**（5-25 ~ 7-14） |
| **漏掉的笔记** | **至少 15 条**高质量 AI/产品/访谈笔记 应入 Wiki |
| **价值损失** | Anthropic Fiona Fung（编码之后）/ Noam Brown（推理测试时计算）/ YC Pete Koomen（内部超级智能）/ Lenny 等重要访谈**全没入 Wiki** |
| **影响范围** | 不止 EJ9zwkln——**整个 insights/ 各子目录**（除 ai-tools 6-23 + 1）**全停 5-25 ~ 5-26** |
| **C-3 cron** | ✅ 每天 100% ratio（daily 正常），但 c3 不检查 insights/ 增量 |

## 根因分析

### 三层根因（链式）

**根因 1（脚本逻辑）**: `getnote_ej9_to_wiki.py` 第 17-22 行 hardcoded 5 条笔记 ID
```python
notes = [
    ("1908684543306663264", "insight-20260501-watchlist-060.md", ...),
    ("1908591773086224360", "insight-20260430-watchlist-059.md", ...),
    ...
]
```
意味着脚本永远只拉这 5 条 → 写完 Wiki 后**永远不会自然更新**。

**根因 2（error swallow）**: launchd 每天 6:00 触发，但每次都:
```
Traceback ... AttributeError: 'NoneType' object has no attribute 'get'
✅ 同步完成: Tue Jul 14 06:00:00 CST 2026  ← 静默吞错
```
**这是 L-29 教训的极端例子**：每次都说成功，但内容为空。

**根因 3（对账缺失）**: 没有脚本检查"API 端 vs Wiki 端 笔记数量差异"。
- API 端 20 条，Wiki 端 5 条（5-25 写的）
- 5-3 ~ 7-14 共 12+ 条新盯人日报 都没入 Wiki
- 50 天没人察觉

### 关键问题

> **同步类脚本的 3 条铁律全违反**：① 不应 hardcode ② 不应 swallow error ③ 必须对账 API vs 本地数量

## 解决措施

### v2.0 重写（5 min · 已完成）

```
scripts/getnote_ej9_to_wiki.py v2.0:
  ✅ fetch_kb_notes(): API 分页拉所有笔记（不是 hardcode）
  ✅ is_high_value(): 关键词过滤（14 个 HIGH_VALUE_KW）
  ✅ write_wiki_insight(): 单条 try/except 失败 raise 不吞错
  ✅ save_state(): 防重复 (synced_note_ids 状态文件)
  ✅ 多知识库路由: KB_ROUTING = {"EJ9zwkln": "ai-technology"}
  ✅ BACKFILL_DAYS = 60: 一次性补 60 天缺口
  ✅ 异常路径测试: env 损坏时 RuntimeError 立即 raise
```

### 立即同步 50 天缺口（已完成 · 14:03:57）

| 写入 | 数量 |
|:---|:---:|
| 总 fetch | 20 条 |
| 总 write | **20/20 100% ✅** |
| 失败 | 0 |
| 写入路径 | `wiki/insights/ai-technology/getnote-{date}-{id}-{title}.md` |

补的 15 条新文件时间分布：
```
2026-07-13 #131
2026-07-12 #130
2026-07-09 #129
2026-07-08 #128
2026-07-07 #127
2026-07-06 #126
2026-07-05 #125
2026-07-04 #124
2026-07-03 #123
2026-07-02 #122
2026-07-01 #121
2026-06-30 Lenny + Noam Brown + YC Pete Koomen (4 篇)
2026-06-29 Anthropic Fiona Fung (2 篇)
2026-05-25, 2026-05-12 每日新知总结
```

### 异常路径测试（L-15 step 5）

| 场景 | 行为 | 结果 |
|:---|:---|:---:|
| env 损坏 | 立即 raise RuntimeError | ✅ |
| API HTTP 错误 | 立即 raise RuntimeError | ✅ |
| 单笔记 detail 失败 | raise 但不中断后续 | ✅ |
| 全部失败 | exit 1 + fail 详情输出 | ✅ |

### 防复发机制（待办·优先级排序）

| # | 动作 | 优先级 |
|:-:|:---|:---:|
| 1 | **c3_daily_check.py 升级**: 加 insights/ 子目录增量监控（API vs Wiki 数量对比）| 🟠 |
| 2 | **同步类 L-32 沉淀**: 任何 fetcher 脚本 3 必检（hardcode / swallow / 对账）| ✅ 已沉淀 |
| 3 | **多 KB 路由**: 扩展到人工智能+WAIC / 产品大神怎么想等 TOOLS.md §5 列出的知识库 | 🟡 |
| 4 | **高频 KB 拆分 v2.1**: 按 KB 路由到不同子目录（避免 ai-technology 巨化）| 之后 |

## 关联文档

- INC-2026-07-14-001: hardcoded 预设（数据层）
- INC-2026-07-14-002: fetcher 算法错（算法层）
- INC-2026-07-14-003: 11 天真空路径错（路径层）
- **INC-2026-07-14-004: 同步脚本 hardcode + swallow（同步层）**
- Lesson L-31: INC/lesson 必须立即归档
- **Lesson L-32 (新增)**: 同步脚本 3 必检——不 hardcode / 不 swallow / 必对账

---

## 后续行动

- [x] v2.0 脚本重写 + py_compile
- [x] 端到端 20/20 跑通
- [x] 异常路径测试
- [x] 50 天缺口补完（15 条新笔记入 Wiki）
- [x] INC-004 写盘
- [x] L-32 沉淀
- [ ] c3_daily_check.py 加 insights 增量检查
- [ ] 扩展 KB 路由到其他知识库

---

*Created: 2026-07-14 14:05 | Updated: 2026-07-14 14:05 | Closed*