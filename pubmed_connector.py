"""
PubMed Connector for Alternative Lifestyle AI

Fetches scientific papers from NCBI PubMed using E-utilities API.
Stores: DOI, title, abstract, year, authors, key findings.
"""

import requests
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PubMedPaper:
    """Represents a PubMed paper with extracted metadata."""
    doi: Optional[str]
    title: str
    abstract: Optional[str]
    year: Optional[str]
    authors: List[str]
    journal: Optional[str]
    pmid: str
    key_findings: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for indexing."""
        return {
            'source': 'pubmed',
            'category': 'Research',
            'type': 'scientific_paper',
            'doi': self.doi or '',
            'title': self.title,
            'content': self.abstract or '',
            'year': self.year or '',
            'authors': ', '.join(self.authors) if self.authors else '',
            'journal': self.journal or '',
            'pmid': self.pmid,
            'key_findings': self.key_findings or '',
            'url': f'https://pubmed.ncbi.nlm.nih.gov/{self.pmid}/'
        }


class PubMedConnector:
    """Connects to NCBI E-utilities API for PubMed data."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    ESEARCH_URL = BASE_URL + "esearch.fcgi"
    EFETCH_URL = BASE_URL + "efetch.fcgi"
    
    # Rate limiting: NCBI allows 3 requests per second for unauthenticated
    # 10 requests per second for authenticated (with email)
    REQUEST_DELAY = 0.35  # ~3 requests per second
    
    def __init__(self, email: str):
        """
        Initialize PubMed connector.
        
        Args:
            email: Email address for NCBI (required by their ToS)
        """
        self.email = email
        self.session = requests.Session()
        self.session.params.update({
            'tool': 'AlternativeLifestyleAI',
            'email': self.email
        })
    
    def search(self, query: str, max_results: int = 10) -> List[str]:
        """
        Search PubMed for papers matching query.
        
        Args:
            query: Search query string
            max_results: Maximum number of PMIDs to return
            
        Returns:
            List of PMIDs (PubMed IDs)
        """
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json',
            'retmax': min(max_results, 100),
            'sort': 'relevance'
        }
        
        try:
            response = self.session.get(self.ESEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            pmids = data.get('esearchresult', {}).get('idlist', [])
            return pmids[:max_results]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Search failed for query '{query}': {e}")
            return []
        
        finally:
            time.sleep(self.REQUEST_DELAY)
    
    def fetch_paper_details(self, pmid: str) -> Optional[PubMedPaper]:
        """
        Fetch full details for a single paper by PMID.
        
        Args:
            pmid: PubMed ID
            
        Returns:
            PubMedPaper object or None if fetch fails
        """
        params = {
            'db': 'pubmed',
            'id': pmid,
            'retmode': 'xml',
            'rettype': 'abstract'
        }
        
        try:
            response = self.session.get(self.EFETCH_URL, params=params)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            # Extract metadata
            article = root.find('.//PubmedArticle')
            if article is None:
                return None
            
            # Title
            title_elem = article.find('.//ArticleTitle')
            title = title_elem.text.strip() if title_elem is not None else "No title"
            
            # Abstract
            abstract_elem = article.find('.//AbstractText')
            abstract = ' '.join([elem.text.strip() for elem in abstract_elem]) if abstract_elem is not None else None
            
            # PMID
            pmid_elem = article.find('.//PMID')
            pmid = pmid_elem.text.strip() if pmid_elem is not None else pmid
            
            # DOI
            doi_elem = article.find('.//ELocationID[@EIdType="doi"]')
            doi = doi_elem.text.strip() if doi_elem is not None else None
            
            # Year
            year_elem = article.find('.//PubDate/Year')
            year = year_elem.text.strip() if year_elem is not None else None
            
            # Journal
            journal_elem = article.find('.//Title[parent::Journal]')
            journal = journal_elem.text.strip() if journal_elem is not None else None
            
            # Authors
            authors = []
            for author in article.findall('.//Author'):
                last_name = author.find('.//LastName')
                first_name = author.find('.//ForeName')
                if last_name is not None:
                    name = last_name.text.strip()
                    if first_name is not None:
                        name = f"{first_name.text.strip()} {name}"
                    authors.append(name)
            
            # Key findings extraction (simple: first sentence of abstract)
            key_findings = None
            if abstract:
                sentences = abstract.split('.')
                if sentences:
                    key_findings = sentences[0].strip() + '.'
            
            return PubMedPaper(
                doi=doi,
                title=title,
                abstract=abstract,
                year=year,
                authors=authors,
                journal=journal,
                pmid=pmid,
                key_findings=key_findings
            )
            
        except (requests.exceptions.RequestException, ET.ParseError) as e:
            logger.error(f"Fetch failed for PMID {pmid}: {e}")
            return None
        
        finally:
            time.sleep(self.REQUEST_DELAY)
    
    def fetch_papers(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search and fetch papers, returning list of indexed documents.
        
        Args:
            query: Search query
            max_results: Maximum number of papers to fetch
            
        Returns:
            List of document dictionaries ready for indexing
        """
        pmids = self.search(query, max_results)
        papers = []
        
        for pmid in pmids:
            paper = self.fetch_paper_details(pmid)
            if paper:
                papers.append(paper.to_dict())
        
        return papers


def main():
    """CLI entry point for PubMed connector."""
    import argparse
    import sys
    import os
    
    # Load config
    try:
        from config import SCIENTIFIC_CONNECTORS
        email = SCIENTIFIC_CONNECTORS.get('pubmed', {}).get('email')
        if not email:
            print("ERROR: PubMed email not configured in config.py")
            sys.exit(1)
    except ImportError:
        print("ERROR: config.py not found")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='PubMed Connector')
    parser.add_argument('--query', type=str, required=True, help='Search query')
    parser.add_argument('--max', type=int, default=10, help='Maximum results')
    parser.add_argument('--output', type=str, help='Output file (JSON)')
    args = parser.parse_args()
    
    connector = PubMedConnector(email)
    papers = connector.fetch_papers(args.query, args.max)
    
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(papers, f, indent=2)
        print(f"Saved {len(papers)} papers to {args.output}")
    else:
        for paper in papers:
            print(f"Title: {paper['title']}")
            print(f"PMID: {paper['pmid']}")
            print(f"Year: {paper['year']}")
            print(f"Abstract: {paper['content'][:200]}...")
            print()
    
    return papers


if __name__ == '__main__':
    main()