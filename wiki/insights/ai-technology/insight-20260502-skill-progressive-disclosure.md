# SKILL系统深度解析：渐进式披露机制与OpenCode实现架构

> 来源: Get笔记
> 原始链接: https://mp.weixin.qq.com/s/ZRCmGlXPUOmUkV6VQjDWLA
> 导入日期: 2026-05-02
> 原始ID: 1908704199224113336

### **🔍 SKILL系统核心问题与解决方案（引言）**

当用户在Claude Code中输入"帮我写一篇技术博客"时，系统会自动加载`content-research-writer`技能，这背后涉及三个核心问题：
* Claude Code如何知道要加载哪个skill？
* Skill内容如何注入到Agent上下文中？
* 为什么初始提示词不会因包含所有skill内容而"爆炸"？

**核心解决方案**：**渐进式披露（Progressive Disclosure）**——先展示能力索引，再按需加载完整指令，在"知道能力存在"和"加载完整能力"之间实现平衡。

### **🏗️ SKILL系统架构对比（背景）**

通过对比主流Agent框架的SKILL实现，OpenCode的SKILL系统因以下优势被选为研究对象：

| 特性 | OpenCode 的优势 |
| :--- | :--- |
| **标准化知识文档** | SKILL.md 采用Markdown格式，易于编写和维护 |
| **双层注入** | 系统提示词（建立认知）+ Tool描述（快速匹配）的组合设计 |
| **远程分发** | 通过HTTP + index.json实现企业级技能库管理 |
| **细粒度权限** | 支持全局配置 + Agent级别覆盖 + 通配符模式的权限控制 |

其他框架的局限性：
* **Claude Code**：简单直接但仅限自身生态
* **OpenAI GPT Actions**：偏向外部API调用，不适合领域知识注入
* **LangChain Tools**：灵活但分散，缺乏统一"技能包"概念
* **AutoGen Skills**：强绑定Python生态，不适合纯知识注入

### **🔬 OpenCode SKILL核心实现剖析（核心技术）**

#### **渐进式披露策略**

OpenCode的核心设计在于**非一次性注入**所有技能内容，而是采用**两层注入策略**：先让Agent知道可用技能，再动态加载具体内容。

#### **第一层：系统提示词注入（建立认知）**

Agent初始化时，OpenCode扫描所有可用SKILL，并将**基本信息**注入系统提示词。

**注入位置**：`src/session/system.ts:63-75`
```typescript
export async function skills(agent: Agent.Info) {  
  if (Permission.disabled(["skill"], agent.permission).has("skill")) return  
  const list = await Skill.available(agent)  
  return [  
    "Skills provide specialized instructions and workflows for specific tasks.",  
    "Use the skill tool to load a skill when a task matches its description.",  
    Skill.fmt(list, { verbose: true }),  
  ].join("\\n")  
}  
```
**注入格式**（Verbose XML）：
```xml
<available_skills>  
  <skill>  
    <name>agents-sdk</name>  
    <description>Build AI agents on Cloudflare Workers using the Agents SDK...</description>  
    <location>file:///Users/mac/.config/opencode/skills/agents-sdk/SKILL.md</location>  
  </skill>  
  <skill>  
    <name>cloudflare</name>  
    <description>Comprehensive Cloudflare platform skill covering...</description>  
    <location>file:///Users/mac/.config/opencode/skills/cloudflare/SKILL.md</location>  
  </skill>  
</available_skills>  
```
**关键信息三要素**：
* ✅ **name**：技能名称（用于后续调用）
* ✅ **description**：技能描述（帮助Agent判断匹配度）
* ✅ **location**：SKILL.md绝对路径（定位技能文件）

**设计原理**（源码注释）：
> the agents seem to ingest the information about skills a bit better if we present a more verbose version of them here and a less verbose version in tool description, rather than vice versa.

即**先在系统提示词建立完整认知框架（含location），再在Tool描述中提供简洁列表（便于快速匹配）**。

#### **第二层：Tool描述注入（快速匹配）**

在**Skill Tool的描述**中注入简洁版技能列表，优化匹配效率。

