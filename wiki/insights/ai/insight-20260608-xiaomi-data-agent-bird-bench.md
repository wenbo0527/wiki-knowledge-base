# 小米 DataAgent 全球第三：Harness 技术突破与行业启示

> **类型**: Insight（行业情报 + 技术方法论）  
> **来源**: Get笔记 2026-06-05 入库  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #data-agent #text-to-sql #bird-bench #xiaomi #harness

---

## 一句话洞察

> **小米 DataAgent 在 BIRD Text-to-SQL 榜单全球第三**——核心突破在 Harness 工程（多轮改写+执行校验+Schema 理解），不是模型本身。这验证了你"Data Agent = Harness + LLM" 的战略判断。

## BIRD 榜单关键信息

| 项目 | 含义 |
|:---|:---|
| **BIRD** | Text-to-SQL 业界公认基准（数据集/榜单） |
| **小米 DataAgent** | 全球第三名 |
| **核心突破** | Harness 工程（非模型） |

## 核心技术拆解

```
Text-to-SQL 难点：
  ├─ Schema 理解（库表字段）
  ├─ 自然语言→SQL 翻译
  ├─ 多轮改写（用户追问/纠正）
  └─ 执行校验（语法错/超时/重试）

小米突破点 = Harness 编排上述 4 步，而非 SFT 更大模型
```

## 对你的核心启发

| 维度 | 我们 4 Agent 团队现状 | 待升级 |
|:---|:---|:---|
| **Data Agent 方向** | MEMORY 已写"Data Agent = 核心" | ✅ 战略正确 |
| **Harness 工程** | 钟离/OpenClaw Harness | 🟡 待对齐 |
| **BIRD 实测** | ❌ 未跑过 | 🟢 拉 baseline |
| **多轮改写** | 部分支持 | 🟡 加固 |

## 落地动作

- [ ] BIRD 榜单 5 维度调研（榜单机制/评分口径/前三名差异）
- [ ] 在 `data_community_arch` 加 BIRD 基线任务（10 个 SQL 问答）
- [ ] 写 `wiki/concepts/data-agent/text-to-sql-playbook.md`
- [ ] 关联 INS-20260520-databricks-data-agent-research

## 引用

- **Get 笔记 ID**: 第 54 条
- **可复用位置**: Data Agent 战略 / Harness 工程 / BIRD 基准

## 关联文档

- [[../ai-strategy/insight-20260520-databricks-data-agent-research|Databricks Data Agent 调研]]
- [[../ai-technology/insight-20260520-agent-skills-landscape-research|Agent Skills 全景研究]]
- [[../../../../05_AgentOutput/agent_work/Nick/02_最佳实践/Agent评估|研发团队 2 评估]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
