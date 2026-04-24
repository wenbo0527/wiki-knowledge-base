# Anthropic Harness 指南：到期清理、别帮倒忙

> **情报日期**: 2026-04-21  
> **来源**: AGI Hunt / Claude 官方博客  
> **原文**: https://claude.com/blog/harnessing-claudes-intelligence  
> **分析师**: 尼克·弗瑞  
> **分类**: Agent Engineering / Harness / Best Practice  
> **关联专题**: [Agent Engineering](../topics/ai-native/agent-engineering.md) | [Harness Engineering](insight-20260417-harness-engineering.md)

---

## 🎯 核心洞察

### 1. 核心观点：Harness 编码的是「Claude 做不到什么」的假设

```
Harness Engineering 的本质假设：
─────────────────────────────────
Harness 编码的是「Claude 做不到什么」的假设
                           ↓
                    但 Claude 在变强
                           ↓
               假设会过期 → Harness 会成为 dead weight
                           ↓
            解决方案：定期审查，该拆就拆
```

**核心原则**: 你给 Claude 搭的每一层脚手架，都应该带着一个**到期日**。

### 2. 三条核心原则：别帮倒忙

| 原则 | 核心要点 | 关键洞察 |
|:---|:---|:---|
| **用 Claude 已经会的** | 先看 Claude 能用什么，而不是造新工具 | 底层工具越通用，Claude 发挥空间越大 |
| **什么时候该停手** | 问自己「我还能停掉什么？」 | 把控制权还给 Claude |
| **边界要谨慎** | 缓存策略、专用工具、安全边界 | 该设的边界要设，但要精准 |

### 3. Dead Weight：Harness 最大的陷阱

```
Dead Weight 的形成机制:

问题出现 ──→ 搭建 Harness 解决 ──→ 模型变强 ──→ Harness 变成 dead weight
     ↑                                                    ↓
     └────────────── 应该拆掉，而不是永久保留 ──────────────┘

典型案例:
• Sonnet 4.5 有「上下文焦虑」→ 我们加了 context 重置机制
• Opus 4.5 行为消失 → 重置机制成了 dead weight
• 结果: 该拆掉了
```

**核心洞察**: Build to delete. 造了就要敢拆。

---

## 🔧 实践指南

### 原则1: 用 Claude 已经会的

#### 底层工具的威力

```python
# Claude 天生就会用的工具组合
基础工具 = {
    "bash": "执行命令",
    "文本编辑器": "读写文件"
}

# 这两个工具组合起来，Claude 可以衍生出复杂工作模式
衍生能力 = [
    "Agent Skills",
    "程序化工具调用",
    "Memory 系统"
]
```

**关键数据**:
- Claude 3.5 Sonnet: SWE-bench Verified 49%，只用 bash + 文本编辑器
- Claude Opus 4.5: SWE-bench Verified 80.9%，工具还是那两个

#### 专用工具的陷阱

```
专用工具设计的问题:

场景: 为 Claude 造一堆专用工具
      ↓
每个工具解决一个具体问题
      ↓
看上去考虑全面
      ↓
实际上是在替 Claude 做它自己能做的决策
      ↓
结果: 限制了 Claude 的发挥空间

反模式:
• 为每个 API 封装一个专用工具
• 为每个查询类型设计不同工具
• 过度设计工具参数
```

#### 正确做法：最大化通用性

```python
# 好的设计：底层工具尽可能通用
tools = {
    "bash": {
        "description": "执行任意 shell 命令",
        "parameters": {"command": "string"}
    },
    "edit": {
        "description": "读写文件",
        "parameters": {
            "path": "string",
            "content": "string (optional)"
        }
    }
}

# Claude 自己组合这些工具完成复杂任务
# 例如：分析代码 → bash查找文件 → edit读取 → bash运行测试 → edit修改
```

---

### 原则2: 什么时候该停手

