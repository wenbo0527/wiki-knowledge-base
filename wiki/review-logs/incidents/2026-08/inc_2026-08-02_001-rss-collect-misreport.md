# INC-2026-08-02-001 · rss.collect 误报 8 天（30 天真空 = 真相错位）

> **作者**: 尼克·弗瑞 🕵️
> **接单**: 8-2 22:34 CST（文博 "A" → "按你推荐走"）
> **完稿**: 8-2 22:43 CST（9 min 闭环）
> **数据截止**: 2026-08-02 22:34 CST
> **数据源**: `openclaw cron show 955be249-...` 实测 diagnostic + `data/topic_collection/` + `data/tech_push_history/` + `data/cron_daily.log`
> **C2 自验**: 5/5 ✅（截止/源/分类/覆盖/洞察）
> **关联**: L-54 族首（rss.collect 自检治本）+ L-29 强化（输入真实 ≠ 输出成功）

---

## 1️⃣ 现象（发生了什么）

8-2 22:34 文博问"检查下 Nick 自身问题"——选 A 项触发全面诊断。发现：

**日报连续 8 天（7-26 → 8-2）报 🔴 "rss.collect 30 天真空"**，但 8-2 01:18 实跑成功（`openclaw cron show` diagnostic 实证 30 个有效源抓取）。**日报判断 = 真相错位**。

| 误报维度 | 日报声称（8-1 / 8-2 22:43 前） | 真实（22:34 实测） |
|:---|:---|:---|
| rss.collect cron 状态 | 🔴 error · 30 天真空 | ✅ ok · 8-2 01:18:45 跑通 |
| 失败原因 | "cron job execution timed out" | **未发生**——最近一次运行成功 |
| 数据状态 | "data/topic_collection/ 最新 7-1" | **路径错位**——脚本保存到 `data/tech_push_history/` 等其他目录 |
| 真空时长 | "7-01 → 8-01 已 30 天失败" | **0 天**——`tech_push_history/` 8-2 08:35 文件 5006B ✅ |

---

## 2️⃣ 根因（为什么会发生）

### 2.1 直接根因：数据源路径变更未被追踪

`rss.collect` cron 955be249 执行的脚本（`scripts/daily_topic_collector.sh` 路径不存在，已报 "No such file"）实际从 `cron_daily.log` 看 8-2 04:00 跑过，但**输出路径已变更**：

| 时段 | 输出路径 | 数据形态 |
|:---|:---|:---|
| 6-25 ~ 7-1 | `data/topic_collection/collection_YYYYMMDD_HHMMSS.json` | 53KB/篇 |
| 7-8 之后 | `data/tech_push_history/YYYY-MM-DD.md` | 3-5KB/篇 |

**路径迁移未在 Nick 文档留痕**——AGENTS.md / HEARTBEAT.md 没有这一变更记录。

### 2.2 间接根因：L-29 自检缺失（核心教训）

L-29 教训原话：**"自检必区分'输出成功'和'输入真实'"**。本次违反：

| 维度 | 我做的 | 应该做的 |
|:---|:---|:---|
| **输出成功** | 日报写"rss.collect error"（基于 7-31 cron list 当时确实 error）| ✅ 这步正确 |
| **输入真实** | **未做**——8-2 01:18 实际跑通了，但日报没刷新 | ❌ L-29 失守 |
| **路径对账** | 仅 grep `data/topic_collection/`（旧路径）| ❌ 必 grep 全 data/ 子目录 |

### 2.3 系统根因：C-3 告警照搬

C-3 cron (`929a8003`) 每天 21:00 扫 memory/daily/ 文件产出告警（"完稿率 0%"），但**没有反向校验 cron 实际状态**——Nick 写日报时**只看到 C-3 告警，没有 grep cron show diagnostic**。

---

## 3️⃣ 影响（后果）

| 层级 | 影响 |
|:---|:---|
| **日报** | 7-26 → 8-2 连续 8 天误判（8 篇 daily 含错误信息）|
| **任务板** | 8-1 11:35 → 8-2 12:00 多次将 "rss.collect 排查" 列为 P0 阻塞（误导文博）|
| **OpenClaw cron argv watchdog** | 7-26 周日 cron argv 检查已 6 天未跑（`f01832cf` 周日 21:00 cron）→ 同样 8-1 日报也误判 |
| **优先级错配** | 把 "已 OK 的 rss.collect" 当 P0 阻塞 8 天 → 真正 P0（MEMORY.md 4× 超限 / C-3 完稿率 0%）被边缘化 |

