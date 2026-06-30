# OpenClaw创始人Peter Steinberger深度访谈：从爆红危机到AI Agent未来展望

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1901568400971432816
> **创建时间**: 2026-02-13 17:06:19
> **更新时间**: 2026-02-14 10:23:34
> **原始链接**: https://mp.weixin.qq.com/s?__biz=MjM5MDE0Mjc4MA==&mid=2651275489&idx=1&sn=9153668d43ba3883f35e92761dabb8d9&chksm=bc8838c61fa5103f34d1cce136a1f5670963f4ba0b7266dc9e663c7bcd5025d5ae0ce256eac2&scene=90&xtrack=1&sessionid=1770973505&subscene=93&clicktime=1770973515&enterid=1770973515&flutter_pos=3&biz_enter_id=4&ranksessionid=1770973506&jumppath=1123_1770973497315%2C1003_1770973500858%2C1001_1770973501227%2C1104_1770973506618&jumppathdepth=4&ascene=56&devicetype=iOS26.3&version=18004434&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQwdxNRET3DiRqLkIIQW7adxLXAQIE97dBBAEAAAAAAHnfMocxDzYAAAAOpnltbLcz9gKNyK89dVj0MtgELKsOIadXaZGiQ%2BJ8qbV0%2BqXr2MqlqYQmcC%2BJkhIL4Dw3VHBslmbfmDE8MrsaG4abm1Xg6HKakmQxXXQ74Zg2nud%2ByfhXcYWPnRUxv1xNKTjolT%2FNfiSMV3zIcl6GrZUDclb5q8HtyKzEAAkVwoAeykktTYU6%2F394mMWRcrJhR84Q0GxMKvl8Igue%2Bm%2FCSmR3KH0hrC2P018%2BM14xt9Huk43DpyJhReRAsAWiaN0l&pass_ticket=QCzfoHFw680CCupJ%2BfRd3JkyeFT1a3i9ADR5%2BN7p5utNW2mm4bh2mbWnQO%2BqX44S&wx_header=3

---

### **🚀 项目爆红与危机应对（改名风波）**

#### **(一) 名称演变与法律压力**

-   **初始命名**：从无人格设定的agent，到加入"龙虾坐在TARDIS里"的Doctor Who元素，先后使用**Wa-Relay**、**Claude’s**、**ClaudeBot**等名称。
    
-   **Anthropic介入**：因名称涉及Claude商标，收到Anthropic友好但强硬的改名要求，需在**48小时内**完成全平台更名。
    

#### **(二) 加密社区骚扰与抢注攻击**

-   **攻击手段**：加密社区通过Discord刷屏、Twitter@轰炸、发送哈希值逼捐、抢注账号名称（如Claude Bot、Mod Bot）并散布恶意软件。
    
-   **应对措施**：制定server rules禁止讨论crypto，花费**1万美元**购买Twitter business account获取OpenClaw名称，执行"原子级"改名作战计划。
    

#### **(三) 改名过程与损失**

-   **关键失误**：因平台无防抢注机制，5秒间隔内账号名被抢注；误改个人GitHub账号导致旧名被用于恶意软件；NPM包名被抢注。
    
-   **最终结果**：成功更名为**OpenClaw**，但未能获得OpenClaw.AI域名，部分旧域名（如claw.bot）需归还且无法跳转。
    

### **💸 项目现状与商业化抉择**

#### **(一) 运营状况**

-   **财务状态**：**每月亏损**，收入1-2万美元（来自捐赠和少量企业支持），需补贴个人维护的依赖项目。
    
-   **社区支持**：ClawCon社区氛围活跃，但规模化面临资源瓶颈。
    

#### **(二) 收购与合作意向**

-   **主要意向方**：**OpenAI**（算力和技术速度优势）、**Meta**（Ned和Mark亲自参与产品测试与代码讨论）。
    
-   **核心诉求**：坚持项目**完全开源**，类似Chrome与Chromium的关系，拒绝修改开源许可证或优先开发企业版。
    

### **🔍 AI行业洞察与技术思考**

#### **(一) AI安全与模型风险**

-   **安全恐慌过度**：MoltBot事件本质为娱乐性质，不存在真实隐私灾难；提示注入攻击成本随模型能力提升而增加。
    
-   **模型安全权衡**：弱模型（如Haiku）易遭攻击，强模型抗攻击能力强但破坏力更大，需通过sandbox、allow list降低风险。
    

#### **(二) Agentic编程的认知转换**

-   **复杂度曲线**：从简单prompt（“plz fix this”）到复杂编排（8个agent、自定义子agent工作流），最终回归极简prompt（“看看这些文件，把这些改了”）。
    
-   **核心原则**：按agent逻辑设计项目结构，接受不完美代码，优先构建"agent友好型"代码库而非个人审美偏好。
    

#### **(三) 模型对比与使用策略**

| 模型  | 特点  | 适用场景 |
| --- | --- | --- |
| **Claude Opus 4.6** | “太美国”，交互性强，需高水平操作，方案更优雅 | 交互式开发、创意性任务 |
| **GPT-5.3 (Codex)** | “更德国”，长讨论+长执行模式，硬核高效 | 大规模代码生成、系统性任务 |

### **🌐 行业趋势预测**

#### **(一) AI内容与人类创作**

-   **AI内容劣质化**：AI生成内容有"独特假味"，用户更珍惜人本创作，平台需明确标记AI内容。
    
-   **创作方式转变**：代码生成可依赖AI，但故事、情感类创作仍需人类主导，文档类内容可结合AI辅助。
    

#### **(二) 应用生态变革**

-   **Agent取代80%独立App**：AI Agent可整合多应用功能（如健身、订餐、日程），取代重复功能的独立应用，催生API化服务。
    
-   **转型压力**：抗拒转型的企业将被淘汰，顺应趋势的公司需提供Agent友好的API或服务接口。
    

#### **(三) 程序员角色演变**

-   **替代与保留**：AI将替代**手写代码工作**，但**核心创意与架构能力**不可替代；编程将演变为"与Agent协作"的新模式。
    
-   **技能迁移**：开发者需从"iOS工程师"转变为"构建者"，掌握与智能体协作的能力。
    

### **📝 补充细节**

-   **soul.md的魔法**：通过让agent自写核心价值观文档（如"不会丢下你自己飞升"），赋予AI人格化特征，探索AI意识定义。
    
-   **开发环境**：使用多屏工作流（主力MacBook外接双大屏），偏好Terminal交互，避免复杂UI干扰。
    
-   **开源理念**：拒绝巨额融资（可融几亿到几十亿），避免利益冲突损害社区，坚持无附加条件的免费开源。