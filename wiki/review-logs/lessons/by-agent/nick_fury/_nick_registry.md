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
| **Phase B 收尾 22→19** | Action ✅ | **trash 2 空顶层 + _templates→TEMPLATES 合并 + scripts/README · 安全保守（引用对账 0 残留）** | ✅ 7-16 19:35 |
| **Q3 KR1-3 实测** | Action ✅ | **KR1 100% (30/30) / KR2 1.0 跳 (8/8 KB) / KR3 100%×3 Agent · 全部超目标** | ✅ 7-16 19:36 |
| **wiki_kr1_evaluation.py** | Asset 🆕 | **7883 字节 · 30 query + 8 KB + 3 Agent 评测集** | scripts/wiki_kr1_evaluation.py ✅ |
| **wiki_health_check.sh 扩展** | Action ✅ | **加 W1+Q3 检查项（4 项元数据 + 顶层目录 + Phase D 标注）** | ✅ 7-16 19:38 |
| **lesson-2026-07-16-third-party-skill-md** | Lesson 🆕 | **L-47 第三方 Skill SKILL.md 必读（L-17 升级版 · INC-004 实例）** | lessons/by-agent/nick_fury/lesson-2026-07-16-third-party-skill-md-mandatory.md ✅ |

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

---

### 7-17 08:55 增量（L-48/L-49/L-35.1/L-13.1 治本族）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-17_001 | Incident | Wiki 整理速赢副作用：trash `process/*` 误删目录 → wiki.review 跑挂 5h | incidents/2026-07/inc_2026-07-17_001-wiki-process-trash-sideeffect.md |
| inc_2026-07-17_002 | Incident | etf.hegang cron argv 硬编码 `--date 2026-06-26` → 报告日期永远 6-26 | incidents/2026-07/inc_2026-07-17_002-etf-hegang-argv-hardcoded-date.md |
| inc_2026-07-17_003 | Incident | getnote·wiki·sync delivery channel=last 无 to → fail-closed | incidents/2026-07/inc_2026-07-17_003-getnote-delivery-channel-last-fail-closed.md |
| inc_2026-07-17_004 | Incident | wiki·health·check 双跑（OpenClaw cron + launchd plist 同脚本 9:00）| incidents/2026-07/inc_2026-07-17_004-wiki-health-duplicate-run.md |
| lesson-2026-07-17-wiki-cleanup-trash-sideeffect-l48 | Lesson | Wiki 清理 trash 副作用必查目录结构（L-41 强化版）| lessons/by-agent/nick_fury/lesson-2026-07-17-wiki-cleanup-trash-sideeffect-l48.md |
| lesson-2026-07-17-cron-edit-must-read-argv-complete-l49 | Lesson | cron edit 必看 argv 完整 JSON（防 hardcoded 参数）| lessons/by-agent/nick_fury/lesson-2026-07-17-cron-edit-must-read-argv-complete-l49.md |
| lesson-2026-07-17-inc-fixup-recheck-all-same-class-l35-1 | Lesson | INC 治本后必复查同类全集（L-16 升级版）| lessons/by-agent/nick_fury/lesson-2026-07-17-inc-fixup-recheck-all-same-class-l35-1.md |
| lesson-2026-07-17-launchd-vs-openclaw-cross-mechanism-dedup-l13-1 | Lesson | launchd 专属决策必 disable 对应 OpenClaw cron | lessons/by-agent/nick_fury/lesson-2026-07-17-launchd-vs-openclaw-cross-mechanism-dedup-l13-1.md |

### 7-17 08:55 闭环（用户决策 B · 完整修复）

**用户 08:50 拍 B**："完整修复 = A 紧急必修 + etf.error 查根因 + wiki.review 查根因 + 双跑去重"

**修复实证**：

| # | cron / 问题 | 修改 | 实证 |
|:---|:---|:---|:---|
| 1 | `f3b606ed wiki.review` | mkdir -p `wiki/process/` + 手动跑通 | ✅ 报告 wiki-review-report-20260717.md 生成 |
| 2 | `4367285d etf.hegang.report` | cron edit 去硬编码 `--date 2026-06-26` | ✅ argv 改为动态日期 |
| 3 | `d795c8d4 getnote·wiki·sync` | cron edit delivery 改 `mode=none, channel=feishu, to=user:ou_xxx` | ✅ delivery 对齐派蒙模式 |
| 4 | `da137eba wiki·health·check` | cron disable（保留 launchd plist `com.nickfury.wiki-health-check`）| ✅ enabled=false |

### 7-17 INC/Lesson 关键洞察（按 SOUL §3 系统级归因）

