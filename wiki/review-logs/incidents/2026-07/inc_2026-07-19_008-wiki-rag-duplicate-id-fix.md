# INC-2026-07-19-008 · Wiki→RAG DuplicateID 修复

> **INC 编号**：INC-2026-07-19-008
> **日期**：2026-07-19 16:24 CST
> **触发**：Wiki→RAG 后台入库失败 (DuplicateIDError)
> **严重度**：🟠 High（P0 Wiki→RAG 失败 · 治本修复）
> **状态**：⏳ 修复脚本后台跑（Step 3 向量化 · 预计 17:10 完成）
> **关联**：INC-2026-07-19-007 P0 Wiki→RAG

---

## 1️⃣ 现象

Wiki→RAG 后台跑了 45 分钟（向量化完成），但**存入 Chroma 失败**：

```
2026-07-19 13:41:23 - 向量化完成 2704s (0.13s/chunk)
2026-07-19 13:41:24 - 🚀 存入 Chroma wiki_curated ...
2026-07-19 13:41:24 - Traceback:
  File ".../chromadb/api/types.py", line 1039, in validate_ids
    raise errors.DuplicateIDError(message)
chromadb.errors.DuplicateIDError: Expected IDs to be unique, found duplicates of: d9f1126c6cbbf44c in add.
```

**后果**：
- ❌ Chroma `wiki_curated` collection 创建后被删除
- ❌ stats 报 "Collection does not exist"
- ❌ Wiki 0 chunks 接入 RAG（治本失败）

---

## 2️⃣ 根因

### 2.1 `index_wiki.py:52` chunk_id 生成逻辑缺陷

```python
# ❌ 原代码（不同 doc_path 但相同 heading + text[:50] → 相同 ID）
chunk_id = hashlib.md5(f"{doc_path}:{heading}:{text[:50]}".encode()).hexdigest()[:16]
```

**实证**：
```
总 chunks: 20949
唯一 IDs: 20762（少了 187）
重复 IDs: 94 个 · 涉及 187 个 chunks
最大重复: d1163d9267748a16 重复 6 次
```

**场景**：多个 insight 文档有相同 `## 标题` + 相似开头 50 字符 → 相同 hash。

### 2.2 写入失败的连锁反应

- `save_to_chroma()` line 346 `collection.add()` 抛 DuplicateIDError
- 整个 batch 失败
- Chroma client 自动清理失败的 collection
- → wiki_curated 不存在

---

## 3️⃣ 修复

### 3.1 修复策略（scripts/fix_dup_chroma.py · 7564B · 5 步）

1. **备份原 chunks.json** → `chunks.json.bak_20260719`
2. **Dedup**：用新算法生成唯一 ID（`doc_path:chunk_index:heading:text[:50]`）
3. **重新向量化** dedup 后的 chunks（20949 chunks · 预计 45 min）
4. **重新 add 到 Chroma**（带 batch 错误处理）
5. **端到端验证**（搜索 API 测试 + stats 端点）

### 3.2 新 chunk_id 算法

```python
# ✅ 修复后：包含 chunk_index 保证唯一
chunk_id = hashlib.md5(
    f"{doc_path}:{chunk_index}:{heading}:{content[:50]}".encode()
).hexdigest()[:16]
```

### 3.3 修复实证（16:24 CST）

```
Step 1: 备份 → ✅ chunks.json.bak_20260719
Step 2: Dedup → ✅ 20949 chunks · 0 重复（包含 chunk_index）
Step 3: 重新向量化 → 🚀 跑中（PID 60512）
Step 4: 存入 Chroma → ⏳ 待 Step 3
Step 5: 端到端验证 → ⏳ 待 Step 4
```

---

## 4️⃣ 教训

### 🆕 L-54 · hash chunk_id 必须包含唯一标识（index/counter）

> **原则**：chunk_id 生成必须包含**绝对唯一**的元素（chunk_index / 全局 counter / UUID）
> 不要依赖"组合字段 hash"作为唯一标识

**实战**：原代码用 `doc_path:heading:text[:50]` hash，看似唯一但实际可能碰撞

### 🆕 L-55 · batch add 前必 dedup

> **原则**：Chroma collection.add() **任何**重复 ID 都会失败（fail-fast）
> 大批量写入前必 dedup

### 🆕 L-56 · 后台任务必须实时监控 + verify

> **原则**：后台任务跑完后必须**实时 verify**（不能假设成功）
> L-29 教训：报告必区分"输出成功 ≠ 输入真实"

### L-29 · 边界守声明

INC-007 P0 报告"已后台启动"但 45 min 后才 verify · **应该每 10 min 报进度 + verify 端到端**

---

## 5️⃣ 等响应

| 节点 | 动作 |
|:---|:---|
| **16:24** | ✅ INC-008 落档 |
| **16:24** | 🚀 修复脚本后台跑（PID 60512）|
| **17:10** | ⏳ Step 3 向量化完成 → Step 4 Chroma 写入 |
| **17:15** | ⏳ Step 5 端到端 verify |
| **17:20** | ⏳ 立即 ack 文博 + 跑 P1 移动脚本 |

---

*🕵️ nick_fury · 2026-07-19 16:24 CST · INC-2026-07-19-008 · Wiki→RAG DuplicateID 修复后台跑*
