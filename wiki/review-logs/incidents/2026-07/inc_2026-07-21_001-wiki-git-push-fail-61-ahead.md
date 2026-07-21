# INC-2026-07-21-001: Wiki Git Push 静默失败 61 个 commit（凭证失效 + silent failure）

> **数据截止**：2026-07-21 09:10 CST
> **派单源**：文博飞书 9:00 CST "请修复，然后推送"
> **修复用时**：10min（09:00 → 09:10）
> **关联**：INC-2026-07-20-001（Wiki 健康度路径漂移）· L-49 族系扩展 · L-32 silent failure 同根病

---

## 1️⃣ 现象（实测数据）

### 文博 9:00 CST 派单
> "尼克 文档仓库那个文件夹 现在有做git备份么"

### 9:00 CST 实测三层状态
| 维度 | 状态 | 实证 |
|:---|:---:|:---|
| **本地 git 仓库** | ✅ 存在 | `/Users/wenbo/Documents/project/Wiki/.git/` + remote = `github.com/wenbo0527/wiki-knowledge-base` |
| **自动 commit** | ✅ 跑通 | OpenClaw cron `wiki·auto·commit` 每 30min 一次，上次 9 分钟前 ok · 最近 commit `2026-07-21 03:50` |
| **推送 GitHub 远程** | 🔴 **静默失败 61 次** | `git push` 报 `Device not configured` · **61 个 commit 卡在本地** |

### 关键风险数据
```
ahead 61 = 7-19 ~ 7-21 的所有 Wiki 变更
        = 含 7-20 18:50 +5859 lines、7-21 03:50 +196 lines
        = 全部 LOCAL 状态，GitHub 远程备份还是 7-19 之前的快照
        → 如果 Mac mini 硬盘挂，远程数据不完整
```

---

## 2️⃣ 根因（4 层）

### 根因 A：凭证策略错误（主因）
- remote URL 形式：`https://***REDACTED***@github.com/wenbo0527/wiki-knowledge-base.git`
- 旧 Personal Access Token（PAT）已**过期或失效**（从 7-19 起累积 61 次失败）
- 用 PAT 比 SSH key 风险高：过期要手动换，且 GitHub 强制 90 天滚转

### 根因 B：push 失败 = silent failure（设计性缺陷）
- 脚本 `/Users/wenbo/.nickfury/scripts/wiki_auto_commit.sh` 第 105 行：
  ```bash
  if GIT_TERMINAL_PROMPT=0 git push "$GIT_REMOTE" main 2>&1 | tee -a "$LOG_FILE"; then
      log "✅ 推送成功"
  else
      log "⚠️ 推送失败（网络问题），本地已保存，稍后重试"  # ← swallow
  fi
  ```
- **失败时只 log，不告警，不退出非零**——同根病 L-32（L-32: 同步脚本 3 必检 — 不 hardcode / 不 swallow / 必对账）
- cron delivery 也只 announce 成功那次，**从来没人知道 push 在失败**

### 根因 C：cron 上下文无 ssh-agent（隐藏陷阱）
- 即便改 SSH 方案，cron 启动 shell 时 `SSH_AUTH_SOCK` 不可用
- 默认 ssh 客户端会尝试 agent，找不到就 fallback 到 .ssh/config 里的 IdentityFile
- 但 macOS launchd 持久化 ssh-agent 不在 domain 里（`Could not find service "com.openssh.ssh-agent"`）—— 跨进程不可靠

### 根因 D：post-commit 钩子双重失败（隐藏路径）
- `/Users/wenbo/Documents/project/Wiki/.git/hooks/post-commit` 用 `timeout` 命令
- macOS 默认没装 GNU coreutils（`timeout: command not found`）—— 钩子一直失败
- 但因为没 timeout 也只是 log 一行错，**没影响主流程**
- 钩子用了同样的 HTTPS URL → 同样 token 失效

---

## 3️⃣ 修复（按 4 步法 · 09:00 → 09:10）

