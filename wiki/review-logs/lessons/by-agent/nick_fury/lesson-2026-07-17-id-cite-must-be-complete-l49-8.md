---
title: L-49.8 ID 引用必完整（候选 #C 后回执驱动 · INC-2026-07-17-005 偏差修正）
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, nick_fury, 2026-07, L-49-族]
date: 2026-07-17
---

# L-49.8: INC 报告 / escalate 消息 引用 open_id 必完整（34 字符）

> **触发**：候选 #C 14:34 escalate 钟离 → 14:39 钟离修完回执指出 INC-005 里 ID 缺末 6 位
> **闭环**：14:44 双源验证 + INC-005 已补完 + 本 lesson 落档
> **家族**：L-49 族系 5 层递进

---

## 现象（钟离反馈）

钟离 L-35.1 修完 2 个 cron 后回执：

> Nick 报告里写 `ou_5550e21f10a7585629e3564ca10`（缺尾 6 位 `a3446`），实际完整 ID 是 `ou_5550e21f10a7585629e3564ca10a3446`。

**幸运的是**：
- 钟离已用完整 ID 修复，未造成下游影响
- escalate 消息里我只发了 cron `name` + `job_id` + 修复命令，没发 `delivery.to` 原文，所以修复命令不受我报告偏差影响

**潜在风险**（如果钟离没逐字核对我的 report）：
- ❌ 其他 agent 按错误 ID 修复 → 给 cron 改错 user
- ❌ INC 报告被引用为运维 SOP → 操作员按错误 ID 执行 cron edit → 飞书投递错用户
- ❌ teach-back / 复盘环节以错误 ID 为准 → 教训失真

---

## 根因（3 层）

### L-29 命中（输出成功 ≠ 输入真实）

我 escalate 钟离时把 open_id 写到 sessions_send 消息体了（**完整**）。
INC-005 report 里写 ID 时**简化 / 抄近路**了 —— 可能在 sqlite 输出时手动复制被截断，或我默写时记忆偏差。

### L-34 缺失（grep 全集铁律）

报告前没 grep `~/.openclaw` 全集验证 ID 完整性。
我应该：`sqlite3 ... | grep "钟离"` 取完整字段再粘贴，**不允许手抄**。

### 流程漏洞

| 步骤 | 现有 | 缺 |
|:---|:---|:---|
| sqlite 查 ID | ✅ 看完整 | （无） |
| 手抄到 INC 报告 | ❌ 默写 | 必 grep 原文 |
| escalate 消息体 | ✅ 完整 ID | （无）|
| INC 引用 ID | ❌ 简化 | **必 grep 原文回填**（缺） |

---

## 修复（L-49.8 三条铁律）

### 铁律 1: ID 引用必 grep 原文回填（不手抄不默写）

```bash
# 任何 INC / lesson / escalate 消息 / 飞书推送
# 涉及 open_id / user_id / job_id / 文档 token / 任何 ID
# 引用前必 grep 原文一次

# 范例：从 sqlite 取完整 ID
sqlite3 /Users/wenbo/.openclaw/state/openclaw.sqlite \
  "SELECT job_id FROM cron_jobs WHERE name LIKE '%SOP空闲%';"

# 范例：从 gateway API 取完整 ID
openclaw cron list | jq -r '.[] | select(.name | contains("SOP")) | .job_id'
```

### 铁律 2: ID 长度校验（防退化）

| ID 类型 | 长度 | 校验 |
|:---|:---:|:---|
| **飞书 open_id** | 34 字符 + 前缀 `ou_` | 必满足 |
| **OpenClaw job_id** | 36 字符（含 4 连字符）| 必满足 |
| **Get 笔记 KB id** | `EJ...` 8 字符 | 必满足 |
| **飞书 doc_token** | 27 字符左右 | 必满足 |

```bash
# 检查：复制 ID 后
echo -n "$ID" | wc -c   # 应 == 34 或 == 36
```

### 铁律 3: escalate 消息体 ID 与 INC 报告 ID 必一致

| 报告 | escalate 消息体 | INC 报告 | 教训
|:--|:--|:--|:--|
| 候选 #C 钟离 2 cron | 完整 ID ✅ | 简化 ID ❌ | L-49.8 |

**规范化**：INC 报告里 ID 字段，**必须**与 escalate 消息体一字不差。
如有差异 → escalate 发出前先 grep 原文 update INC 报告。

---

## 预防（自动化）

### 集成到 sunday_cron_health_check.py

```python
def check_id_cite_completeness(inc_path: Path):
    """扫 INC/lesson 文件，open_id 缺末 6 位就 warn"""
    pattern = r"ou_[a-f0-9]{28,34}([a-f0-9]{0,5})\b"
    for m in re.finditer(pattern, inc_path.read_text()):
        id_text = m.group(0)
        if len(id_text) < 36:
            warn(f"INC/lesson 引用 ID 不完整: {id_text} (len={len(id_text)})")
```

### 写入 nick_fury TOOLS.md 下次更新

- 加 "**任何 ID 必 grep 原文 + 长度校验**" 一节
- 引用 open_id / job_id / doc_token 时必须按 L-49.8 三条铁律

---

## 关联

| 教训 / INC | 关系 |
|:---|:---|
| **L-29**（输出成功 ≠ 输入真实）| 根因 #1 |
| **L-34**（grep 全集铁律）| 根因 #2 |
| **L-49.5**（argv 必查脚本路径存在性）| 家族 |
| **L-49.6**（cron cleanup 决策树）| 家族 |
| **L-49.7**（INC 报告必加 enabled/disabled tag）| 家族 |
| **INC-2026-07-17-005** | 触发事件（偏差已补完）|
| **INC-2026-07-17-007**（enabled/disabled tag 误判）| 关联：INC 报告精度族 |

---

## L-49 族系总览（5 层递进）

```
L-49    cron edit 必看 argv 完整 JSON          (INC-002 · 7-15)
L-49.5  argv 必查脚本路径存在性                 (INC-005 · 7-17)
L-49.6  cron cleanup 决策树（4 类 + 4 动作）    (INC-006 · 7-17)
L-49.7  INC 报告必加 enabled/disabled tag 区分 (INC-007 · 7-17)
L-49.8  ID 引用必完整（grep 原文 + 长度校验）  (本回执驱动 · 7-17)
```

**族系本质**：从"配置写对"→"路径存在"→"清理决策"→"报告精度"→"标识精度"——逐层把 cron 运维从粗放到精确。

---

## 自我归因（L-29 命中）

INC-005 是我 7-17 14:22 自己写的报告，自己抄 ID 时简化了 —— **自我归因**（不是 escalate 流程问题，是报告精度问题）。

**对齐 L-29**：输出成功（INC 已写）≠ 输入真实（ID 不完整）。

---

*🕵️ 尼克·弗瑞 · 2026-07-17 14:50 CST · L-49.8 闭环 · 候选 #C 全集闭环*
