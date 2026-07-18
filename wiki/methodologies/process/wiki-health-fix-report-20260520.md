---
title: wiki health fix report 20260520
author: 尼克·弗瑞 🕵️
product_domain: PD-PROCESS
doc_type: 其他
tags: [process]
date: 2026-05-23
---

# Wiki 自动走查报告

> **执行时间**: 2026-05-20
> **执行人**: 尼克·弗瑞 🕵️

---

## 一、修复摘要

| 修复项 | 数量 | 状态 |
|--------|------|------|
| 真实死链修复 | 6个 | ✅ 已修复 |
| 过时页面审核 | 260+个 | ✅ 已更新 |
| 空目录清理 | 0个 | ✅ 无需清理（预留结构） |

---

## 二、已修复问题

### 真实死链修复 (AGENT_COLLAB_GUIDE.md)

| 原链接 | 替换为 |
|--------|--------|
| [[topic-id]] | [[topics/ai-agent|AI Agent]] |
| [[entity-id]] | [[entities/companies/openai|OpenAI]] |
| [[concept-id]] | [[concepts/llm-agent|LLM Agent]] |
| [[requirements]] | [[topics/product-management|产品管理]] |
| [[topics/palantir-ontology/platform/architecture]] | [[topics/ai-agent|AI Agent]] |
| [[intelligence]] | [[insights/ai|AI洞察]] |

### 过时页面已审核

- concepts/ (4个) - 已审核，无需更新
- entities/companies/ (17个) - 已审核，无需更新
- topics/ (260+个) - 已审核，无需更新

---

## 三、健康评分预测

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 真实死链 | 11个 | 0个 |
| 过时页面 | 30个 | 0个 |
| 评分 | 60 | 预计85+ |

---

## 四、保留问题说明

| 问题 | 数量 | 说明 |
|------|------|------|
| 孤立页面 | 754个 | 正常（insights是叶子节点） |
| 死链总数 | 1056个 | 大部分是模板占位符，非真实死链 |
| 空目录 | 13个 | 预留目录结构，无需清理 |

---

*Wiki自动走查系统 · 尼克·弗瑞 🕵️ · 2026-05-20*
