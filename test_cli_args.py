#!/usr/bin/env python3
"""
Test script to verify command-line argument parsing works correctly
"""

import subprocess
import sys


def test_help_command():
    """Test that --help works"""
    result = subprocess.run(
        ["python3", "scrape_appian_docs.py", "--help"],
        capture_output=True,
        text=True
    )

    if "usage:" in result.stdout and "--url" in result.stdout:
        print("✓ PASS: --help command works")
        return True
    else:
        print("✗ FAIL: --help command failed")
        return False


def test_url_parsing():
    """Test that custom URL is accepted (without actually scraping)"""
    # We can't do a full test without scraping, but we can check the script accepts the args
    result = subprocess.run(
        ["python3", "-c", """
import sys
sys.path.insert(0, '.')
from scrape_appian_docs import AppianDocScraper

# Test instantiation with custom URL
scraper = AppianDocScraper(base_url="https://example.com/test.html")
print(scraper.base_url)
"""],
        capture_output=True,
        text=True
    )

    if "https://example.com/test.html" in result.stdout:
        print("✓ PASS: Custom URL accepted by AppianDocScraper")
        return True
    else:
        print("✗ FAIL: Custom URL not working")
        print(f"  Output: {result.stdout}")
        print(f"  Error: {result.stderr}")
        return False


def test_default_url():
    """Test that default URL is set correctly"""
    result = subprocess.run(
        ["python3", "-c", """
import sys
sys.path.insert(0, '.')
from scrape_appian_docs import AppianDocScraper

scraper = AppianDocScraper()
print(scraper.base_url)
"""],
        capture_output=True,
        text=True
    )

    if "25.4/Appian_Functions.html" in result.stdout:
        print("✓ PASS: Default URL is set to Appian 25.4")
        return True
    else:
        print("✗ FAIL: Default URL not correct")
        print(f"  Output: {result.stdout}")
        return False


if __name__ == "__main__":
    print("Testing CLI argument functionality...\n")

    all_passed = True
    all_passed &= test_help_command()
    all_passed &= test_default_url()
    all_passed &= test_url_parsing()

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All CLI argument tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)

    sys.exit(0 if all_passed else 1)