#### 核心问题：「我还能停掉什么？」

```
控制权转移的演进:

阶段1: 全人工编排
        ↓
阶段2: 人工定义流程，AI执行步骤
        ↓ 
阶段3: AI自主编排，人工审查关键点
        ↓
阶段4: AI完全自主，人工仅在异常时介入
        ↓
目标: 把控制权尽可能还给 Claude
```

#### 三个维度的放权

##### 维度1: 编排 (Orchestration)

```python
# 传统做法: 人工编排所有步骤
workflow = [
    "step1: 调用工具A",
    "step2: 等结果", 
    "step3: 调用工具B",
    "step4: 等结果",
    "step5: 调用工具C"
]
# 问题: 慢、贵、Claude 不需要看全部结果

# 正确做法: Claude 自己编排
# 给 Claude bash，让它自己写代码编排工具调用
# 中间结果在代码里处理，只有最终输出进 context

# 效果对比:
# BrowseComp 基准测试
# Opus 4.6 自己过滤工具输出: 45.3% → 61.6% (+16.3%)
```

##### 维度2: 上下文 (Context)

```python
# 传统做法: 把所有指令预加载到 system prompt
# 问题: 指令越多，注意力越分散；大部分指令当前任务用不到

# 正确做法: Skills 机制

# Skill 文件结构:
skill = {
    "yaml_header": {
        "name": "数据分析",
        "description": "用于处理数据清洗和分析任务",  # 预加载到 context，占很少 token
        "version": "1.0"
    },
    "full_content": "详细的 skill 说明、示例、最佳实践..."  # Claude 自己按需读取
}

# 渐进式披露:
# 1. 给 Claude 一个目录（所有 skill 的 name + description）
# 2. Claude 判断当前任务需要哪个 skill
# 3. Claude 自己去读取 skill 文件的完整内容

# 相关技术: context editing
# 让 Claude 自己删掉已经过时的上下文
# - 旧的工具调用结果
# - 过期的思考块
# - 不再相关的中间状态

# 相关技术: subagent
# Claude 自己判断什么时候该分叉一个新的 context window
# 隔离处理某个子任务
# Opus 4.6 用 subagent 在 BrowseComp 上又多了 2.8%
```

##### 维度3: 记忆 (Memory)

```python
# 问题: 长时运行的 Agent 会超出单个 context window 的容量

# 传统做法: 在模型外面建一套检索基础设施
# 复杂、成本高、与模型分离

# Anthropic 做法: 让 Claude 自己决定记什么

# 技术1: compaction（压缩）
# Claude 总结过去的上下文来保持连续性
# 模型迭代后，Claude 在「选择记什么」这件事上越来越强

# 数据说话:
# 同样的 compaction 设置:
# - Sonnet 4.5: BrowseComp 一直卡在 43%
# - Opus 4.5: 能到 68%
# - Opus 4.6: 到了 84%

# 技术2: memory folder
# Claude 把上下文写成文件，需要的时候再读回来
# Sonnet 4.5 用了 memory folder 后:
# BrowseComp-Plus 准确率: 60.4% → 67.2%

# 核心原则: 让模型自己管理记忆，而不是外部系统
```

---

### 原则3: 边界要谨慎

#### 缓存策略

```python
# Messages API 是无状态的
# 每一轮对话都需要把所有历史打包发给 Claude
# 缓存的 token 成本只有普通 token 的 10%
# cache hit rate 直接关系到账单

# 优化建议:

# 1. 静态内容放前面，动态内容放后面
# 系统指令、工具定义、通用 context → 放前面（容易缓存）
# 用户输入、临时状态、中间结果 → 放后面（经常变化）

# 2. 用 <system-reminder> 追加更新，别改 prompt 本身
# 错误做法: 每次重新构造整个 prompt
# 正确做法: 在 system prompt 末尾追加 <system-reminder> 标签

# 3. 别在会话中间换模型
# 缓存是按模型绑定的
# 一换模型，之前的缓存全失效

# 4. 工具定义在缓存前缀里
# 加减工具会让缓存失效
# 用 tool search 按需加载

# 5. 多轮对话里，把断点移到最新消息处
# 让缓存最大化复用
```

