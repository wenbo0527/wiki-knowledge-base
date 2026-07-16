---
title: insight 20260430 karpathy autoresearch
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-coding]
date: 2026-05-23
---

# Insight: Karpathy Autoresearch - 自主AI研究框架
能力框架: capability-tech-understanding #capability-risk-control

> **来源**: [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
> **发布时间**: 2026-03-06
> **Stars**: 77,873 | **Forks**: 11,359
> **评级**: ⭐⭐⭐⭐⭐ (5/5)
> **标签**: AI-Agent, 自主研究, LLM训练, 自动化实验
> **存储时间**: 2026-04-30

---

## 核心发现

Karpathy的autoresearch是一个**单GPU自动化研究实验框架**，让AI Agent在5分钟内自主完成"修改→训练→验证→保留/丢弃"的循环实验。

### 项目定位
```
AI agents running research on single-GPU nanochat training automatically
```
一句话概括：给AI一个小型但真实的LLM训练环境，让它通宵自主实验。

---

## 项目架构

### 三文件原则（极简设计）

| 文件 | 职责 | 修改权限 |
|------|------|----------|
| `prepare.py` | 固定常量、数据准备、分词器、评估工具 | ❌ 不修改 |
| `train.py` | 模型架构、优化器、训练循环 | ✅ Agent修改 |
| `program.md` | Agent指令规范 | ✅ Human修改 |

### 为什么极简？

> "By design, training runs for a **fixed 5-minute time budget**, regardless of the details of your compute."

- 固定5分钟时间预算
- ~12次实验/小时
- 睡眠8小时可跑~100次实验
- val_bpb越低越好

---

## 核心技术亮点

### 1. 模型架构

```python
# 核心超参
DEPTH = 8               # transformer层数
ASPECT_RATIO = 64       # 模型维度 = depth * 64
HEAD_DIM = 128          # 注意力头维度
WINDOW_PATTERN = "SSSL" # 滑动窗口模式

# 模型维度计算
base_dim = depth * ASPECT_RATIO  # 512
model_dim = 512
num_heads = 4
```

**技术特点**:
- **RMSNorm** 替代 LayerNorm
- **Rotary Embedding** 旋转位置编码
- **GQA (Grouped Query Attention)** 分组查询注意力
- **Value Embedding (ResFormer)**: 每层交替添加值嵌入，带输入依赖门控

### 2. 优化器组合

| 参数类型 | 优化器 | 学习率 |
|----------|--------|--------|
| Token嵌入 | AdamW | 0.6 |
| LM头 | AdamW | 0.004 |
| 矩阵参数 | Muon | 0.04 |
| 标量参数 | AdamW | 0.5 |

**Muon优化器**: 专为矩阵参数设计，配合AdamW用于其他参数。

### 3. 训练策略

```
WARMUP_RATIO = 0.0      # 无预热
WARMDOWN_RATIO = 0.5    # 最后50%时间进行LR衰减
FINAL_LR_FRAC = 0.0     # 最终LR降到0
WEIGHT_DECAY = 0.2      # 谨慎的权重衰减
```

---

## Agent工作流

```
┌─────────────────────────────────────────────────────────────┐
│  LOOP FOREVER:                                              │
│                                                             │
│  1. 读取 train.py 当前状态                                 │
│  2. 修改代码尝试新想法                                      │
│     - 模型架构调整                                         │
│     - 超参数优化                                           │
│     - 优化器配置                                           │
│     - 批量大小                                             │
│  3. git commit                                             │
│  4. 运行: uv run train.py > run.log                        │
│  5. 提取结果: grep "val_bpb:" run.log                     │
│  6. 记录到 results.tsv                                      │
│     - val_bpb↓ → git保留 ("keep")                        │
│     - val_bpb↑ → git回滚 ("discard")                      │
│     - 崩溃 → ("crash")                                     │
│  7. 继续下一轮                                             │
└─────────────────────────────────────────────────────────────┘
```

### Agent行为规范

**能做**:
- 修改train.py的一切（架构/超参/优化器/批量大小）
- 修改program.md

**不能做**:
- 修改prepare.py
- 安装新包或添加依赖
- 修改评估函数evaluate_bpb

### 核心原则

> **简洁性 > 复杂性**
> - 小改进+大复杂度 = 不值得
> - 小改进+删除代码 = 值得保留
> - 无改进+更简单 = 值得保留

---

## 实验日志格式

```tsv
commit     val_bpb    memory_gb  status   description
a1b2c3d    0.997900   44.0       keep     baseline
b2c3d4e    0.993200   44.2       keep     increase LR to 0.04
c3d4e5f    1.005000   44.0       discard  switch to GeLU activation
d4e5f6g    0.000000   0.0        crash    double model width (OOM)
```

---

## 关键设计哲学

| 设计决策 | 原因 | 优势 |
|----------|------|------|
| **固定5分钟预算** | 不同硬件平台可比 | 自动适配GPU性能差异 |
| **单一文件修改** | 降低Agent认知负担 | 保持diff可审查 |
| **val_bpb指标** | 词汇量无关 | 架构变更可公平比较 |
| **禁止安装包** | 防止依赖膨胀 | 环境稳定可复现 |
| **永不停止** | 无人值守运行 | 最大化实验吞吐量 |
| **git分支实验** | 版本控制每次尝试 | 可回溯、可对比 |

---

## 对AI编程的启示

### 1. Program.md作为技能定义

用Markdown定义Agent行为规范，而不是硬编码：

```markdown
# 这个文件是技能定义
## Setup
1. 同意run tag
2. 创建git分支
3. 读取上下文文件
...

## Experimentation
- 能做什么
- 不能做什么
- 目标是什么
```

### 2. 单一修改域原则

```
OpenClaw Agent修改范围:
├── SOUL.md      ← Agent人格定义（不修改）
├── AGENTS.md    ← 工作规范（Human修改）
├── MEMORY.md    ← 记忆系统
├── SKILL.md     ← 技能定义
└── train.py     ← 实际工作域（Agent可改）
```

### 3. 固定时间预算

对我们Agent任务的意义：
- 每个子任务有明确的时间盒
- 任务结果可横向比较
- 避免Agent在某个任务上过度投入

### 4. 简洁性评分

| 情况 | 评估 |
|------|------|
| +0.001改进 + 20行hacky代码 | ❌ 不值得 |
| +0.001改进 - 删除代码 | ✅ 值得 |
| 无改进 - 更简单代码 | ✅ 值得 |

### 5. 无人值守Loop

```
用户: "我去睡觉了，继续跑"
Agent: "好的，我会继续到明天早上"
```

对OpenClaw的意义：定时任务 + Cron机制实现真正的无人值守。

---

## 衍生项目

| 项目 | 平台 | Stars | 说明 |
|------|------|-------|------|
| [autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) | Apple Silicon | 4.1k | Mac MLX移植版，无需PyTorch |
| [autoresearch-macos](https://github.com/miolini/autoresearch-macos) | MacOS | - | Mac原生支持 |
| [autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) | Windows | - | Windows RTX支持 |
| [autoresearch](https://github.com/uditgoenka/autoresearch) | Claude Code | 4.1k | Claude Autoresearch Skill |

---

## 相关资源

- [nanochat](https://github.com/karpathy/nanochat) - 完整版nanochat训练代码
- [Karpathy推文1](https://x.com/karpathy/status/2029701092347630069) - 项目介绍
- [Karpathy推文2](https://x.com/karpathy/status/2031135152349524125) - 详细讨论

---

## 总结

Karpathy的autoresearch展示了**极简主义+自主实验**的力量：

1. **极简架构**: 3个文件，1个可修改域
2. **固定预算**: 5分钟/次，~100次/晚
3. **自主循环**: 修改→验证→保留/丢弃→重复
4. **简洁至上**: 删除代码是好事
5. **无人值守**: 人类睡觉，AI干活

这不仅是LLM训练的研究方法，更是AI Agent工作模式的典范。

---

*分析时间: 2026-04-30*
*分析师: 尼克·弗瑞*
