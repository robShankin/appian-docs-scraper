#!/usr/bin/env python3
"""
Final test before full scrape
"""

import json
from scrape_appian_docs import AppianDocScraper
import sys
sys.path.append('.')


def final_test():
    scraper = AppianDocScraper()

    # Test with functions we know work
    test_case = {
        'name': 'append()',
        'url': 'https://docs.appian.com/suite/help/25.4/fnc_array_append.html',
        'description': 'Test function'
    }

    print("=== Final Test ===")

    detailed_info = scraper.scrape_function_details(test_case)
    snippet = scraper.generate_snippet(detailed_info)

    print("Generated snippet:")
    print(json.dumps(snippet, indent=2))

    # Check quality
    body = snippet.get('body', [])
    has_params = len(detailed_info.get('parameters', [])) > 0

    print(f"\nQuality check:")
    print(f"✓ Parameters found: {len(detailed_info.get('parameters', []))}")
    print(f"✓ Body lines: {len(body)}")
    print(f"✓ Prefixes: {len(snippet.get('prefix', []))}")
    print(f"✓ Description: {snippet.get('description', 'None')}")

    # Check for issues
    body_text = ' '.join(body)
    issues = []

    # Check for malformed parameters (braces outside of tabstops)
    import re
    # Remove valid tabstops like ${1:...}
    cleaned_body = re.sub(r'\$\{\d+:[^}]+\}', '', body_text)
    if '{' in cleaned_body and '}' in cleaned_body:
        issues.append("Malformed parameters detected")

    if not snippet.get('prefix'):
        issues.append("No prefixes")

    if len(body) < 3:
        issues.append("Body too short")

    if issues:
        print(f"\n⚠ Issues: {', '.join(issues)}")
        return False
    else:
        print(f"\n✓ Quality looks good!")
        return True


if __name__ == "__main__":
    success = final_test()
    print(f"\n{'Ready for full scrape!' if success else 'Need to fix issues first'}")
