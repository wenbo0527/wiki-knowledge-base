# PRD 需求文档模板 v5.0

> **版本**: v5.0
> **日期**: {{date}}
> **作者**: {{author}}
> **状态**: {{status}}

---

## 一、元数据

```yaml
---
产品域: {PD-XX} - {产品域名称}
Epic: {Epic 名称}
Epic URI: {Epic:EPIC-XX-XXX}
PRD 版本: {x.x.x}
创建日期: {YYYYMMDD}
审核人: {姓名}
---
```

---

## 二、变更日志

| 时间 | 版本号 | 变更人 | 主要变更内容 |
|:---|:---:|:---|:---|
| {{date}} | 1.0.0 | {{author}} | 初始版本 |
| {{date}} | 1.1.0 | {{author}} | {{change}} |

---

## 三、需求背景

### 3.1 目标

{{goal}}

### 3.2 痛点

1. 痛点1：{{description}}
2. 痛点2：{{description}}

### 3.3 核心挑战

1. 挑战1：{{description}}
2. 挑战2：{{description}}

---

## 四、需求范围

### 4.1 功能范围

本次需求聚焦 {{feature_name}}，核心覆盖：

{{scope_description}}

### 4.2 不在本次范围内

- {{excluded_1}}
- {{excluded_2}}

---

## 五、功能详情

### Feature 1：{{feature_name}} {#F-001}

**类型**：🆕 新增 / 🔄 变更

**关联 Story**：

| Story ID | Story 名称 | 优先级 | 状态 |
|:---|:---|:---:|:---:|
| Story 1-1 | {{story_name}} | P0 | 待开发 |
| Story 1-2 | {{story_name}} | P1 | 待开发 |

#### Story 1-1：{{story_name}}

| 字段 | 内容 |
|:---|:---|
| 角色-场景-价值 | 作为 {{role}}，在 {{scenario}} 时，需要 {{user_need}}，以便 {{business_goal}} |
| 优先级 | P0 |
| 状态 | 待开发 |

**验收标准**：

1. {{acceptance_criteria_1}}
2. {{acceptance_criteria_2}}
3. {{acceptance_criteria_3}}

**交互说明**：

{{interaction_description}}

---

### Feature 2：{{feature_name}} {#F-002}

**类型**：🆕 新增 / 🔄 变更

**关联 Story**：

| Story ID | Story 名称 | 优先级 | 状态 |
|:---|:---|:---:|:---:|
| Story 2-1 | {{story_name}} | P0 | 待开发 |

#### Story 2-1：{{story_name}}

| 字段 | 内容 |
|:---|:---|
| 角色-场景-价值 | 作为 {{role}}，在 {{scenario}} 时，需要 {{user_need}}，以便 {{business_goal}} |
| 优先级 | P0 |
| 状态 | 待开发 |

**验收标准**：

1. {{acceptance_criteria_1}}
2. {{acceptance_criteria_2}}

---

## 六、Story 与 FP 关联表

### Story 1-1 关联 FP

| FP ID | 功能点 | 优先级 | 验收标准 |
|:---|:---|:---:|:---|
| FP-001 | {{fp_name}} | P0 | {{criteria}} |
| FP-002 | {{fp_name}} | P1 | {{criteria}} |

### Story 1-2 关联 FP

| FP ID | 功能点 | 优先级 | 验收标准 |
|:---|:---|:---:|:---|
| FP-003 | {{fp_name}} | P1 | {{criteria}} |

### Story 2-1 关联 FP

| FP ID | 功能点 | 优先级 | 验收标准 |
|:---|:---|:---:|:---|
| FP-004 | {{fp_name}} | P0 | {{criteria}} |
| FP-005 | {{fp_name}} | P1 | {{criteria}} |

---

## 七、FP 清单汇总

| FP ID | 功能点 | 所属 Feature | 所属 Story | 优先级 | 验收标准 |
|:---|:---|:---|:---|:---:|:---|
| FP-001 | {{fp_name}} | Feature 1 | Story 1-1 | P0 | {{criteria}} |
| FP-002 | {{fp_name}} | Feature 1 | Story 1-1 | P1 | {{criteria}} |
| FP-003 | {{fp_name}} | Feature 1 | Story 1-2 | P1 | {{criteria}} |
| FP-004 | {{fp_name}} | Feature 2 | Story 2-1 | P0 | {{criteria}} |
| FP-005 | {{fp_name}} | Feature 2 | Story 2-1 | P1 | {{criteria}} |

---

## 八、菜单映射表

| 功能模块 | 一级菜单 | 二级菜单 | 三级菜单 | 路由路径 |
|:---|:---|:---|:---|:---|
| {{module}} | {{menu1}} | {{menu2}} | {{menu3}} | /path/to/page |

---

## 九、审批流接入（如有）

| 审批节点 | 审批角色 | 接入条件 | 审批方式 |
|:---|:---|:---|:---|
| {{node}} | {{role}} | {{condition}} | {{method}} |

> 注：如无需审批流，标注"无需审批"

---

## 十、版本历史

| 版本 | 日期 | 作者 | 变更内容 |
|:---|:---|:---|:---|
| v1.0 | YYYY-MM-DD | {{author}} | 初始版本 |

---

🦾 *PRD 模板 v5.0 | 用于指导开发*
