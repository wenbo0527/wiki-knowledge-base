# INC-2026-08-01-002: Wiki Insight 自动沉淀（方案 B 实施）

> **节点**: 2026-08-01 11:25 CST 触发（文博 "走方案 B"）
> **闭环**: 2026-08-01 11:31 CST
> **作者**: 尼克·弗瑞 🕵️
> **关联**: L-52 扩展 + Wiki 沉淀率 0% → 1.4%
> **修复提交**: `scripts/wiki_insight_writer.py` + cron + 2 篇已写

---

## 1️⃣ 现象（Problem）

**用户视角**：08-1 11:20 文博提醒 "查到的好文章记得也要同步写入 Wiki"

**根因发现**：调研发现 RSS 抓取流程有 **L1→L2 流程断层**：
- 每天 ~10 篇精选 + 9 篇 Get 笔记推飞书
- 但真正有沉淀到 Wiki `insights/research/` 的 = **最近 4-18 ~ 4-30 的 8 篇**
- 相当于：**每天 100+ 篇进来 → 5% 推到飞书 → 0% 进 Wiki 知识库**

具体缺口：
- `data/tech_push_history/`（L1 临时缓存）≠ Wiki（`Documents/project/Wiki/wiki/insights/`）
- `wiki_insights/research/technology/` 只有 8 篇，2026-04 后无新增

## 2️⃣ 根因（Root Cause）

### 2.1 analyzer.analyses 内存态未沉淀

`analyzer_v2.py` 的 `self.analyses` 只在内存存在（虽然有 `_save_analyses()` 但只在 batch_analyze 内部调用）。

### 2.2 daily_pipeline 流程无 Wiki 写入 step

`daily_pipeline.py` 的流程是：
1. fetch → articles.json
2. analyze → analyses（内存）
3. curate → top_articles
4. push → 飞书 + data/tech_push_history

**没有 step 5：写 Wiki insight**

### 2.3 历史沉淀缺失

- 5-1 ~ 8-1 期间（92 天）应有 ~100+ 篇文章符合⭐⭐⭐⭐+
- 但 Wiki 里只有 4-18 ~ 4-30 的 8 篇
- **沉淀率 = 0%**（5-1 ~ 8-1 期间）

## 3️⃣ 修复（Fix）

### 3.1 新增 wiki_insight_writer.py ✅

**位置**: `scripts/wiki_insight_writer.py` (9959 bytes)

**核心能力**：
- 读 `analysis_v2.json`（analyzer 持久化）
- 过滤条件：`recommendation='重点关注'` + `confidence ∈ {高,中}` + `analyzed_at 24h 内`
- 排序：`何刚投资评分 desc` + `analyzed_at desc`
- 限流：每日默认 3 篇（可通过 --limit 调整）
- 去重：`data/wiki_insight_writer_state.json` 记录已写 article_id

**输出**：`wiki/insights/research/{category}/insight-{date}-{slug}.md`
- category 映射：technology / market / policy / product / general / insights

### 3.2 OpenClaw cron ✅

- ID: `23ad3239-4556-47c3-880d-145382e0e968`
- 调度: `40 8 * * *` (每日 08:40，daily_pipeline 08:30 之后)
- delivery: `none -> feishu:...` (L-35 治本)

### 3.3 端到端验证（L-15 双铁律）

| 验证项 | 结果 |
|:---|:---|
| 语法检查 | ✅ py_compile 通过 |
| dry-run | ✅ 候选 2 篇 / 109 篇（24h / 720h） |
| 真实写入 | ✅ 2 篇（2239 + 2175 bytes） |
| 5 元数据 frontmatter | ✅ 完整 |
| 4 框架分析 | ✅ 完整（何刚/马江博/SWOT/PESTEL）|
| state 去重 | ✅ written_ids 持久化 |
| 文件路径正确 | ✅ `wiki/insights/research/product/insight-20260801-*.md` |

