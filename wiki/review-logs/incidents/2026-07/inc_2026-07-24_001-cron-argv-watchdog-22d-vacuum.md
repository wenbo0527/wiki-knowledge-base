# INC-2026-07-24-001: Cron argv 失效 + 推送脚本退出码误判 4 层 silent failure（22 天 RSS 真空 + 3 cron error + 1 plist 失效）

> **数据截止**: 2026-07-24 09:35 CST
> **作者**: 尼克·弗瑞 🕵️
> **治本时长**: 30 min（08:41 接单 → 09:30 闭环）
> **决策路径**: 文博 C 选项治本（A 盘点 + B 修 + C 看门狗）
> **关联 lessons**: L-49.12 / L-36 强化

---

## 1️⃣ 现象（4 层 silent failure）

文博 7-24 08:41 报"大量信息抓取失败" → 实测发现 4 个 silent failure：

| # | 现象层 | cron 状态 | 实际行为 | 静默天数 |
|:---:|:---|:---:|:---|:---:|
| 1 | `data/topic_collection/collection_*.json` 7-01 断档 | cron ok | `daily_topic_collector.sh` 7-2 失败一次后再没被调起 | **22d** |
| 2 | `daily·report·c3` (929a8003) cron error | exit 1 | 脚本跑通 + 飞书推成功 + KB 告警（exit 1 误判）| 1d |
| 3 | `nick_cron_health_weekly` (ab65ed59) cron error | exit 1 | 脚本跑通 + 飞书推成功（有告警 exit 1 误判）| 5d |
| 4 | `com.nickfury.wiki.monthly-refresher` plist argv 失效 | launchd 加载 | 指向已删 `monthly_refresher.py` 静默退出 | 22d+ |

**daily 完稿率 / 推送影响**：🟢 **用户面无感**（rss.collect 走 daily_pipeline.py + tech.briefing 5 篇基线）—— 这反而是更糟的 silent failure。

**致命漏检**：**C-3 自检 cron** 和 **周日 cron 健康检查** 应该是发现 #1 #4 22 天 silent failure 的两道告警网 —— **两层都一起挂了**（root cause B），没人发现。

---

## 2️⃣ 根因（3 层）

### 🔴 根因 A：scripts 改造 + cron argv 不同步（L-34 复演）

7-1 大重构删 `daily_topic_collector.sh` / `topic_rss_collector.py`（INC-2026-07-03-002 治本），但某个 launchd 仍 schedule 调它 → 7-2 04:01 一次失败后**再没被调用**（cron_daily.log 7-2 后零新增）。

→ **L-34 教训复演**：scripts 改造必同步 cron argv 验证。

### 🔴 根因 B：推送脚本退出码 = 1 当告警 = OpenClaw cron 误判 error

`c3_daily_check.py` + `sunday_cron_health_check.py` 用 `sys.exit(main())`：
- main 在"告警已推飞书成功"场景 return 1
- OpenClaw cron 看到 exit code 1 标记 error

→ 这是 **L-36 教训命中**（7-15 已落档但未应用到 c3 + sunday 脚本）。

### 🔴 根因 C：launchd plist argv 失效未检测（L-49 族系缺口）

`wiki.monthly-refresher.plist` 指向 `monthly_refresher.py`（已删），launchd 静默退出（exit != 0 但 launchctl list 不报错）→ 没有任何看门狗发现。

→ L-49.5 / L-49.9 仅覆盖"cron 写对时"——不覆盖"持续有效"。

---

## 3️⃣ 修复（B + C 项 · 文博拍板 C 选项）

### B 项 1：`c3_daily_check.py` 退出码治本（L-36 治本）

4 处 `return 1` → `return 0`（告警已推飞书 = 业务成功），保留 `return 2` 当脚本异常。

### B 项 2：`sunday_cron_health_check.py` 退出码治本（L-36 治本）

1 处 `return 1` → `return 0`，保留 `sys.exit(2)` 当脚本异常。

### B 项 3：`wiki.monthly-refresher.plist` 退役

- `launchctl bootout gui/$(id -u)/com.nickfury.wiki.monthly-refresher`
- `mv .plist → .plist.disabled-20260724-cron-argv-watchdog`

### C 项：`cron_argv_watchdog.py` + OpenClaw cron 注册（L-49.12）

