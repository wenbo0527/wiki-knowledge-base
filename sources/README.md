# 📚 Sources 目录说明

> 原始资料库 - Wiki的知识来源

---

## 目录结构

```
sources/
├── rss/                    # RSS情报
│   ├── articles/           # 🆕 797篇文章归档
│   │   ├── 钛媒体/         # 56篇
│   │   ├── 雷峰网/         # 42篇
│   │   ├── 人人都是产品经理/ # 39篇
│   │   ├── Lilian_Weng/    # 51篇
│   │   ├── simonwillison.net/ # 44篇
│   │   └── ...             # 其他来源
│   ├── daily/             # 每日简报
│   ├── weekly/            # 每周汇总
│   ├── intelligence.json  # RSS原始数据(3.7MB)
│   └── analysis_v2.json   # 分析数据
│
├── etf/                    # ETF数据
│   ├── records/           # CSV历史数据
│   ├── *.json            # ETF历史
│   └── *.md              # 分析报告
│
├── best_practices/         # 最佳实践收集
│   ├── 01_核心领域_第一轮/  # 15个Day
│   ├── 02_新兴领域_2026年/  # 6个领域
│   ├── 03_深度专题_待收集/  # 8个专题
│   ├── 04_交叉分析/        # 跨领域分析
│   └── 05_更新方向/        # 规划文档
│
└── references/            # 参考资料
```

## 数据统计

| 来源 | 数量 | 说明 |
|------|------|------|
| RSS文章 | 797篇 | 来自20+个来源 |
| 每日简报 | 1+ | 待持续补充 |
| ETF数据 | 多份 | CSV+JSON+MD |
| 最佳实践 | 15+Day | 结构化研究 |

## 来源详情

### RSS来源 (按数量排序)

| 来源 | 数量 | 类型 |
|------|------|------|
| antirez.com | 101 | 技术博客 |
| utcc.utoronto.ca | 100 | 技术博客 |
| daringfireball.net | 72 | 技术博客 |
| ericmigi.com | 61 | 技术博客 |
| 钛媒体 | 56 | 中文科技 |
| Lilian Weng | 51 | AI研究 |
| mitchellh.com | 47 | 技术博客 |
| simonwillison.net | 44 | AI/数据 |
| 雷峰网 | 42 | 中文科技 |
| 人人都是产品经理 | 39 | 产品经理 |

## 使用方式

### Ingest流程

1. **新简报** → 保存到 `rss/daily/YYYY-MM-DD.md`
2. **新文章** → 保存到 `rss/articles/{来源}/`
3. **触发Ingest** → LLM读取并更新Wiki

### 查询流程

1. 读取 `index.md` 找到相关来源
2. 访问 `rss/articles/` 查找原始文章
3. 综合生成回答

---

*最后更新: 2026-04-08*
*维护者: 尼克·弗瑞*