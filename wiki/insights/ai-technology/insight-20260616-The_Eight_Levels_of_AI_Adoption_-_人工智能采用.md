# The Eight Levels of AI Adoption - 人工智能采用的八个层级指南

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1912234232845225048
> **创建时间**: 2026-06-08 16:21:49
> **更新时间**: 2026-06-08 16:21:49
> **原始链接**: https://every.to/guides/the-eight-levels-of-ai-adoption?loggedin=true#level-2-copilot

---

### **📋 核心概述**

本文提出了人工智能采用的八个层级模型，从基础的聊天机器人使用到全代理编排，每个层级代表不同程度的AI任务委托与信任。文章强调：**更高层级不一定更好**，应根据任务性质、信任度和风险后果选择合适层级；知识工作者当前的最佳区间为1-4级，工程师则更多处于5-8级。

### **🔍 八个AI采用层级概览**

| 层级 | 英文名称 | 描述 | 典型工具 |
| :--- | :--- | :--- | :--- |
| **1** | **Chatbot** | 人工给出任务，AI提供单次响应 | ChatGPT, Claude, Gemini |
| **2** | **Copilot** | AI嵌入文件系统，与用户协同完成工作 | Cursor, Claude in Excel, Gemini in Google Docs |
| **3** | **Agent** | 描述任务后，AI分步执行并需用户批准才能继续 | Cowork, Codex |
| **4** | **Autopilot** | 无需中间批准，AI独立完成任务后供用户审核结果 | Lovable, Codex, Claude Code |
| **5** | **Workflows** | 构建系统化流程以优化AI输出专业性 | Compound engineering, Claude Workflows, Copilot AI Studio |
| **6** | **Assistant** | AI在后台主动工作，无需人工提示触发 | OpenClaw, Hermes Agent, Claude Managed Agents |
| **7** | **Multi-agent** | 同时管理多个长期运行的独立代理 | Claude Managed Agents, OpenClaw, Codex Goals |
| **8** | **Orchestrator** | 由管理代理协调多个子代理团队执行任务 | Gas Town, Paperclip, Symphony |

### **📝 层级细节与优秀提示词（Level 1示例）**

#### **Level 1—Chatbot（聊天机器人）**

**定义**：基础问答模式，用户提供任务，AI返回单次响应，不嵌入文件或系统。  
**价值转变**：从完全人工操作到借助AI通用助手进行起草和信息综合。  
**适用场景**：基于草稿撰写内容、文档摘要、上传文件的问答处理。  

**优秀提示词示例1：会议跟进邮件**  
```
I need to send a post-meeting follow-up email to a client. Here are my rough notes, the decisions we made, and two risks we need to flag. Draft the email in a calm, confident tone and end with three clear next steps. Tell me if anything sounds unclear or unsupported before you start writing.
```- **输入**：会议笔记  
- **输出**： polished email draft（含信息缺失提示）  
- **人工判断**：确认语气、事实准确性及内容立场  

**优秀提示词示例2：PDF政策文档分析**  
```
I am uploading a 20-page PDF on our new benefits policy. Summarize the five changes employees will care about the most, and then answer these three questions: Who is affected, what specific policies does the new timeline impact, and what would likely confuse someone who is reading this quickly?
```- **输入**：PDF或文档集  
- **输出**：基于源材料的摘要和问题解答  
- **人工判断**：验证摘要事实性及模型对模糊信息的识别能力  

**升级时机**：当频繁从聊天会话中复制粘贴结果，且希望减少手动设置和上下文提供时。

### **📌 补充细节**
- **层级选择原则**：主要取决于对AI自主完成任务的信任度，以及任务失败的影响程度。高风险任务建议采用低层级人工监督，或投入资源在高层级实现同等质量控制。  
- ** adoption障碍**：多数用户面临的核心问题是AI输出质量不足或实现高质量的成本过高，安全升级需要持续实验或模型能力提升。  
- **角色差异**：知识工作者（Levels 1-4）与工程师（Levels 5-8）的使用差异源于后者具备构建系统支架的能力，可在技术成熟前实现高层级应用。