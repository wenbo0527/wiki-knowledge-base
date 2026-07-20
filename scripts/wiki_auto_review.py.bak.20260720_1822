#!/usr/bin/env python3
"""
Wiki 自动走查脚本 - 尼克·弗瑞专用
定期执行健康检查，生成报告并更新维护状态
"""

import os
import sys
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Set, Tuple

# ============ 配置 ============
WIKI_ROOT = Path("/Users/wenbo/Documents/project/Wiki/wiki")
REPORT_DIR = WIKI_ROOT / "process"
STATS_FILE = REPORT_DIR / "wiki_stats.json"
LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')

# 阈值配置
DAYS_THRESHOLD_STALE = 90      # 90天未更新 → 标记STALE
DAYS_THRESHOLD_VERY_STALE = 180  # 180天未更新 → 标记ARCHIVED
DAYS_THRESHOLD_REVIEW = 30     # 30天未更新 → 需要review

# ============ 工具函数 ============

def get_all_pages() -> List[Path]:
    """获取所有wiki页面"""
    exclude = {'index.md', 'log.md', 'NICK_SCHEMA.md', 'PROCESS.md', 'WIKI_MANAGEMENT_RULES.md'}
    pages = []
    for md_file in WIKI_ROOT.rglob("*.md"):
        if md_file.name not in exclude:
            pages.append(md_file)
    return pages

def get_page_links(page: Path) -> Set[str]:
    """获取页面中的所有链接"""
    try:
        content = page.read_text(encoding='utf-8')
        return set(LINK_PATTERN.findall(content))
    except:
        return set()

def get_page_age_days(page: Path) -> int:
    """获取页面年龄（天）"""
    try:
        mtime = page.stat().st_mtime
        age = datetime.now() - datetime.fromtimestamp(mtime)
        return age.days
    except:
        return 999

def get_frontmatter(page: Path) -> Dict:
    """提取frontmatter元数据"""
    try:
        content = page.read_text(encoding='utf-8')
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                fm_text = content[3:end]
                fm = {}
                for line in fm_text.split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        fm[key.strip()] = val.strip().strip('"\'')
                return fm
    except:
        pass
    return {}

def get_page_status(page: Path) -> str:
    """判断页面状态"""
    fm = get_frontmatter(page)
    if fm.get('status') in ['archived', 'stale', 'conflict']:
        return fm['status']
    
    age = get_page_age_days(page)
    if age > DAYS_THRESHOLD_VERY_STALE:
        return 'very_stale'
    elif age > DAYS_THRESHOLD_STALE:
        return 'stale'
    elif age > DAYS_THRESHOLD_REVIEW:
        return 'needs_review'
    return 'active'

# ============ 核心检查 ============

def check_orphaned_pages(all_pages: List[Path]) -> Dict:
    """检查孤立页面（无 inbound links）"""
    # 构建反向索引：哪些页面被链接
    inbound = {}  # page_path -> set of pages that link to it
    
    for page in all_pages:
        page_rel = str(page.relative_to(WIKI_ROOT))
        inbound[page_rel] = set()
    
    for page in all_pages:
        links = get_page_links(page)
        for link in links:
            # link格式可能是 "topics/xxx" 或 "topics/xxx|别名"
            link_path = link.split('|')[0].strip()
            if link_path in inbound:
                inbound[link_path].add(str(page.relative_to(WIKI_ROOT)))
    
    orphaned = []
    for page in all_pages:
        rel = str(page.relative_to(WIKI_ROOT))
        if not inbound[rel] and page.name not in {'README.md', 'index.md'}:
            orphaned.append({
                'page': rel,
                'age_days': get_page_age_days(page),
                'status': get_page_status(page)
            })
    
    return {'count': len(orphaned), 'pages': orphaned[:20]}

def check_stale_pages(all_pages: List[Path]) -> Dict:
    """检查过时页面"""
    stale = []
    for page in all_pages:
        status = get_page_status(page)
        if status in ('stale', 'very_stale', 'needs_review'):
            stale.append({
                'page': str(page.relative_to(WIKI_ROOT)),
                'age_days': get_page_age_days(page),
                'status': status
            })
    
    # 按年龄排序
    stale.sort(key=lambda x: -x['age_days'])
    return {'count': len(stale), 'pages': stale[:30]}

