# AgentForge：零门槛Agent创建与部署平台技术解析

> **来源**: Get笔记
> **知识库**: ai-practice
> **导入日期**: 2026-06-16
> **原始ID**: 1912575474440224496
> **创建时间**: 2026-06-12 08:38:35
> **更新时间**: 2026-06-12 08:38:35
> **原始链接**: https://mp.weixin.qq.com/s/6Bs2mLC-o7qiUllx5zJ8xQ

---

### **🚀 核心产品定位（背景）**

**产品概述**
- **核心价值**：实现**零门槛创建、部署、共享Agent**，无需代码、无需Prompt工程、无需关心底层技术。
- **关键指标**：生产一个线上可运行的云端Agent Team仅需**1分13秒（73秒）**。
- **目标用户**：覆盖非技术同学、前端/Node技术同学、Java同学（集团主力）及所有想尝试AI应用的用户。

### **🎯 目标用户痛点分析（问题）**

| 用户类型 | 核心痛点 | 具体表现 |
| :--- | :--- | :--- |
| **非技术同学** | 有AI自动化需求但技术门槛高 | 不懂代码/Prompt结构/MCP对接/容器部署，想法无法落地 |
| **前端/Node技术同学** | 重复劳动多，开发效率低 | 每个Agent需从零搭建Dockerfile、容器适配、启动脚本等基础架构 |
| **Java同学** | 跨语言生态适配困难 | Agent生态以Node/Python为主，需自学新语言或自建简陋框架 |
| **所有用户** | 共享与协作能力不足 | 个人助手无法多人共享，平台太轻或框架太重（如OpenAI Agents SDK需写代码） |

### **🔧 解决方案：AgentForge平台功能（产品）**

#### **(一) 核心定位**

「Agent工厂」型平台，支持用户通过自然语言描述需求，流式生成Agent人设、技能链、工具装备，并提供调试、部署、共享全流程支持。

#### **(二) 分角色功能设计**
1. **非技术同学：5分钟出真Loop Agent**
   - **描述生成**：一句话需求→自动生成7层Prompt（SOUL/USER/AGENTS/SKILL_CHAIN/TOOLS/MEMORY等）
   - **技能扩展**：上传ZIP文件或Markdown即可添加新技能，支持自动校验与沙盒预检
   - **调试部署**：同一页面切换「装备/对话」模式，SSE事件流可视化路由与工具调用，一键部署完整生产闭环

2. **Node技术同学：直接上生产的全链路SOP**
   - 提供Dockerfile容器配置、Aone容器适配、Egg启动脚本等企业级模板
   - 基于**Anvil Agent框架**（独立可部署运行时）和**Anvil-Multi**（多Agent仓库支持）

3. **Java同学：无痛复用Agent架构**
   - 提供HTTP API（POST /api/chat）、钉钉机器人、MCP反向调用三种复用通道
   - 跨Session记忆中心化，零Node依赖、零LLM SDK key、零Maven pom修改

4. **小团队：Agent战队编排**
   - **可视化画布**：拖拽已有Agent组成Manager+Worker战队，支持hub-and-spoke拓扑与handoff路由
   - **协议化互通**：共享记忆/技能装备，支持跨团队组合（如客服+行程规划+设计师组成旅游业务team）

### **📋 使用流程（操作）**
1. **新建Agent**：选择SOLO（单个Agent）或TEAM（Agent战队）模式
2. **描述生成**：输入需求→平台生成系统提示词、推荐SKILL与MCP草稿
3. **装备配置**：可视化界面配置技能链与工具装备
4. **调试使用**：实时对话调试，查看SSE事件流与记忆召回
5. **私有化部署**：一键部署至GitLab仓库，支持dev/pre/prod多环境配置

### **🛠️ 核心技术资产（技术）**

| 技术模块 | 功能描述 | 技术优势 |
| :--- | :--- | :--- |
| **fliggy-memory-sdk** | 飞猪自研Agent长期记忆SDK | 对标mem0，支持namespace隔离、catalog注入、topK召回、事实抽取等集团适配功能 |
| **FECHO** | 集团HSF自动转MCP网关 | 实现集团所有RPC接口的Agent调用，突破能力边界至集团服务全集 |
| **ANVIL/ANVIL MULTI** | 自研Agent运行时框架 | 支持单/多Agent部署，覆盖鉴权、模型调用、MCP集成等全链路生产闭环 |
| **chatLoop** | ReAct+Function Calling主循环 | 2200行核心代码+5子模块懒加载，提供SSE事件暴露与标准化hook点 |
| **7层Prompt模板** | SOUL/USER/AGENTS等分层设计 | 权责分离，支持独立编辑/版本/复用，适配复杂Agent协作 |

### **🌐 生态串联（集成）**
- **自研能力**：编排协议+TeamCanvas、ANVIL框架、FECHO网关、AgentBuilder、fliggy-memory-sdk
- **集团生态**：Aone容器、HSF服务、ali-skills仓库、BUC鉴权、SchedulerX调度、钉钉机器人

### **📈 成果与规划（价值）**

**当前成果**：
- 稳定运行并私有化部署多个业务线Agent（客服路由助理/研发任务派单/辩论赛庭等）
- 完整打通BUC鉴权/Aone部署/SchedulerX调度/钉钉机器人/集团MCP服务链路

**未来规划**：
- 短期：将Agent创建门槛降至纯业务同学5分钟上手
- 中期：构建Agent生态，实现跨团队能力乐高式组合