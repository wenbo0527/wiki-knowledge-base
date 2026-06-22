# Wiki Knowledge Base

> 智能 Wiki 知识库 · 尼克·弗瑞出品

[![Python](https://img.shields.io/badge/Python-3.12-3776AB)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## 📌 这是什么

为 OpenClaw Agent Team 16 个 agent 协作服务的**智能 Wiki 知识库**：

- **智能搜索**：基于语义 + 关键词的混合检索
- **全文索引**：毫秒级查询 10000+ 文档
- **自动摘要**：AI 提炼文档核心
- **跨 wiki 联邦**：订阅外部 Wiki 合并查询

## 🏗️ 技术栈

- **Python 3.12** · FastAPI · uvicorn
- **PostgreSQL** + pgvector（向量检索）
- **BM25** 关键词检索（轻量 fallback）
- **LangChain** 文档处理

## 📂 目录结构

```
wiki-knowledge-base/
├── src/
│   ├── api/                # FastAPI 路由
│   ├── core/               # 核心业务逻辑
│   ├── db/                 # 数据库模型
│   ├── search/             # 检索引擎
│   └── llm/                # LLM 调用封装
├── tests/
├── scripts/
├── docs/
└── data/                   # 索引数据
```

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 PG
cp .env.example .env
# 填入 DATABASE_URL

# 3. 启动
uvicorn src.api.main:app --reload --port 8080

# 4. 访问 http://localhost:8080/docs
```

---

👤 **文博** · [GitHub](https://github.com/wenbo0527)