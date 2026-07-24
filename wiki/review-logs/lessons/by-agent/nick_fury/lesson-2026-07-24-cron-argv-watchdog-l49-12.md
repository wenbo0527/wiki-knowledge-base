# L-49.12: cron argv 失效检测 cron（7 天看门狗）

> **作者**: 尼克·弗瑞 🕵️
> **创建**: 2026-07-24 09:35 CST
> **关联**: INC-2026-07-24-001
> **L-49 族系位置**: 第 13 层
> **铁律级别**: 🔴 P0 · 必查

---

## 🎯 1 条铁律

**任何 scripts 改造必同步 cron argv 验证（防失效）**，且每 7 天看门狗 cron 自动扫描 OpenClaw cron + launchd plist argv 中的 `.py` / `.sh` 路径存在性，失效即推飞书告警。

---

## 🔥 触发场景（INC-2026-07-24-001 实证）

| 现象 | 静默天数 | 检测路径 |
|:---|:---:|:---|
| `daily_topic_collector.sh` 7-2 死亡 | 22d | ❌ 无（cron 已删但 argv 残留）|
| `com.nickfury.wiki.monthly-refresher.plist` 指向已删脚本 | 22d+ | ❌ 无（launchd 静默）|
| `c3_daily_check.py` / `sunday_cron_health_check.py` exit 1 误判 | 1-5d | ✅ OpenClaw cron 状态 = error（但被 L-36 修复）|

**致命场景**：C-3 自检 cron + 周日 cron 健康 应该是发现 #1 #2 的两道告警网 —— **两层都挂**导致 22 天 silent failure。

---

## 🛠️ 实施清单

### 1. 写 `cron_argv_watchdog.py`

- 全集扫描 OpenClaw cron argv + launchd plist argv
- 提取 `/Users/...+\.(py|sh)` 路径
- `Path().exists()` 校验
- 有失效：写 `data/argv_alerts/*.argv-watchdog.md` + lark-cli 推飞书 + exit 0
- 无失效：log INFO + exit 0

### 2. 注册 OpenClaw cron

```bash
openclaw cron add \
  --agent nick_fury \
  --name "cron.argv.watchdog" \
  --cron "0 21 * * 0" \
  --tz Asia/Shanghai \
  --command "cd /Users/wenbo/.openclaw/workspace/agents/nick_fury && /usr/bin/python3 /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/cron_argv_watchdog.py" \
  --channel feishu \
  --to "user:ou_ca04de68a40f571f59bcf2e71241415a" \
  --session isolated
```

### 3. 退出码（L-36 治本）

- 0 = 全活 / 有失效但推送成功
- 1 = 有失效且推送失败
- 2 = 脚本异常

---

## 📊 L-49 族系扩展（7-24 更新到第 13 层）

```
L-49    cron edit 必看 argv 完整 JSON          (7-15)
L-49.5  argv 必查脚本路径存在性                 (7-15)
L-49.6  cron cleanup 决策树（4 类 + 4 动作）    (7-15)
L-49.7  INC 报告必加 enabled/disabled tag 区分 (7-17)
L-49.8  ID 引用必完整（grep 原文 + 长度校验）  (7-17)
L-49.9  脚本路径常量漂移 silent failure 治本   (7-20)
L-49.10 cron 投递必对齐派蒙模式                (7-21)
L-49.11 cron argv 必注入 cd cwd 上下文         (7-22)
L-49.12 cron argv 失效检测 cron（7 天看门狗）  ← NEW (7-24) 🆕
```

**本质延伸**：从"argv 写对"→"路径存在"→"清理决策"→"报告精度"→"标识精度"→"产物落点对"→"投递配置对"→"argv 上下文对"→**"argv 持续有效"**——逐层把 cron 运维从粗放到精确。

---

## ⚠️ 边界

| 维度 | 范围 |
|:---|:---|
| ✅ 团队通用 | 扫全 LaunchAgents plist（含其他 agent）|
| ✅ 路径匹配 | 仅 `/Users/...+\.(py\|sh)` 绝对路径 |
| ❌ 不覆盖 | cron schedule 表达（语法错误 / 失效周期）|
| ❌ 不覆盖 | payload kind 字段（command vs system-event）|
| ❌ 不覆盖 | delivery 字段（mode / channel / to 配错）|

后续可扩展（按 L-49 族系"逐层精确"思路）：
- L-49.13：cron schedule 语法校验
- L-49.14：cron delivery 字段全集复查（已部分在 sunday_cron_health_check L-35.1 实现）

---

## 🔗 关联

- **INC-2026-07-24-001**（22d RSS 真空 + 3 cron error + 1 plist 失效）
- **L-36 强化**（推送成功 = exit 0）— c3 + sunday 同步应用
- **L-34 复演**（scripts 改造必同步 cron argv）— 治本之一
- **L-49.5 升级**（argv 必查脚本路径存在性 · 单次 → 持续）

---

*🕵️ 尼克·弗瑞 · L-49 族系第 13 层 · 7-24 09:35 CST*