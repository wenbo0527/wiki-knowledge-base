# #14 OpenClaw 创始人 Peter Steinberger 访谈：爆红危机与 AI Agent 未来

**源**: 刀哥 KB `2eYxaj0z` | note_id `1901568400971432816` | 2026-02-13 | tags: OpenClaw, AI Agent
**链接**: https://kb.daode.com/note/1901568400971432816
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐（**OpenClaw 治理的直接借鉴 + 安全风险警钟**）

---

## 🎯 核心 Insight

**Peter Steinberger**：OpenClaw 创始人，前 PSPDFKit 创始人

### 项目爆红与危机应对

- **改名风波**：Anthropic 48 小时改名要求（Claude 商标），OpenClaw 命名由此而来
- **加密社区骚扰**：Discord 刷屏、Twitter@轰炸、抢注账号名、散布恶意软件
- **损失**：1 万美元买 Twitter business account + 错过账号名抢注

### 项目现状

- **财务**：**每月亏损**，收入 1-2 万美元
- **社区**：ClawCon 活跃，但规模化资源瓶颈
- **收购意向**：OpenAI（速度）+ Meta（Ned + Mark 亲自测试）
- **核心诉求**：**坚持完全开源**，类似 Chrome 与 Chromium 关系

### 模型使用策略

| 模型 | 特点 | 适用 |
|:---|:---|:---|
| Claude Opus 4.6 | "太美国"，交互性强，方案优雅 | 交互式开发、创意 |
| GPT-5.3 (Codex) | "更德国"，长讨论+长执行，硬核高效 | 大规模代码生成 |

### 行业预测

- **Agent 取代 80% 独立 App**
- **AI 内容有"独特假味"**，平台需标记 AI 内容
- **程序员转型**：从"手写代码" → "与 Agent 协作"

---

## 🔧 对钟离可借鉴的部分

### 借鉴 1: 改名风波 = 我的 SKILL.md 命名要"前瞻"

**借鉴**：Peter 因为"Claude"商标被迫 48 小时改名，损失重大  
**钟离的应用**：
- SKILL.md 命名要**避开 OpenAI/Anthropic/Google 商标**
- 项目名也要避开（如不要叫 "Zhongli-OpenAI-Bridge"）

### 借鉴 2: OpenClaw 每月亏损 = 我的开源策略

**借鉴**：OpenClaw 即使爆红也每月亏损  
**钟离的应用**：
- 不要急着开源所有 SKILL.md
- 先私有化沉淀，再选择性开源
- 开源前要确保社区可持续

### 借鉴 3: 安全风险（抢注 + 恶意软件）

**借鉴**：Peter 误改个人 GitHub 账号，导致旧名被用于恶意软件  
**钟离的应用**：
- 我用 `wenbo` 账号操作前，必须确认账号隔离（**教训 86**）
- 不要在同一 GitHub 账号混用"个人"和"agent"项目

### 借鉴 4: Claude Opus vs Codex 选择策略

**借鉴**：Opus 适合"交互+创意"，Codex 适合"长执行+硬核"

**钟离的应用**：
- 创意类任务（写 PRD、写 SKILL.md）→ Claude Opus
- 长执行类（构建工具、跑批量任务）→ Codex / minimax

### 借鉴 5: "Agent 取代 80% App"

**借鉴**：Agent 会让手动操作界面消失

**钟离的应用**：
- 文博的个人主页 5 个 demo 页面，应该**逐步 API 化**让 Agent 调用
- 不再做"给人看"的 UI，做"给 Agent 调"的 API

### 借鉴 6: 程序员转型论

**借鉴**：从"手写代码" → "与 Agent 协作"

**钟离的应用**：
- 我的角色：钟离 = **架构师 + Agent 协调器**，不再是纯代码工人
- 应该把"代码工作"委派给 subagent，我做"概念设计 + 整体性 review"

---

## 🚦 立即可执行（24h）

- [ ] 检查所有 SKILL.md 命名（避免商标冲突）
- [ ] 把"Agent 取代 80% App"加入 MEMORY.md 趋势章节
- [ ] 评估我应该用 Opus 还是 Codex（任务分级）

## 🟡 本周可执行

- 写"钟离的开源策略 v1.0"（参考 Peter 的经验）
- 跟 Paimon 讨论：团队 1 的 SKILL.md 是否要开源？

## ⚠️ 风险

- **商标风险**：钟离命名时必须谨慎
- **安全风险**：GitHub 账号要隔离

## 📚 关联 Wiki

- 03: OpenClaw 范式转移（同源）
- 13: AGI-Next（行业趋势）

---

*🛡️ 钟离 · 19:16 · 2026-06-23*  
*消化: Nick 派单 #14/15 · 同源系统治理经验*