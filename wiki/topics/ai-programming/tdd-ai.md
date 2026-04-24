# AI时代的TDD实践

> 来源：Cursor-Windsurf-Mastery-Handbook + Superpowers
> 整理时间：2026-04-14

---

## 一、TDD的演进：从人工到AI驱动

### 1.1 传统TDD vs AI-TDD

| 维度 | 传统TDD | AI-TDD |
|------|---------|---------|
| **测试编写** | 人工逐个编写 | AI批量生成 |
| **测试执行** | 手动运行 | 自动循环 |
| **代码生成** | 人工实现 | AI辅助生成 |
| **重构验证** | 人工检查 | 自动回归 |
| **迭代速度** | 较慢 | 快 |

### 1.2 AI-TDD工作流

```
┌─────────────────────────────────────────────────────────────┐
│                    AI-TDD 工作流                             │
├─────────────────────────────────────────────────────────────┤
│  1. 规格定义（Spec）                                         │
│     ├── 输入：需求描述、用户故事                               │
│     └── 输出：功能规格文档                                    │
├─────────────────────────────────────────────────────────────┤
│  2. 测试生成（Test Generation）                              │
│     ├── AI根据规格生成测试用例                                │
│     ├── 覆盖：正常路径 + 边界值 + 异常情况                    │
│     └── 输出：可执行的测试代码                                │
├─────────────────────────────────────────────────────────────┤
│  3. 红阶段（Red）                                           │
│     ├── 运行测试，确认失败                                    │
│     └── 验证测试本身正确                                      │
├─────────────────────────────────────────────────────────────┤
│  4. 绿阶段（Green）                                          │
│     ├── AI生成最小化代码使测试通过                             │
│     └── 人工审查代码质量                                      │
├─────────────────────────────────────────────────────────────┤
│  5. 重构阶段（Refactor）                                     │
│     ├── AI建议重构机会                                        │
│     ├── 人工决策执行                                          │
│     └── 自动回归验证                                          │
├─────────────────────────────────────────────────────────────┤
│  6. 循环迭代                                               │
│     └── 返回Step 2处理下一个功能                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、AI测试生成的类型

### 2.1 单元测试生成

```typescript
// 输入：待测函数
function calculateDiscount(price: number, rate: number): number {
  if (price < 0 || rate < 0 || rate > 1) {
    throw new Error('Invalid input');
  }
  return price * rate;
}

