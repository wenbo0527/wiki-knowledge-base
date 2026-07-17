# L-49.5: cron edit 必查脚本路径存在性（L-49 升级版）

> **创建时间**：2026-07-17 14:22 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-17-005（L-49.5 升级揭穿 9 个死脚本）
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-17-cron-edit-must-check-script-path-l49-5.md`

---

## 🎯 核心教训

**cron argv 必含 4 项**（L-49 升级版）：
1. ✅ **路径存在性**（升级项 · L-49.5）—— `Path(token).exists()` 验证
2. ✅ 路径正确性（脚本存在 + 可执行）
3. ✅ 参数语义合理（无 hardcoded 时间戳/ID/用户）
4. ✅ 无副作用参数（不会产生空目录/硬编码日期/污染全局）

**L-49 原版教训**（INC-002 揭穿）：只看 argv 内 hardcoded 日期/用户，**没看脚本路径是否存在**——L-49.1 升级后揭穿 9 个死脚本。

---

## 📚 INC-005 揭穿真根因（实例）

### 揭穿链路（wiki.monthly·refresher 修复链）

| 时间 | 动作 | 发现 |
|:---|:---|:---|
| 14:18 | 用户授权"请修复" | |
| 14:18 | cron edit `wiki.monthly·refresher` delivery 对齐 L-35 | channel=feishu, to=user:ou_xxx ✅ |
| 14:18 | 手动跑 `monthly_refresher.py run` 验证 | ❌ `No such file or directory` |
| 14:19 | grep 全集（按 L-49 4 路全集）| 揭穿 4 个 wiki.* disabled cron argv 死脚本 |
| 14:20 | L-49.5 升级：加 Path.exists() 检查 | 揭穿 9 个总死脚本 |
| 14:21 | sunday_cron_health_check.py 升级版跑通 | 38 个新问题（9 死脚本 + 27 disabled delivery + 2 钟离）|

### 9 个死脚本清单

| cron | enabled | 死脚本路径 | 来源推测 |
|:--|:--:|:--|:--|
| `bestpractice.daily.append` | ❌ | `skills/best-practice-daily/daily_append.py` | 7-1 改造合并 |
| `morning·rss·etf·push` | ❌ | `scripts/morning_rss_etf_push.py` | 7-15 合并到 daily_tech_report.py |
| `rss.organize` | ❌ | `skills/rss-intelligence/scripts/organizer.py` | 7-1 改造改名 |
| `wiki.daily·expander` | ❌ | `skills/rss-intelligence/scripts/daily_expander.py` | 同上 |
| `wiki.ingest` | ❌ | `skills/rss-intelligence/scripts/wiki_ingestor.py` | 同上 |
| `wiki.monthly·refresher` | ❌ | `skills/rss-intelligence/scripts/monthly_refresher.py` | 同上 |
| `wiki.weekly·synthesizer` | ❌ | `skills/rss-intelligence/scripts/weekly_synthesizer.py` | 同上 |
| `投资纪律-每日汇总` | ❌ | `scripts/daily_investment_summary.py` | 7-1 改造合并到 evening_tracker.py |
| `投资纪律-周报` | ❌ | `scripts/daily_investment_summary.py` | 同上 |

**根因**：7-1 scripts 改造合并 39→20 + 7-14 launchd→OpenClaw cron 迁移 + 7-15 INC-001 修复期间，**所有"删除脚本"动作没同步 disable 对应 cron argv**——L-34 不彻底。

---

## 🔧 L-49.5 argv 完整检查清单（cron 修必跑）

```bash
#!/bin/bash
# L-49.5 标准化 cron edit argv 检查脚本（含 4 项）

CRON_ID="$1"

echo "=== L-49.5 argv 完整检查（4 项） ==="

# 1. 看 argv 完整 JSON
echo "[1] argv 完整 JSON:"
openclaw cron get "$CRON_ID" | python3 -c "
import json, sys, re
from pathlib import Path
data = json.load(sys.stdin)
argv = data['payload']['argv']
print('  argv:', argv)

# [1] 路径存在性（L-49.5 新增）
for i, arg in enumerate(argv):
    for token in str(arg).split():
        if token.endswith(('.py', '.sh')) and not token.startswith('-'):
            exists = Path(token).exists()
            status = '✅' if exists else '🔴 不存在'
            print(f'  [1] 路径检查: {token} → {status}')
            break

# [2] 参数 hardcoded 日期/用户/ID
for arg in argv:
    s = str(arg)
    for m in re.finditer(r'\b20\d{2}-\d{2}-\d{2}\b', s):
        print(f'  [2] hardcoded 日期: {m.group(0)} 🔴')
    for m in re.finditer(r'\bou_[a-f0-9]{16,}\b', s):
        print(f'  [2] hardcoded user: {m.group(0)} 🔴')

# [3] delivery 字段
d = data.get('delivery', {})
print(f'  [3] delivery: mode={d.get(\"mode\")}, channel={d.get(\"channel\")}, to={d.get(\"to\", \"\")[:30]}')
if d.get('mode') == 'announce':
    if d.get('channel') != 'feishu':
        print(f'  [3] 🔴 channel={d.get(\"channel\")} 不对齐派蒙')
    if not (d.get('to') or '').startswith('user:'):
        print(f'  [3] 🔴 to 不以 user: 开头')
"
```

---

## 📜 L-49.5 教训族清单

| 编号 | 教训 |
|:---|:---|
| **L-49.5.1** | cron argv 必含 4 项（原 3 项 + **脚本路径存在性**）|
| **L-49.5.2** | 任何 cron 涉及日期/ID/用户参数必 grep `hardcoded\|fixed\|static`（防退化）|
| **L-49.5.3** | 写新 cron 必先 `python3 -c "from pathlib import Path; print(Path('<path>').exists())"` 验证 |
| **L-49.5.4** | scripts 改造必查 OpenClaw cron argv 全集（含 disabled · L-34 不彻底治本）|

---

## 🎯 防退化机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次 cron edit** | L-49.5 4 项检查（路径 + hardcoded + delivery）| `scripts/cron_argv_check.sh`（待写）|
| **每日 22:00** | sunday_cron_health_check.py 自动跑 L-49.5 | 已升级 |
| **每周日 22:00** | MEMORY 压缩时 grep "dead script" | 手动 |
| **每次新 INC** | 必查 `find review-logs -name "*dead*script*"` | L-31 |

---

## 关联

- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— L-35 原版
- **INC-2026-07-17-002**（etf.hegang argv 硬编码）—— L-49 原版
- **INC-2026-07-17-005**（L-49.5 升级揭穿 9 死脚本）—— 揭穿案例
- **L-34**（scripts 改造必 grep cron argv）—— 原版（不彻底）
- **L-49**（cron edit 必看 argv 完整 JSON）—— 升级版基础
- **L-49.5**（新增 · argv 必查脚本路径存在性）
- **scripts/sunday_cron_health_check.py**（升级版 · 集成 4 项 check）