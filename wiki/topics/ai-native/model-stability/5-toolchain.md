# 模型稳定性工具链
> 开源工具、商业平台、自建方案选型，支撑生产级监控落地
---
## 元信息
- **创建时间**: 2026-04-21
- **维护者": 尼克·弗瑞
- **类型": 工具指南
- **标签": #监控工具 #PSI计算 #开源工具 #平台建设 #自动化
---
## 开源工具选型
| 工具名称 | 核心能力 | 优势 | 劣势 | 适用场景 |
|----------|----------|------|------|----------|
| **Evidently AI** | 模型监控、数据漂移检测、可视化Dashboard | 开源免费，支持多种漂移检测方法，可视化好 | 实时监控能力弱，适合离线批量监控 | 中小团队快速搭建监控 |
| **SHAP** | 特征重要性计算、模型解释、基础稳定性监控 | 工业界标准，准确性高 | 不是专门的监控工具，需要二次开发 | 配合其他监控工具使用 |
| **Prometheus + Grafana** | 指标采集、可视化、报警 | 通用监控平台，可扩展性强，生态成熟 | 需要自定义开发PSI等金融指标的计算 | 有技术能力的中大型团队 |
| **Apache Superset** | 数据可视化、Dashboard | 开源免费，可视化能力强 | 需要配合数据仓库使用 | 有数据仓库基础的团队 |
| **MLflow** | 模型管理、实验跟踪、监控集成 | 模型全生命周期管理，生态完善 | 监控能力不是核心，需要集成其他工具 | 已使用MLflow管理模型的团队 |
---
## 商业平台选型
| 平台名称 | 核心能力 | 优势 | 劣势 | 适用场景 |
|----------|----------|------|------|----------|
| **Arize AI** | 模型监控、可解释性、数据漂移检测 | 专注模型监控，功能全面，支持实时监控 | 价格较高，适合中大型团队 | 中大型AI团队，有预算的机构 |
| **Fiddler** | 模型监控、可解释性、公平性检测 | 可解释性功能强，符合监管要求 | 价格较高 | 对可解释性要求高的金融机构 |
| **WhyLabs** | 模型监控、数据漂移检测 | 专注于模型监控，性价比高 | 可解释性功能弱 | 中型团队，有成本考虑的机构 |
| **阿里云PAI模型在线服务** | 模型监控、在线解释、报警 | 国内云厂商，集成方便，有中文支持 | 监控功能不是最全面 | 使用阿里云的国内金融机构 |
| **腾讯云TI-ONE** | 模型监控、自动化建模 | 国内云厂商，集成方便 | 监控功能偏基础 | 使用腾讯云的国内金融机构 |
---
## PSI计算工具实现
### Python实现（基础版）
```python
import numpy as np
import pandas as pd

def calculate_psi(expected, actual, buckets=10):
    """
    计算PSI值
    expected: 基准分布（训练集）
    actual: 实际分布（当前）
    """
    # 分箱
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf
    
    expected_bins = pd.cut(expected, bins=breakpoints, labels=False)
    actual_bins = pd.cut(actual, bins=breakpoints, labels=False)
    
    # 计算各分箱占比
    expected_pct = expected_bins.value_counts(normalize=True, sort=False).fillna(0)
    actual_pct = actual_bins.value_counts(normalize=True, sort=False).fillna(0)
    
    # 计算PSI
    psi = 0
    for i in range(buckets):
        e = expected_pct.get(i, 0.001)  # 避免除零
        a = actual_pct.get(i, 0.001)
        psi += (a - e) * np.log(a / e)
    
    return psi

def psi_interpretation(psi_value):
    """PSI值解读"""
    if psi_value < 0.1:
        return "非常稳定 ✅"
    elif psi_value < 0.25:
        return "一般稳定 ⚠️"
    elif psi_value < 0.5:
        return "严重不稳定 ❌"
    else:
        return "极度不稳定 🔴"
```
### 大规模PSI计算（生产版）
```python
# 使用Spark做大规模PSI计算
from pyspark.sql import functions as F

def calculate_psi_spark(df, feature_col, label_col, buckets=10):
    """
    使用Spark计算PSI，支持大规模数据
    """
    # 计算分位点
    quantiles = df.approxQuantile(feature_col, [i/buckets for i in range(buckets+1)], 0.01)
    
    # 分箱
    df = df.withColumn("bucket", 
        F.when(F.col(feature_col) < quantiles[1], 0)
        .when(F.col(feature_col) < quantiles[2], 1)
        ...
        .otherwise(buckets-1)
    )
    
    # 计算PSI
    expected = df.filter(F.col("split") == "train").groupBy("bucket").count()
    actual = df.filter(F.col("split") == "test").groupBy("bucket").count()
    
    # 合并计算PSI...
```
---
## 自建监控平台架构
中大型消费金融公司建议自建监控平台，架构如下：
```
┌─────────────────────────────────────────────────────────────┐
│  数据层                                                       │
│  ├── 模型输入特征（Kafka实时流 + Hive离线）                        │
│  ├── 模型输出预测分                                            │
│  ├── 标签数据（逾期标记）                                       │
│  └── 外部数据（征信、第三方数据）                                  │
├─────────────────────────────────────────────────────────────┤
│  计算层                                                       │
│  ├── 实时特征PSI计算（Flink实时流）                              │
│  ├── 离线PSI/KS/AUC计算（Spark每日批量）                        │
│  └── 特征级诊断分析（Python）                                    │
├─────────────────────────────────────────────────────────────┤
│  存储层                                                       │
│  ├── 时序数据库（InfluxDB/Prometheus）存储指标时序数据            │
│  ├── MySQL存储告警记录、处置记录                                │
│  └── Hive存储历史明细数据                                       │
├─────────────────────────────────────────────────────────────┤
│  展示层                                                       │
│  ├── Grafana/Kibana Dashboard可视化                            │
│  ├── 自定义监控大屏                                            │
│  └── 自动化报告生成（每日/每周/每月）                             │
├─────────────────────────────────────────────────────────────┤
│  告警层                                                       │
│  ├── Prometheus Alertmanager告警规则                           │
│  ├── 钉钉/短信/邮件通知                                        │
│  └── 告警升级机制（P0问题超时自动升级）                           │
└─────────────────────────────────────────────────────────────┘
```
---
## 自动化监控方案
### 每日自动检查脚本
```python
# 每日凌晨自动执行模型稳定性检查
import subprocess
from datetime import datetime

def daily_health_check():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"开始执行{today}模型健康度检查...")
    
    # 1. 计算昨日所有模型的PSI
    result = subprocess.run(["python", "calculate_psi.py", "--date", yesterday], 
                          capture_output=True)
    
    # 2. 检查是否有异常
    result = subprocess.run(["python", "check_thresholds.py"], 
                          capture_output=True)
    
    # 3. 生成报告
    result = subprocess.run(["python", "generate_report.py", "--date", yesterday],
                          capture_output=True)
    
    # 4. 发送报告
    if has_anomalies:
        send_alert(report)  # 钉钉/短信
    else:
        send_normal(report)  # 邮件
    
    print(f"{today}模型健康度检查完成")
```
### 自动化应急切换
```python
# 当PSI>0.5时自动触发切换
def auto_switch_if_needed(model_name, psi_value):
    if psi_value > 0.5:
        print(f"[P0告警] {model_name} PSI={psi_value} > 0.5，启动自动切换...")
        
        # 1. 关闭主模型
        disable_model(model_name)
        
        # 2. 启用备用模型
        backup_model = get_backup_model(model_name)
        enable_model(backup_model)
        
        # 3. 发送告警
        send_p0_alert(f"{model_name}已自动切换到{backup_model}")
        
        # 4. 创建故障工单
        create_incident(f"{model_name}模型失效，已自动切换")
```
---
## 小团队轻量方案
不需要搭建复杂平台，用定时任务+脚本+邮件即可：
1. **每日PSI计算**：Python脚本定时计算所有模型PSI，结果写入Excel
2. **邮件通知**：如果PSI超标，自动发送邮件告警
3. **Dashboard**：用Excel或者Google Sheet做简单的可视化
4. **处置记录**：用简单的工单系统记录处置过程
> 成本：1个工程师2-3周可以完成，满足基本监控需求
---
*最后更新: 2026-04-21
*维护者: 尼克·弗瑞*
