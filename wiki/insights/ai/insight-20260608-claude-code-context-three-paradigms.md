# Claude Code Agent 架构：上下文管理三种范式

> **类型**: Insight（架构方法论）  
> **来源**: Get笔记 2026-06-08 入库  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #claude-code #agent-architecture #context-management

---

## 一句话洞察

> **Claude Code 设计核心不是多 Agent 并行，而是"上下文管理"**——通过三种范式（压缩/分层/检索）解决 Agent 跑长任务的"上下文爆炸"问题。这直接对齐 blog 30 的"多 Agent 隐藏成本"。

## 三种范式

| 范式 | 核心 | 适用 |
|:---|:---|:---|
| **压缩（Compaction）** | 把历史对话压成摘要 | 中等任务（10-50 步） |
| **分层（Layering）** | 不同层用不同 context | 大任务（>50 步） |
| **检索（Retrieval）** | 按需检索历史/RAG | 知识密集型任务 |

## 与我们 4 Agent 团队的关系

| Agent | 当前 context 管理 | 建议 |
|:---|:---|:---|
| **Nick**（研究/分析）| ✅ 已有 MEMORY.md + RAG | 加 compaction 机制 |
| **钟离**（技术）| ✅ SOUL/MEMORY + Skill 库 | 检索范式为主 |
| **托尼**（PM）| ✅ PRD 模板 + 任务派单 | 分层范式 |
| **派蒙**（协调）| 🟡 Session log 增长快 | **加 compaction 优先** |

## 落地动作

- [ ] 在 `wiki/insights/ai-coding/` 补充 context-management.md
- [ ] 给 4 Agent 各自 context 用量 baseline
- [ ] 加 compaction 触发器：context > 80% 时自动总结

## 引用

- **Get 笔记 ID**: 第 6 条（Claude Code Agent 架构深度解析）
- **可复用位置**: Agent 架构 / Context 工程 / Memory 设计

## 关联文档

- [[../ai-coding/insight-20260430-architecture-agent-planning|架构 Agent 规划（已有）]] ← 需核对补充
- [[../ai-technology/insight-20260520-agent-skills-landscape-research|Agent Skills 全景研究]]
- [[../../../../05_AgentOutput/agent_work/Nick/02_最佳实践/Agent评估/方法论/Agent能力评估方法论-PM自驱版-v1.0|PM 自驱版方法论]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
