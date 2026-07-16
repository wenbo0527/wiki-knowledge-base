---
title: inc 2026 07 15 005 strategic 3 kb sync
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-15
---

# INC-2026-07-15-005: 战略 3 KB 同步（文博 AI 转型 + 快刀青衣 + 2026 WAIC）

> **揭穿**: 7-15 14:16 文博指定战略 3 KB（印象笔记不需要）  
> **新发现**: 真 2026 WAIC 是 `JawjeBlY`（487 笔记）· v1.0 备份的 `9YerORB0` "人工智能+WAIC" 是 2025 旧版  
> **13:50 闭环**: 战略 3 KB 全部扩到 KB_ROUTING + KB_LIST

---

## 现象

7-15 10:55 路线图阶段 3 列"Get 笔记 KB 战略 4 同步"包括：印象笔记 2196 + 文博 AI 转型 132 + 数字社区 183 + AI 实践日志 504。

7-15 14:16 文博拍板：**印象笔记不需要**，主要看：
1. 文博的 AI 产品经理转型之路（API 已配）
2. 快刀青衣 AI 学习笔记（**v1.0 备份 1,146 但实测 1,258**）
3. 2026 WAIC（v1.0 备份 9YerORB0 但实测 `JawjeBlY` 487 笔记）

## 根因（三层）

### 🔴 错版 1：v1.0 备份的 `9YerORB0` "人工智能+WAIC" 不是 2026 WAIC

- v1.0 备份 `scripts/_backup_before_20260701/getnote_to_wiki.py`：
  ```python
  "9YerORB0": {"name": "人工智能+WAIC", "tag": "ai-research"}
  ```
- 实际 `getnote kbs-sub` 命令（v1.0 备份写过但 7-1 改造丢失）：
  ```
  JawjeBlY | 2026 WAIC 世界人工智能大会知识库 - 持续更新 | 487 笔记
  9YerORB0 | 人工智能+WAIC | 246 笔记（2025 旧版）
  ```

### 🔴 错版 2：v1.0 备份的笔记数 vs 实测不符

- v1.0 备份：`2eYxaj0z = 1146 篇`
- API 实测（7-15 14:16）：**1,258 篇**（11 天的增量）

### 🔴 错版 3：API `/resource/knowledge/list` 不返回订阅 KB

- 8:53 / 9:33 实测 API 只返回 8 个**自有** KB（`scope=DEFAULT`）
- 订阅的 KB（WAIC / 快刀青衣 / 高质量人类谈话库 等）必须用 `getnote kbs-sub` 命令

## 修复（L-37 + L-40 治本）

### Step 1: 扩展 KB_ROUTING（getnote_ej9_to_wiki.py）

**改前**：9 KB（含 8 自有 + 1 订阅主力 EJ9zwkln）  
**改后**：**11 KB**（8 自有 + 3 订阅）

```python
KB_ROUTING = {
    # === 8 自有 KB ===
    "04p8P2m0": "finance-journal",         # 投资日记
    "yYvRWqaY": "ai-pm",                  # 文博的ai产品经理转型之路 (139) ⭐⭐ 战略
    "EJlOEG10": "digital-community",        # 数字社区
    "K0BVyZM0": "ai-practice",             # AI实践日志
    "7JbLLvYe": "fintech",                 # 消费金融数据产品
    "Y2mRx3En": "lifestyle",               # 江浙沪徒步旅行杂记
    "n3EGyBd0": "notes-mixed",             # 印象笔记（文博 14:16 排除）
    "oJOA1ENY": "health",                  # 健康生活100年
    # === 3 订阅 KB 主力（战略 3 KB · 7-15 14:16）===
    "EJ9zwkln": "ai-technology",           # 高质量人类谈话库
    "2eYxaj0z": "ai-learning",             # 快刀青衣AI学习笔记 (1,258) ⭐⭐ 战略
    "JawjeBlY": "ai-waic-2026",            # 2026 WAIC 世界人工智能大会 (487) ⭐⭐ 战略
}
```

### Step 2: 同步扩展 KB_LIST（daily_note_scan.py）

`KB_LIST` 从 8 → 11（8 自有 + 3 订阅主力）

### Step 3: L-15 端到端 verify

```
✅ getnote_ej9 语法 OK
✅ daily_note_scan 语法 OK
✅ 3 KB_API 拉第 1 页：JawjeBlY 首条 WAIC 2025 AI 领导力论坛
✅ 11 KB dry-run：187 笔记（每 KB 20，小 KB 实际数）
```

### Step 4: 排除印象笔记（文博 14:16 指令）

`n3EGyBd0` 保留在 KB_LIST（用于未来抽样），但本次不主动同步

## 教训（L-40 治本）

详见 `lesson-2026-07-15-getnote-kbs-sub-cli-discovery.md`

### L-40 核心

**订阅的 GET 笔记 KB 必须用 `getnote kbs-sub` 命令列出，不能用 HTTP API `/resource/knowledge/list`**。

反例（7-15 14:16 揭穿前）：
- ❌ HTTP API 只返回 8 自有 KB
- ❌ v1.0 备份的 HIGH_VALUE_KBS 信息过时（WAIC 2026 是新 KB）
- ❌ 路径错位：写代码用了错误 ID（`9YerORB0`）

正例（7-15 14:16 后）：
- ✅ `getnote kbs-sub` 返回 12 个订阅 KB（含 `JawjeBlY`）
- ✅ 实测笔记数（API `/notes?topic_id=<id>` 第 1 页）
- ✅ L-37 揭穿 v1.0 备份 vs 实测差异

## 关联

- **INC-2026-07-15-001** (cron 25 fail-closed) — L-34/L-35/L-36
- **INC-2026-07-15-002** (GET 笔记 KB 报告 4 错) — L-37
- **INC-2026-07-15-003** (Agent 30 错) — L-38
- **INC-2026-07-15-004** (本地文档 RAG 化) — L-39
- **INC-2026-07-15-005** (战略 3 KB 同步) — **L-40 治本 · 本 INC**

## 状态

- [x] INC-005 创建（14:21）
- [x] L-40 沉淀
- [x] KB_ROUTING 9 → 11（getnote_ej9_to_wiki.py）
- [x] KB_LIST 8 → 11（daily_note_scan.py）
- [x] L-15 端到端 11 KB dry-run 187 笔记
- [ ] c3 cron 21:00 第一次跑实测（11 KB · 预期 ~1,884 笔记）
- [ ] state JSON 含 11 KB 笔记数
- [ ] 文博实际检索 3 KB 内容 verify
- [ ] Close

---

*INC 完稿: 2026-07-15 14:21 CST*
*接单人: 尼克·弗瑞 🕵️*
*关联: TASK-20260715-DCFA1C80 · 战略 3 KB 同步闭环*
