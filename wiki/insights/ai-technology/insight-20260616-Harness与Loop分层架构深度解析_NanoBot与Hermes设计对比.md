---
title: insight 20260616 Harness与Loop分层架构深度解析 NanoBot与Hermes设计对比
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# Harness与Loop分层架构深度解析：NanoBot与Hermes设计对比

> **来源**: Get笔记
> **知识库**: ai-practice
> **导入日期**: 2026-06-16
> **原始ID**: 1912944130808648920
> **创建时间**: 2026-06-16 08:00:53
> **更新时间**: 2026-06-16 08:00:53
> **原始链接**: https://mp.weixin.qq.com/s/FrVm7DXot9grHpsGKwhPRQ

---

### **🏗️ 一、Harness 和 Loop：两个层次**

**核心架构**
- **Harness（基础设施层）**：回答"能不能做事"，负责一次同步调用的完整流程，包含四个核心组件：
  - Provider（模型接入）
  - Session（会话持久化 + compaction）
  - Tools（工具系统）
  - Runner（LLM调用 + 工具循环）
- **Loop（自主循环层）**：回答"能不能自己做到完"，在Harness外围实现循环控制，包含三个核心组件：
  - GoalManager（状态机）
  - Judge（完成评估）
  - Budget（停损边界）

**分层关系**
- Loop是Harness的消费者，而非替代者
- 分层设计使Loop实现可随意替换，不影响Harness

### **🔧 二、NanoBot：完整的 Harness + 可扩展的 Goal 原语**

**Harness完整性**
- 支持Provider多模型接入
- Session文件持久化与compaction
- Tools自注册与MCP（多工具协调）
- Runner工具循环与注入机制

**三大Goal机制**
1. **持久化标记**：`long_task`将目标写入session metadata的`goal_state`字段，`complete_goal`标记完成，数据不受compaction影响
2. **上下文注入**：通过`goal_state_runtime_lines()`从metadata读取目标，注入`[Runtime Context — metadata only, not instructions]`块，确保Agent在所有轮次可见
3. **轮内续跑**：Runner在工具循环结束后检查`sustained_goal_active()`，若目标活跃则注入goal continue消息，仅限同一轮内生效

**设计特点**
- 执行流：`消息 → Agent 跑一轮 → 返回`
- 无内置Judge和跨turn自动续跑
- 优势：轻量（核心~250行）、无额外LLM调用、Loop策略完全受控

### **🔄 三、Hermes：一种完整的 Loop 实现**

**Loop工作流程**
```
run_conversation()  ← 用户消息 / continuation    
↓  Agent 跑一轮（正常 Harness 流程，无感知）    
↓  GoalManager.evaluate_after_turn()    
↓  Judge 评估 → continue / done / pause    
↓  如果是 continue：构造 prompt，伪装成 user 消息，塞回队列    
↓ run_conversation()  ← 再跑一轮    
↓  ... 循环直到 done 或停损
```
**核心设计**
- Loop仅通过`GoalManager.evaluate_after_turn()`挂载于Harness
- Continuation prompt作为普通user消息通过`run_conversation`追加到会话
- 不修改system prompt，不交换工具集，保持prompt缓存完整
- 用户真实消息在队列中优先级高于continuation消息，可自然打断循环

**Judge实现**
- 使用auxiliary LLM（辅助大语言模型）进行判定
- turn budget + parse failure guard实现停损
- FIFO队列实现用户抢占机制

### **⚖️ 四、Judge：Loop 的判断支点**

**独立Judge优势**
- 避免Agent自评的局限性：Agent注意力聚焦于当前工具调用而非全局目标
- 上下文压缩影响评估准确性
- Agent倾向于给出确定回答而非"不确定"

**Hermes Judge设计**
- 严格约束：system prompt定义明确的"done"条件（回复确认完成/交付物已产出/目标不可达成）
- temperature=0保证判定确定性
- **fail-open机制**：API超时、返回非JSON、模型不可用时均返回"continue"，由turn budget兜底

**Judge实现选项**
- LLM判定（如Hermes）
- 规则判定（如"测试全绿？"）
- 超时退出
- 用户确认

### **🛑 五、停损：Loop 必须有出口**

**四层退出机制**

| 退出路径 | 触发条件 | 行为 |
| --- | --- | --- |
| 正常完成 | Judge 判定 done | 退出循环 |
| Turn budget | `turns_used ≥ 20` | auto-pause，通知用户 |
| Parse failure guard | Judge 连续 3 轮输出非 JSON | auto-pause，提示换模型 |
| 用户 preempt | 真实消息到达 | FIFO 自然排在 continuation 前面 |

