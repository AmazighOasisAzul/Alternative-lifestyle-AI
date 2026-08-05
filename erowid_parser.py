"""
Erowid Parser for Alternative Lifestyle AI

Dedicated parser for Erowid substance pages and experience reports (vault).
Extracts: substance info, experience reports, effects, dosage, duration.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass
import re
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ErowidSubstance:
    """Represents a substance page from Erowid."""
    name: str
    url: str
    summary: Optional[str]
    effects: List[str]
    dosage: Optional[str]
    duration: Optional[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for indexing."""
        return {
            'source': 'erowid',
            'category': 'Pharmacology',
            'type': 'substance',
            'title': self.name,
            'content': self.summary or '',
            'url': self.url,
            'effects': ', '.join(self.effects) if self.effects else '',
            'dosage': self.dosage or '',
            'duration': self.duration or '',
            'warnings': ' | '.join(self.warnings) if self.warnings else ''
        }


@dataclass
class ErowidExperience:
    """Represents an experience report from Erowid Vault."""
    title: str
    url: str
    substance: str
    author: Optional[str]
    date: Optional[str]
    rating: Optional[str]
    report: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for indexing."""
        return {
            'source': 'erowid',
            'category': 'Pharmacology',
            'type': 'experience_report',
            'title': self.title,
            'content': self.report,
            'url': self.url,
            'substance': self.substance,
            'author': self.author or '',
            'date': self.date or '',
            'rating': self.rating or ''
        }


class ErowidParser:
    """Parser for Erowid substance pages and experience reports."""
    
    BASE_URL = "https://erowid.org"
    SUBSTANCE_BASE = BASE_URL + "/pharmaceuticals/"
    VAULT_BASE = BASE_URL + "/experiences/"
    
    # User agent for requests
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AlternativeLifestyleAI/1.0"
    
    # Rate limiting
    REQUEST_DELAY = 2.0  # 2 seconds between requests
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
    
    def _get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page with retry and delay."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(self.REQUEST_DELAY)
            return BeautifulSoup(response.content, 'lxml')
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def parse_substance_page(self, substance_name: str) -> Optional[ErowidSubstance]:
        """
        Parse a substance page from Erowid.
        
        Args:
            substance_name: Name of the substance (e.g., 'mdma', 'cannabis')
            
        Returns:
            ErowidSubstance object or None
        """
        url = f"{self.SUBSTANCE_BASE}{substance_name}/{substance_name}.shtml"
        soup = self._get_page(url)
        
        if not soup:
            return None
        
        # Extract name
        name = substance_name.upper()
        
        # Extract summary (first paragraph or description)
        summary = None
        main_content = soup.find('div', {'id': 'maincol'})
        if main_content:
            first_p = main_content.find('p')
            if first_p:
                summary = first_p.get_text().strip()
        
        # Extract effects
        effects = []
        effects_section = soup.find('h2', string=lambda t: t and 'EFFECTS' in t.upper())
        if effects_section:
            next_node = effects_section.find_next_sibling()
            if next_node and next_node.name == 'ul':
                effects = [li.get_text().strip() for li in next_node.find_all('li')]
        
        # Extract dosage
        dosage = None
        dosage_section = soup.find('h2', string=lambda t: t and 'DOSAGE' in t.upper())
        if dosage_section:
            next_node = dosage_section.find_next_sibling()
            if next_node:
                dosage = next_node.get_text().strip()
        
        # Extract duration
        duration = None
        duration_section = soup.find('h2', string=lambda t: t and 'DURATION' in t.upper())
        if duration_section:
            next_node = duration_section.find_next_sibling()
            if next_node:
                duration = next_node.get_text().strip()
        
        # Extract warnings
        warnings = []
        warnings_section = soup.find('h2', string=lambda t: t and ('WARNING' in t.upper() or 'CAUTION' in t.upper()))
        if warnings_section:
            next_node = warnings_section.find_next_sibling()
            if next_node and next_node.name == 'ul':
                warnings = [li.get_text().strip() for li in next_node.find_all('li')]
            elif next_node:
                warnings = [next_node.get_text().strip()]
        
        return ErowidSubstance(
            name=name,
            url=url,
            summary=summary,
            effects=effects,
            dosage=dosage,
            duration=duration,
            warnings=warnings
        )
    
    def parse_experience_report(self, exp_id: str) -> Optional[ErowidExperience]:
        """
        Parse an experience report from Erowid Vault.
        
        Args:
            exp_id: Experience ID (e.g., 'exp12345')
            
        Returns:
            ErowidExperience object or None
        """
        url = f"{self.VAULT_BASE}{exp_id}.html"
        soup = self._get_page(url)
        
        if not soup:
            return None
        
        # Extract title
        title_elem = soup.find('title')
        title = title_elem.get_text().replace(' : Erowid Experience Vault', '').strip() if title_elem else "Untitled"
        
        # Extract substance
        substance = None
        substance_elem = soup.find('a', href=lambda h: h and '/pharmaceuticals/' in h)
        if substance_elem:
            substance = substance_elem.get_text().strip().upper()
        
        # Extract author
        author = None
        author_elem = soup.find('span', class_='author')
        if author_elem:
            author = author_elem.get_text().strip()
        
        # Extract date
        date = None
        date_elem = soup.find('span', class_='date')
        if date_elem:
            date = date_elem.get_text().strip()
        
        # Extract rating
        rating = None
        rating_elem = soup.find('span', class_='rating')
        if rating_elem:
            rating = rating_elem.get_text().strip()
        
        # Extract report body
        report = ""
        report_div = soup.find('div', class_='report')
        if report_div:
            # Remove unwanted elements
            for elem in report_div.find_all(['script', 'style', 'iframe']):
                elem.decompose()
            report = report_div.get_text().strip()
            # Clean up whitespace
            report = re.sub(r's+', ' ', report)
        
        if not report:
            return None
        
        return ErowidExperience(
            title=title,
            url=url,
            substance=substance or '',
            author=author,
            date=date,
            rating=rating,
            report=report
        )
    
    def parse_all_substances(self, substance_list: List[str]) -> List[Dict]:
        """
        Parse multiple substance pages.
        
        Args:
            substance_list: List of substance names
            
        Returns:
            List of substance dictionaries
        """
        results = []
        for substance in substance_list:
            parsed = self.parse_substance_page(substance)
            if parsed:
                results.append(parsed.to_dict())
            time.sleep(0.5)  # Additional delay between substances
        return results
    
    def parse_experience_ids(self, exp_ids: List[str]) -> List[Dict]:
        """
        Parse multiple experience reports.
        
        Args:
            exp_ids: List of experience IDs
            
        Returns:
            List of experience dictionaries
        """
        results = []
        for exp_id in exp_ids:
            parsed = self.parse_experience_report(exp_id)
            if parsed:
                results.append(parsed.to_dict())
            time.sleep(0.5)  # Additional delay between experiences
        return results


def main():
    """CLI entry point for Erowid parser."""
    import argparse
    import sys
    import json
    
    parser = argparse.ArgumentParser(description='Erowid Parser')
    parser.add_argument('--substance', type=str, help='Parse a substance page')
    parser.add_argument('--experience', type=str, help='Parse an experience report')
    parser.add_argument('--substances', nargs='+', help='Parse multiple substance pages')
    parser.add_argument('--experiences', nargs='+', help='Parse multiple experience reports')
    parser.add_argument('--output', type=str, help='Output file (JSON)')
    args = parser.parse_args()
    
    parser_obj = ErowidParser()
    results = []
    
    if args.substance:
        result = parser_obj.parse_substance_page(args.substance)
        if result:
            results.append(result.to_dict())
    
    if args.experience:
        result = parser_obj.parse_experience_report(args.experience)
        if result:
            results.append(result.to_dict())
    
    if args.substances:
        results.extend(parser_obj.parse_all_substances(args.substances))
    
    if args.experiences:
        results.extend(parser_obj.parse_experience_ids(args.experiences))
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Saved {len(results)} items to {args.output}")
    else:
        for result in results:
            print(json.dumps(result, indent=2))
    
    return results


if __name__ == '__main__':
    main()