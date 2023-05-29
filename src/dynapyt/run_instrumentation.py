import argparse
from os import walk
from os import path
from pathlib import Path
import shutil
from subprocess import run
import time
from multiprocessing import Pool
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--directory", help="Directory of the project to analyze")
parser.add_argument(
    "--analysis", help="Analysis class name")
parser.add_argument(
    "--module", help="Adds external module paths")
parser.add_argument(
    "--external_dir", help="Place instrumented files in another directory",
    dest='external_dir', action='store_true'
)
parser.add_argument(
    "--ignore", help="Path to a json file containing two keys, 'title' and 'content', which are lists of strings."
                     " If a file path contains any of the strings in 'title' or the file contains any of the strings in"
                     " 'content', it will be ignored.",
)

def process_files(cmd_list, file_path):
    comp_proc = run(cmd_list)
    if comp_proc.returncode != 0:
        print('Error at', file_path)

if __name__ == '__main__':
    args = parser.parse_args()
    start = args.directory
    analysis = args.analysis
    module = args.module
    use_external_dir = args.external_dir
    start_time = time.time()
    all_cmds = []

    if use_external_dir:
        external_path = Path(start) / "dynapyt_analysis"
        # create new folder /dynapyt_analysis on same level as specified directory
        shutil.rmtree(external_path, ignore_errors=True)
        shutil.copytree(start, external_path)
        start = str(external_path)

    if args.ignore is not None:
        ignore_file = args.ignore
        try:
            with open(ignore_file) as f:
                ignore_dict = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f'Error reading ignore file {e}')
            exit(1)
        print('Ignoring files with title containing:', ignore_dict.get('title', []))
        ignore_title = ignore_dict.get('title', [])
    else:
        ignore_title = []

    for dir_path, dir_names, file_names in walk(start):
        if any(title in dir_path for title in ignore_title):
            print('Ignoring directory', dir_path)
            continue
        for name in file_names:
            if any(title in name for title in ignore_title):
                print('Ignoring file', name)
                continue
            if name.endswith('.py'):
                file_path = path.join(dir_path, name)
                cmd_list = ['python', '-m', 'dynapyt.instrument.instrument',
                            '--files', file_path, '--analysis', analysis]
                if args.ignore is not None:
                    cmd_list.extend(['--ignore', ignore_file])
                if module is not None:
                    cmd_list.extend(['--module', module])
                all_cmds.append((cmd_list, file_path))
    with Pool(maxtasksperchild=5) as p:
        p.starmap(process_files, all_cmds)
    print('#################### Instrumentation took ' + str(time.time() - start_time))
