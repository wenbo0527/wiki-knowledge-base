# Agent Harness Engineering：从组件架构到运行时闭环的可靠性工程

> **类型**: Insight（可靠性工程）  
> **来源**: Get笔记 2026-06-03 入库  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #harness #reliability #runtime-closure #agent-engineering

---

## 一句话洞察

> **Agent 开始长期运行任务时，可靠性关注点从"模型答得对不对"转向"系统是否崩溃/超时/越权"**——Harness Engineering 的核心是"运行时闭环"（观察→决策→执行→恢复→观察），这是我们 4 Agent 团队治理的基础。

## 范式演进

| 阶段 | 关注点 | 失败模式 |
|:---|:---|:---|
| **Prompt Engineering** | 模型答对 | 答错/幻觉 |
| **Agent Engineering** | 工具调用 | 工具错/超时 |
| **Harness Engineering** | 运行时闭环 | 崩溃/越权/死循环 |

## 运行时闭环 5 阶段

```
观察 (Observe) → 决策 (Decide) → 执行 (Act) → 恢复 (Recover) → 观察
  │                                                            │
  └──────────── 长程运行可靠性 = 全程不崩 ─────────────────────┘
```

## 可靠性关键指标

| 指标 | 阈值 | 我们现状 |
|:---|:---:|:---:|
| **崩溃率** | < 1% | 🟡 6/5 派单真空暴露 |
| **超时率** | < 5% | ✅ fail-fast 兜底 |
| **越权率** | 0 | ✅ Standing Orders 守卫 |
| **死循环率** | < 0.5% | 🟡 待加 max-iter 硬限 |
| **状态丢失** | < 1% | ✅ Checkpoint 机制 |

## 落地动作

- [ ] 给 4 Agent 各自加"运行时自检"（每 30 min 一次）
- [ ] 写 `wiki/concepts/agent/runtime-closure-checklist.md`
- [ ] 关联 Standing Orders v2.0 治理规范
- [ ] 7/15 前做 1 次"长程任务"压力测试（>1h 任务）

## 引用

- **Get 笔记 ID**: 第 80 条（Agent Harness Engineering 深度解析）
- **可复用位置**: Harness 工程 / 可靠性 / 长程任务

## 关联文档

- [[insight-20260608-harness-engineering-third-paradigm|Harness Engineering 范式跃迁（C 已入库）]]
- [[../../../../05_AgentOutput/agent_work/Nick/02_最佳实践/OpenClaw治理/Standing-Orders-5层解法与落地实践-v2.0|Standing Orders v2.0]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
