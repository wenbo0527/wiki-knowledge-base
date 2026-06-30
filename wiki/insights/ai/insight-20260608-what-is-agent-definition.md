# "什么是 Agent"：从能说到能做的范式跃迁

> **类型**: Insight（概念框架）  
> **来源**: Get笔记 2026-06-05 入库（培训逐字稿）  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #agent #definition #paradigm-shift #concept

---

## 一句话洞察

> **Agent = 能做事的 AI**——传统 AI 只能"说"（问答/生成），Agent 能"做"（调用工具/执行任务/改变世界）。这看似简单的"一字之差"，背后是**决策权下放 + 工具调用 + 状态管理 + 错误恢复**的完整工程。

## 核心定义（4 要素）

| 要素 | 含义 | 缺失会怎样 |
|:---|:---|:---|
| **决策权** | Agent 自己决定下一步 | 退化为问答 |
| **工具调用** | 能影响外部世界 | 退化为聊天 |
| **状态管理** | 跨步骤记忆 | 退化为单次交互 |
| **错误恢复** | 失败能重试/降级 | 退化为人工兜底 |

## 范式对比

```
传统 AI（问答/生成）：
  用户提问 → LLM → 文字回答（不改变世界）
  
Agent（能做）：
  用户目标 → LLM 决策 → 工具调用 → 状态更新 → 错误恢复 → 目标达成
```

## 我们 4 Agent 团队对照

| Agent | 决策权 | 工具 | 状态 | 错误恢复 | 完整度 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Nick**（研究）| ✅ | ✅ sessions_send/RAG/写文件 | ✅ MEMORY | ✅ fail-fast | 🟢 完整 |
| **钟离**（技术）| ✅ | ✅ spec-driven/code-review | ✅ MEMORY | ✅ skill 兜底 | 🟢 完整 |
| **托尼**（PM）| ✅ | ✅ PRD/任务派单 | ✅ | 🟡 部分 | 🟡 90% |
| **派蒙**（协调）| ✅ | ✅ sessions_send/cron | ✅ | ✅ | 🟢 完整 |
| **团队 2 pm** | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 60% 待建评估 |

## 培训核心观点（你周三讲过的）

- Agent ≠ 高级 LLM
- Agent ≠ 多 LLM 投票
- Agent = **决策+工具+状态+恢复** 的完整工程体

## 落地动作

- [ ] 写 `wiki/concepts/agent/what-is-agent.md` 作为概念入门
- [ ] 给团队 2 5 Agent 各打"4 要素完整度"评分
- [ ] 关联 Harness Engineering（C 已入库）
- [ ] 补"AI 时代的原生组织"（曾鸣教授）观点

## 引用

- **Get 笔记 ID**: 第 57 条（什么是 Agent）
- **可复用位置**: Agent 概念入门 / 培训材料 / 团队 2 教育

## 关联文档

- [[insight-20260608-harness-engineering-third-paradigm|Harness Engineering 范式]]
- [[insight-20260608-skill-vs-subagent-architecture|Skill vs Sub-Agent 决策]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
