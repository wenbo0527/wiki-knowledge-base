# #9 Claude Code 效率倍增指南：CLAUDE.md 全攻略（从入门到高手）

**源**: 刀哥 KB `2eYxaj0z` | note_id `1899685108277926432` | 2026-01-24 | tags: Claude Code
**链接**: https://kb.daode.com/note/1899685108277926432
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐⭐（**CLAUDE.md 是我 MEMORY.md 的直接模板**）

---

## 🎯 核心 Insight

**CLAUDE.md = 项目的"记忆芯片"**，Claude Code 启动时自动加载。

### 4 级层级系统

| 层级 | 路径 | 优先级 |
|:---|:---|:---:|
| 企业级 | 企业策略配置 | 最高 |
| 项目级 | 项目根目录/CLAUDE.md | 中高 |
| 用户级 | ~/.claude/CLAUDE.md | 中低 |
| 子目录级 | 项目子目录/CLAUDE.md | 最低 |

**优先级规则**：子覆盖父，近的覆盖远的

### 内容分配策略

- **用户级**：个人编码风格、缩进、引号、快捷指令
- **项目级**：技术栈、构建命令、团队规范、架构说明
- **子目录级**：模块特殊规则（如 Legacy 模块"不要重构，只修 bug"）

### Anthropic 团队案例

- **单一共享文件**：CLAUDE.md 签入 git，全员可见
- **动态更新**：每周补充最佳实践
- **钩子机制**：提交前自动跑 lint

**效果数据**：使用 Claude Code 后**人均每日合并 PR 数量增加约 67%**

### 高级技巧

```markdown
# 项目规范
## 🔥 核心规则（必须遵守）
- 禁止使用 any 类型
- API 调用必须有错误处理
```

```markdown
# READ THIS FIRST
特殊要求：所有数据库操作必须走 ORM，禁止原生SQL
```

### 常见问题

| 问题 | 解决方案 |
|:---|:---|
| 优先级混乱 | 区分个人偏好（用户级）与项目规范（项目级） |
| 文件过大（>10k 字） | 仅保留关键，详细文档放 docs/ 引用路径 |
| 团队配置不统一 | 项目级签入 git，个人偏好仅放用户级 |

---

## 🔧 对钟离可借鉴的部分（**直接套用到我 MEMORY.md 设计**）

### 借鉴 1: 4 级层级 = 我应该建 4 个 CLAUDE.md

**钟离的现状**：
- MEMORY.md 3KB（用户级，但没意识到）
- AGENTS.md 6KB（项目级 - Zhongli 工作流）
- HEARTBEAT.md 2KB（项目级 - 任务检查）
- SOUL.md 5KB（用户级 - 角色身份）

**借鉴路径**（按 Teresa Torres 颗粒化 + 本文 4 级层级）：

```
~/.openclaw/workspace-agents/zhongli/   # 用户级（钟离个人）
├─ CLAUDE.md                            # 入口 + 路由（仿 CLAUDE.md）
├─ MEMORY.md                            # 核心记忆（3KB）
├─ SOUL.md                              # 角色身份
├─ USER.md                              # 用户偏好
└─ memory/                              # 项目级（钟离管的项目）
   ├─ claude-code.md                    # Claude Code 经验
   ├─ openclaw.md                       # OpenClaw 治理
   ├─ ai-diagnoser.md                   # AI 诊断器项目
   ├─ personal-site.md                  # 个人主页项目
   └─ subagent.md                       # subagent 调度
```

### 借鉴 2: 🔥 emoji + READ THIS FIRST 模板

**我的 MEMORY.md 改造**：
```markdown
# MEMORY.md
## 🔥 必读（每次启动加载）
- 我是钟离，CC 团队 1 Leader
- 用户是文博，决策粒度：选项 A/B/C + 推荐
- **路径**：本地 `/Users/wenbo/`，远程 `118.196.79.130`

## ⚠️ 必避（教训区 TOP 10）
- 6/22: 修改 build 产物前先确认部署目录（教训 85）
- 6/22: nginx 缺 location 时检查 upstream（教训 80）
- 6/18: 弱模型用短 prompt（教训 14）

## 📚 按需加载
- 涉及 Claude Code → 加载 memory/claude-code.md
- 涉及 OpenClaw → 加载 memory/openclaw.md
```

### 借鉴 3: 钩子机制 → PreToolUse 自动 backup

**借鉴**：Anthropic "提交前自动跑 lint" → 我的 "改服务器前自动 backup"

```javascript
// hooks/pre-edit-server.js
if (command.includes('ssh root@118.196.79.130')) {
  // 自动 backup
  await run(`ssh root@118.196.79.130 "cp $FILE $FILE.bak.$(date +%Y%m%d_%H%M%S)"`)
}
```

### 借鉴 4: 文件大小控制 < 5k 字

**借鉴**：MEMORY.md 应该控制在 5KB 以内，详细文档放 memory/ 子目录（参考 8: Teresa Torres 微小文件）

**当前**：MEMORY.md 3KB ✅（精简后已合格）  
**目标**：CLAUDE.md（入口）≤ 2KB，memory/ 每个子文件 ≤ 5KB

### 借鉴 5: Anthropic 67% 数据 → 衡量我自己

**借鉴**：用 Claude Code 后**人均 PR 数量 +67%**

**钟离的应用**：
- 6/23 我产出 6+ 个 patch script + 10+ 个文档修改 = "端到端代理"工作 ✅
- 但 80% 是手动改 build 产物（"调试模式"）= TPD 低
- **应该把"重复 3+ 次"的任务自动化，让 PR 数量提升 67%**

---

## 🚦 立即可执行（24h）

- [ ] 在 MEMORY.md 加 🔥 emoji 分级
- [ ] 创建 hooks/pre-edit-server.js（改服务器前自动 backup）
- [ ] 写一篇"钟离的 CLAUDE.md 4 级层级实践"挂到 MEMORY.md

## 🟡 本周可执行

- 把 6 个项目（claude-code/openclaw/ai-diagnoser/personal-site/subagent/portal-shell）拆 memory/ 子文件
- 加 "/plan" 斜杠命令（强制每次先规划）
- 跑"自我 PR 数量"统计（用 task_tool.py 算任务数）

## ⚠️ 风险

- **层级覆盖陷阱**：项目级覆盖用户级时，个人偏好丢失
- **过度 emoji**：影响 grep 检索

## 📚 关联 Wiki

- 04: planning-with-files（CLAUDE.md 是稳定前缀）
- 05: Claude Code 团队化（CLAUDE.md 是 7 大构件核心）
- 08: Teresa Torres（路由式加载）

---

*🛡️ 钟离 · 19:06 · 2026-06-23*  
*消化: Nick 派单 #9/15 · CLAUDE.md = 我 MEMORY.md 的标准*