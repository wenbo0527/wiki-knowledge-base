# INC-2026-08-04-001: 东方财富 push2 API 100% 失败 + v2.5 L-55 治本闭环

> 创建时间: 2026-08-04 09:13 CST
> 闭环时间: 2026-08-04 09:13 CST（接单 → 闭环 12 min）
> 责任人: 尼克·弗瑞 🕵️
> 状态: ✅ Closed
> 关联: L-55 族首（数据源采集 fail-fast + 多源兜底模式）

---

## 现象

8-4 08:54 文博问"东方财富 不是昨天删除了么？" → 8-4 08:57 追问"API 现在是否也实际很久没有数据了？" → 8-4 09:01 拍板"同意 A"（写 INC + 立即 fork 修复）→ 12 min 闭环。

### 8-4 08:35 cron 跑通时（24 min 前）的真实数据

```
⚠️ 东方财富获取 000016 失败: ('Connection aborted.', RemoteDisconnected(...))
✅ sina 备用源 000016 成功: 2908.51
⚠️ 东方财富获取 000300 失败: ('Connection aborted.', RemoteDisconnected(...))
✅ sina 备用源 000300 成功: 4561.82
⚠️ 东方财富获取 000905 失败: ('Connection aborted.', RemoteDisconnected(...))
✅ sina 备用源 000905 成功: 7457.12
⚠️ 东方财富获取 000688 失败: ('Connection aborted.', RemoteDisconnected(...))
✅ sina 备用源 000688 成功: 1619.29
⚠️ 东方财富获取 881121 失败: ('Connection aborted.', RemoteDisconnected(...))
⚠️ 东方财富获取 885728 失败: ('Connection aborted.', RemoteDisconnected(...))
⚠️ 东方财富获取 884035 失败: ('Connection aborted.', RemoteDisconnected(...))
⚠️ 东方财富获取 931748 失败: ('Connection aborted.', RemoteDisconnected(...))
```

**东方财富 push2 接口 100% 失败**（9/9），sina 兜底 4 个宽基，**4 个行业 ETF 完全无数据源**。

### 8-4 08:57 直接 curl 实测

| URL | HTTP | 含义 |
|:---|:---:|:---|
| `push2.eastmoney.com/api/qt/stock/get?...` | **000** (0.18s 断) | API 死封 |
| `fund.eastmoney.com/` | 200 | 首页浏览器正常 |
| `push2.eastmoney.com/` | 404 | 限制爬虫 |

**东方财富 push2 全面封锁非浏览器访问**——即使有 User-Agent + Referer 也过不了。

---

## 根因

1. **历史原因**：东方财富 push2 API 历史可用 → ETF fetcher v2.0~v2.4 一路通畅
2. **8-4 察觉**：push2 死亡是渐进式（可能是反爬升级对脚本 UA 封锁）
3. **盲点放大**：v2.4 L-46 加的 sina 备用源只覆盖 4 个宽基，**4 个行业 ETF（881121/885728/884035/931748）三源全 fail**
4. **v2.5 fail-fast 缺失**：原 retry 3 次 × 6s = 浪费 18s/指数 × 9 = **54s/cron 跑**
5. **数据源标记失真**：报告里"东方财富 API 失效"风险标 🟢 低，但实际已 100% 失败

### 8-3 闭环盲点（Nick 自我归因）

8-3 闭环时（INC-2026-08-01-001 L-52 衍生）只 grep "东方财富" 有没有出现 → 没查实际可用性。今天 8-4 数据反驳 8-3 判断：

| 项 | 8-3 闭环时 | 8-4 实证 |
|:---|:---|:---|
| 东方财富 API 状态 | "不能删"（隐含=可用）| **100% 失败** |
| 实际数据源 | (没查) | **全靠 sina 兜底** |
| 4 个行业 ETF | (没查) | **sina 也没数据** |

---

## 修复（v2.5 L-55 治本）

### 改动 1：`_request_with_retry` 加 fail-fast 模式

```python
DEAD_SOURCE_PATTERNS = ('Connection aborted', 'RemoteDisconnected', 'Remote end closed',
                        'Connection refused', 'Connection reset')

def _request_with_retry(self, url, retries=3, headers=None, fail_fast_connection_aborted=True):
    """v2.5 L-55: 源端死封 → 0 retry 直接 raise，避免 9×6s = 54s 浪费"""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=_headers, timeout=10)
            return response.json()
        except Exception as e:
            if fail_fast_connection_aborted and _is_dead_source(e):
                raise e
            ... # retry 兜底
```

### 改动 2：加腾讯 qt.gtimg.cn 第三备用源

```python
def _parse_tx_index(self, index_code: str) -> Optional[Dict]:
    """v2.5 L-55: 腾讯 qt.gtimg.cn 备用源（行业指数可获取）

    tx 字段: [3]当前 [4]昨收 [5]今开 [30]时间 [31]涨跌 [32]涨跌幅%
    """
    url = f'https://qt.gtimg.cn/q=sh{index_code}'
    ...
```

