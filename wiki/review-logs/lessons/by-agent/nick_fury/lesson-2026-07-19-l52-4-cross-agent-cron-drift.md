# Lesson L-52.4 · cron 漂移治本跨 agent 通用

> **日期**：2026-07-19
> **教训编号**：L-52.4（L-52 族系扩展）
> **触发 INC**：INC-2026-07-19-003（钟离 own cron 漂移 2 个）
> **状态**：⏳ 待钟离 own decision

---

## L-52.4 · cron 漂移治本跨 agent 通用

### 原则

> **每个 agent 的 cron 注册脚本都要检查标题生成逻辑**
> 不只是派蒙 own cron，所有 agent 都可能命中同根病

### INC-002 vs INC-003 对比

| 维度 | 派蒙 INC-002 | 钟离 INC-003 |
|:---|:---|:---|
| 漂移 cron 数 | 11 | 2 |
| 最大漂移天数 | 41 天 | 4 天 |
| 根因 | cron 标题写死创建日期 | 同 INC-002 |
| 治本方向 | A（标题改功能描述）| 待钟离选（A/B/C）|
| 闭环状态 | ✅ 已闭环 | ⏳ 待钟离 |

### Nick 24h 监控扩展

**等钟离 INC-003 闭环后**，Nick 验证脚本扩展：

```bash
# 当前
bash scripts/verify_paimon_cron_rename.sh  # 派蒙 11 个

# 扩展后（待钟离 INC-003 闭环）
bash scripts/verify_all_cron_rename.sh     # 全 agent cron 漂移验证
```

**监控指标**：
- `openclaw cron list | grep -- "-20260"` 应持续 = 0 行（含所有 agent）
- 派蒙已闭环 11/11
- 钟离待闭环 2/2

### 触发新 INC 阈值

| 触发条件 | 升级路径 |
|:---|:---|
| 钟离 INC-003 闭环 | ✅ 标 close |
| 钟离 24h 未响应 | 写 INC-004 升级（升级到文博） |
| 其他 agent cron 漂移（> 7 天）| 写 INC-NNN |

### 关联教训

| 教训 | 关联 |
|:---|:---|
| **L-52.0** | cron 标题不带创建日期 |
| **L-52.1** | 看到漂移 cron 别误删 |
| **L-52.2** | 派蒙 cron 注册脚本硬编码检测 |
| **L-52.3** | 升级 INC 阈值（≥ 10 次必升级）|
| **L-52.4** | cron 漂移治本跨 agent 通用（**新增**）|

---

*🕵️ nick_fury · 2026-07-19 07:08 CST · L-52.4 cron 漂移跨 agent 治本*