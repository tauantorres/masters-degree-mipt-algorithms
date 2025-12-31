#!/usr/bin/env python3
"""
Quick script to scrape Yandex Contest problems and save samples to exercise files.

Usage examples:
    python scrape_exercise.py https://contest.yandex.ru/contest/87640/problems/G/ 07
    python scrape_exercise.py 87640 G 07
"""

import sys
import os
from scraper import YandexContestScraper


def main():
    if len(sys.argv) < 3:
        print("❌ Not enough arguments!")
        print("\nUsage:")
        print("  # Using full URL:")
        print("  python scrape_exercise.py <URL> <exercise_number>")
        print("  python scrape_exercise.py https://contest.yandex.ru/contest/87640/problems/G/ 07")
        print("\n  # Using contest ID and problem letter:")
        print("  python scrape_exercise.py <contest_id> <problem_letter> <exercise_number>")
        print("  python scrape_exercise.py 87640 G 07")
        return
    
    scraper = YandexContestScraper()
    
    if len(sys.argv) == 3:
        # URL and exercise number
        url = sys.argv[1]
        exercise_number = sys.argv[2]
        
        if not url.startswith('http'):
            print("❌ First argument should be a valid URL when using 2 arguments")
            return
            
        success = scraper.scrape_problem(url, exercise_number)
        
    elif len(sys.argv) == 4:
        # Contest ID, problem letter, exercise number
        contest_id = sys.argv[1]
        problem_letter = sys.argv[2].upper()
        exercise_number = sys.argv[3]
        
        success = scraper.scrape_contest_problem(contest_id, problem_letter, exercise_number)
        
    else:
        print("❌ Too many arguments!")
        return
    
    if success:
        print(f"\n🎉 Exercise {exercise_number} samples saved successfully!")
        print(f"📁 Check the Data/{exercise_number}/inputs/ and Data/{exercise_number}/outputs/ folders")
    else:
        print("\n💥 Failed to scrape the exercise")


if __name__ == "__main__":
    main()