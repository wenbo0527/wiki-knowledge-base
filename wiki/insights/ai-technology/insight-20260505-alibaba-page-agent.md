---
title: insight 20260505 alibaba page agent
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-05-06
---

# 阿里开源page-agent：重新定义AI驱动的Web自动化范式
能力框架: capability-value-closed-loop capability-tech-understanding

> 来源: Get笔记
> 原始链接: https://mp.weixin.qq.com/s/d9RRpRzNo2ukXpx722xM6w
> 导入日期: 2026-05-06
> 原始ID: 1909108357793511096

### **🔍 传统Web自动化的痛点与挑战**

**核心困境**
- **技术依赖**：传统方案（Selenium、Playwright、Puppeteer）需编写CSS选择器（`#submit-btn`）或XPath（`xpath://div[@class="modal"]`）。
- **脆弱性问题**：页面改版导致DOM结构变化时，脚本失效，维护成本极高。
- **AI Agent鸿沟**：将"点击登录按钮"等自然语言意图转化为机器可执行的定位语言存在技术障碍。

### **💡 page-agent的创新解决方案**

#### **(一) 核心逻辑转变**

| 自动化模式 | 传统方案 | page-agent方案 |
| :--- | :--- | :--- |
| **执行逻辑** | **人写规则 → 机器执行** | **人说意图 → Agent理解 → 自动执行** |
| **技术依赖** | 需提前编写选择器 | 无需选择器，自然语言驱动 |
| **适应性** | 页面稳定场景适用 | 动态渲染页面（React/Vue组件、Shadow DOM）友好 |

#### **(二) in-page嵌入架构**

**设计特点**：Agent代码直接运行在页面上下文，而非外部控制浏览器。  
**核心优势**：
- 直接访问DOM、JavaScript运行时和组件状态
- 对动态渲染内容感知能力更强
- 操作延迟更低（无跨进程通信开销）

### **🚀 使用方式与接入路径**

#### **(一) Chrome扩展（推荐新手）**
- **特点**：零代码、即装即用，支持自然语言指令操作任意网页
- **适用场景**：快速体验、非开发人员使用
- **文档链接**：官方提供详细安装配置步骤

#### **(二) npm集成（适合开发者）**

**安装命令**：
```
npm install page-agent
```
**基础使用示例**：
```javascript
import { PageAgent } from 'page-agent';  

// 初始化配置（需LLM支持）
const agent = new PageAgent({  
    model: 'qwen3.5-plus',  
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',  
    apiKey: 'YOUR_API_KEY',  
})  

// 自然语言执行操作
await agent.execute('在搜索框中输入"TypeScript"，然后点击搜索按钮');  
await agent.execute('找到价格最低的商品，加入购物车');
```
### **📈 核心适用场景**

#### **(一) 自动化测试**
- **传统方式**：`await page.click('#login-btn');`（依赖选择器）
- **page-agent方式**：`await agent.execute('点击登录按钮，在用户名输入框填入testuser');`（自然语言描述）
- **价值**：页面改版无需同步修改测试脚本，维护成本降低

#### **(二) RPA流程自动化**

适用于企业级重复性网页操作：填表、数据录入、报表导出，无需编写复杂脚本。

#### **(三) AI Agent工具调用**

作为AI Agent系统的底层工具，支持动态查询网站数据、填写表单，无需为每个网站开发专用爬虫。

#### **(四) 无障碍辅助**

通过自然语言指令降低复杂UI操作门槛，提升特殊用户群体使用体验。

### **🔬 与同类方案技术对比**

| 方案 | 控制方式 | 需要选择器 | 核心定位 | 典型应用场景 |
| :--- | :--- | :--- | :--- | :--- |
| Playwright/Puppeteer | 外部控制浏览器 | 是 | 精确控制 | 传统自动化测试 |
| 浏览器扩展方案 | 注入扩展 | 部分需要 | 用户侧辅助 | 简单页面操作 |
| **page-agent** | **in-page嵌入** | **否** | **意图理解** | **AI Agent集成、自然语言自动化** |

**补充说明**：传统工具在需要精确控制的复杂场景中仍具优势，page-agent更适合需灵活性和LLM集成的场景。

### **📊 项目当前状态**
- **基础信息**：9599 stars，阿里出品，TypeScript实现
- **更新时间**：最近更新于2026年3月
- **生态定位**：阿里AI Agent基础设施布局的重要组件，与OpenSandbox（Agent沙箱）形成互补
- **GitHub地址**：https://github.com/alibaba/page-agent

### **📝 关键洞察**
- **技术突破**：page-agent通过in-page架构解决了传统自动化工具对DOM结构的强依赖问题，实现了从"规则驱动"到"意图驱动"的跨越。
- **生态意义**：作为阿里Agent技术栈的关键环节，填补了"AI如何理解并操作网页UI"的能力空白。
- **应用前景**：在AI Agent快速发展的背景下，自然语言驱动的Web自动化可能成为RPA和测试领域的标准配置。