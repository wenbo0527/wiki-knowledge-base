# L-49.7: INC 报告必加 enabled/disabled tag 区分（L-49.6 强化版）

> **创建时间**：2026-07-17 14:40 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-17-007（INC-006 报告纠错 · escalate 钟离）
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-17-inc-report-enabled-disabled-tag-l49-7.md`

---

## 🎯 核心教训

**INC 报告必加 `WHERE enabled=1` 过滤**——不要拿"全集"算"需要修的"。

**sunday_cron_health_check.py alert 必加 tag 区分**（必修 vs 保留）—— 用户 1 秒看懂该做什么。

---

## 📚 INC-007 揭穿真根因（实例）

### INC-006 报告原文错误

> **剩余 17 个问题分类**：
> - 14 个 disabled cron delivery 错配（保留）
> - **3 个 enabled cron delivery 错配**（钟离 2 + nick_fury 测试 1）—— **错！**

### 14:34 纠错实证

```sql
-- 真 enabled delivery 错配（精确集）
SELECT COUNT(*) FROM cron_jobs
WHERE enabled=1
  AND delivery_mode='announce'
  AND (delivery_channel!='feishu'
       OR delivery_to IS NULL
       OR delivery_to=''
       OR delivery_to NOT LIKE 'user:%');
-- 结果: 2 (不是 3！)
```

### 误判来源

- INC-006 我用 sqlite 查 `delivery_mode='announce' AND ...` 没加 `enabled=1` 过滤
- 把 disabled 算成 enabled（"测试情报推送" / "每日情报推送" / "wiki-lint" 实际全 disabled）

---

## 🔧 L-49.7 升级实现（sunday_cron_health_check.py）

```python
# L-49.7 升级: enabled/disabled tag 区分
if mode == "announce":
    # L-49.6 升级: enabled/disabled tag 区分（enabled 必修 / disabled 保留）
    tag = "🔴 " if data.get("enabled") else "⚠️ "
    action = "必修" if data.get("enabled") else "保留（C 决策）"
    if channel != "feishu":
        issues.append(f"{tag} {name}: mode=announce 但 channel={channel} · {action}")
    if not to.startswith("user:"):
        to_display = to[:30] if to else "(空)"
        issues.append(f"{tag} {name}: mode=announce 但 to={to_display} · {action}")
```

### 升级后 alert 输出（14:38 实证）

```
🔴 钟离-SOP空闲探活-20260715: mode=announce 但 to=ou_xxx · 必修
🔴 钟离-P0阻塞3级升级-1h-20260716: 同上 · 必修
⚠️ 15 个 disabled cron · 保留（C 决策）
```

---

## 📜 L-49.7 教训族清单

| 编号 | 教训 |
|:---|:---|
| **L-49.7.1** | INC 报告必加 `WHERE enabled=1` 过滤（不要拿"全集"算"需要修的"）|
| **L-49.7.2** | sunday_cron_health alert 必加 tag 区分（必修 vs 保留）· 用户 1 秒看懂该做什么 |
| **L-49.7.3** | "enabled delivery 错配必修 + disabled delivery 错配保留" 是 L-49.6 决策树核心 |
| **L-49.7.4** | 跨 agent escalate 必带 cron ID + L-35 标准修法（参考已修案例）|

---

## 🎯 防退化机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次 INC 报告** | L-49.7.1 必加 enabled=1 过滤 | 标准 checklist |
| **每日 22:00** | sunday_cron_health 自动 tag 区分 | 已升级 |
| **每周日 22:00** | 周报必含 enabled vs disabled 分类 | 手动 |
| **每次跨 agent escalate** | L-49.7.4 必带 cron ID + L-35 标准修法 | 标准模板 |

---

## 关联

- **INC-2026-07-17-006**（用户决策 C · 9 死脚本 rm）—— 误判源头
- **INC-2026-07-17-007**（INC-006 报告纠错 · escalate 钟离）—— 揭穿案例
- **L-29**（报告必区分输出成功 vs 输入真实）—— 直接相关
- **L-49.6**（cron cleanup 决策树）—— 强化版基础
- **L-49.7**（新增 · INC 报告必加 enabled/disabled tag）
- **scripts/sunday_cron_health_check.py**（升级版 · L-49.6 tag + L-49.7 集成）