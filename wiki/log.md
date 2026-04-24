# Wiki 操作日志

> 记录Wiki内容的更新历史，便于追踪知识积累过程

---

## 2026-04-21

### Ingest | 批量文章入库（3篇高质量Insight）

**执行人**: 尼克·弗瑞  
**入库时间**: 2026-04-21 07:40-08:00  
**价值评级**: ⭐⭐⭐⭐⭐ (5/5 - 极高价值)

**入库内容**:

| Insight | 来源 | 核心主题 | 关联专题 |
|:---|:---|:---|:---|
| `insight-20260421-openai-skill-evaluation` | OpenAI Skill评分调研 | Skill自动评分系统 | [[ai-native/skill-evaluation]] ⭐新增专题 |
| `insight-20260421-palantir-ontology-enterprise-ai` | DataFunTalk微信公众号 | Palantir本体论企业落地 | [[ai-native/agent-engineering]] |
| `insight-20260421-anthropic-harness-guide` | Anthropic官方博客 | Harness到期清理最佳实践 | [[ai-native/agent-engineering]] |

**创建/更新文件**:

```
wiki/
├── insights/
│   ├── insight-20260421-openai-skill-evaluation.md           # 新增
│   ├── insight-20260421-palantir-ontology-enterprise-ai.md   # 新增
│   └── insight-20260421-anthropic-harness-guide.md           # 新增
├── topics/ai-native/
│   ├── skill-evaluation.md                                     # ⭐ 新增专题
│   └── README.md                                               # 更新索引
├── sources/references/
│   ├── palantir-ontology-wechat-article-20260421.md            # 原文存档
│   └── openai-skill-evaluation-research-note.md                # 调研笔记
└── log.md                                                      # 本条目
```

**内容亮点**:

1. **OpenAI Skill评分系统**: 完整的三层混合架构（规则层/模型层/人工层），含可运行Python代码
2. **Palantir本体论**: 深度解读金融风控+云运维双场景落地，含阿里云U-Model和上海银行五级建模详细架构
3. **Anthropic Harness指南**: 官方最佳实践，强调"Build to Delete"理念，含大量Claude版本对比数据

**关联更新**:
- 更新 `ai-native/README.md` - 新增3个Insight链接和Skill Evaluation专题
- 更新 `index.md` - 同步Insight统计（34→37个）
- 更新 `WIKI_PROJECT.md` - 同步项目进度

**价值评估**: ⭐⭐⭐⭐⭐
- 三篇文章均为各自领域的高质量一手资料
- 填补了Wiki在Agent Engineering评估体系和本体论落地的空白
- 可直接用于团队技术决策参考

---

## 2026-04-19

### Project | 框架进化路线图文档创建

**执行人**: 尼克·弗瑞
**创建时间**: 2026-04-19 21:22

**创建文件**:
```
projects/
├── framework-evolution-master.md    # 框架进化总文档 (11KB)
└── tasks/
    ├── registry.md                 # 任务注册表
    ├── agent-availability.md       # Agent可用性面板
    ├── research-task.md             # 研究类任务模板
    ├── document-task.md            # 文档类任务模板
    └── task-templates/
        └── standard-task.md         # 标准任务卡片模板
```

**文档内容**:
- 5大层进化方案（协调层/知识层/产品层/技术层/情报层）
- 15个具体解决方案
- 实施计划和成功指标
- Phase 1/2/3时间线（Q3 2026 → Q4 2026 → 2027）

**更新文件**:
- `projects/README.md` - 新增框架进化项目条目
- `index.md` - 新增项目文档索引

**说明**: 基于2026-04-19今日Insights分析会议产出，将框架增强建议落地为可执行的项目文档。

---

## 2026-04-16

### Lint | Wiki健康检查与修复

**执行人**: 尼克·弗瑞
**检查时间**: 2026-04-16 09:41

