---
能力框架: "#tech-understanding #data-driven"
来源: "录音笔记-技术分享会 | 发布时间: 2026-05-19 | 分类: Data Infrastructure / Metadata Management"
Insight ID: insight-20260519-gravitino-lixiang
维护者: "尼克·弗瑞 | 更新: 2026-05-20"
title: insight 20260519 gravitino lixiang
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai]
date: 2026-05-23
---


## 📌 执行摘要

**核心内容**：理想汽车与小米基于Apache Gravitino构建统一元数据管理平台的实践经验。

**理想汽车成果**：
- 接入15类catalog，覆盖DBA和数仓全部主流数据源
- Spark权限管控全自动化，国内生产灰度推进，海外全量开启
- 数据血缘自动采集，覆盖DAG图谱、影响评估、敏感标签传播

**核心价值**：统一命名空间 + 开箱即用REST API + 多引擎原生支持

---

## 🏢 理想汽车案例

### 背景痛点

| 痛点 | 表现 |
|:---|:---|
| **数据源分散** | 超过15种数据源分散独立管理，无统一视图 |
| **权限不统一** | 各系统权限策略不统一，无法满足GDPR合规要求 |
| **自助发现难** | 业务方自助发现数据资产难度大，沟通成本高 |
| **跨引擎治理** | Spark、Flink、Starrocks各有权限体系，策略无法统一下发 |
| **血缘缺失** | PB级数据完全缺失血缘分析能力 |

### 核心架构

**Gravitino元数据体系位于存储层核心位置**：
- 向上为Flink、Spark、Starrocks等计算引擎提供统一元数据管理
- 向下对接湖格式完成存储编排
- 是贯穿上下游协同的关键纽带

### 四层数据模型

```
metalake → catalog → schema → entity
```

### catalog自动化注册流程

1. 业务方在自研catalog平台填写信息提交bpm审批
2. 审批通过后自动调用Gravitino REST API完成创建
3. 业务方录入schema
4. 完成entity元数据入库

### 权限体系设计

| 权限类型 | 粒度 | 说明 |
|:---|:---|:---|
| **ddl操作权限** | metalake/catalog/schema/entity四级 | 结构定义 |
| **dml数据权限** | 同上 | 数据访问 |

**角色分类**：owner（全部权限）、admin（可向下授权）、读写、只读

**实现机制**：通过Spark extension机制，对业务SQL完全无侵入

### 数据血缘采集方案

**方案选择**：SQL解析 + Gravitino lineage API组合

**上层应用**：
- DAG血缘图谱可视化
- ddl变更影响评估与审批推送
- 敏感标签沿血缘自动传播
- 结合访问日志识别核心表与僵尸表

---

## 🏢 小米案例

### 定位

Gravitino在小米定位为**统一元数据管理引擎**，当前使用基于社区1.1版本定制开发。

### 接入范围

- Iceberg、Paimon、Hive、非开源内部格式、Lance
- 上层计算引擎、数据工厂、元数据审计、生命周期管理都从Gravitino获取元数据

### Fileset增强能力

- 基于目录日期格式的TTL生命周期自动清理
- 支持managed和external两种Fileset类型
- 支持HDFS到对象存储的存储路径切换
- 用户侧统一使用GVFS协议访问

### 部署架构

- **多地域集群部署**：每个地域部署单独的Gravitino集群
- **容器化部署**：基于Kubernetes
- **底层存储**：统一MySQL + Redis缓存
- **大集群优化**：使用自研GJ分库分表中间件

---

## 💡 关键洞察

1. **统一命名空间是核心**：解决多数据源分散管理的根本问题
2. **REST API开箱即用**：无需额外开发即可接入多引擎
3. **权限管控无侵入**：通过extension机制，对业务SQL完全无感知
4. **血缘是治理抓手**：从ddl变更影响评估到敏感标签传播
5. **自动化是关键**：从catalog注册到权限申请，全流程自动化

---

## 📅 未来规划

### 理想汽车

- 2026下半年：推进Flink血缘采集、AI数据搜索与智能推荐、元数据MCP和skill能力
- 长远目标：和社区共建统一数据资产平台

### 小米

- 从0.6版本直接升级到1.1版本（跨5个大版本）
- 升级原因：接入Lance catalog + 使用job system管理能力
