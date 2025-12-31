# Contest Exercise Scraper

Automatically scrape sample inputs and outputs from Yandex Contest problems and save them to your exercise structure.

## Files Created

- **`scraper.py`** - Main scraping functionality
- **`scrape_exercise.py`** - Command-line interface for scraping
- **`manual_scraper.py`** - For when URLs require authentication
- **`test_scraper.py`** - Test the scraper functionality
- **`Tools.py`** - Enhanced with scraping capabilities
- **`example_usage.ipynb`** - Jupyter notebook examples

## Quick Start

### Method 1: Auto Scrape from URL

```bash
# Using contest ID and problem letter (recommended)
python scrape_exercise.py 87640 G 07

# Using full URL
python scrape_exercise.py "https://contest.yandex.ru/contest/87640/problems/G/" 07
```

### Method 2: Manual Scraping (for authenticated pages)

If the contest page requires login:

1. Open the contest page in your browser
2. Right-click → "View Page Source" 
3. Copy all the HTML content
4. Run the manual scraper:

```bash
python manual_scraper.py 09
```

5. Paste the HTML content and press Ctrl+D (or Ctrl+Z on Windows)

### Method 3: Using in Python/Jupyter

```python
from Tools import scrape_and_prepare_data, get_data

# Scrape and prepare data in one step
scrape_and_prepare_data("87640", "G", "07")

# Or work with already scraped data
input_data, output_data = get_data("07", 1)
```

## What It Does

1. **Scrapes the contest page** - Downloads HTML and extracts sample data
2. **Parses sample inputs/outputs** - Finds all test cases from the page  
3. **Saves to your structure** - Creates files in `Data/XX/inputs/` and `Data/XX/outputs/`
4. **Integrates with Tools.py** - Works seamlessly with your existing workflow

## File Structure Created

After scraping exercise 07 with 3 samples:

```
Data/
  07/
    inputs/
      01.txt  (Sample 1 input)
      02.txt  (Sample 2 input) 
      03.txt  (Sample 3 input)
    outputs/
      01.txt  (Sample 1 output)
      02.txt  (Sample 2 output)
      03.txt  (Sample 3 output)
```

## Enhanced Tools.py Usage

The enhanced `Tools.py` now includes scraping capabilities:

```python
from Tools import scrape_and_prepare_data, get_data

# Scrape and immediately prepare for use
scrape_and_prepare_data(
    contest_url_or_id="87640",
    problem_letter_or_number="G", 
    exercise_number="07",
    sample_number=1  # Which sample to prepare for immediate use
)

# This will:
# 1. Scrape all samples from the contest page
# 2. Save them to Data/07/inputs/ and Data/07/outputs/ 
# 3. Copy sample 1 to input.txt and output.txt for immediate use

# Regular usage (unchanged)
input_data, output_data = get_data("07", 1)
```

## Examples

### Example 1: Scrape REQ Problem

```bash
python scrape_exercise.py 87640 G 07
```

This will:
- Fetch `https://contest.yandex.ru/contest/87640/problems/G/`
- Extract all sample inputs and outputs
- Save to `Data/07/inputs/01.txt`, `Data/07/outputs/01.txt`, etc.

### Example 2: Manual Scraping

When the page requires authentication:

```bash
python manual_scraper.py 08
# Paste HTML content here
# Press Ctrl+D when done
```

### Example 3: In Jupyter Notebook

```python
# In your notebook
from Tools import scrape_and_prepare_data

# Scrape and prepare exercise 09 
scrape_and_prepare_data("87640", "H", "09")

# Now work on your solution
input_data, output_data = get_data("09", 1)

# Your solution code here...
```

## Features

- ✅ **Auto-detection** of sample inputs/outputs
- ✅ **Multiple sample support** (Sample 1, 2, 3, etc.)
- ✅ **Robust HTML parsing** with multiple fallback methods
- ✅ **Integration** with existing Tools.py
- ✅ **Manual mode** for authenticated pages
- ✅ **Debug output** to see what's happening
- ✅ **Error handling** and informative messages

## Troubleshooting

### "No samples found"

1. **Try manual scraping** - The page might require authentication
2. **Check the URL** - Make sure it's the correct problem page
3. **Run test** - `python test_scraper.py` to verify the scraper works

### Authentication Required

Use the manual scraper:
```bash
python manual_scraper.py <exercise_number>
```

### Wrong Data Format

The scraper extracts exactly what's on the page. If formatting is weird:
1. Check the original contest page
2. Manually edit the files in `Data/XX/inputs/` if needed

## Dependencies

```bash
pip install requests beautifulsoup4
```

## Tips

1. **Use contest ID + problem letter** instead of full URLs when possible
2. **Test with known working examples** first
3. **Keep your browser open** to the contest page for manual scraping
4. **Check Data/ folders** after scraping to verify the content looks right
5. **Use the debug output** to understand what the scraper is finding

## Integration with Your Workflow

This scraper integrates seamlessly with your existing setup:

1. **Same Tools.py interface** - `get_data()` works exactly the same
2. **Same file structure** - Uses your existing `Data/XX/inputs/outputs/` format  
3. **Same notebook workflow** - Just scrape once, then code as usual
4. **Additional convenience** - `scrape_and_prepare_data()` does everything in one step

Happy coding! 🚀