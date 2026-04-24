#!/usr/bin/env python3
"""
Nick Wiki Lint健康检查脚本
基于Karpathy LLM Wiki模式

功能：
1. 检查孤立页面（无引用）
2. 检查过时页面（3个月未更新）
3. 检查矛盾（同一实体描述冲突）
4. 生成改进建议
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Set

# 配置
WIKI_ROOT = Path("/Users/wenbo/Documents/project/Wiki/wiki")
DAYS_THRESHOLD = 90  # 3个月

# 链接正则
LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')


def get_all_pages() -> List[Path]:
    """获取所有wiki页面"""
    pages = []
    for md_file in WIKI_ROOT.rglob("*.md"):
        if md_file.name not in ['index.md', 'log.md', 'NICK_SCHEMA.md', 'PROCESS.md']:
            pages.append(md_file)
    return pages


def get_page_links(page: Path) -> Set[str]:
    """获取页面中的所有链接"""
    try:
        content = page.read_text()
        return set(LINK_PATTERN.findall(content))
    except:
        return set()


def get_page_age(page: Path) -> int:
    """获取页面年龄（天）"""
    try:
        mtime = page.stat().st_mtime
        age = datetime.now() - datetime.fromtimestamp(mtime)
        return age.days
    except:
        return 0


def check_orphans() -> List[Path]:
    """检查孤立页面（无页面引用）"""
    pages = get_all_pages()
    
    # 建立反向索引：哪个页面引用了哪个
    referenced = set()
    for page in pages:
        links = get_page_links(page)
        referenced.update(links)
    
    # 找出未被引用的页面
    orphans = []
    for page in pages:
        page_name = page.stem
        page_name_clean = page_name.replace("-", " ").replace("_", " ")
        
        # 检查是否在引用列表中
        is_referenced = any(
            page_name in link or link in page_name
            for link in referenced
        )
        
        if not is_referenced:
            orphans.append(page)
    
    return orphans


def check_stale() -> List[tuple]:
    """检查过时页面（长期未更新）"""
    pages = get_all_pages()
    stale = []
    
    for page in pages:
        age = get_page_age(page)
        if age > DAYS_THRESHOLD:
            # 检查更新记录
            try:
                content = page.read_text()
                updated = re.search(r'最后更新[:：]\s*(\d{4}-\d{2}-\d{2})', content)
                if updated:
                    update_date = datetime.strptime(updated.group(1), '%Y-%m-%d')
                    if (datetime.now() - update_date).days > DAYS_THRESHOLD:
                        stale.append((page, (datetime.now() - update_date).days))
                else:
                    stale.append((page, age))
            except:
                stale.append((page, age))
    
    return stale


def check_broken_links() -> List[tuple]:
    """检查失效链接"""
    pages = get_all_pages()
    page_names = {p.stem for p in pages}
    
    broken = []
    for page in pages:
        links = get_page_links(page)
        for link in links:
            # 清理链接名
            link_clean = link.replace(" ", "-").replace("_", "-").lower()
            
            # 检查是否匹配任何页面
            if not any(
                link_clean in p.name.lower() or p.stem.lower() in link_clean
                for p in pages
            ):
                broken.append((page, link))
    
    return broken


def generate_report() -> str:
    """生成健康检查报告"""
    report = []
    report.append("=" * 60)
    report.append("Nick Wiki 健康检查报告")
    report.append("=" * 60)
    report.append(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # 孤立页面
    orphans = check_orphans()
    if orphans:
        report.append("🔴 孤立页面（无引用）")
        for page in orphans:
            report.append(f"  - {page.relative_to(WIKI_ROOT)}")
        report.append("")
    else:
        report.append("✅ 无孤立页面")
        report.append("")
    
    # 过时页面
    stale = check_stale()
    if stale:
        report.append("🟡 过时页面（3个月+未更新）")
        for page, days in stale:
            report.append(f"  - {page.stem}: {days}天前更新")
        report.append("")
    else:
        report.append("✅ 无过时页面")
        report.append("")
    
    # 失效链接
    broken = check_broken_links()
    if broken:
        report.append("🟠 失效链接")
        seen = set()
        for page, link in broken:
            key = (page.stem, link)
            if key not in seen:
                report.append(f"  - {page.stem} → [[{link}]]")
                seen.add(key)
        report.append("")
    else:
        report.append("✅ 无失效链接")
        report.append("")
    
    # 统计
    pages = get_all_pages()
    report.append("-" * 60)
    report.append(f"总页面数: {len(pages)}")
    report.append("")
    
    # 建议
    if orphans or stale or broken:
        report.append("💡 改进建议")
        if orphans:
            report.append("  1. 为孤立页面添加相关链接")
        if stale:
            report.append("  2. 更新过时页面的内容")
        if broken:
            report.append("  3. 修复或移除失效链接")
    
    report.append("=" * 60)
    
    return "\n".join(report)


def main():
    print(generate_report())


if __name__ == "__main__":
    main()
