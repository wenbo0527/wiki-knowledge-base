# Everything Claude Code (ECC) 项目研究报告
能力框架: capability-tech-understanding #capability-risk-control

> **来源**: GitHub - affaan-m/everything-claude-code
> **Stars**: 168,867（全球最高Star的Claude Code项目）
> **Fork数**: 26,174
> **评级**: ⭐⭐⭐⭐⭐ (5/5)
> **标签**: #Claude Code #Skills #Agent #Harness #性能优化 #Anthropic Hackathon Winner

---

## 一、项目概览

### 基本信息

| 维度 | 数据 |
|------|------|
| **Stars** | 168,867 |
| **Fork数** | 26,174 |
| **语言** | JavaScript/TypeScript |
| **贡献者** | 170+ |
| **语言生态** | 12+ (TS, Python, Go, Java, C++, Rust, Perl等) |
| **荣誉** | Anthropic Hackathon Winner |

### 核心定位

> **The performance optimization system for AI agent harnesses.**

ECC不仅是一套配置，而是一个**完整系统**：
- Skills（技能）
- Instincts（本能）
- Memory optimization（记忆优化）
- Security scanning（安全扫描）
- Research-first development（研究驱动开发）

### 跨平台支持

- **Claude Code** ✅
- **Codex** (OpenAI)
- **Cursor**
- **OpenCode**
- **Gemini**
- **其他AI Agent Harnesses**

---

## 二、核心架构

### 2.1 三大核心系统

```
┌─────────────────────────────────────────────────────────────┐
│                    Everything Claude Code                    │
├─────────────────────────────────────────────────────────────┤
│  Agents (48个)                                              │
│  └── 专业角色：架构师、代码审查员、安全专家、性能优化师等      │
├─────────────────────────────────────────────────────────────┤
│  Skills (183个)                                             │
│  └── 可组合技能单元：agentic-engineering, security等        │
├─────────────────────────────────────────────────────────────┤
│  Commands (79个命令)                                        │
│  └── slash commands: /plan, /security-scan, /multi-*      │
├─────────────────────────────────────────────────────────────┤
│  Hooks (钩子系统)                                           │
│  └── SessionStart, Stop, BeforeMsg等生命周期钩子            │
├─────────────────────────────────────────────────────────────┤
│  Rules (多语言规则)                                         │
│  └── common/, typescript/, python/, golang/等              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Agents (48个专业角色)

| Agent | 用途 |
|-------|------|
| **planner.md** | 复杂功能的专家规划 |
| **architect.md** | 架构设计 |
| **code-reviewer.md** | 代码审查 |
| **security-reviewer.md** | 安全审查 |
| **performance-optimizer.md** | 性能优化 |
| **tdd-guide.md** | TDD指导 |
| **harness-optimizer.md** | Harness优化 |
| **silent-failure-hunter.md** | 静默失败追踪 |
| **e2e-runner.md** | 端到端测试 |
| **refactor-cleaner.md** | 重构清洁 |
| **docs-lookup.md** | 文档查询 |
| **loop-operator.md** | 循环操作 |

**按语言分类的Reviewer**：
- TypeScript, Python, Go, Java, C++, Rust, Dart, Flutter, C#, Kotlin

### 2.3 Skills (183个技能)

**技能分类示例**：

| 分类 | 包含技能 |
|------|----------|
| **Agent工程** | agentic-engineering, autonomous-agent-harness, autonomous-loops |
| **代码质量** | ai-regression-testing, agent-eval, benchmark |
| **安全** | agent-payment-x402, opensource-sanitizer |
| **后端** | backend-patterns, api-design, api-connector-builder |
| **前端** | accessibility, browser-qa, click-path-audit |
| **DevOps** | automation-audit-ops, canary-watch, carrier-relationship-management |
| **内容** | article-writing, brand-voice, content-hash-cache-pattern |
| **特定框架** | nestjs-patterns, pytorch-patterns, django-patterns |

---

## 三、核心功能详解

### 3.1 Agentic Engineering Skill

**核心理念**：AI Agent执行大部分实现工作，人类负责质量和风险控制。

**操作原则**：
1. 执行前定义完成标准
2. 将工作分解为Agent-sized单元
3. 按任务复杂度路由模型层级
4. 用evals和回归检查测量

**15分钟单元规则**：
- 每个单元应可独立验证
- 每个单元应有单一主要风险
- 每个单元应有清晰的完成条件

**模型路由策略**：
- **Haiku**: 分类、样板转换、窄范围编辑
- **Sonnet**: 实现和重构
- **Opus**: 架构、根本原因分析、多文件不变量

### 3.2 Memory Persistence

ECC的Hook系统支持跨会话自动保存/加载上下文。

### 3.3 Continuous Learning

从会话中自动提取模式，转化为可复用Skills。

### 3.4 Security Scanning

AgentShield集成，1282测试，102规则。

### 3.5 Multi-Agent Orchestration

PM2支持的复杂多服务工作流：
- `/multi-plan` - 多任务规划
- `/multi-execute` - 并行执行
- `/multi-backend` - 后端服务
- `/multi-frontend` - 前端服务
- `/multi-workflow` - 工作流编排

---

## 四、版本演进

| 版本 | 主要更新 |
|------|----------|
| **v1.10.0** (Apr 2026) | Dashboard GUI、Operator workflows、ECC 2.0 Alpha |
| **v1.9.0** (Mar 2026) | 选择性安装、6新语言支持、SQLite状态存储 |
| **v1.8.0** (Mar 2026) | Harness性能系统、Hook可靠性重构 |
| **v1.7.0** (Feb 2026) | Codex支持、演示构建器、5新业务技能 |
| **v1.6.0** (Feb 2026) | Codex CLI、AgentShield、GitHub Marketplace |
| **v1.4.0** (Feb 2026) | 多语言规则、PM2支持、安装向导 |
| **v1.3.0** (Feb 2026) | OpenCode插件支持 |

---

## 五、安装方式

### 方式1：Plugin安装（推荐）

```bash
# 添加marketplace
/plugin marketplace add https://github.com/affaan-m/everything-claude-code

