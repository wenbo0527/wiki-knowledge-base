---
title: inc 2026 07 14 001 etf 18 day mock data
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-15
---

# 🔴 Incident 001: ETF 速览分位数据 18 天失真（hardcoded 预设冒充分位）

| 字段 | 值 |
|:---|:---|
| **ID** | inc_2026-07-14_001 |
| **严重级别** | 🔴 Critical |
| **状态** | ✅ Closed |
| **发现时间** | 2026-07-14 09:00 |
| **发现者** | wenbo（用户主动疑问） |
| **负责人** | nick_fury |
| **最后更新** | 2026-07-14 09:30 |

---

## 问题描述

2026-06-26 至 2026-07-14（**18 天**），每日 07:15 推送的投资日报「ETF 速览」表中的「2 年分位」列全部是 **2026-06-25 写死在代码里的 hardcoded 预设值**，不是真实计算的市场数据。

文博 7-14 09:00 问"ETF 速览的数据是否不太对" → 弗瑞立即检查 → 发现 18 天决策依据失真。

### 失真对照（预设 vs 真实，7-13 收盘）

| ETF | 预设 6-25 | 真实 7-13 | 差异 | 决策影响 |
|:---|---:|---:|---:|:---|
| **半导体** | 82.1% | **29.4%** | **-52.7pp** | 推送"减仓 20-30%"，实际应在低位**加仓** |
| AI | 76.4% | 45.9% | -30.5pp | 推送"持观"，实际可**加仓** |
| 卫星 | 70.2% | 36.2% | -34.0pp | 推送"持观"，实际可**加仓** |
| 电力 | 65.7% | 40.7% | -25.0pp | 推送"加仓"，实际可在**更深低位加仓** |
| 中证500 | 89.3% | 80.7% | -8.6pp | 推送"减仓 40%"，严重度高估 |
| 科创50 | 78.6% | 85.4% | +6.8pp | 推送"持观"突破 80% 应减仓 |
| 沪深300 | 81.2% | 81.8% | +0.6pp | 接近，决策影响小 |
| 上证50 | 72.5% | 77.6% | +5.1pp | 接近 |

## 影响分析

| 影响范围 | 说明 |
|:---|:---|
| **功能影响** | 投资日报「ETF 速览」每天推送的"减仓/加仓/持观"决策建议失真 |
| **用户体验** | 18 天来文博的 ETF 决策可能基于错误分位，特别是**半导体**（预设 82.1% 减仓 vs 真实 29.4% 加仓）|
| **数据影响** | 真实市场分位变化无法触达用户；"何刚动作"全错 |
| **信任影响** | Nick 推送 18 天每天说"✅ 成功"但内容失真，**自检机制形同虚设** |

## 根因分析

**核心问题：东方财富 ETF 估值字段 API（f162）失效后，旧 `etf_real_time_fetcher.py` 静默 fallback 到 hardcoded 预设，没有任何"数据来源"标注或报警。**

### 链路

1. `etf_real_time_fetcher.py:152-164` `_get_preset_data()` 写死 8 只 ETF 6-25 当天的预设分位 + PE
2. `_get_fallback_valuation()` 在东方财富估值字段失效时**静默**调用 preset
3. `etf_hegang_report.py` 生成的 `data/etf_hegang_report.md` 标注"待 6-26 修 akshare"，但**没人改、没人看、没人报警**
4. `daily_investment_report.py:114-180` 从 md 文件读分位时，**不校验数据日期是否新鲜**，也**不校验数据源**——只看字符串里有几%数字
5. 每日 07:15 cron 跑 exit 0，飞书推送成功，文博收到"✅ 成功"但内容是 6-25 死数据
6. **没有任何"分位数据超过 N 天未更新"的报警**

### 关键问题

> **失真的数据被无标识地推送了 18 天。所有自检机制（exit 0、push 成功、内容长度 ≥ 100）只看"输出"，不看"输入是否真实"。**

## 解决措施

### 已尝试的措施

| 时间 | 措施 | 结果 |
|:---|:---|:---|
| 09:00 | 文博疑问"数据不太对" | 触发排查 |
| 09:01 | grep preset 找到 `etf_real_time_fetcher.py` hardcoded 数据 | 揭穿根因 |
| 09:03 | curl sina K 线接口测试 | 验证可用 |
| 09:05 | 文博同意"1 然后多数据源兜底 + 拉不到告诉我" | 启动修复 |
| 09:07 | 写 `scripts/etf_percentile_fetcher.py` (多源 + raise + 新鲜度) | 8/8 通 |
| 09:08 | 集成到 `daily_investment_report.py`（v3 表格） | 4 路径测试全过 |
| 09:09 | 手动推送 7-14 修正版给文博（lark-cli ✅ + wiki ✅） | 文博立即看到真实数据 |

### 解决方案

```
1. 写 etf_percentile_fetcher.py (v1.0)
   - 8 只 ETF 多源兜底：sina_etf_kline → sina_index_kline → raise
   - 新鲜度校验：最后一天距今 ≤ 6 天（覆盖长假）
   - 失败必须 raise + 完整错误（哪个 ETF / 哪个源 / 什么错），不准静默
   - 输出：data/etf_percentile_today.json

2. 改 daily_investment_report.py read_yesterday_etf_summary (v3)
   - 优先读 etf_percentile_today.json
   - failures 非空 → 报警"🔴 X 只拉不到"，绝不 fallback 预设
   - JSON 缺失/损坏/部分成功 → 显式错给文博
   - PE 字段：标 "⚠️ PE 待 v2.1"（sina 无 PE 接口，先用分位做决策）

3. L-15 端到端验证 6 步
   - ✅ 1. 语法 py_compile
   - ✅ 2. 生成内容
   - ✅ 3. 数据正确（真实对照预设）
   - ✅ 4. 新鲜度检查（last_day ≥ 6 天前）
   - ✅ 5. 异常 raise（全部模拟失败时 exit 1 + 8/8 报警）
   - ⏳ 6. INC + lessons（本文档）

4. 给文博手动推送 7-14 修正版（飞书消息 om_x100b6a6c8d3e04...）
```

## 依赖与阻塞

| 依赖方 | 事项 | 状态 |
|:---|:---|:---:|
| python3.11 venv | akshare 装通（如用户选 v2 路径）| 🟢 可选——sina 已够用 |
| eastmoney | push2his K 线 secid 对齐 | ❌ 已验证 14 个代码全 null（备用）|
| 文博 | 决策是否升级 PE 字段（v2.1）| 🟡 等文博 |

## 关联文档

- 相关 Lesson: `review-logs/lessons/2026-07-14_lessons_L28-L29.md`
- 修复 commit: scripts/etf_percentile_fetcher.py + daily_investment_report.py
- 推送备份: `data/investment_push_history/2026-07-14_fix.md`

---

## 后续行动

- [x] 揭穿 hardcoded 预设 → 写 fetcher
- [x] L-28/L-29 lessons 沉淀
- [x] 集成 daily_investment_report.py + 4 路径测试
- [x] 手动推送 7-14 修正版
- [ ] **plist 跑前预演**（7-15 07:15 第一次自动跑，先看 09:00 抓数据 + 跑通）
- [ ] **PE 字段 v2.1**（eastmoney secid 对齐 / 找 akshare 替代接口）
- [ ] **MEMORY.md 更新 7-14 INC + L-28/L-29**
- [ ] **daily/2026-07-14.md 写今日记录**

---

*Created: 2026-07-14 09:00 | Updated: 2026-07-14 09:30*
*Closed: 2026-07-14 09:30*
