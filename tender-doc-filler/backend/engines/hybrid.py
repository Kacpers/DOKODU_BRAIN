"""Hybrid engine: rules first, AI fallback for unfilled fields."""
from pathlib import Path
from ..models import CompanyProfile, FieldResult, AnalysisMode
from .rule_engine import analyze_rules
from .ai_engine import analyze_ai


def analyze(docx_path: Path, profile: CompanyProfile, mode: AnalysisMode) -> list[FieldResult]:
    if mode == AnalysisMode.RULE:
        return analyze_rules(docx_path, profile)
    if mode == AnalysisMode.AI:
        return analyze_ai(docx_path, profile)
    # HYBRID: rules first, then AI for additional fields
    rule_results = analyze_rules(docx_path, profile)
    rule_locations = {r.location_id for r in rule_results}
    ai_results = analyze_ai(docx_path, profile)
    additional = [r for r in ai_results if r.location_id not in rule_locations]
    return rule_results + additional
