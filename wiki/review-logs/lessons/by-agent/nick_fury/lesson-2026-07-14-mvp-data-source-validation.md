---
title: lesson 2026 07 14 mvp data source validation
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# Lessons L-28 & L-29 · 2026-07-14 ETF 速览失真 18 天

> 两个新教训，源自 **INC-2026-07-14-001**（🔴 Critical）
> 沉淀者：nick_fury 🕵️
> 验证者：文博（07-14 09:00 主动揭穿）

---

## L-28: 多源兜底必须 raise，不能静默 fallback 到"看起来像数据"的预设

**教训**：任何"数据源失效 → 用预设值顶替"的设计，必须满足 3 个条件才能"安全"：
1. **显眼标注**（如 `"data_source": "预设后备（API 全挂）"` 字段直接进推送）
2. **失败必须 raise**（绝不准静默 return，让上游能 catch 到）
3. **预设必须有过期检查**（超过 N 天的预设 vs 真实数据偏差应触发报警）

**反例**（etf_real_time_fetcher.py v2.3 / 7-14 已修）：
```python
def get_index_valuation(index_code):
    try:
        pe_ttm = fetch_eastmoney_pe(index_code)  # 失败
    except:
        pe_ttm = 0
    if pe_ttm == 0:
        preset_data = self._get_preset_data(index_code)  # 静默用 6-25 写的预设
        current_pe = preset_data['current_pe']           # 9.2 兆半导体，PE 95.3 出去了
        # ❌ 没有 preset_used=True 标记
        # ❌ 没有 preset_date=2026-06-25 标记
        # ❌ 没有 raise
```

**正例**（etf_percentile_fetcher.py v1.0）：
```python
def fetch_one_etf(etf_def):
    sources = [
        ("sina_etf_kline", lambda: fetch_sina_etf_kline(...)),
        ("sina_index_kline", lambda: fetch_sina_index_kline(...)),
    ]
    errors = []
    for source_name, fetch_fn in sources:
        try:
            klines = fetch_fn()  # 验证真实数据
            ...
            return {... "source": source_name, ...}
        except (URLError, ValueError, ...) as e:
            errors.append(f"{source_name}: {e}")
    raise RuntimeError(f"🔴 {name} 全部源失败 → {' / '.join(errors)}")
```

**L-28 grep 检查（修一类必 grep 全集）**：
```bash
# 任何"装死的兜底"都应 grep
grep -rn "_preset\|fallback.*=.*0\|try:.*except.*pass" \
  /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/ \
  | grep -v "_deprecated\|.bak"
# 当前已知：e_tf_real_time_fetcher.py:_get_preset_data（已弃用），其他要再 grep
```

---

## L-29: 自检必须区分"输出成功"和"输入真实"

**教训**：报告"✅ 推送成功"只证明 3 个通道可用，不证明内容是真实的。
- 长度检查 ≥ 100 字符 → 内容存在
- lark-cli exit 0 → 网络通
- 飞书收到 → 通道通
- 但**"分位数字"本身是 6-25 写死的预设** → 没人查

**3 个新自检规则（7-14 起 daily_investment_report.py 内置）**：
1. **数据新鲜度**：JSON 落盘时间戳距推送 ≤ 6 小时（不是数据日期）
2. **数据来源标注**：表格首行加 `*数据源: sina_xxx_kline (last: YYYY-MM-DD)*`
3. **failures 非空必报警**：daily_investment_report 看到 failures 字段非空 → 显式告诉用户"X 只拉不到"

**反例自检脚本**（`scripts/c3_daily_check.py` 升级用）：
```python
# 任何"研究报告类"推送，发起方应自问：
# 1. 数据日期是否新鲜？（如果 last_day < 6 天前，必须报警）
# 2. 数据来源是否标注？（如果 "data_source": "preset"，必须告诉用户）
# 3. 数据个数是否齐？（如果 failures 非空，必须告诉用户）
```

**新 cron 设计（C-3 增强）**：
```xml
<!-- 每天 07:00 preflight cron -->
<key>etf-fetcher-preflight</key>
<date>0 7 * * 1-5</date>
<command>/usr/bin/python3 /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/etf_percentile_fetcher.py</command>
<!-- 提前 15 分钟抓数据，让 07:15 推送有真数据 -->
```

---

## 两 INC + 七教训系列（最新）

| INC | 教训 | 一句话 |
|:---|:---|:---|
| INC-2026-06-08-001 | (C-1) | 4 次口头承诺未落盘 |
| INC-2026-06-15-001 | (L-15) | Wiki PermissionError 44 天未发现 |
| INC-2026-06-23-001/002 | | 11 plist launchd 修复 |
| INC-2026-07-01-001 | L-14/L-15 | morning-rss-etf-push 三连失败 |
| INC-2026-07-02-001 | L-19/L-20/L-21 | Lark-CLI 在 Launchd 失败 |
| INC-2026-07-02-002 | L-23 | 技术日报重复推送 |
| INC-2026-07-06-001 | L-24/L-25/L-26 | RSS 数据真空 7 天 + 内容重复 |
| **INC-2026-07-14-001** | **L-28/L-29** | **ETF 速览 18 天失真（hardcoded 预设）** |

---

## 预防机制（已加 / 待加）

- [x] `etf_percentile_fetcher.py`：多源 + raise + 新鲜度 + 数据源标注
- [x] `daily_investment_report.py` v3：失败必报警 + 数据来源可见
- [ ] **07:00 preflight cron**（L-20 治本）—— 提前 15min 抓数据
- [ ] **C-3 升级**：21:00 自检 grep `data/*today*.json` 落盘时间戳 < 6h
- [ ] **MEMORY.md** 更新 + daily/2026-07-14.md

---

*Created: 2026-07-14 09:30 · nick_fury 🕵️*
