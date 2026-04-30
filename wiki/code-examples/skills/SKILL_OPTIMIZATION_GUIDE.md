# 📚 Skill优化最佳实践手册

> **目标读者**: 需要优化Skill的Agent（托尼、钟离、尼克）
> **制定依据**: mgechev/skills-best-practices
> **生效日期**: 2026-04-30

---

## 🎯 这本手册解决什么问题

当你的Skill评分<75分，或者被派蒙通知需要优化时，
你应该怎么做？这本手册给你**一步步的具体操作**。

---

## 📋 优化清单

### 第一步：检查SKILL.md行数

**目标**: SKILL.md < 500行

```bash
# 检查行数
wc -l ~/.openclaw/skills/{your-skill}/SKILL.md

# 如果超过500行，需要精简
```

**精简方法**：

| 精简内容 | 移动到 |
|----------|--------|
| 完整案例 | `references/case-xxx.md` |
| 详细代码示例 | `scripts/` 目录 |
| 大段说明文档 | `references/doc-xxx.md` |
| 模板文件 | `references/template-xxx.md` |

**SKILL.md只保留**：
- 触发条件
- 核心流程（精简版）
- 对references/的引用

---

### 第二步：优化触发词

**目标**: description包含"Use when" + "Don't use for"

**检查触发词**：
```bash
head -10 ~/.openclaw/skills/{your-skill}/SKILL.md
```

**优化前**（❌）：
```yaml
name: my-skill
description: 这是一个处理需求的Skill
```

**优化后**（✅）：
```yaml
name: my-skill
description: >
  处理产品需求拆解和PRD生成。
  Use when: 用户提出新需求、需要拆解Epic/Feature/Story、生成PRD文档。
  Don't use for: 纯技术问题（用技术评审）、紧急Bug修复、日常运维任务。
```

---

### 第三步：创建references/目录

**目标**: 把详细内容移到references/

```bash
# 创建references目录
mkdir -p ~/.openclaw/skills/{your-skill}/references

# 移动案例文件
mv your-case.md ~/.openclaw/skills/{your-skill}/references/case-xxx.md
```

**references/结构规范**：
```
references/
├── case-1.md      ← 典型案例
├── case-2.md      ← 边界案例
├── template.md    ← 输出模板
└── doc.md         ← 详细文档
```

**注意**：只嵌套一层，不要 `references/sub/case.md`

---

### 第四步：检查scripts/目录

**目标**: 把重复操作写成脚本

```bash
# 检查是否有scripts/
ls -la ~/.openclaw/skills/{your-skill}/scripts/
```

**应该脚本化的场景**：
- 重复的数据查询
- 固定的API调用
- 格式化输出
- 批量操作

**scripts/应该包含**：
```bash
#!/bin/bash
# scripts/run.sh
# 执行入口脚本

set -e

echo "Starting skill execution..."
python3 scripts/process.py "$@"
```

---

### 第五步：添加"Don't use for"

**目的**: 明确不适用场景，避免误触发

在SKILL.md的description中添加：
```yaml
Don't use for:
- 场景1
- 场景2
- 场景3
```

---

## 📝 案例：requirement-breakdown优化

### 优化前问题

| 问题 | 详情 |
|------|------|
| SKILL.md行数 | 570行（超过500） |
| 无"Don't use for" | 只有触发场景 |
| 案例在主文件 | 占据大量篇幅 |

### 优化步骤

```
Step 1: 分析内容
   - 提取飞书写入脚本 → references/feishu-script.md
   - 提取9项清单模板 → references/requirement-9-items.md
   - 提取思考伙伴卡片 → references/thinking-partner.md

Step 2: 重写SKILL.md
   - 精简到222行
   - 保留核心流程
   - 添加"Use when"+"Don't use for"

Step 3: 验证
   - wc -l SKILL.md → 应该是<500行
   - grep "Don't use for" SKILL.md → 应该找到
```

### 优化后结构

```
requirement-breakdown/
├── SKILL.md                    ← 222行（精简后）
├── references/
│   ├── feishu-script.md       ← 飞书脚本（提取）
│   ├── requirement-9-items.md  ← 9项清单（提取）
│   └── thinking-partner.md     ← 思考伙伴（提取）
└── scripts/
    └── (已有脚本)
```

---

## ✅ 优化检查清单

优化完成后，逐项检查：

```markdown
## 优化完成检查

### 结构规范
- [ ] SKILL.md < 500行
- [ ] references/目录存在
- [ ] references/只有一层深度
- [ ] scripts/目录存在（如果需要）

### 触发词
- [ ] description < 1024字符
- [ ] 有"Use when"正例
- [ ] 有"Don't use for"反例
- [ ] 触发词无歧义

### 内容
- [ ] 核心流程清晰
- [ ] 步骤是确定性的
- [ ] 有错误处理说明
- [ ] 引用路径正确

### 验证
- [ ] SKILL.md可以正常读取
- [ ] references/文件可访问
- [ ] 触发词通过自测
```

---

## 🚀 快速优化模板

如果你的Skill需要快速优化，按这个模板改：

```markdown
---
name: {skill-name}
description: >
  {一句话描述功能}
  Use when: {触发场景1}、{触发场景2}、{触发场景3}
  Don't use for: {不适场景1}、{不适场景2}
---

# {Skill名称}

> 版本: v2.0（优化版）
> 更新: 2026-04-30

## 能做什么
{1-2句话}

## 激活条件
{触发场景}

## 执行流程

### Step 1: {步骤名称}
{简短的步骤说明}

### Step 2: {步骤名称}
{简短的步骤说明}

## 参考文档
- 详细内容: `references/{doc}.md`
- 案例: `references/{case}.md`
- 模板: `references/{template}.md`

---

*版本: v2.0*
*更新: 2026-04-30*
```

---

## 📂 常见问题

### Q1: 什么时候需要创建scripts/？

**需要**：重复执行相同操作、有固定API调用、批量处理
**不需要**：一次性分析、纯人工判断流程

### Q2: references/要放什么？

**放**：
- 完整案例（>10行的示例）
- 输出模板
- 详细文档
- 代码示例

**不放**：
- 核心流程（留在SKILL.md）
- 简单的配置（可以直接写在SKILL.md）

### Q3: SKILL.md最少要有什么？

1. **Frontmatter**：name + description
2. **能做什么**：1-2句话
3. **激活条件**：触发场景
4. **执行流程**：精简的步骤
5. **参考引用**：指向references/

---

## 🔗 相关文档

| 文档 | 说明 |
|------|------|
| [SKILL_EVALUATION.md](../SKILL_EVALUATION.md) | 评价标准 |
| [SKILL_BEST_PRACTICES.md](../SKILL_BEST_PRACTICES.md) | mgechev最佳实践 |
| [SKILL_SCORING_REPORT.md](../SKILL_SCORING_REPORT.md) | 当前评分 |

---

*手册版本: v1.0*
*创建: 2026-04-30*