**修复内容**:
- 修复 `[[real-time-risk]]` → `[[risk-management]]`
- 修复 `[[data-governance]]` → `[[insight-20260409-data-governance]]`
- 删除失效实体链接：`[[wechat-pay]]`, `[[oceanbase]]`, `[[us-markets]]`, `[[tech-indices]]`, `[[china-unicom]]`, `[[baidu]]`
- 修复 `[[analysis-frameworks]]` 自引用（5个分析框架文件）
- 修复 `[[zhaolian]]`, `[[msxf]]`, `[[duxiaoman]]` 中文实体引用
- 修复 `[[icbc]]`, `[[ping-an]]`, `[[tongdun]]` 改为普通文本
- 修复 `[[ant-cloud]]`, `[[banking-digital]]`, `[[alibaba-cloud]]` 删除
- 修复 Concept 文件中的占位符链接

**统计**:
- 检查页面总数: 171
- 修复失效链接: 27条
- 剩余模板占位符: 22条（无需修复）

**说明**: 剩余的22条"失效链接"均为模板文档中的示例占位符（如 `[[xxx]]`, `[[insight-YYYYMMDD-xxx]]`）和 lint 脚本不支持的目录级双向链接，无需修复。

---

### Lint | 孤立页面关联修复（第二轮）

**执行人**: 尼克·弗瑞
**检查时间**: 2026-04-16 10:11

**修复内容**:
- Insights → Topics 关联（7个）:
  - `insight-20260409-agent-framework` → agent-engineering.md
  - `insight-20260409-vibe-coding` → vibe-coding/README.md
  - `insight-20260414-vibe-coding` → vibe-coding/README.md
  - `insight-20260409-finance-agent` → llm-finance.md
  - `insight-20260409-openclaw-11-person-team` → openclaw-practices.md
  - `insight-20260409-privacy-computing` → compliance.md
  - `insight-20260409-agentic-ai-aws` → ai-application.md
  - `insight-20260409-ai-project-weekly` → product-management/README.md

- Entities → Topics 关联:
  - `apple` → tech-ai.md（相关实体）
  - `deepmind` → tech-ai.md（相关实体）
  - `meituan` → marketing-suite.md（相关实体）

- Vibe Coding 子专题 → 父 README 关联:
  - `gap-analysis.md`
  - `开发经验.md`
  - `通用项目架构模板.md`
  - `项目管理.md`

- Enterprise Refactoring 子专题 → 父 README 关联:
  - `brownfield-projects.md`
  - `clean-architecture.md`
  - `security-coding.md`

- tech-ai.md → 添加相关实体（apple, deepmind, nvidia 等）

- product-solutions/README.md → 添加相关洞察

**统计**:
- 检查页面总数: 173
- 孤立页面: 65 → 47（减少18个）
- Insights 孤立: 8 → 0 ✅
- Entities 孤立: 3 → 0 ✅

---

## 更新规则

### LLM Wiki三种操作

| 操作 | 说明 | 触发条件 |
|------|------|----------|
| **Ingest** | 消化新资料 | RSS抓取，最佳实践收集 |
| **Query** | 回答问题 | 用户提问 |
| **Lint** | 健康检查 | 每周/发现问题 |

### Ingest触发

当有新的source内容时：
1. 读取source文档
2. 识别关键实体/概念
3. 创建/更新相关Wiki页面
4. 更新index.md引用
5. 记录到本log.md

### Query触发

当回答用户问题时：
1. 读取index.md找到相关页面
2. 综合生成回答
3. 如果有价值，创建insight页

---

## 2026-04 操作日志

### 2026-04-15

#### Ingest | Karpathy Coding Guidelines（钟离）

**新增Source**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[sources/references/karpathy-coding-guidelines-source]] | 原始文档完整备份 |

**新增Concept**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[concepts/karpathy-coding-guidelines]] | Karpathy编码指南 - 四大核心原则 |

**内容概要**
- 来源：GitHub forrestchang/andrej-karpathy-skills
- 四大原则：Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution
- 已在AGENTS.md中添加编码规范章节

---

### 2026-04-14

#### Ingest | AI人设训练方法论（刀哥）

**新增Topic**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[topics/ai-native/ai-persona-training/README]] | AI人设训练七步法 |

**新增Insight**

| 操作 | 页面 | 来源 |
|------|------|------|
| 新建 | [[insights/insight-20260414-ai-persona-training]] | 刀哥训练案例 |

**来源**

- 刀哥（快刀青衣/得到联合创始人）

---

#### Ingest | PM晋升方法论（文博职业规划）

