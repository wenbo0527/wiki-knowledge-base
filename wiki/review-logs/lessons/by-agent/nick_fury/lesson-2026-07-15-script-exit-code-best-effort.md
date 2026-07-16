---
title: lesson 2026 07 15 script exit code best effort
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# L-36: 推送脚本退出码 = 0 当主通道（lark-cli）成功

> **教训族**：INC-2026-07-15-001 治本（脚本侧 + cron 侧 联动）
> **类别**：脚本质量 / Cron 退出码
> **创建**：2026-07-15 09:08
> **关联**：INC-2026-07-15-001 / L-22 / L-33 / L-35

---

## 反例（INC-2026-07-15-001 现场 · 改前）

**daily_tech_report.py 7-1 写的退出码逻辑**：

```python
success_count = sum(1 for ok, _ in results.values() if ok)
if success_count == 0:
    return 1  # 全失败
elif success_count < 3:
    return 1  # 部分失败（lark-cli 成功 + sessions_send 跳过 = 2/3 也算部分失败）
else:
    return 0  # 3/3 全成功
```

**问题**：
- sessions_send 在非 launchd 上下文（OpenClaw cron / 手动 shell）不可用 → 永远 2/3
- 实际 lark-cli 已经成功推送给文博，但脚本返 1
- OpenClaw cron 看到 exit 1 → lastRunStatus=error
- consecutiveErrors 持续累计

**根因**：
- 7-1 写脚本时只在 launchd 上下文测过（3/3 全成功）
- 7-14 INC-006 disable 14 launchd plist → 负载转 OpenClaw cron → 暴露 2/3 问题
- **L-22 治本未联动到脚本退出码**

---

## 正例（改后 · 9:08 verify）

```python
success_count = sum(1 for ok, _ in results.values() if ok)
lark_cli_ok = results.get("lark-cli", (False, ""))[0]
if success_count == 0:
    return 1  # 全失败
elif lark_cli_ok:
    return 0  # L-36: 主通道成功即视为推送成功
elif success_count < 3:
    return 1  # 主通道失败
else:
    return 0  # 3/3 全成功（理想情况）
```

**关键**：
- **lark-cli 主通道成功 = 推送成功**（lark-cli 推文博主动作）
- sessions_send 是 backup 通道（launchd 上下文才有，OpenClaw cron 没有是正常）
- wiki 是本地兜底（不阻塞飞书推送）

---

## 治本 SOP（推送脚本退出码 必检）

### ✅ 正确做法

| 场景 | 退出码 |
|:---|:---:|
| 主通道（lark-cli）成功 | **0** |
| 主通道失败但 backup/wik成功 | 1 |
| 全部失败 | 1 |
| 脚本异常 | 2 |

### ❌ 反例

| 场景 | 错误退出码 |
|:---|:---:|
| lark-cli 成功 + sessions_send 跳过 + wiki 成功 | 1（错） |
| 必须 3/3 全成功才返 0 | 太严格 |
| 主通道失败不报错直接返 0 | 太宽松 |

### 适用脚本（Nick 团队所有推送类）

| 脚本 | 当前是否已修 |
|:---|:---:|
| `daily_tech_report.py` | ✅ 9:08 修 |
| `daily_investment_report.py` | 🟡 待 9:15 修 |
| `evening_tracker.py` | 🟡 待 9:20 修 |
| `daily_note_scan.py` | 🟡 待 9:25 修（不推送，只入库）|
| `getnote_ej9_to_wiki.py` | 🟡 待 9:30 修（不推送，只入库）|

---

## L-15 端到端验证（改后必跑）

```bash
# 1. 语法检查
python3 -m py_compile scripts/<name>.py && echo "✅ 语法 OK"

# 2. OpenClaw cron 跑一次
openclaw cron run <id>

# 3. 等 3-5s，看 status
openclaw cron get <id> | python3 -c "
import json, sys
d = json.load(sys.stdin)
s = d.get('state', {})
print('lastRunStatus:', s.get('lastRunStatus'))
print('consecutiveErrors:', s.get('consecutiveErrors'))
"
# 期望: lastRunStatus=ok, consecutiveErrors=0
```

---

## 关联教训

- **L-22** (lark-cli v1.0.63 隐性依赖 OPENCLAW_HOME) — 推送通道上下文依赖
- **L-29** (自检必须区分"输出成功"和"输入真实") — 推送主通道 vs 备份通道
- **L-33** (cron Delivery 显式 feishu 初版) — 已合并到 L-35
- **L-35** (cron 投递对齐派蒙 mode=none 模式) — 治本 cron 侧
- **L-36** (脚本退出码 = 0 当主通道成功) — 治本脚本侧 · **本条**

---

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次写推送脚本** | 退出码逻辑按 L-36 模板 | 手动 |
| **每周一 09:00** | c3 cron check consecutiveErrors | c3 cron |
| **每次改推送脚本** | L-15 端到端验证（必跑）| 手动 |

---

*Lesson 完稿: 2026-07-15 09:08 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-001 ✅ 应急已闭环*