# L-47: 第三方 Skill / API SKILL.md 必读（升级 L-17）

> **创建时间**：2026-07-16 19:30 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-16-004 + INC-2026-07-16-003 + L-46
> **路径**：`Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-16-third-party-skill-md-mandatory.md`

---

## 🎯 核心教训

**调用任何第三方 Skill / API 前必先 read 官方 SKILL.md / OpenAPI spec**——不能凭"业界通用模式"假设。

L-17（"脚本前必 read 3 行示例"）的**第三方升级版**：不仅读"已有数据 3 行"，还要读"SKILL.md 完整 API 描述"。

---

## 📚 INC-004 揭穿真根因（实例）

### 错误归因链（3 次归因都错）

| 错误归因 | 实际根因 |
|:---|:---|
| ❌ 第 1 次（19:14）："WAF bot 检测" | ❌ 错 |
| ❌ 第 2 次（19:21）："token 过期" | ❌ 错 |
| ✅ 第 3 次（19:30）：**"认证格式错（无 Bearer）"** | ✅ 真根因 |

**根本问题**：我**没在调用前 read SKILL.md**，凭"业界通用 Bearer"假设 写了 5 种错误格式，全部 401。

### 真凶：认证格式 ≠ 标准 OAuth Bearer

```http
# ❌ 我凭印象写的 5 种格式
Authorization: Bearer <key>     # ❌
Authorization: <key>           # ❌（仅差 Bearer）
X-API-Key: ***                 # ❌
?api_key=<key>                 # ❌
POST body api_key=***          # ❌

# ✅ SKILL.md 明确
Authorization: <key>           # ✅ 直接传 key，无 Bearer 前缀
X-Client-ID: <client_id>        # ✅ 额外必需的 header
```

---

## 🛡 L-47 应用规则

### 触发条件

任何时候满足以下任一条件**必先 read SKILL.md / 官方文档**：
1. 首次调用第三方 API（Get笔记 / Lark / Notion / Slack / 自定义）
2. 升级 / 修改第三方集成代码
3. 第三方 Skill 失败返回错误（**在 5 种猜错误前先 read SKILL.md**）
4. 凭印象写了 N 种调用方式全失败（说明 SKILL.md 有未读信息）

### read SKILL.md 的具体步骤（L-17 强化）

| 步 | 动作 |
|:---:|:---|
| 1 | 找到官方来源（ClawHub / OpenAPI / GitHub README / reference docs）|
| 2 | **read 完整 SKILL.md**（不止标题/简介）|
| 3 | 提炼 4 项关键信息：Base URL / 认证格式 / Scope / 错误码 |
| 4 | 写文档小抄到 `TOOLS.md` §3.1 一次性记录，下次不再查 |
| 5 | 第一次实际调用前 30 秒把认证格式 + base URL 对一遍 |

### ClawHub Skill 速查清单

```bash
# Step 1: 找 skill
curl "https://clawhub.ai/<owner>/<skill>" -A "Mozilla/5.0" | head -100

# Step 2: SKILL.md 关键 section 提取
# - ⚠️ Agent 必读约束
# - Base URL
# - 认证
# - Scope 权限
# - 反幻觉边界
# - 失败重试策略

# Step 3: 必须 reference 文档读全
ls https://clawhub.ai/<owner>/<skill>/references/
# 典型包含: api-details.md / 错误码.md / examples.md
```

### wiki_curated colllection 的元教训

INC-004 揭穿 search_api.py 报 `50085a6f-... does not exist` 也有类似根因：chroma.sqlite3 db 实际**完整（17718 embeddings）**，只是 `collection.count()` 元数据有 stale UUID cache。**只重启 search_api 即清 cache**。

但 chroma.sqlite3 内的 Wiki chunks.json 是 20949 个，含**完整 metadata**（doc_path / doc_title / product_domain），这才是知识源。

---

## ⚠️ 反模式（必须避免）

| 反模式 | 例子 | 后果 |
|:---|:---|:---|
| ❌ 凭"业界通用"假设 | "OAuth 一定用 Bearer" "API 一定有 /me 端点"| 5 种错格式全 401 |
| ❌ 只看 error 字符串 | "401 → token 过期" | INC-003 揭穿：实际是 auth format 错 |
| ❌ 不 read 第三方 skill 文档 | 直接 `import` + 调用 | 90% 时间浪费在猜格式 |
| ❌ 不沉淀 TOOLS.md | 每次调用都查文档 | 重复劳动 + 浪费 token |

---

## 🔗 关联教训族

| L-* | 标题 | 关系 |
|:---:|:---|:---|
| L-17 | 脚本前必 read 3 行示例 | 基础原则 |
| **L-47** | **第三方 Skill SKILL.md 必读** | L-17 的第三方升级版 |
| L-46 | Get笔记 auth format | L-47 的实际应用（Get笔记 SKILL.md 揭穿真根因）|
| L-45 | 报告必含真实状态 | L-47 的归零原则（凭印象错归因）|

---

## 📝 应用 Checklist

下次调用第三方 Skill / API 必做：

- [ ] **必先 read SKILL.md**（在 ClawHub / OpenAPI / GitHub）
- [ ] **必记录 4 项关键信息**到 TOOLS.md §3.X：
  - Base URL
  - 认证格式（注意区分 Bearer / 直接 token）
  - Scope 权限列表
  - 常见错误码
- [ ] **第一次调用前 30 秒对照**：认证格式 + Base URL
- [ ] **失败时不要仅凭 error 字符串归因**（L-45）：先 read SKILL.md 验证
- [ ] **5 种猜错前先 read**（L-47 的"红旗阈值"）

---

## 🆕 教训强化对照表

| 顺序 | L-17 | L-47 |
|:---|:---|:---|
| 触发 | 自己写新脚本 | 用第三方 Skill / 调第三方 API |
| read 什么 | 已有数据 3 行示例 | 官方 SKILL.md / OpenAPI spec |
| read 时机 | 写脚本前 | 调用前 5 min |
| 错误时 | 重新 read 数据 | 优先 read SKILL.md（如没读过）|

---

*版本: v1.0*
*创建时间: 2026-07-16 19:30 CST*
*🕵️ 尼克·弗瑞*
