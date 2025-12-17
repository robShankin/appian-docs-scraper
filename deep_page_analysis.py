#!/usr/bin/env python3
"""
Deep analysis of a single function page to understand the real structure
"""

import requests
from bs4 import BeautifulSoup


def analyze_page_structure():
    # Test with a well-known function
    url = "https://docs.appian.com/suite/help/25.4/fnc_array_append.html"

    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })

    soup = BeautifulSoup(response.content, 'lxml')

    print("=== Full Page Structure Analysis ===")

    # Look for main content area
    main_content = soup.find('main') or soup.find(
        'div', class_='content') or soup.find('body')

    if main_content:
        print("Found main content area")

        # Look for headings to understand structure
        headings = main_content.find_all(['h1', 'h2', 'h3', 'h4'])
        print(f"\n--- Page Headings ---")
        for i, heading in enumerate(headings[:10]):
            print(f"{i+1}. {heading.name}: {heading.get_text(strip=True)}")

        # Look for code blocks
        print(f"\n--- Code Blocks ---")
        code_blocks = main_content.find_all(['code', 'pre'])
        for i, block in enumerate(code_blocks[:5]):
            text = block.get_text(strip=True)
            if len(text) < 100:
                print(f"{i+1}. {text}")

        # Look for tables in main content only
        print(f"\n--- Tables in Main Content ---")
        tables = main_content.find_all('table')
        for i, table in enumerate(tables[:3]):
            print(f"\nTable {i+1}:")
            rows = table.find_all('tr')[:5]  # First 5 rows
            for j, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                if cells:
                    row_text = " | ".join(
                        [cell.get_text(strip=True) for cell in cells[:3]])
                    print(f"  Row {j+1}: {row_text}")

        # Look for definition lists (dl, dt, dd)
        print(f"\n--- Definition Lists ---")
        dl_elements = main_content.find_all('dl')
        for i, dl in enumerate(dl_elements[:2]):
            print(f"\nDefinition List {i+1}:")
            terms = dl.find_all('dt')[:3]
            for term in terms:
                dt_text = term.get_text(strip=True)
                dd = term.find_next_sibling('dd')
                dd_text = dd.get_text(strip=True)[
                    :100] if dd else "No description"
                print(f"  {dt_text}: {dd_text}")

    # Look for specific sections
    print(f"\n--- Looking for 'Usage considerations' or 'Parameters' sections ---")

    # Find text containing "usage" or "parameter"
    usage_text = soup.find_all(string=lambda text: text and (
        'usage' in text.lower() or 'parameter' in text.lower()))
    for text in usage_text[:5]:
        parent = text.parent
        if parent and parent.name in ['h2', 'h3', 'h4']:
            print(f"Section found: {text.strip()}")

            # Look for content after this heading
            next_sibling = parent.find_next_sibling()
            if next_sibling:
                content = next_sibling.get_text(strip=True)[:200]
                print(f"  Content: {content}")


if __name__ == "__main__":
    analyze_page_structure()
