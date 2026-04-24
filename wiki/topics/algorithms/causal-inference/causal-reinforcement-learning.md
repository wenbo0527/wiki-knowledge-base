# 因果强化学习（Causal Reinforcement Learning）

> 将因果推断融入强化学习：因果策略、状态抽象与反事实决策

---

## 元信息

- **创建时间**: 2026-04-22
- **维护者**: 尼克·弗瑞
- **类型**: article
- **标签**: #causal-inference #reinforcement-learning #causal-rl #decision-making
- **难度**: ⭐⭐⭐⭐⭐

---

## 1. 为什么强化学习需要因果？

### 1.1 传统RL的问题

**关联性陷阱**：
```
传统RL观察到的数据：
State S_t → Action A_t → Reward R_{t+1} → State S_{t+1}

问题：
- RL学习的是"相关性"而非"因果性"
- 策略可能学到虚假关联（spurious correlations）
- 在分布偏移时泛化能力差
```

**因果强化学习的目标**：
> 学习可解释、可泛化、可干预的决策策略

### 1.2 因果视角的强化学习

| 传统RL | 因果RL |
|--------|--------|
| 最大化累积奖励 | 学习因果效应下的最优策略 |
| 策略是黑箱 | 策略有因果解释 |
| 对环境变化脆弱 | 理解干预效果，泛化能力强 |
| 需要大量数据 | 利用因果结构减少数据需求 |

---

## 2. 核心概念

### 2.1 因果策略（Causal Policy）

**定义**：考虑动作的因果效应的策略

```
因果策略 vs 传统策略：

传统策略: π(a|s) = P(A=a|S=s)
因果策略: π(a|s, do(X=x)) = P(Y=y | S=s, do(A=a))

区别：考虑如果我干预设置A=a，会发生什么
```

### 2.2 反事实RL（Counterfactual RL）

**核心思想**：利用反事实推理来提升策略学习效率

```python
class CounterfactualRL:
    """
    反事实强化学习框架
    """
    
    def __init__(self, env, causal_model):
        self.env = env
        self.causal_model = causal_model  # 因果图模型
    
    def counterfactual_value(self, state, action, imagined_action):
        """
        计算反事实价值：如果我采取imagined_action而不是action
        """
        # Step 1: 识别当前状态的因果图
        causal_graph = self.causal_model.get_graph(state)
        
        # Step 2: 计算干预 do(A = imagined_action) 的效应
        counterfactual_state = self.causal_model.do_intervention(
            state,
            action=imagined_action
        )
        
        # Step 3: 估计反事实奖励
        cf_reward = self.env.reward(counterfactual_state, imagined_action)
        
        return cf_reward
    
    def update_policy(self, experience_buffer):
        """
        使用反事实经验更新策略
        """
        for state, action, reward, next_state in experience_buffer:
            # 对每个采取的动作，想象一个反事实动作
            for cf_action in self.counterfactual_actions:
                cf_reward = self.counterfactual_value(state, action, cf_action)
                
                # 计算反事实优势
                advantage = cf_reward - self.baseline(state)
                
                # 更新策略
                self.policy.update(state, cf_action, advantage)
```

---

## 3. 状态抽象的因果学习

### 3.1 问题定义

**状态抽象（State Abstraction）**：将相似状态归类，提取关键特征

```
为什么需要因果状态抽象？

例子：自动驾驶
- 状态空间巨大（无数种路况组合）
- 但驾驶决策的因果因素只有几个：
  - 前车距离 → 刹车
  - 红灯/绿灯 → 停车/前进
  - 行人 → 减速

因果状态抽象 = 识别哪些状态特征真正影响决策
```

### 3.2 因果状态抽象（Causal State Abstraction）

