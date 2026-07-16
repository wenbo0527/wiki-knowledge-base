---
title: lesson 2026 07 15 cron delivery explicit feishu
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# L-33: OpenClaw cron Delivery 必须显式 feishu user-id 推送

> **教训族**：INC-2026-07-15-001 治本
> **类别**：OpenClaw 平台机制 / Cron 路由
> **创建**：2026-07-15 08:55
> **关联**：INC-2026-07-15-001 / INC-2026-07-14-006 / L-13 / L-22

---

## 反例（INC-2026-07-15-001 现场）

**Nick 团队 22 个 OpenClaw cron 全部 fail-closed**，Delivery 字符串：

```
announce -> last (last -> no route, will fail-closed: Deliver...)
```

**失败根因**：
- `announce -> last` 试图把消息回 Nick main session
- Nick main session 无 active route（LEADER 空闲 + 平时 active session 关闭）
- OpenClaw 平台 fail-closed 策略：不投递且 cron status=error

**业务影响**：
- 8:30 morning daily 不会自动跑
- 8:35 tech·briefing / etf.hegang.report 不推送
- 9:00 daily·report·c3 / wiki.daily·expander 不自检
- 21:00 daily·note·scan 不入库
- 23:00 / 0:30 bestpractice 不推送

---

## 正例（派蒙成熟模式）

**派蒙团队所有 cron Delivery 配置都是显式 feishu 推送**：

```
none -> feishu:ou_415aaf2674f34d5034a3e71882b89d94 (explicit)
```

**优点**：
- 不依赖 main session route
- 不依赖 platform session 状态
- 显式推送 → 即使 main session 不在也成功投递
- 即使 platform fail-closed 也不会 fail（status 仍 ok）

**Status 实证**：

| Cron | Target | Delivery | Status |
|:---|:---:|:---|:---:|
| 派蒙-8文件大小监控 | isolated | `none -> feishu:... (explicit)` | running ✅ |
| 派蒙-T3prime-自查-DAY | isolated | `none -> feishu:... (explicit)` | ok ✅ |
| 派蒙-T3prime-24h复检 | isolated | `none -> feishu:... (explicit)` | ok ✅ |
| 阿加莘-日报定时 | isolated | `none -> feishu:... (explicit)` | ok ✅ |
| 钟离-日报定时 | isolated | `none -> feishu:... (explicit)` | ok ✅ |

---

## 治本原则（Nick 团队 cron 注册/更新 必检）

### ✅ 必填字段（OpenClaw cron 注册脚本）

| 字段 | 值 | 说明 |
|:---|:---|:---|
| **Target** | `isolated`（派蒙同）| 独立 session 执行 |
| **Delivery** | `announce -> feishu:ou_ca04de68a40f571f59bcf2e71241415a (explicit)` | 显式推送文博 |
| **Agent ID** | `nick_fury` | 必须填，不能是 `-` |
| **Schedule** | cron 表达式 @ Asia/Shanghai | 时区显式 |

### ❌ 不要用

| 模式 | 后果 |
|:---|:---|
| `announce -> last` | 依赖 main session → fail-closed |
| `not requested` | 不投递，文博看不到 |
| Agent ID `-` | cron run 不能绑定 Nick agent |

---

## 验证步骤（注册/更新后 24h 内必跑）

```bash
# 1. 看 status 是否 ok
openclaw cron list | grep <cron-name>

# 2. 验证 Delivery 字符串
openclaw cron list | grep -E "announce.*feishu.*explicit"

# 3. 验证 Last Run 时间 ≤ 24h
openclaw cron list | grep <cron-id>

# 4. 验证 Agent ID 是 nick_fury（不是 -）
openclaw cron list | grep <cron-id>
```

---

## 操作 SOP

### 新建 Nick cron 时

```bash
openclaw cron add \
  --name "tech·briefing" \
  --schedule "35 8 * * *" \
  --tz Asia/Shanghai \
  --target isolated \
  --delivery "announce -> feishu:ou_ca04de68a40f571f59bcf2e71241415a (explicit)" \
  --agent nick_fury
```

### 批量迁移（22 个 cron）

```bash
# 1. 列出所有 Nick cron
openclaw cron list | grep -E "tech·briefing|morning·daily|rss.collect" | awk '{print $1}'

# 2. 对每个 cron 跑 openclaw cron update --delivery "..."
# （待 verify openclaw cron update 命令语法）
```

---

## 关联教训

- **L-13** (OpenClaw 原生优先) — 治本前提（选 cron 不选 launchd）
- **L-22** (lark-cli v1.0.63 隐性依赖 OPENCLAW_HOME) — 平台依赖
- **L-33** (cron Delivery 必须显式 feishu) — 投递机制
- **L-29** (自检必须区分"输出成功"和"输入真实") — Cron 投递也需核对

---

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每日 21:00** | c3_daily_check.py 检查 OpenClaw cron status | c3 cron |
| **每周一 09:00** | grep `announce -> last` 看是否还有未迁移 | 手动 |
| **新加 cron 后** | 24h 内 verify status=ok | 手动 |

---

*Lesson 完稿: 2026-07-15 08:55 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-001 ✅ 待闭环*