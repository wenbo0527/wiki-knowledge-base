# LLM与因果推断：大模型时代的因果AI

> 探索大语言模型如何增强因果推断能力，以及因果思维如何改进LLM

---

## 元信息

- **创建时间**: 2026-04-22
- **维护者**: 尼克·弗瑞
- **类型**: article
- **标签**: #causal-inference #llm #large-language-models #causal-ai #foundation-models
- **难度**: ⭐⭐⭐⭐

---

## 1. LLM能否进行因果推理？

### 1.1 当前能力评估

**LLM的因果能力（2024年水平）**：

| 能力 | 评估 | 说明 |
|------|------|------|
| **因果识别** | ⭐⭐⭐⭐ | 能从文本中识别因果关系 |
| **因果问答** | ⭐⭐⭐ | 基本因果问答表现良好 |
| **反事实推理** | ⭐⭐ | 复杂反事实表现有限 |
| **因果发现** | ⭐⭐ | 需要结合工具才能做因果发现 |
| **因果解释** | ⭐⭐⭐⭐ | 能生成高质量因果解释 |

### 1.2 核心问题

```
❌ LLM的问题：
- 缺乏真正的因果理解，只是模式匹配
- 容易受到虚假相关的影响
- 反事实推理能力有限

✅ 解决方案：
- 使用LLM增强因果推断的特定环节
- 将因果先验知识注入LLM
- 构建因果+LLM混合系统
```

---

## 2. LLM增强因果推断

### 2.1 核心框架

**CausalEval框架**：

```
┌─────────────────────────────────────────────────────────────┐
│  LLM增强因果推断流程                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: 因果假设生成（LLM）                                 │
│  ─────────────────────────────────                          │
│  用户描述 → LLM生成因果图候选                                 │
│                                                             │
│  输入: "我想分析营销活动对销售额的影响"                        │
│  输出: ["营销 → 销售", "季节 → 销售", "营销 ← 季节 → 销售"]   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 2: 因果结构验证（数据+LLM）                             │
│  ─────────────────────────────────                          │
│  使用数据验证LLM生成的因果假设                                │
│                                                             │
│  方法: PC算法 / GES / LLM辅助的因果发现                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 3: 因果效应估计（传统方法）                              │
│  ─────────────────────────────────                          │
│  DiD / PSM / IV / RDD 等                                    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 4: 因果解释生成（LLM）                                  │
│  ─────────────────────────────────                          │
│  将因果结果转化为自然语言解释                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 LLM生成因果假设

```python
import anthropic
from typing import List, Dict

class CausalHypothesisGenerator:
    """
    使用LLM生成因果假设
    """
    
    def __init__(self, model_name="claude-3-sonnet"):
        self.client = anthropic.Anthropic()
        self.model_name = model_name
    
    def generate_causal_hypotheses(
        self, 
        domain: str, 
        outcome: str, 
        treatments: List[str],
        covariates: List[str] = None
    ) -> List[Dict]:
        """
        生成因果假设
        
        参数:
        - domain: 领域描述
        - outcome: 结果变量
        - treatments: 处理变量列表
        - covariates: 可能的混杂变量
        """
        
        prompt = f"""你是因果推断专家。请为以下场景生成因果假设。

领域: {domain}
结果变量: {outcome}
处理变量: {', '.join(treatments)}
{('混杂变量: ' + ', '.join(covariates)) if covariates else ''}

请生成3-5个因果假设，每个假设包含：
1. 因果图描述（用箭头表示因果方向）
2. 混杂因素列表
3. 中介因素列表（如果有）
4. 冲突因素列表（如果有）

用JSON格式输出。
"""
        
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        hypotheses = json.loads(response.content[0].text)
        
        return hypotheses


# 使用示例
generator = CausalHypothesisGenerator()

hypotheses = generator.generate_causal_hypotheses(
    domain="电商平台的营销活动",
    outcome="月销售额",
    treatments=["优惠券投放", "限时折扣", "满减活动"],
    covariates=["用户活跃度", "商品类目", "季节因素", "用户年龄"]
)

