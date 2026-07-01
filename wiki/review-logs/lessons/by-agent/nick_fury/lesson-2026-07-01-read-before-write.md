# Lesson 2026-07-01: 写脚本前 read 3 行 + 修一类必 grep（L-16 / L-17）

> **作者**: 尼克·弗瑞 🕵️
> **日期**: 2026-07-01 10:05
> **关联**: L-7（修一个≠修一类）/ L-8（INC 附原文）/ L-14（白名单）/ L-15（端到端）/ INC-2026-07-01-001

---

## L-16: 修复一类问题后必须 grep 全集是否有同类问题

### 教训原文

> **修一个 ≠ 修一类。修一类 ≠ 修一类再 grep 一次。**

### 反例

- 6-23 修 11 个 launchd plist（INC-001 复发），**漏掉 6-29 新加的 `morning-rss-etf-push.plist`**
- 结果 7-1 INC-001 复发（同一类问题：plist PATH 缺失）
- 8 天真空（6-23 → 7-1）

### 正例

```bash
# 修一类问题后 24h 内必 grep（同属性全集）
grep -l "missing.path" /Users/wenbo/Library/LaunchAgents/com.nickfury.*.plist 2>/dev/null
grep -L "EnvironmentVariables" /Users/wenbo/Library/LaunchAgents/com.nickfury.*.plist 2>/dev/null
launchctl list | grep -v " 0 " | grep "com.nickfury"
```

### 可执行

**AGENTS.md §4.1 错误恢复加 "L-16 grep 全集" 段**：

> 任何修一类问题（如 plist 修、cron 修、permission 修、format 修）动作完成后：
> 1. **24h 内 grep 同类全集**（确认无遗漏）
> 2. **写日记到 daily**（如 7-1 中午 L-16 grep 记录）
> 3. **追加到 lessons 文件**（即可复用）

**L-16 实践 7-1**：
- 修 1 个 plist（morning-rss-etf-push 加 PATH）→ 立即 grep 全集
- 发现 daily-note-scan 也缺 PATH → 同次修
- 还发现 bestpractice / rss.* / wiki.* 等其他 16 个 plist 都缺 → 7-2 批量修队列

---

## L-17: 写脚本/写新功能前必 read 3 行示例数据

### 教训原文

> **写新脚本不 read 现有数据，等于盲人摸象。3 行示例 ≤ 30 秒，可省 3 天返工。**

### 反例

- 6-29 写 `morning_rss_etf_push.py` 没 read `collection_*.json`
- 假设 JSON 结构是 `{articles: [...]}` 顶级
- 实际是 `{results: [{articles: [...]}]}` 嵌套
- 结果：RSS 永远是 0 篇，3 天没发现（6-29 ~ 7-1）

### 正例

```bash
# 写任何读 JSON / CSV / 数据库的脚本前：
head -3 data/topic_collection/collection_20260701_*.json | python3 -m json.tool | head -50

# 看 API 响应结构：
curl -s "https://api.example.com/v1/list" | head -50

# 看数据库表结构：
sqlite3 data/nick_fury.sqlite ".schema notes"
```

### 可执行

**SOUL §9 工具策略加 "read 示例数据铁律"**：

> 任何新脚本 / 任何修改数据 pipeline / 任何加新数据源动作：
> 1. **写之前必 read 3 行** 示例数据（≤ 30 秒，可省 3 天）
> 2. **写完必端到端跑**（L-15）
> 3. **异常必 raise**（"0 篇"不许静默通过）
> 4. **写 INC + lessons**（L-N 必写）

**L-17 实践 7-1**：

| 新脚本 | read 数据耗时 | 端到端跑耗时 | 节省 debug 时间 |
|:---|:---:|:---:|:---:|
| daily_tech_report.py | read collection JSON (2 min) | dry-run (1 min) | 预估 3 天 |
| evening_tracker.py | read daily_investment_summary.py (已存在) | --dry-run (1 min) | 预估 2 天 |

---

## 与 7-1 INC-009 闭环的关联

| 行动 | L-14 | L-15 | L-16 | L-17 |
|:---|:---:|:---:|:---:|:---:|
| 修 plist 加 PATH | | | ✅ | |
| 写 daily_investment_report.py | ✅ | ✅ | | ✅ |
| 写 daily_tech_report.py | ✅ | ✅ | | ✅ |
| 写 evening_tracker.py | ✅ | ✅ | | ✅ |
| trash 19 旧脚本 | ✅ | | ✅ | |
| 后续：批量修 16 个 plist | | | ✅ | |

---

## 落地清单（7-2 / 7-3 待办）

- [ ] **7-2 上午**: 批量修 16 个 plist（bestpractice / rss.* / wiki.* / kb.* 等），应用 L-16
- [ ] **7-2 上午**: AGENTS.md §3 加脚本白名单段（L-14）
- [ ] **7-2 上午**: AGENTS.md §4.1 加 L-16 grep 全集段
- [ ] **7-2 下午**: SOUL §9 加 read 示例数据 + 端到端铁律（L-15/L-17）
- [ ] **7-3 周日**: 全部 22 个 plist 端到端验证 + scripts/ 复盘

---

*沉淀: 尼克·弗瑞 🕵️ | 验证: 7-2 09:00 batch 修复时*
*下次审计: 7-3 周日 22:00 复盘*
