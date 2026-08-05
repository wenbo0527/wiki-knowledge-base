# L-56 · 报告数据失真家族（数据基准日 + 真实/preset 比例透明）

> **入库日期**: 2026-08-05 08:56 CST
> **触发**: INC-2026-08-05-001（NFT 报告 50% 数据是 39 天前硬编码）
> **关联**: L-29（输出成功 ≠ 输入真实）· L-55（东方财富 fail-fast 治本）· C-1 闭环

---

## L-56 族首

L-56 是 **报告数据失真** 教训族的首条，下设 5 子：

| 子 | 标题 | 核心 |
|:---:|:---|:---|
| **L-56.1** | 报告标题日期 ≠ 数据基准日 | 报告头部必须显式 📅 标注 |
| **L-56.2** | data_source 字符串判断要严格 | "预设"字样 ≠ preset 兜底 |
| **L-56.3** | 写报告后必须持久化 | 修复 7-14 真空 |
| **L-56.4** | 数据新鲜度 assert | > 24h 进 stale_warnings |
| **L-56.5** | C+B 组合 > 单纯 A 删 | 透明 + 治本更鲁棒 |

---

## L-56.1 报告标题日期 ≠ 数据基准日

### 现象
8-5 08:35 cron 跑出的 `etf_hegang_report.md` 标题写"2026-08-05"，但 4/8 ETF 估值分位是 6-25 硬编码（39 天前）。

### 教训
报告标题日期 = **生成时间** ≠ 数据基准日 = **数据真实采集时间**。两者必须**显式区分**。

### 落地
```python
# etf_hegang_report.py 头部
lines.append(f"> 📅 **数据基准日**: {data_baseline} | 真实数据: {len(sources_real)}/{len(etf_data)}")
if sources_preset:
    lines.append(f"> ⛔ **fallback preset** ({len(sources_preset)}/{len(etf_data)}): {', '.join(sources_preset)} | 估值/分位为 6-25 硬编码")
```

### 验证
跑 8-5 报告，看到头部：
```
> 📅 数据基准日: 2026-08-05 08:56:45 | 真实数据: 4/8
> ⛔ fallback preset (4/8): 半导体, AI, 电力, 卫星 | 估值/分位为 6-25 硬编码
```

---

## L-56.2 data_source 字符串判断要严格

### 现象
第一次 patch 把腾讯备用源（`data_source="腾讯备用源(8-4 L-55) + 预设估值"`）误判成 preset —— 因为字符串含"预设"字样。

### 教训
**字符串包含判断 ≠ 语义判断**。`data_source` 字符串里出现"预设"不一定代表 preset 兜底（可能是 "X 源 + 预设估值字段"）。

### 落地
```python
# ❌ 反例
is_fallback = '预设' in ds or '全源失败' in ds

# ✅ 正例
is_fallback = ds.startswith('全源失败') or '仅用预设' in ds
```

### 验证
patch 后跑 8-5 报告：4/8 真实（宽基🟢 tx）+ 4/8 preset（行业⛔ preset）—— 划分正确。

---

## L-56.3 写报告后必须持久化

### 现象
7-14 之前 `etf_percentile_fetcher.py` 写 `etf_percentile_today.json`，7-14 重构后脚本归档到 `_deprecated/2026-07-14/`，**没人写这个文件**。timestamp 停在 7-14 09:12。

### 教训
**报告生成 ≠ 数据持久化**。如果报告是临时 markdown，json 缓存必须同步更新，否则下游消费者（`daily_investment_report.py`）读到的永远是旧数据。

### 落地
```python
# etf_hegang_report.py main() 末尾
persist_data = _build_persist_payload(target_date)
persist_path = Path('/Users/wenbo/.openclaw/workspace/agents/nick_fury/data/etf_percentile_today.json')
persist_path.write_text(json.dumps(persist_data, ensure_ascii=False, indent=2), encoding='utf-8')
```

### 验证
8-5 08:56 持久化文件 2596B，fetched_at=2026-08-05T08:56:51，success/failure/total=4/4/8 ✅

---

## L-56.4 数据新鲜度 assert

### 现象
fetcher 自身有 `cache_ttl` 但**没设 24h 阈值告警**。14 天的旧数据 + preset 写入 report 后，cron status 仍 ok。

### 教训
**缓存命中 ≠ 数据新鲜**。ttl 内可以快取，但 ttl 外必须 assert 告警（> 24h 进 stale_warnings）。

### 落地
```python
# _build_persist_payload() 内
for r in results:
    ut = r.get('update_time', '')
    if ut:
        try:
            ut_dt = datetime.strptime(ut, '%Y-%m-%d %H:%M:%S')
            age_hours = (datetime.now() - ut_dt).total_seconds() / 3600
            if age_hours > 24:
                stale.append({'name': r['name'], 'age_hours': round(age_hours, 1)})
        except Exception:
            pass
```

### 验证
8-5 08:56 跑出 stale_warnings=[]（4 个真实数据都 < 24h，4 个 preset 没 update_time 不算 stale）✅

---

## L-56.5 C+B 组合 > 单纯 A 删

### 现象
8-5 08:46 文博问"东方财富怎么还在？"——表面答案是 **A 删**（移除东方财富引用）。

### 教训
**A 删不是治本**。删掉东方财富引用 → 全部走 tx 备用源 → 行业指数（881121/885728/884035/931748）拿不到 → 仍需 preset 兜底。问题不在"源是否存在"，在"数据是否透明"。

### 落地
8-5 08:52 拍板 **C + B 组合**：
- **C 透明**：报告顶部加 📅 数据基准日 + ⛔ preset 警示
- **B 治本**：fetcher 数据新鲜度 assert + 持久化修复（7-14 真空）

**保留东方财富作为兜底**（fail-fast + 备用源 v2.5 L-55 已是标准做法）。

### 验证
- 东方财富 fail-fast 仍按 v2.5 工作（不浪费 54 秒）
- 报告清晰标注 4/8 真实 + 4/8 preset
- 持久化 json 修复 7-14 真空

---

## 复用检查清单

任何"写报告 + 写数据"的脚本都要过 5 子：

- [ ] L-56.1：报告头部有 📅 数据基准日 + 真实/preset 比例
- [ ] L-56.2：data_source 字段判断用 `startswith()` 严格匹配
- [ ] L-56.3：报告生成后同步写 json 缓存（防 7-14 真空）
- [ ] L-56.4：数据新鲜度 assert > 24h 进 stale_warnings
- [ ] L-56.5：透明 + 治本组合 > 单纯删源

---

## 关联

- **L-29**：输出成功 ≠ 输入真实（7-2 数据流断点）
- **L-55**：东方财富 push2 100% 失败 → fail-fast + 备用源（8-4 治本）
- **L-55 + L-56 配套**：fetcher 拿数据 + 报告透明化 = 完整治本循环
- **C-1 闭环**：5 件 write 全部成功（脚本 + 报告 + json + INC + lesson）
- **INC-2026-08-05-001**：本族首发 INC

---

🕵️ nick_fury · 2026-08-05 08:56 CST · L-56 族首 · 报告数据失真家族治本 · 5 子教训入族 · 复用检查清单 5 项
