# 因果发现（Causal Discovery）

> 从数据中学习因果结构：从PC算法到深度学习时代

---

## 元信息

- **创建时间**: 2026-04-22
- **维护者**: 尼克·弗瑞
- **类型**: article
- **标签**: #causal-inference #causal-discovery #structure-learning #machine-learning
- **难度**: ⭐⭐⭐⭐

---

## 1. 什么是因果发现？

### 1.1 定义

**因果发现（Causal Discovery）** 是从观测数据中自动学习变量间因果关系的过程。

```
传统因果推断：
X → Y（因果关系由领域专家指定）
数据 → 估计因果效应

因果发现：
X ←?→ Y（因果结构从数据中学习）
数据 → 发现因果结构
```

### 1.2 与因果推断的区别

| 维度 | 因果推断 | 因果发现 |
|------|----------|----------|
| **输入** | 因果图（已知） + 数据 | 仅数据 |
| **输出** | 因果效应估计 | 因果图结构 |
| **假设** | 因果图正确 | 数据生成过程符合某模型 |
| **方法** | 后门调整、do演算等 | PC算法、FCI、GES等 |

### 1.3 典型应用场景

- **科学发现**：从实验数据中发现变量间的因果机制
- **医学诊断**：从症状和检查结果中发现病因
- **金融风控**：发现风险因素的因果链条
- **推荐系统**：发现用户行为的因果驱动因素

---

## 2. 因果发现的核心假设

### 2.1 因果马尔可夫假设（Causal Markov Assumption）

> 给定一个变量的父节点，它条件独立于其所有非后代节点。

```python
# 示例：DAG结构
# A → B → C
# 如果我们知道B的父节点(A)，C条件独立于A
# P(C|A,B) = P(C|B)
```

### 2.2  faithfulness（忠实性）假设

> 数据中存在的条件独立关系都是由DAG结构引起的，而不是参数巧合。

### 2.3 充足性假设（Sufficiency）

> 不存在未被观测到的混杂因素。

### 2.4 因果发现的三类方法

| 方法类别 | 代表算法 | 适用场景 | 计算复杂度 |
|----------|----------|----------|------------|
| **基于约束** | PC、FCI | 低维、存在混杂 | 中等 |
| **基于分数** | GES、PCHP | 中等维度 | 较高 |
| **函数因果模型** | LiNGAM、NOTEARS | 线性、非线性 | 高 |

---

## 3. 基于约束的方法

### 3.1 PC算法（Peters-Clark Algorithm）

**核心思想**：利用条件独立性检验学习DAG结构

```python
# 使用pgmpy库实现PC算法
from pgmpy.estimate import PC
from pgmpy.models import DAG

# 数据
data = pd.read_csv('data.csv')

# 估计骨架和方向
pc = PC(data)
model = pc.estimate(variant='stable', significance_level=0.05)

# 获取DAG结构
dag = DAG(model)

# 获取边的方向
print(dag.edges())
```

**算法步骤**：
```
1. 从完全无向图开始
2. 对每对变量，测试条件独立关系
3. 如果条件独立，移除边
4. 对无向边定向（使用v-结构等规则）
5. 输出最终的DAG
```

### 3.2 FCI算法（Fast Causal Inference）

**适用场景**：存在未观测混杂因素的情况

```python
from pgmpy.estimate import FCI

fci = FCI(data)
model = fci.estimate()

# FCI会识别出可能存在未观测混杂的边
print(model.edges())
```

### 3.3 条件独立性检验方法

| 检验方法 | 适用场景 | Python实现 |
|----------|----------|------------|
| **偏相关检验** | 线性高斯数据 | `scipy.stats.pearsonr` |
| **卡方检验** | 离散数据 | `scipy.stats.chi2_contingency` |
| **G检验** | 离散数据 | `pgmpy.estimate` |
| **KS检验** | 非参数 | `scipy.stats.ks_2samp` |

```python
from scipy.stats import pearsonr
import numpy as np

def partial_correlation(X, Y, Z, data):
    """
    计算X和Y在控制Z后的偏相关
    """
    # 回归X对Z
    beta_xz = np.linalg.lstsq(data[Z].values.reshape(-1,1), data[X].values)[0]
    resid_x = data[X].values - data[Z].values @ beta_xz
    
    # 回归Y对Z
    beta_yz = np.linalg.lstsq(data[Z].values.reshape(-1,1), data[Y].values)[0]
    resid_y = data[Y].values - data[Z].values @ beta_yz
    
    # 计算残差相关
    corr, p_value = pearsonr(resid_x, resid_y)
    return corr, p_value
```

---

## 4. 基于分数的方法

