---
title: insight 20260616 ClaudeCode AI编程助手使用指南  
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# ClaudeCode AI编程助手使用指南 🚀

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1889189502065480488
> **创建时间**: 2025-10-03 06:40:31
> **更新时间**: 2025-10-03 06:40:31
> **原始链接**: https://mp.weixin.qq.com/s?chksm=fbbe8b4fccc902592f46fe9f5b30f9475c3bb8bebb9aaac9093bc895d1f0df4dbaf54b280863&exptype=unsubscribed_card_recommend_article_u2i_mainprocess_coarse_sort_tlfeeds&ranksessionid=1759444773_1&req_id=1759444773810683&scene=169&mid=2247486287&sn=3eb4fb392d8ef9313ca3cd38e00d2aef&idx=1&__biz=MzU0ODM5NTM3NQ%3D%3D&sessionid=1759444371&subscene=200&clicktime=1759444814&enterid=1759444814&flutter_pos=45&biz_enter_id=5&jumppath=20020_1759444649992%2C1104_1759444699165%2C20020_1759444707738%2C1104_1759444747567&jumppathdepth=4&ascene=56&devicetype=iOS18.7&version=18004028&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQo90xS6W5tjTrNj%2B0JEH58RLXAQIE97dBBAEAAAAAAFsIEA08ro0AAAAOpnltbLcz9gKNyK89dVj07%2FU2Y0mjFpoP8CZbJ0hUtNISQkajIg1uaD%2FSLZWbXAE%2Fq0YqGlJF4OwF0mk1PufKu%2Frt724ybxciRCUpExphWhnXe0Jx2Y75tjx8hlPkLpCIvYiRSF1AB90leunhcJyAfEA1QxsLDRTNvw2FUFuZck2IAdiJL%2BZTQSuxS4Qjn7ZtWFRYahRL4aoPG0ThH9RxmkAhmf6fE1ymewPl3arzzymtrmmwASGQVFP5Nrc8XXjA&pass_ticket=Vd9RGuNnEnN8MYr4CIfAezirUxF6Vzk7YARspElS%2FQHqYuvarqk5wPINMwrmMNge&wx_header=3

---

### 一、核心定位与优势

💡 **第二代AI编程助手**  
- 命令行界面（CLI）设计，适配程序员操作习惯  
- 支持全项目理解与多任务处理，可直接编辑文件/运行命令  
- 对比传统IDE插件：从"代码补全工具"升级为"端到端开发伙伴"，能处理需求分析→实现→验证全流程  

📊 **性能测试数据**  
| 评估维度         | Claude Opus 4.1 | OpenAI o3 | Gemini 2.5 Pro |
|------------------|-----------------|-----------|----------------|
| 工程编码能力     | 74.5%           | 69.1%     | 67.2%          |
| 终端编码能力     | 43.3%           | 30.2%     | 25.3%          |
| 研究生级推理能力 | 80.9%           | 83.3%     | 86.4%          |

### 二、安装与国内配置方案

#### 基础安装
```bash
npm install -g @anthropic-ai/claude-code  # Node.js ≥18
claude  # 启动程序（首次需登录）
```
#### 国内访问解决方案

🔑 **环境变量配置法**（推荐）  
1. **智谱GLM4.5**（首月20元）  
   ```bash
   export ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
   export ANTHROPIC_AUTH_TOKEN=你的APIKEY  # 需在bigmodel.cn注册获取
   ```
2. **Kimi K2**（需充值50元解锁速率）  
   ```bash
   export ANTHROPIC_BASE_URL=https://api.moonshot.cn/anthropic/
   export ANTHROPIC_AUTH_TOKEN=你的APIKEY
   ```
🔄 **ClaudeCodeRouter转接方案**  
支持将OpenAI格式模型（如Qwen/Doubao）接入：  
```bash
npm install -g @musistudio/claude-code-router
ccr ui  # 启动可视化配置界面
```
### 三、核心功能与使用技巧

#### 1. 高效操作符号
- `@文件名`：指定文件进行操作  
- `#指令`：设置记忆规则（如`#变量命名需体现含义`）  
- `!命令`：切换bash模式执行系统命令  
- `ESC`：中断当前任务  

#### 2. 关键指令详解

| 指令         | 功能描述                                  |
|--------------|-------------------------------------------|
| `/init`      | 生成项目文档CLAUDE.md，帮助AI理解项目结构 |
| `/compact`   | 压缩对话历史，节省上下文空间              |
| `/memory`    | 编辑编码规则（全局/项目级）               |
| `/agents`    | 管理子智能体系统                          |
| `/hooks`     | 配置事件触发钩子（如自动格式化代码）      |

#### 3. 子Agent系统案例

📋 **创建UX设计师Agent流程**  
1. 运行`/agents` → `Create new agent`  
2. 描述需求："创建UX设计师，负责界面设计"  
3. 自动生成专业提示词，支持并行协作  

🎯 **应用场景**：一次性完成"UX设计→前端实现→后端开发"全流程，主智能体自动分配任务给子Agent

### 四、高级应用与最佳实践

#### 结构化提示词模板
```xml
<instruction>实现用户认证API</instruction>
<context>使用Node.js+Express，需支持JWT验证</context>
<code_example>// 参考代码片段
app.post('/login', (req, res) => { ... })</code_example>
```
#### 三种工作模式切换（Shift+Tab）
- **正常模式**：操作需用户批准  
- **自动接受模式**：完全信任AI决策  
- **计划模式**：仅生成执行计划不实际操作  

### 五、资源与工具链
- **官方中文文档**：https://docs.claude.com/zh-CN/docs/claude-code  
- **自定义指令库**：https://www.buildwithclaude.com/（174+指令模板）  
- **代码回退工具**：`npm install -g ccundo`  
- **钩子生成工具**：claudecode-rule2hook（自然语言转钩子配置）