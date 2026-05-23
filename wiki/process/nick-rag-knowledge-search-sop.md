---
name: nick-rag-knowledge-search
description: >
  尼克·弗瑞知识检索SOP。在情报收集、文章处理、简报生成等场景中，
  使用knowledge_search进行RAG检索，避免重复劳动，实现知识复用。
  Use when: 执行情报任务前、生成分析报告前、处理用户分享的文章时。
metadata:
  openclaw:
    emoji: "🕵️"
---

# Nick RAG Knowledge Search SOP

> 版本: v1.0
> 创建: 2026-05-21
> 维护者: 尼克·弗瑞
> 状态: 已生效

---

## 一、概述

### 1.1 目的

本SOP定义尼克·弗瑞在情报工作流中如何使用RAG知识检索能力，实现：
- 避免重复收集已有知识
- 在已有知识基础上增量补充
- 提高情报产出质量和效率

### 1.2 能力定义

| 能力 | 说明 |
|:---|:---|
| **名称** | knowledge_search |
| **类型** | RAG混合检索 |
| **模型** | Chroma + Ollama bge-m3 |
| **模式** | 向量+BM25+RRF融合 |
| **API** | POST http://localhost:8082/search |

### 1.3 评分阈值

| 分数区间 | 含义 | 处理方式 |
|:---:|:---|:---|
| 0.8 - 1.0 | 高度相关 | 直接作为参考，核对是否需更新 |
| 0.6 - 0.8 | 中度相关 | 参考补充，确认差异 |
| 0.4 - 0.6 | 弱相关 | 仅参考，独立沉淀 |
| < 0.4 | 不相关 | 完全新知，新建文档 |

---

## 二、核心流程

### 2.1 情报工作流（集成RAG）

```
┌─────────────────────────────────────────────────────────────────┐
│                    情报工作流（v5.0 RAG增强版）                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  情报收集                                                        │
│     │                                                           │
│     ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Step 1: RSS/GitHub/Get笔记抓取                          │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Step 2: RAG知识检索（knowledge_search）                  │    │
│  │          • query: 主题关键词                             │    │
│  │          • top_k: 5                                     │    │
│  │          • mode: hybrid                                 │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Step 3: 认知核对                                        │    │
│  │          • 高度相关 → 已有知识，核对差异                  │    │
│  │          • 中度相关 → 参考补充，确认差异                  │    │
│  │          • 弱相关 → 仅参考，独立沉淀                      │    │
│  │          • 不相关 → 完全新知，新建文档                    │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Step 4: Wiki沉淀（带方法论Tag）                         │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Step 5: 情报分发                                        │    │
│  │          • ⭐⭐⭐⭐+ → 飞书即时推送                     │    │
│  │          • ⭐⭐⭐ → Wiki归档                            │    │
│  │          • ⭐⭐ → 暂存待观察                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、应用场景

### 3.1 场景1：文章处理（用户分享链接）

**触发条件**：用户发送微信公众号/文章链接

**流程**：

```
Step 1: 内容抓取
        ↓
Step 2: RAG检索
        ├── query: 文章主题关键词
        ├── top_k: 5
        ├── mode: hybrid
        ↓
Step 3: 认知核对
        │
        ├── score ≥ 0.8 → 高度相关
        │      ├── 动作：核对差异，更新现有文档
        │      └── 示例："该文章与现有insight-xxx重复，内容更全面"
        │
        ├── 0.6 ≤ score < 0.8 → 中度相关
        │      ├── 动作：参考补充，独立沉淀
        │      └── 示例："补充新角度到现有文档"
        │
        ├── 0.4 ≤ score < 0.6 → 弱相关
        │      ├── 动作：独立沉淀
        │      └── 示例："新视角，新建文档"
        │
        └── score < 0.4 → 不相关
               ├── 动作：完全新知，新建文档
               └── 示例："全新领域，建立新insight"
        ↓
Step 4: 打法论Tag
        ↓
Step 5: 价值评估 → 决策
```

**代码示例**：

```python
# 文章处理中的RAG调用
def process_article_with_rag(article_content, article_topic):
    # Step 1: 抓取内容（已做）
    content = fetch_article(article_url)
    
    # Step 2: RAG检索
    results = knowledge_search(
        query=article_topic,
        top_k=5,
        mode="hybrid"
    )
    
    # Step 3: 认知核对
    if results['total'] > 0:
        top_score = results['results'][0]['score']
        
        if top_score >= 0.8:
            # 高度相关：核对差异
            return {
                "decision": "UPDATE",
                "target": results['results'][0]['doc_path'],
                "action": "核对差异，更新现有文档"
            }
        elif top_score >= 0.6:
            # 中度相关：参考补充
            return {
                "decision": "APPEND",
                "target": results['results'][0]['doc_path'],
                "action": "补充新角度"
            }
        else:
            # 弱/不相关：独立沉淀
            return {
                "decision": "CREATE",
                "action": "新建文档"
            }
    else:
        # 无检索结果：完全新知
        return {"decision": "CREATE", "action": "新建文档"}
```

---

### 3.2 场景2：晨间简报生成

**触发条件**：每日08:30投资简报、08:35科技简报

**流程**：

```
Step 1: RSS抓取今日更新
        ↓
Step 2: RAG检索背景知识
        ├── query: "今日主题 + 历史简报"
        ├── top_k: 3
        ├── mode: hybrid
        ↓
Step 3: 结合背景知识生成简报
        ↓
