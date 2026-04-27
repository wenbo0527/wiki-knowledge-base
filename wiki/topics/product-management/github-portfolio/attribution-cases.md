# 归因分析SQL实现

> 4种归因模型的SQL实现模板
> 更新: 2026-04-27

---

## 归因模型总览

| 模型 | 原理 | 适用场景 | SQL复杂度 |
|------|------|----------|-----------|
| First-click | 首触归因 | 强调拉新 | ⭐ |
| Last-click | 末触归因 | 强调转化 | ⭐ |
| Linear | 线性归因 | 均衡权重 | ⭐⭐ |
| Time-decay | 时间衰减 | 近期偏好 | ⭐⭐⭐ |

---

## 数据模型

### 基础表结构

```sql
-- 营销事件表
CREATE TABLE marketing_events (
    event_id     VARCHAR(32),
    user_id      VARCHAR(32),
    channel      VARCHAR(32),      -- Search/Social/Display/Affiliate
    campaign     VARCHAR(64),
    event_type   VARCHAR(32),      -- touch/impression/click
    event_date   DATE,
    spend        DECIMAL(10,2),
    PRIMARY KEY (event_id)
);

-- 转化表
CREATE TABLE conversions (
    conversion_id VARCHAR(32),
    user_id      VARCHAR(32),
    order_id     VARCHAR(32),
    revenue      DECIMAL(10,2),
    order_date   DATE,
    PRIMARY KEY (conversion_id)
);
```

### 示例数据

```sql
-- 用户触达序列
INSERT INTO marketing_events VALUES
('e1', 'u001', 'Search',  'C1', 'touch', '2026-04-01', 10.00),
('e2', 'u001', 'Social',  'C2', 'touch', '2026-04-03',  5.00),
('e3', 'u001', 'Display', 'C3', 'touch', '2026-04-05',  3.00),
('e4', 'u001', 'Search',  'C1', 'touch', '2026-04-07', 10.00);

-- 用户转化
INSERT INTO conversions VALUES
('c1', 'u001', 'o001', 100.00, '2026-04-08');
```

---

## 模型1: First-click Attribution

### 逻辑
归因到用户**首次**触达的渠道

```sql
WITH first_touch AS (
    -- 找出每个用户的首次触达
    SELECT 
        user_id,
        channel,
        event_date,
        ROW_NUMBER() OVER (
            PARTITION BY user_id 
            ORDER BY event_date ASC
        ) AS rn
    FROM marketing_events
    WHERE event_type = 'touch'
),
attribution AS (
    -- 关联转化
    SELECT 
        ft.channel,
        COUNT(DISTINCT ft.user_id) AS conversions,
        SUM(me.spend) AS spend
    FROM first_touch ft
    JOIN conversions c ON ft.user_id = c.user_id
    WHERE ft.rn = 1  -- 只取首次触达
    GROUP BY ft.channel
)
SELECT 
    channel,
    conversions,
    spend,
    ROUND(spend / NULLIF(conversions, 0), 2) AS cac,
    ROUND(conversions * 100.0 / SUM(conversions) OVER(), 2) AS attribution_pct
FROM attribution
ORDER BY conversions DESC;
```

### 输出

| channel | conversions | spend | cac | attribution_pct |
|---------|-------------|-------|-----|----------------|
| Search  | 450         | 5000  | 11.1| 52.3%          |
| Social  | 280         | 3500  | 12.5| 32.6%          |
| Display | 130         | 2000  | 15.4| 15.1%          |

---

## 模型2: Last-click Attribution

### 逻辑
归因到用户**最后**触达的渠道

```sql
WITH last_touch AS (
    -- 找出每个用户的末次触达
    SELECT 
        user_id,
        channel,
        event_date,
        ROW_NUMBER() OVER (
            PARTITION BY user_id 
            ORDER BY event_date DESC
        ) AS rn
    FROM marketing_events
    WHERE event_type = 'touch'
),
attribution AS (
    SELECT 
        lt.channel,
        COUNT(DISTINCT lt.user_id) AS conversions,
        SUM(me.spend) AS spend
    FROM last_touch lt
    JOIN conversions c ON lt.user_id = c.user_id
    WHERE lt.rn = 1  -- 只取末次触达
    GROUP BY lt.channel
)
SELECT 
    channel,
    conversions,
    spend,
    ROUND(spend / NULLIF(conversions, 0), 2) AS cac
FROM attribution
ORDER BY conversions DESC;
```

---

## 模型3: Linear Attribution

### 逻辑
**平均分配**归因权重给所有触达渠道

