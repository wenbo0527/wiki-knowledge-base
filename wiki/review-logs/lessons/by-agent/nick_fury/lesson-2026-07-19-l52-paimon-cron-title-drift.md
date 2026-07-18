# Lesson L-52 · 派蒙 cron 标题漂移治本

> **日期**：2026-07-19
> **教训编号**：L-52.0 ~ L-52.3（4 条铁律）
> **触发 INC**：INC-2026-07-19-002（派蒙 cron 漂移 11 个 16-41 天）
> **状态**：⏳ 待派蒙侧修

---

## L-52 族系（4 条铁律）

### L-52.0 · cron 标题不带创建日期

**原则**：cron 标题应该用**功能描述**，不带日期 / 版本号

**理由**：
- 创建日期是一次性元数据，不应在标题中重复
- 版本号应该用 git tag / changelog 管理，不在 cron 标题里
- 日期易误导（看着像过期任务）

**反例**：
```
❌ PM-disconnect-escalate-20260608       # 41 天漂移，看着像过期
❌ 派蒙-T3prime-自查-NIGHT-20260703       # 16 天漂移
❌ 派蒙-9:00-软链自检-20260616            # 33 天漂移
```

**正例**：
```
✅ PM-disconnect-escalate                # 纯功能描述
✅ 派蒙-T3prime-自查-NIGHT                # 不带日期
✅ 派蒙-9:00-软链自检                     # 不带日期
```

---

### L-52.1 · 看到漂移 cron 别误删

**原则**：看到标题日期 < 真实日期的 cron，**别 disable / 别删**

**真实判断活跃度的方法**：
- `lastRunAtMs`（最后运行时间戳）
- `schedule.expr`（调度表达式）
- `enabled`（是否启用）
- `state.lastRunStatus`（最后状态）

**忽略标题日期**：
- 即使标题写 `-20260608`，只要 last run = 今天，cron 是活跃的

---

### L-52.2 · 派蒙 cron 注册脚本硬编码检测

**派蒙侧 cron 注册脚本必须**：
```python
# ✅ 正确：标题用功能描述，不带日期
name = "PM-disconnect-escalate"

# ✅ 正确：标题用功能 + 版本号
name = f"PM-disconnect-escalate-v2"

# ❌ 错误：标题带创建日期硬编码
name = f"PM-disconnect-escalate-{datetime.now().strftime('%Y%m%d')}"  # 只在注册时算一次
```

---

### L-52.3 · 升级 INC 阈值（通用规则）

**原则**：同一 Block 累计口头报告 ≥ 10 次必须升级 INC

**实战**：
- Block #1 派蒙 cron 漂移：6-30 / 7-2 / 7-12 / 7-13 / 7-14 / 7-15 / 7-16 / 7-17 / 7-18 / 7-19 = **10 次**
- 7-19 升级 INC-2026-07-19-002 闭环

**机制**：
- daily 报告里 Block #N 计数
- 达到 10 次 → 自动升级 INC + escalate 对应 owner
- 否则继续 daily 口头报告

---

## 应用清单（7-19 已应用）

| 应用项 | 状态 |
|:---|:---:|
| INC-2026-07-19-002 落档 | ✅ 6:35 |
| L-52 治本 lesson 落档 | ✅ 6:35 |
| escalate 派蒙（sessions_send）| ⏳ 待发 |
| _nick_registry 7-19 06:35 段 | ⏳ 待追加 |
| memory/daily 7-19 L-52 段 | ⏳ 待追加 |

---

## 关联教训

| 教训 | 关联 |
|:---|:---|
| **L-49.6** | cron cleanup 决策树（漂移 cron 不在清理范围）|
| **L-49.7** | INC 报告必加 enabled/disabled tag 区分 |
| **L-49.8** | ID 引用必完整 |

---

*🕵️ nick_fury · 2026-07-19 06:35 CST · L-52 派蒙 cron 漂移治本*