# Uplift Modeling进阶：增量效应建模与营销优化

> 从传统响应模型到因果推断驱动的Uplift Modeling，实现真正的营销增量优化

---

## 元信息

- **创建时间**: 2026-04-22
- **维护者**: 尼克·弗瑞
- **类型**: article
- **标签**: #causal-inference #uplift-modeling #marketing #causal-ml #incremental-effect
- **难度**: ⭐⭐⭐⭐

---

## 1. 什么是Uplift Modeling？

### 1.1 传统响应模型 vs Uplift模型

**传统响应模型**：
```
P(Y=1|X) = P(购买|用户特征)

问题：这包括了"本来就会购买的用户"
结果：浪费营销预算在已转化客户身上
```

**Uplift模型**：
```
U(X) = P(Y=1|T=1,X) - P(Y=1|T=0,X) = ΔP

目标：识别"营销增量最大的用户"
即：只有收到营销才会购买的用户
```

### 1.2 四象限用户分群

```
                    购买倾向高
                        │
           Non-       │       │
         Persuadables │  │ Convertibles
           (无感度)   │  │ (自然转化)
                        │
────────────────────────┼─────────────────────────
                        │
           Lost Causes  │   Persuadables
           (流失用户)   │  (应触达用户)
                        │
                        │ 购买倾向低
```

| 群体 | 购买(T=1) | 购买(T=0) | Uplift | 营销策略 |
|------|-----------|-----------|--------|----------|
| **Persuadables** | 高 | 低 | **高** | ⭐ 优先触达 |
| **Convertibles** | 高 | 高 | 低 | 自然转化，减少触达 |
| **Lost Causes** | 低 | 低 | 低 | 不触达 |
| **Sleeping Dogs** | 低 | 高 | **负** | ⚠️ 避免触达 |

### 1.3 数学定义

**个体处置效应（Individual Treatment Effect）**：

```
τ(x) = E[Y(1) - Y(0) | X=x]

其中：
- Y(1): 处理条件下的潜在结果
- Y(0): 对照条件下的潜在结果
- X: 用户特征

由于无法同时观测Y(1)和Y(0)，需要估计τ(x)
```

---

## 2. Uplift Modeling方法

### 2.1 方法分类

```
Uplift Modeling方法
├── 基于元学习器（Meta-Learners）
│   ├── S-Learner（单模型）
│   ├── T-Learner（双模型）
│   ├── X-Learner
│   ├── R-Learner（Robinson）
│   └── Class Transformation法
│
├── 直接建模（Two-Model变体）
│   ├── 差分响应模型
│   ├── 加权差分模型
│   └── 倾向加权
│
└── 专门Uplift模型
    ├── Uplift决策树
    ├── Uplift随机森林
    └── 深度Uplift网络
```

### 2.2 S-Learner（单模型）

```python
class SLearnerUplift:
    """
    S-Learner: 将处理变量作为特征，用单一模型估计
    
    τ(x) = E[Y|X=x, T=1] - E[Y|X=x, T=0]
    """
    
    def __init__(self, base_model=None):
        if base_model is None:
            self.model = GradientBoostingClassifier(n_estimators=100)
        else:
            self.model = base_model
    
    def fit(self, X, T, Y):
        """
        训练
        
        X: 特征矩阵
        T: 处理指示 (1=处理组, 0=对照组)
        Y: 结果 (1=转化, 0=未转化)
        """
        # 将T作为特征加入
        X_with_t = np.column_stack([X, T])
        
        self.model.fit(X_with_t, Y)
        self.feature_names = list(X.columns) + ['treatment']
    
    def predict_uplift(self, X):
        """
        预测Uplift
        
        U(x) = P(Y=1|X, T=1) - P(Y=1|X, T=0)
        """
        # 预测T=1的结果
        X_t1 = np.column_stack([X.values, np.ones(len(X))])
        pred_t1 = self.model.predict_proba(X_t1)[:, 1]
        
        # 预测T=0的结果
        X_t0 = np.column_stack([X.values, np.zeros(len(X))])
        pred_t0 = self.model.predict_proba(X_t0)[:, 1]
        
        return pred_t1 - pred_t0


# 使用示例
uplift_model = SLearnerUplift()
uplift_model.fit(X_train, T_train, Y_train)

uplift_scores = uplift_model.predict_uplift(X_test)

# 分层
df_test = X_test.copy()
df_test['uplift'] = uplift_scores
df_test['segment'] = pd.qcut(df_test['uplift'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

print(df_test.groupby('segment')[['uplift', 'treatment', 'conversion']].mean())
```

