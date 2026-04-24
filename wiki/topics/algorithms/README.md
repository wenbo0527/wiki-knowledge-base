# 算法专题 (Algorithms)

> 从基础理论到工程实践的全栈算法知识体系

---

## 元信息

- **创建时间**: 2026-04-20
- **维护者**: 尼克·弗瑞
- **类型**: topic
- **标签**: #algorithms #machine-learning #data-science

---

## 专题定位

本专题覆盖算法领域的核心知识体系，重点关注：

1. **基础理论** - 算法设计与分析、复杂度理论
2. **机器学习** - 监督/无监督/强化学习
3. **因果推断** - 从相关性到因果性 ⭐ 核心专题
4. **系统工程** - ML系统设计、推荐系统、NLP
5. **评估实验** - A/B测试、因果推断实验设计

---

## 目录结构

```
algorithms/
├── README.md                    # 本文件：专题总览
├── causal-inference/            # 因果推断 ⭐
│   ├── README.md
│   ├── potential-outcomes.md    # 潜在结果框架
│   ├── do-calculus.md           # Pearl的do-演算
│   ├── instrumental-variables.md # 工具变量
│   ├── diff-in-diff.md          # 双重差分
│   ├── applications.md          # 应用案例（金融风控）
│   └── tools.md                 # 工具包
├── ml-systems/                  # ML系统设计
├── recommendation/              # 推荐算法
├── nlp/                         # NLP算法
└── evaluation/                  # 评估与实验
```

---

## 学习路径

### 路径一：因果推断专家（推荐）

```
1. 潜在结果框架 → 2. 工具变量/DID → 3. Pearl因果图
     ↓
4. 金融风控应用 → 5. 实验平台设计
```

### 路径二：ML系统工程师

```
1. 基础ML算法 → 2. 特征工程 → 3. 模型 serving
     ↓
4. 推荐系统 → 5. A/B测试平台
```

---

## 与现有专题的关联

| 本专题 | 关联专题 | 关联点 |
|--------|----------|--------|
| 因果推断 | `fintech/risk-management` | 风控策略归因分析 |
| 因果推断 | `fintech/marketing-suite` | 营销效果评估 |
| 因果推断 | `analysis-frameworks` | 分析框架底层逻辑 |
| ML系统 | `ai-programming` | 工程实现 |
| 推荐系统 | `product-management` | 产品策略 |

---

## 待建设内容

- [ ] `ml-systems/` - ML系统设计
- [ ] `recommendation/` - 推荐算法
- [ ] `nlp/` - NLP算法
- [ ] `evaluation/` - 评估与实验

---

## 参考资源

### 因果推断
- **书籍**: *Causal Inference in Statistics* (Pearl)
- **书籍**: *Mostly Harmless Econometrics* (Angrist & Pischke)
- **课程**: Causal Inference for Data Science (Coursera)

### ML系统
- **书籍**: *Designing Machine Learning Systems* (Chip Huyen)
- **书籍**: *Machine Learning Engineering* (Andriy Burkov)

---

*最后更新: 2026-04-20*  
*维护者: 尼克·弗瑞*  
*状态: 🚧 建设中 - 因果推断专题优先*
