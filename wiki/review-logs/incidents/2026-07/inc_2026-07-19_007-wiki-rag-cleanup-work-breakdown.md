# INC-2026-07-19-007 · Wiki 知识库 + RAG 脚本整理方案

> **INC 编号**：INC-2026-07-19-007
> **日期**：2026-07-19 11:55 CST
> **触发**：文博 11:37 "我希望你同步整理一下 Wiki 知识库 和 RAG相关的各类脚本"
> **状态**：⏳ 方案落档 · 待文博拍板执行范围
> **关联**：INC-004~006（推送管线重构）· L-13 OpenClaw 原生优先
> **独立工程**：区别于推送管线重构（阶段 1 正在等文博"开干"）

---

## 0️⃣ 现状全景（11:55 CST 实测）

### 0.1 Wiki 知识库

| 维度 | 数值 | 状态 |
|:---|:---:|:---|
| **总文档数** | 1704 | - |
| **顶层目录** | 17 | 🟡 超 KR1 ≤15（多 2 个） |
| **insights/** | 926 (54%) | 🟢 最大目录 |
| **topics/** | 228 (13%) | 🟢 |
| **methodologies/** | 147 (9%) | 🟢 |
| **review-logs/** | 140 (8%) | 🟡 含 13 个空目录 |
| **_archive/** | 66 (4%) | 🟡 历史归档 |
| **其他 11 个** | 256 | 🟢 |
| **4 项元数据覆盖率** | 1653 篇 (97%) | 🟢 |

### 0.2 review-logs 结构（13 个空目录）

```
review-logs/
├── by-severity/
│   ├── low/          (空 · 设计占位)
│   ├── critical/     (空 · 设计占位)
│   └── medium/       (空 · 设计占位)
├── archives/
│   └── 2026/         (空 · 设计占位)
├── daily/            ✅
├── lessons/
│   ├── by-agent/{data_community_dev, tony, paimon, nick_fury, agatha, zhongli, wenbo} (7 个 agent · 已用)
│   └── by-topic/{product, collab, tech, ...} (多主题)
├── incidents/        ✅
└── reviews/
    ├── monthly/      (空 · 设计占位)
    └── weekly/       (空 · 设计占位)
```

### 0.3 RAG 服务

| 维度 | 数值 | 状态 |
|:---|:---:|:---|
| **服务地址** | localhost:8082 (Chroma + Ollama bge-m3) | 🟢 |
| **authored chunks** | 10743 (文档仓库 688 md) | 🟢 |
| **curated chunks** | 0 (Wiki 未接入！) | 🔴 大问题 |
| **混合检索** | vector + BM25 + RRF | 🟢 |
| **5 关键文档可检索** | ✅ | 🟢 |
| **MRR@10** | 1.000 | 🟢 |
| **延迟 P99** | ~200ms | 🟢 |

### 0.4 RAG 相关脚本（12+ 个 · 分散在 3 个目录）

#### 📁 /Users/wenbo/Documents/project/Wiki/scripts/（官方 · 7 个）

| 脚本 | 行数 | 用途 | 最后修改 |
|:---|:---:|:---|:---:|
| wiki_auto_review.py | 17555B (7-18 最新) | 自动走查 · 健康度评分 | 7-18 |
| daily_ingest.py | 5520B | 每日入库 | 4-08 |
| topic_ingest.py | 6473B | 主题入库 | 4-08 |
| wiki_lint.py | 5501B | Lint 检查 | 4-16 |
| wiki_outdated_check.py | 4028B | 过时检测 | 5-06 |
| wiki_search.py | 3427B | 搜索 | 4-08 |

#### 📁 /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/（Nick · 5 个）

| 脚本 | 用途 | 状态 |
|:---|:---|:---:|
| wiki_health_check.sh | Wiki 健康检查（v2.0 RAG 驱动）| ✅ 活跃 |
| wiki_kr1_evaluation.py | KR1 评估（≤15 目录）| ✅ 活跃 |
| wiki_metadata_batch.py | 4 项元数据批量 | ✅ 活跃 |
| getnote_to_wiki.sh | Get 笔记 → Wiki | ✅ 活跃 |
| c3_daily_check.py | 含 Wiki 引用检查 | ✅ 活跃 |

#### 📁 /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/_backup_before_20260701/（备份 · 10+ 旧脚本 · 未清理）

- add_p0_rss_sources.py / batch_import_rss.py / c3_daily_check.py / check_task_status.py
- daily_investment_summary.py / daily_topic_collector.sh / etf_allocation_analysis.py
- fetch_etf_history.py / getnote_ej9_to_wiki.py / getnote_sync_articles.py
- getnote_to_wiki.sh / getnote_to_wiki.py / github_explorer.py / github_tracker.py
- morning_rss_etf_push.py / wiki_health_check.sh

#### 📁 skills/（RAG 相关 · 3 个）

- skills/best-practice-collector/run_collector_fixed.sh
- skills/rss-intelligence/scripts/cleanup_old_articles.py
- skills/rss-intelligence/scripts/github_tracker.py

---

## 1️⃣ 5 大整理任务（按优先级）

### 🔴 P0 · Wiki 接入 RAG（最大价值 · 0 chunks 治本）

**目标**：Wiki 1704 md → RAG authored collection（类似文档仓库）

| 子任务 | 工作量 | 备注 |
|:---|:---:|:---|
| 写 `wiki_to_rag_ingest.py`（参考 daily_ingest.py）| 1-2 h | 解析 Wiki md → chunk |
| 加 bge-m3 embedding → Chroma authored | 30 min | 复用现有 API |
| 端到端验证（Wiki 检索"情报分析 SOP"等）| 30 min | L-15 铁律 |

**预期收益**：curated chunks 0 → ~3000+（Wiki 1704 md × ~2 chunks/md）

### 🟠 P1 · Wiki 顶层目录收敛（17 → 15）

**目标**：超 KR1 ≤15 的 2 个目录收敛

| 候选 | 现状 | 建议 |
|:---|:---|:---|
| `.obsidian/` | Obsidian 配置目录 | 🟢 不算（隐藏目录）· 实际 = 16 |
| `projects/fintech-product/` | 1 个文档 | 🟡 决定：归档到 projects/ 或保留独立 |

**评估**：实际顶层目录 16 个（不含 .obsidian），其中 1 个是 `projects/fintech-product`（1 个文档）—— 可合并到 `projects/`

### 🟡 P2 · review-logs 规范化（13 个空目录）

| 候选 | 现状 | 建议 |
|:---|:---|:---|
| by-severity/{low,critical,medium} | 设计占位 | 🟡 加 .gitkeep + README 说明用途 |
| archives/2026 | 设计占位 | 🟡 同上 |
| lessons/by-topic/{product,collab,tech} | 主题占位 | 🟡 同上 |
| reviews/{monthly,weekly} | 周月报占位 | 🟡 同上 |
| lessons/by-agent/{tony,agatha,wenbo} | 部分 agent 暂未写 | 🟡 加 README 说明 |

### 🟢 P3 · RAG 脚本整理（清理 + 归档）

| 候选 | 现状 | 建议 |
|:---|:---|:---|
| `_backup_before_20260701/` (10+ 脚本) | 备份目录 | 🟡 移到 `_deprecated/2026-07-01/` 或 trash |
| `_deprecated/2026-07-01/` | 已归档 | 🟢 检查是否完整 |
| `_deprecated/2026-07-14/` | 已归档 | 🟢 检查 |
| `scripts/daily_investment_summary.py` | 已被 daily_investment_report.py 替代 | 🟡 归档 |

### 🟢 P4 · Wiki 文档补全（双向链接）

| 候选 | 现状 | 建议 |
|:---|:---|:---|
| insights/ 中无双向链接 30+ | 7-19 报告 | 🟡 批量补双向链接（insight → 来源文章）|

---

## 2️⃣ 5 大整理任务的执行计划（7 天）

### Day 1（明天 7-20 周一）
- ✅ **P0 写 wiki_to_rag_ingest.py** + 端到端验证
- ✅ Wiki 接入 RAG curated collection

### Day 2（7-21 周二）
- ✅ **P1 顶层目录收敛**：projects/fintech-product → projects/
- ✅ KR1 ≤15 验证

### Day 3（7-22 周三）
- ✅ **P2 review-logs 规范化**：13 个空目录加 .gitkeep + README
- ✅ 13 个 README 说明用途

### Day 4（7-23 周四）
- ✅ **P3 RAG 脚本整理**：备份目录归档
- ✅ 删除或 trash 已废弃脚本

### Day 5（7-24 周五）
- ✅ **P4 Wiki 文档双向链接补全**：insights/ 30+ 文档
- ✅ 端到端验证检索

### Day 6-7（7-25 ~ 7-26）
- ✅ 整体端到端验证
- ✅ lessons + INC-007 闭环

**注意**：阶段 1（推送管线重构 7-20~7-26）与本工程并行，但优先 P0 Wiki→RAG（价值最大）

---

## 3️⃣ 风险评估

| 风险 | 概率 | 影响 | 缓解 |
|:---|:---:|:---:|:---|
| Wiki 接入 RAG 引入性能问题 | 🟡 低 | 🟠 中 | 分批入库 · 监控 P99 |
| 顶层目录移动破坏 wiki-link | 🟡 低 | 🟠 中 | L-49.6 决策树 · 先查引用再移 |
| 空目录加 README 引起 wiki.review 误报 | 🟢 低 | 🟢 低 | .gitkeep 不被算法扫到 |
| 备份目录归档丢失历史 | 🟢 低 | 🟡 中 | trash 而非 rm（可恢复） |

---

## 4️⃣ 立即可做（不需文博 explicit OK）

🟢 今天 12:00-13:00 Nick 自己：
- 列出 Wiki 顶层目录每个文档的"目标目录"映射表
- 检查 `daily_ingest.py` 能否作为 Wiki 接入 RAG 模板
- 备份脚本 → `_backup_before_20260719/`（L-17 铁律）

---

## 5️⃣ 等文博拍板

| 决策点 | 选项 |
|:---|:---|
| **A 执行范围** | (a) 全部 5 大任务 · (b) 只 P0 Wiki→RAG · (c) P0+P1+P2 · (d) 等阶段 1 完成 |
| **B 顶层目录 projects/fintech-product** | (a) 合并到 projects/ · (b) 保留独立 · (c) 删除（仅 1 个文档）|
| **C review-logs 13 空目录** | (a) 加 .gitkeep + README · (b) 删除空目录 · (c) 保留 |
| **D 备份目录归档** | (a) 移到 _deprecated/ · (b) trash · (c) 保留观察 |
| **E 时间窗** | (a) 立即开始 · (b) 阶段 1 完成后（7-26 后）· (c) 周末复盘时定 |

---

## 6️⃣ 与推送管线重构的关系

| 工程 | INC | 范围 | 互斥？ |
|:---|:---|:---|:---:|
| **推送管线重构**（阶段 1）| INC-004~006 | 5 个推送脚本 + cron | - |
| **Wiki + RAG 整理**（本工程）| INC-007 | Wiki 1704 md + RAG 12+ 脚本 | ❌ 独立 |

**建议**：两个工程可并行，但优先 P0 Wiki→RAG（价值最大）+ 阶段 1 P0 daily_pipeline.py（推送核心）

---

*🕵️ nick_fury · 2026-07-19 11:55 CST · Wiki + RAG 整理方案 · 等文博拍板*