### 2.3 T-Learner（双模型）

```python
class TLearnerUplift:
    """
    T-Learner: 分别用处理组和对照组数据训练两个模型
    
    τ(x) = E[Y|T=1,X=x] - E[Y|T=0,X=x]
    """
    
    def __init__(self, base_model=None):
        if base_model is None:
            self.model_t = GradientBoostingRegressor(n_estimators=100)
            self.model_c = GradientBoostingRegressor(n_estimators=100)
        else:
            self.model_t = clone(base_model)
            self.model_c = clone(base_model)
    
    def fit(self, X, T, Y):
        """
        分别训练处理组和对照组模型
        """
        # 处理组数据
        idx_t = T == 1
        self.model_t.fit(X[idx_t], Y[idx_t])
        
        # 对照组数据
        idx_c = T == 0
        self.model_c.fit(X[idx_c], Y[idx_c])
    
    def predict_uplift(self, X):
        """
        预测Uplift
        """
        pred_t = self.model_t.predict(X)
        pred_c = self.model_c.predict(X)
        
        return pred_t - pred_c


# 优点：模型可以更灵活地处理不同组
# 缺点：每组数据量减少，模型方差增大
```

### 2.4 X-Learner（更鲁棒）

```python
class XLearnerUplift:
    """
    X-Learner: 处理数据量不平衡和效果异质性
    
    步骤：
    1. 分别训练处理组和对照组模型
    2. 计算伪处置效应（ imputed treatment effects）
    3. 训练处置效应模型
    4. 用倾向得分加权组合
    """
    
    def __init__(self, base_model=None):
        if base_model is None:
            self.model_t = GradientBoostingRegressor(n_estimators=100)
            self.model_c = GradientBoostingRegressor(n_estimators=100)
            self.model_tau_t = GradientBoostingRegressor(n_estimators=100)
            self.model_tau_c = GradientBoostingRegressor(n_estimators=100)
        else:
            self.model_t = clone(base_model)
            self.model_c = clone(base_model)
            self.model_tau_t = clone(base_model)
            self.model_tau_c = clone(base_model)
    
    def fit(self, X, T, Y):
        # Step 1: 训练基础模型
        idx_t = T == 1
        idx_c = T == 0
        
        self.model_t.fit(X[idx_t], Y[idx_t])  # 处理组模型
        self.model_c.fit(X[idx_c], Y[idx_c])  # 对照组模型
        
        # Step 2: 计算伪处置效应
        # 对处理组：用对照模型预测，处理组真实-预测
        tau_t = Y[idx_t] - self.model_c.predict(X[idx_t])
        
        # 对照组：用处理模型预测，处理预测-对照真实
        tau_c = self.model_t.predict(X[idx_c]) - Y[idx_c]
        
        # Step 3: 训练处置效应模型
        self.model_tau_t.fit(X[idx_t], tau_t)  # 处理组的伪效应
        self.model_tau_c.fit(X[idx_c], tau_c)  # 对照组的伪效应
    
    def predict_uplift(self, X):
        # 估计倾向得分
        propensity = self._estimate_propensity(X)
        
        # 加权组合两个处置效应估计
        tau_t_pred = self.model_tau_t.predict(X)
        tau_c_pred = self.model_tau_c.predict(X)
        
        # 根据倾向得分加权
        uplift = propensity * tau_c_pred + (1 - propensity) * tau_t_pred
        
        return uplift
    
    def _estimate_propensity(self, X):
        """估计倾向得分"""
        # 简化：使用0.5作为倾向得分
        # 实际应该用倾向得分模型估计
        return np.full(len(X), 0.5)
```

