from typing import List, Any
from ..analyses.BaseAnalysis import BaseAnalysis
from .load_class_from_path import load_class_from_path


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
