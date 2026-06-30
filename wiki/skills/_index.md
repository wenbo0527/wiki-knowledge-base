# Skills 索引 - 方案 B 落地

> **创建日期**：2026-06-11
> **维护者**：派蒙（大总管）
> **关联决策**：方案 B - Agent 简化 + Skill 化

---

## 📊 统计

| 指标 | 数量 |
|:--|--:|
| 已沉淀 Skill | **3**（demo-generation / quick-demo-sample / digital-community-dev-workflow） |
| 待沉淀 Skill | 7 |
| 总规划 Skill | 10 |

---

## 🟠 当前 3 个 Skill（已落地）

### 1. demo-generation（钟离 - 诊断流程）

- **路径 A**：`~/.openclaw/skills/demo-generation/`
- **路径 C**：[demo-generation.md](./demo-generation.md)
- **沉淀来源**：火匠（Smith）能力迁移 + 4 个 Python 模板
- **触发场景**：诊断流程中给业务方展示 AI 能力概念验证
- **4 类场景**：dialogue / recommendation / classification / detection
- **核心创新**：4 层架构（SKILL.md + references/ + assets/ + scripts/）+ 真校验脚本
- **渐进式披露**：触发前 100 token / 触发后 3000 token / 资源按需加载

### 2. quick-demo-sample（数字社区 dev - PM 演示）

- **路径 A**：`~/.openclaw/skills/quick-demo-sample/`
- **沉淀来源**：你给的范例 §六"数字社区Demo样例的归属"
- **触发场景**：PM 需要给用户展示数字社区某功能原型
- **核心**：单 HTML + Tailwind CDN + 30 秒生成

### 3. digital-community-dev-workflow（数字社区 6 角色端到端 Workflow）⚠️ 改定位

- **路径 A**：`~/.openclaw/skills/digital-community-dev-workflow/SKILL.md`
- **路径 C**：[digital-community-dev-workflow.md](./digital-community-dev-workflow.md)
- **沉淀来源**：active memory + 派蒙 MEMORY 6/4 02:00 冲刺 + 6/11 dev 实战
- **覆盖范围**：数字社区 dev 端到端 8 步流程（Tony → PM → arch → dev + doc → qa → PM → Tony）
- **关键设计**：每步独立输入/输出/时限/派单源；含状态机 + 断点续跑 + 断路器
- **Workflow 信号**：4/4 全中（强依赖 / 跨天断点 / 2 处人机回环 / 8 个降级点）
- **改定位**：原 `data-community-app-demo` 6/11 改名为 Workflow（不是 Skill）

---

## ⏳ 待沉淀（P1/P2）

| 优先级 | Skill 名 | 归属 | 沉淀来源 | 计划 |
|:--|:--|:--|:--|:--|
| P1 | typesetting-standard | 阿加莘 | 内容专家 SOUL §1 | 6/12 周五 |
| P1 | doc-spec-review | 阿加莘 | 内容专家 SOUL §2 | 6/12 周五 |
| P1 | ux-calibration | 钟离 | 交互测试专家 SOUL §3 | 6/12 周五 |
| P2 | comment-standard | 阿加莘 | 内容专家 SOUL §1 | 6/15 周一 |
| P2 | e2e-test-design | 钟离 | 交互测试专家 SOUL §2 | 6/15 周一 |
| P2 | weekly-finance-sync | 派蒙 | 麦麦 cron | 6/15 周一 |
| P2 | industry-research-template | 派蒙 | 小二子 SOUL | 6/15 周一 |

---

## 🎯 命名规范（OpenClaw 官方）

| 项 | 规范 | 来源 |
|:--|:--|:--|
| 命名 | **kebab-case**（小写 + 连字符） | `creating-skills.md` 官方原话 |
| 目录名 | 必须与 frontmatter `name` 一致 | 官方硬约束 |
| description | 一行 ≤ 160 字符 | 影响 agent 发现 |
| 加载顺序 | `~/.openclaw/skills/` 第 4 级 | `skills.md` 官方 |
| Skill 结构 | SKILL.md + references/ + assets/ + scripts/ | 你给的范例 |

---

## 🔄 已删除（按你指正）

| 原 Skill | 删除原因 | 删除日期 |
|:--|:--|:--|
| `demo-for-mkt` | 写死 1 个 app，应改为通用 + 案例动态加载 | 2026-06-11 |
| `demo-full-generation` | 逻辑缺失 + 场景错（不在我们 OpenClaw） | 2026-06-11 |
| `demo-quick-response` | 同样逻辑缺失，应是 `demo-generation` 的 quick 模式 | 2026-06-11 |

**3 个全被 `demo-generation` 替代**。

---

## 📊 沉淀记录

| 日期 | 变更 | 变更人 |
|:--|:--|:--|
| 2026-06-11 | 初版（3 个 demo Skill 落地） | 派蒙 |
| 2026-06-11 | 文博指正："demo-full-generation 不在我们 OpenClaw"，按范例重写为真逻辑版 `demo-generation` | 派蒙复盘 |
| 2026-06-11 | 文博指正："for-mkt 写死 1 个 app"，改为通用规则 + 案例动态加载 `digital-community-dev-workflow` | 派蒙复盘 |
| 2026-06-11 | 修正结构：3 个 Skill 全部按范例 4 层架构（SKILL.md + references/ + assets/ + scripts/）组织 | 派蒙 |