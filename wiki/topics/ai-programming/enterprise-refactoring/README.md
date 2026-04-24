# 企业中后台项目重构最佳实践

> 🕵️ 情报来源：Cursor-Windsurf-Mastery-Handbook + 行业实践
> 📅 整理时间：2026-04-14
> 📊 情报价值：⭐⭐⭐⭐⭐（5/5）

---

## 一、核心框架：AI作为监督下的初级工程师

> **核心理念**：AI operates at the level of a competent L3 engineer who requires architecture guidance, security constraints, and systematic code review.

| 原则 | 说明 |
|------|------|
| **AI作为监督下的初级工程师** | 需要架构指导、安全约束和系统化代码审查 |
| **加速但不产生债务** | 速度提升不能损害类型安全、认证逻辑、数据完整性、合规要求 |
| **人工必审** | AI生成的代码是"建议代码"，不是"生产代码"，合并决策权专属于人类 |

---

## 二、重构策略分类

### 1. Brownfield项目（存量系统重构）

| 阶段 | 说明 | 关键产出 |
|------|------|----------|
| **Context Boundary** | 定义AI能看什么、不能改什么 | `.ai-context`, `.ai-readonly` |
| **Constraint Declaration** | 声明约束规则 | `.cursorrules`, `ARCHITECTURE.md` |
| **Controlled Generation** | 受控生成 | 代码 + 审查清单 |
| **Verification & Merge** | 验证与合并 | 测试报告 + 安全扫描 |

### 2. 大规模重构策略（Large Scale Refactoring）

**关键原则**：
- 每次重构必须有明确的验证点
- 禁止一次性大规模修改
- AI辅助的微调优于手动全面重写

**分层重构路径**：

```
┌─────────────────────────────────────────────────────┐
│ 1. 安全边界层（Security Boundary）                  │
│    - 定义 .ai-readonly 区域                         │
│    - 安全相关代码禁止AI修改                          │
├─────────────────────────────────────────────────────┤
│ 2. 架构约束层（Architecture Constraints）            │
│    - .cursorrules 约束                             │
│    - Hexagonal architecture 规则                   │
├─────────────────────────────────────────────────────┤
│ 3. 业务逻辑层（Business Logic）                     │
│    - 最小改动单元                                   │
│    - 每个改动 < 500行                               │
├─────────────────────────────────────────────────────┤
│ 4. 代码清理层（Code Cleanup）                       │
│    - 注释、格式化、死代码删除                        │
│    - 可由AI主导                                     │
└─────────────────────────────────────────────────────┘
```

---

## 三、安全边界定义

### .ai-readonly 关键区域

```bash
# 安全相关的核心模块 - 禁止AI修改
src/core/auth/**
src/middleware/auth.ts
database/migrations/**

# 支付相关 - 需要双重审批
src/modules/payments/**
src/services/payment/**
```

### .cursorrules 安全约束示例

```markdown
## Security Boundaries
- Never generate authentication logic
- Never write SQL without parameterization
- Never expose internal IDs in API responses
- Never modify .ai-readonly files

## Architecture Constraints
- All services must implement IService interface
- All database access through repository pattern
- All external calls through circuit breaker
- Domain layer has no HTTP imports
```

---

## 四、AI辅助重构工作流

### 标准流程

```
┌─────────────────────────────────────────────────────┐
│ Phase 1: Context Boundary Definition (5-10 min)     │
│ ├── 定义AI能看到的文件范围                           │
│ └── 定义AI不能修改的区域                             │
├─────────────────────────────────────────────────────┤
│ Phase 2: Constraint Declaration (10-15 min)         │
│ ├── 创建 .cursorrules                              │
│ └── 定义架构约束和模式                               │
├─────────────────────────────────────────────────────┤
│ Phase 3: Controlled Generation (30-60 min)          │
│ ├── 分步骤执行重构                                   │
│ ├── 每步验证后再下一步                               │
│ └── 记录每个变更                                     │
├─────────────────────────────────────────────────────┤
│ Phase 4: Verification & Merge (15-30 min)           │
│ ├── 静态分析: npm run lint                         │
│ ├── 安全扫描: npm audit / snyk test                 │
│ ├── 测试覆盖: npm run test:coverage                 │
│ └── 代码审查: git diff                              │
└─────────────────────────────────────────────────────┘
```

