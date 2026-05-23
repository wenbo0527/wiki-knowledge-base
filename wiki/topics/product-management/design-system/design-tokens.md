# 中后台设计系统规范
> 版本: v1.0 | 创建: 2026-05-23 | 维护者: 尼克·弗瑞
> 来源: Arco Design / Ant Design Vue / 企业中后台最佳实践

---

## 一、定位

本规范用于**数字社区**（数据社区）中后台项目，为托尼·斯塔克和钟离提供 Arco Design 规范参考。

---

## 二、Arco Design 设计 Token

### 2.1 主色板（Primary Palette）

| 级别 | Token | 用途 |
|:---|:---|:---|
| primary-6 | `rgb(var(--arcoblue-6))` | 常规/主按钮 |
| primary-5 | `rgb(var(--arcoblue-5))` | 悬浮（hover） |
| primary-7 | `rgb(var(--arcoblue-7))` | 点击（click） |
| primary-4 | `rgb(var(--arcoblue-4))` | 特殊场景 |
| primary-3 | `rgb(var(--arcoblue-3))` | 一般禁用 |
| primary-2 | `rgb(var(--arcoblue-2))` | 文字禁用 |
| primary-1 | `rgb(var(--arcoblue-1))` | 浅色背景悬浮 |

### 2.2 功能色板

| 用途 | Token | 色值 |
|:---|:---|:---|
| Success | `--success-6` | `rgb(var(--green-6))` |
| Warning | `--warning-6` | `rgb(var(--orange-6))` |
| Danger/Error | `--danger-6` | `rgb(var(--red-6))` |
| Info | `--link-6` | `rgb(var(--arcoblue-6))` |

### 2.3 中性色板（Neutral Palette）

| Token | 用途 |
|:---|:---|
| `--color-neutral-10` | 深色背景 |
| `--color-neutral-9` | 卡片背景 |
| `--color-neutral-8` | 边框/分隔线 |
| `--color-neutral-7` | 强边框 |
| `--color-neutral-6` | 次级文字 |
| `--color-neutral-5` | 占位符 |
| `--color-neutral-4` | 禁用文字 |
| `--color-neutral-3` | 浅背景 |
| `--color-neutral-2` | 页面背景 |
| `--color-neutral-1` | 浅色背景 |

### 2.4 边框颜色

| Token | 用途 |
|:---|:---|
| `--color-border-1` | 浅色边框（表格分隔等） |
| `--color-border-2` | 一般边框（输入框等） |
| `--color-border-3` | 深色边框（聚焦状态） |

---

## 三、Arco Design 组件使用规范

### 3.1 通用组件

| 组件 | 规范要点 |
|:---|:---|
| **Button** | 优先使用 Primary 次之 Secondary，Ghost 用于工具栏 |
| **Icon** | 必须使用 Arco 内置图标，禁止使用不存在的图标 |
| **Typography** | 标题/正文/次级分层清晰，颜色对比 ≥ 4.5:1 |
| **Link** | 链接色使用 `--link-6` |

### 3.2 数据展示组件

| 组件 | 规范要点 |
|:---|:---|
| **Table** | 列头固定，支持排序，禁止超过7列 |
| **Card** | 圆角 `--border-radius-small`（6px）|
| **Tag** | 用于状态标签，危险标签用 danger 色 |
| **Badge** | 用于数量徽标，右上角定位 |
| **Avatar** | 头像组件，圆形/方形两种模式 |

### 3.3 数据输入组件

| 组件 | 规范要点 |
|:---|:---|
| **Input** | 带 label，必填项用 `*` 标识 |
| **Select** | 支持搜索，支持多选 |
| **DatePicker** | 范围选择支持快捷选项 |
| **Cascader** | 用于省市区等层级选择 |
| **Form** | 使用 `a-form` 和 `a-form-item` 组合 |

### 3.4 布局组件

| 组件 | 规范要点 |
|:---|:---|
| **Grid** | 24栅格系统，响应式断点 |
| **Space** | 组件间距统一使用 Space |
| **Layout** | Sidebar + Header + Content 结构 |

### 3.5 反馈组件

| 组件 | 规范要点 |
|:---|:---|
| **Modal** | 顶部标题栏，底部操作区 |
| **Message** | 全局轻提示，3秒自动消失 |
| **Notification** | 重要通知右下角弹出 |
| **Alert** | 页面内警告提示 |

---

## 四、中后台布局模式

### 4.1 标准后台布局

```
┌─────────────────────────────────────┐
│            Header (56px)             │
├────────┬────────────────────────────┤
│        │                            │
│Sidebar │      Content Area          │
│(240px) │                            │
│        │                            │
│        │                            │
└────────┴────────────────────────────┘
```

### 4.2 侧边栏规范

| 项目 | 规范 |
|:---|:---|
| 宽度 | 240px（可折叠到64px）|
| 背景色 | `--color-neutral-10` |
| 菜单项高度 | 44px |
| 选中态 | 左侧4px primary色边框 + 浅背景 |

### 4.3 页面结构

| 区域 | 高度/间距 |
|:---|:---|
| 页面标题栏 | 48px，含标题+操作按钮 |
| 筛选区 | 与内容区16px间距 |
| 表格区 | 自适应撑满 |
| 分页区 | 底部48px固定 |

---

## 五、响应式断点

| 断点 | 宽度 | 布局 |
|:---|:---|:---|
| **xs** | < 768px | 单栏/隐藏侧边栏 |
| **sm** | 768-992px | 双栏/侧边栏折叠 |
| **md** | 992-1200px | 三栏/侧边栏展开 |
| **lg** | 1200-1400px | 三栏/宽表格 |
| **xl** | > 1400px | 三栏/完整显示 |

---

## 六、暗黑模式支持

Arco Design 支持暗黑模式，使用 `arco-design-vue` 的 `ConfigProvider`：

```vue
<a-config-provider theme="dark">
  <App />
</a-config-provider>
```

**注意：** 切换主题时需要覆盖 CSS 变量：
```css
:root[arco-theme='dark'] {
  --color-bg-1: #171717;
  --color-bg-2: #111111;
}
```

---

## 七、设计检查清单

### 功能性检查
- [ ] 表单有 label，无 label 有 aria-label
- [ ] 表格有表头，无表头有 role="rowheader"
- [ ] 弹窗有 focus trap，ESC 可关闭
- [ ] 错误提示有描述，可访问

### 视觉检查
- [ ] 颜色对比 ≥ 4.5:1（大字 ≥ 3:1）
- [ ] 按钮/输入框 圆角一致（6px）
- [ ] 间距使用 4px 基准网格
- [ ] 表格行高统一，行高 ≥ 44px（可点击）

### 可访问性检查
- [ ] 所有交互元素 Tab 可聚焦
- [ ] Focus ring 可见
- [ ] 禁用态有 aria-disabled
- [ ] 加载状态有 aria-busy

---

## 八、数据社区特殊约束

| 约束项 | 说明 |
|:---|:---|
| **禁止修改** `accompany.ts` | 计算公式统一使用已有方法 |
| **禁止修改** `calculation.ts` | 计算逻辑不开放 |
| **路由同步** | 新增路由必须同步修改侧边栏菜单配置 |
| **样式隔离** | 使用 scoped CSS，避免样式污染 |

---

*版本：v1.0*
*最后更新：2026-05-23*
*维护者：尼克·弗瑞*
*参考：Arco Design Vue / Ant Design Vue / 企业中后台实践*