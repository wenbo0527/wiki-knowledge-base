# Agent工程思考：从ReAct循环走向Agent Harness产品化体系

> 来源: Get 笔记
> 知识库: ai-practice (AI实践日志)
> KB 等级: ⭐self
> KB ID: K0BVyZM0
> 原始 ID: 1916933568090377992
> 创建时间: 2026-07-29 08:05:06
> 同步时间: 2026-07-30T06:00:47.459077

### **🎯 核心总论点是什么？**

Agent工程不能停留在ReAct的model+loop阶段，要走向**Agent Harness**，把模型行为落地成产品可依赖的软件事实，满足可恢复、可控制、可展示、可追溯的要求。
- 作者为**vivo互联网项目团队-丁俊杰**，调研了codex、lobehub、goose、opencode、PI、Flue等多款优秀Agent产品后提出该体系。

### **⚠️ 现有ReAct模式存在哪些产品痛点？**

纯ReAct循环仅能跑通demo，落地真实产品会遇到大量运行时问题。
- 典型运行时问题清单：
  - 用户刷新页面后，之前的工具审批状态丢失
  - 后端进程中途重启，无法从断点恢复执行
  - 后台运行的子Agent无法在主线程正常展示状态
  - 生成的artifact（产物）没有明确的引用、状态和归属记录
  - 用户点击stop后，无法精准控制哪些任务取消、哪些保留
- ReAct仅解释模型微循环（Thought/Action/Observation），完全不定义产品系统需要的事实边界（event/state/checkpoint/control）。

### **🔍 ReAct的解释边界到底在哪里？**

ReAct的最小单元是Thought→Action→Observation，仅面向模型推理链路。
- **Observation的定位**：它是给模型看的输入，仅用来补充模型上下文，本身只是一段返回文本。
- 真实产品工程中，单次工具调用会被拆分为多段事件：run.started、message.created、assistant.text.delta、tool.call.created、tool.approval_required、tool.call.running、tool.call.completed、artifact.created、run.finished。
- 产品系统不能只依赖Observation文本，否则前端要从文本猜状态、后端靠临时字段补状态，多处推导逻辑会出现一致性问题。

### **🛠️ Agent Harness的核心职责是什么？**

为Agent产品定义统一的事实协议，所有运行事实必须在runtime运行路径上产生，而非事后由UI adapter拼接生成。
- 传统事后拼接方案的缺陷：ReAct循环跑完后，UI adapter从message、observation、tool result里反向推导isBusy、pending-Approval、artifactRefs等状态，事实是事后重建的，极易出现状态失真。
- Harness必须直接覆盖的核心问题清单：
  1. 当前谁在运行、运行卡在哪里
  2. 哪个状态可以恢复、哪个动作需要用户审批
  3. 哪个结果可以被检查、哪个artifact属于哪次运行
  4. 哪个子Agent是谁派生出的、用户可发送哪些控制命令
  5. 刷新、重连、进程重启后，系统如何回到同一个现场
- 核心判断标准：同一个运行事实，绝对不应该从多个来源拼接生成。

### **📐 从Loop到协议的数据流怎么设计？**

明确拆分state、view、control三个层级的分工与边界，形成前后端共享的标准化数据流。
- 两条核心数据流链路：
  1. runtime event → agent.state → agent.view → UI
  2. user action → agent.control → runtime event
- 各层级明确定义：
  - **state（事实层）**：由runtime和明确业务边界生成，包含messages、activeRun、checkpoint、pendingApproval、todos、subagents、artifactRefs、workspaceContext等核心运行数据，不属于前端展示缓存。
  - **view（派生层）**：完全从state计算派生，包含isBusy、canStop、waitingForFirstToken、approvalBanner、toolBadges、subagentGroups、messageProjection等展示相关状态。
  - **control（命令层）**：仅负责下发操作指令，包含invoke(input, stateSnapshot)、resume(approvalDecision)、stop(runId)、updateState(patch)、reload(threadId)等接口，不直接修改展示状态。
- 说白了，runtime只负责写事实，UI只负责读事实，谁也不能越界改对方的核心数据。

### **📋 State Schema如何定义事实边界？**

开发Agent时要先设计state schema，再写prompt、选工具和模型，避免运行事实被迫散落在message、工具结果或前端缓存中。
- 一等事实判定规则：影响恢复、审批、继续执行、跨端一致、审计和可检查结果的内容，必须进入state。
- 三类典型落地场景：
  1. **审批场景**：将pendingApproval写入state，包含id、runId、turnId、toolCallId、toolName、arguments、policy字段，用户通过control.resume提交审批决策，runtime从checkpoint继续执行后写回新state。
  2. **artifact场景**：产物的内容本体可存放在文件系统/对象存储中，但artifact的引用、状态、归属必须进入state，包含id、type、title、status、ownerRunId、createdByToolCallId、contentRef字段，支持全链路通过引用定位产物。
  3. **子Agent场景**：子Agent的运行关系必须进入state，包含id、parentRunId、parentTurnId、title、status、startedAt、completedAt、resultRef、error字段，前端从state派生分组、徽标、进度文案、跳转目标。
- 仅改变展示方式的内容，全部留在view层，不需要进入state。

| State（一等事实） | View（派生展示） |
| :--- | :--- |
| checkpoint | isBusy |
| pendingApproval | approvalBanner |
| artifactRef | toolBadges |
| subagent status | subagentGroups |

### **🚫 UI层的工程边界规则是什么？**

UI绝对不能“补写事实”，只能消费runtime写入的state，再派生view完成渲染，否则刷新、恢复、归属逻辑都会失真。
- 错误反例：UI从message文本中识别出“需要审批”字样，本地创建pendingApproval状态，刷新后审批状态直接丢失，后端也不知道任务停在哪个tool call节点。
- 正确路径：runtime生成tool.approval_required事件 → 写入state.pendingApproval → 派生view.approvalBanner → UI渲染出批准/拒绝按钮。

### **✅ 系统验收的核心标准有哪些？**

所有验收项都指向“运行事实有明确稳定归属”这一核心要求。
- 刷新页面后，pendingApproval仍然存在且指向同一个toolCall
- 进程重启后，能从checkpoint resume到同一个run/turn
- 用户点击stop后，activeRun终止，后端不会继续执行后续tool call
- artifactRef存在时，内容可被定位，可追溯到ownerRunId和toolCallId
- 子Agent完成后，主turn能拿到resultRef并正常展示归属关系

### **📝 补充细节**
- 最终分工结论：ReAct负责“让模型动起来”，Harness负责“让Agent在产品里可被信任”。
- 文中明确指出，Agent Harness最核心的工程问题不是skill安装、mcp加载、记忆设计，而是**事实应该在哪里产生**。