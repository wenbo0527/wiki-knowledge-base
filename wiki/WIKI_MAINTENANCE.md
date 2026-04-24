# Wiki知识库维护手册

> 规范Wiki知识库的持续运营与保鲜机制

---

## 元信息

- **创建时间**: 2026-04-24
- **维护者**: 尼克·弗瑞
- **类型**: process
- **标签**: #wiki #maintenance #governance

---

## 一、维护原则

### 核心原则

| 原则 | 说明 |
|------|------|
| **内容为王** | 先有内容，再追求形式 |
| **持续迭代** | 架构不是一次成型的 |
| **用户导向** | 考虑谁会来搜索什么 |
| **保持简洁** | 避免过度工程化 |

---

## 二、角色与职责

| 角色 | 职责 |
|------|------|
| **知识库Owner** | 整体规划、标准制定、重大决策 |
| **专题维护者** | 各专题的内容更新、质量把控 |
| **贡献者** | 按需添加/修改内容 |

---

## 三、文档标准

### 3.1 元信息要求

每个文档必须包含以下头部信息：

```markdown
---
title: 文档标题
created: 2026-04-24
updated: 2026-04-24
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

## 四、保鲜机制

### 4.1 定期评审日历

| 评审类型 | 频率 | 时间 | 负责人 |
|----------|------|------|--------|
| 专题Review | 每季度 | 季度末 | 专题维护者 |
| 全库Audit | 每半年 | 6月/12月 | 知识库Owner |
| 过期内容清理 | 每月 | 每月最后一周 | 自动+人工 |

### 4.2 保鲜规则

| 规则 | 说明 | 触发条件 |
|------|------|----------|
| **到期提醒** | 到期前30天提醒 | review日期到达 |
| **低访问警告** | 6个月无访问标记 | 访问日志分析 |
| **过时标记** | 1年未更新标记 | 时间戳判断 |
| **自动归档** | 2年未更新移至Archive | 时间戳判断 |

### 4.3 知识生命周期

```
创建 → 发布 → 维护 → 评审 → 归档/删除
  │        │        │        │
  ▼        ▼        ▼        ▼
 1周内    持续     每季度   按需
```

---

## 五、质量标准

### 5.1 文档质量检查清单

- [ ] 有完整的元信息头部
- [ ] 有清晰的标题和简介
- [ ] 内容结构清晰，有适当的标题层级
- [ ] 有相关资源链接（相关文档、外部链接）
- [ ] 有更新日志记录
- [ ] 无拼写错误和格式问题

### 5.2 专题质量标准

每个专题目录应包含：

| 文件 | 要求 | 说明 |
|------|------|------|
| `README.md` | 必须 | 专题概览、核心内容索引 |
| `*.md` | 至少3篇 | 有实质内容的文档 |
| 更新日志 | 必须 | 记录专题的重要变更 |

---

## 六、Git提交规范

### 6.1 提交频率

| 场景 | 最低频率 |
|------|----------|
| 日常更新 | 每周至少1次 |
| 大型项目 | 每功能完成1次 |
| 紧急修复 | 完成后立即提交 |

### 6.2 提交信息格式

```
<类型>: <简短描述>

可选的详细说明

类型:
- 📚 新增: 新增文档或内容
- 🔄 更新: 内容修改或补充
- 🗑️ 删除: 删除内容
- 📋 管理: 配置、流程修改
- 🔧 维护: 格式调整、修复
```

### 6.3 示例

```bash
git commit -m "📚 新增AI编程专题 - Claude Code并行开发指南

- 添加Subagents使用指南
- 添加Agent Teams配置
- 添加Git Worktree工作流

相关Issue: #12"
```

---

## 七、备份与恢复

### 7.1 备份策略

| 备份类型 | 频率 | 位置 | 说明 |
|----------|------|------|------|
| Git自动推送 | 每次commit | GitHub | 主要备份 |
| 本地Time Machine | 每日 | 本地硬盘 | 快速恢复 |
| 关键节点备份 | 按需 | 外置硬盘 | 极端情况 |

### 7.2 恢复流程

```bash
# 从Git恢复
git clone https://github.com/wenbo0527/wiki-knowledge-base.git
cd wiki-knowledge-base
git checkout <commit-hash>

# 查看历史
git log --oneline
```

---

## 八、问题诊断

### 常见问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 层级过深 | 历史积累 | 定期扁平化审查 |
| 内容孤立 | 缺乏链接 | 补充双向链接 |
| 质量参差 | 无标准 | 执行本手册标准 |
| 更新滞后 | 无机制 | 启用到期提醒 |

---

## 九、附录

### 9.1 自动化工具

```bash
# Wiki健康检查
cd /Users/wenbo/Documents/project/Wiki
python3 wiki/scripts/wiki_lint.py

# 检查深层目录
find wiki -type d -depth 4 -not -path '*/.*'

# 检查缺少README的目录
find wiki/topics -mindepth 2 -type d | while read d; do 
  [ ! -f "$d/README.md" ] && echo "缺少: $d"
done
```

### 9.2 相关文档

- [企业Wiki架构设计](./topics/knowledge-management/enterprise/wiki-architecture.md)
- [知识治理与权限](./topics/knowledge-management/enterprise/governance.md)
- [AI驱动的企业知识库](./topics/knowledge-management/enterprise/ai-knowledge-base.md)

---

*最后更新: 2026-04-24*
*维护者: 尼克·弗瑞*
*下次评审: 2026-07-24*
