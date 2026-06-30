# INC-2026-06-30-001：Nick 推送链路断裂 + launchd 23 plist 迁 openclaw cron

> **作者**：尼克·弗瑞
> **日期**：2026-06-30
> **状态**：🟡 In Progress
> **触发**：文博 6-30 09:22 反馈"今天好像没有收到推送？"
> **根因层级**：🔴 系统级（OpenClaw 官方 cron 系统未对齐）+ 🟠 治理级（launchd 绕路）
> **关联**：INC-2026-06-08-001（口头承诺未落盘）/ INC-2026-06-15-001（PermissionError 44 天）/ INC-2026-06-23-001（launchd 11 plist 错根因）

---

## 一、现象

| 时间 | 事件 | 数据 |
|:---|:---|:---|
| **6-29 19:36** | morning_rss_etf_push 第 1 次 lark-cli exit 3 token_missing | 通道 3 wiki ✅ / 通道 1 ❌ / 通道 2 ❌ |
| **6-30 07:15** | morning_rss_etf_push 最后一次：lark-cli exit 127 node not found | 通道 3 wiki ✅ / 通道 1 ❌ / 通道 2 ❌ |
| **6-30 08:30** | OpenClaw cron `da3c0cae` 第 4 次 `isolated agent setup timeout` | 文博 12h 内零推送 |
| **6-30 08:35** | tech-briefing launchd 任务 `FEISHU_WEBHOOK_URL` 缺失 | "📋 飞书webhook未配置，简报仅打印" |
| **6-30 09:22** | 文博反馈"今天好像没有收到推送？" | 真空 12h+，无人告警 |

**关键症状**：
- 文博 6-30 08:30 推送应该收 3 份（科技简报 + RSS/ETF 简报 + ETF 何刚报告）→ **0/3 收到**
- 报告 ✅ 都生成了（落盘 Wiki），但飞书投递 100% 失败
- 监督层 C-3 cron (`launchctl list | grep " 78 "`) **未发现** OpenClaw cron 8:30 失败

---

## 二、根因（双层 + 3 个并存系统的真相）

### 2.1 系统级根因（之前误判）

**我 09:24 之前的诊断**（已错）：
- ❌ "tech-briefing.plist 缺 FEISHU_WEBHOOK_URL"
- ❌ "lark-cli 找不到 node（PATH 不含 /opt/homebrew/bin）"

**这些都是 launchd 那条线的问题，跟 8:30 主推送无关。**

### 2.2 真正的系统根因（OpenClaw 官方 cron 失败）

```
ID: da3c0cae-34d5-4f88-8133-f9589837fb6c
Name: 尼克·弗瑞 - 每日情报推送
Schedule: cron 30 8 * * * @ Asia/Shanghai
Last run: 41m ago (6-30 08:30)
Status: error  ← consecutiveErrors: 4
Last error: "cron: isolated agent setup timed out before runner start"
Last duration: 60008 ms (60s timeout)
Delivery: feishu:ou_ca04de68a40f571f59bcf2e71241415a
```

按官方 cron-jobs.md 文档：
> If an isolated agent-turn stalls before the runner starts or before the first model call, cron records a phase-specific timeout such as `setup timed out before runner start` or `stalled before first model call (last phase: context-engine)`. These watchdogs cover embedded providers and CLI-backed providers before their external CLI process is actually started, and are capped independently from long `timeoutSeconds` values so cold-start/auth/context failures surface quickly instead of waiting for the full job budget.

**这是 cold-start/auth/context 失败**——不是 webhook 缺失。

### 2.3 治理级根因（23 vs 2 的严重失衡）

| 调度器 | Nick 任务数 | 状态 |
|:---|---:|:---|
| **launchd plist** | 23 | 我单打独斗，没跟团队对齐 |
| **openclaw cron** | 2 | 1 个失败 4 次，1 个正常 |
| **其他 agent 对比** | 派蒙 7+ / 钟离 3+ / 托尼 1+ | 全部用 openclaw cron |

**派蒙、钟离、托尼都用 openclaw cron。就我 Nick 用 launchd。** 6-23 我修了 11 个 launchd plist 是**治标不治本**——真本是我用错了调度器。

### 2.4 doctor 输出（feishu 通道层）

```
- Left plugin install index in place because shared SQLite state has 
  conflicting plugin install metadata for: feishu
- Feishu session agent:nick_fury:feishu:direct:ou_415aaf2674f34d5034a3e71882b89d94
  points to a missing transcript in 
  ~/.openclaw/agents/nick_fury/sessions/sessions.json
- Feishu session agent:main:feishu:direct:ou_ca04de68a40f571f59bcf2e71241415a
  points to a missing transcript in 
  ~/.openclaw/agents/main/sessions/sessions.json
```

**feishu session transcript 缺失** = cron 启动 agent 时加载 transcript 失败 → setup timeout。

### 2.5 教训沉淀对比（6-23 错根因 vs 6-30 真根因）

| 维度 | 6-23 我的判断 | 6-30 真相 |
|:---|:---|:---|
| 根因 | plist 缺 UserName + UMASK | **plist 不该用**——OpenClaw 有官方 cron |
| 修法 | 加 UserName / UMASK 后 launchd 重启 | **应该迁到 openclaw cron** |
| 任务数 | 修 11/12 plist | 23 个 plist 全部该退役 |

---

## 三、修复计划（C 选项 = B + Standing Orders 写 AGENTS.md）

