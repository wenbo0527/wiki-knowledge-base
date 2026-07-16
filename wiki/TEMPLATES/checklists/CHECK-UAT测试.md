---
title: CHECK UAT测试
author: 尼克·弗瑞 🕵️
product_domain: PD-TEMPLATE
doc_type: 其他
tags: [TEMPLATES, checklists]
date: 2026-04-30
---

# UAT测试检查清单

> **版本**: v1.0
> **日期**: {{YYYY-MM-DD}}
> **作者**: {{author}}
> **状态**: 正式

---

## 基本信息

| 字段 | 内容 |
|:---|:---|
| Feature名称 | {{feature_name}} |
| Feature编号 | {{feature_id}} |
| 测试环境 | {{environment}} |
| 测试人员 | {{tester}} |
| 测试日期 | {{date}} |

---

## 功能测试

### {{module_name}}

| # | 测试项 | 预期结果 | 实际结果 | 结果 |
|:---:|:---|:---|:---|:---:|
| 1 | {{test_case_1}} | {{expected}} | {{actual}} | ✅/❌ |
| 2 | {{test_case_2}} | {{expected}} | {{actual}} | ✅/❌ |
| 3 | {{test_case_3}} | {{expected}} | {{actual}} | ✅/❌ |

---

## 边界测试

| # | 测试项 | 测试数据 | 预期结果 | 实际结果 | 结果 |
|:---:|:---|:---|:---|:---|:---:|
| 1 | {{test_case}} | {{data}} | {{expected}} | {{actual}} | ✅/❌ |
| 2 | {{test_case}} | {{data}} | {{expected}} | {{actual}} | ✅/❌ |

---

## 异常测试

| # | 测试项 | 异常场景 | 预期结果 | 实际结果 | 结果 |
|:---:|:---|:---|:---|:---|:---:|
| 1 | {{test_case}} | {{exception}} | {{expected}} | {{actual}} | ✅/❌ |
| 2 | {{test_case}} | {{exception}} | {{expected}} | {{actual}} | ✅/❌ |

---

## 权限测试

| # | 测试项 | 角色 | 预期结果 | 实际结果 | 结果 |
|:---:|:---|:---|:---|:---|:---:|
| 1 | {{test_case}} | {{role}} | {{expected}} | {{actual}} | ✅/❌ |
| 2 | {{test_case}} | {{role}} | {{expected}} | {{actual}} | ✅/❌ |

---

## 测试统计

| 类型 | 通过 | 失败 | 总计 |
|:---|:---:|:---:|:---:|
| 功能测试 | {{count}} | {{count}} | {{total}} |
| 边界测试 | {{count}} | {{count}} | {{total}} |
| 异常测试 | {{count}} | {{count}} | {{total}} |
| 权限测试 | {{count}} | {{count}} | {{total}} |

---

## 测试结论

| 结论 | 说明 |
|:---|:---|
| **测试结果** | {{通过/不通过}} |
| **遗留问题** | {{issues}} |
| **风险评估** | {{risk}} |

---

## 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|:---|:---:|:---|:---|
| {{date}} | v1.0 | 初始版本 | {{author}} |

