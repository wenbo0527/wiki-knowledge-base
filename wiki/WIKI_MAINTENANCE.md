---
title: WIKI MAINTENANCE
author: 尼克·弗瑞 🕵️
product_domain: PD-RESEARCH
doc_type: 其他
tags: []
date: 2026-04-24
---

# Wiki知识库维护手册

> 规范Wiki知识库的持续运营与保鲜机制

---

## 元信息

- **创建时间**: 2026-04-24
- **更新时间**: 2026-04-30
- **维护者**: 尼克·弗瑞
- **版本**: v2.0
- **类型**: process
- **标签**: #wiki #maintenance #governance

---

## 一，维护原则

### 核心原则

| 原则 | 说明 |
|------|------|
| **内容为王** | 先有内容，再追求形式 |
| **持续迭代** | 架构不是一次成型的 |
| **用户导向** | 考虑谁会来搜索什么 |
| **保持简洁** | 避免过度工程化 |

---

## 二、角色与职责

| 角色 | 职责 | 范围 |
|------|------|------|
| **知识库Owner** | 整体规划、标准制定、重大决策 | 全部 |
| **专题维护者** | 各专题的内容更新、质量把控 | topics/ |
| **模板维护者** | Templates创建、评价、更新 | templates/ |
| **代码样例维护者** | Code Examples创建、评价、更新 | skills/code-examples/ |
| **贡献者** | 按需添加/修改内容 | 全部 |

---

## 三、文档标准

### 3.1 元信息要求

每个文档必须包含以下头部信息：

```markdown
---
title: 文档标题
created: 2026-04-24
updated: 2026-04-30
owner: 维护者名称
type: article/concept/reference
tags: #tag1 #tag2
level: 🟢公开 | 🟡内部 | 🟠敏感 | 🔴机密
review: 2026-07-24
---
```

### 3.2 命名规范

```
✅ 推荐格式
├── 产品管理
│     ├── 01_方法论
│     ├── 02_流程
│     └── 03_模板
│
└── 技术架构
      ├── overview.md
      ├── detailed-design.md
      └── changelog.md

❌ 避免格式
├── 新建文件夹
├── 文档2
├── (1)重要文件
└── final_最终版_v3
```

### 3.3 目录层级

**原则**：最多3层，禁止超过4层

```
✅ 正确示例 (3层)
wiki/topics/fintech/risk-management/README.md

❌ 错误示例 (5层)
wiki/topics/ai-native/business-world-model/jd-pricing-practice/README.md
→ 应压缩为: wiki/topics/business-world-model/jd-pricing-practice/README.md
```

---

## 四、知识库概览

| 类型 | 数量 | 说明 |
|------|------|------|
| **Insights** | 68+个 | 洞察输出（观点、分析、趋势判断） |
| **Topics** | 20+个 | 专题深度研究 |
| **Entities** | 20+个 | 实体档案（公司、产品、人物） |
| **Concepts** | 7个 | 概念定义 |
| **Code Examples** | 5+个 | 代码示例（多智能体/上下文/图记忆） |
| **Templates** | 15个 | 文档模板（产品/技术/日志/检查清单） |
| **Tools** | 2个 | 工具原型（Wiki维护/源评估） |
| **Epics** | 32+个 | 需求史诗文档 |

**存储位置**: `/Users/wenbo/Documents/project/Wiki/wiki/`

---

## 五、保鲜机制

### 5.1 定期评审日历

| 评审类型 | 频率 | 时间 | 负责人 |
|----------|------|------|--------|
| 专题Review | 每季度 | 季度末 | 专题维护者 |
| Templates评价 | 每季度 | 季度末 | 模板维护者 |
| Code Examples评价 | 每季度 | 季度末 | 代码样例维护者 |
| 全库Audit | 每半年 | 6月/12月 | 知识库Owner |
| 过期内容清理 | 每月 | 每月最后一周 | 自动+人工 |

### 5.2 保鲜规则

| 规则 | 说明 | 触发条件 |
|------|------|----------|
| **到期提醒** | 到期前30天提醒 | review日期到达 |
| **低访问警告** | 6个月无访问标记 | 访问日志分析 |
| **过时标记** | 1年未更新标记 | 时间戳判断 |
| **自动归档** | 2年未更新移至Archive | 时间戳判断 |

### 5.3 知识生命周期

```
创建 → 发布 → 维护 → 评审 → 归档/删除
  │        │        │        │
  ▼        ▼        ▼        ▼
 1周内    持续     每季度   按需
```

---

## 六、质量标准

### 6.1 文档质量检查清单

- [ ] 有完整的元信息头部
- [ ] 有清晰的标题和简介
- [ ] 内容结构清晰，有适当的标题层级
- [ ] 有相关资源链接（相关文档、外部链接）
- [ ] 有更新日志记录
- [ ] 无拼写错误和格式问题

### 6.2 专题质量标准

每个专题目录应包含：

| 文件 | 要求 | 说明 |
|------|------|------|
| `README.md` | 必须 | 专题概览、核心内容索引 |
| `*.md` | 至少3篇 | 有实质内容的文档 |
| 更新日志 | 必须 | 记录专题的重要变更 |

### 6.3 Templates质量评价（四维模型）

详见: [templates/TEMPLATE_EVALUATION.md](templates/TEMPLATE_EVALUATION.md)

| 维度 | 权重 | 说明 |
|:---|:---:|:---:|
| 完整性 | 30% | 元信息/章节/变更记录/使用说明 |
| 可用性 | 25% | 变量命名/示例/说明 |
| 规范性 | 25% | 命名/版本/状态/分级 |
| 实用性 | 20% | 可直接使用/产出质量 |

**入库阈值**: ≥60分

