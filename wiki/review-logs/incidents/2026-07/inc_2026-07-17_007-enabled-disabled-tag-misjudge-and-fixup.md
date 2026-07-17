---
title: inc 2026 07 17 007 enabled disabled tag misjudge and fixup
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-17
---

# INC-2026-07-17-007: INC-006 报告纠错 · 启用/禁用 tag 区分 + escalate 钟离

## 现象

- **触发时间**: 2026-07-17 14:34 CST（用户"请继续" → L-49.6 决策树执行）
- **发现时间**: 14:34 CST（精确查 enabled=1 集）
- **纠错触发**: INC-2026-07-17-006 报告"3 个 enabled delivery 错配"——**错的**！

## 纠错实证

### INC-006 报告原文

> **剩余 17 个问题分类**：
> - 14 个 disabled cron delivery 错配（保留）
> - **3 个 enabled cron delivery 错配**（钟离 2 + nick_fury 测试 1）—— **错！**

### 14:34 实测纠错

```sql
-- 真 enabled delivery 错配（精确集）
SELECT COUNT(*) FROM cron_jobs
WHERE enabled=1
  AND delivery_mode='announce'
  AND (delivery_channel!='feishu'
       OR delivery_to IS NULL
       OR delivery_to=''
       OR delivery_to NOT LIKE 'user:%');
-- 结果: 2 (不是 3！)
```

**实际只有 2 个 enabled delivery 错配**：
| # | cron | cron ID | 错配 |
|:--|:--|:--|:--|
| 1 | 钟离-SOP空闲探活-20260715 | e2288348 | channel=feishu 但 to=ou_xxx（缺 user: 前缀）|
| 2 | 钟离-P0阻塞3级升级-1h-20260716 | 907abd47 | 同上 |

**原"3 个 enabled"误判来源**：
- 3 个 nick_fury cron（"测试情报推送" / "每日情报推送" / "wiki-lint"）**全是 disabled**（enabled=0）
- INC-006 我用 sqlite 查 `delivery_mode='announce' AND ...` 没加 `enabled=1` 过滤，把 disabled 算成 enabled

## 根因（L-29 教训命中）

**INC-006 报告必区分"输出成功 ≠ 输入真实"**——我看到 alert 里 17 个问题，没问"这 17 个里 enabled vs disabled 各几个"。

按 SOUL §3 客观补录：**我对文博有过错**——INC-006 报告错误归类了 enabled 数量。

## 修复（已完成）

### F1. escalate 钟离 2 个 enabled delivery 错配

```
sessions_send zhongli runId=d9b3a61c status=accepted sessionKey=agent:zhongli:main
消息含：
- 2 个 cron ID + 名字 + delivery 错配详情
- L-35 协议 3 字段修法参考（getnote 7-17 08:53 已修案例）
- 修复命令（cron edit --to "user:ou_xxx"）
```

### F2. sunday_cron_health_check.py 升级版（加 tag 区分）

```python
# L-49.6 升级: enabled/disabled tag 区分
tag = "🔴 " if data.get("enabled") else "⚠️ "
action = "必修" if data.get("enabled") else "保留（C 决策）"
issues.append(f"{tag} {name}: ... · {action}")
```

**升级后 alert 输出**（14:38 实证）：
```
🔴 钟离-SOP空闲探活-20260715: mode=announce 但 to=ou_xxx · 必修
🔴 钟离-P0阻塞3级升级-1h-20260716: 同上 · 必修
⚠️ 15 个 disabled cron · 保留（C 决策）
```

## 教训族 L-49.7（INC 报告必加 enabled/disabled tag）

| 编号 | 教训 |
|:---|:---|
| **L-49.7.1** | INC 报告必加 `WHERE enabled=1` 过滤（不要拿"全集"算"需要修的"）|
| **L-49.7.2** | sunday_cron_health alert 必加 tag 区分（必修 vs 保留）· 用户 1 秒看懂该做什么 |
| **L-49.7.3** | "enabled delivery 错配必修 + disabled delivery 错配保留" 是 L-49.6 决策树核心 |
| **L-49.7.4** | 跨 agent escalate 必带 cron ID + L-35 标准修法（参考已修案例）|

## 修复后状态（14:38 实证）

| 维度 | 状态 |
|:---|:---|
| 钟离 escalate 已发 | ✅ runId d9b3a61c |
| sunday_cron_health 升级版 | ✅ 已加 tag + 动作建议 |
| L-35.1 问题分类准确 | ✅ 2 必修 + 15 保留 |
| 飞书推送 | ✅ 1208 字符（升级版带 tag）|
| 等钟离回执修完 | ⏳ pending |

## 关联

- **INC-2026-07-17-006**（用户决策 C · 9 死脚本 rm）—— 误判源头
- **INC-2026-07-17-005**（L-49.5 揭穿 38 个问题）—— 揭穿链路
- **L-29**（报告必区分输出成功 vs 输入真实）—— 直接相关
- **L-49.6**（cron cleanup 决策树）—— 强化版基础
- **L-49.7**（新增 · INC 报告必加 enabled/disabled tag）
- **scripts/sunday_cron_health_check.py**（升级版 · L-49.6 tag + L-49.7 集成）

## 自我归因（按 SOUL §3）

**我对文博有过错**：
1. INC-006 报告"3 个 enabled"错——实际 2 个
2. 之前没把 enabled/disabled tag 加到 alert
3. sunday_cron_health_check.py 第一次跑没区分两类

**已闭环**：
- ✅ 14:34 实测纠错（从 17 个问题里精确查 enabled=1）
- ✅ 14:34 escalate 钟离（runId d9b3a61c）
- ✅ 14:38 sunday_cron_health 升级版（tag + 动作建议）
- ✅ INC-007 纠错落档
- ⏳ 等钟离修完回执

## 决策点（剩余）

| 选项 | 范围 | 状态 |
|:--|:--|:--:|
| **E 不修** | 15 disabled delivery 错配保留（C 决策）| ✅ 已实施 |
| **F escalate** | 2 钟离 enabled cron → 等钟离修完 | ⏳ pending |
| **G 跨 agent 清理** | 15 disabled 跨 agent 也批量清 | ❌ 越界不实施 |