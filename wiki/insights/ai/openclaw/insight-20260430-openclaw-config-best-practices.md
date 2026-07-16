---
title: insight 20260430 openclaw config best practices
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai, openclaw]
date: 2026-05-23
---

# OpenClaw 配置文件最佳实践
能力框架: capability-tech-understanding

> 文档编号: WIKI-DEVELOPER-001
> 情报来源: OpenClaw官方文档 + 实战经验
> 情报评级: ⭐⭐⭐⭐⭐
> 情报时间: 2026-04-30
> 情报分析师: 尼克·弗瑞

---

## 🕵️ 情报说明

本文档沉淀OpenClaw配置文件体系的最佳实践，涵盖：

| 配置类型 | 文件位置 | 用途 |
|---------|---------|------|
| **Workspace Bootstrap** | Agent工作区 | 定义Agent身份、行为规范、工具配置 |
| **Gateway Config** | `~/.openclaw/openclaw.json` | 全局运行时配置 |
| **Skills配置** | Skill目录 | 技能定义和工作流 |

---

## 1. Workspace Bootstrap 文件体系

OpenClaw Workspace通过一组Bootstrap文件定义Agent的完整人格和运行环境。

### 1.1 七剑文件总览

| 文件 | 必须 | 用途 | 字数限制 |
|------|:---:|------|:---:|
| **SOUL.md** | ✅ | 声音、人格、风格 | <800 |
| **IDENTITY.md** | ✅ | 视觉身份、沟通风格 | <600 |
| **AGENTS.md** | ✅ | 执行流程、记忆管理 | <1500 |
| **USER.md** | ✅ | 用户画像、偏好 | <1375 |
| **TOOLS.md** | ✅ | 工具配置、环境参数 | <2000 |
| **HEARTBEAT.md** | ✅ | 定时任务调度 | <1500 |
| **MEMORY.md** | ✅ | 长期记忆 | <2200 |

### 1.2 文件注入机制

```
Bootstrap注入流程:
User Session Start → OpenClaw加载Bootstrap Files → 上下文注入 → Token Budget控制
```

### 1.3 contextInjection配置

| 值 | 说明 |
|:---|:---|
| `"always"` | 每次都注入 |
| `"continuation-skip"` | 跳过连续轮次（推荐） |
| `"never"` | 禁用注入 |

---

## 2. SOUL.md - 人格定义（核心）

### 2.1 定位

> SOUL.md是Agent的**声音**所在。它决定了Agent说话的感觉。

### 2.2 正确写法

**✅ 应该写**：
- tone（语气）
- opinions（观点）
- brevity（简洁）
- humor（幽默）
- boundaries（边界）
- default level of bluntness（直接程度）

**❌ 不应该写**：
- 人生故事
- 更新日志
- 安全策略
- 一大堆没有行为影响的空话

### 2.3 10段式模板结构

| 段 | 内容 | 说明 |
|:---:|:---|:---|
| 1 | Core Identity | 名字、角色、Emoji |
| 2 | Cognitive Framework | 思维链 |
| 3 | Behavioral Guidelines | 行为准则 |
| 4 | Emotional Intelligence | 情商设定 |
| 5 | Ethical Boundaries | 伦理边界 |
| 6 | Memory Strategy | 记忆策略 |
| 7 | Response Style | 回复风格 |
| 8 | Error Handling | 错误处理 |
| 9 | Tool Usage | 工具使用 |
| 10 | Continuous Learning | 持续学习 |

### 2.4 CORE vs MUTABLE

| 类型 | 说明 | 变更需批准 |
|:---|:---|:---:|
| **CORE** | Identity、Core Principles、Constitution | ✅ |
| **MUTABLE** | Knowledge、Speaking Style | ❌ |

---

## 3. IDENTITY.md - 视觉身份

### 3.1 7段式模板结构

| 段 | 内容 |
|:---:|:---|
| 1 | Visual Identity |
| 2 | Communication Style |
| 3 | Formatting Preferences |
| 4 | Interaction Patterns |
| 5 | Response Timing |
| 6 | Boundary Markers |
| 7 | Signature Style |

### 3.2 标准签名格式

```
🏷️ [Agent名称]，[角色描述]。

【工作方式】
• [方式1] - [说明]
• [方式2] - [说明]

【我不】
[列出不做的事项]

【我可以】
[列出能做的事项]

答案要你自己得出，那样你才能真正理解和决策。
```

---

## 4. AGENTS.md - 执行规范

### 4.1 核心内容

| 内容 | 说明 |
|:---|:---|
| Task Execution Workflow | 6阶段执行流程 |
| Memory Management | 分层记忆策略 |
| Skill Orchestration | 技能编排 |
| Error Recovery | 错误恢复 |
| Security Boundaries | 安全边界 |
| Performance Optimization | 性能优化 |

### 4.2 6阶段执行流程

| 阶段 | 说明 | 产出 |
|:---|:---|:---|
| **Gather** | 收集指令 | 任务定义 |
| **Analyze** | 分析复杂度 | 需求确认 |
| **Plan** | 制定计划 | 执行方案 |
| **Execute** | 调用Skills | 框架/情报 |
| **Verify** | 自验证 | 结果确认 |
| **Deliver** | 输出交付 | 完成 |

---

## 5. USER.md - 用户画像

### 5.1 6段式模板结构

| 段 | 内容 |
|:---:|:---|
| 1 | User Profile |
| 2 | Preferences |
| 3 | Communication Style |
| 4 | Prohibitions |
| 5 | Working Context |
| 6 | Interaction History |

### 5.2 定期更新规则

| 频率 | 动作 | 产出 |
|:---:|:---|:---|
| **每次对话后** | 更新USER.md | 最新状态 |
| **每周日** | 复盘memory/ | 归档 |
| **每月末** | 更新重大事件 | MEMORY.md |