Step 4: Wiki归档（避免重复）
```

**代码示例**：

```python
# 简报生成中的RAG调用
def generate_brief_with_rag(topic, today_updates):
    # Step 1: 抓取今日更新
    new_items = fetch_rss_updates(topic)
    
    # Step 2: RAG检索背景
    background = knowledge_search(
        query=f"{topic} 背景知识 历史简报",
        top_k=3,
        mode="hybrid"
    )
    
    # Step 3: 结合背景生成
    brief = generate_brief(
        topic=topic,
        new_items=new_items,
        background=background['results']
    )
    
    # Step 4: 检查是否重复
    if is_duplicate(brief, background):
        return {"status": "DUPLICATE", "action": "更新现有文档"}
    else:
        return {"status": "NEW", "action": "新建文档归档"}
```

---

### 3.3 场景3：最佳实践收集

**触发条件**：每日23:00最佳实践收集

**流程**：

```
Step 1: 确定收集主题
        ↓
Step 2: RAG检索已有收集
        ├── query: "主题 + 最佳实践"
        ├── top_k: 5
        ├── mode: hybrid
        ↓
Step 3: 判断
        │
        ├── score ≥ 0.8 → 已充分覆盖，跳过或更新
        ├── 0.6 ≤ score < 0.8 → 部分覆盖，补充新角度
        └── score < 0.6 → 未覆盖，进行收集
        ↓
Step 4: 收集并归档
```

**代码示例**：

```python
# 最佳实践收集中的RAG调用
def collect_best_practice_with_rag(topic):
    # Step 1: 确定主题
    search_topic = f"{topic} 最佳实践"
    
    # Step 2: RAG检索已有
    existing = knowledge_search(
        query=search_topic,
        top_k=5,
        mode="hybrid"
    )
    
    # Step 3: 判断是否已收集
    if existing['total'] > 0:
        top_score = existing['results'][0]['score']
        
        if top_score >= 0.8:
            # 已充分覆盖
            return {
                "action": "SKIP",
                "reason": f"已有充分覆盖（score={top_score:.2f}）",
                "existing_doc": existing['results'][0]['doc_path']
            }
        elif top_score >= 0.6:
            # 部分覆盖，补充
            return {
                "action": "COLLECT",
                "mode": "APPEND",
                "target": existing['results'][0]['doc_path']
            }
    
    # Step 4: 未覆盖或无结果，进行收集
    return {"action": "COLLECT", "mode": "CREATE"}
```

---

### 3.4 场景4：情报质量评估

**触发条件**：评估RSS文章价值

**流程**：

```
Step 1: RSS文章抓取
        ↓
Step 2: RAG检索相关已有知识
        ↓
Step 3: 评估
        │
        ├── score ≥ 0.8 → 重复，跳过
        ├── 0.6 ≤ score < 0.8 → 补充，更新
        └── score < 0.6 → 新知，深度处理
        ↓
Step 4: 打Tag归档
```

---

## 四、知识库分工

### 4.1 RAG检索范围

| 知识库 | 说明 | 检索方式 |
|:---|:---|:---|
| **Wiki insights** | 洞察文档 | RAG检索 |
| **Wiki methodologies** | 方法论文档 | RAG检索 |
| **Wiki process** | 流程SOP | RAG检索 |
| **文档仓库** | 行业研究报告 | RAG检索 |

### 4.2 沉淀位置

| 内容类型 | 沉淀位置 | Tag |
|:---|:---|:---|
| 洞察 | `wiki/insights/` | 方法论Tag |
| 方法论 | `wiki/methodologies/` | methodology |
| 流程 | `wiki/process/` | SOP |
| 行业研究 | `文档仓库/行业研究/` | product_domain |

---

## 五、异常处理

| 场景 | 处理方式 |
|:---|:---|
| **RAG服务不可用** | 降级为手动Wiki检索，标注"待RAG校验" |
| **检索超时** | 使用缓存结果，标注"数据可能非最新" |
| **无检索结果** | 按完全新知处理，新建文档 |
| **结果质量差** | 放宽阈值，重新检索 |

---

## 六、效果评估

### 6.1 指标

| 指标 | 说明 | 目标 |
|:---|:---|:---:|
| **检索覆盖率** | 需要检索的场景中实际调用的比例 | ≥90% |
| **重复检测率** | 识别出重复内容的比例 | ≥80% |
| **知识复用率** | 复用已有知识的产出比例 | ≥60% |

### 6.2 监控方式

```bash
# 每周检查检索日志
# 每月评估知识复用效果
# 每季度优化检索策略
```

---

## 七、相关文档

| 文档 | 位置 | 说明 |
|:---|:---|:---|
| **RAG知识检索SOP（正式版）** | `文档仓库/产品管理项目/架构规范/SOP/情报研究类/Nick-S13-RAG知识检索.md` | RAG可检索的正式SOP |
| 情报收集SOP | `SOP/情报研究类/Nick-S1-情报收集.md` | 情报收集流程 |
| 情报分析SOP | `SOP/情报研究类/Nick-S2-情报分析.md` | 情报分析流程 |

## 八、更新记录

| 日期 | 版本 | 更新内容 |
|:---|:---:|:---|
| 2026-05-21 | v1.0 | 初始版本，定义4个核心场景SOP |
| 2026-05-21 | v1.1 | 增加正式SOP路径引用 |

---

*版本: v1.0*
*日期: 2026-05-21*
*维护者: 尼克·弗瑞 🕵️*