- 写新脚本 `scripts/cron_argv_watchdog.py`（6734 bytes）
- 全集扫描 OpenClaw cron argv + launchd plist argv 中的 `.py` / `.sh` 路径
- 有失效：写告警 + 飞书推送 + exit 0（L-36 治本）
- 无失效：静默成功 + exit 0
- OpenClaw cron 注册：每周日 21:00（id `f01832cf-4651-4d2b-b0b9-ba1979b37dd8`）
- **L-15 端到端验证全过**：fake plist 失效场景 → 检测 + 推飞书 + exit 0 ✅

---

## 4️⃣ 验证（端到端 3 步 · L-15 铁律）

### 验证 1：脚本语法 + 实跑

| 步骤 | 结果 |
|:---|:---|
| `py_compile cron_argv_watchdog.py` | ✅ 语法 OK |
| 实跑（应 0 失效）：扫到 48 cron / 3 plist 活跃 / 0 失效 | ✅ exit 0 |

### 验证 2：fake 失效场景

| 步骤 | 结果 |
|:---|:---|
| 建 fake plist `com.fake.test.dead.argv.plist` 指向 `__definitely_missing_xyz.py` | ✅ |
| 实跑：扫到 48 cron / 23 plist 活跃 / 1 失效（fake） | ✅ |
| 写告警文件 `data/argv_alerts/2026-07-24-0929.argv-watchdog.md` | ✅ |
| 飞书推送成功（lark-cli 主通道 · 295 字符） | ✅ |
| exit 0（L-36 治本） | ✅ |

### 验证 3：OpenClaw cron 注册

| 字段 | 值 |
|:---|:---|
| id | `f01832cf-4651-4d2b-b0b9-ba1979b37dd8` |
| name | `cron.argv.watchdog` |
| schedule | `0 21 * * 0` (Asia/Shanghai) = 每周日 21:00 |
| argv | `cd <BASE> && python3 scripts/cron_argv_watchdog.py`（L-49.11 治本） |
| delivery | `announce -> feishu:user:ou_ca04de68a40f571f59bcf2e71241415a`（L-35 对齐）|

---

## 5️⃣ 教训（L-49.12 · L-36 强化）

### L-49.12：cron argv 失效检测 cron（7 天看门狗）

每 7 天 grep 全集 OpenClaw cron + launchd plist argv 中的 `.py` / `.sh` 路径，存在性校验，失效即推飞书告警。

### L-36 强化：推送脚本退出码 = 0 当 lark-cli 主通道成功

适用于所有"告警 → 飞书推送 → 退出"模式的脚本（c3 / sunday / argv-watchdog 等）。

---

## 6️⃣ 24h 自动验证窗口

| 时点 | 期望 | 验证 |
|:---|:---|:---|
| 7-24 21:00 | c3 cron 修后首次 | exit 0 + 飞书推送成功 |
| 7-26 22:00 | sunday_cron_health_weekly 修后首次 | exit 0 |
| 7-26 21:00 | cron.argv.watchdog 注册后首次 | exit 0 + 0 失效（静默成功）|

---

## 7️⃣ 关联产物

| 路径 | 大小 | 状态 |
|:---|:---:|:---:|
| `wiki/review-logs/incidents/2026-07/inc_2026-07-24_001-cron-argv-watchdog-22d-vacuum.md` | ~6KB | ✅ |
| `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-24-cron-argv-watchdog-l49-12.md` | ~4KB | ✅ |
| `wiki/review-logs/lessons/by-agent/nick_fury/_nick_registry.md` | +1KB 增量区 | ✅ |
| `scripts/cron_argv_watchdog.py` | 6734B | ✅ |
| `scripts/c3_daily_check.py` | +1KB（L-36 注释 + 4 处 return 0）| ✅ |
| `scripts/sunday_cron_health_check.py` | +1KB（L-36 注释 + 1 处 return 0）| ✅ |
| `Library/LaunchAgents/com.nickfury.wiki.monthly-refresher.plist.disabled-20260724-cron-argv-watchdog` | rename | ✅ |
| OpenClaw cron id `f01832cf-...` | cron.argv.watchdog | ✅ |

---

*🕵️ 尼克·弗瑞 · INC-2026-07-24-001 · 7-24 09:35 CST · 30 min 闭环 · 文博拍板 C 选项*