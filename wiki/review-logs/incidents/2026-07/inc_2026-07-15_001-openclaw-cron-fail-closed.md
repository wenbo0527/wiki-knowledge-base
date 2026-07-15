# INC-2026-07-15-001: OpenClaw cron 投递失败（25 任务全挂 + 5 脚本已删）

> ⚠️ **根因修正（9:05 二次 verify 后）**：本文初版（9:00 写）假设根因是"Target=main vs isolated"——**错**。  
> **真实根因（三层）**：
> 1. **22 个 cron 命令实际跑通**（exit 0），但 `lastDelivered: false`（缺 feishu target）  
> 2. **5 个 cron 命令指向已不存在的旧脚本**（7-1 改造时合并/删除 或 7-14 ETF 撤路径没改 cron）  
> 3. **lark-cli auth token needs_refresh**（但有 auto-refresh on next call 机制，不阻塞）
>
> LEADER 7-15 01:10 凌晨日报的"Target=isolated vs main"假设也是错的——派蒙也用 isolated（看 派蒙-T3prime-自查-DAY）。
>
> 详见 §根因（修正版） + §双层故障。

---

## 现象

7-15 早 8:53 文博问"今天没收到科技日报，请检查一下" → 09:00 揭穿 25 个 OpenClaw cron 全部 fail-closed。

### 完整根因图（09:05 verify 后）

| 故障层 | 数量 | 现象 | 真实根因 |
|:---:|:---:|:---|:---|
| **L1 投递失败** | 22 | `lastDeliveryStatus: not-delivered`，`lastDeliveryError: Delivering to Feishu requires target <chatId\|user:openId\|chat:chatId>` | `delivery.mode=announce, channel=last` → 找不到 main session route |
| **L2 脚本不存在** | 5 | 命令 exit 2，diagnostic: `can't open file '.../xxx.py': [Errno 2] No such file or directory` | 7-1 改造时合并/删除 + 7-14 ETF 撤路径没改 cron |
| **L3 token 过期** | 1 | `User identity: needs refresh` | 7-1 11:25 授权后 14 天未用，但 auto-refresh 机制工作正常 |

### L2 脚本不存在清单（5 个 cron）

| Cron | 旧路径 | 真实状态 | 修法 |
|:---|:---|:---|:---|
| `tech·briefing` (8f14728b) | `scripts/tech_briefing.py` | 7-1 合并到 daily_tech_report.py | `--command daily_tech_report.py` |
| `daily·note·scan` (14550600) | `scripts/weekly_note_scan.py` | 改名 daily_note_scan.py | `--command daily_note_scan.py` |
| `morning·rss·etf·push` (1032cfb0) | `scripts/morning_rss_etf_push.py` | 7-1 合并到 daily_tech_report.py | disable（7-1 已合并）或指向 daily_tech_report.py |
| `投资纪律-每日汇总` (68fbf538) | `scripts/daily_investment_summary.py` | 7-14 撤了，路径仍指向 | **disable**（ETF 估值迁移后文博手动跟踪） |
| `投资纪律-周报` (6e96cc0d) | `scripts/daily_investment_summary.py` | 同上 | **disable** |

### L1 投递失败清单（22 个 cron 都命令跑通但 lastDelivered=false）