print(hypotheses)
```

### 2.3 LLM辅助因果发现

```python
class LLMAssistedCausalDiscovery:
    """
    LLM辅助的因果发现
    结合领域知识和数据驱动方法
    """
    
    def __init__(self, llm_generator):
        self.llm = llm_generator
        self.constraints = []
    
    def add_structural_constraints(self, domain_knowledge: str):
        """
        添加领域知识约束
        
        例如：
        - "价格永远不能是销量的因果父节点"（销量不影响价格）
        - "用户满意度不受当次购买金额直接影响"
        """
        constraints_prompt = f"""从以下领域知识中提取因果约束：

{domain_knowledge}

请列出：
1. 必须存在的因果边（格式：A → B）
2. 不可能存在的因果边（格式：A ↛ B）
3. 因果顺序约束（格式：A 必须在 B 之前）

以JSON格式输出。
"""
        response = self.llm.client.messages.create(
            model=self.llm.model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": constraints_prompt}]
        )
        
        import json
        constraints = json.loads(response.content[0].text)
        self.constraints = constraints
        
        return constraints
    
    def discover_with_constraints(self, data: pd.DataFrame) -> nx.DiGraph:
        """
        使用约束进行因果发现
        """
        from causallearn import PC
        
        # 标准PC算法
        cg = PC(data.values)
        
        # 应用LLM生成的约束
        # 1. 移除不可能存在的边
        # 2. 添加必须存在的边
        # 3. 强制执行因果顺序
        
        self._apply_constraints(cg)
        
        return self._to_networkx(cg)
    
    def _apply_constraints(self, causal_graph):
        """应用约束到因果图"""
        for impossible_edge in self.constraints.get('impossible_edges', []):
            A, B = impossible_edge.split(' → ')
            if causal_graph.has_edge(A, B):
                causal_graph.remove_edge(A, B)
        
        for required_edge in self.constraints.get('required_edges', []):
            A, B = required_edge.split(' → ')
            if not causal_graph.has_edge(A, B):
                causal_graph.add_edge(A, B)
```

---

## 3. 因果改进LLM

### 3.1 核心思想

**问题**：LLM容易受到虚假相关的影响

**解决方案**：在LLM训练/推理中注入因果先验

```
虚假相关示例：
训练数据：所有正例都有特征A
测试：特征A出现在负例中
结果：LLM会把特征A作为正例的标志

因果诊断：
因果图：X → Y（X导致Y）
而非：X ← Z → Y（Z同时影响X和Y，X与Y是虚假相关）

因果纠偏方法：
1. 因果特征选择：只使用因果特征
2. 反事实数据增强：生成反事实样本
3. 因果正则化：惩罚虚假路径
```

### 3.2 因果特征选择

```python
class CausalFeatureSelector:
    """
    使用因果发现选择因果特征
    """
    
    def __init__(self):
        self.causal_features = None
    
    def select_causal_features(
        self, 
        data: pd.DataFrame, 
        target: str,
        n_features: int = 10
    ) -> List[str]:
        """
        选择因果特征
        
        方法：
        1. 构建因果图
        2. 识别直接指向目标的变量
        3. 排除中介变量（如果关注总效应则保留）
        """
        from causallearn import PC
        
        # 构建因果图
        cg = PC(data.values)
        
        # 获取因果图的邻接矩阵
        adj_matrix = cg.G.graph
        
        # 找到指向目标变量的直接原因
        target_idx = data.columns.get_loc(target)
        direct_causes = []
        
        for i, col in enumerate(data.columns):
            if adj_matrix[i, target_idx] != 0:  # i → target
                direct_causes.append(col)
        
        # 如果直接原因太少，加入因果路径上的变量
        if len(direct_causes) < n_features:
            # 找到2-hop因果路径上的变量
            for i in range(len(data.columns)):
                if adj_matrix[i, target_idx] == 0:
                    # 检查是否有 i → ... → target
                    for j in range(len(data.columns)):
                        if adj_matrix[i, j] != 0 and adj_matrix[j, target_idx] != 0:
                            direct_causes.append(col)
                            break
        
        self.causal_features = direct_causes[:n_features]
        return self.causal_features


