---
title: inc 2026 07 17 004 wiki health duplicate run
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-17
---

# INC-2026-07-17-004: wiki·health·check 双跑（OpenClaw cron + launchd plist 同脚本 9:00）

## 现象

- **触发时间**: 2026-07-14 09:00 CST 起（每天 9:00 双跑 wiki_health_check.sh）
- **发现时间**: 2026-07-17 07:58 CST（"请检查下遇到的问题"诊断时发现 wiki_health.log 双时间戳）
- **影响 cron + plist**:
  - **OpenClaw cron**: `da137eba-569b-46ab-bced-c515f626c186 wiki·health·check` (cron 0 9 * * * Asia/Shanghai)
  - **launchd plist**: `/Users/wenbo/Library/LaunchAgents/com.nickfury.wiki-health-check.plist` (Hour=9, Minute=0)
- **错误实证**:

```
# data/wiki_health.log 9:00 时间戳每天都是 2 条
✅ 健康检查完成: Tue Jul 14 09:00:01 CST 2026
✅ 健康检查完成: Tue Jul 14 09:00:06 CST 2026     ← 双跑
✅ 健康检查完成: Wed Jul 15 09:00:01 CST 2026
✅ 健康检查完成: Wed Jul 15 09:00:02 CST 2026     ← 双跑
✅ 健康检查完成: Thu Jul 16 09:00:00 CST 2026
✅ 健康检查完成: Thu Jul 16 09:00:02 CST 2026     ← 双跑
✅ 健康检查完成: Thu Jul 16 19:38:36 CST 2026     ← 手动触发？
✅ 健康检查完成: Thu Jul 16 19:38:57 CST 2026     ← 手动触发？

# 两个机制 argv 完全相同
openclaw cron get da137eba → argv: [sh, -lc, /bin/bash .../scripts/wiki_health_check.sh]
launchd plist com.nickfury.wiki-health-check → /bin/bash .../scripts/wiki_health_check.sh
```

## 根因

**INC-2026-07-14-006（launchd → OpenClaw cron 迁移）治本不彻底**——

| 7-14 INC-006 决策 | 实际状态 |
|:---|:---|
| ✅ 14 个重复 launchd plist disable | ✅ 完成 |
| ✅ wiki-health-check 保留 launchd（**TCC 限制**）| ✅ 决策正确 |
| ❌ **OpenClaw cron da137eba 没 disable** | ❌ 决策遗漏 |
| ❌ **没在 AGENTS.md 写入"wiki-health-check 是 launchd 专属"** | ❌ 文档遗漏 |

**L-13 治本未彻底**：
- L-13 7-14 决策"wiki.health.check 保留 launchd 绕过 TCC" 是正确的
- 但决策时只看了"launchd plist + OpenClaw cron 双跑"这个事实
- 没做对应的"双跑 = 必 disable 一个"动作

**为什么 wiki_health_check TCC 限制**：
- launchd plist UserName=wenbo + 9:00 跑 `wiki_health_check.sh`
- 该脚本内部 `find /Users/wenbo/Documents/project/Wiki -name "*.md"` 需要 TCC 权限
- 在 OpenClaw cron gateway 进程下没 wenbo TCC（gateway 进程是 root 或系统用户）
- 所以必须保留 launchd plist

**正确修法**：保留 launchd plist，disable OpenClaw cron（而非反向，因为 launchd 是为了 TCC）。

## 修复（1min · 8:53 完成）

```bash
# F6. disable OpenClaw cron wiki·health·check（保留 launchd plist）
openclaw cron edit da137eba-569b-46ab-bced-c515f626c186 --disable

# 验证
openclaw cron get da137eba-569b-46ab-bced-c515f626c186 | grep enabled
# ✅ enabled: false
```

**修复后状态**：
- OpenClaw cron da137eba → disabled
- launchd plist com.nickfury.wiki-health-check → 保留（9:00 跑）
- 明早 7-18 09:00 只跑 1 次（launchd 单独）

## 教训族 L-13.1（launchd 专属决策必 disable 对应 OpenClaw cron）

| 编号 | 教训 |
|:---|:---|
| **L-13.1.1** | launchd 专属决策必 3 步：(1) 决策保留 launchd (2) **disable 对应 OpenClaw cron** (3) AGENTS.md 写入决策 |
| **L-13.1.2** | 双跑必 grep 全集（`openclaw cron list` + `launchctl list | grep com.nickfury`）—— 跨机制全集 |
| **L-13.1.3** | wiki_health_check.log 9:00 双时间戳 = 双跑信号（任何 log 同分钟双记录 = 必查） |
| **L-13.1.4** | 7-19 周日 cron 新增 "launchd plist vs OpenClaw cron 跨机制重复检测" |

## 关联

- **INC-2026-07-14-006**（launchd → OpenClaw cron 迁移）—— L-13 原版
- **L-13**（OpenClaw 原生优先 · 7-14 决策）—— 原版
- **L-13.1**（新增 · launchd 专属必 disable 对应 OpenClaw cron）
- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— 同一治理族
- **cron da137eba**（已 disable · launchd plist 保留）