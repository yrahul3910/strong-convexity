import subprocess
import os
import threading

class list(list):
    def map(self, f):
        return list(map(f, self))

import sys
import numpy as np


def parse_opentuner(base_dir: str):
    scores = []
    __proc = subprocess.Popen(f'ls {base_dir}/*.txt', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    __proc.wait()
    EXIT_CODE = __proc.returncode
    __comm = __proc.communicate()
    _, STDERR = __comm[0].decode('utf-8').rstrip(), __comm[1].decode('utf-8').rstrip()
    _ = _.split('\n')
    try:
        _ = list(_)
    except ValueError:
        raise
    file = _[0]

    if EXIT_CODE != 0:
        return []

    print("Parsing", file)
    __proc = subprocess.Popen(f'grep "\[Accuracy\]" {file}', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    __proc.wait()
    EXIT_CODE = __proc.returncode
    __comm = __proc.communicate()
    _, STDERR = __comm[0].decode('utf-8').rstrip(), __comm[1].decode('utf-8').rstrip()
    _ = _.split('\n')
    try:
        _ = list(_)
    except ValueError:
        raise
    lines = _
    lines = lines.map(lambda x: float(x.split(" ")[1]))

    
    try:
        lines = np.array(lines[:600]).reshape(20, 30)
    except ValueError:
        lines = np.array(lines[:250]).reshape(10, 25)

    def foo(arr):
        keep = [x for x in arr if x != 100.]
        return max(keep)

    maxes = list(map(foo, lines))
    print('Maxes:', maxes)
    
    return maxes


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} BASE_DIR')
        sys.exit(1)

    dir = sys.argv[1]
    maxes = parse_opentuner(dir)
    print('Scores:', maxes)
    print('Median:', np.median(maxes))
