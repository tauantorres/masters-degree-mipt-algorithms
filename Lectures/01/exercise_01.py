import sys
from pathlib import Path

file_path = 'input.txt'
input_path = Path(__file__).with_name(file_path)

ID_INDEX = 0
SCORE_INDEX = 1
NAME_INDEX = 2

content = []
with open(input_path) as f:
    for line in f:
        content.append(line.strip())

Data = content.copy()
N = int(Data.pop(0))

students = []
for item in Data:
    id, score, name = item.split()
    students.append((int(id), int(score), name))

for i in range(N):
    for j in range(0, N - i - 1):
        current_score = students[j][SCORE_INDEX]
        next_score = students[j + 1][SCORE_INDEX]

        current_id = students[j][ID_INDEX]
        next_id = students[j + 1][ID_INDEX]

        if current_score < next_score or (current_score == next_score and current_id > next_id):
            students[j], students[j + 1] = students[j + 1], students[j]

for i in range(3):
    print(students[i][NAME_INDEX])

ids = [students[i][ID_INDEX] for i in range(N)]
for id in ids:
    print(id, end=' ')
