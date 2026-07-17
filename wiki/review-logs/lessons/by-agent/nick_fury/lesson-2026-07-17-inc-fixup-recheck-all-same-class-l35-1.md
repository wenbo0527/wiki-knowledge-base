# L-35.1: INC 治本后必复查同类全集（修一类 ≠ 修一类再 grep 一次）

> **创建时间**：2026-07-17 08:55 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-17-003（getnote delivery channel=last fail-closed）
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-17-inc-fixup-recheck-all-same-class-l35-1.md`

---

## 🎯 核心教训

**任何 INC 治本后 24h 内必 grep 同类全集**——"修一个 ≠ 修一类，修一类 ≠ 修一类再 grep 一次"（L-16 升级）。

L-16 原版是"修 launchd plist 必 grep 全集 plist"——L-35.1 升级为"任何 INC 治本后必 grep 同类全集"。

**getnote·wiki·sync delivery channel=last fail-closed**就是 INC-2026-07-15-001 治本后没复查同类 delivery 配置的漏网之鱼——已经 fail-closed 24h+，文博每天 6:00 收不到 getnote 同步完成通知。

---

## 📚 INC-003 揭穿真根因（实例）

### 7-15 INC-001 治本不彻底

| 7-15 INC-001 修复范围 | 实际漏修 |
|:---|:---|
| ✅ 5 个 cron argv 失效修复 | ❌ getnote·wiki·sync argv 没失效，没在 5 个里 |
| ✅ L-35 "cron 投递必对齐派蒙" 写入 | ❌ 复查机制缺 —— 没"7-15 后所有 cron delivery 复查"动作 |
| ✅ 17 个 cron delivery 改 feishu | ❌ getnote 没改（不知道它的 delivery 是 channel=last） |

### "假阳性"状态命中（L-29 升级）

```json
{
  "lastRunStatus": "ok",              ← 表面：脚本跑通
  "lastDelivered": false,              ← 实质：推送失败
  "lastDeliveryStatus": "not-delivered"
}
```

**L-29 升级**：status=ok ≠ 推送成功，必须 `lastDelivered=true` 才算真成功。

### getnote·wiki·sync 推送失败链路

1. 6:00 cron 触发
2. `getnote_to_wiki.sh` 跑通（exit 0）✅
3. cron 试图推送 delivery `channel=last`
4. **last 是"上一次推送的 channel" 特殊标识**
5. **没有上一次推送**（cron isolated session 不是用户会话）
6. → "no route, will fail-closed" → 推送跳过
7. → 文博收不到 getnote 同步完成通知

---

## 🔧 cron delivery 复查清单（INC 治本后必跑）

```bash
#!/bin/bash
# L-35.1 标准化 cron delivery 复查脚本

echo "=== L-35.1 cron delivery 复查（必 3 字段） ==="

# 列出所有 cron + delivery 状态
openclaw cron list 2>&1 | tail -n +2 | while IFS='|' read -r line; do
  ID=$(echo "$line" | awk '{print $1}')
  NAME=$(echo "$line" | awk '{print $2}')
  DELIVERY=$(echo "$line" | awk '{print $NF}')

  # 必查 3 字段
  if echo "$DELIVERY" | grep -q "last\|fail-closed\|no route"; then
    echo "🔴 $NAME ($ID): $DELIVERY"
  fi
done

# 复查每个 cron delivery 必含 channel=feishu + to=user:ou_xxx
openclaw cron list 2>&1 | tail -n +2 | awk '{print $1}' | while read -r ID; do
  DELIVERY=$(openclaw cron get "$ID" 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    d = data.get('delivery', {})
    mode = d.get('mode', '')
    channel = d.get('channel', '')
    to = d.get('to', '')
    if mode == 'announce' and channel != 'feishu':
        print(f'⚠️  mode=announce 但 channel={channel}')
    elif mode == 'announce' and not to.startswith('user:'):
        print(f'⚠️  mode=announce 但 to={to}')
except: pass
")
  if [ -n "$DELIVERY" ]; then
    echo "  [$ID] $DELIVERY"
  fi
done
```

---

## 📜 L-35.1 教训族清单

| 编号 | 教训 |
|:---|:---|
| **L-35.1.1** | 任何 INC 治本后 24h 内必 grep 同类全集（"修一个 ≠ 修一类，修一类 ≠ 修一类再 grep 一次" = L-16 升级）|
| **L-35.1.2** | cron delivery 复查必 3 字段：`mode=none` + `channel=feishu` + `to=user:ou_xxx`（缺一即 fail-closed）|
| **L-35.1.3** | "假阳性"检测：`lastRunStatus=ok + lastDelivered=false` = 推送失败（不是 ok）—— L-29 升级 |
| **L-35.1.4** | 7-19 周日 cron 新增 "OpenClaw cron delivery 复查" 检查项（每周日扫一遍所有 cron delivery）|

---

## 🎯 防退化机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次 INC 治本** | L-35.1.1 同类复查 | `scripts/inc_fixup_recheck.sh`（待写）|
| **每周日 22:00** | cron delivery 全集复查 | `scripts/cron_delivery_weekly_check.sh`（待写）|
| **每日 21:00** | C-3 cron 检测 "lastDelivered=false" | `scripts/c3_daily_check.py` 升级 |
| **每次新 INC** | 必查 `find review-logs -name "*delivery*"` | L-31 |

---

## 关联

- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— L-35 原版
- **INC-2026-07-17-003**（getnote delivery channel=last）—— 揭穿案例
- **L-16**（修一类必 grep 全集）—— 原版（launchd 范围）
- **L-29**（报告必区分"输出成功"和"输入真实"）—— 直接相关
- **L-35**（cron 投递必对齐派蒙）—— 原版
- **L-35.1**（新增 · INC 治本后同类复查 + "假阳性"检测）
- **cron d795c8d4**（已 edit delivery 对齐派蒙模式，明早 7-18 06:00 验证 status=ok + 真推送文博飞书）