def check_dead_links(all_pages: List[Path]) -> Dict:
    """检查死链（v4 · L-50.2.4 治本 · 7-18 升级 · ../ 跳出 wiki 根支持）"""
    # 1. 构建 all_paths：.md + 去 .md + 目录 + 目录/README.md + 大小写不敏感
    all_paths = set()
    all_paths_lower = set()
    for p in all_pages:
        rel = str(p.relative_to(WIKI_ROOT))
        all_paths.add(rel)
        all_paths_lower.add(rel.lower())
        if rel.endswith('.md'):
            no_md = rel[:-3]
            all_paths.add(no_md)
            all_paths_lower.add(no_md.lower())
    for d in WIKI_ROOT.rglob("*"):
        if d.is_dir():
            rel = str(d.relative_to(WIKI_ROOT))
            all_paths.add(rel)
            all_paths_lower.add(rel.lower())
            for readme in ['README.md', 'index.md']:
                if (d / readme).exists():
                    full = f"{rel}/{readme}"
                    all_paths.add(full)
                    all_paths_lower.add(full.lower())
                    no_md = f"{rel}/{readme[:-3]}"
                    all_paths.add(no_md)
                    all_paths_lower.add(no_md.lower())
    
    # 2. 死链 = wiki-link 不在 all_paths（含 ../ 跳出 + 外部引用支持）
    dead_links = []
    for page in all_pages:
        links = get_page_links(page)
        page_rel = str(page.relative_to(WIKI_ROOT))
        for link in links:
            link_path = link.split('|')[0].strip()
            if link_path.startswith(('http', 'https', 'mailto')):
                continue
            
            # 多候选
            candidates = {link_path}
            candidates_lower = {link_path.lower()}
            if link_path.endswith('.md'):
                candidates.add(link_path[:-3])
                candidates_lower.add(link_path[:-3].lower())
            else:
                candidates.add(link_path + '.md')
                candidates_lower.add((link_path + '.md').lower())
            # 目录候选
            for readme in ['README.md', 'index.md']:
                candidates.add(f"{link_path}/{readme}")
                candidates.add(f"{link_path}/{readme[:-3]}")
                candidates_lower.add(f"{link_path}/{readme}".lower())
                candidates_lower.add(f"{link_path}/{readme[:-3]}".lower())
            
            # v4 新增：../ 相对路径解析（Obsidian 风格 + 跳出 wiki 根支持）
            if link_path.startswith('../') or link_path.startswith('./'):
                # 尝试解析（不抛 ValueError）
                try:
                    full_path = (page.parent / link_path).resolve()
                    # 在 wiki 内
                    full_path_str = str(full_path)
                    if full_path_str.startswith(str(WIKI_ROOT.resolve())):
                        rel_str = str(full_path.relative_to(WIKI_ROOT.resolve()))
                        candidates.add(rel_str)
                        candidates_lower.add(rel_str.lower())
                        if rel_str.endswith('.md'):
                            no_md = rel_str[:-3]
                            candidates.add(no_md)
                            candidates_lower.add(no_md.lower())
                    else:
                        # 跳出 wiki 根：检查文件是否真实存在（外部引用）
                        if full_path.exists():
                            continue  # 外部引用且存在 → 跳过不算死链
                except Exception:
                    pass
            
            # 双层匹配：严格 + 大小写不敏感
            if not (any(c in all_paths for c in candidates) or 
                    any(c in all_paths_lower for c in candidates_lower)):
                dead_links.append({
                    'from': page_rel,
                    'link': link_path
                })
    
    return {'count': len(dead_links), 'links': dead_links[:20]}

def check_empty_dirs() -> Dict:
    """检查空目录"""
    empty_dirs = []
    for d in WIKI_ROOT.rglob("*"):
        if d.is_dir() and not any(d.iterdir()):
            empty_dirs.append(str(d.relative_to(WIKI_ROOT)))
    return {'count': len(empty_dirs), 'dirs': empty_dirs}

def check_insights_quality() -> Dict:
    """检查Insights质量（抽查）"""
    insights_dir = WIKI_ROOT / "insights"
    if not insights_dir.exists():
        return {'count': 0, 'issues': []}
    
    issues = []
    for insight in list(insights_dir.glob("insight-*.md"))[-10:]:  # 抽查最近10个
        content = insight.read_text(encoding='utf-8')
        problems = []
        
        # 检查必需字段
        if '---' not in content:
            problems.append('无frontmatter')
        if not re.search(r'\[{2}[^\]]+\]{2}', content):  # 无双向链接
            problems.append('无双向链接')
        if len(content) < 500:
            problems.append('内容过短(<500字)')
        
        if problems:
            issues.append({
                'file': insight.name,
                'problems': problems
            })
    
    return {'count': len(issues), 'issues': issues}