**状态**: 🏆≥85 | ✅60-84 | ⚠️45-59 | ❌<45

### 6.4 Code Examples质量评价（六维模型）

详见: [skills/code-examples/CODE_EXAMPLES_EVALUATION.md](skills/code-examples/CODE_EXAMPLES_EVALUATION.md)

| 维度 | 权重 | 说明 |
|:---|:---:|:---:|
| 可运行性 | 25% | 代码能否实际执行 |
| 可读性 | 20% | 代码是否清晰易懂 |
| 可复用性 | 20% | 是否易于应用到其他场景 |
| 文档完整性 | 15% | README/注释是否充分 |
| 来源可靠性 | 10% | 来源是否可追溯 |
| 组合价值 | 10% | 是否易于与其他样例组合 |

**入库阈值**: ≥60分

**状态**: 🟢≥80 | 🔵60-79 | 🟡45-59 | 🔴<45

---

## 七、Git提交规范

### 7.1 提交频率

| 场景 | 最低频率 |
|------|----------|
| 日常更新 | 每周至少1次 |
| 大型项目 | 每功能完成1次 |
| 紧急修复 | 完成后立即提交 |

### 7.2 自动Commit机制

**已配置自动Commit脚本**，无需手动执行：

| 组件 | 说明 |
|------|------|
| **定时检查** | 每30分钟自动检查变更 |
| **自动提交** | 检测到变更自动git add + commit |
| **自动推送** | 提交后自动推送到GitHub |
| **本地优先** | 推送失败不影响本地提交 |

**脚本位置**: `~/.nickfury/scripts/wiki_auto_commit.sh`
**日志位置**: `~/.nickfury/logs/wiki_auto_commit.log`
**定时任务**: `com.nickfury.wiki-auto-commit` (LaunchAgent)

**手动触发**: 
```bash
~/.nickfury/scripts/wiki_auto_commit.sh
```

**查看日志**: 
```bash
tail -f ~/.nickfury/logs/wiki_auto_commit.log
```

**停止自动任务**: 
```bash
launchctl unload /Users/wenbo/Library/LaunchAgents/com.nickfury.wiki-auto-commit.plist
```

### 7.3 提交信息格式

```
<类型>: <简短描述>

可选的详细说明

类型:
- 📚 新增: 新增文档或内容
- 🔄 更新: 内容修改或补充
- 🗑️ 删除: 删除内容
- 📋 管理: 配置、流程修改
- 🔧 维护: 格式调整、修复
- 🕵️ 情报: Insights/Templates/Code Examples更新
```

### 7.4 示例

```bash
git commit -m "🕵️ 新增Code Examples - Subagent Pattern

- 添加子智能体调度器实现
- 添加六角评价模型
- 更新README索引

相关: insight-20260430-claude-code-subagents"
```

---

## 八、备份与恢复

### 8.1 备份策略

| 备份类型 | 频率 | 位置 | 说明 |
|----------|------|------|------|
| Git自动推送 | 每次commit | GitHub | 主要备份 |
| 本地Time Machine | 每日 | 本地硬盘 | 快速恢复 |
| 关键节点备份 | 按需 | 外置硬盘 | 极端情况 |

### 8.2 恢复流程

```bash
# 从Git恢复
git clone https://github.com/wenbo0527/wiki-knowledge-base.git
cd wiki-knowledge-base
git checkout <commit-hash>

# 查看历史
git log --oneline
```

---

## 九、问题诊断

### 常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 层级过深 | 历史积累 | 定期扁平化审查 |
| 内容孤立 | 缺乏链接 | 补充双向链接 |
| 质量参差 | 无标准 | 执行本手册标准 |
| 更新滞后 | 无机制 | 启用到期提醒 |

---

## 十、附录

### 10.1 相关文档

- [WIKI_MANAGEMENT_RULES.md](./WIKI_MANAGEMENT_RULES.md) - 管理细则（v2.3）
- [WIKI_PRINCIPLES.md](./WIKI_PRINCIPLES.md) - 管理原则
- [templates/TEMPLATE_EVALUATION.md](./templates/TEMPLATE_EVALUATION.md) - Templates评价体系
- [skills/code-examples/CODE_EXAMPLES_EVALUATION.md](./skills/code-examples/CODE_EXAMPLES_EVALUATION.md) - Code Examples评价体系

### 10.2 评价体系概览

| 体系 | 评估对象 | 维度 | 入库阈值 |
|:---|:---|:---:|:---:|
| Insights | 洞察文档 | 来源可靠性+价值评级 | ⭐⭐⭐+ |
| Templates | 文档模板 | 四维（完整/可用/规范/实用） | ≥60分 |
| Code Examples | 代码样例 | 六维（运行/可读/复用/文档/来源/组合） | ≥60分 |
| Tools | 工具原型 | 状态定义（✅/🟡/❌） | 实际使用 |

### 10.3 自动化工具

```bash
# Wiki健康检查
cd /Users/wenbo/Documents/project/Wiki
python3 wiki/tools/wiki-maintenance/wiki_lint.py

# 检查深层目录
find wiki -type d -depth 4 -not -path '*/.*'

# 检查缺少README的目录
find wiki/topics -mindepth 2 -type d | while read d; do 
  [ ! -f "$d/README.md" ] && echo "缺少: $d"
done
```

---

## 版本历史

| 版本 | 日期 | 更新内容 | 更新人 |
|:---:|:---|:---|:---:|
| v1.0 | 2026-04-24 | 初始版本 | 尼克·弗瑞 |
| v2.0 | 2026-04-30 | 新增Templates/Code Examples评价体系、知识库概览更新 | 尼克·弗瑞 |

---

*最后更新: 2026-04-30*
*维护者: 尼克·弗瑞*
*下次评审: 2026-07-01*
