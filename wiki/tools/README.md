# Tools - 尼克·弗瑞工具原型集合

> 🕵️ 尼克·弗瑞情报工具集
> 📅 创建时间: 2026-04-30
> 🎯 定位: 展示AI Agent能力边界，供组合参考

---

## 目录结构

```
tools/
├── README.md                    ← 本文件
├── rss-intelligence/            ← RSS情报收集工具
│   └── rss_fetcher.py
├── wiki-maintenance/            ← Wiki健康检查工具
│   └── wiki_lint.py
└── source-evaluation/           ← 信息源评估工具
    └── source_evaluator.py
```

---

## 工具清单

| 工具 | 功能 | 状态 |
|------|------|------|
| **rss_fetcher.py** | RSS源抓取与去重 | ✅ 稳定 |
| **wiki_lint.py** | Wiki链接健康检查 | ✅ 稳定 |
| **source_evaluator.py** | 信息源质量评估 | ✅ 稳定 |

---

## 核心理念

> **"工具原型 > 纯文档"** - 展示能力边界

每个工具应该：
1. **可运行** - 有完整的依赖声明
2. **有输出** - 展示实际运行效果
3. **可组合** - 易于作为其他工具的输入

---

*维护者: 尼克·弗瑞*
*最后更新: 2026-04-30*
