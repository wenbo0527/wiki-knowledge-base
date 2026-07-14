# Lesson L-31: INC/lesson 必须立即归档到 review-logs 子目录

> 7-14 14:00 沉淀 · nick_fury 🕵️ · INC-2026-07-14-003

---

## 教训主体

**任何 INC/lesson 写完 24h 内必须归档到 `review-logs/incidents/YYYY-MM/` 或 `review-logs/lessons/by-agent/{agent}/`，不得写在 `/05_AgentOutput/`、`/tmp/`、根目录、备份目录等任何其他路径。**

## 反例（INC-2026-07-14-003 揭穿 11 天真空根因）

```
✅ 7-6 INC 写在：  /05_AgentOutput/agent_work/Nick/INC/INC-2026-07-06-001_technical_report_repeat.md
✅ 7-6 lessons：    /05_AgentOutput/agent_work/Nick/lessons/2026-07-06_lessons_L24-L26.md
❌ Wiki 找不到     →  11 天真空（7-3 → 7-13）

❌ 写错路径 = 等于没写
   - Wiki 索引不到（路径不对）
   - AGENTS.md 不引用
   - _registry/_nick_registry 看不到
   - 7 天后根本想不起来在哪
   - 等于把经验扔进垃圾桶
```

## 正例（路径规范）

```
📁 路径规范 (按 _index.md v1.0):

  Incident  →  review-logs/incidents/YYYY-MM/inc_YYYY-MM-DD_NNN-{描述}.md
  Lesson    →  review-logs/lessons/by-agent/{agent}/lesson-YYYY-MM-DD-{描述}.md
  Registry  →  review-logs/_registry.md (全局) / by-agent/{agent}/_registry.md (团队)
  
✅ 写完后:
  1. write 工具调用成功（必须，lark-cli 推前必须 ls 确认）
  2. 更新 _registry.md / _nick_registry.md
  3. C-3 21:00 cron 会自动检查 review-logs 7 天新文档数
```

## L-31 grep 检查（修一类必 grep 全集）

```bash
# 任何 INC/lesson 文件应该在 review-logs/ 子目录, 不在 05_AgentOutput 或根目录
# 立即检查 - 应该查不到
find /Users/wenbo/Documents/05_AgentOutput -name "INC-2026-*" -newer /tmp/today_start \
  -type f 2>/dev/null
find /Users/wenbo/Documents/05_AgentOutput -name "les_*" -newer /tmp/today_start \
  -type f 2>/dev/null

# 任何根目录或散落文件
find /Users/wenbo/Documents/project/Wiki/wiki/review-logs -maxdepth 1 -name "inc_*" -type f
find /Users/wenbo/Documents/project/Wiki/wiki/review-logs -maxdepth 2 -name "les_*" -type f

# 当前: 13:55 grep 已清 (已移到规范路径) ✅
```

## L-31 防复发机制

| 机制 | 实现 |
|:---|:---|
| **C-3 升级** | `c3_daily_check.py` 21:00 cron 加 review-logs 7/30 天新文档检查 |
| **AGENTS.md §0 修正** | 区分"Agent 输出文件"(05_AgentOutput) vs "Wiki 沉淀"(review-logs) |
| **_nick_registry.md** | Nick 团队 lessons/INC 索引（已建 13:52）|
| **写完必更 registry** | 任何 INC/lesson 写完 → 必更 registry，否则算"未完成"|

## L-31 关联

| INC | 教训 | 关键点 |
|:---|:---|:---|
| INC-001 | L-28 | 数据层：多源 raise |
| INC-002 | L-29 | 验证层：输出/输入真实 |
| INC-003 | **L-31** | **路径层：写错 = 没写** |

3 个 INC + 3 个 lessons 拼出 Nick 团队 Wiki 沉淀的"三层质量门":
- L-28: 数据真实
- L-29: 验证真实
- **L-31: 路径真实**（最后一道门）

---

*🕵️ 尼克·弗瑞 · 2026-07-14 14:00*