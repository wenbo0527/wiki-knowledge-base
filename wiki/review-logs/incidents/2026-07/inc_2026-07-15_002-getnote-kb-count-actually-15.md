---
title: inc 2026 07 15 002 getnote kb count actually 15
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-15
---

# INC-2026-07-15-002: GET 笔记 KB 真实数量 15 个（报告"4 个"是错的）

> **揭穿**: 7-15 09:31 文博指出"GET笔记中有订阅的知识库 + 我自己的知识库 应该不止4个"  
> **9:35 verify 后**: API `/open/api/v1/resource/knowledge/list` 返回 8 个自有 KB（3,091 笔记）+ v1.0 备份列 7 个订阅 KB = **15 个 KB**  
> **报告错版**: `wiki/reports/wiki-project-status-report-20260715.md §5.2` 写"~1,130 笔记 / 7 个 KB 路径"（漏了 6 个自有 + 漏 1 个订阅）

---

## 现象

报告 `wiki-project-status-report-20260715.md` §5.2 写：

> L2 Get 笔记 | ~1,130 笔记 / 7 KB 路径 | 🟡 30% 同步

但 7-15 09:31 文博指出 GET 笔记有"订阅的知识库 + 我自己的知识库"两类，应该更多。

## 根因（双层）

### 🔴 漏数 1：只统计了 4 个 KB（v1.0 备份的 HIGH_VALUE_KBS 7 个里的 4 个）

报告里列的 4 个 KB（高质量人类谈话库 / AI 实践日志 / 消费金融数据产品 / 数字社区）只覆盖 v1.0 备份 7 个 HIGH_VALUE_KBS 的 57%。

**v1.0 备份的完整 7 个 HIGH_VALUE_KBS**（`scripts/_backup_before_20260701/getnote_to_wiki.py`）：

```python
HIGH_VALUE_KBS = {
    "EJ9zwkln": {"name": "高质量人类谈话库", "tag": "ai-persona"},
    "9YerORB0": {"name": "人工智能+WAIC", "tag": "ai-research"},          # ← 漏
    "6n1KzOW0": {"name": "产品大神怎么想", "tag": "product-thinking"},   # ← 漏
    "K0BVyZM0": {"name": "AI实践日志", "tag": "ai-practice"},
    "7JbLLvYe": {"name": "消费金融数据产品", "tag": "fintech"},
    "5qY2wG04": {"name": "产品&运营&营销一把抓", "tag": "marketing"},     # ← 漏
    "2eYxaj0z": {"name": "快刀青衣AI学习笔记", "tag": "ai-learning"},    # ← 漏（刀哥）
}
```

### 🔴 漏数 2：完全漏了 8 个"自有 KB"（API 实测有）

GET 笔记 API `/open/api/v1/resource/knowledge/list` 7-15 09:33 实测返回：

```json
{"data": {"topics": [
  {"id": "04p8P2m0", "name": "投资日记", "note_count": 27, "scope": "DEFAULT"},
  {"id": "yYvRWqaY", "name": "文博的ai产品经理转型之路", "note_count": 132, "scope": "DEFAULT"},
  {"id": "EJlOEG10", "name": "数字社区", "note_count": 183, "scope": "DEFAULT"},
  {"id": "K0BVyZM0", "name": "AI实践日志", "note_count": 504, "scope": "DEFAULT"},
  {"id": "7JbLLvYe", "name": "消费金融数据产品", "note_count": 42, "scope": "DEFAULT"},
  {"id": "Y2mRx3En", "name": "江浙沪徒步旅行杂记", "note_count": 3, "scope": "DEFAULT"},
  {"id": "n3EGyBd0", "name": "印象笔记", "note_count": 2196, "scope": "DEFAULT"},  # ← 最大 2196 篇
  {"id": "oJOA1ENY", "name": "健康生活100年", "note_count": 4, "scope": "DEFAULT"}
]}}
```

**8 个自有 KB / 3,091 笔记**（之前报告全漏了"自有 vs 订阅"分类）

## 真实全量

