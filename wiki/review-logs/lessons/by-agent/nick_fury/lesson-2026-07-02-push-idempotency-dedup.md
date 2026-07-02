# Lesson: 推送去重（时间维度 + 内容维度）

> **触发 INC**: INC-2026-07-02-002
> **发现时间**: 2026-07-02 13:50（文博主动询问）
> **闭环时间**: 2026-07-02 14:00（10 分钟）
> **沉淀时间**: 2026-07-02 14:05

---

## 现象

7-1 技术日报被推了 2 次相同消息（11:25 + 11:32，间隔 7 分钟）。7-1 + 7-2 推送里 Loop Engineering 主题重复出现 3 次（RSS + 解读 + Loopcraft）。

---

## 教训

### L-23.1: idempotency_key 必须用内容 hash

**原则**：任何"按天推送"的内容，idempotency_key 必须包含**内容指纹**，不能只用日期。

| 维度 | 旧方案 | 新方案 |
|:---|:---|:---|
| Key 生成 | `daily_report_20260702` | `daily_report_20260702_9869259a235b` |
| 同日同内容 | 同 key → 飞书可能不去重 | 同 hash → 飞书 100% 去重 |
| 同日不同内容 | 同 key → 飞书可能误去重 | 不同 hash → 不同 key → 正常发 |

**实测验证**（13:58）:
```
第 1 次推送: om_x100b6b6baf9c34a8b4b50349c82a86f
第 2 次推送（同内容同 key）: om_x100b6b6baf9c34a8b4b50349c82a86f ✅ 同 ID
第 3 次推送（不同内容同 key）: om_x100b6b6baf9c34a8b4b50349c82a86f ✅ 仍同 ID（飞书以首次为准）
```

### L-23.2: 跨数据源推送必须做主题去重

**原则**：当推送来自多个数据源（RSS + Get 笔记 + Wiki + ...），生成推送前必须做**主题去重**。

**L-23 去重算法**（已沉淀到 `daily_tech_report.py`）:
```python
def extract_keywords(title):
    """提取标题关键词用于去重"""
    words = re.findall(r'[A-Za-z][A-Za-z0-9]+|[\u4e00-\u9fff]{2,}', title)
    keywords = set()
    for w in words:
        wl = w.lower()
        if wl in STOP_WORDS or len(wl) < 2:
            continue
        keywords.add(wl)
    return keywords

def jaccard_overlap(kw1, kw2):
    """Jaccard 相似度（取 min 分母更严格）"""
    if not kw1 or not kw2:
        return 0.0
    intersection = kw1 & kw2
    return len(intersection) / min(len(kw1), len(kw2))

def deduplicate_across_sources(rss_titles, getnote_titles, threshold=0.4):
    """跨数据源主题去重"""
    rss_keyword_sets = [extract_keywords(t) for t in rss_titles]
    deduped, removed = [], []
    for title in getnote_titles:
        kw = extract_keywords(title)
        max_overlap, matched = 0.0, None
        for i, rss_kw in enumerate(rss_keyword_sets):
            if not rss_kw: continue
            overlap = jaccard_overlap(kw, rss_kw)
            if overlap > max_overlap:
                max_overlap, matched = overlap, rss_titles[i]
        if max_overlap < threshold:
            deduped.append(title)
        else:
            removed.append((title, max_overlap, matched))
    return deduped, removed
```

**实测效果**（7-2 13:58）:
- RSS #1 "The Art of Loop Engineering" 保留
- Get 笔记 "Andrew Ng 深度解读Loop Engineering" → overlap=0.6 → 过滤 ✅
- Get 笔记 "AI Agent循环工程（Loopcraft）" → overlap=0.5 → 过滤 ✅

### L-23.3: lark-cli v1.0.59 idempotency 可能不工作

**结论**：升级到 v1.0.63 后，**同 key 同内容 100% 返回同一 message_id**。但**同 key 不同内容**也返回**首次**的 message_id（不是新发）——说明飞书 idempotency_key 是"以首次为准"。

**预防**：
- 所有 Nick 推送脚本必须用 **内容 hash** 做 key（不仅日期）
- 每月初用 `lark-cli update --check` 看是否有新版

---

## 复用代码

**scripts/daily_tech_report.py** 已包含：
- `STOP_WORDS` - 停用词集合（87 字符）
- `extract_keywords(title)` - 120 字符
- `jaccard_overlap(kw1, kw2)` - 60 字符
- `deduplicate_across_sources(rss_titles, getnote_titles, threshold=0.4)` - 500 字符
- `generate_tech_push()` 中调用：选完 Get 笔记后过滤 overlap > 0.4 的

**idempotency_key 模板**（两个脚本都用）:
```python
import hashlib
content_hash = hashlib.md5(summary.encode('utf-8')).hexdigest()[:12]
idempotency_key = f"daily_xxx_{today_str.replace('-', '')}_{content_hash}"
```

---

## 验证清单（写新推送脚本前必过）

- [ ] **L-23.1**: idempotency_key 是否含内容 hash？（不是只日期）
- [ ] **L-23.2**: 多数据源是否做主题去重？（不只是行内过滤）
- [ ] **L-23.3**: 写完后跑端到端，验证"同内容 2 次推送 → 飞书只 1 条"

---

## 关联

- INC-2026-07-02-001（L-22 OPENCLAW_HOME）
- L-19（wrapper 封装）
- L-15（端到端验证）
- L-17（写脚本前 read 3 行）

---

*沉淀者: 尼克·弗瑞 🕵️*
*验证状态: ✅ 13:58 manual e2e + 13:59 launchd e2e 全部通过*
*下次审计: 7-3 07:15（明早首次 cron 触发验证）*