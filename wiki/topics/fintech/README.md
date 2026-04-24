# 金融科技 - Fintech Topics

> 金融科技最佳实践的Wiki主题索引

---

## 主题概览

| 主题 | 文件 | 来源 | 说明 | 状态 |
|------|------|------|------|------|
| **数据中台** | [data-platform.md](data-platform.md) | Day01+04 | Lambda架构、OneData、实时数仓 | ✅ |
| **风控系统** | [risk-management.md](risk-management.md) | Day05 | 智能风控、实时决策、反欺诈 | ✅ |
| **智能系统** | [intelligent-systems.md](intelligent-systems.md) | Day06+08+09 | 智能客服、智能信贷、支付系统 | ✅ |
| **营销套件** | [marketing-suite.md](marketing-suite.md) | Day03 | 精准营销、用户运营 | ✅ |
| **基础设施** | [infrastructure.md](infrastructure.md) | Day12 | 云原生、DevOps、分布式 | ✅ |
| **合规科技** | [compliance.md](compliance.md) | Day11 | 合规检查、监管科技 | ✅ |
| **开放银行** | [open-banking.md](open-banking.md) | Day10 | API开放、生态建设 | ✅ |
| **大模型金融** | [llm-finance.md](llm-finance.md) | 专题01 | LLM在金融的应用 | ✅ |
| **未来趋势** | [future-trends.md](future-trends.md) | Day13 | AI金融展望 | ✅ |

---

## 主题关系图

```
                         ┌──────────────────┐
                         │   金融科技整体   │
                         └────────┬─────────┘
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
       ▼                          ▼                          ▼
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│  数据中台   │◄────────►│   风控系统   │◄────────►│  智能系统   │
│ data-platform│          │ risk-mgmt   │          │ intelligent  │
└─────────────┘          └─────────────┘          └─────────────┘
       │                          │                          │
       │                          │                          │
       ▼                          ▼                          ▼
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│  基础设施   │          │   合规科技   │          │  开放银行   │
│infra        │          │ compliance  │          │ open-banking│
└─────────────┘          └─────────────┘          └─────────────┘
                                                             │
                                                             ▼
                                                     ┌─────────────┐
                                                     │  大模型金融 │
                                                     │ llm-finance │
                                                     └─────────────┘
```

---

## 领域分布

### 消费金融
- [数据中台](data-platform.md) - 招联、马上消费
- [风控系统](risk-management.md) - 天镜、智鹿
- [智能信贷](intelligent-systems.md) - 智能审批

### 互联网金融
- [智能客服](intelligent-systems.md) - 支小宝、微小宝
- [支付系统](intelligent-systems.md) - 支付宝、微信支付

### 传统银行
- [营销套件](marketing-suite.md) - 招行、建行
- [开放银行](open-banking.md) - API Bank

### 互联网大厂
- [数据中台](data-platform.md) - 阿里OneData、字节Flink
- [基础设施](infrastructure.md) - 腾讯云、阿里云

---

## 关键词索引

| 关键词 | 相关主题 |
|--------|----------|
| 数据中台, Lambda, Doris, Flink | [数据中台](data-platform.md) |
| 风控, 反欺诈, 知识图谱 | [风控系统](risk-management.md) |
| 客服, 智能问答, 大模型 | [智能系统](intelligent-systems.md) |
| 营销, 用户增长, A/B测试 | [营销套件](marketing-suite.md) |
| 云原生, K8s, DevOps | [基础设施](infrastructure.md) |
| 合规, 监管, AML/KYC | [合规科技](compliance.md) |
| 开放银行, API, 生态 | [开放银行](open-banking.md) |
| LLM, 大模型, RAG | [大模型金融](llm-finance.md) |

---

## Insights索引 (22个全部完成✅)

### 核心领域Insights

| Insight | 主题 | 来源 |
|---------|------|------|
| [[insight-20260408-analysis-suite]] | 分析套件 | Day02 |
| [[insight-20260408-marketing-suite]] | 营销套件 | Day03 |
| [[insight-20260408-risk-management]] | 风控系统 | Day05 |
| [[insight-20260408-customer-service]] | 智能客服 | Day06 |
| [[insight-20260408-smart-credit]] | 智能信贷 | Day08 |
| [[insight-20260408-payment]] | 支付系统 | Day09 |
| [[insight-20260408-open-banking]] | 开放银行 | Day10 |
| [[insight-20260408-regtech]] | 合规科技 | Day11 |
| [[insight-20260408-cloud-native]] | 云原生 | Day12 |
| [[insight-20260408-comprehensive-review]] | 综合复盘 | Day07 |
| [[insight-20260408-capability-roadmap]] | 能力路线图 | Day14 |
| [[insight-20260408-llm-deep-dive]] | 大模型深度 | Day15 |

### 深度专题Insights

| Insight | 主题 | 来源 |
|---------|------|------|
| [[insight-20260409-privacy-computing]] | 隐私计算 | 专题02 |
| [[insight-20260408-digital-currency]] | 数字人民币 | 专题04 |
| [[insight-20260408-llm-agent]] | LLM Agent | 概念 |

### Round3 Insights

| Insight | 主题 | 来源 |
|---------|------|------|
| [[insight-20260408-data-asset]] | 数据资产 | Day16 |
| [[insight-20260408-metrics-platform]] | 指标中台 | Day17 |
| [[insight-20260408-data-security]] | 数据安全 | Day18 |
| [[insight-20260408-aigc-product]] | AIGC产品 | Day19 |
| [[insight-20260408-open-platform]] | 开放平台 | Day20 |
| [[insight-20260408-collaboration]] | 组织协同 | Day21 |
| [[insight-20260408-p8-capability]] | P8+能力 | Day22 |

## 待补充主题

- [x] Day07_全领域_综合复盘 ✅
- [x] Day14_金融科技核心能力路线图 ✅
- [x] Day15_大模型金融应用深度调查 ✅
- [x] 专题02_实时风控架构 ✅
- [x] 专题04_数字人民币生态 ✅
- [ ] 专题03_隐私计算金融应用 (insight占位)
- [ ] 专题05_金融数据治理 (insight占位)
- [ ] 专题06_跨境金融科技 (待收集)
- [ ] 专题07_金融AI_Agent (待收集)
- [ ] 专题08_AI_Agent_Design (待收集)
- [x] Round3 Day16-22 (7个) ✅

---

## 来源

所有内容来自：
`sources/best_practices/01_核心领域_第一轮/`
`sources/best_practices/03_深度专题_待收集/`

---

*最后更新: 2026-04-08*
*维护者: 尼克·弗瑞*
---

## 消费金融 🆕

**面向个人消费者的信贷、分期、支付等金融服务**

- [[consumer-finance/README|消费金融总览]] - 行业全景与MECE结构
- [[consumer-finance/credit-card|信用卡业务]] - 贷记卡/借记卡/特权卡
- [[consumer-finance/installment|消费分期]] - 医美/教育/3C场景分期
- [[consumer-finance/cash-loan|现金贷]] - 小额信贷定价与风控
- [[consumer-finance/assisted-lending|助贷/联合贷款]] - 平台与金融机构合作
- [[consumer-finance/auto-collateral|车抵贷]] - 汽车抵押贷款的独特模式

---

## 商业世界模型关联 🆕

**AI赋能电商/金融定价是商业世界模型的核心落地场景**

- [[ai-native/business-world-model/README|商业世界模型]] - 因果推断与仿真决策
- [[ai-native/business-world-model/jd-pricing-practice|京东定价实践]] - 定价决策仿真案例

**金融应用**：信用风险定价、保险定价、贷款利率优化