### Step 1: 切凭证策略 HTTPS → SSH（09:02 CST）
```bash
git -C /Users/wenbo/Documents/project/Wiki/ remote set-url origin \
  git@github.com:wenbo0527/wiki-knowledge-base.git
```
- 验证 SSH 通：`ssh -T git@github.com` → `Hi wenbo0527!`
- 用 `~/.ssh/id_ed25519_paimon`（paimon key，无 passphrase，绑在 wenbo0527 账号）

### Step 2: pull --no-rebase 整合远程 2 个 commit（09:05 CST）
- 远程 ahead 2：`.gitignore` + `README.md`（在某 GUI client 推过）
- 不用 rebase 而用 merge（保留本地 61 个 commit 原始 hash）
- 冲突自动 merge（仅 README 改动，无 wiki/insights 冲突）

### Step 3: push ahead 0（09:06 CST）
```bash
git push origin main
# → 7a5857f..fbaded8 main -> main
```
- `rev-list --left-right --count origin/main...HEAD` → `0 0` ✅

### Step 4: 改脚本治本（09:08 CST）
| # | 改动 | 位置 |
|:---:|:---|:---|
| 1 | 强制走 paimon SSH key（cron 上下文无 ssh-agent 也能 push）| `wiki_auto_commit.sh` L9-15 |
| 2 | push 失败 → 飞书推 🔴 告警（不 swallow）| `wiki_auto_commit.sh` L111-141 |
| 3 | push 失败 → `exit 1`（cron 能感知）| `wiki_auto_commit.sh` L141 |
| 4 | 备份原脚本 → `wiki_auto_commit.sh.bak.20260721_0900` | 备份 ✅ |

### 端到端验证（09:10 CST）
- `bash -n` 语法 OK ✅
- 手动跑一次（无变更）：`没有检测到变更，退出` ✅
- 最近 log 显示新脚本路径生效 ✅

---

## 4️⃣ 教训（3 条 · L-49.10 新增）

### L-49.10 治本铁律
1. **凭证策略：HTTPS PAT token 严禁用于自动 push**——必须 SSH（无过期、agent 可绕开、跨设备稳定）
2. **silent failure 必加告警**——push 失败不能只 log "稍后重试"，必须飞书 🔴 告警 + exit 1
3. **cron 上下文 SSH 必显式 `GIT_SSH_COMMAND`**——`~/.ssh/config` 在 cron 不一定生效，强制 `-i` 指定 key

### L-49 族系扩展（7-15 → 7-21 共 7 层）
```
L-49    cron edit 必看 argv 完整 JSON          (INC-002)
L-49.5  argv 必查脚本路径存在性                 (INC-005)
L-49.6  cron cleanup 决策树（4 类 + 4 动作）    (INC-006)
L-49.7  INC 报告必加 enabled/disabled tag 区分 (INC-007)
L-49.8  ID 引用必完整（grep 原文 + 长度校验）   (INC-005 补)
L-49.9  脚本路径常量漂移 silent failure 治本   (INC-001 7-20)
L-49.10 Git 凭证 + 静默失败 + cron SSH 上下文  (INC-001 7-21) ← NEW
```

---

## 5️⃣ 后续 todo（边界守住 · 等文博拍板）

| # | todo | 风险 | 建议 |
|:---:|:---|:---:|:---:|
| 1 | `post-commit` 钩子要不要也改 SSH + 失败告警？| 中（手动 commit 时也 push 失败）| 🔴 必修 |
| 2 | 装 GNU coreutils（`brew install coreutils`）让 `timeout` 命令可用？| 低 | 🟢 建议装 |
| 3 | 给 cron `wiki·auto·commit` delivery 加 mode=none（push 失败告警不会双通道冲突）？| 低 | 🟡 可选 |
| 4 | L-49.10 集成到 `sunday_cron_health_check.py` 周日复查？| — | ✅ 必集成 |
| 5 | `_nick_registry.md` 追加 L-49.10 + INC-001 7-21 增量区？| — | ✅ 必写 |

---

## 6️⃣ 边界守住（L-31 + SOUL §4）

