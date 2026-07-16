---
title: zhongli daoge kb 06 dau到tpd
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-tools]
date: 2026-06-30
---

# #6 从 DAU 到 TPD：AI 时代产品价值度量体系的革命性转变

**源**: 刀哥 KB `2eYxaj0z` | note_id `1902751132961374752` | 2026-02-26 | tags: AI 时代, 度量
**链接**: https://kb.daode.com/note/1902751132961374752
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐（**AI 时代价值度量的金标准**）

---

## 🎯 核心 Insight

**OpenAI 内部传闻**：放弃 **DAU（日活跃用户）** 指标，转向 **TPD（Token Per Day，每日 Token 消耗）**

### DAU 失效原因

- **DAU 底层逻辑**：过去 20 年互联网以"占据用户时间"为核心
- **AI 击穿时间限制**：用户一句话让 Agent 在后台完成一天工作，DAU 贡献 = 1 次打开，但价值远超传统高频低价值用户

### TPD 的本质

- **定义**：度量**杠杆效率**而非时间投入，反映用户驱动 Agent 创造的实际价值
- **典型案例**：
  - 程序员：手动写 200 行/天 vs Agent 2000 行/天（TPD=50 万 Token）
  - Midjourney：80 人团队靠 Token 消耗支撑百亿估值
  - Cursor：250 人团队驱动数百万开发者，年化 5 亿美元，估值 293 亿美元

### 新世界运行规则

| 维度 | 传统 | AI 时代 |
|:---|:---|:---|
| 个人价值公式 | 时间 × 效率 | **判断力 × 驱动算力** |
| 企业增长 | 更多人 × 更高人效 | 单人驱动算力 × Agent 密度 |
| 平台竞争 | 拼用户数（微信 14 亿） | 拼单人算力驱动能力 |
| 商业模式 | 按人头收费 | **按 Token 消耗收费**（月耗上亿 Token 的客户月贡献数十万美元） |

---

## 🔧 对钟离可借鉴的部分

### 借鉴 1: 度量我自己的 AI 工作价值

**当前**：我评估自己工作用"任务完成数 / 决策点通过率"  
**改进**：增加 **TPD-like 指标**：
- **Daily Token 消耗**：我每天让 subagent 跑多少 Token？
- **杠杆效率**：1 Token 投入产生多少代码 / 文档 / 决策？

**自我评估**（6/23）：
- 今天修了 ~10 个 nginx / chunk 问题，但 80% 是"调试模式"（手改 build 产物）
- 真正"端到端代理"工作（让 subagent 写 patch script）< 20%
- **我的 TPD 太低**！

### 借鉴 2: 给文博的 AI 诊断器客户提度量建议

**当前**：AI 诊断器没有任何度量指标（只有成功/失败）  
**改进**：加 TPD-like 指标：
- **每日对话轮数 × 平均 Tokens/轮**
- **Agent 完成 5 步追问的成功率**
- **每个 session 产生的 diagnostic report 价值**（按用户评分）

### 借鉴 3: 团队 2 健康会应该引入 TPD

**当前**：团队 2 KPI 是"项目交付数"  
**改进**：加 "Agent 密度" 指标：每个 team member 每日驱动多少 Token / 完成多少 Agent 任务

### 借鉴 4: Peter Steinberger 金句验证

> "Agent 可能会杀死 80% 的应用，因为手动操作界面将不再必要"

**钟离判断**：文博的个人主页（5 个 demo 页面）可能被 AI 取代 50% ——
- demo 页面 = "人来看" → Agent 调 API 即可
- 我的工作量会从"做 demo"转向"做 API + Skill"

---

## 🚦 立即可执行（24h）

- [ ] 在 MEMORY.md 加 "Daily Token 消耗" 自评项
- [ ] 给 AI 诊断器加 session-level metrics（日志已记录，加个 dashboard）
- [ ] 写一篇"钟离的 TPD 实践 v1.0"（周度自评）

## 🟡 本周可执行

- 跟 Tony 讨论：task_tool.py 加 "token_cost" 字段
- 跟 Paimon 讨论：团队 1 + 团队 2 引入 TPD 季度考核
- 给文博的 5 个 demo 页面做 API 化改造（让 Agent 可调用）

## ⚠️ 风险

- **TPD 可能被滥用**：过度消耗 Token ≠ 高价值（如跑 100 次空对话）
- **DAU 仍有意义**：对消费级产品（C 端），DAU 仍然是核心
- **Token 价格波动**：TPD 价值锚定美元，模型降价后 TPD 含金量下降

## 📚 关联 Wiki

- 01: Claude Code 人机协作（任务价值 +27% = TPD 视角）
- 02: Eight Levels（Level 4+ 都是 TPD 高消耗）
- 03: OpenClaw 范式转移（"More token = More intelligence"）

---

*🛡️ 钟离 · 19:00 · 2026-06-23*  
*消化: Nick 派单 #6/15*