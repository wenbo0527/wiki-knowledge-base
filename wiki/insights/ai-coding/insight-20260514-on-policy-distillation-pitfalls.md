---
title: insight 20260514 on policy distillation pitfalls
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-coding]
date: 2026-05-23
---

# On-Policy Distillation 全面研究：陷阱、机制与修复

能力框架: capability-tech-understanding #capability-risk-control
标签: #distillation #LLM #training #arXiv-2026

> **来源**: arXiv:2605.11182
> **分类**: cs.AI (Artificial Intelligence)
> **评级**: ⭐⭐⭐⭐ (4/5)
> **日期**: 2026-05-13
> **作者**: Siqi Zhu, Xuyan Ye et al.
> **Tags**: #tech-understanding #risk-control #distillation

---

## 一、核心问题

### 研究背景

On-policy distillation (OPD) 和 on-policy self-distillation (OPSD) 是 LLMs 后训练的重要方法：
- 提供密集的、token 级的轨迹监督
- 用于系统 prompt 内化和知识迁移

### 现状

现有结果**喜忧参半**：
- ✅ 在系统 prompt 和知识内化上有前景
- ❌ 但也报告了不稳定和性能下降

**核心问题**: OPD/OPSD 什么时候有效？为什么有效（或无效）？

---

## 二、主要发现

### 2.1 OPD 在数学推理上的敏感性

| 因素 | 影响 |
|:---|:---|
| **Teacher 选择** | 高度敏感 |
| **Loss formulation** | 高度敏感 |
| **任务类型** | 数学推理 > 其他任务 |

### 2.2 OPSD 的失效场景

> **OPSD 在测试时缺少实例级特权信息（PI）时会失败。**

| PI 类型 | OPSD 效果 |
|:---|:---|
| **Instance-specific PI**（如数学推理的具体步骤） | ❌ 失效 |
| **Shared latent rule**（如 system prompt、alignment preference） | ✅ 有效 |

---

## 三、三大失败机制

### 机制 1: Distribution Mismatch

**问题**: Teacher 和 Student 条件于 Student 自己生成的前缀时产生分布不匹配。

```
Student 生成的前缀
       ↓
Teacher 条件于此前缀
       ↓
Teacher 分布 ≠ Student 真实分布
       ↓
学习效果下降
```

### 机制 2: Optimization Instability

**问题**: TopK reverse-KL gradients 存在优化不稳定性。

- TopK 操作引入了非平滑梯度
- 导致训练不稳定

### 机制 3: OPSD 特异性限制

**问题**: Student 学习了一个"聚合 PI 条件 Teacher 的 PI-free 策略"。

- 当 PI 是 instance-specific 时不够用
- Student 无法区分不同实例需要不同的 PI

---

## 四、修复方案

| 机制 | 修复方案 |
|:---|:---|
| **Distribution Mismatch** | Stop-gradient TopK objectives |
| **Optimization Instability** | RLVR-adapted teachers |
| **OPSD Limitation** | SFT-stabilized students |

### 核心建议

```
✅ 做 OPD 时：
   - 选择匹配的 Teacher（不要让 Teacher 条件于 Student 的错误输出）
   - 使用 stop-gradient 防止梯度弥散
   - 用 SFT 稳定 Student 初始阶段

✅ 做 OPSD 时：
   - 确保 PI 是共享规则（如 system prompt）
   - 避免在 instance-specific PI 场景使用
```

---

## 五、实践建议

### 什么时候用 OPD/OPSD？

| 场景 | 推荐 |
|:---|:---|
| System prompt 内化 | ✅ 适合 |
| Alignment preference 迁移 | ✅ 适合 |
| 数学/代码等 instance-specific 任务 | ⚠️ 谨慎，需用修复方案 |
| 知识蒸馏（通用） | ❌ 可能不适合 |

### 检查清单

```
□ 我的任务是 shared rule 还是 instance-specific？
□ Teacher 会不会条件于 Student 的错误输出？
□ 我用了 stop-gradient 吗？
□ Student 初始阶段稳定吗？
```

---

## 六、与其他技术的对比

| 技术 | 适用场景 | 稳定性 | 成本 |
|:---|:---|:---|:---|
| **OPD** | 知识迁移、风格迁移 | 中 | 中 |
| **OPSD** | System prompt、Alignment | 高 | 低 |
| **RLVR** | 偏好优化 | 高 | 高 |
| **SFT** | 基础能力 | 高 | 中 |

---

## 七、认知更新

### 旧认知
- Distillation 是万能的，直接用就行
- OPD/OPSD 效果差不多

### 新认知
- OPD 对 teacher/loss 高度敏感
- OPSD 只适合 shared rule，不适合 instance-specific
- 有明确的失败机制和修复方案

---

*🕵️ 尼克·弗瑞 | 情报分析师*
*来源: arXiv RSS 抓取 | 2026-05-13*
