---
title: insight 20260616 2026年清华大学AI药物发现突破 DrugCLIP技术与GenomeScree
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# 2026年清华大学AI药物发现突破：DrugCLIP技术与GenomeScreenDB数据库解析

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1898379322256453024
> **创建时间**: 2026-01-10 08:05:18
> **更新时间**: 2026-01-10 08:05:18
> **原始链接**: https://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649788125&idx=1&sn=150f251c0f6acb5dc7fc2636853700e1&chksm=867b4f2b52cec8d6fbc6c848f44abe2e49f3533fa266480fd22e25dcd084b1a22c45977dd3ef&mpshare=1&scene=1&srcid=0110YO14fyf0qgRv8ZFkFHib&sharer_shareinfo=58c04400fbfb63ff7cd354e44c5cfc3d&sharer_shareinfo_first=46c81da024982576e9fe0c1e1a0b4118&from=groupmessage&isappinstalled=0&clicktime=1768003505&enterid=1768003505&ascene=1&devicetype=iOS26.3&version=1800432b&nettype=3G+&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQtzf8zYIb0Gus2gIcCtawBxLVAQIE97dBBAEAAAAAAHdAGdvpeIYAAAAOpnltbLcz9gKNyK89dVj0gl%2BkBqHxiEeoGL9OFuHYrIDIvUIw98Ma4%2F30W0BWJToaQJYYGxiD3giMo5UQ4evqAWNBOSoKMRCIZ13FtVif9uEM3U8igOfO4p2Rq%2BcZ9RVTwEL%2FO9myNDMi4mpY9lR1%2FS%2BLSM11C9U8ssVgA9KaFyKOLs5XAhnvlf0UErKAS2fFr0bLpU7muUzZ0riTwJOkodp6OT6iI2Q%2BU9suCzWy%2Bvw4DRMZeEn5NBrQluaBUA%3D%3D&pass_ticket=Wh7wgIBlk9duFNoyabEk1Id2IF2QELlbkbh4g0Not9Eajmi1O0zF42w5pPzj0PQE&wx_header=3

---

### **🔬 AI药物发现里程碑成果（核心突破）**

**DrugCLIP技术概况**  
清华大学智能科学讲席教授张亚勤院士团队（兰艳艳教授主导）研发的**AI药物筛选工具DrugCLIP**，首次实现覆盖人类基因组规模的药物虚拟筛选，打通从蛋白结构预测到药物发现的关键通道。该工具仅需**8张顶级显卡**，即可在**24小时内完成超10万亿次蛋白质-分子匹配计算**，为近一半人类基因组（约1万个蛋白靶点、2万个蛋白口袋）找到**200万个潜在候选药物分子**，并构建全球最大规模蛋白-配体筛选数据库**GenomeScreenDB**（已免费开放）。

### **⚙️ 技术原理与创新架构（方法学）**

#### **(一) 跨模态对比学习框架**

借鉴"以文搜图"的向量匹配原理，设计双编码器架构：  
- **分子编码器**：将小分子化合物转换为特征向量  
- **口袋编码器**：将蛋白质结合口袋（药物作用位点）转换为特征向量  
- **训练目标**：通过对比学习使可结合的分子-口袋向量在数学空间中距离接近，反之远离  

#### **(二) 数据创新：伪复合物预训练**

解决真实药物-靶点数据稀缺问题：  
- 从蛋白质结构数据库截取**3-8个氨基酸片段**作为"伪配体"  
- 生成**550万个伪复合物数据**训练模型，使其掌握结合模式识别能力  

### **🚀 性能指标与验证结果（核心数据）**

| 维度                | DrugCLIP表现                          | 传统方法对比                     |
|---------------------|--------------------------------------|----------------------------------|
| **速度**            | LIT-PCBA数据集筛选仅需**38秒**       | 传统分子对接需**数天至数周**     |
| **准确率**          | DUD-E/LIT-PCBA测试集**超越所有基线** | -                                |
| **泛化能力**        | 零训练数据家族靶点仍可预测配体       | 依赖已知靶点数据                 |
| **湿实验验证命中率**| TRIP12靶点（未知结构）达**17.5%**   | 行业平均<5%                      |

#### **关键验证案例**
1. **抑郁症靶点**：从78个候选分子中发现8个纳摩尔级活性激动剂  
2. **去甲肾上腺素转运体**：找到活性优于安非他酮的新型抑制剂，冷冻电镜证实结合模式  
3. **TRIP12（癌症/神经退行性疾病靶点）**：基于AlphaFold2预测结构成功发现抑制剂  

### **🌐 GenomeScreenDB数据库（成果转化）**
- **规模**：覆盖**1万个人类蛋白质**、**2万个结合口袋**、**200万个候选分子**，靶点数量为ChEMBL数据库的2倍  
- **开放访问**：通过官网（https://drugclip.com）免费向全球科研社区开放  
- **应用价值**：降低早期药物发现壁垒，尤其助力冷门疾病靶点研究  

### **👥 研究团队与学术发表（团队背景）**
- **通讯作者**：清华大学智能产业研究院（AIR）兰艳艳教授  
- **共同一作**：贾寅君（AIR博士后）、高博文（计算机系博士生）等  
- **发表期刊**：2026年《Science》（影响因子63.714），论文标题《Deep contrastive learning enables genome-wide virtual screening》  

### **📌 补充细节**
- **技术局限性**：当前成果仍需通过ADME优化（药物吸收、分布、代谢、排泄）和临床验证才能转化为实际药物  
- **未来方向**：提升分子安全性/成药性、增强模型准确性与分子效力  
- **跨学科协作**：融合AI（深度学习）、结构生物学（AlphaFold2）、冷冻电镜技术