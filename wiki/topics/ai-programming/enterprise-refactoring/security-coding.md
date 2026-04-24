# AI辅助安全编码实践

> 来源：Cursor-Windsurf-Mastery-Handbook
> 整理时间：2026-04-14

---

## 一、安全风险矩阵

| 风险类别 | 可能性 | 影响 | 缓解措施 |
|----------|--------|------|----------|
| **认证绕过** | 中 | 严重 | `.ai-readonly` 标记关键文件 |
| **SQL注入** | 高 | 严重 | 参数化查询linting |
| **XSS注入** | 高 | 高 | CSP headers + 消毒测试 |
| **代码中的密钥** | 中 | 严重 | 提交前secret扫描 |
| **逻辑炸弹** | 低 | 严重 | 代码审查 + 行为测试 |
| **依赖投毒** | 中 | 严重 | 锁文件 + 签名验证 |

---

## 二、常见失败模式

### 1. Silent Logic Replacement（静默逻辑替换）

**场景**：工程师让AI"优化"认证检查。

**AI行为**：移除昂贵的数据库调用，替换为始终为真的条件。

**结果**：完全认证绕过。

**检测**：
```bash
# 审计安全关键文件变更
git diff main -- src/auth/ src/middleware/auth.ts

# 自动化安全回归测试
npm run test:security-regression
```

**规避**：
- `.ai-readonly` 标记安全文件
- 安全相关变更需要安全团队审批
- 自动化测试："未认证请求返回401"

---

### 2. Dependency Injection Attack（依赖注入攻击）

**场景**：AI建议添加"有用"的日志库。

**AI输出**：`import logger from 'very-helpful-logger'`

**实际**：拼写错误攻击，窃取环境变量。

**检测**：
```bash
# 阻止package.json中的未知依赖
npm install --ignore-scripts
npm audit signatures
```

**规避**：
- 锁文件强制
- 依赖变更需要安全审查
- 仅使用内部artifact registry中的批准包

---

### 3. Architectural Drift（架构漂移）

**场景**：50个AI-PR各自做出"小"架构妥协。

**结果**：系统不再遵循六边形架构，领域逻辑泄漏到控制器。

**检测**：
```bash
# 架构合规测试
npx dependency-cruiser --validate .dependency-cruiser.js src/
```

**规避**：
- AI生成代码月度架构审查
- 自动化架构测试（如"domain层无HTTP导入"）

---

### 4. Hallucinated Security Controls（幻觉安全控制）

**场景**：AI添加看起来正确但有逻辑缺陷的"安全中间件"。

**示例**：
```javascript
// AI生成的代码（有漏洞）
function checkPermission(user, resource) {
  if (user.role === 'admin' || resource.public) {
    return true; // BUG: 应该是 === true
  }
  return false;
}
```

**实际**：`resource.public` 是undefined，类型转换为false，逻辑反转。

**检测**：
- 所有AI生成的安全代码进行渗透测试
- 安全单元测试包含负向案例

---

## 三、安全编码规则

### 1. 认证授权

```typescript
// ❌ 禁止AI生成
function checkAuth(req) {
  return req.headers.authorization !== undefined;
}

// ✅ 正确的模式
function checkAuth(req: Request): AuthResult {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return { authorized: false, reason: 'No token' };
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return { authorized: true, user: decoded };
  } catch {
    return { authorized: false, reason: 'Invalid token' };
  }
}
```

### 2. SQL注入防护

```typescript
// ❌ 禁止：字符串拼接
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 正确：参数化查询
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);

// ✅ 更安全：ORM/Query Builder
const user = await userRepository.findById(userId);
```

### 3. 输入验证

```typescript
// ✅ 始终验证和清理输入
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  name: z.string().min(1).max(100)
});

function createUser(input: unknown) {
  const validated = UserSchema.parse(input); // 抛出ZodError如果无效
  // ... 处理验证后的数据
}
```

### 4. 错误处理

```typescript
// ❌ 禁止：泄露内部信息
catch (error) {
  return { error: error.message, stack: error.stack };
}

// ✅ 正确：通用错误消息
catch (error) {
  logger.error('Payment failed', { error, orderId });
  return { error: 'Payment processing failed. Please try again.' };
}
```

### 5. 日志安全

```typescript
// ❌ 禁止：记录敏感数据
logger.info('User logged in', { password: user.password });

// ✅ 正确：只记录非敏感信息
logger.info('User logged in', { userId: user.id, email: user.email });
```

---

## 四、CI/CD安全门控

### 安全检查清单

```yaml
# .github/workflows/secure-ci.yml
name: Secure CI

on: [push, pull_request]

jobs:
  security-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run linting
        run: npm run lint
        
      - name: Type check
        run: npm run type-check
        
      - name: Security audit
        run: npm audit --audit-level=high
        
      - name: Dependency scanning
        run: snyk test
        
      - name: Secret detection
        run: git传播 --secret-name='API_KEY|SECRET|PASSWORD|TOKEN'
        
      - name: Architecture validation
        run: npx dependency-cruiser --validate .dependency-cruiser.js src/
```

---

## 五、.cursorrules安全模板

```markdown
## 安全边界 (.cursorrules)

### 禁止事项
- 🚫 Never generate authentication logic
- 🚫 Never write SQL without parameterization
- 🚫 Never expose internal IDs in API responses
- 🚫 Never log sensitive data (passwords, tokens, keys)
- 🚫 Never modify .ai-readonly files
- 🚫 Never add dependencies without security review

### 必需事项
- ✅ All database queries must use parameterized statements
- ✅ All user input must be validated using schema validation
- ✅ All errors must return generic messages to clients
- ✅ All external API calls must have timeouts
- ✅ All secrets must come from environment variables

### 审批要求
- 认证/授权代码：安全团队 + 技术负责人
- 数据库Schema变更：DBA
- 依赖添加：安全审查
- API契约变更：API评审委员会
```

---

## 六、AI生成代码审查清单

```markdown
## AI生成代码安全审查

### 认证授权
- [ ] 无硬编码凭证
- [ ] 会话管理安全
- [ ] 权限检查正确

### 输入验证
- [ ] 所有用户输入已验证
- [ ] 类型安全
- [ ] 边界条件处理

### 输出编码
- [ ] 无SQL注入
- [ ] 无XSS漏洞
- [ ] 响应不泄露内部信息

### 错误处理
- [ ] 无堆栈跟踪泄露
- [ ] 日志不含敏感数据
- [ ] 错误消息通用化

### 依赖管理
- [ ] 无新依赖（需审查）
- [ ] 锁文件更新
- [ ] 已知漏洞检查
```

---

*整理：尼克·弗瑞*
*来源：Cursor-Windsurf-Mastery-Handbook*
