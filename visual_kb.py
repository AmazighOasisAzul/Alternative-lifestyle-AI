#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Visual Knowledge Base
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
from config import VISUAL_KB_CONFIG


class VisualKnowledgeBase:
    def __init__(self, config: Dict = None):
        self.config = config or VISUAL_KB_CONFIG
        self.index_path = Path(self.config.get('index_path', './visual_kb'))
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.image_index_file = self.index_path / 'image_index.json'
        self.image_index = self._load_index()
    
    def _load_index(self) -> Dict:
        if self.image_index_file.exists():
            try:
                with open(self.image_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                # Corrupt or unreadable index - start fresh
                return {'images': [], 'categories': {}, 'sources': {}}
        return {'images': [], 'categories': {}, 'sources': {}}
    
    def _save_index(self):
        try:
            with open(self.image_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.image_index, f, indent=2)
        except OSError:
            # Could not write index; ignore but don't crash
            pass
    
    def add_image(self, image_info: Dict) -> str:
        image_id = hashlib.md5(image_info['url'].encode()).hexdigest()
        for img in self.image_index['images']:
            if img['id'] == image_id:
                return image_id
        image_entry = {
            'id': image_id,
            'url': image_info['url'],
            'local_path': image_info.get('local_path'),
            'thumbnail_path': image_info.get('thumbnail_path'),
            'category': image_info.get('category', 'general'),
            'source': image_info.get('source', 'unknown'),
            'width': image_info.get('width'),
            'height': image_info.get('height'),
            'size': image_info.get('size'),
            'metadata': image_info.get('metadata', {}),
            'tags': image_info.get('tags', [])
        }
        self.image_index['images'].append(image_entry)
        if image_entry['category'] not in self.image_index['categories']:
            self.image_index['categories'][image_entry['category']] = []
        self.image_index['categories'][image_entry['category']].append(image_id)
        if image_entry['source'] not in self.image_index['sources']:
            self.image_index['sources'][image_entry['source']] = []
        self.image_index['sources'][image_entry['source']].append(image_id)
        self._save_index()
        return image_id
    
    def get_image(self, image_id: str) -> Optional[Dict]:
        for img in self.image_index['images']:
            if img['id'] == image_id:
                return img
        return None
    
    def get_image_by_url(self, url: str) -> Optional[Dict]:
        return self.get_image(hashlib.md5(url.encode()).hexdigest())
    
    def get_images_by_category(self, category: str) -> List[Dict]:
        ids = self.image_index['categories'].get(category, [])
        return [img for img in self.image_index['images'] if img['id'] in ids]
    
    def get_images_by_source(self, source: str) -> List[Dict]:
        ids = self.image_index['sources'].get(source, [])
        return [img for img in self.image_index['images'] if img['id'] in ids]
    
    def search_images(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        results = []
        ql = query.lower()
        for img in self.image_index['images']:
            if category and img.get('category') != category:
                continue
            if (ql in img.get('url', '').lower() or
                ql in img.get('source', '').lower() or
                any(ql in t.lower() for t in img.get('tags', []))):
                results.append(img)
                if len(results) >= limit:
                    break
        return results
    
    def get_statistics(self) -> Dict:
        return {
            'total_images': len(self.image_index['images']),
            'categories': {k: len(v) for k, v in self.image_index['categories'].items()},
            'sources': {k: len(v) for k, v in self.image_index['sources'].items()}
        }