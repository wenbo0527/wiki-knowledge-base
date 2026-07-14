# 🔴 Incident 006: 18 launchd plist vs OpenClaw cron 重复（14/18 重复）

| 字段 | 值 |
|:---|:---|
| **ID** | inc_2026-07-14_006 |
| **严重级别** | 🟠 High |
| **状态** | ✅ **Closed** |
| **发现时间** | 2026-07-14 14:20 |
| **闭环时间** | 2026-07-14 18:36 |
| **发现者** | wenbo 提醒"后续内容走 OpenClaw 原生定时触发" |
| **负责人** | nick_fury |
| **最后更新** | 2026-07-14 18:40 |

---

## 问题描述

文博 14:20 提醒"后续内容需要走 OpenClaw 的原生定时触发" → nick_fury 立即 `openclaw cron list` 对照 launchd plist。

**揭穿**：
- **18 个 launchd plist** + **46 个 OpenClaw cron 任务**
- **14/18 Nick 团队 launchd 任务**在 OpenClaw cron 都有对应（重复！）
- 重复任务每天 2 次跑（一次 launchd 一次 OpenClaw cron），浪费资源 + 可能产生竞态
- 违反 L-13 教训（🔴 P0 · 2026-06-30 文博明示）：OpenClaw 原生优先

## 重复任务清单（14 disable / 4 保留）

### ✅ 已 disable（14 个 · 2026-07-14 18:36 闭环）

| LaunchAgent plist | 对应 OpenClaw cron ID |
|:---|:---|
| com.nickfury.daily-report-c3 | `daily·report·c3` (cron:c0a4.../cf8e...) |
| com.nickfury.morning-daily | `morning·daily` (cron:34b6...) |
| com.nickfury.daily-investment-push | `morning·rss·etf·push` (cron:1032...) |
| com.nickfury.daily-tech-push | `tech·briefing` (cron:8f14...) |
| com.nickfury.getnote-wiki-sync | `getnote·wiki·sync` (cron:d795...) |
| com.nickfury.etf.hegang.report | `etf·hegang.report` (cron:4367...) |
| com.nickfury.rss.collect | `rss.collect` (cron:955b...) |
| com.nickfury.github.track | `github.track` (cron:e382...) |
| com.nickfury.kb.track | `kb.track` (cron:f227...) |
| com.nickfury.daily-note-scan | `daily·note·scan` (cron:1455...) |
| com.nickfury.wiki-auto-commit | `wiki·auto·commit` (cron:c0a4...) |
| com.nickfury.wiki.review | `wiki.review` (cron:f3b6...) |
| com.nickfury.wiki.weekly-synthesizer | `wiki.weekly·synthesizer` (cron:c39d...) |
| com.nickfury.evening-tracker | `投资纪律-每日汇总` (cron:68fb...) |

### 🟢 保留（4 个 · launchd 专属）

| LaunchAgent plist | 保留原因 |
|:---|:---|
| com.nickfury.wiki-health-check | TCC 权限拦截 launchd 进程访问 ~/Documents，需 RAG API 绕过 |
| com.nickfury.wiki.monthly-refresher | 无 OpenClaw cron 对应 |
| com.nickfury.bestpractice.daily | 派蒙团队脚本 |
| com.nickfury.bestpractice.daily.collect | 派蒙团队脚本 |

## 根因分析

L-13 教训（2026-06-30 文博明示）半年后**仍未执行**：
- 当时 Nick 写新任务用 launchd plist（更熟悉）
- 没人按 L-13 强制规则"先 openclaw cron list | grep {name}"
- 18 plist 半年累积 → 14 个重复

### 关键问题

> **L-13 是文博红线规则**（"OpenClaw 原生优先"），但没人执行 grep 验证。**教训≠改变**（SOUL §6.4）。

## 解决措施（2026-07-14 18:36 闭环）

### 执行

```bash
# /tmp/disable_duplicate_launchd_2026-07-14.sh (82 行)
# 步骤：
# 1. launchctl bootout 14 个 (从 launchd 卸载)
# 2. cp 到 2 个备份位置 (Wiki _deprecated + scripts/_deprecated)
# 3. mv 到 LaunchAgents/_disabled_2026-07-14/
```

### 验证结果

| 检查项 | 结果 |
|:---|:---:|
| disable 成功数 | **14/14 ✅** |
| 备份完整性（Wiki）| 14/14 ✅ |
| 备份完整性（Scripts）| 14/14 ✅ |
| launchctl list 剩余 | 4/4 ✅（专属保留）|
| bootout 全部 ✅ | ✅ |
| 失败 | 0 |

### 防失效机制

| 机制 | 状态 |
|:---|:---:|
| AGENTS.md §0.5 写入"openclaw cron list \| grep"流程 | ✅ |
| 14 个 disabled plist 备份到 3 个位置 | ✅ |
| 备份位置: Wiki `_deprecated/2026-07-14/launchd_disabled/` | ✅ |
| 备份位置: Scripts `_deprecated/2026-07-14/launchd_plists_backup/` | ✅ |
| 移动位置: LaunchAgents `_disabled_2026-07-14/` | ✅（恢复用 `mv` 即可）|

## 关联文档

- **L-13 教训**（🔴 P0 · 2026-06-30）: OpenClaw 原生优先
- **L-31 教训**（2026-07-14）: INC 路径规范
- **INC-2026-07-14-001~005**: 7-14 已闭环的 5 个 INC
- **AGENTS.md §0.5**: 4 层路径 + L-13 治本

## 后续行动（可复用脚本）

- [x] AGENTS.md §0.5 修正（4 层路径 + L-13 治本）✅
- [x] launchd vs OpenClaw cron 对照表（14 重复 / 4 专属）✅
- [x] **批量 disable 14 个 launchd plist**（2026-07-14 18:36）✅
- [x] 备份完整性验证（2 个位置 + 原位置移动）✅
- [x] INC-006 转 Closed ✅
- [ ] 7-19 周日 AGENTS.md v3.2 升级（含 L-13 强化）
- [ ] 派蒙开 INC-007 评估派蒙团队 launchd → OpenClaw cron
- [ ] 观察明早 8:35 tech·briefing cron 正常（disable 重复 launchd 不影响）

---

*Created: 2026-07-14 17:25 | Updated: 2026-07-14 18:40 | Closed*

## 📌 恢复方法（如果 OpenClaw cron 出问题临时回退）

```bash
# 1 个命令恢复: 从 LaunchAgents/_disabled_2026-07-14/ 移回 + bootout 重新加载
mv /Users/wenbo/Library/LaunchAgents/_disabled_2026-07-14/com.nickfury.{NAME}.plist \
   /Users/wenbo/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) /Users/wenbo/Library/LaunchAgents/com.nickfury.{NAME}.plist
```
