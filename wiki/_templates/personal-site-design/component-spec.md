# Personal Site 组件设计规范
> 版本: v1.0 | 创建: 2026-05-23 | 维护者: 尼克·弗瑞
> 参考: Apple HIG / Material Design 3 / Vercel / Linear / Stripe

---

## 一、Personal Site 专用组件清单

### 1.1 内容展示组件

| 组件 | 说明 | 设计要点 |
|:---|:---|:---|
| **Hero** | 首屏展示区 | 左文右图，留白充足，标题45px |
| **BioCard** | 个人介绍卡 | 头像+简介+社交链接，Full圆角 |
| **DemoCard** | Demo展示卡片 | 封面图+标题+标签，hover:scale(1.02) |
| **DesignCaseCard** | 设计案例卡片 | 前后对比图，16:9缩略 |
| **ProjectCard** | 项目展示卡 | 图标+名称+描述+链接 |
| **SkillTag** | 技能标签 | 胶囊形，Accent边框，hover填充 |
| **TimelineItem** | 时间线 | 竖线+节点，左文字右年份 |
| **BlogCard** | 博客文章卡 | 标题+日期+摘要，hover下划线 |

### 1.2 交互组件

| 组件 | 说明 | 设计要点 |
|:---|:---|:---|
| **CTAButton** | 行动按钮 | Primary蓝，hover加深5% |
| **GhostButton** | 次级按钮 | 无边框，hover显示边框 |
| **IconButton** | 图标按钮 | 圆形，hover背景显现 |
| **CopyButton** | 复制按钮 | 带成功反馈动效 |
| **ThemeToggle** | 主题切换 | 太阳/月亮图标过渡 |

### 1.3 容器组件

| 组件 | 说明 | 设计要点 |
|:---|:---|:---|
| **Section** | 内容区块 | 上下padding 64-96px |
| **Container** | 宽度容器 | max-width 1200px，居中 |
| **Grid** | 网格布局 | 12栅格，卡片网格 |
| **Card** | 通用卡片 | 12px圆角，微弱阴影 |

---

## 二、组件设计细节

### 2.1 Hero Section

```html
<!-- 结构 -->
<section class="hero">
  <div class="hero-content">
    <h1 class="hero-title">你的名字</h1>
    <p class="hero-subtitle">你的定位/一句话简介</p>
    <div class="hero-cta">
      <a href="#contact" class="cta-primary">联系我</a>
      <a href="#projects" class="cta-ghost">看作品</a>
    </div>
  </div>
  <div class="hero-image">
    <img src="/avatar.jpg" alt="头像" />
  </div>
</section>

<!-- 规格 -->
.hero { display: flex; gap: 64px; align-items: center; min-height: 70vh; }
.hero-title { font-size: 45px; font-weight: 700; line-height: 1.2; }
.hero-subtitle { font-size: 20px; color: var(--color-text-secondary); margin-top: 16px; }
.hero-cta { display: flex; gap: 16px; margin-top: 32px; }
.hero-image img { width: 280px; height: 280px; border-radius: 50%; object-fit: cover; }
```

### 2.2 DemoCard

```html
<!-- 结构 -->
<article class="demo-card">
  <div class="demo-cover">
    <img src="/demo-cover.jpg" alt="Demo截图" />
    <div class="demo-overlay">
      <a href="/demo-link" target="_blank">查看Demo</a>
    </div>
  </div>
  <div class="demo-info">
    <h3 class="demo-title">Demo名称</h3>
    <div class="demo-tags">
      <span class="tag">React</span>
      <span class="tag">TypeScript</span>
    </div>
  </div>
</article>

<!-- 规格 -->
.demo-card { border-radius: 12px; overflow: hidden; background: var(--color-surface); }
.demo-card:hover { transform: translateY(-4px); transition: transform 0.2s; }
.demo-cover { aspect-ratio: 16/9; position: relative; overflow: hidden; }
.demo-cover img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s; }
.demo-card:hover .demo-cover img { transform: scale(1.05); }
.demo-overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.6); opacity: 0; transition: opacity 0.2s; display: flex; align-items: center; justify-content: center; }
.demo-card:hover .demo-overlay { opacity: 1; }
.demo-info { padding: 16px 20px; }
.demo-title { font-size: 16px; font-weight: 600; }
.demo-tags { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.tag { padding: 4px 10px; border-radius: 9999px; border: 1px solid var(--color-accent); font-size: 12px; color: var(--color-accent); }
```

### 2.3 BioCard

