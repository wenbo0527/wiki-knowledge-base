# Insight: 卡片式对话协议方案 - 淘宝实践

> 来源: 大淘宝技术 | 作者: 无二 | 发布时间: 2026-04-17

---

## 元信息

- **来源**: [微信公众 - 大淘宝技术](https://mp.weixin.qq.com/s/-aPwcWt076X0B-sEXIeTAg)
- **类型**: 行业实践
- **标签**: #AgentUI #协议设计 #MCP #A2UI #卡片交互
- **关联专题**: [[agent-engineering]], [[ai-programming]]

---

## 核心摘要

本文探讨了在智能助手对话流中实现卡片式交互的系统性工程方案，围绕三个核心问题展开：

1. **卡片如何嵌入对话流？** - Markdown扩展方案
2. **卡片数据从何而来？** - 数据获取模式演进
3. **多团队协作怎么不乱？** - 四层统一协议体系

---

## 一、卡片嵌入方案

### 三种方案对比

| 方案 | 实现方式 | 优势 | 劣势 | 推荐场景 |
|------|----------|------|------|----------|
| **代码块扩展** | ` ```ProductCard {...} ``` ` | 改造成本低、模型约束简单 | JSON格式要求严格 | ✅ 生产环境首选 |
| **占位符替换** | `[(ProductCard)]` | 轻量、数据可异步填充 | 流式体验差、需骨架屏 | 静态内容场景 |
| **自定义标签** | `<boltArtifact>` | 表达力最强、支持嵌套 | 需独立XML parser | 多模型统一管控 |

### 生产实践：代码块扩展

```markdown
模型输出的Markdown格式：
```ProductCard
{
  "title": "iPhone 15 Pro Max",
  "itemPrice": 9999,
  "imageUrl": "https://example.com/iphone.jpg"
}
```
```

```javascript
// React-Markdown扩展实现
const CARD_COMPONENTS = {
  ProductCard: ProductCard,
  FlightCard: FlightCard,
  UserProfile: UserProfile,
};

function ChatMessage({ markdown }) {
  return (
    <Markdown
      children={markdown}
      components={{
        code(props) {
          const { children, className, ...rest } = props;
          const match = /language-(\w+)/.exec(className || '');
          const langName = match ? match[1] : null;
          
          // 命中组件注册表 → 渲染业务卡片
          if (langName && CARD_COMPONENTS[langName]) {
            const CardComponent = CARD_COMPONENTS[langName];
            const cardProps = JSON.parse(String(children));
            return <CardComponent {...cardProps} />;
          }
          
          // 未命中 → 走默认的代码高亮渲染
          return <code {...rest} className={className}>{children}</code>;
        },
      }}
    />
  );
}
```

### System Prompt约束

```markdown
# 卡片生成规范
当需要展示结构化信息（商品、航班、用户资料等）时，使用Markdown代码块格式：
## 语法
- 语言标识使用组件名（PascalCase），如 `ProductCard`、`FlightCard`
- 代码体使用标准 JSON，属性名 camelCase
- 确保 JSON 格式合法，属性名使用双引号
## 示例
```ProductCard
{
  "title": "商品名称",
  "itemPrice": 99,
  "imageUrl": "https://example.com/img.jpg"
}
```
```

---

## 二、数据获取方案演进

### 三阶段演进

```
模型直出 → 增量Patch → Tool驱动
(最快出活)  (数据可靠)  (架构干净)
```

### 阶段1: 模型直出 (不可靠)

**问题**：
- 模型编造不存在的商品链接
- 价格和实际售价不一致
- 无法做个性化推荐

**结论**：只适合静态内容（百科摘要、功能说明）

### 阶段2: 增量Patch (先占位，后补数据)

```
模型输出骨架 → 前端渲染骨架屏 → 服务端异步获取数据 → Patch替换
```

```json
// 消息格式示例
[
  {"type": "full", "data": {"markdown": "为你推荐以下商品：\n```ProductCard\n{\n id:xxx\n}\n```\n"}},
  {"type": "patch", "patch": [
    {"op": "replace-substring", "path": "/markdown", "substring": "```ProductCard\n{\n id:xxx\n}\n```", "replacement": "```ProductCard\n{\n \"id\": \"12345\", \"title\": \"智能手环\", \"price\": 299\n}\n```"}
  ]}
]
```

**问题**：用户体验有"跳变"，RPC延迟时更明显

### 阶段3: Tool驱动 (推荐)

#### MCP Apps (Anthropic)

- **理念**：Tool返回数据+UI描述，UI是Tool的附属
- **特点**：Tool强绑定UI（search_products → ProductList卡片）
- **优势**：数据与UI一步到位

#### A2UI (Google)

- **理念**：Agent自主组合UI组件，纯粹定义"界面应该长什么样"
- **特点**：框架无关JSON Schema，描述与渲染分离
- **优势**：Web/iOS/Android共用一份JSON描述

#### 两者关系

| 维度 | MCP Apps | A2UI |
|------|----------|------|
| 驱动方式 | 工具驱动 | Agent驱动 |
| 粒度 | Tool级别 | 组件级别 |
| 适用场景 | 卡片类型确定 | 动态UI生成 |

**推荐组合**：MCP Apps Tool层绑定 + A2UI JSON Schema

---

## 三、四层统一协议体系

### 协议架构

```
┌─────────────────────────────────────────────────────────────┐
│                    四层协议体系                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Markdown标记协议                                    │
│  ├── 解决：卡片在文本流中怎么写                               │
│  └── 约定：代码块扩展格式、支持组件类型                        │
│                                                              │
│  Layer 2: 消息传输协议                                        │
│  ├── 解决：前后端之间传什么格式                               │
│  └── 定义：full/patch/recommend等数据包结构                   │
│                                                              │
│  Layer 3: UI渲染协议                                          │
│  ├── 解决：卡片长什么样                                       │
│  └── 标准：JSON Schema，跨端一致性                           │
│                                                              │
│  Layer 4: 事件通信协议                                        │
│  ├── 解决：用户点了卡片之后怎么办                             │
│  └── 定义：Action类型、API调用、状态更新                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Markdown标记协议

