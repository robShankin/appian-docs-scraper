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

### Original Sample
- `appian-el_v0.0.1.json` - Initial sample snippets file

### Development Tools
- `scrape_appian_docs.py` - Main scraper script
- `requirements.txt` - Python dependencies
- `setup.py` - Environment setup script

### Testing & Debug Scripts
- `test_function_types.py` - Analyze function type distribution
- `test_single_function.py` - Test individual function processing
- `final_test.py` - Quality verification
- `debug_*.py` - Various debugging utilities

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
├── appian-functions-complete.json     # Main output (713 functions)
├── appian-el_v0.0.1.json             # Original sample
├── scrape_appian_docs.py             # Main scraper
├── requirements.txt                   # Dependencies
├── setup.py                          # Setup script
├── test_*.py                         # Testing utilities
├── debug_*.py                        # Debug scripts
└── .kiro/                            # AI assistant steering
    └── steering/
        ├── product.md                # Project objectives
        ├── tech.md                   # Technology stack
        └── structure.md              # Project organization
```

## Success Metrics

✅ **Complete coverage**: All 713 documented functions processed  
✅ **High quality**: Proper parameter extraction with types  
✅ **Format compliance**: Matches original snippet format exactly  
✅ **Error resilience**: Handles malformed pages gracefully  
✅ **Type distinction**: Correctly identifies a! vs regular functions  

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

**Generated**: December 15, 2025
**Appian Version**: 25.4
**Total Functions**: 713
**GitHub**: https://github.com/robShankin/appian-docs-scraper