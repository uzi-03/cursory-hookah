#!/usr/bin/env python3
"""
Test script to validate website URLs and check accessibility
"""

import requests
from urllib.parse import urlparse

def test_url(url, name):
    """Test if a URL is accessible"""
    print(f"\nTesting {name}: {url}")
    
    try:
        # Parse URL
        parsed = urlparse(url)
        print(f"  Parsed URL - Scheme: {parsed.scheme}, Netloc: {parsed.netloc}, Path: {parsed.path}")
        
        # Test request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ SUCCESS - URL is accessible")
            print(f"  Content Length: {len(response.content)} bytes")
        else:
            print(f"  ❌ FAILED - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ ERROR - {e}")

def main():
    """Test all configured website URLs"""
    websites = {
        'hookah-shisha': {
            'base_url': 'https://www.hookah-shisha.com',
            'search_url': 'https://www.hookah-shisha.com/c-1-hookahs.html',
            'hookah_url': 'https://www.hookah-shisha.com/c-1-hookahs.html',
            'bowl_url': 'https://www.hookah-shisha.com/c-2-bowls.html',
            'hose_url': 'https://www.hookah-shisha.com/c-3-hoses.html',
            'hmd_url': 'https://www.hookah-shisha.com/c-4-heat-management.html'
        },
        'juicyhookah': {
            'base_url': 'https://www.juicyhookah.com',
            'search_url': 'https://www.juicyhookah.com/hookahs/',
            'hookah_url': 'https://www.juicyhookah.com/hookahs/',
            'bowl_url': 'https://www.juicyhookah.com/bowls/',
            'hose_url': 'https://www.juicyhookah.com/hoses/',
            'hmd_url': 'https://www.juicyhookah.com/heat-management/'
        },
        '5starhookah': {
            'base_url': 'https://5starhookah.com',
            'search_url': 'https://5starhookah.com/hookahs/',
            'hookah_url': 'https://5starhookah.com/hookahs/',
            'bowl_url': 'https://5starhookah.com/bowls/',
            'hose_url': 'https://5starhookah.com/hoses/',
            'hmd_url': 'https://5starhookah.com/heat-management/'
        },
        'southsmoke': {
            'base_url': 'https://www.southsmoke.com',
            'search_url': 'https://www.southsmoke.com/hookahs',
            'hookah_url': 'https://www.southsmoke.com/hookahs',
            'bowl_url': 'https://www.southsmoke.com/bowls',
            'hose_url': 'https://www.southsmoke.com/hoses',
            'hmd_url': 'https://www.southsmoke.com/heat-management'
        },
        'sobehookah': {
            'base_url': 'https://www.sobehookah.com',
            'search_url': 'https://www.sobehookah.com/hookahs/',
            'hookah_url': 'https://www.sobehookah.com/hookahs/',
            'bowl_url': 'https://www.sobehookah.com/bowls/',
            'hose_url': 'https://www.sobehookah.com/hoses/',
            'hmd_url': 'https://www.sobehookah.com/heat-management/'
        }
    }
    
    print("🔍 Testing Website URLs")
    print("=" * 50)
    
    for website_name, urls in websites.items():
        print(f"\n📋 {website_name.upper()}")
        print("-" * 30)
        
        # Test base URL
        test_url(urls['base_url'], f"{website_name} base")
        
        # Test search URL
        test_url(urls['search_url'], f"{website_name} search")
        
        # Test category URLs
        for category in ['hookah', 'bowl', 'hose', 'hmd']:
            url_key = f'{category}_url'
            if url_key in urls:
                test_url(urls[url_key], f"{website_name} {category}")

if __name__ == '__main__':
    main() 