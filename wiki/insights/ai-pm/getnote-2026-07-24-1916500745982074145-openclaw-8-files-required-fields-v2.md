# openclaw-8-files-required-fields-v2

> 来源: Get 笔记
> 知识库: ai-pm
> 原始 ID: 1916500745982074145
> 创建时间: 2026-07-24 16:06:47
> 同步时间: 2026-07-25T06:00:32.781461

# OpenClaw 8 文件必填字段 v2.0 (整合 partme-ai/teams-of-agents 实证)

> **拍板**: 文博 @ 2026-06-22 10:31 G2
> **关联**: SOP `openclaw-7-files-template-v1.md` v1.0 (升级到 v2.0)
> **抓取实证**: web_fetch 抓 `partme-ai/teams-of-agents` 仓库（原始 URL 自动 redirect）
> **拍板范围**: 派蒙梳理 v2.0 + 建 BOOTSTRAP.md 模板 + 改 N2 cron 阈值

---

## 🎯 关键发现（partme-ai 仓库实证 + 派蒙 6-22 10:25 梳理整合）

### 5 大关键发现

| # | 发现 | 派蒙应做什么 |
|:--:|:--|:--|
| 1 | **partme-ai 7 文件规范**（AGENTS/SOUL/IDENTITY/TOOLS/USER/BOOTSTRAP/HEARTBEAT）| 派蒙加 MEMORY = **8 文件**（派蒙特色）|
| 2 | **HEARTBEAT.md 可空白**（"Keep this file empty to skip heartbeat"）| 派蒙**改 N2 cron 阈值**（HEARTBEAT.md 不必查大小）|
| 3 | **TOOLS.md = 默认模板**（partme-ai 仓库也是）| 派蒙**保留加强要求**（6-18 BUG 教训）|
| 4 | **BOOTSTRAP.md 必含**（partme-ai 实证）| 派蒙**建模板**（派蒙之前漏）|
| 5 | **Orchestration 段必含**（technical-director 实证）| 派蒙**补 AGENTS.md 管理层必填**（派蒙之前漏）|

---

## 📋 8 文件必填字段 v2.0

### 文件 1: AGENTS.md

#### 管理层必填（10 个 agent 适用：派蒙/钟离/尼克/Tony/PM/内容专家/交互专家/arch/PM/arch）

| # | 必填段 | 内容要求 | 长度 | partme-ai 实证 |
|:--:|:--|:--|:--:|:--:|
| ⭐ 1 | **First Run 段** | 处理 BOOTSTRAP.md + 明确**不询问**对方称呼 | ~300B | ✅ technical-director |
| ⭐ 2 | **Role 段** | 身份陈述 + 责任 + When to Invoke | ~500B | ✅ |
| ⭐ 3 | **Core Responsibilities 段** | 5-7 核心责任（项目/技术/团队/质量/外部）| ~400B | ✅ |
| ⭐ 4 | **Orchestration 段** | 子 agent 生态表 + 编排协议 + 模式 + 升级 | ~800B | ✅ **派蒙之前漏** |
| ⭐ 5 | **Priority Matrix 段** | 紧急 × 影响 4 象限决策 | ~200B | ✅ |
| ⭐ 6 | **派单 SOP** | `create + 改 assignee + sessions_send` 三件套 + 5 min ack | ~300B | 派蒙 + 团队 2 |
| ⭐ 7 | **反糊弄 SOP 5 条硬规矩** | 5 min 回报 + grep 行号 + test -d + 24h 验证 + 派蒙边界 | ~500B | 派蒙 + 团队 1 |
| 🟡 8 | **跨组通信 v1.8 协议** | sessions_send 跨组可用（6-18 已修）+ sessions_spawn 兜底 | ~300B | 派蒙 + 团队 2 |
| 🟡 9 | **错误处理 SOP** | 工具 deny / 编译失败 / 部署失败 升级路径 | ~400B | 派蒙 + 团队 1 |
| 🟡 10 | **21:00 写日报** | `memory/daily/YYYY-MM-DD.md` 路径 + 必含 5 模块 | ~200B | 派蒙 + 团队 1 |
| ⚪ 11 | **数字社区技术栈** | 框架 + 状态管理 + 库（仅团队 2）| 视场景 | 派蒙 + 团队 2 |
| ⚪ 12 | **跨组协调示例** | 团队 1 ↔ 团队 2 派单 + sessions_send 中转 | ~300B | 派蒙 + 团队 1/2 |

