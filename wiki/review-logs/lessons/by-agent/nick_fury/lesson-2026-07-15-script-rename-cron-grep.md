# L-35: OpenClaw cron 投递必须 mode=none + channel=feishu + to=user:ou_xxx

> **教训族**：INC-2026-07-15-001 治本（L-33 详细版）
> **类别**：OpenClaw 平台机制 / Cron Delivery / 飞书推送
> **创建**：2026-07-15 09:05
> **关联**：INC-2026-07-15-001 / L-33 / L-13

---

## 反例（INC-2026-07-15-001 现场）

**Nick 22 个 OpenClaw cron 投递全部 fail-closed**，delivery 配置：

```json
{
  "delivery": {
    "mode": "announce",
    "channel": "last"
  }
}
```

**失败原因**（cron 状态全 error）：

```
lastRunStatus: error
lastDelivered: false
lastDeliveryStatus: not-delivered
lastDeliveryError: "Delivering to Feishu requires target <chatId|user:openId|chat:chatId>"
```

**根因**：
- `mode: announce` —— 试图把任务输出回传 main session
- `channel: last` —— 通过"最后一个 active session"路由
- Nick main session（LEADER）平时 idle，没有 active route
- OpenClaw 平台 fail-closed：不投递且状态记 error

**业务影响**：
- 8:30 morning·daily（命令跑通 + daily 骨架写好）→ 文博**没收到**
- 8:35 tech·briefing（命令 exit 2 找不到脚本）→ 文博**没收到**（双层故障）
- 9:00 wiki.daily·expander / daily·report·c3（命令跑通）→ 文博**没收到**
- 21:00 daily·note·scan（命令 exit 2）→ 笔记未入库
- 23:00 / 0:30 bestpractice.* → 全部没收到

**consecutiveErrors 计数**（morning·daily）：
```
consecutiveErrors: 15
```
说明从 OpenClaw cron 启用以来，**15 次连续投递失败**没人发现。

---

## 正例（派蒙成熟模式 · 9:05 verify）

**派蒙 cron 投递配置**（`派蒙-T3prime-自查-DAY` 实证）：

```json
{
  "delivery": {
    "mode": "none",
    "channel": "feishu",
    "to": "user:ou_415aaf2674f34d5034a3e71882b89d94"
  }
}
```

**为什么 OK**：
- `mode: "none"` —— **不通过 main session announce**，直接推送
- `channel: "feishu"` —— **显式飞书渠道**（不依赖 main session route）
- `to: "user:ou_xxx"` —— **显式目标用户**（user: 前缀 + 飞书 open_id）

**优点**：
- 不依赖 main session active 状态
- 不依赖 platform session 路由
- 显式推送 → 即使 LEADER 不在也成功投递
- 即使 platform fail-closed 也不会 fail（status 仍 ok）

**对照表**：

| 维度 | 派蒙（✅ ok）| Nick（❌ error）|
|:---|:---|:---|
| mode | `none` | `announce` |
| channel | `feishu` | `last` |
| to | `user:ou_415aaf...` | （空）|
| 依赖 | 无（直接推）| main session route |
| status | ok | error（22 个）|
| lastDelivered | true | false |
| consecutiveErrors | 0 | 15 |

---

## 治本 SOP（Nick cron 注册/更新 必检）

### ✅ 必填字段

```bash
openclaw cron edit <id> \
  --channel feishu \
  --to "user:ou_ca04de68a40f571f59bcf2e71241415a"
```

| 字段 | 值 | 说明 |
|:---|:---|:---|
| **mode** | `none` | 不通过 main session announce（默认行为） |
| **channel** | `feishu` | 显式飞书渠道 |
| **to** | `user:ou_xxx` | user: 前缀 + 飞书 open_id（**不是手机号**） |
| **agent** | `nick_fury` | 必须填，不能是 `-` |

### ❌ 不要用

| 模式 | 后果 |
|:---|:---|
| `mode: announce, channel: last` | 依赖 main session → fail-closed（22 个 cron 全挂现场） |
| `--no-deliver` | 完全不投递，文博看不到 |
| agent `-` | cron run 不绑定 Nick agent（看 22 个 cron 多数 agent 是 `-`） |

### 注：`openclaw cron edit --to` description

`--to` description 写的是 "E.164, Telegram chatId, or Discord channel/user"，**没明说支持飞书**。但派蒙 9:05 实证用 `user:ou_415aaf2674f34d5034a3e71882b89d94` 成功（status ok, lastDelivered 正常），所以**实际支持**。如果格式有变，可以试 `chat:ou_xxx` 或纯 `ou_xxx` 备选。

---

## 验证步骤（注册/更新后 24h 内必跑）

```bash
# 1. 看 status 是否 ok
openclaw cron get <id> | grep lastRunStatus
# 期望: "lastRunStatus": "ok"

# 2. 看 lastDelivered
openclaw cron get <id> | grep lastDelivered
# 期望: "lastDelivered": true

# 3. 看 consecutiveErrors
openclaw cron get <id> | grep consecutiveErrors
# 期望: "consecutiveErrors": 0

# 4. 看 delivery 配置
openclaw cron get <id> | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('delivery'))"
# 期望: {'mode': 'none', 'channel': 'feishu', 'to': 'user:ou_xxx'}
```

---

## 批量修复（22 个 cron）

```bash
# 1. 列出所有 Nick cron ID
NICK_CRON_IDS=$(openclaw cron list | grep -E "tech·briefing|morning·daily|rss\.daily|rss\.collect|etf\.hegang|daily·report|daily·note|bestpractice|github\.track|kb\.track|rss\.organize|wiki\.ingest|wiki\.review|wiki\.weekly|wiki\.daily|morning·rss|wiki·auto|wiki·health|投资纪律" | awk '{print $1}')

# 2. 批量改 delivery
for id in $NICK_CRON_IDS; do
  openclaw cron edit $id \
    --channel feishu \
    --to "user:ou_ca04de68a40f571f59bcf2e71241415a" \
    --agent nick_fury 2>&1 | head -3
  echo "--- $id done ---"
done
```

**注意**：
- 22 个 cron 工作量，可并行（`&` + `wait`）
- 改完后 24h 内 verify consecutiveErrors=0
- 部分 cron 需要先 disable 或修 command（L-34 治本）

---

## 关联教训

- **L-13** (OpenClaw 原生优先) — 治本前提
- **L-22** (lark-cli v1.0.63 隐性依赖 OPENCLAW_HOME) — 平台依赖
- **L-33** (cron Delivery 显式 feishu · 初版) — 升级为 L-35
- **L-35** (cron 投递对齐派蒙 mode=none 模式) — **本条**
- **L-29** (自检必须区分"输出成功"和"输入真实") — cron 投递同理（status ok ≠ lastDelivered true）

---

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每日 21:00** | c3_daily_check.py 检查 OpenClaw cron consecutiveErrors | c3 cron |
| **每周一 09:00** | grep `mode: announce, channel: last` 看是否还有未迁移 | 手动 |
| **新加 cron 后** | 24h 内 verify status=ok + lastDelivered=true | 手动 |
| **scripts 改造后** | 同步 update cron argv（L-34 治本） | 手动 |

---

*Lesson 完稿: 2026-07-15 09:05 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-001 ✅ 应急已闭环 / 治本待 9:10 执行*