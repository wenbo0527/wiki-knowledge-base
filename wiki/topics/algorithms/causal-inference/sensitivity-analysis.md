# 因果推断敏感性分析

> 评估因果估计的稳健性：Rosenbaum界限、混淆矩阵与元分析

---

## 元信息

- **创建时间**: 2026-04-22
- **维护者**: 尼克·弗瑞
- **类型**: article
- **标签**: #causal-inference #sensitivity-analysis #robustness #causal-inference-diagnostics
- **难度**: ⭐⭐⭐⭐

---

## 1. 为什么需要敏感性分析？

### 1.1 核心问题

> **"我们的因果估计有多稳健？"**

因果推断依赖于假设，但这些假设通常无法被完全验证。敏感性分析帮助我们回答：

- 如果假设稍微不满足，估计会如何变化？
- 存在多大程度的未观测混杂才能使结论反转？
- 结果是否对模型设定敏感？

### 1.2 敏感性分析的类型

| 类型 | 问题 | 方法 |
|------|------|------|
| **混杂敏感性** | 未观测混杂有多强才能反转结论？ | Rosenbaum界限、E值 |
| **模型设定敏感性** | 模型假设变化时结果是否稳定？ | 不同规范、不同方法对比 |
| **样本敏感性** | 样本选择偏差的影响？ | 逆概率加权敏感性分析 |
| **测量误差敏感性** | 变量测量误差的影响？ | 误差传播分析 |

---

## 2. Rosenbaum界限

### 2.1 核心思想

**Rosenbaum Bounds (1987)** 回答一个关键问题：

> "如果存在未观测混杂，它需要多强才能使统计显著的结果变为不显著？"

### 2.2 数学框架

对于二元处理情况，Rosenbaum界限考虑**倾向得分的不确定性**：

```
定义 Γ（Gamma）为混杂强度的上界：
Γ = max(P(T=1|X,U))/min(P(T=1|X,U))

其中U是未观测混杂因素

Rosenbaum不等式：
- 上界：P(T=1|X) ≤ min(Γ*P(T=1|X), 1)
- 下界：P(T=1|X) ≥ P(T=1|X)/Γ
```

### 2.3 实现代码

```python
import numpy as np
from scipy import stats

def rosenbaum_bounds(data, outcome_var, treatment_var, gamma_range=None):
    """
    计算Rosenbaum界限
    
    参数:
    - data: DataFrame
    - outcome_var: 结果变量名
    - treatment_var: 处理变量名
    - gamma_range: Γ值范围
    
    返回:
    - bounds: 显著性水平的上下界
    """
    if gamma_range is None:
        gamma_range = np.arange(1.0, 3.0, 0.1)
    
    Y = data[outcome_var].values
    T = data[treatment_var].values
    
    # 计算处理组和对照组的观察值差异
    Y_t = Y[T == 1]
    Y_c = Y[T == 0]
    
    observed_diff = Y_t.mean() - Y_c.mean()
    n_t, n_c = len(Y_t), len(Y_c)
    
    # 计算Wilcoxon秩和统计量
    all_Y = np.concatenate([Y_t, Y_c])
    ranks = stats.rankdata(all_Y)
    W = ranks[:n_t].sum()
    
    results = []
    
    for Gamma in gamma_range:
        # 计算在混杂强度Γ下的p值界限
        # 上界（过度估计处理效应）
        log_odds_ratio = np.log(Gamma)
        
        # 渐近p值（使用Chernoff界限）
        # 这是一个简化版本
        alpha_upper = np.exp(-2 * (W - n_t * (n_t + n_c + 1) / 2)**2 / (n_t * n_c * (n_t + n_c + 1) / 3))
        
        results.append({
            'Gamma': Gamma,
            'p_value_lower': max(0, 1 - alpha_upper),  # 简化
            'p_value_upper': min(1, alpha_upper * Gamma),  # 简化
            'significant_at_5pct': alpha_upper < 0.05,
            'significant_at_1pct': alpha_upper < 0.01
        })
    
    return pd.DataFrame(results)


# 使用示例
# df = pd.read_csv('ab_test_data.csv')
# bounds = rosenbaum_bounds(df, 'conversion', 'treatment', gamma_range=np.arange(1.0, 2.5, 0.1))
# print(bounds)
```

