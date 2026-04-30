#!/usr/bin/env python3
"""
Source Evaluator - 信息源质量评估工具

功能:
- 追踪RSS/GitHub源的质量变化
- TIER评级 (TIER_1/2/3)
- 30天产出统计

来源: insight-20260429-simon-willison-hoard-things
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class SourceRecord:
    """信息源记录"""
    source_id: str
    name: str
    url: str
    tier: str  # TIER_1, TIER_2, TIER_3
    total_articles: int = 0
    quality_articles: int = 0  # ⭐⭐⭐+
    last_checked: Optional[datetime] = None
    first_seen: datetime = field(default_factory=datetime.now)
    
    @property
    def quality_rate(self) -> float:
        if self.total_articles == 0:
            return 0.0
        return self.quality_articles / self.total_articles

@dataclass
class EvaluationResult:
    """评估结果"""
    source_id: str
    action: str  # promote, demote, remove, keep
    reason: str
    current_tier: str
    suggested_tier: Optional[str] = None

class SourceEvaluator:
    """
    信息源质量评估器
    
    规则:
    - TIER_1: 30天内产出≥3篇⭐⭐⭐+ → 晋升
    - TIER_2→TIER_1: 30天内产出≥3篇⭐⭐⭐+ → 晋升
    - TIER_1→TIER_2: 连续30天无⭐⭐⭐+ → 降级
    - TIER_3→remove: 连续60天无任何产出 → 移除
    """
    
    TIER_LIMITS = {
        "TIER_1": 20,   # 最多20个
        "TIER_2": 50,   # 最多50个
        "TIER_3": 100   # 最多100个
    }
    
    PROMOTION_THRESHOLD = 3  # 30天内至少3篇⭐⭐⭐+
    DEMOTION_WINDOW = 30     # 天数
    REMOVAL_WINDOW = 60      # 天数
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.sources: Dict[str, SourceRecord] = {}
        self.article_history: Dict[str, List[dict]] = defaultdict(list)
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        sources_file = self.data_path / "sources.json"
        if sources_file.exists():
            with open(sources_file) as f:
                data = json.load(f)
                for s in data.get('sources', []):
                    self.sources[s['source_id']] = SourceRecord(**s)
        
        history_file = self.data_path / "article_history.json"
        if history_file.exists():
            with open(history_file) as f:
                self.article_history = defaultdict(list, json.load(f))
    
    def _save_data(self):
        """保存数据"""
        sources_file = self.data_path / "sources.json"
        with open(sources_file, 'w') as f:
            json.dump({
                'sources': [s.__dict__ for s in self.sources.values()]
            }, f, indent=2, default=str)
        
        history_file = self.data_path / "article_history.json"
        with open(history_file, 'w') as f:
            json.dump(dict(self.article_history), f, indent=2, default=str)
    
    def add_article(self, source_id: str, article: dict):
        """添加文章记录"""
        self.article_history[source_id].append({
            **article,
            'timestamp': datetime.now().isoformat()
        })
        if source_id in self.sources:
            self.sources[source_id].total_articles += 1
            if article.get('rating', 0) >= 3:
                self.sources[source_id].quality_articles += 1
    
    def evaluate_all(self) -> List[EvaluationResult]:
        """评估所有源"""
        results = []
        now = datetime.now()
        
        for source_id, source in self.sources.items():
            result = self._evaluate_source(source, now)
            if result:
                results.append(result)
        
        return results
    
    def _evaluate_source(self, source: SourceRecord, now: datetime) -> Optional[EvaluationResult]:
        """评估单个源"""
        cutoff_promotion = now - timedelta(days=self.DEMOTION_WINDOW)
        cutoff_removal = now - timedelta(days=self.REMOVAL_WINDOW)
        
        # 统计最近30天产出
        recent_articles = [
            a for a in self.article_history[source.source_id]
            if datetime.fromisoformat(a['timestamp']) > cutoff_promotion
        ]
        
        recent_quality = [a for a in recent_articles if a.get('rating', 0) >= 3]
        
        # 晋升规则: TIER_2→TIER_1
        if source.tier == "TIER_2" and len(recent_quality) >= self.PROMOTION_THRESHOLD:
            # 检查TIER_1是否有空位
            tier1_count = sum(1 for s in self.sources.values() if s.tier == "TIER_1")
            if tier1_count < self.TIER_LIMITS["TIER_1"]:
                return EvaluationResult(
                    source_id=source.source_id,
                    action="promote",
                    reason=f"30天内产出{len(recent_quality)}篇⭐⭐⭐+，达到晋升标准",
                    current_tier=source.tier,
                    suggested_tier="TIER_1"
                )
        
        # 降级规则: TIER_1→TIER_2
        if source.tier == "TIER_1" and len(recent_quality) == 0:
            return EvaluationResult(
                source_id=source.source_id,
                action="demote",
                reason=f"连续{self.DEMOTION_WINDOW}天无⭐⭐⭐+产出",
                current_tier=source.tier,
                suggested_tier="TIER_2"
            )
        
        # 移除规则: TIER_3→remove
        if source.tier == "TIER_3":
            recent_any = [
                a for a in self.article_history[source.source_id]
                if datetime.fromisoformat(a['timestamp']) > cutoff_removal
            ]
            if len(recent_any) == 0:
                return EvaluationResult(
                    source_id=source.source_id,
                    action="remove",
                    reason=f"连续{self.REMOVAL_WINDOW}天无任何产出",
                    current_tier=source.tier
                )
        
        return None
    
    def print_report(self, results: List[EvaluationResult]):
        """打印评估报告"""
        print("=" * 60)
        print("SOURCE EVALUATION REPORT")
        print("=" * 60)
        print(f"Total sources: {len(self.sources)}")
        
        for tier in ["TIER_1", "TIER_2", "TIER_3"]:
            count = sum(1 for s in self.sources.values() if s.tier == tier)
            limit = self.TIER_LIMITS[tier]
            print(f"  {tier}: {count}/{limit}")
        
        if results:
            print(f"\n📋 Recommended Actions ({len(results)}):")
            for r in results:
                icon = {"promote": "⬆️", "demote": "⬇️", "remove": "🗑️"}.get(r.action, "•")
                print(f"\n  {icon} {r.source_id}")
                print(f"     Action: {r.action}")
                print(f"     Reason: {r.reason}")
                if r.suggested_tier:
                    print(f"     {r.current_tier} → {r.suggested_tier}")
        
        print("\n" + "=" * 60)


if __name__ == "__main__":
    data_path = "/Users/wenbo/.nickfury/source_data"
    evaluator = SourceEvaluator(data_path)
    results = evaluator.evaluate_all()
    evaluator.print_report(results)