**注入位置**：`src/tool/registry.ts:240-256`
```typescript
const describeSkill = Effect.fn("ToolRegistry.describeSkill")(function* (agent: Agent.Info) {  
  const list = yield* skill.available(agent)  
  if (list.length === 0) return "No skills are currently available."  
  return [  
    "Load a specialized skill that provides domain-specific instructions and workflows.",  
    "",  
    "When you recognize that a task matches one of the available skills listed below, use this tool to load the full skill instructions.",  
    "",  
    "The skill will inject detailed instructions, workflows, and access to bundled resources (scripts, references, templates) into the conversation context.",  
    "",  
    'Tool output includes a ``` block with the loaded content.',  
    "",  
    "The following skills provide specialized sets of instructions for particular tasks:",  
    "",  
    Skill.fmt(list, { verbose: false }),  
  ].join("\\n")  
})  
```
**注入格式**（简洁Markdown）：
```markdown
## Available Skills  
- **agents-sdk**: Build AI agents on Cloudflare Workers using the Agents SDK...  
- **cloudflare**: Comprehensive Cloudflare platform skill covering Workers, Pages...  
```
**信息特点**：包含技能名称和描述，但**不包含location**，避免Tool描述过长影响可读性。

#### **skill_tool调用机制**

当Agent识别到任务匹配某个技能时，通过调用**skill_tool**加载完整内容，流程为：识别→调用→返回→执行。

**Tool参数定义**（位置：`src/tool/skill.ts:11-13`）：
```typescript
const Parameters = z.object({  
  name: z.string().describe("The name of the skill from available_skills"),  
})  
```
仅需传递技能`name`参数（来自系统提示词中的`<name>`列表）。

**调用后输出内容**：
```xml
<skill_content name="agents-sdk">  
# Skill: agents-sdk  
[SKILL.md 的完整内容]  
Base directory: file:///Users/mac/.config/opencode/skills/agents-sdk/  
Relative paths in this skill are relative to this base directory.  
Note: file list is sampled.  
<skill_files>  
<file>/Users/.config/opencode/skills/agents-sdk/references/callable.md</file>  
<file>/Users/.config/opencode/skills/agents-sdk/references/workflows.md</file>  
<file>/Users/.config/opencode/skills/agents-sdk/scripts/setup.sh</file>  
</skill_files>  
</skill_content>  
```
**输出三要素**：
1. ✅ **完整SKILL.md内容**：提供详细指令和工作流程
2. ✅ **Base directory**：技能包绝对路径，解决相对路径问题
3. ✅ **Skill files列表**：技能包中所有文件路径

**相对路径解决方案**：SKILL.md中使用相对路径（如`./scripts/setup.sh`）时，Agent通过Base directory可计算出完整路径（`file:///Users/mac/.config/opencode/skills/agents-sdk/scripts/setup.sh`），确保资源正确访问。

### **💻 开源实践：open-agent-sdk（应用案例）**

基于**Claude Agent SDK**接口设计的跨平台Agent框架，解决Claude Code深度依赖CLI的问题，具备：
* ✅ 跨平台、轻量级特性
* ✅ 兼容Claude Agent SDK接口
* ✅ 基于TypeScript，摆脱CLI限制

**GitHub地址**：zerone-agent/open-agent-sdk，继承OpenCode的渐进式披露、双层注入、远程分发等设计。

### **🎯 结论与未来展望**

OpenCode SKILL系统通过**渐进式披露**机制实现三大核心价值：
1. **Token效率**：初始提示词仅注入约200 tokens的元信息，避免资源浪费
2. **可发现性**：系统提示词建立认知框架，Tool描述提供快速匹配入口
3. **灵活性**：支持远程分发、细粒度权限和多路径资源访问

**未来发展方向**：
* 技能版本管理（多版本共存）
* 技能依赖管理（自动加载依赖技能）
* 技能测试框架（验证SKILL.md有效性）
* 技能市场生态（类似npm的技能包管理）

**核心哲学**：在"能力可见"和"资源高效"之间找到平衡，让Agent既强大又轻盈。

### **📝 补充细节**
- **渐进式披露vs一次性注入**：传统一次性注入将所有技能内容加载到提示词中（类似左侧"一次性"图示的密集圆点），导致Token爆炸；渐进式注入则分阶段加载（类似右侧"渐进式"图示的分层方块），保持轻量高效。
- **双层注入顺序重要性**：必须先系统提示词（完整认知）后Tool描述（快速匹配），反向设计会导致Agent无法正确识别技能。