# Source: Anthropic长文：多智能体协作模式，五种方法及其适用场景

> **Source ID**: source-20260419-anthropic-multi-agent-patterns  
> **原文链接**: https://mp.weixin.qq.com/s/Ag2TMKhM8qRYhy3wIpzMHQ  
> **发布平台**: 微信公众号（AI寒武纪）  
> **原文来源**: Anthropic官方博客  
> **发布时间**: 2026年4月15日  
> **抓取时间**: 2026-04-19  
> **关联Insight**: insight-20260419-anthropic-multi-agent-patterns.md

---

## 原文核心信息

**Anthropic官方长文**：多Agent协作模式指南，总结了5种架构和适用场景，何时该用多智能体系统，以及何时单智能体反而是更好的选择。

**核心观点**:
- 强烈建议从最能跑通的最简模式开始，观察它在什么地方遇到瓶颈，然后再逐步进化
- 不是按智能体能干什么活来分工，而是按它们需要什么上下文来分工

**五大模式**:
1. **生成器与验证器** - 把控输出质量且标准明确
2. **编排器与子智能体** - 清晰拆解独立子任务
3. **智能体团队** - 处理并行且长期独立作业
4. **消息总线** - 事件驱动流水线和扩展生态
5. **共享状态** - 协作研究与成果共享

**给新手的建议**:
- 对于绝大多数刚刚起步的项目，强烈建议无脑首选编排器与子智能体模式
- 它以极低的协调成本扛住了最广泛的业务场景
- 先用它跑起来，仔细观察哪里卡脖子了，再去向其他模式进化

**原文来源**: https://claude.com/blog/multi-agent-coordination-patterns

---

## 关联文档

- **深度分析**: [[insight-20260419-anthropic-multi-agent-patterns|Anthropic多智能体协作模式深度解析]]
- **相关主题**: [[topics/ai-native/agent-engineering|Agent工程]]

---

*Source存档时间: 2026-04-19*  
*存档者: 尼克·弗瑞 (Nick Fury)*