// AI生成的测试用例
describe('calculateDiscount', () => {
  // 正常路径
  test('applies 10% discount correctly', () => {
    expect(calculateDiscount(100, 0.1)).toBe(10);
  });
  
  test('applies 50% discount correctly', () => {
    expect(calculateDiscount(200, 0.5)).toBe(100);
  });
  
  // 边界值
  test('handles 0% discount', () => {
    expect(calculateDiscount(100, 0)).toBe(0);
  });
  
  test('handles 100% discount', () => {
    expect(calculateDiscount(100, 1)).toBe(100);
  });
  
  // 异常情况
  test('throws on negative price', () => {
    expect(() => calculateDiscount(-1, 0.1)).toThrow('Invalid input');
  });
  
  test('throws on negative rate', () => {
    expect(() => calculateDiscount(100, -0.1)).toThrow('Invalid input');
  });
  
  test('throws on rate over 100%', () => {
    expect(() => calculateDiscount(100, 1.1)).toThrow('Invalid input');
  });
});
```

### 2.2 集成测试生成

```typescript
// AI生成的集成测试
describe('Order Service Integration', () => {
  test('creates order and updates inventory', async () => {
    // Setup
    const initialStock = await inventoryService.getStock(productId);
    
    // Execute
    const order = await orderService.createOrder({
      userId: testUserId,
      items: [{ productId, quantity: 2 }]
    });
    
    // Verify
    const updatedStock = await inventoryService.getStock(productId);
    expect(updatedStock).toBe(initialStock - 2);
  });
  
  test('handles payment failure gracefully', async () => {
    // Mock payment failure
    paymentGatewayMock.reject = true;
    
    // Execute & Verify
    await expect(
      orderService.createOrder({...})
    ).rejects.toThrow('Payment failed');
    
    // Ensure inventory not changed
    const stock = await inventoryService.getStock(productId);
    expect(stock).toBe(initialStock);
  });
});
```

### 2.3 性能测试生成

```typescript
// AI生成的性能测试
describe('Performance Tests', () => {
  test('response time under 200ms for single user', async () => {
    const start = Date.now();
    await userService.getUser(userId);
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(200);
  });
  
  test('handles 100 concurrent requests', async () => {
    const promises = Array(100).fill(null).map(() => 
      userService.getUser(userId)
    );
    const results = await Promise.all(promises);
    expect(results.length).toBe(100);
  });
  
  test('no memory leaks in repeated calls', async () => {
    const initialMemory = process.memoryUsage().heapUsed;
    for (let i = 0; i < 1000; i++) {
      await userService.getUser(userId);
    }
    const finalMemory = process.memoryUsage().heapUsed;
    expect(finalMemory - initialMemory).toBeLessThan(10 * 1024 * 1024); // 10MB
  });
});
```

---

## 三、AI-TDD最佳实践

### 3.1 测试命名规范

```typescript
// AI生成的测试命名
describe('OrderService', () => {
  // 格式：should_expectedBehavior_when_condition
  test('should_returnOrder_when_validOrderId_provided', async () => {});
  test('should_throwError_when_orderNotFound', async () => {});
  test('should_updateStatus_when_confirmed', async () => {});
  test('should_emitEvent_when_orderCreated', async () => {});
});
```

### 3.2 测试数据构建

```typescript
// AI辅助的测试数据构建器
class TestDataFactory {
  static createUser(overrides = {}) {
    return {
      id: faker.string.uuid(),
      email: faker.internet.email(),
      name: faker.person.fullName(),
      createdAt: new Date(),
      ...overrides
    };
  }
  
  static createOrder(overrides = {}) {
    return {
      id: faker.string.uuid(),
      userId: this.createUser().id,
      items: [this.createOrderItem()],
      total: 100,
      status: 'pending',
      createdAt: new Date(),
      ...overrides
    };
  }
}

// 使用
test('should_calculateTotal_withMultipleItems', () => {
  const order = TestDataFactory.createOrder({
    items: [
      TestDataFactory.createOrderItem({ price: 50, quantity: 2 }),
      TestDataFactory.createOrderItem({ price: 30, quantity: 1 })
    ]
  });
  // ...
});
```

### 3.3 Mock策略

```typescript
// AI生成的Mock策略
const mocks = {
  userRepository: {
    findById: jest.fn(),
    save: jest.fn()
  },
  eventBus: {
    publish: jest.fn()
  },
  logger: {
    info: jest.fn(),
    error: jest.fn()
  }
};

// 在每个测试前重置
beforeEach(() => {
  Object.values(mocks).forEach(mock => mock.mockReset());
});

// 设置默认行为
mocks.userRepository.findById.mockResolvedValue(testUser);
```

---

## 四、TDD与AI的协同模式

### 4.1 测试即文档

```typescript
/**
 * # calculateTax(taxableAmount, taxRate)
 * 
 * ## 规格
 * - 输入金额必须为正数
 * - 税率必须在0-1之间
 * - 返回金额 = 税额 × 税率
 * 
 * ## 示例
 * calculateTax(100, 0.1) // 返回 10
 * calculateTax(200, 0.05) // 返回 10
 * 
 * ## 异常
 * - 负数金额抛出 InvalidInputError
 * - 超范围税率抛出 InvalidInputError
 */
test('should_calculateTax_correctly', () => {
  expect(calculateTax(100, 0.1)).toBe(10);
});
```

### 4.2 测试驱动AI代码生成

```
工程帅：\"为以下测试用例生成实现代码：

