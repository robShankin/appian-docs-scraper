#!/usr/bin/env python3
"""
Debug the append() function specifically to understand parameter extraction
"""

import requests
from bs4 import BeautifulSoup


def debug_append_function():
    url = "https://docs.appian.com/suite/help/25.4/fnc_array_append.html"

    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })

    soup = BeautifulSoup(response.content, 'lxml')

    print("=== Debugging append() function ===")

    # Look for main content area
    main_content = soup.find('main') or soup.find(
        'div', class_='content') or soup
    print(f"Main content found: {main_content is not None}")

    # Look for parameter tables in main content
    tables = main_content.find_all('table')
    print(f"Found {len(tables)} tables in main content")

    for i, table in enumerate(tables):
        print(f"\n--- Table {i+1} ---")
        rows = table.find_all('tr')
        print(f"Rows: {len(rows)}")

        if len(rows) >= 2:
            # Check headers
            header_row = rows[0]
            header_cells = header_row.find_all(['th', 'td'])
            header_text = ' '.join(
                [cell.get_text(strip=True).lower() for cell in header_cells])
            print(f"Headers: {header_text}")

            # Check if this looks like a parameter table
            is_param_table = 'keyword' in header_text or (
                'type' in header_text and 'description' in header_text)
            print(f"Is parameter table: {is_param_table}")

            if is_param_table:
                print("Parameter rows:")
                for j, row in enumerate(rows[1:4]):  # First 3 data rows
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:
                        param_name = cells[0].get_text(strip=True)
                        param_type = cells[1].get_text(strip=True)
                        param_desc = cells[2].get_text(strip=True)
                        print(
                            f"  {j+1}. {param_name} | {param_type} | {param_desc[:50]}...")
                    else:
                        print(
                            f"  {j+1}. Row has {len(cells)} cells: {[cell.get_text(strip=True) for cell in cells]}")


if __name__ == "__main__":
    debug_append_function()
