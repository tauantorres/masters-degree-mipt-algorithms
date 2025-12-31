from typing import (
    Any, List, Tuple,
    Callable, Optional,
)


INPUT_DATA: str = "./input.txt"
OUTPUT_DATA: str = "./output.txt"

COLORS = {
    "reset":   "\033[0m",
    "red":     "\033[31m",
    "green":   "\033[32m",
    "yellow":  "\033[33m",
    "blue":    "\033[34m",
    "magenta": "\033[35m",
    "cyan":    "\033[36m",
    "white":   "\033[37m",
}

def print_colored(text: str, color: str = "green") -> None:
    print(f"{COLORS.get(color.lower(), color)}{text}{COLORS['reset']}")

def log_colored(message: str, color: str = "green", with_space: bool = True) -> None:
    print(f"[{COLORS.get(color.lower(), color)}{message}{COLORS['reset']}]", end=' ' if with_space else '')

def prepare_raw_data(exercise_id: str, sample_number: int) -> None:
    
    raw_input_data: str = f"Data/{exercise_id}/inputs/{sample_number:02}.txt"
    raw_output_data: str = f"Data/{exercise_id}/outputs/{sample_number:02}.txt"

    input_lines: list[str] = read_data(raw_input_data)
    output_lines: list[str] = read_data(raw_output_data)

    write_data(FILE_PATH=INPUT_DATA, lines=input_lines)
    write_data(FILE_PATH=OUTPUT_DATA, lines=output_lines)

def read_data(FILE_PATH: str = INPUT_DATA) -> List[str]:
    try:
        with open(FILE_PATH, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"{log_colored('ERROR', 'red')} File not found: {FILE_PATH}")
        return []

def write_data(FILE_PATH: str, lines: list[str]) -> None:
    try:
        with open(FILE_PATH, 'w') as file:
            file.writelines(lines)
    except IOError as e:
        print(f"{log_colored('ERROR', 'red')} An error occurred while writing to the file: {FILE_PATH} | Error: {print_colored(str(e), 'yellow')}")

def get_data(exercise_id: str, sample_number: int, get_data_prepared: bool = False) -> Tuple[List[str], List[str]]:

    if get_data_prepared:
        prepare_raw_data(exercise_id=exercise_id, sample_number=sample_number)

    return read_data(INPUT_DATA), read_data(OUTPUT_DATA)

def _print_one_data_before_return(data: Any, log_message: str, message: str, color: str = "cyan") -> None:
    log_colored(log_message, color)
    print(f"{message}: {data}")

def print_data_before_return_function(contents: List[Tuple[Any, str]]) -> None:
    for data, (log_message, message, color) in contents:
        _print_one_data_before_return(data, log_message, message, color)

def prepare_data(
    exercise_id: str,
    sample_number: int,
    raw_data: bool = False,
    get_data_prepared: bool = True,
    print_data_before_return: bool = False,
    exercise_function_rules: Optional[Callable] = None,
) -> Tuple[Any, list[str]]:

    raw_input, raw_output = get_data(
        exercise_id=exercise_id,
        sample_number=sample_number,
        get_data_prepared=get_data_prepared,
    )

    if raw_data:
        if print_data_before_return:
            print_data_before_return_function([
                (raw_input, ('RAW INPUT DATA', 'Raw Input Data', 'cyan')),
                (raw_output, ('RAW OUTPUT DATA', 'Raw Output Data', 'cyan')),
            ])
        return raw_input, raw_output

    if exercise_function_rules is None:
        if print_data_before_return:
            print_data_before_return_function([
                ([''.join(raw_input).strip()], ('RAW INPUT DATA', 'Raw Input Data', 'cyan')),
                ([''.join(raw_output).strip()], ('RAW OUTPUT DATA', 'Raw Output Data', 'cyan')),
            ])
        return [''.join(raw_input).strip()], [''.join(raw_output).strip()]

    if print_data_before_return:
        processed_input = exercise_function_rules(raw_input)
        print_data_before_return_function([
            (processed_input, ('PROCESSED INPUT DATA', 'Processed Input Data', 'cyan')),
            (raw_output, ('RAW OUTPUT DATA', 'Raw Output Data', 'cyan')),
        ])

    return exercise_function_rules(raw_input), raw_output
