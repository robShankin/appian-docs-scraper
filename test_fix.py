#!/usr/bin/env python3
"""
Test script to verify the fix for the '1' prefix bug
Tests the _create_body_from_signature method with problematic signatures
"""

from scrape_appian_docs import AppianDocScraper


def test_signature_fix():
    """Test that signatures with numeric prefixes are handled correctly."""
    scraper = AppianDocScraper()

    # Test cases: signatures that caused the bug
    test_cases = [
        ("1now()", "now("),
        ("1today()", "today("),
        ("1timezone()", "timezone("),
        ("1timezoneid()", "timezoneid("),
        ("1infinity()", "infinity("),
        ("2today()", "today("),  # Different digit
        ("123test()", "test("),  # Multiple digits
        ("now()", "now("),  # Already correct
        ("a!forEach()", "a!forEach("),  # a! function (no digits)
    ]

    print("Testing _create_body_from_signature fix...\n")
    all_passed = True

    for signature, expected_func_start in test_cases:
        body = scraper._create_body_from_signature(signature)
        actual_func = body[0]  # First line of body

        if actual_func == expected_func_start:
            print(f"✓ PASS: '{signature}' -> '{actual_func}'")
        else:
            print(f"✗ FAIL: '{signature}' -> '{actual_func}' (expected '{expected_func_start}')")
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = test_signature_fix()
    exit(0 if success else 1)
