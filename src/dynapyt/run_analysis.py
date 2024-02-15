from typing import List
import argparse
import importlib
from os.path import abspath
from tempfile import gettempdir
from shutil import rmtree
import sys
from pathlib import Path
from . import runtime as _rt
from .utils.load_class_from_path import load_class_from_path
from .utils.base_initial_configuration import BaseInitialConfiguration


def run_analysis(
    entry: str, analyses: List[str], name: str = None, coverage: bool = False, init = None, entry_args = None,
):
    coverage_dir = Path(gettempdir()) / "dynapyt_coverage"
    if coverage:
        coverage_dir.mkdir(exist_ok=True)
    else:
        rmtree(str(coverage_dir), ignore_errors=True)

    analyses_file = Path(gettempdir()) / "dynapyt_analyses.txt"
    if analyses_file.exists():
        analyses_file.unlink()
    with open(str(analyses_file), "w") as f:
        f.write("\n".join(analyses))

    if init is not None:
        init_config = load_class_from_path(init)
        if init_config is None:
            raise ValueError("init config not found")
        if not isinstance(init_config, BaseInitialConfiguration):
            raise ValueError("init config should be a subclass of BaseInitialConfiguration")
        init_config.setup()

    _rt.set_analysis(analyses)

    for analysis in _rt.analyses:
        func = getattr(analysis, "begin_execution", None)
        if func is not None:
            func()
    if entry.endswith(".py"):
        argv = [entry, *entry_args]
        entry_full_path = abspath(entry)
        globals_dict = globals().copy()
        sys.path.insert(0, str(Path(entry_full_path).parent))
        globals_dict["__file__"] = entry_full_path
        exec(open(entry_full_path).read(), {'argv': argv, **globals_dict})
    else:
        importlib.import_module(entry)
    _rt.end_execution()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--entry", help="Entry file for execution", required=True)
    parser.add_argument(
        "--analysis", help="Analysis class name(s)", nargs="+", required=True
    )
    parser.add_argument("--name", help="Associates a given name with current run")
    parser.add_argument("--coverage", help="Enables coverage", action="store_true")
    parser.add_argument("--init", help="Runs initial configuration")
    parser.add_argument("--args", help="Arguments to pass to entry file", nargs="*")
    args = parser.parse_args()
    name = args.name
    analyses = args.analysis
    coverage = args.coverage
    init = args.init
    entry_args = args.args or []
    run_analysis(args.entry, analyses, name, coverage, init, entry_args)
