---
title: README
author: 尼克·弗瑞 🕵️
product_domain: PD-CODE
doc_type: 其他
tags: [code-examples]
date: 2026-04-30
---

# Code Examples - 代码示例库

> 🕵️ 尼克·弗瑞知识资产管理
> 📅 创建时间: 2026-04-30
> 🎯 定位: "运行代码 > 理论知识" - Simon Willison

---

## 目录结构

```
code-examples/
├── README.md                          ← 本文件
├── CODE_EXAMPLES_STANDARDS.md         ← 准入标准
├── CODE_EXAMPLES_EVALUATION.md        ← 🆕 v2.0 质量评价体系
├── skills/                           ← 🆕 Skill评价
│   ├── SKILL_EVALUATION.md           ← 四维评价（自动化/使用/独特/评估）
│   ├── SKILL_BEST_PRACTICES.md       ← 🆕 mgechev最佳实践
│   └── SKILL_INTEGRATION_ANALYSIS.md ← Skill整合分析
├── concepts/                          ← 从Insights转化
├── products/                          ← Tony贡献
└── backend/                          ← Zhongli贡献
```

---

## 质量评价体系

### Code Examples 六维模型

| 维度 | 权重 |
|:---|:---:|
| 可运行性 | 25% |
| 可读性 | 20% |
| 可复用性 | 20% |
| 文档完整性 | 15% |
| 来源可靠性 | 10% |
| 组合价值 | 10% |

### Skill 四维模型 v2.0

| 维度 | 问题 | 权重 |
|:---|:---|:---:|
| 能自动化 | 这个Skill能自动执行吗？ | 25% |
| 有人使用 | 最近30天被调用过几次？ | 25% |
| 功能独特 | 有其他Skill替代吗？ | 25% |
| 持续评估 | 能定期复审优化吗？ | 25% |

---

## mgechev最佳实践

详见: [skills/SKILL_BEST_PRACTICES.md](skills/SKILL_BEST_PRACTICES.md)

| 原则 | 说明 |
|:---|:---|
| SKILL.md < 500行 | 保持精简 |
| 渐进式披露 | 案例移至references/ |
| 触发词优化 | Use when + Don't use for |
| scripts/确定性 | 重复操作脚本化 |

---

## 准入标准

### Code Examples准入

| 准入条件 | 说明 |
|----------|------|
| ✅ 可运行 | 有完整的依赖声明和main函数 |
| ✅ 有来源 | 标注来源Insight |
| ✅ 最小化 | 聚焦单一概念，≤300行 |
| ✅ 自文档化 | 有清晰注释和README |
| ✅ 有输出示例 | 展示运行效果 |

### Skill准入

| 准入条件 | 说明 |
|----------|------|
| ✅ SKILL.md < 500行 | 保持精简 |
| ✅ 触发词优化 | 包含正例+反例 |
| ✅ references/案例 | 案例移至目录 |
| ✅ 目录结构 | 符合规范 |

---

*维护者: 尼克·弗瑞*
*最后更新: 2026-04-30*
