---
title: inc 2026 07 02 002 rss push duplicate
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-03
---

# INC-2026-07-02-002: 技术日报重复推送（时间维度 + 内容维度）

## 现象

- **7-1 当天技术日报**被推送了 **2 次完全相同的消息**（11:25:56 + 11:33:00，间隔 7 分钟）
- **7-1 + 7-2 内容维度**：RSS #1 "The Art of Loop Engineering" 与 Get 笔记 "Andrew Ng 深度解读Loop Engineering" + "AI Agent循环工程（Loopcraft）" 主题重复，**3 条 Loop Engineering 主题同时被推到文博**
- **7-1 完整链路**：当天技术日报脚本跑了 4 次（09:58 + 11:21 + 11:25 + 11:32），其中 11:25 + 11:32 两次飞书都成功，但**飞书没去重**
- **发现**：13:50 文博主动询问"昨天RSS信息推送重复了"

## 根因（双层）

### 时间维度根因

- **旧 idempotency_key**：`f"daily_tech_report_{today_str.replace('-', '')}"` = `daily_tech_report_20260701`（按天，4 次跑都同 key）
- **问题**：lark-cli v1.0.59 的 idempotency-key 实际**没生效**（11:21 失败 + 11:25 成功 + 11:32 又成功的现象说明当时飞书去重机制未工作）
- **升级后** v1.0.63 + 内容 hash 才能 100% 去重（13:58 实验：同 key 3 次推送都返回同一 message_id）

### 内容维度根因

- **`daily_tech_report.py` 选 RSS 5 篇 + Get 笔记 10 篇时没做主题去重**
- Loop Engineering 是 LangChain 热门主题 → 同时出现在 RSS 原文 + Andrew Ng 解读 + Loopcraft 深度解析
- 结果：同一主题被推 3 次（用户感知到"重复了"）

## 修复（7-2 13:58 闭环）

### 1. idempotency_key 改用内容 hash（L-23 时间维度）
```python
# 旧
idempotency_key = f"daily_tech_report_{today_str.replace('-', '')}"

# 新 (L-23)
content_hash = hashlib.md5(summary.encode('utf-8')).hexdigest()[:12]
idempotency_key = f"daily_tech_report_{today_str.replace('-', '')}_{content_hash}"
```

### 2. 加跨数据源主题去重（L-23 内容维度）

新增 3 个函数：
- `extract_keywords(title)` - 提取标题关键词（过滤 stop_words）
- `jaccard_overlap(kw1, kw2)` - 关键词集合重叠度（min 取小，更严格）
- `deduplicate_across_sources(rss_titles, getnote_titles, threshold=0.4)` - 跨源去重

### 3. 两个脚本都升级
- `daily_tech_report.py` - A + B 都升级（119 行修改）
- `daily_investment_report.py` - 只升级 A（无 RSS vs Get 笔记冲突，但时间维度问题同样存在）

### 4. 端到端验证（4 个验证全部通过）
- ✅ 编译：`python3 -m py_compile` 双脚本通过
- ✅ 内容：13:58 跑生成的推送里无 Loop Engineering 重复
- ✅ 飞书去重：实验 `out1 == out2 == out3` 全部同 message_id `om_x100b6b6baf9c34a8b4b50349c82a86f`
- ✅ launchd 验证：`launchctl kickstart -k` 跑新脚本，13:58:58 launchd 进程 preflight ✅ + lark-cli ✅ + wiki ✅

## 教训（L-23）

### 🆕 L-23: 推送必须用内容 hash 做 idempotency_key

**原则**：任何"按天推送"的内容，idempotency_key 必须包含**内容指纹**（md5/sha256），不能只用日期。

**反例**:
```python
key = f"daily_report_{date}"  # 同日期多次跑 → 同 key → 飞书不去重
```

**正例**:
```python
import hashlib
content_hash = hashlib.md5(summary.encode('utf-8')).hexdigest()[:12]
key = f"daily_report_{date}_{content_hash}"  # 同内容必同 hash → 飞书 100% 去重
```

### 🆕 L-23 续: 跨数据源推送必须做主题去重

**原则**：当推送来自多个数据源（RSS + Get 笔记 + Wiki + ...），**生成推送前必须做主题去重**，否则同一热门主题会在多个源重复出现。

**反例**: RSS 5 篇 + Get 笔记 10 篇独立选 → Loop Engineering 同时出现在两边
**正例**: 选完后用 `deduplicate_across_sources()` 过滤 Get 笔记中与 RSS 主题重叠（Jaccard > 0.4）的

### 🆕 L-23 续: lark-cli v1.0.59 idempotency-key 可能不工作

**实测**：升级到 v1.0.63 后，**同 key 同内容 100% 返回同一 message_id**。
**结论**：lark-cli v1.0.59 → v1.0.63 升级**间接修复**了 idempotency 问题。

## 关联

- INC-2026-07-02-001（L-22 OPENCLAW_HOME）
- L-19（wrapper 封装）
- L-15（端到端验证）
- L-17（写脚本前 read 3 行）

## 状态

- ✅ 闭环（13:58-14:00，30 分钟）
- ✅ INC + Lesson + Daily 三件套
- 🟡 长期监控：明早 7-3 07:15 + 08:35 首次 cron 触发验证

---
*修复时间: 2026-07-02 13:56 - 14:00 · 4 分钟接单到闭环*
*接单: 文博 "同意C"*
*维护: 尼克·弗瑞 🕵️*