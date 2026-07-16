---
title: WIKI PRINCIPLES
author: 尼克·弗瑞 🕵️
product_domain: PD-RESEARCH
doc_type: 其他
tags: []
date: 2026-04-28
---

# Wiki知识管理原则 v4.0

> Wiki知识库的构建与维护准则
>
> **版本**: v4.0
> **更新**: 2026-05-13
> **维护者**: 尼克·弗瑞
> **基于**: Karpathy LLM Wiki Pattern + MECE原则 + 混合存储方案

---

## 一、混合存储方案

### 1.1 核心原则

| 原则 | 说明 |
|:---|:---|
| **L1-L3 物理存放** | 流程/方法论/模板需要完整展示，物理存放 |
| **L4 逻辑链接** | 洞察/案例量大(600+)，只做索引+Tag，不复制 |

### 1.2 存储方式

| 层级 | 内容 | 存储方式 |
|:---|:---|:---|
| **L0 核心问题** | 能力定位 | 物理存放 |
| **L1 流程步骤** | MECE流程 | 物理存放 |
| **L2 方法论** | 方法论文档 | 物理存放 |
| **L3 模板工具** | 模板文档 | 物理存放 |
| **L4 知识填充** | 洞察/案例/最佳实践 | Tag+链接 |

---

## 二、Tag体系

### 2.1 能力Tag覆盖现状（2026-05-13）

| 能力 | Tag数 | 状态 |
|:---|:---:|:---:|
| tech-understanding | 153个 | ✅ 充足 |
| requirement-decision | 131个 | ✅ 充足 |
| value-closed-loop | 123个 | ✅ 充足 |
| risk-control | 114个 | ✅ 充足 |
| data-driven | 89个 | ✅ 充足 |
| product-design | 76个 | ✅ 充足 |

**总计: 686个洞察已Tag**

### 2.2 层级Tag

```yaml
#L1-流程
#L2-方法论
#L3-模板
#L4-知识
```

### 2.3 类型Tag

```yaml
#insight        #洞察文章
#case-study     #案例研究
#best-practice #最佳实践
#framework     #方法框架
#template      #模板工具
#tool          #工具介绍
```

### 2.4 领域Tag

```yaml
#domain-fintech     #金融科技
#domain-banking     #银行
#domain-consumer-finance  #消费金融
#domain-payment      #支付
#domain-ai           #AI领域
#domain-product      #产品管理
```

---

## 三、文档结构

### 3.1 methodologies-v2（索引目录）

```
methodologies-v2/
├── 00-框架总览/
│   ├── README.md           ← 能力框架总览+链接索引
│   ├── 能力关系网.md       ← 能力间关联
│   ├── Wiki维护机制.md     ← 维护规则
│   └── 评估报告模板.md     ← 评估模板
│
├── 01-价值闭环/
│   ├── README.md           ← 能力总览+洞察索引
│   ├── L1-流程步骤/        ← 物理存放
│   ├── L2-方法论/          ← 物理存放
│   ├── L3-模板工具/        ← 物理存放
│   └── L4-知识填充/        ← 索引文件+物理案例
│       ├── RSS最佳实践/     ← 索引文件
│       └── 文博案例/        ← 物理存放
│
├── 02-需求决策/
├── 03-数据驱动/
│   └── L2-方法论/
│       └── PDF萃取/        ← PDF萃取方法论
├── 04-产品设计/
├── 05-技术理解/
└── 06-风险防控/
    └── L2-方法论/
        └── PDF萃取/        ← 风控引擎方法论
```

### 3.2 insights（洞察原位置）

```
insights/
├── ai-coding/
│   └── insight-xxx.md     ← 包含Tag: #capability-tech-understanding #L4-知识
├── fintech/
│   └── insight-yyy.md    ← 包含Tag: #capability-data-driven
└── ...
```

---

## 四、索引文件格式

### 4.1 L4知识索引示例

```markdown
# L4: 价值闭环 - 知识索引

> 本目录不存储洞察内容，只做索引链接

## Tag筛选

筛选条件: `#capability-value-closed-loop`

## 洞察列表

共 **123** 个洞察

| 标题 | 路径 |
|:---|:---|
| 洞察标题 | [insights/xxx.md](../insights/xxx.md) |
```

---

## 五、维护规则

### 5.1 添加洞察时的Tag规则

1. 判断能力Tag（最多2个）
2. 判断层级Tag（L4知识）
3. 更新对应能力的L4索引文件

### 5.2 搜索时的Tag使用

```
搜索: #capability-data-driven #insight
→ 找到所有数据驱动相关的洞察
```

### 5.3 知识闭环

```
ingest → 打Tag → 更新索引 → 知识库
                ↓
           查询索引 → 找到原文
```

---

## 六、反模式

| ❌ 禁止 | ✅ 正确 |
|--------|--------|
| 复制洞察到能力目录 | 添加Tag+索引链接 |
| 删除洞察原文 | 保留原文，更新索引 |
| Tag冲突 | 一个洞察最多2个能力Tag |

---

## 七、PDF萃取

### 7.1 萃取文档

| 文档 | 能力方向 | 位置 |
|:---|:---|:---|
| AB实验方法论 | data-driven | 03-数据驱动/L2/PDF萃取/ |
| 指标体系方法论 | data-driven | 03-数据驱动/L2/PDF萃取/ |
| 数据采集与分析方法论 | data-driven | 03-数据驱动/L2/PDF萃取/ |
| 风控引擎方法论 | risk-control | 06-风险防控/L2/PDF萃取/ |

### 7.2 原始PDF存档

位置: `~/Downloads/已分析笔记/`（25个PDF）

---

*版本: v4.0*
*更新: 2026-05-13*
*尼克·弗瑞*
