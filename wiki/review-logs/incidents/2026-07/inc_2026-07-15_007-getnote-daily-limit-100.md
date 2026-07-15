# INC-2026-07-15-007: GET 笔记入库 v2.1（每日 100 篇限流）

> **触发**: 7-15 15:01 文博拍 A："可以每天 100 篇这样"
> **修复**: v2.0 → v2.1
> **状态**: ✅ 已部署

---

## 修复内容

### v2.1 4 大新增（L-41 + L-42 治本）

| 常量 | 值 | 用途 |
|:---|:---:|:---|
| `DAILY_LIMIT` | **100** | 每日最多入库 100 篇（防雪崩）|
| `REQUEST_DELAY` | **1.0** | 每条 API 请求间隔 1s（避免 HTTP 429）|
| `BATCH_DELAY` | **5.0** | 跨 KB 间隔 5s（安全缓冲）|
| `MAX_RETRY` | **3** | HTTP 429 retry 3 次 |

> ⚠️ **API 限制**：GET 笔记 API 不支持 `size` 参数，每页固定 20 条。分页循环至 `has_more=False` 拉全量。

### 逻辑修改

```python
# fetch_kb_notes: size=100 拉全量
url = f"...?topic_id={kb_id}&page={page}&size=100"

# fetch_note_detail: retry 3 次 + sleep
for attempt in range(1, MAX_RETRY + 1):
    data = fetch_url(url, headers)
    time.sleep(REQUEST_DELAY)
    if "HTTP 429" in str(e):
        wait = REQUEST_DELAY * attempt * 2
        time.sleep(wait)
        continue
    raise

# main: DAILY_LIMIT 检查
if total_written >= DAILY_LIMIT:
    print(f"🟡 已达每日上限 DAILY_LIMIT={DAILY_LIMIT} · 剩余 KB 推迟到明日")
    break

# main: 跨 KB BATCH_DELAY
time.sleep(BATCH_DELAY)
```

## 预计运行节奏

| 天 | 写入 | 累计 | 剩余 |
|:---|:---:|:---:|:---:|
| 7-15 | 115 (已跑) | 115 | ~4,700 |
| 7-16 | 100 | 215 | ~4,600 |
| 7-17 | 100 | 315 | ~4,500 |
| ... | ... | ... | ... |
| ~8-10 | 100 × N | ~1,000 | ~4,000 |

**预计 ~50 天完成全量**（BACKFILL_DAYS=60 × 11 KB ≈ 5,000 笔记）

---

## 状态

- [x] INC-007 创建（15:02）
- [x] v2.1 部署（语法 OK）
- [ ] dry-run（验证 DAILY_LIMIT 逻辑）
- [ ] 今晚 21:00 cron 自动跑
- [ ] Close

---

*INC 完稿: 2026-07-15 15:02 CST*
*接单人: 尼克·弗瑞 🕵️*
