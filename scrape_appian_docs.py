#!/usr/bin/env python3
"""
Appian Documentation Scraper
Extracts all Appian functions from the official documentation and generates VS Code snippets.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse


class AppianDocScraper:
    def __init__(self, base_url: str = "https://docs.appian.com/suite/help/25.4/Appian_Functions.html"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.functions = {}

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page."""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_function_info(self, soup: BeautifulSoup) -> Dict:
        """Extract function information from the main functions page."""
        functions = {}

        # Look for all links that could be functions
        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)

            # Filter for Appian functions
            if (text.startswith('a!') or
                'fnc_' in href or
                    (text.endswith('()') and len(text) > 3)):

                # Clean up function name
                function_name = text.replace(' [Deprecated]', '').strip()
                if not function_name.endswith('()'):
                    function_name += '()'

                full_url = urljoin(self.base_url, href)
                functions[function_name] = {
                    'name': function_name,
                    'url': full_url,
                    'description': self._get_function_description(link),
                    'deprecated': '[Deprecated]' in text
                }

        return functions

    def _get_function_description(self, link_element) -> str:
        """Extract description text near the function link."""
        # Look for description in nearby elements
        parent = link_element.parent
        if parent:
            desc = parent.get_text(strip=True)
            return desc[:200] + "..." if len(desc) > 200 else desc
        return ""

    def scrape_function_details(self, function_info: Dict) -> Dict:
        """Scrape detailed information for a specific function."""
        soup = self.fetch_page(function_info['url'])
        if not soup:
            return function_info

        # Extract function signature
        signature = self._extract_signature(soup)
        parameters = self._extract_parameters(soup)
        examples = self._extract_examples(soup)

        function_info.update({
            'signature': signature,
            'parameters': parameters,
            'examples': examples
        })

        return function_info

    def _extract_signature(self, soup: BeautifulSoup) -> str:
        """Extract function signature from the documentation."""
        # Look for main content area
        main_content = soup.find('main') or soup.find(
            'div', class_='content') or soup

        # Look for syntax section first
        syntax_headings = main_content.find_all(
            string=lambda text: text and 'syntax' in text.lower())
        for heading in syntax_headings:
            parent = heading.parent if hasattr(heading, 'parent') else heading
            if parent:
                code_block = parent.find_next(['code', 'pre'])
                if code_block:
                    signature = code_block.get_text(strip=True)
                    if '(' in signature and len(signature) < 200:
                        return signature.split('\n')[0]  # First line

        # Fallback: look for code blocks containing function name
        code_blocks = main_content.find_all(['code', 'pre'])
        for block in code_blocks[:5]:  # Check first 5 code blocks
            text = block.get_text(strip=True)
            # Look for function calls (contains parentheses and reasonable length)
            if '(' in text and ')' in text and len(text) < 100:
                lines = text.split('\n')
                for line in lines:
                    if '(' in line and ')' in line:
                        return line.strip()

        return ""

    def _extract_parameters(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract parameter information."""
        parameters = []

        # Look for main content area to avoid footer elements
        main_content = soup.find('main') or soup.find(
            'div', class_='content') or soup

        # Look for parameter tables in main content
        tables = main_content.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue

            # Check if this is a parameter table by looking at headers
            header_row = rows[0]
            header_cells = header_row.find_all(['th', 'td'])
            header_text = ' '.join(
                [cell.get_text(strip=True).lower() for cell in header_cells])

            # Only process tables that look like parameter tables
            if 'keyword' in header_text or ('type' in header_text and 'description' in header_text):
                for row in rows[1:]:  # Skip header
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:  # Keyword, Type, Description
                        param_name = cells[0].get_text(strip=True)
                        param_type = cells[1].get_text(strip=True)
                        param_desc = cells[2].get_text(strip=True)

                        # Filter out invalid parameters
                        if (param_name and
                            param_name not in ['Keyword', 'Parameter', 'Name', 'Disclaimer', 'Privacy'] and
                                len(param_name) < 50):  # Reasonable parameter name length
                            parameters.append({
                                'name': param_name,
                                'type': param_type,
                                # Limit description length
                                'description': param_desc[:100]
                            })
                break  # Only process the first valid parameter table

        return parameters

    def _extract_examples(self, soup: BeautifulSoup) -> List[str]:
        """Extract code examples."""
        examples = []

        # Look for example sections
        example_sections = soup.find_all(
            text=re.compile(r'example', re.IGNORECASE))
        for section in example_sections:
            parent = section.parent
            if parent:
                # Find code blocks near example text
                code_blocks = parent.find_next_siblings(['pre', 'code'])
                for block in code_blocks[:2]:  # Limit to first 2 examples
                    example_text = block.get_text(strip=True)
                    if example_text and 'a!' in example_text:
                        examples.append(example_text)

        return examples

    def generate_snippet(self, func_info: Dict) -> Dict:
        """Generate VS Code snippet from function information."""
        name = func_info['name']

        # Determine if this is an a! domain function or regular function
        is_a_function = name.startswith('a!')

        # Create snippet body based on parameters (preferred) or signature
        parameters = func_info.get('parameters', [])
        if parameters:
            body = self._create_basic_body(name, parameters, is_a_function)
        elif func_info.get('signature'):
            body = self._create_body_from_signature(func_info['signature'])
        else:
            body = self._create_basic_body(name, [], is_a_function)

        # Create prefixes based on function type
        if is_a_function:
            # a! domain function
            prefixes = [name, name[2:]]  # e.g., ["a!forEach", "forEach"]
            function_type = "a! domain"
        else:
            # Regular function (fn! domain)
            clean_name = name.replace('()', '')
            prefixes = [name, clean_name]  # e.g., ["append()", "append"]
            function_type = "fn! domain"

        return {
            "prefix": prefixes,
            "body": body,
            "description": f"{name}: {func_info.get('description', f'Appian {function_type} function')}"
        }

    def _create_body_from_signature(self, signature: str) -> List[str]:
        """Create snippet body from function signature."""
        # Don't parse signatures as they contain examples, not parameter names
        # Just create a simple function call
        if '(' in signature and ')' in signature:
            func_name = signature.split('(')[0].strip()
            return [
                f"{func_name}(",
                "  ${1:/* parameters */}",
                ")"
            ]
        else:
            return [signature]

    def _create_basic_body(self, name: str, parameters: List[Dict], is_a_function: bool = True) -> List[str]:
        """Create basic snippet body."""
        # Remove () from name for the function call
        clean_name = name.replace('()', '')

        lines = [f"{clean_name}("]

        if parameters:
            for i, param in enumerate(parameters[:5], 1):  # Limit to 5 params
                param_name = param['name']
                param_type = param.get('type', 'value')

                # Create a more descriptive placeholder
                if param_type and param_type != 'value':
                    placeholder = f"{param_name} ({param_type})"
                else:
                    placeholder = param_name

                lines.append(f"  {param_name}: ${{{i}:{placeholder}}},")

            # Remove trailing comma from last parameter
            if lines[-1].endswith(','):
                lines[-1] = lines[-1][:-1]
        else:
            # No parameters found, add a generic placeholder
            lines.append(f"  ${{1:/* parameters */}}")

        lines.append(")")
        return lines

    def run(self) -> Dict:
        """Main scraping process."""
        print("Starting Appian documentation scraping...")

        # Fetch main page
        soup = self.fetch_page(self.base_url)
        if not soup:
            print("Failed to fetch main page")
            return {}

        # Extract function list
        print("Extracting function list...")
        functions = self.extract_function_info(soup)
        print(f"Found {len(functions)} functions")

        # Scrape details for each function (limit for testing)
        snippets = {}
        for i, (name, info) in enumerate(functions.items()):
            if i >= 713:  # Process all functions
                break

            print(f"Processing {name}...")
            detailed_info = self.scrape_function_details(info)
            snippet = self.generate_snippet(detailed_info)
            snippets[f"Appian {name}"] = snippet

        return snippets


def main():
    scraper = AppianDocScraper()
    snippets = scraper.run()

    if snippets:
        # Save to JSON file
        output_file = "appian-functions-complete.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(snippets, f, indent=4, ensure_ascii=False)

        print(f"\nGenerated {len(snippets)} snippets")
        print(f"Saved to: {output_file}")
    else:
        print("No snippets generated")


if __name__ == "__main__":
    main()
