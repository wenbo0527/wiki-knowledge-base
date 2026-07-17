# L-49.6: cron cleanup 决策树（部分清模式 · L-49 升级版）

> **创建时间**：2026-07-17 14:32 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-17-006（用户决策 C · 批量删除 9 个死脚本 cron）
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-17-cron-cleanup-decision-tree-l49-6.md`

---

## 🎯 核心教训

**cron cleanup 决策树**（4 类 + 4 动作）：

| 类型 | 风险 | 推荐动作 | 候选 #C 二段实证 |
|:---|:---|:---|:---|
| **enabled + argv 死脚本** | 🔴 高（下次跑会爆）| 必修 argv 或 disable | wiki.monthly·refresher (14:18 disable) |
| **disabled + argv 死脚本** | 🟡 中（误启用会爆）| **必删**（C 模式）| 9 个已删 ✅ |
| **enabled + delivery 错配** | 🔴 高（推送失败）| 必修 delivery | 钟离 2 个 + nick_fury 测试 1 个 |
| **disabled + delivery 错配** | 🟢 低（disabled 不跑）| **保留**（C 模式）| 14 个保留不动 |

**L-49 原版 + L-49.5 升级 + L-49.6 决策树**——三层递进：

| 层 | 教训 | 触发 INC |
|:---:|:---|:---|
| L-49 | cron edit 必看 argv 完整 JSON | INC-002 (etf.hegang hardcoded) |
| L-49.5 | argv 必查脚本路径存在性 | INC-005 (38 个新问题) |
| **L-49.6** | **cleanup 决策树（4 类 + 4 动作）** | **INC-006 (C 模式实证)** |

---

## 📚 INC-006 揭穿真根因（实例）

### 用户决策 C 完整链路

```
14:18 文博拍 C（部分清）
14:30 sqlite 备份（91MB）
14:30:35 第 1 次 rm 失败（shell 变量解析 bug · 9 个都被当成一个 ID）
14:31:00 while 循环修正 · 9 个全部 rm 成功
14:31:27 sunday_cron_health_check 复跑 · 问题数 38→17（减 21 个）
```

### shell 变量解析 bug 实证

```bash
# ❌ 错误写法（第一次）
CRON_IDS="id1 id2 id3"
for ID in $CRON_IDS; do
  openclaw cron rm "$ID"  # shell 把整个 $CRON_IDS 当一个 string
done
# 报错: invalid cron.remove params: id not found

# ✅ 正确写法（第二次）
sqlite3 -json ... | python3 -c "
import json, sys, subprocess
rows = json.loads(sys.stdin.read())
for r in rows:
    cid = r['job_id']
    result = subprocess.run(['openclaw', 'cron', 'rm', cid], ...)
    ...
"
```

### 删前必备份实证（§5 安全边界）

```bash
cp ~/.openclaw/state/openclaw.sqlite \
   ~/.openclaw/state/openclaw.sqlite.bak-2026-07-17-pre-delete-dead-scripts-1784269807
# 备份 91MB · 万一 rm 误删可恢复
```

---

## 🔧 cron cleanup 决策树（4 类 + 4 动作 · 实战脚本）

```bash
#!/bin/bash
# L-49.6 cron cleanup 决策树（4 类 + 4 动作）

echo "=== L-49.6 cron cleanup 决策树 ==="

# 第 1 类: enabled + argv 死脚本 → 必修或 disable
echo "[1] enabled + argv 死脚本（必 disable）:"
sqlite3 -json ~/.openclaw/state/openclaw.sqlite "SELECT job_id, name FROM cron_jobs WHERE enabled=1 AND job_json LIKE '%.py%';" 2>&1 | python3 -c "
import json, sys
from pathlib import Path
rows = json.loads(sys.stdin.read())
for r in rows:
    import re
    m = re.search(r'([^\s]+\.py)', r['name'])  # 简化：实际要 parse job_json
    # ... argv path check
"

# 第 2 类: disabled + argv 死脚本 → 必删
echo "[2] disabled + argv 死脚本（必删 · C 模式）:"
# 用 sunday_cron_health_check.py 自动揭穿 → 批量 rm

# 第 3 类: enabled + delivery 错配 → 必修
echo "[3] enabled + delivery 错配（必修）:"
# 用 sunday_cron_health_check.py 自动揭穿 → cron edit delivery

# 第 4 类: disabled + delivery 错配 → 保留
echo "[4] disabled + delivery 错配（保留）:"
# 不动
```

---

## 📜 L-49.6 教训族清单

| 编号 | 教训 |
|:---|:---|
| **L-49.6.1** | cron cleanup 决策树 4 类 + 4 动作：enabled 死脚本必修/disabled 死脚本必删/enabled delivery 必修/disabled delivery 保留 |
| **L-49.6.2** | 任何 cron 删除前必备份 sqlite（§5 安全边界 · L-49.6 强化）|
| **L-49.6.3** | shell 变量解析陷阱：`VAR="a b c"` for ID in $VAR 当一个 string 用 → 必用 while 循环 / Python |
| **L-49.6.4** | 7-19 周日 cron 自动复查 L-49.5 揭穿的死脚本 → L-49.6 自动清理流程（待集成）|

---

## 🎯 防退化机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次 cron 删除** | L-49.6.2 sqlite 备份 + L-49.6.3 while 循环 | 标准操作 |
| **每日 22:00** | sunday_cron_health_check.py 自动 L-49.5 检测 | 已部署 |
| **每周日 22:00** | 周报含 L-49.6 决策树执行结果 | 手动 |
| **每次新 INC** | 必查 `find review-logs -name "*cleanup*"` | L-31 |

---

## 关联

- **INC-2026-07-17-002**（etf.hegang argv 硬编码）—— L-49 原版
- **INC-2026-07-17-005**（L-49.5 揭穿 38 个问题）—— L-49.5 升级版
- **INC-2026-07-17-006**（用户决策 C · 批量删除 9 个）—— L-49.6 决策树实证
- **L-49**（cron edit 必看 argv 完整 JSON）—— 基础
- **L-49.5**（argv 必查脚本路径存在性）—— 升级
- **L-49.6**（新增 · cleanup 决策树 · 部分清模式）
- **scripts/sunday_cron_health_check.py**（L-49.5 自动揭穿 → L-49.6 自动清理待集成）