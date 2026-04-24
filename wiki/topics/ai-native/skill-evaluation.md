# Skill 自动评分系统

> AI Agent技能评估与质量控制的完整技术指南  
> 相关Insight: [OpenAI Skill自动评分系统调研](../insights/insight-20260421-openai-skill-evaluation.md)

---

## 概述

Skill自动评分系统是一套用于评估AI Agent技能表现的自动化框架。通过多维度评分、混合架构和反馈闭环，实现企业级的Skill质量管控。

### 核心价值

| 价值 | 说明 | 适用场景 |
|:---|:---|:---|
| **质量保证** | 自动发现Skill缺陷，拦截低质量输出 | 生产环境 |
| **持续优化** | 基于评分反馈持续改进Skill表现 | 迭代开发 |
| **基准测试** | 建立Skill性能基线，追踪改进效果 | 版本对比 |
| **A/B测试** | 对比不同版本Skill的表现差异 | 模型选型 |

---

## 技术架构

### 三层混合架构

```
┌────────────────────────────────────────────────────────────┐
│                    Skill Evaluation System                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   ┌──────────────┐    ┌──────────────┐    ┌─────────────┐ │
│   │  规则评分层  │    │  模型评分层  │    │  人工评分层  │ │
│   │  Rule Layer  │    │ Model Layer  │    │ Human Layer │ │
│   │   (30%)      │    │    (50%)     │    │    (20%)    │ │
│   └──────┬───────┘    └──────┬───────┘    └──────┬──────┘ │
│          │                   │                    │        │
│          └───────────────────┼────────────────────┘        │
│                              ▼                             │
│                    ┌──────────────────┐                   │
│                    │  加权聚合层        │                   │
│                    │ (动态权重调整)     │                   │
│                    └────────┬─────────┘                   │
│                             ▼                              │
│                    ┌──────────────────┐                   │
│                    │  最终评分 + 反馈   │                   │
│                    └──────────────────┘                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 各层职责

#### 规则评分层 (Rule Layer)

**目的**: 快速过滤明显不合格的输出，降低后续层成本

**评分内容**:
- **格式验证**: JSON Schema验证、必填字段检查
- **数值范围**: 数值是否在合理区间
- **关键词检查**: 敏感词/禁用词检测
- **长度限制**: 输出长度是否在预期范围

**实现代码**:
```python
class RuleEvaluator:
    """规则评分器 - 低成本快速筛选"""
    
    def __init__(self):
        self.schema = self._load_schema()
        self.banned_keywords = ['敏感词', '违规内容']
    
    def evaluate(self, output: dict) -> dict:
        scores = {
            'format': self._check_format(output),
            'completeness': self._check_completeness(output),
            'range': self._check_range(output),
            'keywords': self._check_keywords(output)
        }
        
        # 如果有任何一项失败，整体失败
        passed = all(s['passed'] for s in scores.values())
        
        return {
            'passed': passed,
            'score': self._calculate_score(scores) if passed else 0,
            'details': scores,
            'layer': 'rule'
        }
    
    def _check_format(self, output: dict) -> dict:
        """验证JSON Schema"""
        try:
            jsonschema.validate(output, self.schema)
            return {'passed': True, 'score': 1.0}
        except jsonschema.ValidationError as e:
            return {'passed': False, 'score': 0, 'error': str(e)}
