---
title: lesson 2026 07 15 local docs rag pipeline
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# L-39: 本地文档 RAG 化 4 步 SOP

> **教训族**: INC-2026-07-15-004 治本  
> **类别**: 本地文档 / RAG 化 / 跨层 metadata  
> **创建**: 2026-07-15 11:08  
> **关联**: INC-2026-07-15-004 / L-31 / L-32 / L-37

---

## 反例（7-15 11:06 揭穿前）

**文档仓库 6 项目 976 个 .md 几乎 0% RAG 化**：

- ❌ 落盘到 `Documents/文档仓库/`（独立目录，与 Wiki 不通）
- ❌ 无 `wiki/topics/local-docs/` 镜像
- ❌ 无 `_index.md` 索引
- ❌ 无跨层 metadata（`source_layer: local` 缺失）
- ❌ 无 RAG ingest
- ❌ 无召回率 verify

**业务影响**：
- 文博决策时查不到项目过程产物
- 行业研究（苏银 5 篇 + MarketAgent 2 篇）只在 Tony 团队偶尔手动 search
- 数字社区项目 760 篇过程文档全部"沉睡"

## 正例（7-15 11:06 后 · 第一波落盘）

**4 步 SOP**：

### Step 1: 落盘到 `wiki/topics/local-docs/<project>/`（镜像 `文档仓库/<project>/`）

```bash
# 例：行业研究 7 篇
mkdir -p /Users/wenbo/Documents/project/Wiki/wiki/topics/local-docs/行业研究
cp -r "/Users/wenbo/Documents/文档仓库/行业研究/"* \
      /Users/wenbo/Documents/project/Wiki/wiki/topics/local-docs/行业研究/
```

### Step 2: 写 `_index.md`（项目总览 + 跨层 metadata）

```yaml
---
title: 本地文档库 · 索引
source_layer: local
verified_at: 2026-07-15 11:06
agent_id: nick_fury
---

# 本地文档库 · 索引
## 6 项目总览
| 项目 | .md 数 | 价值 | RAG 化 |
|:---|:---:|:---:|:---:|
```

### Step 3: RAG ingest（复制完成后 trigger）

```bash
# Tony 团队的 RAG ingest 工具
python3 scripts/ingest_wiki_docs.py --path wiki/topics/local-docs/行业研究
```

### Step 4: 召回率 verify（curl /search 4 个查询 ≥ 0.6 阈值）

```bash
for q in "苏银 BI 平台" "苏银营销套件" "MarketAgent 多 Agent 协作" "本地文档 RAG 化"; do
  curl -s -X POST http://localhost:8082/search \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"$q\", \"top_k\":3, \"mode\":\"hybrid\"}"
done
# 期望: score ≥ 0.6 · 本波实测 1.0/1.0/0.974
```

## 跨层 metadata 规范（必填）

每个本地文档 frontmatter **必须**含：

```yaml
---
title: 文档标题
source_layer: local           # 必填：wiki / getnote / local
source_path: 文档仓库原路径    # 必填：可追溯
product_domain: PD-RESEARCH   # 项目域（PD-RESEARCH / PD-PM / ...）
verified_at: 2026-07-15 11:06  # 必填：verify 时间
agent_id: nick_fury            # 必填：负责 agent
status: published              # draft / review / published / archived
---
```

## 4 阶段 RAG 化路线图（Nick 团队）

| 阶段 | 项目 | 优先级 | 预估 |
|:---:|:---|:---:|:---:|
| ✅ 第一波 | 行业研究 7 篇 | ⭐⭐⭐⭐⭐ | 30min ✅ |
| 🟠 第二波 | cloud-agent-team 20 + AI team 3 = 23 篇 | ⭐⭐⭐⭐ | 4h |
| 🟡 第三波 | 产品管理项目 146 篇 | ⭐⭐⭐ | 8h |
| 🟢 第四波 | 个人网站 40 + 数字社区 760 = 800 篇 | ⭐⭐ | 持续 |

## 关联教训

- **L-31** (路径铁律：本地文档落盘到 wiki/topics/local-docs/，不进 review-logs/)
- **L-32** (同步脚本 3 必检：本地文档 ingest 不 hardcode + 必对账)
- **L-37** (报告必 verify 实时 API：召回率 4 查询 ≥ 0.6)
- **L-39** (本地文档 RAG 化 4 步 SOP) — **本条**

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| 每次新本地文档 | 4 步 SOP 落盘 | 手动 |
| 每周日 22:00 | c3 cron 加"本地文档 RAG 化进度"检查 | c3 cron |
| 每月末 | 文档仓库 vs wiki/local-docs 对账 | 手动 |

---

*Lesson 完稿: 2026-07-15 11:08 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-004 ✅ 第一波 7 篇落盘 · 召回率 1.0*
