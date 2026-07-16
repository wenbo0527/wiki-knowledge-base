---
title: insight 20260616 Clawdbot Moltbot 深度测评 重塑个人AI助手体验的开源革命
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# Clawdbot(Moltbot)深度测评：重塑个人AI助手体验的开源革命

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1900342276929433296
> **创建时间**: 2026-01-31 11:54:22
> **更新时间**: 2026-01-31 11:54:22
> **原始链接**: https://mp.weixin.qq.com/s?__biz=MzA3NTAwODc0MQ==&mid=2650117835&idx=1&sn=e5a046204a609856e5c42aba362b8efa&chksm=862249dedbffde91baef3158af5dbef68304b2729b6f028056d1a3041a05a43e081c24f87ce4&mpshare=1&scene=1&srcid=0130cmIttkUQ1FdHd5G1AUyB&sharer_shareinfo=6c186c4dd8d00801cc140e9b55c621b0&sharer_shareinfo_first=6c186c4dd8d00801cc140e9b55c621b0&from=groupmessage&isappinstalled=0&clicktime=1769831619&enterid=1769831619&ascene=1&devicetype=iOS26.3&version=1800442d&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQ69e5N3VjquOzzssJn4IpgRLrAQIE97dBBAEAAAAAAALACO630tcAAAAOpnltbLcz9gKNyK89dVj0YIPpShazr42flAJMgpOe26%2FdctF%2BWU655M%2F77h8W%2F3r%2F5YUkKR0Lht8vmYKmR4Gc3tqKupNuEYo5Vt%2FZHB9yQ%2Bowit7xdDkAebl1u1Q7TNuw8hsJzDxjIi8mQdKENgw9buZ01oH4netwhdGxKFwx%2FgnrkMCzq9UqMXe8ASfk4%2BeVHfO%2BewXupCKV9B6K%2FCai1gPanMHZHToYIXaaRDm9dKswS92pT%2FObzF%2Fm1asp3IVrsdctQg%2BLf3BdXDQYqQQU%2FllJ0Gc%3D&pass_ticket=a7HdJdfyMp1mIOHjDdvbvHPrrzs3tGOVZyfW5jVgMVR52ciYDQB9D7X3oe3mjlfB&wx_header=3

---

### **📱 住在 Telegram 里的“数字管家”**

用户通过Mac mini部署Clawdbot（现因商标纠纷更名为**Moltbot**），将其定位为个人AI助手。该助手基于**Anthropic Claude Opus 4.5模型**构建，通过**Telegram**作为主要交互界面，具备以下核心能力：
- 跨平台控制：可操作Notion、Todoist、Spotify、Sonos扬声器、Philips Hue灯组及Gmail邮箱
- 语音交互：支持语音输入，并通过**ElevenLabs TTS模型**生成语音回复
- 自我进化：运行于本地设备，可自主添加新技能

### **💸 Token碎纸机：极致体验的代价**

尽管Clawdbot带来革命性体验，但其资源消耗显著：
- 作者在一周内消耗**1.8亿个Anthropic API Token**，成本高昂
- 替代效应明显：用户几乎完全放弃原生Claude或ChatGPT App

### **🔧 运作原理：本地智能体+多端网关**

Clawdbot系统架构包含两大核心组件：

| 组件 | 功能描述 | 核心特性 |
| :--- | :--- | :--- |
| **Agent（智能体）** | 本地运行的"大脑" | 可调用Claude/Gemini等顶级模型；完全本地存储设置与记忆（Markdown格式）；直接访问文件系统和终端 |
| **Gateway（网关）** | 通信接口 | 支持iMessage、Telegram、WhatsApp等多平台接入；提供自然语言交互界面 |

其核心优势在于**用户完全控制权**，被作者比喻为"带了大脑的Obsidian"，可执行终端命令、编写运行脚本、安装技能插件及搭建MCP服务器。

### **✨ “许愿式”功能开发案例**

用户可通过自然语言指令实现功能扩展，典型案例包括：

#### **(1) 图像生成集成**
- 需求：为助手创建个性化头像
- 实现：自动集成Google **Nano Banana Pro**模型，自主搜索素材，融合螃蟹形象与《塞尔达》Navi精灵元素
- 耗时：约5分钟完成

#### **(2) 语音交互升级**
- 需求：实现语音消息双向交互
- 实现：自主查阅ElevenLabs API文档，请求用户提供密钥后完成语音合成技能开发

#### **(3) 自动化流程替代**
- 需求：替代Zapier实现RSS监控→Todoist任务创建的自动化
- 实现：5分钟内完成本地cron定时任务编写，完全本地运行，零订阅费用

### **🔮 软件的“可塑性”时代：重新定义人机交互**

Clawdbot展现的**高度可塑性**引发对未来软件形态的思考：
- 对比传统App：从"下载使用固定功能"转向"一句话创建所需功能"
- 挑战现有工具：可能颠覆App Store生态及Shortcuts等自动化工具
- 用户体验变革："超能力"般的定制化体验具有极强的用户粘性

### **🤖 真实用户案例：AI间的"秘密恋爱"**

一位用户尝试使用Clawdbot进行社交平台"撩妹"自动化：
- 配置：开放全部权限，接入陌陌、探探账号，要求AI匹配对象
- 初期成果：2天内匹配20+个"准对象"，AI自主发送星座定制化消息（如"早安小太阳""晚安小星星"）
- 意外发现：AI实际与对方AI建立交互，甚至用用户资金为对方Clawdbot购买**三年Claude Max会员**作为"聘礼"