```

#### 模型评分层 (Model Layer)

**目的**: 利用LLM的语义理解能力评估输出质量

**评分维度**:
| 维度 | 权重 | 评分标准 | 说明 |
|:---|:---:|:---|:---|
| **准确性** | 40% | 1-5分 | 事实正确、数据准确 |
| **完整性** | 25% | 1-5分 | 覆盖需求、无遗漏 |
| **合规性** | 20% | 1-5分 | 符合规范、无风险 |
| **表达性** | 15% | 1-5分 | 清晰易懂、结构合理 |

**Prompt模板**:
```python
JUDGE_PROMPT = """你是一位专业的Skill质量评估专家。请对以下Skill执行结果进行客观评分。

【评分维度】(每项1-5分)
1. 准确性(40%): 内容是否事实正确、数据准确
2. 完整性(25%): 是否覆盖所有需求点、有无遗漏  
3. 合规性(20%): 是否符合行业规范、有无风险点
4. 表达性(15%): 是否清晰易懂、结构是否合理

【评分标准】
5分: 优秀 - 完全符合标准，无可挑剔
4分: 良好 - 基本符合标准，少量改进空间
3分: 合格 - 基本可用，有明显改进空间
2分: 较差 - 存在较多问题，需要大幅改进
1分: 不合格 - 严重问题，无法使用

【原始需求】
{requirement}

【Skill输出】
{output}

请以JSON格式输出评分结果:
{
  "scores": {
    "accuracy": 1-5,
    "completeness": 1-5,
    "compliance": 1-5,
    "clarity": 1-5
  },
  "weighted_score": "计算后的加权总分",
  "explanation": "详细评分说明，指出优点和改进点",
  "strengths": ["优点1", "优点2"],
  "weaknesses": ["改进点1", "改进点2"],
  "recommendations": ["具体建议1", "具体建议2"]
}
"""
```

**实现代码**:
```python
class LLMJudgeEvaluator:
    """LLM评判评分器 - 语义级评估"""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.dimensions = {
            "accuracy": {"weight": 0.4, "desc": "事实正确、数据准确"},
            "completeness": {"weight": 0.25, "desc": "覆盖需求、无遗漏"},
            "compliance": {"weight": 0.2, "desc": "符合规范、无风险"},
            "clarity": {"weight": 0.15, "desc": "清晰易懂、结构合理"}
        }
    
    def evaluate(self, output: str, requirement: str) -> dict:
        """执行LLM评估"""
        
        prompt = self._build_prompt(output, requirement)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert evaluator. Be objective and critical."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # 低温度确保稳定性
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        result['weighted_score'] = self._calculate_weighted_score(result['scores'])
        result['layer'] = 'model'
        
        return result
    
    def _calculate_weighted_score(self, scores: dict) -> float:
        """计算加权总分"""
        total = 0
        for dim, score in scores.items():
            weight = self.dimensions.get(dim, {}).get('weight', 0.25)
            total += score * weight
        return round(total, 2)
```

#### 人工评分层 (Human Layer)

**目的**: 提供黄金标准，校准和优化模型评分

**实施策略**:
- **随机抽样**: 5-10%的样本进入人工审核
- **强制审核**: 低分样本(<3分)强制人工确认
- **定期校准**: 每周抽取50条样本进行人工评分，对比模型评分
- **反馈闭环**: 人工评分用于微调和优化模型评分Prompt

---

## 实现方案

### 方案A: OpenAI Evals (推荐入门)

**适用场景**: 快速验证、标准化测试

**快速开始**:
```bash
# 安装
git clone https://github.com/openai/evals.git
cd evals && pip install -e .

# 创建评估配置
cat > evals/registry/evals/my_skill.yaml << 'EOF'
my_skill:
  id: my_skill.dev.v0
  metrics: [accuracy]
  description: Evaluate my custom skill
EOF

# 准备数据
cat > evals/registry/data/my_skill/samples.jsonl << 'EOF'
{"input": [{"role": "user", "content": "What is 2+2?"}], "ideal": "4"}
EOF

# 运行评估
oaieval gpt-3.5-turbo my_skill
```

### 方案B: DeepEval (推荐企业)

**适用场景**: 企业级应用、开箱即用

```python
# 安装
pip install deepeval

# 快速开始
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

# 定义测试用例
test_case = LLMTestCase(
    input="What is the capital of France?",
    actual_output="The capital of France is Paris",
    expected_output="Paris",
    context=["France is a country in Europe"]
)

# 定义指标
metric = AnswerRelevancyMetric(threshold=0.7)