**统一约定**：
- 所有Agent共用一份System Prompt"卡片生成规范"
- 前端只维护一套Markdown解析器
- 新增卡片类型只需注册组件，不改解析逻辑

### Layer 2: 消息传输协议

```json
// 标准消息格式
{
  "type": "text",           // 模型Markdown消息
  "content": "为你推荐..."
}
{
  "type": "recommend/prompt",  // 追问推荐
  "content": ["你可能喜欢1", "你可能喜欢2"]
}
```

### Layer 3: UI渲染协议 (A2UI)

**两阶段演进**：
1. **预设卡片阶段** - 预定义模板+JSON数据，保证内容可控
2. **Agent生成阶段** - Agent自主组合UI组件，实现千人千面

### Layer 4: 事件通信协议

**核心原则**：卡片JSON只描述"是什么"和"能做什么"，不包含"怎么做"

```json
// 声明式Action示例
{
  "type": "button",
  "text": "加入购物车",
  "action": {
    "type": "api",
    "action": "addToCart",
    "params": {"itemId": "12345"}
  }
}
```

**事件处理流程**：
```
用户点击 → 事件处理器识别type=api → 发起网关请求 → 更新卡片状态
```

---

## 四、Agentic协议生态

### 关键协议一览

| 协议 | 厂商 | 定位 |
|------|------|------|
| **MCP** | Anthropic | Agent安全连接外部工具、工作流和数据源的开放标准 |
| **MCP Apps** | Anthropic | Tool返回数据+UI描述，Tool驱动UI |
| **A2UI** | Google | 声明式UI规范，Agent响应的视觉组织方式 |
| **A2A** | Google | 分布式Agent系统中Agent之间的协调协议 |
| **AG-UI** | Agent Protocol | 基于事件的标准，连接Agent与面向用户的应用 |
| **Open-JSON-UI** | OpenAI | Agent响应的视觉描述格式 |

