import random
from pathlib import Path

# file_path = 'tests/02/input-02.txt'
file_path = 'input.txt'
input_file = Path(__file__).with_name(file_path)


def partition(x: list, l: int, r: int, pivot: int) -> int:
    i = l - 1
    for j in range(l, r):
        if x[j] <= pivot:
            i += 1
            x[i], x[j] = x[j], x[i]

    x[i + 1], x[r] = x[r], x[i + 1]
    return i + 1


def qsort(x: list, l: int = 0, r: int = None) -> None:
    if r is None:
        r = len(x)

    if (r - l) > 1:
        pivot = x[random.randint(l, r - 1)]
        il, ir = partition(x, l, r, pivot)
        qsort(x, l, il)
        qsort(x, ir, r)


content = []
with open(input_file) as f:
    for line in f:
        content.append(line.strip())

N, Data = int(content.pop(0)), content.copy()

qsort(Data)
print(' '.join(map(str, Data)))