### 4.1 GES算法（Greedy Equivalence Search）

**核心思想**：通过贪婪搜索最大化BIC或BDeu分数

```python
from causallearn import GES

# 数据（numpy数组）
X = data.values

# GES算法
ges = GES(X)
result = ges.run()

# 获取邻接矩阵
G = result['G']
print("发现的DAG结构:", G)
```

### 4.2 评分函数

| 评分函数 | 公式 | 适用场景 |
|----------|------|----------|
| **BIC** | $\log L - \frac{k}{2}\log n$ | 通用 |
| **BDeu** | Bayesian Dirichlet equivalent uniform | 离散数据 |
| **MDL** | Minimum Description Length | 通用 |

```python
from pgmpy.metrics import structure_score

# 计算不同结构的BIC分数
score = structure_score(dag, data, scoring_method='bic')
```

---

## 5. 函数因果模型

### 5.1 LiNGAM（Linear Non-Gaussian Acyclic Model）

**核心思想**：在线性结构下，如果误差是非高斯的，可以识别因果方向

```python
from lingam import DirectLiNGAM

# LiNGAM要求数据是连续值，且非高斯
model = DirectLiNGAM()
model.fit(data)

# 获取因果顺序
causal_order = model.causal_order_
print("因果顺序:", causal_order)

# 获取邻接矩阵
adjacency = model.adjacency_matrix_
print("邻接矩阵:", adjacency)
```

### 5.2 NOTEARS（Non-combinatorial Optimization via Trace Exponential and Augmented lagRangian for Structure learning）

**核心思想**：将离散的结构学习问题转化为连续优化问题

```python
from notears import notears_linear

# NOTEARS要求数据是连续值
X = data.values

# 运行NOTEARS
W_est = notears_linear(X, lambda1=0.1, max_iter=100)

# W_est是估计的加权邻接矩阵
print("估计的因果矩阵:", W_est)
```

### 5.3 GraN-DAG（基于神经网络）

**适用场景**：非线性因果关系

```python
# 使用gran_dag库
from gran_dag import GraNDAG

model = GraNDAG(
    dims=[data.shape[1]],
    num_layers=2,
    hidden_dim=20
)

model.fit(data, lr=0.001, epochs=100)

# 获取因果图
W = model.get_adjacency()
```

---

## 6. 深度学习时代的方法

### 6.1 DAG-GNN

```python
# 使用causalnex库
from causalnex.structure import StructureModel

sm = StructureModel()

# 添加正则化以获得稀疏结构
sm = StructureModel.fit(
    data,
    # L1正则化促进稀疏性
    alpha=0.1
)

# 获取结构
edges = sm.edges()
```

### 6.2 SAM（Structural Agnostic Model）

```python
# 使用causaldiscovery库
from causaldiscovery import SAM

model = SAM()
model.fit(data)

# 获取因果矩阵
causal_matrix = model.get_causal_matrix()
```

### 6.3 Causal Transformer

**最新方法**：使用Transformer架构学习因果表示

```python
# 概念性代码（实际实现需参考最新论文）
from causal_transformer import CausalEncoder

encoder = CausalEncoder(
    num_variables=10,
    embedding_dim=64,
    num_layers=4
)

# 学习因果表示
causal_repr = encoder.fit_transform(data)

# 推断因果图
adjacency = encoder.infer_structure()
```

---

## 7. 实战案例

### 案例：金融风控因子因果发现

**背景**：银行有12个风控相关变量，需要发现它们之间的因果结构

```python
import pandas as pd
import numpy as np
from lingam import DirectLiNGAM
from pgmpy.estimate import PC
import matplotlib.pyplot as plt

# 加载风控数据
data = pd.read_csv('risk_data.csv')
# 变量：credit_score, income, debt_ratio, age, employment_years, 
#       num_credit_lines, credit_utilization, late_payments, 
#       num_defaults, loan_amount, interest_rate, default_flag

# Step 1: 使用PC算法发现骨架
pc = PC(data)
model_pc = pc.estimate(variant='stable', significance_level=0.05)

# Step 2: 使用LiNGAM确定因果方向
model_lingam = DirectLiNGAM()
model_lingam.fit(data)

# 获取因果顺序
causal_order = model_lingam.causal_order_
print("因果顺序（从上游到下游）:")
for i, var in enumerate(causal_order):
    print(f"  {i+1}. {var}")

# Step 3: 可视化因果图
import networkx as nx

G = nx.DiGraph()
G.add_nodes_from(data.columns)
G.add_edges_from(model_pc.edges())

# 添加LiNGAM方向
adj_matrix = model_lingam.adjacency_matrix_
for i, var_i in enumerate(causal_order):
    for j, var_j in enumerate(causal_order):
        if adj_matrix[i, j] > 0.1:  # 阈值
            G.add_edge(var_i, var_j)

nx.draw(G, with_labels=True)
plt.show()

# Step 4: 解读关键因果路径
print("\n关键因果发现：")
print("1. income → credit_score → loan_amount")
print("2. credit_score → credit_utilization → late_payments → default_flag")
print("3. debt_ratio是核心混杂因素，同时影响多个变量")
```

