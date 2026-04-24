#!/usr/bin/env python3
"""
Nick Wiki Topic Ingest脚本
基于Karpathy LLM Wiki模式

功能：
1. 分析新信息内容
2. 判断属于哪个Topic
3. 执行增量更新
4. 记录到log.md
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# 配置
WIKI_ROOT = Path("/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/Nick_Wiki")
TOPICS_DIR = WIKI_ROOT / "wiki" / "topics"
ENTITIES_DIR = WIKI_ROOT / "wiki" / "entities"
LOG_FILE = WIKI_ROOT / "wiki" / "log.md"
INDEX_FILE = WIKI_ROOT / "wiki" / "index.md"

# Topic分类配置
TOPIC_CLASSIFIER = {
    "data-platform": {
        "keywords": ["数据中台", "数仓", "ETL", "数据治理", "Lambda", "Kappa", "Doris", "Flink", "Spark", "Hive", "OneData", "数据平台"],
        "files": ["data-platform.md", "data-platform"]
    },
    "risk-management": {
        "keywords": ["风控", "反欺诈", "信用评估", "风控系统", "欺诈", "决策引擎", "规则引擎", "核身"],
        "files": ["risk-management.md"]
    },
    "intelligent-systems": {
        "keywords": ["智能客服", "智能信贷", "支付", " chatbot", "对话", "问答", "客服"],
        "files": ["intelligent-systems.md"]
    },
    "marketing-suite": {
        "keywords": ["营销", "增长", "A/B测试", "用户运营", "精准营销", "CRM", "营销套件"],
        "files": ["marketing-suite.md"]
    },
    "infrastructure": {
        "keywords": ["云原生", "K8s", "Kubernetes", "Docker", "DevOps", "微服务", "分布式", "容器"],
        "files": ["infrastructure.md"]
    },
    "compliance": {
        "keywords": ["合规", "监管", "AML", "KYC", "反洗钱", "合规检查", "监管科技"],
        "files": ["compliance.md"]
    },
    "open-banking": {
        "keywords": ["开放银行", "API Bank", "Open API", "生态", "场景金融"],
        "files": ["open-banking.md"]
    },
    "llm-finance": {
        "keywords": ["LLM", "大模型", "RAG", "Agent", "GPT", "LLM金融", "生成式AI"],
        "files": ["llm-finance.md"]
    },
    "tech-ai": {
        "keywords": ["AI", "人工智能", "LLM", "GPT", "Agent", "深度学习", "神经网络", "ChatGPT", "Claude"],
        "files": ["../tech-ai.md"]
    }
}


def classify_topic(content: str) -> Optional[str]:
    """根据内容分类到Topic"""
    content_lower = content.lower()
    
    scores = {}
    for topic, config in TOPIC_CLASSIFIER.items():
        score = 0
        for keyword in config["keywords"]:
            if keyword.lower() in content_lower:
                score += 1
        if score > 0:
            scores[topic] = score
    
    if not scores:
        return None
    
    return max(scores, key=scores.get)


def extract_entities(content: str) -> List[str]:
    """从内容中提取公司/实体名称"""
    # 简单实现：匹配常见公司名
    companies = [
        "蚂蚁集团", "支付宝", "阿里巴巴", "阿里云",
        "腾讯", "微信支付", "微众银行",
        "字节跳动", "抖音", "TikTok",
        "百度", "度小满",
        "招商银行", "招联金融",
        "马上消费金融", "马上消费",
        "工商银行", "建设银行", "中国银行", "农业银行",
        "京东", "京东金融", "美团", "滴滴",
        "网易", "新浪", "搜狐",
        "NVIDIA", "英伟达", "OpenAI", "Anthropic", "Google", "Meta"
    ]
    
    found = []
    for company in companies:
        if company in content:
            found.append(company)
    
    return found


def update_topic(topic_key: str, title: str, content: str, source: str) -> bool:
    """更新Topic文件"""
    config = TOPIC_CLASSIFIER.get(topic_key)
    if not config:
        print(f"未找到Topic: {topic_key}")
        return False
    
    topic_file = TOPICS_DIR / topic_key / f"{topic_key}.md"
    
    # 如果是tech-ai，需要回到wiki目录
    if ".." in config["files"][0]:
        topic_file = WIKI_ROOT / "wiki" / config["files"][0]
    
    if not topic_file.exists():
        print(f"Topic文件不存在: {topic_file}")
        return False
    
    # 读取现有内容
    existing = topic_file.read_text()
    
    # 检查是否已存在该案例
    if title in existing:
        print(f"案例已存在: {title}")
        return False
    
    # 提取实体
    entities = extract_entities(content)
    entity_links = ", ".join([f"[[{e}]]" for e in entities])
    
    # 准备新案例
    new_case = f"""

---

### {title}

{content}

**来源**: {source}
**实体**: {entity_links}
**更新时间**: {datetime.now().strftime('%Y-%m-%d')}

"""
    
    # 添加到文件
    updated = existing + new_case
    topic_file.write_text(updated)
    
    return True


def log_update(topic_key: str, title: str, source: str) -> None:
    """记录到log.md"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    entry = f"""

## [{today}] ingest | {title}
- **Topic**: {topic_key}
- **操作**: 新增案例
- **来源**: {source}
"""
    
    with open(LOG_FILE, 'a') as f:
        f.write(entry)


def main():
    if len(sys.argv) < 3:
        print("用法: python topic_ingest.py <标题> <内容文件> <来源>")
        print("示例: python topic_ingest.py '案例标题' content.txt 'RSS/手动输入'")
        sys.exit(1)
    
    title = sys.argv[1]
    content_file = Path(sys.argv[2])
    source = sys.argv[3] if len(sys.argv) > 3 else "手动输入"
    
    # 读取内容
    if content_file.exists():
        content = content_file.read_text()
    else:
        content = sys.argv[2]  # 直接传入内容
    
    print(f"\n🔍 分析: {title}")
    print(f"   来源: {source}")
    
    # 分类
    topic = classify_topic(content)
    if not topic:
        print("   ⚠️ 未匹配到Topic，归档到待定")
        topic = "undetermined"
    else:
        print(f"   ✅ 匹配Topic: {topic}")
    
    # 提取实体
    entities = extract_entities(content)
    if entities:
        print(f"   🏢 实体: {', '.join(entities)}")
    
    # 更新
    if topic != "undetermined":
        success = update_topic(topic, title, content, source)
        if success:
            print(f"   ✅ Topic更新成功")
            log_update(topic, title, source)
        else:
            print(f"   ⚠️ Topic更新失败或案例已存在")
    else:
        print(f"   📋 归档到待定")


if __name__ == "__main__":
    main()
