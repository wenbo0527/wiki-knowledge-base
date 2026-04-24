# Arco Design Pro Vue 中后台最佳实践规范

*基于官方 Arco Design Pro Vue 项目总结*

---

## 1. 📁 项目结构规范

```
src/
├── api/              # API 接口层（按模块划分）
│   ├── user.ts
│   ├── menu.ts
│   └── interceptor.ts
├── assets/          # 静态资源
├── components/       # 公共组件（按功能命名）
│   ├── breadcrumb/
│   ├── chart/
│   ├── menu/
│   └── navbar/
├── config/           # 配置文件
│   └── settings.json
├── directive/        # 自定义指令
├── hooks/            # 组合式函数（推荐）
│   ├── request.ts   # 请求封装
│   ├── loading.ts
│   ├── permission.ts
│   └── user.ts
├── layout/           # 布局组件
├── locale/          # 国际化
├── mock/            # Mock 数据
├── router/          # 路由（分层设计）
│   ├── index.ts     # 入口
│   ├── guard/       # 路由守卫
│   ├── routes/      # 路由配置
│   └── app-menus/   # 菜单配置
├── store/            # 状态管理（Pinia）
│   ├── index.ts
│   └── modules/
│       ├── user/
│       ├── app/
│       └── tab-bar/
├── types/           # TypeScript 类型定义
├── utils/           # 工具函数
│   ├── auth.ts      # Token 管理
│   ├── is.ts        # 类型判断
│   └── route-listener.ts
└── views/           # 页面（按业务域划分）
    ├── dashboard/
    ├── user/
    ├── form/
    └── list/
```

---

## 2. 🔌 API 层规范

### 基础规则
- 使用 axios 封装请求
- 类型安全：每个 API 函数都有明确的返回类型
- 按模块划分文件

### 示例

```typescript
// api/user.ts
import axios from 'axios';
import type { HttpResponse } from '@/api/interceptor';

export interface LoginData {
  username: string;
  password: string;
}

export interface LoginRes {
  token: string;
}

export function login(data: LoginData) {
  return axios.post<LoginRes>('/api/user/login', data);
}

export function logout() {
  return axios.post<LoginRes>('/api/user/logout');
}

export function getUserInfo() {
  return axios.post<UserState>('/api/user/info');
}

export function getMenuList() {
  return axios.post<RouteRecordNormalized[]>('/api/user/menu');
}
```

---

## 3. 🗄️ 状态管理规范（Pinia）

### 基础规则
- 使用 `defineStore` 创建 store
- 类型安全：state、getters、actions 都要有类型
- 按模块划分 store 文件

### 示例

```typescript
// store/modules/user/index.ts
import { defineStore } from 'pinia';
import { login as userLogin, logout as userLogout, getUserInfo, LoginData } from '@/api/user';
import { setToken, clearToken } from '@/utils/auth';
import { removeRouteListener } from '@/utils/route-listener';
import { UserState } from './types';
import useAppStore from '../app';

const useUserStore = defineStore('user', {
  state: (): UserState => ({
    name: undefined,
    avatar: undefined,
    // ...
  }),

  getters: {
    userInfo(state: UserState): UserState {
      return { ...state };
    },
  },

  actions: {
    setInfo(partial: Partial<UserState>) {
      this.$patch(partial);
    },

    resetInfo() {
      this.$reset();
    },

    async info() {
      const res = await getUserInfo();
      this.setInfo(res.data);
    },

    async login(loginForm: LoginData) {
      const res = await userLogin(loginForm);
      setToken(res.data.token);
    },

    async logout() {
      try {
        await userLogout();
      } finally {
        this.logoutCallBack();
      }
    },
  },
});

export default useUserStore;
```

---

## 4. 🛡️ 路由守卫规范

### 基础规则
- 路由守卫分层：页面守卫、权限守卫、登录信息守卫
- 使用 `beforeEach` 处理路由变化
- 统一错误处理

### 示例

```typescript
// router/guard/index.ts
import type { Router } from 'vue-router';
import { setRouteEmitter } from '@/utils/route-listener';
import setupUserLoginInfoGuard from './userLoginInfo';
import setupPermissionGuard from './permission';

function setupPageGuard(router: Router) {
  router.beforeEach(async (to) => {
    setRouteEmitter(to);
  });
}

export default function createRouteGuard(router: Router) {
  setupPageGuard(router);
  setupUserLoginInfoGuard(router);
  setupPermissionGuard(router);
}
```

---

## 5. 🎣 Hooks 规范

### 基础规则
- 使用 hooks 封装复用逻辑
- 单一职责：每个 hook 只做一件事
- 统一管理 loading 状态

### 示例

```typescript
// hooks/request.ts
import { ref, UnwrapRef } from 'vue';
import { AxiosResponse } from 'axios';
import { HttpResponse } from '@/api/interceptor';
import useLoading from './loading';

export default function useRequest<T>(
  api: () => Promise<AxiosResponse<HttpResponse>>,
  defaultValue = [] as unknown as T,
  isLoading = true
) {
  const { loading, setLoading } = useLoading(isLoading);
  const response = ref<T>(defaultValue);

  api()
    .then((res) => {
      response.value = res.data as unknown as UnwrapRef<T>;
    })
    .finally(() => {
      setLoading(false);
    });

  return { loading, response };
}
```

---

## 6. 🛠️ 工具函数规范

### 基础规则
- 单一职责：每个文件只做一件事
- 统一导出
- TypeScript 类型支持

### 示例

```typescript
// utils/auth.ts
const TOKEN_KEY = 'token';

export const isLogin = () => !!localStorage.getItem(TOKEN_KEY);
export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (token: string) => localStorage.setItem(TOKEN_KEY, token);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);
```

---

## 7. 📦 推荐依赖

### 核心依赖
| 包名 | 版本 | 用途 |
|------|------|------|
| vue | ^3.2 | 框架 |
| vue-router | ^4.0 | 路由 |
| pinia | ^2.0 | 状态管理 |
| @arco-design/web-vue | ^2.44 | UI 组件库 |
| axios | ^0.24 | HTTP 请求 |
| @vueuse/core | ^9.3 | Vue 组合式工具 |

### 开发规范依赖
| 包名 | 用途 |
|------|------|
| eslint + prettier | 代码规范 |
| husky + lint-staged | Git Hooks |
| typescript | 类型检查 |
| vite | 构建工具 |

---

## 8. 📋 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserCard.vue` |
| 工具函数 | camelCase | `formatDate.ts` |
| API 文件 | 与模块对应 | `user.ts` |
| 类型定义 | `types/` 目录 | `types/user.ts` |
| Hooks | `use` 前缀 | `useRequest.ts` |
| Store 模块 | 与功能对应 | `store/modules/user/` |
| 页面组件 | `index.vue` 为主 | `views/user/index.vue` |

---

## 9. 📝 Git 提交规范

使用 CommitLint + Conventional Commits：

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
perf: 性能优化
test: 测试
chore: 构建/工具
```

---

*最后更新：2026-04-22*
