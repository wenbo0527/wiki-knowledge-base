---
title: quick demo sample
author: 尼克·弗瑞 🕵️
product_domain: PD-SKILL
doc_type: 其他
tags: [skills]
date: 2026-06-30
---

# Quick Demo Sample - 人类浏览版

> **机器版**：`~/.openclaw/skills/quick-demo-sample/SKILL.md`
> **归属 Agent**：数字社区 dev
> **沉淀来源**：你给的范例 §六"数字社区Demo样例的归属"
> **创建日期**：2026-06-11

---

## 这是什么？

数字社区 PM 演示功能原型专用 Skill：**30 秒生成单 HTML 样例**，给用户"看个样子"。

## 触发 vs 不触发

| 用 | 不用 |
|:--|:--|
| ✅ PM 给用户展示功能原型 | ❌ 需要生产级代码（→ `digital-community-dev-workflow`） |
| ✅ 快速验证交互可行性 | ❌ 需要完整 UI 设计（→ 设计流程） |
| ✅ 用户对真实界面没概念 | ❌ 需要技术架构评审（→ 钟离） |

## 4 步执行

| 步 | 动作 |
|:--|:--|
| Step 1 | PM 提供 `feature_point` + `interaction_flow` + `target_audience` |
| Step 2 | 选择实现方案（HTML + Tailwind CDN） |
| Step 3 | 填入 `html_scaffold.html` 模板 |
| Step 4 | 输出（文件路径 + 交互流程 + 与正式版差距） |

## 关键约束

- ✅ 单 HTML 文件，可双击打开
- ✅ 30 秒内生成
- ✅ Tailwind CDN（无构建步骤）
- ❌ 不集成 Arco Design
- ❌ 不连真实 API

## 与 `digital-community-dev-workflow` 的边界

| 维度 | `quick-demo-sample` | `digital-community-dev-workflow` |
|:--|:--|:--|
| 目标 | PM 演示给用户看 | dev 写生产代码 |
| 技术栈 | HTML + Tailwind CDN | Vue 3 + Arco Design + Vite |
| 速度 | 30 秒 | 数小时到 1 天 |

---

## 沉淀记录

| 日期 | 变更 | 变更人 |
|:--|:--|:--|
| 2026-06-11 | 初版（按你给的范例 §六复刻） | 派蒙 |