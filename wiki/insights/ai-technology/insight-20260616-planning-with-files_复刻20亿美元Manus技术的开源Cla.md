# planning-with-files：复刻20亿美元Manus技术的开源Claude Skill深度解析

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1898194470085755504
> **创建时间**: 2026-01-08 08:16:01
> **更新时间**: 2026-01-08 08:16:01
> **原始链接**: https://mp.weixin.qq.com/s?__biz=Mzg4MzYxODkzMg==&mid=2247506305&idx=1&sn=a3933430c2b90d421268feec417df3f9&chksm=ceaf51e372ed5941f55150f7205495790f4fb08d37a03346c3fa5065be421189aee5b02bf090&scene=90&xtrack=1&req_id=1767831112601614&sessionid=1767831259&subscene=93&clicktime=1767831295&enterid=1767831295&flutter_pos=9&biz_enter_id=4&ranksessionid=1767831259&jumppath=1001_1767831212858%2C1101_1767831215536%2C1001_1767831248267%2C1104_1767831260047&jumppathdepth=4&ascene=56&devicetype=iOS26.3&version=1800432b&nettype=3G+&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQ1w5g1q016IkH565Xts3cdxLXAQIE97dBBAEAAAAAABdZBXzwijQAAAAOpnltbLcz9gKNyK89dVj0ChThneF7w8W86%2BDyoq2HBt3gP6x%2BZBzuwID%2FlS8SeCyW9knZAVgKMceOrrdwDyM7%2BWM4xF%2BFJu3mMYOU1Vq2689WN6yPDRlg5UIQj%2FgKh8NsNFHvMACNR9M2gF5Dq2erv7UbH1Ks3fkq%2BDrufSvbggLj3nxesLjLGX%2BqhGo9cN3lYX36Ooectj4ZiwDVqaqeG39TZRa78XY1XZHrtv2UczOFirLl%2B%2B6NqTlX7ILVAup1&pass_ticket=5TnsV5r0RsO%2BflwK5ziiTYE1J7XTwwGwdJYpHU5Taz4225kFyWDRm9Eu2dwMuRLU&wx_header=3

---

### **🚀 项目爆火概况（背景）**

