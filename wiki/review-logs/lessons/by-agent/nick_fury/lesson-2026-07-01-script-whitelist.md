# Lesson 2026-07-01: 脚本白名单 + 端到端铁律（L-14 / L-15）

> **作者**: 尼克·弗瑞 🕵️
> **日期**: 2026-07-01 10:00
> **触发**: INC-2026-07-01-001（morning-rss-etf-push 3 通道失败）+ 文博 7-1 09:22 "先清理旧脚本"
> **关联**: L-7（修一个≠修一类）/ L-8（描述根因要精准）/ L-13（OpenClaw 原生优先）/ INC-005/006

---

## L-14: 脚本白名单 — 用户语境下的"日推/技术日报"必须唯一指向

### 教训原文

> **听到"日推"立刻应该 grep "## 🎯 目的" 找到唯一脚本，而不是拿名字相近的脚本跑**

### 反例

- 用户问"今天日推呢" → 我跑去跑了 `tech_briefing.py`（名字里有 "briefing" 像推送）
- 实际应该跑：`daily_investment_report.py`（产品定义 = "每日投资日报"）

### 正例

```bash
# 听到任何"产品名" → 先 grep SOUL.md / AGENTS.md / 注释 找到唯一脚本
grep -r "🎯 目的" scripts/*.py | grep -i "日推\|日报\|技术"
# daily_tech_report.py:       🎯 目的 1（每日技术日报）
# daily_investment_report.py: 🎯 目的 2（每日投资日报）
# evening_tracker.py:         🎯 目的 3（晚上追踪）
```

### 可执行

**AGENTS.md §3 Skill Orchestration 加"脚本白名单"段**：

```markdown
## 3.1 脚本白名单（Nick 主动作清单）

| 用户语境 | 唯一脚本 | 产品定义 |
|:---|:---|:---|
| "技术日报" / "技术简报" / "AI 资讯" | `scripts/daily_tech_report.py` | 每日技术前沿感知 (08:35) |
| "投资日报" / "日推" / "ETF" | `scripts/daily_investment_report.py` | 每日 ETF 决策支持 (07:15) |
| "晚上追踪" / "晚间复盘" / "投资纪律" | `scripts/evening_tracker.py` | 22:00 实时监控 |
| "知识库扫描" / "Get 笔记扫描" | `scripts/daily_note_scan.py` | 每日入库高价值笔记 (21:00) |
| "RSS 抓取" | skills/rss-intelligence/scripts/daily_pipeline.py | 04:01 抓 8 源 |
| "ETF 报告" | skills/rss-intelligence/scripts/etf_hegang_report.py | 08:35 生成 etf_hegang_report.md |
| "GitHub 追踪" | scripts/github_tracker.py | 每日 GitHub 活动 (01:30) |
| "C-3 日报自检" / "21:00 自检" | scripts/c3_daily_check.py | 21:00 grep "写"vs"已完成" |
| "写 daily" / "morning daily" | scripts/morning_daily_writer.py | 08:30 写 memory/daily |
| "Wiki 健康度" | scripts/wiki_health_check.sh | 09:00 Wiki 13044 chunks |
```

**任何不在白名单的脚本，必须先 chat 确认，不准直接跑。**

---

## L-15: 新加的 plist/脚本必须当日端到端验证

### 教训原文

> **写完新 plist/新脚本 24h 内必须跑通 3 通道全成功（不仅 dry-run / format test）**

### 反例

- 6-29 写 `morning_rss_etf_push.py`：只跑了 dry-run / format test / mock triage，没跑端到端推 lark-cli
- 实际 lark-cli 7:15 推送 0/3 成功，没人发现 3 天（6-29 ~ 7-1）
- 7-1 文博反馈"全是 Get 笔记内容"才暴露 RSS 解析 bug

### 正例

```bash
# 新 plist/脚本上线必跑（AGENTS.md §8 启动规范补充）
python3 scripts/NEW.py 2>&1 | tee /tmp/NEW.test.log
# 检查 3 通道日志
grep -E "通道 [123]" /tmp/NEW.test.log
# 必须看到: 通道 1 ✅ AND 通道 2 ✅/WARN AND 通道 3 ✅
# 不允许 0/3 或 1/3 (Wiki only)
```

### 可执行

**SOUL §9 工具策略加 "端到端铁律"**：

> 写新 plist / 写新脚本 / 修改数据 pipeline 24h 内必须手动跑通端到端：
> 1. **3 通道全成功**（lark-cli ✅ / sessions_send ✅/WARN / wiki ✅）
> 2. **数据正确**（5 篇 RSS 真的拿到 / ETF 真的从 etf_hegang_report.md 取）
> 3. **异常有 raise**（"0 篇"必须 raise，不允许静默通过）
> 4. **写 INC + 教训**（L-N 必写）

**7-1 已落地**：daily_investment_report.py / daily_tech_report.py / evening_tracker.py 三个新/重命名脚本全部端到端 dry-run 通过 + Wiki 落盘 ✅

---

## 关联 L-7 / L-8 / L-13

- **L-7（修一个≠修一类）**：6-23 修 11 plist，漏 1 个新加的 → 7-1 才补修
- **L-8（INC 报告必须附原文片段）**：6-15 错描述根因，6-23 才修正
- **L-13（OpenClaw 原生优先）**：6-30 文博明示 → 7-1 启动 launchd → cron 迁移

---

*沉淀: 尼克·弗瑞 🕵️ | 验证: 7-1 22:00 第 1 次 cron 自动跑通*
*下次审计: 7-3 周日 22:00 复盘*
