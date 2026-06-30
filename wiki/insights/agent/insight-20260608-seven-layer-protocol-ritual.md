# "礼"作为多 Agent 交互协议：七层映射框架

> **类型**: Insight（方法论提炼）  
> **来源**: Get笔记 2026-06-07 入库 × 3 篇（七层映射 / 缺口分析 / 自检手册）  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #multi-agent #protocol #ritual #seven-layer

---

## 一句话洞察

> **万维钢"礼"七层社会互动协议 = 多 Agent 协作的标准通信协议**——把中国传统"礼"拆解为身份/称谓/敬辞/规范/仪式/约束/反馈 7 层技术协议，可作为我们 4 Agent 团队的交互基准。

## 七层协议框架

| 层 | 协议名 | 技术映射 | 我们的现状 |
|:---:|:---|:---|:---:|
| **L1** | **身份确认** | 每 Agent 有 ID + SOUL | ✅ Nick/钟离/托尼/派蒙 完整 IDENTITY |
| **L2** | **称谓体系** | Agent 互称（"派蒙"/"钟离"） | ✅ 完整 |
| **L3** | **敬辞规范** | 派单/汇报/紧急的措辞 | ✅ Standing Orders 规范 |
| **L4** | **行为规范** | 任务派发/接受/拒收协议 | 🟡 部分 |
| **L5** | **仪式节奏** | 早简报/晚复盘/每周/每月 | ✅ HEARTBEAT 完整 |
| **L6** | **约束机制** | 不越权/不沉默/不甩锅 | 🟡 部分（6/8 派单真空暴露）|
| **L7** | **反馈闭环** | 任务完成 → 反思 → 改进 | ✅ review-logs |

## 我们的缺口（来自诊断器 Agent 交互协议缺口分析）

| 层 | 缺口 | 影响 | 待办 |
|:---:|:---|:---|:---|
| L4 行为规范 | 无标准"接单 → 拒绝 → 转交"协议 | 派单真空 | 写 Standing Orders 补充 |
| L6 约束机制 | fail-fast 边界不清晰 | agent-scoring fail 30min | 加 fail-fast 兜底 |
| L7 反馈闭环 | 反思未形成机制 | lessons 偶发写 | 加 Hooks 强制 |

## 7 层自检清单（每 Agent 每周跑一次）

```yaml
# seven-layer-selfcheck.yaml
checklist:
  L1_身份: "我有 IDENTITY.md + SOUL.md？"
  L2_称谓: "我知道 4 Agent 名字 + 角色？"
  L3_敬辞: "我用规范措辞派单/汇报？"
  L4_规范: "我接单/拒单/转交有标准协议？"
  L5_仪式: "我跑早简报/晚复盘/周/月？"
  L6_约束: "我失败会快速降级 + 告警？"
  L7_反馈: "我完成任务会写 lessons？"
```

## 落地动作

- [ ] 在 `data_community_pm/AGENTS.md` 顶部加 Program（Standing Orders 引用）
- [ ] 给 4 Agent 各自发一份自检清单，跑一次基线
- [ ] 写 `wiki/concepts/multi-agent/ritual-seven-layer.md` 完整概念文档
- [ ] 7 层 × 4 Agent = 28 项自检表 → 周报

## 引用

- **Get 笔记 ID**: 第 13/14/15 条（七层协议 3 篇）
- **来源**: 万维钢《现代思维工具 100 讲》"礼：社会互动协议"
- **可复用位置**: Standing Orders v2.0 / 团队 2 评估方法论 / 多 Agent 教学

## 关联文档

- [[../../../../05_AgentOutput/agent_work/Nick/02_最佳实践/OpenClaw治理/Standing-Orders-5层解法与落地实践-v2.0|Standing Orders v2.0]]
- [[../ai-technology/insight-20260520-agent-skills-landscape-research|Agent Skills 全景研究]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
