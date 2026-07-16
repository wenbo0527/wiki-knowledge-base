---
title: inc 2026 06 23 001 launchd 11 plists permissionerror
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-06]
date: 2026-06-30
---

# 🟠 Incident inc_2026-06-23_001: launchd 11 个 plist PermissionError 8 天未批量修复（6-15 INC 衍生）

| 字段 | 值 |
|:---|:---|
| **ID** | inc_2026-06-23_001 |
| **严重级别** | 🟠 High（情报链路半瘫 8 天 / 修复已完成）|
| **状态** | ✅ Resolved（2026-06-23 09:13 闭环）|
| **发现时间** | 2026-06-23 09:05（daily 自检 + launchctl list 扫描）|
| **发现者** | nick_fury（daily 自检触发）|
| **负责人** | nick_fury |
| **关联** | INC-2026-06-15-001（首批 PermissionError）· MEMORY.md L-4 · TOOLS.md §1 RSS 状态 6-15 · daily/2026-06-23.md |

---

## 问题描述

6-15 INC-2026-06-15-001 修复 `getnote-wiki-sync` 1 个 plist 后，**未批量修复其余 18 个 launchd plist**。6-23 09:05 自检时发现 22 个 plist 中：

- **12 个 78 状态**（PermissionError，root cause：plist 重复 `EnvironmentVariables` key）
- 4 个 1/2 状态（脚本级异常）
- 仅 8 个 0 状态（其中 6 个本来就不需访问 `/Users/wenbo/...`）

**链路影响**（6-15 ~ 6-23 共 8 天半瘫）：

| 链路 | plist | 影响 |
|:---|:---|:---|
| **RSS 抓取** | rss.collect / rss.daily / rss.organize | 8 天无新源增量 |
| **Wiki 索引** | wiki.daily-expander / wiki.ingest / wiki.monthly-refresher / wiki.weekly-synthesizer | 8 天无索引更新 |
| **KB 追踪** | kb.track | 8 天无 KB 监控 |
| **GitHub 追踪** | github.track | 8 天无 GitHub 监控 |
| **Best Practice** | bestpractice.round2 / bestpractice.daily / bestpractice.daily.collect | 8 天无最佳实践收集 |

---

## 影响分析

| 维度 | 说明 |
|:---|:---|
| **情报新鲜度** | RSS / GitHub / KB 监控数据 8 天滞后，错过 6-15 ~ 6-23 期间所有 ⭐⭐⭐⭐+ 内容 |
| **Wiki 健康度** | insights 增量停滞，C-3 cron 自检（21:00 写 vs 已完成比）无可信数据 |
| **C-3 自检失效** | "21:00 cron 扫描"依赖 wiki.lint 等 cron 上游，上游瘫 → 自检数据失真 |
| **不构成阻塞** | TOOLS.md / MEMORY.md 手动维护未中断，核心功能仍可工作 |

---

## 根因分析（分层）

### 表层：plist 语法错误

12 个 plist 都有**重复的 `<key>EnvironmentVariables</key>` 块**（每个出现 2 次）：

```xml
<!-- 错误结构 -->
<key>EnvironmentVariables</key>
<dict>
  <key>PATH</key>
  <string>...</string>
</dict>
<key>UserName</key>
<string>wenbo</string>
<key>EnvironmentVariables</key>  <!-- 重复！ -->
<dict>
  <key>UMASK</key>
  <string>022</string>
</dict>
```

**macOS launchd 行为**：
- plistlib 解析保留最后一个 dict（Python dict 同 key 覆盖语义）
- 但 launchd 解析时遇到重复 key 会**拒绝整个 plist**或**部分字段失效**
- `UserName` 在第二个块之后，导致 launchd **实际以默认用户**（root 或 launchd 上下文用户）运行
- 默认用户对 `/Users/wenbo/...` 路径无写权限 → PermissionError 78