**新增Topic**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[topics/product-management/pm-career-development/README]] | PM晋升方法论（通用）|

**新增Insight**

| 操作 | 页面 | 来源 |
|------|------|------|
| 新建 | [[insights/insight-20260414-pm-career-development]] | 文博职业规划洞察 |

**来源**

- 文博个人职业规划（通用化整理）

---

#### Ingest | AI Programming专题大扩充

**新增Topics (2个)**

| 操作 | 页面 | 来源 |
|------|------|------|
| 新建 | [[topics/ai-programming/vibe-coding/]] | vibe-coding-cn (19k+ stars) |
| 新建 | [[topics/ai-programming/enterprise-refactoring/]] | Cursor-Windsurf-Mastery-Handbook |

**新增Vibe Coding子专题 (5个)**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[topics/ai-programming/vibe-coding/README]] | Vibe Coding总览 |
| 新建 | [[topics/ai-programming/vibe-coding/开发经验]] | 开发经验 |
| 新建 | [[topics/ai-programming/vibe-coding/通用项目架构模板]] | 架构模板 |
| 新建 | [[topics/ai-programming/vibe-coding/gap-analysis]] | 能力差距分析 |
| 新建 | [[topics/ai-programming/vibe-coding/项目管理]] | 项目管理工作拆解 |

**新增Enterprise Refactoring子专题 (4个)**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[topics/ai-programming/enterprise-refactoring/README]] | 企业重构总览 |
| 新建 | [[topics/ai-programming/enterprise-refactoring/brownfield-projects]] | Brownfield项目重构 |
| 新建 | [[topics/ai-programming/enterprise-refactoring/clean-architecture]] | Clean Architecture |
| 新建 | [[topics/ai-programming/enterprise-refactoring/security-coding]] | 安全编码实践 |

**新增AI代码审查专题 (1个)**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[topics/ai-programming/code-review-ai]] | AI-Pair异构团队协作 |

**新增AI-TDD专题 (1个)**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[topics/ai-programming/tdd-ai]] | AI时代测试驱动开发 |

**新增Insights (1个)**

| 操作 | 页面 | 来源 |
|------|------|------|
| 新建 | [[insights/insight-20260414-vibe-coding]] | Vibe Coding情报洞察 |

**结构更新**

| 操作 | 页面 | 说明 |
|------|------|------|
| 更新 | [[index]] | 新增AI Programming专题索引 |
| 更新 | [[topics/ai-native/README]] | 同步新专题进度 |
| 移动 | vibe-coding-gap-analysis.md → topics/ai-programming/vibe-coding/ | 归类整理 |
| 更新 | [[AGENT_COLLAB_GUIDE]] | 新增托尼·斯塔克角色 |

**涉及Sources**

