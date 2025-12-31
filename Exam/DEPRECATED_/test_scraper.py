#!/usr/bin/env python3
"""
Test the scraper with local HTML content.
"""

from scraper import YandexContestScraper
import os


def test_local_html():
    """Test the scraper with local HTML file."""
    scraper = YandexContestScraper()
    
    # Read the test HTML file
    html_file = "test_sample.html"
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("📖 Testing with local HTML content...")
        samples = scraper.extract_samples(html_content)
        
        if samples:
            print(f"✅ Found {len(samples)} samples!")
            
            # Save to exercise 07
            for i, (input_text, output_text) in enumerate(samples, 1):
                scraper.save_sample_to_files("07", i, input_text, output_text)
                
            print("🎉 Test completed successfully!")
        else:
            print("❌ No samples found in test HTML")
    else:
        print(f"❌ Test file {html_file} not found")


def test_html_from_string():
    """Test with HTML string directly from your example."""
    
    # This is a simplified version of the HTML structure from your example
    html_content = '''
<div class="problem-statement">
    <h3>Sample 1</h3>
    <table class="sample-tests">
        <thead>
            <tr>
                <th>Input</th>
                <th>Output</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><pre>2 8 1
0 0
? 0 2 0
? 0 2 1
+ 0 1
? 0 2 0
? 0 2 1
+ 1 1
? 0 2 0
? 0 2 1</pre></td>
                <td><pre>2
0
1
1
0
2</pre></td>
            </tr>
        </tbody>
    </table>
</div>
    '''
    
    scraper = YandexContestScraper()
    print("🧪 Testing with HTML string...")
    samples = scraper.extract_samples(html_content)
    
    if samples:
        print(f"✅ Found {len(samples)} samples!")
        
        # Save to exercise 08
        for i, (input_text, output_text) in enumerate(samples, 1):
            scraper.save_sample_to_files("08", i, input_text, output_text)
            
        print("🎉 String test completed successfully!")
        return True
    else:
        print("❌ No samples found in test string")
        return False


if __name__ == "__main__":
    print("🧪 Testing scraper functionality...\n")
    
    # Test with string first
    success = test_html_from_string()
    
    if success:
        print("\n" + "="*50)
        print("✅ Scraper is working correctly!")
        print("You can now use it with real contest URLs.")
        print("\nUsage examples:")
        print("python scrape_exercise.py 87640 G 07")
        print('python scrape_exercise.py "https://contest.yandex.ru/contest/87640/problems/G/" 07')
    else:
        print("\n❌ Scraper test failed - check the implementation")