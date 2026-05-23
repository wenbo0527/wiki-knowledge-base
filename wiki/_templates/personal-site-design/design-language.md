# Personal Site 设计语言规范
> 版本: v1.0 | 创建: 2026-05-23 | 维护者: 尼克·弗瑞

---

## 一、定位与目标

### 核心定位
**个人品牌 + 创意作品集** — 技术深度与设计表现力兼具的个人网站

### 内容边界
| 模块 | 说明 |
|:---|:---|
| **个人展示** | 简介、能力、经历、方法论 |
| **Demo Gallery** | 产品Demo、设计系统、技术方案 |
| **设计展示** | UI设计、交互设计、品牌设计 |

### 设计目标
```
专业感 ←————————————→ 创意感
         70 : 30

克制留白 ←————————————→ 视觉张力
         60 : 40
```

---

## 二、设计语言（Design Language）

### 2.1 色彩系统

#### 主色调（Primary Palette）
参考 Apple + Vercel 的克制用色：

| 用途 | 色值 | 说明 |
|:---|:---|:---|
| **Primary** | `#0A0A0A` | 近黑，主文字 |
| **Secondary** | `#525252` | 次级文字 |
| **Accent** | `#0066FF` | 链接/CTA（蓝） |
| **Accent Alt** | `#7C3AED` | 高亮/徽标（紫） |

#### 功能色
| 用途 | 色值 |
|:---|:---|
| Success | `#10B981` |
| Warning | `#F59E0B` |
| Error | `#EF4444` |
| Info | `#3B82F6` |

#### 背景色
| 用途 | Light Mode | Dark Mode |
|:---|:---|:---|
| **Base** | `#FFFFFF` | `#0A0A0A` |
| **Surface** | `#F5F5F5` | `#171717` |
| **Elevated** | `#FAFAFA` | `#262626` |

#### 灰阶（Neutral Scale）
```
0:  #FAFAFA / #262626
50: #F5F5F5 / #171717
100: #EBEBEB / #111111
200: #E0E0E0 / #0A0A0A
300: #CFCFCF / #525252
400: #A3A3A3 / #737373
500: #737373 / #525252
600: #525252 / #3F3F3F
700: #3F3F3F / #262626
800: #262626 / #1A1A1A
900: #171717 / #111111
950: #0A0A0A / #09090B
```

---

### 2.2 字体系统（Typography）

#### 字体选择
| 用途 | 字体 | 备选 |
|:---|:---|:---|
| **中文正文** | `Noto Sans SC` | 系统默认 |
| **英文正文** | `Inter` | `SF Pro Display` |
| **代码/技术内容** | `JetBrains Mono` | `Fira Code` |
| **标题（英文）** | `SF Pro Display` | `Inter` |

#### Type Scale（M3启发）
```
Display Large:   57px / 1.12 lh / -0.25 letter
Display Medium: 45px / 1.16 lh /  0    letter
Display Small:  36px / 1.22 lh /  0    letter

Headline Large:  32px / 1.25 lh /  0    letter
Headline Medium: 28px / 1.29 lh /  0    letter
Headline Small:  24px / 1.33 lh /  0    letter

Title Large:     22px / 1.27 lh /  0    letter
Title Medium:    16px / 1.50 lh /  0.15 letter
Title Small:     14px / 1.43 lh /  0.1  letter

Body Large:      16px / 1.50 lh /  0.5  letter
Body Medium:     14px / 1.43 lh /  0.25 letter
Body Small:      12px / 1.33 lh /  0.4  letter

Label Large:     14px / 1.43 lh /  0.1  letter
Label Medium:    12px / 1.33 lh /  0.5  letter
Label Small:     11px / 1.45 lh /  0.5  letter
```

---

### 2.3 间距系统（Spacing Scale）

参考 8px 基准网格：

```
0:  0px
1:  4px
2:  8px
3:  12px
4:  16px
5:  24px
6:  32px
7:  48px
8:  64px
9:  96px
10: 128px
11: 192px
12: 256px
```

**常用场景：**
| 场景 | 间距 |
|:---|:---|
| 组件内 padding | 12-16px |
| 卡片 padding | 20-24px |
| 区块间距 | 48-64px |
| 页面边距（移动） | 16-20px |
| 页面边距（桌面） | 48-64px |

---

### 2.4 圆角（Border Radius）

| 级别 | 半径 | 用途 |
|:---|:---|:---|
| **None** | 0px | 几何图形/分隔线 |
| **Small** | 6px | 小标签/徽标 |
| **Medium** | 8px | 按钮/输入框 |
| **Large** | 12px | 卡片/面板 |
| **XLarge** | 16px | 模态框/大卡片 |
| **Full** | 9999px | 头像/胶囊按钮 |

**原则：** 中后台用 Medium，互联网产品可用 Large。Personal Site 偏向 Large。

---

### 2.5 阴影（Elevation / Shadow）

| 级别 | 值 | 用途 |
|:---|:---|:---|
| **None** | none | - |
| **1** | `0 1px 2px rgba(0,0,0,0.05)` | 卡片hover |
| **2** | `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)` | 悬浮元素 |
| **3** | `0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)` | 模态前奏 |
| **4** | `0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)` | 模态框 |

**Personal Site偏好：** 用微妙阴影，不滥用。不使用强渐变背景。

---

### 2.6 动效原则（Motion Principles）

参考 Apple + M3 的动效哲学：

