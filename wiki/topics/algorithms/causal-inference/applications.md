# 因果推断应用案例：金融风控与营销

> 从理论到实践：因果推断在金融科技中的落地应用

---

## 元信息

- **创建时间**: 2026-04-20
- **维护者**: 尼克·弗瑞
- **关联专题**: `fintech/risk-management`, `fintech/marketing-suite`
- **标签**: #causal-inference #fintech #risk-management #marketing

---

## 为什么金融科技需要因果推断？

### 传统分析的陷阱

```
场景：风控策略优化
─────────────────────────────────────────
观察数据：
- 策略A组逾期率：5%
- 策略B组逾期率：3%

❌ 错误结论：策略B更好，全面推广

⚠️ 问题：
- 策略A/B的客群是否可比？
- 策略B是否只覆盖了低风险客群？
- 时间趋势是否影响了结果？

✅ 因果推断回答：
"在**相同客群**条件下，策略B相比策略A
对逾期率的**因果效应**是多少？"
─────────────────────────────────────────
```

### 金融科技的核心因果问题

| 业务场景 | 相关性问题 | 因果问题 | 方法 |
|---------|-----------|---------|------|
| **风控策略** | "策略B组逾期率更低" | "策略B**导致**逾期率降低了多少？" | DiD / PSM |
| **营销归因** | "收到优惠券的用户GMV更高" | "优惠券**带来**了多少增量GMV？" | IV / Uplift |
| **额度管理** | "提额用户借款增加" | "提额**导致**了借款增加？" | RDD |
| **产品功能** | "用新功能的用户留存高" | "新功能对留存的**净效应**？" | 工具变量 |
| **渠道效果** | "App用户比H5用户质量高" | "App使用**导致**质量提升？" | 工具变量 |

---

## 案例1：风控策略效果评估 (DiD方法)

### 场景

新风控策略在某省试点，评估其对逾期率的**因果效应**。

### 识别策略：双重差分 (Difference-in-Differences)

```python
# DiD核心思想：
# 效应 = (处理组后 - 处理组前) - (对照组后 - 对照组前)
#        = 处理组变化 - 对照组变化 (趋势)
#        = 剔除共同趋势后的净效应

# 数据准备
import pandas as pd
import statsmodels.formula.api as smf

# 数据格式：
# province | month | treated | post | default_rate
# 省        | 月份  | 是否试点 | 试点后 | 逾期率

df = pd.read_csv('pilot_data.csv')

# DiD回归
model = smf.ols(
    'default_rate ~ treated * post + C(month) + C(province)',
    data=df
).fit()

print(model.summary())

# 关键系数: treated:post 交互项
# 含义：策略对逾期率的因果效应
```

### 关键假设与检验

```
平行趋势假设 (关键!)
─────────────────────────────
假设：如果没有试点，处理组和对照组的趋势应该平行

检验方法：
1. 事件研究法 (Event Study)
   - 试点前各期虚拟变量回归
   - 系数应不显著 (平行趋势成立)

2. 可视化
   - 试点前处理组vs对照组趋势图
   - 应大致平行

图示：
逾期率
  │    处理组 ─────────────╲
  │                       ╲____  ← 策略效应
  │    对照组 ───────────────────
  │          ↑
  └──────────┼──────────────────→ 时间
            试点启动

如果试点前趋势不平行 → 考虑:
- 更换对照组 (PSM匹配)
- 加入协变量控制
- 换用其他方法 (如Synthetic Control)
─────────────────────────────
```

### 实践要点

| 要点 | 说明 |
|------|------|
| **对照组选择** | 与处理组相似但未实施策略的地区/客群 |
| **时间窗口** | 试点前后足够长，但避免太久引入其他干扰 |
| **稳健性检验** | 换对照组、换时间窗口、安慰剂检验 |
| **效应分解** | 异质性分析(客群、时段)、机制分析 |

---