**管理层 AGENTS.md 总长度目标**：≤4KB

#### 执行层必填（7 个 agent 适用：阿加莘/老六/麦麦/小二子/smith/qa/doc/dev）

| # | 必填段 | 内容要求 | 长度 |
|:--:|:--|:--|:--:|
| ⭐ 1 | **First Run 段** | 同上 | ~300B |
| ⭐ 2 | **Role 段** | 身份 + 责任 | ~400B |
| ⭐ 3 | **Core Responsibilities 段** | 5-7 核心责任 | ~400B |
| ⭐ 4 | **任务执行 SOP** | 接收派单 → 5 min ack → 24h 推进 → 完工 sessions_send 反馈 | ~300B |
| ⭐ 5 | **工具调用 SOP** | 实测可用工具清单（allow/deny）+ 故障兜底 | ~400B |
| ⭐ 6 | **反馈 SOP** | 完工 / 阻塞 / 失败 → sessions_send 通知 PM + 飞书 | ~200B |
| ⭐ 7 | **21:00 写日报** | 同上 | ~200B |
| 🟡 8 | **错误处理 SOP** | 编译失败 / 部署失败 / 测试失败 升级路径 | ~300B |
| 🟡 9 | **跨组通信** | sessions_send 派蒙中转（如需跨团队）| ~200B |
| 🟡 10 | **领域技术栈** | QA / 文档 / 财务 / 投资 / Demo / 风控 专业工具 | 视场景 |
| 🟡 11 | **daily 必含段** | 5 模块（系统自检 / 任务完成 / 今日计划 / 阻塞 / 问题）| ~200B |
| ⚪ 12 | **Orchestration 段** | 仅当有子 agent 时需（如 qa 有 dev 测试 subagent）| ~400B |

**执行层 AGENTS.md 总长度目标**：≤3KB

---

### 文件 2: SOUL.md

| # | 必填段 | 内容要求 | 长度 | partme-ai 实证 |
|:--:|:--|:--|:--:|:--:|
| ⭐ 1 | **身份陈述** | 1-2 句功能描述（不是 motivational）| ≤100B | ✅ 个性 / 语气 / 价值观 |
| ⭐ 2 | **5 核心特质** | 一行（性格 / 风格 / 关注点）| ≤150B | ✅ 沟通风格 |
| ⭐ 3 | **行为规则** | 5 条硬规矩（每条 1 行）| ≤300B | ✅ 行为准则 |
| ⭐ 4 | **硬限制** | 具体禁止动作（≥3 条，每条具体）| ≤200B | ✅ 边界 |
| 🟡 5 | **边界** | 该做 / 不该做（4+4）| ≤200B | ✅ |
| 🟡 6 | **PDCA 闭环** | Plan → Do → Check → Act → Adjust（不闭环=失职）| ≤100B | 派蒙特色 |
| ⚪ 7 | **详细特质描述** | 性格 / 风格 / 美食 等 | 视场景 | 派蒙特色 |
| ⚪ 8 | **项目维护流程** | 团队 / 项目索引（管理层推荐）| 视场景 | 派蒙特色 |

**SOUL.md 总长度目标**：≤1KB（OpenClaw 推荐）/ 1.5KB（派蒙实际略宽）

---

### 文件 3: IDENTITY.md

| # | 必填段 | 内容要求 | 长度 | partme-ai 实证 |
|:--:|:--|:--|:--:|:--:|
| ⭐ 1 | **name** | agent 名字 | ≤50B | ✅ 身份卡 |
| ⭐ 2 | **vibe / 性格** | 1 行 | ≤100B | ✅ |
| ⭐ 3 | **emoji** | agent 代表 emoji | ≤10B | ✅ |
| ⭐ 4 | **theme / 角色** | 1 行 | ≤100B | ✅ 角色定位 |
| ⭐ 5 | **创建日期** | 激活时间 | ≤50B | ✅ |
| 🟡 6 | **What I do** | 1 句功能描述（partme-ai 强调）| ≤200B | ✅ **partme-ai 强调** |
| 🟡 7 | **核心特质** | 5 关键词 | ≤100B | 派蒙特色 |
| 🟡 8 | **服务对象** | 文博 / 团队 / 团队 2 | ≤100B | 派蒙特色 |
| ⚪ 9 | **avatar 描述** | 视觉化 | ≤100B | 派蒙特色 |

