#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Image Handler
"""

import os
import hashlib
from PIL import Image
from typing import Tuple, Optional, Dict, List
import requests
from pathlib import Path
from config import IMAGE_CONFIG


class ImageHandler:
    def __init__(self, config: Dict = None):
        self.config = config or IMAGE_CONFIG
        self.storage_path = Path(self.config.get('storage_path', './images'))
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.thumbnail_size = tuple(self.config.get('thumbnail_size', [300, 300]))
        self.max_image_size = tuple(self.config.get('max_image_size', [2000, 2000]))
        self.allowed_extensions = set(self.config.get('allowed_extensions', ['.jpg', '.jpeg', '.png', '.gif', '.webp']))
        self.max_file_size = self.config.get('max_file_size', 10485760)
        self.organize_by_category = self.config.get('organize_by_category', True)
        self.create_thumbnails = self.config.get('create_thumbnails', True)
    
    def get_image_path(self, image_url: str, category: str = None) -> Tuple[Path, Path]:
        url_hash = hashlib.md5(image_url.encode()).hexdigest()
        extension = self._get_extension(image_url)
        if self.organize_by_category and category:
            category_dir = self.storage_path / category.replace(' ', '_').lower()
            category_dir.mkdir(parents=True, exist_ok=True)
            base_path = category_dir
        else:
            base_path = self.storage_path
        image_path = base_path / f"{url_hash}{extension}"
        thumbnail_path = base_path / f"{url_hash}_thumb.jpg"
        return image_path, thumbnail_path
    
    def _get_extension(self, url: str) -> str:
        parsed = url.lower()
        for ext in self.allowed_extensions:
            if parsed.endswith(ext):
                return ext
        return '.jpg'
    
    def download_image(self, image_url: str, category: str = None) -> Optional[Dict]:
        try:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
            if len(response.content) > self.max_file_size:
                return None
            image_path, thumbnail_path = self.get_image_path(image_url, category)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            if self.create_thumbnails:
                try:
                    self._create_thumbnail(image_path, thumbnail_path)
                except Exception:
                    # Continue even if thumbnail creation fails
                    pass
            return {
                'url': image_url,
                'local_path': str(image_path),
                'thumbnail_path': str(thumbnail_path) if self.create_thumbnails else None,
                'category': category,
                'size': len(response.content),
                'hash': hashlib.md5(response.content).hexdigest()
            }
        except requests.exceptions.RequestException:
            return None
        except (OSError, IOError):
            return None
    
    def _create_thumbnail(self, image_path: Path, thumbnail_path: Path):
        try:
            with Image.open(image_path) as img:
                img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
                img.save(thumbnail_path, 'JPEG', quality=85)
        except (OSError, IOError):
            # Ignore thumbnail creation errors
            pass
    
    def _extract_metadata(self, image_path: Path, image_info: Dict):
        try:
            with Image.open(image_path) as img:
                image_info['width'] = img.width
                image_info['height'] = img.height
                image_info['format'] = img.format
                image_info['mode'] = img.mode
        except (OSError, IOError):
            # Ignore metadata extraction errors
            pass
    
    def get_image_info(self, image_path: Path) -> Optional[Dict]:
        if not image_path.exists():
            return None
        try:
            with Image.open(image_path) as img:
                return {
                    'path': str(image_path),
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'size': image_path.stat().st_size
                }
        except (OSError, IOError):
            return None
    
    def list_images_by_category(self, category: str = None) -> List[Dict]:
        images = []
        search_path = self.storage_path / category if category else self.storage_path
        if search_path.exists():
            for img_file in search_path.glob('*'):
                if img_file.suffix.lower() in self.allowed_extensions:
                    info = self.get_image_info(img_file)
                    if info:
                        info['category'] = category
                        images.append(info)
        return images