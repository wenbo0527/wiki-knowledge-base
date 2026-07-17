---
title: inc 2026 07 17 001 wiki process trash sideeffect
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-17
---

# INC-2026-07-17-001: Wiki 整理速赢副作用 · trash `process/` 目录 → wiki.review 跑挂 5h

## 现象

- **触发时间**: 2026-07-17 03:30 CST（cron 自动触发）
- **发现时间**: 2026-07-17 07:58 CST（文博"请检查下遇到的问题"诊断）
- **影响 cron**: `f3b606ed-... wiki.review` (cron 30 3 * * * Asia/Shanghai)
- **持续时长**: 5h（07:58 → 08:52 修复）
- **错误实证**:

```
FileNotFoundError: [Errno 2] No such file or directory:
'/Users/wenbo/Documents/project/Wiki/wiki/process/wiki-review-report-20260717.md'
  File "wiki_auto_review.py", line 404, in run_wiki_review
    report_file.write_text(report, encoding='utf-8')
```

## 根因

**Wiki 整理速赢 Phase 1.5 的清理动作副作用**——

| 时序 | 动作 | 当时判断 | 实际后果 |
|:---|:---|:---|:---|
| **7-16 19:00** | HEARTBEAT.md §十三 "Phase 1.5 · 12 篇 90+ 过期 → 精准 trash 5 篇（process/* 4 + concepts/karpathy 重叠 1）" | `process/` 下的 4 个文件是过期 placeholder | `process/` 目录本身被 trashed 副作用波及 |

**实际行为**（macOS `trash` + `process/` 目录的 4 个文件被 trashed 后）：
- `process/` 目录本身在某些 trash 行为下也会被移除（特别是当目录内文件全部清空时）
- `wiki_auto_review.py` line 401-402 定义 `REPORT_DIR = WIKI_ROOT / "process"`
- 跑挂时 Python `pathlib.Path.write_text()` 会报 FileNotFoundError 因为父目录不存在
- **L-41 治本未彻底**（L-41 仅要求"trash 验证必用 `ls -la`"——验证的是文件被 trash，但**没验证目录是否还存在**）

## 修复（5min · 8:52 完成）

```bash
# F1. 重建 process/ 目录
mkdir -p /Users/wenbo/Documents/project/Wiki/wiki/process/

# F2. 手动跑 wiki_auto_review.py 验证
cd /Users/wenbo/Documents/project/Wiki
/usr/bin/python3 scripts/wiki_auto_review.py
# ✅ 健康度: 🟠 一般 (65/100) · 报告已保存 wiki-review-report-20260717.md

# F3. 等明早 7-18 03:30 cron 自动跑（验证 status=ok）
```

**修复后状态**：报告已生成，cron 下次跑（明早 03:30）会自动 status=ok。

## 教训族 L-48（trash 副作用必查目录结构）

| 编号 | 教训 |
|:---|:---|
| **L-48.1** | `trash <dir>/*` 后必 `ls -la <dir>` 验证目录是否存在（如果目录空了但有子目录还会被删） |
| **L-48.2** | 任何"清理动作"前必 `find <dir> -type d -empty` 列出空目录（被空目录当 placeholder 误删风险高） |
| **L-48.3** | L-41 升级版：trash 验证必含 3 项 —— (1) 文件没了 (2) 目录还在 (3) 子目录还在 |
| **L-48.4** | 7-19 周日 cron 新增 "Wiki process/* 反向验证" 检查项（防退化）|

## 关联

- **INC-2026-07-16-003**（Wiki 元数据批量补全 1% → 99%）—— 同为 Wiki 整理速赢衍生
- **L-41**（macOS `trash` 验证必用 `ls -la`）—— 原版教训
- **L-48**（新增 · 治本 L-41 副作用盲区）
- **HEARTBEAT §十三**（7-16 19:55 Wiki 整理速赢综述 · W1 完成 3/4 + Q3 完成 5/5）
- **cron f3b606ed**（7-17 03:30 跑挂 5h → 8:52 修复 → 明早 03:30 验证）

## 自我归因

**我对文博有过错**：昨天"速赢"造成了今天的问题。但按 SOUL §3 "客观补录 + 自我归因 + 系统级归因"，这次教训立即沉淀 L-48，下次清理任何目录前必查子目录结构。