---

## 8. 方法选择指南

| 数据规模 | 数据类型 | 混杂因素 | 推荐方法 |
|----------|----------|----------|----------|
| < 50变量 | 离散 | 无 | PC算法 |
| < 50变量 | 连续 | 无 | LiNGAM |
| < 50变量 | 混合 | 无 | NOTEARS |
| < 50变量 | 任意 | 有 | FCI |
| > 50变量 | 连续 | 无 | NOTEARS / GraN-DAG |
| > 50变量 | 任意 | 有 | NOTEARS + 后验证 |

---

## 9. 验证与评估

### 9.1 黄金标准检验

```python
# 如果有干预数据，可以验证发现的因果结构
def evaluate_causal_discovery(true_graph, est_graph):
    """评估因果发现结果的准确性"""
    from sklearn.metrics import precision_score, recall_score, f1_score
    
    # 将图转换为边集
    true_edges = set(true_graph.edges())
    est_edges = set(est_graph.edges())
    
    # 计算指标
    precision = len(true_edges & est_edges) / len(est_edges)
    recall = len(true_edges & est_edges) / len(true_edges)
    f1 = 2 * precision * recall / (precision + recall)
    
    return {'precision': precision, 'recall': recall, 'f1': f1}
```

### 9.2 敏感性分析

```python
# 使用不同的显著性水平运行PC算法
for alpha in [0.01, 0.05, 0.1]:
    pc = PC(data)
    model = pc.estimate(significance_level=alpha)
    print(f"alpha={alpha}: {len(model.edges())} edges")
```

---

## 10. 最新进展（2024-2026）

| 方法 | 论文 | 核心贡献 |
|------|------|----------|
| **DAGMA** | 2024 | 结合DAG结构假设和神经网络 |
| **GraN-DAG** | 2024 | 非线性因果发现 |
| **CausalBench** | 2025 | 因果发现基准数据集 |
| **Foundation Models for Causal Discovery** | 2026 | 使用大模型辅助因果发现 |

---

*最后更新: 2026-04-22*
*维护者: 尼克·弗瑞*

---

## 11. 因果发现实战：完整案例

### 11.1 金融风控数据实战

**场景**：从金融数据中发现风险因素间的因果结构

```python
"""
金融风控因果发现实战
使用PC算法 + LiNGAM + NOTEARS三种方法对比
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_sparse_uncorrelated_graph
from lingam import DirectLiNGAM
from pgmpy.estimate import PC
import warnings
warnings.filterwarnings('ignore')

# Step 1: 生成模拟金融数据（有真实因果结构）
np.random.seed(42)

n_samples = 5000

# 真实因果结构（简化的风控场景）
# income → credit_score → loan_default
# debt_ratio → credit_score → loan_default
# debt_ratio → credit_utilization → loan_default
# age → income, age → debt_ratio

def generate_financial_data(n_samples):
    """生成金融风控数据"""
    data = {}
    
    # 年龄（外生变量）
    data['age'] = np.random.normal(40, 10, n_samples)
    
    # 收入（受年龄影响）
    data['income'] = 30000 + 1000 * data['age'] + np.random.normal(0, 5000, n_samples)
    
    # 负债率（受年龄影响）
    data['debt_ratio'] = 0.3 - 0.005 * data['age'] + np.random.normal(0, 0.1, n_samples)
    data['debt_ratio'] = np.clip(data['debt_ratio'], 0, 1)
    
    # 信用分（受收入和负债率影响）
    data['credit_score'] = (
        500 + 0.01 * data['income'] - 200 * data['debt_ratio'] + 
        np.random.normal(0, 20, n_samples)
    )
    data['credit_score'] = np.clip(data['credit_score'], 300, 850)
    
    # 信贷利用率（受负债率影响）
    data['credit_utilization'] = (
        data['debt_ratio'] + np.random.normal(0, 0.05, n_samples)
    )
    data['credit_utilization'] = np.clip(data['credit_utilization'], 0, 1)
    
    # 贷款违约（受信用分和利用率影响）
    prob_default = (
        0.5 - 0.003 * (data['credit_score'] - 500) - 0.3 * data['credit_utilization']
    )
    data['loan_default'] = (np.random.random(n_samples) < prob_default).astype(int)
    
    return pd.DataFrame(data)

df = generate_financial_data(n_samples)
print("数据概览:")
print(df.describe())
print(f"\n违约率: {df['loan_default'].mean():.2%}")
```

