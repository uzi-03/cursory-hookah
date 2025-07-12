#!/usr/bin/env python3
"""
Investigate actual working URLs for hookah websites
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def investigate_website(base_url, website_name):
    """Investigate a website to find working category URLs"""
    print(f"\n🔍 Investigating {website_name}: {base_url}")
    print("-" * 50)
    
    try:
        # Get the homepage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(base_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to access homepage: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for navigation links
        nav_links = []
        
        # Common selectors for navigation
        nav_selectors = [
            'nav a', '.navigation a', '.menu a', '.nav a', 
            'header a', '.header a', '#navigation a', '#nav a',
            '.main-menu a', '.primary-menu a', '.top-menu a'
        ]
        
        for selector in nav_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                text = link.get_text(strip=True).lower()
                if href and isinstance(href, str) and any(keyword in text for keyword in ['hookah', 'bowl', 'hose', 'heat', 'accessory']):
                    full_url = urljoin(base_url, href)
                    nav_links.append((text, full_url))
        
        # Look for category links in content
        content_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True).lower()
            if any(keyword in text for keyword in ['hookah', 'bowl', 'hose', 'heat', 'accessory']):
                full_url = urljoin(base_url, href)
                content_links.append((text, full_url))
        
        # Test common URL patterns
        test_patterns = [
            '/hookahs', '/hookah', '/bowls', '/bowl', '/hoses', '/hose',
            '/heat-management', '/heat-management-devices', '/accessories',
            '/category/hookahs', '/category/bowls', '/category/hoses',
            '/products/hookahs', '/products/bowls', '/products/hoses',
            '/shop/hookahs', '/shop/bowls', '/shop/hoses'
        ]
        
        working_urls = []
        for pattern in test_patterns:
            test_url = urljoin(base_url, pattern)
            try:
                test_response = requests.get(test_url, headers=headers, timeout=5)
                if test_response.status_code == 200:
                    working_urls.append((pattern, test_url))
                    print(f"✅ Working: {test_url}")
                else:
                    print(f"❌ Failed ({test_response.status_code}): {test_url}")
            except Exception as e:
                print(f"❌ Error: {test_url} - {e}")
        
        # Print findings
        print(f"\n📋 Findings for {website_name}:")
        if nav_links:
            print("Navigation links found:")
            for text, url in nav_links[:5]:  # Limit to first 5
                print(f"  - {text}: {url}")
        
        if working_urls:
            print("Working category URLs:")
            for pattern, url in working_urls:
                print(f"  - {pattern}: {url}")
        else:
            print("❌ No working category URLs found")
            
    except Exception as e:
        print(f"❌ Error investigating {website_name}: {e}")

def main():
    """Investigate all websites"""
    websites = [
        ('https://www.hookah-shisha.com', 'Hookah-Shisha'),
        ('https://5starhookah.com', '5StarHookah'),
        ('https://www.juicyhookah.com', 'JuicyHookah'),
        ('https://www.sobehookah.com', 'SobeHookah')
    ]
    
    print("🔍 Investigating Hookah Website URLs")
    print("=" * 60)
    
    for base_url, name in websites:
        investigate_website(base_url, name)
        print("\n" + "="*60)

if __name__ == '__main__':
    main() 