# 使用示例
selector = CausalFeatureSelector()

# 假设我们要预测"sales"
causal_features = selector.select_causal_features(
    data=df,
    target='sales',
    n_features=10
)

print("因果特征:", causal_features)

# 用因果特征训练模型
X_causal = df[causal_features]
y = df['sales']

model = GradientBoostingRegressor()
model.fit(X_causal, y)
```

### 3.3 反事实数据增强

```python
class CounterfactualDataAugmentation:
    """
    反事实数据增强
    通过干预生成反事实样本
    """
    
    def __init__(self, causal_model):
        self.causal_model = causal_model
    
    def generate_counterfactuals(
        self, 
        sample: pd.Series, 
        interventions: List[Dict]
    ) -> List[pd.Series]:
        """
        对样本进行反事实干预
        
        sample: 原始样本
        interventions: 干预列表，格式：[{'var': 'price', 'value': 100}]
        """
        counterfactuals = []
        
        for intervention in interventions:
            # 执行 do(X = x) 干预
            cf_sample = self._do_intervention(sample, intervention)
            counterfactuals.append(cf_sample)
        
        return counterfactuals
    
    def _do_intervention(self, sample, intervention):
        """
        执行 do-intervention
        """
        cf_sample = sample.copy()
        
        var = intervention['var']
        value = intervention['value']
        
        # 设置干预值
        cf_sample[var] = value
        
        # 重新计算受影响的变量（沿着因果图）
        affected_vars = self._get_affected_variables(var)
        
        for affected_var in affected_vars:
            # 使用因果模型预测
            parents = self.causal_model.get_parents(affected_var)
            
            if parents:
                # 使用条件期望估计
                cf_sample[affected_var] = self.causal_model.predict_mean(
                    affected_var, 
                    {p: cf_sample[p] for p in parents}
                )
        
        return cf_sample
    
    def augment_dataset(
        self, 
        data: pd.DataFrame, 
        treatment_var: str,
        n_cf_per_sample: int = 2
    ) -> pd.DataFrame:
        """
        增强数据集
        """
        augmented_data = [data]
        
        for idx, sample in data.iterrows():
            # 生成反事实样本（处理组→对照组，对照组→处理组）
            interventions = [
                {treatment_var: 1 - sample[treatment_var]}  # 翻转处理状态
            ]
            
            counterfactuals = self.generate_counterfactuals(sample, interventions)
            
            for cf in counterfactuals:
                cf_row = data.iloc[[idx]].copy()
                for var, value in cf.items():
                    cf_row[var] = value
                augmented_data.append(cf_row)
        
        return pd.concat(augmented_data, ignore_index=True)
