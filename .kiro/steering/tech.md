# Technology Stack

## Platform & Tools
- Platform: Appian Low-Code Development Platform
- Language: Appian Expression Language (EL)
- IDE: Appian Designer or compatible editor with EL support
- Snippets: Custom Appian EL code snippets for development efficiency

## Core Appian Technologies
- Expression Language (EL): Primary development language
- Record Types: Data modeling and queries
- Process Models: Workflow automation
- Interfaces: User interface development
- Integrations: External system connectivity

## Key Appian Functions
Reference the comprehensive snippets file for all patterns:
#[[file:appian-functions-complete.json]]

Original sample file:
#[[file:appian-el_v0.0.1.json]]

### Essential Functions
- `a!forEach()`: List iteration with fv!item and fv!index
- `a!localVariables()`: Variable scoping and management
- `a!queryRecordType()`: Data retrieval from Record Types
- `a!pagingInfo()`: Pagination and sorting configuration
- `ri!`: Rule input references
- `fv!`: Feature variable references (context-specific)

## Appian EL Code Style Guidelines
- Use descriptive variable names with `local!` prefix
- Leverage `a!forEach()` for list operations with meaningful expressions
- Always specify proper paging configuration for queries
- Use `ri!` for rule inputs and `fv!` for contextual variables
- Structure complex expressions with `a!localVariables()` for readability
- Include comments for business logic explanations
- Follow Appian naming conventions for consistency

## Development Workflow
- Use provided snippets for faster development
- Test expressions in Appian Designer expression editor
- Validate data queries with appropriate filters and paging
- Ensure proper error handling in expressions

*Note: This project focuses on Appian Expression Language development patterns.*