# Lesson: Lark-CLI 在 Launchd 上下文推送失败的预防与恢复

> **触发 INC**: INC-2026-07-02-001
> **发现时间**: 2026-07-02 08:50（文博主动询问"今天的推送呢"）
> **闭环时间**: 2026-07-02 09:00（7 分钟）
> **沉淀时间**: 2026-07-02 09:05

---

## 现象

Launchd 触发的 `lark-cli im +messages-send` 报 `config/not_configured`，但手动 shell 跑同一条命令完全正常。

---

## 根因

**三层叠加**:

| 层 | 现象 | 根本 |
|:---:|:---|:---|
| **进程级** | launchd 跑 lark-cli 报 not_configured | launchd 进程的 pwd / 某些 env 变量没在 lark-cli config 搜索路径 |
| **时间级** | `tokenStatus=needs_refresh` 但自动 refresh 没触发 | lark-cli v1.0.59 在 launchd 上下文直接报错，没走 refresh 分支 |
| **文件级** | lark-cli v1.0.59 已知问题 | v1.0.61 提示可升级（未验证是否彻底修复） |

---

## 教训（L-19 / L-20 / L-21）

### L-19: launchd 上下文里的 lark-cli 是"薛定谔的配置"

**原则**: 任何 launchd 触发的脚本调 lark-cli，**必须**通过 wrapper（`scripts/lib/lark_cli_wrapper.py`），**不能**直接 `subprocess.run(["lark-cli", ...])`。

**反例**:
```python
subprocess.run(["/opt/homebrew/bin/lark-cli", "im", "+messages-send", "--as", "user", ...])
# launchd 下跑会报 config/not_configured
```

**正例**:
```python
from lib.lark_cli_wrapper import push_im
ok, info = push_im(user_id, markdown, idempotency_key)
# wrapper 内部显式 env={HOME=/Users/wenbo, PATH=完整, LANG=en_US.UTF-8} + cwd=/Users/wenbo
```

**复用场景**: 所有 Nick 的 launchd plist 脚本（22 个）只要调 lark-cli 都用 wrapper。

---

### L-20: 监督层 ≠ 推送前自检（C-3 修订）

**原 C-3**: 每日 21:00 cron 扫描"写" vs "已完成" 比 < 80% 即告警。

**L-20 修订**: 21:00 是日终审计，**07:15 投资日报 / 08:35 技术日报 是当日首次推送窗口**，如果失败到 21:00 才被发现 = **13h 真空**。

**预防**:
- 🟡 **加 07:00 preflight cron**: 跑 `lark_cli_wrapper.preflight()`，失败时给文博发飞书告警
- 🟡 **preflight 失败时 webchat 兜底**: 让脚本在 lark-cli 不可用时，自动切换到 webchat 通知

---

### L-21: 用户主动询问 = 兜底信号

**现象**: 文博 8:50 问"今天的推送呢" → 才发现 19.7h 推送失败。

**原则**: 用户主动询问 = 系统已有信号没告警 = **告警链路缺失** 的证据。

**预防**:
- 当用户问"X 呢"时，立即触发 X 相关系统的全链路审计
- 把"被问到次数"作为告警链路健康度的指标（被问 1 次 = 1 个缺失告警）

---

## 验证清单（写新 launchd 推送脚本前必过）

- [ ] **L-17**: 写脚本前 read 3 行 lark-cli 输出示例（确认响应格式）
- [ ] **L-15**: 写完后端到端验证：preflight ✅ + 实际推送 ✅ + Wiki 落盘 ✅
- [ ] **L-19**: 调 lark-cli 必须用 `lark_cli_wrapper`，不直接 subprocess
- [ ] **L-20**: 加 preflight 步骤，失败时 WARN 但不阻塞 Wiki 兜底
- [ ] **L-21**: 加 preflight 失败告警链路（飞书 / webchat / cron 7:00 自检）

---

## 复用代码

**scripts/lib/lark_cli_wrapper.py**（4.9KB · 已沉淀）:
- `preflight()` → 检查 lark-cli auth status + scope
- `push_im(user_id, markdown, idempotency_key, as_user=True)` → 推送飞书消息

**调用模板**:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.lark_cli_wrapper import push_im as lark_push_im, preflight as lark_preflight

# main() 开头
preflight_ok, preflight_msg = lark_preflight()
write_log("INFO", f"lark-cli preflight: {'✅' if preflight_ok else '❌'} {preflight_msg}")

# 推送时
ok, info = lark_push_im(
    user_id=WENBO_USER_ID,
    markdown=summary,
    idempotency_key=f"xxx_{today_str.replace('-', '')}",
)
```

---

## 关联

- INC-2026-07-02-001（本次事件）
- L-4（监督层未上线临时自检）
- L-15（写脚本必端到端验证）
- L-16（修一类必 grep 全集）— **本次 22 个 plist 都需要验证是否同样使用 lark-cli**
- L-18（lark-cli setup 必加 send_as_user scope）
- TOOLS.md §3.1（lark-cli 配置步骤）

---

*沉淀者: 尼克·弗瑞 🕵️*
*验证状态: ✅ 08:55 end-to-end 跑通（preflight ✅ + lark-cli ✅ + wiki ✅）*
*下次审计: 7-3 07:15（明早首次推送窗口验证修复）*