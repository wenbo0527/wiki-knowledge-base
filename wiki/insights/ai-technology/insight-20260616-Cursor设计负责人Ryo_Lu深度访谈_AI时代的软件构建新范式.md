---
title: insight 20260616 Cursor设计负责人Ryo Lu深度访谈 AI时代的软件构建新范式
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# Cursor设计负责人Ryo Lu深度访谈：AI时代的软件构建新范式

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1902390543611170744
> **创建时间**: 2026-02-22 13:47:39
> **更新时间**: 2026-02-22 13:47:39
> **原始链接**: https://mp.weixin.qq.com/s?__biz=Mzk1NzgxMjQ0OA==&mid=2247493540&idx=1&sn=5fbe08ab90bb4a8fd073c2f33be02974&chksm=c213d9e7cfbf77349d980d7e756582d17a8ab6265c135e46086ffc6927187f11d9758d4bd7bb&scene=90&xtrack=1&req_id=1771738855074443&sessionid=1771738888&subscene=93&clicktime=1771739177&enterid=1771739177&flutter_pos=11&biz_enter_id=4&ranksessionid=1771738888&jumppath=1001_1771738886631%2C1104_1771738888893%2CMMWebViewController_1771738917209%2C1104_1771739165689&jumppathdepth=4&ascene=56&devicetype=iOS26.4&version=1800452c&nettype=3G+&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQA%2FMNrFKSEV7AYeWub1jxCRLXAQIE97dBBAEAAAAAAAxHBGJEGVAAAAAOpnltbLcz9gKNyK89dVj03mI1UAcaWgne9ztrriDTKyH8xLY9%2FVFKCC7%2FkEidV1JNB0IM202CAq%2BxHLfgXyjR%2F30NfUjHdr0hEWSzzmPlj383B8aHW%2BEqoOUNOHY5JbPA4ZCng7hWSpIFEOgHmDbFOHHHAOyRlihX9%2Fm41Z5FKhQix%2FwEF6J%2F6soSNIFUtZmR2Dk2NhSgMKLe6FKVAjrEWNMm8V5%2B%2FkZEPQB9r9%2FPRtX5bMjG01RP84ZAGdfHChtz&pass_ticket=yq9HRO2xUj1mSjv4tJLIL44oS%2F8bTWjaQl6DhdKU5cTcLbau2GiIrRQktRngSzlw&wx_header=3

---

### **🎯 核心人物与背景概述**

**对话双方背景**
- **Ryo Lu**：Cursor设计负责人，前Notion创始设计师，曾任职于Stripe和Asana，早期AI辅助设计与编码实践者。
- **Soleio**：Facebook早期设计师（创造Like按钮），前Dropbox设计负责人，现天使投资人（投资Figma、Vercel、Perplexity等）。

**访谈基本信息**
- **节目**：First of Kind第二季第二集
- **发布时间**：2026年2月18日
- **核心话题**：Cursor团队运作模式、递归开发飞轮、Agent时代人机交互、设计师角色转型、产品终极愿景

**Cursor公司概况**（注）
- **成立**：2022年MIT期间，由Michael Truell等4人创立
- **技术基础**：基于VS Code开发
- **融资与估值**：2025年11月完成23亿美元D轮融资，估值293亿美元
- **商业化**：年化收入超10亿美元，服务超半数财富500强企业

### **👥 4人设计团队的创新协作模式**

#### **团队构成与运作**
- **核心设计团队**：仅4人（含Ryo Lu），包括2名产品设计师+1名品牌设计师
- **扩展设计力量**：几乎所有工程师深度参与设计决策，关注系统运作与功能流转逻辑
- **设计负责人角色**：核心工作是"收拢"分散的设计成果，清理冗余，统一概念，确保系统整体性，而非传统的"画mock"

#### **工作方式特点**
- **超前思考**：基于现有系统和团队工作判断产品演进方向
- **概念整合**：发现不同成员工作中的概念重叠，促进协作或合并优化
- **全层统一**：从视觉层、数据模型到系统扩展逻辑、核心理念保持连贯性
> "I help people break down the problem, see — ah, this piece and this piece is the same. Maybe you should talk to this guy because he's working on that."

### **🔄 用Cursor构建Cursor：递归飞轮效应**

#### **自我改进循环机制**
1. **使用Cursor**：团队成员日常使用工具进行开发
2. **发现痛点**：在复杂项目构建中识别工具缺陷
3. **改进工具**：基于痛点反馈优化Cursor功能
4. **工具变好→人变强→做更多事**：形成正向循环
5. **未来展望**：Agent自主完成循环后将加速迭代

#### **内部实践案例**
- **3D版Minecraft**：工程师Ian使用Cursor在浏览器中构建
- **ryOS个人操作系统**：Ryo Lu个人项目，模仿经典Mac OS风格，使用React和TypeScript开发（开源地址：github.com/ryokun6/ryos）
> "The tool gets better, you also get better. It's like a self-improving loop. Once the agent is able to do this by themselves it will be even faster."

### **🤖 Agent时代的人机交互范式**

#### **人机交互抽象层级跃升路径**

