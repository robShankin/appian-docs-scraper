#!/usr/bin/env python3
"""
Test the scraper on a single function to debug the issue
"""

from scrape_appian_docs import AppianDocScraper
import sys
sys.path.append('.')


def test_single_function():
    scraper = AppianDocScraper()

    # Test append() function specifically
    function_info = {
        'name': 'append()',
        'url': 'https://docs.appian.com/suite/help/25.4/fnc_array_append.html',
        'description': 'Appends values to an array',
        'deprecated': False
    }

    print("=== Testing append() function ===")
    print(f"Function info: {function_info}")

    # Scrape detailed info
    detailed_info = scraper.scrape_function_details(function_info)
    print(f"\nDetailed info: {detailed_info}")

    # Generate snippet
    snippet = scraper.generate_snippet(detailed_info)
    print(f"\nGenerated snippet:")
    import json
    print(json.dumps(snippet, indent=2))


if __name__ == "__main__":
    test_single_function()