### 2.5 Class Transformation法（Jaskowski & Jaroszewicz）

```python
class ClassTransformationUplift:
    """
    Class Transformation: 简化版但高效的Uplift建模
    
    核心思想：将Uplift问题转化为标准分类问题
    
    对于二元结果：
    U(x) ≈ 2 * P(Y=1|X, D=1) - 1  当 D=Y时
          ≈ 2 * P(Y=0|X, D=0) - 1  当 D≠Y时
    
    简化为：
    U(x) ≈ 2 * E[D*Y - (1-D)*(1-Y) | X]
    """
    
    def __init__(self, base_model=None):
        if base_model is None:
            self.model = GradientBoostingClassifier(n_estimators=100)
        else:
            self.model = base_model
    
    def fit(self, X, T, Y):
        """
        转换目标变量
        """
        # 转换目标：Z = Y*D + (1-Y)*(1-D) = Y*D + (1-D) - Y*(1-D) 
        # 简化：Z = D*(2*Y-1) + (1-Y)
        # 实际使用更简洁的版本
        Z = T * Y - (1 - T) * (1 - Y)  # Jaskowski公式
        
        # 训练分类器
        self.model.fit(X, Z)
    
    def predict_uplift(self, X):
        """
        预测Uplift
        """
        # P(Z=1|X) ≈ U(x)/2 + 0.5
        p_z1 = self.model.predict_proba(X)[:, 1]
        
        # U(x) = 2 * P(Z=1|X) - 1
        uplift = 2 * p_z1 - 1
        
        return uplift
```

---

## 3. 评估指标

### 3.1 Qini系数

```python
def qini_score(y_true, uplift, treatment, n_bins=10):
    """
    计算Qini系数
    
    Qini = Area Under Qini Curve
    
    Qini曲线：按uplift分数排序，计算累积增量
    """
    df = pd.DataFrame({
        'y': y_true,
        'uplift': uplift,
        'treatment': treatment
    })
    
    # 按uplift分数排序
    df = df.sort_values('uplift', ascending=False)
    
    n = len(df)
    bin_size = n // n_bins
    
    cumulative_lift = []
    cumulative_treated = []
    cumulative_control = []
    
    for i in range(n_bins):
        start_idx = i * bin_size
        end_idx = (i + 1) * bin_size if i < n_bins - 1 else n
        
        bin_df = df.iloc[start_idx:end_idx]
        
        # 计算该bin的转化率差异
        treated = bin_df[bin_df['treatment'] == 1]
        control = bin_df[bin_df['treatment'] == 0]
        
        if len(treated) > 0 and len(control) > 0:
            rate_treated = treated['y'].mean()
            rate_control = control['y'].mean()
            lift = rate_treated - rate_control
            
            cumulative_lift.append(lift * len(bin_df))
            cumulative_treated.append(treated['y'].sum())
            cumulative_control.append(control['y'].sum())
    
    # 计算Qini曲线下面积（简化版）
    qini = sum(cumulative_lift)
    
    return qini


def qini_curve(y_true, uplift, treatment, n_bins=100):
    """
    计算完整的Qini曲线
    """
    df = pd.DataFrame({
        'y': y_true,
        'uplift': uplift,
        'treatment': treatment
    })
    
    df = df.sort_values('uplift', ascending=False)
    
    # 计算累积统计
    cum_treated_y = df[df['treatment']==1]['y'].cumsum()
    cum_treated_n = (df['treatment']==1).cumsum()
    cum_control_y = df[df['treatment']==0]['y'].cumsum()
    cum_control_n = (df['treatment']==0).cumsum()
    
    # 避免除零
    cum_treated_n = cum_treated_n.replace(0, np.nan)
    cum_control_n = cum_control_n.replace(0, np.nan)
    
    # Qini曲线
    qini_curve = (cum_treated_y / cum_treated_n) - (cum_control_y / cum_control_n)
    
    return qini_curve.fillna(0).values
```

### 3.2 AUUC（Area Under Uplift Curve）