### 深层：6-15 修复方案不可扩展

INC-2026-06-15-001 修复 `getnote-wiki-sync` 时：
- ✅ 方案正确：单一 `<key>EnvironmentVariables</key>` 块 + `UserName=wenbo` + `UMASK=022`
- ❌ 范围太窄：仅修了 1 个 plist，未推广到其他 18 个

**为什么没推广？** 反思：
1. 当时 INC 描述"plist 无 UserName"是简化描述，**真实根因是 plist 重复 key**——其他 18 个 plist 实际上**有 UserName=wenbo**！
2. 我（Nick）当时未对其他 plist 做差异性诊断，只套用了"加 UserName"模式
3. 没有脚本自动化，靠手工改 plist（如果当时写了脚本，6-15 当天就能修完）

---

## 解决措施

### 修复脚本（09:12 执行）

| 工具 | 用途 |
|:---|:---|
| `/tmp/fix_launchd_plists.py` | 解析 plist → 检测重复 EnvironmentVariables → 合并到一个 dict → 写回 |
| 备份 | `~/Library/LaunchAgents/*.bak.20260623`（12 个 plist）|
| 重启 | `launchctl bootout` + `launchctl bootstrap` |

### 修复结果（09:13 验证）

| plist | 修复前 | 修复后 |
|:---|:---:|:---:|
| rss.collect | 🔴 78 | 🟢 0 |
| rss.daily | 🔴 78 | 🟢 0 |
| wiki.daily-expander | 🔴 78 | 🟢 0 |
| wiki.ingest | 🔴 78 | 🟢 0 |
| wiki.monthly-refresher | 🔴 78 | 🟢 0 |
| github.track | 🔴 78 | 🟢 0 |
| kb.track | 🔴 78 | 🟢 0 |
| rss.organize | 🔴 78 | 🟢 0 |
| bestpractice.round2 | 🔴 78 | 🟢 0 |
| bestpractice.daily | 🔴 78 | 🟡 2（脚本级异常，plist 已修）|
| bestpractice.daily.collect | 🔴 78 | 🟢 0 |
| wiki.weekly-synthesizer | 🔴 78 | 🟢 0 |

**11/12 修复成功**（bestpractice.daily 的 2 状态是脚本本身异常，需单独排查）

---

## 教训沉淀

| ID | 教训 | 验证方法 |
|:---:|:---|:---|
| **L-7** | **修一个 ≠ 修一类**：修复单实例问题后，必须立即 grep 全集是否有同类问题 | 修复 `getnote-wiki-sync` 后应 `grep -l "EnvironmentVariables" *.plist` |
| **L-8** | **描述根因要精准**：6-15 INC 描述"plist 无 UserName"是错的，实际是"plist 重复 EnvironmentVariables"。错描述导致错方案推广 | INC 报告必须附 plist 原文片段 |
| **L-9** | **修复需脚本化**：手工改 plist 易漏，脚本一次扫描 + 备份 + 修复 + 验证 = 闭环 | 6-23 脚本 `/tmp/fix_launchd_plists.py` 验证有效 |
| **L-10** | **launchctl list 78 状态必查**：cron 自检脚本必须把 78 状态视为 🔴 Critical，不能忽略 | C-3 cron 增加 `grep " 78 " launchctl_list.txt` |

---

## 验证清单（24h 观察）

- [x] 09:13 修复完成，11/12 launchctl status=0
- [ ] 09:00 6-24 观察 wiki-health-check 自动 cron（看 health 报告是否变绿）
- [ ] 23:00 6-23 观察 rss.collect 自动 cron（看是否抓到新源）
- [ ] 24h 后 rss.collect / wiki.daily-expander 是否有新数据落盘

---

*Owner: nick_fury*
*Created: 2026-06-23 09:13*
*Status: ✅ Resolved*
*Review: 6-24 09:00 cron 验证 + MEMORY.md 更新*