```

---

## 4. 因果LLM应用案例

### 4.1 医疗诊断辅助

```python
class MedicalDiagnosisCausalLLM:
    """
    医疗诊断的因果LLM系统
    """
    
    def __init__(self):
        self.causal_graph = self._build_medical_causal_graph()
        self.llm = CausalHypothesisGenerator()
    
    def _build_medical_causal_graph(self):
        """
        构建医疗因果图（简化版）
        """
        graph = {
            'symptoms': ['fever', 'cough', 'fatigue', 'headache'],
            'diseases': ['flu', 'covid', 'cold'],
            'risk_factors': ['age', 'vaccination_status', 'comorbidity'],
            'edges': [
                # 风险因素 → 疾病
                ('age', 'flu'), ('age', 'covid'),
                ('vaccination_status', 'flu'),
                ('comorbidity', 'covid'),
                
                # 疾病 → 症状
                ('flu', 'fever'), ('flu', 'cough'), ('flu', 'fatigue'),
                ('covid', 'fever'), ('covid', 'cough'), ('covid', 'fatigue'),
                ('cold', 'cough'),
                
                # 症状之间的关系（虚假相关）
                ('fever', 'headache'),  # 发热导致头痛
            ]
        }
        return graph
    
    def diagnose_with_explanation(
        self, 
        patient_info: Dict,
        symptoms: List[str]
    ) -> Dict:
        """
        带因果解释的诊断
        """
        # Step 1: LLM生成可能的病因假设
        hypotheses = self.llm.generate_causal_hypotheses(
            domain="传染病诊断",
            outcome="疾病诊断",
            treatments=["病毒感染"],
            covariates=["年龄", "疫苗状态", "基础病"]
        )
        
        # Step 2: 因果推断计算疾病概率
        disease_probs = self._compute_disease_causal_probability(
            patient_info, symptoms
        )
        
        # Step 3: LLM生成诊断解释
        explanation = self._generate_explanation(
            patient_info, symptoms, disease_probs
        )
        
        return {
            'primary_diagnosis': max(disease_probs, key=disease_probs.get),
            'differential_diagnosis': disease_probs,
            'causal_explanation': explanation
        }
    
    def _compute_disease_causal_probability(self, patient_info, symptoms):
        """
        使用贝叶斯网络计算疾病概率
        """
        # 简化实现
        # 实际应使用pgmpy或其他概率编程库
        return {
            'flu': 0.6,
            'covid': 0.3,
            'cold': 0.1
        }
    
    def _generate_explanation(self, patient_info, symptoms, disease_probs):
        """
        LLM生成因果解释
        """
        prompt = f"""根据以下信息生成诊断解释：

患者信息：{patient_info}
症状：{symptoms}
疾病概率：{disease_probs}

请生成：
1. 主要诊断的依据（因果解释）
2. 为什么其他疾病可能性较低
3. 建议的检查项目

以通俗易懂的语言解释。
"""
        # 调用LLM
        response = self.llm.client.messages.create(
            model=self.llm.model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
```

### 4.2 商业决策支持

```python
class BusinessDecisionCausalLLM:
    """
    商业决策的因果LLM系统
    """
    
    def __init__(self):
        self.llm = CausalHypothesisGenerator()
    
    def analyze_decision(
        self,
        decision: str,  # "是否降价10%"
        context: Dict,  # 市场上下文
        historical_data: pd.DataFrame
    ) -> Dict:
        """
        决策的因果分析
        """
        # Step 1: LLM理解决策场景
        decision_understanding = self._understand_decision(decision, context)
        
        # Step 2: 构建因果模型
        causal_model = self._build_decision_causal_model(
            decision, context, historical_data
        )
        
        # Step 3: 反事实分析
        counterfactual_results = self._run_counterfactual_analysis(
            causal_model, historical_data
        )
        
        # Step 4: LLM生成决策建议
        recommendation = self._generate_recommendation(
            decision, decision_understanding, counterfactual_results
        )
        
        return {
            'decision': decision,
            'expected_outcome': counterfactual_results['expected_effect'],
            'confidence_interval': counterfactual_results['ci'],
            'risks': counterfactual_results['risks'],
            'recommendation': recommendation
        }
    
    def _understand_decision(self, decision, context):
        """LLM理解决策"""
        prompt = f"""分析以下商业决策：

决策：{decision}
上下文：{context}

请提取：
1. 处理变量（我们控制的）
2. 结果变量（我们关心的）
3. 可能的混杂因素
4. 预期的因果路径
"""
        # 简化：返回基本理解
        return {
            'treatment': 'price_change',
            'outcome': 'revenue',
            'confounders': ['competitor_price', 'seasonality', 'marketing_spend']
        }
    
    def _build_decision_causal_model(self, decision, context, data):
        """构建因果模型"""
        # 使用数据学习因果结构
        return CausalModel(data)
    
    def _run_counterfactual_analysis(self, causal_model, data):
        """反事实分析"""
        return {
            'expected_effect': '+8.5% revenue',
            'ci': ['+5.2%', '+11.8%'],
            'risks': ['competitor response', 'brand perception impact']
        }
    
    def _generate_re