from typing import Tuple, List


INPUT_DATA: str = "./input.txt"
OUTPUT_DATA: str = "./output.txt"


def prepare_raw_data(
    exercise_id: str,
    sample_number: int,
) -> None:
    
    raw_input_data: str = f"Data/{exercise_id}/inputs/{sample_number:02}.txt"
    raw_output_data: str = f"Data/{exercise_id}/outputs/{sample_number:02}.txt"

    input_lines: list[str] = read_data(raw_input_data)
    output_lines: list[str] = read_data(raw_output_data)

    write_data(FILE_PATH=INPUT_DATA, lines=input_lines)
    write_data(FILE_PATH=OUTPUT_DATA, lines=output_lines)

def read_data(FILE_PATH: str = INPUT_DATA) -> list[str]:
    with open(FILE_PATH, 'r') as file:
        lines = file.readlines()
    return lines

def write_data(FILE_PATH: str, lines: list[str]) -> None:
    with open(FILE_PATH, 'w') as file:
        file.writelines(lines)

def get_data() -> Tuple[List[str], List[str]]:
    return read_data(INPUT_DATA), read_data(OUTPUT_DATA)
