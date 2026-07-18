---
title: 产品Demo管理 - 架构、Coding、测试、上线最佳实践
version: v1.2
created_date: 2026-05-19
author: 钟离
owner: 钟离
product_domain: PD-DEMO-MANAGEMENT
tags: [SOP, 架构, coding, 测试, 部署, 最佳实践, Portal-Shell, Vibe-Coding, BUG修复]
status: 活跃维护
capability: [tech-understanding, product-design, data-driven]
doc_type: 其他
date: 2026-05-23
---


# 产品Demo管理 - 架构、Coding、测试、上线最佳实践

> Portal Shell + 子应用集成全流程规范
> 版本: v1.2 | 对齐 Vibe Coding 最佳实践

> ⚡ 快速上手：见 [[memory-bank/@quickstart.md]] 一页纸指南

---

## 🚀 快速上手

```
1. 阅读上下文 → CLAUDE.md + memory-bank/@design-doc.md + memory-bank/@tech-stack.md
2. 任务拆分 → 钟离拆分 → 写 tmp/cc_tasks.md
3. 执行 → CC 执行 → 记录到 tmp/cc_results.md
4. 验收 → 钟离验收 → 通过/打回
```

**常用命令**：
```bash
pnpm build                    # 构建
./scripts/deploy.sh <app>    # 部署 (portal-shell/risk-app/mkt-app/...)
curl -sk https://118.196.79.130:8443/<app>/  # 验证
```

**关键文件**：
- `CLAUDE.md` - AI 行为准则
- `memory-bank/@quickstart.md` - 快速上手一页纸
- `src/config/domainDictionary.ts` - 产品域配置

---

## 📑 目录

