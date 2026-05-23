# Harness工程：AI Agent可靠开发的系统方法论

能力框架: capability-tech-understanding #capability-requirement-decision
标签: #Harness #AI-Agent #工程方法论 #Anthropic

> **来源**: Get笔记 - AI链接笔记
> **原文标题**: Harness工程：AI Agent可靠开发的系统方法论与实践指南
> **评级**: ⭐⭐⭐⭐⭐ (5/5)
> **日期**: 2026-05-12
> **Tags**: #tech-understanding #requirement-decision #Harness #Claude-Code

---

## 一、Harness定义与本质

### 核心定位

> **Harness是AI智能体的运行时控制层**，负责连接模型（大脑）、Agent（身体）和Skills（标准），实现稳定、可控的连接。

### 功能本质

解决"模型能聊但做不了事"的关键问题：
- 权限控制
- 工具调度
- 任务恢复
- Agent通信

### 命名来源

源自Anthropic在Claude Code技术博客中的"马具"比喻，强调对模型能力的引导与控制。

---

## 二、四大核心管理范畴

### 1. 权限控制

| 实现 | Claude Code | Hermes Agent |
|:---|:---|:---|
| **机制** | pattern-based权限白名单 | 工具分组按平台单独开关 |
| **审批** | 弹框确认非白名单操作 | 危险命令由独立AI模型审批 |

### 2. 工具调度

| 实现 | Claude Code | Hermes Agent |
|:---|:---|:---|
| **机制** | hooks + MCP servers | SQLite任务账本 |
| **能力** | - | 子任务恢复与父任务追溯 |

### 3. 记忆管理

| 实现 | Claude Code | Hermes Agent |
|:---|:---|:---|
| **特点** | 简化设计 | OTEL全链路追踪，50+项自诊断 |

### 4. 安全机制

| 实现 | Claude Code | Hermes Agent |
|:---|:---|:---|
| **机制** | 弹框确认 | 并发审批带线程锁 |

---

## 三、Agent与Chatbot的本质区别

| 类型 | 模式 |
|:---|:---|
| **Chatbot** | "输入一段话，输出一段话" |
| **Agent** | "理解意图→检查权限→加载Context→执行动作→观察结果→更新记忆→调整策略"的闭环 |

> **该闭环通过Harness实现稳定运转。**

---

## 四、大脑：模型的选择

| 模型 | 核心优势 | 适用场景 |
|:---|:---|:---|
| **DeepSeek V4 Pro** | 开源顶级复杂推理与Agent能力 | 复杂任务、Agent系统 |
| **Kimi K2.6** | 长上下文与工程工作流 | 文档处理、工作流自动化 |
| **Qwen 3** | 均衡与工程化能力 | 通用场景 |

### 选型原则

> **"什么任务用什么模型"**

---

## 五、身体：Agent的选择

### 三大品类

| 品类 | 代表产品 | 核心特点 | 适用场景 |
|:---|:---|:---|:---|
| **终端编程Agent** | Claude Code | 命令行和Plan Mode见长 | 多文件重构、架构设计 |
| **自主Agent** | Hermes Agent | 7×24后台运行，持久记忆 | 消息处理、定时周报 |
| **IDE编程Agent** | Cursor、Cline | 嵌入编辑器，视觉反馈快 | 轻量重构、深度编程 |

---

## 六、自进化：当Agent开始互相学习

### 多Agent协同进化

```
Claude Code（执行层）←→ Hermes Agent（记忆层）
         ↓
    Harness桥接
  hooks + shared memory + Skills
```

### 进化表现

积累Bug模式库 → 关联根因 → 生成预防规则 → 减少重复错误

---

## 七、认知更新

### 旧认知
- Harness是给Agent兜底的补丁
- Prompt是主要资产

### 新认知
- **Harness是AI时代的软件工程接口**
- "Prompt是消耗品，系统才是资产"

---

*🕵️ 尼克·弗瑞 | 情报分析师*
*来源: Get笔记 | 2026-05-12*
