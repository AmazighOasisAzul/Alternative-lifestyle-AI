#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import json
from pathlib import Path
from config import SOCIAL_MEDIA_SOURCES, IMAGE_CONFIG
from image_handler import ImageHandler


class InstagramScraper:
    def __init__(self, accounts: List[str], config: Dict = None):
        self.accounts = accounts
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.image_handler = ImageHandler(self.config.get('image_config', IMAGE_CONFIG))
    
    def scrape_profile(self, username: str) -> Optional[Dict]:
        url = f"https://www.instagram.com/{username}/"
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return None
            soup = BeautifulSoup(response.text, 'html.parser')
            profile_data = {
                'username': username, 'url': url, 'bio': '',
                'followers': 0, 'following': 0, 'posts': 0,
                'images': [], 'videos': []
            }
            script_tag = soup.find('script', {'type': 'application/ld+json'})
            if script_tag:
                json_data = json.loads(script_tag.string)
                profile_data['bio'] = json_data.get('description', '')
            for img in soup.find_all('img', src=True):
                src = img['src']
                if 'cdninstagram.com' in src:
                    profile_data['images'].append(src)
            return profile_data
        except Exception as e:
            return None
    
    def scrape_all_profiles(self) -> List[Dict]:
        all_profiles = []
        for account in self.accounts:
            profile = self.scrape_profile(account)
            if profile:
                all_profiles.append(profile)
            time.sleep(2)
        return all_profiles


class TwitterScraper:
    def __init__(self, accounts: List[str], config: Dict = None):
        self.accounts = accounts
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.image_handler = ImageHandler(self.config.get('image_config', IMAGE_CONFIG))
    
    def scrape_profile(self, username: str) -> Optional[Dict]:
        url = f"https://twitter.com/{username}"
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return None
            soup = BeautifulSoup(response.text, 'html.parser')
            profile_data = {
                'username': username, 'url': url, 'bio': '',
                'followers': 0, 'following': 0, 'tweets': 0,
                'images': [], 'videos': []
            }
            bio_element = soup.find('div', {'data-testid': 'UserDescription'})
            if bio_element:
                profile_data['bio'] = bio_element.get_text(strip=True)
            for img in soup.find_all('img', src=True):
                src = img['src']
                if 'twimg.com' in src:
                    profile_data['images'].append(src)
            return profile_data
        except Exception as e:
            return None
    
    def scrape_all_profiles(self) -> List[Dict]:
        all_profiles = []
        for account in self.accounts:
            profile = self.scrape_profile(account)
            if profile:
                all_profiles.append(profile)
            time.sleep(2)
        return all_profiles


class SocialMediaScraper:
    def __init__(self, config: Dict = None):
        self.config = config or SOCIAL_MEDIA_SOURCES
        self.instagram_scraper = InstagramScraper(
            self.config.get('instagram', {}).get('accounts', []),
            self.config
        )
        self.twitter_scraper = TwitterScraper(
            self.config.get('twitter', {}).get('accounts', []),
            self.config
        )
    
    def scrape_all(self) -> Dict:
        return {
            'instagram': self.instagram_scraper.scrape_all_profiles(),
            'twitter': self.twitter_scraper.scrape_all_profiles()
        }