```python
class CausalStateAbstraction:
    """
    因果状态抽象：从数据中学习决策相关的状态特征
    """
    
    def __init__(self, state_dims, action_dims):
        self.state_dims = state_dims
        self.action_dims = action_dims
        self.causal_graph = None
        self.abstract_states = None
    
    def learn_causal_abstraction(self, data, n_abstraction_levels=3):
        """
        学习因果状态抽象
        
        data: 包含(state, action, reward, next_state)的经验数据
        """
        # Step 1: 构建因果图（使用因果发现）
        self.causal_graph = self._discover_causal_graph(data)
        
        # Step 2: 识别每个动作的因果父节点
        causal_parents = self._identify_causal_parents()
        
        # Step 3: 基于因果父节点进行状态抽象
        self.abstract_states = self._compute_abstraction(causal_parents)
        
        return self.abstract_states
    
    def _discover_causal_graph(self, data):
        """使用PC算法发现因果图"""
        from pgmpy.estimate import PC
        
        # 构建状态-动作-下一状态的联合数据
        joint_data = pd.DataFrame(data)
        
        pc = PC(joint_data)
        model = pc.estimate(variant='stable', significance_level=0.05)
        
        return model
    
    def _identify_causal_parents(self):
        """识别每个动作的因果父节点"""
        causal_parents = {}
        
        for action in self.action_dims:
            # 找到直接指向该动作的变量
            # 以及从动作指向的变量
            parents = []
            children = []
            
            for edge in self.causal_graph.edges():
                if edge[1] == action:
                    parents.append(edge[0])
                if edge[0] == action:
                    children.append(edge[1])
            
            causal_parents[action] = {
                'parents': parents,      # 影响动作的变量
                'children': children     # 动作影响的变量
            }
        
        return causal_parents
    
    def _compute_abstraction(self, causal_parents, n_levels=3):
        """计算分层抽象"""
        # 提取核心因果变量
        core_variables = set()
        for action in causal_parents:
            core_variables.update(causal_parents[action]['parents'])
            core_variables.update(causal_parents[action]['children'])
        
        # 创建抽象映射
        abstraction_levels = {}
        
        # Level 0: 完整状态
        abstraction_levels[0] = lambda s: s
        
        # Level 1: 只保留因果相关变量
        abstraction_levels[1] = lambda s: {k: v for k, v in s.items() if k in core_variables}
        
        # Level 2+: 进一步离散化
        # ...
        
        return abstraction_levels
```

---

## 4. 因果奖励塑造（Causal Reward Shaping）

### 4.1 问题

传统RL的奖励函数可能包含虚假关联，导致：
- 策略对无关特征敏感
- 奖励黑客（reward hacking）
- 泛化能力差

### 4.2 因果奖励塑造

```python
class CausalRewardShaping:
    """
    因果奖励塑造：将领域知识编码为因果奖励
    """
    
    def __init__(self, causal_graph):
        self.causal_graph = causal_graph
    
    def shape_reward(self, state, action, next_state, intrinsic_reward):
        """
        塑造奖励，增强因果结构
        
        参数:
        - state, action, next_state: 转移
        - intrinsic_reward: 环境原始奖励
        """
        # Step 1: 计算因果效应分数
        causal_effect = self._compute_causal_effect(state, action, next_state)
        
        # Step 2: 计算因果一致性分数
        causal_consistency = self._check_causal_consistency(action, next_state)
        
        # Step 3: 组合奖励
        shaped_reward = (
            intrinsic_reward +
            0.1 * causal_effect +
            0.05 * causal_consistency
        )
        
        return shaped_reward
    
    def _compute_causal_effect(self, state, action, next_state):
        """
        计算动作的因果效应
        """
        # 找到动作的直接因果后代
        effects = []
        
        for edge in self.causal_graph.edges():
            if edge[0] == 'action':
                effect_var = edge[1]
                # 计算该变量的变化
                if effect_var in state and effect_var in next_state:
                    delta = abs(next_state[effect_var] - state[effect_var])
                    effects.append(delta)
        
        return sum(effects) / len(effects) if effects else 0
    
    def _check_causal_consistency(self, action, next_state):
        """
        检查是否与因果结构一致
        """
        # 检查动作的预期效果是否出现
        expected_effects = self._get_expected_effects(action)
        
        consistency_score = 0
        for var, expected_change in expected_effects.items():
            if var in next_state:
                actual_change = next_state[var] - action.get(var, 0)
                if expected_change * actual_change > 0:  # 同向变化
                    consistency_score += 1
        
        return consistency_score / len(expected_effects) if expected_effects else 0
```

