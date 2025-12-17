# Appian Documentation Scraper

A Python-based web scraper that extracts all Appian functions from the official documentation and generates comprehensive VS Code snippets.

## Project Overview

This project successfully scraped **713 Appian functions** from the official Appian 25.4 documentation and generated high-quality VS Code snippets for development efficiency.

**Used by:** [Appian Expression Language AI Code Generator](https://github.com/robShankin/appian-ael-ai-generator) - A VS Code extension that provides AI-powered code generation and autocomplete for Appian developers.

## Results

- **713 total functions processed**
- **402 a! domain functions** (e.g., `a!forEach`, `a!localVariables`, `a!queryRecordType`)
- **311 regular functions** (e.g., `append`, `length`, `concat`)
- **Complete parameter extraction** with type information
- **VS Code compatible format** with tabstops and prefixes

## Generated Files

### Main Output
- `appian-functions-complete.json` - Complete snippets file with all 713 Appian functions
- `appian-functions-docs.json` - Enriched function documentation for AI-driven code generation

### Original Sample
- `appian-el_v0.0.1.json` - Initial sample snippets file

### Development Tools
- `scrape_appian_docs.py` - Main scraper script
- `scrape_appian_docs_enhanced.py` - Enhanced version with additional features
- `requirements.txt` - Python dependencies
- `setup.py` - Environment setup script

### Testing & Debug Scripts
- `test_fix.py` - Regression test for numeric prefix bug fix
- `test_function_types.py` - Analyze function type distribution
- `test_single_function.py` - Test individual function processing
- `test_individual_pages.py` - Test scraping of individual function pages
- `test_page_structure.py` - Validate HTML page structure
- `test_correct_urls.py` - Verify function URL extraction
- `test_edge_cases.py` - Test edge cases and error handling
- `final_test.py` - Quality verification
- `debug_append_function.py` - Debug specific function extraction
- `debug_extraction.py` - Debug parameter extraction logic
- `deep_page_analysis.py` - Analyze page structure in detail

## Usage

### Setup
```bash
python3 setup.py
```

### Run Full Scraper
```bash
python3 scrape_appian_docs.py
```

### Test Quality
```bash
python3 test_function_types.py
```

## Snippet Format

Each function generates a VS Code snippet with:

```json
{
  "prefix": ["functionName()", "functionName"],
  "body": [
    "functionName(",
    "  parameter: ${1:parameter (Type)},",
    "  value: ${2:value (Type)}",
    ")"
  ],
  "description": "functionName(): Brief description"
}
```

## Key Features

- **Intelligent parameter extraction** from documentation tables
- **Type information preservation** (e.g., "Any Type Array")
- **Function type distinction** between a! domain and regular functions
- **Error handling** for malformed pages and missing content
- **Quality validation** with comprehensive testing

## Technical Details

- **Source**: https://docs.appian.com/suite/help/25.4/Appian_Functions.html
- **Method**: BeautifulSoup HTML parsing with requests
- **Output**: VS Code snippet format (JSON)
- **Processing time**: ~25-30 minutes for full scrape

## Project Structure

```
.
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
│
├── appian-functions-complete.json     # Main output (713 functions)
├── appian-functions-docs.json         # Enriched documentation
├── appian-el_v0.0.1.json             # Original sample
│
├── scrape_appian_docs.py             # Main scraper
├── scrape_appian_docs_enhanced.py    # Enhanced scraper
├── requirements.txt                   # Dependencies
├── setup.py                          # Setup script
│
├── test_fix.py                       # Regression test for bug fix
├── test_function_types.py            # Function type analysis
├── test_single_function.py           # Single function test
├── test_individual_pages.py          # Page scraping test
├── test_page_structure.py            # HTML structure validation
├── test_correct_urls.py              # URL extraction test
├── test_edge_cases.py                # Edge case testing
├── final_test.py                     # Quality verification
│
├── debug_append_function.py          # Debug specific function
├── debug_extraction.py               # Debug parameter extraction
├── deep_page_analysis.py             # Page analysis
│
└── .kiro/                            # AI assistant steering
    └── steering/
        ├── product.md                # Project objectives
        ├── tech.md                   # Technology stack
        └── structure.md              # Project organization
```

## Success Metrics

✅ **Complete coverage**: All 713 documented functions processed
✅ **High quality**: Proper parameter extraction with types
✅ **Format compliance**: VS Code snippet format with proper syntax
✅ **Error resilience**: Handles malformed pages gracefully
✅ **Type distinction**: Correctly identifies a! vs regular functions

## Recent Fixes

### December 16, 2025 - Numeric Prefix Bug Fix
Fixed a bug where certain functions had numeric prefixes in snippet bodies:
- **Issue**: Functions like `now()`, `today()`, `timezone()`, `timezoneid()`, and `infinity()` were generated with "1" prefix (e.g., `1now()`)
- **Root Cause**: Signature extraction captured arithmetic examples from documentation (e.g., `1*now()`)
- **Solution**: Strip leading digits from extracted function names in `_create_body_from_signature()` method
- **Status**: ✅ Fixed - All tests passing
- **Note**: Regenerate JSON files by running `python3 scrape_appian_docs.py` to get corrected output

See commit [b8d60b9](https://github.com/robShankin/appian-docs-scraper/commit/b8d60b9) for details.

## Integration with VS Code Extension

The generated JSON files from this scraper are used by the [Appian Expression Language AI Code Generator](https://github.com/robShankin/appian-ael-ai-generator) VS Code extension:

- `appian-functions-complete.json` - Provides autocomplete snippets for all 713 functions
- `appian-functions-docs.json` - Powers the AI-driven code generation with enriched documentation
- Used in the extension's function reference viewer and intelligent prompt builder

## Future Enhancements

- Update for new Appian versions
- Add function categories/grouping
- Include usage examples in snippets
- Generate additional IDE formats (IntelliJ, etc.)
- Automated scraping pipeline for version updates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Initial Scrape**: December 15, 2025
**Last Updated**: December 16, 2025
**Appian Version**: 25.4
**Total Functions**: 713
**GitHub**: https://github.com/robShankin/appian-docs-scraper
**License**: MIT