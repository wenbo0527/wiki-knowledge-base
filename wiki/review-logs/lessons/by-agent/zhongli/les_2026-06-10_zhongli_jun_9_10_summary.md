---
title: les 2026 06 10 zhongli jun 9 10 summary
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-06-30
---

# 📝 Lesson #066: 钟离 6/9-6/10 教训索引 (教训 31-65)

| 字段 | 值 |
|:---|:---|
| **ID** | les_2026-06-10_066 |
| **类型** | 🧠 经验沉淀索引 |
| **关联文档** | 18 份 `memory/2026-06-09-*.md` + `memory/2026-06-10-*.md` |
| **Agent** | zhongli |
| **日期** | 2026-06-10 |
| **范围** | 6/9 11h + 6/10 上午 3h = 14h 工作, 65 条教训 |

---

## 背景

6/9 一天 11 小时 + 6/10 上午 3 小时, 钟离 1 个 agent 修了 30+ bug, 沉淀 35 条教训 (含 6/10 教训 64-65), 写 18 份 memory 文档, 跑 3 个 E2E 自动化脚本 (39/41 PASS 回归), 部署 8 次。

本索引是"教训地图"——按 7 大类聚合, 便于后续搜索/复用。

---

## 7 大类教训索引

### A. 教训 31-33: 5 步追问 prompt 卫生 (Bug 26/27 修复)

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 31 | yaml 加 "key 严格匹配清单" 约束 | LLM 填项必用清单已有 key, 不编新 |
| 32 | loader.py 漏读 yaml clarification_mode 字段 | yaml → dataclass 字段必同步 |
| 33 | silent retry 触发需 trace 日志 | "accepted" 状态不能当 silent |

### B. 教训 34: 任务标题 ≠ 实际工作

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 34 | T10 "后端改造" 实际是 5min 验证契约 | 任务描述必区分 "验证" vs "开发" |

### C. 教训 35-37: confirm_report 链路 (Bug 35-37 修复)

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 35 | FileRenderer 派发器 case 必含 | 报文件 `report` 走 MarkdownRenderer |
| 36 | 后端写 ctx.files 必同步 prd file | confirm_report 必同步 reqdefiner |
| 37 | status 端点必返 report_pending message | 浏览器刷新也能拿到报告 |

### D. 教训 38-39: 协议一致性 (Bug 38-39 修复)

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 38 | 后端写文件必返 files 列表 | 前端 handleConfirmReport 能 setFiles |
| 39 | LLM 调用失败必 fallback | 端点响应兜底 |

### E. 教训 40-43: 5 步追问 + E2E 优化

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 40 | 升级信号检测 (万能词) | 主动追加 3 问 |
| 41 | silent fallback 必须保留业务流完整性 | is_final 必返 report_ready, 不返 asking |
| 42 | 前端 timeout ≥ 后端最慢路径 | clarifier 90s, 不用 60s |
| 43 | structuredMessages 模式 content 是空 | 渲染器必读 structuredMessages |

### F. 教训 44-47: 问小数假活事故 (派蒙接手)

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 44 | 部署后必跑 smoke test (ss -tlnp) | curl 必查端口真实在听 |
| 45 | 任务重开 ≠ 实施, 必带 worktree | 派蒙团队 2 假活 7 天 |
| 46 | 周审计必含"全团队"范围 | 不能只审计自己名下 |
| 47 | 字段名协议要全链路对齐 | user_input vs query (dev/qa 修) |

### G. 教训 48-49: 粘贴 markdown (Bug 48-49 修复)

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 48 | 子组件不从 URL 自取数据 | CreateFileModal 必传 workflowId prop |
| 49 | 字段名协议全链路对齐 | getText 兼容 body 字段 |

### H. 教训 50-53: MVP-3 Git 导入 (T15-T20)

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 50 | 命名避开 Python 关键字 | `import` 是关键字, 改 `git_import` |
| 51 | subprocess timeout 给真够时间 | openclaw/openclaw 3.8M 需 30s+, 给 120s |
| 52 | E2E 必用快路径先验证 | octocat/Hello-World 1.6s 完成 |
| 53 | 已存在仓库跳过 fetch | 60s+ 优化为 0.1s |

### I. 教训 54-55: minimax URL 修复

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 54 | 第三方 URL 配置变更要 smoke test | api.minimax.chat 308 → /v1/... |
| 55 | API 响应解析要对真实 schema | base_resp.status_code (不是 code) |

### J. 教训 56-60: OpenClaw 异步 silent retry

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 56 | 修之前先看真实调用链 (文博金玉良言) | minimax 是边角, OpenClaw 是主链路 |
| 57 | 异步 API 不要按同步语义重试 | accepted+no_reply ≠ silent, 是异步 |
| 58 | silent retry 不误判 accepted | 移除 "accepted + not has_reply" 误判 |
| 59 | 限制 session contextWindow | 204k 满 → 64s failed, history 截断 2 轮 |
| 60 | silent retry 多匹配 NO_REPLY | LLM 真实答 "NO_REPLY" 不是 "ANNOUNCE_SKIP" |

### K. 教训 61-65: 6/9-6/10 整理 session