```python
def auuc_score(y_true, uplift, treatment):
    """
    计算AUUC（Uplift曲线下面积）
    
    对比随机选择，AUUC表示增量收益
    """
    df = pd.DataFrame({
        'y': y_true,
        'uplift': uplift,
        'treatment': treatment
    })
    
    df = df.sort_values('uplift', ascending=False)
    
    n = len(df)
    
    # 计算uplift曲线
    uplift_curve = []
    random_uplift = []
    
    for i in range(1, n + 1):
        # 前i个样本
        top_i = df.iloc[:i]
        
        # 实际uplift
        treated = top_i[top_i['treatment'] == 1]
        control = top_i[top_i['treatment'] == 0]
        
        if len(treated) > 0 and len(control) > 0:
            actual = treated['y'].sum() / len(treated) - control['y'].sum() / len(control)
        else:
            actual = 0
        
        uplift_curve.append(actual)
        
        # 随机uplift（期望为0）
        random_uplift.append(0)
    
    # 计算AUUC（曲线下面积 - 随机基线）
    uplift_curve = np.array(uplift_curve)
    random_uplift = np.array(random_uplift)
    
    auuc = np.trapz(uplift_curve - random_uplift) / n
    
    return auuc
```

### 3.3 提升曲线

```python
def plot_uplift_curves(y_true, uplift, treatment):
    """
    绘制Uplift曲线和Qini曲线
    """
    df = pd.DataFrame({
        'y': y_true,
        'uplift': uplift,
        'treatment': treatment
    })
    
    df = df.sort_values('uplift', ascending=False)
    
    # 计算累积增量
    n = len(df)
    percentiles = np.arange(10, 110, 10)
    
    results = []
    for p in percentiles:
        idx = int(n * p / 100)
        top_p = df.iloc[:idx]
        
        treated = top_p[top_p['treatment'] == 1]
        control = top_p[top_p['treatment'] == 0]
        
        if len(treated) > 0 and len(control) > 0:
            uplift = treated['y'].mean() - control['y'].mean()
            n_treated = len(treated)
            n_control = len(control)
        else:
            uplift = 0
            n_treated = 0
            n_control = 0
        
        results.append({
            'percentile': p,
            'uplift': uplift,
            'n_treated': n_treated,
            'n_control': n_control,
            'incremental_response': uplift * n_treated
        })
    
    return pd.DataFrame(results)


# 使用示例
results = plot_uplift_curves(Y_test, uplift_scores, T_test)
print(results)
```

---

## 4. CausalML实现

### 4.1 CausalML库

```python
from causalml.inference.meta import (
    BaseTClassifier, BaseRClassifier, BaseXClassifier, BaseSClassifier,
    BaseDRClassifier, BaseTMLEClassifier
)
from causalml.inference uplift import (
    uplift_nn, uplift_kNeighbors, uplift_random_forest
)
from causalml.metrics import qini_score, auuc_score, uplift_curve

# T-Learner
t_learner = BaseTClassifier(
    learner=GradientBoostingClassifier(n_estimators=100)
)
t_learner.fit(X=X_train, treatment=T_train, y=Y_train)
uplift_t = t_learner.predict(X=X_test)

# X-Learner
x_learner = BaseXClassifier(
    learner=GradientBoostingClassifier(n_estimators=100)
)
x_learner.fit(X=X_train, treatment=T_train, y=Y_train)
uplift_x = x_learner.predict(X=X_test)

# S-Learner
s_learner = BaseSClassifier(

s_learner.fit(X=X_train, treatment=T_train, y=Y_train)
uplift_s = s_learner.predict(X=X_test)

# DR-Learner（双重稳健）
dr_learner = BaseDRClassifier(
    learner=GradientBoostingClassifier(n_estimators=100)
)
dr_learner.fit(X=X_train, treatment=T_train, y=Y_train)
uplift_dr = dr_learner.predict(X=X_test)

# 评估对比
print("Qini Score:")
print(f"  T-Learner: {qini_score(Y_test, uplift_t, T_test):.4f}")
print(f"  X-Learner: {qini_score(Y_test, uplift_x, T_test):.4f}")
print(f"  S-Learner: {qini_score(Y_test, uplift_s, T_test):.4f}")
print(f"  DR-Learner: {qini_score(Y_test, uplift_dr, T_test):.4f}")

print("\nAUUC:")
print(f"  T-Learner: {auuc_score(Y_test, uplift_t, T_test):.4f}")
print(f"  X-Learner: {auuc_score(Y_test, uplift_x, T_test):.4f}")
```

