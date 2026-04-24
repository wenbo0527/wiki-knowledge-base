# Brownfield项目：存量系统重构指南

> 来源：Cursor-Windsurf-Mastery-Handbook
> 整理时间：2026-04-14

---

## 一、什么是Brownfield项目

**Brownfield** = 已有系统 + 需要改造升级的传统架构

与**Greenfield**（从零开始的新项目）相对。

### Brownfield特征

| 特征 | 说明 |
|------|------|
| 遗留代码 | 大量无文档、无测试的遗留代码 |
| 技术债务 | 架构老化、依赖老旧 |
| 业务耦合 | 业务逻辑与基础设施紧耦合 |
| 风险敏感 | 任何改动都可能影响现有功能 |
| 团队惯性 | 成员对现有模式有惯性依赖 |

---

## 二、AI辅助Brownfield项目的工作流

### Phase 1: Context Boundary Definition (5-10分钟)

**目标**：定义AI能看什么、不能改什么

```bash
# 定义AI可以查看的文件范围
echo "src/modules/payments/**" > .ai-context
echo "src/services/**" >> .ai-context
echo "src/repositories/**" >> .ai-context

# 定义AI禁止修改的区域
echo "src/core/auth/**" > .ai-readonly
echo "database/migrations/**" >> .ai-readonly
echo "src/config/**" >> .ai-readonly
```

**关键原则**：
- 安全相关代码必须设为`.ai-readonly`
- 数据库迁移脚本必须人工审批
- 配置文件禁止AI直接修改

---

### Phase 2: Constraint Declaration (10-15分钟)

**目标**：创建`.cursorrules`声明架构约束

```markdown
# .cursorrules

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
- Controllers only handle HTTP, delegate to Application layer

## Code Quality
- No `any` types allowed
- All public methods must have JSDoc
- Error handling must follow existing patterns
- Logging must not include sensitive data

## Testing Requirements
- All new functions require unit tests
- Test coverage must not decrease
- Integration tests for all API endpoints
```

---

### Phase 3: Controlled Generation (30-60分钟)

**核心原则**：小步迭代，每步验证

#### Step 1: 理解现有代码

```
Prompt: "分析 src/services/UserService.ts 的：
1. 主要功能和职责
2. 依赖关系
3. 已知问题或坏味道
4. 测试覆盖情况"
```

#### Step 2: 规划重构单元

```
Prompt: "基于对UserService.ts的分析，
将其拆分为不超过50行的小单元，
每个单元有明确的输入输出和测试点"
```

#### Step 3: 逐单元重构

```
Prompt: "重构第一个单元：extractEmailValidation
要求：
- 创建新文件或修改指定文件
- 保持现有功能不变
- 添加单元测试
- 运行测试验证"
```

#### Step 4: 验证并记录

```bash
# 验证清单
npm run lint
npm run type-check
npm run test -- --testPathPattern="UserService"
npm run test:coverage -- --changedSince=main

# 记录变更
git add .
git commit -m "refactor: extract email validation from UserService

AI-Assisted: yes
AI-Tool: Cursor
AI-Percentage: 70%
Reviewed-By: [name]"
```

---

### Phase 4: Verification & Merge (15-30分钟)

#### 自动化验证

```bash
# 1. 静态分析
npm run lint
npm run type-check

# 2. 安全扫描
npm audit
snyk test

# 3. 测试覆盖
npm run test:coverage -- --changedSince=main

# 4. 架构验证
npx dependency-cruiser --validate .dependency-cruiser.js src/
```

#### 人工审查清单

```markdown
## Code Review Checklist for AI-Generated Changes

### Functionality
- [ ] 原有功能保持不变
- [ ] 新功能符合需求
- [ ] 边界条件处理正确

### Security
- [ ] 无SQL注入风险
- [ ] 无敏感数据泄露
- [ ] 认证授权逻辑未被意外修改

### Architecture
- [ ] 遵循分层架构
- [ ] 无循环依赖
- [ ] 接口定义清晰

### Code Quality
- [ ] 无类型警告
- [ ] 错误处理完善
- [ ] 日志适当（无敏感数据）

### Testing
- [ ] 新增代码有测试
- [ ] 原有测试通过
- [ ] 覆盖率未下降
```

---

## 三、重构策略模式

### 模式1：Extract Method / Function
**场景**：长方法拆解

```typescript
// Before: 100行的processOrder方法

// After: 拆分为
function validateOrder(order: Order): ValidationResult
function calculatePricing(order: Order): PricingResult
function persistOrder(order: Order): Order
function notifyOrderCreated(order: Order): void
```