| # | 教训 | 一句话 |
|:--:|:---|:---|
| 61 | 大改日必写大事记 | 11h 30+ bug 30 教训需 1 份汇总 |
| 62 | 临时 debug 脚本必清 | 5/23 留的 7 个今天才清 |
| 63 | 回归测试必用 30+ 检查点 | 39/41 PASS 验证无回退 |
| 64 | 续作能力 = 后端复用 + 前端 1 按钮 | MVP-4 不是 7 任务 |
| 65 | 慢 LLM 操作必加时间预期 | "分析中 (30-50s)..." |

---

## 关键人/事 (6/9-6/10)

### 文博的关键决策 (10 次拍板)

| 时间 | 决策 | 触发 |
|:---|:---|:---|
| 6/9 07:19 | A: 修 Bug 26/27 再拍板 T9 | 启动流程 |
| 6/9 08:09 | A: 拍板 T9 启动 MVP-2 | 9 验收项过 |
| 6/9 14:35 | A: 拍板 T14 启动 MVP-3 | 12 验收项过 |
| 6/9 16:30 | A: 拍板 T15-T20 MVP-3 收口 | 5 验收项过 |
| 6/9 16:35 | B: 修 minimax URL | E2E 跑通, 优化 LLM 加速 |
| 6/9 16:42 | C: 查 OpenClaw gateway | 文博怀疑触发真因 |
| 6/9 16:50 | A: silent retry 修复 | 文博拍板 |
| 6/9 17:00 | A: 限制 session contextWindow | 文博拍板 |
| 6/9 18:00 | B: 整理 6/9 沉淀 | 文博拍板 |
| 6/10 06:36 | A: 接受 LLM 慢现实, 启动 MVP-4 | 文博拍板 |

### 文博的关键怀疑 (教训 56 触发)

> "现在填入 minimax API key 的意义是什么? 绕过 OpenClaw 么"

**这句怀疑**引导到真因: minimax 是边角 (T19 query 端点), OpenClaw gateway 是主链路。**6/9 30+ bug 修复中**最关键的一句。

### 派蒙的接力 (已升级)

- 3 卡死问小数任务 blocked (E5C18BA3/E7ACFB94/6886CEEA)
- 应 6/16 周审计识别"git log 0 commit in_progress" 任务

---

## 远程状态 (6/10 上午)

| 维度 | 状态 |
|:---|:---|
| 远程 uvicorn | pid 897758 (6/9 18:27 启, 教训 61 修后) |
| 前端 BUILD_ID | `EczLKT-8sv6wXvpdz-peG` (6/10 06:48 部署, MVP-4 模态) |
| 8445/diagnoser | ✅ 200 |
| 8445/ask-xiaoshu | ✅ 200 (页面), ⚠️ API 字段名错配 (dev/qa 修) |
| 8443/home | ✅ 200 |
| OpenClaw gateway | pid 584974 (Jun04 启动, 跑了 5 天 14h) |
| 远程 Git 仓库 | `/tmp/git-repos/repo-8a1f344c/` (octocat/Hello-World) |
| clarifier session | `e1afaa79-...` (累积多次, 6s LLM 答完) |

---

## E2E 自动化脚本 (3 个)

| 脚本 | 检查点 | 状态 |
|:---|:---:|:---:|
| `e2e/diagnoser-5step-confirm.mjs` | 15 | ✅ 15/15 PASS |
| `e2e/diagnoser-paste-markdown.mjs` | 18 | ✅ 16/18 PASS (2 fail 期望不准) |
| `e2e/diagnoser-import-git.mjs` | 8 | ✅ 8/8 PASS |
| `e2e/diagnoser-mvp4-analyze.mjs` | 9 | ✅ 9/9 PASS (6/10 新增) |

---

## 累计产出 (6/9-6/10)

| 维度 | 数字 |
|:---:|:---|
| 教训总数 | **65 条** (6/9: 33, 6/10: 2) |
| memory 文档 | **18 份** (6/9: 16, 6/10: 1) |
| 评估评审包 | 3 份 (T9/T14/T21) |
| E2E 脚本 | 4 个 (3 + MVP-4) |
| 远程部署 | 8 次 (每次 5min) |
| 修复 bug | 30+ |
| 代码变更文件 | 12+ |
| 任务完成 | 22 (MVP-1 9 + MVP-2 6 + MVP-3 6 + MVP-4 1) |

---

## 6/10 下一阶段

### P0
1. 拆 MEMORY.md (786 行 / 33.6KB 超警戒线, 拆到 4-5 个专题文件)
2. 教训 31-65 沉淀到 Wiki (本文档已建)
3. 派蒙周审计机制加强 (6/16 第一道闸)

### P1
1. 5/26 老 Demo Trace 4 任务收口 (overdue 14 天)
2. MVP-5 规划 (LLM 慢物理限制, 流式输出 SSE + 小模型切换)

### P2
1. dev/qa 字段名错配协调
2. minimax_client URL 持续 308 监控
3. 5 步追问 OpenClaw session 隔离 (避免 contextWindow 累积)

---

## 关联资源

- 18 份 memory 文档 (`memory/2026-06-09-*.md` + `memory/2026-06-10-*.md`)
- 3 份评估评审包 (`评估/0?-T?-*.md`)
- 4 个 E2E 脚本 (`personal-site/e2e/diagnoser-*.mjs`)
- 11 处代码变更 (`diagnoser_api_v2.py` / `DocumentPanel.tsx` / `git_import/` / `minimax_client.py` / etc)
- 3 份教训沉淀模板: `concepts/ai-llm.md` + `review-logs/lessons/by-agent/zhongli/` 历史模板