### 重构Prompt模板

**Weak Prompt**:
```
"Refactor UserProfile.tsx to use hooks"
```

**Strong Prompt**:
```markdown
## Context
File: src/components/UserProfile.tsx
Dependencies: React 18, TypeScript 5, React Query
State management: Zustand

## Intent
Convert UserProfile from class to functional component.

## Requirements
1. Replace componentDidMount with useEffect
2. Replace this.state with useState
3. Preserve all existing functionality

## Constraints
1. BACKWARD COMPATIBILITY: Props interface must remain identical
2. PATTERNS: Use custom hooks for complex logic
3. TYPES: No `any` types

## Validation
1. Run existing test suite
2. Check bundle size (should not increase >5%)
3. Verify no console warnings
```

---

## 五、后端重构最佳实践

### 1. 分层架构约束

| 层级 | 约束 | 示例 |
|------|------|------|
| Domain | 无HTTP/外部依赖 | `User.java`, `Order.java` |
| Application | 依赖Domain | `UserService.java` |
| Infrastructure | 实现接口 | `UserRepository.java` |
| API | 调用Application | `UserController.java` |

### 2. 数据库重构原则

- 所有SQL必须参数化
- 使用Repository Pattern封装数据访问
- 禁止在业务逻辑层直接写SQL
- 迁移脚本必须经过审批

### 3. API重构检查清单

```bash
□ 认证/授权逻辑未改变
□ 参数化查询（防止SQL注入）
□ 响应中无内部ID暴露
□ 错误处理符合现有模式
□ 日志中无敏感数据
□ 事务边界正确
□ 幂等性保证
```

---

## 六、失败模式与规避

| 失败模式 | 场景 | 规避方法 |
|----------|------|----------|
| **Silent Logic Replacement** | AI"优化"认证检查，移除数据库调用 | `.ai-readonly` + 安全回归测试 |
| **Dependency Injection Attack** | AI添加恶意依赖库 | 锁文件 + 签名验证 + 安全审查 |
| **Architectural Drift** | 50个AI-PR逐步破坏架构 | 月度架构审查 + 自动化架构测试 |
| **Hallucinated Security** | AI生成有逻辑漏洞的安全代码 | 安全单元测试 + 渗透测试 |

---

## 七、团队协作模式

### Git提交规范

```bash
git commit --author="Human <human@company.com>" \
  -m "feat: payment refund endpoint

AI-Assisted: yes
AI-Tool: Cursor
AI-Percentage: 60%
Reviewed-By: [engineer name]"
```

### 人工审批节点

| 变更类型 | 审批要求 |
|----------|----------|
| 安全相关代码 | 安全团队 + 技术负责人双重审批 |
| 数据库Schema变更 | DBA审批 |
| API接口变更 | API评审委员会 |
| 配置文件变更 | 技术负责人审批 |
| 业务逻辑变更 | 同行代码审查 |

---

## 八、工具链推荐

| 类别 | 工具 |
|------|------|
| AI编辑器 | Cursor, Windsurf, Claude Code |
| 架构验证 | dependency-cruiser, archUnit |
| 安全扫描 | snyk, npm audit, SonarQube |
| 测试覆盖 | Jest, Pytest, JUnit |
| CI/CD | GitHub Actions, Jenkins |

---

## 九、关联资源

- [Cursor-Windsurf-Mastery-Handbook](https://github.com/hamodywe/Cursor-Windsurf-Mastery-Handbook)
- [[../vibe-coding/README]] - Vibe Coding专题
- [[../superpowers-framework]] - Superpowers工作流

## 子专题文件

- [[enterprise-refactoring/brownfield-projects]] - Brownfield项目重构
- [[enterprise-refactoring/clean-architecture]] - Clean Architecture设计模式
- [[enterprise-refactoring/security-coding]] - 安全编码实践

---

## 十、情报来源

> 本专题内容整理自：
> - **Cursor-Windsurf-Mastery-Handbook** - 企业级AI辅助开发手册
> - 包含31个章节，覆盖Brownfield项目、大规模重构、安全编码等核心主题

---

*🕵️ 情报分析师：尼克·弗瑞*
*最后更新：2026-04-16*
