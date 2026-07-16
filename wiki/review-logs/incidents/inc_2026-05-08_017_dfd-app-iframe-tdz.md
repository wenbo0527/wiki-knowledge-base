---
title: inc 2026 05 08 017 dfd app iframe tdz
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents]
date: 2026-05-09
---

# 🔴 Incident #017: dfd-app iframe 空白 + rsync 权限覆盖 + 8081 后端离线

| 字段 | 值 |
|:---|:---|
| **ID** | inc_2026-05-08_017 |
| **严重级别** | 🔴 Critical |
| **状态** | ✅ Resolved |
| **发现时间** | 2026-05-08 09:30 |
| **发现者** | zhongli / wenbo |
| **负责人** | zhongli |
| **最后更新** | 2026-05-08 10:41 |

---

## 问题描述

dfd-app 微前端子应用在 portal-shell iframe 中加载后**空白无内容**，同时 `/dfd/discovery` 路径直接访问返回 500 Internal Server Error。另外用户访问时发现 API 请求 502。

## 影响分析

| 影响范围 | 说明 |
|:---|:---|
| **功能影响** | dfd-app 所有路由（`/dfd/discovery`、`/dfd/asset-catalog` 等）在 iframe 内均不可见 |
| **用户体验** | portal-shell 用户点击 dfd 相关菜单项后 iframe 区域空白 |
| **数据影响** | 无数据损失，仅前端渲染问题 |

## 根因分析

### 问题 1：dfd-app iframe 空白（TDZ 错误）

**核心问题**：Vite 动态导入代码分割 + terser 压缩，产生跨 chunk 循环引用，触发 Temporal Dead Zone（TDZ）错误。

```
Cannot access 'Dc' before initialization
  ← vue-vendor-DJ6UH4qI.js:10:13010（函数 kr）
  ← arco-design-DekX6mVc.js:1:4125
  ← __vite__mapDeps 动态 import 包装函数
```

**根本原因**：Vite 为动态 `import()` 创建 `__vite__mapDeps` 包装函数，当这些函数跨 chunk 引用时，terser 的 minification 改变了模块执行顺序，导致变量在初始化前被访问。

**对比**：risk-app 使用相同 terser 但无此问题 → dfd-app 特定 chunk 结构导致。

### 问题 2：rsync 权限覆盖导致 500

**核心问题**：`rsync` 默认保留源文件权限，本地 `dist/` 中 `index.html` 以 600 权限上传，www-data 无法读取。

**nginx 错误循环**：
```
stat() "/var/www/html/dfd/index.html" failed (13: Permission denied)
→ rewrite or internal redirection cycle while internally redirecting to "/dfd/index.html"
→ 500 Internal Server Error
```

### 问题 3：502 Bad Gateway（API 后端离线）

**核心问题**：`product-backend` 服务未在服务器上运行，nginx `proxy_pass localhost:8081` 无人接收。

```nginx
location /api/v1/ {
    proxy_pass http://localhost:8081/api/v1/;  # ← 无服务监听 8081
}
```

控制台日志显示 shell-app 已有 fallback 到 mock 数据的逻辑，不影响主 portal 功能，但 dfd-app 内部的 API 调用（如果有）会 502。

---

## 解决措施

### 问题 1 解决：禁用 Vite 代码分割 + exclude vendor

```ts
// vite.config.ts
build: {
  rollupOptions: { output: { manualChunks: undefined } },
  optimizeDeps: {
    exclude: ['vue', '@arco-design/web-vue', 'vue-router', 'pinia', 'echarts']
  },
  minify: 'terser',
  chunkSizeWarningLimit: 2000
}
```

**效果**：所有 node_modules 打包为单个 3.5MB vendor chunk，消除了跨 chunk 引用。

**最终 chunks**：
- `index-6FQokTm6.js`（16KB 主入口）
- `vendor-D4Kmdb2e.js`（3.5MB 全量依赖）

### 问题 2 解决：修复 index.html 权限

```bash
ssh root@118.196.79.130 \
  "chmod 644 /var/www/html/dfd/index.html && chown www-data:www-data /var/www/html/dfd/index.html"
```

**预防**：后续 rsync 部署后统一执行权限修复：
```bash
rsync -avz --delete dist/ root@118.196.79.130:/var/www/html/dfd/ && \
ssh root@118.196.79.130 "chown -R www-data:www-data /var/www/html/dfd/ && chmod -R 755 /var/www/html/dfd/"
```

### 问题 3 状态：临时性基础设施问题

product-backend（Java Spring Boot JAR）未在服务器运行，非 dfd-app 代码问题。

---

## 依赖与阻塞

| 依赖方 | 事项 | 状态 |
|:---|:---|:---:|
| 基础设施 | product-backend 服务重启（端口 8081） | 🔄 待确认 |

---

## 关联文档

- dfd-app 源码：`/Users/wenbo/Documents/project/data_community/apps/dfd-app/`
- vite.config.ts：`/Users/wenbo/Documents/project/data_community/apps/dfd-app/vite.config.ts`
- nginx 配置：`/etc/nginx/sites-enabled/shell-app-single-port`
- 相关 Lesson：`lessons/by-agent/zhongli/les_2026-05-08_017.md`

---

## 解决方案扩展：nginx upstream 故障转移（2026-05-08 新增）

### 问题
后端 8081 不可用时，nginx 直接返回 502，前端 fallback 逻辑无法触发。

### 解法
```nginx
upstream product_backend {
    server localhost:8081;
    server localhost:8082 backup;  # mock server
}
```

**实现步骤**：
1. mock server 端口从 8081 → 8082（避免冲突）
2. nginx 添加 upstream 块，所有 `proxy_pass localhost:8081` → `proxy_pass http://product_backend`
3. 启动 mock server：`nohup node /var/www/product/mock-api-server.js > mock-api-server.log &`
4. nginx `-s reload`

**验证**：8081 down 时，`curl https://localhost:8443/api/v1/product-overview/` 返回 200（来自 8082）

---

## 后续行动

- [x] 编写 Lesson 沉淀 dfd-app TDZ 问题经验 - zhongli - 2026-05-08
- [x] 将权限修复步骤加入部署脚本 - zhongli - 2026-05-08
- [ ] [ ] 确认 product-backend 状态并通知相关方 - 基础设施 - 待定
- [ ] [ ] 将 mock server 8082 启动脚本永久化（systemd 或 pm2）- zhongli - 2026-05-08
- [ ] [ ] 解决 conflicting server name "_" warning - 基础设施 - 待定

---

*Created: 2026-05-08 | Updated: 2026-05-08*
