# Quick Start Guide

Get up and running with the Appian Documentation Scraper in 5 minutes.

## What This Does

This scraper:
1. Visits the official Appian documentation website
2. Extracts all function definitions (713 functions)
3. Generates VS Code snippet files with autocomplete information
4. Saves everything to JSON files you can use in your VS Code extension

**Time required:** 25-30 minutes for a full scrape

---

## Prerequisites

Before you start, make sure you have:

- [x] **Python 3.7 or higher** installed
- [x] **Internet connection** (to download Appian docs)
- [x] **5 GB free disk space** (for dependencies and output)

### Check Your Python Version

```bash
python3 --version
```

You should see something like `Python 3.9.6` or higher.

---

## Installation (3 Steps)

### Step 1: Clone the Repository

```bash
git clone https://github.com/robShankin/appian-docs-scraper.git
cd appian-docs-scraper
```

### Step 2: Install Dependencies

```bash
python3 setup.py
```

This installs:
- `requests` - for downloading web pages
- `beautifulsoup4` - for parsing HTML
- `lxml` - for fast HTML processing

**Expected output:**
```
Installing required packages...
✓ Requirements installed successfully
✓ All required modules available
✓ Setup complete!
```

### Step 3: Verify Installation

```bash
python3 scrape_appian_docs.py --help
```

If you see the help message, you're ready to go!

---

## Running the Scraper

### Default Usage (Appian 25.4)

```bash
python3 scrape_appian_docs.py
```

**What happens:**
1. Scraper connects to Appian docs (25.4 by default)
2. Finds all function pages
3. Extracts function details (parameters, descriptions, examples)
4. Generates VS Code snippets
5. Saves to `appian-functions-complete.json`

**Expected output:**
```
Starting Appian documentation scraping...
Fetching: https://docs.appian.com/suite/help/25.4/Appian_Functions.html
Extracting function list...
Found 713 functions
Processing a!forEach()...
Processing append()...
...
(25-30 minutes later)
...
Generated 713 snippets
Saved to: appian-functions-complete.json
```

### For a Different Appian Version

When Appian releases a new version (e.g., 25.5 or 26.0):

```bash
python3 scrape_appian_docs.py --url https://docs.appian.com/suite/help/26.0/Appian_Functions.html
```

**Pro tip:** Use a custom output file to avoid overwriting:

```bash
python3 scrape_appian_docs.py \
  --url https://docs.appian.com/suite/help/26.0/Appian_Functions.html \
  --output appian-26.0-functions.json
```

---

## Verifying Success

After the scraper finishes, check:

### 1. File Exists

```bash
ls -lh appian-functions-complete.json
```

**Expected:** File size around 300 KB

### 2. Function Count

```bash
python3 -c "import json; data = json.load(open('appian-functions-complete.json')); print(f'Total functions: {len(data)}')"
```

**Expected:** `Total functions: 713` (for Appian 25.4)

### 3. Sample Content

```bash
python3 -c "import json; data = json.load(open('appian-functions-complete.json')); print(list(data.keys())[0:3])"
```

**Expected:** List of function names like `['Appian a!forEach()', 'Appian append()', ...]`

---

## What To Do Next

### Option 1: Use with VS Code Extension

Copy the generated JSON to your extension:

```bash
cp appian-functions-complete.json /path/to/your/vscode-extension/
```

See the [Appian AEL AI Code Generator](https://github.com/robShankin/appian-ael-ai-generator) for integration details.

### Option 2: Inspect the Data

Open the JSON file to see the structure:

```bash
python3 -m json.tool appian-functions-complete.json | less
```

Each function has:
- `prefix` - Trigger words for autocomplete
- `body` - Code template with placeholders
- `description` - Function description

---

## Common Issues & Solutions

### Issue: "command not found: python3"

**Problem:** Python isn't installed or isn't in your PATH

**Solution:**
```bash
# macOS
brew install python3

# Windows
# Download from https://www.python.org/downloads/

# Linux
sudo apt-get install python3
```

### Issue: "ModuleNotFoundError: No module named 'bs4'"

**Problem:** Dependencies not installed

**Solution:**
```bash
python3 setup.py
# OR manually:
pip3 install -r requirements.txt
```

### Issue: "Permission denied (publickey)"

**Problem:** SSH authentication issue when cloning

**Solution:** Use HTTPS instead:
```bash
git clone https://github.com/robShankin/appian-docs-scraper.git
```

### Issue: Scraper hangs or times out

**Problem:** Network issues or Appian docs are down

**Solution:**
1. Check your internet connection
2. Try again later
3. Check if Appian docs are accessible: https://docs.appian.com
4. Increase timeout in scraper (line 28): `response = self.session.get(url, timeout=60)`

### Issue: "Generated 0 snippets"

**Problem:** Appian changed their documentation structure

**Solution:**
1. Check the URL is correct and accessible in your browser
2. Open an issue on GitHub with the URL you're trying to scrape
3. The scraper may need updates to handle new HTML structure

---

## Quick Reference

### Common Commands

```bash
# Default scrape (Appian 25.4)
python3 scrape_appian_docs.py

# Different version
python3 scrape_appian_docs.py --url https://docs.appian.com/suite/help/26.0/Appian_Functions.html

# Custom output file
python3 scrape_appian_docs.py --output my-functions.json

# Help
python3 scrape_appian_docs.py --help

# Test the fix
python3 test_fix.py
```

### File Locations

| File | Purpose |
|------|---------|
| `appian-functions-complete.json` | Main output - VS Code snippets |
| `appian-functions-docs.json` | Enriched docs (if using enhanced scraper) |
| `scrape_appian_docs.py` | Main scraper script |
| `requirements.txt` | Python dependencies |

### Useful Python One-Liners

```bash
# Count functions
python3 -c "import json; print(len(json.load(open('appian-functions-complete.json'))))"

# List all function names
python3 -c "import json; [print(k) for k in json.load(open('appian-functions-complete.json')).keys()]"

# Check for specific function
python3 -c "import json; print('now()' in str(json.load(open('appian-functions-complete.json'))))"
```

---

## When to Re-Run the Scraper

You should re-run the scraper when:

1. **New Appian version released** - Update `--url` parameter
2. **Appian adds new functions** - Documentation gets updated
3. **Bug fixes in the scraper** - Get corrected output
4. **Extension needs updated data** - Refresh your VS Code extension

**Frequency:** Typically when Appian releases quarterly updates (check https://docs.appian.com/suite/help/)

---

## Getting Help

- **Documentation issues:** Check the main [README.md](README.md)
- **Bug reports:** [Open an issue](https://github.com/robShankin/appian-docs-scraper/issues)
- **Questions:** See the main README or open a discussion on GitHub

---

**Ready to scrape?** Run `python3 scrape_appian_docs.py` and get a coffee. ☕

You'll have 713 Appian functions ready to use in ~30 minutes!
