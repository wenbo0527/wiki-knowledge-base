---
title: inc 2026 07 14 005 c3 sync check implementation
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-15
---

# 🔴 Incident 005: C-3 自检增加 Get 笔记 → Wiki 同步对账检查

| 字段 | 值 |
|:---|:---|
| **ID** | inc_2026-07-14_005 |
| **严重级别** | 🟠 High |
| **状态** | ✅ Closed |
| **发现时间** | 2026-07-14 14:11 |
| **发现者** | nick_fury（INC-004 防复发机制） |
| **负责人** | nick_fury |
| **最后更新** | 2026-07-14 14:15 |

---

## 问题描述

INC-004 揭穿 Get 笔记 → Wiki 50 天静默真空后，需要一个**治本机制**：让 C-3 21:00 cron 自动监控"API 端 vs Wiki 端差异"，而不是依赖"飞书用户主动发现"。

**实现**：在 `scripts/c3_daily_check.py` 加新检查项 C-4，对账 `data/getnote_sync_state.json` 的 synced_note_ids vs Get 笔记 API 端笔记 ID。

## 影响分析

| 维度 | 之前 | 修复后 |
|:---|:---|:---|
| 静默检测能力 | ❌ 无 | ✅ C-3 21:00 自动对账 |
| 检测窗口 | 50 天没发现 | ≤ 24 小时 |
| 报警形式 | 无 | c3_alerts/ 落盘 + 飞书推送 + exit 1 |
| L-32 治本 | ❌ 3 必检无对账 | ✅ 满足"必对账" |

## 修复方案

### C-3 增加 C-4 检查项（5 min）

```python
def check_getnote_wiki_sync():
    """对账 API 端 vs state JSON 的 synced_note_ids"""
    # 1. 加载 .getnote_env
    # 2. 拉 API 端所有笔记 ID (分页)
    # 3. 读 state JSON 的 synced_note_ids
    # 4. diff = api - synced
    # 5. 返回未同步数量

def write_sync_alert(unsynced_ids, api_total, synced_total, reason):
    """同步对账报警文件"""
    # 落盘 c3_alerts/ + 飞书推送

# 在 main() 集成
unsynced_ids, api_total, synced_total, sync_err = check_getnote_wiki_sync()
if len(unsynced_ids) > SYNC_THRESHOLD_UNSYNCED:  # 阈值 3
    alert_path = write_sync_alert(...)
    push_to_feishu(alert_path)
    return 1
```

### 端到端测试

| 场景 | 期望 | 实际 | 结果 |
|:---|:---|:---|:---:|
| 正常（20/20）| exit 0 | exit 0 | ✅ |
| 制造 5 条未同步 | exit 1 + 飞书推送 | ✅ 飞书推送 om_x100b6a6972... | ✅ |
| env 损坏 | 配置报警 | raise + log warn | ✅ |
| state JSON 不存在 | 视为 0 同步 | API=20 synced=0 unsynced=20 → ALERT | ✅ |

### 调整点

| # | 修复 |
|:-:|:---|
| 1 | 顺手修复 `with open(env_file)` (PosixPath 不能直接 open) → `open(env_file, "r")` |
| 2 | 顺手修复 `write_log(new_files, ..., alert_path)` 调用（之前 alert_path PosixPath 会被拼到 log_line，导致 `for line in PosixPath` 错）|
| 3 | 顺手修复 `import json / urllib.request`（c3 之前没引，新检查需要）|

### 防复发：覆盖真问题

```
之前 (50 天静默):
- launchd 6:00 同步脚本静默跑 + error swallow
- 没人监控 API 端 vs Wiki 端 差异
- 7-14 文博主动疑问才揭穿

修复后 (今日上线):
- 任何 > 3 条未同步 → 21:00 自动 ALERT → 飞书推送
- L-32 治本机制："必对账"已实际部署
```

## 关联文档

- **INC-2026-07-14-004**: Get 笔记 → Wiki 同步静默 50 天（根因）
- **Lesson L-32**: 同步脚本 3 必检（不 hardcode / 不 swallow / 必对账）
- ✅ L-32 第 3 项"必对账"**今日实际落地**

## 防失效机制

C-4 检查本身也会 fail，需要监控：
- 飞书推送失败时：c3_alerts/ 落盘 ✅（不依赖飞书）
- API 端 down 时：sync_err 报警并写入 log
- env 配置缺失时：sync_err 写日志不中断

---

## 后续行动

- [x] C-4 检查实现（5 min）
- [x] 端到端 + 异常路径测试
- [x] 飞书推送验证
- [x] 写 INC-005
- [ ] **AGENTS.md §0 修正**：区分"Agent 输出文件"vs"Wiki 沉淀"（INC-003 待办，今晚一起做）
- [ ] **多 KB 路由扩展**：人工智能+WAIC / 产品大神 (INC-004 待办，本周)

---

*Created: 2026-07-14 14:15 | Closed: 2026-07-14 14:15*
*测试通过: 飞书消息 `om_x100b6a6972...` (2026-07-14 14:14)*