# 企业知识组织四层进化：从标签到知识图谱

> **类型**: Insight（知识管理方法论）  
> **来源**: Get笔记 2026-06-08 入库  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #knowledge-management #ontology #knowledge-graph #taxonomy

---

## 一句话洞察

> **企业知识库"标签上万却答不出复杂问题"的根因 = 知识组织停留在标签层**——必须经历 4 层进化：标签 → 分类 → 本体 → 知识图谱。这是我们 Wiki 知识库升级的方向标。

## 四层进化路径

| 层 | 形态 | 能力 | 我们 Wiki 现状 |
|:---:|:---|:---|:---:|
| **L1 标签** | 单维 tag | 检索 | ✅ 已有 |
| **L2 分类** | 多维分类（topic/category） | 导航 | ✅ 已有 |
| **L3 本体（Ontology）** | 概念 + 关系 | 推理 | 🟡 部分（Agent-engineering 等） |
| **L4 知识图谱** | 实体 + 关系 + 推理 | 复杂问答 | ❌ 缺（Neo4j 有，Wiki 无） |

## 核心痛点

> "今年 Q3 华东区退货率上升的原因"  
> — 标签层答不出，需要 **L4 知识图谱**（退货率 × 华东 × Q3 × 原因链）

## 落地动作

- [ ] 在 `wiki/topics/knowledge-management/personal/ai-pkm-workflow.md` 加 4 层进化图
- [ ] 调研 Neo4j ↔ Wiki 联动方案
- [ ] 给核心概念建"实体卡"（Agent/Skill/项目/方法论）
- [ ] 写 `wiki/concepts/knowledge-organization-four-layers.md`

## 引用

- **Get 笔记 ID**: 第 5 条（企业知识组织的四层进化）
- **可复用位置**: 知识管理方法论 / KM 工具选型 / Wiki 升级

## 关联文档

- [[../../../topics/knowledge-management/personal/ai-pkm-workflow|AI-PKM 工作流]]
- [[../../../topics/knowledge-management/personal/second-brain|第二大脑方法论]]
- [[../ai/insight-20260430-architecture-agent-planning|架构 Agent 规划]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
