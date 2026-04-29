# 洞察：Playwright CLI + Skills UI自动化测试 — 无障碍树方案

> **洞察编号**：insight-20260429-playwright-cli-skills-uitesting
> **来源**：Raina测试 微信公众号 (2026-04-20)
> **原始链接**：https://mp.weixin.qq.com/s/CCLV_CU1AgSNOjCHkyafAA
> **价值评级**：⭐⭐⭐ (3/5)
> **标签**：#Playwright #VibeCoding #HarnessEngineering #AI测试
> **维护人**：尼克·弗瑞
> **更新日期**：2026-04-29

---

## 核心洞察

### 1. 无障碍树 vs 视觉识别：效率的本质差异

本文指出了一个关键对比：

| 方案 | 识别方式 | 速度 | 可复用性 |
|------|---------|------|---------|
| midscene.js | 截图 + 视觉AI识别 | 慢（几分钟/用例） | 低（每次重新识别） |
| Playwright CLI + 无障碍树 | DOM解析，ref引用 | 快 | 高（一次生成可复用） |

**核心原理**：
- 无障碍树（Accessibility Tree）是浏览器在DOM之上构建的辅助技术树
- 每个节点有role（按钮/文本框）、可访问名称、state（禁用/勾选）
- 用ref（如e105）表示元素，而非XPath或CSS选择器
- 不是视觉识别，是**结构化DOM解析**

> 这解释了为什么上篇文章（kaitong）里AI能快速执行——Playwright CLI的YAML快照本质上是无障碍树的精简表示。

---

### 2. MCP vs CLI：token效率的选择

**MCP的问题**：完整工具Schema（函数名、参数、类型、描述、枚举）全部塞进上下文 → token爆炸

**CLI的优势**：
- 工具Schema不在上下文里
- 命令返回精简的YAML/JSON快照
- 只返回元素ref引用，而非整个DOM

这是**token成本敏感型AI应用**的典型权衡。

---

### 3. 脚本自愈：自动化测试的关键能力

本文提出的**脚本自愈机制**：

```
执行失败（元素定位错误）
  → 自动重新快照
  → 修改脚本中的element_ref
  → 重新执行
```

这解决了自动化测试的经典痛点：**UI变了一次，脚本全部失效**。

结合上篇文章（kaitong）的CRITICAL RULES，两篇文章共同构成了一个更完整的自动化测试架构：

| 层 | 上篇(kaitong) | 本文(Raina) |
|----|-------------|------------|
| 用例格式 | .md文件 + CRITICAL RULES | JSON结构化用例 |
| 元素定位 | YAML快照ref引用 | 无障碍树ref引用 |
| 自愈能力 | 无（CRITICAL RULES预防） | 有（运行时自愈） |
| 执行模型 | haiku子Agent并发 | 单一Agent执行 |
| 可视化 | 原始执行输出 | JSON→Excel可选 |

---

### 4. Skills产品化：把经验封装成可复用单元

本文的Skills思路：
- **Skill 1**（探索+生成）：探索页面 → 生成JSON用例
- **Skill 2**（可视化）：JSON → Excel评审
- **Skill 3**（执行）：执行 + 中断恢复 + 自愈
- **辅助Skill**：扩展能力

这与Anthropic的Skill框架思路一致：**把领域经验封装成标准化可复用单元**。

---

## 与上篇文章的对比

| 维度 | kaitong版 | Raina版 |
|------|----------|---------|
| **侧重点** | 演进过程踩坑 | Skills产品化封装 |
| **用例格式** | .md（人机双可读） | JSON（AI友好，可转Excel） |
| **约束机制** | CRITICAL RULES（预防） | 脚本自愈（修复） |
| **元素定位** | YAML快照ref | 无障碍树ref |
| **执行模型** | haiku子Agent并发 | 单一Agent |
| **适用场景** | 长期回归测试 | 探索性测试 |

**两篇互补**：kaitong告诉你演进过程和CRITICAL RULES，Raina告诉你无障碍树原理和自愈机制。

---

## 实践要点

### 无障碍树的使用步骤

```
1. 安装playwright-cli
2. AI探索页面（有头模式打开浏览器）
3. 对每个变化页面进行无障碍快照采集
4. 生成JSON用例文件（结构化）
5. 可选：JSON→Excel用于评审
6. 执行用例（支持中断恢复+自愈）
```

### 选型建议

| 场景 | 推荐方案 |
|------|---------|
| 长期高频回归测试 | kaitong方案（.md + CRITICAL RULES + haiku并发） |
| 探索性/一次性测试 | Raina方案（无障碍树 + JSON + 自愈） |
| 团队无编码能力 | Raina方案（自然语言→JSON→执行） |
| 需要高可重复性 | kaitong方案（CRITICAL RULES约束） |

---

## 关联文件

- 源文件存档：`sources/references/playwright-cli-skills-uitesting-20260420.md`
- 上篇文章对比：`sources/references/playwright-claude-code-testing-20260424.md`
- 上篇Insight：`insights/insight-20260429-playwright-claude-code-testing.md`
- Claude Code并行开发：`topics/ai-programming/claude-code-parallel-dev.md`
- Harness Engineering：`topics/ai-native/agent-engineering.md`

---

## 参考链接

- 原文：https://mp.weixin.qq.com/s/CCLV_CU1AgSNOjCHkyafAA
- Playwright CLI：https://playwright.dev/
