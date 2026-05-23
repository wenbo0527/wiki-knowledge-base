# Skill Benchmark 评估系统

> **版本**: v1.0
> **日期**: 2026-05-22
> **制定者**: 派蒙（大总管）
> **方法论来源**: Anthropic skill-creator

---

## 一、系统概述

基于 Anthropic skill-creator 方法论，建立标准化 Skill 评估体系。

### 核心目标

| 目标 | 说明 |
|:-----|:-----|
| **可量化** | 用 pass_rate/time/tokens 三维指标评估 |
| **可对比** | with-skill vs baseline 对比 |
| **可迭代** | 持续改进，追踪历史版本 |

---

## 二、评估流程

### 2.1 环形迭代模型

```
创建/更新 Skill → 编写测试用例 → 运行测试（with vs without）
       ↑                                              ↓
       ← ← ← ← 评估结果 → 改进 → 重复直到满意 ← ← ←
```

### 2.2 测试流程

| 步骤 | 动作 | 产出 |
|:-----|:-----|:-----|
| 1 | 编写测试用例（evals.json） | `skills/<name>/evals/evals.json` |
| 2 | 同时启动 with-skill 和 baseline subagent | 运行中 |
| 3 | 捕获 timing.json（tokens/duration） | `timing.json` |
| 4 | Grader 评分（grading.json） | `grading.json` |
| 5 | 聚合 benchmark.json | `benchmark.json` |
| 6 | 分析结果（analyzer） | 分析报告 |

---

## 三、数据格式规范

### 3.1 evals.json（测试用例定义）

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": [],
      "expectations": [
        "The output includes X",
        "The skill used script Y"
      ]
    }
  ]
}
```

### 3.2 timing.json（运行时数据）

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z"
}
```

### 3.3 grading.json（评分结果）

```json
{
  "expectations": [
    {
      "text": "The output includes the name 'John Smith'",
      "passed": true,
      "evidence": "Found in transcript Step 3: 'Extracted names: John Smith'"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  },
  "execution_metrics": {
    "tool_calls": {"Read": 5, "Write": 2, "Bash": 8},
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  }
}
```

### 3.4 benchmark.json（聚合结果）

```json
{
  "metadata": {
    "skill_name": "pdf",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0},
      "tokens": {"mean": 3800, "stddev": 400, "min": 3200, "max": 4100}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0},
      "tokens": {"mean": 2100, "stddev": 300, "min": 1800, "max": 2500}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  }
}
```

---

## 四、目录结构

```
skills/
├── <skill-name>/
│   ├── SKILL.md
│   ├── evals/
│   │   └── evals.json          # 测试用例
│   └── references/
│       └── schemas.md          # 辅助文档

benchmarks/
└── <skill-name>/
    └── <timestamp>/
        ├── benchmark.json       # 聚合结果
        └── eval-1/
            ├── with_skill/
            │   ├── run-1/
            │   │   ├── grading.json
            │   │   └── timing.json
            │   └── run-2/
            └── without_skill/
                └── run-1/
                    └── grading.json
```

---

## 五、评分标准

### 5.1 三维指标

| 指标 | 说明 | 重要性 |
|:-----|:-----|:-------|
| **pass_rate** | 通过率（通过数/总数） | ⭐⭐⭐⭐⭐ |
| **time_seconds** | 执行时间 | ⭐⭐⭐ |
| **tokens** | Token 消耗 | ⭐⭐ |

### 5.2 等级划分

| Grade | Pass Rate | 说明 |
|:------|:---------:|:-----|
| 🏆 A+ | 95-100% | Elite performance |
| ✅ A | 85-94% | Excellent |
| 👍 B | 70-84% | Good |
| ⚠️ C | 50-69% | Needs work |
| ❌ D | <50% | Broken |

### 5.3 Delta 解读

| Delta | 解读 |
|:-------|:-----|
| pass_rate > +0.2 | Skill 效果显著 |
| pass_rate 0~+0.2 | Skill 效果有限 |
| pass_rate < 0 | Skill 可能有害 |

---

## 六、执行指南

### 6.1 创建测试用例

1. 分析 Skill 的核心功能
2. 设计 2-3 个真实场景测试
3. 明确 expected_output 和 expectations
4. 保存到 `evals/evals.json`

### 6.2 运行测试

```bash
# 同时启动 with-skill 和 baseline
sessions_spawn --task "执行测试..." --runtime subagent
sessions_spawn --task "执行基线..." --runtime subagent
```

### 6.3 评分

使用 Grader agent 读取 transcript 和 outputs，输出 grading.json。

### 6.4 聚合

运行 `aggregate_benchmark.py` 生成 benchmark.json。

---

## 七、改进建议分类

| Category | 说明 |
|:---------|:-----|
| `instructions` | 技能指令改进 |
| `tools` | 脚本/工具添加或修改 |
| `examples` | 示例补充 |
| `error_handling` | 错误处理指导 |
| `structure` | 内容结构重组 |

---

## 八、注意事项

### 8.1 测试用例设计原则

- 客观可验证：断言必须能验证
- 有区分度：能区分 skill 好坏
- 真实场景：模拟实际使用

### 8.2 Grader 评分标准

**PASS**: 有明确证据，且反映实质性完成  
**FAIL**: 无证据/证据矛盾/表面合规但实际未完成  
**存疑**: 举证责任在通过方

### 8.3 分析器关注点

- 总是通过的断言（无区分度）
- 高方差测试（不稳定）
- with-skill 反而更差的异常情况

---

## 九、与现有系统的关系

| 组件 | 来源 | 用途 |
|:-----|:-----|:-----|
| **evals.json** | Anthropic 标准 | 测试用例格式 |
| **grading.json** | Anthropic 标准 | 评分结果 |
| **benchmark.json** | Anthropic 标准 | 聚合结果 |
| **skillbench** | 自建 | CLI 工具 |
| **agent-task-board** | 自建 | 任务管理 |

---

## 十、后续计划

| 阶段 | 内容 | 负责人 |
|:-----|:-----|:-------|
| Phase3 | 制定各 Skill 的 evals.json | Tony/Nick |
| Phase3 | 配置 Cron 自动跑 benchmark | Tony |
| Phase4 | 建立测试用例模板 | Nick |
| Phase4 | 自动回归测试 | Tony |

---

*版本: v1.0 | 更新: 2026-05-22*
*参考: Anthropic skill-creator 方法论*