### 4.2 EconML实现

```python
from econml.dml import CausalForestDML, LinearDML
from econml.metalearners import XLearner, TLearner, SLearner

# CausalForestDML（双重机器学习）
causal_forest = CausalForestDML(
    model_y=GradientBoostingRegressor(n_estimators=100),
    model_t=GradientBoostingClassifier(n_estimators=100),
    n_estimators=100,
    random_state=42
)

causal_forest.fit(Y_train, T_train, X=X_train)
uplift_forest = causal_forest.effect(X_test)

# X-Learner from EconML
x_learner_econml = XLearner(
    models=GradientBoostingRegressor(n_estimators=100)
)
x_learner_econml.fit(Y_train, T_train, X=X_train)
uplift_x_econml = x_learner_econml.effect(X_test)

# 置信区间
effect_interval = causal_forest.effect_interval(X_test, alpha=0.05)
print(f"95% CI: [{effect_interval[0].mean():.4f}, {effect_interval[1].mean():.4f}]")
```

---

## 5. 金融营销实战案例

### 5.1 场景：银行信用卡营销

**背景**：
- 银行计划向100万客户发送营销短信
- 目标：提升信用卡申请转化率
- 预算：只能触达30%客户
- 需要识别最有响应倾向的客户

**解决方案**：Uplift Modeling

```python
class BankMarketingUpliftModel:
    """
    银行营销Uplift模型
    """
    
    def __init__(self):
        self.uplift_model = None
        self.propensity_model = None
        self.best_method = None
    
    def train(self, historical_data, features, treatment_col, outcome_col):
        """
        训练Uplift模型
        """
        X = historical_data[features]
        T = historical_data[treatment_col]  # 是否发送短信
        Y = historical_data[outcome_col]     # 是否申请信用卡
        
        # 评估多种方法
        methods = {
            'T-Learner': TLearnerUplift(),
            'X-Learner': XLearnerUplift(),
            'Class-Transformation': ClassTransformationUplift(),
            'S-Learner': SLearnerUplift()
        }
        
        results = {}
        
        for name, model in methods.items():
            model.fit(X, T, Y)
            uplift_pred = model.predict_uplift(X)
            
            # 计算Qini分数
            qini = qini_score(Y.values, uplift_pred, T.values)
            auuc = auuc_score(Y.values, uplift_pred, T.values)
            
            results[name] = {
                'model': model,
                'qini': qini,
                'auuc': auuc,
                'uplift_pred': uplift_pred
            }
        
        # 选择最佳方法
        best_qini = max(results.items(), key=lambda x: x[1]['qini'])
        self.best_method = best_qini[0]
        self.uplift_model = best_qini[1]['model']
        
        print(f"最佳方法: {self.best_method}")
        print(f"Qini Score: {best_qini[1]['qini']:.4f}")
        
        return results
    
    def predict_target_customers(self, candidate_data, top_percent=30):
        """
        预测并选择目标客户
        """
        # 预测uplift
        uplift_scores = self.uplift_model.predict_uplift(candidate_data)
        
        # 添加uplift分数
        candidate_data = candidate_data.copy()
        candidate_data['uplift_score'] = uplift_scores
        
        # 按uplift分数排序，选择top百分比
        candidate_data = candidate_data.sort_values('uplift_score', ascending=False)
        
        n_target = int(len(candidate_data) * top_percent / 100)
        target_customers = candidate_data.head(n_target)
        
        return target_customers, candidate_data
    
    def evaluate_campaign(self, target_df, non_target_df):
        """
        评估营销活动效果
        """
        # 预估增量效果
        avg_uplift = target_df['uplift_score'].mean()
        n_target = len(target_df)
        
        # 预估转化增量
        estimated_incremental = avg_uplift * n_target
        
        return {
            'target_size': n_target,
            'avg_uplift': avg_uplift,
            'estimated_incremental_conversions': estimated_incremental,
            'roi_comparison': self._estimate_roi(target_df, non_target_df)
        }
    
    def _estimate_roi(self, target_df, non_target_df):
        """
        估算ROI
        """
        # 假设
        marketing_cost_per_customer = 1.0  # 每客户营销成本
        average_card_value = 500  # 每张信用卡平均价值
        
        total_cost = len(target_df) * marketing_cost_per_customer
        expected_conversions = target_df['uplift_score'].sum()
        expected_revenue = expected_conversions * average_card_value
        
        roi = (expected_revenue - total_cost) / total_cost
        
        return {
            'total_cost': total_cost,
            'expected_conversions': expected_conversions,
            'expected_revenue': expected_revenue,
            'roi': roi
        }


# 使用示例
# 加载历史营销数据
# historical_df = pd.read_csv('bank_marketing_history.csv')
# 
# features = ['age', 'income', 'balance', 'tenure', 'num_products', 'credit_score']
# 
# bank_model = BankMarketingUpliftModel()
# results = bank_model.train(historical_df, features, 'sms_sent', 'card_applied')
# 
# # 选择目标客户
# candidate_df = pd.read_csv('candidate_customers.csv')
# target_customers, all_customers = bank_model.predict_target_customers(
#     candidate_df, 
#     top_percent=30
# )
# 
# # 评估
# non_target = all_customers.iloc[len(target_customers):]
# campaign_eval = bank_model.evaluate_campaign(target_customers, non_target)
# print(campaign_eval)
```

