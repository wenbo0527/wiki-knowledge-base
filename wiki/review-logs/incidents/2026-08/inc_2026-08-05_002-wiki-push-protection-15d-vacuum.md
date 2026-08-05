# INC-2026-08-05-002 · Wiki push 阻塞 15 天 = PAT 泄漏到 commit 历史（GH013 治本）

> **数据截止**: 2026-08-05 14:13 CST
> **触发**: 14:00 文博"🔴 [Wiki Hook Push] push 失败" + 14:03 "同意 A"
> **闭环**: 5/6 步完成（识别 + rebase 改写 + push 验证 + 公开仓库扫描），剩 PAT 撤销等用户操作
> **关联**: L-57 族首 · L-49.10 强化 · INC-2026-07-21-001 根治延伸

---

## 1️⃣ 现象

8-5 14:00 文博推送"🔴 [Wiki Hook Push] push 失败"：
- 时间：2026-08-05 09:10:05
- 错误：`GH013: Repository rule violations found for refs/heads/main`
- 命中规则：`Push cannot contain secrets`
- 命中类型：`GitHub Personal Access Token`
- 命中 commit：`31dbf669dcf2f5056a0dbe5eebb60080692b6426`
- 命中文件：`wiki/review-logs/incidents/2026-07/inc_2026-07-21_001-wiki-git-push-fail-61-ahead.md:35`
- 阻塞时长：7-21 至今 **15 天**
- ahead 状态：31 commits 积压

---

## 2️⃣ 根因（5 层）

### 2.1 7-21 INC 写作时把 PAT 写进了 commit
commit 31dbf669 是 7-21 写的 INC-2026-07-21-001 文档，记录当时"凭证策略错误"。**第 35 行原文**：
```
remote URL 形式：`https://***REDACTED***@github.com/wenbo0527/wiki-knowledge-base.git
```
当时为了"完整记录"，把字符串写进了文档 → commit → main 分支。

### 2.2 GitHub Push Protection 触发
GitHub 7-21 之后升级了 Push Protection（默认扫描所有 PAT 字符串）。即使 PAT 已经过期或即将到期，**任何包含 `***REDACTED***` 模式的字符串都可能被拦截**。

### 2.3 后续 30 commits 全部依赖 31dbf669
31dbf669 是 31 ahead 中的最早 commit，所有后续 commits 通过 parent 链引用它。**fix 31dbf669 才能 push 整个 main 分支**。

### 2.4 INC 文档发现的滞后性
INC-2026-07-21-001 当时记录了"push 失败 61 ahead"问题，但**没发现根因是 PAT 泄漏进 commit**。后续每天 cron 跑都失败，但没人深挖。

### 2.5 凭证策略升级不彻底
L-49.10（7-21 写入）已经教"严禁用 HTTPS PAT 推，必须 SSH"，但**没教"历史清理 + 治本循环"**。本次 7-21 至今 15 天没人解决。

---

## 3️⃣ 修复（A 方案 · 14:03 文博拍板）

### 3.1 三件套（REDACTED + rebase + force push）

| 步 | 操作 | 命令 |
|:---:|:---|:---|
| 1 | 备份 main 指针 | `git tag backup-pre-pat-cleanup main` |
| 2 | 改 31dbf669 文档（3 处 PAT 替换为 `***REDACTED***`）| `sed -i '' 's|***REDACTED***|***REDACTED***|g' file` |
| 3 | 自动化 rebase 标记 31dbf669 为 edit | `GIT_SEQUENCE_EDITOR="cp /tmp/rebase-todo.txt" git rebase -i origin/main` |
| 4 | amend commit 31dbf669 → `7889f6a` | `git commit --amend --no-edit` |
| 5 | 二次清理 2 处 PAT 缩写/占位 | `sed -i '' 's|***REDACTED***|***REDACTED***|g'` |
| 6 | 再次 amend → `bc3bd37` | `git commit --amend --no-edit` |
| 7 | rebase --continue（30 commits 重新 base）| `git rebase --continue` |
| 8 | wiki_auto_commit hook 自动 force push | `HOOK [✅ 推送成功] 47e0313..bc3bd37` |

### 3.2 意外发现：L-49.10 同步机制善意生效

**wiki_auto_commit.sh 设计了"HEAD 变更自动 force push"（同步模式 L-49.10 治本）**：
- 我 rebase 改写完 head，`7889f6a` → `bc3bd37`
- hook 自动检测到 HEAD 变更，触发同步 push
- 因为新 history 不含 PAT，**GitHub Push Protection 放行**
- 31 ahead 全部推出去（ahead 0）

**日记**：
```
[2026-08-05 14:12:56] [HOOK] 提交完成，尝试推送（同步模式·L-49.10 治本）...
[2026-08-05 14:13:02] [HOOK] ✅ 推送成功（hook 同步）
```

---

## 4️⃣ 端到端验证（L-15 6 步）

| 步 | 项 | 结果 |
|:---:|:---|:---|
| 1 | GitHub 规则识别（GH013 触发）| ✅ |
| 2 | rebase 改写 31dbf669 历史 | ✅ |
| 3 | hook 同步 force push 成功 | ✅ |
| 4 | 31 ahead 全部 push | ✅ |
| 5 | 公开仓库扫描 0 PAT 暴露 | ✅ |
| 6 | write INC + lessons | ✅ 本文件 |

### 4.1 公开仓库验证

```bash
$ curl -s "https://api.github.com/repos/wenbo0527/wiki-knowledge-base/commits?per_page=100" \
  | python3 -c "..."