**关键特性**
- 所有退出均为pause而非discard
- 完整保留状态（计数器、子目标、判定历史）
- 支持通过`/goal resume`从断点继续

### **🔨 六、从标记到循环：五步装配**

**能力叠加过程**
1. **标记（对抗遗忘）**：NanoBot的`long_task` + `goal_state_runtime_lines`实现
2. **完成判定（对抗虚假完成）**：引入LLM、规则或用户确认机制
3. **续跑（让判定推动行动）**：turn边界hook + user消息注入
4. **停损（防止黑洞）**：budget + guard + preempt
5. **Subgoals（运行时可组合）**：通过`/subgoal`追加或删除子约束

**装配关系**
```
Step 1: 标记        →  NanoBot 的内置原语  
Step 2: +判定       →  可选：LLM Judge / 规则 / 用户确认  
Step 3: +续跑       →  turn 边界 hook + user 消息注入  
Step 4: +停损       →  budget + guard + preempt  
Step 5: +Subgoals   →  可组合的子约束  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
                                              Hermes 的完整 Loop  
```
**核心认知**
- NanoBot停在Step 1，提供稳定轻量基础
- Hermes实现全部五步，提供完整Loop解决方案

### **🎯 七、设计原则**
1. **Harness与Loop分层**：Continuation作为普通user消息，不影响system prompt、缓存和provider
2. **判定与执行解耦**：Judge独立配置、独立模型、独立故障域
3. **停损是一等设计**：Budget、guard、preempt作为状态机正式转移
4. **状态离开消息历史**：Goal/subgoals/turns_used存储于session metadata或独立表，不参与compaction

### **📊 八、总结：NanoBot与Hermes对比**

**核心架构对比**
```
                    NanoBot                          Hermes  
               ┌──────────────┐               ┌──────────────┐  
               │ Goal 原语     │               │   Loop       │  
               │ long_task    │               │  GoalManager │  
               │ complete_goal│               │  Judge       │  
               ├──────────────┤               │  Budget      │  
               │   Harness    │               ├──────────────┤  
               │  Provider    │               │   Harness    │  
               │  Session     │               │  (同等)       │  
               │  Tools       │               │              │  
               │  Runner      │               │              │  
               └──────────────┘               └──────────────┘  
   设计选择: 提供原语，定制 Loop              设计选择: 提供完整的 Loop 实现  
   驱动: 用户手动 / 外部 Loop                  驱动: 内置 Judge 自动  
   轮次: 1..N（取决于上层 Loop）                轮次: 1..N（N ≤ budget）  
```
**关键维度对比**

| 维度 | NanoBot | Hermes |
| --- | --- | --- |
| Harness | ✅ 完整 | ✅ 同等 |
| Goal 存储 | session metadata | SessionDB state_meta |
| 可见性 | Runtime Context 注入 | Continuation prompt 注入 |
| 内置 Loop | 不内置——提供原语，由使用者装配 | 内置 Ralph Loop |
| 判定方式 | 开放：LLM / 规则 / 用户确认均可 | auxiliary LLM（可替换） |
| 续跑机制 | 开放：MessageBus + metadata 原语 | 内置：FIFO 注入 |
| Turn 预算 | 由外部 Loop 实现决定 | 默认 20，可配 |
| 核心代码量 | ~250 行（goal 原语） + Harness | ~900 行（完整 Loop） + Harness |

**一句话总结**
- NanoBot："给你底盘和发动机，车身自己造"
- Hermes："给你一辆能直接开的整车，但引擎盖一样可以打开"

### **🌐 九、更一般的视角**

**分层模式应用场景**
- **自主调试**：Harness跑测试→修代码，Loop控制重试直到全绿
- **Code Review**：Harness跑review，Loop续跑直到issues清零
- **多轮谈判**：Harness执行对话，Loop控制来回直到达成协议

**共同特征**
- Harness负责"能做"，Loop负责"做完"
- Loop实现多样化（LLM Judge、规则引擎、用户确认），但均基于同一Harness接口

### **📝 补充细节**
- **技术版本**：分析基于NanoBot v0.2.1和Hermes Agent v0.16.0，均采用MIT许可
- **MCP**：文中提及的Tools自注册+MCP指多工具协调协议，允许Agent同时调用多个工具并处理结果
- **compaction**：指会话历史压缩机制，用于控制上下文长度，防止超出模型token限制
- **fail-open机制**：一种故障处理策略，当系统关键组件失效时，默认采取"继续运行"而非"停止"的行为