def calculate_health_score(stats: Dict) -> Tuple[int, str]:
    """计算健康度评分"""
    score = 100
    reasons = []

    # 孤立页面：Insights是独立存在的笔记，不算孤立
    # 只对非Insights页面中的孤立者扣分
    non_insight_orphaned = [p for p in stats['orphaned']['pages'] if 'insight' not in p['page']]
    if len(non_insight_orphaned) > 20:
        score -= 15
        reasons.append(f"非Insight孤立页面({len(non_insight_orphaned)}个)")
    elif len(non_insight_orphaned) > 5:
        score -= 5

    # 过时页面：超过90天未更新的非Insights页面
    real_stale = [p for p in stats['stale']['pages']]
    if len(real_stale) > 10:
        score -= 20
        reasons.append(f"过时页面({len(real_stale)}个)")
    elif len(real_stale) > 5:
        score -= 10
        reasons.append(f"过时页面({len(real_stale)}个)")
    elif len(real_stale) > 0:
        score -= 3
        reasons.append(f"过时页面({len(real_stale)}个)")

    # 死链：过滤模板占位符，只计算真实死链
    placeholders = ['xxx', 'yyy', 'YYYYMMDD', 'topic-id', 'entity-id', 'concept-id', 'requirement']
    real_dead = [dl for dl in stats['dead_links']['links']
                  if not any(tmpl in dl['link'] for tmpl in placeholders)]
    if len(real_dead) > 20:
        score -= 15
        reasons.append(f"真实死链({len(real_dead)}个)")
    elif len(real_dead) > 5:
        score -= 5
        reasons.append(f"真实死链({len(real_dead)}个)")

    # 空目录
    if stats['empty_dirs']['count'] > 3:
        score -= 10
        reasons.append(f"空目录({stats['empty_dirs']['count']}个)")
    elif stats['empty_dirs']['count'] > 0:
        score -= 5
        reasons.append(f"空目录({stats['empty_dirs']['count']}个)")

    score = max(0, min(100, score))

    if score >= 90:
        label = "🟢 优秀"
    elif score >= 75:
        label = "🟡 良好"
    elif score >= 60:
        label = "🟠 一般"
    else:
        label = "🔴 需修复"

    return score, f"{label} ({score}/100)" + (f" - {', '.join(reasons)}" if reasons else " - 无问题")


# ============ 报告生成 ============