### 5.2 保险推荐实战

```python
class InsuranceUpliftModel:
    """
    保险产品Uplift模型
    识别哪些客户收到保险推荐后更可能购买
    """
    
    def __init__(self):
        self.models = {}
    
    def train_with_classification(
        self, 
        X_train, T_train, Y_train,
        X_test, T_test, Y_test
    ):
        """
        使用Class Transformation训练
        """
        # Class Transformation
        ct_model = ClassTransformationUplift(
            base_model=GradientBoostingClassifier(n_estimators=100)
        )
        ct_model.fit(X_train, T_train, Y_train)
        
        # 预测uplift
        uplift_pred = ct_model.predict_uplift(X_test)
        
        # 评估
        qini = qini_score(Y_test, uplift_pred, T_test)
        
        self.models['ClassTransformation'] = ct_model
        
        print(f"Class Transformation Qini: {qini:.4f}")
        
        return {
            'method': 'ClassTransformation',
            'qini': qini,
            'model': ct_model
        }
    
    def customer_segmentation(self, X, uplift_pred, n_segments=4):
        """
        客户分层
        """
        df = X.copy()
        df['uplift'] = uplift_pred
        
        # 四象限分群
        df['segment'] = pd.qcut(
            df['uplift'], 
            q=n_segments, 
            labels=['SleepingDogs', 'LostCauses', 'Convertibles', 'Persuadables']
        )
        
        segment_summary = df.groupby('segment').agg({
            'uplift': ['mean', 'std', 'count']
        }).round(4)
        
        return df, segment_summary
    
    def recommend_strategy(self, segments):
        """
        根据分层推荐策略
        """
        strategies = {
            'SleepingDogs': {
                'action': '⚠️ 避免触达',
                'reason': '负Uplift，触达反而降低转化',
                'priority': 0
            },
            'LostCauses': {
                'action': '❌ 不触达',
                'reason': '极低Uplift，营销资源浪费',
                'priority': 0
            },
            'Convertibles': {
                'action': '📩 减少触达',
                'reason': '自然转化，营销增量有限',
                'priority': 2
            },
            'Persuadables': {
                'action': '⭐ 优先触达',
                'reason': '高Uplift，营销增量最大',
                'priority': 5
            }
        }
        
        recommendations = segments.map(str).map(strategies)
        
        return recommendations
```

---

## 6. 最佳实践与避坑指南