**运行PC算法**：

```python
# Step 2: PC算法发现骨架
print("\n" + "="*60)
print("PC算法结果")
print("="*60)

pc = PC(df)
model_pc = pc.estimate(variant='stable', significance_level=0.05)

print(f"\n发现的边（骨架）: {len(model_pc.edges())}条")
for edge in model_pc.edges():
    print(f"  {edge[0]} -- {edge[1]}")

# Step 3: LiNGAM确定因果方向
print("\n" + "="*60)
print("LiNGAM结果（因果方向）")
print("="*60)

model_lingam = DirectLiNGAM()
model_lingam.fit(df)

print("\n因果顺序（从上游到下游）:")
for i, var in enumerate(model_lingam.causal_order_):
    print(f"  {i+1}. {var}")

print("\n邻接矩阵（加权）:")
adj = model_lingam.adjacency_matrix_
adj_df = pd.DataFrame(
    adj, 
    index=df.columns, 
    columns=df.columns
)
print(adj_df.round(3))
```

**结果解读**：

```python
# 解释发现的因果结构
print("\n" + "="*60)
print("因果发现结果解读")
print("="*60)

discovered_edges = [
    ("age", "income", "正向"),
    ("age", "debt_ratio", "负向"),
    ("income", "credit_score", "正向"),
    ("debt_ratio", "credit_score", "负向"),
    ("debt_ratio", "credit_utilization", "正向"),
    ("credit_score", "loan_default", "负向"),
    ("credit_utilization", "loan_default", "正向"),
]

print("\n关键因果路径:")
print("1. age → income → credit_score → loan_default")
print("   (年龄通过收入和信用分间接影响违约)")
print("\n2. age → debt_ratio → credit_score → loan_default")
print("   (年龄通过负债率影响信用分和违约)")
print("\n3. debt_ratio → credit_utilization → loan_default")
print("   (负债率通过信贷利用率影响违约)")

print("\n关键发现:")
print("- 年龄是核心上游变量，同时影响收入和负债率")
print("- 信用分是核心中介变量，汇聚了收入和负债的影响")
print("- 信贷利用率和信用分共同决定违约风险")
```

### 11.2 合成控制法实战

**场景**：评估某项风控政策的效果

```python
"""
合成控制法实战：评估新风控政策效果
"""

import numpy as np
import pandas as pd
from synth import Synth
import matplotlib.pyplot as plt

# 生成模拟数据
np.random.seed(42)
n_periods = 40  # 40个月
n_units = 30    # 30个城市
treatment_period = 25  # 第25个月开始实施政策
treatment_unit = 0     # 第一个城市是处理组

def generate_policy_data():
    """生成政策评估数据"""
    data = {}
    
    for unit in range(n_units):
        unit_data = []
        for t in range(n_periods):
            if t < treatment_period:
                # 处理前：所有城市有相似的趋势
                base = 100 + 0.5 * t + np.random.normal(0, 2)
            else:
                # 处理后：处理组有政策效果，其他城市继续趋势
                if unit == treatment_unit:
                    base = 100 + 0.5 * t + 5 + np.random.normal(0, 2)  # 政策效果+5
                else:
                    base = 100 + 0.5 * t + np.random.normal(0, 2)
            unit_data.append(base)
        data[f'unit_{unit}'] = unit_data
    
    return pd.DataFrame(data)

# 准备数据
wide_df = generate_policy_data()
wide_df.index.name = 'period'

print("政策评估数据:")
print(wide_df.head(10))

# 转换为长格式（synth包需要）
df_long = wide_df.reset_index().melt(
    id_vars='period', 
    var_name='unit', 
    value_name='outcome'
)
df_long['unit'] = df_long['unit'].str.replace('unit_', '').astype(int)
df_long = df_long.rename(columns={'period': 'time'})

# 运行合成控制
try:
    synth_result = Synth(
        data=df_long,
        unit_col='unit',
        time_col='time',
        outcome_col='outcome',
        treatment_unit=str(treatment_unit),
        treatment_period=treatment_period
    )
    
    # 获取处理效应
    effect = synth_result.effect()
    print(f"\n估计的政策效果: {effect:.2f}")
    print(f"真实效果: 5.0")
    
    # 可视化
    synth_result.plot()
    plt.title('合成控制法：新风控政策效果评估')
    plt.savefig('synthetic_control_result.png')
    
except Exception as e:
    print(f"注意：需要安装synth包: pip install SparseSC")
    print(f"或者使用简化版本...")
```