**IDENTITY.md 总长度目标**：≤1KB

---

### 文件 4: TOOLS.md

| # | 必填段 | 内容要求 | 长度 | partme-ai 实证 |
|:--:|:--|:--|:--:|:--:|
| ⭐ 1 | **openclaw.json 实证** | allow/deny 列表 + 5 tools | ≤300B | ⚠️ partme-ai 用默认模板（920B） |
| ⭐ 2 | **系统 prompt 工具集** | 实际注入 LLM 的工具列表（实测）| ≤300B | 派蒙加强 |
| ⭐ 3 | **工具故障兜底** | 不可调时 fallback | ≤200B | 派蒙加强 |
| ⭐ 4 | **紧急升级路径** | 飞书文博 + sessions_send 派蒙 main | ≤200B | 派蒙加强 |
| 🟡 5 | **L1-L5 验证方法** | 工具调用 5 层验证（派蒙 T3' 触发链）| ≤400B | 派蒙特色 |
| 🟡 6 | **工具实测记录** | 每次 session 跑过的命令 + 结果 + 教训 | ≤500B | 派蒙特色 |
| 🟡 7 | **environment-specific** | SSH / API endpoint / cron 路径 | 视场景 | partme-ai 同 |
| ⚪ 8 | **T3' 触发机制理解** | 事件触发 ≠ 轮询 + 24h 验证 | ≤300B | 派蒙特色 |

**TOOLS.md 总长度目标**：≤4KB（OpenClaw 推荐）/ 9KB（派蒙实际偏宽）

**关键警告**（OpenClaw 官方）：
> "`TOOLS.md` does **not** control which tools exist; it's guidance for how _you_ want them used."

**派蒙加强要求**（保留）：
- ❌ 不写 tool description（重复，浪费 token）
- ✅ 写 local conventions（agent-specific 工具约定）
- ✅ 写实测状态（哪些能用 / 哪些不能用）
- ✅ 写故障兜底（6-18 BUG 教训）

---

### 文件 5: USER.md

| # | 必填段 | 内容要求 | 长度 | partme-ai 实证 |
|:--:|:--|:--|:--:|:--:|
| ⭐ 1 | **名字 + 角色** | 文博 + 大总管服务对象 | ≤50B | ✅ 目标用户 |
| ⭐ 2 | **时区 + 位置** | Asia/Shanghai + Mac mini | ≤50B | ✅ |
| ⭐ 3 | **公司 / 项目** | AI Agent 团队 / 团队 1+2 | ≤100B | ✅ |
| ⭐ 4 | **关键偏好** | 工作时间 / 沟通风格 / 提醒方式 | ≤200B | ✅ 服务对象信息 |
| 🟡 5 | **重要客户 / 项目** | 团队 1+2 关键项目索引 | ≤300B | 派蒙特色 |
| 🟡 6 | **飞书 / 微信 偏好** | 飞书 ou_415... | ≤100B | 派蒙特色 |
| ⚪ 7 | **健康 / 财务偏好** | 麦麦服务时用 | ≤200B | 派蒙特色 |
| ⚪ 8 | **文博常驻项目** | 5 个核心项目 | ≤300B | 派蒙特色 |

**USER.md 总长度目标**：≤1.2KB

---

### 文件 6: BOOTSTRAP.md（**派蒙新增强制**）

