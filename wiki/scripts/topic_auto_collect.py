#!/usr/bin/env python3
"""
Topic自动收集系统 v1.0
RSS采集 + 自动分类 + 入库决策

作者: 尼克·弗瑞
日期: 2026-04-21
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional

# 配置文件路径
P0_RSS_CONFIG = "/Users/wenbo/.openclaw/workspace/agents/nick_fury/data/p0_rss_sources.json"
MONITORING_CONFIG = "/Users/wenbo/Documents/project/Wiki/wiki/process/topic-monitoring-config.md"

class TopicAutoCollector:
    """Topic自动收集器"""
    
    def __init__(self):
        self.p0_sources = self._load_p0_sources()
        self.state = self._load_state()
    
    def _load_p0_sources(self) -> Dict:
        """加载P0级RSS源配置"""
        if os.path.exists(P0_RSS_CONFIG):
            with open(P0_RSS_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_state(self) -> Dict:
        """加载采集状态"""
        state_path = os.path.expanduser(
            "~/.openclaw/workspace/agents/nick_fury/data/auto_collect_state.json"
        )
        if os.path.exists(state_path):
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "last_run": None,
            "processed_count": 0,
            "auto_imported": 0,
            "pending_review": 0
        }
    
    def _save_state(self):
        """保存采集状态"""
        state_path = os.path.expanduser(
            "~/.openclaw/workspace/agents/nick_fury/data/auto_collect_state.json"
        )
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def get_all_feeds(self) -> List[Dict]:
        """获取所有RSS源列表"""
        feeds = []
        
        if "sources" in self.p0_sources:
            for category, sources in self.p0_sources["sources"].items():
                for source in sources:
                    feeds.append({
                        "name": source["name"],
                        "url": source["url"],
                        "category": source["category"],
                        "priority": source["priority"],
                        "type": category
                    })
        
        return feeds
    
    def auto_classify(self, title: str, content: str) -> Dict:
        """
        自动分类文章
        返回: {"topic": str, "sub_topic": str, "confidence": float}
        """
        # Topic关键词匹配规则
        rules = {
            "ai_native": {
                "keywords": ["AI Agent", "LLM", "大模型", "Vibe Coding", "Multi-Agent", 
                           "Skill", "RAG", "Claude Code", "Cursor", "LangChain", 
                           "CrewAI", "AutoGen", "Agent", "Harness", "Prompt"],
                "sub_topics": {
                    "ai_programming": ["Vibe Coding", "Cursor", "Windsurf", "IDE", "代码生成"],
                    "agent_engineering": ["Multi-Agent", "CrewAI", "AutoGen", "LangChain", "Memory", "Tool Use"],
                    "skill_evaluation": ["Skill", "评分", "自动评估", "Benchmark"]
                }
            },
            "fintech": {
                "keywords": ["数字银行", "智能风控", "消费金融", "数字人民币", 
                           "金融科技", "信贷", "反欺诈", "风控", "银行", "支付"],
                "sub_topics": {
                    "consumer_finance": ["消费金融", "现金贷", "助贷", "信用卡"],
                    "risk_management": ["风控", "反欺诈", "智能风控", "风险"],
                    "payment": ["数字人民币", "支付", "CBDC", "跨境支付"]
                }
            }
        }
        
        text = (title + " " + content).lower()
        scores = {}
        
        for topic, config in rules.items():
            score = 0
            matched_keywords = []
            
            for keyword in config["keywords"]:
                if keyword.lower() in text:
                    score += 1
                    matched_keywords.append(keyword)
            
            # 子专题匹配
            sub_topic = None
            for sub_name, sub_keywords in config.get("sub_topics", {}).items():
                sub_score = sum(1 for k in sub_keywords if k.lower() in text)
                if sub_score > 0 and (sub_topic is None or sub_score > sub_topic["score"]):
                    sub_topic = {"name": sub_name, "score": sub_score}
            
            scores[topic] = {
                "score": score,
                "keywords": matched_keywords,
                "sub_topic": sub_topic["name"] if sub_topic else None
            }
        
        # 选择得分最高的Topic
        best_topic = max(scores.items(), key=lambda x: x[1]["score"])
        
        if best_topic[1]["score"] > 0:
            confidence = min(best_topic[1]["score"] / 3, 1.0)  # 3个关键词 = 100%置信度
            return {
                "topic": best_topic[0],
                "sub_topic": best_topic[1]["sub_topic"],
                "confidence": confidence,
                "matched_keywords": best_topic[1]["keywords"]
            }
        
        return {"topic": "general", "sub_topic": None, "confidence": 0.0}
    
    def score_content(self, title: str, content: str, source: str) -> Dict:
        """
        评分内容质量 (1-5星)
        返回: {"score": int, "reason": str, "action": str}
        """
        score = 0
        reasons = []
        
        # 1. 来源权威性 (+1-2星)
        high_authority = ["Anthropic", "OpenAI", "Cursor", "Microsoft", "LangChain"]
        medium_authority = ["GitHub", "Vercel", "TechCrunch", "MIT"]
        
        if any(s in source for s in high_authority):
            score += 2
            reasons.append("高权威来源")
        elif any(s in source for s in medium_authority):
            score += 1
            reasons.append("中等权威来源")
        
        # 2. 内容深度 (+1星)
        if len(content) > 2000:
            score += 1
            reasons.append("深度内容(>2000字)")
        
        # 3. 技术价值 (+1星)
        tech_keywords = ["架构", "实践", "案例", "方案", "开源", "代码", "GitHub"]
        if any(k in content for k in tech_keywords):
            score += 1
            reasons.append("技术/实践价值")
        
        # 4. 时效性 (+1星)
        if any(k in content for k in ["2025", "2026", "最新", "新发布"]):
            score += 1
            reasons.append("高时效性")
        
        # 评分结果映射到行动
        actions = {
            5: {"action": "auto_import", "notify": "immediate"},
            4: {"action": "auto_import", "notify": "daily"},
            3: {"action": "pending_review", "notify": "batch"},
            2: {"action": "pending_review", "notify": "weekly"},
            1: {"action": "discard", "notify": "none"}
        }
        
        return {
            "score": min(score, 5),
            "reason": "; ".join(reasons),
            **actions.get(score, {"action": "discard", "notify": "none"})
        }
    
    def generate_summary(self) -> str:
        """生成配置摘要"""
        feeds = self.get_all_feeds()
        
        ai_native = [f for f in feeds if f["type"] == "ai_native"]
        fintech = [f for f in feeds if f["type"] == "fintech"]
        
        summary = f"""# Topic自动收集系统摘要

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 📊 RSS源配置