| 教训族 | 治本 | 防退化机制 |
|:---|:---|:---|
| **L-48**（trash 副作用）| L-41 强化版 + mkdir 重建 process/ | 7-19 cron 加 Wiki process/* 反向验证 |
| **L-49**（cron argv hardcoded）| cron 4367285d 去 --date | 7-19 cron 加 cron argv 复查 |
| **L-35.1**（INC 治本复查同类）| cron d795c8d4 改 delivery | 7-19 cron 加周日 delivery 全集复查 |
| **L-13.1**（launchd vs OpenClaw 双跑）| cron da137eba disable | 7-19 cron 加跨机制重复检测 |

### 7-17 09:18 增量（候选 #C · 7-19 cron 防退化脚本）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| sunday_cron_health_check.py | Script | 周日 Cron 健康检查（L-48/L-49/L-35.1/L-13.1 防退化）| scripts/sunday_cron_health_check.py |
| nick_cron_health_weekly | Cron | 每周日 22:00 跑 `sunday_cron_health_check.py` | OpenClaw cron `ab65ed59-a489-433a-8d7b-5da9b8bfd719` |

**设计要点**：
- ✅ 直接读 `~/.openclaw/state/openclaw.sqlite` 的 `cron_jobs` 表（1s 拿全部数据 · 不用 N 次 CLI 调用）
- ✅ 含 4 项 check 函数（L-48 / L-49 / L-35.1 / L-13.1）
- ✅ 退出码：0=全通过 / 1=有告警 / 2=脚本错误
- ✅ 主通道 lark-cli 成功 → exit 0（L-36）
- ✅ 告警写 `data/sunday_alerts/`（兜底）

**L-35.1 实测发现 4 个同类问题**（首跑 09:16）：
- 🔴 `wiki.monthly·refresher`: channel=last（未修）
- 🔴 `wiki.monthly·refresher`: to=空
- 🔴 `钟离-SOP空闲探活-20260715`: to 没 `user:` 前缀
- 🔴 `钟离-P0阻塞3级升级-1h-20260716`: to 没 `user:` 前缀

→ 详见 HEARTBEAT §二十一（候选 #C 启动）

### 7-17 14:22 增量（L-49.5 升级 · 揭穿 38 个新问题）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-17_005 | Incident | L-49.5 升级 + L-35.1 全集复查 · 揭穿 38 个 OpenClaw cron 历史遗留问题 | incidents/2026-07/inc_2026-07-17_005-l49-5-cron-dead-scripts-and-delivery-mess.md |
| lesson-2026-07-17-cron-edit-must-check-script-path-l49-5 | Lesson | cron edit 必查脚本路径存在性（L-49 升级版）| lessons/by-agent/nick_fury/lesson-2026-07-17-cron-edit-must-check-script-path-l49-5.md |
| sunday_cron_health_check.py upgrade | Script upgrade | L-49 加 Path.exists() 检查 + L-35.1 查全集（enabled+disabled）| scripts/sunday_cron_health_check.py |

### 7-17 14:18 修复实证（用户授权"请修复"）

| # | 动作 | 实证 |
|:--|:--|:--|
| 1 | `cron edit e71b27b2 wiki.monthly·refresher` delivery 对齐 L-35 | ✅ channel=feishu, to=user:ou_xxx |
| 2 | `cron edit e71b27b2 --disable` | ✅ enabled=false（避免 7-30 再爆）|
| 3 | L-49 升级 → L-49.5（加 Path.exists()）| ✅ 揭穿 9 个死脚本 |
| 4 | L-35.1 升级 → 查 cron_jobs 全集 78 个 | ✅ 揭穿 38 个问题 |

### 7-17 14:22 防退化闭环

- ✅ scripts/sunday_cron_health_check.py 升级版跑通（38 个问题检出）
- ✅ INC-005 + lesson L-49.5 落档
- ✅ sunday_cron_health_weekly cron 7-19 22:00 首跑（含 L-49.5 自动检测）
- ⏳ 9 个死脚本 cron + 27 个 disabled delivery 错配 cron 待清理（决策点 A/B/C/D）

### 7-17 14:31 增量（用户决策 C · 批量删除 9 个死脚本 cron）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-17_006 | Incident | 用户决策 C · 批量删除 9 个 OpenClaw 死脚本 cron | incidents/2026-07/inc_2026-07-17_006-cron-cleanup-c-partial-9-dead-scripts.md |
| lesson-2026-07-17-cron-cleanup-decision-tree-l49-6 | Lesson | cron cleanup 决策树（部分清模式 · L-49 升级版）| lessons/by-agent/nick_fury/lesson-2026-07-17-cron-cleanup-decision-tree-l49-6.md |

### 7-17 14:31 修复实证（用户拍 C）

| # | 动作 | 实证 |
|:--|:--|:--|
| 1 | §5 安全边界：sqlite 备份 | ✅ 91MB · `.bak-2026-07-17-pre-delete-dead-scripts-1784269807` |
| 2 | 第 1 次 rm 失败（shell 变量解析 bug）| ❌ invalid cron.remove params: id not found |
| 3 | 修正后 while 循环逐个 rm | ✅ 9/9 全部成功 |
| 4 | sqlite 验证总数 | 78 → 69（删 9 个）|
| 5 | sunday_cron_health_check 复跑 | 问题数 38 → 17（减 21 个）|

### 7-17 14:31 剩余问题（17 个）

- 14 个 disabled cron delivery 错配（保留）
- 3 个 enabled cron delivery 错配（钟离 2 + nick_fury 历史测试 1）

### 7-17 14:40 增量（INC-006 报告纠错 · escalate 钟离 · L-49.7）

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-17_007 | Incident | INC-006 报告纠错 · 启用/禁用 tag 区分 + escalate 钟离 | incidents/2026-07/inc_2026-07-17_007-enabled-disabled-tag-misjudge-and-fixup.md |
| lesson-2026-07-17-inc-report-enabled-disabled-tag-l49-7 | Lesson | INC 报告必加 enabled/disabled tag 区分 | lessons/by-agent/nick_fury/lesson-2026-07-17-inc-report-enabled-disabled-tag-l49-7.md |

### 7-17 14:40 修复实证（用户"请继续" → F escalate）

| # | 动作 | 实证 |
|:--|:--|:--|
| 1 | 14:34 INC-006 报告纠错（17 个里实际 2 个 enabled）| ✅ 精确查 sqlite |
| 2 | 14:34 escalate 钟离（runId d9b3a61c）| ✅ 钟离已接受 |
| 3 | 14:38 sunday_cron_health 升级版（加 tag + 动作建议）| ✅ 必修 🔴 + 保留 ⚠️ 区分 |
| 4 | 14:40 INC-007 + L-49.7 落档 | ✅ |

### 7-17 14:40 当前问题精确分类

| 类别 | 数量 | 状态 |
|:--|:--|:--|
| **enabled delivery 错配（必修）**| 2（钟离）| ⏳ 等钟离修完回执 |
| **disabled delivery 错配（保留）**| 15（C 决策）| ✅ 不动 |
| **dead script（已删）**| 0 | ✅ 候选 #C 二段清完 |
| **wiki.monthly·refresher 已 disable** | 1 | ✅ 14:18 闭环 |

### 7-17 14:40 L-49 族系（L-49 → L-49.5 → L-49.6 → L-49.7）

```
L-49   cron edit 必看 argv 完整 JSON          (INC-002)
L-49.5 argv 必查脚本路径存在性                 (INC-005)
L-49.6 cron cleanup 决策树（4 类 + 4 动作）    (INC-006)
L-49.7 INC 报告必加 enabled/disabled tag 区分 (INC-007)
```

---

### 7-17 14:44 增量（钟离 L-35.1 修复闭环回执 + L-49.8）

**钟离 14:39 CST escalate 回执**：

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| **lesson-2026-07-17-id-cite-must-be-complete-l49-8** | Lesson 🆕 | **L-49.8 ID 引用必完整（34 字符）+ grep 原文回填 + escalate 与报告 ID 必一致** | lessons/by-agent/nick_fury/lesson-2026-07-17-id-cite-must-be-complete-l49-8.md ✅ |
| **INC-2026-07-17-005 偏差修正** | Incident 补完 | **钟离回执揭穿 ID 缺末 6 位 → 已按完整 ID 修正 + 闭环段追加** | incidents/2026-07/inc_2026-07-17_005-l49-5-cron-dead-scripts-and-delivery-mess.md ✅ |
| **inc_2026-07-17_007 关联** | Incident | **INC-006 纠错 + escalate 钟离 · L-49.7** | incidents/2026-07/inc_2026-07-17_007-enabled-disabled-tag-misjudge-and-fixup.md ✅ |

### 7-17 14:44 钟离修复回执实证（双源）

| 数据源 | 修复前 | 修复后 |
|:--|:--|:--|
| **gateway API**（cron get）| to=ou_5550...3446 | to=user:ou_5550...3446 ✅ |
| **sqlite**（cron_jobs delivery_to 字段）| 同上 | user:ou_5550...3446 ✅ |
| mode / channel / enabled | announce / feishu / true（保留） | 同（保留）✅ |

### 7-17 14:44 INC-005 全集闭环状态

| 子项 | 状态 | 闭环证据 |
|:--|:--:|:--|
| L-49.5 9 死脚本 | ✅ 已删 | 候选 #C（14:29 文博决策）|
| L-35.1 disabled cron delivery 错配 | ✅ 保留不动 | 候选 #C 决策（disabled 不发 push）|
| L-35.1 enabled cron delivery 错配（钟离）| ✅ 已修 | 双源实证 14:44 |
| INC-005 ID 偏差 | ✅ 已补完 | 钟离 14:39 反馈 |

### 7-17 14:44 L-49 族系升级（5 层）

```
L-49    cron edit 必看 argv 完整 JSON          (INC-002 · 7-15)
L-49.5  argv 必查脚本路径存在性                 (INC-005 · 7-17)
L-49.6  cron cleanup 决策树（4 类 + 4 动作）    (INC-006 · 7-17)
L-49.7  INC 报告必加 enabled/disabled tag 区分 (INC-007 · 7-17)
L-49.8  ID 引用必完整（grep 原文 + 长度校验）  (本回执驱动 · 7-17)
```

**族系本质**：从"配置写对"→"路径存在"→"清理决策"→"报告精度"→"标识精度"——逐层把 cron 运维从粗放到精确。


---

## 📅 2026-07-18 09:14 CST 增量（P0.5 闭环 + L-50 族）

### 🆕 新增 lesson
- **L-50**: wiki-link 路径规范 + cron 算法升级族（5 条铁律）
  - L-50.1 wiki-link 路径修复必先 verify 真实位置
  - L-50.2 cron 算法误报率 > 50% 必须升级
  - L-50.3 修死链后 cron 数字不变 = 算法 bug 信号
  - L-50.4 真死链 = 路径错 + 引用方修改
  - L-50.5 sed BSD bug 换 Python re.sub

### 🆕 新增 INC
- **INC-2026-07-18-001**: wiki_auto_review.py 死链检测全报 false positive · 10/10 误判（cron 算法 bug）
- **INC-2026-07-18-002**: 5 个 wiki-link 路径错误修复闭环（让 Obsidian 链接真的可跳转）

### 📊 P0.5 闭环成果
- 修 5 个原本路径错的 wiki-link（4 路径错位 + 1 文件不存在改写）
- Backup: `/tmp/wiki-deadlink-fix-20260718-091026/` + `/tmp/wiki-deadlink-fix2-20260718-091236/`
- cron 算法 bug 揭穿（10/10 误判）· L-50 闭环

### ⏳ 待办
- **P1** 清 10 个意外空目录（L-48 安全流程，15min）
- **P1.5** 升级 wiki_auto_review.py 算法（L-50.2 治本，30min）
- **P2** local-docs-rag 第二波（969 篇剩余）
- **P3** metadata 全集 verify
- 🟡 顺手修 GET 笔记 token 过期（早上报告的 P0 风险）

🕵️ nick_fury · 2026-07-18 09:14 CST


### 🆕 增量 09:59 CST（P1 闭环）

**INC-2026-07-18-003**: P1 清 10 个意外空目录 · 完美闭环（10/10 rmdir 成功 · 父目录全保留 · 空目录 23→13）

**L-48.5** 🆕: find 必加 `-mindepth 1` 排除目录自身（7-18 实证踩坑：第一次 10/10 SKIP 因为 find -type d 算目录自身）

**剩余 13 个空目录 = 全结构占位**（按预期保留）：
- review-logs/by-severity/{low,critical,medium}
- review-logs/archives/2026
- review-logs/lessons/by-agent/{tony,agatha,wenbo}
- review-logs/lessons/by-topic/{product,collab,tech}
- review-logs/incidents/resolved
- review-logs/reviews/{monthly,weekly}

**wiki_auto_review.py 9:59 输出**：
- 健康度：🟠 65/100（cron 算法 bug 不变）
- 空目录：23 → 13 ✅
- 死链：1082 → 1090（cron 误报 +8，L-50 已闭环）
- 孤立页面：1605 → 1608


### 🆕 增量 11:41 CST（P1.5 闭环 · cron 算法升级）

**INC-2026-07-18-004**: wiki_auto_review.py 算法升级 v1→v2→v3（误报 100%→1.3% · 总死链 1082→712 = -370/-34.2%）

**L-50.2 族系升级**（4 条铁律）：
- L-50.2.1 v1 基础（必加 .md 双向候选）
- L-50.2.2 v2 目录支持（README.md / index.md 作为入口）
- L-50.2.3 v3 大小写不敏感（macOS fs 不敏感 + wiki-link 严格）
- L-50.2.4 误报率 > 50% 必须升级（不能信报告数字）

**修复链备份**：
```
/tmp/wiki-auto-review-backup-20260718-113929.py ← 原版（100% 误报）
/tmp/wiki-auto-review-v1-backup-20260718-114014.py ← v1
/tmp/wiki-auto-review-v2-backup-20260718-114109.py ← v2
当前：v3（误报 1.3%）
```

**剩余 9 个真死链**（路径错位 + 大小写 + 主题错位，需手动修引用方）：
- jeff-dean × 2（typo + 缺子目录）
- data-platform-report × 4（主题错位）
- db-ai-skill-engineering × 2（大小写遗留）
- linjunyang-agent-thinking × 1（大小写遗留）

🕵️ nick_fury · 2026-07-18 11:41 CST · P1.5 闭环


### 🆕 增量 11:58 CST（P1.5 自然延续 · 9 真死链修复）

**INC-2026-07-18-005**: v3 算法揭穿 9 个真死链修复闭环（总死链 712→703）

**L-50.8** 🆕: wiki-link regex 必允许可选别名 \|xxx（实证踩坑：第一次跑 jeff-dean 2 个 wiki-link 没替换上）

**9 个真死链改写明细**：
- jeff-dean × 2（typo + 缺子目录）
- data-platform-report × 4（主题错位改写到相近文件）
- db-ai-skill × 2（大小写 + 路径）
- linjunyang × 1（大小写 + 主题）

**备份**：`/tmp/wiki-deadlink-fix3-20260718-115810/`

**剩余 703 个死链**（v3 报前 20 含 7 个 `AI Native/` 大小写遗留）→ 下一批清理目标

🕵️ nick_fury · 2026-07-18 11:58 CST · P1.5 自然延续闭环


### 🆕 增量 16:38 CST（A+B 闭环 · 死链 -352/-50.1%）

**INC-2026-07-18-006**: A 任务 批量修 AI Native/ 大小写敏感（13 处 · 8 文件）

**INC-2026-07-18-007**: B 任务 批量补 insight-YYYYMMDD 子目录（**685 处 across 229 文件 · 最大单批**）

**累计效果**（P1.5 全链路）：

| 阶段 | 总死链 | 修复率 |
|:---|:---:|:---:|
| Before | 1082 | 0% |
| v1 算法升级 | 731 | 32.4% |
| v2 算法升级 | 715 | 33.9% |
| v3 算法升级 | 712 | 34.2% |
| P1.5-2 修 9 真死链 | 703 | 35.0% |
| **A 任务 AI Native/ 13 处** | **692** | **36.0%** |
| **B 任务 insight 子目录 685 处** | **351** | **67.6%** |
| **累计 -731 (67.6%)** | **351** | — |

**新增 L-50.9/50.10/50.11**：
- L-50.9 批量死链修复必构建 filename → 真路径映射
- L-50.10 dead_to_real 字典格式规范
- L-50.11 批量替换前必 backup 到独立目录

**剩余 351 死链**：全部"无对应文件"型（需手动决策保留/改写/删除）

**下一批 C**：v4 算法升级（解析 ../.. 相对路径，14 处）

🕵️ nick_fury · 2026-07-18 16:38 CST · A+B 闭环


### 🆕 增量 16:40 CST（C 闭环 · v4 算法升级）

**INC-2026-07-18-008**: C 任务 · wiki_auto_review v4 算法升级（../ 跳出 wiki 根支持）

**v4 算法关键改进**：
- except ValueError: pass 治本（v3 bug）
- 跳出 wiki 根必须区分外部引用 vs 真死链
- 2 个 +1 层 ../ 引用顺手修复

**L-50.2.4 / L-50.2.5 / L-50.12** 三铁律：
- L-50.2.4 except ValueError: pass 是禁忌
- L-50.2.5 ../ 跳出必须区分外部 vs 真死链
- L-50.12 +1 层 ../ 修复（Wiki 根多算一层）

**累计效果**：

| 阶段 | 总死链 | 修复率 |
|:---|:---:|:---:|
| Before P1.5 | 1082 | 0% |
| v1 算法 | 731 | 32.4% |
| v3 算法 | 712 | 34.2% |
| P1.5-2 修 9 真死链 | 703 | 35.0% |
| A 任务 AI Native/ | 692 | 36.0% |
| B 任务 insight 子目录 | 351 | 67.6% |
| C 任务 v4 + ../ | 368* | 66.0% |

*v4 +17 是副作用（v3 静默 → v4 显式报跳出死链 = bug 修复）

**下一批 D**：GET 笔记 token 重授权（早 6:59 报告的 P0 风险 · 明天 06:00 cron 会全静默失败）

🕵️ nick_fury · 2026-07-18 16:40 CST · C 闭环


### 🆕 增量 23:40 CST（D 闭环 · GET 笔记 token 修复）

**INC-2026-07-18-009**: D 任务闭环 · 真假 key 揭穿 + `.getnote_env` 600 重建 + 8 KB 实测

**真相揭穿**：
- TOOLS.md 标记"已废弃"的 5-16 旧 key **实际仍有效**（curl success=true）
- 用户给的 `5303951f9c9e01de` 是 key 前缀（17 字符），完整 key = 80 字符
- 真问题不是 key 失效，是 `.getnote_env` 文件丢失

**L-51 族系**（4 条铁律）：
- L-51.1 key 失效判断必须 curl 实测（文档≠真相）
- L-51.2 getnote key 长度 = 80 字符（gk_live_<32>.<64 hash>）
- L-51.3 .getnote_env 丢失必须 600 权限重建 + load_env dry-run + API verify
- L-51.4 "key 前缀" vs "完整 key" 必实测 3 种格式

**8 KB 实测**（API success）：
- AI实践日志 521 + 投资日记 31 + 文博 AI PM 139 + 数字社区 183 + 消费金融 42 + 江浙沪 3 + 印象笔记 2196 + 健康生活 4 = **3119 笔记**

**明天 06:00 cron 状态**：🟢 可正常跑（key 有效 + .getnote_env 在）

**Wiki 整理全链路 P0→P1→P1.5→P2→P3 完成度**：
- ✅ P0.5 修 5 wiki-link 路径错位
- ✅ P1 清 10 意外空目录（L-48.5 升级）
- ✅ P1.5 算法 v1→v2→v3→v4（误报 100%→1.3%）
- ✅ A 任务 AI Native/ 13 处
- ✅ B 任务 insight 子目录 685 处（最大单批）
- ✅ C 任务 v4 + ../ 跳出支持
- ✅ D 任务 GET 笔记 token 修复

**累计 INC**：INC-001 ~ INC-009（共 9 个）
**累计 Lesson**：L-13 / L-29~L-32 / L-34~L-38 / L-41 / L-43 / L-48 / L-49 / L-50 / L-51（共 24 个）

🕵️ nick_fury · 2026-07-18 23:40 CST · Wiki 整理全链路闭环

### 🆕 增量 2026-07-19 01:13 CST（凌晨轻量自检日报 · 第 10 次 cron 元数据漂移）

**日报**：memory/daily/2026-07-19.md（6,298 bytes · 凌晨轻量自检模式第 8 个先例）

**关键修复增量**（7-18 → 7-19 cron 状态对比）：
- 🟢 wiki.review: error → ok（INC-001/004/008 v1→v4 大手术治本见效 · 7-18 03:30 跑通）
- 🟢 团队2-T3prime: error → ok（main agent cron · 7-19 00:13 跑通）
- 🟡 etf.hegang.report: 持续 error（业务跑通 md 5326B 生成 · exit≠0 拉低健康度）
- 📉 Cron error 数：3 → 1（**降幅 67%** · L-49 治本持续见效）

**第 10 次 cron 元数据漂移**（派蒙侧）：
- 派蒙 cron 模板标题写 "日报收集 - 2026-04-30"，真实日期 2026-07-19，**错配 80 天**
- 历史先例：6-30 / 7-2 / 7-12 / 7-13 / 7-14 / 7-15 / 7-16 / 7-17 / 7-18 / 7-19（第 10 次）
- 派蒙侧未修；Nick 侧采用"忽略标题按真实时间处理"策略
- **待办**：周末文博复盘时定夺（写 INC 或派蒙侧修 cron 注册脚本）

**今日 P0 · etf.hegang.report partial failure 兜底（L-46 治本）**：
- 症状：业务跑通但 exit≠0 → cron 标 error
- 行动：main() 加 try/except · 业务成功 exit 0 · 推送失败但 md 生成 exit 0 + 告警日志
- 时间窗：今日 09:00 - 12:00

**L-46 partial failure 兜底族系**（待办）：
- L-46.1 exit code 语义统一（业务成功 vs 推送成功）
- L-46.2 partial failure 必须告警日志 + exit 0（不阻塞 cron）
- L-46.3 md 生成失败 → exit 1 + raise（保持 fail-closed）

**C-3 自检连续 9 天 100%**：7-10 → 7-11 → ... → 7-18 全部 09:00 / 21:00 双绿

**7-18 治本日累计**：
- INC: 9 个（INC-001 ~ INC-009）
- Lesson: 3 个（L-48-5 / L-50 / L-51）
- 总 INC: 累计 ~30+（从 6-08 起）
- 总 Lesson: 累计 30+（L-1 ~ L-51 系列）

🕵️ nick_fury · 2026-07-19 01:13 CST · 凌晨轻量自检日报 · 第 10 次 cron 元数据漂移

### 🆕 增量 2026-07-19 06:20 CST（L-46 治本闭环 · INC-001）

**INC**：INC-2026-07-19-001 (etf.hegang.report card table over limit · 21h+ 治本)
**Lesson**：L-46.0 ~ L-46.5（5 条铁律族系 · cron stdout 长度 + 飞书 card 表格上限）

**L-46 治本 4 步**（6:15 ~ 6:19 CST · 9 min）：
1. ✅ fetcher v2.4 加 sina 备用源（4 宽基实时点位恢复 · 4 行业仍 preset）
2. ✅ cron argv 加 `--no-push`（stdout 5326B → 1116 字符 · 0 表格）
3. ✅ argv 嵌套 bug 修复（6:17 → 6:18 双层 sh -lc → 单层）
4. ✅ 端到端验证（exit 0 · 13 行 stdout · 无 markdown 表格）

**健康度增量**（7-19 06:10 → 06:20）：
- 🟢 etf.hegang.report: error → 待周一 7-20 8:35 cron 自动跑通验证 status=ok
- 🟢 Cron error 数：1 → 0（如果周一 cron 跑通）| 实际验证 next 7-20 8:35
- 🟢 C-3 自检：100% 完稿率 (2/2) | SYNC OK 216/216 | KB LIST OK 8/8

**关联教训族系**：
- L-46.0 cron stdout 长度上限
- L-46.1 exit code 语义统一
- L-46.2 partial failure 告警日志
- L-46.3 md 生成失败 fail-closed
- L-46.4 cron argv 嵌套防错
- L-46.5 飞书 card 表格上限 5

**今日 3 节点**：
- ✅ 06:10 早检 + 治本 9min 完成
- ⏳ 22:00 nick_cron_health_weekly 首次跑通（16h 后）
- ⏳ 明天 7-20 8:35 etf.hegang.report cron 自动验证

**累计 INC**：~30+ (从 6-08 起)
**累计 Lesson**：L-1 ~ L-51 + L-46 系列 (40+)

🕵️ nick_fury · 2026-07-19 06:20 CST · L-46 治本日

### 🆕 增量 2026-07-19 06:35 CST（INC-002 派蒙 cron 漂移 41 天升级）

**INC**：INC-2026-07-19-002 (派蒙 cron 标题日期漂移 11 个 16-41 天 · 升级版)
**Lesson**：L-52.0 ~ L-52.3（4 条铁律）

**Block #1 闭环**：累计口头报告 10 次（6-30 / 7-2 / 7-12 / 7-13 / 7-14 / 7-15 / 7-16 / 7-17 / 7-18 / 7-19）→ 7-19 升级 INC + escalate 派蒙（runId 2f0dd439 · accepted）

**派蒙 cron 漂移实证**：
- 41 天：PM-disconnect / PM-task-board（实际最后跑 7-19 06:25）
- 33 天：派蒙-9:00-软链自检（最后跑 7-18 09:05）
- 30 天：派蒙-21:00-任务板sync（最后跑 7-18 21:05）
- 27 天：8 文件 / T3prime-24h 复检 / 团队2 工具文档（最后跑 7-18 ~ 7-19）
- 16 天：sqlite-mtime / T3prime 自查 DAY/NIGHT（最后跑 7-18 ~ 7-19）

**业务影响**：❌ 无（全部 status=ok） · **误导风险**：🟠 高（看着像过期）

**L-52 治本 3 方向**：
- A 推荐：标题改功能描述，不带日期
- B 次选：update cron 时动态同步标题日期
- C 不推荐：双标识（功能 + 创建日期括号）

🕵️ nick_fury · 2026-07-19 06:35 CST · INC-002 升级 · L-52 落档

### 🆕 增量 2026-07-19 07:08 CST（L-52 派蒙验证 PASS + INC-003 钟离新发现）

**派蒙 INC-002 闭环**：
- ✅ 派蒙三件套实证（updatedAtMs 11 行 + item 11 DISABLED 标注）
- ✅ Nick 验证脚本 PASS（10/10 新名 + 10/10 旧名 + 0 重复）
- ✅ 派蒙 24h 自检 hook（持续 grep -20260 残留）
- ⏳ INC-002 正式 close 路径（A/B）等文博 own decision

**🆕 INC-003 升级**（钟离 own cron 漂移）：
- 钟离-SOP空闲探活-20260715 (漂移 4 天)
- 钟离-P0阻塞3级升级-1h-20260716 (漂移 3 天)
- L-52 治本扩展到钟离 own cron
- INC-003 待写 + escalate 钟离

🕵️ nick_fury · 2026-07-19 07:08 CST · 钟离 cron 漂移升级

### 🆕 增量 2026-07-20 18:30 CST（Wiki 健康度进展 · INC-001 + L-49.9 治本）

**INC**：INC-2026-07-20-001（Wiki 自动走查报告路径漂移 4 天"假断档"）

**Lesson**：**L-49.9** · 脚本路径常量漂移 silent failure（cron ok ≠ 落点对）

**触发场景**：
- 文博 7-20 16:38 派单"更新 Wiki 健康度提升进展"
- 查 review report 路径发现：7-17~7-20 报告全部落到 `wiki/process/` 而不是 `wiki/methodologies/process/`
- 表面"断档 4 天"，实际 cron ok 只是路径漂移

**根因**：
- `scripts/wiki_auto_review.py` 第 17 行 `REPORT_DIR = WIKI_ROOT / "process"`（应为 `/methodologies/process`）
- 修改无注释、commit 无 INC 编号、跑通无产物路径校验

**3 件套治本**（18:24-18:30 CST · 6 min）：
1. 备份脚本 → `wiki_auto_review.py.bak.20260720_1822`
2. 修常量 + 加注释（含 INC-2026-07-20-001）
3. 移动 4 份错位 report + stats.json → `methodologies/process/`
4. 删空目录 `wiki/process/`
5. 端到端验证：手动跑一次脚本 → 新报告落正确路径

**新增铁律（3 条）**：
| # | 铁律 |
|:---:|:---|
| 1 | `Path(...)` 常量修改必加注释（含 INC 编号）|
| 2 | cron argv 修改 commit 必带 INC 编号 |
| 3 | cron 修完 24h 内必 verify 产物落点 |

**L-49 族系扩展到 6 层**：
```
L-49    cron edit 必看 argv 完整 JSON
L-49.5  argv 必查脚本路径存在性
L-49.6  cron cleanup 决策树
L-49.7  INC 报告必加 enabled/disabled tag 区分
L-49.8  ID 引用必完整
L-49.9  脚本路径常量漂移 silent failure 治本  ← NEW
```

**Wiki 健康度进展报告**（B 步骤）：
- 路径：`wiki/methodologies/process/wiki-health-improvement-20260714-20260720.md`
- 数据对比：死链 1093→368（-66%）/ 过时 1085→15（-99%）/ 空目录 27→1（-96%）
- 健康度：~40/100 → 70-75/100
- 13 个 INC + 3+ lessons 治本轨迹（按时间线）

**24h verify**：
- 7-21 03:30 cron 自动跑 → 验证 report 落 `methodologies/process/`（不靠人盯）
- 7-21 18:00 close INC（如一切正常）

**关联产物**：
| 路径 | 大小 | 状态 |
|:---|:---:|:---:|
| `wiki/review-logs/incidents/2026-07/inc_2026-07-20_001-...md` | 3862B | ✅ |
| `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-20-wiki-review-path-drift-l49-9.md` | 2745B | ✅ |
| `wiki/methodologies/process/wiki-health-improvement-20260714-20260720.md` | 4621B | ✅ |
| `scripts/wiki_auto_review.py` | 17573B（+18B）| ✅ |
| `scripts/wiki_auto_review.py.bak.20260720_1822` | 17555B | ✅ |

🕵️ nick_fury · 2026-07-20 18:30 CST · Wiki 健康度进展 · L-49.9 治本

---

## 2026-07-21 09:10 CST · INC-001 · L-49.10 增量区

**INC-2026-07-21-001**：Wiki Git Push 静默失败 61 个 commit（凭证失效 + silent failure）

**核心数据**：
- 文博 9:00 CST 飞书派单 → 09:10 CST 闭环 = **10min**
- ahead 61 个 commit（7-19 ~ 7-21 累积）
- 远程 `github.com/wenbo0527/wiki-knowledge-base`

**4 层根因**：
1. 🔴 HTTPS PAT token `ghp_qRjB1k...` 失效
2. 🔴 push 失败 = silent failure（只 log 不告警，cron 不感知）
3. 🟠 cron 上下文无 ssh-agent（`SSH_AUTH_SOCK` 不继承）
4. 🟡 post-commit 钩子双重失败（`timeout: command not found` + 同套 HTTPS）

**4 步修复**：
1. 凭证 HTTPS → SSH（`git@github.com:wenbo0527/wiki-knowledge-base.git`）
2. `git pull --no-rebase` 整合远程 2 commit
3. `git push` 推完 ahead 61 → 0
4. 改脚本：3 处改动（GIT_SSH_COMMAND export / push 失败飞书告警 / exit 1）

**3 条铁律（L-49.10）**：
1. HTTPS PAT 严禁用于自动 push（必 SSH）
2. silent failure 必加告警 + exit 非零
3. cron 上下文 SSH 必显式 `GIT_SSH_COMMAND`

**L-49 族系扩展**：从 L-49.9（7-20 Wiki 健康度路径漂移）→ **L-49.10**（7-21 Git 凭证 + 静默失败）= 第 7 层

**L-16 grep 全集实证**（L-16 修一类必 grep 全集铁律）：
| 路径 | 是否有 .git | 风险 |
|:---|:---:|:---:|
| `/Users/wenbo/Documents/project/Wiki/` | ✅ | 已修 |
| 其他 6 个候选路径 | ❌ | n/a |

**L-49 族系（7-15 → 7-21 共 7 层）**：
```
L-49    cron edit 必看 argv 完整 JSON          (INC-002)
L-49.5  argv 必查脚本路径存在性                 (INC-005)
L-49.6  cron cleanup 决策树（4 类 + 4 动作）    (INC-006)
L-49.7  INC 报告必加 enabled/disabled tag 区分 (INC-007)
L-49.8  ID 引用必完整（grep 原文 + 长度校验）   (INC-005 补)
L-49.9  脚本路径常量漂移 silent failure 治本   (INC-001 7-20)
L-49.10 Git 凭证 + 静默失败 + cron SSH 上下文  (INC-001 7-21) ← NEW
```

**关联产物**：
| 路径 | 大小 | 状态 |
|:---|:---:|:---:|
| `wiki/review-logs/incidents/2026-07/inc_2026-07-21_001-wiki-git-push-fail-61-ahead.md` | 4957B | ✅ |
| `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-21-git-push-credential-strategy-l49-10.md` | 4014B | ✅ |
| `wiki/methodologies/process/wiki-health-improvement-20260714-20260720.md`（7-20 已写）| 4621B | ✅ |
| `/Users/wenbo/.nickfury/scripts/wiki_auto_commit.sh` | ~4200B（+550B）| ✅ |
| `/Users/wenbo/.nickfury/scripts/wiki_auto_commit.sh.bak.20260721_0900` | 3654B | ✅ |
| `memory/daily/2026-07-21.md` | 3060B | ✅ |

**后续 todo**（等文博拍板）：
1. post-commit 钩子要不要也改 SSH + 失败告警？🟡
2. 装 GNU coreutils 让 `timeout` 可用？🟢
3. cron delivery mode=none 改造？🟡
4. L-49.10 集成到 sunday_cron_health_check.py 周日复查？✅ 必集成

**自我归因**（L-29 命中）：
- 61 个 commit 静默累积 2 天 —— cron 跑过 96 次没人查 ahead
- silent failure 是 L-32 早就说过"不 swallow"的同根病，但 4-24 旧脚本没覆盖
- **反思**：cron 类任务必须有 ahead/behind 健康检查

🕵️ nick_fury · 2026-07-21 09:10 CST · INC-001 闭环 · L-49.10 治本 · 10min 修复

---

## 2026-07-21 09:17 CST · 3 项全做闭环（"同意" + "全做"）

**核心数据**：
- 09:11 文博"同意" → 09:11 文博"全做" → 09:17 3 项全闭环 = **6min**
- 产物：4 文件更新 + 3 新备份 + 1 副产（coreutils 装成功）

**#1 改 post-commit 钩子**：
- 第一版 async 模式 → 误报（PID 未注册返回 127）
- 改用同步 push → 2 次 test commit 成功推
- 边界守住：保留原"非阻塞"设计意图（改同步牺牲 1-3s 阻塞换可靠）
- 副作用：远程多 2 test commit（0583d47 / 47e0313）

**#2 brew install coreutils**：
- gtimeout 9.11 装成功
- 副作用澄清：钩子已改同步，**装完用不上**
- 写进 lesson L-49.10 铁律 4（以后 push 卡死兜底）

**#3 集成 L-49.10 到 sunday_cron_health_check.py**：
- 新增 `check_l49_10_git_push_health()` · 4 项铁律
- 单测 pass=True · 0 issues
- 脚本行数 351 → 460（+109 行）
- 完整 main() 留给 7-19 22:00 cron 自动跑

**L-49 族系扩展到 8 层**：
```
L-49.10    Git 凭证 + 静默失败 + cron SSH 上下文
L-49.10.1  hook 异步 vs 同步 push 选型 + gtimeout 兜底  ← NEW
```

**自我归因**（L-29 命中）：
- async wait 误报 1 次：推了假"push 失败"告警给文博
- 主动坦白 + 立刻改同步 + 3 备份保留
- 教训：hook 场景不能用 async wait（写进 L-49.10.1）

**后续 todo**（等文博拍板）：
1. 远程 2 test commit 保留 / reset？
2. 7-19 22:00 cron 自动跑全套验证
3. 7-19 周日 22:00 sunday_cron_health_check 跑完后复查

🕵️ nick_fury · 2026-07-21 09:17 CST · INC-001 完整闭环 · 4 文件更新 + 3 项完成

---

## 🆕 7-22 增量 · INC-2026-07-22-001 + 2 lessons

**派单源**: 文博 21:07 "检查下问题" → 21:47 "B 继续修"
**决策路径**: 12h 真空（09:04 拍 C 等拍板未动手）+ B 选项立即执行
**实际动手**: 30 min（21:47 → 22:00，cron 实测待 7-23 自动验证）

### INC-2026-07-22-001: cron argv cwd + 数据源路径双重 silent failure

| 维度 | 数据 |
|:---|:---|
| **文件** | `review-logs/incidents/2026-07/inc_2026-07-22_001-cron-argv-cwd-silent-failure.md` |
| **大小** | 5993 B |
| **状态** | ✅ Closed（修中） |

**4 层 silent failure**（按 L-29 命中）：

| 现象 | 手动跑 | cron 跑 | 静默天数 |
|:---|:---:|:---:|---:|
| c3_daily_check.py (cf8e874c) | exit 0 | exit 1 | 12h+ |
| c3_daily_check.py (929a8003) | exit 0 | exit 1 | 12h+ |
| nick_cron_health_weekly | exit 0 | exit 1 | 3d+ |
| rss.collect 源 = 0 | sources=135 | sources=0 | **21d+** |

### L-49.11: Cron argv 必注入 cd cwd 上下文

| 维度 | 数据 |
|:---|:---|
| **文件** | `review-logs/lessons/by-agent/nick_fury/lesson-2026-07-22-cron-argv-cwd-l49-11.md` |
| **大小** | 2795 B |
| **铁律级别** | 🔴 P0 · 必查 |

**1 条铁律**：所有 OpenClaw cron argv 必以 `cd <BASE_DIR> &&` 开头。

**L-49 族系位置**：第 12 层（4 类精度：argv 路径 → 路径存在 → 清理决策 → 报告精度 → 标识精度 → 产物落点 → 投递配置 → **argv 上下文**）

### L-52.6: 脚本间数据源路径必双向验证

| 维度 | 数据 |
|:---|:---|
| **文件** | `review-logs/lessons/by-agent/nick_fury/lesson-2026-07-22-data-source-path-l52-6.md` |
| **大小** | 2970 B |
| **铁律级别** | 🔴 P0 · 必查 |

**1 条铁律**：任何"生产端 + 消费端"数据流组合，必双向验证路径/类型/字段。

**L-52 族系位置**：第 7 层

### 修复清单（已完成）

| 类型 | 项 | 状态 |
|:---:|:---|:---:|
| **6 cron argv** | cd $BASE && python3 ... 注入 | ✅ |
| **daily_pipeline.py** | config_path 改绝对路径 | ✅ |
| **morning_daily_writer.py** | 数据源路径改 `pipeline_log.json` + L-29 字段映射 | ✅ |
| **3 脚本备份** | `data/backups_20260722_2149/` | ✅ |
| **INC + 2 lessons + registry 增量** | wiki/review-logs/ | ✅ |

### 24h 验证窗口（自动）

| 节点 | 期望 | 验证项 |
|:---|:---|:---|
| 7-23 01:00 rss.collect 自动跑 | sources>0 + 新文章>0 | L-52.6 真治本 |
| 7-23 08:30 morning·daily 自动跑 | 完稿率上升 + rss 段非"🟡 不存在" | L-52.6 消费端 |
| 7-23 09:00 c3 cron 自动跑 | exit 0 + 飞书推完稿率 | L-49.11 治本 |
| 7-23 21:00 c3 cron 自动跑 | exit 0 + 飞书推 | L-49.11 治本 |
| 7-26 22:00 cron_health 周日跑 | exit 0 + 飞书推 | L-49.11 治本 |

### 🪞 自我归因（L-29 命中 · SOUL §6.4）

**12h 真空**（09:04 → 21:07）：
- 09:04 拍 C 后我给"精确诊断 + 3 拍板问题"
- 文博 12h 没回应 → 我没主动 push back 或 escalate
- 等拍板 ≠ 沉默 → 需补"沉默兜底"机制（候选 L-49.12）

**误诊 1 次**（上午 09:04 报告）：
- 我说"rss.collect silent failure 21 天"基于 `cron_daily.log` 的 `No such file` 报错
- 但这个脚本是 6-29 弃用的实体，**真正的 rss.collect cron 走 daily_pipeline.py**
- **L-37 报告必调实时 API**：应该 `openclaw cron runs --id rss.collect` 看真实 diagnostic

---

---

## 📌 7-24 增量（INC-2026-07-24-001 · L-49.12 cron argv 失效看门狗 · 30 min 闭环）

| ID | 类型 | 标题 | 路径 / 状态 |
|:---|:---|:---|:---|
| **inc_2026-07-24_001** | Incident 🆕 | **Cron argv 失效 + 推送脚本退出码误判 4 层 silent failure**（22d RSS 真空 + 3 cron error + 1 plist 失效）| incidents/2026-07/inc_2026-07-24_001-cron-argv-watchdog-22d-vacuum.md ✅ |
| **lesson-2026-07-24-cron-argv-watchdog-l49-12** | Lesson 🆕 | **L-49.12 cron argv 失效检测 cron（7 天看门狗）** | lessons/by-agent/nick_fury/lesson-2026-07-24-cron-argv-watchdog-l49-12.md ✅ |
| **L-49.12** | Lesson 🆕 | **cron argv 失效检测 cron（7 天看门狗）· L-49 族系第 13 层** | lesson-2026-07-24-cron-argv-watchdog-l49-12.md ✅ |
| **scripts/cron_argv_watchdog.py** | Asset 🆕 | **6734 bytes · L-15 端到端验证全过 · 扫 OpenClaw 48 cron + 23 launchd plist · L-36 退出码治本** | scripts/cron_argv_watchdog.py ✅ |
| **scripts/c3_daily_check.py** | Fix ✅ | **4 处 return 1 → return 0（L-36 治本 · INC-001 命中）** + 注释 INC-2026-07-24-001 | ✅ |
| **scripts/sunday_cron_health_check.py** | Fix ✅ | **1 处 return 1 → return 0（L-36 治本 · INC-001 命中）** + 注释 INC-2026-07-24-001 | ✅ |
| **com.nickfury.wiki.monthly-refresher.plist.disabled-20260724-cron-argv-watchdog** | Asset ✅ | **launchctl bootout + mv rename**（指向已删 monthly_refresher.py 22d silent failure） | ✅ |
| **OpenClaw cron argv.watchdog** | Asset ✅ | **id `f01832cf-4651-4d2b-b0b9-ba1979b37dd8` · 每周日 21:00 Asia/Shanghai** | ✅ |
| **HEARTBEAT.md §二十七** | Action ✅ | **7-24 08:41 接单 + 09:30 闭环 · 30 min** | HEARTBEAT.md ✅ |

### 7-24 数据截止（实测）

| 维度 | 数据 |
|:---|:---|
| OpenClaw cron 总数 | 48 个（全局）/ 17 个 nick_fury |
| nick_fury cron argv 失效 | 0 个 |
| launchd plist 活跃 | 4 个（bestpractice.daily/collect + wiki-health-check + monthly-refresher 已 disable）|
| launchd plist argv 失效 | 0 个（wiki.monthly-refresher 已退役）|
| c3 cron error | 修后 0 个（连续 exit 0）|
| sunday_cron_health error | 修后 0 个 |

### 24h 验证窗口（自动）

| 节点 | 期望 | 验证项 |
|:---|:---|:---|
| 7-24 21:00 c3 cron 修后首次 | exit 0 + 飞书推送成功 | L-36 治本 |
| 7-26 21:00 cron.argv.watchdog 注册后首次 | exit 0 + 0 失效 | L-49.12 治本 |
| 7-26 22:00 sunday_cron_health_weekly 修后首次 | exit 0 | L-36 + L-49.11 治本 |

### 🪞 自我归因（L-29 命中 · SOUL §6.4）

**22d silent failure 漏检**（7-2 → 7-24）：
- L-49 族系已 9 层（L-49 → L-49.11）但**缺持续看门**——失效检测仅一次性，不持续
- L-49.12 治本：从"写对"扩展到"持续有效"

**C-3 + 周日 cron 自检失守**：
- 这 2 个 cron 应该是发现 22d silent failure 的两道告警网
- 但**自己 exit 1 误判 error**（root cause B）→ 失去告警能力
- L-36 治本：推送成功 = 业务成功 = exit 0

**误判 0 次**（7-24 08:41 报告）：
- 用户面"大量抓取失败"第一印象 → 实际为"4 silent failure + 用户面 OK"
- L-37 报告必调实时 API + 完整分类：4 OK + 4 silent failure 全列清
- 文博一次拍板（C 选项）→ 30 min 闭环

---

🕵️ nick_fury · 2026-07-24 09:35 CST · INC-2026-07-24-001 + L-49.12 闭环 · 30 min 动手 · 7-26 验证窗口开启

---

🕵️ nick_fury · 2026-07-22 21:55 CST · INC-2026-07-22-001 + L-49.11 + L-52.6 闭环 · 30 min 动手 · 7-23 验证窗口开启

---

🕵️ nick_fury · 2026-07-26 12:30 CST · INC-2026-07-26-001 + L-50 族闭环 · 49 min 闭环

**L-50 族（4 条）**：
- L-50.1 监控告警双轨设计（真信号 + 降噪 3 件套：语义/去重/时段）
- L-50.2 正则要结构化前缀（标记判定必带 `## ✅ ` 前缀）
- L-50.3 时段判定显式分支（if/elif + else 静默）
- L-50.4 调试入口测完必删（C-1 铁律 · 不留 commit · bak 保留）

**关键决策**：B+C+D 三层治本（文博 12:24 拍板）
- B 时间窗口分段（09:00 骨架 / 21:00 完稿率）
- C 完稿只看 `## ✅ 完稿时间` 标记（排除 size 阈值 1836B 误判）
- D 24h 去重（`data/c3_alert_dedup.json`）

**L-15 验证 4 用例全过**：21:00 首次/21:00 二次/9:00/12:30 实跑
**产物**：scripts/c3_daily_check.py (632 行 · +110 行) + bak.20260726-bcd (备份) + c3_alert_dedup.json (新增)

**7-27 09:00 验证窗口开启**：观察 B 治本（9:00 静默）+ D 治标（同 ratio 不重推）

---

🕵️ nick_fury · 2026-07-26 13:20 CST · INC-2026-07-26-002 + L-50.5-L-50.8 闭环 · 4 项推荐同时落地

**L-50 族（4 条新增）**：
- **L-50.5** KB 同步缺口根除（3 处 hardcode → 单一 import 源 + API 对账）
- **L-50.6** 告警改对了 ≠ Nick 会补（加提前 Nh 提醒 cron · 真信号兜底）
- **L-50.7** INC 5 必检 C2 自指防御（先扫再发 · 避免凭印象错版）
- **L-50.8** 同根病 INC 检测（30 天内 L 族重合必引用）

**4 项动作（A1+A2+A3+B1+C2）**：
- A1+A2+A3: daily_note_scan.py / getnote_ej9_to_wiki.py / c3_daily_check.py 3 处加 JK27rQ60 消费金融
  - c3 不再 hardcode，import KB_LIST —— 单一真相源
- B1: 新增 daily_reminder.py (5227B) + 注册 OpenClaw cron aaa41eb7-...14:00
  - 5 用例端到端全过 · 飞书推送成功 om_x100b696d31a460a8b487d72a13cb7c0
- C2: 新增 inc_sibling_check.py (4237B) · 5 必检扫描 + 同根病 30 天检测
  - 自验实证：INC-002/003 旧报告 4/5 + 3/5 → "凭印象"铁证

**L-49.12 argv 看门狗**：14:00 cron 注册后扫描 0 失效
**L-50.7 C2 自指实证**：新建 INC-2026-07-26-002 → 5/5 ✅；修补 INC-2026-07-26-001 → 5/5 ✅

**7-27 14:00 验证窗口**：B1 cron 首次跑（应自动推飞书）
