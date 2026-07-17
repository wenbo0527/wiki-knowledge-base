# L-49: cron edit 必看 argv 完整 JSON（防 hardcoded 参数）

> **创建时间**：2026-07-17 08:55 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-17-002（etf.hegang cron argv 硬编码 --date 2026-06-26）
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-17-cron-edit-must-read-argv-complete-l49.md`

---

## 🎯 核心教训

**任何 cron 修改前必先 `openclaw cron get <id>` 看 argv 完整 JSON**——不看完整 JSON 就 edit 等于盲改。

argv 必含 3 项：
1. ✅ **路径正确性**（脚本存在 + 可执行）
2. ✅ **参数语义合理**（参数值不是 hardcoded 时间戳/ID/用户）
3. ✅ **无副作用参数**（不会产生空目录/硬编码日期/污染全局）

---

## 📚 INC-002 揭穿真根因（实例）

### argv 实证（cron 4367285d）

```json
{
  "id": "4367285d-e352-448a-893f-721f7625e009",
  "name": "etf.hegang.report",
  "argv": [
    "sh",
    "-lc",
    "/usr/bin/python3 .../etf_hegang_report.py --date 2026-06-26 --output .../data/etf_hegang_report.md"
  ]
}
```

**问题**：
- `--date 2026-06-26` 是 **hardcoded 日期**（6-26 当天手动测试后没改回）
- 每天 8:35 cron 跑都生成 6-26 的报告（覆盖当天）
- 文博每天早上收到的 ETF 报告都是 6-26 内容 —— **23 天报告内容与日期不符**

### 7-15 INC-001 L-34 漏修链路

| L-34 原版 | L-49 升级版 |
|:---|:---|
| scripts 改造必 grep cron argv | cron edit 必 grep argv 完整 JSON |
| 只看 argv 是否失效 | 必看 argv 内每个参数是否合理 |
| 缺 hardcoded 检测 | 必 grep `hardcoded\|fixed\|static` |
| 不查副作用 | 必查 `--date`/`--user`/`--id` 等具体参数 |

---

## 🔧 argv 完整检查清单（cron 修必跑）

```bash
#!/bin/bash
# L-49 标准化 cron edit argv 检查脚本

CRON_ID="$1"

echo "=== L-49 argv 完整检查 ==="

# 1. 看 argv 完整 JSON
echo "[1] argv 完整 JSON:"
openclaw cron get "$CRON_ID" | python3 -c "
import json, sys
data = json.load(sys.stdin)
argv = data['payload']['argv']
print('  argv:', argv)
# 2. 检测 hardcoded 日期
for arg in argv:
    if '--date' in arg or '--time' in arg:
        import re
        m = re.search(r'(\d{4}-\d{2}-\d{2})', arg)
        if m:
            print(f'  ⚠️  hardcoded 日期: {m.group(1)}')
# 3. 检测 hardcoded 用户/ID
for arg in argv:
    if '--user' in arg or '--id' in arg:
        import re
        m = re.search(r'(?:ou_[a-f0-9]+|user-\d+)', arg)
        if m:
            print(f'  ⚠️  hardcoded user/ID: {m.group(0)}')
# 4. 检测路径
for i, arg in enumerate(argv):
    if arg.startswith('/') and not arg.startswith('/usr') and not arg.startswith('/bin'):
        import os
        if not os.path.exists(arg.split()[0]):
            print(f'  ❌ 路径不存在: {arg.split()[0]}')
"
```

---

## 📜 L-49 教训族清单

| 编号 | 教训 |
|:---|:---|
| **L-49.1** | cron 修必先 `openclaw cron get <id>` 看 argv 完整 JSON（不是只看 schedule name） |
| **L-49.2** | argv 必含 3 项：路径正确性 + 参数语义合理 + 无 hardcoded 时间戳/ID/用户 |
| **L-49.3** | 任何 cron 涉及日期/ID/用户参数必 grep `hardcoded\|fixed\|static`（防退化）|
| **L-49.4** | INC-2026-07-15-001 升级版：原 L-34 "scripts 改造必 grep cron argv" → 升级为 L-49 "cron 修必 4 路全集 + argv 完整" |

---

## 🎯 防退化机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次 cron edit** | L-49.1-3 三项检查 | `scripts/cron_argv_check.sh`（待写）|
| **每日 9:00** | cron_argv_check.sh 检测所有 cron argv | 已扩展 |
| **每周日 22:00** | MEMORY 压缩时 grep "argv hardcoded" | 手动 |
| **每次新 INC** | 必查 `find review-logs -name "*argv*"` | L-31 |

---

## 关联

- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— L-34 原版
- **INC-2026-07-17-002**（etf.hegang argv 硬编码）—— 揭穿案例
- **L-34**（scripts 改造必 grep cron argv）—— 原版
- **L-49**（新增 · cron edit 完整 JSON + hardcoded 检测）
- **cron 4367285d**（已 edit 去 --date，明早 7-18 08:35 验证 status=ok + 报告日期动态）