### 2.4 结果解读

```python
def interpret_rosenbaum(bounds_df):
    """解释Rosenbaum界限结果"""
    print("="*60)
    print("Rosenbaum界限解读")
    print("="*60)
    
    # 找到使结果不再显著的最小Γ值
    not_significant = bounds_df[~bounds_df['significant_at_5pct']]
    
    if len(not_significant) > 0:
        critical_gamma = not_significant['Gamma'].min()
        print(f"\n临界Γ值 (p<0.05变为不显著): {critical_gamma:.1f}")
        print(f"\n解读:")
        print(f"  - 如果未观测混杂使处理组和对照组在处理概率上")
        print(f"    差异超过{critical_gamma:.1f}倍，结论将被反转")
        print(f"  - 一般认为Γ<2时结论较为稳健")
    else:
        print("\n即使Γ=3，结论仍然显著")
        print("结论对未观测混杂非常稳健")
```

---

## 3. E值（E-value）

### 3.1 概念定义

**E-value (VanderWeele & Ding, 2017)**：

> 评估"使因果结论无效所需的最弱未观测混杂强度"。

```python
def compute_evalue(rr, se_log_rr=None, ci_lower=None, ci_upper=None):
    """
    计算E-value
    
    参数:
    - rr: 相对风险（处理组结果率 / 对照组结果率）
    - se_log_rr: 对数相对风险的标准误
    - ci_lower: 95%置信区间下界
    - ci_upper: 95%置信区间上界
    
    返回:
    - evalue: 使结论无效所需的最小混杂风险比
    """
    # E-value for point estimate
    if rr <= 1:
        evalue_point = rr
    else:
        evalue_point = rr + np.sqrt(rr * (rr - 1))
    
    # E-value for CI
    if ci_lower is not None and ci_upper is not None:
        if ci_lower <= 1:
            evalue_ci = ci_lower + np.sqrt(ci_lower * (ci_lower - 1))
        else:
            evalue_ci = ci_lower + np.sqrt(ci_lower * (ci_lower - 1))
        
        return {
            'E_value_point': evalue_point,
            'E_value_CI_lower': evalue_ci,
            'interpretation': f"未观测混杂需要使处理组结果风险比为{evalue_point:.2f}才能反转结论"
        }
    
    return {
        'E_value_point': evalue_point,
        'interpretation': f"未观测混杂需要使处理组结果风险比为{evalue_point:.2f}才能反转结论"
    }


# 使用示例
print(compute_evalue(rr=1.5, ci_lower=1.2, ci_upper=1.9))
# E_value_point ≈ 1.87
# E_value_CI_lower ≈ 1.34

print(compute_evalue(rr=2.0))
# E_value_point ≈ 2 + sqrt(2) ≈ 3.41
```

### 3.2 E值可视化

```python
def plot_evalue_heatmap(rr_range, gamma_range):
    """
    绘制E值热力图
    """
    evalues = np.zeros((len(rr_range), len(gamma_range)))
    
    for i, rr in enumerate(rr_range):
        for j, gamma in enumerate(gamma_range):
            # E值作为Γ的函数
            if rr <= 1:
                evalues[i, j] = 1.0
            else:
                evalues[i, j] = min(rr + np.sqrt(rr * (rr - 1)), gamma)
    
    plt.figure(figsize=(10, 6))
    plt.contourf(gamma_range, rr_range, evalues, levels=20)
    plt.colorbar(label='E-value')
    plt.xlabel('混杂强度 (Γ)')
    plt.ylabel('观察到的相对风险 (RR)')
    plt.title('E值敏感性分析')
    plt.axhline(y=1, color='white', linestyle='--', alpha=0.5)
    plt.axvline(x=1, color='white', linestyle='--', alpha=0.5)
    
    return plt
```