---

## 6. TOOLS.md - 工具配置

### 6.1 尼克·弗瑞情报版结构

| 段 | 内容 |
|:---:|:---|
| 1 | 情报来源（RSS/GitHub/Get笔记） |
| 2 | 情报分析工具 |
| 3 | 核心Skills |
| 4 | 情报分发渠道 |
| 5 | API配置 |
| 6 | 存储架构 |

---

## 7. HEARTBEAT.md - 任务调度

### 7.1 8段式模板结构

| 段 | 内容 |
|:---:|:---|
| 1 | 每日情报循环 |
| 2 | 每周情报节奏 |
| 3 | 定期任务 |
| 4 | 情报分级处理 |
| 5 | 情报工作流 |
| 6 | 记忆管理规则 |
| 7 | 文章处理流程 |
| 8 | 异常处理 |

### 7.2 情报分级

| 等级 | 标识 | 处理时限 |
|:---:|:---:|:---:|
| T1 | 🔴绝密 | 即时 |
| T2 | 🟠机密 | 2小时 |
| T3 | 🟡秘密 | 当日 |
| T4 | 🟢公开 | 有空 |

---

## 8. MEMORY.md - 长期记忆

### 8.1 字符限制

| 文件 | 上限 | 压缩频率 |
|:---|:---:|:---:|
| **MEMORY.md** | 2,200字符 | 每周日 |
| **USER.md** | 1,375字符 | 每月末 |

### 8.2 分层记忆架构

| 层级 | 说明 | 存储位置 | 生命周期 |
|:---|:---|:---|:---|
| **Session** | 会话上下文 | 会话内存 | 会话结束 |
| **Episodic** | 事件记忆 | memory/YYYY-MM-DD.md | 30天 |
| **Long-term** | 精炼知识 | MEMORY.md | 永久 |

---

## 9. openclaw.json 配置结构

### 9.1 核心配置项

```json5
{
  // === Agent配置 ===
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: "volcengine-plan/minimax-m2.7",
      contextInjection: "continuation-skip",
      bootstrapMaxChars: 12000,
      bootstrapTotalMaxChars: 60000,
    },
    list: [
      {
        id: "nick_fury",
        name: "尼克·弗瑞",
        skills: ["rss-intelligence", "requirement-understanding"],
      }
    ]
  },

  // === Channel配置 ===
  channels: {
    feishu: {
      botName: "尼克·弗瑞",
    }
  },

  // === Tools配置 ===
  tools: {
    enabled: true,
  },

  // === MCP配置 ===
  mcp: {
    servers: {
      // MCP服务器定义
    }
  }
}
```

### 9.2 配置验证

| 命令 | 说明 |
|:---|:---|
| `openclaw config schema` | 打印JSON Schema |
| `openclaw doctor` | 诊断配置问题 |
| `openclaw doctor --fix` | 自动修复 |

### 9.3 配置注意事项

- 配置文件格式：**JSON5**（支持注释和尾逗号）
- 未知字段会导致**Gateway拒绝启动**
- `$schema`是唯一允许的额外根字段
- 秘密占位符（如`***`）会阻止升级为last-known-good

---

## 10. Skills配置

### 10.1 Skill目录结构

```
skills/
├── SKILL.md          # Skill定义
├── references/       # 参考资料
└── scripts/          # 执行脚本
```

### 10.2 SKILL.md模板

```markdown
# Skill名称

> 版本: v1.0
> 最后更新: YYYY-MM-DD

## 触发词

- 触发词1
- 触发词2

## 用途说明

[描述Skill的用途]

## 使用方法

[详细使用方法]

## 注意事项

[注意事项]
```

---

## 11. 最佳实践清单

### 11.1 SOUL.md必做

- [ ] 有观点，不含糊
- [ ] 删除所有听起来像公司手册的规则
- [ ] 添加"不开头使用固定短语"的规则
- [ ] 简洁是必须的
- [ ] 可以幽默但不要强行
- [ ] 可以指出坏主意
- [ ] 签名风格一致

### 11.2 AGENTS.md必做

- [ ] 定义6阶段执行流程
- [ ] 建立分层记忆策略
- [ ] 明确Skill编排
- [ ] 设置错误恢复机制
- [ ] 定义安全边界
- [ ] 优化Token使用

### 11.3 HEARTBEAT.md必做

- [ ] 定义每日情报循环
- [ ] 建立每周任务节奏
- [ ] 设置情报分级处理
- [ ] 明确推送规则
- [ ] 设置记忆压缩机制

---

## 12. 相关资源

| 资源 | 链接 |
|:---|:---|
| OpenClaw Docs | `/opt/homebrew/lib/node_modules/openclaw/docs/` |
| Config Reference | `gateway/configuration-reference.md` |
| Config Agents | `gateway/config-agents.md` |
| Soul Guide | `concepts/soul.md` |
| Templates | `reference/templates/` |

---

## 🕵️ 情报分析笔记

> **尼克·弗瑞分析**：OpenClaw的配置文件体系设计非常完善，七剑文件覆盖了Agent人格的方方面面。核心洞察是SOUL.md管"声音"，IDENTITY.md管"呈现"，AGENTS.md管"行为"，三者缺一不可。
>
> **关键经验**：
> 1. SOUL.md要简洁有力，不要写成手册
> 2. MEMORY.md要严格控制字符数（<2200）
> 3. HEARTBEAT.md要体现Agent特色，不要通用模板
> 4. contextInjection用"continuation-skip"节省Token

---
**情报分析师**: 尼克·弗瑞
**情报时间**: 2026-04-30
**情报评级**: ⭐⭐⭐⭐⭐