暴露扫描: 0 个提交含 PAT 字符串
最近 100 个 commits 全部干净 ✅
```

### 4.2 PAT 暴露范围真相

| 范围 | 状态 |
|:---|:---|
| 本地 main 分支 | 🟡 31dbf669 dangling（reflog 保留 30 天）|
| 公开仓库 origin/main | ✅ **从未暴露**（7-21 至今 push 失败意外保护）|
| GitHub Push Protection | ✅ 主动拦截（即使有人手动 push）|
| 文博本人 GitHub 账户 | 🟡 PAT `***REDACTED***` 仍可能有效（待撤销）|

### 4.3 dangling commit 兜底

```bash
$ git fsck --dangling
dangling tree c3e828cef2e37bc06de3eee992fcafdc76eeb11d

$ git tag -l "backup-pre-pat-cleanup"
backup-pre-pat-cleanup  # → 2bdb0276 最新 main 指针
```

---

## 5️⃣ 教训（L-57 族首 5 子）

| # | 教训 | 落地 |
|:---:|:---|:---|
| **L-57.1** | PAT 永远不能进 commit（无论原因）| 🚨 GitHub 推保护 + 治本循环 |
| **L-57.2** | 历史改写三件套（REDACTED + rebase + force push）| 8-5 14:09 实证 |
| **L-57.3** | 公开仓库 PAT 扫描（api endpoint 验证）| 8-5 14:13 验证 0 暴露 |
| **L-57.4** | L-49.10 同步机制善用（hook 自动 force push）| 8-5 14:13 意外生效 |
| **L-57.5** | reflog 兜底（dangling commit 30 天保留）| backup-pre-pat-cleanup tag |

### 5.1 L-57 与 L-49.10 关系

- **L-49.10**（7-21 写入）：教"严禁 HTTPS PAT 推"、"silent failure 必告警"、"SSH 显式 key"
- **L-57**（8-5 写入）：教"历史清理治本"、"公开仓库扫描"、"hook 同步机制"

**L-49 + L-57 = 完整治本循环**：
- L-49.10 治未病（不让 PAT 进 commit）
- L-57 治已病（PAT 已进 commit 后怎么清理）

### 5.2 INC-2026-07-21-001 根治延伸

7-21 INC 写了"push 失败 61 ahead"但**没发现根因是 PAT 泄漏进 commit**。本次 8-5 闭环：

- 7-21：找到 push 失败，但归因到 "remote URL 形式 PAT 失效"（以为是 PAT 本身过期）
- 8-5：才发现 commit 31dbf669 里有 PAT 字符串（**commit history 里**残留）
- 教训：INC 写作要**深挖历史**，不能只看 log 表面

---

## 6️⃣ 边界守住

| 边界 | 实证 |
|:---|:---|
| **C-1 闭环** | 5 件 write 全部成功（脚本 + INC + lesson + reflog + 备份 tag）|
| **C-2 分段** | INC 5178B 单件 ≤ 边界 |
| **L-31 路径守** | INC/lesson 都在 `review-logs/` 子目录 ✅ |
| **L-37/L-38 报告必实测** | 8-5 14:13 公开仓库 api 扫描 0 PAT 暴露 ✅ |
| **L-49.10 边界守** | 文博拍板 A 后才动手 force push ✅ |
| **L-15 端到端** | 6 步全部通过 ✅ |

---

## 7️⃣ 待办（仍需文博操作）

| # | 项 | 紧急度 | 阻塞 |
|:---:|:---|:---:|:---|
| 1 | **撤销 PAT `***REDACTED***` 在 GitHub Settings** | 🔴 | 无法在这里做 |
| 2 | 清 dangling commit `c3e828ce`（reflog expire 30 天自动）| 🟢 | 时间等待 |
| 3 | 改 `wiki_auto_commit.sh` 加 PAT 字符串扫描（治本）| 🟡 | 等 L-57.1 治本 |
| 4 | 评估是否清 `backup-pre-pat-cleanup` tag | 🟢 | 等 PR 验收 |

---

## 8️⃣ 验证窗口（8-5 → 8-12）

| 节点 | 期望 | 状态 |
|:---|:---|:---:|
| 8-5 14:13 | rebase + hook 同步 push 成功 | ✅ |
| 8-5 14:14 | 公开仓库 0 PAT 暴露 | ✅ |
| 8-5 14:00+ | 文博撤销 PAT | ⏳ 等操作 |
| 8-12 周日 | cron_argv_watchdog 跑 | ⏳ 7d 后 |
| 9-5 | dangling commit reflog expire | ⏳ 30d 后 |

---

🕵️ nick_fury · 2026-08-05 14:13 CST · INC-2026-08-05-002 闭环 · L-57 族首 · Wiki push 阻塞 15 天治本 · force push + 历史改写三件套 · 公开仓库 0 PAT 暴露 · L-49.10 同步机制意外生效 · 5 子教训入族 · 边界守住 6 项
