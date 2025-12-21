

from typing import Tuple, List
from bisect import bisect_left, bisect_right


INPUT_DATA: str = "./input.txt"

def read_data(FILE_PATH: str = INPUT_DATA) -> list[str]:
    with open(FILE_PATH, 'r') as file:
        lines = file.readlines()
    return lines


def prepare_data() -> Tuple[int, int, List[int], List[Tuple[int, int]]]:

    content_input = read_data()

    N, M = map(int, content_input[0].split())
    scores = sorted(list(map(int, content_input[1].split())))
    lrs = [tuple(map(int, line.split())) for line in content_input[2 : M+2]]

    return N, M, scores, lrs


def count_scores_in_interval(scores: List[int], interval: Tuple[int, int]) -> int:
    left, right = min(interval), max(interval)

    left_index = bisect_left(scores, left)
    right_index = bisect_right(scores, right)

    return right_index - left_index

def main() -> None:

    N, M, scores, lrs = prepare_data()

    for interval in lrs:
        result = count_scores_in_interval(scores, interval)
        print(result)


if __name__ == "__main__":
    main()
