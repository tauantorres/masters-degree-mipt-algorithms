#!/usr/bin/env python3
"""
Manual HTML paste scraper for when URLs require authentication.

Usage:
1. Copy the HTML source from the contest page
2. Paste it into html_content variable below
3. Run: python manual_scraper.py <exercise_number>
"""

import sys
from scraper import YandexContestScraper


def manual_scrape(exercise_number: str, html_content: str):
    """Manually scrape from pasted HTML content."""
    scraper = YandexContestScraper()
    
    print(f"🔄 Processing HTML content for exercise {exercise_number}...")
    samples = scraper.extract_samples(html_content)
    
    if samples:
        print(f"✅ Found {len(samples)} samples!")
        
        for i, (input_text, output_text) in enumerate(samples, 1):
            scraper.save_sample_to_files(exercise_number, i, input_text, output_text)
        
        print(f"🎉 Exercise {exercise_number} samples saved successfully!")
        print(f"📁 Check Data/{exercise_number}/inputs/ and Data/{exercise_number}/outputs/")
        return True
    else:
        print("❌ No samples found in the provided HTML")
        return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python manual_scraper.py <exercise_number>")
        return
    
    exercise_number = sys.argv[1]
    
    print("📋 Manual HTML Scraper")
    print("=" * 50)
    print("Please paste the HTML content from the contest page below.")
    print("Press Ctrl+D (or Ctrl+Z on Windows) when finished:")
    print()
    
    # Read HTML content from stdin
    html_content = ""
    try:
        while True:
            line = input()
            html_content += line + "\n"
    except EOFError:
        pass
    
    if html_content.strip():
        manual_scrape(exercise_number, html_content)
    else:
        print("❌ No HTML content provided")


if __name__ == "__main__":
    main()