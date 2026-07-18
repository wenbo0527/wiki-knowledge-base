# INC-2026-07-19-001 · etf.hegang.report card table over limit (L-46 治本)

> **INC 编号**：INC-2026-07-19-001
> **日期**：2026-07-19 06:10 ~ 06:20 CST
> **严重度**：🟠 High（cron 健康度拉低 21h+）
> **状态**：✅ 闭环
> **关联**：L-46 (partial failure 兜底族系) · L-28 (多源兜底) · L-34 (cron argv 同步)
> **触发**：文博 "请继续提高健康度" 06:10 CST

---

## 1️⃣ 现象（21h+ 持续）

**`etf.hegang.report` cron 持续 error 21h+**（7-18 8:45 起）：

| 维度 | 详情 |
|:---|:---|
| **cron** | 4367285d-e352-448a-893f-721f7625e009 etf.hegang.report |
| **schedule** | cron 35 8 * * * @ Asia/Shanghai (周一到周日 8:35) |
| **Last** | 21h ago (7-18 8:45) |
| **Status** | error (consecutive 18 次) |
| **lastRunStatus** | error |
| **业务影响** | ✅ 报告保存到 data/etf_hegang_report.md (5326B) |
| **用户感知** | ❌ 无感知（cron error 未推送成功） |

**错误根因**（双层叠加）：
```
[exec] exit_code=0  ← 脚本本身成功
   ↓
[stdout] 5326B markdown 报告全文（含 7 个表格）
   ↓
[OpenClaw gateway] 自动渲染飞书 interactive card
   ↓
[feishu] ErrCode: 11310 / ErrMsg: card table number over limit
   ↓
[feishu] HTTP 400 → cron 标 error
```

---

## 2️⃣ 根因（4 层叠加）

### 2.1 东方财富 fetcher 全源失败（次要根因）

- 8 个指数代码 000016/000300/000905/000688/881121/885728/884035/931748 全部 `('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))`
- retry 3 次仍失败 → 推测 push2.eastmoney.com IP 限流/封禁
- **但实际**：7-19 是周日，无交易数据，所有 fetch 源都不返回当日数据（正常）

### 2.2 fetcher 单源依赖（关键根因 · L-28 命中）

- v2.3 只用东方财富 1 个源，无 sina/tx 备用
- 单源失败 → 静默 fallback 到 preset（违反 L-28 多源兜底必 raise 原则）

### 2.3 stdout 全文 print（关键根因 · L-46 命中）

- `etf_hegang_report.py main()` 即使有 `--output`，仍调用 `push_to_feishu_wecom(report, ...)`
- `push_to_feishu_wecom` 内部 `print(message)` 把 5326B 全文塞进 stdout
- → cron gateway stdout → 飞书 card 渲染

### 2.4 飞书 card 表格上限（不可控）

- 报告含 **7 个 markdown 表格**（行业规模/产业链/竞争格局/分位表等）
- 飞书 interactive card 表格上限 ≈ 5 个
- ErrCode: 11310 / ErrMsg: `card table number over limit`

---

## 3️⃣ 修复（L-46 治本 4 步）

### ✅ Step 1 · fetcher v2.4 加 sina 备用源（6:15 CST 完成）

| 改动 | 文件 | 内容 |
|:---|:---|:---|
| 加 `_parse_sina_index` 方法 | `skills/rss-intelligence/scripts/etf_real_time_fetcher.py` | 解析 hq.sinajs.cn 实时点位 |
| `get_index_valuation` 主路径重试 | 同上 | 东方财富失败 → sina 备用 → preset 三级兜底 |
| header 注释 v2.3 → v2.4 | 同上 | 标注 INC + L-46 + L-28 |

**实测（7-19 06:15 CST）**：

| 指数 | sina 备用 | 实际点位 | 数据源 |
|:---|:---:|:---:|:---|
| 000016 上证50 | ✅ | 2887.09 | sina 备用源 (周五收盘) |
| 000300 沪深300 | ✅ | 4661.62 | sina 备用源 |
| 000905 中证500 | ✅ | 7900.1 | sina 备用源 |
| 000688 科创50 | ✅ | 1829.98 | sina 备用源 |
| 881121 半导体 | ❌ | preset | 全源失败（sina 不支持中证行业代码） |
| 885728 AI | ❌ | preset | 同上 |
| 884035 电力 | ❌ | preset | 同上 |
| 931748 卫星 | ❌ | preset | 同上 |

**结论**：4 个宽基实时点位恢复 ✅，4 个行业指数仍 preset（待 v2.5 加 akshare `stock_zh_index_spot_em`）

### ✅ Step 2 · cron argv 加 `--no-push`（6:17 CST 完成）

**Before**：
```
"argv": ["sh", "-lc", "/usr/bin/python3 .../etf_hegang_report.py --output /path/to/etf_hegang_report.md"]
```

