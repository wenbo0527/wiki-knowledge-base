#!/usr/bin/env python3
"""
Wiki Lint - Wiki链接健康检查工具

功能:
- 检查所有.md文件中的链接
- 识别失效链接
- 生成健康报告

来源: Wiki维护实践
"""

import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from datetime import datetime

@dataclass
class LinkIssue:
    """链接问题"""
    file_path: str
    line_number: int
    link_type: str  # internal, external, wiki
    link_target: str
    issue_type: str  # broken, missing_extension, relative_path
    suggestion: Optional[str] = None

@dataclass
class WikiHealthReport:
    """Wiki健康报告"""
    total_files: int = 0
    total_links: int = 0
    broken_links: List[LinkIssue] = field(default_factory=list)
    warnings: List[LinkIssue] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.now)

class WikiLinkChecker:
    """Wiki链接检查器"""
    
    DOC_EXTENSIONS = {'.md', '.mdx', '.txt'}
    WIKI_LINK_PATTERN = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
    MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^\)]+\))')
    EXTERNAL_PATTERN = re.compile(r'https?://')
    
    def __init__(self, wiki_root: str):
        self.wiki_root = Path(wiki_root)
        self.issues: List[LinkIssue] = []
        self.checked_files: Set[str] = set()
    
    def scan(self) -> WikiHealthReport:
        """扫描整个Wiki"""
        report = WikiHealthReport()
        all_files = list(self.wiki_root.rglob("*.md"))
        report.total_files = len(all_files)
        
        for file_path in all_files:
            self._check_file(file_path, report)
        
        return report
    
    def _check_file(self, file_path: Path, report: WikiHealthReport):
        """检查单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8')
            rel_path = file_path.relative_to(self.wiki_root)
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for match in self.MD_LINK_PATTERN.finditer(line):
                    link_text = match.group(1)
                    link_target = match.group(2)
                    report.total_links += 1
                    
                    if self.EXTERNAL_PATTERN.match(link_target):
                        continue
                    else:
                        issue = self._check_internal_link(
                            file_path.parent, link_target, rel_path, line_num
                        )
                        if issue:
                            if issue.issue_type == 'broken':
                                report.broken_links.append(issue)
                            else:
                                report.warnings.append(issue)
                
                for match in self.WIKI_LINK_PATTERN.finditer(line):
                    wiki_link = match.group(1)
                    report.total_links += 1
                    resolved = file_path.parent / (wiki_link + ".md")
                    if not resolved.exists():
                        issue = LinkIssue(
                            file_path=str(rel_path),
                            line_number=line_num,
                            link_type='wiki',
                            link_target=wiki_link,
                            issue_type='missing_extension',
                            suggestion=f"{wiki_link}.md"
                        )
                        report.warnings.append(issue)
                        
        except Exception as e:
            print(f"Error checking {file_path}: {e}", file=sys.stderr)
    
    def _check_internal_link(self, current_dir: Path, link_target: str,
                            original_file: Path, line_num: int) -> Optional[LinkIssue]:
        """检查内部链接"""
        link_target = link_target.split('#')[0]
        if not link_target:
            return None
        
        if link_target.startswith('/'):
            target_path = self.wiki_root / link_target.lstrip('/')
        else:
            target_path = current_dir / link_target
        
        if not target_path.suffix:
            for ext in self.DOC_EXTENSIONS:
                if target_path.with_suffix(ext).exists():
                    target_path = target_path.with_suffix(ext)
                    break
        
        if not target_path.exists():
            return LinkIssue(
                file_path=str(original_file),
                line_number=line_num,
                link_type='internal',
                link_target=str(target_path),
                issue_type='broken'
            )
        return None
    
    def print_report(self, report: WikiHealthReport):
        """打印报告"""
        print("=" * 60)
        print("WIKI HEALTH REPORT")
        print("=" * 60)
        print(f"Checked: {report.checked_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total files: {report.total_files}")
        print(f"Total links: {report.total_links}")
        
        if report.broken_links:
            print(f"\n🔴 BROKEN LINKS ({len(report.broken_links)})")
            for issue in report.broken_links[:10]:
                print(f"  {issue.file_path}:{issue.line_number}")
                print(f"    -> {issue.link_target}")
        
        if report.warnings:
            print(f"\n🟡 WARNINGS ({len(report.warnings)})")
            for issue in report.warnings[:10]:
                print(f"  {issue.file_path}:{issue.line_number}")
                print(f"    -> {issue.link_target}")
        
        if not report.broken_links and not report.warnings:
            print("\n✅ Wiki is healthy!")
        
        if report.total_links > 0:
            health = (1 - len(report.broken_links) / report.total_links) * 100
            print(f"\nHealth Score: {health:.1f}%")


if __name__ == "__main__":
    wiki_root = "/Users/wenbo/Documents/project/Wiki/wiki"
    if len(sys.argv) > 1:
        wiki_root = sys.argv[1]
    
    checker = WikiLinkChecker(wiki_root)
    report = checker.scan()
    checker.print_report(report)
