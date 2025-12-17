#!/usr/bin/env python3
"""
Test to find the correct URL patterns for functions
"""

import requests
from bs4 import BeautifulSoup


def test_url_patterns():
    # Get the main page to see actual URL patterns
    main_url = "https://docs.appian.com/suite/help/25.4/Appian_Functions.html"

    response = requests.get(main_url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })

    soup = BeautifulSoup(response.content, 'lxml')

    # Look for specific functions we're testing
    test_functions = ['a!forEach', 'now()', 'a!queryRecordType']

    all_links = soup.find_all('a', href=True)

    print("=== Finding correct URLs ===")
    for func in test_functions:
        print(f"\nLooking for {func}:")
        found = False
        for link in all_links:
            text = link.get_text(strip=True)
            href = link.get('href')

            if func.replace('()', '') in text.replace('()', ''):
                print(f"  Found: {text} -> {href}")
                found = True

        if not found:
            print(f"  Not found directly, checking partial matches...")
            for link in all_links[:20]:
                text = link.get_text(strip=True)
                href = link.get('href')
                if 'forEach' in text or 'now' in text or 'query' in text.lower():
                    print(f"    Maybe: {text} -> {href}")


if __name__ == "__main__":
    test_url_patterns()
