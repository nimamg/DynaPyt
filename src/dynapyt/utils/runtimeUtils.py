from typing import List, Any
from ..analyses.BaseAnalysis import BaseAnalysis
from .load_class_from_path import load_class_from_path

PRIORITIZE_OLD_ARGS = 1
PRIORITIZE_NEW_ARGS = 2

def load_analyses(analyses: List[Any]) -> List[BaseAnalysis]:
    res_analyses = []
    for ana in analyses:
        if isinstance(ana, str):
            res_analyses.append(load_class_from_path(ana))
        elif isinstance(ana, BaseAnalysis):
            res_analyses.append(ana)
        else:
            continue
    return res_analyses


def merge_coverage(base_coverage: dict, new_coverage: dict) -> dict:
    for cov_file, coverage in new_coverage.items():
        if cov_file not in base_coverage:
            base_coverage[cov_file] = {}
        for line, analysis_cov in coverage.items():
            if line not in base_coverage[cov_file]:
                base_coverage[cov_file][line] = {}
            for analysis, count in analysis_cov.items():
                if analysis not in base_coverage[cov_file][line]:
                    base_coverage[cov_file][line][analysis] = 0
                base_coverage[cov_file][line][analysis] += count
    return base_coverage
