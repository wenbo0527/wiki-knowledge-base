# Harness Engineering：AI Agent的操作系统

> 2026年AI工程圈最热话题深度解读

## 📌 基本信息

| 属性 | 值 |
|------|-----|
| **来源** | AGI Hunt 公众号 |
| **原文** | 《模型不是关键，Harness才是》 |
| **发布时间** | 2026-03-22 |
| **链接** | https://mp.weixin.qq.com/s/sVGeofV9uTgvhgR44q8pNA |
| **标签** | `#harness` `#agent` `#ai-engineering` `#2026` |

---

## 💡 核心洞察

### 洞察1：Harness是AI Agent的操作系统

> "模型就是CPU，算力再强，没有操作系统也跑不起来。"

Harness不是"壳"，是控制系统：
- 上下文管理
- 架构约束
- 反馈循环
- 工具链
- 生命周期管理

### 洞察2：七根杠杆量化 Harness 配置

1. AGENTS.md（60行以内）
2. 确定性约束（linter/测试）
3. 工具精简（Vercel案例：15→2工具，准确率80%→100%）
4. Sub-Agent隔离
5. 反馈循环（Agent自验证）
6. CI限速（最多两轮）
7. 垃圾回收

### 洞察3：OpenAI实战数据

- 5个月，100万行代码，1500 PR
- 人类一行没写
- 7个工程师，每人每天合并3.5 PR
- 工期是传统方式的1/10

### 洞察4：护栏悖论

> "车速越快，护栏越重要"

模型越强，越需要精心设计的约束系统。

---

## 🔗 关联知识

- [[topics/ai-native/agent-engineering]] - Agent工程实践
- [[topics/ai-native/vibe-coding]] - Vibe Coding专题
- [[insight-20260408-llm-agent]] - LLM Agent洞察

---

## 📋 参考资源

| 资源 | 链接 |
|------|------|
| OpenAI Harness博文 | https://openai.com/index/harness-engineering/ |
| Mitchell Hashimoto博客 | https://mitchellh.com/writing/my-ai-adoption-journey |
| Martin Fowler分析 | https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html |
| arxiv论文 | https://arxiv.org/abs/2603.05344v3 |

---

*维护者：尼克·弗瑞*
*收录时间：2026-04-17*
*来源：AGI Hunt 公众号*
