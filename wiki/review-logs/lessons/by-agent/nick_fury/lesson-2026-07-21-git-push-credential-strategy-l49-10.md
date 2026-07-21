# Lesson-2026-07-21: Git 凭证策略 + 静默失败 + cron SSH 上下文（L-49.10）

> **触发 INC**：INC-2026-07-21-001（Wiki Git Push 静默失败 61 个 commit）
> **沉淀日期**：2026-07-21 09:10 CST
> **所属族系**：L-49 cron/cron-like 运维族（7-15 → 7-21 扩展到第 7 层）
> **可执行性**：✅ 含 3 条铁律 + 3 条 checklist + 端到端验证脚本

---

## 1️⃣ 背景

INC-2026-07-21-001 揭穿 4 层根因：
1. HTTPS Personal Access Token 失效
2. push 失败 = silent failure（只 log 不告警）
3. cron 上下文无 ssh-agent
4. post-commit 钩子也用同套失败路径

任何 cron/git 自动化场景都通用，**不只是 Wiki**。

---

## 2️⃣ 3 条铁律（必背）

### 铁律 1：凭证策略——HTTPS PAT 严禁用于自动 push

```bash
# ❌ 错（PAT 会过期，失效就静默失败）
git remote add origin https://ghp_xxxx@github.com/owner/repo.git

# ✅ 对（SSH key 永久有效，paimon key 无 passphrase）
git remote add origin git@github.com:owner/repo.git
```

**为什么 PAT 必弃**：
- GitHub 强制 90 天滚转 → 必然过期
- Token 出现在 URL 里 → log/进程列表泄漏风险
- 失效时不报错，只 `Device not configured`
- macOS keychain 在 cron 上下文不可访问

### 铁律 2：silent failure 必加告警 + exit 非零

```bash
# ❌ 错（swallow 失败）
if git push ... 2>&1 | tee -a "$LOG"; then
    log "✅ 成功"
else
    log "⚠️ 失败（稍后重试）"  # ← swallow
fi

# ✅ 对（失败告警 + exit 1）
push_output=$(GIT_TERMINAL_PROMPT=0 git push ... 2>&1)
push_exit=$?
if [ $push_exit -eq 0 ]; then
    log "✅ 成功"
else
    log "🔴 失败（exit=$push_exit）"
    "$FEISHU_BIN" im +messages-send --as user \
      --user-id ou_xxx --markdown "🔴 [告警] push 失败: $push_output"
    exit 1  # ← cron 能感知
fi
```

**3 个必做**：
1. **告警**：飞书推 🔴 消息（不只 log）
2. **退出码**：失败 = exit 1（cron 才能 fail-fast）
3. **包含 ahead 数**：让用户知道丢了几个 commit

### 铁律 3：cron 上下文 SSH 必显式 `GIT_SSH_COMMAND`

```bash
# ❌ 错（依赖 ssh-agent，cron 上下文不可靠）
# 仅在 .ssh/config 写 Host github.com → IdentityFile

# ✅ 对（强制指定 key + 绕过 agent）
export GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_paimon \
  -o IdentitiesOnly=yes \
  -o StrictHostKeyChecking=no"
```

**为什么 cron 上下文 SSH 易踩坑**：
- macOS launchd 持久化 ssh-agent 不在 `gui/501` domain
- OpenClaw cron 用 `sh -lc` 启动 → `SSH_AUTH_SOCK` 不继承
- 即便 .ssh/config 写了 IdentityFile，agent 不可达时仍可能 fallback 失败

---

## 3️⃣ 迁移 checklist（3 类 git 仓库通用）

| 步骤 | 命令 | 验证 |
|:---:|:---|:---:|
| 1 | `ssh -T git@github.com` 测连通 | 应返回 `Hi <user>!` |
| 2 | `ssh-keygen -y -f ~/.ssh/<key>` 验 passphrase | 不要求输入 = OK |
| 3 | `git remote set-url origin git@github.com:.../repo.git` 改 URL | `git config --get remote.origin.url` |
| 4 | `git push` 测一次 | 成功且 ahead/behind 归零 |
| 5 | 改脚本加 `GIT_SSH_COMMAND` export | `bash -n` 语法 OK |
| 6 | 改脚本 push 失败加飞书告警 | 模拟一次失败验证 |
| 7 | 端到端跑一次无变更场景 | log 显示"无变更退出" |
| 8 | 等下一个 cron tick 实跑 | log 显示 push ✅ |

