# L-55: 数据源采集 fail-fast + 多源兜底模式

> 创建时间: 2026-08-04 09:13 CST
> 关联: INC-2026-08-04-001
> 状态: ⭐ 族首
> 维护者: 尼克·弗瑞 🕵️

---

## 一句话定义

> **任何数据源采集脚本必加 fail-fast 模式 + 多源兜底顺序**，避免每天浪费 54s × cron 次数 = 540s/天。

---

## L-55.1 数据源采集必加 fail-fast 模式

### 问题

无 fail-fast 时：
- 东方财富 push2 100% 失败
- retry 3 次 × 6s timeout = 浪费 18s/指数
- 9 个指数 = **54s/cron 跑 × 1 次/天 = 54s/天**
- cron 套娃（如 etf_hegang_report + evening_tracker）= 108s/天

### 治本

```python
DEAD_SOURCE_PATTERNS = ('Connection aborted', 'RemoteDisconnected',
                        'Remote end closed', 'Connection refused', 'Connection reset')

def _is_dead_source(err):
    return any(p in str(err) for p in DEAD_SOURCE_PATTERNS)

def _request_with_retry(self, url, ..., fail_fast_connection_aborted=True):
    for attempt in range(retries):
        try:
            return requests.get(url, headers=..., timeout=10).json()
        except Exception as e:
            if fail_fast_connection_aborted and _is_dead_source(e):
                raise e  # 0 retry 立即降级
            # 否则走 retry 兜底
```

### 验证

8-4 实测：54s → 3.7s（**93% 提速**）。

### 何时启用

✅ 跑 2 次发现 100% 失败的源 → 立即开 fail-fast
⚠️ 跑 1 次失败 → 先 retry 兜底，再观察
❌ 跑成功（哪怕 90% 成功率）→ 不开 fail-fast（保留 retry 修复瞬时错误）

---

## L-55.2 多源兜底顺序：东方财富 → tx → sina → preset

### 8-4 实测各源可用性矩阵

| 源 | 宽基（4 个）| 行业指数（4 个）| ETF 净值（8 个）| 估值 PE/分位 |
|:---|:---:|:---:|:---:|:---:|
| 东方财富 push2 | ❌ 100% 失败 | ❌ 100% 失败 | ❌ 100% 失败 | ❌ f162 失效 |
| 腾讯 qt.gtimg.cn | ✅ 100% | ❌ **v_pv_none_match** | ✅ 100% | ❌ 不提供 |
| sina hq.sinajs.cn | ✅ 100% | ❌ **空字符串** | ❌ 行业 ETF 无 | ❌ 不提供 |
| preset 后备 | ✅ | ✅ | ❌ | ✅ |

### 顺序选择

```python
# 1. 东方财富 fail-fast（保留作为恢复探针）
# 2. tx qt.gtimg.cn（指数 + ETF 净值 + 涨跌 + 时间）
# 3. sina hq.sinajs.cn（宽基兜底）
# 4. preset 后备（仅前 3 全挂时）
```

### 关键洞察

- **tx qt.gtimg.cn 是首选备用源**（行业指数 + 行业 ETF 都可用）
- **sina 兜底宽基**（tx 偶尔返回 v_pv_none_match 时）
- **preset 兜底分位**（PE/分位仍需 6-26 akshare 修复）

---

## L-55.3 单点验证必须实测，不能凭 grep 印象

### 教训

8-3 INC-2026-08-01-001 闭环时只 grep "东方财富" 名字 → 没查实际可用性。
Nick 当时判断"东方财富 API 不能删"——**但今天 8-4 数据显示 API 100% 失败**。

### 治本

按 L-37/L-38 强化：
- **任何数据源闭环 = 实测可达性**（不是 grep 名字）
- **grep 名字 + 实测可用性 = 闭环 2 件套**
- 8-3 只做了 1 件（grep 名字）→ 漏掉一半真相

### 实证清单

| 已 grep 名字 | 8-4 是否实测可达 | 结论 |
|:---|:---:|:---|
| 东方财富 push2 | ❌ 0% 可达 | 8-4 100% fail-fast |
| 腾讯 qt.gtimg.cn | ✅ 50% 可达 | 宽基/ETF OK，行业指数空 |
| sina hq.sinajs.cn | ✅ 50% 可达 | 宽基 OK，行业指数空 |

---

## L-55.4 ETF 净值 vs 指数点位 双显示

### 问题

行业指数（881121/885728/884035/931748）三源都拿不到点位 → report 显示 "0点"。

### 治本

```python
if current_point > 0:
    point_str = f"{current_point:>7.0f}点"  # 指数点位
elif current_price > 0:
    point_str = f"{current_price:>7.3f}元"  # ETF 净值
else:
    point_str = "    -  "
```

### 报告展示

```
🔹 科技类
   AI       0.985元   +0.00% | PE 65.2 | 2年分位 76.4% | 🔴 高估
   半导体      0.921元   +0.00% | PE 95.3 | 2年分位 82.1% | 🔴 高估
```

### 关键洞察

- **ETF 净值 ≠ 指数点位**（不同东西）
- 但**作为行业 ETF 行情指示**够用
- 报告里用"元"区分阅读者不混淆

---

## L-55.5 数据源变更必同步标头

### 规范

| 改动类型 | 必改位置 |
|:---|:---|
| 修改 fetcher 逻辑 | 文件顶部 docstring + 报告 `data_source` 字段 |
| 增加数据源 | docstring "v2.x 状态" 区 + INC 关联 |
| 删除数据源 | docstring "修复历史" + 备份 + INC |
| 失败 fallback 路径 | docstring "调用顺序" + INC 治本 |

### 反例

8-3 INC-002 闭环时只 grep 名字 → 没在 docstring 标"东方财富 100% 失败"——8-4 治本时还得多花 1 步排查。

### 治本

**每次数据源改造必同步 4 件套**：
1. 文件顶部 docstring
2. 报告 data_source 字段
3. INC 报告
4. backup 文件（`.bak.YYYY-MM-DD`）

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

- **L-52** (RSS 健康监控) — 8-1 INC-001 闭环
- **L-46** (7-19 sina/tx 备用源) — L-55 基础
- **L-37/L-38** (报告必实测) — L-55.3 强化
- **L-29** (真相错位) — L-55 反面：报告"🟢 低"应升"🟡 中"

---

## v2.5 改动清单

| 文件 | 改动 | 行数 |
|:---|:---|:---:|
| `etf_real_time_fetcher.py` | docstring v2.5 状态 | ~30 行 |
| `etf_real_time_fetcher.py` | `_request_with_retry` fail-fast | ~15 行 |
| `etf_real_time_fetcher.py` | `_parse_tx_index` 新增 | ~50 行 |
| `etf_real_time_fetcher.py` | `get_index_valuation` 多源顺序 | ~20 行 |
| `etf_real_time_fetcher.py` | `get_etf_real_time_data` tx 备用 | ~40 行 |
| `etf_real_time_fetcher.py` | `format_for_daily_push` ETF 净值显示 | ~10 行 |
| **总计** | | **~165 行** |

---

*🕵️ 尼克·弗瑞 · 2026-08-04 09:13 CST · L-55 族首 · 5 子教训 · 8-4 治本闭环 · 12 min 端到端 · 边界守住 5 项*