| 类别 | 数量 | 优先级 |
|:---|:---:|:---:|
| AI-Native | {len(ai_native)} | P0 |
| Fintech | {len(fintech)} | P0 |
| **总计** | **{len(feeds)}** | - |

### AI-Native源
"""
        for feed in ai_native:
            summary += f"- {feed['name']} ({feed['category']})\n"
        
        summary += "\n### Fintech源\n"
        for feed in fintech:
            summary += f"- {feed['name']} ({feed['category']})\n"
        
        summary += """
## ⚙️ 自动化规则

### 入库标准
| 评分 | 处理方式 | 通知方式 |
|:---:|:---|:---|
| ★★★★★ | 自动入库 | 立即通知 |
| ★★★★ | 自动入库 | 每日汇总 |
| ★★★ | 待审核队列 | 批量通知 |
| ★★ | 暂存观察 | 每周清理 |
| ★ | 直接丢弃 | 不通知 |

### 分类规则
- AI-Native: Agent, LLM, Vibe Coding, Skill等关键词
- Fintech: 数字银行, 风控, 支付, 信贷等关键词

---
*由尼克·弗瑞自动维护*
"""
        
        return summary

if __name__ == "__main__":
    collector = TopicAutoCollector()
    
    # 生成配置摘要
    summary = collector.generate_summary()
    
    # 保存到文件
    summary_path = "/Users/wenbo/.openclaw/workspace/agents/nick_fury/data/auto_collect_summary.md"
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(summary)
    print(f"\n✅ 摘要已保存: {summary_path}")
