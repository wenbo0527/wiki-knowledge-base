# Clean Architecture与AI安全设计模式

> 来源：Cursor-Windsurf-Mastery-Handbook
> 整理时间：2026-04-14

---

## 一、Clean Architecture核心原则

### 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│              (Controllers, API Endpoints)                   │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│              (Use Cases, Application Services)              │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                           │
│            (Entities, Business Rules, Domain Services)       │
├─────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                       │
│        (Repositories, External Services, DB, Cache)         │
└─────────────────────────────────────────────────────────────┘
```

### 各层约束

| 层级 | 约束 | AI可修改 |
|------|------|----------|
| Domain | 纯粹的业务逻辑，无外部依赖 | ⚠️ 需严格审查 |
| Application | 依赖Domain，编排业务 | ✅ 可辅助 |
| Infrastructure | 实现接口，外部调用 | ✅ 可辅助 |
| Presentation | HTTP处理，参数验证 | ✅ 可辅助 |

---

## 二、AI-Safe Design Patterns

### 1. 依赖注入边界

```typescript
// ❌ AI不安全的模式：直接实例化
class UserService {
  private db = new PostgreSQL(); // 违反依赖倒置
  
  async getUser(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}

// ✅ AI安全的模式：依赖注入
class UserService {
  constructor(
    private readonly db: IDatabase, // 接口
    private readonly logger: ILogger
  ) {}
  
  async getUser(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}
```

### 2. Repository Pattern

```typescript
// 定义接口（Domain层）
interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
}

// 实现（Infrastructure层）
class PostgreSQLUserRepository implements IUserRepository {
  constructor(private readonly db: IDatabase) {}
  
  async findById(id: string): Promise<User | null> {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
  
  // ... 其他实现
}
```

### 3. Circuit Breaker Pattern

```typescript
// ✅ 所有外部调用必须通过熔断器
class PaymentService {
  constructor(
    private readonly paymentGateway: ICircuitBreaker<PaymentGateway>,
    private readonly logger: ILogger
  ) {}
  
  async processPayment(order: Order): Promise<PaymentResult> {
    try {
      return await this.paymentGateway.execute(
        (gateway) => gateway.charge(order)
      );
    } catch (error) {
      this.logger.error('Payment failed', { orderId: order.id, error });
      throw new PaymentException('Payment processing failed');
    }
  }
}
```

---

## 三、Hexagonal Architecture（六边形架构）

### 核心概念

```
                    ┌─────────────────┐
                    │   Application   │
                    │     Core        │
                    │  (Domain +      │
                    │   Use Cases)    │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────┴─────┐      ┌─────┴─────┐      ┌─────┴─────┐
    │  Driving  │      │   Ports   │      │  Driven   │
    │  Adapters │◄────►│           │◄────►│  Adapters │
    │ (Primary) │      │  (Interfaces)│     │(Secondary)│
    └───────────┘      └─────────────┘      └───────────┘
         │                                        │
         ▼                                        ▼
    HTTP/REST                                  DB/Queue
    GraphQL                                   External APIs
    CLI                                       File System
```

### AI辅助开发的关键约束

```markdown
## Hexagonal Architecture Rules for AI

###  Ports（接口）
- 所有端口定义在 Domain 层
- 禁止在端口中引用 Infrastructure

###  Adapters（适配器）
- Adapters 实现 Ports
- 禁止 Adapters 直接调用其他 Adapters

###  Domain（核心）
- 禁止引入任何外部依赖
- 禁止使用 HTTP、SQL 等基础设施相关注解
- 业务逻辑必须可测试（不依赖任何外部系统）
```

---

## 四、模块间通信模式

### 1. 同步通信：API/事件

```typescript
// ✅ 推荐的模块间调用
class OrderService {
  constructor(
    private readonly eventBus: IEventBus,
    private readonly userGateway: IUserGateway
  ) {}
  
  async createOrder(order: Order): Promise<void> {
    // 业务逻辑
    await this.orderRepository.save(order);
    
    // 通过事件通知其他模块
    await this.eventBus.publish(
      new OrderCreatedEvent(order.id, order.userId)
    );
  }
}
```

### 2. 异步通信：消息队列

```typescript
// ✅ 事件驱动架构
interface IEvent {
  readonly occurredAt: Date;
  readonly aggregateId: string;
}

class OrderCreatedEvent implements IEvent {
  readonly occurredAt = new Date();
  