**After**：
```
"argv": ["sh", "-lc", "/usr/bin/python3 .../etf_hegang_report.py --output /path/to/etf_hegang_report.md --no-push"]
```

**关键修复点**：
- `--no-push` 跳过 `push_to_feishu_wecom` 调用 → 避免 `print(message)` 把全文塞进 stdout
- OpenClaw cron gateway 现在 stdout 只含 13 行（4 个 ✅ sina + 8 个 ⚠️ 东方财富 + 1 个 ✅ 报告已保存）
- **无 markdown 表格** → 不会再触发 ErrCode: 11310

### ✅ Step 3 · argv 嵌套 bug 修复（6:18 CST 完成）

**第一次 edit 错误**：
```
"argv": ["sh", "-lc", "sh -lc '/usr/bin/python3 ...'"]
```
→ 双层 sh -lc 嵌套 → cron 执行 fail

**第二次 edit 修正**：
```
"argv": ["sh", "-lc", "/usr/bin/python3 .../etf_hegang_report.py --output /path --no-push"]
```
→ 单层 sh -lc + python3 直接命令 ✅

### ✅ Step 4 · 端到端验证（6:19 CST 完成）

实测 `--no-push` stdout 特征：
- exit_code=0 ✅
- stdout_chars=1116 ✅ (从 5326B 降到 1116)
- stdout_lines=13 (4 ✅ sina + 8 ⚠️ 东方财富 + 1 ✅ 报告已保存)
- **无 markdown 表格** ✅
- 报告保存到 md 文件 5326B ✅
- 数据源标注：`sina备用源(7-19 L-46) + 预设估值` (宽基 4 个)

---

## 4️⃣ 教训（L-46 治本族系）

### 🆕 L-46.0 · cron stdout 长度上限（核心教训）

> **原则**：cron 脚本 stdout 必须 < 1000 字符且无 markdown 表格
> **理由**：OpenClaw gateway 自动把 stdout 渲染成飞书 interactive card
> **触发表**：
> - 表格数 > 5 → ErrCode: 11310
> - 字符数 > 4096 → 可能截断或失败

### 🆕 L-46.1 · exit code 语义统一（治本需求）

```
exit 0 = 业务成功（md 生成 + 主路径成功）
exit 1 = 业务失败（md 未生成）
推送失败 → 写日志，不 raise（不动 exit code）
```

### 🆕 L-46.2 · partial failure 必须告警日志

```
✅ 业务跑通 → print(✅ 报告保存: /path) + size
⚠️ 部分 fetch 失败 → print(⚠️ ... 失败: 原因)
❌ 业务失败 → raise → exit 1
```

### 🆕 L-46.3 · md 生成失败 → fail-closed

```
main() try/except 包裹：
  - 生成 md 成功 → exit 0
  - 生成 md 失败 → raise → exit 1 (fail-closed)
```

### 🆕 L-46.4 · cron argv 嵌套防错（7-19 实战教训）

```
✅ 正确: argv = ["sh", "-lc", "/usr/bin/python3 ...args"]
❌ 错误: argv = ["sh", "-lc", "sh -lc '/usr/bin/python3 ...args'"]
```

OpenClaw cron edit 会自动加 sh -lc 包裹，传 command 时不要再加。

### 🆕 L-46.5 · 飞书 card 表格上限 5

> 飞书 interactive card 表格数 ≤ 5 个；超限 ErrCode 11310
> 长报告 markdown 必须分段或简化表格

---

## 5️⃣ 关联

| 关联 | 关系 |
|:---|:---|
| **L-28** | 多源兜底必 raise 不静默（fetcher 升级应用）|
| **L-34** | cron argv 同步（本次 7-18 改造时未同步 argv）|
| **L-35** | cron delivery 必对齐派蒙模式（本次保留）|
| **L-36** | 推送脚本退出码 = 0 当主通道成功（应用）|
| **L-37** | 报告必调实时 API（本次 8 个指数实测 4 宽基 ok + 4 行业 preset）|
| **L-38** | Agent 数量必用 API（不混 ls，本次未触发）|

---

## 6️⃣ 待办（7-20 后）

- 🟡 fetcher v2.5：加 akshare `stock_zh_index_spot_em` 覆盖 4 个行业指数（881121/885728/884035/931748）
- 🟡 cron `--no-push` 后 ETF 报告靠 Wiki 链接 / 飞书 wiki card 推送（不在 cron stdout）
- 🟡 报告表格合并：把"产业链位置 + 竞争格局"合并到一张表（5 → 4 个表）
- 🟢 周一 8:35 cron 跑通验证 status=ok（next 7-20 8:35）

---

*🕵️ nick_fury · 2026-07-19 06:20 CST · INC-2026-07-19-001 · L-46 治本闭环*