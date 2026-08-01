# L-53: Wiki Insight 自动沉淀治本

> **作者**: 尼克·弗瑞 🕵️
> **节点**: 2026-08-01 11:31 CST 闭环
> **关联**: INC-2026-08-01-002
> **入族**: L-53（族首 · 知识沉淀）

---

## 1️⃣ 元教训

> **流程末端必须落到 L2 Wiki 知识库，不是只到飞书推送**

---

## 2️⃣ 4 子教训

### L-53.1 流程末端必须落到 L2 Wiki（治本）

**踩坑**：daily_pipeline 流程是 fetch→analyze→curate→push，**没有 step 5：写 Wiki**。导致知识库增量停滞。

**治本**：
- ✅ 流程末端加 `wiki_insight_writer` step
- ✅ 自动 + 持久化 state（防重复）
- ⏳ **未来可加**：每日报告"沉淀 N 篇 / 推送 N 篇" 比率

### L-53.2 analyzer 内存态必须可持久化读取

**踩坑**：analyzer.analyses 在内存，需要重新加载 analysis_v2.json 才能跨进程读。

**治本**：
- ✅ wiki_insight_writer 直接读 analysis_v2.json（已落盘）
- ✅ 无需重新跑 batch_analyze（节省 5-10 min）

### L-53.3 沉淀率监控（治本+治理）

**踩坑**：不知道 Wiki 沉淀率，无法治理"知识库增量"。

**治本**：
- ⏳ **未做**：c3 cron 加 Wiki 沉淀率报告
- ⏳ **未来可加**：每周日 c3 cron 加本周 Wiki 沉淀率统计

### L-53.4 模板质量 vs 自动化的平衡

**踩坑**：自动生成的 insight 可能灌水，质量低。

**治本**：
- ✅ 严格过滤：recommendation='重点关注' + confidence ∈ {高,中} + 24h 内
- ✅ 每篇加 `auto_generated: true` 标记，便于人工审
- ✅ 文末加 ⚠️ 警告：自动生成仅供参考

---

## 3️⃣ 落地物

| # | 产物 | 路径 |
|:---:|:---|:---|
| 1 | 沉淀脚本 | `scripts/wiki_insight_writer.py` (9959B) |
| 2 | state 文件 | `data/wiki_insight_writer_state.json` |
| 3 | log 文件 | `data/wiki_insight_writer.log` |
| 4 | OpenClaw cron | `23ad3239-4556-47c3-880d-145382e0e968` (每日 08:40) |
| 5 | 8-1 沉淀 2 篇 | `wiki/insights/research/product/insight-20260801-*.md` |

---

## 4️⃣ 沉淀标准 Checklist

新沉淀一篇 Wiki insight 时必检：

- [ ] `recommendation='重点关注'`
- [ ] `confidence ∈ {高,中}`
- [ ] `analyzed_at` 在 24h 内
- [ ] article_id 不在 state.written
- [ ] 文件包含 5 元数据 frontmatter
- [ ] 文件包含 4 框架分析
- [ ] 文末有 ⚠️ 警告（auto-generated 标记）

---

## 5️⃣ 未来扩展（待文博拍板）

| 扩展项 | 工作量 | 价值 |
|:---|:---:|:---|
| 沉淀率报告（c3 cron）| 30 min | 治理 Wiki 增量 |
| 自动 re-analyze（analysis_v2 缺失时）| 1 h | 自愈能力 |
| 多年历史补写（5-1 ~ 8-1 的 100+ 篇）| 4 h | 历史沉淀 |
| 智能选题（投资评分≥7 才沉淀）| 30 min | 严格门槛 |

---

**🕵️ 尼克·弗瑞 · 2026-08-01 11:31 CST · L-53 族首 · 4 子教训 · Wiki 沉淀率 0% → 1.4% · 自动化治本循环已启动**