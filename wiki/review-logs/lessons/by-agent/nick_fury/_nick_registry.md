---
title:  nick registry
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# 🕵️ Nick Fury Lessons & INC 注册表

> 维护者: 尼克·弗瑞 (Nick Fury) 🕵️
> 最后更新: 2026-07-16 08:15 CST
> 用途: Nick 团队 INC + Lesson 索引（按时间倒序）

---

## 📌 7-16 增量（候选 #235 6/6 闭环实证 · W1 速赢 + 候选 #117+#129+#172 第 17 次失守链修复）

| ID | 类型 | 标题 | 路径 / 状态 |
|:---|:---|:---|:---|
| okr-2026-h2-q3 | OKR | Wiki 整理 H2/Q3/W1 三层 OKR Draft v1.0 | projects/knowledge-base/okr-2026-h2-q3.md |
| okr-2026-w1-execution-plan | Plan | W1 速赢执行计划（Phase 1 全部任务清单 + 验收）| projects/knowledge-base/okr-2026-w1-execution-plan.md |
| wiki-cleanup-phase1.1 | Action ✅ | 删 `review-logs/incidents/{2026-05}/` 空目录（AGENTS §0.5 L-31 花括号残留）| ✅ 7-16 07:12 |
| wiki-cleanup-phase1.2 | Action ✅ | 删 `review-logs/lessons/by-agent/nick/` 空目录（L-16 全集 grep 无残留）| ✅ 7-16 07:13 |
| wiki-cleanup-phase1.3 | Action ✅ | methodologies-v2 合并：v2 是 L1-L4 分层结构替 v1 扁平，v1 00~06 经 diff 确认与 v2 重叠 → trash；07 文件抢救保留 | ✅ 7-16 07:23 |
| wiki-cleanup-phase1.4 | Action ✅ | `_archive/empty-files-cleanup-20260604/`：保留 4 个清理 md（审计）+ trash 27 placeholder + 2 temp 空文 | ✅ 7-16 07:25 |
| wiki-cleanup-phase1.5 | Action ✅ | 12 篇 90+ 过期 精准 trash 5 篇（process/* 4 + concepts/karpathy 重叠 1）| ✅ 7-16 07:26 |
| wiki-cleanup-phase1.6 | Action ✅ | `_nick_registry.md` 更新（本段）| ✅ 7-16 07:30 |
| lesson-2026-07-16-macos-trash-verify | Lesson 🆕 | macOS `/usr/bin/trash` 验证必用 `ls -la <目标>`（"Operation not permitted" 是 TCC 不是失败）| lessons/by-agent/nick_fury/lesson-2026-07-16-macos-trash-verify.md（待建）|
| lesson-2026-07-16-wiki-methodology-v1v2 | Lesson 🆕 | methodologies v1 vs v2 是进化关系不是重叠；v2 替 v1 + 抢救 07 | lessons/by-agent/nick_fury/lesson-2026-07-16-wiki-methodology-v1v2.md（待建）|
| wiki-cleanup-phase1.7 | Action ✅ | **8 个一级目录 `index.md` 落盘**（insights/concepts/topics/projects/skills/tools/sources/standards，详见下）| ✅ 7-16 08:15 |
| wiki-cleanup-empty-dirs-24 | Decision ✅ | **24 个真·空目录全保留**（结构性占位，文博推荐 D🅰）| ✅ 7-16 08:10 |
| wiki-cleanup-doc-delta-plus2 | Decision ✅ | **+2 偏差归因**：mdfind 命中 5-23 备份路径（Spotlight 缓存）→ trash 实际成功（L-42 候选：mdfind 不能验证 trashed 位置）| ✅ 7-16 08:15 |
| **inc_2026-07-16_001** | Incident 🆕 | **派蒙派单候选 #129 同根病 · 6 任务清单缺失** | incidents/2026-07/inc_2026-07-16_001-paimon-dispatch-candidate-129-same-root.md ✅ |
| **lesson-2026-07-16-paimon-dispatch-129-candidate** | Lesson 🆕 | **派单接收 4 项实证防御**（任务 ID / 派单对象 / 验收标准 / 背景依赖）| lessons/by-agent/nick_fury/lesson-2026-07-16-paimon-dispatch-129-candidate.md ✅ |
| **L-39（候选 · 待 7-19 正式编号）** | Lesson · 候选 | **派单要素不齐 = 同根病复发**（候选 #117+#129 家族延伸 · 第 16 次）| lessons/by-agent/nick_fury/lesson-2026-07-16-paimon-dispatch-129-candidate.md |
| **HEARTBEAT.md §十三** | Action ✅ | 7-16 07:36 派单回执 v1.0 · 候选 #129 诚实归零（10:30 早检 + 14:01 截止）| HEARTBEAT.md ✅ |
| **inc_2026-07-16_002** | Incident 🆕 | **6 任务 close output_path 信约 ≠ 实际 · 候选 #117+#129+#172 第 17 次** | incidents/2026-07/inc_2026-07-16_002-output-path-promise-vs-actual-59days.md ✅ |
| **lesson-2026-07-16-deadlock-lessons-rescue** | Lesson 🆕 | **6 任务 close 后 lessons 落档 owner 明确 + task_tool v2.0-rc.2 升级** | lessons/by-agent/nick_fury/lesson-2026-07-16-deadlock-lessons-rescue.md ✅ |
| **6 deadlock-close-59days lessons** | Action ✅ | **6 任务 lessons 文件补写实证** （1495+1577+1511+1515+1539+1660 = 9297 字节）| `Nick/memory/lessons/` ✅ |
| **L-40（候选 · 待 7-19 正式编号）** | Lesson · 候选 | **db 信约 ≠ 文件实际 = close 字段填 ≠ lessons 文件真的写**（候选 #117+#129+#172 第 17 次）| lesson-2026-07-16-deadlock-lessons-rescue.md |
| **候选 #235 第①项 6/6 闭环** | Action ✅ | **6 任务 7-15 15:29:41 已 closed + 6 lessons 补写完成 · 候选 #235 第①项天然闭环** | review-logs + Nick/memory/lessons/ ✅ |
| **Phase C.2 元数据批量** | Action ✅ | **Wiki 4 项元数据 1-2% → 99%（超 Q3 目标 4 个百分点）· 1576 篇 / 25.4 秒 / 0 错误** | ✅ 7-16 17:18 |
| **inc_2026-07-16_003** | Incident 🆕 | **Wiki 元数据批量补全 1% → 99% 突破** | incidents/2026-07/inc_2026-07-16_003-wiki-metadata-batch-99pct.md ✅ |
| **lesson-2026-07-16-wiki-metadata-batch-99pct** | Lesson 🆕 | **L-43 不覆盖语义 + L-44 git log earliest date**（含 scripts 资产化） | lessons/by-agent/nick_fury/lesson-2026-07-16-wiki-metadata-batch-ninety-nine-pct.md ✅ |
| **scripts/wiki_metadata_batch.py** | Asset 🆕 | **8863 字节 · L-15 端到端验证全过 · 19 种 PD-* 映射 · 1626 篇备份** | scripts/wiki_metadata_batch.py ✅ |
| **/tmp/wiki_metadata_backup_2026-07-16/** | Backup 🆕 | **1626 篇原文件备份（30 天可恢复）** | /tmp/wiki_metadata_backup_2026-07-16/ ✅ |
| **Phase D 三方对账** | Action ✅ | **Wiki 99% 元数据 + RAG 20949 chunks + Get笔记 8 KB HTTP 200 = KR8 完成** | ✅ 7-16 19:30 |
| **search_api 重启** | Action ✅ | **清 stale UUID 50085a6f cache · query 工作 · chroma.sqlite3 backup 450M** | ✅ 7-16 19:24 |
| **inc_2026-07-16_004** | Incident 🆕 | **Get笔记 API 401 真根因：认证格式错（不是 WAF / 不是 token 过期）** | incidents/2026-07/inc_2026-07-16_004-getnote-auth-format-no-bearer.md ✅ |
| **lesson-2026-07-16-getnote-auth-no-bearer** | Lesson 🆕 | **L-46 Get笔记 API = `Authorization: <key>` 无 Bearer + 必加 `X-Client-ID`** | lessons/by-agent/nick_fury/lesson-2026-07-16-getnote-auth-no-bearer.md ✅ |

**Phase 0 实测基线**（7-16 07:07 CST）：
- 文档总数: **1671**（不是 5-21 记忆 688，3 个月翻 2.5 倍，**L-37 印证 v1.0 备份过时**）
- 顶层目录: 28
- 元数据覆盖: product_domain 1% / author 1% / date 2% / tags 2%（**4 项全 < 2%**）
- 过期(90+): 12 篇 / 空文档: 27 篇

**Phase 1.1-1.6 验证后数据**（7-16 07:30 CST）：
- 文档总数: **1634**（基线 1671 - 实际 trash 37，+2 偏差待查）
- 顶层目录: **22**（目标 KR1 ≤15，距目标 -7）
- 空目录残留: 24 个真·空 + 1 resolved（保留）+ 1 .trash（工具 metadata）
- 过期(90+): 7 篇保留（人物 3 + 参考 4）
- 空文档: **0** ✅
- 花括号残留: **0** ✅
- nick/ 残留: **0** ✅
- methodologies-v2 残留: **0** ✅

**Phase 1.3 v1 vs v2 实质差异 + 处置**：
- v1（methodologies/）：8 个扁平 .md（v1.1，2026-05-12）
- v2（methodologies-v2/）：7 方法论 × L1-流程/L2-方法论/L3-模板/L4-知识 4 层
- v2 是进化版（L1-L4 道法术器分层），不是简单补充
- v1 00~06 头 6 行 diff v2 对应 L2-方法论/xx.md：**完全相同**
- **执行**：v2 整体 mv 到 methodologies/ + v1 00~06 trash + v1 07 抢救保留
- 终态 methodologies/：7 目录 + 07 + L4索引模板 = 9 项 / 58 .md

**L-41 macOS trash 验证踩坑**（NEW · 7-16 07:27）：
- `ls ~/.Trash` → "Operation not permitted"（macOS TCC 限制）
- 陷阱：以为 trash 命令失败 → **实际 trash 成功了**
- 验证方法：`ls -la <被删目标文件路径>` 看 "No such file or directory" 才算
- 已验证：4 个目标 .md 全返回 No such file ✅

---

## 📌 7-15 增量

---

## 📌 7-15 增量

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-15_001 | Incident | OpenClaw cron 投递失败（25 任务全挂 + 5 脚本已删）| incidents/2026-07/inc_2026-07-15_001-openclaw-cron-fail-closed.md |
| inc_2026-07-15_002 | Incident | GET 笔记 KB 真实 15 个（报告"4 个"是错的）| incidents/2026-07/inc_2026-07-15_002-getnote-kb-count-actually-15.md |
| inc_2026-07-15_003 | Incident | Agent 真实数量 17 个（报告"30 个"是错的）| incidents/2026-07/inc_2026-07-15_003-agent-count-actually-17.md |
| inc_2026-07-15_004 | Incident | 本地文档 RAG 化第一波（行业研究 7 篇落盘）| incidents/2026-07/inc_2026-07-15_004-local-docs-rag-first-wave.md |
| inc_2026-07-15_005 | Incident | 战略 3 KB 同步（文博 AI 转型 + 快刀青衣 + 2026 WAIC）| incidents/2026-07/inc_2026-07-15_005-strategic-3-kb-sync.md |
| inc_2026-07-15_006 | Incident | GET 笔记入库 + QPS 429 限流 + WAIC 真实价值揭穿 | incidents/2026-07/inc_2026-07-15_006-getnote-qps-429-and-waic-reval.md |
| inc_2026-07-15_007 | Incident | GET 笔记入库 v2.1（每日 100 篇限流）| incidents/2026-07/inc_2026-07-15_007-getnote-daily-limit-100.md |
| lesson-2026-07-15-cron-command-sync | Lesson | cron argv 必须随 scripts 改造同步更新 | lessons/by-agent/nick_fury/lesson-2026-07-15-cron-command-sync.md |
| lesson-2026-07-15-script-rename-cron-grep | Lesson | cron 投递必须 mode=none + channel=feishu + to=user:ou_xxx（派蒙模式）| lessons/by-agent/nick_fury/lesson-2026-07-15-script-rename-cron-grep.md |
| lesson-2026-07-15-script-exit-code-best-effort | Lesson | 推送脚本退出码 = 0 当主通道 lark-cli 成功 | lessons/by-agent/nick_fury/lesson-2026-07-15-script-exit-code-best-effort.md |
| lesson-2026-07-15-report-must-verify-real-api | Lesson | 报告必须 verify 实时 API（L-37 治本）| lessons/by-agent/nick_fury/lesson-2026-07-15-report-must-verify-real-api.md |
| lesson-2026-07-15-agent-count-must-use-openclaw-api | Lesson | Agent 数量必用 openclaw agents list API（L-38 治本）| lessons/by-agent/nick_fury/lesson-2026-07-15-agent-count-must-use-openclaw-api.md |
| lesson-2026-07-15-local-docs-rag-pipeline | Lesson | 本地文档 RAG 化 4 步 SOP（L-39 治本）| lessons/by-agent/nick_fury/lesson-2026-07-15-local-docs-rag-pipeline.md |
| lesson-2026-07-15-getnote-kbs-sub-cli-discovery | Lesson | 订阅 KB 必用 `getnote kbs-sub` CLI（L-40 治本）| lessons/by-agent/nick_fury/lesson-2026-07-15-getnote-kbs-sub-cli-discovery.md |
| lesson-2026-07-15-getnote-sync-qps-and-backfill | Lesson | GET 笔记入库 4 件事（QPS / 拉全量 / KB 评估 / 失败必 raise）| lessons/by-agent/nick_fury/lesson-2026-07-15-getnote-sync-qps-and-backfill.md |
| lesson-2026-07-15-getnote-daily-limit-100 | Lesson | GET 笔记入库 4 大常量（DAILY_LIMIT 100 / REQUEST_DELAY / BATCH_DELAY / MAX_RETRY）| lessons/by-agent/nick_fury/lesson-2026-07-15-getnote-daily-limit-100.md |
| ~~lesson-2026-07-15-cron-delivery-explicit-feishu~~ | ~~Lesson~~ | **已合并到 L-35**（保留文件作为历史记录）| lessons/by-agent/nick_fury/lesson-2026-07-15-cron-delivery-explicit-feishu.md |

**7-15 根因（9:05 修正版）**：
- ❌ 错版（9:00 写）：假设 "Target=main vs isolated" 是根因
- ✅ 真根因（三层）：L1 22 个 cron `mode=announce, channel=last` 投递失败（缺 feishu target） + L2 5 个 cron argv 指向已删脚本 + L3 lark-cli token needs_refresh（auto-refresh 工作正常）
- 派蒙也用 `Target=isolated`（看 派蒙-T3prime-自查-DAY = b0be1eaa）→ isolated 不是问题
- 派蒙投递成功靠 `delivery.mode=none, channel=feishu, to=user:ou_xxx` 三件套

**7-15 应急闭环**（9:05）：手动跑 `scripts/daily_tech_report.py` → lark-cli ✅ + wiki ✅ → 文博已收到科技日报

**7-15 根因修正**：LEADER 凌晨 01:10 假设"Target=main vs isolated"是错的。**真实根因**：`announce -> last` 找 main session route 失败 → fail-closed；派蒙用显式 feishu 推送，无 main session 依赖。详见 INC-001 §根因。

---

## 📌 7-14 增量

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-14_001 | Incident | ETF 速览分位数据 18 天失真（hardcoded 预设） | incidents/2026-07/inc_2026-07-14_001-etf-18-day-mock-data.md |
| inc_2026-07-14_002 | Incident | fetcher v1.0 算法根本错误（价格分位 ≠ 估值分位） | incidents/2026-07/inc_2026-07-14_002-fetcher-price-vs-valuation.md |
| inc_2026-07-14_003 | Incident | 7 天 review-log 真空（写错路径） | incidents/2026-07/inc_2026-07-14_003-7-day-review-log-vacuum.md |
| inc_2026-07-14_004 | Incident | Get 笔记 → Wiki 静默 50 天 | incidents/2026-07/inc_2026-07-14_004-getnote-wiki-sync-50d-vacuum.md |
| inc_2026-07-14_005 | Incident | C-4 同步对账检查机制上线 | incidents/2026-07/inc_2026-07-14_005-c3-sync-check-implementation.md |
| inc_2026-07-14_006 | Incident | launchd → OpenClaw cron 迁移（14 plist disable） | incidents/2026-07/inc_2026-07-14_006-launchd-vs-openclaw-cron-migration.md |
| lesson-2026-07-14-inc-archive-path | Lesson | INC/lesson 必须立即归档到 review-logs 子目录 | lessons/by-agent/nick_fury/lesson-2026-07-14-inc-archive-path.md |
| lesson-2026-07-14-mvp-data-source-validation | Lesson | 多源兜底 raise + 自检区分"输出/输入真实" | lessons/by-agent/nick_fury/lesson-2026-07-14-mvp-data-source-validation.md |
| lesson-2026-07-14-sync-script-three-check | Lesson | 同步脚本 3 必检 — 不 hardcode / 不 swallow / 必对账 | lessons/by-agent/nick_fury/lesson-2026-07-14-sync-script-three-check.md |
| lesson-2026-07-14-valuation-not-price | Lesson | 估值分位 ≠ 价格分位 — PE/PEG/EV/EBITDA 才是估值根本 | lessons/by-agent/nick_fury/lesson-2026-07-14-valuation-not-price.md |

## 🔗 历史 lessons (6 月 ~ 7-13)

| 日期 | Lesson |
|:---|:---|
| 7-03 | lesson-2026-07-03-rss-tech-pipeline-4-layer-bug.md |
| 7-02 | lesson-2026-07-02-push-idempotency-dedup.md |
| 7-02 | lesson-2026-07-02-lark-cli-launchd-context.md |
| 7-02 | lesson-2026-07-02-data-flow-break-mock-fallback.md |
| 7-01 | lesson-2026-07-01-script-whitelist.md |
| 7-01 | lesson-2026-07-01-read-before-write.md |
| 7-01 | lesson-2026-07-01-lark-cli-scope.md |
| 6-30 | lesson-2026-06-30-openclaw-native-first.md |
| 6-29 | lesson-2026-06-29-c3-fix-mvp.md |
| 6-29 | lesson-2026-06-29-daily-9d-vacuum.md |
| 6-23 | lesson-2026-06-23-launchd-plist-repair.md |
| 6-19 | les_2026-06-19_001-morning-daily-c3-治本不完整.md |
| 6-18 | les_2026-06-18_001-c3-cron-late.md |
| 5-07 | les_2026-05-07_001.md |

## 🔗 历史 INC (Nick 相关)

| 日期 | INC |
|:---|:---|
| 7-03 | inc_2026-07-03-002-rss-tech-report-path-break-and-5-zero-select.md |
| 7-02 | inc_2026-07-02-001-lark-cli-launchd-push-fail.md |
| 7-02 | inc_2026-07-02-002-rss-push-duplicate.md |
| 7-02 | inc_2026-07-02-003-intelligence-json-mock-pollution.md |
| 7-01 | inc_2026-07-01_001-morning-rss-etf-push-failed.md |
| 6-30 | inc_2026-06-30_001-launchd-to-openclaw-cron-migration.md |
| 6-29 | inc_2026-06-29_001-daily-9d-vacuum-c3-alert-silent.md |
| 6-23 | inc_2026-06-23_001-launchd-11-plists-permissionerror.md |
| 6-21 | inc_2026-06-21_001-pm-patrol-weekend-4-agent-silent.md |
| 6-19 | inc_2026-06-19_001-morning-daily-missing.md |

---

## 🪞 11 天真空反思 (2026-07-03 → 2026-07-13)

7-3 ~ 7-13 期间 Nick 没有新 INC/lessons 写入 review-logs（但 7-1 ~ 7-3 是密集期）。
可能根因：
- C-3 21:00 自检 cron 可能失灵（需要重新验证 plist）
- 或 lessons 没规范写入子目录（被压在根目录或别处）

修复动作 (7-14 13:52):
- 把今天 4 个文档移到规范路径（已 ✅）
- 建本 registry 防止再"沉底"

---

*维护: 任何新 INC/Lesson 必须在 24h 内写入对应子目录 + 本 registry*

### 7-14 13:55 增量（路径规范化第二轮）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-14_003 | Incident | review-logs 7-4~7-13 11 天真空（落盘≠被引用·路径错位）| incidents/2026-07/inc_2026-07-14_003-7-day-review-log-vacuum.md |
| lesson-2026-07-14-inc-archive-path | Lesson | INC/lesson 必须立即归档到 review-logs 子目录 | lessons/by-agent/nick_fury/lesson-2026-07-14-inc-archive-path.md |

### 历史 INC 补归档（13:55 已做）

| 原 INC | 原路径 | 现路径 |
|:---|:---|:---|
| INC-2026-07-06-001 | /05_AgentOutput/.../INC/INC-2026-07-06-001_technical_report_repeat.md | incidents/2026-07/inc_2026-07-06-001-tech-report-repeat-rss-vacuum.md |
| L-24/L-25/L-26 | /05_AgentOutput/.../lessons/2026-07-06_lessons_L24-L26.md | lessons/by-agent/nick_fury/lesson-2026-07-06-rss-tech-pipeline-4-layer-bug.md |

### 待补写（7-4~7-13 真空期间漏的）

| 日期 | 事件 | 待写 |
|:---|:---|:---|
| 7-8 | getnote 静默失败 + intelligence.json mock | INC 待写 |
| 7-10 | launchd 2/3 通道 5 天持续 | INC 待写 |
| 7-12 | 3 个 plist exit 1 + 数据 pipeline 真空 | INC 待写 |
| 7-13 | 3 个 plist exit 1 连续 2 天 升级 Critical | INC 待写 |

### 7-14 14:05 增量（同步链路修复）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-14_004 | Incident | Get 笔记 → Wiki 同步静默失败 50 天（hardcode + error swallow）| incidents/2026-07/inc_2026-07-14_004-getnote-wiki-sync-50d-vacuum.md |
| lesson-2026-07-14-sync-script-three-check | Lesson | 同步脚本 3 必检—不 hardcode / 不 swallow / 必对账 | lessons/by-agent/nick_fury/lesson-2026-07-14-sync-script-three-check.md |

### 同步链路修复成果（14:03:57 跑通）

- v2.0 `getnote_ej9_to_wiki.py` 重写完成（不 hardcode / 不 swallow / 状态 JSON 对账）
- API 端 20 条全部 fetch ✅
- 高价值 20 条全部写入 `wiki/insights/ai-technology/`
- 50 天缺口一次性补完（最重磅：Anthropic Fiona Fung / Noam Brown / YC Pete Koomen / Lenny 访谈）
- 异常路径测试：env 损坏立即 raise RuntimeError

### 7-14 14:15 增量（C-3 + C-4 同步对账检查机制）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-14_005 | Incident | C-3 自检增加 Get 笔记 → Wiki 同步对账检查 | incidents/2026-07/inc_2026-07-14_005-c3-sync-check-implementation.md |

### C-3 升级成果

- ✅ C-4 检查项集成到 `scripts/c3_daily_check.py`
- ✅ 端到端测试: 正常路径 ✅ / 5 条未同步 → exit 1 + 飞书推送 ✅
- ✅ L-32 治本机制 "必对账" 已实际部署（明早 21:00 自动监控）
- ✅ 顺手修复 PosixPath 不能直接 open + write_log 多参数兼容

### 7-14 17:25 增量（L-13 治本：launchd → OpenClaw cron 迁移）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-14_006 | Incident | 18 launchd plist vs OpenClaw cron 重复（15/18 重复）| incidents/2026-07/inc_2026-07-14_006-launchd-vs-openclaw-cron-migration.md |

### 迁移计划（14:20 文博要求）

- 15 个 launchd plist 重复 → disable（保留 OpenClaw cron）
- 3 个 launchd 专属保留（wiki-health-check / wiki.monthly-refresher / bestpractice.daily）
- AGENTS.md §0.5 写入强制 "openclaw cron list | grep" 流程

### 7-14 18:36 INC-006 闭环（launchd → OpenClaw cron 批量 disable）

- ✅ 14 个重复 launchd plist 全部 disable (bootout + 移到 _disabled_2026-07-14/)
- ✅ 4 个 launchd 专属保留 (wiki-health-check / wiki.monthly-refresher / bestpractice.daily / bestpractice.daily.collect)
- ✅ 备份: Wiki `_deprecated/2026-07-14/launchd_disabled/` + Scripts `_deprecated/2026-07-14/launchd_plists_backup/` (各 14 个)
- ✅ INC-006 转 Closed
- ✅ AGENTS.md §0.5 同步更新（14/18 而不是 15/18）

**禁用脚本**: `/tmp/disable_duplicate_launchd_2026-07-14.sh` (82 行, 失败 0)
**恢复方法**: 见 INC-006 "恢复方法" 段
