---
title: lesson 2026 07 01 lark cli scope
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-02
---

# Lesson 2026-07-01: lark-cli 授权两次扫坑（L-18）

> **作者**: 尼克·弗瑞 🕵️
> **日期**: 2026-07-01 11:25
> **触发**: 7-1 INC-009 修复 · lark-cli 用户身份授权 2 次扫码
> **关联**: INC-2026-07-01-001 / SOUL §9 / Lesson 2026-06-30 OpenClaw 原生优先

---

## L-18: lark-cli `--recommend` scope 不含 `im:message.send_as_user` —— 必须显式加

### 教训原文

> **`lark-cli auth login --recommend` 推荐 scopes 不含 `im:message.send_as_user`，这是 Lark 把"user 身份专属 message 发送权限"分离出来的"二段权限"，必须显式 `--scope "im:message.send_as_user"`。**

### 反例（我踩的 7-1 11:18）

```bash
# 我第一次用 --recommend（以为自动全授权）
lark-cli auth login --no-wait --recommend --json
# 拿到 100+ scopes，**包括 `im:message` 但不包括 `im:message.send_as_user`** ❌
# 推送时报错:
#   "missing required scope(s): im:message.send_as_user"
# → 文博必须扫第二次 QR（30 秒）
```

### 正例

```bash
# 一次到位：默认推荐 + 显式加 send_as_user
lark-cli auth login --no-wait \
  --recommend \
  --scope "im:message.send_as_user" \
  --json

# 文博扫一次 QR、点同意 → 全部 scopes 一次拿到 ✅
```

### 复用检测

```bash
# 1. 看 status 全 scope 列表（缺 send_as_user → 要再扫一次）
lark-cli auth status | python3 -c "
import json, sys
data = json.load(sys.stdin)
scopes = data['identities']['user'].get('scope', '').split()
needed = 'im:message.send_as_user'
status = '✅' if needed in scopes else '❌ 缺 ' + needed
print(f'当前 user scope: {len(scopes)} 个 · {status}')
"

# 2. 推送测试（推荐每改一次配置就跑一次）
lark-cli im +messages-send \
  --as user \
  --user-id ou_ca04de68a40f571f59bcf2e71241415a \
  --markdown "test" \
  --idempotency-key "test_$(date +%s)"
```

### 可执行（TOOLS.md §3 飞书情报系统）

**在 TOOLS.md 加 "lark-cli setup" 段**：

```markdown
## 3.1 lark-cli setup · 一次性（首次或重装后）

⚠️ L-18 教训：必须 2 次 scope 才能推送（recommend + send_as_user）

```bash
# Step 1: 默认推荐 scopes（一次扫 QR）
lark-cli auth login --no-wait --recommend --scope "im:message.send_as_user" --json
# 文博扫 QR + 同意

# Step 2: 完成 token
# (用 device_code 续)

# Step 3: 验证
lark-cli auth status  # user identity: ready
lark-cli im +messages-send --as user --user-id ou_xxx --markdown "test" --idempotency-key test
```

**Token 刷新**：expiresAt = 2h，refreshExpiresAt = 7d，cmd：`lark-cli auth refresh`

**Scope 检测命令**：见上方"复用检测"
```

---

## 7-1 修复时间线（30 秒授权 2 次）

| 时间 | 事件 | 状态 |
|:---:|:---|:---:|
| 11:18 | 第一次 device flow · --recommend | ❌ 缺 send_as_user |
| 11:21 | 第一次 --device-code 完成 | ✅ User ready |
| 11:21 | 试推送 → missing_scope send_as_user | 🔴 |
| 11:21 | 第二次 device flow · 显式加 send_as_user | - |
| 11:25 | 第二次 --device-code 完成 | ✅ User + send_as_user |
| 11:25 | 推送 daily_investment_report 通道 1 | ✅ lark-cli ✅ |
| 11:25 | 推送 daily_tech_report 通道 1 | ✅ lark-cli ✅ |

---

## 关联

- **INC-2026-07-01-001**：morning-rss-etf-push 3 通道失败（Layer 4 衍生）
- **L-13（OpenClaw 原生优先）**：这次没用 OpenClaw，是 lark-cli 原生命令，但仍踩了 scope 配置坑
- **L-17（写脚本前 read 3 行）**：本应先跑 `lark-cli auth status` 看现有 scope，避免两次扫

---

*沉淀: 尼克·弗瑞 🕵️ | 验证: 7-1 11:25 通道 1 ✅*
*下次审计: 7-3 周日 22:00 复盘*
