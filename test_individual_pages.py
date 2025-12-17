#!/usr/bin/env python3
"""
Test individual function pages to understand their structure
"""

import requests
from bs4 import BeautifulSoup
import json


def test_function_page(url, function_name):
    """Test parsing of a single function page."""
    print(f"\n=== Testing {function_name} ===")
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        print(f"Page title: {soup.title.string if soup.title else 'No title'}")

        # Look for function syntax/signature
        print("\n--- Function Syntax ---")
        syntax_found = False

        # Look for syntax in various places
        syntax_patterns = [
            soup.find(
                'h2', string=lambda text: text and 'syntax' in text.lower()),
            soup.find(
                'h3', string=lambda text: text and 'syntax' in text.lower()),
            soup.find(string=lambda text: text and 'syntax' in text.lower())
        ]

        for pattern in syntax_patterns:
            if pattern:
                # Find code block after syntax heading
                parent = pattern.parent if hasattr(
                    pattern, 'parent') else pattern
                if parent:
                    code_block = parent.find_next(['code', 'pre'])
                    if code_block:
                        syntax_text = code_block.get_text(strip=True)
                        print(f"Found syntax: {syntax_text}")
                        syntax_found = True
                        break

        if not syntax_found:
            # Look for any code blocks containing the function name
            code_blocks = soup.find_all(['code', 'pre'])
            for block in code_blocks[:3]:
                text = block.get_text(strip=True)
                if function_name.replace('()', '') in text and '(' in text:
                    print(f"Code block: {text}")
                    break

        # Look for parameters
        print("\n--- Parameters ---")
        param_found = False

        # Look for parameter tables
        tables = soup.find_all('table')
        for table in tables:
            headers = table.find_all(['th', 'td'])
            header_text = ' '.join(
                [h.get_text(strip=True).lower() for h in headers[:3]])

            if 'parameter' in header_text or 'name' in header_text:
                print("Found parameter table:")
                # Skip header, limit to 5 rows
                rows = table.find_all('tr')[1:6]
                for i, row in enumerate(rows):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        param_name = cells[0].get_text(strip=True)
                        param_desc = cells[1].get_text(strip=True)[:100]
                        print(f"  {i+1}. {param_name}: {param_desc}")
                param_found = True
                break

        if not param_found:
            # Look for parameter lists
            param_headings = soup.find_all(
                string=lambda text: text and 'parameter' in text.lower())
            for heading in param_headings[:2]:
                parent = heading.parent if hasattr(
                    heading, 'parent') else heading
                if parent:
                    next_list = parent.find_next(['ul', 'ol', 'dl'])
                    if next_list:
                        items = next_list.find_all('li')[:3]
                        if items:
                            print("Found parameter list:")
                            for item in items:
                                print(f"  - {item.get_text(strip=True)[:100]}")
                            param_found = True
                            break

        # Look for examples
        print("\n--- Examples ---")
        example_found = False

        example_headings = soup.find_all(
            string=lambda text: text and 'example' in text.lower())
        for heading in example_headings[:2]:
            parent = heading.parent if hasattr(heading, 'parent') else heading
            if parent:
                code_block = parent.find_next(['code', 'pre'])
                if code_block:
                    example_text = code_block.get_text(strip=True)
                    if len(example_text) < 200:
                        print(f"Example: {example_text}")
                        example_found = True
                        break

        return {
            'syntax_found': syntax_found,
            'param_found': param_found,
            'example_found': example_found
        }

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    # Test a few different types of functions
    test_functions = [
        ("https://docs.appian.com/suite/help/25.4/fnc_array_a_flatten.html", "a!flatten()"),
        ("https://docs.appian.com/suite/help/25.4/fnc_array_append.html", "append()"),
        ("https://docs.appian.com/suite/help/25.4/fnc_array_a_update.html", "a!update()"),
        ("https://docs.appian.com/suite/help/25.4/fnc_array_length.html", "length()"),
    ]

    results = {}
    for url, func_name in test_functions:
        result = test_function_page(url, func_name)
        if result:
            results[func_name] = result

    print(f"\n=== Summary ===")
    for func, result in results.items():
        print(
            f"{func}: syntax={result['syntax_found']}, params={result['param_found']}, examples={result['example_found']}")


if __name__ == "__main__":
    main()
