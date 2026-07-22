# L-49.11: Cron argv 必注入 cd cwd 上下文（cron 上下文 ≠ 手动上下文）

> **作者**: 尼克·弗瑞 🕵️
> **创建**: 2026-07-22 21:55 CST
> **关联**: INC-2026-07-22-001
> **L-49 族系位置**: 第 12 层
> **铁律级别**: 🔴 P0 · 必查

---

## 🎯 1 条铁律

**所有 OpenClaw cron argv 必以 `cd <BASE_DIR> &&` 开头**，确保脚本启动 cwd 锚定到工作区根目录。

```bash
# ✅ 正确
argv: ["sh", "-lc", "cd /Users/wenbo/.openclaw/workspace/agents/nick_fury && /usr/bin/python3 <BASE>/scripts/foo.py"]

# ❌ 错误（cron 上下文 cwd = 用户家目录，相对路径全失效）
argv: ["/usr/bin/python3", "<BASE>/scripts/foo.py"]
```

---

## 🔥 触发场景

| 现象 | 命令 | argv | 手动跑 | cron 跑 |
|:---|:---|:---|:---:|:---:|
| exit 0 vs exit 1 | c3_daily_check.py | 绝对路径 | ✅ exit 0 | ❌ exit 1 |
| exit 0 vs exit 1 | sunday_cron_health_check.py | 绝对路径 | ✅ exit 0 | ❌ exit 1 |
| sources=135 vs 0 | daily_pipeline.py | 相对 config_path | ✅ 135 | ❌ 0 |

**手动 vs cron 差异**（已实测确认）：

| 维度 | 手动 | cron |
|:---|:---|:---|
| cwd | 工作区根 | 用户家目录（默认）|
| PATH | 完整 shell PATH | 极简 PATH |
| HOME | 正常 | 可能不同 |
| LANG/LC_ALL | UTF-8 | 可能 C/POSIX |

---

## 🪜 4 项必查清单

任何 cron argv 修改必走：

1. **[ ] argv 是否以 `cd <BASE_DIR> &&` 开头**？（强制锚 cwd）
2. **[ ] BASE_DIR 是否绝对路径**？（不依赖 $HOME 推断）
3. **[ ] 脚本内部是否有 sys.path.insert 相对 BASE_DIR**？（防止 lark_cli_wrapper 类相对 import 失败）
4. **[ ] 修改后是否手动 + cron 端到端各跑一次**？（L-15 5 步）

---

## 🛠️ 修改 API

```bash
# 1 个 cron
openclaw cron edit <id> --command "cd <BASE> && /usr/bin/python3 <BASE>/<script>.py"

# 批量（同模式）
for id in ${cron_ids[@]}; do
  openclaw cron edit "$id" --command "cd <BASE> && <rest>"
done
```

**禁止模式**：
- ❌ `cd ~/<path>`（依赖 $HOME）
- ❌ `cd .`（相对）
- ❌ 多个 `&&` 嵌套（不易排查）

---

## 📊 L-49.11 在 L-49 族系的位置

```
L-49    cron edit 必看 argv 完整 JSON          (INC-002)
L-49.5  argv 必查脚本路径存在性                 (INC-005)
L-49.6  cron cleanup 决策树（4 类 + 4 动作）    (INC-006)
L-49.7  INC 报告必加 enabled/disabled tag 区分 (INC-007)
L-49.8  ID 引用必完整（grep 原文 + 长度校验）
L-49.9  脚本路径常量漂移 silent failure 治本   (7-20)
L-49.10 cron 投递必对齐派蒙模式                (7-21)
L-49.11 cron argv 必注入 cd cwd 上下文         ← NEW (7-22) 🆕
```

**本质延伸**：从"argv 写对"→"脚本路径存在"→"清理决策"→"报告精度"→"标识精度"→"产物落点对"→"投递配置对"→**"argv 上下文对"**——逐层把 cron 运维从粗放到精确。

---

## ⚠️ 反例（7-22 真实踩坑）

| 修前 argv | 修后 argv | 影响 |
|:---|:---|:---|
| `/usr/bin/python3 .../c3_daily_check.py` | `cd $BASE && /usr/bin/python3 .../c3_daily_check.py` | 修 c3 cron 3d silent |
| `/usr/bin/python3 .../daily_pipeline.py collect 30` | `cd $BASE && /usr/bin/python3 .../daily_pipeline.py collect 30` | 仅 cd 治不了 sources=0 根因 |

**L-49.11 不能独立治本 rss.collect 0 源**——那个更深层在 daily_pipeline.py 相对 config_path（由 L-52.6 治本）。

---

## 📈 验证窗口

- 7-23 09:00 c3 cron 自动跑 → 应 exit 0 + 飞书推送
- 7-23 22:00 cron_health 自动跑（不在周日）→ 应 exit 0
- 7-26 22:00 cron_health 周日跑 → 应 exit 0
- 7-23 01:00 rss.collect 自动跑 → **期望 sources > 0**（验证 daily_pipeline.py 修复）

---

*🕵️ 尼克·弗瑞 · L-49 族系第 12 层 · 7-22 创建 · 7-23 自动验证窗口*