| 类别 | 数量 | KB 列表 | 笔记总数 |
|:---|:---:|:---|:---:|
| **订阅** | 7 | 高质量人类谈话库 / 人工智能+WAIC / 产品大神怎么想 / AI实践日志 / 消费金融数据产品 / 产品&运营&营销一把抓 / 快刀青衣AI学习笔记（刀哥）| ~750+（各 100-300 篇）|
| **自有** | 8 | 投资日记(27) / 文博的ai产品经理转型之路(132) / 数字社区(183) / AI实践日志(504) / 消费金融数据产品(42) / 江浙沪徒步旅行杂记(3) / 印象笔记(2196) / 健康生活100年(4) | **3,091** |
| **去重后** | **15** | 7 订阅 + 8 自有 | **~3,841** |

注：AI实践日志 / 消费金融数据产品 在两表都出现，需要 verify 是同一 KB（v1.0 是订阅视角，API 是自有视角，名字一致 → 同 KB）

## 报告修正（9:35）

| 维度 | 错版（9:15）| 正版（9:35）|
|:---|:---|:---|
| KB 总数 | 4 | **15**（7 订阅 + 8 自有）|
| 笔记总数 | ~1,130 | **~3,841** |
| 同步覆盖率 | 30% | **3/15 = 20%**（更糟）|
| 缺漏 | 缺 11 个 KB | 全覆盖 |

## 教训（L-37）

### L-37: 报告必须 verify 实时 API，不能依赖 v1.0 备份

反例（9:15 报告）：
- 看了 v1.0 备份脚本（7 个 HIGH_VALUE_KBS）但只列 4 个
- 完全没调 API 实测
- 没分"订阅 vs 自有"两类

正例（9:35 修正）：
- 实调 `/open/api/v1/resource/knowledge/list` API
- 列出 8 个自有 KB + 7 个订阅 KB = 15 个
- 笔记总数从 ~1,130 修正为 ~3,841

### L-37 治本

| 动作 | 实施 |
|:---|:---|
| 报告类输出必调实时 API | 任何"现状盘点"类报告，必先 curl 实测 |
| 分类必完整 | KB 要分"订阅/自有"两类（不仅看名字） |
| 同步链路配置真实 | `KB_ROUTING` 必须覆盖所有自有 + 关键订阅 |
| L-32 对账扩展 | c3_daily_check.py 不仅对账笔记数，还要对账 KB 列表 |

## 修复方向

### 短期（9:45 前）

- ✅ 写 INC-002 归档本次揭穿
- ✅ 修正 `wiki/reports/wiki-project-status-report-20260715.md §5.2`
- 🟡 扩展 `scripts/getnote_ej9_to_wiki.py` `KB_ROUTING` 到 8 个自有 KB
- 🟡 扩展 `scripts/daily_note_scan.py` `KB_AI/KB_FINTECH` → 包含全部 8 个自有

### 中期（本周）

- 🟢 KB_ROUTING 包含全部 15 个 KB（7 订阅 + 8 自有）
- 🟢 L-32 对账升级：KB 列表 + 笔记数双向对账
- 🟢 报告 §7 优化项更新：Get 笔记覆盖率从 30% 改为 20%（更紧迫）

### 长期（本月）

- 🟡 KB 价值评级：8 个自有 KB 哪些值得同步到 Wiki
  - 印象笔记 2196 篇（最大但杂）
  - 文博的ai产品经理转型之路 132 篇（战略相关 ⭐）
  - 数字社区 183 篇（业务相关 ⭐）
  - AI实践日志 504 篇（工作日志 ⭐）
  - 消费金融数据产品 42 篇（行业研究 ⭐）
  - 投资日记 27 篇（个人）
  - 江浙沪徒步旅行杂记 3 篇（生活）
  - 健康生活100年 4 篇（生活）

## 状态

- [x] INC-002 创建（9:35）
- [x] L-37 沉淀
- [x] 报告 §5.2 修正（9:36）
- [ ] 扩展 KB_ROUTING 到 8 个自有 KB
- [ ] 扩展 daily_note_scan.py KB 配置
- [ ] c3_daily_check.py KB 列表对账升级
- [ ] Close

---

*INC 完稿: 2026-07-15 09:35 CST*
*接单人: 尼克·弗瑞 🕵️*
*关联: 报告 `wiki-project-status-report-20260715.md` §5.2 已修正*