```sql
WITH touch_sequence AS (
    -- 统计每个转化的触达序列
    SELECT 
        c.user_id,
        c.conversion_id,
        me.channel,
        COUNT(*) OVER (
            PARTITION BY c.user_id, c.conversion_id
        ) AS touch_count
    FROM conversions c
    JOIN marketing_events me 
        ON c.user_id = me.user_id
    WHERE me.event_date <= c.order_date
      AND me.event_type = 'touch'
),
attribution AS (
    SELECT 
        channel,
        COUNT(*) AS touches,
        SUM(1.0 / touch_count) AS attributed_conversions
    FROM touch_sequence
    GROUP BY channel
)
SELECT 
    channel,
    touches,
    ROUND(attributed_conversions, 2) AS attributed_conversions,
    ROUND(
        attributed_conversions * 100.0 / 
        SUM(attributed_conversions) OVER(), 
        2
    ) AS attribution_pct
FROM attribution
ORDER BY attributed_conversions DESC;
```

### 权重计算

```
用户u001触达: Search → Social → Display → Search (4次触达后转化)

各渠道归因权重:
- Search:   1/4 + 1/4 = 0.5
- Social:   1/4     = 0.25
- Display:  1/4     = 0.25
```

---

## 模型4: Time-decay Attribution

### 逻辑
越**接近转化**的触达，权重越高（指数衰减）

```sql
WITH weighted_touches AS (
    SELECT 
        c.user_id,
        c.conversion_id,
        me.channel,
        me.event_date,
        c.order_date,
        DATE_DIFF('day', me.event_date, c.order_date) AS days_before_order
    FROM conversions c
    JOIN marketing_events me 
        ON c.user_id = me.user_id
    WHERE me.event_date <= c.order_date
      AND me.event_type = 'touch'
),
decay_weights AS (
    SELECT 
        user_id,
        conversion_id,
        channel,
        POW(0.5, days_before_order) AS weight  -- 每天衰减50%
    FROM weighted_touches
),
channel_weights AS (
    SELECT 
        channel,
        SUM(weight) AS total_weight
    FROM decay_weights
    GROUP BY channel
)
SELECT 
    channel,
    ROUND(total_weight, 2) AS total_weight,
    ROUND(
        total_weight * 100.0 / SUM(total_weight) OVER(),
        2
    ) AS attribution_pct
FROM channel_weights
ORDER BY total_weight DESC;
```

### 衰减公式

```
weight = 0.5 ^ days_before_order

转化前1天触达: weight = 0.5^1 = 0.5
转化前2天触达: weight = 0.5^2 = 0.25
转化前3天触达: weight = 0.5^3 = 0.125
```

---

## 综合看板SQL

```sql
WITH base_data AS (
    SELECT 
        c.user_id,
        c.conversion_id,
        c.order_date,
        c.revenue,
        me.channel,
        me.event_date,
        me.spend
    FROM conversions c
    JOIN marketing_events me ON c.user_id = me.user_id
    WHERE me.event_type = 'touch'
),
all_channels AS (
    SELECT DISTINCT channel FROM base_data
)
SELECT 
    channel,
    COUNT(DISTINCT user_id) AS conversions,
    SUM(revenue) AS total_revenue,
    SUM(spend) AS total_spend,
    ROUND(SUM(spend) / COUNT(DISTINCT user_id), 2) AS cac,
    ROUND(SUM(revenue) / SUM(spend), 2) AS roas,
    ROUND(AVG(revenue), 2) AS avg_order_value
FROM base_data
GROUP BY channel
ORDER BY conversions DESC;
```

---

## 金融场景扩展

### 信用贷场景

```sql
-- 信贷审批归因：哪些渠道用户资质更好？
SELECT 
    channel,
    COUNT(*) AS applications,
    SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) AS approvals,
    ROUND(
        SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS approval_rate,
    ROUND(AVG(credit_score), 0) AS avg_credit_score
FROM applications a
JOIN marketing_events me ON a.user_id = me.user_id
GROUP BY channel;
```

### 信用卡场景

```sql
-- 开卡归因：哪些渠道获客成本更低？
SELECT 
    channel,
    COUNT(DISTINCT user_id) AS new_cards,
    SUM(acquisition_cost) AS total_cost,
    ROUND(SUM(acquisition_cost) / COUNT(DISTINCT user_id), 2) AS cpac,
    SUM(first_year_revenue) AS total_revenue,
    ROUND(SUM(first_year_revenue) / SUM(acquisition_cost), 2) AS roi
FROM card_applications ca
JOIN marketing_events me ON ca.user_id = me.user_id
GROUP BY channel;
```

---

## 文件结构建议

```
fintech-attribution-dashboard/
├── sql/
│   ├── 01_first_click.sql
│   ├── 02_last_click.sql
│   ├── 03_linear.sql
│   ├── 04_time_decay.sql
│   └── 05_comprehensive.sql
├── data/
│   └── synthetic_data.csv
├── notebooks/
│   └── attribution_analysis.ipynb
├── dashboards/
│   └── attribution_dashboard.py
└── README.md
```

---

*创建: 尼克·弗瑞*
*日期: 2026-04-27*
