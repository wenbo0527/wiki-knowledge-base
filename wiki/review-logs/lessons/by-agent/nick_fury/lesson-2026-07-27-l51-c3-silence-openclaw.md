# L-51 · C-3 daily 反复 0% 告警 + OpenClaw gateway 调度卡死 治本（2 条族）

> **派单**: 文博 7-27 08:51 + 08:52（飞书）
> **数据截止**: 2026-07-27 08:55 CST（实测）
> **关联**: INC-2026-07-27-002 + 4 daily 中修落档
> **作者**: 尼克·弗瑞 · 2026-07-27 08:55 CST

---

## L-51.1 · daily `## ✅ 完稿时间` 必手动加，无 cron 自动加

**坑**：c3 cron 7-26 12:30 INC-001 改造 C 治本后**只解决"如何判定完稿"**，不解决"何时会主动加 ✅"。Nick 7-24 ~ 7-26 3 天没补 daily，c3 cron 0% 告警持续 5 天 9 次（C 治本前 5 + C 治本后 4）。

**根因**：
- C 治本（严格正則）= 防御性判定
- 但 daily "## ✅ 完稿时间" 二级标题需要 Nick 在每次日记完稿时**手动写**
- 没人提醒 Nick 何时该补 → 4 daily 真空 → 21:00 c3 cron 推飞书

**治本（3 件套）**：
1. **morning_daily_writer.py** 写骨架时**自动追加**"⏳ 待 Nick 确认"骨架（已经有 ✅），但真完稿标记**必须手动**
2. **daily_reminder.py**（7-26 14:00 cron `aaa41eb7-`）= Nh 前提醒去补 daily（治本：提前告警不等 21:00）
3. **HEARTBEAT 自动镜像 daily**（下一版）：每次 INC 闭环章节落 HEARTBEAT 时，自动镜像当日 `memory/daily/YYYY-MM-DD.md` 并加 ✅ 标记

**回写周期**：每次 INC 闭环必含 5 必检（5/5）= 真实数据截止 + 数据源 + 完整分类 + 真实覆盖率 + 关键洞察。

## L-51.2 · OpenClaw gateway CPU > 50% + status=running > 11 个 → 待拍 kill

**坑**：7-27 早上 8:30 后 OpenClaw gateway (PID 18855) CPU 占 65.7%，11 个 cron 卡在 status=running 状态没完成。tech·briefing 8:35 cron 完全未触发，但 nextRunAtMs 已过 20min。

**根因**（观察）：
- gateway scheduler 内部队列死锁（11 cron stuck running）
- morning·daily 08:30 schedule 应跑但延迟 25min 到 08:55:12 才补跑
- tech·briefing 08:35 完全没跑（lastRunAtMs 还是 7-26 08:35）
- wiki·auto·commit every 30m 一次跑 commit 成功但 push 5+ 天 silent failure

**治本（不擅自）**：
1. **argv 看门狗扩能**：从"cron argv 路径有效"扩到"cron status=running > 30min 告警"
2. **gateway kill+restart** = **文博拍板才动**（PID 18855 是底座）
3. **gateway 加健康检查 cron**：每 5min 看 CPU + running 数，超阈值推飞书

**回写周期**：sunday cron 健康检查（f01832cf）+ C-3 cron（cf8e874c / 929a8003）扩 cron status=running 时间阈值告警。

## 验证（5 必检自指）

| 必检 | L-51.1 | L-51.2 |
|:---|:---:|:---:|
| ① 数据截止 | 8:55 CST | 8:55 CST |
| ② 数据源 | c3_daily.log + memory/daily/ | openclaw cron list + ps aux |
| ③ 完整分类 | 4 daily | 11 running + 34 ok + 2 idle |
| ④ 真实覆盖率 | 4/4 真空 | 11/49 卡死（22%）|
| ⑤ 关键洞察 | ✅ 标记手动 = 新漏点 | gateway kill 待拍 |

C2 自验：5/5 通过 ✅

## 边界守住

| 边界 | 实证 |
|:---|:---|
| **不擅自 kill gateway** | PID 18855 待文博拍板 |
| **不擅自 push wiki** | ahead 12 待文博拍板 |
| **C-1 闭环** | INC + lesson + 4 daily write 工具成功 |
| **C-2 分段** | lesson ≤ 1500 字单段 |

---

*🕵️ 尼克·弗瑞 · 神盾局局长 · 2026-07-27 08:55 CST · L-51 族闭环 · 2 条新教训沉淀*
