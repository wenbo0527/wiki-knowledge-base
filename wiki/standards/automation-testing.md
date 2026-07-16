---
title: automation testing
author: 尼克·弗瑞 🕵️
product_domain: PD-STANDARD
doc_type: 其他
tags: [standards]
date: 2026-05-09
---

# 自动化测试规范

> 本规范基于 **Demo 项目 Mock API 部署实战**（2026-05-06）总结。
> 核心原则：**快速反馈、覆盖全面、可复现**。

---

## 1. 测试分层模型

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: HTTP API 测试                                       │
│  目的: 验证后端 API 响应状态、数据格式、业务逻辑                │
│  工具: curl / Node.js http 模块                               │
│  时机: 每次代码提交后 CI/CD 自动执行                           │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: 页面状态测试                                         │
│  目的: 验证前端页面可访问性、静态资源加载                       │
│  工具: curl / Node.js http 模块                               │
│  时机: 每次部署后自动执行                                      │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: 浏览器端测试 (E2E)                                   │
│  目的: 验证用户交互、JS 错误、UI 渲染                          │
│  工具: Playwright / Cypress                                   │
│  时机: 关键路径、发布前手动触发或定时执行                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. HTTP API 测试规范

### 2.1 测试文件位置

```
项目/
├── scripts/
│   └── api-test.js          # API 测试脚本（Node.js）
├── test/
│   ├── http-api/
│   │   ├── *.test.js        # Vitest 单元测试
│   │   └── *.api.test.js    # API 集成测试
```

### 2.2 测试用例结构

```javascript
const API_TESTS = [
  // ✅ 必填字段
  { name: 'GET /api/resource',      // 显示名称，包含方法和路径
    path: '/api/resource',           // 请求路径
    method: 'GET',                   // HTTP 方法: GET | POST | PUT | DELETE
    expectedStatus: 200 },           // 期望状态码
  
  // ✅ 响应体验证
  { name: 'GET /api/list',
    path: '/api/list',
    method: 'GET',
    expectedStatus: 200,
    validator: (data) => data.list && data.list.length > 0 },  // 自定义验证
  
  // ✅ POST 带请求体
  { name: 'POST /api/resource',
    path: '/api/resource',
    method: 'POST',
    expectedStatus: 200,
    body: { name: '测试资源' } },   // 请求体
  
  // ✅ 带查询参数
  { name: 'GET /api/search',
    path: '/api/search?q=test',
    method: 'GET',
    expectedStatus: 200 },
];
```

### 2.3 测试脚本模板

```javascript
#!/usr/bin/env node
/**
 * HTTP API 自动化测试
 * 用法: node scripts/api-test.js
 * 依赖: Node.js 内置模块 (http, https, url)
 */

const http = require('http');
const https = require('https');

const BASE_URL = process.env.API_BASE_URL || 'https://118.196.79.130:8443';

/**
 * 发起 HTTP 请求
 */
function httpRequest(path, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const client = url.protocol === 'https:' ? https : http;
    
    const req = client.request({
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'APITest/1.0',
        ...(body && { 'Content-Length': Buffer.byteLength(JSON.stringify(body)) }),
      },
      rejectUnauthorized: false,  // 允许自签名证书
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, data });
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Timeout')); });
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

/**
 * 执行单个测试
 */
async function runTest(test) {
  const start = Date.now();
  try {
    const result = await httpRequest(test.path, test.method, test.body);
    const duration = Date.now() - start;
    const passed = result.status === test.expectedStatus;
    const valid = test.validator ? test.validator(result.data) : true;
    
    return {
      name: test.name,
      passed: passed && valid,
      status: result.status,
      duration,
      error: !passed ? `Status ${result.status} !== ${test.expectedStatus}` : 
             !valid ? 'Validator failed' : null,
    };
  } catch (err) {
    return {
      name: test.name,
      passed: false,
      status: null,
      duration: Date.now() - start,
      error: err.message,
    };
  }
}

/**
 * 主测试流程
 */
async function main() {
  // ... 加载测试用例，执行，输出报告
}

main();
```

---

## 3. 页面状态测试规范

### 3.1 测试范围

| 类型 | 检查项 | 阈值 |
|:---|:---|:---|
| HTTP 状态码 | 200 = 正常，4xx/5xx = 异常 | 必须是 200 |
| Content-Type | HTML/JSON/JS/CSS 等 | 必须是有效类型 |
| 响应时间 | 页面加载时间 | < 2s（生产环境）|

### 3.2 页面清单模板

```javascript
const PAGE_TESTS = [
  // === Shell App ===
  { name: 'Shell App 首页',        path: '/home/' },
  { name: 'Shell App 产品概览',    path: '/home/product-overview' },
  
  // === risk-app ===
  { name: 'Risk App 首页',         path: '/risk/' },
  { name: 'Risk App 外数档案',     path: '/risk/external-data/archive' },
  { name: 'Risk App 预算合同',     path: '/risk/budget/contract' },
  
  // ... 其他子应用
];
```

### 3.3 子应用健康检查点

每个子应用必须验证：
1. **首页** (`/`) - 基础可访问性
2. **核心功能页** (至少 1 个) - 业务路径验证
3. **静态资源** (`/assets/*.js`, `/assets/*.css`) - CDN/缓存验证

---

## 4. Mock API 管理规范

### 4.1 Mock API 适用场景

```
✅ 适用 Mock：
  - 后端 API 未完成（前后端并行开发）
  - 依赖第三方服务不稳定
  - 需要快速搭建 Demo 环境
  - 数据库未部署或不可用

❌ 不适用 Mock：
  - 已有真实后端 API
  - 需要真实数据的端到端测试
  - 生产环境部署
```

### 4.2 Mock API 实现原则