  constructor(
    public readonly orderId: string,
    public readonly userId: string
  ) {}
}

// 事件处理器（另一个模块）
class InventoryEventHandler {
  async handle(event: OrderCreatedEvent): Promise<void> {
    await this.inventoryService.reserveStock(event.orderId);
  }
}
```

---

## 五、AI辅助的架构验证

### 自动化架构测试

```bash
# dependency-cruiser 配置
# .dependency-cruiser.js
module.exports = {
  forbidden: [
    {
      name: 'no-domain-to-infrastructure',
      comment: 'Domain layer should not depend on Infrastructure',
      from: { pathStartsWith: 'src/domain' },
      to: { pathStartsWith: 'src/infrastructure' },
    },
    {
      name: 'no-controller-to-repository',
      comment: 'Controllers should not access repositories directly',
      from: { pathStartsWith: 'src/presentation' },
      to: { pathStartsLike: 'src/infrastructure/repositories' },
    }
  ]
};
```

### 运行架构验证

```bash
# CI中必须通过的架构检查
npx dependency-cruiser --validate .dependency-cruiser.js src/

# 如果失败，阻止合并
if [ $? -ne 0 ]; then
  echo "Architecture violation detected!"
  exit 1
fi
```

---

## 六、代码组织模板

### 标准目录结构

```
src/
├── domain/                    # 纯业务逻辑
│   ├── entities/            # 实体
│   ├── value-objects/      # 值对象
│   ├── services/            # 领域服务
│   ├── events/              # 领域事件
│   └── ports/              # 接口定义（输入/输出端口）
│
├── application/              # 应用层
│   ├── use-cases/          # 用例
│   ├── dto/                # 数据传输对象
│   ├── services/           # 应用服务
│   └── ports/              # 应用层端口
│
├── infrastructure/          # 基础设施层
│   ├── repositories/       # 仓储实现
│   ├── adapters/          # 适配器
│   ├── messaging/         # 消息队列
│   └── external/          # 外部服务
│
└── presentation/           # 表现层
    ├── controllers/        # 控制器
    ├── dto/               # 请求/响应DTO
    ├── middleware/        # 中间件
    └── routes/            # 路由定义
```

---

## 七、常见架构问题与修复

### 问题1：Domain层污染

```typescript
// ❌ 问题：Domain中有HTTP注解
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: string;
  
  @Column()
  email: string;
}

// ✅ 修复：Entity保持纯粹
export class User {
  constructor(
    public readonly id: string,
    public readonly email: Email,
    public readonly createdAt: Date
  ) {}
}

// ORM映射移到Infrastructure层
// orm.config.ts
export const UserEntity = new EntitySchema({
  name: 'User',
  columns: {
    id: { type: String, primary: true },
    email: { type: String },
    createdAt: { type: Date }
  }
});
```

### 问题2：循环依赖

```typescript
// ❌ 问题：循环依赖
// UserService -> OrderService -> UserService

// ✅ 修复：通过事件解耦
// UserService 发布 UserCreatedEvent
// OrderService 订阅并处理
```

### 问题3：上帝对象

```typescript
// ❌ 问题：一个Service处理所有业务
class MonsterService {
  createUser() { ... }
  processOrder() { ... }
  sendEmail() { ... }
  generateReport() { ... }
}

// ✅ 修复：职责分离
class UserService { createUser() { ... } }
class OrderService { processOrder() { ... } }
class NotificationService { sendEmail() { ... } }
class ReportingService { generateReport() { ... } }
```

---

## 八、AI辅助架构重构检查清单

```markdown
## 架构重构审查清单

### 分层合规
- [ ] Domain层无基础设施依赖
- [ ] Application层只依赖Domain
- [ ] Infrastructure实现定义的Ports
- [ ] Presentation层只调用Application

### 依赖方向
- [ ] 无循环依赖
- [ ] 依赖关系指向内层
- [ ] 接口定义在内层，实现放在外层

### 可测试性
- [ ] Domain层可独立测试
- [ ] 无硬编码外部依赖
- [ ] 使用依赖注入

### 安全性
- [ ] 数据库访问通过Repository
- [ ] 外部API调用通过Gateway
- [ ] 所有外部调用有超时和熔断

### 事件驱动
- [ ] 模块间通过事件通信
- [ ] 事件是不可变的
- [ ] 事件处理器是幂等的
```

---

*整理：尼克·弗瑞*
*来源：Cursor-Windsurf-Mastery-Handbook*