```typescript
test('should_returnUserWithOrders_when_validUserId', async () => {
  const user = await userService.getUserWithOrders(userId);
  expect(user.orders).toHaveLength(3);
  expect(user.totalSpent).toBe(500);
});
```

AI：\"以下是符合规格的实现代码：

```typescript
async getUserWithOrders(userId: string): Promise<UserWithOrders> {
  const user = await this.userRepository.findById(userId);
  if (!user) {
    throw new UserNotFoundError(userId);
  }
  
  const orders = await this.orderRepository.findByUserId(userId);
  const totalSpent = orders.reduce((sum, order) => sum + order.total, 0);
  
  return {
    ...user,
    orders,
    totalSpent
  };
}
```

工程帅审查 ✓
```

### 4.3 回归测试保障重构

```bash
# AI建议重构后，自动运行回归测试
$ npm test

> Running 127 tests
> ✓ should_calculateTax_correctly (5ms)
> ✓ should_throwOnNegativeAmount (3ms)
> ✓ should_returnUserWithOrders_when_validUserId (45ms)
> ...
>
> 127 passed, 0 failed

# 重构安全通过 ✓
```

---

## 五、AI-TDD检查清单

```markdown
## AI-TDD 实施检查清单

### 开始前
- [ ] 需求已澄清，无歧义
- [ ] 功能边界已定义
- [ ] 验收标准已明确

### 测试生成
- [ ] 正常路径覆盖
- [ ] 边界值测试
- [ ] 异常情况测试
- [ ] 性能基准测试

### 代码实现
- [ ] 测试通过
- [ ] 代码简洁
- [ ] 无重复逻辑
- [ ] 错误处理完善

### 重构验证
- [ ] 回归测试全部通过
- [ ] 代码可读性改善
- [ ] 性能无退化
- [ ] 无新增复杂度

### 交付标准
- [ ] 测试覆盖率 >= 80%
- [ ] 所有CI检查通过
- [ ] 代码审查通过
- [ ] 文档已更新
```

---

## 六、常见问题与解决

### 问题1：AI生成的测试过于简单

**解决**：补充边界条件和异常场景测试

```typescript
// AI初始生成
test('calculates sum', () => {
  expect(add(2, 3)).toBe(5);
});

// 人工补充
test('returns_0_when_bothInputs_0', () => {
  expect(add(0, 0)).toBe(0);
});

test('handles_negative_numbers', () => {
  expect(add(-1, 1)).toBe(0);
});

test('throws_on_overflow', () => {
  expect(() => add(Number.MAX_SAFE_INTEGER, 1)).toThrow();
});
```

### 问题2：测试与实现耦合

**解决**：使用接口抽象，通过Mock隔离

```typescript
// 依赖接口而非具体实现
interface IUserRepository {
  findById(id: string): Promise<User | null>;
}

// 测试时使用Mock
const mockRepo = { findById: jest.fn() };

// 实现时使用真实Repository
class PostgresUserRepository implements IUserRepository {
  async findById(id: string): Promise<User | null> {
    return db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}
```

### 问题3：测试执行太慢

**解决**：分级测试策略

```typescript
// 快速测试（单元测试）- 每次保存时运行
describe.skip('quick', () => {});

// 中速测试（集成测试）- PR前运行
describe.slow('integration', () => {});

// 慢速测试（E2E测试）- 每日CI运行
describe.periodic('e2e', () => {});
```

---

## 七、工具推荐

| 工具 | 用途 | AI能力 |
|------|------|--------|
| **Jest** | JavaScript测试框架 | 内置Mock支持 |
| **Vitest** | Vite原生测试 | 快速、现代化的API |
| **Testing Library** | DOM测试 | 行为驱动测试 |
| **Playwright** | E2E测试 | AI辅助测试生成 |
| **Codium** | 代码完整性测试 | AI分析代码变更 |
| **Cursor** | IDE | 内置测试生成 |
| **Claude Code** | AI编程 | TDD工作流支持 |

---

*整理：尼克·弗瑞*
*来源：Cursor-Windsurf-Mastery-Handbook, Superpowers*