| 交互层级 | 特点 | 局限性 |
|---------|------|--------|
| **手动写代码** | 直接操作代码 | 效率低下，需掌握语法 |
| **自动补全** | AI辅助完成函数，保持心流 | 仅支持片段式生成 |
| **聊天交互** | AI理解代码库，回答问题，应用修改 | 一次只能处理一个线程 |
| **Agent管理** | 同时管理多个Agent执行任务 | **人类瓶颈**：最强程序员仅能同时管理约4个Agent |
| **规划仪表盘**（下一代界面） | 可视化规划任务，监控Agent状态 | 尚未实现，需解决多Agent协同问题 |

#### **核心洞察**
- **人类成为瓶颈**：随着Agent自主性增强，人类管理能力成为系统扩展的限制因素
- **界面进化方向**：从直接代码交互→聊天交互→规划式交互，需开发适应更高抽象层级的界面
- **用户群扩展**：抽象层级提升将降低使用门槛，自然扩大用户群体

### **🎨 设计哲学：核心集合与通用工具**

#### **简化核心，丰富组合**
- **TikTok案例**：核心是"自动循环的视频信息流"，用户动作仅需"划到下一个"
- **Notion案例**：通过"块(blocks)、页面(pages)、数据库(databases)"三个核心概念统一所有工作场景
- **设计原则**：核心集合越简单，组合出来的复杂度越高，系统可伸缩性越强

#### **AI时代的工具通用性**
- **通用基底**：以代码为统一基底，但不要求所有人学编程
- **适配思维方式**：设计师用图片和2D空间思考，PM用文字描述约束，程序员用代码原型试想法
- **统一Agent层**：对接不同输入方式，覆盖用户不擅长的部分，保留个人工作习惯与优势
> "How do I kind of keep my habits, keep my strength, all the years of Figma-ing that I've done — like don't throw those away — but with this new thing you can be like a hundred times more productive."

### **🔬 创新实践：Baby Cursor与原型环境**

#### **Baby Cursor的诞生背景**
- **开发痛点**：Cursor基于VS Code开发，修改受限于原有架构，验证新想法需启动完整开发环境
- **解决方案**：构建简化版Cursor原型环境，外观一致但更接近理想状态，专注想法验证

#### **软件原型的独特价值**
- **与建筑模型的区别**：建筑模型不能直接变成建筑，而软件原型有潜力转化为产品
- **行业趋势**：Ramp、Notion等公司也在构建类似原型环境，支持设计师快速探索创意
> "You realize all of these things are actually the same thing."

### **⚠️ 设计师角色转型警告**

#### **传统设计师的风险**
- **被淘汰的技能**：仅会画按钮、做mock、搭设计系统，这些AI已能实现
- **Ryo的警示**："If you're a designer who thinks designing is just drawing buttons and inputs and making mocks and maybe like building design systems, you're like a little fucked."

#### **设计师的真正价值**
1. **发现事物真实形态**：识别事物本质及未来可能形态
2. **跨层级工作能力**：在视觉、概念、架构等多个层面协同优化
3. **因人而异的表达**：根据合作对象调整沟通方式（mock、原型或概念讨论）
4. **可能性洞察**：帮助团队看到潜在机会与创新方向

### **🚀 AI时代的双重效应**

#### **同时发生的两种趋势**
- **门槛降低**：非程序员也能通过AI工具实现创意，从粗糙原型逐步迭代
- **优势放大**：有经验者进入高效心流状态，生产力提升10-100倍，与跨领域专家协作创造更复杂软件

#### **新的"流利度"**
- **vibe coder现象**：大量使用AI的开发者形成与AI协作的直觉，知道如何拆分提示词、判断模型能力边界
- **能力重构**：不一定要精通编程语言语法，但需理解如何与AI有效协作

### **💡 Cursor的差异化定位**

#### **与其他工具的对比**

| 工具 | 局限性 | Cursor优势 |
|------|--------|------------|
| **Figma** | 困在像素层 | 不强制特定工作方式，适配用户思维习惯 |
| **V0/Lovable** | 限制在"安全区"内，超出范围则失效 | 底层统一为代码，支持无限扩展 |

#### **产品愿景**
- **不是代码编辑器**：而是"适配每个人思维方式的构建平台"
- **通用语言(lingua franca)**：让不同角色（设计师、PM、程序员、普通人）用各自方式在同一系统协作
- **核心主张**："I don't want to force people to change. I want them to figure themselves out."

### **🔮 未来展望**

#### **关键方向**
1. **超越代码编辑器**：构建适应不同角色、输入方式、工作习惯的全新软件创造界面
2. **解决Agent管理瓶颈**：开发支持更高抽象层级的人机交互界面
3. **原型到产品的转化**：实现软件原型直接转化为产品的开发新模式

#### **终极目标**

Ryo Lu用一个词概括：**"Software"**（软件），强调专注于当下构建，持续探索未来可能性。

### **📌 补充细节**
- **vibe coding**：由Andrej Karpathy（OpenAI联合创始人）2025年2月提出，指完全依赖AI生成代码、开发者不审查具体实现的编程方式，被Collins词典评为2025年度词汇
- **模式语言(Pattern language)**：Ryo设计方法论核心，源自建筑师Christopher Alexander（1977年提出），指一套可复用的设计模式及关系
- **VS Code基础**：Cursor基于VS Code开源版开发，业内戏称"我们是VS Code的fork"