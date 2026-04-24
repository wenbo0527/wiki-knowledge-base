# Wiki Sources 说明

> 本目录用于存放已消化但尚未归类到正式 Wiki 层级的参考资料

---

## ⚠️ 重要说明

**源数据实际存储位置**：`/Users/wenbo/Documents/project/Wiki/sources/`

本目录（`wiki/sources/`）是**过渡目录**，用于存放：
- 已消化但未归类的参考资料
- 临时缓存的原始文档
- 等待整理的笔记

---

## 源数据存储结构

```
/Users/wenbo/Documents/project/Wiki/sources/
├── best_practices/              # 最佳实践收集
│   ├── 01_核心领域_第一轮/     # Day01-Day15
│   ├── 02_新兴领域_2026年/     # 新兴领域专题
│   └── 03_深度专题_待收集/    # Round3 Day16-22
│
├── references/                  # 参考资料
│   ├── agentic_ai_aws.md
│   ├── ai项目周刊_20260409.md
│   ├── openclaw案例分享.md
│   └── wechat_article2.md
│
└── rss/                        # RSS原始数据
    ├── articles/               # 按来源分类的文章
    ├── daily/                  # 每日简报
    └── intelligence.json       # 情报汇总
```

---

## 使用说明

1. **Ingest 流程**：从 `sources/` 读取原始资料 → 消化 → 输出到 `wiki/insights/` 或 `wiki/topics/`
2. **搜索**：使用 `scripts/wiki_search.py` 搜索 `sources/` 中的原始数据
3. **整理**：定期将 `wiki/sources/` 中的过渡文件归类到正式位置

---

*维护者：尼克·弗瑞*
*最后更新：2026-04-16*
