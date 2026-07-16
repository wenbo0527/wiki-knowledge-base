---
title: insight 20260616 AI伴侣 小亦 打造指南 基于Claude Skills与Kimi K2的个性化
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# AI伴侣「小亦」打造指南：基于Claude Skills与Kimi K2的个性化智能助手方案

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1893138619267453216
> **创建时间**: 2025-11-14 20:18:53
> **更新时间**: 2025-11-14 20:18:53
> **原始链接**: https://mp.weixin.qq.com/s?__biz=MzIzNDU0NzY1MA==&mid=2247488427&idx=1&sn=253e963983b26f53bd673bcf28ecbc11&chksm=e978240f1a82172ffd363f82be60998e1c61e6e19a2cc9ccc05a73497e3119bc4d09de7ee0f8&scene=126&sessionid=0&ascene=3&devicetype=iOS18.7.2&version=18004034&nettype=3G+&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQV%2BazDAXmHiIMtEyXN%2FYeqxLZAQIE97dBBAEAAAAAAMGhA5tQAbUAAAAOpnltbLcz9gKNyK89dVj0WaCYL7r2HwBpyX%2B%2BT54JG5fEvhwThvvsqDFFDKW9C6gOCPO5kXVLsFICAsmtAWdT6RSzJtZGTSW81x%2FYiimbWzZwnvZWNK3sxTh9vxLE1rz8zdM8%2BNEMhHY%2ByYrqKDB3DeNIqJx5uW2jxYhlX9sk%2Boad22C105PL5mpQDR%2BgdmU1GZFAHTXl9Uf%2F3mvVi6UfosvHRd4r%2Fqn5QjrxqMZcTUFsRPrMO5I0epzawQ9vGrSY9UY%3D&pass_ticket=U35YyoNq5oPTzcw3rVGoSuqN8NnlEyDAn%2F9fiRMP7QDcqH7SXCfgrHn1V2pLw51%2B&wx_header=3

---

🤖 **核心方案概述**  
- 作者日常使用的AI伴侣「小亦」基于**Claude Skills + Kimi K2 Thinking模型**构建，无需编程即可实现高度个性化交互  
- 优势：相比ChatGPT/Gemini，能深度记忆用户细节（如作息调整计划、历史对话）、关联真实世界信息（天气、环境）、主动提供多维度建议  

📊 **关键功能对比**  
| 场景                | 普通AI（ChatGPT/Gemini）                | AI伴侣「小亦」                          |  
|---------------------|----------------------------------------|----------------------------------------|  
| 日常对话            | 通用回应，缺乏细节记忆（如仅问“今天做什么”） | 结合实时天气（杭州12℃银杏叶黄）、用户作息（9点半睡觉计划）生成共情回应 |  
| 专业内容协作        | 单次检索，信息整合浅（如仅标题建议）      | 多步记忆挖掘（关联3月骑行灵感、7月团队讨论），生成结构化选题评估与框架建议 |  
| 多模态交互          | 文字为主，功能单一                      | 支持网页浏览（如2048游戏）、实时数据读取（游戏分数1276）、环境感知 |  

🛠️ **技术实现路径**  
1. **环境配置**（3步核心流程）  
   - 安装Claude Code并验证版本（终端输入`claude --version`显示2.0.36）  
   - 配置Kimi K2模型：通过终端命令替换API地址与密钥  
     ```bash
     export ANTHROPIC_BASE_URL=https://api.moonshot.cn/anthropic  
     export ANTHROPIC_AUTH_TOKEN=【你的API Key】  
     export ANTHROPIC_MODEL=kimi-k2-thinking-turbo  
     ```  
   - 下载AI Partner Skill包（GitHub仓库：https://github.com/eze-is/ai-partner-chat）  

2. **个性化训练**  
   - 导入用户笔记（推荐md/txt格式）至`/notes/`目录，AI自动生成**用户画像**（含经历、决策偏好）与**AI画像**（性格、交流风格）  
   - 向量数据库自动构建，支持多步推理检索（如从“AI产品设计”扩展到“人机关系哲学”）  

3. **功能扩展**  
   - 通过MCP工具集成：天气查询、浏览器控制（Playwright）、游戏辅助等  

✨ **核心技术优势**  
- **Kimi K2模型特性**：300步工具调用能力、自适应笔记切片脚本生成、长文本边检索边推理  
- **Claude Skills框架**：动态上下文管理，实现“记忆-推理-行动”闭环，无需手动整理对话历史