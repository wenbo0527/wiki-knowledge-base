---
title: Lesson 2026 07 18 L-48-5 find mindepth 1
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, 2026-07, L-48, find, rmdir]
date: 2026-07-18
---

# L-48.5: find 必加 `-mindepth 1` 排除目录自身（7-18 实证踩坑）

> **触发**: INC-2026-07-18-003 P1 第一次执行 10/10 SKIP
> **治本**: L-48 trash 安全流程族扩展

## 教训

**错误写法**：
```bash
REAL_SUBDIRS=$(find "$d" -type d 2>/dev/null | wc -l)
# 输出 1（即使目录本身是空的）
```

**正确写法**：
```bash
REAL_SUBDIRS=$(find "$d" -mindepth 1 -type d 2>/dev/null | wc -l)
# 输出 0（真子目录数）
```

## 影响

L-48 三必查全部失效，会误判"空目录非空"，导致 rmdir 全部 SKIP。

## 治本

所有 find 子目录计数场景，必加 `-mindepth 1`。

## 关联

- **INC-2026-07-18-003**: P1 清 10 个意外空目录
- **L-48**（trash 副作用必查目录结构族）
- **L-48.1**: `trash <dir>/*` 后必 ls -la 验证目录
- **L-48.2**: 清理动作前必 find 空目录
- **L-48.3**: trash 验证必含 3 项（文件没了 / 目录还在 / 子目录还在）
- **L-48.4**: Wiki process/* 反向验证 cron

🕵️ 尼克·弗瑞 · 2026-07-18 09:59 CST · L-48.5 闭环