### 3.1 Phase 1：feishu 通道修复（10 min）

| 动作 | 投入 | 验收 |
|:---|:---:|:---|
| `openclaw doctor --fix` 修复 feishu session transcript 缺失 | 5 min | doctor 警告清零 |
| 手动 `openclaw cron run da3c0cae-...` 验证 8:30 推送能否跑通 | 5 min | isolated agent 不再 setup timeout |

### 3.2 Phase 2：launchd 23 plist 全部迁 openclaw cron（2-3 h）

**对照表**（待补完整）：

| launchd plist | 对应 openclaw cron（拟） | Schedule | Agent |
|:---|:---|:---|:---|
| bestpractice.daily.append | 派蒙已有 bestpractice 系 | 由派蒙管 | - |
| bestpractice.daily.collect | 派蒙已有 | 由派蒙管 | - |
| bestpractice.daily | 派蒙已有 | 由派蒙管 | - |
| bestpractice.round2 | 派蒙已有 | 由派蒙管 | - |
| daily-note-scan | 拟新建 | cron 0 8 * * * | nick_fury |
| daily-report-c3 | 拟新建（接 C-3 自检）| cron 0 21 * * * | nick_fury |
| etf.hegang.report | 拟新建（独立 bug：4 天未刷新）| cron 0 8 * * * | nick_fury |
| getnote-wiki-sync | 拟新建 | every 6h | nick_fury |
| github.track | 拟新建 | every 6h | nick_fury |
| kb.track | 拟新建 | daily 09:00 | nick_fury |
| morning-daily | **已存在**：`f0da80b0` 尼克·弗瑞-日报定时（cron 10 1 * * *）| 凌晨 1:10 | nick_fury |
| morning-rss-etf-push | **已存在**：`da3c0cae` 8:30 推送（修复后）| cron 30 8 * * * | nick_fury |
| rss.collect | 拟新建 | cron 0 4 * * * | nick_fury |
| rss.daily | 拟新建 | cron 30 8 * * * | nick_fury |
| rss.organize | 拟新建 | weekly 周日 22:00 | nick_fury |
| tech-briefing | 拟新建 | cron 35 8 * * * | nick_fury |
| wiki-auto-commit | 拟新建 | every 1h | nick_fury |
| wiki-health-check | 拟新建 | cron 0 9 * * * | nick_fury |
| wiki.daily-expander | 拟新建 | cron 0 22 * * * | nick_fury |
| wiki.ingest | 拟新建 | every 4h | nick_fury |
| wiki.monthly-refresher | 拟新建 | cron 0 3 1 * * | nick_fury |
| wiki.review | 拟新建 | weekly 周六 20:00 | nick_fury |
| wiki.weekly-synthesizer | 拟新建 | weekly 周日 20:00 | nick_fury |
| wiki.lint | ✅ **已退役**（6-23 移到 disabled/）| - | - |

**23 → 0 launchd plist**，全部用 `openclaw cron add` 重建。

**验收**：
- 24h 观察所有新 cron 跑通
- launchd `~/Library/LaunchAgents/com.nickfury.*.plist` 全部移到 `disabled/`
- launchctl list 不再有 com.nickfury.* 状态

### 3.3 Phase 3：Standing Orders v2.0 写进 AGENTS.md 顶部（30 min）

按官方 standing-orders.md 规范：
> The recommended approach is to include them directly in `AGENTS.md` (which is auto-injected every session) so the agent always has them in context.

**改造**：
- 读 6-15 Standing Orders v2.0.md（已存在）
- 提取 Program 段（4 件套：Scope/Triggers/Approval gates/Escalation）
- 写进 `AGENTS.md` 顶部（在 `## 0. 全局路径配置` 之前）作为 `## Program: 尼克·弗瑞永久授权指令`
- 删除 MEMORY.md 里的 file:// 引用（auto-inject 每次会话都有，不需要记路径）

**验收**：
- `grep "Program: 尼克·弗瑞" AGENTS.md` 命中
- 下次会话 bootstrap 阶段能看到 Program 段
- C-1 / C-2 / C-3 硬约束直接来自 Program 段而非 SOUL §8.1

### 3.4 Phase 4：验证 + 收尾（30 min）

- 24h 后 `openclaw cron list | grep error` 应为 0
- 24h 后 launchd 0 状态 plist = 0
- daily.md / lessons.md 三件套落盘
- 写 lessons.md

---

## 四、临时止血（A 已含）

**今天 6-30 08:30 推送已用 sessions_send 立即重推**（前面 9:24 已承诺，10:03 文博拍板 C 后未实际执行）——**等等，C-1 硬约束要求先实际执行再回话**。我必须现在就 push 才能说"已完成"。

---

## 五、Lessons 沉淀

待 Phase 1~4 完成后补全，先占位：
- L-13 反思 ≠ 改变：6-23 launchd 修了 11 plist 但**没问"为什么 Nick 用 launchd 而别人用 openclaw cron"**
- L-14 修一个 ≠ 修一类：feishu session transcript 缺失**会影响所有 cron 8:30 推送**，不是单点
- L-15 监督层要覆盖官方机制：C-3 cron 用 `openclaw cron list | grep error` 不用 `launchctl list | grep 78`
- L-16 Standing Orders 必须写 AGENTS.md：auto-inject 才会每次会话都生效

---

*作者：尼克·弗瑞 🕵️*
*状态：In Progress*
*下次更新：Phase 1 完成后（预计 10:30）*
