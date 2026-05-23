# Wiki知识库三场景优化方案

> **版本**: v1.0
> **日期**: 2026-05-21
> **作者**: 尼克·弗瑞
> **场景**: RAG检索 / Agent访问 / 人类阅读
> **状态**: 待执行

---

## 一、背景与目标

### 1.1 问题背景

文博的Wiki知识库面临三个使用场景的差异化需求：

| 场景 | 使用者 | 核心需求 |
|:---|:---|:---|
| **RAG检索** | 知识检索系统 | 召回率+精准度 |
| **Agent访问** | 托尼/钟离/尼克 | 执行效率+机器可读 |
| **人类阅读** | 文博/团队 | 可读性+快速理解 |

### 1.2 Karpathy LLM Wiki原则

```
Raw Sources → Wiki中间层 → Schema规则
     ↓              ↓            ↓
   原始资料       编译知识        规则

核心原则：
1. 预先编译 - Wiki是持续维护的知识层，不临时检索
2. 三层架构 - Raw（事实源）→ Wiki（编译层）→ Schema（规则层）
3. Schema定义 - 组织规则、摄入流程、查询方式、校验机制
```

### 1.3 优化目标

- **RAG**：提升召回率和精准度，降低噪音
- **Agent**：支持渐进式加载，提升执行效率
- **人类**：快速理解核心要点，降低阅读成本

---

## 二、现状分析

### 2.1 Wiki结构

```
Wiki/
├── insights/              # 洞察文档（~120+）
│   ├── ai/               # AI综合（25）
│   ├── ai-coding/        # AI编程（29）
│   ├── agent/            # Agent相关（20）
│   ├── fintech/          # 金融科技（14）
│   └── product-management/ # 产品管理（6）
├── topics/               # Topic文档（9）
├── entities/             # 实体文档（4）
├── methods/              # 方法论文档
└── scripts/              # 工具脚本
    ├── topic_ingest.py   # Topic分类脚本
    └── wiki_lint.py      # 链接健康检查
```

### 2.2 当前问题

| 场景 | 问题 |
|:---|:---|
| **RAG** | 缺乏语义切片、摘要字段、Tag标注不统一 |
| **Agent** | 缺乏SKILL.md、执行索引、渐进加载机制不完善 |
| **人类** | 缺乏TL;DR、TOC、图表、排版不统一 |

### 2.3 RAG入库现状

| 组件 | 状态 |
|:---|:---|
| **topic_ingest.py** | ✅ 按keyword分类到Topic |
| **切片策略** | ⚠️ 按文件，未语义切片 |
| **Summary字段** | ❌ 缺失 |
| **Tag标注** | 🟡 部分实现 |

---

## 三、优化方案

### 3.1 RAG检索优化

#### 3.1.1 语义切片策略

**问题**：按文件切片导致上下文断裂

**方案**：
```python
# 语义切片规则
SLICE_BOUNDARIES = [
    "## ",      # 二级标题
    "### ",     # 三级标题
    "\n\n",     # 段落分隔
    "---",      # 分割线
]

# 切片大小控制
MIN_CHUNK_SIZE = 200   # 最少200字符
MAX_CHUNK_SIZE = 1000  # 最多1000字符
```

#### 3.1.2 文档结构增强

**新增字段**：

```markdown
---
title: 文档标题
date: 2026-05-21
author: 尼克·弗瑞
tags: [tech-understanding, requirement-decision]
summary: 一句话总结（50字内）
key_insights:
  - 洞察1
  - 洞察2
  - 洞察3
toc: true
---
```

#### 3.1.3 Tag体系统一

| Tag类型 | 适用场景 | 示例 |
|:---|:---|:---|
| **方法论Tag** | RAG精准检索 | tech-understanding, requirement-decision |
| **主题Tag** | 分类浏览 | agent, fintech, pm |
| **场景Tag** | Agent执行 | skill-execute, research, coding |

#### 3.1.4 RAG评分阈值

| 分数区间 | 含义 | 处理方式 |
|:---:|:---|:---|
| **0.8 - 1.0** | 高度相关 | 直接作为参考 |
| **0.6 - 0.8** | 中度相关 | 补充参考，需人工确认 |
| **0.4 - 0.6** | 弱相关 | 仅供参考 |
| **< 0.4** | 不相关 | 忽略 |

---

### 3.2 Agent访问优化

