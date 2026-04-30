# 📚 Skill最佳实践指南

> **来源**: mgechev/skills-best-practices (1,861 stars)
> **整理时间**: 2026-04-30
> **分析师**: 尼克·弗瑞 🕵️

---

## 核心参考

- **GitHub**: https://github.com/mgechev/skills-best-practices
- **作者**: Minko Gechev (Angular Team)
- **许可**: MIT

---

## 一、Skill结构规范

### 1.1 标准目录结构

```
skill-name/
├── SKILL.md              ← 必需：元数据+核心指令（<500行）
├── scripts/              ← 可执行脚本（Python/Bash）
├── references/           ← 补充上下文（案例/模板）
│   ├── case-1.md        ← 案例1
│   ├── case-2.md        ← 案例2
│   └── schema.md         ← 数据schema
└── assets/              ← 输出模板/静态文件
```

### 1.2 目录职责

| 目录 | 职责 | 原则 |
|------|------|------|
| **SKILL.md** | 大脑，导航+核心流程 | <500行，按需引用 |
| **scripts/** | 确定性重复操作 | 避免每次让LLM写重复代码 |
| **references/** | 案例/模板/数据schema | 一级深度，不过深嵌套 |
| **assets/** | 输出模板/JSON Schema | 按需加载 |

---

## 二、SKILL.md编写规范

### 2.1 核心原则

| 原则 | 说明 | 我们的现状 |
|------|------|----------|
| **<500行** | 保持精简，避免上下文污染 | ⚠️ 部分Skill超过 |
| **渐进式披露** | 按需加载，不过早暴露细节 | ⚠️ 需要优化 |
| **第三人人称命令** | "Execute..."而非"I will..." | ⚠️ 需要检查 |
| **确定性scripts/** | 把重复操作脚本化 | ✅ 已有部分实现 |

### 2.2 Frontmatter规范

```yaml
---
name: skill-name                    # 必需：1-64字符，小写+连字符
description: >                     # 必需：<=1024字符
  一句话描述能力。
  Use when: 触发场景...
  Don't use for: 不适用场景...
---
```

### 2.3 触发词优化

```yaml
# ❌ 错误：太模糊
name: react-skills
description: React best practices for agents

# ✅ 正确：具体+正例+反例
name: angular-vite-migrator
description: |
  Migrates Angular CLI projects from Webpack to Vite.
  Use when: user wants to update builder configs, replace webpack plugins,
            speed up Angular compilation.
  Don't use for: React/Vue projects, updating Angular versions only.
```

### 2.4 案例处理方案

**问题**: 如果需要写案例，但SKILL.md要<500行？

**解决方案**: 案例移到references/

```markdown
# SKILL.md - 保持精简

## 执行流程

### Step 1: 解析需求
分析用户需求，识别关键实体。

### Step 2: 验证场景
**必须阅读案例**：
- 典型场景：见 `references/case-typical.md`
- 边界场景：见 `references/case-edge.md`
- 错误处理：见 `references/case-error.md`

### Step 3: 输出结果
按 `references/output-template.md` 格式输出。

---

# references/case-typical.md

## 典型案例：用户说"我要做一个登录功能"

### 用户原始输入
> "我要做一个登录功能，支持手机号和邮箱"

### 解析结果
- Feature: 账号登录
- FP: 手机号登录、邮箱登录、验证码登录
- 菜单: 用户中心/登录

---

# references/output-template.md

## PRD输出模板

```markdown
# PRD: [功能名称]

## 元数据
| 字段 | 值 |
|:---|:---|
| 产品域 | {product_domain} |
...
```
```

---

## 三、验证方法论

### 3.1 Discovery验证

> 测试LLM是否能正确判断触发/不触发

**Prompt模板**:
```
I am building an Agent Skill with this description:

name: {skill-name}
description: {description}

Based strictly on this description:
1. Generate 3 prompts that SHOULD trigger this skill.
2. Generate 3 prompts that should NOT trigger this skill.
3. Critique: Is the description too broad?
```

### 3.2 Logic验证

> 测试逐步指令是否确定性

**Prompt模板**:
```
Here is my SKILL.md and directory structure.

[Paste SKILL.md content]

Act as an autonomous agent. Simulate execution step-by-step.
For each step, write:
1. What exactly are you doing?
2. Which file/script are you reading?
3. Flag any blockers: Where are you forced to guess?
```

### 3.3 Edge Case测试

> 让LLM攻击你的Skill

**Prompt模板**:
```
Switch roles. Act as a ruthless QA tester.
Ask me 3-5 specific questions about:
- Edge cases I didn't handle
- Failure states
- Missing fallbacks

Do not fix yet. Just identify the problems.
```

---

## 四、我们应该做什么

### 4.1 立即行动

| 优先级 | 行动 | 负责人 |
|:---:|:---|:---:|
| P1 | 检查所有SKILL.md是否<500行 | 尼克 |
| P1 | 把案例移到references/ | 贡献者 |
| P2 | 优化触发词description | 贡献者 |
| P2 | 添加正例+反例到触发词 | 贡献者 |

### 4.2 中期目标

| 优先级 | 行动 | 负责人 |
|:---:|:---|:---:|
| P2 | 建立Discovery验证流程 | 派蒙 |
| P3 | 建立Logic验证流程 | 派蒙 |
| P3 | 建立Edge Case测试 | 派蒙 |

### 4.3 评估检查清单

```markdown
## Skill自检清单

□ SKILL.md < 500行
□ description包含Use when + Don't use for
□ 案例移到references/目录
□ scripts/用于确定性任务
□ 目录结构符合规范
□ 触发词通过Discovery验证
□ 步骤通过Logic验证
□ 有Edge Case处理
□ references/不超过一级深度
```

---

## 五、相关资源

| 资源 | URL |
|------|-----|
| mgechev/skills-best-practices | https://github.com/mgechev/skills-best-practices |
| mgechev/skillgrade | https://github.com/mgechev/skillgrade |
| agent-skills-standard | https://github.com/HoangNguyen0403/agent-skills-standard |

---

*整理者: 尼克·弗瑞*
*最后更新: 2026-04-30*
