# L-13.1: launchd 专属决策必 disable 对应 OpenClaw cron（双跑 = 必去重）

> **创建时间**：2026-07-17 08:55 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-17-004（wiki·health·check 双跑）
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-17-launchd-vs-openclaw-cross-mechanism-dedup-l13-1.md`

---

## 🎯 核心教训

**launchd 专属决策必 3 步**：
1. ✅ 决策保留 launchd（如 wiki-health-check 因 TCC 限制）
2. ✅ **disable 对应 OpenClaw cron**（双跑必去重）
3. ✅ **AGENTS.md 写入决策**（防 7 天后遗忘）

**L-13 原版**（7-14 INC-006）：OpenClaw 原生优先——"每次新任务前必查 OpenClaw 原生，只有原生不覆盖时才自建 + 标注 ⚠️ + 写 INC"。

**L-13.1 升级**：launchd 专属决策必 disable 对应 OpenClaw cron（保留 ≠ 共存）。本次 wiki·health·check 双跑 3 天（7-14 ~ 7-17）就是 L-13 治本时决策了"保留 launchd"，但没 disable 对应 OpenClaw cron da137eba 的漏修。

---

## 📚 INC-004 揭穿真根因（实例）

### 双跑实证（data/wiki_health.log）

```
✅ 健康检查完成: Tue Jul 14 09:00:01 CST 2026   ← OpenClaw cron
✅ 健康检查完成: Tue Jul 14 09:00:06 CST 2026   ← launchd plist
✅ 健康检查完成: Wed Jul 15 09:00:01 CST 2026   ← OpenClaw cron
✅ 健康检查完成: Wed Jul 15 09:00:02 CST 2026   ← launchd plist
✅ 健康检查完成: Thu Jul 16 09:00:00 CST 2026   ← OpenClaw cron
✅ 健康检查完成: Thu Jul 16 09:00:02 CST 2026   ← launchd plist
✅ 健康检查完成: Thu Jul 16 19:38:36 CST 2026   ← 手动触发 1
✅ 健康检查完成: Thu Jul 16 19:38:57 CST 2026   ← 手动触发 2
```

**两个机制 argv 完全相同**：
- OpenClaw cron `da137eba` argv: `[sh, -lc, /bin/bash scripts/wiki_health_check.sh]`
- launchd plist `com.nickfury.wiki-health-check`: `/bin/bash scripts/wiki_health_check.sh`

### 为什么保留 launchd（TCC 限制）

- launchd plist `UserName=wenbo` → 9:00 跑 `wiki_health_check.sh`
- 脚本内部 `find /Users/wenbo/Documents/project/Wiki -name "*.md"` 需要 TCC 权限
- 在 OpenClaw cron gateway 进程下没 wenbo TCC（gateway 是 root 或系统用户）
- 所以 **必须保留 launchd plist**

**正确修法**：保留 launchd plist，disable OpenClaw cron da137eba（而非反向）。

### 7-14 INC-006 决策漏修链

| 7-14 INC-006 决策 | 实际状态 |
|:---|:---|
| ✅ 14 个重复 launchd plist disable | ✅ 完成 |
| ✅ wiki-health-check 保留 launchd（TCC 限制）| ✅ 决策正确 |
| ❌ **OpenClaw cron da137eba 没 disable** | ❌ 决策遗漏 |
| ❌ **AGENTS.md 没写入"wiki-health-check 是 launchd 专属"** | ❌ 文档遗漏 |

---

## 🔧 launchd 专属决策标准化清单

```bash
#!/bin/bash
# L-13.1 launchd 专属决策必跑 3 步

PLIST="$1"  # launchd plist 路径
CRON_NAME="$2"  # 对应 OpenClaw cron name

echo "=== L-13.1 launchd 专属决策 3 步 ==="

# Step 1: 决策保留 launchd（如 wiki-health-check 因 TCC 限制）
echo "[1] 决策保留 launchd: $PLIST"

# Step 2: disable 对应 OpenClaw cron
CRON_ID=$(openclaw cron list 2>&1 | grep "$CRON_NAME" | awk '{print $1}' | head -1)
if [ -n "$CRON_ID" ]; then
  echo "[2] disable 对应 OpenClaw cron: $CRON_NAME ($CRON_ID)"
  openclaw cron edit "$CRON_ID" --disable
fi

# Step 3: AGENTS.md 写入决策
echo "[3] AGENTS.md 写入决策:"
echo "  | $CRON_NAME | launchd plist \`$PLIST\` | 🟢 启动 TCC 专属 |
echo "  （防 7 天后遗忘）"
```

---

## 📜 L-13.1 教训族清单

| 编号 | 教训 |
|:---|:---|
| **L-13.1.1** | launchd 专属决策必 3 步：(1) 决策保留 launchd (2) **disable 对应 OpenClaw cron** (3) AGENTS.md 写入决策 |
| **L-13.1.2** | 双跑必 grep 全集（`openclaw cron list` + `launchctl list | grep com.nickfury`）—— 跨机制全集 |
| **L-13.1.3** | wiki_health_check.log 9:00 双时间戳 = 双跑信号（任何 log 同分钟双记录 = 必查）|
| **L-13.1.4** | 7-19 周日 cron 新增 "launchd plist vs OpenClaw cron 跨机制重复检测" |

---

## 🎯 防退化机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次 launchd 专属决策** | L-13.1.1 三步 | `scripts/launchd_dedup.sh`（待写）|
| **每周日 22:00** | 跨机制重复检测 | `scripts/cross_mechanism_dedup_check.sh`（待写）|
| **每日 9:00** | wiki_health_check.log 单时间戳检查 | `scripts/wiki_health_check.sh` 升级 |
| **每次新 INC** | 必查 `find review-logs -name "*duplicate*"` | L-31 |

---

## 关联

- **INC-2026-07-14-006**（launchd → OpenClaw cron 迁移）—— L-13 原版
- **INC-2026-07-17-004**（wiki·health·check 双跑）—— 揭穿案例
- **L-13**（OpenClaw 原生优先 · 7-14 决策）—— 原版
- **L-13.1**（新增 · launchd 专属必 disable 对应 OpenClaw cron）
- **cron da137eba**（已 disable · launchd plist 保留）
- **launchd plist com.nickfury.wiki-health-check**（保留 · 9:00 跑）