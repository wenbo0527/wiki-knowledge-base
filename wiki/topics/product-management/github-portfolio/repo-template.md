# 仓库README模板

> 3个核心仓库的标准README模板
> 更新: 2026-04-27

---

## 模板A: fintech-cdp-analytics（CDP/分群/画像）

```markdown
# Fintech CDP Analytics Demo

## 🎯 一句话定位
企业级客户数据平台演示，覆盖**找数→画像→分群→触达**完整链路。

## 📊 业务场景
- **行业**: 金融科技（消费金融/银行/支付）
- **痛点**: 客户数据分散，标签体系缺失，营销触达效率低
- **目标**: 构建统一客户视图，实现精准分群自动化

## 💡 核心功能

### 1. 客户数据整合（找数）
- 多源数据融合：交易 + 行为 + 第三方
- 实时数据更新：T+0 客户状态同步
- 数据质量监控：完整性/一致性/时效性

### 2. 用户画像体系
| 维度 | 标签示例 |
|------|----------|
| 基础属性 | 年龄段/地域/设备 |
| 金融属性 | 额度/周期/逾期/活跃 |
| 行为标签 | 浏览/点击/转化/复购 |

### 3. 智能分群
| 分群类型 | 维度 | 策略 |
|---------|------|------|
| RFM | 最近/频率/金额 | 激活沉默用户 |
| CLV | 生命周期价值 | VIP服务 |
| Churn | 流失风险 | 预警+挽留 |

### 4. 触达激活
- 多渠道触达：App Push / SMS / 消息
- 个性化内容：标签匹配
- 效果追踪：触达→转化→ROI

## 🏗 技术架构

![架构图](assets/architecture.png)

```
数据采集 → 数据加工 → 数据服务 → 应用展示
   │          │           │          │
 SDK/API   Spark/Airflow  SQL/API   Vue 3 UI
```

## 🚀 快速开始

\`\`\`bash
git clone https://github.com/wenbo0527/fintech-cdp-analytics.git
cd fintech-cdp-analytics
npm install
npm run dev
# http://localhost:3000
\`\`\`

## 📈 核心指标

| 指标 | 值 | 说明 |
|------|-----|------|
| 客户覆盖率 | 99.5% | 数据完整度 |
| 画像维度 | 50+ | 标签数量 |
| 分群准确率 | 85%+ | 模型验证 |
| 触达转化率 | 12.3% | A/B测试 |

## 🛠 技术栈

Vue 3 | Vite | Arco Design | Python | FastAPI | PostgreSQL | Redis

## ⚠️ 声明

所有数据均为**合成/脱敏数据**，仅用于Portfolio展示。

---

**Author:** [名字] | 数据中台PM | [LinkedIn]
**Live Demo:** https://data-community-two.vercel.app
```

---

## 模板B: fintech-attribution-dashboard（归因分析）

```markdown
# Fintech Attribution Analytics

## 🎯 一句话定位
营销归因分析看板，覆盖**首触→末触→线性→MMM**全模型。

## 📊 业务场景
- **行业**: 金融科技
- **痛点**: 多渠道营销效果难量化，预算分配凭经验
- **目标**: 建立归因体系，实现数据驱动的预算优化

## 📈 核心KPI

| 指标 | 定义 | 计算 |
|------|------|------|
| CAC | 获客成本 | Spend ÷ New Customers |
| LTV | 生命周期价值 | Avg Revenue × Lifespan |
| ROAS | 广告回报率 | Revenue ÷ Ad Spend |
| M+1 Retention | 月留存 | Day30复购率 |

## 🛠 归因模型

| 模型 | SQL实现 |
|------|---------|
| First-click | `sql/attribution_first_click.sql` |
| Last-click | `sql/attribution_last_click.sql` |
| Linear | `sql/attribution_linear.sql` |
| Time-decay | `sql/attribution_time_decay.sql` |

## 🚀 快速开始

\`\`\`bash
git clone https://github.com/wenbo0527/fintech-attribution-dashboard.git
cd fintech-attribution-dashboard
pip install -r requirements.txt
streamlit run dashboard.py
\`\`\`

## ⚠️ 声明

所有数据均为**合成/脱敏数据**，仅用于Portfolio展示。

---

**Author:** [名字] | 数据中台PM | [LinkedIn]
```

---

## 模板C: fintech-data-platform（找数·看数·用数）

```markdown
# Fintech Data Platform Prototype

## 🎯 一句话定位
数据中台核心流程演示：**找数**（指标平台）→ **看数**（BI看板）→ **用数**（数据产品）。

## 📊 三大模块

### 找数（指标平台）
- 指标字典（定义+血缘）
- 指标查询（搜索+推荐）
- 指标订阅（日报/周报）

### 看数（BI看板）
- 管理驾驶舱
- 专题分析（拉新/促活/留存）
- 实时监控大屏

### 用数（数据产品）
- 智能推荐（实时推荐）
- 风险预警（实时风控）
- 营销自动化（自动化触达）

## 🏗 架构图

\`\`\`
┌────────────────────────────────────────────────┐
│                  数据中台架构                    │
├────────────────────────────────────────────────┤
│  找数 ──▶ 看数 ──▶ 用数                        │
│   │        │        │                         │
│  指标平台   BI看板   数据产品                    │
│   50+     20+      5+                        │
└────────────────────────────────────────────────┘
\`\`\`

## 🚀 快速开始

\`\`\`bash
git clone https://github.com/wenbo0527/fintech-data-platform.git
cd fintech-data-platform/apps/metrics-platform
npm install && npm run dev
\`\`\`

## ⚠️ 声明

所有数据均为**合成/脱敏数据**，仅用于Portfolio展示。

---

**Author:** [名字] | 数据中台PM | [LinkedIn]
```

---

## README检查清单

每个仓库的README必须包含：

- [ ] 一句话定位（🎯）
- [ ] 业务场景（📊）
- [ ] 核心功能/模块（💡）
- [ ] 架构图/流程图（🏗）
- [ ] 快速开始（🚀）
- [ ] 效果指标（📈）
- [ ] 技术栈（🛠）
- [ ] 数据声明（⚠️）

---

*创建: 2026-04-27*