def generate_report(stats: Dict, health: Tuple[int, str]) -> str:
    """生成走查报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lines = [
        f"# Wiki 自动走查报告",
        f"",
        f"> **执行时间**: {now}",
        f"> **执行人**: 尼克·弗瑞 🕵️",
        f"",
        f"---",
        f"",
    ]
    
    # 执行摘要
    lines.extend([
        f"## 一、执行摘要",
        f"",
        f"| 项目 | 数值 |",
        f"|------|------|",
        f"| 总文件数 | {stats['total_pages']} |",
        f"| 孤立页面 | {stats['orphaned']['count']} |",
        f"| 过时页面 | {stats['stale']['count']} |",
        f"| 死链 | {stats['dead_links']['count']} |",
        f"| 空目录 | {stats['empty_dirs']['count']} |",
        f"",
        f"**整体健康度**: {health[1]}",
        f"",
    ])
    
    # 孤立页面
    if stats['orphaned']['count'] > 0:
        lines.extend([
            f"## 二、孤立页面 ⚠️",
            f"",
            f"| 页面 | 天数 | 状态 |",
            f"|------|------|------|",
        ])
        for p in stats['orphaned']['pages'][:10]:
            status_icon = {"active": "✅", "stale": "⚠️", "very_stale": "🔴"}.get(p['status'], "")
            lines.append(f"| {p['page']} | {p['age_days']} | {status_icon} {p['status']} |")
        if stats['orphaned']['count'] > 10:
            lines.append(f"| ... | | |（共{stats['orphaned']['count']}个）")
        lines.append("")
    
    # 过时页面
    if stats['stale']['count'] > 0:
        lines.extend([
            f"## 三、过时页面 ⏰",
            f"",
            f"| 页面 | 天数 | 状态 |",
            f"|------|------|------|",
        ])
        for p in stats['stale']['pages'][:15]:
            status_icon = {
                "needs_review": "🟡", 
                "stale": "⚠️", 
                "very_stale": "🔴"
            }.get(p['status'], "")
            lines.append(f"| {p['page']} | {p['age_days']} | {status_icon} {p['status']} |")
        if stats['stale']['count'] > 15:
            lines.append(f"| ... | | |（共{stats['stale']['count']}个）")
        lines.append("")
    
    # 死链
    if stats['dead_links']['count'] > 0:
        lines.extend([
            f"## 四、死链 🔗",
            f"",
            f"| 来源文件 | 失效链接 |",
            f"|----------|---------|",
        ])
        for dl in stats['dead_links']['links'][:10]:
            lines.append(f"| {dl['from']} | {dl['link']} |")
        lines.append("")
    
    # 空目录
    if stats['empty_dirs']['count'] > 0:
        lines.extend([
            f"## 五、空目录 📁",
            f"",
        ])
        for d in stats['empty_dirs']['dirs']:
            lines.append(f"- [ ] {d}")
        lines.append("")
    
    # Insights质量
    if stats.get('insights_quality', {}).get('count', 0) > 0:
        lines.extend([
            f"## 六、质量问题 🔍",
            f"",
        ])
        for iq in stats['insights_quality']['issues']:
            problems = ', '.join(iq['problems'])
            lines.append(f"- **{iq['file']}**: {problems}")
        lines.append("")
    
    # 建议行动
    lines.extend([
        f"## 七、建议行动",
        f"",
    ])
    
    actions = []
    if stats['orphaned']['count'] > 0:
        actions.append(f"- [ ] 处理 {stats['orphaned']['count']} 个孤立页面（删除或建立链接）")
    if stats['stale']['count'] > 0:
        actions.append(f"- [ ] 更新 {stats['stale']['count']} 个过时页面")
    if stats['dead_links']['count'] > 0:
        actions.append(f"- [ ] 修复 {stats['dead_links']['count']} 个死链")
    if stats['empty_dirs']['count'] > 0:
        actions.append(f"- [ ] 清理 {stats['empty_dirs']['count']} 个空目录")
    
    if actions:
        lines.extend(actions)
    else:
        lines.append("✅ 无需处理的问题")
    
    lines.extend([
        f"",
        f"---",
        f"*Wiki自动走查系统 · 尼克·弗瑞 🕵️ · {now}*",
    ])
    
    return '\n'.join(lines)

# ============ 主流程 ============

def run_wiki_review() -> Dict:
    """执行Wiki走查"""
    print("🔍 执行Wiki自动走查...")
    
    all_pages = get_all_pages()
    print(f"📄 扫描 {len(all_pages)} 个页面...")
    
    # 执行各项检查
    stats = {
        'total_pages': len(all_pages),
        'orphaned': check_orphaned_pages(all_pages),
        'stale': check_stale_pages(all_pages),
        'dead_links': check_dead_links(all_pages),
        'empty_dirs': check_empty_dirs(),
        'insights_quality': check_insights_quality(),
    }
    
    # 计算健康度
    health = calculate_health_score(stats)
    print(f"✅ 健康度: {health[1]}")
    
    # 生成报告
    report = generate_report(stats, health)
    
    # 保存报告
    report_file = REPORT_DIR / f"wiki-review-report-{datetime.now().strftime('%Y%m%d')}.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"📝 报告已保存: {report_file.name}")
    
    # 更新统计文件
    stats_summary = {
        'last_run': datetime.now().isoformat(),
        'total_pages': stats['total_pages'],
        'health_score': health[0],
        'health_label': health[1],
        'orphaned_count': stats['orphaned']['count'],
        'stale_count': stats['stale']['count'],
        'dead_links_count': stats['dead_links']['count'],
        'empty_dirs_count': stats['empty_dirs']['count'],
    }
    STATS_FILE.write_text(json.dumps(stats_summary, indent=2, ensure_ascii=False), encoding='utf-8')
    
    # 输出摘要
    print(f"")
    print(f"📊 走查摘要:")
    print(f"  - 孤立页面: {stats['orphaned']['count']}")
    print(f"  - 过时页面: {stats['stale']['count']}")
    print(f"  - 死链: {stats['dead_links']['count']}")
    print(f"  - 空目录: {stats['empty_dirs']['count']}")
    
    return stats_summary

if __name__ == "__main__":
    result = run_wiki_review()
    sys.exit(0)
