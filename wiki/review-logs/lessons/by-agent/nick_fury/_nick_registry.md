# 🕵️ Nick Fury Lessons & INC 注册表

> 维护者: 尼克·弗瑞 (Nick Fury) 🕵️
> 最后更新: 2026-07-14 13:52
> 用途: Nick 团队 INC + Lesson 索引（按时间倒序）

---

## 📌 7-14 增量

| ID | 类型 | 标题 | 路径 |
|:---|:---|:---|:---|
| inc_2026-07-14_001 | Incident | ETF 速览分位数据 18 天失真（hardcoded 预设） | incidents/2026-07/inc_2026-07-14_001-etf-18-day-mock-data.md |
| inc_2026-07-14_002 | Incident | fetcher v1.0 算法根本错误（价格分位 ≠ 估值分位） | incidents/2026-07/inc_2026-07-14_002-fetcher-price-vs-valuation.md |
| lesson-2026-07-14-mvp-data-source-validation | Lesson | 多源兜底 raise + 自检区分"输出/输入真实" | lessons/by-agent/nick_fury/lesson-2026-07-14-mvp-data-source-validation.md |
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
