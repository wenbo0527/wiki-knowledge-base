---
title: insight 20260616  信息站  每次代码提交都跑一遍 Codex
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# [信息站] 每次代码提交都跑一遍 Codex

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1910088681931447216
> **创建时间**: 2026-05-16 13:18:29
> **更新时间**: 2026-05-16 13:18:29

---

> 快刀信息站素材 | 2026-05-16T13:18:28+08:00 | 来源：AIHOT 全部 AI 动态

# 每次代码提交都跑一遍 Codex

原标题：在每次提交上运行Codex

原文链接：https://x.com/gdb/status/2055436684666274020

发布时间：2026-05-15T23:54:28.000Z

信息评分：83.0/100

摘要：
发生了什么：Greg Brockman 转发了 OpenClaw 的做法：他们在云端常驻约 100 个 Codex 实例，每次代码提交都让 Codex 做安全审查，还让它处理 PR、issue、垃圾评论和性能回归。为什么值得关注：这不是新模型发布，而是一个把软件团队日常杂活交给一群 AI 代理的早期样本；如果 token 成本继续下降，开发流程可能先变成「AI 互相写、互相审，人只管定方向」。

推荐理由：
最有画面的是「约 100 个 Codex」同时巡逻一个项目：一个发现 6 个月前的旧 issue，另一个复现 Telegram 场景录视频，另一个开会时听到新功能就直接建 PR。它适合讲成软件公司的新荒诞日常：不是程序员用 AI 写几行代码，而是 AI 把项目管理、安全审计、客服式清理都接过去。

正文/原帖：
AIHOT 来源：X：Greg Brockman (@gdb)

中文摘要：在“tokens成本无关紧要”的未来设想下，项目通过云端持续运行约100个Codex实例，实现软件开发全流程自动化。系统自动化审查每次代码提交以发现安全问题，处理所有PR和issue：自动关联并关闭陈旧issue、去重问题并聚类报告、监控新issue并自动创建PR。智能代理能复现复杂环境、进行演示、监听会议并主动启动工作（如创建PR），同时扫描评论垃圾、验证性能基准。结合clawpatch.ai进行功能单元拆分和Vercel deepsec安全审计，最终达成极精简的自动化运营。

推荐理由：Greg Brockman 转发的这个实践把「tokens 不要钱」的极端场景搬到了眼前，Codex 无孔不入地审查、生成、监控，对还在计较 API 费用的团队来说是剂猛药，流程比模型更值得琢磨。

原文内容：run codex on every commit

引用内容：People freaking out over my AI spend. What nobody sees: Part of what excites me so much about working on OpenClaw is that I'm trying to answer the question:

How would we build software in the future if tokens don't matter?

We constant run ~100 codex in the cloud, reviewing every PR, every issue. If a fix on main lands, @clawsweeper will eventually find that 6 month old issue and close it with an exact reference.

We run codex on every commit to review for security issues (as it's far too easy to miss).

We run codex to de-duplicate issues and find clusters and send reports for the most pressing issues.

We have agents that can recreate complex setups, spin up ephemeral http://crabbox.sh machines, log into e.g. Telegram, make a video and post before/after fix on the PR.

There's codex that watch new issues and - if it fits our documented vision well, automatically create a PR of it. (that then another codex reviews)

We have codex running that scans comments for spam and blocks people.

We have codex instances running that verify performance benchmarks and report regressions into Discord.

We have agents that listen on our meetings and proactively start work, e.g. create PRs when we discuss new features while we discuss them.

We build http://clawpatch.ai to split all our projects into functional units to review and find bugs and regresssions.

We do the same split for security with Vercel's deepsec and Codex Security to find regressions and vulnerabilities.

All that automation allows us to run this project extremely lean.

标签：AI 编程、软件开发、自动化代理