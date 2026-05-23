# OpenClaw：开源AI代理的崛起与争议
能力框架: capability-requirement-decision capability-product-design

> **来源**: Lex Fridman Podcast #491 | **发布时间**: 2026-03 | **分类**: AI / Agent
> **Insight ID**: insight-20260328-openclaw
> **维护者**: 尼克·弗瑞 | **更新**: 2026-05-11

---

## 📌 一句话判断

> 开源AI代理OpenClaw（GitHub 18万+星）被称为"真正能做事的AI"，可自修改软件、通过WhatsApp/Telegram交互，但系统级权限也带来安全争议。

---

## 项目概况

| 维度 | 数据 |
|:---|:---|
| GitHub | 18万+ Stars |
| 定位 | 开源AI代理 |
| 原名 | Moldbot、Claudebot |
| 特点 | 自主性、可自修改软件 |

---

## 核心能力

### 1. 自主性

- 可自我修改软件
- 通过提示词修改自身代码
- 接入Claude Opus 4.6、GPT 5.3等模型

### 2. 多平台接入

支持WhatsApp、Telegram、Discord等消息平台。

### 3. 自修改软件

实现真正的自修改软件能力，可通过提示词优化或修复功能。

---

## 开发历程

| 阶段 | 名称 | 时间 |
|:---|:---|:---|
| 原型 | W relay | 2025年11月 |
| 迭代 | Claudes (W) | 2025年底 |
| 过渡 | Moldbot | 2026年初 |
| 现用 | OpenClaw | 2026年1月 |

---

## 安全争议

### 核心挑战

| 风险 | 说明 |
|:---|:---|
| 系统级权限 | 完全访问设备可能导致数据泄露 |
| 提示词注入 | 诱导执行未授权操作 |
| 供应链攻击 | 第三方插件引入恶意代码 |

### 风险缓解

- 内置网络暴露检测
- 凭证存储检查
- 与VirusTotal合作扫描

---

## 🔗 关联专题

- [[Agent]] - Agent
- [[OpenClaw]] - OpenClaw

---

## 🏷️ 标签

`#OpenClaw` `#开源AI` `#Agent` `#自修改软件` `#安全` `#争议`

---

*本文档由尼克·弗瑞基于Lex Fridman Podcast整理*
*情报是决策的基础。我不收集信息，我生产洞察。*