### 6.1 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **Uplift预测全为正** | 模型偏差 | 检查数据质量、对照组足够大 |
| **Qini分数为负** | 随机基线更好 | 重新检查模型、数据分布 |
| **高估Uplift** | 过拟合 | 使用交叉验证、正则化 |
| **低区分度** | 特征与处置无交互 | 添加处置-特征交互项 |
| **对照组太小** | 选择偏差 | 使用倾向得分加权 |

### 6.2 数据要求

```python
def check_uplift_data_quality(X, T, Y):
    """
    检查Uplift建模数据质量
    """
    checks = {}
    
    # 1. 处理组和对照组样本量
    n_treated = (T == 1).sum()
    n_control = (T == 0).sum()
    treatment_ratio = n_treated / len(T)
    
    checks['treatment_balance'] = {
        'n_treated': n_treated,
        'n_control': n_control,
        'ratio': treatment_ratio,
        'ok': 0.2 < treatment_ratio < 0.8
    }
    
    # 2. 结果分布
    y_given_treated = Y[T == 1].mean()
    y_given_control = Y[T == 0].mean()
    
    checks['outcome_difference'] = {
        'y_treated': y_given_treated,
        'y_control': y_given_control,
        'raw_diff': y_given_treated - y_given_control
    }
    
    # 3. 倾向得分分布
    propensity_model = GradientBoostingClassifier()
    propensity_model.fit(X, T)
    propensity_scores = propensity_model.predict_proba(X)[:, 1]
    
    checks['propensity_distribution'] = {
        'mean': propensity_scores.mean(),
        'std': propensity_scores.std(),
        'min': propensity_scores.min(),
        'max': propensity_scores.max(),
        'overlap_ok': propensity_scores.min() < 0.1 and propensity_scores.max() > 0.9
    }
    
    # 4. 特征平衡
    smd_before = {}
    for col in X.columns:
        mean_t = X[T == 1][col].mean()
        mean_c = X[T == 0][col].mean()
        pooled_std = X[col].std()
        smd_before[col] = abs(mean_t - mean_c) / pooled_std
    
    checks['feature_balance'] = {
        'max_smd': max(smd_before.values()),
        'all_balanced': max(smd_before.values()) < 0.1,
        'smd': smd_before
    }
    
    return checks
```

### 6.3 超参数调优

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

def tune_uplift_model(X, T, Y, model_class, param_grid, n_splits=5):
    """
    Uplift模型超参数调优
    """
    cv_results = []
    
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    for params in ParameterGrid(param_grid):
        scores = []
        
        for train_idx, val_idx in skf.split(X, T):
            X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
            T_tr, T_val = T.iloc[train_idx], T.iloc[val_idx]
            Y_tr, Y_val = Y.iloc[train_idx], Y.iloc[val_idx]
            
            model = model_class(**params)
            model.fit(X_tr, T_tr, Y_tr)
            uplift_pred = model.predict_uplift(X_val)
            
            # 使用Qini作为评估指标
            qini = qini_score(Y_val.values, uplift_pred, T_val.values)
            scores.append(qini)
        
        cv_results.append({
            'params': params,
            'mean_qini': np.mean(scores),
            'std_qini': np.std(scores)
        })
    
    # 选择最佳参数
    best_result = max(cv_results, key=lambda x: x['mean_qini'])
    
    return best_result


# 使用示例
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1]
}

best = tune_uplift_model(
    X, T, Y,
    model_class=SLearnerUplift,
    param_grid=param_grid
)
print(f"Best params: {best['params']}")
print(f"Best Qini: {best['mean_qini']:.4f}")
```

---

## 7. 与其他专题的关联

| Uplift Modeling应用 | Wiki关联 |
|---------------------|----------|
| 营销归因 | `fintech/marketing-suite` |
| A/B测试 | `applications.md` |
| 因果森林 | `causal-discovery.md` |
| 个性化推荐 | `recommendation-systems` |
| 定价策略 | `jd-pricing-practice.md` |

---

*最后更新: 2026-04-22*
*维护者: 尼克·弗瑞*