## 案例2：营销增量效果评估 (Uplift/IV方法)

### 场景

评估短信优惠券的**增量GMV**（即：因为收到短信而产生的GMV，而非用户本来就会产生的）。

### 挑战

```
观察数据：
- 收到短信组平均GMV：¥500
- 未收到短信组平均GMV：¥300

❌ 错误结论：短信带来了 ¥200 增量

⚠️ 问题：
- 收到短信的用户可能本身就是高价值用户
- 这部分用户即使不发短信，GMV也会更高
- ¥200 的差距包含选择偏差

✅ 需要回答：
"对于同一个用户，发vs不发短信，
GMV的因果效应是多少？"
```

### 识别策略1：随机对照实验 (RCT) - 黄金标准

```python
# 理想情况下：随机分配处理
# 随机化消除了选择偏差

import numpy as np
from scipy import stats

# 数据
np.random.seed(42)
# 随机分配：50%收到短信，50%不收到
n = 10000
received_sms = np.random.binomial(1, 0.5, n)

# 潜在结果模型
# Y(1): 收到短信的GMV, Y(0): 未收到的GMV
# 假设真实效应是 +50
Y0 = np.random.normal(300, 50, n)  # 基准GMV
Y1 = Y0 + 50 + np.random.normal(0, 20, n)  # 真实效应 +50

# 观察到的结果
observed_gmv = received_sms * Y1 + (1 - received_sms) * Y0

# 因果效应估计 (RCT下直接比较即可)
ate_estimate = np.mean(observed_gmv[received_sms==1]) - \
               np.mean(observed_gmv[received_sms==0])

print(f"估计的ATE: {ate_estimate:.2f}")
print(f"真实的ATE: 50.00")
# 结果应该接近 50

# 显著性检验
t_stat, p_value = stats.ttest_ind(
    observed_gmv[received_sms==1],
    observed_gmv[received_sms==0]
)
print(f"t-statistic: {t_stat:.2f}, p-value: {p_value:.4f}")
```

### 识别策略2：工具变量 (IV) - 当无法随机化时

```python
# 场景：短信发送依赖用户手机号是否有效
# 工具变量："运营商短信网关是否畅通" (随机冲击)
#   - 影响短信送达 (相关性)
#   - 不直接影响GMV (排他性)

import numpy as np
from linearmodels.iv import IV2SLS
import pandas as pd

np.random.seed(42)
n = 5000

# 工具变量: 网关畅通 (随机)
gateway_open = np.random.binomial(1, 0.7, n)

# 第一阶段：网关 -> 短信送达
# 只有网关畅通时才能收到短信
sms_received = gateway_open * np.random.binomial(1, 0.8, n)

# 结果(GMV)：受短信影响 + 其他因素
# 真实效应: 收到短信 +100 GMV
base_gmv = np.random.normal(200, 30, n)
true_effect = 100
# 观察到的GMV
# 潜在结果: Y(1) = base + 100, Y(0) = base
observed_gmv = base_gmv + sms_received * true_effect + np.random.normal(0, 20, n)

# 数据结构
df = pd.DataFrame({
    'gmv': observed_gmv,
    'sms': sms_received,
    'gateway': gateway_open
})

print("===  naive估计 (有偏) ===")
naive_ate = df[df['sms']==1]['gmv'].mean() - df[df['sms']==0]['gmv'].mean()
print(f"直接比较 (sms=1 vs sms=0): {naive_ate:.2f}")
print(f"真实效应: {true_effect}")
print(f"偏差: {naive_ate - true_effect:.2f} (选择偏差)")

print("\n===  IV估计 (工具变量) ===")
# 2SLS估计
# 第一阶段: sms ~ gateway
# 第二阶段: gmv ~ fitted_sms

# 手动2SLS演示
from sklearn.linear_model import LinearRegression

# 第一阶段
stage1 = LinearRegression()
stage1.fit(df[['gateway']], df['sms'])
sms_fitted = stage1.predict(df[['gateway']])

# 第二阶段
stage2 = LinearRegression()
stage2.fit(sms_fitted.reshape(-1, 1), df['gmv'])
iv_estimate = stage2.coef_[0]

print(f"IV估计 (2SLS): {iv_estimate:.2f}")
print(f"与真实效应的误差: {abs(iv_estimate - true_effect):.2f}")
print("\nIV消除了选择偏差，估计接近真实效应！")

# 第一阶段F统计量 (检验工具变量强度)
import statsmodels.api as sm
X = sm.add_constant(df['gateway'])
model_1st = sm.OLS(df['sms'], X).fit()
print(f"\n第一阶段F统计量: {model_1st.fvalue:.2f}")
print("(F>10表示工具变量足够强)")
```