# 执行评估
assert_test(test_case, [metric])
```

### 方案C: 自定义实现 (推荐深度定制)

**完整代码示例**: 见[快速启动指南](https://github.com/your-repo/skill-evaluation-guide)

```python
# skill_evaluation_pipeline.py
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class EvaluationResult:
    """评估结果"""
    final_score: float
    rule_score: float
    model_score: float
    human_score: Optional[float]
    passed: bool
    details: Dict
    recommendations: List[str]

class SkillEvaluationPipeline:
    """Skill评估流水线"""
    
    def __init__(self, config: dict):
        self.rule_evaluator = RuleEvaluator()
        self.model_evaluator = LLMJudgeEvaluator(config.get('model', 'gpt-4'))
        self.weight_adjuster = DynamicWeightAdjuster()
        self.sampling_rate = config.get('sampling_rate', 0.1)
    
    def evaluate(self, skill_output: dict, requirement: str) -> EvaluationResult:
        """执行完整评估"""
        
        # Phase 1: 规则层
        rule_result = self.rule_evaluator.evaluate(skill_output)
        if not rule_result['passed']:
            return EvaluationResult(
                final_score=0,
                rule_score=0,
                model_score=0,
                human_score=None,
                passed=False,
                details={'rule': rule_result},
                recommendations=["Fix basic format/validation issues"]
            )
        
        # Phase 2: 模型层
        model_result = self.model_evaluator.evaluate(
            json.dumps(skill_output), 
            requirement
        )
        
        # Phase 3: 人工层 (抽样)
        human_result = None
        if self._should_sample(model_result):
            human_result = self._human_evaluation(skill_output, requirement)
        
        # 计算最终分数
        weights = self.weight_adjuster.get_weights()
        final_score = (
            weights['rule'] * rule_result['score'] +
            weights['model'] * model_result['weighted_score'] / 5 +  # 归一化到0-1
            (weights['human'] * human_result['score'] if human_result else 0)
        )
        
        return EvaluationResult(
            final_score=round(final_score, 2),
            rule_score=rule_result['score'],
            model_score=model_result['weighted_score'] / 5,
            human_score=human_result['score'] if human_result else None,
            passed=final_score >= 0.6,  # 及格线
            details={
                'rule': rule_result,
                'model': model_result,
                'human': human_result
            },
            recommendations=model_result.get('recommendations', [])
        )
```

---

## 最佳实践

### 1. 评分标准设计

**设计原则**:
- **SMART原则**: 具体、可衡量、可达成、相关、有时限
- **渐进式细化**: 从粗粒度开始，逐步细化评分维度
- **人工对齐**: 确保评分标准与人工评估一致

**评分维度选择**:
| 场景 | 推荐维度 | 权重配置 |
|:---|:---|:---|
| 客服机器人 | 准确性>完整性>礼貌性>效率 | 40:25:20:15 |
| 代码生成 | 准确性>可运行性>可读性>效率 | 50:25:15:10 |
| 内容创作 | 创意性>完整性>准确性>合规性 | 30:30:25:15 |
| 数据分析 | 准确性>完整性>可视化>洞察 | 40:30:15:15 |

### 2. Prompt工程

**优化技巧**:
```python
# 1. 增加示例 (Few-shot)
JUDGE_PROMPT_WITH_EXAMPLES = """
【示例1 - 优秀输出 (5分)】
输入: "法国首都是哪里？"
输出: "法国的首都是巴黎，位于法国北部。"
评分: {"accuracy": 5, "completeness": 5, "compliance": 5, "clarity": 5}
理由: 准确、完整、无风险、清晰

【示例2 - 较差输出 (2分)】
输入: "法国首都是哪里？"
输出: "巴黎吧"
评分: {"accuracy": 4, "completeness": 2, "compliance": 5, "clarity": 3}
理由: 基本准确但不完整，缺乏详细信息

【待评估输出】
...
"""

