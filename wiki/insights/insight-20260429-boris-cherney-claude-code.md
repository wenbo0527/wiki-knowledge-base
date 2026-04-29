# Insight: Claude Code创建者亲述"后编程时代"工作方式

> **来源**: Get笔记订阅 · 高质量人类谈话库 (The Pragmatic Engineer Podcast)
> **原始标题**: Boris Cherny (Anthropic Claude Code创建者/负责人) 深度访谈
> **访谈时间**: 2026年3月初
> **时长**: 约1小时36分钟
> **方向**: AI Agent / Vibe Coding / AI Programming
> **评级**: ⭐⭐⭐⭐⭐ (5/5 - 极高价值)
> **获取时间**: 2026-04-29

---

## 核心洞察

### 1. "后编程时代"工作方式

**Boris Cherny的日常工作**：
- 日均提交 **20-30个PR**
- 100%代码由Claude生成，**人工零编辑**
- 通过5个并行Claude实例实现
- 约**1/3编码工作在移动设备**上完成（iOS应用）

**核心工作流**：
```
┌─────────────────────────────────────────────────────────────┐
│                    Boris的一天                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 打开5个终端标签（各自独立checkout）                       │
│  2. 用Plan Mode让Claude制定计划                             │
│  3. 迭代优化计划                                            │
│  4. one-shot实现 → 一次性成功率极高                          │
│                                                              │
│  🚩 关键洞察：AI编程的瓶颈不在代码生成，而在计划质量          │
└─────────────────────────────────────────────────────────────┘
```

> "Once there is a good plan, it will one-shot the implementation almost every time."
> — Boris Cherny

---

### 2. Claude Code的"agentic search"就是glob和grep——打败了RAG

**团队尝试过的方案**：
- 本地向量数据库
- 递归模型索引（Recursive Model Indexing）
- 其他fancy方法

**全都有缺点**：索引过期、权限复杂、维护成本高

**最终胜出**：最朴素的glob和grep，由模型驱动

**灵感来源**：在Instagram观察到一个现象——当Meta内部IDE的"点击跳转定义"功能坏了时，工程师们就是用grep搜代码的。

> "Plain glob and grep, driven by the model, beat everything."

**启示**：简单打败复杂。有时候最朴素的技术方案就是最好的。

---

### 3. Claude Code安全架构："瑞士奶酪模型"

多层防护叠加，每层都有漏洞，但层层叠加后漏洞被极大减少：

| 层级 | 机制 | 作用 |
|------|------|------|
| 模型层 | Opus 4.6增强抗prompt injection | 基础防护 |
| 运行时层 | 分类器检测拦截可疑请求 | 实时监控 |
| 应用层 | 子agent总结外部内容 | 降低风险 |

> 没有单一防线是完美的，但层层叠加后系统足够安全。

---

### 4. PRD已死，原型取代之

**Claude Code团队的工作方式**：
- 不写PRD（产品需求文档）
- 取而代之：**发布前先构建几十个可运行的原型**

> "If we started with static mocks and Figma, or if we started with a PRD, this product would never have shipped."

**核心逻辑变化**：
- 过去：先写文档，再写代码（文档是合同）
- 现在：直接写代码就是文档（代码即原型）

**当生成代码的成本趋近于零**，"先文档后代码"变成了"代码即文档"。

---

### 5. Claude Cowork：10天构建，增长速度超过Claude Code发布时

**发现"潜在需求"**：
- 非工程师（数据科学家、财务、销售）已经在hack式使用Claude Code
- 他们无法获取公司内部资源，但有强烈的AI辅助需求

**10天构建**：工程复杂度主要在安全层面
- 分类器
- 沙箱VM
- OS级防误删
- 非技术用户权限模型

**增长速度**：超过Claude Code发布时

---

### 6. 印刷机类比——今天的程序员可能是中世纪的抄写员

**最震撼的类比**：

> 中世纪的抄写员是极少数识字精英，为不识字的国王服务。
> 
> 印刷术发明后，抄写员"失业"了。但许多人变成了作家，文学市场规模扩大了超出所有人预期。

**Boris的问题**：
> 今天的软件工程师是否会经历同样的转变？
> 
> 编程变得人人可及，但工程师构建的系统影响范围可能远超以往？

---

## 人物侧写

### Boris Cherny
**身份**：Anthropic Claude Code创建者/Head of Claude Code

**背景**：
- 前Meta Principal Engineer（5年）
- O'Reilly《Programming TypeScript》作者
- 在Meta主导"Better Engineering"计划

**成长轨迹**：
- 13岁在eBay卖Pokemon卡片时学会HTML
- 用`<blink>`标签让商品溢价（49美分→99美分）——天生的产品直觉
- 在Meta不断把自己的code review工作自动化
- 加入Anthropic后基于实验性工具Clyde开发Claude Code
- 从side project变成公司增长最快的产品

---

## 关键引言汇总

| 引言 | 场景 |
|------|------|
| "Once there is a good plan, it will one-shot the implementation almost every time." | Plan Mode的重要性 |
| "I ship 20-30 PRs a day by running 5 parallel Claude instances." | 并行Agent工作 |
| "Plain glob and grep, driven by the model, beat everything." | Agentic Search |
| "If we started with static mocks and Figma... this product would never have shipped." | PRD已死 |
| "It's not so much about deep work, it's about context switching and jumping across multiple contexts." | 新工作模式 |
| "In the middle ages, scribes were a tiny literate elite. When the printing press was invented..." | 印刷机类比 |

---

## 关联知识

- [[ai-native/agent-engineering]] - Agent工程化专题
- [[topics/ai-programming/claude-code-parallel-dev]] - Claude Code并行开发指南
- [[insights/insight-20260428-everything-claude-code]] - Simon Willison的Claude Code指南
- [[insights/insight-20260429-agent-27-design-patterns]] - 27种设计模式

---

## 要点总结

1. **计划 > 代码**：AI编程瓶颈在计划质量，不在代码生成
2. **简单打败复杂**：glob+grep打败了RAG等fancy方案
3. **瑞士奶酪安全模型**：多层防护缺一不可
4. **PRD已死，原型取代**：代码即文档，原型即文档
5. **印刷机类比**：编程人人可及，工程师影响范围扩大百倍
6. **5并行实例**：日均20-30个PR，100% AI生成

---

*尼克·弗瑞 🕵️ | Get笔记订阅引入 · 高质量人类谈话库 | 2026-04-29*
