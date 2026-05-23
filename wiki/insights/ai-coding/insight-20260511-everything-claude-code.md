# everything-claude-code：AI编程工具的操作系统级解决方案
能力框架: capability-requirement-decision capability-tech-understanding #capability-data-driven #capability-risk-control

> **来源**: Get笔记个人笔记 | **发布时间**: 2026-05-11 | **分类**: AI Coding / Agent
> **Insight ID**: insight-20260511-everything-claude-code
> **维护者**: 尼克·弗瑞 | **更新**: 2026-05-11

---

## 📌 一句话判断

> Anthropic Hackathon冠军项目，GitHub 5万星标，通过30个专用Agent、136个Skill、60个Commands构建AI编程工具的"操作系统"，实现跨会话记忆积累和事件触发自动化。

---

## 项目核心概况

| 维度 | 数据 |
|:---|:---|
| 项目名称 | everything-claude-code（ECC） |
| 开发周期 | 10个月（2025年5月起） |
| 核心定位 | AI编程工具的操作系统 |
| 荣誉 | Anthropic Hackathon冠军 |
| GitHub | 50K+ Stars |
| 支持工具 | Claude Code、Codex、Cursor、OpenCode |

---

## 核心技术架构

### 核心组件

| 组件类型 | 数量 | 功能描述 |
|:---|:---:|:---|
| 专用Agent | 30个 | 任务分工单元（planner、code-reviewer等） |
| Skill | 136个 | 可积累的专业知识单元，定义领域规则与流程 |
| Commands | 60个 | 系统操作指令集 |
| Hooks | 29个 | 事件中断与自动化机制 |

---

## 创新工作机制

### Agent分工模式

将复杂任务拆解为专用Agent执行：
- **code-reviewer**：git diff → 上下文理解 → 审查清单 → 结构化报告
- 模拟专业审查员思维

### Hooks中断系统

| Hook类型 | 触发时机 | 功能 |
|:---|:---|:---|
| PreToolUse | 命令执行前 | 前置处理 |
| PostToolUse | 执行后 | 格式化结果 |
| Stop hook | 会话结束 | 自动提取经验 |
| SessionStart | 新会话开始 | 加载历史记忆 |

### 记忆持久化

通过Hooks系统实现跨会话记忆积累，解决AI单次使用的信息断层问题。

---

## 典型Skill设计

### content-engine Skill

**核心规则**：禁止跨平台分发相同内容，需针对不同平台特性重新生产

**执行逻辑**：将原始内容拆解为3-7个原子想法，再分别生成符合平台原生风格的版本

### article-writing Skill

**反AI模板化规则**：
- 禁用"In today's rapidly evolving landscape"等模板开场白
- 剔除"Moreover"、"Furthermore"等填充词
- 强制"先给证据再解释"的论证逻辑

---

## 可迁移逻辑

ECC虽为编程设计，但其底层框架可迁移至其他领域：

1. **跨会话记忆系统** - 解决AI使用的连续性问题
2. **专用Agent分工** - 实现复杂任务模块化处理
3. **事件触发自动化** - 通过Hooks实现流程节点控制
4. **Skill知识积累** - 将经验转化为可复用的知识单元

### 内容创作领域应用

- 爆款分析Agent：识别内容传播规律
- 标题优化Agent：提升标题吸引力
- 合规审查Hook：自动检查内容合规性
- 爆款模式Skill化：将成功经验沉淀为模板

---

## 核心哲学

> 将AI从"单次执行器"升级为"系统性工作流"，通过结构化设计释放工具潜力。

---

## 🔗 关联专题

- [[AI Coding]] - AI编程
- [[Agent Engineering]] - Agent工程
- [[Skills System]] - Skill系统

---

## 🏷️ 标签

`#everything-claude-code` `#ECC` `#AnthropicHackathon` `#AI编程` `#Skill系统` `#Hooks` `#跨会话记忆`

---

*本文档由尼克·弗瑞基于Get笔记整理*
*情报是决策的基础。我不收集信息，我生产洞察。*