---

## 4. 倾向得分敏感性分析

### 4.1 核心思想

当使用**倾向得分匹配（PSM）**时，我们需要评估：

- 倾向得分模型是否正确指定？
- 未观测混杂会如何影响匹配平衡性？
- 处理效应估计对倾向得分规范有多敏感？

### 4.2 平衡性敏感性

```python
def balance_sensitivity_analysis(df, covariates, treatment_var, propensity_model=None):
    """
    评估匹配后的平衡性及其对未观测混杂的敏感性
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import NearestNeighborMatcher
    
    # 如果没有提供倾向得分模型，使用默认logit
    if propensity_model is None:
        propensity_model = LogisticRegression()
    
    # 计算倾向得分
    X = df[covariates].values
    T = df[treatment_var].values
    propensity_model.fit(X, T)
    df['propensity_score'] = propensity_model.predict_proba(X)[:, 1]
    
    # 分离处理组和对照组
    treated = df[df[treatment_var] == 1]
    control = df[df[treatment_var] == 0]
    
    # 计算标准化均值差异（SMD）before matching
    smd_before = {}
    for cov in covariates:
        mean_t = treated[cov].mean()
        mean_c = control[cov].mean()
        pooled_std = df[cov].std()
        smd_before[cov] = abs(mean_t - mean_c) / pooled_std
    
    # Nearest Neighbor Matching
    matcher = NearestNeighborMatcher(n_neighbors=1, replacement=False)
    
    # 匹配
    matched_idx = matcher.match(treated['propensity_score'], control['propensity_score'])
    matched = treated.iloc[matched_idx].copy()
    
    # 计算after matching SMD
    smd_after = {}
    for cov in covariates:
        mean_t = matched[cov].mean()
        mean_c = control.iloc[matched_idx][cov].mean()
        pooled_std = df[cov].std()
        smd_after[cov] = abs(mean_t - mean_c) / pooled_std
    
    # 敏感性分析：如果存在未观测混杂
    def sensitivity_correction(smd, U_strength, sigma_U=1):
        """
        校正SMD以考虑未观测混杂
        U_strength: 未观测混杂与处理的关系强度
        """
        return smd * np.sqrt(1 + U_strength**2 * sigma_U**2)
    
    results = pd.DataFrame({
        'Covariate': covariates,
        'SMD_before': [smd_before[c] for c in covariates],
        'SMD_after': [smd_after[c] for c in covariates],
        'SMD_with_U_0.1': [sensitivity_correction(smd_after[c], 0.1) for c in covariates],
        'SMD_with_U_0.2': [sensitivity_correction(smd_after[c], 0.2) for c in covariates],
    })
    
    print("平衡性敏感性分析结果:")
    print(results.round(4))
    
    # 阈值判断
    problematic = results[results['SMD_with_U_0.2'] > 0.1]['Covariate'].tolist()
    if problematic:
        print(f"\n⚠️ 在U=0.2的未观测混杂假设下，以下协变量不平衡: {problematic}")
    else:
        print("\n✅ 即使存在中等强度未观测混杂，平衡性仍然良好")
    
    return results
```

---

## 5. 模型设定敏感性

### 5.1 不同规范的敏感性

```python
def specification_sensitivity(df, outcome, treatment, covariates_list):
    """
    测试不同模型规范对处理效应估计的影响
    """
    import statsmodels.formula.api as smf
    
    results = []
    
    for covariates in covariates_list:
        formula = f'{outcome} ~ {treatment}'
        
        if len(covariates) > 0:
            formula += ' + ' + ' + '.join(covariates)
        
        model = smf.ols(formula, data=df).fit()
        
        effect = model.params[treatment]
        se = model.std_errors[treatment]
        pvalue = model.pvalues[treatment]
        
        results.append({
            'covariates': ', '.join(covariates) if covariates else 'none',
            'n_covariates': len(covariates),
            'effect': effect,
            'se': se,
            'pvalue': pvalue,
            'ci_lower': effect - 1.96 * se,
            'ci_upper': effect + 1.96 * se
        })
    
    return pd.DataFrame(results)


# 使用示例
# df = pd.read_csv('experiment_data.csv')
# 
# specs = [
#     [],  # 无协变量
#     ['age'],  # 只控制年龄
#     ['age', 'income'],  # 控制年龄和收入
#     ['age', 'income', 'education'],  # 控制更多
#     ['age', 'income', 'education', 'gender', 'region'],  # 全控制
# ]
# 
# sens_results = specification_sensitivity(df, 'outcome', 'treatment', specs)
# print(sens_results)
```