#### 专用工具 vs 通用工具

```python
# 不是所有操作都需要专用工具
# bash 已经够用了
# 但有三种情况应该提升为专用工具:

# 情况1: 安全边界
# 不可逆的操作（比如外部 API 调用）应该有确认机制
# 写操作可以加过期检查，防止覆盖已更新的文件

# 情况2: 用户界面
# 工具调用可以渲染成弹窗，给用户展示选项或阻塞等待反馈

# 情况3: 可观测性
# 类型化的工具调用有结构化参数，方便日志、追踪和回放

# 新模式: Claude Code 的 auto-mode
# 用第二个 Claude 来审查第一个 Claude 的 bash 命令是否安全
# 这个模式可以减少专用工具的数量
# 但只适合用户信任整体方向的场景
```

---

## 💀 Dead Weight：Harness 最大的陷阱

### 形成机制

```
问题出现
    ↓
搭建 Harness 解决
    ↓
模型变强
    ↓
Harness 变成 dead weight
    ↓
应该拆掉，而不是永久保留
```

### 典型案例

**案例1: Context 重置机制**

```python
# Sonnet 4.5 的问题:
# 有「上下文焦虑」——在感觉到 context 上限时提前收工

# 解决方案:
# 我们加了 context 重置机制来应对

# Opus 4.5 的变化:
# 这个行为消失了

# 结果:
# 重置机制成了 dead weight
# 该拆掉了
```

**案例2: Sprint 分解**

```python
# V1 的做法:
# sprint 分解是护栏
# 在 Opus 4.5 时代有用

# V2 的变化:
# Opus 4.6 来了
# sprint 成了 dead weight

# 结果:
# 拆掉，成本省了 37%
```

### 核心原则: Build to Delete

```
造了就要敢拆。

每一层脚手架都应该带着一个到期日。

定期审查，该拆就拆。
```

### 具体行动

```python
# 建立定期审查机制
review_schedule = {
    "frequency": "每月",
    "questions": [
        "这层 Harness 现在还有必要吗？",
        "Claude 自己能做这件事了吗？",
        "如果不确定，做 A/B 测试验证",
    ]
}

# 建立 deprecation 流程
deprecation_process = {
    "step1": "标记为 deprecated",
    "step2": "监控使用率",
    "step3": "如无异议，彻底移除",
    "step4": "文档更新"
}
```

---

## 📊 关键数据对比

| 模型版本 | BrowseComp 准确率 | 关键改进 |
|:---|:---:|:---|
| Sonnet 3.5 | ~40% | 基础能力 |
| Sonnet 4.5 | 43% | Compaction |
| Opus 4.5 | 68% | 自主编排 |
| Opus 4.6 | 61.6% → 84% | +Subagent, +Memory |

---

## 🔗 关联资源

| 类型 | 资源 | 链接 |
|:---|:---|:---|
| 原文 | Harnessing Claude's Intelligence | https://claude.com/blog/harnessing-claudes-intelligence |
| 推文 | Lance Martin | https://x.com/RLanceMartin/status/2039783012427333755 |
| 前置阅读 | Anthropic 工程博客 - 多智能体编排 | [[insight-20260417-harness-engineering\|Harness Engineering 深度调研]] |
| 前置阅读 | 模型不是关键，Harness 才是 | [[sources/references/harness-engineering-wechat-article\|Harness 工程文章]] |

---

**维护者**: 尼克·弗瑞 🕵️  
**最后更新**: 2026-04-21  
**状态**: ✅ 已入库

**标签**: #Anthropic #Harness #AgentEngineering #BestPractice #Claude
