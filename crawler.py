#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Multi-Source Crawler
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import hashlib
from typing import List, Dict, Optional
import json
import os
from config import SOURCES


class WebCrawler:
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'AlternativeLifestyleAI/1.0'})
        self.visited = set()
        self.domain = urlparse(config['url']).netloc
    
    def is_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.netloc != self.domain:
            return False
        for exclude in self.config.get('exclude', []):
            if exclude in url:
                return False
        if any(url.lower().endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.gif', '.svg']):
            return False
        return True
    
    def crawl_page(self, url: str) -> Optional[Dict]:
        if url in self.visited:
            return None
        self.visited.add(url)
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content_selector = self.config['selectors'].get('content', 'body')
            content_element = soup.select_one(content_selector)
            content = content_element.get_text(separator='\n', strip=True) if content_element else ""
            title_selector = self.config['selectors'].get('title', 'h1, title')
            title_element = soup.select_one(title_selector)
            title = title_element.get_text(strip=True) if title_element else url
            date_selector = self.config['selectors'].get('date')
            date = None
            if date_selector:
                date_element = soup.select_one(date_selector)
                if date_element:
                    date = date_element.get_text(strip=True)
            content = self.clean_content(content)
            if not content or len(content) < 50:
                return None
            return {
                'url': url,
                'title': title,
                'content': content,
                'date': date,
                'source': self.config.get('name', urlparse(url).netloc),
                'category': self.config.get('category', 'general'),
                'content_hash': hashlib.md5(content.encode()).hexdigest(),
                'last_resort_only': self.config.get('last_resort_only', False)
            }
        except Exception as e:
            return None
    
    def clean_content(self, text: str) -> str:
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
        boilerplate = ['Cookie Policy', 'Privacy Policy', 'Terms', 'All rights', 'Copyright',
                      'Subscribe', 'Share', 'Print', 'Email', 'Navigation', 'Footer']
        return '\n'.join(line for line in text.split('\n')                         if line.strip() and not any(bp.lower() in line.lower() for bp in boilerplate))
    
    def get_all_links(self, url: str) -> List[str]:
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                if parsed.netloc == self.domain:
                    links.add(full_url)
            return list(links)
        except Exception:
            return []
    
    def get_sitemap_urls(self) -> List[str]:
        sitemap_url = self.config.get('sitemap')
        if not sitemap_url:
            return []
        try:
            response = self.session.get(sitemap_url, timeout=10)
            soup = BeautifulSoup(response.text, 'xml')
            return [loc.text.strip() for loc in soup.find_all('loc') if self.is_allowed(loc.text.strip())]
        except Exception:
            return []
    
    def crawl_site(self, max_pages: int = 500) -> List[Dict]:
        documents = []
        urls_to_crawl = self.get_sitemap_urls()
        if not urls_to_crawl:
            urls_to_crawl = [self.config['url']]
        priority_pages = self.config.get('priority_pages', [])
        for url in priority_pages:
            if url not in urls_to_crawl:
                urls_to_crawl.insert(0, url)
        deep_crawl = self.config.get('deep_crawl', False)
        while urls_to_crawl and len(documents) < max_pages:
            url = urls_to_crawl.pop(0)
            if url in self.visited:
                continue
            doc = self.crawl_page(url)
            if doc:
                documents.append(doc)
            if deep_crawl:
                new_links = self.get_all_links(url)
                for link in new_links:
                    if link not in self.visited and link not in urls_to_crawl:
                        urls_to_crawl.append(link)
            time.sleep(self.config.get('rate_limit', 2))
        return documents
    
    def save_to_json(self, documents: List[Dict], filename: str):
        with open(filename, 'w') as f:
            json.dump(documents, f, indent=2)


def crawl_all_sources(max_pages: int = 500, output_dir: str = "data"):
    os.makedirs(output_dir, exist_ok=True)
    all_documents = []
    for source_name, source_config in SOURCES.items():
        print(f"Crawling {source_name}...")
        crawler = WebCrawler(source_config)
        documents = crawler.crawl_site(max_pages=max_pages)
        if documents:
            output_file = os.path.join(output_dir, f"{source_name}.json")
            crawler.save_to_json(documents, output_file)
            all_documents.extend(documents)
            print(f"  Saved {len(documents)} documents")
        time.sleep(5)
    print(f"Total documents crawled: {len(all_documents)}")
    return all_documents


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Crawl all data sources")
    parser.add_argument("--max-pages", type=int, default=500)
    parser.add_argument("--output", type=str, default="data")
    args = parser.parse_args()
    crawl_all_sources(max_pages=args.max_pages, output_dir=args.output)