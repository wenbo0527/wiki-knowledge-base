# 归因分析Portfolio案例深度解析

> 来源: Daniel Guidi - delivery-industry-growth-analytics
> 更新: 2026-04-27
> 分析师: 尼克·弗瑞

---

## 案例概述

**GitHub:** https://github.com/danielguidid/delivery-industry-growth-analytics
**Star数:** 1
**定位:** 端到端数据分析案例 - 营销归因+ROI分析

**核心价值:**
- 完整的SQL归因模型实现
- 端到端分析流程（清洗→SQL→Python→Tableau→PPT）
- 虚构公司场景，适合Portfolio展示

---

## 项目结构分析

```
delivery-industry-growth-analytics/
├── raw_business_data.csv          # 原始数据（虚构）
├── clean_business_data.csv        # 清洗后数据
├── data_preparation.ipynb         # Python清洗notebook
├── advanced_queries.sql           # 高级SQL（CTE+归因）
├── marketing_performance_dashboard.twbx  # Tableau看板
├── stakeholders_presentation.pdf  # 商业呈现PPT
└── project_requirements.pdf       # 需求文档
```

### 流水线设计

```
数据采集 → 数据清洗 → SQL分析 → Python验证 → BI看板 → 商业PPT
   │           │           │           │          │         │
  raw      clean       queries    原型验证   可视化    决策支撑
```

---

## 核心KPI矩阵

### 四大核心指标

| 指标 | 英文 | 定义 | 计算公式 |
|------|------|------|----------|
| **转化数** | Conversions | 首单用户数 | COUNT(DISTINCT user_id) |
| **获客成本** | CAC | 每新客成本 | Spend ÷ New Customers |
| **生命周期价值** | LTV | 用户价值 | Avg Revenue × Lifespan |
| **月留存** | M+1 Retention | 次月复购率 | Day30复购用户 / 总用户 |

### 扩展指标

| 指标 | 说明 | 用途 |
|------|------|------|
| ROAS | 广告回报率 | Revenue ÷ Ad Spend |
| LTV/CAC | 价值倍数 | 判断盈利性 |
| CPA | 行动成本 | 每行动成本 |
| CR | 转化率 | 转化数/访客数 |

---

## 归因模型实现

### 模型1: First-order, month-strict

```sql
-- 首单归因：当月首次触达渠道
WITH first_touch AS (
  SELECT 
    user_id,
    MIN(event_date) AS first_date,
    LIST(channel) ORDER BY event_date ASC[0] AS first_channel
  FROM marketing_events
  WHERE event_type = 'touch'
    AND event_date >= '2026-01-01'
    AND event_date <= '2026-01-31'
  GROUP BY user_id
),
conversions AS (
  SELECT 
    user_id,
    MIN(order_date) AS first_order_date
  FROM orders
  WHERE order_date >= '2026-01-01'
    AND order_date <= '2026-01-31'
  GROUP BY user_id
)
SELECT 
  f.first_channel,
  COUNT(DISTINCT c.user_id) AS conversions,
  SUM(spend) AS total_spend,
  SUM(spend) / COUNT(DISTINCT c.user_id) AS cac
FROM first_touch f
JOIN conversions c ON f.user_id = c.user_id
GROUP BY f.first_channel;
```

### 模型2: Last-click attribution

```sql
-- 末触归因：最后触达渠道
WITH last_touch AS (
  SELECT 
    user_id,
    LIST(channel) ORDER BY event_date DESC[0] AS last_channel
  FROM marketing_events
  WHERE event_type = 'touch'
  GROUP BY user_id
)
SELECT 
  last_channel,
  COUNT(DISTINCT user_id) AS conversions,
  SUM(spend) AS total_spend,
  SUM(spend) / COUNT(DISTINCT user_id) AS cac
FROM last_touch lt
JOIN conversions c ON lt.user_id = c.user_id
GROUP BY last_channel;
```

### 模型3: Linear attribution

```sql
-- 线性归因：平均分配
WITH touch_sequence AS (
  SELECT 
    user_id,
    order_id,
    COUNT(*) AS touch_count
  FROM marketing_events me
  JOIN conversions c ON me.user_id = c.user_id
  GROUP BY user_id, order_id
)
SELECT 
  channel,
  COUNT(DISTINCT user_id) AS conversions,
  SUM(1.0 / touch_count) AS attributed_conversions
FROM marketing_events me
JOIN touch_sequence ts ON me.user_id = ts.user_id
GROUP BY channel;
```

### 模型4: Time-decay attribution

```sql
-- 时间衰减归因：近期渠道权重更高
WITH weighted_touches AS (
  SELECT 
    user_id,
    channel,
    event_date,
    order_date,
    DATE_DIFF(order_date, event_date) AS days_before_order
  FROM marketing_events me
  JOIN conversions c ON me.user_id = c.user_id
),
decay_weights AS (
  SELECT 
    user_id,
    channel,
    POW(0.9, days_before_order) AS weight
  FROM weighted_touches
)
SELECT 
  channel,
  SUM(weight) AS total_weight,
  SUM(weight) / (SELECT SUM(weight) FROM decay_weights) AS attribution_share
FROM decay_weights
GROUP BY channel;
```

