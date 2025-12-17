#!/usr/bin/env python3
"""
Test edge cases and high-risk scenarios before full scrape
"""

import json
from scrape_appian_docs import AppianDocScraper
import sys
sys.path.append('.')


def test_edge_cases():
    scraper = AppianDocScraper()

    # Test cases that might break
    test_cases = [
        # Complex a! function
        {
            'name': 'a!forEach()',
            'url': 'https://docs.appian.com/suite/help/25.4/fnc_looping_a_forEach.html',
            'description': 'Complex a! function with multiple parameters'
        },
        # Function with no parameters
        {
            'name': 'now()',
            'url': 'https://docs.appian.com/suite/help/25.4/fnc_date_and_time_now.html',
            'description': 'Function with no parameters'
        },
        # Function that might have broken page
        {
            'name': 'length()',
            'url': 'https://docs.appian.com/suite/help/25.4/fnc_array_length.html',
            'description': 'Simple function'
        },
        # Complex function name
        {
            'name': 'a!queryRecordType()',
            'url': 'https://docs.appian.com/suite/help/25.4/fnc_system_a_queryrecordtype.html',
            'description': 'Complex query function'
        }
    ]

    results = {}

    for i, test_case in enumerate(test_cases):
        print(f"\n=== Test {i+1}: {test_case['name']} ===")

        try:
            # Test the scraping
            detailed_info = scraper.scrape_function_details(test_case)
            snippet = scraper.generate_snippet(detailed_info)

            # Check for common issues
            issues = []

            # Check if body is reasonable
            body = snippet.get('body', [])
            if len(body) < 2:
                issues.append("Body too short")

            # Check for malformed parameters
            body_text = ' '.join(body)
            if '{' in body_text and '}' in body_text and 'array' not in test_case['name']:
                issues.append(
                    "Possible malformed parameters (contains braces)")

            # Check prefix
            prefixes = snippet.get('prefix', [])
            if not prefixes or not any(test_case['name'].replace('()', '') in p for p in prefixes):
                issues.append("Missing or incorrect prefixes")

            # Check description
            desc = snippet.get('description', '')
            if not desc or desc == f"{test_case['name']}: {test_case['name']}":
                issues.append("Poor description")

            results[test_case['name']] = {
                'success': True,
                'issues': issues,
                'parameters_found': len(detailed_info.get('parameters', [])),
                'signature_found': bool(detailed_info.get('signature')),
                'snippet': snippet
            }

            print(
                f"✓ Success - {len(detailed_info.get('parameters', []))} params, signature: {bool(detailed_info.get('signature'))}")
            if issues:
                print(f"⚠ Issues: {', '.join(issues)}")

        except Exception as e:
            print(f"✗ Failed: {e}")
            results[test_case['name']] = {
                'success': False,
                'error': str(e)
            }

    # Summary
    print(f"\n=== Summary ===")
    successful = sum(1 for r in results.values() if r.get('success', False))
    total_issues = sum(len(r.get('issues', [])) for r in results.values())

    print(f"Successful: {successful}/{len(test_cases)}")
    print(f"Total issues: {total_issues}")

    if total_issues > 0:
        print("\nIssues found:")
        for name, result in results.items():
            if result.get('issues'):
                print(f"  {name}: {', '.join(result['issues'])}")

    # Show one good example
    print(f"\n=== Example Good Snippet ===")
    good_example = next((r for r in results.values() if r.get(
        'success') and not r.get('issues')), None)
    if good_example:
        print(json.dumps(good_example['snippet'], indent=2))

    return successful == len(test_cases) and total_issues < 3


if __name__ == "__main__":
    success = test_edge_cases()
    print(
        f"\n{'✓ Ready for full scrape!' if success else '⚠ Consider fixing issues first'}")
