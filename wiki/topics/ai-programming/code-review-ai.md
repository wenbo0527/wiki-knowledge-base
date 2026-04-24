# AI代码审查工具与实践

> 来源：Cursor-Windsurf-Mastery-Handbook + AI-Pair
> 整理时间：2026-04-14

---

## 一、AI代码审查框架

### 1.1 审查层次模型

```
┌─────────────────────────────────────────────────────────────┐
│                    Human Review（人类终审）                   │
│         - 架构决策      - 安全关键      - 业务逻辑            │
├─────────────────────────────────────────────────────────────┤
│                    AI Deep Review（AI深度审查）               │
│         - 逻辑正确性    - 边界条件      - 性能分析            │
├─────────────────────────────────────────────────────────────┤
│                    AI Quick Review（AI快速审查）             │
│         - 代码风格      - 命名规范      - 简单bug             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 两阶段审查流程

```
Stage 1: AI Self-Review（AI自审）
├── 开发者提交PR
├── AI自动执行代码扫描
├── 生成初步审查报告
└── 标记需要人类关注的问题

Stage 2: Human Review（人类终审）
├── 人类审查关键变更
├── AI辅助问题修复
└── 最终合并决策
```

---

## 二、AI-Pair：异构AI团队协作

> 来源：https://github.com/axtonliu/ai-pair

### 2.1 核心概念

**核心理念**：让不同AI模型组成团队协作。一个创作，两个审查 — 不是为了冗余，而是因为不同模型天然关注不同维度。

```
User (你)
  │
Team Lead (Claude Code)
  |-- creator — 写代码或内容
  |-- codex-reviewer — 分析型审查（bug、安全、性能、边界条件）
  |-- gemini-reviewer — 编辑型审查（架构、设计模式、可维护性）
```

### 2.2 工作流程

1. **你下达任务** → creator执行
2. **Creator回报** → 你决定是否送审
3. **两个审查者并行分析** → 汇总报告
4. **你决定** → 修改还是通过

### 2.3 三种团队模式

| 模式 | 用途 | 角色分工 |
|------|------|----------|
| `dev-team` | 写代码、修bug、重构 | developer + codex-reviewer + gemini-reviewer |
| `content-team` | 写文章、脚本、Newsletter | author + codex-reviewer + gemini-reviewer |
| `team-stop` | 关闭团队 | - |

### 2.4 真实案例

三个AI发现的问题**零重叠**：

- **Claude (Team Lead)**：发现对引用来源的过度解读
- **GPT (Codex)**：拆解论证链，质疑逻辑跳跃
- **Gemini**：建议开头对目标读者来说太学术化

---

## 三、Cursor-Windsurf代码审查最佳实践

### 3.1 审查质量门控

```yaml
# 质量门控清单
quality_gates:
  - name: Static Analysis
    tools: [eslint, typescript]
    fail_on: error
    
  - name: Security Scan
    tools: [npm audit, snyk]
    fail_on: high
    
  - name: Test Coverage
    threshold: 80%
    fail_on: below
    
  - name: Architecture Validation
    tool: dependency-cruiser
    rules: no-circular, layer-compliance
```

### 3.2 审查要点清单

```markdown
## AI生成代码审查清单

### 功能性
- [ ] 代码完成预期功能
- [ ] 边界条件已处理
- [ ] 错误处理适当
- [ ] 日志记录充分

### 安全性
- [ ] 无硬编码凭证
- [ ] 输入验证存在
- [ ] SQL/命令注入防护
- [ ] 敏感数据不泄露

### 性能
- [ ] 无明显N+1查询
- [ ] 适当缓存
- [ ] 索引考虑

### 可维护性
- [ ] 命名清晰
- [ ] 函数短小
- [ ] 单一职责
- [ ] 无重复代码
```

### 3.3 团队协作流程

```
┌─────────────────────────────────────────────────────────────┐
│ PR创建 → AI自动审查 → 人类审查 → 讨论 → 批准/拒绝             │
└─────────────────────────────────────────────────────────────┘