### 识别策略3：Uplift Modeling (营销增量建模)

```python
# Uplift建模：预测"处理效应"本身
# 目标：识别"Persuadables" (只有收到营销才会转化的人群)

# 四类人群 (根据处理效应分类)：
# 1. Sure Things: 无论如何都会转化 (Y(1)=1, Y(0)=1) - 不需要营销
# 2. Lost Causes: 无论如何都不会转化 (Y(1)=0, Y(0)=0) - 不需要营销
# 3. Persuadables: 只有收到营销才会转化 (Y(1)=1, Y(0)=0) - 重点营销对象！
# 4. Sleeping Dogs: 收到营销反而不转化 (Y(1)=0, Y(0)=1) - 要避免营销

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

np.random.seed(42)

# 生成模拟数据
n = 10000

# 用户特征
age = np.random.normal(35, 10, n)
income = np.random.normal(50000, 15000, n)
engagement_score = np.random.beta(2, 5, n)  # 活跃度

# 真实处理效应 (不可观测，仅用于模拟)
# 假设高engagement用户对营销更敏感
true_uplift = 0.05 + 0.2 * engagement_score - 0.001 * (age - 35)

# 随机分配处理 (是否收到营销)
treatment = np.random.binomial(1, 0.5, n)

# 基础转化率 (与处理无关)
base_conversion = 0.1 + 0.001 * (income - 50000) / 10000

# 观察到的转化率 = 基础转化率 + 处理效应(仅当treatment=1)
conversion = base_conversion + treatment * true_uplift + np.random.normal(0, 0.02, n)
conversion = np.clip(conversion, 0, 1)

# 二值化结果
converted = (conversion > np.random.uniform(0, 1, n)).astype(int)

# 创建数据框
df = pd.DataFrame({
    'age': age,
    'income': income,
    'engagement_score': engagement_score,
    'treatment': treatment,
    'converted': converted
})

print("=== 数据概览 ===")
print(f"总样本: {len(df)}")
print(f"处理组: {df['treatment'].sum()}")
print(f"对照组: {len(df) - df['treatment'].sum()}")
print(f"\n整体转化率:")
print(f"  处理组: {df[df['treatment']==1]['converted'].mean():.3f}")
print(f"  对照组: {df[df['treatment']==0]['converted'].mean():.3f}")
print(f"  平均处理效应(ATE): {df[df['treatment']==1]['converted'].mean() - df[df['treatment']==0]['converted'].mean():.3f}")

# ======================================
# Uplift Modeling 方法1: Two-Model Approach
# ======================================
print("\n\n=== Uplift Modeling: Two-Model Approach ===")

from sklearn.ensemble import GradientBoostingClassifier

# 分割数据
train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

features = ['age', 'income', 'engagement_score']

# 模型1: 处理组 (treatment=1)
model_treat = GradientBoostingClassifier(n_estimators=100, random_state=42)
model_treat.fit(train_df[train_df['treatment']==1][features],
                train_df[train_df['treatment']==1]['converted'])

# 模型2: 对照组 (treatment=0)
model_control = GradientBoostingClassifier(n_estimators=100, random_state=42)
model_control.fit(train_df[train_df['treatment']==0][features],
                  train_df[train_df['treatment']==0]['converted'])

# 预测Uplift
test_df = test_df.copy()
test_df['pred_treat'] = model_treat.predict_proba(test_df[features])[:, 1]
test_df['pred_control'] = model_control.predict_proba(test_df[features])[:, 1]
test_df['uplift_score'] = test_df['pred_treat'] - test_df['pred_control']

print("Uplift Score分布:")
print(test_df['uplift_score'].describe())

# ======================================
# Uplift模型评估: Qini Curve
# ======================================
print("\n\n=== Uplift Model Evaluation ===")

def compute_qini_curve(df, uplift_col='uplift_score', treatment_col='treatment', outcome_col='converted'):
    """计算Qini Curve"""
    # 按uplift排序
    df_sorted = df.sort_values(uplift_col, ascending=False).reset_index(drop=True)
    n = len(df_sorted)

    # 计算累积指标
    results = []
    for i in range(1, n+1, max(1, n//100)):  # 采样100个点
        subset = df_sorted.iloc[:i]

        # 实际处理组的转化数
        treated = subset[subset[treatment_col]==1]
        y_t = treated[outcome_col].sum() if len(treated) > 0 else 0
        n_t = len(treated)

        # 实际对照组的转化数
        control = subset[subset[treatment_col]==0]
        y_c = control[outcome_col].sum() if len(control) > 0 else 0
        n_c = len(control)

        # 累积Qini值
        if n_t > 0 and n_c > 0:
            qini = y_t - (n_t / n_c) * y_c
        else:
            qini = 0

        results.append({
            'n': i,
            'pct': i/n,
            'qini': qini
        })

    return pd.DataFrame(results)

# 计算Qini Curve
qini_df = compute_qini_curve(test_df)

# 计算Qini系数 (类似AUC)
qini_auc = np.trapz(qini_df['qini'], qini_df['pct'])
print(f"Qini AUC: {qini_auc:.2f}")

# 与随机策略对比
random_qini = []
for _ in range(10):
    test_df_random = test_df.sample(frac=1).reset_index(drop=True)
    qini_random = compute_qini_curve(test_df_random)
    random_qini.append(np.trapz(qini_random['qini'], qini_random['pct']))

print(f"随机策略Qini AUC (平均): {np.mean(random_qini):.2f}")
print(f"Uplift模型提升: {(qini_auc / np.mean(random_qini) - 1) * 100:.1f}%")

# ======================================
# 业务应用：四类人群划分
# ======================================
print("\n\n=== 业务应用：四类人群划分 ===")

def classify_users(uplift_score, threshold=0.01):
    """基于uplift score划分用户类型"""
    if uplift_score > threshold:
        return 'Persuadable'  # 说服型：营销活动有效
    elif uplift_score < -threshold:
        return 'Sleeping Dog'  # 沉睡狗：营销反而有害
    else:
        # 需要进一步判断是Sure Thing还是Lost Cause
        # 这里简化处理，实际可以用模型预测的基础转化率
        return 'Sure Thing/Lost Cause'

test_df['user_type'] = test_df['uplift_score'].apply(classify_users)

print("用户类型分布:")
print(test_df['user_type'].value_counts())

print("\n各类型营销效果 (观察到的实际转化率):")
for user_type in test_df['user_type'].unique():
    subset = test_df[test_df['user_type'] == user_type]
    treat_conv = subset[subset['treatment']==1]['converted'].mean()
    control_conv = subset[subset['treatment']==0]['converted'].mean()
    actual_effect = treat_conv - control_conv
    print(f"{user_type:20s}: 处理组={treat_conv:.3f}, 对照组={control_conv:.3f}, 效应={actual_effect:+.3f}")

print("\n营销策略建议:")
print("- Persuadables: 优先营销，预期正向ROI")
print("- Sleeping Dogs: 避免营销，防止负向效应")
print("- Sure Things: 无需营销，自然转化")
print("- Lost Causes: 节省成本，放弃营销")

# ======================================
# 总结
# ======================================
print("\n\n" + "="*60)
print("因果推断在营销中的应用总结")
print("="*60)
print("""
核心问题：营销活动带来的增量效果（而非总体转化率）

方法选择：
1. 理想情况：随机对照实验 (RCT) - 黄金标准
2. 观察性数据：
   - Uplift Modeling: 预测个体处理效应
   - IV/PSM/DiD: 解决选择偏差

业务价值：
1. 量化真实增量ROI
2. 识别高响应人群 (Persuadables)
3. 避免对负向响应人群的过度营销
4. 优化营销预算分配

关键洞察：
- 平均处理效应(ATE) 不等于 个体处理效应(ITE)
- 人群异质性：不同用户对营销响应不同
- 因果推断帮助找到"对的人会"
""")

---

## 案例3：商业世界模型 — 京东定价场景的因果推断实践

> 来源：Get笔记 - AI电商与商业世界模型分享 (2026-04-18)

### 场景背景

京东自营万亿GMV，大量商品需要定价调整：
- 电商价格竞争激烈，要求精细化快速响应市场变化
- 定价需要兼顾销售目标与供应链库存调节
  - 积压库存需要降价快速去化
  - 缺货商品需要维持价格控制销量

### 核心挑战：真实价格是动态序列

```
传统方法：单一变量（平均成交价）
真实场景：动态价格策略序列
├── 日常价
├── 周末促销
├── 大促降价
├── 满减
├── 区域优惠
└── 人群优惠券（可叠加）
```

### 三维评估体系

| 维度 | 评估内容 | 方法 |
|------|----------|------|
| **准确率维度** | 销量序列误差 | 预测值 vs 真实值对比 |
| **因果效应维度** | 价格调整的销量影响 | 逐段评估 + 拉长周期评估 |
| **因果逻辑校验** | 基本逻辑合理性 | 规则检测（如力度大销量应更高）|

### 动态因果响应模型

**输入三个维度**：
1. **商品基础信息** → 多模态大模型编码
2. **历史时序信息** → 时序网络编码
3. **价格策略信息** → **LLM直接编码自然语言描述** ⭐

> 创新点：使用LLM对复杂价格策略做编码，解决结构化输入的信息损失问题

### 两阶段训练流程

```
阶段1: 监督预训练 (SFT)
├─ 先训练单维度平均价格的小因果模型
├─ 用小模型对历史数据做数据增广
└─ 训练基础时序预测模型（因果正确性保证）

阶段2: 强化学习优化
├─ 输入成对价格序列（仅某段存在差异）
├─ 奖励函数：
│   ├─ 单因果模型评估
│   ├─ 拉长周期因果评估
│   └─ 因果逻辑规则校验
└─ 负奖励给不符合因果逻辑的输出
```

### 关键洞察

1. **预测准确 ≠ 决策准确**
   - 错误关联模型的单点预测误差可能更小
   - 但用于定价决策会得出完全错误的结论

2. **商业世界模型的价值**
   - 经营决策反馈周期长（数周甚至数月）
   - 直接在真实环境迭代试错成本高
   - 仿真环境可快速迭代降低风险

3. **混淆变量的处理**
   - 大促是典型的混淆变量：大促期间价格低+销量高
   - 不能直接推出"降价提升销量"

### 与传统方法的对比

| 方法 | 局限性 | 本方案优势 |
|------|--------|------------|
| 单变量因果推断 | 仅处理"降价/不降价" | 处理复杂价格序列 |
| 固定结构化输入 | 新增促销形式需改模型 | LLM编码灵活扩展 |
| 单次评估 | 无法评估序列决策 | 三维评估体系 |
