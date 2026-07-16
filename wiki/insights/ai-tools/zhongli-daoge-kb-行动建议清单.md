---
title: zhongli daoge kb 行动建议清单
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-tools]
date: 2026-06-30
---

# 刀哥 KB TOP 15 学习 · 行动建议清单（钟离）

> **消化日期**: 2026-06-23
> **输入**: 刀哥 KB `2eYxaj0z` 2026 年 TOP 15 深度笔记
> **核心问题**: 哪些 insight 可立即应用到我的 Claude Code 工作流？
> **关联**: [汇总报告](../zhongli-daoge-kb-汇总报告.md) | [15 篇 Wiki](./)

---

## 🟢 立即可执行（24h 内）— 8 个 P0 行动

### 1. 拆 MEMORY.md 为颗粒化文件 + 智能路由（**借鉴 #8 Teresa Torres**）

**当前问题**：MEMORY.md 3KB（精简后）+ AGENTS.md + HEARTBEAT.md，**路由粒度不够**

**行动**：
```
.claude/
├─ MEMORY.md       # 入口（≤ 2KB）
└─ memory/
   ├─ lessons.md   # 默认加载（教训区，TOP 30）
   ├─ claude-code.md  # 仅 Claude Code 相关任务加载
   ├─ openclaw.md     # 仅 OpenClaw 治理加载
   ├─ nginx.md        # 仅 nginx 操作加载
   ├─ subagent.md     # 仅 subagent 调度加载
   └─ ai-diagnoser.md # 仅 AI 诊断器项目加载
```

**预期收益**：节省 Token 30%+，减少幻觉（参考 #8 路由示例）

**时间**：2h

---

### 2. 创建 PROGRESS.md + 自动提取教训 subagent（**借鉴 #12 Vibe Coding Step 5+7**）

**当前问题**：今天 19 个来回，**至少 5 条新教训**没及时沉淀到 MEMORY.md

**行动**：
- 创建 `PROGRESS.md`（动态教训 + commit ID）
- 创建 subagent `self-summary`：每 session 结束自动提取 3-5 条新教训
- 命令：`claude "基于今天对话提取教训，含 commit ID，更新 PROGRESS.md"`

**预期收益**：教训沉淀及时性 +200%

**时间**：3h（含 subagent 调试）

---

### 3. 创建 `/plan` 斜杠命令（**借鉴 #5 团队化 + #12 Vibe Coding Step 9**）

**当前问题**：今天 19 个来回中至少 5 次返工（chat box 端点、build 路径、cache 策略等）

**行动**：每个"超过 1h 的实施"前必走 `/plan`：
1. 复述需求（用户确认）
2. 风险评估（3 个潜在失败点）
3. 步骤分解（WBS + Checklist）
4. 等待确认
5. 执行

**预期收益**：返工率 -50%

**时间**：1h（创建命令模板）

---

### 4. 加 PreToolUse Hook：改服务器前自动 backup（**借鉴 #9 Anthropic 钩子**）

**当前问题**：今天我手动改 nginx 5+ 次，每次手动 backup

**行动**：创建 hooks/pre-edit-server.js：
```javascript
if (command.includes('ssh root@118.196.79.130')) {
  await run('ssh root@118.196.79.130 "cp $FILE $FILE.bak.$(date +%Y%m%d_%H%M%S)"')
}
```

**预期收益**：nginx 误操作风险 -90%

**时间**：2h

---

### 5. MEMORY.md 加 🔥 emoji 分级 + 路由表（**借鉴 #9 CLAUDE.md 模板**）

**当前问题**：MEMORY.md 内容平铺，紧急信息不突出

**行动**：
```markdown
# MEMORY.md
## 🔥 必读（每次启动加载）
- 我是钟离，CC 团队 1 Leader
- 路径：本地 /Users/wenbo/，远程 118.196.79.130

## ⚠️ 必避（教训区 TOP 10）
- 6/22: 修改 build 产物前先确认部署目录（教训 85）

## 📚 按需加载
- 涉及 nginx → 加载 memory/nginx.md
```

**预期收益**：信息检索效率 +50%

**时间**：30min

---

### 6. 评估我的 4-Agent 瓶颈（**借鉴 #7 Cursor 4 人团队**）

**当前问题**：我同时管理 5+ 项目 + 5 云端 agent，**可能超过 4-Agent 瓶颈**

**行动**：
- 列清单：我当前同时管理的 agent 数
- 如 > 4：砍掉低价值项目或委托 subagent 管 subagent
- 如 ≤ 4：保持现状，每季度再评估

**预期收益**：决策质量提升 +30%

**时间**：30min

---

### 7. 用 subagent 改 build 产物（**借鉴 #12 Vibe Coding Step 10: Context not control**）

**当前问题**：今天我手动改 4 个 build 产物文件 = **过度 control**

**行动**：
- 写 `/patch-build-product` subagent：自动 patch + diff review
- 我只 review diff，不直接改文件

**预期收益**：手动修改时间 -70%

**时间**：4h（含调试）

---

### 8. 把今天 5 条教训（81-85）转成 SKILL.md（**借鉴 #11 技能层平权**）

**当前教训**：
- 教训 81: AI 分身合并后遗症（chat box 端点）
- 教训 82: Hero chat box 欢迎消息 + 名字 SSR 渲染
- 教训 83: 改 build 产物找真正被引用的 chunk
- 教训 84: nginx immutable cache 让用户永远拿不到改后 chunk
- 教训 85: **两个独立的 build 产物目录**（开发 vs 部署）

