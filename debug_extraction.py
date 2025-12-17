#!/usr/bin/env python3
"""
Debug script to understand the actual page structure and improve extraction
"""

import requests
from bs4 import BeautifulSoup
import re


def debug_page_content():
    url = "https://docs.appian.com/suite/help/25.4/Appian_Functions.html"

    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })

    soup = BeautifulSoup(response.content, 'lxml')

    print("=== Looking for function patterns ===")

    # Find all links that might be functions
    all_links = soup.find_all('a', href=True)
    function_links = []

    for link in all_links:
        href = link.get('href', '')
        text = link.get_text(strip=True)

        # Look for Appian function patterns
        if (text.startswith('a!') or
            'fnc_' in href or
            'function' in href.lower() or
                text.endswith('()')):
            function_links.append((text, href))

    print(f"Found {len(function_links)} potential function links:")
    for i, (text, href) in enumerate(function_links[:20]):  # First 20
        print(f"{i+1:2d}. {text} -> {href}")

    # Look for different patterns
    print("\n=== Alternative patterns ===")

    # Look for code elements containing a!
    code_elements = soup.find_all(['code', 'tt'])
    a_functions = []
    for code in code_elements:
        text = code.get_text(strip=True)
        if text.startswith('a!') and '(' in text:
            a_functions.append(text)

    print(
        f"Found {len(set(a_functions))} unique 'a!' functions in code elements:")
    for func in sorted(set(a_functions))[:15]:  # First 15 unique
        print(f"  - {func}")

    # Look for table rows or list items
    print("\n=== Table/List structure ===")
    tables = soup.find_all('table')
    for i, table in enumerate(tables[:3]):  # First 3 tables
        rows = table.find_all('tr')
        print(f"Table {i+1}: {len(rows)} rows")
        for j, row in enumerate(rows[:5]):  # First 5 rows
            cells = row.find_all(['td', 'th'])
            if cells:
                first_cell = cells[0].get_text(strip=True)
                if 'a!' in first_cell:
                    print(f"  Row {j+1}: {first_cell}")


if __name__ == "__main__":
    debug_page_content()
