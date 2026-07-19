# INC-2026-07-19-009 · 周日 Cron 健康检查 disabled noise 修复

> **INC 编号**：INC-2026-07-19-009
> **日期**：2026-07-19 22:09 CST
> **触发**：文博 22:09 "周日 Cron 健康检查告警 请检查一下问题"
> **严重度**：🟡 Medium（cron 误报 error · L-49.6 实施不完整）
> **状态**：✅ 修复 + verify · cron 下次 7-26 自动 PASS
> **关联**：INC-2026-07-19-006（cron cleanup 决策 C）· L-49.6（enabled/disabled tag）· L-49.7（INC 报告 tag）

---

## 1️⃣ 现象

周日 22:00 nick_cron_health_weekly 首次跑通，**但 status=error**：

```
[2026-07-19 22:00:41] Running L-35.1 cron delivery 全集复查...
[2026-07-19 22:00:41]   ❌ 15 个问题
[2026-07-19 22:00:41] 汇总: 15 个问题
[2026-07-19 22:00:41] ✅ 飞书推送成功 (1042 字符)
```

**告警文件**：data/sunday_alerts/sunday_alert_20260719-220041.md（1042 字符）
**consecutiveErrors**：1
**cron status**：error（虽然业务跑通）

---

## 2️⃣ 根因

### 2.1 L-35.1 检测逻辑缺陷

`sunday_cron_health_check.py:183-205` 检查所有 `mode=announce` cron（包括 disabled）的 delivery 字段：

```python
# ❌ 原代码：所有 disabled cron 也计入 issues
for cron_id, data in all_data.items():
    if mode == "announce":
        tag = "🔴 " if data.get("enabled") else "⚠️ "
        action = "必修" if data.get("enabled") else "保留（C 决策）"
        if channel != "feishu":
            issues.append(f"{tag} {name}: mode=announce 但 channel={channel} · {action}")
        # ... to 检测同样
```

### 2.2 7-17 文博决策 C 已保留这些 disabled cron

INC-2026-07-19-006 中，文博对 9 个 disabled cron 拍板 **"保留（C 决策）"**：
- 测试情报推送 / 每日情报推送 / 米家生态提醒 / wiki-lint
- P1-10-M03-1600-钟离预警检查
- 钟离-bigmodel部署轮询 06:30/07:30/08:30
- 钟离-候选#235派蒙14:01watchdog-20260716

**L-49.6 实施的 tag 区分不完整**：
- ✅ issues 列表带 `⚠️ 保留（C 决策）` 标记
- ❌ 但仍计入 issues 数量 → 触发 cron error 告警

### 2.3 15 个问题分布

| 维度 | 数量 |
|:---|:---:|
| 全部是 disabled cron | 11 个 |
| channel 不为 feishu | 9 个 |
| to 缺 `user:` 前缀或空 | 9 个 |
| （部分 cron 同时有 2 个问题）| 15 个 |

---

## 3️⃣ 修复（L-62 升级 · 5 分钟）

### 3.1 修脚本（sunday_cron_health_check.py）

**新增 L-62 升级**：disabled cron **仅报告不计入 issues**

```python
# ✅ 修复后：disabled cron 单独列表，不影响 cron error 判定
def check_l35_1_cron_delivery():
    issues = []
    disabled_warnings = []  # L-62 升级
    for cron_id, data in all_data.items():
        if mode == "announce":
            enabled = data.get("enabled", True)
            target_list = issues if enabled else disabled_warnings
            # ... 检查并添加到对应列表
    if disabled_warnings:
        print(f'[L-62] disabled cron 报告（仅参考）：')
        for w in disabled_warnings:
            print(f'  {w}')
    return (len(issues) == 0, issues)
```

### 3.2 端到端 verify

```
修复前: 汇总 15 个问题 ❌ 飞书 1042 字符
修复后: 汇总 0 个问题 ✅ 飞书 170 字符
       [L-62] disabled cron 报告（仅参考）：15 个 ⚠️ （不计入告警）
```

### 3.3 飞书消息对比

- 修复前：1042 字符的告警（15 个问题）
- 修复后：170 字符的"全通过"消息

---

## 4️⃣ 教训

### 🆕 L-62 · 检测脚本必须区分 disabled vs enabled（不计入）

> **原则**：检测脚本发现 issue 时，**必须**区分 enabled/disabled：
> - enabled 必修 → 计入 issues → 触发告警
> - disabled 保留（C 决策） → 仅日志参考 → 不计入 issues

**实战**：L-49.6 实施只加了 tag，**没改 issues 数量** → 治本不彻底

### 🆕 L-63 · cron health 告警应分级

> **原则**：cron 健康检查的告警**应分级**：
> - 🔴 必修（enabled + 异常）：触发 cron error + 飞书告警
> - ⚠️ 参考（disabled + 异常）：仅日志 · 不告警
> - 🟢 全通过：飞书推"全 OK"短消息（确认机制运转）

### L-49.6 / L-49.7 强化

- L-49.6 tag 区分 + L-62 数量分离 = 治本完整
- L-49.7 INC 报告 tag 区分（这次触发升级条件 · 完美应用）

---

## 5️⃣ 等下次验证

| 节点 | 动作 |
|:---|:---|
| **下次周日 7-26 22:00** | nick_cron_health_weekly 自动跑通 → status=ok 验证 L-62 修复 |
| 平时每日 | 检测脚本按修复后逻辑运行，disabled cron 不再触发告警 |

---

*🕵️ nick_fury · 2026-07-19 22:19 CST · INC-2026-07-19-009 · 周日 Cron 健康检查 disabled noise 修复 · L-62 升级*
