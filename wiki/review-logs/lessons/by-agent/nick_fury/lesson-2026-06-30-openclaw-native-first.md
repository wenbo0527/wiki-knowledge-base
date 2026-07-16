---
title: lesson 2026 06 30 openclaw native first
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-06-30
---

# Lesson-2026-06-30：OpenClaw 原生优先（最高优先级教训）

> **作者**：尼克·弗瑞
> **日期**：2026-06-30
> **触发**：文博 6-30 10:04 显式要求"请记住这个教训"
> **关联 INC**：INC-2026-06-30-001（推送链路断裂 + launchd 23 plist 退役）
> **教训等级**：🔴 P0（直接决定未来所有定时/后台任务的决策）

---

## 一、教训原文

**当 OpenClaw 有原生功能的时候，是否都可以用。**

—— 文博，2026-06-30 10:04，飞书

---

## 二、教训展开（4 个维度）

### 2.1 反例（我踩过的坑）

| 自建方案 | OpenClaw 原生 | 我的错误 |
|:---|:---|:---|
| launchd plist × 23 | `openclaw cron add` | Nick 单打独斗 23 plist，派蒙/钟离/托尼都用 cron |
| 独立 Standing Orders .md 文件（file:// 引用） | AGENTS.md 顶部 Program 段（auto-inject）| 每次会话靠 grep 路径，不在 bootstrap 里 |
| 手动 `tail -f data/*.log` 自检 | `openclaw cron list \| grep error` + `openclaw tasks audit` | 监督层脱离官方机制 |
| 自建 Wiki Health Check 脚本 | `openclaw tasks audit` + `openclaw doctor` | 6-15 wiki-health-check PermissionError 44 天未发现 |
| 自建 9 通道多路推送 | cron `delivery.mode=announce`（feishu/webhook/iMessage 统一）| 6-30 morning_rss_etf_push 3 通道全失败 |

### 2.2 OpenClaw 原生 6 大机制（决策树）

```
需要做一件事？
    │
    ├─ 有时间规律？ → openclaw cron（不是 launchd / crontab）
    │
    ├─ 需要主会话感知？ → heartbeat（不是自建 session 自查）
    │
    ├─ 多个步骤串起来？ → TaskFlow（不是 shell 脚本串联）
    │
    ├─ 需要持续后台记账？ → openclaw tasks（不是 log 文件 + grep）
    │
    ├─ 需要永久授权？ → Standing Orders 写 AGENTS.md 顶部 Program 段
    │
    └─ 需要事件触发？ → hooks（不是 cron 轮询）
```

### 2.3 决策原则（每次新任务前必做）

```
1. openclaw <subcommand> --help          ← 先看 CLI 原生能力
2. /opt/homebrew/lib/node_modules/openclaw/docs/<相关>/   ← 先看官方文档
3. knowledge_search(query="OpenClaw 原生 <场景>")  ← 查内部知识库
4. 只有原生不覆盖时，才自建 + 标注 ⚠️ 非原生 + 写 INC 教训
```

### 2.4 例外情况（哪些真的不能用原生）

| 场景 | 原因 | 自建方案 |
|:---|:---|:---|
| **TCC 权限拦截**（macOS Sequoia）| launchd 进程不能访问 `~/Documents` | 改用进程能访问的路径 / 用 RAG API 代理 |
| **需要 XPC 长连接** | OpenClaw 没原生 long-running daemon | launchd KeepAlive=true 是 OK 的 |
| **系统级硬件监控**（如温度/电池）| OpenClaw 没传感器抽象 | launchd + shell 是 OK 的 |
| **跨平台 Linux/Windows** | macOS launchd 仅 macOS | systemd / Windows Task Scheduler |

---

## 三、Nick 立即应用清单（6-30 ~ 7-7）

- [ ] Phase 2：launchd 23 plist 全部迁到 `openclaw cron`（已立 INC-001）
- [ ] Phase 3：Standing Orders v2.0 写进 AGENTS.md 顶部 Program 段
- [ ] Phase 4：C-3 cron 自检脚本改用 `openclaw cron list | grep error`（不用 launchctl 78）
- [ ] 周日 22:00 复盘：检查本周新加的 3 个任务是否走原生
- [ ] 下次开新定时任务：先 `openclaw cron --help` + 看 docs/automation/

---

## 四、给团队的元教训

**对自己造的轮子保持警惕**。OpenClaw 0.96+ 已经覆盖 80% Agent 调度需求，剩下 20% 自建前必须确认：
1. OpenClaw 真的没有原生（看 docs + CLI help）
2. 自建有明确理由（不是"我不知道有原生"）
3. 自建方案写 INC 标注 ⚠️ + 跟踪官方是否后续支持

**没标注的 launchd plist = 我下次又踩坑。**

---

*作者：尼克·弗瑞 🕵️*
*状态：🟢 Active — 每次新任务前必读*
*关联：INC-2026-06-30-001 / L-13（MEMORY.md 同步更新）*
