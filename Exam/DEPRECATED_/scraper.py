import os
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple


class YandexContestScraper:
    def __init__(self, base_data_path: str = "Data"):
        self.base_data_path = base_data_path
        self.session = requests.Session()
        # Add headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def fetch_page(self, url: str) -> str:
        """Fetch the HTML content of a page."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch page: {e}")

    def extract_samples(self, html_content: str) -> List[Tuple[str, str]]:
        """Extract sample inputs and outputs from the HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        samples = []

        # Debug: Print some info about what we found
        print("🔍 Searching for sample tables...")
        
        # Method 1: Look for the standard sample-tests class
        sample_tables = soup.find_all('table', class_='sample-tests')
        print(f"Found {len(sample_tables)} tables with class 'sample-tests'")
        
        # Method 2: If no tables found, look for any table containing "Input" and "Output" 
        if not sample_tables:
            print("🔍 Looking for tables with Input/Output headers...")
            all_tables = soup.find_all('table')
            print(f"Found {len(all_tables)} total tables on page")
            
            for table in all_tables:
                # Check if table has Input/Output headers
                headers = table.find_all(['th', 'td'])
                header_text = ' '.join([h.get_text().strip().lower() for h in headers])
                if ('input' in header_text and 'output' in header_text) or 'sample' in header_text.lower():
                    sample_tables.append(table)
                    print(f"✅ Found potential sample table with headers: {header_text[:100]}...")
        
        # Method 3: If still no luck, look for specific patterns
        if not sample_tables:
            print("🔍 Looking for pre tags with sample data...")
            # Look for patterns like "Sample 1", "Sample 2" etc.
            sample_headings = soup.find_all(['h3', 'h4', 'h5'], string=re.compile(r'Sample \d+'))
            print(f"Found {len(sample_headings)} sample headings")
            
            for heading in sample_headings:
                # Look for the table that follows this heading
                next_table = heading.find_next('table')
                if next_table:
                    sample_tables.append(next_table)
                    print(f"✅ Found table after sample heading")
        
        print(f"📊 Total sample tables to process: {len(sample_tables)}")
        
        for i, table in enumerate(sample_tables):
            try:
                print(f"Processing table {i+1}...")
                
                # Find the tbody section or just tr elements
                tbody = table.find('tbody')
                if tbody:
                    trs = tbody.find_all('tr')
                else:
                    trs = table.find_all('tr')
                
                print(f"  Found {len(trs)} rows in table")
                
                # Skip header row and find data row
                for tr in trs:
                    tds = tr.find_all('td')
                    if len(tds) >= 2:  # Should have at least input and output columns
                        print(f"  Processing row with {len(tds)} columns...")
                        
                        # Extract input (first td)
                        input_pre = tds[0].find('pre')
                        if input_pre:
                            input_text = input_pre.get_text().strip()
                        else:
                            input_text = tds[0].get_text().strip()
                        
                        # Extract output (second td) 
                        output_pre = tds[1].find('pre')
                        if output_pre:
                            output_text = output_pre.get_text().strip()
                        else:
                            output_text = tds[1].get_text().strip()
                        
                        # Only add if we have meaningful data
                        if input_text and output_text and len(input_text) > 0 and len(output_text) > 0:
                            print(f"  ✅ Extracted sample - Input: {len(input_text)} chars, Output: {len(output_text)} chars")
                            samples.append((input_text, output_text))
                            break  # Only take first data row from each table
                
            except Exception as e:
                print(f"  ⚠️ Failed to extract sample from table {i+1}: {e}")
                continue
        
        print(f"🎯 Final result: {len(samples)} samples extracted")
        
        # Debug: show first few characters of each sample
        for i, (inp, out) in enumerate(samples):
            print(f"  Sample {i+1} preview - Input: '{inp[:50]}...', Output: '{out[:20]}...'")
        
        return samples

    def save_sample_to_files(self, exercise_number: str, sample_number: int, input_text: str, output_text: str):
        """Save sample input and output to the appropriate files."""
        # Ensure exercise number is zero-padded
        exercise_dir = f"{self.base_data_path}/{exercise_number:02d}" if isinstance(exercise_number, int) else f"{self.base_data_path}/{exercise_number}"
        
        # Create directories if they don't exist
        input_dir = f"{exercise_dir}/inputs"
        output_dir = f"{exercise_dir}/outputs"
        
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Create file names (zero-padded)
        input_file = f"{input_dir}/{sample_number:02d}.txt"
        output_file = f"{output_dir}/{sample_number:02d}.txt"
        
        # Save input file
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(input_text)
            if not input_text.endswith('\n'):
                f.write('\n')
        
        # Save output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)
            if not output_text.endswith('\n'):
                f.write('\n')
        
        print(f"✅ Saved sample {sample_number} to {exercise_dir}/")

    def scrape_problem(self, url: str, exercise_number: str) -> bool:
        """Main method to scrape a problem and save all samples."""
        try:
            print(f"🌐 Fetching problem from: {url}")
            html_content = self.fetch_page(url)
            
            print("🔍 Extracting samples...")
            samples = self.extract_samples(html_content)
            
            if not samples:
                print("❌ No samples found on this page")
                return False
            
            print(f"📝 Found {len(samples)} sample(s)")
            
            # Save each sample
            for i, (input_text, output_text) in enumerate(samples, 1):
                self.save_sample_to_files(exercise_number, i, input_text, output_text)
            
            print(f"✨ Successfully scraped {len(samples)} samples for exercise {exercise_number}")
            return True
            
        except Exception as e:
            print(f"❌ Error scraping problem: {e}")
            return False

    def scrape_contest_problem(self, contest_id: str, problem_letter: str, exercise_number: str) -> bool:
        """Scrape a problem from contest ID and problem letter."""
        url = f"https://contest.yandex.ru/contest/{contest_id}/problems/{problem_letter}/"
        return self.scrape_problem(url, exercise_number)


def main():
    """Example usage of the scraper."""
    scraper = YandexContestScraper()
    
    # Example usage:
    # scraper.scrape_problem("https://contest.yandex.ru/contest/87640/problems/G/", "07")
    # or
    # scraper.scrape_contest_problem("87640", "G", "07")
    
    print("YandexContestScraper initialized!")
    print("Usage examples:")
    print('scraper.scrape_problem("https://contest.yandex.ru/contest/87640/problems/G/", "07")')
    print('scraper.scrape_contest_problem("87640", "G", "07")')


if __name__ == "__main__":
    main()