---

## 5. 离线因果RL（Offline Causal RL）

### 5.1 问题定义

**离线RL**：从已收集的日志数据中学习策略

**因果视角的挑战**：
- 数据收集策略与目标策略不同（分布偏移）
- 未观测的混杂因素
- 反事实评估的需求

### 5.2 因果离线RL框架

```python
class CausalOfflineRL:
    """
    因果离线强化学习
    """
    
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.causal_model = None
        self.policy = None
    
    def fit(self, dataset, gamma=0.99):
        """
        从离线数据学习
        
        dataset: {(s, a, r, s')}
        """
        # Step 1: 从数据中学习因果结构
        self.causal_model = self._learn_causal_structure(dataset)
        
        # Step 2: 估计因果转移模型
        self.causal_transition = self._estimate_causal_transition(dataset)
        
        # Step 3: 矫正分布偏移
       矫正后的数据 = self._adjust_distribution_shift(dataset)
        
        # Step 4: 用矫正数据训练策略
        self.policy = self._train_policy(矫正后的数据, gamma)
        
        return self.policy
    
    def _learn_causal_structure(self, dataset):
        """
        学习因果结构
        """
        from causalgraphicalmodels import CausalGraphicalModel
        
        # 准备数据：s, a, s'的联合分布
        data = []
        for s, a, r, s_next in dataset:
            row = {**s, **a, **s_next}
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # PC算法发现因果结构
        # 状态变量 ← 动作 → 下一状态变量
        # 或更复杂的结构
        
        return causal_model
    
    def _adjust_distribution_shift(self, dataset):
        """
        使用因果模型矫正分布偏移
        
        核心思想：只对因果相关的分布偏移进行矫正
        """
       矫正_data = []
        
        for s, a, r, s_next in dataset:
            # 计算倾向得分（使用因果父节点）
            p_a_given_parents = self._compute_action_score(s, a)
            
            # 重要性加权
            importance_weight = 1 / p_a_given_parents
            
            # 加权样本
            for _ in range(int(importance_weight)):
               矫正_data.append((s, a, r, s_next))
        
        return矫正_data
    
    def _compute_action_score(self, state, action):
        """
        计算倾向得分（基于因果父节点）
        """
        # 找到动作的因果父节点
        causal_parents = self.causal_model.get_parents('action')
        
        # 只用因果父节点计算倾向
        parent_values = {k: state[k] for k in causal_parents if k in state}
        
        # 估计 P(A|Parents)
        score = self.action_model.predict(parent_values)
        
        return score
```

---

## 6. 实战案例：金融交易Agent

### 6.1 场景

**加密货币日内交易Agent**：
- 状态：价格、技术指标、市场情绪
- 动作：买入、持有、卖出
- 奖励：利润/损失

### 6.2 因果RL实现

