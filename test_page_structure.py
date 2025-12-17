#!/usr/bin/env python3
"""
Test script to examine the structure of the Appian documentation page
"""

import requests
from bs4 import BeautifulSoup


def analyze_page_structure():
    url = "https://docs.appian.com/suite/help/25.4/Appian_Functions.html"

    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        print(f"Page title: {soup.title.string if soup.title else 'No title'}")
        print(f"Page length: {len(response.text)} characters")

        # Look for function-related content
        print("\n=== Links containing 'function' ===")
        function_links = soup.find_all('a', href=True)
        count = 0
        for link in function_links[:20]:  # First 20 links
            href = link.get('href', '')
            text = link.get_text(strip=True)
            if 'function' in href.lower() or text.startswith('a!'):
                print(f"Link: {text} -> {href}")
                count += 1

        print(f"\nFound {count} function-related links in first 20")

        # Look for common HTML structures
        print("\n=== Page structure analysis ===")
        print(f"Tables: {len(soup.find_all('table'))}")
        print(f"Lists (ul/ol): {len(soup.find_all(['ul', 'ol']))}")
        print(f"Code blocks: {len(soup.find_all(['code', 'pre']))}")
        print(f"Divs: {len(soup.find_all('div'))}")

        # Look for specific patterns
        print("\n=== Content patterns ===")
        a_functions = soup.find_all(text=lambda text: text and 'a!' in text)
        print(f"Text containing 'a!': {len(a_functions)} instances")

        if a_functions:
            print("First few 'a!' instances:")
            for func in a_functions[:5]:
                clean_text = ' '.join(func.strip().split())
                if len(clean_text) < 100:
                    print(f"  - {clean_text}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    analyze_page_structure()
