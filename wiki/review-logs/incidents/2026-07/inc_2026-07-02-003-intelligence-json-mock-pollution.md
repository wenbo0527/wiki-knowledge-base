---
title: inc 2026 07 02 003 intelligence json mock pollution
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-03
---

# INC-2026-07-02-003: 每日情报推送数据污染（intelligence.json 空 → mock fallback）

## 现象

- **7-2 18:21 cron run** 推送了 5 篇文章到 OpenClaw 当前会话（**A 方案生效验证**）
- 但推送内容**5 篇全是 seangoedecke.com**，而 **collection 7-1 里 0 篇 seangoedecke**
- agent 自己在 fix 记录里承认 "走 mock 浏览器搜索补充（假数据）"
- **影响范围**：5-25 之后所有 `push_today_v7.py` 推送都受影响（待审计 5-25 daily brief 内容真实性）
- **发现**：18:21 文博问 "请检查飞书渠道对接" 时，agent 通过 sessions_send 注入，**自己报告**了这个问题

## 根因（3 层）

### Layer 1: 数据源断裂（系统级）
- `analyzer_v2.py` 加载 `intelligence.json` 作为 articles 来源
- `intelligence.json` 是 **空 list**（0 条）
- 原因待查：RSS collection 文件**没回流**到 intelligence.json

### Layer 2: Filter 返回 0（应用级）
- `analyzer_v2.filter_recent_articles(days=30)` 在空 articles 上返回 0
- filter 逻辑：published 优先 + fetched_at fallback（**双重**）
- **agent 报告说 "filter 用 published 导致 0 篇"** → 不完全准确，真因是 articles 本身就是空的

### Layer 3: Mock Fallback 不 raise（设计缺陷）
- `push_today_v7.py` 第 250-265 行：当 `need_search_supplement=True`（< 3 篇）时调 `search_with_browser()`
- `search_with_browser()` 返回**硬编码 mock 数据**（"关于 X 的最新资讯..."）
- **不 raise 也不 WARN**，mock 数据被加入 all_articles 并继续推送
- L-17 教训的反面：违反 "0 篇必须 raise" 原则

## 修复（7-2 18:29-20:42 · 73 分钟）

### 1. A. 暂停 cron da3c0cae（30s）
- `openclaw cron disable da3c0cae-34d5-4f88-8133-f9589837fb6c`
- ✅ enabled=false（防明早 8:30 推送 mock）

### 2. B. 修 push_today_v7.py mock fallback（10 min · L-24）
```python
# 旧（mock 黙默通过）
if need_search_supplement:
    results = search_with_browser(topic, count=2)
    search_articles.extend(results)

# 新（raise + 详细错误信息）
if need_search_supplement:
    raise RuntimeError(
        f"🔴 RSS 内容不足 {len(top_articles)} 篇（需 ≥3 篇）\n"
        f"   不会调用 mock fallback 填充。\n"
        f"   原因可能是: intelligence.json 空 / collection 未同步 / analyzer 加载失败\n"
        f"   修复后才能推送，请勿用 mock 数据顶替。\n"
        f"   参考: INC-2026-07-02-003 + L-24 教训。"
    )
```

**端到端验证**：
- ✅ `python3 -m py_compile` 通过
- ✅ 0 篇场景 raise 正确（intelligence.json 空 → analyzer 加载 0 → filter 返回 0 → 触发 raise）

### 3. D. INC + lessons 沉淀（15 min）
- INC-2026-07-02-003（本文件）
- lesson-2026-07-02-data-flow-break.md（L-24）
- 7-2 daily 增量段

## 影响审计（待做）

- ⏳ **5-25 daily brief**（昨天发给文博）：12 篇精选需逐条验证
- ⏳ **5-26 ~ 7-1** 期间所有 push_today_v7.py 推送
- ⏳ 评估是否需要补真实推送 + 给文博致歉

## 教训（L-24）

### 🆕 L-24.1: mock fallback 不能黙黙通过
- **原则**：任何"主源 0 → fallback mock"的设计，**必须 raise**，不能用 mock 顶替
- **反例**：`search_with_browser()` 返回硬编码 mock 数据 → 推送污染
- **正例**：`raise RuntimeError("RSS 内容不足 3 篇，请勿用 mock 数据顶替")`

### 🆕 L-24.2: 数据流必须有 end-to-end 验证
- **问题**：RSS collection 90 篇 → intelligence.json 0 条（**数据流断裂**）
- **预防**：每次 RSS 抓取后必校验"collection 总数 → intelligence.json 总数"是否匹配
- **TODO**：找 intelligence.json 为什么空 + 修复 collection → intelligence.json 的同步逻辑

### 🆕 L-24.3: agent 自报问题 = 黄金信号
- **正面案例**：cron run agent 完成后**自己报告** fix 记录，诚实承认 mock 污染
- **预防**：保留 agent 修复报告链路（不要被"已完成"消息掩盖问题细节）
- **行动**：本 INC 是因为"agent 报问题"才能在 18:21 当天发现

### 🆕 L-24.4: 信任源验证（Nick 情报分析师特有）
- **原则**：作为情报分析师，**每日情报推送内容必须抽样验证**
- **失职**：5-25 之后我（Nick）没抽检 daily brief 内容真实性
- **预防**：每次推送后跑 `grep URL` 验证文章能从 RSS collection 找到

## 关联

- INC-2026-07-02-001（lark-cli launchd 上下文推送失败）
- INC-2026-07-02-002（技术日报重复推送）
- L-17（"0 篇必须 raise"教训 · 7-1 daily_tech_report.py 已用 · push_today_v7.py 没贯彻）
- L-19（用户主动询问 = 兜底信号）
- L-15（端到端验证铁律）

## 状态

- ✅ A 暂停 cron（enabled=false）
- ✅ B 修 mock fallback（raise 验证通过）
- ✅ D INC + lessons 落盘
- 🟡 intelligence.json 数据流治本（待周日复盘 + 周一修复）
- 🟡 5-25 ~ 7-1 推送内容审计（待排期）

---
*修复时间: 2026-07-02 18:29 - 20:42 · 73 分钟*
*接单: 文博 "D" (A+B+D 并行)*
*维护: 尼克·弗瑞 🕵️*