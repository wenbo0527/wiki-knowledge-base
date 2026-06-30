# mkt-app 案例数据

> **A 路径**：`~/.openclaw/skills/digital-community-dev-workflow/_registry/mkt-app.json`
> **扫描日期**：2026-06-11

## 技术栈

| 依赖 | 版本 |
|:--|:--|
| vue | ^3.4.0 |
| @arco-design/web-vue | ^2.55.0 |
| build | vite |

## 规模

| 指标 | 值 |
|:--|--:|
| index.vue 数 | 47 |
| mock 文件数 | 13 |

## 关键教训

### 教训 #1: a-dropdown 菜单触发器必须配 <template #content>
- **日期**: 2026-06-11
- **来源**: dev Story-003-2 v1.2.9

### 教训 #2: confirmModal 弹窗双状态复用（action 字段切换）
- **日期**: 2026-06-11
- **来源**: dev Story-003-2 v1.2.9

### 教训 #3: handleStatusChange 接受 targetStatus 参数而非双向推断
- **日期**: 2026-06-11
- **来源**: dev Story-003-2 v1.2.9

### 教训 #4: 解绑回退 draft 要清 inactive_time
- **日期**: 2026-06-11
- **来源**: dev Story-003-2 v1.2.9

### 教训 #5: vue SFC <script setup> 不能用 TS type annotation（用 as const）
- **日期**: 2026-06-09
- **来源**: dev 6/9 mock 补 12 字段


## 加载方式

```bash
# 加载本 app 的教训
bash /Users/wenbo/.openclaw/skills/digital-community-dev-workflow/scripts/load-app.sh mkt-app
```
