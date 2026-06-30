# #10 OpenClaw + KimiClaw 知识管理系统深度实践

**源**: 刀哥 KB `2eYxaj0z` | note_id `1902281048789181024` | 2026-02-21 | tags: OpenClaw, 第二大脑
**链接**: https://kb.daode.com/note/1902281048789181024
**派单**: INC-2026-06-23-003 · Nick 派单 · 钟离消化
**钟离评级**: ⭐⭐⭐⭐（**OpenClaw 知识管理实操模板**）

---

## 🎯 核心 Insight

**核心技术栈**：
- **OpenClaw**：开源 Agent 框架（定时任务、多源信息抓取、记忆系统）
- **KimiClaw**：手机端对话界面（云端部署 / 本地实例关联）
- **Obsidian**：本地知识库（obsidian-direct Skill 双向同步）

### 关键功能

| 模块 | 触发 | 输出 |
|:---|:---|:---|
| 视频内容追踪 | 每日 9:00 | 3 要点摘要 + 标注 |
| 财报监控 | 每周日 18:00 | Beat/Miss 状态 + EPS 对比 + AI 亮点 |
| 目标管理 | 每日 8:00 | 4-5 项可执行任务清单 |
| 邮件/Newsletter 聚合 | 每日 20:00 | 92 个长文源核心要点 |

### KimiClaw 两种接入模式

1. **一键部署**：云端 1 分钟完成（自带 K2.5 Thinking + 40G 云存储）
2. **关联本地实例**：保留历史配置、记忆、技能

### 高级技巧

- **左脚踩右脚**：Cron 每周自动检索 100+ 优质信息源
- **MVP 开发辅助**：基于日常对话自动生成产品原型
- **多模态内容**：HTML 预览 + Markdown 笔记

---

## 🔧 对钟离可借鉴的部分

### 借鉴 1: 我的知识管理改造

**当前**：MEMORY.md + Wiki，靠手动写  
**借鉴**：用 OpenClaw + Obsidian 自动化：

```
OpenClaw cron:
- 每日 9:00 抓 OpenClaw 相关 10 篇 → wiki/topics/openclaw/
- 每日 10:00 抓 Claude Code 相关 → wiki/topics/claude-code/
- 每日 18:00 抓 AI Agent 趋势 → wiki/topics/ai-agent/
- 每周日 18:00 抓 MIT/Stanford/HBS AI 报告 → wiki/reports/
```

### 借鉴 2: 信息聚合自动化的 4 个 cron

**借鉴**：参考文中表格，建我自己的 cron：

```yaml
# /etc/cron.d/zhongli-knowledge
0 9 * * *  openclaw-cron youtube-claude-code --out wiki/topics/claude-code/
0 10 * * * openclaw-cron arxiv-ai-agent --out wiki/topics/ai-agent/
0 18 * * * openclaw-cron hacker-news-ai --out wiki/topics/hn-ai/
0 18 * * 0 openclaw-cron mit-stanford-reports --out wiki/reports/
```

### 借鉴 3: "第二大脑"系统构建

**借鉴**：用 Next.js 极简 UI 看板 + 任务状态实时同步

**钟离的应用**：把 Tony 的 task_tool.py 升级为"看板 UI"（任务状态 6 种：待办/进行中/阻塞/已完成/已关闭/失败）

### 借鉴 4: 排重机制 `seen-videos.txt`

**借鉴**：避免重复处理同一内容

**钟离的应用**：MEMORY.md 加 `seen-articles.txt` 记录已读过的 KB 文章 ID

### 借鉴 5: RSS 改邮件订阅

**借鉴**：RSS 易断连，建议邮件订阅 + Playwright MCP

**钟离的应用**：把 92 个长文订阅改成邮件订阅（更稳定）

---

## 🚦 立即可执行（24h）

- [ ] 在 OpenClaw 装 obsidian-direct skill
- [ ] 建 4 个 cron（OpenClaw 主题 / Claude Code 主题 / AI Agent 主题 / 周报）
- [ ] 给 MEMORY.md 加 `seen-articles.txt`

## 🟡 本周可执行

- 用 OpenClaw 监听飞书群（自动生成周报）
- 写"钟离的第二大脑架构 v1.0"
- 把 Wiki 按"主题"重构（topics/openclaw/, topics/claude-code/）

## ⚠️ 风险

- **信息过载**：自动化抓取容易堆积垃圾
- **OpenClaw 仍不稳定**：KimiClaw 是国内云端，可能有政策风险

## 📚 关联 Wiki

- 03: OpenClaw 范式转移（同源系统）
- 09: CLAUDE.md（CLAUDE.md 就是"第二大脑"入口）

---

*🛡️ 钟离 · 19:08 · 2026-06-23*  
*消化: Nick 派单 #10/15*