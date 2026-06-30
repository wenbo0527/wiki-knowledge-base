# #2 The Eight Levels of AI Adoption - 人工智能采用的八个层级

**源**: 刀哥 KB `2eYxaj0z` | note_id `1912234232845225048` | 2026-06-08 | tags: AI Adoption, Chatbot
**链接**: https://kb.daode.com/note/1912234232845225048
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐（客户分级框架的直接素材）

---

## 🎯 核心 Insight

**8 层级采用模型**（更高 ≠ 更好，按任务信任度选择）：

| 层级 | 名称 | 描述 | 典型工具 |
|:---:|:---|:---|:---|
| 1 | Chatbot | 单次问答 | ChatGPT, Claude |
| 2 | Copilot | AI 嵌入文件协同 | Cursor, Claude in Excel |
| 3 | Agent | 分步执行需批准 | Cowork, Codex |
| 4 | Autopilot | 独立完成供审核 | **Claude Code**, Lovable, Codex |
| 5 | Workflows | 系统化流程优化 | Compound engineering |
| 6 | Assistant | 后台主动工作 | **OpenClaw**, Hermes |
| 7 | Multi-agent | 多 agent 长期运行 | Claude Managed Agents, OpenClaw |
| 8 | Orchestrator | 管理代理协调子代理 | Gas Town, Paperclip |

**关键论断**：
- 知识工作者最佳区间：**Level 1-4**
- 工程师更多处于：**Level 5-8**（因为能搭系统支架）
- 层级选择原则：**对 AI 自主信任度 + 任务失败影响**

---

## 🔧 对钟离可借鉴的部分

### 1. 客户分级工具（钟离的咨询/PM 工作）

**当前**：钟离帮文博做 AI 诊断器 PRD，没有客户分级模型  
**改进**：用 Eight Levels 给客户 AI 成熟度打 1-8 分，决定服务深度

```
Level 1-2: 只回答问题，不做定制（"AI 是什么"）
Level 3-4: 提供 Agent 化 SOP，帮搭 Claude Code 项目（钟离当前工作）
Level 5-6: 提供 OpenClaw 部署 + Skills 开发（钟离下一步）
Level 7-8: 多 Agent 编排（暂不接，需钟离升级自己）
```

### 2. 我自己的 AI 采用层级评估

- 我目前用 Claude Code 处理 `~80%` 任务 = **Level 4 (Autopilot)**
- 但还在手动写 patch script = **Level 2 (Copilot)**
- 应该把所有重复 3+ 次的任务升级到 Level 4+

### 3. 重要警句

> "高层级不一定更好，应根据任务性质、信任度和风险后果选择合适层级"

钟离的判断：把"架构评审"放 Level 3（agent 起草 → 我审），把"代码生成"放 Level 4（Claude 独立完成）

---

## 🚦 立即可执行

- [ ] 给文博的 AI 诊断器客户做个 **Eight Levels 自评问卷**（5 分钟可填）
- [ ] 我自己的高频任务清单 → 标注每个任务应该放哪个层级
- [ ] 写一篇"钟离的 Eight Levels 实战解读"挂到 MEMORY.md

## 🟡 本周可执行

- 和 Tony 讨论：把 Eight Levels 加进 task_board 的"客户分级"字段

---

*🛡️ 钟离 · 18:52 · 2026-06-23*  
*消化: Nick 派单 #2/15*