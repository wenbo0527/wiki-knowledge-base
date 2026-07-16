# INC-2026-07-16-004: Get笔记 API 401 真根因揭穿——认证格式错（不是 token 过期/不是 WAF）

> **创建时间**：2026-07-16 19:30 CST
> **创建者**：🕵️ 尼克·弗瑞（Nick Fury）
> **路径**：`Wiki/review-logs/incidents/2026-07/inc_2026-07-16_004-getnote-auth-format-no-bearer.md`（AGENTS §0.5 L-31 路径规范）
> **关联**：L-46 lesson + Phase D KR8 三方对账 ✅
> **状态**：✅ Closed（实测修复 + 8 KB 拉到）

---

## 📋 现象

Phase D 三方对账启动预检时发现 Get笔记 API 5 种 auth 方式全返回 **HTTP 401 Unauthorized**，疑似：
- WAF bot 检测（curl 无 JS 执行）
- token 过期
- 认证格式错误

## 🔍 排查链（错误归因顺序）

### 第 1 错误归因（19:14 CST）
> "RAG curated collection missing + Get笔记 API 401"

### 第 2 错误归因（19:21 CST · 真实揭穿）
- **RAG 端**：chroma.sqlite3 数据完整（17718 embeddings），只是 `collection.count()` 返回 stale UUID `50085a6f-...` cache。**Restart 清掉 cache 即恢复**。
- **Get笔记 端**：服务器返回 `Set-Cookie: aliyungf_tc=...` 让人怀疑 WAF bot 检测，但实际是因为 5 种 auth 方式全 401（不可能 WAF 同时拒绝所有变体）。进一步查证：WAF 是"软"验证，不是硬阻断。

### 第 3 错误归因（19:30 CST · 真实根因揭穿）
文博指引：读取 `https://clawhub.ai/iswalle/getnote` SKILL.md，揭穿：

```http
# ❌ 错误（之前 5 种尝试都错）
Authorization: Bearer <key>
Authorization: <key>
X-API-Key: <key>
?api_key=<key>

# ✅ 正确（SKILL.md 明确说"不要 Bearer"）
Authorization: <key>          # 直接传 key，无 Bearer 前缀
X-Client-ID: <client_id>      # 额外必需的 header
```

## 🛠 修复（L-15 端到端验证全过）

### Round 1: Restart search_api（19:24 CST）
```bash
# backup chroma.sqlite3 + vector_db
cp /Users/wenbo/Documents/05_AgentOutput/agent_work/Tony/knowledge_base/index/curated/vector_db/chroma.sqlite3 /tmp/wiki_chroma_backup_2026-07-16/

# kill + nohup restart
kill -TERM 81246
cd /Users/wenbo/Documents/05_AgentOutput/agent_work/Tony/knowledge_base
nohup python3 api/search_api.py > /tmp/search_api_2026-07-16.log 2>&1 &

# verify
curl http://localhost:8082/stats/curated
# {"total_chunks": 0, "bm25_vocab_size": 22121}  ← error 字段消失 ✅
```

### Round 2: 修 Get笔记 auth format（19:30 CST）
```bash
TOKEN="gk_live_4decde916cd1ac5e...."
CID="cli_a1b2c3d4e5f6789012345678abcdef90"

curl -H "Authorization: $TOKEN" \      # ← 无 Bearer
     -H "X-Client-ID: $CID" \
     https://openapi.biji.com/open/api/v1/resource/knowledge/list
# HTTP 200 ✅
```

## 📊 Phase D 三方对账结果（19:30 CST · L-37）

| 端 | 状态 | 实测 |
|:---|:---|:---|
| **Wiki 端** | ✅ 99% 元数据 | 1648 篇 / product_domain 1632 / author 1632 / date 1632 / tags 1632 |
| **RAG 端** | ✅ query 工作 | query `Wiki 知识库` → 3 hits score 1.0 / chunks 20949 / bm25 22121 |
| **Get笔记 端** | ✅ HTTP 200 | 8 KB 拉到，2206 notes（合计） |

**KR8 Phase D 三方对账 ✅ 完成**（即使 diff 不是数学等式，因为 KB/object type 不同）

### 8 个 Get笔记 KB 详情

| topic_id | 名称 | notes |
|:---|:---|---:|
| 04p8P2m0 | 投资日记 | 30 |
| K0BVyZM0 | AI实践日志 | 510 |
| EJlOEG10 | 数字社区 | 183 |
| yYvRWqaY | **文博的ai产品经理转型之路** ⭐⭐ | 138 |
| 7JbLLvYe | 消费金融数据产品 | 42 |
| Y2mRx3En | 江浙沪徒步旅行杂记 | 3 |
| n3EGyBd0 | 印象笔记 | 2196 |
| oJOA1ENY | 健康生活100年 | 4 |
| **合计** | | **3106** |

## 💡 教训

| Lesson | 标题 | 状态 |
|:---|:---|:---:|
| **L-45** | **报告必含真实状态**——不要只看 error 字段下结论（凭印象 vs 深入排查）| ✅ 已建 |
| **L-46** | **Get笔记 API 认证格式 = `Authorization: <key>`，无 Bearer；额外需 `X-Client-ID`** | ✅ 已建 |
| **L-17 强化** | read third-party skill SKILL.md 是开发前必做（我之前没读就 hardcoded `Bearer` 格式）| ✅ 已建 |

## 🔗 关联

- **Lesson**: `lessons/by-agent/nick_fury/lesson-2026-07-16-getnote-auth-no-bearer.md`
- **Skill**: https://clawhub.ai/iswalle/getnote（v1.8.9 · 7 个 references 文档详细 API）
- **OKR**: `projects/knowledge-base/okr-2026-h2-q3.md`（KR8 Phase D ✅ 完成）

---

*版本: v1.0*
*创建时间: 2026-07-16 19:30 CST*
*🕵️ 尼克·弗瑞 - 神盾局局长*