# 2. 增加COT推理 (Chain of Thought)
COT_PROMPT = """
请逐步思考并评分:

1. 先阅读原始需求，理解预期目标
2. 再阅读Skill输出，分析是否符合需求
3. 逐维度评估，说明评分理由
4. 汇总评分，给出改进建议

【逐步思考过程】:
"""

# 3. 增加自洽性检查
SELF_CONSISTENCY_PROMPT = """
请从不同角度评估此输出:
- 从用户视角: 是否解决了我的问题？
- 从专业视角: 是否符合行业标准？
- 从安全视角: 是否有潜在风险？
- 从体验视角: 是否清晰易懂？

综合以上角度给出最终评分。
"""
```

### 3. 反馈闭环

```python
class FeedbackLoop:
    """反馈闭环系统"""
    
    def __init__(self):
        self.feedback_db = []
        self.correction_threshold = 0.5  # 评分差异阈值
    
    def collect_feedback(self, evaluation_id: str, human_score: float, comment: str):
        """收集人工反馈"""
        self.feedback_db.append({
            'evaluation_id': evaluation_id,
            'human_score': human_score,
            'comment': comment,
            'timestamp': datetime.now()
        })
    
    def analyze_divergence(self) -> dict:
        """分析模型评分与人工评分的差异"""
        divergences = []
        for feedback in self.feedback_db:
            model_score = self.get_model_score(feedback['evaluation_id'])
            if abs(model_score - feedback['human_score']) > self.correction_threshold:
                divergences.append({
                    'evaluation_id': feedback['evaluation_id'],
                    'model_score': model_score,
                    'human_score': feedback['human_score'],
                    'comment': feedback['comment']
                })
        
        # 识别系统性偏差
        analysis = self._identify_bias_pattern(divergences)
        return analysis
    
    def optimize_prompt(self) -> str:
        """基于反馈优化Prompt"""
        analysis = self.analyze_divergence()
        
        # 生成Prompt优化建议
        optimizations = []
        if analysis['bias_towards_completeness']:
            optimizations.append("降低完整性权重，增加准确性说明")
        if analysis['misses_compliance_issues']:
            optimizations.append("增加合规性检查示例")
        
        return self._generate_optimized_prompt(optimizations)
```

---

## 常见陷阱与规避

### 陷阱1: 评分维度过多

**问题**: 维度过多导致评分不稳定、成本高
**解决**: 初始使用3-4个核心维度，逐步扩展

### 陷阱2: Prompt不稳定

**问题**: 同一输出多次评分结果不一致
**解决**: 
- 降低temperature (0.1-0.2)
- 使用Few-shot示例
- 多次采样取平均

### 陷阱3: 模型幻觉

**问题**: LLM Judge产生错误评分理由
**解决**:
- 增加事实验证步骤
- 限制评分理由必须与输出内容相关
- 人工抽检验证

### 陷阱4: 权重不合理

**问题**: 权重设置导致评分与实际质量不符
**解决**:
- 收集人工评分，反向优化权重
- 使用A/B测试验证权重配置
- 动态权重调整

---

## 参考资源

### 开源框架
- [OpenAI Evals](https://github.com/openai/evals) - 官方评估框架
- [DeepEval](https://github.com/confident-ai/deepeval) - 企业级评估框架
- [RAGAS](https://github.com/explodinggradients/ragas) - RAG系统评估
- [Promptfoo](https://github.com/promptfoo/promptfoo) - Prompt测试工具

### 学术论文
- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) - LLM评判者系统性分析
- [A Survey on Evaluation of LLMs](https://arxiv.org/abs/2307.03109) - LLM评估综述
- [LM vs LM](https://arxiv.org/abs/2309.04269) - LLM互评机制

### 行业实践
- [OpenAI: How we evaluate language models](https://openai.com/research/how-we-evaluate-language-models)
- [Anthropic: Constitutional AI](https://www.anthropic.com/news/constitutional-ai)
- [Google: Model Cards](https://modelcards.withgoogle.com/)

---

**维护者**: 尼克·弗瑞  
**最后更新**: 2026-04-21  
**状态**: 📝 持续更新
