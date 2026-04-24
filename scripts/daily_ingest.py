#!/usr/bin/env python3
"""
Nick Wiki 每日Ingest脚本
基于Karpathy LLM Wiki模式

功能：
1. 读取每日RSS简报
2. 保存到sources/rss/daily/
3. 生成LLM处理指令
4. 更新log.md
"""

import os
import json
import datetime
from pathlib import Path
from typing import Optional

# 配置
WIKI_ROOT = Path("/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/Nick_Wiki")
SOURCES_ROOT = WIKI_ROOT / "sources"
RSS_SOURCE = Path("/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/01_情报分析/rss_intelligence/daily_briefs")
LOG_FILE = WIKI_ROOT / "wiki" / "log.md"
INDEX_FILE = WIKI_ROOT / "wiki" / "index.md"

def get_today_str() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")

def get_yesterday_str() -> str:
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def ingest_daily_brief(date_str: Optional[str] = None) -> dict:
    """
    Ingest每日简报到Wiki sources
    
    Returns:
        dict: 包含ingest结果
    """
    if date_str is None:
        date_str = get_yesterday_str()
    
    source_file = RSS_SOURCE / f"{date_str}.md"
    target_file = SOURCES_ROOT / "rss" / "daily" / f"{date_str}.md"
    
    result = {
        "date": date_str,
        "source": str(source_file),
        "target": str(target_file),
        "success": False,
        "pages_updated": [],
        "error": None
    }
    
    # 1. 检查源文件是否存在
    if not source_file.exists():
        # 尝试查找最新文件
        existing = list(RSS_SOURCE.glob("*.md"))
        if existing:
            latest = max(existing, key=lambda p: p.stat().st_mtime)
            source_file = latest
            date_str = latest.stem
            target_file = SOURCES_ROOT / "rss" / "daily" / f"{date_str}.md"
            result["date"] = date_str
            result["source"] = str(source_file)
            result["target"] = str(target_file)
        else:
            result["error"] = f"源文件不存在: {source_file}"
            return result
    
    # 2. 确保目标目录存在
    target_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 3. 复制文件到sources
    try:
        content = source_file.read_text()
        target_file.write_text(content)
        result["success"] = True
    except Exception as e:
        result["error"] = f"复制失败: {str(e)}"
        return result
    
    # 4. 读取内容，提取关键信息
    result["pages_updated"] = extract_key_entities(content)
    
    return result

def extract_key_entities(content: str) -> list:
    """
    从内容中提取关键实体
    
    Returns:
        list: 实体列表（需要更新的页面）
    """
    # 这里应该调用LLM来提取
    # 目前简单基于关键词
    entities = []
    
    keywords = {
        "nvidia": "nvidia.md",
        "openai": "openai.md", 
        "apple": "apple.md",
        "nvidia": "entities/companies/nvidia.md",
    }
    
    content_lower = content.lower()
    for keyword, page in keywords.items():
        if keyword in content_lower and page not in entities:
            entities.append(page)
    
    return entities

def update_log(date_str: str, result: dict) -> None:
    """更新log.md"""
    if not LOG_FILE.exists():
        LOG_FILE.write_text("# 📋 Nick Wiki 操作日志\n\n---\n\n")
    
    log_entry = f"""## [{date_str}] ingest | RSS Daily {date_str}
- 操作：Ingest每日简报到sources/
- 涉及页面：{', '.join(result['pages_updated']) if result['pages_updated'] else 'index.md'}
- 摘要：{'简报已Ingest，相关实体待更新' if result['success'] else f"失败: {result['error']}"}
"""
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)

def generate_ingest_prompt(date_str: str, result: dict) -> str:
    """生成LLM Ingest指令"""
    
    prompt = f"""
## Ingest任务

请处理今日Ingest的RSS简报：

**日期**: {date_str}
**源文件**: {result['target']}

**任务**:
1. 阅读源文件内容
2. 识别关键实体（公司、人物、技术）
3. 更新相关实体页（如有新技术/公司）
4. 更新主题页（如有行业趋势）
5. 生成洞察摘要（存入insights/）
6. 更新 index.md（如有新页面）

**当前Wiki结构**:
- entities/companies/ - 公司实体
- entities/markets/ - 市场实体
- entities/people/ - 人物实体
- concepts/ - 概念页
- topics/ - 主题页
- insights/ - 洞察页

**格式要求**:
- 每个页面包含 created/updated 元数据
- 使用 [[pagename]] 双向链接
- 引用使用 [source] 标注

请开始处理。
"""
    return prompt

def main():
    """主函数"""
    print("🚀 Nick Wiki 每日Ingest")
    print("=" * 50)
    
    # 执行Ingest
    result = ingest_daily_brief()
    
    if result["success"]:
        print(f"✅ Ingest成功: {result['date']}")
        print(f"📁 目标: {result['target']}")
        print(f"📄 可能需要更新的页面: {result['pages_updated']}")
        
        # 生成LLM指令
        prompt = generate_ingest_prompt(result['date'], result)
        print("\n" + "=" * 50)
        print("📝 LLM Ingest指令:")
        print("=" * 50)
        print(prompt)
        
        # 保存prompt到临时文件
        prompt_file = WIKI_ROOT / f"ingest_prompt_{result['date']}.txt"
        prompt_file.write_text(prompt)
        print(f"\n💾 指令已保存到: {prompt_file}")
        
    else:
        print(f"❌ Ingest失败: {result['error']}")
    
    return result

if __name__ == "__main__":
    main()