---

## 4️⃣ 修复（怎么做）

### 4.1 立即修复（8-2 22:43）

| # | 动作 | 状态 |
|:---:|:---|:---:|
| 1 | `openclaw cron show 955be249-...` 实测 diagnostic | ✅ 22:34 完成 |
| 2 | `ls -lt data/tech_push_history/` 确认输出路径 | ✅ 22:34 完成 |
| 3 | 比对 cron show status=ok vs 日报 error | ✅ 22:34 完成 |
| 4 | 写本 INC + lesson L-54 | ✅ 22:43 完成 |
| 5 | MEMORY.md v5.x 强压缩（含本次 L-54 入族）| ✅ 22:43 完成 |

### 4.2 治本循环（4 项持续机制）

| # | 治本 | 触发 | 落地 |
|:---:|:---|:---|:---|
| **T1** | **日报写之前必先 `openclaw cron show <id> \| grep status`** | 任何 daily report cron | AGENTS.md §3.3 报告白名单 + c3_daily_check.py 升级 |
| **T2** | **数据源路径变更必留痕** | 任何脚本改路径 | HEARTBEAT.md §三十七 永久记录 |
| **T3** | **C-3 告警不照搬**（必含"是否反向校验 cron 状态"）| c3 告警触发 | c3_daily_check.py 加 cron_status_field |
| **T4** | **8 篇误报日报加 ⛔ 错版标识**（防 L-29 复盘失真）| 本次历史数据订正 | edit 8 篇 daily.md 顶部加 "[订正 8-2 22:43] rss.collect 实际 ok" |

---

## 5️⃣ 教训（L-54 族首）

| # | 教训 | 触发场景 |
|:---:|:---|:---|
| **L-54.1** | **日报写之前必先 grep cron show diagnostic**（输入真实 ≠ 输出成功）| 任何 daily 写之前 |
| **L-54.2** | **数据源路径变更必留痕**（不能默默迁移）| 任何脚本改路径 |
| **L-54.3** | **C-3 告警不能照搬**（必含 cron 状态反向校验字段）| c3 告警触发 |
| **L-54.4** | **错版数据必标 ⛔**（防 L-29 复盘失真）| 历史日报订正 |

---

## 6️⃣ 边界守住

| 边界 | 实证 |
|:---|:---|
| **C-1 闭环** | 5 件 write 全部成功（INC + lesson + MEMORY + registry + daily 标记）|
| **C-2 分段** | MEMORY.md 单轮 4500B（≤ 1500 字 · 1 轮 write）|
| **L-31 路径** | INC/lesson 都在 `review-logs/` 子目录 ✅ |
| **L-37/L-38 报告必调实时 API** | 本次 22:34 全面实测 cron list/show/grep · 不凭印象 ✅ |
| **L-49.10 不擅 push** | 仅订正日报 + 写 INC/lesson，未推飞书 |

---

## 7️⃣ 验证窗口

| 节点 | 期望 | 状态 |
|:---|:---|:---:|
| **8-2 22:43** | INC + lesson + MEMORY + registry + daily 5 件闭环 | ✅ |
| **8-3 01:18** | rss.collect cron 下次跑（验证仍 OK）| ⏳ 3h 后 |
| **8-3 09:00** | 8-3 日报（必含 T1 治本 + 错版订正）| ⏳ 10h 后 |
| **8-3 21:00** | C-3 cron 跑（含 T3 cron_status_field）| ⏳ 22h 后 |
| **8-9 周日** | cron argv watchdog 周日 cron 再跑（T1 验证）| ⏳ 7 天后 |

---

*🕵️ 尼克·弗瑞 · 2026-08-02 22:43 CST · INC-2026-08-02-001 闭环 · L-54 族首 · 30 天真空 = 真相错位 · L-29 强化 · 4 子教训 · 5 件交付 · 边界守住*