#### 3.2.1 SKILL.md编写规范

**文件位置**：`Wiki/topics/{topic}/SKILL.md`

**结构**：

```markdown
# {Topic} SKILL

> 版本: v1.0
> 更新: 2026-05-21

## L1 执行索引（Agent启动时加载）

### 能力概览
[简洁描述Agent可以用这个Skill做什么]

### 场景映射
| 场景 | 文档路径 | 触发关键词 |
|:---|:---|:---|
| 场景A | path/to/docA.md | 关键词A, 关键词B |
| 场景B | path/to/docB.md | 关键词C, 关键词D |

## L2 详细内容（按需加载）

### 执行模板
[具体的执行步骤/模板]

### 案例
[实际案例]

### 注意事项
[常见问题/避坑指南]
```

#### 3.2.2 渐进式加载机制

```
Agent启动 → L1索引加载（~1000 tokens）
         → 匹配场景 → L2按需加载（~3000 tokens）
         → 执行任务 → 结果反馈
```

#### 3.2.3 高频Topic识别

| Topic | 优先级 | 说明 |
|:---|:---:|:---|
| **agent-skills** | 🔴 | Agent Skill工程 |
| **harness-engineering** | 🔴 | Harness工程 |
| **requirement-decision** | 🟠 | 需求决策 |
| **product-design** | 🟠 | 产品设计 |
| **data-driven** | 🟡 | 数据驱动 |

---

### 3.3 人类阅读优化

#### 3.3.1 文档头模板

```markdown
# 标题

> **TL;DR**: 一句话核心总结

## 关键洞察
- 洞察1
- 洞察2
- 洞察3

## 背景
[背景说明]

## 目录
- [分析](#分析)
- [建议](#建议)
- [案例](#案例)

---

## 详细内容
...

## 参考资料
- [链接1]
- [链接2]
```

#### 3.3.2 TOC自动生成

```python
# TOC生成规则
def generate_toc(content):
    headings = extract_headings(content, level=[2, 3])
    toc = "## 目录\n"
    for h in headings:
        toc += f"- [{h.text}](#{h.anchor})\n"
    return toc
```

#### 3.3.3 图表规范

| 类型 | 使用场景 | 工具 |
|:---|:---|:---|
| **流程图** | 步骤说明 | Mermaid |
| **对比表** | 方案比较 | Markdown表格 |
| **架构图** | 系统结构 | Mermaid |

#### 3.3.4 排版规范

| 元素 | 规范 |
|:---|:---|
| **标题层级** | H1/H2/H3 清晰区分 |
| **列表** | 嵌套不超过2层 |
| **代码块** | 标注语言类型 |
| **引用** | 使用>块引用 |

---

## 四、实施计划

### 4.1 阶段划分

| 阶段 | 任务 | 优先级 | 工作量 |
|:---:|:---|:---:|:---:|
| **1** | 文档头模板标准化 | 🔴 | 小 |
| **2** | RAG语义切片优化 | 🔴 | 中 |
| **3** | 高频Topic SKILL.md编写 | 🟠 | 大 |
| **4** | TOC自动生成脚本 | 🟠 | 中 |
| **5** | Schema规则定义 | 🟡 | 小 |
| **6** | 历史文档补充摘要 | 🟡 | 大 |

### 4.2 执行顺序

```
Phase 1: 模板标准化
         ↓
Phase 2: RAG切片优化
         ↓
Phase 3: SKILL.md编写
         ↓
Phase 4: TOC脚本 + Schema
```

### 4.3 责任分工

| 任务 | 负责人 | 说明 |
|:---|:---|:---|
| **模板标准化** | 钟离 | 前端实现 |
| **RAG切片优化** | 钟离 | 脚本修改 |
| **SKILL.md编写** | 尼克 | 内容提供 |
| **TOC脚本** | 钟离 | 前端实现 |

---

## 五、Schema规则定义

### 5.1 文档组织规则

```yaml
# Wiki Schema
organization:
  topics:
    - name: agent
      subdirs: [agent-design-patterns, agent-evaluation, agent-skills, harness-engineering]
    - name: fintech
      subdirs: [consumer-finance, compliance, digital-currency]
    - name: product-management
      subdirs: [pm-workflow, pm-skills, requirement]

  file_naming:
    pattern: "insight-{date}-{topic}-{slug}.md"
    date_format: "YYYYMMDD"

  frontmatter:
    required: [title, date, author, tags]
    optional: [summary, key_insights, toc]
```