AI审查重点：
├── 代码风格一致性
├── 潜在bug检测
├── 安全漏洞扫描
├── 性能问题识别
└── 测试覆盖度分析
```

---

## 四、企业级代码审查工具链

### 4.1 GitHub AI Autobot Action

> 来源：https://github.com/jon-the-dev/github-ai-autobot-action

**企业级AI代码审查自动化工具**，基于OpenAI GPT和Anthropic Claude。

**核心特性**：
- 支持GPT + Claude双引擎
- 安全扫描（DevSecOps）
- 企业级部署
- 自动问题分类

### 4.2 工具矩阵

| 工具 | 用途 | 适用场景 |
|------|------|----------|
| **GitHub AI Autobot** | 自动PR审查 | 企业团队 |
| **AI-Pair** | 异构AI团队协作 | 需要多视角审查 |
| **Cursor/Windsurf** | IDE内置审查 | 日常开发 |
| **Claude Code** | 智能代码审查 | 复杂逻辑分析 |
| **Codex CLI** | GPT驱动的审查 | 安全/性能分析 |
| **Gemini CLI** | 编辑型审查 | 架构/设计审查 |

---

## 五、AI审查提示词模板

### 5.1 安全审查

```
# 安全审查提示词
请审查以下代码的安全问题：

```代码
[粘贴代码]
```

审查要点：
1. 认证/授权是否正确实现
2. 输入验证是否存在
3. SQL/命令注入风险
4. 敏感数据处理
5. 错误信息是否泄露内部信息

请用以下格式输出：
- 问题描述
- 严重程度（高/中/低）
- 修复建议
```

### 5.2 性能审查

```
# 性能审查提示词
请审查以下代码的性能问题：

```代码
[粘贴代码]
```

审查要点：
1. 数据库查询效率（N+1问题）
2. 循环中的昂贵操作
3. 缓存使用
4. 异步处理
5. 内存泄漏风险

请用以下格式输出：
- 问题位置
- 影响评估
- 优化建议
```

### 5.3 架构审查

```
# 架构审查提示词
请审查以下代码是否符合架构规范：

```代码
[粘贴代码]
```

架构约束：
- 分层架构（Domain/Application/Infrastructure/Presentation）
- 依赖方向（只能外层依赖内层）
- Repository模式
- 无循环依赖

请用以下格式输出：
- 架构违规（如果有）
- 违反原因
- 符合架构的最佳实践
```

---

## 六、持续集成中的AI审查

### 6.1 CI/CD审查流程

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on: [pull_request]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Run AI Code Review
        uses: jon-the-dev/github-ai-autobot-action@v2
        with:
          openai_key: ${{ secrets.OPENAI_API_KEY }}
          anthropic_key: ${{ secrets.ANTHROPIC_API_KEY }}
          review_level: comprehensive
          security_scan: true
          
      - name: Report Results
        run: |
          echo "AI Review completed"
          cat review-report.md
```

### 6.2 审查结果处理

```markdown
## AI审查结果分类

### 🔴 必须修复（Blocker）
- 安全漏洞
- 认证/授权bug
- 数据完整性问题

### 🟡 建议修复（Suggestion）
- 性能优化机会
- 代码可读性改进
- 测试覆盖不足

### 🟢 可选改进（Optional）
- 代码风格建议
- 文档改进
- 命名规范
```

---

## 七、最佳实践总结

| 实践 | 说明 |
|------|------|
| **分层审查** | AI快速扫描 + 人类深度审查 |
| **异构AI协作** | 不同模型关注不同维度 |
| **自动化质量门控** | CI中强制执行 |
| **安全优先** | 安全问题必须修复 |
| **人类终审** | 合并决策权在人类 |
| **迭代改进** | 审查结果反馈到开发流程 |

---

*整理：尼克·弗瑞*
*来源：Cursor-Windsurf-Mastery-Handbook, AI-Pair*
