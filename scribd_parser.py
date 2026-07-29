#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import time
import json
from pathlib import Path
from config import SCRIBD_DOCUMENTS, IMAGE_CONFIG
from image_handler import ImageHandler


class ScribdParser:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.image_handler = ImageHandler(self.config.get('image_config', IMAGE_CONFIG))
    
    def extract_document_id(self, url: str) -> Optional[str]:
        patterns = [
            r'scribd\.com/doc(?:ument)?/(\d+)',
            r'scribd\.com/(\w+)/d/(\d+)',
            r'scribd\.com/\w+\?doc_id=(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1) if match.group(1) else match.group(2)
        return None
    
    def parse_document(self, url: str, category: str = None) -> Optional[Dict]:
        doc_id = self.extract_document_id(url)
        if not doc_id:
            return None
        try:
            result = {
                'url': url, 'doc_id': doc_id, 'title': '',
                'content': '', 'images': [], 'pages': 0,
                'category': category or 'general'
            }
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            title_element = soup.find('title')
            if title_element:
                result['title'] = title_element.get_text(strip=True).replace(' | Scribd', '')
            script_tag = soup.find('script', {'type': 'application/ld+json'})
            if script_tag:
                json_data = json.loads(script_tag.string)
                result['title'] = json_data.get('name', result['title'])
                result['pages'] = json_data.get('numberOfPages', 0)
            content_div = soup.find('div', {'class': re.compile(r'Document')})
            if content_div:
                result['content'] = self._clean_text(content_div.get_text(separator='\n'))
            for img in soup.find_all('img', src=True):
                src = img['src']
                if 'scribdassets.com' in src or 'scribd.com' in src:
                    result['images'].append(src)
            return result
        except Exception as e:
            return None
    
    def _clean_text(self, text: str) -> str:
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def download_document_images(self, document: Dict) -> List[Dict]:
        downloaded = []
        for image_url in document.get('images', []):
            image_info = self.image_handler.download_image(image_url, document.get('category'))
            if image_info:
                downloaded.append(image_info)
            time.sleep(0.5)
        return downloaded
    
    def parse_multiple_documents(self, document_urls: List[str]) -> List[Dict]:
        results = []
        for url in document_urls:
            document = self.parse_document(url)
            if document:
                results.append(document)
            time.sleep(2)
        return results


if __name__ == "__main__":
    parser = ScribdParser()
    documents = parser.parse_multiple_documents([doc['url'] for doc in SCRIBD_DOCUMENTS])
    print(f"Parsed {len(documents)} documents")