---
title: inc 2026 07 17 006 cron cleanup c partial 9 dead scripts
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-17
---

# INC-2026-07-17-006: 用户决策 C · 批量删除 9 个 OpenClaw 死脚本 cron

## 现象

- **触发时间**: 2026-07-17 14:29 CST（用户拍"C 部分清"决策）
- **执行时间**: 14:29-14:31 CST（2min）
- **删除对象**: 9 个 disabled cron（argv 路径不存在的死脚本）
- **保留对象**: 27 个 disabled cron delivery 错配（按 C 决策"保留 disabled delivery 错配"）+ 2 个钟离 enabled cron

## 决策背景

候选 #C 二段揭穿 38 个问题后，给文博 A/B/C/D 4 个决策点：
- A 不修（拖 2 天）
- B 批量删（9 死脚本 + 27 disabled delivery 全删）
- **C 部分清（只删 9 死脚本 cron + 保留 disabled delivery 错配）** ← 用户选
- D escalate 钟离

## 修复实证（2min · 14:30-14:31 CST）

### §5 安全边界：删除前必备份

```bash
cp ~/.openclaw/state/openclaw.sqlite \
   ~/.openclaw/state/openclaw.sqlite.bak-2026-07-17-pre-delete-dead-scripts-1784269807
# ✅ 备份 91MB
```

### F1. 9 个 rm 实证（14:30:35 CST）

| cron | ID | 状态 |
|:--|:--|:--:|
| `bestpractice.daily.append` | 28f1e956-400f-436b-9a2d-3be549bef61e | ✅ removed |
| `morning·rss·etf·push` | 1032cfb0-2dad-49b6-ace0-d6a4a688476f | ✅ removed |
| `rss.organize` | 8976a6aa-2168-4e6f-b069-72f902f4343b | ✅ removed |
| `wiki.daily·expander` | 12b84189-4d5b-4fed-bbef-d80c50c82feb | ✅ removed |
| `wiki.ingest` | cfe440d7-bd90-4779-9029-59c1d5de2db8 | ✅ removed |
| `wiki.monthly·refresher` | e71b27b2-e1b5-4a3a-8fbe-5333d4539cad | ✅ removed |
| `wiki.weekly·synthesizer` | c39d124c-7c70-4755-ab02-a40e5e55308f | ✅ removed |
| `投资纪律-周报` | 6e96cc0d-2df4-45b0-9b9c-9cbe930b22d7 | ✅ removed |
| `投资纪律-每日汇总` | 68fbf538-d910-4c64-9ed7-aa1d8daaa9c2 | ✅ removed |

**成功**: 9/9（修一波 shell 解析 bug 后）

### F2-F3. sqlite 验证（78 → 69）

```
F2 总数: COUNT(*)=69, SUM(enabled)=50 (50 enabled, 19 disabled)
F3 9 个 cron 已不在: COUNT(*)=0 ✅
```

### F4. sunday_cron_health_check.py 复跑（14:31:27 CST）

```
✅ L-48 通过
✅ L-49 通过（9 个死脚本都没了）
❌ L-35.1 17 个问题（从 29 → 17，减少 12 个同 cron delivery 错配）
✅ L-13.1 通过
汇总: 17 个问题（从 38 → 17，减少 21 个）
```

## 教训族 L-49.6（cron cleanup 决策树 · 部分清模式）

| 编号 | 教训 |
|:---|:---|
| **L-49.6.1** | cron cleanup 决策树：(1) enabled argv 死脚本 → 必 disable 或修 (2) disabled argv 死脚本 → 必删（C 模式）(3) enabled delivery 错配 → 必修 (4) disabled delivery 错配 → 保留不动 |
| **L-49.6.2** | 任何 cron 删除前必备份 sqlite（§5 安全边界 · L-49.6 强化）|
| **L-49.6.3** | shell 变量解析陷阱：`VAR="a b c"` for ID in $VAR 当一个 string 用 → 必用 while 循环逐个处理 |
| **L-49.6.4** | 7-19 周日 cron 自动复查 L-49.5 揭穿的死脚本 → L-49.6 自动清理流程（待集成）|

## 剩余 17 个问题分类

| 类别 | 数量 | 风险 |
|:--|:--:|:--:|
| **disabled cron delivery 错配**（保留）| **14 个** | 🟢 低（disabled 不跑推送）|
| **enabled cron delivery 错配**（钟离 + nick_fury 历史测试）| **3 个** | 🔴 中（推送失败）|

## 关联

- **INC-2026-07-17-005**（L-49.5 升级揭穿 38 个新问题）—— 揭穿
- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— L-35 原版
- **候选 #C 二段**（L-49.5 升级）—— 揭穿链路
- **L-49.6**（新增 · cron cleanup 决策树 · 部分清模式）
- **scripts/sunday_cron_health_check.py**（升级版 · 自动复查 17 个剩余问题）

## 自我归因（按 SOUL §3）

**我对文博有过错**：
1. shell 变量解析 bug（第一次 9 个 rm 失败）—— L-49.6.3 强化
2. 之前清理 disabled cron 没区分"argv 死脚本"vs"delivery 错配"—— L-49.6.1 决策树补

**已闭环**：
- ✅ shell bug 修（用 while 循环）
- ✅ 9 个 rm 实证
- ✅ sqlite 验证（78→69）
- ✅ sunday_cron_health_check baseline 改善
- ⏳ 14 个 disabled delivery 错配 + 3 个 enabled delivery 错配（钟离等）待决策

## 决策点（剩余 · 待文博）

| 选项 | 范围 |
|:--|:--|
| **E 不修** | 14 个 disabled delivery 错配保留，3 个 enabled delivery 等钟离处理 |
| **F escalate** | sessions_send 给钟离 3 个 enabled cron delivery 错配 |
| **G 跨 agent 清理** | 14 个 disabled delivery 错配也批量清 |