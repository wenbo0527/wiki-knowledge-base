# Insight: 为Agent设计产品 - 从"界面工具"到"运行底座"的范式转变

> 原始链接: https://mp.weixin.qq.com/s/mlajGBnYpugyxjTDc7JGNA
能力框架: capability-requirement-decision capability-product-design #capability-data-driven #capability-risk-control

> **来源**: 微信公众号 · AI科技媒体
> **原始链接**: https://mp.weixin.qq.com/s/mlajGBnYpugyxjTDc7JGNA
> **评级**: ⭐⭐⭐⭐ (4/5)
> **标签**: Agent产品设计, Headless架构, MCP, SaaS
> **存储时间**: 2026-04-30

---

## 核心命题

**软件产品正在从"给人操作的界面"，演变为"给人和Agent共同调用的运行底座"**

这一转变要求产品能力需被重新整理为Agent可理解、可调用、可约束、可审计的动作集合，而非简单增加API或MCP入口。

---

## Agent视角的工具设计原则

### 职责单一化

工具需专注单一功能（如`AskUserQuestion`工具仅负责提问），避免多职责导致Agent推理混乱。

### 渐进式信息披露

- 优先提供文档索引
- 需用时再让Agent主动拉取细节
- 而非一次性塞入系统提示词

### 机器可读性

工具名、参数、返回值、错误消息需结构化（如CLI的`--help`、`--json`、exit code），减少Agent猜测空间。

---

## 产品调用链路的进化

| 阶段 | 链路模型 | 设计重点 |
|------|----------|----------|
| **过去** | 用户 → UI（页面/按钮/表单）→ 平台 | 让人看懂、少点错、可撤回 |
| **现在** | 用户 → 用户Agent → 产品Agent → 平台底座 | 让Agent知道何时/如何调用、失败如何恢复 |

---

## Salesforce Headless 360案例

### 核心能力拆解

| 能力 | 说明 |
|------|------|
| **Build any way you want** | 60+ MCP工具、30+预配置coding skills，支持外部Agent直接操作 |
| **Deploy on any surface** | Agentforce Experience Layer实现跨平台渲染 |
| **Build agents you can trust** | 开源Agent Script + Testing Center + Custom Scoring Evals |

### 关键洞察：守住底座而非入口

- **开放入口但保留核心**：暴露API/MCP/CLI调用能力，但数据/权限/流程/审计逻辑仍保留在平台底座
- **超越数据库的业务能力**：不仅提供数据查询，还需回答"在特定组织/角色/状态下，下一步能安全做什么"

---

## 为Agent设计产品的五大关键步骤

### 1. 能力原子化

将复杂功能拆解为职责清晰的原子动作，定义：
- 前置条件
- 失败处理
- 副作用（如CLI需包含`--dry-run`、非交互模式）

**自检标准**：移除页面后，Agent仅通过工具和文档能否独立完成任务？

### 2. 语义层建设

提供机器可读的规范：
- `llms.txt`（文档索引）
- OpenAPI（接口schema）
- `skill.md`（能力摘要）

### 3. 确定性保障

**Agent Script**：通过flat file定义if/else、状态转移、动作顺序

**治理基础设施**：
- Testing（离线测试）
- Evals（自定义评分）
- A/B Testing
- Observability（调用链观测）
- Rollback（版本回滚）

### 4. 场景差异化

| 场景 | 结构类型 | 核心约束 | 人的角色 |
|------|----------|----------|----------|
| **客户Agent** | 静态流程图 | 合规、品牌、可审计 | 兜底和审批 |
| **员工Agent** | 动态任务图 | 效率、探索、工具覆盖 | 审阅和决策 |

### 5. 产品架构五层模型

```
┌─────────────────────────────────────────────────────────────┐
│  表面层：用户工作环境（Slack/Teams/ChatGPT/移动端）          │
├─────────────────────────────────────────────────────────────┤
│  调用层：Agent接入方式（API/CLI/MCP/Hosted Server）         │
├─────────────────────────────────────────────────────────────┤
│  语义层：减少猜测（Schema/Policy/Error Contract/Examples）  │
├─────────────────────────────────────────────────────────────┤
│  业务底座：核心资产（Data/Workflow/Business Logic）         │
├─────────────────────────────────────────────────────────────┤
│  治理层：可控执行（Auth/Audit/Testing/Observability/Rollback）│
└─────────────────────────────────────────────────────────────┘
```

---

## 行业趋势

### SaaS计费模式变革

传统按席位/登录收费将被替代：
- 动作数量
- 流程完成率
- 自动化节省时间

（如Agentforce转向按消耗计费）

### 反馈循环产品化

通过工具调用`rationale`字段、结构化feedback工具收集Agent失败路径，反哺产品优化。

### CLI与MCP协同

- CLI适合本地快速组合
- MCP适合多租户权限治理
- 两者非对立而是互补入口

---

## 对OpenClaw的启示

1. **底座思维 > 界面思维**：思考产品作为"运行底座"而非"界面工具"
2. **语义层优先**：先建设机器可读的规范（Schema/OpenAPI），再考虑UI
3. **治理即产品**：Testing/Evals/Observability/Rollback是Agent产品的核心组成
4. **按消耗计费**：考虑从按席位向按动作/完成率计费转型

---

*分析时间: 2026-04-30*
*分析师: 尼克·弗瑞*