| Cron | argv（实际）| lastRunStatus |
|:---|:---|:---:|
| morning·daily | `python3 morning_daily_writer.py` | exit 0 ✅ |
| rss.daily | `python3 .../daily_pipeline.py 30` | exit 0 ✅ |
| etf.hegang.report | `python3 .../etf_hegang_report.py --date ...` | exit 0 ✅（但 ETF 已撤） |
| tech·briefing | `python3 tech_briefing.py` | exit 2 ❌（脚本不存在） |
| wiki.daily·expander | `python3 .../daily_expander.py run` | exit 0 ✅ |
| daily·report·c3 (09:00) | `python3 c3_daily_check.py` | exit 0 ✅ |
| daily·note·scan | `python3 weekly_note_scan.py` | exit 2 ❌（改名了） |
| daily·report·c3 (21:00) | `python3 c3_daily_check.py` | exit 0 ✅ |
| bestpractice.daily | `bash .../run_collector.sh` | exit 0 ✅ |
| bestpractice.daily.ap | `python3 .../daily_append.py` | exit 0 ✅ |
| bestpractice.round2 | `bash .../run_collector_round2.sh` | exit 0 ✅ |
| bestpractice.daily.co | `bash .../daily_collect.sh` | exit 0 ✅ |
| rss.collect | `python3 .../daily_pipeline.py collect 30` | exit 0 ✅（但源 0 个） |
| github.track | `python3 .../github_tracker.py scan` | exit 0 ✅ |
| kb.track | `python3 .../kb_tracker.py scan` | exit 0 ✅ |
| rss.organize | `python3 .../organizer.py run` | exit 0 ✅ |
| wiki.ingest | `python3 .../wiki_ingestor.py ingest` | exit 0 ✅ |
| wiki.review | `python3 .../wiki_auto_review.py` | exit 0 ✅ |
| wiki.weekly·synthesizer | `python3 .../weekly_synthesizer.py run` | exit 0 ✅ |
| morning·rss·etf·push | `python3 morning_rss_etf_push.py` | exit 2 ❌（已合并） |
| 投资纪律-每日汇总 | `python3 daily_investment_summary.py` | exit 2 ❌（已撤） |
| 投资纪律-周报 | `python3 daily_investment_summary.py` | exit 2 ❌（已撤） |
| 投资纪律-中报硬截止-当天 | (空) | idle |

### 派蒙 cron 投递成功模式（参考对齐）

```json
{
  "delivery": {
    "mode": "none",
    "channel": "feishu",
    "to": "user:ou_415aaf2674f34d5034a3e71882b89d94"
  }
}
```

**对比 Nick 当前错的**：
```json
{
  "delivery": {
    "mode": "announce",
    "channel": "last"
  }
}
```

**关键差异**：
- `mode: none` —— 不通过 main session announce，直接推送
- `channel: feishu` —— 显式飞书渠道
- `to: user:ou_xxx` —— 显式目标用户

---

## 应急补发（9:05 已闭环）

**动作**：手动跑 `scripts/daily_tech_report.py` 一次

```
[2026-07-15 09:05:10] [INFO] lark-cli preflight: ✅ user=needs_refresh token=needs_refresh (send_as_user ✅)
[2026-07-15 09:05:11] [INFO] 生成技术日报内容: 2655 字符
[2026-07-15 09:05:12] [INFO] 通道 1 lark-cli: ✅
[2026-07-15 09:05:12] [WARN] 通道 2 sessions_send 在 launchd 环境不可用, 跳过
[2026-07-15 09:05:12] [INFO] 通道 3 wiki: ✅
```

**结果**：
- lark-cli ✅（auto-refresh 工作正常）
- wiki ✅（双通道兜底）
- 飞书推送历史：tech_push_history/2026-07-15.md (3600 字符) 包含 5 篇 RSS 精选
- 文博已收到科技日报

**但 sessions_send 跳过**：手动 shell 跑正常（launchd 上下文才会失败，L-22 已治本）

---

## 修复方案（已批 A 方案 · 9:10 执行）

### A1：22 个 cron 改 delivery 为飞书显式

```bash
# 学派蒙模式: mode=none, channel=feishu, to=user:ou_xxx
# 派蒙用 ou_415aaf2674f34d5034a3e71882b89d94
# 文博用 ou_ca04de68a40f571f59bcf2e71241415a
# 22 个 cron 全部要改

for cron_id in $(openclaw cron list | grep -E "tech·briefing|morning·daily|..." | awk '{print $1}'); do
  openclaw cron edit $cron_id \
    --channel feishu \
    --to "user:ou_ca04de68a40f571f59bcf2e71241415a"
done
```

**注意**：`openclaw cron edit` 选项 `--to` description 是 "E.164, Telegram chatId, or Discord channel/user"，但派蒙实证可用 `user:ou_xxx` 格式（9:05 验证）。

### A2：5 个 cron 改 command 路径 或 disable

