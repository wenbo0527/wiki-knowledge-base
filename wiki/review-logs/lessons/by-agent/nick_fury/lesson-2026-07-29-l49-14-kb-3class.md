# lesson-2026-07-29-l49-14-kb-3class.md

> **教训编号**: L-49.14
> **触发事件**: 7-29 09:06 文博问「Get 笔记精选 能否区分 自写 vs 关注的知识库」
> **闭环时间**: 7-29 09:54 CST
> **关联 INC**: 无（用户需求改进，不是 INC）
> **关联 L-**: L-37（API 实测）· L-49.13（通用扫描原则）· L-15（端到端验证）· L-34（cron argv）
> **作者**: 尼克·弗瑞 🕵️

---

## 一、需求背景

文博 7-29 09:06 提出：
> "Get 笔记精选 是否有可能区分一下 是我自己写的还是 从知识广场 我关注的知识库获取的 我们是否可以重点关注 关注的知识库 我自己写的 或 记录的 我知道是什么"

核心诉求：**在推送中标注每条笔记的来源类型**，重点看「我写的」和「我关注的 KB 同步的」，跳过已知内容。

## 二、API 实测发现（L-37 治本）

### 2.1 KB 列表接口 `/resource/knowledge/list`
- 返回字段：`cover, created_at, description, id, name, scope, stats, topic_id, updated_at`
- **关键字段 `scope`**：区分 `DEFAULT`（11 个自有/添加的）vs `BOOKSPACE`（10 个知识广场的书）
- ❌ **无 `is_self` / `owner` / `is_subscribed` 字段**（API 不返回 owner 信息）

### 2.2 个人笔记流 `/note/list?since_id=0`
- 返回字段：`id, note_id, title, content, note_type, source, tags, topics, created_at, updated_at, ref_content`
- **关键字段 `source`**：5 种取值
  - `app` = App 内手动保存（**高置信度"我手写"**）
  - `knowledge` = 从 KB 同步来的副本
  - `wechat` = 微信公众号剪藏
  - `web` = 浏览器剪藏
  - `getnote_bu` = 商业版同步
- **新发现（7-29）**：`source=openapi` = 通过 API 同步的手写内容（如书草稿）

### 2.3 KB 下笔记接口 `/resource/knowledge/notes?topic_id=XXX`
- 返回字段：`note_id, title, content, note_type, tags, is_ai_generated, created_at, edit_time`
- ⚠️ **没有 `source` 字段**（无法在 KB 内判定笔记来源）

## 三、3 分类判定原则（L-49.14 治本）

### 3.1 笔记层（daily_note_scan.py · KB 视角）
| 分类 | 判定条件 | 置信度 |
|:---|:---|:---:|
| ⭐ 自手写 | `source in {"app", "openapi"}` AND `note_type in {plain_text, meeting, audio}` | 高 |
| 🔔 KB 同步副本 | `source == "knowledge"` | 高 |
| 📚 其他来源 | 公众号 / 网页 / 商业版 / `source=app + note_type=link` | 高（兜底）|

### 3.2 KB 层（getnote_ej9_to_wiki.py · 推送视角）
| 分类 | 判定条件 | 数据来源 |
|:---|:---|:---|
| ⭐ 自有 KB | `KB_META[kb_id]["is_self"] == True` | 硬编码白名单（API 不返回 owner）|
| 🔔 订阅 KB | `KB_META[kb_id]["is_self"] == False` | 硬编码白名单 |
| 📚 知识广场 | `scope == "BOOKSPACE"` 的 KB | API 实时（不参与 cron 扫描）|

### 3.3 ⚠️ 关键技术约束
- **`/knowledge/notes` API 不返回 source 字段**——不能在 KB 层判定"哪条是自写 vs 同步"
- **应对**：KB 层只分 ⭐self / 🔔sub（看 KB 归属），不细化到单条笔记粒度
- **替代方案**（未来需要时）：双 API 交叉（`/note/list` 取 source → `/knowledge/notes` 校验是否入库）改造量 ~5x

## 四、实施细节

### 4.1 daily_note_scan.py 改造
```python
# 新增 KB_META（带 scope + is_self + tier）
KB_META = {
    "K0BVyZM0": {"name": "AI实践日志", "tier": "⭐"},  # is_self=True
    "EJ9zwkln": {"name": "高质量人类谈话库", "tier": "🔔"},  # is_self=False
    ...
}

# 笔记 3 分类
HANDWRITE_TYPES = {"plain_text", "meeting", "audio"}
HANDWRITE_SOURCES = {"app", "openapi"}  # 7-29 加 openapi

for n in high_value:
    src = n.get('source', '')
    if src in HANDWRITE_SOURCES and n.get('note_type') in HANDWRITE_TYPES:
        bucket_self.append(n)        # ⭐
    elif src == 'knowledge':
        bucket_kb.append(n)          # 🔔
    else:
        bucket_other.append(n)       # 📚
```

