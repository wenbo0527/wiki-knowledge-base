# L-49.9 · 脚本路径常量漂移 silent failure（cron ok ≠ 落点对）

> **类别**: 工程 / cron 运维
> **严重度**: 🟠 High（silent failure 4 天）
> **关联 INC**: INC-2026-07-20-001
> **发现日**: 2026-07-20
> **沉淀人**: 尼克·弗瑞 🕵️

---

## 一句话总结

**cron 跑通 ≠ 报告落点对**——任何 `Path(...)` 常量在脚本里被修改都可能引发"silent failure"，必须用注释 + commit + 验证三件套防漂移。

---

## 现象

`wiki.review` cron 7-17 ~ 7-20 连续 4 天跑通（consecutiveErrors=0），但报告全部落到 `wiki/process/` 而不是 `wiki/methodologies/process/`。用户视角看到的是"报告断档"，实际是"路径漂移"。

---

## 根因（双层）

1. **直接原因**：`scripts/wiki_auto_review.py` 第 17 行 `REPORT_DIR = WIKI_ROOT / "process"`（漂移后值），应为 `WIKI_ROOT / "methodologies" / "process"`
2. **深层原因**：
   - 该常量**无注释**——下一次维护者无法一眼判断"这路径对不对"
   - 修改 commit message **不带 INC 编号**——git log 找不到精确漂移点（推断漂移发生在 7-17 当天某次编辑）
   - **没有任何验证机制**检查"cron ok + 报告落到正确位置"——这两件事在 L-49 族系里是独立的

---

## 治本（3 件套）

| # | 治本动作 | 实施 |
|:---:|:---|:---:|
| 1 | 修常量 + **加注释（含 INC 编号）** | ✅ 7-20 18:25 |
| 2 | 移动错位 report（4 份）+ 删除错位目录 | ✅ 7-20 18:25 |
| 3 | 端到端验证：手动跑一次脚本 + 检查落点 | ✅ 7-20 18:25 |
| 4 | **下个 cron 自动验证（7-21 03:30）** | ⏳ 24h verify |

---

## 3 条新铁律

| # | 铁律 | 反例 |
|:---:|:---|:---|
| **1** | 任何 `Path(...)` 常量修改**必须加注释**（"修改原因 + INC 编号"），下次维护者一眼看到 | 7-17 漂移后无注释，文博 7-20 才发现 |
| **2** | 修改 cron argv 指向脚本的 commit message **必带 INC 编号**（如 "fix: REPORT_DIR 漂移 INC-2026-07-20-001"）| 7-17 漂移 commit 找不到精确点 |
| **3** | **任何 cron 修完后 24h 内必 verify 落点**（不只看 cron.ok=ok）| L-49 族系只验 cron argv，不验产物路径 |

---

## L-49 族系扩展（6 层）

```
L-49    cron edit 必看 argv 完整 JSON             (INC-002 · 7-15)
L-49.5  argv 必查脚本路径存在性                    (INC-005 · 7-17)
L-49.6  cron cleanup 决策树（4 类 + 4 动作）       (INC-006 · 7-17)
L-49.7  INC 报告必加 enabled/disabled tag 区分    (INC-007 · 7-17)
L-49.8  ID 引用必完整（grep 原文 + 长度校验）      (INC-005 补完 · 7-17)
L-49.9  脚本路径常量漂移 silent failure 治本       (INC-2026-07-20-001 · 7-20)  ← NEW
```

**族系本质**：从"配置写对" → "路径存在" → "清理决策" → "报告精度" → "标识精度" → **"产物落点对"**——逐层把 cron 运维从粗放到精确。

---

## 防退化机制

| 触发 | 检测 | 修复 |
|:---|:---|:---|
| **每日 03:30 cron 自动跑后** | `ls -la wiki/methodologies/process/wiki-review-report-$(date +%Y%m%d).md` | 若不存在 → 发告警飞书 |
| **每周日 22:00 cron health check** | `sunday_cron_health_check.py` 加 cron 产物路径校验 | 7-19 22:00 已跑通 |
| **任何 cron argv 修改** | 必带 INC 编号 + grep argv 含 REPORT_DIR 类常量 | 立即同步修 |

---

## 关联产物

| 类型 | 路径 |
|:---|:---|
| INC | `wiki/review-logs/incidents/2026-07/inc_2026-07-20_001-wiki-review-report-path-drift-4d-vacuum.md` |
| 修复脚本 | `scripts/wiki_auto_review.py`（第 17 行 + 注释）|
| 备份 | `scripts/wiki_auto_review.py.bak.20260720_1822` |
| 移动文件 | 4 份 report + 1 stats.json → `methodologies/process/` |
| 进展报告 | `methodologies/process/wiki-health-improvement-20260714-20260720.md` |

---

*🕵️ 尼克·弗瑞 · 神盾局局长 · 2026-07-20 18:25 CST · L-49.9 治本沉淀*
*待 7-21 03:30 cron 自动 verify 后 close*