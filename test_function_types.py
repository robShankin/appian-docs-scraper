#!/usr/bin/env python3
"""
Test script to verify a! vs fn! function distinction
"""

import json


def analyze_function_types():
    """Analyze the generated snippets to see function type distribution."""

    try:
        with open('appian-functions-complete.json', 'r') as f:
            snippets = json.load(f)

        a_functions = []
        regular_functions = []

        for key, snippet in snippets.items():
            # Check the first prefix to determine type
            first_prefix = snippet['prefix'][0] if snippet['prefix'] else ''

            if first_prefix.startswith('a!'):
                a_functions.append(first_prefix)
            else:
                regular_functions.append(first_prefix)

        print(f"=== Function Type Analysis ===")
        print(f"Total snippets: {len(snippets)}")
        print(f"a! domain functions: {len(a_functions)}")
        print(f"Regular functions (fn! domain): {len(regular_functions)}")

        print(f"\n=== Sample a! functions ===")
        for func in sorted(a_functions)[:10]:
            print(f"  - {func}")

        print(f"\n=== Sample regular functions ===")
        for func in sorted(regular_functions)[:10]:
            print(f"  - {func}")

        # Show a complete example of each type
        print(f"\n=== Example a! function snippet ===")
        a_example = next((v for k, v in snippets.items()
                         if v['prefix'][0].startswith('a!')), None)
        if a_example:
            print(json.dumps(a_example, indent=2))

        print(f"\n=== Example regular function snippet ===")
        reg_example = next((v for k, v in snippets.items()
                           if not v['prefix'][0].startswith('a!')), None)
        if reg_example:
            print(json.dumps(reg_example, indent=2))

    except FileNotFoundError:
        print("appian-functions-complete.json not found. Run the scraper first.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    analyze_function_types()