### 4.2 getnote_ej9_to_wiki.py 改造
- KB_ROUTING 保留（路由逻辑不变）
- 新增 KB_META（重复定义 · TODO: 未来抽共享模块 `_getnote_meta.py`）
- `write_wiki_insight` 加 `kb_id` 参数 → frontmatter 加 `KB 等级` 行
- 推送消息按 tier 分类统计
- L-34 cron argv 不变（`getnote_to_wiki.sh` 调 `getnote_ej9_to_wiki.py`），自动生效

### 4.3 Wiki frontmatter 升级
```markdown
# {title}

> 来源: Get 笔记
> 知识库: {category} ({kb_name})
> KB 等级: ⭐self       # 新增
> KB ID: {kb_id}        # 新增
> 原始 ID: {note_id}
> 创建时间: {note_created_at}
> 同步时间: {now}

{content}
```

## 五、L-15 端到端验证（5 用例）

| # | 验证项 | 结果 |
|:---:|:---|:---:|
| 1 | `python3 -m py_compile` 两个脚本 | ✅ |
| 2 | dry-run / mock 跑通 + 真实跑 `fetch=191 write=0 skip=191 fail=0` | ✅ |
| 3 | 3 通道全成功（飞书/sessions_send/wiki）| ⏭️ cron 自动推送（非脚本直调）|
| 4 | 数据正确（fetched 数与 state 一致）| ✅ |
| 5 | 异常 raise（HTTP 429 不静默）| ✅ |

## 六、教训沉淀

### L-49.14.1：API 字段盘点先于逻辑改造
**陷阱**：拿到需求直接动手改代码
**治本**：先 curl 实测所有相关 API → 列出可用字段 → 再设计判定逻辑

### L-49.14.2：KB notes API 不返回 source 是硬约束
**陷阱**：以为能像 personal notes 流一样判定每条笔记来源
**治本**：KB 层只分 ⭐self / 🔔sub；笔记粒度判定走 `/note/list` 双 API 路径（改造量大，本期不做）

### L-49.14.3：硬编码白名单的合理性
**陷阱**：硬编码 `is_self` 觉得"不优雅"
**治本**：API 不返回 owner → 硬编码白名单是**唯一可靠方案**；只要标注"API 不返回"+ 留好更新入口（KB_META 字典）即可

### L-49.14.4：标签渲染要用 bucket 类别而非 source 字段
**陷阱（7-29 11:30 实测发现）**：
```python
# ❌ 错版：用 SOURCE_TAG 渲染 → source=app 但 note_type=link 错标 ⭐
src_tag = SOURCE_TAG.get(n.get('source', ''), '❓其他')

# ✅ 正版：用 bucket 自身标签（⭐ / 🔔 / 📚）
tag = label.split('（')[0].strip()
```
**治本**：分类标签 = bucket 决策结果，不混用原始字段

### L-49.14.5：3 分类改造要双脚本同步
**陷阱**：只改 daily_note_scan.py → getnote_ej9_to_wiki.py 还是旧格式
**治本**：Q1 = 两者都要改 → 一次同步改造（已在 7-29 09:54 完成）

## 七、未来 TODO（不阻塞）

- [ ] 抽 `_getnote_meta.py` 共享模块（两个脚本 KB_META 重复定义）
- [ ] 评估是否要把 Wiki frontmatter 升级为 YAML（更标准的 RAG 元数据）
- [ ] 探索 BOOKSPACE KB（10 个知识广场的书）的接入策略——目前不在 cron 扫描范围
- [ ] 验证 RAG 检索是否能用 `KB 等级` 字段做过滤（未来 query 时区分⭐ vs 🔔）

## 八、影响范围

| 改造项 | 范围 | 风险 |
|:---|:---|:---:|
| daily_note_scan.py 推送格式 | 21:00 飞书 | 🟢 仅 print 改动 |
| daily_note_scan.py 入库逻辑 | 入库到 AI实践日志/消费金融 | 🟢 **未改**（保持原 FIN_KW 路由）|
| getnote_ej9_to_wiki.py 推送格式 | 06:00 飞书 | 🟢 仅 print + frontmatter 改动 |
| getnote_ej9_to_wiki.py Wiki 写入路径 | `wiki/insights/{category}/` | 🟢 **未改**（保持原路径）|
| getnote_ej9_to_wiki.py Wiki frontmatter | 新写入文件加 `KB 等级` + `KB ID` | 🟡 **新写入才生效**（state 防重复）|

---

*版本: L-49.14 v1.0*
*最后更新: 2026-07-29 09:54 CST*
*维护者: 尼克·弗瑞 🕵️*