### 模式2：Introduce Repository
**场景**：数据访问与业务逻辑耦合

```typescript
// Before: Service直接写SQL
async function getUserOrders(userId: string) {
  return await db.query(`SELECT * FROM orders WHERE user_id = ${userId}`);
}

// After: 通过Repository
async function getUserOrders(userId: string) {
  return await this.orderRepository.findByUserId(userId);
}
```

### 模式3：Extract Domain Layer
**场景**：业务逻辑与基础设施紧耦合

```typescript
// Before: Controller直接处理HTTP和DB
async function createUser(req, res) {
  const { name, email } = req.body;
  await db.query('INSERT INTO users...');
  res.json({ success: true });
}

// After: 分层
// Controller: 处理HTTP
// Application Service: 业务编排
// Domain Entity: 纯粹业务逻辑
// Repository: 数据访问
```

### 模式4：Replace Magic Strings with Constants
**场景**：硬编码字符串

```typescript
// Before
if (user.role === 'admin') { ... }

// After
const ROLE_ADMIN = 'admin';
if (user.role === ROLE_ADMIN) { ... }
```

---

## 四、重构优先级矩阵

| 象限 | 价值 | 风险 | 优先级 |
|------|------|------|--------|
| 高价值 + 低风险 | 立即重构 | - | **P0** |
| 高价值 + 高风险 | 计划后重构 | 充分测试 | **P1** |
| 低价值 + 低风险 | 有空时重构 | - | **P2** |
| 低价值 + 高风险 | 不重构 | - | **P3** |

### 重构优先级参考

| 优先级 | 类型 | 示例 |
|--------|------|------|
| **P0** | 无测试的高风险代码 | 支付逻辑、认证模块 |
| **P0** | 频繁变更的代码 | 业务核心模块 |
| **P1** | 技术债务集中区 | 10年+遗留代码 |
| **P1** | 新功能依赖的旧代码 | API Gateway |
| **P2** | 工具类/辅助函数 | 格式化、数据转换 |
| **P3** | 死代码/废弃功能 | 删除优先 |

---

## 五、遗留系统评估框架

### 代码质量维度

| 维度 | 指标 | 阈值 |
|------|------|------|
| 测试覆盖 | 单元测试覆盖率 | > 70% |
| 复杂度 | 平均圈复杂度 | < 10 |
| 耦合度 | Afferent Coupling | 无循环依赖 |
| 内聚度 | LCOM | < 2 |
| 重复率 | 重复代码比例 | < 5% |

### 技术债务评估

```markdown
## 技术债务评估报告

### 模块：OrderManagement
| 债务项 | 类型 | 修复时间 | 影响范围 |
|--------|------|----------|----------|
| 硬编码配置 | 维护性 | 2h | 中 |
| 无事务边界 | 正确性 | 4h | 高 |
| SQL拼接 | 安全性 | 8h | 高 |
| 循环依赖 | 架构 | 16h | 中 |

### 总评估
- 总债务：30 story points
- 建议：分4个sprint逐步偿还
```

---

## 六、最佳实践清单

### 重构前

- [ ] 完整备份现有代码
- [ ] 建立基线测试套件
- [ ] 定义`.ai-readonly`区域
- [ ] 创建`.cursorrules`约束
- [ ] 确定重构单元（每单元<500行）
- [ ] 规划回滚方案

### 重构中

- [ ] 每次改动后运行完整测试
- [ ] 保持CI/CD绿灯
- [ ] 小步提交，每步可回滚
- [ ] 记录所有变更决策
- [ ] 定期同步变更到主干

### 重构后

- [ ] 完整回归测试
- [ ] 性能基准对比
- [ ] 安全扫描通过
- [ ] 文档更新
- [ ] 团队代码审查
- [ ] 监控告警确认

---

## 七、常见问题处理

### Q1: 如何处理无测试的遗留代码？

**策略**：
1. 先用AI生成集成测试（覆盖主要流程）
2. 基于集成测试，添加单元测试
3. 有测试保护后再重构

### Q2: 如何避免重构破坏现有功能？

**策略**：
1. 功能测试驱动：先写功能测试，再重构
2. 特性开关：新旧代码并存，通过开关切换
3. 影子部署：新代码并行运行，对比结果

### Q3: 大规模重构如何控制风险？

**策略**：
1. Strangler Fig模式：用新系统逐步替换旧系统
2. 特性分支：每个重构点一个分支
3. 金丝雀发布：小流量验证后全量

---

*整理：尼克·弗瑞*
*来源：Cursor-Windsurf-Mastery-Handbook*
