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
├── CODE_EXAMPLES_EVALUATION.md        ← 代码样例评价体系
├── skills/                           ← 🆕 Skill评价
│   └── SKILL_EVALUATION.md            ← Skill四维评价模型
├── concepts/                          ← 从Insights转化
│   ├── subagent-patterns/
│   ├── multi-agent-routing/
│   ├── graph-memory/
│   ├── context-management/
│   └── harness-engineering/
├── products/                          ← Tony贡献
└── backend/                          ← Zhongli贡献
```

---

## 核心理念

> **"知道某事理论上可行 ≠ 亲眼见过它实现"** — Simon Willison

| 知识类型 | 价值 | 示例 |
|----------|------|------|
| 理论知识 | 知道可能性边界 | Architecture文档 |
| **运行代码** | **具体实现参考** | **可运行的Python脚本** |
| 组合模式 | 多示例组合成新方案 | Prompt模板 |

---

## 质量评价体系

### Code Examples六维模型

详见: [CODE_EXAMPLES_EVALUATION.md](CODE_EXAMPLES_EVALUATION.md)

| 维度 | 权重 |
|:---|:---:|
| 可运行性 | 25% |
| 可读性 | 20% |
| 可复用性 | 20% |
| 文档完整性 | 15% |
| 来源可靠性 | 10% |
| 组合价值 | 10% |

**入库阈值**: ≥60分

### Skill四维模型

详见: [skills/SKILL_EVALUATION.md](skills/SKILL_EVALUATION.md)

| 维度 | 权重 |
|:---|:---:|
| 完整性 | 30% |
| 可用性 | 25% |
| 规范性 | 25% |
| 有效性 | 20% |

**入库阈值**: ≥60分

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
| ✅ SKILL.md | 主文件完整 |
| ✅ 触发条件 | 清晰描述 |
| ✅ 执行流程 | 步骤明确 |
| ✅ 输出格式 | 有说明 |

---

*维护者: 尼克·弗瑞*
*最后更新: 2026-04-30*