| # | 必填段 | 内容要求 | 长度 | partme-ai 实证 |
|:--:|:--|:--|:--:|:--:|
| ⭐ 1 | **First Run 标识** | "If BOOTSTRAP.md exists, this is for configurer-only setup" | ≤100B | ✅ technical-director |
| ⭐ 2 | **USER.md 提示** | 让用户确认 USER.md 信息 | ≤200B | ✅ |
| ⭐ 3 | **Path 配置** | 工作空间路径 + agentDir 路径 + sessions 路径 | ≤200B | ✅ |
| ⭐ 4 | **身份确认** | 明确 agent 身份已定义（不询问对方称呼）| ≤200B | ✅ |
| ⭐ 5 | **完成 ritual** | "After setup, delete BOOTSTRAP.md" | ≤100B | ✅ |
| 🟡 6 | **首启动检查清单** | openclaw doctor / channels status / agents list | ≤200B | 派蒙特色 |
| 🟡 7 | **MCP / Skills 检查** | 关键 skill 是否安装 | ≤200B | 派蒙特色 |
| ⚪ 8 | **关联 cron** | agent 关联的 cron ID | ≤100B | 派蒙特色 |

**BOOTSTRAP.md 总长度目标**：≤1.5KB

**关键设计原则**（partme-ai 实证）：
- BOOTSTRAP.md 只在**首启动**时存在
- 配置完成后**删除**（避免污染 workspace）
- 身份 / 角色已在 SOUL.md / IDENTITY.md 定义，**不要询问对方**

---

### 文件 7: HEARTBEAT.md（**派蒙改阈值**）

**partme-ai 实证重大发现**：
```markdown
# HEARTBEAT.md
# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.
```

**关键结论**：
- ✅ **HEARTBEAT.md 可以保持空白**（"Keep this file empty to skip"）
- ⚠️ 派蒙之前 10:09-10:13 N2 cron 设了 HEARTBEAT.md 阈值 = **错**
- ⚠️ 派蒙之前 10:25 必填字段梳理说 HEARTBEAT.md 必填 = **错**

**派蒙整改**：
- **N2 cron 改阈值**：HEARTBEAT.md 不应作为必查大小项
- **新阈值设计**：
  - HEARTBEAT.md = 0 字节 = OK（"empty or with only comments"）
  - HEARTBEAT.md > 2KB = ⚠️ 偏长（仍然要告警，但可接受）
  - HEARTBEAT.md > 4KB = 🔴 异常

**HEARTBEAT.md 必填段**（**仅当有 periodic check 时**）：

| # | 必填段 | 内容要求 | 长度 |
|:--:|:--|:--|:--:|
| ⚪ 1 | **任务卡检查** | task_tool.py list pending | 视场景 |
| ⚪ 2 | **daily 落地检查** | `memory/daily/YYYY-MM-DD.md` | 视场景 |
| ⚪ 3 | **失联阈值检查** | < 12h 无活动 = 告警 | 视场景 |
| ⚪ 4 | **HEARTBEAT_OK 响应** | 静默条件 + 触发动作 | ≤100B |
| ⚪ 5 | **升级路径** | 飞书文博 + sessions_send 派蒙 | ≤150B |

**HEARTBEAT.md 设计原则**：
- **如果 agent 全部靠 cron** → HEARTBEAT.md 可空白
- **如果 agent 需要 periodic check** → HEARTBEAT.md 必填
- **HEARTBEAT.md 永远 ≤ 2KB**（OpenClaw 官方：避免 token burn）

---

### 文件 8: MEMORY.md（**派蒙特色**）

| # | 必填段 | 内容要求 | 长度 | partme-ai 实证 |
|:--:|:--|:--|:--:|:--:|
| ⭐ 1 | **现行版段** | 当前拍板的 v1.x 协议（每段 ≤1KB）| ≤6KB 总 | ❌ partme-ai 没列 |
| ⭐ 2 | **行为指南** | 角色定位 + 关键协议 + 边界 | ≤500B | ❌ |
| ⭐ 3 | **关联 cron / skill** | cron ID + skill 路径 | ≤300B | ❌ |
| ⭐ 4 | **沉淀日期 + 关联** | 派蒙惯例 | ≤200B | ❌ |
| 🟡 5 | **派单 / 接收历史** | 关键事件（最近 3-5 个）| ≤500B | ❌ |
| 🟡 6 | **失败教训** | 派蒙失职 / 反思≠改变 实证 | ≤500B | ❌ |
| ⚪ 7 | **活跃项目** | 团队 1+2 当前在跑 | ≤500B | ❌ |
| ⚪ 8 | **协议合规度** | v1.x 当前版本号 | ≤200B | ❌ |