- [vibe-coding-cn](https://github.com/2025Emma/vibe-coding-cn) (19k+ stars)
- [Cursor-Windsurf-Mastery-Handbook](https://github.com/hamodywe/Cursor-Windsurf-Mastery-Handbook)
- [AI-Pair](https://github.com/axtonliu/ai-pair)

---

### 2026-04-13

#### Ingest | 产品管理专题完善（托尼·斯塔克）

**产品管理专题内容（托尼负责）**

| 操作 | 页面 | 说明 |
|------|------|------|
| 新建 | [[topics/product-management/PRODUCT_MGMT_GUIDE]] | 产品管理指南 |
| 新建 | [[topics/product-management/PRODUCT_MGMT_WIKI]] | 产品管理知识库 |
| 新建 | [[topics/product-management/EPIC_GUIDE]] | Epic编写指南 |
| 新建 | [[topics/product-management/EPIC_DOC_PLAN]] | Epic文档计划 |
| 新建 | [[topics/product-management/EPIC_NAVIGATION]] | Epic导航 |
| 新建 | [[topics/product-management/PROJECT_HAND]] | 项目控件 |
| 新建 | [[topics/product-management/PROJECT_STATUS]] | 项目状态 |
| 新建 | [[topics/product-management/product-management-cases]] | 产品管理案例 |
| 新建 | [[topics/product-management/product-management-methodology]] | 产品管理方法论 |
| 新建 | [[topics/product-management/product-management-ontology]] | 产品管理本体论 |
| 新建 | [[topics/product-management/product-management-toolchain]] | 产品管理工具链 |
| 新建 | 8个产品线Roadmap | COM/DEX/DFD/DMT/MKT/RISK等 |
| 新建 | [[topics/product-management/epics/]] | 32个Epic文档 |

---

### 2026-04-09

#### Ingest | Wiki建设日

**新增Topics (4个)**

| 操作 | 页面 | 来源 |
|------|------|------|
| 新建 | [[topics/ai-native/README]] | 专题规划 |
| 新建 | [[topics/ai-native/ai-programming]] | 最佳实践 |
| 新建 | [[topics/ai-native/agent-engineering]] | Day15+专题08 |
| 新建 | [[topics/ai-native/ai-application]] | Day15+Day19 |
| 新建 | [[topics/ai-native/openclaw-practices]] | OpenClaw实践 |
| 新建 | [[topics/analysis-frameworks/README]] | 专题规划 |
| 新建 | [[topics/analysis-frameworks/hegang-framework]] | 何刚分析 |
| 新建 | [[topics/analysis-frameworks/majiangbo-framework]] | 马江博分析 |
| 新建 | [[topics/analysis-frameworks/caiyu-framework]] | 蔡钰商业 |
| 新建 | [[topics/analysis-frameworks/10-analysis-models]] | 经典模型 |

**新增Insights (6个)**

| 操作 | 页面 | 来源 |
|------|------|------|
| 新建 | [[insights/insight-20260409-vibe-coding]] | RSS+实践 |
| 新建 | [[insights/insight-20260409-agent-framework]] | Day15+专题08 |
| 新建 | [[insights/insight-20260409-privacy-computing]] | 专题03 |
| 新建 | [[insights/insight-20260409-data-governance]] | 专题05 |
| 新建 | [[insights/insight-20260409-cross-border-fintech]] | 专题06 |
| 新建 | [[insights/insight-20260409-finance-agent]] | 专题07 |

**新增Entities (2个)**

| 操作 | 页面 | 来源 |
|------|------|------|
| 新建 | [[entities/companies/anthropic]] | AI公司研究 |
| 新建 | [[entities/companies/deepmind]] | AI公司研究 |

**更新Topics (1个)**

| 操作 | 页面 | 说明 |
|------|------|------|
| 重构 | [[topics/tech-ai]] | AI专题主入口 |

---

### 2026-04-08

#### Ingest | Wiki初始化

**初始Topics (9个fintech)**

| 页面 | 说明 |
|------|------|
| [[topics/fintech/llm-finance]] | 大模型金融 |
| [[topics/fintech/data-platform]] | 数据中台 |
| [[topics/fintech/marketing-suite]] | 营销套件 |
| [[topics/fintech/risk-management]] | 风控系统 |
| [[topics/fintech/customer-service]] | 智能客服 |
| [[topics/fintech/payment]] | 支付系统 |
| [[topics/fintech/open-banking]] | 开放银行 |
| [[topics/fintech/regtech]] | 合规科技 |
| [[topics/fintech/cloud-native]] | 云原生架构 |

**初始Insights (22个)**

- Day01-Day15最佳实践洞察
- Round3 Day16-22洞察

**初始Entities (14个)**

- 金融公司: 蚂蚁、支付宝、微众、招联等
- 科技公司: NVIDIA、OpenAI、Apple等

---

## TODO / 待处理

### 矛盾标注

- [ ] 检查同一实体在不同页面的描述是否一致

### 过时检查

- [ ] 2026-01前的Insights需要更新

### 孤立页面

- [ ] 检查没有引用的页面

### 缺失检查

- [ ] 马江博框架内容待补充
- [ ] 蔡钰框架内容待补充

---

## 统计

| 维度 | 数量 | 维护者 |
|------|------|--------|
| Topics | 20+ | 尼克 & 钟离 & 托尼 |
| Insights | 31+ | 尼克 |
| Entities | 16+ | 尼克 |
| Concepts | 6 | 尼克 & 钟离 |
| Epics | 32+ | 托尼 |

---

*最后更新: 2026-04-14*
*维护者: 派蒙 & 尼克·弗瑞 & 钟离 & 托尼·斯塔克*
