---
title: zhongli daoge kb 08 teresa torres
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-tools]
date: 2026-06-30
---

# #8 Teresa Torres 的 AI 原生工作流：从 GUI 到 Claude Code + Obsidian

**源**: 刀哥 KB `2eYxaj0z` | note_id `1899335874823466856` | 2026-01-20 | tags: Claude Code, Obsidian
**链接**: https://kb.daode.com/note/1899335874823466856
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐⭐（**"微小文件 + 智能路由"是钟离 MEMORY.md 拆分的最佳参考**）

---

## 🎯 核心 Insight

**Teresa Torres**（产品管理咨询师，Lenny's Newsletter "How I AI"）从 Trello/GUI 转向 **Claude Code + Obsidian** 的 5 大核心用例：

### 用例 1: 彻底个性化的任务管理系统

- **数据本地化**：任务 = Obsidian Markdown 文件（避免平台锁定）
- **`/today` 指令**：Python 脚本扫 YAML 元数据 → 生成 `today.md`
- **自动标签化**：AI 根据内容自动分类
- **语义搜索**：突破关键词限制

### 用例 2: 降维打击的学术科研流

- **自动抓取**：arXiv / Google Scholar 定时抓论文
- **两步过滤法**：Day 1 生成清单 + Day 2 深度阅读
- **特定视角摘要**：聚焦"研究方法"+"效应值"而非泛泛
- **实战价值**：识别出 Ethan Mollick 分享论文的方法论缺陷，写出 LinkedIn 爆款

### 用例 3: "颗粒化"上下文仓库（**最关键的借鉴**）

- **微小文件策略**：信息拆为数百个小 Markdown（避免大文件处理低效）
- **智能路由配置**：Claude.md 定义规则（"业务问题查 business_profile.md"）
- **示例**：问宠物健康 → AI 仅加载"个人资料"，不加载"市场分析"，省 Token 减幻觉
- **动态学习机制**：每次对话结束问"今天学到的新知识需要记录吗？"

### 用例 4: 增强型写作伙伴

- 实时事实核查 / 风格审查 / 错别字修正 / 访谈转文章

### 用例 5: 极客式交互习惯

- **`/clear` 命令**：陷入死循环时清理对话历史
- **终端优先**：几乎所有操作通过终端指令

---

## 🔧 对钟离可借鉴的部分（**直接落地到我 MEMORY.md 拆分**）

### 借鉴 1: 微小文件 + 智能路由（**核心改进**）

**钟离的现状**：MEMORY.md 3KB（精简后）+ AGENTS.md 6KB + HEARTBEAT.md 2KB，**但还没做到"路由式加载"**

**借鉴路径**：
```
.claude/
├─ MEMORY.md          # 入口 + 路由表
├─ memory/
│  ├─ claude-code.md  # Claude Code 经验（不加载除非相关）
│  ├─ openclaw.md     # OpenClaw 治理（不加载除非相关）
│  ├─ nginx.md        # nginx 经验（不加载除非相关）
│  ├─ subagent.md     # subagent 调度
│  └─ lessons.md      # 教训区（默认加载）
└─ routes.md          # 智能路由规则
```

**路由规则示例**（写到 routes.md）：
```markdown
# 智能路由规则（仿 Teresa Torres）
- 涉及 nginx → 加载 memory/nginx.md
- 涉及 OpenClaw → 加载 memory/openclaw.md
- 涉及 Claude Code → 加载 memory/claude-code.md
- 涉及 subagent → 加载 memory/subagent.md
- 默认 → 只加载 lessons.md
```

### 借鉴 2: "每次对话结束问 AI：今天学到什么？"

**钟离的痛点**：今天和文博 19 个来回，**至少 3 个新教训**（chat box 端点、build 产物路径、cache 策略），但**没及时更新 MEMORY.md**

**改进**：每个 session 结束自动触发：
```
claude "基于今天的对话，提取 3-5 条新教训，更新到 memory/lessons.md"
```

### 借鉴 3: `/clear` 救命命令

**钟离的痛点**：今天和文博对话 19 轮后，**上下文臃肿**，注意力被淹没  
**改进**：每 10 轮执行 `/clear`，重新加载核心 MEMORY.md

### 借鉴 4: "特定视角摘要"套用到我读文章

**借鉴**：我今天读 15 篇论文，但**每篇都从架构师视角写**——借鉴 Teresa 的"特定视角"方法：
- Claude Code 类文 → 看"架构决策点"
- Skill 类文 → 看"复用模式"
- 协议类文 → 看"安全边界"

---

## 🚦 立即可执行（24h）

- [ ] 拆 MEMORY.md 为 memory/ 子目录 + routes.md
- [ ] 创建 `/clear` 斜杠命令（OpenClaw）
- [ ] 创建 "session-end self-summary" subagent（自动提取教训）

## 🟡 本周可执行

- 写"钟离的颗粒化上下文仓库 v1.0"挂到 MEMORY.md
- 把"教训 81/82/83/84/85"（今天 5 条）整理到 memory/lessons.md
- 给 AGENTS.md 加"特定视角阅读"段落

## ⚠️ 风险

- **过度拆分**：100+ 小文件可能反而降低检索效率
- **路由错误**：AI 可能错过相关文件，造成幻觉
- **动态学习噪声**：不是每条对话都值得记录

## 📚 关联 Wiki

- 04: planning-with-files（"Store, Don't Stuff" 同样思想）
- 05: Claude Code 团队化（CLAUDE.md 本身就是路由入口）

---

*🛡️ 钟离 · 19:04 · 2026-06-23*  
*消化: Nick 派单 #8/15 · **个人最想立即落地的一篇***