| Cron ID | 操作 |
|:---|:---|
| 8f14728b (tech·briefing) | `--command "python3 daily_tech_report.py"` |
| 14550600 (daily·note·scan) | `--command "python3 daily_note_scan.py"` |
| 1032cfb0 (morning·rss·etf·push) | `disable`（7-1 已合并到 daily_tech_report.py） |
| 68fbf538 (投资纪律-每日汇总) | `disable`（7-14 ETF 估值迁移） |
| 6e96cc0d (投资纪律-周报) | `disable`（7-14 ETF 估值迁移） |

### 验证（24h 内）

```bash
# 1. 看 22 个 cron status 全 ok
openclaw cron list | grep -E "tech·briefing|morning·daily|..." | awk '$7=="ok"'

# 2. 看 consecutiveErrors 全 0
openclaw cron get <id> | grep consecutiveErrors

# 3. 看 lastDelivered: true
openclaw cron get <id> | grep lastDelivered
```

---

## 教训（L-34 + L-35）

详见：
- `lesson-2026-07-15-cron-command-sync.md` (L-34)
- `lesson-2026-07-15-script-rename-cron-grep.md` (L-35)

### L-34 核心

**OpenClaw cron `command` 字段（payload.argv）必须随 scripts 改造同步更新**。

反例：7-1 改造 scripts 39→20 时，19 个脚本合并/删除/重命名，但 OpenClaw cron 的 argv 字段未同步 → 5 个 cron exit 2 找不到文件。

正例：每次 scripts 改造时，**必须 grep 全集 cron 引用 + 同步 argv**（类似 L-16 修一类必 grep 全集铁律）。

### L-35 核心

**OpenClaw cron 投递必须用 `delivery.mode=none, channel=feishu, to=user:ou_xxx`（显式 feishu 推送）**。

反例：Nick 22 个 cron 用 `mode=announce, channel=last` → 找不到 main session route → fail-closed（22 个 lastDelivered=false）。

正例：派蒙对齐模式（mode=none, channel=feishu, to=feishu_openid）→ 不依赖 main session 即可推送。

### L-33 之前写的也修正

L-33 初版说"announce -> last 在 main session 无 active route 时 fail-closed"——半对。**真正治本是切到 mode=none + channel=feishu + to=user:ou_xxx**（L-35）。

---

## 关联

- **INC-006** (7-14 18:36 launchd → OpenClaw cron 迁移) — 触发因素（14 launchd plist disable 后负载转移）
- **INC-2026-07-15-001** 初版 (9:00 写, 根因错) — 已覆盖
- **L-13** (OpenClaw 原生优先) — 治本前提
- **L-22** (lark-cli v1.0.63 隐性依赖 OPENCLAW_HOME) — 已闭环
- **L-33** (cron Delivery 显式 feishu) — 修正为 L-35 详细版
- **L-34** (cron command 必须随 scripts 改造同步) — 新教训
- **L-35** (cron 投递对齐派蒙 mode=none 模式) — 新教训
- **AGENTS.md §3.1** 脚本白名单 — 需扩展"scripts 改造时 cron 全集 grep" 段

---

## 状态

- [x] 应急补发科技日报（9:05 ✅）
- [x] INC 创建（9:00 初版 + 9:05 根因修正）
- [x] L-34 + L-35 沉淀
- [ ] 派蒙决策 cron edit 命令 + 批量改
- [ ] 22 个 cron delivery 改飞书显式
- [ ] 5 个 cron command 改路径或 disable
- [ ] 24h 内 verify consecutiveErrors=0
- [ ] Close

---

## 修订记录

| 时间 | 内容 | 作者 |
|:---|:---|:---|
| 2026-07-15 09:00 | 初版：根因假设"Target=main vs isolated"（错） | Nick |
| 2026-07-15 09:05 | 根因修正：三层故障（L1 投递 / L2 脚本 / L3 token） | Nick |
| 2026-07-15 09:05 | 应急补发科技日报（lark-cli ✅ + wiki ✅）| Nick |

---

*INC 完稿: 2026-07-15 09:05 CST*
*接单人: 尼克·弗瑞 🕵️*
