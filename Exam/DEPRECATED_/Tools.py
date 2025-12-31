from typing import Tuple, List
from scraper import YandexContestScraper


INPUT_DATA: str = "./input.txt"
OUTPUT_DATA: str = "./output.txt"


def scrape_and_prepare_data(
    contest_url_or_id: str,
    problem_letter_or_number: str = None,
    exercise_number: str = "01",
    sample_number: int = 1
) -> None:
    """
    Scrape contest data and prepare it for use.
    
    Args:
        contest_url_or_id: Either full URL or contest ID
        problem_letter_or_number: Problem letter (if using contest ID) or exercise number (if using URL)
        exercise_number: Exercise number to save to (only when using contest_id)
        sample_number: Which sample to prepare (default: 1)
    
    Examples:
        # Using full URL
        scrape_and_prepare_data("https://contest.yandex.ru/contest/87640/problems/G/", exercise_number="07")
        
        # Using contest ID and problem letter
        scrape_and_prepare_data("87640", "G", "07")
    """
    scraper = YandexContestScraper()
    
    if contest_url_or_id.startswith('http'):
        # Full URL provided
        url = contest_url_or_id
        if problem_letter_or_number:
            exercise_num = problem_letter_or_number
        else:
            exercise_num = exercise_number
        
        success = scraper.scrape_problem(url, exercise_num)
    else:
        # Contest ID and problem letter provided
        contest_id = contest_url_or_id
        problem_letter = problem_letter_or_number
        
        if not problem_letter:
            raise ValueError("Problem letter is required when using contest ID")
        
        success = scraper.scrape_contest_problem(contest_id, problem_letter, exercise_number)
        exercise_num = exercise_number
    
    if success:
        # After scraping, prepare the specific sample
        prepare_raw_data(exercise_num, sample_number)
        print(f"✅ Scraped and prepared exercise {exercise_num}, sample {sample_number}")
    else:
        print(f"❌ Failed to scrape exercise data")


def prepare_raw_data(
    exercise_number: str,
    sample_number: int,
) -> None:
    
    raw_input_data: str = f"Data/{exercise_number}/inputs/{sample_number:02}.txt"
    raw_output_data: str = f"Data/{exercise_number}/outputs/{sample_number:02}.txt"

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


def get_data(
        exercise_number: str,
        sample_number: int,
        get_data_prepared: bool = False,
    ) -> Tuple[List[str], List[str]]:
    
    if not get_data_prepared:
        prepare_raw_data(exercise_number=exercise_number, sample_number=sample_number)

    return read_data(INPUT_DATA), read_data(OUTPUT_DATA)