---

## 4️⃣ 端到端验证脚本（5min 自检）

```bash
# 1. 远程 URL 是不是 SSH
git -C <repo> config --get remote.origin.url | grep "^git@github.com" || echo "❌ 仍是 HTTPS"

# 2. ahead/behind 归零
ahead=$(git -C <repo> rev-list --count origin/main..HEAD 2>/dev/null)
behind=$(git -C <repo> rev-list --count HEAD..origin/main 2>/dev/null)
[ "$ahead" = "0" ] && [ "$behind" = "0" ] && echo "✅ 同步" || echo "❌ ahead=$ahead behind=$behind"

# 3. SSH key passphrase 验
ssh-keygen -y -f ~/.ssh/id_ed25519_paimon -P "" >/dev/null 2>&1 && echo "✅ 无 passphrase" || echo "❌ 有 passphrase"

# 4. push dry-run
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_paimon -o IdentitiesOnly=yes" \
  git -C <repo> push --dry-run origin main 2>&1 | tail -3

# 5. 脚本语法
bash -n <cron-script>.sh && echo "✅ 语法 OK"
```

---

## 5️⃣ L-49 族系（7 层 · 7-21 止）

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

## 6️⃣ 复用场景（4 类）

| 场景 | 复用方式 |
|:---|:---|
| **新建 cron 自动 push 任务** | 先 SSH 验 + GIT_SSH_COMMAND export + 失败告警 3 件套 |
| **现有 cron 改 HTTPS → SSH** | checklist 8 步全跑 |
| **manual commit + 钩子** | 同步改 post-commit 钩子（不在本次 INC 范围） |
| **跨设备** | 把 paimon SSH key 复制到新设备，`.ssh/config` 同步 |

---

*🕵️ 尼克·弗瑞 · 神盾局局长 · 2026-07-21 09:10 CST · L-49.10 治本 · 3 条铁律 + 8 步 checklist + 5min 自检*

---

## 7️⃣ 7-21 09:17 CST 闭环追加（3 项全做验证）

### 异步 vs 同步 push 选型（hook 场景）

| 模式 | 优点 | 缺点 | 结论 |
|:---|:---|:---|:---:|
| **async（& 后台）**| 不阻塞 commit | wait $pid 不可靠 · PID 太快启动时 bash 返回 127 误报 | ❌ |
| **sync（直接 push）**| 拿真实退出码 · 告警精确 | commit 后等 1-3s（可接受）| ✅ |

**铁律 4（新增）**：post-commit 钩子必须同步 push，不能用 async `wait`

### coreutils 兜底（#2 副作用澄清）
- `brew install coreutils` 装 `gtimeout` 是正确预防
- 但**当前钩子用不上**（已改同步）
- 保留作为"以后 push 卡死兜底"基础设施
- 同步 push 偶发卡死时（极少见），可改用 `gtimeout 30 git push` 强制超时

### sunday_cron_health_check.py 集成（#3）
- 新增 `check_l49_10_git_push_health()` · 4 项铁律自动检查
- 7-19 22:00 周日 cron 自动跑实测
- 故障案例：ahead > 5 = 🔴（INC-2026-07-21-001 触发线）

### L-49 族系扩展到 8 层（7-21 止）
```
L-49     cron edit 必看 argv 完整 JSON          (INC-002)
L-49.5   argv 必查脚本路径存在性                 (INC-005)
L-49.6   cron cleanup 决策树（4 类 + 4 动作）    (INC-006)
L-49.7   INC 报告必加 enabled/disabled tag 区分 (INC-007)
L-49.8   ID 引用必完整（grep 原文 + 长度校验）   (INC-005 补)
L-49.9   脚本路径常量漂移 silent failure 治本   (INC-001 7-20)
L-49.10  Git 凭证 + 静默失败 + cron SSH 上下文  (INC-001 7-21 上午)
L-49.10.1 hook 异步 vs 同步 push 选型 + gtimeout 兜底 (INC-001 7-21 下午) ← NEW
```

🕵️ nick_fury · 2026-07-21 09:17 CST · L-49.10 + L-49.10.1 双层治本
