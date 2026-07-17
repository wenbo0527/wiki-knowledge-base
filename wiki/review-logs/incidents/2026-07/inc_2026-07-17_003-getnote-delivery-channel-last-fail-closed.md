---
title: inc 2026 07 17 003 getnote delivery channel last fail closed
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-17
---

# INC-2026-07-17-003: getnote·wiki·sync delivery channel=last 无 to → fail-closed（L-35 7-15 没复查）

## 现象

- **触发时间**: 2026-07-17 06:00 CST（cron 自动触发）
- **发现时间**: 2026-07-17 08:50 CST（用户决策 B 完整修复时查到）
- **影响 cron**: `d795c8d4-06c2-4371-8ed4-36d0f71f321c getnote·wiki·sync` (cron 0 6 * * * Asia/Shanghai)
- **持续时长**: ≥ 24h（7-15 INC-001 治本后未复查 getnote delivery）
- **错误实证**:

```
delivery:
  mode: announce
  channel: last           ← 错！不是 feishu
  to: (空)                ← 错！没指定 user
lastDelivered: false
lastDeliveryStatus: not-delivered
lastFailureNotificationDeliveryStatus: not-requested

# cron list 列表里显示:
announce -> last (last -> no route, will fail-closed: Deliver...)
```

**L-29 命中**：`lastRunStatus: ok` + `lastDeliveryStatus: not-delivered`——脚本执行成功但**推送失败**！

## 根因

**INC-2026-07-15-001（OpenClaw cron 25 任务 fail-closed）治本不彻底**——

| 7-15 INC-001 修复范围 | 实际漏修 |
|:---|:---|
| ✅ 5 个 cron argv 失效 | ❌ **getnote·wiki·sync delivery channel=last 未在 5 个里** |
| ✅ L-35 "cron 投递必对齐派蒙（mode=none, channel=feishu, to=user:ou_xxx）" 写入 | ❌ **复查机制缺**——L-35 写完没"7-15 后所有 cron delivery 复查"动作 |

**getnote·wiki·sync 推送失败链路**：
1. 6:00 cron 触发
2. `getnote_to_wiki.sh` 跑通（exit 0）✅
3. cron 试图推送 delivery `channel=last` —— last 是个特殊 channel 标识"上一次推送的 channel"
4. **没有上一次推送**（这是 cron isolated session，不是用户会话）
5. → "no route, will fail-closed" → 推送跳过
6. → 文博收不到 getnote 同步完成通知

**为什么 7-15 没发现**：INC-001 治本时只看 `lastRunStatus != ok` 的 5 个 cron，没看 `lastRunStatus=ok + lastDelivered=false` 这种"假阳性"状态（L-29 教训）。

## 修复（5min · 8:53 完成）

```bash
# F5. cron edit getnote 改 delivery 对齐派蒙模式
openclaw cron edit d795c8d4-06c2-4371-8ed4-36d0f71f321c \
  --channel feishu \
  --to "user:ou_ca04de68a40f571f59bcf2e71241415a"

# 验证
openclaw cron get d795c8d4-06c2-4371-8ed4-36d0f71f321c | grep -A4 delivery
# ✅ delivery.mode=announce, channel=feishu, to=user:ou_ca04de68a40f571f59bcf2e71241415a
```

**修复后状态**：delivery 对齐派蒙模式，下次跑（明早 7-18 06:00）会真推送到文博飞书。

## 教训族 L-35.1（INC 治本后必复查同类全集）

| 编号 | 教训 |
|:---|:---|
| **L-35.1.1** | 任何 INC 治本后 24h 内必 grep 同类全集（"修一个 ≠ 修一类，修一类 ≠ 修一类再 grep 一次" = L-16 升级）|
| **L-35.1.2** | cron delivery 复查必 3 字段：`mode=none` + `channel=feishu` + `to=user:ou_xxx`（缺一即 fail-closed）|
| **L-35.1.3** | "假阳性"检测：`lastRunStatus=ok + lastDelivered=false` = 推送失败（不是 ok）—— L-29 升级 |
| **L-35.1.4** | 7-19 周日 cron 新增 "OpenClaw cron delivery 复查" 检查项（每周日扫一遍所有 cron delivery）|

## 关联

- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— L-35 原版 + L-34 原版
- **L-29**（报告必区分"输出成功"和"输入真实"）—— 直接相关
- **L-35**（cron 投递必对齐派蒙）—— 原版
- **L-35.1**（新增 · INC 治本后同类复查）
- **cron d795c8d4**（明早 7-18 06:00 验证 status=ok + 真推送文博飞书）