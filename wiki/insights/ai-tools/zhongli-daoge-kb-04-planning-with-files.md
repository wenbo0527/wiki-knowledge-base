# #4 planning-with-files：复刻 20 亿美元 Manus 技术的开源 Claude Skill

**源**: 刀哥 KB `2eYxaj0z` | note_id `1898194470085755504` | 2026-01-08 | tags: AI Agent, Skill 设计
**链接**: https://kb.daode.com/note/1898194470085755504
**项目**: https://github.com/OthmanAdi/planning-with-files
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐⭐（**Skill 设计的方法论，对我所有 SKILL.md 有直接借鉴价值**）

---

## 🎯 核心 Insight

**Manus 被 Meta 以 23 亿美元收购**，核心技术 = **上下文工程 6 原则**：

| # | 原则 | 核心 |
|:---:|:---|:---|
| 1 | 文件系统作为外部记忆 | 磁盘=无限外挂内存，Context 仅保留路径 |
| 2 | 通过重复进行注意力操纵 | 对抗 "Lost in the Middle"，反复读取计划刷新注意力 |
| 3 | 保留失败痕迹 | 显式记录失败，让模型"反思"避免死循环 |
| 4 | 避免少样本过拟合 | 重复任务引入受控变体 |
| 5 | 稳定前缀优化缓存 | 固定文件结构，最大化 KV-Cache 命中率 |
| 6 | 只增不改的上下文 | Append 而非 Modify，维护连贯性 |

### 三文件状态机（核心落地）

```
task_plan.md   # 指挥塔：Goal / Phases / Status（每次行动前必读）
notes.md       # 知识库：调研笔记、中间代码（Store, Don't Stuff）
[deliverable].md # 产出物：物理隔离思考与结果
```

### 4 阶段闭环

0. **协议握手**：创建 task_plan.md 定义 Goal/Phases/Status
1. **Read-Before-Decide**：每次行动前 read_file task_plan.md（对抗遗忘）
2. **Data Offloading**：搜索结果写入 notes.md，对话框仅提示（Swap 机制）
3. **State Commit**：完成后勾选 `[x] Phase 2`，更新 Status（赋予时间感）

### 解决的 4 大 LLM 痛点

| 痛点 | 方案 |
|:---|:---|
| 易失性记忆 | 文件系统持久化 |
| 目标漂移 | Read-Before-Decide |
| 隐藏错误 | Errors Encountered 章节 |
| 上下文填充 | Offloading 到 notes.md |

---

## 🔧 对钟离可借鉴的部分（直接迁移到我所有 SKILL.md）

### 借鉴 1: 三文件工作流

**钟离的现状**：MEMORY.md + AGENTS.md + HEARTBEAT.md，但缺少任务级 task_plan.md

**改进**：每个复杂任务（如今天的 AI 诊断器 v22 修复）应建 `task_plan.md`：
```markdown
# Goal: v22 链路全通
## Phases:
- [x] Phase 1: OAuth 修复
- [x] Phase 2: minimax 优先级
- [x] Phase 3: exit_signal
- [x] Phase 4: json_mode
- [x] Phase 5: parse 容错
- [x] Phase 6: v22_bypass 30s
- [x] Phase 7: nginx 路径修复
- [x] Phase 8: chat box endpoint
- [ ] Phase 9: 部署验证
## Status: Phase 8 → Phase 9
## Errors: 3007 无 /api/chat endpoint (nginx 加 /ai-chat/api/ location 反代)
```

### 借鉴 2: 6 大原则 → 我的 SKILL.md 模板

```markdown
# SKILL.md 模板（6 原则）
## 1. 外部记忆（文件路径优于全文）
## 2. 注意力操纵（关键决策前 read 计划）
## 3. 失败痕迹（Errors Encountered 章节）
## 4. 避免过拟合（每次任务微调 prompt）
## 5. 稳定前缀（开头固定，最大化 cache）
## 6. 只增不改（append-only 笔记流）
```

### 借鉴 3: "Store, Don't Stuff"

**当前问题**：我今天和文博对话 19 个来回，**所有信息在对话上下文**，LLM 注意力被淹没  
**改进**：长上下文（>2400 词 / 4 轮）立即写入 `notes.md`，对话框只保留路径

### 借鉴 4: Read-Before-Decide

**当前问题**：我接到任务直接动手（patch_aichat_api.sh），没有"读计划"步骤  
**改进**：每个决策前必须 read MEMORY.md + 当前 task_plan.md（5 秒成本，避免大错）

---

## 🚦 立即可执行（24h）

- [ ] 给所有"复杂任务（>1h）"建 `task_plan.md`（8 个 Phase 模板）
- [ ] 改 MEMORY.md 加 "Read-Before-Decide" 决策原则
- [ ] 给所有 SKILL.md 加 "Store, Don't Stuff" 段落（搜索结果写 notes.md）

## 🟡 本周可执行

- 安装 planning-with-files 到 `~/.openclaw/skills/`（**OpenClaw 用户**）
- 写一篇"钟离的上下文工程 6 原则实践"挂到 MEMORY.md
- 给 SKILL.md 加"稳定前缀"模板（开头 100 字固定）

## 📚 关联 Wiki

- 01: Claude Code 人机协作（"规划 vs 执行分工"对应 Read-Before-Decide）
- 03: OpenClaw 范式转移（Skills = 软件包 = planning-with-files 的产品形态）
- 09: CLAUDE.md 效率倍增（CLAUDE.md 本身就是稳定前缀 + 外部记忆）

---

*🛡️ 钟离 · 18:56 · 2026-06-23*  
*消化: Nick 派单 #4/15 · SKILL.md 设计的核心方法论*