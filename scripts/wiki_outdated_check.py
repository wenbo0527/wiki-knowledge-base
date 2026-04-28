#!/usr/bin/env python3
"""
Wiki过时机员检测脚本
检测超过3个月未更新的页面

用法:
    python3 scripts/wiki_outdated_check.py          # 检查所有页面
    python3 scripts/wiki_outdated_check.py --months 6  # 自定义月数
"""

import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path

WIKI_ROOT = Path("/Users/wenbo/Documents/project/Wiki/wiki")
DEFAULT_MONTHS = 3


def get_file_mtime(file_path: Path) -> datetime:
    """获取文件最后修改时间"""
    stat = file_path.stat()
    return datetime.fromtimestamp(stat.st_mtime)


def get_file_age_days(file_path: Path) -> int:
    """计算文件年龄（天）"""
    mtime = get_file_mtime(file_path)
    age = datetime.now() - mtime
    return age.days


def is_outdated(file_path: Path, months: int) -> bool:
    """判断文件是否过时期"""
    age_days = get_file_age_days(file_path)
    threshold_days = months * 30  # 粗略计算
    return age_days > threshold_days


def check_wiki_outdated(months: int = DEFAULT_MONTHS) -> dict:
    """
    检查Wiki中的过期页面
    
    Returns:
        dict: {
            'outdated_files': [...],
            'summary': {...}
        }
    """
    threshold_days = months * 30
    outdated_files = []
    total_checked = 0
    
    # 遍历所有.md文件（排除README统计）
    for md_file in WIKI_ROOT.rglob("*.md"):
        total_checked += 1
        age_days = get_file_age_days(md_file)
        
        if age_days > threshold_days:
            # 获取相对路径
            rel_path = md_file.relative_to(WIKI_ROOT)
            
            # 计算更精确的月数
            exact_months = age_days / 30
            
            outdated_files.append({
                'path': str(rel_path),
                'age_days': age_days,
                'age_months': round(exact_months, 1),
                'last_modified': get_file_mtime(md_file).strftime('%Y-%m-%d')
            })
    
    # 按年龄排序
    outdated_files.sort(key=lambda x: x['age_days'], reverse=True)
    
    return {
        'outdated_files': outdated_files,
        'summary': {
            'total_checked': total_checked,
            'outdated_count': len(outdated_files),
            'threshold_months': months,
            'check_date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    }


def print_report(result: dict):
    """打印报告"""
    summary = result['summary']
    files = result['outdated_files']
    
    print("=" * 60)
    print("📋 Wiki过时机员检测报告")
    print("=" * 60)
    print(f"检查日期: {summary['check_date']}")
    print(f"检查范围: {summary['total_checked']} 个文件")
    print(f"过期阈值: {summary['threshold_months']} 个月")
    print(f"过期文件: {summary['outdated_count']} 个")
    print()
    
    if files:
        print("⚠️ 过期文件列表:")
        print("-" * 60)
        for i, f in enumerate(files[:30], 1):  # 最多显示30个
            print(f"{i:2}. {f['path']}")
            print(f"    最后修改: {f['last_modified']} | "
                  f"年龄: {f['age_months']}个月 ({f['age_days']}天)")
        print()
        
        if len(files) > 30:
            print(f"... 还有 {len(files) - 30} 个文件未显示")
            print()
    
    print("=" * 60)
    print("建议操作:")
    print("  1. 更新仍在使用的过期页面")
    print("  2. 归档已过时的内容")
    print("  3. 删除无人访问的死内容")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Wiki过时机员检测')
    parser.add_argument('--months', type=int, default=DEFAULT_MONTHS,
                        help=f'过期月数阈值 (默认: {DEFAULT_MONTHS})')
    args = parser.parse_args()
    
    result = check_wiki_outdated(args.months)
    print_report(result)
    
    # 返回退出码：有过期文件时返回1
    return 1 if result['outdated_files'] else 0


if __name__ == '__main__':
    exit(main())
