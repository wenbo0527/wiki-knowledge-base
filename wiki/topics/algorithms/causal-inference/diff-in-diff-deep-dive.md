# 双重差分法（DiD）深度指南

> 从入门到实战：DiD的原理、假设、检验与最新进展

---

## 元信息

- **创建时间**: 2026-04-22
- **维护者**: 尼克·弗瑞
- **类型**: article
- **标签**: #causal-inference #diff-in-diff #econometrics #policy-evaluation
- **难度**: ⭐⭐⭐

---

## 1. DiD的核心思想

### 1.1 基本框架

双重差分法（Difference-in-Differences，DiD）是一种用于因果推断的准实验方法，特别适用于**政策评估**场景。

```
核心思想：
┌─────────────────────────────────────────────────────────────┐
│  时间 →                                                  │
│    │           对照组          处理组                      │
│  后 │      ┌──────────┐    ┌──────────┐                   │
│    │       │   B2     │    │   A2     │                   │
│    │       │          │    │     ↑    │                   │
│ 前 │       │          │    │     │ Δ   │  ← 处理效应      │
│    │       │   B1     │    │   A1     │                   │
│    │       │          │    │          │                   │
│    └───────┴──────────┴────┴──────────┴────→              │
│              ↑                    ↑                       │
│              └──────── Δ ────────┘                       │
│                   共同趋势假设                              │
└─────────────────────────────────────────────────────────────┘

DiD估计量 = (A2 - A1) - (B2 - B1)
          =  处理组变化  -  对照组变化
          =  剔除时间趋势后的净处理效应
```

### 1.2 数学表达

| 符号 | 含义 |
|------|------|
| $Y_{it}$ | 单元i在时间t的结果 |
| $T_i$ | 处理指示变量（1=处理组，0=对照组） |
| $Post_t$ | 时间指示变量（1=处理后，0=处理前） |
| $\beta_1$ | **DiD估计量**（我们想要的因果效应） |

**标准DiD回归方程**：
```python
# OLS回归
model = smf.ols('Y ~ T * Post + T + Post', data=df).fit()

# 或者使用fixest库的贝叶斯稳健标准误
from fixest import feols
result = feols(Y ~ T | i, data=df, vcov="cluster")
```

---

## 2. 共同趋势假设

### 2.1 假设定义

**共同趋势假设（Common Trends Assumption）**：
> 如果没有处理，处理组和对照组的结果变量会以相同的趋势变化。

**关键含义**：
- 处理组和对照组的**趋势差异是稳定的**
- 处理前的数据可以"预测"处理后的反事实
- 这是DiD最核心的识别假设

### 2.2 平行趋势检验

**方法1：事件研究法（Event Study）**

```python
import pandas as pd
import statsmodels.formula.api as smf

def event_study_plot(df, outcome, time_var, treatment_var, relative_period_var):
    """
    绘制事件研究图
    """
    formula = f'{outcome} ~ C({relative_period_var}) + {treatment_var}'
    model = smf.ols(formula, data=df).fit()
    
    params = model.params
    periods = sorted(df[relative_period_var].unique())
    coef = [params.get(f'C({relative_period_var})[T.{p}]', 0) for p in periods]
    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.5, label='政策实施')
    plt.plot(periods, coef, marker='o')
    plt.xlabel(f'相对时间 ({relative_period_var})')
    plt.ylabel(f'{outcome}的系数')
    plt.title('事件研究图')
    plt.show()
```

**方法2：安慰剂检验**

```python
def placebo_test(df, outcome, treatment_var, time_var, pre_periods):
    """
    安慰剂检验：在处理前寻找"伪处理效应"
    """
    results = []
    
    for placebo_period in pre_periods:
        df_copy = df.copy()
        df_copy['placebo_post'] = (df_copy[time_var] >= placebo_period).astype(int)
        
        model = smf.ols(
            f'{outcome} ~ {treatment_var} * placebo_post + {treatment_var} + placebo_post',
            data=df_copy
        ).fit()
        
        did_coef = model.params.get(f'{treatment_var}:placebo_post')
        results.append({
            'placebo_period': placebo_period,
            'coef': did_coef,
            'p_value': model.pvalues.get(f'{treatment_var}:placebo_post')
        })
    
    return pd.DataFrame(results)
```

### 2.3 违背假设的情况

| 情况 | 说明 | 解决方案 |
|------|------|----------|
| **选择性进入** | 处理组和对照组在趋势上本就不同 | 加入控制变量、使用合成DiD |
| **预期效应** | 处理前处理组已有反应 | 排除预期效应期间 |
| **溢出效应** | 对照组也间接受到影响 | 使用边界控制、空间DiD |
| **异质性趋势** | 不同单元趋势不同 | 交错DiD、面板匹配 |

---

## 3. 交错DiD（Staggered DiD）

### 3.1 问题背景

传统DiD假设**处理状态在所有单元和时间上是一致的**，但实际中：
- 不同地区可能在不同时间点实施政策
- 某些单元可能后来加入处理组

