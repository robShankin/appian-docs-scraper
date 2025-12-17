# Project Structure

## Current Organization
```
.
├── README.md                          # Project documentation
├── appian-functions-complete.json     # ✅ MAIN OUTPUT: All 713 Appian functions
├── appian-el_v0.0.1.json             # Original sample snippets
├── scrape_appian_docs.py             # Main scraper script
├── requirements.txt                   # Python dependencies
├── setup.py                          # Environment setup
├── test_*.py                         # Quality testing scripts
├── debug_*.py                        # Development debugging tools
└── .kiro/
    └── steering/                     # AI assistant guidance documents
        ├── product.md                # Project overview and objectives
        ├── tech.md                   # Technology stack and commands
        └── structure.md              # Project organization (this file)
```

## Recommended Appian Project Structure
As the project develops, consider organizing Appian artifacts using these patterns:

### Appian Application Structure
```
expressions/               # Reusable expression rules
├── constants/            # Constant expressions and configurations
├── utilities/            # Helper functions and common logic
├── queries/              # Data query expressions
└── validations/          # Input validation rules

interfaces/               # User interface definitions
├── forms/                # Data entry forms
├── reports/              # Read-only data displays  
├── dashboards/           # Summary and analytics views
└── components/           # Reusable interface components

processes/                # Process model definitions
├── workflows/            # Business process flows
├── integrations/         # External system processes
└── utilities/            # Process utility models

records/                  # Record type definitions
├── entities/             # Core business entities
├── lookups/              # Reference data records
└── relationships/        # Record type relationships
```

### Development Assets
```
├── snippets/             # Code snippet collections
├── documentation/        # Technical documentation
├── examples/             # Sample implementations
└── templates/            # Reusable code templates
```

## Appian Naming Conventions
- Use camelCase for local variables: `local!myVariable`
- Use descriptive names for rule inputs: `ri!customerData`
- Use clear prefixes for different artifact types:
  - Constants: `CONST_` prefix (e.g., `CONST_MAX_RESULTS`)
  - Expressions: `EXP_` prefix (e.g., `EXP_CalculateTotal`)
  - Interfaces: `INT_` prefix (e.g., `INT_CustomerForm`)
  - Process Models: `PM_` prefix (e.g., `PM_OrderApproval`)
- Use meaningful names that describe business purpose
- Avoid abbreviations unless they're well-known business terms

## File Organization Rules
- Keep related files together
- Separate concerns into different directories
- Use index files for clean imports
- Place configuration files at project root
- Keep documentation up to date

*Note: Adapt this structure based on the chosen technology stack and project requirements.*