**核心数据**
- **发布表现**：开源社区4天收获**3.3k Star**，且持续增长。
- **核心价值**：通过**Claude Skill**形式，用**几百行指令+三个Markdown文件**，在本地终端模拟Meta斥资**20亿美元**收购的Manus公司核心技术——**上下文工程（Context Engineering）**。
- **项目地址**：[https://github.com/OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)

### **🧠 Manus的六大上下文工程原则（理论基础）**

Manus公司的核心竞争力在于重新定义模型与上下文交互方式，其六大原则被planning-with-files完整复刻：

| 原则编号 | 原则名称 | 核心原理 |
| :--- | :--- | :--- |
| 1 | **文件系统作为外部记忆** | 不依赖易失的Context Window，将磁盘视为无限“外挂内存”，仅在Context中保留文件路径 |
| 2 | **通过重复进行注意力操纵** | 对抗“Lost in the Middle”现象，在关键决策前反复读取计划文件，刷新模型“注意力权重” |
| 3 | **保留失败痕迹** | 显式记录失败尝试，让模型通过“反思”避免死循环，而非掩盖错误 |
| 4 | **避免少样本过拟合** | 在重复性任务中引入受控变体，防止模型陷入机械式幻觉 |
| 5 | **稳定前缀优化缓存** | 通过固定文件结构和前置指令，最大化KV-Cache命中率，降低Token成本 |
| 6 | **只增不改的上下文** | 以追加（Append）而非修改（Modify）方式更新信息，维护上下文连贯性 |

### **🏗️ 架构落地：三文件模式（核心设计）**

planning-with-files将抽象原则具象化为**“三文件工作流”**，强制Claude在任务执行时维护以下文件：

#### **1. `task_plan.md`（指挥塔 寄存器）**
- **定位**：架构核心，存储**元数据**而非具体知识。
- **作用**：定义目标、拆解阶段、追踪进度、记录错误。
- **关键机制**：Agent的“罗盘”，**必须在每次行动前读取此文件**。

#### **2. `notes.md`（知识库 堆内存）**
- **作用**：存储调研笔记、网页摘要、中间代码。
- **关键机制**：**“Store, Don't Stuff”**（存储而非填充），禁止将大量资料直接输出到对话框，必须写入此文件以保持对话上下文清爽。

#### **3. `[deliverable].md`（产出物 IO缓冲区）**
- **作用**：存储最终交付结果（如`game.py`或`report.md`）。
- **关键机制**：物理隔离“思考过程”与“最终结果”。

### **🔄 三文件工作流程（运行机制）**

三文件构成**基于文件的状态机（File-Based State Machine）**，通过四阶段闭环实现任务管理：

#### **阶段0：协议握手与状态机初始化**
- **触发条件**：Claude Code识别复杂任务，Skill自动激活。
- **核心动作**：创建`task_plan.md`，定义`Goal`（全局指令）、`Phases`（指令流水线）、`Status`（当前指针位置），使无状态LLM首次获得“状态”。

#### **阶段1：Read-Before-Decide（对抗遗忘）**
- **核心动作**：开始任何工作前，强制执行`read_file task_plan.md`。
- **价值**：确保Context尾部注入最新状态（如“当前处于Phase 2，目标是修改Login接口”），相当于CPU时钟周期开始时强制执行**Fetch Instruction**。

#### **阶段2：Data Offloading（数据卸载）**
- **传统模式问题**：搜索结果全文塞入对话框，燃烧Token且淹没模型。
- **本模式优化**：提炼核心参数写入`notes.md`，对话框仅提示“协议参数已存入notes”，类似操作系统**Swap机制**（换出不常用数据到磁盘，保持主存清爽）。

#### **阶段3：State Commit（状态固化）**
- **核心动作**：任务完成后，必须编辑`task_plan.md`：
  - 将`[ ] Phase 2`改为`[x] Phase 2`
  - 更新`Status`到`Phase 3`
- **价值**：赋予LLM**时间感**，明确区分“过去”（已完成）与“未来”（待完成）。

### **🎯 解决的四大LLM痛点（问题与方案）**

| 痛点 | 现象 | 解决方案 |
| :--- | :--- | :--- |
| **易失性记忆** | 多轮对话后遗忘变量或需求 | **文件系统持久化**：即使对话Session重置，`notes.md`和`task_plan.md`可恢复记忆 |
| **目标漂移** | 执行50步后沉迷细节，忘记原始目标 | **Read-Before-Decide**：行动前读取计划，利用Transformer近因效应保持目标注意力 |
| **隐藏错误** | API调用失败后默默重试，导致死循环或成本爆炸 | **Error Persistence**：`task_plan.md`设“Errors Encountered”章节，显式记录所有失败 |
| **上下文填充** | 无关信息塞满Context，导致模型变笨、变慢、变贵 | **Offloading**：长文本默认存入`notes.md`，Context仅保留文件路径和关键点 |

### **💻 Skill技术剖析（实现细节）**

该Skill未修改Claude模型权重，完全通过`SKILL.md`中的Prompt Engineering实现：

#### **1. 自动触发机制**

YAML头部定义元数据，当用户输入“帮我规划...”“研究...”或“这个任务很复杂”时，Claude语义匹配`description`字段自动挂载Skill。

#### **2. 负面约束（Critical Rules）**

通过强命令语气在System Prompt层级锁定Agent行为：
- **ALWAYS Create Plan First**：非谈判条款，复杂任务必须先创建`task_plan.md`
- **Read Before Decide**：重大决策前必须读取计划文件
- **Update After Act**：完成阶段后立即更新计划状态
- **Store, Don't Stuff**：大输出存入文件而非上下文
- **Log All Errors**：所有错误必须记入“Errors Encountered”章节

#### **3. 循环定义**

显式定义`Read Plan -> Act -> Update Plan`闭环逻辑，将Agent从线性问答机器转变为有状态循环执行者。

### **📦 安装与使用指南（实操步骤）**

#### **安装**

在终端运行（需已配置Claude Code）：
```bash
cd ~/.claude/skills  
git clone https://github.com/OthmanAdi/planning-with-files.git
```
#### **验证**

重启Claude Code，输入`> /skills`，确认`planning-with-files`出现在可用Skill列表。

#### **使用示例**

输入任务：`“研究一下Rust语言在嵌入式开发中的优势，并写一份报告。”`  
Claude将自动：
1. 创建`task_plan.md`  
2. 规划“搜索”“阅读”“撰写”三阶段  
3. 执行搜索并将结果写入`notes.md`  
4. 完成后更新`task_plan.md`的Checkbox  
5. 生成最终报告存入`report.md`

### **📝 补充细节**
- **Manus收购背景**：Manus是一家AI Agent创业公司，因上下文工程技术被Meta以**23亿美元**收购，其核心价值在于重新定义模型与上下文交互方式而非更强模型性能。
- **Skill核心创新**：通过纯Prompt Engineering实现状态机机制，证明在不修改模型权重的情况下，通过**认知架构（Cognitive Architecture）** 优化可显著提升LLM复杂任务处理能力。