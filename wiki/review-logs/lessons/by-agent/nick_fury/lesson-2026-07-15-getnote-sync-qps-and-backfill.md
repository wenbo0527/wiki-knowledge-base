---
title: lesson 2026 07 15 getnote sync qps and backfill
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# L-41: GET 笔记入库必须 QPS 控制 + 拉全量 + KB 价值评估

> **教训族**: INC-2026-07-15-006 治本  
> **类别**: 同步链路 / QPS 限流 / 拉全量 / KB 价值评估  
> **创建**: 2026-07-15 14:46  
> **关联**: INC-2026-07-15-006 / L-32 / L-37 / L-40

---

## 反例（7-15 14:45 揭穿前）

`getnote_ej9_to_wiki.py` v2.0（7-15 11:00 改造）跑了 14 分钟：

```
fetch=187  write=115  skip=63  fail=9  HTTP 429 限流
```

**3 个揭穿**：

### 🔴 QPS 限流：9 个 HTTP 429 失败

GET 笔记 API 限制 ~5 qps / 2s（v1.0 备份`scripts/_backup_before_20260701/getnote_to_wiki.py`注释）

v1.0 备份实现：
```python
REQUEST_DELAY = 1.0  # 每条API请求间隔秒
BATCH_DELAY = 5.0    # 每批笔记间隔秒（跨 KB 安全间隔）
```

**v2.0 改造丢失这两个参数**！

### 🔴 拉全量：只 fetch 第 1 页（前 20 条）

实际 KB 笔记数 vs 拉取数：

| KB | API 总数 | 拉取 | 比例 |
|:---|:---:|:---:|:---:|
| K0BVyZM0 (AI 实践日志) | 504 | 20 | **4%** |
| EJlOEG10 (数字社区) | 183 | 20 | **11%** |
| 2eYxaj0z (快刀青衣) | 1,258 | 20 | **2%** |
| n3EGyBd0 (印象笔记) | 2,196 | 20 | **1%** |
| JawjeBlY (2026 WAIC) | 487 | 20 | **4%** |

**总：~5,000 笔记只拉 187 (3.7%)**

### 🔴 KB 价值评估：WAIC 487 几乎全是 PR 稿

WAIC KB 样本：
- "中国移动 AI 时代" (PR)
- "中国太保 WAIC 2025" (PR)
- "特斯拉 WAIC 2025" (PR)
- "扫描全能王 WAIC" (PR)
- "COLMO 家电智能体" (PR)
- "中远海运亮相 WAIC" (PR)

**几乎全是 2025 展商动态**，不含真正 2026 技术内容。

## 正例（7-15 14:46 揭穿后）

### 4 件事必做

#### 1. QPS 控制（治本 HTTP 429）

```python
import time

REQUEST_DELAY = 1.0  # 每条请求 1 秒（5 qps/2s 安全）
BATCH_DELAY = 5.0    # 跨 KB 间隔

# fetch_kb_notes 内：
data = fetch_url(url, headers)
time.sleep(REQUEST_DELAY)  # 每次请求后 sleep

# main 内：
for kb_id, category in KB_ROUTING.items():
    notes = fetch_kb_notes(env, kb_id)
    time.sleep(BATCH_DELAY)  # KB 之间 sleep
```

#### 2. 拉全量（治本"只看到 20 篇"）

```python
def fetch_kb_notes(env, kb_id):
    """拉知识库所有笔记（分页至 has_more=False）"""
    notes = []
    for page in range(1, 50):  # max 50 页
        url = f"...?topic_id={kb_id}&page={page}&size=100"
        data = fetch_url(url, headers)
        batch = data.get("data", {}).get("notes", [])
        if not batch:
            break
        notes.extend(batch)
        if not data.get("has_more", False):
            break
    return notes
```

**改 `size=100` + 循环至 `has_more=False`**

#### 3. KB 价值评估（先 sample 后入库）

```bash
# 先 sample 5-10 篇
for kb_id in <新 KB>; do
  curl -s "https://openapi.biji.com/open/api/v1/resource/knowledge/notes?topic_id=$kb_id&page=1" \
    -H "Authorization: $GETNOTE_API_KEY" \
    | python3 -c "import json,sys; [print(n.get('title','')) for n in json.load(sys.stdin).get('data',{}).get('notes',[])]"
done
# 评估：标题是否含 "技术 / 模型 / 框架" 等关键词，是否是 PR 稿
```

#### 4. 失败必 raise（L-32 已治本，保留 v2.0 设计）

## 入库价值评估（7-15 14:45 实测）

| KB | written | 平均质量 | 价值 |
|:---|:---:|:---|:---:|
| **yYvRWqaY (文博 AI 转型)** | 18 | 10K 字符 | ⭐⭐⭐⭐⭐ 战略 |
| **2eYxaj0z (快刀青衣)** | 18 | 2-5K 字符 | ⭐⭐⭐⭐⭐ 战略 |
| **EJlOEG10 (数字社区)** | 20 | 8-30K 字符 | ⭐⭐⭐⭐⭐ 业务 |
| **K0BVyZM0 (AI 实践)** | 20 | 3-10K 字符 | ⭐⭐⭐⭐⭐ |
| **EJ9zwkln (高质量人类谈话库)** | 12 | 6-12K 字符 | ⭐⭐⭐⭐⭐ |
| 04p8P2m0 (投资日记) | 11 | 2-6K 字符 | ⭐⭐⭐⭐ |
| 7JbLLvYe (消费金融) | 11 | 7K 字符 | ⭐⭐⭐⭐ |
| n3EGyBd0 (印象笔记) | 0 | —— | 🟡 失败 + 文博排除 |
| Y2mRx3En (江浙沪徒步) | 0 | —— | 🟡 低价值 |
| oJOA1ENY (健康生活) | 0 | —— | 🟡 低价值 |
| **JawjeBlY (WAIC)** | 0 | PR 稿为主 | 🔴 价值待评估 |

**总**：**115 篇高价值入库**（9 个失败待 retry）

## 关联教训

- **L-32** (同步脚本 3 必检) — 失败必 raise（已治本）
- **L-37** (报告必 verify API) — 揭穿 QPS + 拉全量 + KB 价值
- **L-40** (订阅 KB 必用 `getnote kbs-sub`) — KB ID 准确
- **L-41** (GET 笔记入库 4 件事) — **本条**

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每次新 KB** | sample 5-10 篇评估 | 手动 |
| **每日 21:00** | c3 cron 检查 consecutiveErrors | c3 |
| **每周日 22:00** | 入库质量报告 | 手动 |

---

*Lesson 完稿: 2026-07-15 14:46 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-006 ✅ 115 篇入库 · QPS + WAIC 揭穿*
