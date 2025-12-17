#!/usr/bin/env python3
"""
Enhanced Appian Documentation Scraper
Extracts rich function documentation for AI-powered code generation.
Generates a companion file with detailed descriptions, examples, and metadata.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin

class EnhancedAppianDocScraper:
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

    def extract_function_list(self, soup: BeautifulSoup) -> Dict:
        """Extract function list from main page."""
        functions = {}
        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)

            # Filter for Appian functions
            if (text.startswith('a!') or
                'fnc_' in href or
                (text.endswith('()') and len(text) > 3)):

                function_name = text.replace(' [Deprecated]', '').strip()
                if not function_name.endswith('()'):
                    function_name += '()'

                full_url = urljoin(self.base_url, href)
                functions[function_name] = {
                    'name': function_name.replace('()', ''),
                    'url': full_url,
                    'deprecated': '[Deprecated]' in text
                }

        return functions

    def scrape_function_details(self, function_info: Dict) -> Dict:
        """Scrape detailed information for a specific function."""
        soup = self.fetch_page(function_info['url'])
        if not soup:
            return {
                'name': function_info['name'],
                'description': '',
                'parameters': {},
                'returnType': '',
                'examples': [],
                'category': 'Other'
            }

        main_content = soup.find('main') or soup.find('div', class_='content') or soup

        # Extract all the rich information we need
        description = self._extract_full_description(main_content)
        return_info = self._extract_return_type(main_content)
        parameters = self._extract_parameter_details(main_content)
        examples = self._extract_examples(main_content)
        use_case = self._extract_use_case(main_content, description)
        related_functions = self._extract_related_functions(main_content)
        category = self._categorize_function(function_info['name'], description)

        return {
            'name': function_info['name'],
            'description': description,
            'returnType': return_info.get('type', ''),
            'returnDescription': return_info.get('description', ''),
            'parameters': parameters,
            'examples': examples,
            'useCase': use_case,
            'relatedFunctions': related_functions,
            'category': category,
            'deprecated': function_info.get('deprecated', False)
        }

    def _extract_full_description(self, soup: BeautifulSoup) -> str:
        """Extract full function description (not truncated)."""
        # Skip common navigation/share elements
        skip_patterns = [
            'share', 'linkedin', 'reddit', 'email', 'copy', 'print',
            'privacy', 'disclaimer', '©', 'copyright',
            'see also', 'related', 'feedback'
        ]

        def is_valid_description(text: str) -> bool:
            """Check if text looks like a real description."""
            text_lower = text.lower()
            # Must be substantial
            if len(text) < 30:
                return False
            # Must not contain skip patterns
            if any(pattern in text_lower for pattern in skip_patterns):
                return False
            # Should contain actual words
            words = text.split()
            return len(words) > 5

        # Look for the main description paragraph (usually first p after h1)
        h1 = soup.find('h1')
        if h1:
            # Get the next few paragraphs
            description_parts = []
            for sibling in h1.find_next_siblings(['p', 'div'])[:10]:
                text = sibling.get_text(strip=True)
                if is_valid_description(text):
                    description_parts.append(text)
                    if len(description_parts) >= 2:  # Get first 2 meaningful paragraphs
                        break

            if description_parts:
                return ' '.join(description_parts)

        # Fallback: look for any early paragraph with substance
        paragraphs = soup.find_all('p', limit=20)
        for p in paragraphs:
            text = p.get_text(strip=True)
            if is_valid_description(text):
                return text

        return ''

    def _extract_return_type(self, soup: BeautifulSoup) -> Dict:
        """Extract return type and description."""
        result = {'type': '', 'description': ''}

        # Look for "Returns" section
        returns_heading = soup.find(string=re.compile(r'returns?', re.IGNORECASE))
        if returns_heading:
            parent = returns_heading.parent
            if parent:
                # Get the text after the heading
                next_elem = parent.find_next(['p', 'div', 'dd', 'td'])
                if next_elem:
                    text = next_elem.get_text(strip=True)
                    # Try to extract type from patterns like "Returns: Text" or "Text -"
                    type_match = re.match(r'^([\w\s]+?)(?:\s*-|\s*:)', text)
                    if type_match:
                        result['type'] = type_match.group(1).strip()
                        result['description'] = text[len(type_match.group(0)):].strip()
                    else:
                        result['description'] = text

        # Look in tables for return type
        if not result['type']:
            tables = soup.find_all('table')
            for table in tables:
                header_row = table.find('tr')
                if header_row:
                    headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
                    if 'return' in ' '.join(headers) or 'output' in ' '.join(headers):
                        data_rows = table.find_all('tr')[1:]
                        if data_rows:
                            cells = data_rows[0].find_all(['td', 'th'])
                            if cells:
                                result['type'] = cells[0].get_text(strip=True)
                                if len(cells) > 1:
                                    result['description'] = cells[1].get_text(strip=True)
                        break

        return result

    def _extract_parameter_details(self, soup: BeautifulSoup) -> Dict:
        """Extract detailed parameter information."""
        parameters = {}

        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue

            header_row = rows[0]
            header_cells = header_row.find_all(['th', 'td'])
            header_text = ' '.join([cell.get_text(strip=True).lower() for cell in header_cells])

            # Check if this is a parameter table
            if 'keyword' in header_text or ('type' in header_text and 'description' in header_text):
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        param_name = cells[0].get_text(strip=True)

                        # Filter out invalid parameters
                        if (param_name and
                            param_name not in ['Keyword', 'Parameter', 'Name', 'Disclaimer', 'Privacy'] and
                            len(param_name) < 50):

                            param_info = {
                                'type': cells[1].get_text(strip=True) if len(cells) > 1 else '',
                                'description': cells[2].get_text(strip=True) if len(cells) > 2 else ''
                            }

                            # Check if required (some docs indicate this)
                            if len(cells) > 3:
                                required_text = cells[3].get_text(strip=True).lower()
                                param_info['required'] = 'required' in required_text or 'yes' in required_text

                            parameters[param_name] = param_info
                break

        return parameters

    def _extract_examples(self, soup: BeautifulSoup) -> List[str]:
        """Extract code examples with better parsing."""
        examples = []

        # Look for example sections
        example_headings = soup.find_all(string=re.compile(r'example', re.IGNORECASE))

        for heading in example_headings:
            parent = heading.parent
            if parent:
                # Find code blocks near example heading
                for sibling in parent.find_next_siblings(['pre', 'code', 'div'])[:5]:
                    # Check for code blocks
                    code_blocks = sibling.find_all(['code', 'pre']) if sibling.name == 'div' else [sibling]

                    for block in code_blocks:
                        example_text = block.get_text(strip=True)
                        # Only include if it looks like actual code (has function calls)
                        if example_text and ('(' in example_text or 'a!' in example_text) and len(example_text) < 500:
                            # Clean up the example
                            example_text = re.sub(r'\s+', ' ', example_text)  # Normalize whitespace
                            if example_text not in examples:  # Avoid duplicates
                                examples.append(example_text)
                                if len(examples) >= 3:  # Limit to 3 examples
                                    return examples

        return examples

    def _extract_use_case(self, soup: BeautifulSoup, description: str) -> str:
        """Extract or infer the primary use case."""
        # Look for usage or use case sections
        use_case_headings = soup.find_all(string=re.compile(r'usage|use case|when to use', re.IGNORECASE))

        for heading in use_case_headings:
            parent = heading.parent
            if parent:
                next_p = parent.find_next('p')
                if next_p:
                    use_case = next_p.get_text(strip=True)
                    if len(use_case) > 20:
                        return use_case[:200]

        # Fallback: try to extract from description
        if description:
            # Look for sentences that explain purpose
            sentences = description.split('.')
            for sentence in sentences[:3]:
                if any(keyword in sentence.lower() for keyword in ['use', 'when', 'for', 'to']):
                    return sentence.strip() + '.'

        return ''

    def _extract_related_functions(self, soup: BeautifulSoup) -> List[str]:
        """Extract related or similar functions."""
        related = []

        # Look for "See also" or "Related" sections
        related_headings = soup.find_all(string=re.compile(r'see also|related|similar', re.IGNORECASE))

        for heading in related_headings:
            parent = heading.parent
            if parent:
                # Find links in the next few siblings
                for sibling in parent.find_next_siblings(['ul', 'p', 'div'])[:3]:
                    links = sibling.find_all('a')
                    for link in links:
                        func_name = link.get_text(strip=True)
                        if func_name and (func_name.startswith('a!') or '()' in func_name):
                            clean_name = func_name.replace('()', '').strip()
                            if clean_name not in related:
                                related.append(clean_name)
                                if len(related) >= 5:  # Limit to 5 related functions
                                    return related

        return related

    def _categorize_function(self, name: str, description: str) -> str:
        """Categorize the function based on name and description."""
        name_lower = name.lower()
        desc_lower = description.lower()

        # UI Components
        if name.startswith('a!') and any(term in name_lower for term in ['field', 'picker', 'layout', 'section', 'column', 'grid', 'chart', 'button', 'link', 'image']):
            return 'UI Components'

        # Array functions
        if any(term in name_lower for term in ['array', 'append', 'insert', 'remove', 'filter', 'map', 'reduce', 'flatten', 'union']) or \
           any(term in desc_lower for term in ['array', 'list', 'collection']):
            return 'Array Functions'

        # Text functions
        if any(term in name_lower for term in ['text', 'concat', 'split', 'trim', 'upper', 'lower', 'search', 'replace', 'char']) or \
           any(term in desc_lower for term in ['text', 'string', 'character']):
            return 'Text Functions'

        # Date/Time functions
        if any(term in name_lower for term in ['date', 'time', 'day', 'month', 'year', 'hour', 'minute', 'calendar', 'today', 'now']) or \
           any(term in desc_lower for term in ['date', 'time', 'calendar', 'timestamp']):
            return 'Date and Time Functions'

        # Data Query functions
        if any(term in name_lower for term in ['query', 'record', 'data', 'filter', 'aggregate', 'paginginfo']) or \
           'a!queryRecordType' in name or 'a!queryEntity' in name:
            return 'Data Query Functions'

        # Logic functions
        if any(term in name_lower for term in ['if', 'and', 'or', 'not', 'null', 'empty', 'match', 'choose']) or \
           any(term in desc_lower for term in ['condition', 'logic', 'boolean']):
            return 'Logic Functions'

        # Math functions
        if any(term in name_lower for term in ['sum', 'average', 'min', 'max', 'round', 'abs', 'power', 'sqrt', 'mod', 'rand']) or \
           any(term in desc_lower for term in ['mathematical', 'calculation', 'numeric']):
            return 'Math Functions'

        # Document functions
        if any(term in name_lower for term in ['document', 'folder', 'file', 'download', 'export']):
            return 'Document Functions'

        # Process functions
        if any(term in name_lower for term in ['process', 'task', 'node', 'activity']):
            return 'Process Functions'

        return 'Other Functions'

    def run(self, limit: Optional[int] = None) -> Dict:
        """Main scraping process."""
        print("Starting enhanced Appian documentation scraping...")

        # Fetch main page
        soup = self.fetch_page(self.base_url)
        if not soup:
            print("Failed to fetch main page")
            return {}

        # Extract function list
        print("Extracting function list...")
        functions = self.extract_function_list(soup)
        print(f"Found {len(functions)} functions")

        # Scrape details for each function
        docs = {
            'metadata': {
                'version': '1.0',
                'source': self.base_url,
                'scrapedDate': '2025-12-15',
                'totalFunctions': len(functions)
            },
            'functions': {}
        }

        count = 0
        for name, info in functions.items():
            if limit and count >= limit:
                break

            print(f"Processing {name} ({count + 1}/{len(functions)})...")
            detailed_info = self.scrape_function_details(info)
            docs['functions'][detailed_info['name']] = detailed_info
            count += 1

        return docs


def main():
    """Run the enhanced scraper."""
    import sys

    # Check for limit argument
    limit = None
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
            print(f"Limiting to {limit} functions for testing")
        except ValueError:
            print("Usage: python3 scrape_appian_docs_enhanced.py [limit]")
            sys.exit(1)

    scraper = EnhancedAppianDocScraper()
    docs = scraper.run(limit=limit)

    if docs and docs.get('functions'):
        # Save to JSON file
        output_file = "appian-functions-docs.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Generated documentation for {len(docs['functions'])} functions")
        print(f"✓ Saved to: {output_file}")

        # Print sample
        sample_func = list(docs['functions'].values())[0]
        print(f"\nSample function: {sample_func['name']}")
        print(f"  Description: {sample_func['description'][:100]}...")
        print(f"  Category: {sample_func['category']}")
        print(f"  Examples: {len(sample_func['examples'])} found")
    else:
        print("No documentation generated")


if __name__ == "__main__":
    main()
