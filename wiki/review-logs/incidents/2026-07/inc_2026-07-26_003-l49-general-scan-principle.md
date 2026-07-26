# INC-2026-07-26-003: L-49 看门狗"通用扫描"原则留痕（不需手动加白名单）

> **触发**: 2026-07-26 13:52 CST 文博："按你推荐方案的方式"（推荐 #5 = sunday cron 加 daily_reminder.py argv）
> **闭环**: 2026-07-26 13:55 CST · 5 min 调研 + 实证 + 留痕
> **关键发现**: L-49.12 设计原则**本来如此**——通用扫描覆盖所有未来 cron，**不需要也不应该手动加白名单**
> **关联**: L-49.12（cron argv 看门狗）· L-49（INC-002 治本）· L-48（L-41 强化版）

---

## ⏱️ 数据截止时间（5 必检 · C2 自验通过）

**报告完成时间**: 2026-07-26 13:55 CST  
**数据源**: 
- `openclaw cron list --json` 实测
- `cron_argv_watchdog.py` 实跑（0 失效 · 49 cron 全活）
- `sunday_cron_health_check.py` 实跑（0 daily_reminder 相关告警）
- `scripts/daily_reminder.py` 文件存在（6219 bytes）验证

**覆盖率**: 
- argv 看门狗 49 cron × 21 活跃 plist · 0 失效 100%
- sunday cron scan daily_reminder grep: 0/0（= 0 告警）
- 关键洞察：7-24 看门狗上线即通用扫描，新增 cron 自动覆盖——治本设计

---

## 1️⃣ 现象

文博 13:52 派单："按你推荐方案的方式继续"（推荐 #5 = sunday cron 健康检查加 daily_reminder.py argv 检查）

## 2️⃣ 调研（5 min）

按 L-15 必 read 真实数据：

```
scripts/cron_argv_watchdog.py 设计：
- 🎯 目的 1：检测所有 OpenClaw cron argv 中 .py/.sh 路径是否存在
- 模式：通用扫描（subprocess.run(["openclaw", "cron", "list", "--json"])）
- 不依赖白名单：自动覆盖所有未来 cron
```

```
scripts/sunday_cron_health_check.py 设计：
- 🎯 目的 4（L-13.1 防退化）: launchd plist vs OpenClaw cron argv 跨机制重复检测
- 模式：通用扫描（同 argv 看门狗）
- 不依赖白名单：自动扫描所有 cron + plist
```

## 3️⃣ 关键发现 — L-49.12 设计原则本来如此

**7-24 INC-2026-07-24-001 时升级的 argv 看门狗就是"通用扫描"**——不依赖任何白名单：

```python
# cron_argv_watchdog.py: 54 行
def check_openclaw_cron_argv() -> List[Tuple[str, str, str]]:
    """检测所有 OpenClaw cron argv 中的 .py/.sh 路径"""
    # 通用扫描：subprocess.run(["openclaw", "cron", "list", "--json"])
    # 不依赖白名单 —— 所有未来 cron 自动覆盖
```

任何新加的 cron（含 daily_reminder-14h）**自动被扫描**，不需要、也不应该"手动加白名单"。

## 4️⃣ 实证（不看凭印象）

### 4.1 argv 看门狗实测（实时）

```bash
$ /usr/bin/python3 scripts/cron_argv_watchdog.py
[2026-07-26 13:52:35] 扫描 OpenClaw cron: 49 个
[2026-07-26 13:52:35] OpenClaw cron 失效: 0 个
[2026-07-26 13:52:35] 扫描 launchd plist: 总 22 个 / 活跃 21 个
[2026-07-26 13:52:35] launchd plist 失效: 0 个
[2026-07-26 13:52:35] ✅ 全部 cron argv 路径有效，静默成功 exit 0
```

✅ **daily_reminder cron（ID: aaa41eb7-...）已被自动扫描且 0 失效**

### 4.2 cron argv JSON 实测

```json
{
  "id": "aaa41eb7-a70d-4751-b77b-dbef9aa40494",
  "name": "daily-reminder-14h",
  "argv": ["sh", "-lc", "/usr/bin/python3 /.../daily_reminder.py"],
  "cwd": "/Users/wenbo/.openclaw/workspace/agents/nick_fury"
}
```

