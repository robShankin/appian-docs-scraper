#!/usr/bin/env python3
"""
Setup script for the Appian documentation scraper
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required Python packages."""
    try:
        print("Installing required packages...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False


def test_imports():
    """Test if all required modules can be imported."""
    try:
        import requests
        import bs4
        import lxml
        print("✓ All required modules available")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def main():
    print("=== Appian Documentation Scraper Setup ===")

    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt not found")
        return

    # Install requirements
    if not install_requirements():
        return

    # Test imports
    if not test_imports():
        return

    print("\n✓ Setup complete! You can now run:")
    print("  python test_page_structure.py  # Test page structure")
    print("  python scrape_appian_docs.py   # Run full scraper")


if __name__ == "__main__":
    main()
