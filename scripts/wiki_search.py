#!/usr/bin/env python3
"""
Nick Wiki 简单搜索脚本
基于关键词和简单匹配

功能：
- 搜索Wiki页面标题和内容
- 按文件修改时间排序
- 高亮关键词
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# 配置
WIKI_ROOT = Path("/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/Nick_Wiki/wiki")
SEARCH_IN = ["title", "content"]  # 搜索范围


def search_in_file(filepath: Path, keyword: str) -> Dict:
    """在单个文件中搜索"""
    try:
        content = filepath.read_text(encoding='utf-8')
        title = filepath.stem
        
        # 简单匹配
        keyword_lower = keyword.lower()
        content_lower = content.lower()
        
        # 检查是否匹配
        if keyword_lower not in content_lower and keyword_lower not in title.lower():
            return None
        
        # 提取摘要
        lines = content.split('\n')
        summary_lines = []
        in_content = False
        
        for line in lines:
            if line.startswith('## ') or line.startswith('# '):
                in_content = True
            if in_content and len(summary_lines) < 3:
                if keyword_lower in line.lower():
                    summary_lines.append(f"  → {line.strip()[:80]}")
        
        # 获取元信息
        created = "unknown"
        updated = datetime.fromtimestamp(filepath.stat().st_mtime).strftime("%Y-%m-%d")
        
        for line in lines[:20]:
            if '创建时间' in line or 'created' in line.lower():
                match = re.search(r'\d{4}-\d{2}-\d{2}', line)
                if match:
                    created = match.group()
        
        return {
            "title": title,
            "path": str(filepath.relative_to(WIKI_ROOT)),
            "match_count": content_lower.count(keyword_lower),
            "created": created,
            "updated": updated,
            "summary": summary_lines[:2] if summary_lines else ["无匹配摘要"]
        }
    except Exception as e:
        return None


def search_wiki(keyword: str, max_results: int = 10) -> List[Dict]:
    """搜索Wiki"""
    results = []
    
    # 遍历所有md文件
    for md_file in WIKI_ROOT.rglob("*.md"):
        # 跳过index和log
        if md_file.name in ['index.md', 'log.md', 'NICK_SCHEMA.md']:
            continue
        
        result = search_in_file(md_file, keyword)
        if result:
            results.append(result)
    
    # 按匹配次数排序
    results.sort(key=lambda x: -x['match_count'])
    
    return results[:max_results]


def main():
    if len(sys.argv) < 2:
        print("用法: python wiki_search.py <关键词>")
        print("示例: python wiki_search.py agent")
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    print(f"\n🔍 搜索 Wiki: '{keyword}'")
    print("=" * 60)
    
    results = search_wiki(keyword)
    
    if not results:
        print(f"未找到匹配 '{keyword}' 的页面")
        return
    
    print(f"找到 {len(results)} 个匹配:\n")
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   路径: {r['path']}")
        print(f"   匹配次数: {r['match_count']}")
        print(f"   更新: {r['updated']}")
        for s in r['summary']:
            print(s)
        print()


if __name__ == "__main__":
    main()
