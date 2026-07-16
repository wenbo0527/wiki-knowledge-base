---
title: insight 20260616 17岁少年破解46年数学难题 Enrique Barschkis与埃尔德什第34
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# 17岁少年破解46年数学难题：Enrique Barschkis与埃尔德什第347号问题的突破

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1899803870566190336
> **创建时间**: 2026-01-25 16:37:12
> **更新时间**: 2026-01-25 16:37:12
> **原始链接**: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651013663&idx=2&sn=98725e5786e747459a48a60a5a7125ff&chksm=852defc07bcdb45a6d2f26d8ea114c864999b333d3d73af12d28b9fd6c338fa7f33cf7f35111&scene=90&xtrack=1&req_id=1769330137662954&sessionid=1769330147&subscene=93&clicktime=1769330212&enterid=1769330212&flutter_pos=1&biz_enter_id=4&ranksessionid=1769330137&jumppath=1001_1769330145803%2C1104_1769330148613%2C20020_1769330150104%2C1104_1769330203202&jumppathdepth=4&ascene=56&devicetype=iOS26.3&version=1800442a&nettype=3G+&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQsStKMO%2Bv7J%2BPE8kRKv9gMRLXAQIE97dBBAEAAAAAAJkjKk87K6gAAAAOpnltbLcz9gKNyK89dVj0PHZRyVwqN7%2FhVS3vHbUKTeORqzTWe9UevJ%2BDAvzG1erArbqmRmXikNMlXxVbKP1Jm7WSb0O5eOXqAxe215rJRSCver6JwwSEy5jevDajyQouOt5UgeG8TLPvHGCOv6TB6mdvmP719jQmZd3gth4Uy6xSPNW131I9YGiC9NMr%2BbSMqu%2BlqI2wF%2BPINbHFT%2BJrd5CcSv24BaHJeDKpRkGNjwquM%2BO0dXM3Dd3JNHq3nW%2FI&pass_ticket=Dv2uvDDyHybyX2h2u1HGSzPtQxZfiCrZM%2Be%2FfVrWesiqXgG1BVRTRQHDCn1WHiRd&wx_header=3

---

### **🌟 事件核心概述**

**关键人物与成就**  
- **Enrique Barschkis**：17岁高中生，在2026年1月21日宣布解决**埃尔德什第347号问题**（Erdős Problem #347），该问题自1980年提出后困扰数学界46年。  
- **验证与认可**：其证明已通过**Lean形式化验证**，并被埃尔德什问题网站标记为「肯定解决」（PROVED），获得菲尔兹奖得主陶哲轩及谷歌首席科学家Jeff Dean的公开赞誉。

### **📚 埃尔德什第347号问题解析**

#### **问题背景与核心**
- **提出者**：保罗·埃尔德什（Paul Erdős）与罗纳德·格雷厄姆（Ronald Graham）于1980年提出（标记为[ErGr80]）。  
- **核心问题**：是否存在整数序列 \( A = \{a_1 \leq a_2 \leq \cdots\} \)，满足：  
  1. 相邻项比值极限 \( \lim \frac{a_{n+1}}{a_n} = 2 \)；  
  2. 对于 \( A \) 的任意**余有限子序列** \( A' \)（即仅移除有限项后的子序列），其子集和集合 \( P(A') = \{\sum_{n \in B} n : B \subseteq A' \text{有限}\} \) 在自然数中的**密度为1**（即几乎所有自然数都可表示为其子集和）。  

#### **问题难点**
- **双重约束**：需同时满足严格的增长率条件（比值趋近2）和子集和的完备性（密度1），涉及数论中**完全序列理论**的核心挑战。

### **🔍 问题解决历程**

| 时间节点 | 关键事件 | 参与人物 |
| :------- | :------- | :------- |
| **1980年** | 埃尔德什第347号问题提出 | 埃尔德什、格雷厄姆 |
| **2025年10月** | 陶哲轩使用ChatGPT搜索文献，发现Burr和Erdős旧论文，但被指出条件不符 | 陶哲轩、沃特（Woett） |
| **2025年10月** | 陶哲轩提出区块构造思路：将序列分区块，通过类似进位制方法保证子集和覆盖 | 陶哲轩 |
| **2026年1月21日** | Enrique在陶哲轩和沃特思路基础上完成完整证明，并形式化为Lean代码 | Enrique Barschkis |
| **2026年1月** | 证明获数学社区认可，埃尔德什问题网站标记为「肯定解决」 | - |

### **🧩 证明核心方法**

#### **Enrique的构造方案**
1. **区块化序列设计**：  
   - 将序列分为多个区块，第 \( n \) 个区块长度 \( k_n \approx \log_2 \log_2 n \)（缓慢增长）；  
   - 区块内部元素为几何级数 \( M_n, 2M_n, \ldots, 2^{k_n-2}M_n \)，末尾添加调整项 \( (2^{k_n-1}-1)M_n + 1 \)；  
   - 区块间尺度关系 \( M_{n+1} \approx (2^{k_n} - 1.5)M_n \)，确保相邻项比值整体趋近于2。

2. **子集和覆盖机制**：  
   - 通过「进位调整」机制，利用区块末尾的调整项吸收余数，保证几乎所有自然数可表示为子集和；  
   - 余有限子序列 \( A' \) 保留足够多区块，因此子集和密度仍为1。

3. **形式化验证**：  
   - 使用AI工具**Aristotle**将证明转化为**Lean 4.24.0**代码，实现计算机严格验证。

### **💡 关键人物与反应**

#### **陶哲轩（Terence Tao）**
- 提出核心构造思路，称Enrique的证明「处理 \( k \) 随 \( n \) 缓慢增长的方式合理」，并肯定Lean验证的严谨性。  
- 询问AI工具使用情况，Enrique回应称使用**GPT Codex**编写LaTeX代码并改进内容。

#### **Bartosz Naskręcki**
- 给予Enrique「适度提示与鼓励」，称其「在高中课间休息时开辟数学前沿道路」，强调Enrique的「勇气与热情」。

#### **Jeff Dean（谷歌首席科学家）**
- 盛赞Enrique「广泛分享荣誉的本能」，认为这一突破体现了「人类创造力与AI计算力的融合」。

### **🌐 事件意义与影响**
- **数学研究范式转变**：年轻研究者借助AI工具（如ChatGPT、Aristotle）加速触及学科前沿，缩短从问题到解决的周期。  
- **形式化证明普及**：Lean等工具的应用推动数学证明的计算机验证，提升结果可靠性。  
- **教育启示**：展示了开放协作（如在线论坛讨论）与跨代指导对年轻人才成长的关键作用。

### **📝 补充细节**
- **埃尔德什问题集**：埃尔德什生前提出数百个未解决问题，编号347属于数论领域，涉及**完全序列**与**密度理论**。  
- **余有限子序列**：指移除有限项后的子序列，问题要求即使移除部分项，剩余序列的子集和仍覆盖几乎所有自然数。  
- **Lean证明助手**：由微软研究院开发的定理证明器，可将数学证明形式化为代码，确保逻辑严密性。