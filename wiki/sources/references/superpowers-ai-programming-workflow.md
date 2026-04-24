# Superpowers：141k star，AI编程代理工作流引擎

## 基本信息
- **来源**: 微信公众号文章
- **URL**: https://mp.weixin.qq.com/s/Z-xkkcRIduubrIwUO2Sq8w
- **Star数**: 143.7k（最新）
- **主题**: AI编程代理的方法论框架

## 官方资源
- **GitHub**: https://github.com/obra/superpowers
- **作者博客**: https://blog.fsck.com/2025/10/09/superpowers/
- **Discord**: https://discord.gg/35wsABTejz
- **作者**: Jesse Vincent（Prime Radiant）

## 核心观点

### 问题诊断
当前AI编程的痛点：
- AI只有「能力」，没有「方法论」
- 会写代码，但不会规划
- 会改bug，但不知道什么时候该停下来思考
- 能在指导下工作，但不会主动把事情做得更好

### 解决方案
Superpowers是一个完整的**软件开发工作流框架**，专门为AI编程代理设计。

核心是：一套可组合的「技能」，加上初始指令，确保代理正确使用它们。

这不是一个新工具，而是一个「方法论层」，可以安装在Claude Code、Cursor、Codex、OpenCode等平台上。

## 工作流程

### 第一步：不急于写代码
代理看到需求时，不会立刻跳进去写代码，而是停下来问"你到底想做什么"——通过提问细化需求、探索替代方案。

### 第二步：分解实现计划
制定清晰到「一个热情但品味差、没有判断力、没有项目上下文、厌恶测试的初级工程师」也能跟进的实现计划。

重点强调：
- 真正的红/绿 TDD
- YAGNI（你不会需要它）
- DRY（不要重复自己）

### 第三步：子代理驱动开发
启动「子代理驱动开发」流程：代理逐个完成每个工程任务，检查和审查工作，然后继续前进。

## 核心技能库

### 开发流程
1. **brainstorming** - 写代码之前激活，通过提问细化粗略想法
2. **using-git-worktrees** - 设计批准后，在新分支创建隔离工作区
3. **writing-plans** - 将工作分解为小任务（每个2-5分钟）
4. **subagent-driven-development** - 为每个任务派发子代理，两阶段审查
5. **test-driven-development** - RED-GREEN-REFACTOR强制执行
6. **requesting-code-review** - 任务之间按严重程度报告问题
7. **finishing-a-development-branch** - 验证测试，呈现合并/PR选项

### 测试技能
- test-driven-development：RED-GREEN-REFACTOR循环
- systematic-debugging：4阶段根因流程
- verification-before-completion：确保真的修复了

### 协作技能
- brainstorming：苏格拉底式设计细化
- writing-plans：详细实现计划
- dispatching-parallel-agents：并发子代理工作流
- receiving-code-review：响应反馈

## 关键洞察

> 这是**强制工作流，不是建议**。代理在任何任务前检查相关技能。

## 安装方式
- Claude Code：`/plugin install superpowers@claude-plugins-official`
- Cursor：`/add-plugin superpowers`

## 相关主题
- [[ai-programming]] - AI编程实践
- [[agent-engineering]] - Agent工程

## 标签
#AI编程 #工作流 #方法论 #TDD #Superpowers