### 5.2 结果可视化

```python
def plot_specification_sensitivity(results_df):
    """
    可视化不同规范的效应估计
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = range(len(results_df))
    ax.errorbar(
        x, 
        results_df['effect'], 
        yerr=1.96*results_df['se'],
        fmt='o',
        capsize=5,
        label='效应估计 (95% CI)'
    )
    
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='零效应线')
    ax.set_xticks(x)
    ax.set_xticklabels(results_df['covariates'], rotation=45, ha='right')
    ax.set_xlabel('模型规范')
    ax.set_ylabel('处理效应估计')
    ax.set_title('模型设定敏感性分析')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('specification_sensitivity.png')
    
    return fig
```

---

## 6. 元分析敏感性

### 6.1 概念

当多个研究估计同一因果效应时，**元分析**可以评估：

- 总体效应是否稳健？
- 研究间异质性有多大？
- 某些研究是否影响了总体结论？

### 6.2 固定效应 vs 随机效应

```python
def meta_analysis_sensitivity(effect_sizes, standard_errors, method='random'):
    """
    元分析敏感性分析
    
    参数:
    - effect_sizes: 各研究的效应估计
    - standard_errors: 各研究的标准误
    - method: 'fixed' 或 'random'
    """
    import numpy as np
    from scipy import stats
    
    k = len(effect_sizes)
    weights = 1 / (standard_errors ** 2)
    
    if method == 'fixed':
        # 固定效应模型
        pooled_effect = np.sum(weights * effect_sizes) / np.sum(weights)
        pooled_se = np.sqrt(1 / np.sum(weights))
    else:
        # 随机效应模型 (DerSimonian-Laird)
        Q = np.sum(weights * (effect_sizes - np.average(effect_sizes, weights=weights))**2)
        df = k - 1
        
        # 估计tau^2（研究间方差）
        tau2 = max(0, (Q - df) / (np.sum(weights) - np.sum(weights**2) / np.sum(weights)))
        
        # 随机效应权重
        weights_re = 1 / (standard_errors**2 + tau2)
        
        pooled_effect = np.sum(weights_re * effect_sizes) / np.sum(weights_re)
        pooled_se = np.sqrt(1 / np.sum(weights_re))
        
        tau2_estimate = tau2
    
    # 置信区间
    ci_lower = pooled_effect - 1.96 * pooled_se
    ci_upper = pooled_effect + 1.96 * pooled_se
    
    # p值
    z = pooled_effect / pooled_se
    pvalue = 2 * (1 - stats.norm.cdf(abs(z)))
    
    result = {
        'pooled_effect': pooled_effect,
        'pooled_se': pooled_se,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'pvalue': pvalue,
        'method': method
    }
    
    if method == 'random':
        result['tau2'] = tau2_estimate
    
    return result


# 使用示例
# 假设我们有5个独立研究的效应估计
# effects = [0.15, 0.22, 0.18, 0.25, 0.12]
# ses = [0.05, 0.06, 0.04, 0.07, 0.05]
# 
# fixed_result = meta_analysis_sensitivity(effects, ses, 'fixed')
# random_result = meta_analysis_sensitivity(effects, ses, 'random')
# 
# print("固定效应:", fixed_result)
# print("随机效应:", random_result)
```

### 6.3 留一法敏感性分析

```python
def leave_one_out_sensitivity(effect_sizes, standard_errors):
    """
    留一法元分析：评估每个研究对总体