---

## 商业场景设计

### 虚构公司: OnTime

**背景:**
- 随需配送公司
- 覆盖多个城市和地区
- 多个营销渠道

**分析目标:**
- **效率**: 降低CAC同时规模化获客
- **盈利性**: 最大化LTV vs CAC比例
- **留存**: 促进复购
- **渠道组合**: 评估渠道可持续增长能力

### Stakeholder分析

| Stakeholder | 关注点 | 决策 |
|-------------|--------|------|
| CMO/营销负责人 | 渠道预算分配 | 预算增减 |
| 增长团队 | 优化campaign | 出价调整 |
| 财务团队 | ROI验证 | 投资决策 |
| 区域负责人 | 跨市场对比 | 资源调配 |

---

## 技术栈分析

| 工具 | 用途 | 评分 |
|------|------|------|
| **Python** (pandas) | 数据清洗、原型验证 | ⭐⭐⭐⭐⭐ |
| **SQL** (PostgreSQL) | 高级分析、CTE | ⭐⭐⭐⭐⭐ |
| **Tableau** | BI可视化 | ⭐⭐⭐⭐ |
| **PowerPoint** | 商业呈现 | ⭐⭐⭐⭐ |

### 为什么这个组合高效

```
Python (清洗) → SQL (分析) → Python (验证) → Tableau (展示)
    │            │              │              │
  快速原型     复杂查询      结果验证      交互看板
```

---

## 可复用的模板

### 1. 项目README结构

```markdown
# [项目名称]

## 📌 Project Overview
[背景 + 目标]

## 🎯 Objectives
1. [目标1]
2. [目标2]
3. [目标3]

## 🛠 Tools & Tech Stack
- **Python**: [用途]
- **SQL**: [用途]
- **Tableau**: [用途]

## 📂 Repository Structure
- `raw_*.csv` → [说明]
- `clean_*.csv` → [说明]
- `*.ipynb` → [说明]
- `*.sql` → [说明]
- `*.twbx` → [说明]

## 📊 Business Case
[虚构公司背景]

## 📈 Key KPIs
| 指标 | 定义 |
|------|------|
| KPI1 | 定义 |

## 👥 Stakeholders
| 角色 | 关注点 |
|------|--------|
| CMO | 预算分配 |

## ⚠️ Disclaimer
所有数据均为合成/脱敏数据。
```

### 2. 归因SQL模板

```sql
-- [模型名称] Attribution
WITH -- CTE定义
  base_data AS (
    SELECT ...
  ),
  -- 计算逻辑
  attribution AS (
    SELECT 
      channel,
      COUNT(DISTINCT user_id) AS conversions,
      SUM(spend) AS spend,
      SUM(spend) / COUNT(DISTINCT user_id) AS cac
    FROM base_data
    GROUP BY channel
  )
-- 最终输出
SELECT 
  channel,
  conversions,
  spend,
  cac,
  ROUND(cac / AVG(cac) OVER(), 2) AS cac_index
FROM attribution
ORDER BY conversions DESC;
```

---

## 对文博GitHub的启示

### 1. 归因分析仓库

**目标仓库:** `fintech-attribution-dashboard`

**核心内容:**
```
├── sql/
│   ├── attribution_first_click.sql
│   ├── attribution_last_click.sql
│   ├── attribution_linear.sql
│   └── attribution_time_decay.sql
├── notebooks/
│   └── attribution_analysis.ipynb
├── dashboards/
│   └── attribution_dashboard.py (Streamlit)
├── data/
│   └── synthetic_data.csv (脱敏数据)
└── README.md
```

### 2. 核心SQL函数

```sql
-- 需要实现的归因函数
create function calculate_first_click_attribution();
create function calculate_last_click_attribution();
create function calculate_linear_attribution();
create function calculate_time_decay_attribution();
create function calculate_cac_by_channel();
create function calculate_ltv_by_segment();
create function calculate_roas_by_campaign();
```

### 3. 看板指标设计

| 页面 | 指标 |
|------|------|
| **概览** | 总Spend, 总转化, 整体CAC, 整体ROAS |
| **归因对比** | 各模型归因结果对比表 |
| **渠道分析** | CAC/LTV/ROAS按渠道 |
| **趋势** | 月度趋势折线图 |
| **预算建议** | 基于数据的优化建议 |

---

## 参考链接

- GitHub: https://github.com/danielguidid/delivery-industry-growth-analytics
- Tableau Public: https://public.tableau.com/app/profile/daniel.guidi

---

*分析师: 尼克·弗瑞*
*日期: 2026-04-27*
*标签: #归因分析 #Marketing #CAC #LTV #ROI #Portfolio*
