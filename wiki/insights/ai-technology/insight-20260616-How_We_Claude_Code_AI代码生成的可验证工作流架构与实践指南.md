---
title: insight 20260616 How We Claude Code AI代码生成的可验证工作流架构与实践指南
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# How We Claude Code：AI代码生成的可验证工作流架构与实践指南

> **来源**: Get笔记
> **知识库**: ai-practice
> **导入日期**: 2026-06-16
> **原始ID**: 1912765540701373528
> **创建时间**: 2026-06-14 09:48:48
> **更新时间**: 2026-06-14 09:48:48
> **原始链接**: https://mp.weixin.qq.com/s/EDndqVkxfGFIVBqRWJxSkg

---

### **💡 核心问题与解决方案概述**

**用户痛点**：使用Claude Code等Coding Agent时，**小任务高效但复杂任务易失控**（需求理解偏差、UI反复修改、验证成本高）。  
**核心结论**：**模型能力越强，需求澄清、规格定义和结果验证就越关键**。Anthropic提出的How We Claude Code框架通过结构化工作流解决此问题，核心是将"让Agent写代码"转化为**可澄清、可比较、可验证的链路**。

### **🏗️ How We Claude Code工作流架构**

#### **(一) 架构总览**

![图1：How We Claude Code工作流架构](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0ef1695bb48f36cda90ff8b6a30e4368?Expires=1783993779&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=x5EpGfApm%2BTBfyeNjRh2P1qslck%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)  
**核心链路**：  
1. **人类判断层**：回答模糊问题，决定取舍和边界  
2. **需求采访**：通过AskUserQuestion机制将默认猜测转化为显式问题  
3. **短规格**：明确目标用户、核心流程、非目标、状态、权限、验收标准  
4. **HTML原型**：生成可视觉化的中间产物，支持多方案对比  
5. **正式实现**：基于选定规格进入代码开发  
6. **运行时验证面**：通过data-verify-*属性、fixtures等实现Agent、CI和人对结果的一致判断  

#### **(二) 新旧工作节奏对比**

![图2：两种Claude Code使用节奏](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1311d8ab3ae28a496a2c58f50daa0feb?Expires=1783993779&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0%2FCnB%2Fz0WB3mOwJqalYD1ZEhjt0%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)  

| 阶段       | 旧节奏（一次性执行）               | 新节奏（先澄清-再比较-后验证）         |
|------------|-----------------------------------|----------------------------------------|
| **需求**   | 一句需求直接开写，默认设定混进代码 | AskUserQuestion采访，显式列出不确定问题 |
| **规格**   | Markdown写得全，但界面状态靠想象  | Markdown做源文档，HTML做判断界面       |
| **反馈**   | 结果出来后截图返工，问题进入细节   | 多方案并排比较，先选方向再写代码       |
| **验证**   | 人工点一遍，Agent难稳定判断结果    | 运行时验证面，明确PASS/FAIL/BLOCKED    |

### **📝 实施三阶段详解**

#### **(一) 阶段1：需求采访——让Claude先问清楚**

**核心目标**：通过结构化提问减少Agent的默认猜测，避免后期大规模返工。  
**关键步骤**：  
1. **拒绝直接写代码**，使用模板引导Claude采访：  
   ```
   我想做一个[功能名称]。先不要写代码。  
   请采访我：目标用户、核心流程、易出错边界、异常路径、验收标准。  
   生成≤80行的SPEC.md，包含目标/非目标/状态/权限/验收/不确定问题。
   ```
2. **关键问题示例**（以分账应用为例）：  
   - 长期室友分账还是旅行临时分账？  
   - 是否需要账号系统？分享链接能否完成全部操作？  
   - 多币种支持/编辑权限/结算触发条件/异常处理（恶意修改、付款问题）。  

#### **(二) 阶段2：HTML原型——把规格变成可判断的界面**