### 改动 3：`get_index_valuation` 多源兜底

```python
# 顺序: 东方财富(fail-fast) → tx(qt.gtimg.cn) → sina(hq.sinajs.cn) → preset
```

### 改动 4：`get_etf_real_time_data` 加 tx ETF 备用

```python
# ETF 实时数据(510050/512480 等) 东方财富 fail-fast → tx qt.gtimg.cn 备用
# tx 字段: [3]当前 [4]昨收 [5]今开 [31]涨跌 [32]涨跌幅%
```

### 改动 5：`format_for_daily_push` 指数点位=0 时用 ETF 净值

```python
if current_point > 0:
    point_str = f"{current_point:>7.0f}点"
elif current_price > 0:
    point_str = f"{current_price:>7.3f}元"  # ETF 净值
else:
    point_str = "    -  "
```

### 端到端验证（8-4 09:10 实测）

```
✅ 8/8 ETF 实时数据全部拿到
✅ 时间从 54s 降到 3.7s（**93% 提速**）
✅ 4 个宽基显示指数点位（2887/4543/7415/1553 点）
✅ 4 个行业 ETF 显示 ETF 净值（0.921/0.985/1.314/1.062 元）
✅ 数据源标记清晰
```

---

## 教训（L-55 族首）

### L-55.1 数据源采集必加 fail-fast 模式

> 任何已知/疑似死封的数据源，**必须** fail-fast 跳过 retry，避免每天浪费 54s × cron 次数 = 540s/天。

### L-55.2 多源兜底顺序：东方财富 → tx → sina → preset

> 8-4 实测顺序优选：
> - 指数（000016/000300/000905/000688）: **tx 优先**（比 sina 字段更丰富）
> - 行业指数（881121/885728/884035/931748）: **tx 唯一**（东方财富/sina 都拿不到）
> - 兜底 preset 分位数据保留（PE/分位失效）

### L-55.3 单点验证必须实测，不能凭 grep 印象

> 8-3 闭环时只 grep 名字 → 没查可用性。**任何数据源闭环都以实测为准**（L-37/L-38 强化）。

### L-55.4 ETF 净值 vs 指数点位 双显示

> 行业指数点位三源都拿不到时，**ETF 净值（腾讯 qt.gtimg.cn）** 是有效替代。报告里用"元"区分。

### L-55.5 数据源变更必同步标头

> v2.4 → v2.5 改动 5 处，必须在文件 docstring + 报告 data_source 标记 + INC 同步留痕。

---

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| **每日 8:35** | etf.hegang.report cron 自动跑（fail-fast + 多源兜底已生效）| OpenClaw cron |
| **每周日 22:00** | cron_argv_watchdog 检查 fetcher 路径一致性 | scripts/cron_argv_watchdog.py |
| **每日 21:00** | C-3 自检：报告"数据源"标签必须含 tx 标记 | c3_daily_check.py 升级 |
| **每月 1 号** | 数据源健康盘点（东方财富恢复？新源？）| rss_source_health_monitor |

---

## 关联

- **INC-2026-08-01-001** (L-52 RSS 健康监控) — 同源观察 → 数据源采集 L-55 补强
- **L-46** (7-19 sina/tx 备用源) — L-55 在此基础上加 fail-fast + tx qt.gtimg.cn 备用
- **L-37/L-38** (报告必实测) — L-55.3 验证：8-3 凭 grep 印象错，8-4 以实测为准
- **L-29** (真相错位) — L-55: 报告"🟢 低 东方财富 API 失效"风险标，从 8-4 起应升 🟡 中

---

## 待办（已闭环 / 未来）

| # | 项 | 状态 |
|:---:|:---|:---:|
| 1 | etf_real_time_fetcher.py v2.5 改造 | ✅ 09:10 完成 |
| 2 | 端到端 8/8 ETF 验证 | ✅ 09:10 完成 |
| 3 | INC + lesson 落档 | ✅ 09:13 完成 |
| 4 | 备份原文件 v2.4 | ✅ etf_real_time_fetcher.py.bak.2026-08-04 |
| 5 | L-55 写入 lessons 族 | ✅ lesson-2026-08-04-l55-... |
| 6 | 6-26 akshare 修复（PE/分位）| ⏳ 仍未做（PE/分位 仍 preset） |
| 7 | C-3 加数据源标签校验 | ⏳ MEMORY 8-2 待办 |
| 8 | 8 patch v1.1 路线图 | ⏳ 待文博拍板 |

---

*🕵️ 尼克·弗瑞 · 2026-08-04 09:13 CST · INC-2026-08-04-001 闭环 · L-55 族首 · 12 min 闭环 · 边界守住 5 项（C-1/C-2/L-31/L-37/L-38）· 4 项 P0 待办*
