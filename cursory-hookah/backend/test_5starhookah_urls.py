#!/usr/bin/env python3
"""
Test script to verify 5starhookah.com URLs work correctly
"""

import requests
from bs4 import BeautifulSoup
import time
import random

def test_url(url, description):
    """Test if a URL is accessible"""
    print(f"\n=== Testing {description} ===")
    print(f"URL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for product elements
            product_selectors = [
                '.product-item',
                '.product', 
                '.grid-product',
                '.product-card',
                '.collection-product'
            ]
            
            products_found = 0
            for selector in product_selectors:
                products = soup.select(selector)
                if products:
                    print(f"Found {len(products)} products with selector '{selector}'")
                    products_found += len(products)
            
            if products_found == 0:
                print("No products found with common selectors")
                # Try to find any product-related elements
                all_links = soup.find_all('a', href=True)
                product_links = [link for link in all_links if '/products/' in link['href']]
                print(f"Found {len(product_links)} product links")
                
                if product_links:
                    print("Sample product links:")
                    for link in product_links[:5]:
                        print(f"  - {link['href']}")
            
            return True
        else:
            print(f"Error: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Test all 5starhookah.com URLs"""
    urls_to_test = [
        ('https://5starhookah.com/collections/all-hookahs', 'All Hookahs'),
        ('https://5starhookah.com/collections/all-shisha', 'All Shisha'),
        ('https://5starhookah.com/collections/all-charcoals', 'All Charcoals'),
        ('https://5starhookah.com/collections/all-accessories', 'All Accessories'),
        ('https://5starhookah.com/collections/all-hookah-bowls', 'All Hookah Bowls')
    ]
    
    print("Testing 5starhookah.com URLs...")
    print("=" * 50)
    
    working_urls = []
    failed_urls = []
    
    for url, description in urls_to_test:
        if test_url(url, description):
            working_urls.append((url, description))
        else:
            failed_urls.append((url, description))
        
        # Be respectful with delays
        time.sleep(random.uniform(1, 2))
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Working URLs: {len(working_urls)}")
    print(f"Failed URLs: {len(failed_urls)}")
    
    if working_urls:
        print("\nWorking URLs:")
        for url, desc in working_urls:
            print(f"  ✓ {desc}: {url}")
    
    if failed_urls:
        print("\nFailed URLs:")
        for url, desc in failed_urls:
            print(f"  ✗ {desc}: {url}")

if __name__ == "__main__":
    main() 