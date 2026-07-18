---
title: insight 20260608 skills radar platform
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai]
date: 2026-06-30
---

# Skills Radar 重大更新：Agent 技能体系结构化演进

> **类型**: Insight（平台/工具情报）  
> **来源**: Get笔记 2026-06-06 入库  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #skills #radar #agent-ecosystem #platform

---

## 一句话洞察

> **Skills Radar = 技能收录与演进地图**——专门追踪 Skills 技术，让 Agent 能力进化有迹可循。我们 OpenClaw 的 Skill 库（79 个）需要接入这类平台化追踪。

## 平台核心

| 维度 | 说明 |
|:---|:---|
| **定位** | 技术收录 + 演进地图 |
| **追踪** | Skills 出现/成熟/淘汰的时序 |
| **价值** | Agent 能力进化有据可查 |

## 我们当前 Skill 库现状

| 指标 | 数值 | 备注 |
|:---|:---:|:---|
| 总数 | 79 个 | `~/.openclaw/skills/` |
| 维护者 | 多个 | 钟离/Nick/团队 1 |
| 评测机制 | 🟡 5 个相关 skill 碎片化 | 今日已建团队 2 评估方法论 |
| 演进追踪 | ❌ 无 | **Skills Radar 启发点** |

## 落地动作

- [ ] 调研 Skills Radar 平台是否可对接（API？）
- [ ] 给 79 个 Skill 打版本号 + 创建日期
- [ ] 写 `wiki/topics/ai-native/skill-ecosystem.md` 替代/补充
- [ ] 加 `last_updated` 字段到每个 SKILL.md frontmatter

## 引用

- **Get 笔记 ID**: 第 19 条（Skills Radar 重大更新深度解析）
- **Tag**: Agent 技能体系 / Skills Radar / 智能检索
- **可复用位置**: Skill 库治理 / agent-scoring v2.0 / Skill 评估 SOP

## 关联文档

- [[../ai-technology/insight-20260520-agent-skills-landscape-research|Agent Skills 全景研究]]
- [[../ai/insight-20260421-openai-skill-evaluation|OpenAI Skill 评测系统调研]]
- [[../../../../../05_AgentOutput/agent_work/Nick/02_最佳实践/Agent评估|研发团队 2 评估全套]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