- [零、快速上手](#-快速上手)
- [一、核心架构](#一核心架构)
- [二、任务切分](#二任务切分)
- [三、Coding规范](#三coding规范)
- [四、测试流程](#四测试流程)
- [五、部署流程](#五部署流程)
- [六、子应用改造规范](#六子应用改造规范)
- [七、完整案例](#七完整案例)
- [八、最佳实践](#八最佳实践)
- [九、BUG修复SOP](#九bug修复sop)
- [十、关联文档](#十关联文档)

---

## 一、核心架构

### 1.1 架构概览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              钟离 (系统架构师)                              │
│                     架构设计 → 任务拆分 → 结果验收                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
        ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
        │  雅典娜       │     │  波塞冬       │     │  赫尔墨斯     │
        │  Demo管理     │     │  生产运维     │     │  辅助项目     │
        │               │     │               │     │               │
        │ • 子应用路由  │     │ • 部署发布    │     │ • Wiki维护    │
        │ • Demo页面    │     │ • nginx配置   │     │ • 文档整理    │
        │ • 样式适配    │     │ • 健康检查    │     │ • 辅助开发    │
        └───────────────┘     └───────────────┘     └───────────────┘
```

### 1.2 职责矩阵

| 角色 | 核心职责 | 擅长领域 |
|:-----|:---------|:---------|
| **钟离** | 架构设计、Coding、技术评审 | 系统设计、代码审查、方案确定 |
| **波塞冬** | 生产运维、部署发布 | 服务器操作、nginx、部署脚本 |
| **雅典娜** | Demo管理、子应用维护 | 路由配置、样式适配、前端开发 |
| **赫尔墨斯** | 辅助项目、文档整理 | Wiki维护、辅助开发 |

### 1.3 决策权限

| 决策类型 | 决策者 | 说明 |
|:---------|:-------|:-----|
| **架构设计** | 钟离 | 路由方案、技术选型 |
| **技术方案** | 钟离 | API设计、数据模型 |
| **Coding实现** | CC Agent | 钟离评审后执行 |
| **部署发布** | 波塞冬 | 钟离验收后执行 |
| **nginx配置** | 波塞冬 | 钟离评审后执行 |

---

## 二、任务切分

### 2.1 标准流程

```
用户请求 → 钟离(理解+拆分) → CC执行 → 结果记录 → 钟离验收
```

| 步骤 | 操作者 | 产出 |
|:-----|:------|:---|
| 1. 理解 | 钟离 | 需求澄清 |
| 2. 拆分 | 钟离 | 任务清单（每个子任务可60秒内完成） |
| 3. 执行 | CC Agent | 执行结果 |
| 4. 记录 | CC Agent | 结果写入文件 |
| 5. 验收 | 钟离 | 通过/打回 |

### 2.2 CC任务分发判断

| 条件 | 示例 | 决策 |
|:-----|:-----|:---|
| 耗时 < 2分钟 | rm tmp/* | 钟离直接执行 |
| 需多步并行 | 部署43个子应用 | **CC执行** |
| 技术决策 | 架构选型 | 钟离直接做 |
| 构建+传输 | 前端构建 | **CC执行** |
| nginx配置 | 端口/路由修改 | **CC执行** |

### 2.3 任务拆分检查清单

- [ ] 每个子任务是否可在60秒内完成？
- [ ] 子任务之间是否有依赖？
- [ ] 是否有可以并行的子任务？
- [ ] 每个子任务是否有明确的验收标准？

### 2.4 工作文件

| 文件 | 用途 |
|:-----|:-----|
| `tmp/cc_tasks.md` | 拆分后的子任务列表 |
| `tmp/cc_results.md` | 每个子任务执行结果 |
| `tmp/cc_exec_log.json` | 耗时 + 完成状态 |

### 2.5 Memory Bank（Vibe Coding 核心）

> 对齐 [[vibe-coding/项目管理.md]] 的 Memory Bank 机制

每个 Demo 项目需要维护 Memory Bank，确保 AI 能理解项目上下文：

| 文件 | 用途 | 维护时机 | 状态 |
|:-----|:-----|:---------|:-----|
| `memory-bank/@design-doc.md` | AI行为准则 + 项目上下文 | 项目开始 | ✅ 已创建 |
| `memory-bank/@tech-stack.md` | 技术栈 + 依赖说明 | 项目开始 | ✅ 已创建 |
| `memory-bank/@progress.md` | 进度记录 | 每个里程碑 | ✅ 已创建 |
| `memory-bank/@quickstart.md` | 快速上手一页纸 | 项目开始 | ✅ 已创建 |

> ⚠️ memory-bank/ 目录已创建于 `portal-shell/memory-bank/`

### 2.6 部署脚本（已增强）

> 实际可用的部署脚本，支持 data_community 子应用

| 脚本 | 用途 | 状态 |
|:-----|:-----|:-----|
| `scripts/deploy.sh` | 一键部署脚本 | ✅ v2.0 支持多子应用 |

**使用方式**：
```bash
./scripts/deploy.sh mkt-app          # 部署 mkt-app
./scripts/deploy.sh risk-app        # 部署 risk-app
./scripts/deploy.sh mkt-app --rebuild  # 强制重新构建
```

### 2.6 上下文膨胀处理

> 来自 [[insights/agent/insight-20260419-harness-engineering]] 的 Harness 设计思想

当单个会话任务超过30分钟时：

1. **提交当前进度**到 Git
2. **创建新会话**
3. 在 `CLAUDE.md` 中记录上下文摘要
4. 新会话读取 `CLAUDE.md` 继续

### 2.7 SIGKILL 处理

> 当 CC Agent 遇到 SIGKILL（内存/资源限制）时的处理

1. **记录已完成的部分**到 `tmp/cc_results.md`
2. **减小当前子任务的规模**（减少代码量）
3. **使用更短的prompt重试**
4. 如果连续失败，改用**直接文件读取分析**

---

## 三、Coding规范

### 3.1 四大核心原则 (Karpathy)

| 原则 | 说明 | 应用 |
|:-----|:-----|:-----|
| **Think Before Coding** | 不要假设，明确假设，有疑问就问 | 动手前先确认需求和边界 |
| **Simplicity First** | 最少代码解决问题，不做投机性设计 | 避免过度工程 |
| **Surgical Changes** | 精准修改，只改必须改的 | 小步迭代 |
| **Goal-Driven Execution** | 定义成功标准，循环验证 | 每步有验收 |

### 3.2 代码提交前检查清单

> **黄金原则：你负责交付能工作的代码，不是审查者。**

- [ ] 代码能正常工作（已手动验证关键路径）
- [ ] 变更说明清晰（目的、影响范围、关联 Issue）
- [ ] PR 大小合适（≤300行，超过必须拆分）
- [ ] 自己先审查过（不要让别人读你自己没读过的变更说明）
- [ ] 测试覆盖（关键逻辑有基本测试保护）

### 3.3 架构原则

> 对齐 [[vibe-coding/开发经验.md]] 的 KISS/YAGNI/DRY/SOC 原则

| 原则 | 说明 | 应用 |
|:-----|:-----|:-----|
| **KISS** | Keep It Simple, Stupid | 所有场景优先简单方案 |
| **YAGNI** | You Aren't Gonna Need It | 不做投机性设计 |
| **DRY** | Don't Repeat Yourself | 重复代码必须抽取 |
| **SOC** | Separation of Concerns | 按职责分层 |
| **函数长度** | 不超过50行 | 违反需重构 |

### 3.4 错误处理框架

> 对齐 [[insights/agent/insight-20260419-harness-engineering]] 的错误分类处理

| 错误类型 | 识别方式 | 处理策略 |
|:---------|:---------|:---------|
| **编译错误** | 构建失败输出 | 定位文件 + 小步修复 |
| **运行时错误** | Console ERROR | 提供最小复现 + 堆栈 |
| **API 错误** | 4xx/5xx | 检查请求/响应格式 |
| **集成错误** | iframe/跨域 | 检查路由 + CORS 配置 |
| **部署错误** | 部署失败 | 检查 nginx + 权限 |

---

## 四、测试流程

### 4.1 测试类型

| 类型 | 执行者 | 时机 | 方法 |
|:-----|:------|:-----|:-----|
| **浏览器自动化** | 钟离/CC | 关键路径验证 | Playwright/浏览器截图 |
| **控制台日志检查** | 钟离/CC | 每次部署后 | 检查ERROR级别日志 |
| **API连通性** | 自动化脚本 | 部署后 | curl检查 |
| **功能回归** | 钟离 | 大改动后 | 手动测试关键路径 |

### 4.2 AI 写测试用例

> 对齐 [[insights/ai-coding/insight-20260429-playwright-claude-code-testing]] 的三 Skill 架构

让 CC Agent 生成 Playwright 测试用例：

```bash
# Prompt 模板
"为 {功能} 编写 Playwright 测试用例
要求：
- 覆盖正常流程
- 覆盖异常流程
- 包含断言
- 输出到 tests/e2e/{功能}.spec.ts
"
```

### 4.3 部署后检查清单

- [ ] 页面能正常加载（HTTP 200）
- [ ] 控制台无 ERROR 级别错误
- [ ] 关键功能可访问
- [ ] 资源文件加载正确（JS/CSS）

---

## 五、部署流程

### 5.0 部署前检查清单

> 对齐 [[vibe-coding/项目管理.md]] 的部署前检查

- [ ] 代码已提交 Git
- [ ] 本地构建成功 (`npm run build`)
- [ ] 变更说明已写好（目的、影响范围）
- [ ] 关联文档已更新
- [ ] 通知相关方（雅典娜/波塞冬）

### 5.1 标准部署流程

```bash
# 参数说明：
# {app} = 子应用名称，如 risk, mkt, dex, dfd, dmt

1. 本地构建
   cd /path/to/{app} && npm run build

2. 同步到服务器
   rsync -avz --delete dist/ root@118.196.79.130:/var/www/html/{app}/

3. 设置权限
   ssh root@118.196.79.130 "chown -R www-data:www-data /var/www/html/{app}/"

4. nginx重载
   ssh root@118.196.79.130 "nginx -t && nginx -s reload"

5. 验证
   curl -sk https://118.196.79.130:8443/{app}/ | grep expected_content
```

### 5.2 部署脚本

```bash
#!/bin/bash
# deploy.sh - 标准部署脚本
# 用法: ./deploy.sh {app}

APP=$1
LOCAL_DIST="./${APP}/dist"
REMOTE_PATH="root@118.196.79.130:/var/www/html/${APP}/"

echo "=== 部署 ${APP} ==="

# 1. 构建
echo "[1/5] 构建中..."
cd /path/to/project/${APP} && npm run build

# 2. 同步
echo "[2/5] 同步到服务器..."
rsync -avz --delete -e "ssh -p 22" ${LOCAL_DIST}/ ${REMOTE_PATH}

# 3. 权限
echo "[3/5] 设置权限..."
ssh root@118.196.79.130 "chown -R www-data:www-data /var/www/html/${APP}/"

# 4. 重载
echo "[4/5] nginx重载..."
ssh root@118.196.79.130 "nginx -t && nginx -s reload"

# 5. 验证
echo "[5/5] 验证..."
ssh root@118.196.79.130 "curl -sk https://localhost:8443/${APP}/ | head -5"

echo "=== 部署完成 ==="
```

### 5.3 健康检查

```bash
#!/bin/bash
# health_check.sh - 健康检查脚本

echo "=== 健康检查 $(date) ==="

# 1. PM2 服务
echo "[1/4] PM2 服务状态"
pm2 status

# 2. 端口连通性
echo "[2/4] 端口检查"
curl -sk https://localhost:8443/ -o /dev/null -w "8443: %{http_code}\n"

# 3. 子应用
for app in risk mkt dex dfd dmt; do
  curl -sk https://localhost:8443/${app}/ -o /dev/null -w "${app}: %{http_code}\n"
done

# 4. Neo4j
echo "[3/4] Neo4j容器"
docker ps | grep neo4j

echo "=== 检查完成 ==="
```

---

## 六、子应用改造规范

### 6.1 子应用必须使用 Hash 路由

| 要点 | 说明 |
|:-----|:-----|
| **路由类型** | 子应用必须使用 `createWebHashHistory` |
| **原因** | 避免与父窗口路由冲突 |

### 6.2 MainLayout 要求

```vue
<template>
  <div class="main-layout">
    <AppSider :menus="menus" />
    <div class="main-content">
      <AppHeader />
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  display: flex;
  height: 100%;  /* 关键：必须占满父容器 */
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
```

### 6.3 入口页配置

```typescript
{
  path: '/',
  redirect: '/external-data/lifecycle'  // 默认跳转到具体页面
}
```

### 6.4 高度自适应问题排查

**症状**: iframe 高度为 0

**排查步骤**:
1. 检查 `.layout-content` 是否有明确高度
2. 检查 `.layout-body` 是否设置 `display: flex; flex: 1`
3. 检查子元素是否设置 `min-height: 0`

---

## 七、完整案例

### 7.1 案例：risk-app 路由改造

```
【任务：risk-app 改为 Hash 路由，支持 iframe 集成】

1. 钟离分析
   → 确认使用 createWebHashHistory
   → 确认入口页: /external-data/lifecycle
   → 创建子任务清单

2. CC执行 (雅典娜)
   → 修改 router.ts: createWebHistory → createWebHashHistory
   → 修改 MainLayout.vue: height: 100vh → height: 100%
   → 构建: npm run build
   → 部署: rsync to /var/www/html/risk/

3. 波塞冬验证
   → curl -sk https://118.196.79.130:8443/risk/ | grep title
   → 检查控制台错误

4. 钟离最终验收
   → 浏览器自动化测试
   → 截图确认显示正确
```

### 7.2 协作时序图

```
文博 ──需求──→ 钟离
                   │
                   ├──分析──→ 方案确定
                   │
                   ├──执行──→ 雅典娜/波塞冬
                   │              │
                   │              ├──构建部署──→ 线上可用
                   │              │
                   │              └──健康检查──→ 验证通过
                   │
                   └──验收──→ 文博确认
```

---

## 八、最佳实践

### 8.1 当前优势

| 优势 | 说明 |
|:-----|:-----|
| **钟离主导架构** | 架构设计、技术选型由钟离负责，确保技术方向正确 |
| **小步快跑** | 每步可验证，减少返工 |
| **CC执行落地** | 具体Coding、部署由CC Agent执行，钟离专注架构和评审 |
| **自动化检查** | 浏览器自动化 + curl 验证 |

### 8.2 待改进项

| 问题 | 影响 | 解决方案 | 优先级 |
|:-----|:-----|:---------|:-------|
| **iframe高度问题** | risk-app无法正常显示 | 继续排查flex布局 | 🟠 高 |
| **子应用MainLayout缺失** | 其他子应用无法集成 | 逐步建设 | 🟡 中 |
| **部署脚本标准化** | 每次手动部署 | 完善deploy.sh | 🟡 中 |
| **自动化测试覆盖** | 回归风险高 | 补充Playwright用例 | 🟡 中 |

---

## 九、BUG修复SOP

### 9.1 四步稳定法

> 对齐 Vibe Coding + Harness Engineering 最佳实践

```
稳定 BUG 修复 = 最小复现 × 明确边界 × 自动化验证 × 小步提交
```

| Step | 操作 | 产出 |
|:-----|:-----|:-----|
| **Step 1: 最小复现** | 提供复现步骤 + 最小代码 | BUG 报告 |
| **Step 2: 明确边界** | 确认只能改什么、不能改什么 | 修改边界 |
| **Step 3: 自动化验证** | 先写失败测试用例 | 测试覆盖 |
| **Step 4: 小步提交** | 每次只修一个 BUG | Git 提交 |

### 9.2 BUG 报告模板

```markdown
## BUG 报告

**问题**: [一句话描述]
**位置**: 文件路径 + 行号
**复现步骤**:
1. 
2. 
3. 

**预期行为**: 
**实际行为**: 

**最小复现**: [最小代码片段/配置]
```

### 9.3 修复后验证

| 类型 | 命令/| 类型 | 命令/操作 |
|:---|:---|
| **本地构建** | npm run build |
| **API 测试** | curl 检查 |
| **E2E 测试** | Playwright 截图 |
| **回归测试** | 全量测试 |

### 9.4 Claude Code Bug 修复 Prompt

```bash
修复 BUG：{BUG描述}

复现步骤：
1. {步骤1}
2. {步骤2}

预期：{预期行为}
实际：{实际行为}

约束：
- 只能修改：{文件列表}
- 不能修改：{文件列表}
- 必须保留：{功能列表}

验证要求：
- 修复后运行：{测试命令}
- 回归测试：{测试命令}
```

---

## 十、关联文档

| 文档 | 说明 | 关联度 |
|:-----|:-----|:-------|
| [[数字社区产品管理系统现状]] | 当前项目状态记录 | ⭐⭐⭐⭐⭐ |
| [[topics/ai-agent/Agent团队架构与工作流]] | 团队架构与系统拓扑 | ⭐⭐⭐ |
| [[Portal Shell + 子应用集成-技术细节]] | 本次技术实现细节 | ⭐⭐⭐⭐ |
| [[vibe-coding/项目管理.md]] | Vibe Coding 项目管理 | ⭐⭐⭐⭐⭐ |
| [[vibe-coding/开发经验.md]] | Vibe Coding 开发经验 | ⭐⭐⭐⭐ |
| [[automation-testing.md]] | 自动化测试规范 | ⭐⭐⭐⭐ |

---

**文档版本**: v1.2
**维护者**: 钟离
**更新记录**:

| 日期 | 版本 | 更新内容 | 更新人 |
|:-----|:-----|:--------|:------:|
| 2026-05-19 | v1.0 | 初版发布 | 钟离 |
| 2026-05-19 | v1.1 | 对齐Vibe Coding最佳实践 | 尼克·弗瑞 |
| 2026-05-19 | v1.2 | 修复Review问题：补充SIGKILL处理、完整案例、协作时序图、修正Prompt引号 | 尼克·弗瑞 |
| 2026-05-19 | v1.3 | 优化落地：创建memory-bank/目录及文件、创建deploy.sh脚本、添加快速上手一页纸 | 钟离 |
