# Lesson L-46 · cron stdout 长度 + 飞书 card 表格上限（INC-007 治本）

> **日期**：2026-07-19
> **教训编号**：L-46.0 ~ L-46.5（5 条铁律族系）
> **触发 INC**：INC-2026-07-19-001（etf.hegang.report 持续 error 21h+）
> **状态**：✅ 已应用

---

## L-46 族系（5 条铁律）

### L-46.0 · cron stdout 长度上限（核心）

**原则**：cron 脚本 stdout 必须 < 1000 字符且**无 markdown 表格**

**理由**：OpenClaw gateway 自动把 stdout 渲染成飞书 interactive card

**触发表**：
- 表格数 > 5 → ErrCode: 11310 (`card table number over limit`)
- 字符数 > 4096 → 可能截断或失败
- 含 markdown 标题/列表/代码块 → 渲染异常

**预防**：
```bash
# ✅ 正确：argv 末尾加 --no-push / --quiet
argv = ["sh", "-lc", "python3 .../script.py --output /path --no-push"]

# ✅ 正确：argv 末尾加简短成功消息
argv = ["sh", "-lc", "python3 .../script.py && echo '✅ done'"]

# ❌ 错误：脚本里 print 全文 markdown
```

---

### L-46.1 · exit code 语义统一

```
exit 0 = 业务成功（主路径产物生成）
exit 1 = 业务失败（主路径产物缺失）
推送失败 → 写日志，不 raise（不动 exit code）
```

**理由**：cron 只看 exit code 标 ok/error；推送失败不应拉低 cron 健康度

---

### L-46.2 · partial failure 必须告警日志

```
✅ 业务跑通 → print(✅ 报告保存: /path) + size
⚠️ 部分 fetch 失败 → print(⚠️ ... 失败: 原因) + continue
❌ 业务失败 → raise → exit 1
```

**理由**：用户能看到具体失败点；不静默（L-28）

---

### L-46.3 · md 生成失败 → fail-closed

```
main() 必须有 try/except：
  - 生成 md 成功 → exit 0
  - 生成 md 失败 → raise → exit 1（不要静默退 0）
```

**理由**：业务产物缺失必须 fail-closed；不要让 cron 误标 ok

---

### L-46.4 · cron argv 嵌套防错

```
✅ 正确: argv = ["sh", "-lc", "/usr/bin/python3 ...args"]
❌ 错误: argv = ["sh", "-lc", "sh -lc '/usr/bin/python3 ...args'"]
```

OpenClaw cron edit 自动加 `sh -lc` 包裹，传 `--command` 时**不要再加**。

**实战**：7-19 06:17 第一次 edit 触发嵌套 bug；第二次修正。

---

### L-46.5 · 飞书 interactive card 表格上限 5

> 飞书 card 表格数 ≤ 5 个；超限 ErrCode: 11310

**实战**：etf_hegang_report.md 含 7 个 markdown 表格 → ErrCode: 11310 → cron 标 error 21h+

**预防**：
- 长报告 markdown 必须分段（每段 ≤ 5 表）
- 或简化表格（合并同类表格）

---

## 应用清单（7-19 已应用）

| 应用项 | 状态 |
|:---|:---:|
| etf.hegang.report argv 加 `--no-push` | ✅ 6:17 |
| fetcher v2.4 加 sina 备用源 | ✅ 6:15 |
| argv 嵌套 bug 修复 | ✅ 6:18 |
| 端到端验证 stdout 1116 字符 0 表 | ✅ 6:19 |
| INC-2026-07-19-001 落档 | ✅ 6:20 |
| lesson L-46 落档 | ✅ 6:20 |

---

## 验证时间表

| 时间 | 验证项 |
|:---|:---|
| **周一 7-20 8:35** | etf.hegang.report cron 自动跑通 → status=ok 验证 |
| **周日 7-19 22:00** | nick_cron_health_weekly 首次跑通 → 健康度报告 |
| **下周一 7-20 9:00** | morning·daily 推送验证（双重 grep cron status）|

---

## 关联教训

| 教训 | 关联 |
|:---|:---|
| **L-28** | 多源兜底必 raise 不静默（fetcher v2.4 应用）|
| **L-34** | cron argv 必同步（L-46.4 是 L-34 的补充）|
| **L-35** | cron delivery 对齐派蒙模式（本次保留）|
| **L-36** | 推送脚本退出码 = 0 主通道成功（L-46.1 强化）|

---

*🕵️ nick_fury · 2026-07-19 06:20 CST · L-46 治本族系 · 5 条铁律*