# Agent数据合成框架AgentFlow技术解析：设计思路与多场景实践

> **来源**: Get笔记
> **知识库**: ai-practice
> **导入日期**: 2026-05-22
> **原始ID**: 1910546283853287744
> **创建时间**: 2026-05-21 11:41:24
> **更新时间**: 2026-05-21 11:41:24
> **原始链接**: https://mp.weixin.qq.com/s/Ed9QXM0A6qogxafS-wN63g

---

### **🔍 引言**

本文发布于**2026年4月23日**，聚焦Agent数据合成框架**AgentFlow**的技术实现细节。该框架通过三阶段pipeline跨异构Agent环境生成高质量训练与评估数据，支持RAG、MM-Doc、Deep Research、GUI、Text2SQL、Data Analysis、Embodied Agent等任务场景，项目开源地址为：https://github.com/OpenDCAI/AgentFlow。

### **🏗️ 一、Agent数据合成框架AgentFlow设计思路**

#### **核心实现思路**

采用**三阶段pipeline**合成高质量agent训练数据：**Trajectory Sampling（轨迹采样）→ Trajectory Selection（轨迹筛选）→ QA Synthesis（问答合成）**。

##### **Stage1：Trajectory Sampling（轨迹采样）**
- **定义**：由LLM驱动的agent从seed input出发，在sandbox环境中迭代探索，每步执行tool call并记录observation，构建分支trajectory tree。
- **实现步骤**：Seed Inputs → LLM Agent → Tool Call → Execute → Observe  
- **关键特性**：并发扩展（Concurrent Expansion）、动作去重（Action Deduplication）、深度限制（Depth Limitation）、成本控制（Cost Control）。

##### **Stage2：Trajectory Selection（轨迹筛选）**
- **定义**：对所有root-to-leaf路径按多维度评分，筛选高质量内容。
- **实现步骤**：All Paths → Score → Select  
- **评分维度**：路径深度（Depth）、信息丰富度（Info Richness）、工具多样性（Tool Diversity）、质量检查（Quality Checks）。

##### **Stage3：QA Synthesis（问答合成）**
- **定义**：基于选中路径的observation，生成multi-hop、factoid QA pair，并内置质量检查。
- **实现步骤**：Selected Path → LLM → Multi-hop QA → Quality Check → 输出（Question、Answer、Tool Calls Trace、Grounded Facts）。

### **📊 二、多场景具体合成流程**

#### **1、RAG Agent（检索增强生成）**
- **应用场景**：文档问答、知识检索。
- **技术实现**：从本地RAG索引（DenseE5 + Faiss）检索文本块，LLM合成答案。
- **核心管道**（5阶段）：  
  Sandbox Setup → QA Synthesis → Trajectory Synthesis → Model Training → Inference & Evaluation  
- **参考文档**：https://github.com/OpenDCAI/AgentFlow/blob/main/examples/RAGAgent.md

#### **2、Doc Agent（文档理解Agent）**
- **应用场景**：跨页、跨表格推理（处理冗长及多模态元素文档的复杂多跳推理问题）。
- **核心工具**：

| 工具         | 描述                                                                 | 参数                                                                 |
|--------------|----------------------------------------------------------------------|----------------------------------------------------------------------|
| doc_search   | 在文档标题、段落、表格和图像标题中搜索关键字                           | key_words：关键字符串数组，max_search_results：每个关键字的最大结果（可选） |
| doc_read     | 阅读文档部分并使用视觉语言模型提取信息，同时处理文本和图像             | section_ids：部分ID数组，goal：提取目标，max_image_num：最大视觉输入（可选），max_text_token：最大文本长度（可选） |
- **实现流程**：Sandbox Setup → QA Synthesis → Trajectory Synthesis → Model Training → Inference & Evaluation  
- **参考文档**：https://github.com/OpenDCAI/AgentFlow/blob/main/examples/DocAgent.md

#### **3、Deep Research（深度研究Agent）**
- **应用场景**：多步搜索、信息整合（通过互联网搜索回答复杂多跳推理问题）。
- **核心工具**：

| 工具         | 描述                                                                 | 参数                                                                 |
|--------------|----------------------------------------------------------------------|----------------------------------------------------------------------|
| web_search   | 批量网络搜索，返回每个查询的结果                                       | query：搜索查询字符串的数组                                             |
| web_visit    | 访问网页并根据目标提取相关内容                                         | urls：URL数组，goal：提取目标                                           |
- **实现流程**：Sandbox Setup → QA Synthesis → Trajectory Rollout → Model Training & Serving（vLLM）→ Inference & Evaluation  

#### **4、Text2SQL（SQL生成Agent）**
- **应用场景**：数据库查询（自然语言转可执行SQL查询）。
- **核心工具**：

| 工具                 | 描述                                                                 | 参数                                                                 |
|----------------------|----------------------------------------------------------------------|----------------------------------------------------------------------|
| sql:list_databases   | 列出所有可以查询的可用数据库                                           | 无                                                                    |
| sql:get_schema       | 获取数据库的表结构（表、列、外键）                                     | db_id：数据库ID（必填），table_names：可选过滤器                         |
| sql:execute          | 在特定数据库上执行SQL查询（仅限SELECT/WITH/PRAGMA）                    | db_id：数据库ID（必填），query：SQL字符串（必填）                       |
- **实现流程**：Database Setup → Sandbox Setup → QA Synthesis → Model Training → Inference & Evaluation  

#### **5、Data Analysis（数据分析Agent）**
- **应用场景**：表格处理、统计计算（调用DS工具执行多步骤推理）。
- **核心工具**：

| 工具                 | 描述                                                                 | 参数                                                                 |
|----------------------|----------------------------------------------------------------------|----------------------------------------------------------------------|
| ds_inspect_data      | 扫描数据集目录并总结CSV模式/形状/缺失                                  | 无                                                                    |
| ds_read_csv          | 预览CSV的前N行                                                       | csv_file，max_rows                                                    |
| ds_run_python        | 在沙盒中运行Python（pandas/numpy/sklearn等）进行分析                   | code，return_vars（可选）                                              |

### **📝 补充细节**
- **技术共性**：所有Agent场景均遵循"环境配置→数据合成→轨迹生成→模型训练→推理评估"的标准化流程，确保跨场景一致性。
- **工具设计**：每个Agent场景配备专用工具（如DocAgent的视觉处理工具、Text2SQL的数据库交互工具），实现场景化能力定制。
- **开源资源**：项目提供完整的示例文档（如RAGAgent.md、DocAgent.md）及配置文件模板，降低二次开发门槛。