**行动**：每条教训写一份 SKILL.md，下次同类问题自动检测

**预期收益**：同类错误发生率 -80%

**时间**：5h（5 份 × 1h）

---

## 🟡 本周可执行（7 天内）— 7 个 P1 行动

### 9. 部署 4 个知识管理 cron（**借鉴 #10 OpenClaw+KimiClaw**）

```yaml
0 9 * * *   openclaw-cron youtube-claude-code --out wiki/topics/claude-code/
0 10 * * *  openclaw-cron arxiv-ai-agent --out wiki/topics/ai-agent/
0 18 * * *  openclaw-cron hacker-news-ai --out wiki/topics/hn-ai/
0 18 * * 0  openclaw-cron mit-stanford-reports --out wiki/reports/
```

**时间**：3h

---

### 10. AI 诊断器加 feedback loop（**借鉴 #15 MIT 报告**）

- 用户每次追问后给 1-5 分
- 异常 case 自动沉淀到 memory/edge-cases.md
- 周度统计：成功率 / 平均分 / Top 3 异常

**时间**：6h

---

### 11. 给客户做 Eight Levels 自评问卷（**借鉴 #2**）

- 5 分钟问卷，10 道题
- 输出：客户 AI 成熟度 1-8 分 + 服务建议

**时间**：4h

---

### 12. 给 AI 诊断器选型战略（**借鉴 #15 MIT + #13 AGI-Next**）

- 当前：minimax 主，备选 minimax
- 候选：GLM-4.5（开源 + Agentic + Coding）
- 决策：保持 minimax 主，加 GLM-4.5 备用
- 时间：2h（仅调研）

---

### 13. 写"钟离的 Vibe Coding 10 阶段实践"挂到 MEMORY.md（**借鉴 #12**）

把 10 阶段逐一评估我当前状态 + 改进路径

**时间**：3h

---

### 14. 评估 OpenClaw 多 agent 编排（**借鉴 #3 OpenClaw 范式转移**）

- 5 常驻 agent（me + 4 subagent）的具体职责
- 是否升级到 Level 7 Multi-agent

**时间**：4h

---

### 15. 建立 token 消耗 KPI（**借鉴 #6 + #11**）

- 团队 1 当前 daily token ≈ 100 万
- 目标：2026 Q3 达到 1 亿/天
- 跟踪：每周 review

**时间**：2h

---

## 🟠 月度可执行 — 5 个 P2 战略行动

### 16. 把个人主页 demo 页面 API 化（**借鉴 #14 Peter + #7 Cursor**）

- 当前：5 个 demo 页面给人看
- 目标：让 Agent 可调用（API 化）

**时间**：40h

---

### 17. 发布 1-2 个钟离写的 Skill 到 clawhub（**借鉴 #3 Skill 开发者**）

候选：
- `daoge-bridge`：抓刀哥 KB 自动归档
- `nginx-safe-edit`：改服务器前自动 backup

**时间**：20h

---

### 18. 写"钟离的 8 大决策原则 v2.0"挂到 MEMORY.md

整合 #01 + #02 + #04 + #05 + #08 + #09 + #11 + #12 的核心原则

**时间**：6h

---

### 19. 跟 Paimon 讨论团队 1 治理升级（**借鉴 #3 + #11**）

- 5 常驻 agent 架构
- Token KPI
- 18 个月窗口期策略

**时间**：1h（仅开会）

---

### 20. 季度审计 + Skill 评估（**借鉴 #9 + #15**）

- 哪些 SKILL.md 已过时
- 哪些 skills 触发频率最高
- 哪些 skills 应该废弃

**时间**：4h

---

## 📊 总投入产出比

| 阶段 | 行动数 | 预计时间 | 预期收益 |
|:---|:---:|:---:|:---|
| 🟢 24h 内 | 8 | 17.5h | 返工 -50%，风险 -90% |
| 🟡 本周 | 7 | 24h | 知识 +300%，流程 +100% |
| 🟠 月度 | 5 | 71h | 战略能力 +200% |

---

## ⚠️ 风险与依赖

| 风险 | 应对 |
|:---|:---|
| 行动太多执行不完 | **P0 优先**（8 个），其余排队 |
| subagent 调试耗时长 | 用 minimax 而非 GPT（更稳定） |
| OpenClaw cron 不稳 | 配 fallback：手动 + 自动 |
| 团队成员抵触 | **不强制**，先自己用 1 周，再推 |

---

## 🎯 验收标准

- [ ] 8 个 P0 行动 24h 内完成（2026-06-24 19:00 前）
- [ ] 7 个 P1 行动本周内完成（2026-06-30 前）
- [ ] 5 个 P2 行动月度评审（2026-07-23 前）
- [ ] 周度自我 review：行动 → 效果
- [ ] 月度沉淀：哪些行动值得保留，哪些要砍

---

## 📚 关联

- 15 篇 Wiki insight：`./zhongli-daoge-kb-{01..15}-*.md`
- 汇总报告：`/Users/wenbo/Documents/05_AgentOutput/agent_work/Zhongli/research_report/2026-06-25-刀哥KB_TOP15_学习总结.md`
- Nick 6-20 分析报告：`/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/research_report/2026-06-20-快刀青衣AI学习笔记分析报告.md`

---

*🛡️ 钟离 · 19:20 · 2026-06-23*  
*Nick 派单 #1/1 主体完成 · 等 6/25 验收*