# 因果推断工具与实现

> 从理论到代码：常用工具、库与最佳实践

---

## 元信息

- **创建时间**: 2026-04-21
- **维护者**: 尼克·弗瑞
- **类型**: article
- **标签**: #causal-inference #tools #python #code

---

## 常用库对比

| 库 | 功能 | 适用场景 | 优势 | 劣势 |
|------|------|----------|------|------|
| **DoWhy** | 完整因果推断流程 | 大多数场景 | 文档完善、可视化好 | 速度较慢 |
| **EconML** | 异质性处理效应 | 机器学习 + 因果 | 微软维护、功能强 | 学习曲线陡 |
| **CausalML** | 因果机器学习 | 工业界大规模应用 | Uber维护、速度快 | 文档较少 |
| **CausalNex** | 贝叶斯网络 + 因果 | 结构学习 | 可解释性好 | 功能有限 |
| **dowhy-gcm** | 因果生成模型 | 反事实推理 | 生成式建模 | 较新 |

---

## DoWhy 完整流程示例

### 1. 安装与导入
```bash
pip install dowhy
```

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel
import dowhy.datasets
```

### 2. 构建模型
```python
# 加载示例数据
data = dowhy.datasets.linear_dataset(
    beta=10,  # 真实因果效应
    num_common_causes=5,  # 混杂变量数
    num_instruments=2,  # 工具变量数
    num_samples=10000,
    treatment_is_binary=True
)

# 构建因果模型
model = CausalModel(
    data=data["df"],
    treatment=data["treatment_name"],
    outcome=data["outcome_name"],
    common_causes=data["common_causes_names"],
    instruments=data["instrument_names"]
)

# 可视化因果图
model.view_model()
```

### 3. 识别因果效应
```python
# 自动识别
identified_estimand = model.identify_effect()
print(identified_estimand)
```

### 4. 估计因果效应
```python
# 方法1：倾向得分匹配
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.propensity_score_matching"
)

# 方法2：线性回归
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.linear_regression"
)

# 方法3：工具变量
estimate = model.estimate_effect(
    identified_estimand,
    method_name="iv.instrumental_variable"
)

print(f"估计的ATE: {estimate.value}")
print(f"真实的ATE: {data['ate']}")
```

### 5. 反驳验证
```python
# 反驳1：安慰剂测试
refute_placebo = model.refute_estimate(
    identified_estimand,
    estimate,
    method_name="placebo_treatment_refuter"
)
print(refute_placebo)

# 反驳2：添加随机混杂因素
refute_confounder = model.refute_estimate(
    identified_estimand,
    estimate,
    method_name="add_unobserved_common_cause"
)
print(refute_confounder)

# 反驳3：子样本测试
refute_subset = model.refute_estimate(
    identified_estimand,
    estimate,
    method_name="data_subset_refuter"
)
print(refute_subset)
```

---

## EconML 异质性处理效应示例

### 1. 安装与导入
```bash
pip install econml
```

```python
from econml.dml import LinearDML
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
```

### 2. 训练模型
```python
# 数据准备
X = data["df"][data["common_causes_names"]]  # 协变量
T = data["df"][data["treatment_name"][0]]  # 处理
Y = data["df"][data["outcome_name"]]  # 结果

# 构建DML模型
model = LinearDML(
    model_y=RandomForestRegressor(),
    model_t=RandomForestClassifier(),
    discrete_treatment=True
)

# 训练
model.fit(Y, T, X=X, W=None)

# 估计ATE
ate = model.ate(X)
print(f"ATE: {ate}")

# 估计每个个体的CATE
cate = model.effect(X)
print(f"CATE均值: {np.mean(cate)}")
```

### 3. 异质性分析
```python
# 查看哪些变量对效应影响最大
importances = model.feature_importances_
feature_names = X.columns
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance}")

# 按协变量分组查看效应
for feature in feature_names[:3]:
    print(f"\n按{feature}分组的CATE:")
    groups = pd.qcut(X[feature], 5)
    group_effects = X.groupby(groups).apply(lambda x: model.ate(x))
    print(group_effects)
```

---

## 因果森林示例 (CausalML)

### 1. 安装与导入
```bash
pip install causalml
```

```python
from causalml.inference.tree import CausalForestClassifier, CausalTreeRegressor
```

### 2. 训练模型
```python
# 构建因果森林
cf = CausalForestRegressor(
    n_estimators=100,
    max_depth=5,
    min_samples_leaf=100
)

# 训练
cf.fit(X=X, treatment=T, y=Y)

# 预测CATE
cate_cf = cf.predict(X)
```

### 3. 特征重要性
```python
# 特征重要性
importances = cf.feature_importances_
for name, importance in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
    print(f"{name}: {importance:.3f}")
```

---

## 最佳实践

### 1. 项目流程
```
1. 定义问题 → 明确什么是处理，什么是结果
2. 绘制因果图 → 领域专家参与，列出所有可能的混杂因素
3. 识别效应 → 选择合适的识别方法（后门、前门、IV等）
4. 估计效应 → 多种方法交叉验证
5. 反驳验证 → 多种反驳方法验证结果的稳健性
6. 异质性分析 → 查看不同子群体的效应差异
7. 决策支持 → 给出可落地的建议
```

### 2. 常见陷阱
| 陷阱 | 解决方案 |
|------|----------|
| 混淆路径未完全阻断 | 尽可能收集更多混杂变量，用敏感性分析评估未观察到的混杂的影响 |
| 过度匹配 | 不要匹配处理变量之后的变量 |
| 样本量不足 | 功效分析，计算需要的最小样本量 |
| 结果不可解释 | 尽量使用简单方法，复杂方法需要和简单方法对比 |

### 3. 汇报模板
```
因果分析报告
1. 研究问题
2. 因果假设与因果图
3. 识别策略
4. 数据描述
5. 估计结果（ATE + 异质性）
6. 稳健性检验（反驳结果）
7. 业务建议
```

---

*最后更新: 2026-04-21*
*维护者: 尼克·弗瑞*