#### 核心原则
```
1. 意图导向（Intent-driven）
   动效要有意义，服务于信息层级和用户注意力

2. 自然流畅（Natural）
   使用曲线而非线性缓动
   - 标准：cubic-bezier(0.2, 0, 0, 1)  用于进入
   - 标准：cubic-bezier(0.4, 0, 1, 1)  用于退出
   - 标准：cubic-bezier(0.4, 0, 0.2, 1)  用于通用

3. 克制有度（Measured）
   - 快速交互：100-200ms
   - 页面过渡：300-400ms
   - 大型元素：400-500ms

4. 减少干扰（Non-disruptive）
   动效不应打断用户任务流
```

#### 标准时长
| 类型 | 时长 |
|:---|:---|
| 颜色/透明度变化 | 150-200ms |
| 轻微悬浮反馈 | 100-150ms |
| 按钮点击反馈 | 100ms |
| 卡片悬浮抬起 | 200ms |
| 页面元素进入 | 300-400ms |
| 模态打开 | 300ms |
| 大型布局变化 | 400-500ms |

---

## 三、组件设计规范

### 3.1 Personal Site 专用组件

| 组件 | 说明 | 设计要点 |
|:---|:---|:---|
| **Hero Section** | 首屏展示 | 左文右图或纯文字，留足呼吸感，标题32-45px |
| **Demo Card** | Demo展示卡片 | 封面图+标题+标签，hover放大1.02x |
| **Design Case Card** | 设计案例卡片 | 前后对比，16:9缩略图 |
| **Bio Card** | 个人介绍卡 | 头像+简介+社交链接，圆角Full |
| **Skill Tag** | 技能标签 | 胶囊形状，accent边框 |
| **Timeline Item** | 时间线 | 竖线+节点，左文字右年份 |
| **Code Block** | 代码展示 | 深色背景，语法高亮，圆角8px |
| **CTA Button** | 行动按钮 | Primary蓝，hover加深5% |

### 3.2 组件变体规范

#### Demo Card 变体
```
Standard: 封面图 16:9，标题在下
Compact:  封面图 1:1，适合网格布局
Expanded: 包含描述文字，适合详情页
```

#### Button 变体
```
Primary:   蓝色填充，白字
Secondary: 蓝色描边，透明底
Ghost:     无边框，仅文字
Icon:      圆形，仅图标
```

---

## 四、互联网大厂设计参考

### 4.1 Vercel 设计语言
```
色彩：#000000 主色 + #FFFFFF 文字 + #555555 次级
字体：Inter + JetBrains Mono
间距：4px 基准网格
圆角：4px（克制）
动效：快速、功能驱动、无多余装饰
特点：极致克制、大量留白、网格系统精确
```

### 4.2 Linear 设计语言
```
色彩：#000000 主色 + #6942F2 紫色Accent
字体：Inter
圆角：6px（Small）
动效：subtle spring、物理感强
特点：深色模式优先、图标风格统一、键盘快捷键设计
```

### 4.3 Stripe 设计语言
```
色彩：#635BFF 主色 + #00D4FF 渐变
字体：Camphor（自定义）+ Numbers
圆角：6px
特点：金融级精确感、图表设计精致、文档质量标杆
```

### 4.4 Apple HIG 设计语言
```
色彩：系统原生，SF 颜色
字体：SF Pro + SF Mono
圆角：对应 iOS/macOS 系统
动效：物理仿真、意图导向
特点：交互精准反馈、细节极致、无障碍设计完善
```

### 4.5 Material Design 3 设计语言
```
色彩：Dynamic Color（用户定制）+ 语义化色板
字体：Roboto
圆角：Small-Medium-Large-Full（4级）
动效：Easing曲线标准化、共享元素过渡
特点：开源可扩展、设计token标准化、无障碍优先
```

---

## 五、设计原则总结

### Personal Site 10条核心原则

```
1. 克制用色
   不要超过3种主色，避免大量渐变背景
   
2. 大量留白
   区块间距48px起步，让内容呼吸
   
3. 精准对齐
   所有元素必须精确对齐，4px网格
   
4. 层次分明
   标题/正文/次级文字 颜色对比度 ≥ 4.5:1
   
5. 动效有度
   动效服务于反馈，不做装饰性动画
   
6. 组件一致
   同一组件在不同页面必须完全一致
   
7. 响应优先
   移动端优先设计，桌面端增强体验
   
8. 性能感知
   首屏加载≤2秒，使用骨架屏过渡
   
9. 可访问性
   所有交互元素键盘可访问，颜色对比合规
   
10. 内容为王
    设计服务于内容，不做过度设计
```

---

## 六、对比：Personal Site vs 企业中后台

| 维度 | Personal Site | 企业中后台（数字社区） |
|:---|:---|:---|
| **主色调** | 黑色系+蓝色accent | Arco Design 色板 |
| **圆角** | 12-16px（较大） | 4-8px（较小） |
| **阴影** | 微妙（1-2级） | 常规（2-3级） |
| **间距** | 宽松（48px+区块） | 紧凑（16-24px） |
| **动效** | 流畅、有个性 | 克制、功能性 |
| **排版** | 大标题、大留白 | 标准表格+紧凑布局 |

---

*版本：v1.0*
*最后更新：2026-05-23*
*维护者：尼克·弗瑞*
*参考：Apple HIG / Material Design 3 / Vercel / Linear / Stripe*