**核心目标**：解决Markdown在UI流程、状态、布局描述中的直观性不足问题。  
**Markdown与HTML分工**：  

| 场景                 | 更适合Markdown | 更适合HTML               |
|----------------------|----------------|--------------------------|
| 规则、约束、验收标准 | 是             | 不一定                   |
| UI流程、页面状态     | 不够直观       | 是（可直接观察状态）     |
| 复杂代码diff         | 视复杂度而定   | 是（结构化展示更清晰）   |
| 长期维护的源文档     | 是             | 谨慎（维护成本高）       |

**实施模板**：  
```
读取SPEC.md。先不要实现正式代码。  
生成3个静态HTML原型，包含：  
- 核心页面/关键状态/空状态/错误状态/权限受限状态  
- 说明：适合场景与不适合场景  
保存为独立文件，支持浏览器并排比较。
```
#### **(三) 阶段3：运行时验证——让Agent和人看到同一套证据**

**核心目标**：通过DOM contract让Agent直接检查真实运行结果，避免"自我确认式"验证。  
**关键技术**：  
1. **组件暴露验证属性**：  
   ```html
   <section  
     data-verify-unit="BillingSummary"  
     data-verify-total="128.50"  
     data-verify-currency="USD"  
     data-verify-status="ready">
   ```
2. **验证体系构成**：  
   - **Fixtures**：可复现的组件状态（正常/空账单/金额不一致）  
   - **Invariants**：必须成立的不变量  
   - **验证入口**：`/verify/:unit/:fixture`接口或`window.__verify`全局变量  
   - **结果分类**：PASS（通过）/FAIL（失败）/BLOCKED（无法观察）/SKIP（跳过）  

### **🔄 从模糊想法到可验证结果的完整流程**

![图3：从模糊想法到可验证结果](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F94defa482a34b35f3ee696894f28137d?Expires=1783993779&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=B0q4BvoqfRQFuRn3ITX940lLkk4%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)  
**六步流程**：  
1. **采访**：明确目标用户、流程、边界、验收标准  
2. **短规格**：限制篇幅（≤80行），标注非目标和不确定问题  
3. **HTML方案**：生成可比较的原型（含多状态）  
4. **实现**：方向收敛后进入代码开发  
5. **验证**：通过DOM contract和fixtures检查运行结果  
6. **回看**：保留有效部分，优化流程冗余  

### **📌 最小化实施指南**

**适用场景**：  
- 2-4个页面状态的中等复杂度功能  
- 有明显权限/状态边界  
- 需截图反馈或端到端检查  
- 返工成本高但风险可控  

**实施卡片**：  
```
任务：实现[功能名]  
阶段1：采访 → 8-12个问题 → 80行SPEC.md  
阶段2：HTML原型 → 2-4个方向 → 覆盖多状态 → 人工选方向  
阶段3：验证面 → 关键组件+data-verify-* → 1个正常+1个边界fixture  
阶段4：回看 → 记录提前发现的问题/避免的返工/验证效果/可优化点
```
### **⚠️ 方法边界与局限性**
- **小任务无需全流程**：改拼写、补类型等简单任务直接执行更高效  
- **HTML非万能**：长期文档仍建议用Markdown，HTML适用于中间判断界面  
- **验证面≠测试**：需与E2E测试、类型检查、人工判断结合使用  
- **成本权衡**：HTML原型耗token，验证面需维护，需评估返工减少收益  

### **💎 关键洞察**
1. **核心价值不在工具而在节奏**：将人类判断从"结果验收"提前到"需求澄清"和"方案选择"阶段，降低后期返工成本。  
2. **HTML的独特作用**：作为"AI-人协作的视觉契约"，解决自然语言描述界面状态的歧义问题。  
3. **BLOCKED状态的重要性**：区分"无法观察"与"观察到错误"，避免验证假阳性。  
4. **渐进式落地**：先跑3次验证效果，再固化稳定环节为模板/脚本，避免流程过度复杂化。