**MEMORY.md 总长度目标**：≤3KB（OpenClaw 推荐）/ 7.3KB（派蒙实际略宽）

**派蒙现行版段必含**（⭐ 必填）：
- 团队2 sessions_spawn BUG 修复 v1.0（6-18）
- 数字社区 v1.2 协议 + 派蒙 C1 边界（6-11）
- T3' 事件触发机制 v1.0（6-22）
- T3' 首次跑成功 + C-A 自查机制（6-22）
- OpenClaw 7 文件最佳实践 + N2 监控（6-22）
- N2 自我整改（6-22 P2）
- BOOTSTRAP.md 必含（6-22 G2）

---

## 🎯 管理层 vs 执行层 必填字段差异表

| 文件 | 管理层必填差异 | 执行层必填差异 |
|:--|:--|:--|
| **AGENTS.md** | Orchestration 段 + 派单 + 跨组 + 协议合规 | 任务执行 + 工具 + 反馈 |
| **HEARTBEAT.md** | 派单回执 + 跨组 + MEMORY 精简 | 任务 + daily + 失联 |
| **MEMORY.md** | 现行版协议 + 派单历史 | 任务执行记录 + 失败教训 |
| **TOOLS.md** | sessions_send 跨组 + 派蒙中转 | 工具实测 + 故障兜底 |
| **SOUL.md** | 协调 / 派单 / 边界 | 执行 / 反馈 / 边界 |
| **USER.md** | 跨 agent 协调 / 文博服务 | 任务执行 / 文博服务 |
| **IDENTITY.md** | 协调者 / 管理层身份 | 执行者 / 操作员身份 |
| **BOOTSTRAP.md** | 同 | 同 |

---

## 📊 健康检查 v2.0 检查项（每项对应必填字段）

派蒙健康检查 cron 应该检查：

| 检查项 | 对应必填字段 | 阈值 |
|:--|:--|:--:|
| **AGENTS.md 必填段** | First Run / Role / Resp / Orchestration / Priority Matrix | 缺失 = 🔴 |
| **HEARTBEAT.md** | （**可空白** = OK）| 0 字节 = ✅ / > 2KB = ⚠️ / > 4KB = 🔴 |
| **MEMORY.md 现行版段** | 团队2 BUG / T3' / N2 / BOOTSTRAP 等 | 缺失 = ⚠️ |
| **TOOLS.md 工具实测段** | ⭐ 1-4 段 | 缺失 = 🔴（默认模板 = 0 落地）|
| **BOOTSTRAP.md** | ⭐ 1-5 段 | 首启动时存在 = ✅，跑过 = 已删除 ✅ |
| **派单回执率** | 管理层 AGENTS.md | < 80% = ⚠️ |
| **跨组 sessions 成功率** | 管理层 TOOLS.md | < 90% = ⚠️ |
| **daily 落地** | 执行层 HEARTBEAT.md | 当日缺 = 🔴 |
| **失联阈值** | 执行层 HEARTBEAT.md | > 12h = 🔴 |

---

## 🛡 派蒙越界前自查 3 问

1. 我做的是协调还是越界？ → **G2 = 派蒙能力建设 = 边界内** ✅
2. "已完成"声明带 grep 行号了吗？ → **实施时必带** ✅
3. 24h 后经得起戳破吗？ → ✅ **N2 cron 改后 24h 验证**

---

## 📝 关联

- **SOP v1.0**：`memory/sop/openclaw-7-files-template-v1.md`（8334B）
- **本 SOP v2.0**：`memory/sop/openclaw-8-files-required-fields-v2.md`（本文件）
- **N2 cron**：`e345f601-ca9e-49e5-a4e3-16d3a5ec192e`（待改阈值）
- **C1 cron**：`b0be1eaa-3561-4310-a6a3-5dcbebbac00f`（自查）
- **C2 cron**：`2b89d863-30f6-4fff-b734-92e61b8354a2`（24h 复检）
- **抓取实证**：`https://github.com/partme-ai/teams-of-agents`（已 redirect）

---

*派蒙 🍳 · 2026-06-22 10:33 落地 · 文博 @ 10:31 拍 G2 · 整合 partme-ai 实证 + 派蒙 10:25 梳理*