### 协议关系图

```
┌─────────────────────────────────────────────────────────────┐
│                    Agentic协议生态                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Agent能力层                                                 │
│  ├── A2A (Agent ↔ Agent)                                   │
│  ├── MCP (Agent ↔ Tools)                                   │
│  └── AG-UI (Agent ↔ User)                                  │
│                                                              │
│  UI呈现层                                                    │
│  ├── MCP Apps (Tool驱动UI)                                  │
│  ├── A2UI (声明式UI)                                        │
│  └── Open-JSON-UI (视觉描述)                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、核心洞察

### 1. 角色重定义

| 传统角色 | → | Agent时代角色 |
|----------|---|--------------|
| 模型 = 文本生成器 | → | 模型 = 界面规划师 |
| 后端 = 数据提供者 | → | 后端 = 协议协调者 |
| 前端 = 页面渲染器 | → | 前端 = 协议执行引擎 |

### 2. 架构演进方向

```
第一阶段（预设卡片）：
模型能力不稳定 → 预定义卡片模板 → 保证内容可控

第二阶段（Agent生成）：
模型能力提升 → Agent自主组合UI → 千人多面

关键：平滑过渡，渲染器共用
```

### 3. 协议优先思维

> 四层协议体系的价值不在于技术有多先进，而在于为复杂系统建立了**确定性**——当每一层的输入输出都有明确约定，问题排查、能力复用、新业务接入的效率就会**指数级提升**。

---

## 六、LUI演进路线

### LUI (Language User Interface) 两阶段

```
┌─────────────────────────────────────────────────────────────┐
│                    LUI演进路线                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: 预设卡片 (现在)                                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Agent → 填数据 → 预设模板渲染                        │  │
│  │                                                    │  │
│  │ 优势：内容可控、体验一致                            │  │
│  │ 劣势：灵活性受限                                    │  │
│  └─────────────────────────────────────────────────────┘  │
│                           ↓                                 │
│  Phase 2: Agent生成 (未来)                                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Agent → 自主组合UI组件 → 动态渲染                   │  │
│  │                                                    │  │
│  │ 优势：千人多面、体验个性化                           │  │
│  │ 劣势：内容可控性挑战                                 │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 淘宝选择的路径

1. **短期**：代码块扩展 + 增量Patch
2. **中期**：MCP Apps Tool绑定
3. **长期**：A2UI + 动态UI生成

---

## 七、实践建议

### 给Agent开发者的建议

1. **协议先行**：在动手写代码前，先定义好四层协议的边界
2. **Tool为王**：把数据生产责任从模型转移到工具链
3. **渐进演进**：不要试图一步到位，先支持预设卡片再过渡到动态UI
4. **跨端一致**：用统一JSON Schema保证Web/iOS/Android体验一致

### 技术选型建议

| 场景 | 推荐方案 |
|------|----------|
| 快速验证 | 代码块扩展 + 模型直出 |
| 生产落地 | 代码块扩展 + 增量Patch |
| 多端复用 | A2UI JSON Schema |
| 工具整合 | MCP + MCP Apps |
| Agent协作 | A2A协议 |

---

## 八、参考资料

- [bolt.new](https://github.com/stackblitz/bolt.new)
- [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview)
- [A2UI Protocol](https://a2ui.org/)
- [CopilotKit A2UI](https://docs.copilotkit.ai/built-in-agent/generative-ui/a2ui)
- [react-markdown](https://remarkjs.github.io/react-markdown/)

---

## 相关Insight

- [[insight-20260417-harness-engineering]] - Harness工程核心概念
- [[insight-20260417-claude-code-agent-farm]] - Claude Code多Agent编排

---

*归档时间: 2026-04-22*
*归档人: 尼克·弗瑞*
