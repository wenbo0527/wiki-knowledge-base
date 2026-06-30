# Digital Community Dev Workflow - 人类浏览版

> **机器版**：`~/.openclaw/skills/digital-community-dev-workflow/SKILL.md`
> **创建日期**：2026-06-11

---

## 这是什么？

数字社区 dev **端到端 Workflow**——从 Tony 接到需求到 PRD v1.0 归档的**8 步完整流程**。

## 8 步总览

```
① Tony PRD v0.x          (1-2 天)
       ↓
② PM 收口 + 拆任务        (30 min)
       ↓
③ arch 评审              (30 min - 2h)
       ↓
   ┌──┴──┐
   ↓     ↓
④ dev   ⑤ doc            (数小时-1 天 / 30 min，串行)
   ↓     ↓
   └──┬──┘
     ↓
⑥ qa 验证                 (1-2h)
     ↓
⑦ PM 收口 + 反馈          (30 min)
     ↓
⑧ Tony PRD v1.0          (1h)
```

## 每步输入输出速查

| 步 | 输入 | 输出 | 时限 | 派单源 → 接收方 |
|:--|:--|:--|:--|:--|
| ① | 文博需求 / 调研 / 模板 v5.0 | PRD v0.x（10 段） | 1-2 天 | 文博 → Tony |
| ② | PRD v0.x | 4 角色任务清单 + 收口样板 + task_id | 30 min | Tony → PM |
| ③ | 任务清单 + PRD v0.x + 现有代码 | arch 报告（Agent 好读）| 30 min-2h | PM → arch |
| ④ | arch 报告 + PRD v0.x | 修改代码 + 部署 URL + 4 项自验 + lessons | 数小时-1 天 | arch → dev |
| ⑤ | dev 完整体 | PRD 增量 + 字段说明 + 状态机 + lessons | 30 min | dev → doc（串行）|
| ⑥ | 部署 URL + 验收标准 | 5 路由截图 + 自动化脚本 + 回归报告 | 1-2h | dev → qa |
| ⑦ | 4 角色产物 | 完成报告（5 段）+ 飞书 + task done | 30 min | qa → PM |
| ⑧ | 完成报告 + dev 实际产物 | PRD v1.0（终版）| 1h | PM → Tony |

## 关键设计决策（你 6/11 拍板）

| 决策 | 你的拍板 |
|:--|:--|
| ① Tony PRD 模板 | **PRD v5.0 模板 10 段**（含 Feature/Story/FP 三级 + 菜单映射 + 审批流）|
| ③ arch 报告形式 | **以 Agent 好读为准**（1 句话结论 + 范围表 + mermaid + 风险点 + 建议）|
| ⑤ doc 与 dev 关系 | **串行**（等 dev 完成才写 doc）|
| ⑥ qa 验证范围 | **路由验证 + 功能自动化 + 基础功能回归**（3 项必含）|
| ⑦ PM 反馈形式 | **完成报告 + 飞书**（5 段报告 + 飞书消息）|

## 4 个 Workflow 信号

| 信号 | 数字社区 dev 流程 |
|:--|:--:|
| ① 状态依赖（强）| ✅ |
| ② 断点续跑（跨天）| ✅ |
| ③ 人机回环（2 处）| ✅ |
| ④ 断路器（8 个降级点）| ✅ |

**4/4 全中——这是教科书级 Workflow**。

## 沉淀记录

| 日期 | 变更 | 变更人 |
|:--|:--|:--|
| 2026-06-11 | 初版（8 步 + 输入输出 + 状态机 + 断点 + 断路器）| 派蒙 |
| 2026-06-11 | 文博拍板 5 个边界（arch 好读 / doc 串行 / qa 3 项 / PM 报告+飞书 / PRD 模板 v5.0）| 派蒙 |
| 2026-06-11 | 重命名（原 `data-community-app-demo`） + 改定位为 Workflow | 派蒙 |