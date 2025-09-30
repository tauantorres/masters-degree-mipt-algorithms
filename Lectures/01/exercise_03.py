from pathlib import Path


file_path = 'input.txt'
input_path = Path(__file__).with_name(file_path)

lines = []
with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        s = line.strip()
        if s:
            lines.append(s)

if not lines:
    print(0)
    raise SystemExit

first = lines[0].split()
N = int(first[0])
W = int(first[1]) if len(first) > 1 else 0

items = []
items_zero_weight = []
for i in range(1, len(lines)):
    c_str, w_str = lines[i].split()
    c = int(c_str)
    w = int(w_str)

    if w == 0:
        if c > 0:
            items_zero_weight.append([c, w])
    else:
        items.append([c, w])


def compare_density(a, b):
    return a[0] * b[1] > b[0] * a[1]


def partition_hoare(arr, low, high):
    pivot = arr[low + (high - low) // 2]
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while compare_density(arr[i], pivot):
            i += 1

        j -= 1
        while compare_density(pivot, arr[j]):
            j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]


def quicksort_density_desc(arr):
    if len(arr) <= 1:
        return

    stack = [(0, len(arr) - 1)]

    while stack:
        l, r = stack.pop()

        if l < r:
            p = partition_hoare(arr, l, r)
            stack.append((l, p))
            stack.append((p + 1, r))


sorted_items = items_zero_weight
quicksort_density_desc(items)
sorted_items.extend(items)

remaining = W
total_cost = 0

for c, w in sorted_items:
    if remaining <= 0:
        break

    if w == 0:
        total_cost += c
        continue

    if remaining >= w:
        total_cost += c
        remaining -= w
    else:
        total_cost += (c * remaining) // w
        remaining = 0
        break

print(total_cost)