# 安装plugin
/plugin install everything-claude-code@everything-claude-code
```

### 方式2：手动安装

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
npm install
./install.sh --profile full
```

### Dashboard GUI

```bash
npm run dashboard
# 或
python3 ./ecc_dashboard.py
```

---

## 六、与OpenClaw的对比

| 维度 | Everything Claude Code | OpenClaw |
|------|----------------------|----------|
| **定位** | Claude Code性能优化系统 | 通用AI助手 |
| **Skills数量** | 183+ | 20+ (ClawHub) |
| **Agents数量** | 48+ | 3 (当前配置) |
| **生态** | Claude Code专用 | 通用多Agent协作 |
| **复杂度** | 高（面向专业用户） | 中（面向普通用户） |
| **Hackathon Winner** | ✅ Anthropic | - |

---

## 七、关键洞察

### 7.1 ECC的成功要素

1. **生态完整性**: 不仅仅是配置，是涵盖Agents、Skills、Hooks、Rules、Commands的完整系统
2. **多语言支持**: 12+语言生态，覆盖大多数主流编程语言
3. **性能导向**: 明确的Token优化、模型路由、成本控制机制
4. **持续进化**: 10+月密集迭代，每周都有新版本
5. **社区驱动**: 170+贡献者，21K+ forks

### 7.2 可借鉴的设计

| ECC设计 | 借鉴到OpenClaw |
|---------|----------------|
| Agent角色分工 | ✅ 多Agent专业分工 |
| Skill模块化 | ✅ ClawHub技能市场 |
| Hooks生命周期 | ⏳ 待开发 |
| ELO系统 | ⏳ 待开发 |
| Model routing | ⏳ 待开发 |

### 7.3 ECC不擅长的

1. **通用助手场景** - ECC是Claude Code专用
2. **多Agent协作** - 单Agent优化为主
3. **跨平台统一体验** - 主要面向Claude Code

---

## 八、结论

**Everything Claude Code是全球最好的Claude Code性能优化系统**：
- 168k Stars证明其价值
- Anthropic Hackathon Winner认证
- 183 Skills + 48 Agents的完整生态

**对OpenClaw的启示**：
- Skills和Agents的专业分工值得借鉴
- 但OpenClaw的通用多Agent协作定位不同
- 可以在Skills生态建设上学习ECC的模块化思路

---

## 九、相关链接

- [GitHub仓库](https://github.com/affaan-m/everything-claude-code)
- [ECC Dashboard](https://github.com/marketplace/ecc-tools)
- [ECC 2.0 (Rust)](https://github.com/affaan-m/everything-claude-code/tree/main/ecc2)

---

*整理自 GitHub 项目研究*
*最后更新：2026-04-28*