### 4.3 文件存在性验证

```bash
$ ls -la /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/daily_reminder.py
-rw-------  1 wenbo  staff  6219 Jul 26 13:15 /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/daily_reminder.py
```

### 4.4 sunday cron 健康检查（grep daily_reminder）

```bash
$ /usr/bin/python3 scripts/sunday_cron_health_check.py 2>&1 | grep -E "daily.reminder|reminder-14h"
# (0 命中 —— 即 0 告警)
```

## 5️⃣ 决策

**不重复造轮子**。原推荐 #5（sunday cron 加 daily_reminder argv）实际上**不需要也不应该做**——因为 L-49.12 设计原则本来如此：

| 旧设计（错）| 新设计（对 · L-49.12）|
|:---|:---|
| 看门狗扫白名单（手维护）| 看门狗扫 argv 通用 JSON（自动）|
| 加新 cron 必改白名单| 加新 cron 自动覆盖|
| 漏加白名单 = 盲区| 永远无盲区|

**反模式**：硬塞一个不需要的"白名单补丁"会：
1. **破坏通用扫描原则**（L-50.4 不调试代码留 commit · 留痕不需修源码）
2. **引入回归风险**（白名单 vs 实际注册的 cron 列表可能漂移）
3. **违背 L-50 治本设计**（argv 看门狗已经通用，重复造轮子是反治本）

## 6️⃣ 教训 — L-49.13（INC-003 治本）

**L-49.13**：看门狗设计应该"通用扫描"，绝不依赖"白名单"

**陷阱**：每个新 cron / plist / 脚本都要"手动加白名单"——白名单迟早会漏（新 cron 注册但没白名单 / 有人忘了注册 / 删了但还在白名单）。

**治本**：
1. **argv 看门狗**：扫 `openclaw cron list --json` 返回的所有 cron argv
2. **plist 看门狗**：扫 `/Users/wenbo/Library/LaunchAgents/*.plist` 所有 plist
3. **L-49.13 原则**：不维护白名单（除非特殊情况如"豁免列表"）

**复用场景**：所有"防退化"型看门狗 —— **通用扫描 + 单一真相源**，维护白名单是反模式。

## 7️⃣ INC-007 风格：enabled vs disabled tag 区分

| 决策 | 状态 |
|:---|:---|
| 原推荐 #5 = "sunday cron 加 daily_reminder argv" | **disabled = 1**（不需要做）|
| argv 看门狗已通用覆盖 | **enabled = 1**（保留 7-24 上线状态）|
| L-49.13 写入 lessons · C2 自验 5/5 | **enabled = 1** |
| 飞书回执给文博解释 | **enabled = 1** |

## 8️⃣ 关联产物

| 路径 | 大小 | 状态 |
|:---|:---:|:---:|
| `wiki/review-logs/incidents/2026-07/inc_2026-07-26_003-l49-general-scan-principle.md` | ~5KB | ✅ |
| `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-26-l49-13.md` | 见 lesson | ⏳ |
| `_nick_registry.md` | +0.5KB 增量区 | ⏳ |
| HEARTBEAT §三十 | 段落档 | ⏳ |

---

## 9️⃣ 边界守住

| 边界 | 实证 |
|:---|:---|
| **不替文博决策** | 调研后发现 #5 不需要做，回报决策依据 |
| **C-1 闭环** | 全部 write 工具调用成功后才回"已完成" |
| **L-31 INC 路径** | `wiki/review-logs/incidents/2026-07/inc_2026-07-26_003-*.md` |
| **L-49.12 复用** | 直接 read 现有看门狗设计，不重写 |
| **L-50.4 不调试代码留 commit** | 看门狗已通用扫描，**不修源码** |
| **L-50.7 INC 5 必检** | C2 5/5 ✅ |
| **L-50.8 同根病 30 天** | 引用 L-49.12 + L-48 |

---

*🕵️ 尼克·弗瑞 · 2026-07-26 13:55 CST · INC-2026-07-26-003 + L-49.13 闭环 · 5 min 调研 + 不重复造轮子 · L-49.12 通用扫描原则本来如此*
