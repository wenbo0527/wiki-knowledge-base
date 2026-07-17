---
title: inc 2026 07 17 002 etf hegang argv hardcoded date
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-17
---

# INC-2026-07-17-002: etf.hegang cron argv 硬编码 `--date 2026-06-26` → 报告日期永远 6-26

## 现象

- **触发时间**: 2026-07-16 08:35 CST（cron 第一次以 hardcoded 跑，7-16 早 08:35 cron status=error 持续 24h）
- **发现时间**: 2026-07-17 08:50 CST（用户决策 B 完整修复时深挖 argv）
- **影响 cron**: `4367285d-e352-448a-893f-721f7625e009 etf.hegang.report` (cron 35 8 * * * Asia/Shanghai)
- **持续时长**: 24h（7-16 08:35 → 7-17 08:52 修复）
- **错误实证**:

```
lastDiagnostics.summary:
"✅ 报告已保存: .../data/etf_hegang_report.md
🕵️ ETF 何刚框架独立评估 | 2026-06-26  ← 日期永远 6-26
> v2 双消息结构（2026-06-26 落地）
> 主线消息不含 ETF，本消息为独立 ETF 评估"
```

**关键发现**：报告内容里 ETF 数据是 **6-26 的旧数据**（来源 akshare 当时快照），但**报告推送目标时间**是当天——文博每天早上 8:35 收到的 ETF 报告都是 6-26 内容。

## 根因

**cron argv 硬编码日期参数**：

```bash
# argv 实际值（cron 9367285d）
sh -lc "/usr/bin/python3 .../etf_hegang_report.py \
  --date 2026-06-26 \                          ← 硬编码！
  --output .../data/etf_hegang_report.md"
```

**根因分析**：
- 这个 cron 是 **7-16 启用**（7-1 改造 + 7-2 起 argv 未对齐？需要查 history，但很可能 6-26 当天手动测试后 argv 没去 `--date`）
- `etf_hegang_report.py` line 51 用法：`[--date 2026-06-25]` 是**可选参数**，不传时脚本内部默认当天（`datetime.now()`）
- argv 加 `--date 2026-06-26` 之后脚本就被钉死在 6-26
- **L-49 不存在**（cron argv 必看完整 JSON）—— 当时 INC-2026-07-15-001 只 grep `argv` 是否有错，未 grep argv 内具体参数是否合理

**status=error 实际原因**：lastDiagnostics 是 stdout 内容（含 6-26 报告全文），但 lastRunStatus=error——**真正的 error 信息被 stdout 覆盖未看到**（很可能 lark-cli 推送失败、文件权限问题、或 stdout 太长被截断的副作用）。

## 修复（5min · 8:52 完成）

```bash
# F4. cron edit 去硬编码 --date
openclaw cron edit 4367285d-e352-448a-893f-721f7625e009 \
  --command "/usr/bin/python3 .../skills/rss-intelligence/scripts/etf_hegang_report.py \
  --output /Users/wenbo/.openclaw/workspace/agents/nick_fury/data/etf_hegang_report.md"

# F5. 手动验证（不带 --date）
cd /Users/wenbo/.openclaw/workspace/agents/nick_fury
/usr/bin/python3 skills/rss-intelligence/scripts/etf_hegang_report.py \
  --output data/etf_hegang_report_today.md
# ✅ 报告日期: 2026-07-17（动态）
# 注：wecom 推送 500 错误是 wecom API 自身问题（500 Internal Server Error），
#     不影响 cron 推送 → 飞书通道独立工作
```

**修复后状态**：argv 改为动态日期，cron 下次跑（明早 8:35）会自动用当天日期。

## 教训族 L-49（cron edit 必看 argv 完整 JSON）

| 编号 | 教训 |
|:---|:---|
| **L-49.1** | cron 修必先 `openclaw cron get <id>` 看 argv 完整 JSON（不是只看 schedule name） |
| **L-49.2** | argv 必含 3 项：路径正确性 + 参数语义合理 + 无 hardcoded 时间戳/ID/用户 |
| **L-49.3** | 任何 cron 涉及日期/ID/用户参数必 grep `hardcoded\|fixed\|static`（防退化）|
| **L-49.4** | INC-2026-07-15-001 升级版：原 L-34 "scripts 改造必 grep cron argv" → 升级为 L-49 "cron 修必 4 路全集 + argv 完整" |

## 关联

- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— L-34 原版
- **INC-2026-07-16-004**（Get笔记 API 401 真根因）—— 同为"status 表面 ≠ 实质"误判
- **L-49**（新增 · cron edit argv 完整 + hardcoded 检测）
- **cron 4367285d**（明早 7-18 08:35 验证 status=ok + 报告日期动态）