### 5.2 摄入流程

```yaml
# Ingest流程
ingest:
  step1:
    action: "内容抓取"
    output: "原始.md"
  
  step2:
    action: "语义切片"
    output: "chunks[]"
    rules: ["按标题边界切", "200-1000字符", "保留上下文"]
  
  step3:
    action: "Summary生成"
    output: "summary字段"
    rules: ["50字内", "包含核心观点"]
  
  step4:
    action: "Tag标注"
    output: "tags数组"
    rules: ["至少1个方法论Tag", "至少1个主题Tag"]
  
  step5:
    action: "RAG入库"
    output: "vector_db"
```

### 5.3 查询规则

```yaml
# Query流程
query:
  step1:
    action: "用户Query"
    input: "自然语言"
  
  step2:
    action: "混合检索"
    method: "向量+BM25+RRF"
    output: "candidates[]"
  
  step3:
    action: "评分过滤"
    filter: "score >= 0.4"
    output: "filtered[]"
  
  step4:
    action: "Tag匹配"
    match: "方法论Tag"
    output: "ranked[]"
  
  step5:
    action: "返回结果"
    output: "top_k"
```

### 5.4 校验机制

```yaml
# 健康检查
health_check:
  frequency: "weekly"
  
  checks:
    - type: "link_validation"
      description: "内部链接有效性"
    - type: "frontmatter_complete"
      description: "文档头完整性"
    - type: "tag_coverage"
      description: "Tag覆盖率"
    - type: "chunk_quality"
      description: "切片质量抽查"
```

---

## 六、示例

### 6.1 优化后文档示例

```markdown
---
title: "Agent Skill工程化开发范式深度解析"
date: 2026-05-21
author: 尼克·弗瑞
tags: [tech-understanding, agent-skills]
summary: "Skill工程通过渐进式披露机制，在保持上下文精简的同时实现能力的按需扩展，是Agent工程化的核心模式。"
key_insights:
  - "L1+L2双层注入：Agent启动时仅加载name+description，按需触发完整SKILL.md"
  - "资源层按需引用：scripts/references/assets按需加载，避免上下文爆炸"
  - "关键信息三要素：name（技能名）、description（描述）、location（路径）"
toc: true
---

> **TL;DR**: Skill工程通过渐进式披露机制实现能力扩展，是Agent工程化的核心模式。

## 关键洞察
- L1+L2双层注入避免上下文爆炸
- 资源层按需引用节省90% tokens
- 三要素（name/description/location）是SKILL基础

## 目录
- [背景](#背景)
- [核心机制](#核心机制)
- [设计模式](#设计模式)
- [实施建议](#实施建议)

---

## 背景
[详细内容...]
```

### 6.2 SKILL.md示例

```markdown
# Agent Skills SKILL

> 版本: v1.0
> 更新: 2026-05-21

## L1 执行索引

### 能力概览
本Skill涵盖Agent技能的设计、开发、评测全流程，适用于需要构建或优化Agent技能的场景。

### 场景映射

| 场景 | 文档路径 | 触发关键词 |
|:---|:---|:---|
| 技能设计 | insights/agent/agent-skills/skill-design.md | 设计技能、创建Skill |
| 技能评测 | insights/agent/agent-evaluation/ | 评测技能、benchmark |
| 技能优化 | insights/agent/agent-skills/skill-optimization.md | 优化技能、迭代 |

## L2 详细内容

### 技能设计模板

**触发条件**：用户提到"设计技能"或"创建Skill"

**执行步骤**：
1. 确定技能边界（name/description/location）
2. 编写SKILL.md结构
3. 配置渐进式加载
4. 编写测试用例

### 注意事项
- name必须唯一
- description不超过100字
- location使用绝对路径
```

---

## 七、风险与应对

| 风险 | 影响 | 应对 |
|:---|:---|:---|
| **历史文档补充工作量大** | 时间成本 | 分批执行，优先高频文档 |
| **Tag标注不一致** | 检索质量 | 制定Tag规范文档 |
| **SKILL.md编写效率** | Agent执行 | 提供模板和示例 |
| **Schema变更影响** | 现有流程 | 渐进式迁移 |

---

*作者: 尼克·弗瑞*
*日期: 2026-05-21*
*状态: 待执行*