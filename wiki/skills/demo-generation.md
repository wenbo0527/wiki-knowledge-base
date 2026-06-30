# Demo Generation - 人类浏览版

> **机器版**：`~/.openclaw/skills/demo-generation/SKILL.md`
> **归属 Agent**：钟离（诊断流程主 Agent）
> **沉淀来源**：火匠（Smith）能力迁移 + 4 个 Python 模板
> **创建日期**：2026-06-11
> **触发场景**：诊断流程中给业务方展示 AI 能力概念验证

---

## 这是什么？

钟离诊断流程的第 4 步专用 Skill：**根据诊断结论，快速生成可运行的 Demo 样例**。支持 4 类场景：

| scene_type | 框架 | 适用 |
|:--|:--|:--|
| `dialogue` | Gradio + OpenAI API | 客服/问答/咨询 |
| `recommendation` | Streamlit + sklearn | 商品/内容推荐 |
| `classification` | Gradio + transformers | 文本分类/情感分析 |
| `detection` | FastAPI + YOLO | 图像检测/目标识别 |

## 关键设计

### 4 层架构（按你给的范例）

```
demo-generation/
├── SKILL.md                      ← YAML + 5步执行 + 约束
├── references/                   ← 知识判断标准
│   ├── ai_readiness_criteria.md  ← AI 就绪度判断（4维度 + 阈值）
│   └── tech_stack_mapping.md     ← 技术栈 → 框架映射
├── assets/                       ← 真实可运行的模板
│   ├── gradio_chat_template.py   ← 对话类
│   ├── streamlit_rec_template.py ← 推荐类
│   ├── gradio_cls_template.py    ← 分类类
│   ├── fastapi_detect_template.py← 检测类
│   └── requirements.txt          ← 依赖清单
└── scripts/
    └── validate_demo.py          ← 可运行性校验脚本
```

### 触发条件（必须满足）

- ✅ 诊断结论为"适合AI"，置信度 ≥ 0.6
- ✅ 业务方给出明确的 `scene_type`
- ✅ PM / 业务方有 1-2 句业务背景

### 边界（任一即停）

- ❌ 诊断结论为"不适合AI"
- ❌ 需要生产级代码（>200 行）
- ❌ 需要完整系统设计（→ `roadmap-planning`）
- ❌ 置信度 < 0.6

### 5 步执行

| 步骤 | 动作 | 关键产物 |
|:--|:--|:--|
| Step 1 | 确认输入 | `scene_type` + `business_context` + `tech_stack` + `diagnosis_conclusion` |
| Step 2 | 匹配模板 | 4 类模板之一 |
| Step 3 | 填充模板 | 占位符替换（{{BUSINESS_NAME}} 等） |
| Step 4 | 校验可运行性 | `validate_demo.py` 输出 |
| Step 5 | 输出 | 业务方直接拿的"代码 + 部署 + 效果预估" |

## 渐进式披露（核心优势）

```
会话启动：~100 token（仅元数据）
   ↓ 模型判断"需要生成 Demo"
触发 Skill：~3000 token（SKILL.md 正文）
   ↓ 执行 Step 2-4
按需加载：references/ + assets/ + scripts/
```

**对比原火匠 SOUL.md**：每次加载 ~800 token，不管用不用。Skill 化后**不触发只占 100 token**。

## validate_demo.py 真校验脚本

```bash
python3 ~/.openclaw/skills/demo-generation/scripts/validate_demo.py <demo_file>
```

校验 5 项：
1. ✅ 语法（AST 解析）
2. ✅ 入口函数（main / __main__）
3. ✅ 依赖声明（gradio/streamlit/fastapi → requirements.txt）
4. ✅ 代码量（≤200 行）
5. ✅ 占位符残留检查（{{XXX}}）

**实际跑测试**（2026-06-11 16:00）：
- 4 个模板全部成功检测出占位符未替换 = 模板本质 = 校验脚本有效

## 与其他 Skill 的边界

| 场景 | 用哪个 Skill |
|:--|:--|
| 业务方要看 AI 概念验证 | **`demo-generation`**（本 Skill） |
| 数字社区 PM 演示功能原型 | `quick-demo-sample`（待建） |
| 数字社区 dev 写生产代码 | `digital-community-dev-workflow`（已建） |

## 沉淀记录

| 日期 | 变更 | 变更人 |
|:--|:--|:--|
| 2026-06-11 | 初版（按方案 B Skill 化迁移，1:1 复刻范例结构） | 派蒙 |
| 2026-06-11 | 文博指正：原 `demo-full-generation` 逻辑缺失 + 场景错（不在我们 OpenClaw），重写为真逻辑版 | 派蒙复盘 |