```html
<!-- 结构 -->
<div class="bio-card">
  <img class="bio-avatar" src="/avatar.jpg" alt="头像" />
  <div class="bio-content">
    <h2 class="bio-name">名字</h2>
    <p class="bio-title">职位/角色</p>
    <p class="bio-intro">个人简介段落...</p>
    <div class="bio-links">
      <a href="github" class="bio-link">
        <IconGithub />
      </a>
      <a href="twitter" class="bio-link">
        <IconTwitter />
      </a>
    </div>
  </div>
</div>

<!-- 规格 -->
.bio-card { display: flex; gap: 32px; padding: 32px; background: var(--color-surface); border-radius: 16px; }
.bio-avatar { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.bio-name { font-size: 24px; font-weight: 700; }
.bio-title { font-size: 16px; color: var(--color-accent); margin-top: 4px; }
.bio-intro { font-size: 15px; color: var(--color-text-secondary); margin-top: 12px; line-height: 1.6; }
.bio-links { display: flex; gap: 12px; margin-top: 20px; }
.bio-link { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: var(--color-bg); transition: background 0.2s; }
.bio-link:hover { background: var(--color-accent); color: white; }
```

### 2.4 CTAButton

```css
/* 规格 */
.btn-primary {
  padding: 12px 28px;
  background: var(--color-accent);
  color: white;
  border-radius: 8px;
  font-weight: 500;
  transition: background 0.15s, transform 0.1s;
}
.btn-primary:hover { background: #0052CC; }
.btn-primary:active { transform: scale(0.98); }

.btn-ghost {
  padding: 12px 28px;
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-weight: 500;
  transition: border-color 0.15s, background 0.15s;
}
.btn-ghost:hover { border-color: var(--color-accent); color: var(--color-accent); }
```

---

## 三、动效规格

### 3.1 标准过渡时长

| 交互 | 时长 | 缓动 |
|:---|:---|:---|
| 颜色变化 | 150ms | `ease-out` |
| 悬浮反馈 | 200ms | `cubic-bezier(0.2, 0, 0, 1)` |
| 页面元素进入 | 300-400ms | `cubic-bezier(0.2, 0, 0, 1)` |
| 卡片悬浮抬起 | 200ms | `cubic-bezier(0.2, 0, 0, 1)` |
| 模态打开 | 300ms | `cubic-bezier(0.2, 0, 0, 1)` |
| 图片放大 | 300ms | `cubic-bezier(0.4, 0, 0.2, 1)` |

### 3.2 悬浮动效

```css
/* 卡片悬浮抬起 */
.demo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* 按钮悬浮 */
.btn-primary:hover {
  background: #0052CC;
  box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
}

/* 链接下划线 */
.link:hover {
  text-decoration: underline;
  text-underline-offset: 4px;
}

/* 头像悬浮旋转 */
.bio-avatar:hover {
  transform: rotate(3deg) scale(1.02);
}
```

### 3.3 页面进入动效

```css
/* 元素渐入 */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeIn 0.4s cubic-bezier(0.2, 0, 0, 1) forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 交错延迟 */
.fade-in-delay-1 { animation-delay: 0.1s; }
.fade-in-delay-2 { animation-delay: 0.2s; }
.fade-in-delay-3 { animation-delay: 0.3s; }
```

---

## 四、响应式规范

### 4.1 断点

| 断点 | 宽度 | 布局调整 |
|:---|:---|:---|
| Mobile | < 640px | 单栏，Hero垂直堆叠 |
| Tablet | 640-1024px | 双栏网格 |
| Desktop | 1024-1280px | 三栏网格 |
| Wide | > 1280px | 四栏网格，最宽1200px |

### 4.2 移动端适配

```css
/* 移动端优先 */
.hero {
  flex-direction: column;
  text-align: center;
  padding: 48px 20px;
}

.hero-image {
  order: -1; /* 头像在上 */
}

/* 平板及以上 */
@media (min-width: 640px) {
  .hero { flex-direction: row; text-align: left; }
  .hero-image { order: 0; }
}
```

---

## 五、颜色变量（Personal Site）

```css
:root {
  /* 主色 */
  --color-primary: #0A0A0A;
  --color-text-secondary: #525252;
  --color-accent: #0066FF;
  --color-accent-hover: #0052CC;
  
  /* 背景色 */
  --color-bg: #FFFFFF;
  --color-surface: #F5F5F5;
  --color-elevated: #FAFAFA;
  
  /* 边框 */
  --color-border: #E0E0E0;
  
  /* 功能色 */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
}

/* 暗黑模式 */
[data-theme='dark'] {
  --color-primary: #FFFFFF;
  --color-text-secondary: #A3A3A3;
  --color-bg: #0A0A0A;
  --color-surface: #171717;
  --color-elevated: #262626;
  --color-border: #262626;
}
```

---

## 六、无障碍规范

- [ ] 所有按钮/链接有可见焦点环
- [ ] 图片有 alt 描述
- [ ] 颜色对比 ≥ 4.5:1
- [ ] 支持键盘导航
- [ ] 支持 reduce-motion

---

*版本：v1.0*
*最后更新：2026-05-23*
*维护者：尼克·弗瑞*