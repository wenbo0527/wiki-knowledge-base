# INC-2026-07-20-001: Wiki 自动走查报告路径漂移导致 4 天"假断档"

> **报告时间**: 2026-07-20 18:25 CST
> **报告人**: 尼克·弗瑞 🕵️
> **关联 cron**: `wiki.review` (e3826ac4-... · 03:30 daily)
> **关联脚本**: `/Users/wenbo/Documents/project/Wiki/scripts/wiki_auto_review.py`
> **关联修复**: L-N · 7-20 Wiki 健康度进展报告任务

---

## 一、现象

文博 7-20 16:38 让我"更新 Wiki 健康度提升的进展"。我在查 review report 路径时发现：

- `wiki/methodologies/process/wiki-review-report-20260716.md`（最后一份连续报告）
- `wiki/process/wiki-review-report-{20260717,0718,0719,0720}.md`（连续 4 天落到错目录）

**用户视角**："Wiki review report 从 7-16 起断了 4 天"。
**实际真相**：`wiki.review` cron 每天 03:30 都跑通（consecutiveErrors=0，state.status=ok），**只是报告落到了错目录**。

---

## 二、根因

`scripts/wiki_auto_review.py` 第 17 行常量配置漂移：

```python
WIKI_ROOT = Path("/Users/wenbo/Documents/project/Wiki/wiki")
REPORT_DIR = WIKI_ROOT / "process"  # ❌ 错位 · 应为 methodologies/process
STATS_FILE = REPORT_DIR / "wiki_stats.json"
```

| 时间 | REPORT_DIR 值 | 实际落点 |
|:---|:---|:---|
| ~7-16 及之前 | `wiki/methodologies/process/`（历史 report 实证）| `methodologies/process/` ✅ |
| 7-17 → 7-20 | `wiki/process/`（脚本被改）| `wiki/process/` ❌ |

**漂移点未在 git log 中找到精确 commit**——但从 7-19 16:48 新建 `wiki/process/` 目录、7-17 08:52 第一份错位 report 推断：本次漂移发生在 **7-17 当天某次脚本编辑**。

---

## 三、修复（18:25 CST 完成）

| 步骤 | 动作 | 状态 |
|:---|:---|:---:|
| 1 | 备份脚本：`wiki_auto_review.py` → `wiki_auto_review.py.bak.20260720_1822` | ✅ |
| 2 | 修常量：`REPORT_DIR = WIKI_ROOT / "methodologies" / "process"` + 注释 L-N 治本 | ✅ |
| 3 | 移动 4 份错位 report：`wiki/process/wiki-review-report-{17,18,19,20}.md` → `wiki/methodologies/process/` | ✅ |
| 4 | 移动 `wiki_stats.json` 同步 | ✅ |
| 5 | 删除空目录 `wiki/process/`（避免再歧义） | ✅ |
| 6 | 端到端验证：手动跑一次 `wiki_auto_review.py` | ✅ 新 report 落 `methodologies/process/` |

**端到端验证结果**（7-20 18:25 实跑）：

| 维度 | 7-20 03:32（错位旧跑）| 7-20 18:25（修复后新跑）|
|:---|:---:|:---:|
| 总页面数 | 1747 | 1785（+38）|
| 孤立页面 | 1648 | 1686（+38）|
| 过时页面 | 15 | 15（持平）|
| 死链 | 368 | 368（持平）|
| 空目录 | 0 | **1** ⚠️ 新增 1 个 |
| 健康度 | 75/100 | 70/100（-5）|

⚠️ **新发现**：跑两次结果有小幅漂移——空目录从 0 → 1（需后续核查：是不是 7-20 新建了空目录？或 rglob 时序问题？）

---

## 四、教训（L-N · 7-20 治本）

### L-（新增）: 脚本路径常量必须写注释 + git commit 时必 cite

| # | 铁律 |
|:---:|:---|
| 1 | 修改 `Path(...)` 常量时**必须加注释**（含修改原因 + INC 编号），下个维护者立刻看到 |
| 2 | 任何修改 `wiki_auto_review.py` 的 commit message **必带 INC 编号**（如 "fix: REPORT_DIR 漂移 INC-2026-07-20-001"）|
| 3 | **路径漂移属于"silent failure"**：cron ok、report 生成、只是落错目录——下次必须 cron 加 `--output-as` 检查落点路径 |
| 4 | 修一类必 grep 全集（**L-16 治本**）：已确认仅 REPORT_DIR 一处错位，其他 WIKI_ROOT 派生路径一致 |

### L-49 族系扩展

| 教训族 | 主题 | 关联 INC |
|:---:|:---|:---|
| L-49 | cron edit 必看 argv 完整 JSON | INC-002 |
| L-49.5 | argv 必查脚本路径存在性 | INC-005 |
| L-49.6 | cron cleanup 决策树（4 类 + 4 动作）| INC-006 |
| L-49.7 | INC 报告必加 enabled/disabled tag 区分 | INC-007 |
| L-49.8 | ID 引用必完整（grep 原文 + 长度校验）| INC-005 补完 |
| **L-49.9** | **脚本路径常量漂移 silent failure（cron ok ≠ 落点对）** | **INC-2026-07-20-001** |

---

## 五、关联产物

| 路径 | 大小 | 状态 |
|:---|:---:|:---:|
| `/Users/wenbo/Documents/project/Wiki/scripts/wiki_auto_review.py` | 17573B（+18B · 加注释）| ✅ 已修 |
| `/Users/wenbo/Documents/project/Wiki/scripts/wiki_auto_review.py.bak.20260720_1822` | 17555B | ✅ 备份保留 |
| `/Users/wenbo/Documents/project/Wiki/wiki/methodologies/process/wiki-review-report-{20260717,18,19,20}.md` | 5939/6133/6129/5647B | ✅ 已迁 |
| `/Users/wenbo/Documents/project/Wiki/wiki/methodologies/process/wiki_stats.json` | 275B | ✅ 已迁 |
| `/Users/wenbo/Documents/project/Wiki/wiki/process/`（错位目录）| — | ✅ 已删 |
| `/Users/wenbo/Documents/project/Wiki/wiki/methodologies/process/wiki-health-improvement-20260714-20260720.md` | 待写 | ⏳ B 步骤 |

---

## 六、待办（24h 内 verify）

| 节点 | 动作 |
|:---|:---|
| **7-21 03:30** | cron 自动跑一次，验证 report 落到 `methodologies/process/`（不靠人盯）|
| 7-21 09:00 | 跑完后 `ls -la` 验证 + wiki.health cron 同步健康度 |
| 7-21 18:00 | 如一切正常，close INC（升级为 lesson L-49.9 主条目）|

---

*🕵️ 尼克·弗瑞 · 神盾局局长 · 2026-07-20 18:25 CST · INC-2026-07-20-001 闭环*