1. **路径与真实 API 一致**：Mock API 路径必须与前端调用的路径完全一致
2. **响应格式与真实 API 一致**：包括字段名、数据类型、嵌套结构
3. **支持 CORS**：添加 `Access-Control-Allow-Origin: *`
4. **支持 POST/PUT/DELETE**：不要只测 GET
5. **区分 200 和 404**：未实现的 API 返回 404，不是 200

### 4.3 Mock API 数据生成

```javascript
// ✅ 使用函数生成动态数据（推荐）
function generateMockProducts() {
  return [
    { id: 1, name: '运营商数据', supplier: '中国移动', status: 'active' },
    { id: 2, name: '电商消费数据', supplier: '京东', status: 'active' },
    // ...
  ];
}

// ❌ 避免硬编码静态数据（数据无法动态变化）
// const products = [{ id: 1, name: '...', ... }];
```

### 4.4 Mock API 部署

```
Mock API 服务部署路径: /var/www/product/mock-api-server.js
日志文件:                /var/www/product/mock-api.log
端口:                    8081
启动命令:                nohup node mock-api-server.js > mock-api.log 2>&1 &
重启:                    pkill -f mock-api-server.js && nohup node mock-api-server.js > mock-api.log 2>&1 &
```

---

## 5. nginx 配置规范

### 5.1 API 代理配置

```nginx
# ✅ 正确：location 不带尾斜杠，避免 POST 301 重定向
location /external-data-task {
    proxy_pass http://localhost:8081/external-data-task;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Access-Control-Allow-Origin *;
}

# ❌ 错误：location 带尾斜杠，POST /external-data-task 会 301 重定向到 /external-data-task/
location /external-data-task/ {
    proxy_pass http://localhost:8081/external-data-task/;
}
```

### 5.2 关闭绝对重定向

```nginx
server {
    # 防止 POST 请求被重定向
    absolute_redirect off;
}
```

### 5.3 重载 nginx

```bash
# 测试配置
nginx -t

# 重载配置（不中断连接）
nginx -s reload

# 完整重启
systemctl restart nginx
```

---

## 6. 测试执行规范

### 6.1 快速验证命令

```bash
# 测试所有 API（不依赖外部模块）
node scripts/api-test.js

# 检查 nginx 配置
ssh root@118.196.79.130 'nginx -t'

# 检查 Mock API 服务状态
ssh root@118.196.79.130 'ps aux | grep mock-api | grep -v grep'
```

### 6.2 CI/CD 集成

```yaml
# .github/workflows/test.yml
name: API Test
on: [push, pull_request]

jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run API Tests
        run: node scripts/api-test.js
        env:
          API_BASE_URL: ${{ secrets.API_BASE_URL }}
```

### 6.3 部署后验证清单

```
部署完成后必须验证：
□ 所有 GET API 返回 200
□ 所有 POST/PUT/DELETE API 返回 200（非 301/302）
□ 所有页面 URL 返回 200
□ Mock API 服务正在运行（ps aux | grep mock-api）
□ nginx 配置已重载（nginx -t 通过）
```

---

## 7. 常见问题排查

### 7.1 POST 请求返回 301

**原因**：nginx location 带尾斜杠，URL 规范化重定向
**解决**：移除 location 尾斜杠，或添加 `absolute_redirect off;`

### 7.2 API 返回 404

**排查步骤**：
1. 直接测试 Mock API：`curl http://localhost:8081/api/path`
2. 检查 nginx 代理：`curl -I https://domain/api/path`
3. 确认路径匹配：检查 nginx location 配置

### 7.3 后端返回空数据

**原因**：后端连接数据库失败，业务逻辑异常被静默处理
**解决**：查看后端日志，确认数据库连接；临时使用 Mock API 绕过

### 7.4 浏览器显示 "Real API unavailable"

**原因**：前端检测到真实 API 不可用，使用了内置 mock fallback
**解决**：这是前端的容错机制，只要页面数据正常显示即可；如果不希望使用 fallback，修复真实 API

---

## 8. 附录：测试脚本模板

```javascript
// scripts/api-test.js - 复制此模板快速创建测试

const http = require('http');
const https = require('https');

const BASE_URL = process.env.API_BASE_URL || 'https://118.196.79.130:8443';

const API_TESTS = [
  // 在此添加 API 测试用例
];

const PAGE_TESTS = [
  // 在此添加页面测试用例
];

async function httpRequest(path, method = 'GET', body = null) {
  const url = new URL(path, BASE_URL);
  const client = url.protocol === 'https:' ? https : http;
  
  return new Promise((resolve, reject) => {
    const req = client.request({
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers: { 'Content-Type': 'application/json', 'User-Agent': 'Test/1.0' },
      rejectUnauthorized: false,
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, data }); }
      });
    });
    req.on('error', reject);
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Timeout')); });
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function runTests() {
  let passed = 0, failed = 0;
  
  for (const test of [...API_TESTS, ...PAGE_TESTS]) {
    try {
      const r = await httpRequest(test.path, test.method, test.body);
      const ok = r.status === test.expectedStatus;
      if (ok) { passed++; console.log(`✅ ${test.name}`); }
      else { failed++; console.log(`❌ ${test.name} - Status ${r.status}`); }
    } catch (e) {
      failed++; console.log(`❌ ${test.name} - ${e.message}`);
    }
  }
  
  console.log(`\n结果: ${passed} 通过, ${failed} 失败`);
  process.exit(failed > 0 ? 1 : 0);
}

runTests();
```

---

## 9. 更新记录

| 日期 | 版本 | 更新内容 |
|:---|:---:|:---|
| 2026-05-06 | v1.0 | 初稿，基于 Demo 项目 Mock API 部署实战 |