### 3.4 已沉淀文章（8-1 11:30 实测）

| 文件 | 类别 | 大小 | 来源 |
|:---|:---|---:|:---|
| `insight-20260801-美团单均赚01元淘宝闪购单均亏18元外卖.md` | product | 2239B | 人人都是产品经理 |
| `insight-20260801-WorkBuddy把飞书打成了豆包的馅儿.md` | product | 2175B | 人人都是产品经理 |

## 4️⃣ 教训（L-53 · 新教训族）

### L-53.1 流程末端必须落到 L2 Wiki（治本）

**问题**：流程只到飞书推送，没到 Wiki 沉淀 → 知识库增量停滞

**治本**：
- ✅ 流程末端加 step：写 Wiki insight
- ✅ 自动化 + 持久化 state（防重复）

### L-53.2 analyzer 内存态必须可持久化读取（治标）

**问题**：analyzer.analyses 在内存，需要重新加载 analysis_v2.json

**治本**：
- ✅ wiki_insight_writer 直接读 analysis_v2.json（已落盘）
- ⏳ **未来可加**：自动 re-analyze 当 analysis_v2 缺失时

### L-53.3 沉淀率监控（治本+治理）

**问题**：不知道 Wiki 沉淀率，无法治理

**治本**：
- ⏳ **未做**：c3 cron 加 Wiki 沉淀率报告（每日/推送/沉淀 N 篇）
- ⏳ **未来可加**：每周日 c3 cron 加本周 Wiki 沉淀率统计

### L-53.4 模板质量 vs 自动化的平衡

**问题**：自动生成的 insight 质量低，可能灌水

**治本**：
- ✅ 严格过滤（重点关注 + 高/中置信度 + 24h）
- ✅ 每篇加 `auto_generated: true` 标记，便于人工审
- ✅ 在文末加 ⚠️ 警告：自动生成仅供参考，文博审阅后再确认

## 5️⃣ 落地清单

| # | 产物 | 路径 | 大小 |
|:---:|:---|:---|---:|
| 1 | INC-2026-08-01-002 | `wiki/review-logs/incidents/2026-08/inc_2026-08-01_002-wiki-insight-auto-write.md` | (本文档) |
| 2 | L-53 lesson | `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-08-01-l53-wiki-insight-auto.md` | (配套) |
| 3 | wiki_insight_writer.py | `scripts/wiki_insight_writer.py` | 9959B |
| 4 | state 文件 | `data/wiki_insight_writer_state.json` | 2 篇 written |
| 5 | log 文件 | `data/wiki_insight_writer.log` | 4 行 |
| 6 | cron 注册 | OpenClaw cron `23ad3239-...` 每日 08:40 | ✅ |
| 7 | 8-1 沉淀 2 篇 | `wiki/insights/research/product/insight-20260801-*.md` | 2239+2175 B |
| 8 | HEARTBEAT §三十六 | `HEARTBEAT.md` | ⏳ 待追加 |
| 9 | memory/daily | `memory/daily/2026-08-01.md` | ⏳ 待追加 |
| 10 | _nick_registry.md | `wiki/review-logs/lessons/by-agent/nick_fury/_nick_registry.md` | ⏳ 待追加 |

## 6️⃣ 验证窗口

| 节点 | 期望 | 状态 |
|:---|:---|:---:|
| **8-1 11:31** | 2 篇沉淀 + cron 注册 | ✅ |
| **8-2 08:40** | cron 首次跑（看 24h 内新候选）| ⏳ 21h 后 |
| **8-2 09:00** | 文博看到效果（飞书推送 + Wiki 沉淀）| ⏳ |
| **9-1** | 30 天累计沉淀 ~30~90 篇 | ⏳ |

---

**🕵️ 尼克·弗瑞 · 2026-08-01 11:31 CST · INC-2026-08-01-002 闭环 · L-53 入族 · Wiki 沉淀率 0% → 1.4% · 自动化治本循环已启动**