**这导致了"负权重"问题**：
> 传统DiD估计量可能会给"后期处理"单元过大的权重，导致估计偏误。

### 3.2 Callaway-Sant'Anna (2021) 方法

**核心思想**：为每个处理 cohort 单独估计处理效应，然后加权平均。

```python
# 使用did包实现Callaway-Sant'Anna方法
from did import Did

result = Did(
    data=panel_data,
    unit_id='unit',
    time_id='time',
    y='Y',
    treatment='D',
    covariates=['age', 'income', 'education']
)

summary = result.summary(level='simple')
time_agg = result.summary(level='by_time')
cohort_agg = result.summary(level='by_cohort')
```

### 3.3 Sun-Abrahams (2022) 方法

**适用场景**：面板数据，重复横截面

```python
from fixest import feols

df['cohort'] = df.groupby('unit')['first_treated'].transform('first')

result = feols(
    Y ~ sunab(cohort, time) + controls,
    data=df,
    vcov="cluster"
)
```

---

## 4. 合成控制法（Synthetic Control Method）

### 4.1 适用场景

当**只有一个或少数几个处理单元**时，传统DiD失效。

**典型应用**：
- 加州控烟法案效果评估（只有加州实施了政策）
- 一个国家/州的特殊政策效果
- 单一企业的经营决策效果

### 4.2 方法原理

```python
from synth import Synth

synth_result = Synth(
    data=panel_data,
    unit_col='state',
    time_col='year',
    outcome_col='cigarette_sales',
    treatment_unit='California',
    treatment_period=1988
)

treatment_effect = synth_result.effect()
placebo_effects = synth_result.placebo_effects()
rmspe = synth_result.mspe_ratio()
```

---

## 5. 断点回归（RDD）

### 5.1 适用场景

当**处理分配基于某个连续变量是否超过阈值**时。

**典型应用**：
- 奖学金发放（基于考试分数是否过线）
- 银行信贷审批（基于信用分是否达标）
- 政策补贴（基于收入是否低于门槛）

### 5.2 Sharp RDD vs Fuzzy RDD

| 类型 | 说明 | 公式 |
|------|------|------|
| **Sharp RDD** | 超过阈值100%接受处理 | T_i = 1(R_i >= c) |
| **Fuzzy RDD** | 超过阈值处理概率跳跃，但不100% | P(T_i=1|R_i=c+) > P(T_i=1|R_i=c-) |

### 5.3 实现代码

```python
import statsmodels.formula.api as smf
import numpy as np

def sharp_rdd(df, outcome, running_var, cutoff, bandwidth=None):
    """Sharp RDD估计"""
    if bandwidth is None:
        bandwidth = 1.06 * np.std(running_var) * len(running_var)**(-1/5)
    
    df_rdd = df[
        (df[running_var] >= cutoff - bandwidth) &
        (df[running_var] <= cutoff + bandwidth)
    ].copy()
    
    df_rdd['running_centered'] = df_rdd[running_var] - cutoff
    df_rdd['above'] = (df_rdd['running_centered'] >= 0).astype(int)
    
    model = smf.ols(
        f'{outcome} ~ running_centered * above + above',
        data=df_rdd
    ).fit()
    
    return {
        'effect': model.params['above'],
        'se': model.std_errors['above'],
        'bandwidth': bandwidth
    }
```

---

## 6. 实战案例

### 案例：银行新政对信贷违约率的影响

**背景**：某银行在2023年1月对信贷政策进行了调整，将最低信用分要求从650提高到680。

```python
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

data = pd.read_csv('credit_data.csv')

# Step 1: 共同趋势检验（事件研究）
data['relative_month'] = data['month'] - pd.to_datetime('2023-01-01')
data['relative_month'] = data['relative_month'].dt.days / 30

data_es = data[data['relative_month'].between(-12, 12)].copy()

# Step 2: DiD估计
did_model = smf.ols(
    'default_flag ~ policy_group * post_2023_01 + policy_group + post_2023_01',
    data=data
).fit()

did_effect = did_model.params['policy_group:post_2023_01']
did_se = did_model.std_errors['policy_group:post_2023_01']

print(f"ATT = {did_effect:.4f}")
print(f"95% CI = [{did_effect - 1.96*did_se:.4f}, {did_effect + 1.96*did_se:.4f}]")
```

### 结果解读

| 指标 | 值 | 说明 |
|------|------|------|
| DiD效应 | -0.003 | 政策实施后违约率降低0.3个百分点 |
| 统计显著性 | p<0.01 | 在1%水平上显著 |
| 经济显著性 | 假设贷款规模100亿 | 每年减少损失3000万 |
| 平行趋势检验 | F=1.23, p=0.26 | 处理前趋势无显著差异 |

---

## 7. 常见陷阱

| 陷阱 | 解决方案 |
|------|----------|
| 并行趋势违背 | 加入控制变量、使用合成控制 |
| 处理前效应 | 排除预期窗口 |
| 处理效应异质性 | 使用交错DiD |
| 溢出效应 | 空间DiD |

---

*最后更新: 2026-04-22*
*维护者: 尼克·弗瑞*