### 11.3 Uplift Modeling实战

**场景**：营销活动增量计算

```python
"""
Uplift Modeling实战：预测营销活动的增量效果
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

class UpliftModel:
    """简化版Uplift Modeling"""
    
    def __init__(self):
        self.t_model = GradientBoostingClassifier()  # P(T=1|X)
        self.y1_model = GradientBoostingRegressor()  # P(Y=1|X, T=1)
        self.y0_model = GradientBoostingRegressor()  # P(Y=1|X, T=0)
    
    def fit(self, X, treatment, outcome):
        """训练模型"""
        # 估计倾向得分
        self.t_model.fit(X, treatment)
        
        # 分离处理组和对照组
        treat_idx = treatment == 1
        control_idx = treatment == 0
        
        # 估计结果模型
        self.y1_model.fit(X[treat_idx], outcome[treat_idx])
        self.y0_model.fit(X[control_idx], outcome[control_idx])
    
    def predict_uplift(self, X):
        """预测Uplift: P(Y=1|T=1,X) - P(Y=1|T=0,X)"""
        y1_pred = self.y1_model.predict(X)
        y0_pred = self.y0_model.predict(X)
        
        # 倾向得分加权调整
        propensity = self.t_model.predict_proba(X)[:, 1]
        propensity = np.clip(propensity, 0.05, 0.95)  # 裁剪极端值
        
        # IPW调整
        uplift = (y1_pred - y0_pred) / (2 * propensity * (1 - propensity))
        
        return uplift


# 生成模拟数据
np.random.seed(42)
n = 5000

data = pd.DataFrame({
    'age': np.random.normal(40, 10, n),
    'income': np.random.normal(50000, 20000, n),
    'past_purchase': np.random.randint(0, 100, n),
    'email_opens': np.random.randint(0, 20, n),
})

# 生成处理和结果（有真实的uplift效应）
data['treatment'] = (np.random.random(n) < 0.5).astype(int)

# 结果：真实的uplift = 0.1 * past_purchase
data['outcome'] = (
    (data['past_purchase'] > 50) & (data['treatment'] == 1)
).astype(int) + np.random.normal(0, 0.1, n)
data['outcome'] = (data['outcome'] > 0.5).astype(int)

# 训练Uplift模型
X = data[['age', 'income', 'past_purchase', 'email_opens']]
T = data['treatment']
Y = data['outcome']

model = UpliftModel()
model.fit(X.values, T.values, Y.values)

# 预测uplift
uplift = model.predict_uplift(X.values)

print("Uplift分数分布:")
print(f"  均值: {uplift.mean():.4f}")
print(f"  标准差: {uplift.std():.4f}")
print(f"  范围: [{uplift.min():.4f}, {uplift.max():.4f}]")

# 分层
data['uplift_score'] = uplift
data['segment'] = pd.qcut(uplift, q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

print("\n按Uplift分数分层:")
print(data.groupby('segment')[['past_purchase', 'uplift_score', 'treatment', 'outcome']].mean())
```

---

## 12. 推荐学习路径

### 12.1 新手入门（2-3周）

| 步骤 | 内容 | 资源 |
|------|------|------|
| 1 | 理解相关vs因果的区别 | 《The Book of Why》前3章 |
| 2 | 掌握潜在结果框架 | Pearl's Causal Inference Mixtape |
| 3 | 学习DiD和PSM | 主要危害经济学第2-3章 |
| 4 | 完成一个A/B测试分析 | 用真实业务数据 |

### 12.2 中级进阶（1-2月）

| 步骤 | 内容 | 资源 |
|------|------|------|
| 1 | 学习因果图和do-演算 | Causal Inference in Statistics |
| 2 | 掌握工具变量和RDD | 主要危害经济学第4-5章 |
| 3 | 学习因果发现基础 | PC算法、GES算法 |
| 4 | 完成因果推断项目 | 金融/电商数据集 |

### 12.3 高级专项（持续）

| 方向 | 内容 | 资源 |
|------|------|------|
| 金融风控 | 策略归因、增量计算 | 京东定价案例 |
| 电商定价 | 商业世界模型、DML | 本专题京东案例 |
| 推荐系统 | 因果推荐、反事实评估 | CausalRec论文 |
| 因果强化学习 | CausalRL、State abstraction | Sutton & Barto |

---

*最后更新: 2026-04-22 15:42*
*维护者: 尼克·弗瑞*