```python
class CryptoTradingCausalRL:
    """
    加密货币交易的因果RL Agent
    """
    
    def __init__(self):
        self.causal_model = None
        self.policy_network = None
        self.value_network = None
    
    def build_causal_graph(self, historical_data):
        """
        构建交易场景的因果图
        """
        # 使用领域知识 + 数据验证构建因果图
        
        causal_graph = {
            'variables': [
                'price_change',      # 价格变化
                'volume',            # 成交量
                'volatility',        # 波动率
                'sentiment',         # 市场情绪
                'macro_index',       # 宏观指标
                'action',            # 交易动作
                'pnl'               # 盈亏
            ],
            'edges': [
                # 技术指标影响价格
                ('volume', 'price_change'),
                ('volatility', 'price_change'),
                
                # 市场情绪影响价格
                ('sentiment', 'price_change'),
                
                # 宏观影响
                ('macro_index', 'price_change'),
                ('macro_index', 'sentiment'),
                
                # 动作影响盈亏（直接因果）
                ('action', 'pnl'),
                ('price_change', 'pnl'),
                
                # 价格变化影响下一时刻的指标
                ('price_change', 'volume'),
                ('price_change', 'volatility'),
            ]
        }
        
        return causal_graph
    
    def learn_causal_policy(self, states, actions, rewards, next_states):
        """
        学习因果策略
        """
        # Step 1: 构建因果图
        causal_graph = self.build_causal_graph(states)
        
        # Step 2: 识别动作的因果父节点
        # 动作应该只由因果父节点决定，而非所有状态变量
        action_parents = self._get_action_causal_parents(causal_graph)
        
        # Step 3: 只用因果父节点训练策略
        causal_states = states[:, action_parents]  # 只选因果相关特征
        
        # 训练策略网络
        self.policy_network = self._train_policy_network(
            causal_states, 
            actions, 
            rewards
        )
        
        # Step 4: 使用反事实评估
        self._counterfactual_evaluation(causal_states, actions, rewards)
    
    def _get_action_causal_parents(self, graph):
        """
        获取动作的因果父节点索引
        """
        # 基于领域知识
        # 交易动作主要由以下因素决定：
        # 1. 短期价格动量（price_change）
        # 2. 波动率（volatility）
        # 3. 风险偏好（sentiment的某个维度）
        
        parent_indices = [0, 2, 3]  # 假设对应关系
        return parent_indices
    
    def select_action(self, state):
        """
        基于因果策略选择动作
        """
        # 只提取因果父节点
        causal_state = state[self.causal_parent_indices]
        
        # 策略网络输出动作概率
        action_probs = self.policy_network.predict(causal_state.reshape(1, -1))
        
        # epsilon-greedy
        if np.random.random() < 0.1:
            return np.random.randint(3)
        
        return np.argmax(action_probs)
```

---

## 7. 工具与资源

### 7.1 主要库

| 库 | 语言 | 功能 | GitHub |
|------|------|------|--------|
| CausalRL | Python | 因果强化学习算法 |TDB |
| causal-world | Python | 因果RL环境 | causal-world |
| DoWhy-RL | Python | 因果+RL结合 | DoWhy扩展 |
| CausalAgents | Python | 多智能体因果 | research |

### 7.2 经典论文

| 论文 | 年份 | 核心贡献 |
|------|------|----------|
| Causal Reasoning for RL | 2019 | 因果RL基础框架 |
| State Abstraction via Causal | 2020 | 因果状态抽象 |
| Offline Causal RL | 2021 | 离线因果RL |
| Causal Reward Shaping | 2022 | 因果奖励塑造 |
| Foundation Models for CausalRL | 2024 | 大模型+因果RL |

### 7.3 学习路径

```
阶段1: 基础（2-3周）
├── 因果推断基础（潜在结果框架、do演算）
├── 强化学习基础（马尔可夫决策过程）
└── 因果图基础（d-separation、因果路径）

阶段2: 因果RL核心（4-6周）
├── CausalRL框架
├── 反事实RL
├── 因果状态抽象
└── 因果奖励塑造

阶段3: 高级专题（持续）
├── 离线因果RL
├── 多智能体因果RL
├── 因果策略迁移
└── 因果RL在大模型Agent中的应用
```

---

## 8. 与其他专题的关联

| 因果RL应用 | Wiki关联 |
|------------|----------|
| 自动驾驶 | `autonomous-driving`, `simulation` |
| 金融交易 | `fintech/risk-management` |
| 推荐系统 | `recommendation-systems` |
| 机器人控制 | `robotics/control-systems` |
| 大模型Agent | `concepts/llm-agent` |

---

*最后更新: 2026-04-22*
*维护者: 尼克·弗瑞*