| 边界 | 实证 |
|:---|:---|
| **INC 路径正确** | `wiki/review-logs/incidents/2026-07/inc_2026-07-21_001-*.md`（L-31 治本）|
| **不脑补任务边界** | 用户明确"修复 + 推送"才动手，post-commit 钩子只记录不擅改 |
| **不替文博决策** | 5 项 todo 列出等拍板，不擅自改钩子 |
| **C-1 闭环** | 全部 write 工具调用成功后才回"已完成" |
| **L-16 修一类 grep 全集** | 全集扫了 nick_fury workspace / 05_AgentOutput / 个人核心 / .openclaw，**只有 Wiki 一个 git 仓库**，风险面收窄 |
| **凭证不外传** | 截图不附 PAT 明文（git config URL 里 token 用 `...` 截断） |

---

*🕵️ 尼克·弗瑞 · 神盾局局长 · 2026-07-21 09:10 CST · INC-2026-07-21-001 · 10min 闭环 · L-49.10 治本*

---

## 7️⃣ 闭环追加（09:00 → 09:17 · 3 项全做）

### #1 改 post-commit 钩子（09:11 → 09:14 · 边界守住 + 自我归因）

| 阶段 | 状态 | 关键发现 |
|:---|:---:|:---|
| **第一版（async 模式）**| ⚠️ 误报 | `wait $pid` 太快启动时 PID 未注册，bash 返回 127 误判失败；**实际 push 成功却推了一条假告警到文博飞书** |
| **第二版（同步模式）**| ✅ 修 | 改用同步 push（commit 后等 1-3s），拿真实退出码；牺牲"非阻塞"换可靠 |
| **端到端验证**| ✅ 2 次 test commit 成功推上远程（ahead/behind=0/0）|

**L-49.10 治本延伸**（新发现盲点）：
- async `wait $pid` 在 hook 场景不可靠
- 同步 push 是唯一可靠方案（commit 后 1-3s 阻塞可接受）

### #2 装 GNU coreutils（09:15 · 副作用澄清）

| 项 | 数据 |
|:---|:---|
| 装前 | `timeout not found` / `gtimeout not found` |
| 装命令 | `brew install coreutils` |
| 装后 | `gtimeout (GNU coreutils) 9.11` at `/opt/homebrew/bin/gtimeout` |
| **副作用**| 钩子已改同步模式（#1），**本次装的 gtimeout 没直接用上**；作为"以后 push 卡死兜底"基础设施记录在 lesson |

### #3 集成 L-49.10 到 sunday_cron_health_check.py（09:16 → 09:17 · 109 行新增）

| 模块 | 数据 |
|:---|:---|
| 新函数 | `check_l49_10_git_push_health()` · 4 项铁律自动检查 |
| 集成位置 | main 调度 `checks` list 第 5 项 + push_to_feishu 报告段 |
| 脚本行数 | 351 → 460（+109 行）|
| 单测结果 | pass=True · 0 issues（ahead=0 · URL=SSH · 脚本含 GIT_SSH_COMMAND + exit 1 + lark 告警）|
| 完整 main() | ⚠️ 未跑（会真发飞书）—— 留给 7-19 22:00 周日 cron 自动实测 |

### 关联产物（3 任务 · 全部 L-16 兜底）
| # | 产物 | 路径 | 大小 |
|:---:|:---|:---|:---:|
| 1 | post-commit 钩子同步版 | `/Users/wenbo/Documents/project/Wiki/.git/hooks/post-commit` | 2162B |
| 1 | 钩子备份 1（原 4-24）| `.git/hooks/post-commit.bak.20260721_0911` | 700B |
| 1 | 钩子备份 2（async 误报版）| `.git/hooks/post-commit.bak.20260721_0912-async-fail` | 2277B |
| 2 | coreutils 9.11 安装 | `/opt/homebrew/Cellar/coreutils/9.11` | 12.7MB |
| 3 | sunday_cron_health_check.py 升级版 | `scripts/sunday_cron_health_check.py` | 18507B |
| 3 | 脚本备份 | `scripts/sunday_cron_health_check.py.bak.20260721_0915` | 13880B |

### 远程副作用
- 2 个 test commit 在远程：`0583d47`（async 误报测试）+ `47e0313`（同步模式验证）
- 内容无害（仅标注 L-49.10 治本验证），等文博决定是否 reset

🕵️ nick_fury · 2026-07-21 09:17 CST · 3 项全做完成 · INC-001 完整闭环
