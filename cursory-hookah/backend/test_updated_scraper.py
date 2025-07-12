#!/usr/bin/env python3
"""
Test script to verify the updated scraper works with new 5starhookah.com URLs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.real_scrapers import RealHookahScraper
import time

def test_scraper():
    """Test the updated scraper with 5starhookah.com"""
    print("Testing Updated 5starhookah.com Scraper")
    print("=" * 50)
    
    scraper = RealHookahScraper()
    
    # Test categories
    categories_to_test = [
        'hookah',
        'bowl', 
        'tobacco',
        'coal',
        'accessory'
    ]
    
    total_products = 0
    
    for category in categories_to_test:
        print(f"\n--- Testing Category: {category.upper()} ---")
        
        try:
            # Test scraping for this category
            products = scraper.scrape_website('5starhookah', category=category, max_pages=1)
            
            print(f"Found {len(products)} products for {category}")
            
            if products:
                print("Sample products:")
                for i, product in enumerate(products[:3]):  # Show first 3 products
                    print(f"  {i+1}. {product['name']} - ${product['price']} - {product['category']}")
                    print(f"     Brand: {product['brand']}")
                    print(f"     URL: {product['product_url']}")
                    print(f"     Tags: {', '.join(product['compatibility_tags'])}")
                    print()
            
            total_products += len(products)
            
        except Exception as e:
            print(f"Error testing {category}: {e}")
        
        # Be respectful with delays
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print(f"TOTAL PRODUCTS FOUND: {total_products}")
    print("=" * 50)
    
    return total_products > 0

def test_category_urls():
    """Test that category URLs are correctly mapped"""
    print("\nTesting Category URL Mapping")
    print("-" * 30)
    
    scraper = RealHookahScraper()
    
    categories = ['hookah', 'bowl', 'tobacco', 'coal', 'accessory']
    
    for category in categories:
        url = scraper._get_category_url('5starhookah', category)
        print(f"{category:12} -> {url}")
    
    print("-" * 30)

if __name__ == "__main__":
    print("5starhookah.com Scraper Test")
    print("=" * 50)
    
    # Test category URL mapping
    test_category_urls()
    
    # Test actual scraping
    success = test_scraper()
    
    if success:
        print("\n✅ SUCCESS: Scraper is working with updated URLs!")
    else:
        print("\n❌ FAILURE: Scraper encountered issues")
    
    print("\nTest completed!") 