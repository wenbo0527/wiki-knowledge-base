# L-46: Get笔记 API 认证格式 = Authorization: <key>，无 Bearer

> **创建时间**：2026-07-16 19:30 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-16-004
> **路径**: `Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-16-getnote-auth-no-bearer.md`（L-31 路径规范）

---

## 🎯 核心教训

**Get笔记 OpenAPI 的认证 ≠ 标准 OAuth Bearer 格式**——是 direct token。

```http
# ❌ 错（5 种错法）
Authorization: Bearer <key>
Authorization: <key>
X-API-Key: <key>
?api_key=<key>
POST body {"api_key":"<key>"}

# ✅ 正确（SKILL.md 明确）
Authorization: <key>          # 直接传 key，无 Bearer 前缀
X-Client-ID: <client_id>      # 额外必需的 header
```

**根因**：凭"业界通用 OAuth Bearer 模式"的印象假设，未读 `https://clawhub.ai/iswalle/getnote` 的 SKILL.md。

---

## 📚 完整 SKILL.md 关键点（来自 ClawHub）

### Base URL
```
https://openapi.biji.com
```
**所有 API 请求必须用此 Base URL**，不要用 `biji.com` 或其他地址。

### 认证 Headers
```http
Authorization: $GETNOTE_API_KEY    # 格式: gk_live_xxx
X-Client-ID: $GETNOTE_CLIENT_ID    # 格式: cli_xxx
```

**每次调用 API 前先检查 `$GETNOTE_API_KEY` 是否存在**。若不存在，提示用户运行 `/note config`。

### Scope 权限
- `note.content.read`（读取）
- `note.content.write`（写入）
- `note.recall.read`（搜索）

完整列表见 SKILL.md references/api-details.md。

### 笔记 ID 处理（重要！）
笔记 ID 是 **64 位整数 (int64)**，超出 JavaScript `Number.MAX_SAFE_INTEGER`，直接 `JSON.parse` 会**静默丢失精度**。

**正确做法**：始终把 ID 当字符串处理，在 `JSON.parse` 之前替换：

```javascript
const safe = text.replace(/"(id|note_id|parent_id|follow_id|live_id)"\s*:\s*(\d+)/g, '"$1":"$2"');
const data = JSON.parse(safe);
```

**Python / Go 等语言原生支持大整数，无此问题**。

### 安全规则
- 笔记数据属于用户隐私，不在群聊中主动展示笔记内容
- 若配置了 `GETNOTE_OWNER_ID`，检查 sender_id 是否匹配；不匹配时回复"抱歉，笔记是私密的，我无法操作"
- API 返回 `error.reason: "not_member"` 或错误码 `10201` 时，引导开通会员
- 创建笔记建议间隔 1 分钟以上，避免触发限流

### 反幻觉边界（严格禁止）
- ❌ 禁止编造 note_id（必须来自 API 响应）
- ❌ 禁止跳过轮询（链接/图片笔记返回 task_id 后必须轮询 `/task/progress`）
- ❌ 禁止伪造 API 响应（不得在未实际调用 API 的情况下告诉用户"已保存"）
- ❌ 禁止忽略错误码（API 返回 `success: false` 时必须处理，不得静默吞掉）
- ❌ 禁止混淆内链和分享链接：
  - `biji.com/note/{id}` = 内链（仅笔记主人可见）
  - `share_note/{id}` = 分享链接（公开可访问）

### 失败重试策略
- **异步任务失败**（链接/图片保存）：自动重试 1 次 → 二次失败停止
- **网络/服务错误**（5xx/超时）：等待 5s 后重试 1 次 → 附 `request_id` 报错
- **限流**（错误码 `10202` 或 HTTP 429）：读 `rate_limit.retry_after` 等待指定秒数 → 默认 10s

---

## 🛡 L-17 强化：第三方 Skill 必先 read SKILL.md

按 L-17 教训："写脚本前必 read 3 行示例"——我之前调用 Get笔记 API 时**未先 read SKILL.md**，凭印象写 `Authorization: Bearer <key>`，导致 401。

**新增强化**：

> **第三方 Skill / 任何 API 集成前必先 read 官方文档**（包括 SKILL.md / OpenAPI spec / references/）。
> 不要凭"业界通用模式"假设。

---

## 📝 应用 Checklist

下次调用 Get笔记 API 必做：

- [ ] **读 SKILL.md**（先搜索 ClawHub / Clawhub）
- [ ] `Authorization: <key>`（无 Bearer）
- [ ] `X-Client-ID: <client_id>`（额外 header）
- [ ] Base URL = `https://openapi.biji.com`
- [ ] 笔记 ID 处理：Python `int()` 安全，JS 需字符串保护
- [ ] API 返回 `success: false` 必 raise 不静默

---

## 🔗 关联

- **INC**: `inc_2026-07-16_004-getnote-auth-format-no-bearer.md`
- **Skill**: https://clawhub.ai/iswalle/getnote（v1.8.9）
- **调用**: 8 KB 已拉到（投资日记 / AI实践日志 / 数字社区 / 文博PM转型 / 消费金融 / 徒步 / 印象笔记 / 健康100年）

---

## 🆕 L-46 应用实例

```bash
# 正确调用
TOKEN=$(grep "^GETNOTE_API_KEY=" /Users/wenbo/.openclaw/workspace/agents/nick_fury/.getnote_env | cut -d '=' -f 2-)
CID=$(grep "^GETNOTE_CLIENT_ID=" /Users/wenbo/.openclaw/workspace/agents/nick_fury/.getnote_env | cut -d '=' -f 2-)

curl -H "Authorization: $TOKEN" \
     -H "X-Client-ID: $CID" \
     https://openapi.biji.com/open/api/v1/resource/knowledge/list
# HTTP 200 ✅
```

---

*版本: v1.0*
*创建时间: 2026-07-16 19:30 CST*
*🕵️ 尼克·弗瑞*
