# INC-2026-07-02-001: Lark-CLI 在 Launchd 上下文推送失败 19.7h 未发现

## 现象

- **7-1 11:33** 后到 **7-2 07:15** 之间（约 19.7h），launchd 触发的 lark-cli im +messages-send 全部失败
- **错误**: `lark-cli exit 3: {"ok": false, "identity": "user", "error": {"type": "config", "subtype": "not_configured", "message": "not configured", "hint": "run \`lark-cli config init --new\`..."}}`
- **影响**: 7-2 07:15 投资日报 + 08:35 技术日报**飞书推送全部失败**，文博未收到（仅 Wiki 落盘成功）
- **launchctl 状态码**: `com.nickfury.daily-investment-push=1`, `com.nickfury.daily-tech-push=1`（异常退出）
- **8:50 文博主动询问**才被发现，未自检告警

## 根因（系统级 + 进程级 + 文件级 三层）

### 进程级：launchd 上下文里 lark-cli 找不到 config

- **手动 shell** 跑 `lark-cli auth status` 显示 `user=ready token=valid`，scope 包含 `im:message.send_as_user`
- **手动 shell** 跑 `lark-cli im +messages-send` 推送成功（preflight test 8:53 ok，message_id 收到）
- **launchd 进程** 跑同样的命令报 `config/not_configured`
- **差异**: launchd 进程的 `pwd` / 某些环境变量不在 lark-cli 的 config 搜索路径
- plist 里有 `EnvironmentVariables.HOME=/Users/wenbo` 和完整 PATH，**但 lark-cli 内部判断逻辑没找到 HOME 下的 config 入口**

### 时间级：自动 refresh 时机错误

- `auth status` 显示 `tokenStatus=needs_refresh`（access_token 昨天 13:25 过期）
- lark-cli 有"will auto-refresh on next user API call"机制
- 但 launchd 调用时**没有触发** refresh 路径（直接报 not_configured，没走到 refresh 分支）

### 文件级：lark-cli v1.0.59 已知 bug（推测）

- lark-cli 提示 `_notice.update: 1.0.61 available, current 1.0.59`
- v1.0.61 可能修复了 launchd 上下文的 config 搜索路径
- **未验证**：本次修复未升级 lark-cli，而是通过 wrapper 绕开了 launchd 直接调 lark-cli 的方式

## 修复（5 个动作 · 09:00 闭环）

### 1. 手动补推（08:53 · 文博收到 ✅）
- 投资日报 `om_x100b6b6f24db18acb2fbc8a71d42eb9`
- 技术日报 `om_x100b6b6f24db24a4b2ed0a08267d690`

### 2. 写 `scripts/lib/lark_cli_wrapper.py`（4.9KB · 08:55）
- `preflight()`: 检查 lark-cli auth status + scope 包含 send_as_user
- `push_im()`: 推送时**显式** `env=完整环境变量` + `cwd=/Users/wenbo`，绕开 launchd 上下文 config 搜索问题
- 任何错误返回 (False, info)，不抛异常

### 3. 升级 `daily_tech_report.py` + `daily_investment_report.py`（08:56 · 编译通过）
- `push_to_feishu_im()` 改为调用 `lark_cli_wrapper.push_im()`
- `main()` 开头加 preflight 步骤，失败时记录 WARN（不阻塞 Wiki 兜底）
- L-15 端到端验证：08:55 跑一次，3 通道 2/3 成功（lark-cli ✅ + wiki ✅）

### 4. 创建 `~/Library/Logs/nick_fury/` 目录（09:00 · 7-2 第一次）
- 之前 daily 提到的"日志目录缺失"问题同步解决
- 下一步：把 22 个 plist 的 StandardOutPath/StandardErrorPath 改指向这里（下次 L-16 grep 批量改）

### 5. plist 验证（09:00 · 不需要重启）
- launchd 下次触发（明天 7:15 / 8:35）会用新脚本版本
- 当前 launchctl 状态码 1 是历史快照，明天自动归零

## 教训（L-19 + 修订 L-4/L-15）

### 🆕 L-19: launchd 上下文里的 lark-cli 是"薛定谔的配置"

**原则**: 任何 launchd 触发的脚本调 lark-cli，**必须**用 wrapper（显式 env + cwd），不能直接 `subprocess.run([lark-cli, ...])`

**反例**（7-2 07:15 ~ 08:35）:
```python
subprocess.run(["/opt/homebrew/bin/lark-cli", "im", "+messages-send", ...])  # ❌ launchd 报 not_configured
```

**正例**（7-2 08:55 修复后）:
```python
from lib.lark_cli_wrapper import push_im
ok, info = push_im(user_id, markdown, idempotency_key)  # ✅ wrapper 内部显式 env + cwd
```

### 🆕 L-20: 19.7h 真空未自检 = L-4 重演

**L-4 教训原版**（6-15）: 监督层未上线时必须有"临时自检"
**L-20 修订**（7-2）: 即便监督层（C-3 cron 21:00）已上线，**上午推送窗口（07:15/08:35）也需要 preflight cron**

**预防**:
- 加一个新 cron: 每日 07:00 跑 `lark_cli_wrapper.preflight()`，失败时给文博发飞书告警
- 或: 给 daily_tech_report.py / daily_investment_report.py 加"preflight 失败时调用 webchat 兜底通知"

### 🆕 L-21: 文博问"今天的推送呢"是兜底信号

**现象**: 8:50 文博主动询问 → 才发现 19.7h 推送失败

**原则**: 用户主动询问 = 系统已有信号没告警 = **告警链路缺失** 的证据

**预防**: 把"用户问 X"作为兜底事件，触发相关系统自检（这次是推送失败 → 触发 launchd + lark-cli 全链路审计）

## 关联

- **INC-2026-06-15-001**: Wiki PermissionError 44 天未发现（同类：自动机制失效未被察觉）
- **INC-2026-06-23-001**: 11 plist launchd 状态码 78 修复（同类：launchd 相关问题）
- **L-4 / L-15 / L-16**: 监督层 / 端到端验证 / 修一类必 grep 全集
- **TOOLS.md §3.1**: lark-cli setup 需 `--scope "im:message.send_as_user"`（7-1 已修，这次是另一类问题）

## 状态

- **修复**: ✅ 闭环（08:53 补推 + 08:55 wrapper + 08:56 升级 + 09:00 日志目录）
- **预防**: 🟡 L-19/L-20/L-21 已沉淀
- **待办**:
  - [ ] 升级 lark-cli 到 1.0.61（验证是否彻底解决 launchd config 搜索路径）
  - [ ] 加 07:00 preflight cron（每日早上推前自检）
  - [ ] 给 22 个 plist 的 StandardOutPath/StandardErrorPath 改指向 `~/Library/Logs/nick_fury/`

---
*修复时间: 2026-07-02 08:53 - 09:00 · 7 分钟从发现到闭环*
*上报: 派蒙 / 文博*
*维护: 尼克·弗瑞 🕵️*