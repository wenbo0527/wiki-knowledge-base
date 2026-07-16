---
title: lesson 2026 07 15 cron command sync
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# L-34: OpenClaw cron `command` 字段（payload.argv）必须随 scripts 改造同步更新

> **教训族**：INC-2026-07-15-001 治本
> **类别**：OpenClaw 平台机制 / Cron 配置 / Scripts 改造
> **创建**：2026-07-15 09:05
> **关联**：INC-2026-07-15-001 / L-16 / L-35 / AGENTS.md §3.1

---

## 反例（INC-2026-07-15-001 现场）

**7-1 改造 scripts 39→20 时**（AGENTS.md / SOUL 升级），**5 个 OpenClaw cron 的 argv 字段未同步**：

| Cron | argv（指向）| 实际状态 |
|:---|:---|:---|
| `tech·briefing` (8f14728b) | `python3 scripts/tech_briefing.py` | ❌ ERRNO 2 — 已合并到 daily_tech_report.py |
| `daily·note·scan` (14550600) | `python3 scripts/weekly_note_scan.py` | ❌ ERRNO 2 — 改名 daily_note_scan.py |
| `morning·rss·etf·push` (1032cfb0) | `python3 scripts/morning_rss_etf_push.py` | ❌ ERRNO 2 — 已合并到 daily_tech_report.py |
| `投资纪律-每日汇总` (68fbf538) | `python3 scripts/daily_investment_summary.py` | ❌ ERRNO 2 — 7-14 ETF 估值迁移后撤了 |
| `投资纪律-周报` (6e96cc0d) | `python3 scripts/daily_investment_summary.py` | ❌ ERRNO 2 — 同上 |

**为什么 5 个 cron 暴露出来**：
- 7-1 之前：launchd plist `com.nickfury.daily-tech-push` 跑 daily_tech_report.py（plist 与 scripts 同步改）
- 7-1 ~ 7-14：launchd plist 还在跑，掩盖了 OpenClaw cron argv 失效问题
- 7-14 18:36 INC-006 disable 14 个 launchd plist → 所有负载转移到 OpenClaw cron → 立刻暴露 5 个 argv 失效

**业务影响**（7-14 18:36 ~ 7-15 09:00）：
- tech·briefing / daily·note·scan / morning·rss·etf·push 一直没跑成功
- 投资纪律-每日汇总 / 投资纪律-周报 一直没跑成功
- 文博 7-15 早问"今天没收到科技日报"才揭穿

---

## 正例（改造时必检 SOP）

### 步骤 1：scripts 改造前先 grep cron 引用

```bash
# 列出所有 cron argv 实际引用
for cron_id in $(openclaw cron list | awk '{print $1}'); do
  argv=$(openclaw cron get $cron_id 2>&1 | python3 -c "import json,sys; print(' '.join(json.load(sys.stdin).get('payload',{}).get('argv',[])))")
  echo "$cron_id | $argv"
done > /tmp/all_cron_argv.txt

# 找出所有引用即将被改/删的脚本的 cron
grep -E "scripts/tech_briefing\.py|scripts/weekly_note_scan\.py|scripts/morning_rss_etf_push\.py|scripts/daily_investment_summary\.py" /tmp/all_cron_argv.txt
```

### 步骤 2：scripts 改造时同步更新 cron argv

**3 种处理**：

| 情况 | 操作 |
|:---|:---|
| 脚本合并到新脚本（如 tech_briefing.py → daily_tech_report.py） | `openclaw cron edit <id> --command "python3 <new_script>.py"` |
| 脚本改名（如 weekly_note_scan.py → daily_note_scan.py） | `openclaw cron edit <id> --command "python3 <new_name>.py"` |
| 脚本废弃（如 daily_investment_summary.py ETF 撤了） | `openclaw cron disable <id>` 或 `openclaw cron rm <id>` |

### 步骤 3：改造后 24h 内 verify

```bash
# 跑 1 次后看 exit code
openclaw cron run <id>

# 看 lastRunStatus
openclaw cron get <id> | grep -E "lastRunStatus|lastError"
```

---

## 操作 SOP（scripts 改造 checklist）

```
□ 1. 改造前先 grep cron argv（步骤 1）
□ 2. 改造时同步 edit/disable cron（步骤 2）
□ 3. 改造后 24h 内 verify（步骤 3）
□ 4. AGENTS.md §3.1 脚本白名单同步更新
□ 5. lessons/ 写一条新 L-N 沉淀（如涉及新模式）
```

---

## 关联教训

- **L-16** (修一类必 grep 全集铁律) — 通用方法论（修 plist PATH/UMASK 时同类）
- **L-34** (cron argv 必须随 scripts 改造同步) — 本条
- **L-35** (cron 投递必须 mode=none + channel=feishu + to=feishu_openid) — 配对
- **L-13** (OpenClaw 原生优先) — 治本前提
- **AGENTS.md §3.1 脚本白名单** — 需扩展 "scripts 改造时 cron 全集 grep" 段

---

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次 scripts 改造** | grep cron argv + 同步 update | 手动 |
| **每周一 09:00** | cron status 全量检查（命令错误检测）| 新 c3 检查项 |
| **每日 21:00** | c3_daily_check.py 看 consecutiveErrors | c3 cron |

---

*Lesson 完稿: 2026-07-15 09:05 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-001 ✅ 应急已闭环*